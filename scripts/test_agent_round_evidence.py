"""Regression coverage for round wake retries and the canonical section chain."""

from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from io import StringIO
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import agent_wake_verification as reader
from capture_round_evidence import capture
import blueberry_phase1_guard as phase1
from round_source_checks import FUNNEL_FEEDS, audit_source, liquidation_pace
from verify_round_evidence import FUNNELS, verify


class RoundEvidenceTest(unittest.TestCase):
    def setUp(self):
        tmp = self.enterContext(tempfile.TemporaryDirectory())
        self.root = Path(tmp)
        desk = self.root / "desk"
        desk.mkdir()
        self.spec_path = desk / reader.SPEC.name
        for name in (reader.SPEC.name, *reader.COMPANIONS.values()):
            shutil.copyfile(reader.SPEC.parent / name, desk / name)
        self.enterContext(patch.multiple(reader, ROOT=self.root, SPEC=self.spec_path))
        self.probe = self.enterContext(patch.object(reader, "bootstrap", return_value={
            "state": "REPORTED",
            "report": {"spec": {}, "terminal_engine": {}, "mt5_status": {}},
        }))
        self.directory = self.root / "data" / "round-evidence" / "R1"
        self.spec = reader.load_round_spec(self.spec_path)

    def invoke(self, *args):
        stream = StringIO()
        with redirect_stdout(stream):
            exit_code = reader.main(["--round", "R1", *args])
        contents = stream.getvalue()
        receipt = json.loads(contents.splitlines()[-1].removeprefix("WAKE_RECEIPT "))
        return exit_code, receipt, contents

    def test_wake_retry_preserves_original_bytes(self):
        code, original, _ = self.invoke("--save")
        self.assertEqual(code, 0)
        raw = (self.directory / "wake_receipt.json").read_bytes()
        code, retry, _ = self.invoke()
        self.assertEqual(code, 0)
        self.assertEqual(original, retry)
        self.assertEqual(raw, (self.directory / "wake_receipt.json").read_bytes())
        self.probe.assert_called_once()

    def test_reader_blocks_skips_and_companion_changes(self):
        self.invoke()
        code, payload, _ = self.invoke("--step", "1")
        self.assertEqual(code, 1)
        self.assertIn("Step 0 still needs", payload["error"])
        code, payload, text = self.invoke("--step", "0")
        self.assertEqual(code, 0)
        self.assertIn("--- SOP SECTION launch-prompt ---", text)
        self.assertEqual(payload["remaining_anchors"], ["sec-0", "sec-1"])
        (self.spec_path.parent / reader.COMPANIONS["evidence-contract"]).write_text("changed", encoding="utf-8")
        code, payload, _ = self.invoke("--step", "0")
        self.assertEqual(code, 1)
        self.assertIn("use a new round ID", payload["error"])

    def test_complete_chain_and_reject_copied_receipt(self):
        self.invoke()
        for step, anchors in self.spec["stages"].items():
            for anchor in anchors:
                code, receipt, text = self.invoke("--step", str(step))
                self.assertEqual(code, 0, receipt)
                self.assertIn(f"--- SOP SECTION {anchor} ---", text)
            self.assertEqual(receipt["remaining_anchors"], [])
        _, status, _ = self.invoke("--status")
        self.assertFalse(any(status["missing"].values()))
        self.write_empty_round()
        self.assertEqual(verify(self.directory, "R1", self.spec)[0], [])
        path = self.directory / "screen_rows.json"
        screen = reader.read_receipt(path)
        screen["rows"][0]["reason"] = "Gate 9 concurrency saturated"
        path.write_text(json.dumps(screen), encoding="utf-8")
        issues, _ = verify(self.directory, "R1", self.spec)
        self.assertTrue(any("portfolio capacity cannot decide" in issue for issue in issues), issues)

        path = next((self.directory / "section_receipts").glob("01-*.json"))
        payload = reader.read_receipt(path)
        payload["wake_id"] = "0" * 32
        path.write_text(json.dumps(payload), encoding="utf-8")
        issues, _ = verify(self.directory, "R1", self.spec)
        self.assertTrue(any("receipt does not match" in issue for issue in issues), issues)

    def write_empty_round(self):
        wake = reader.read_receipt(self.directory / "wake_receipt.json")
        def captured_feed(feed, window=None):
            args = SimpleNamespace(feed=feed, symbol="TEST", range=window)
            if feed == "delta-inventory":
                with patch("capture_round_evidence.delta_inventory", return_value={
                    "pages": [{"success": True, "result": [{"symbol": "TESTUSD", "id": 1}], "meta": {"after": None}}]
                }):
                    return capture(self.directory, wake, args)
            if feed == "mt5-inventory":
                with patch("capture_round_evidence.mt5_inventory", return_value={
                    "login": 5126976, "symbols": [{"name": "TEST.pi", "trade_mode": 4}]
                }):
                    return capture(self.directory, wake, args)
            payload = {"ok": True, "sym": "TEST", "value": 0,
                       "updatedAt": int(datetime.now(timezone.utc).timestamp() * 1000)}
            if window:
                payload["range"] = window
            with patch("capture_round_evidence.fetch", return_value=json.dumps(payload).encode("utf-8")):
                return capture(self.directory, wake, args)
        ids = {"delta": "1", "mt5": "TEST.pi"}
        inventories = {venue: {"instrument_ids": [key], "source": captured_feed(f"{venue}-inventory")}
                       for venue, key in ids.items()}
        sources = {item: captured_feed(*item) for item in set.union(*FUNNEL_FEEDS.values())}
        source = sources[("market", None)]
        assets = [{"venue": venue, "instrument_id": key} for venue, key in ids.items()]
        cutoff = (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
        documents = {
            "scope.json": {"cutoff_utc": cutoff, "instruments": assets,
                           "managed": [], "desk_positions": [], "inventories": inventories},
            "screen_rows.json": {"rows": [{**a, "funnel": f, "status": "NO_HIT",
                                           "reason": "fixture", "checks": [
                                               {"feed": name, "range": window, "source": sources[(name, window)],
                                                "pointer": "/value", "observed": 0, "op": "gt", "threshold": 1}
                                               for name, window in FUNNEL_FEEDS[f]
                                           ]} for a in assets for f in sorted(FUNNELS)]},
            "telemetry_rows.json": {"rows": []},
            "gate_rows.json": {"rows": [{"venue": "round", "instrument_id": "round", "rule": f"C-{n:02d}",
                                          "status": "PASS", "observed": True, "threshold": True,
                                          "reason": "fixture", "source": source} for n in range(1, 11)]},
        }
        for name, payload in documents.items():
            payload.update(round_id="R1", spec_sha256=self.spec["sha256"])
            (self.directory / name).write_text(json.dumps(payload), encoding="utf-8")

    def test_source_binding_and_five_minute_coverage(self):
        now = datetime.now(timezone.utc)
        when = (now - timedelta(seconds=2)).isoformat()
        ms = int((now - timedelta(seconds=3)).timestamp() * 1000)
        wake = {"round_id": "R1", "wake_id": "1" * 32, "spec_sha256": "fixture",
                "observed_utc": (now - timedelta(minutes=5)).isoformat()}
        ref = {"path": "raw/feed.json", "sha256": "fixture"}
        receipt = {**wake, **ref, "feed": "liqlevels", "query": {"sym": "BTC", "range": "7d"},
                   "requested_utc": when, "received_utc": when}
        payload = {"sym": "BTC", "range": "7d", "ok": True, "updatedAt": ms}
        audit_source(ref, receipt, payload, wake, now, {"liqlevels"}, "BTCUSD", "7d")
        with self.assertRaisesRegex(ValueError, "symbol"):
            audit_source(ref, receipt, payload, wake, now, {"liqlevels"}, "ETHUSD", "7d")
        with self.assertRaisesRegex(ValueError, "range"):
            audit_source(ref, receipt, payload, wake, now, {"liqlevels"}, "BTCUSD", "30d")
        event = {"t": ms, "asset": "BTC", "venue": "delta", "pair": "BTCUSD",
                 "side": "long", "price": 100, "qtyBase": 1, "usd": 100}
        body = {"asset": {"sym": "BTC", "events": [event, event]}, "venues": [
            {"status": "open", "connectedAt": ms - 330_000, "lastFrameAt": ms}
        ]}
        self.assertEqual(liquidation_pace(body, now), 100)
        body["venues"][0]["connectedAt"] = ms - 5_000
        with self.assertRaisesRegex(ValueError, "continuous"):
            liquidation_pace(body, now)

    def test_phase1_legacy_mutation_flag_is_refused_before_import(self):
        result = phase1.check_and_enforce_phase1(True)
        self.assertFalse(result["ok"])
        self.assertIn("read-only", result["error"])


if __name__ == "__main__":
    unittest.main()
