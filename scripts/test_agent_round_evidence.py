"""Regression coverage for round wake retries and the canonical section chain."""

from contextlib import redirect_stdout
import hashlib
from io import StringIO
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import agent_wake_verification as reader
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

        path = next((self.directory / "section_receipts").glob("01-*.json"))
        payload = reader.read_receipt(path)
        payload["wake_id"] = "0" * 32
        path.write_text(json.dumps(payload), encoding="utf-8")
        issues, _ = verify(self.directory, "R1", self.spec)
        self.assertTrue(any("receipt does not match" in issue for issue in issues), issues)

    def write_empty_round(self):
        raw = self.directory / "raw" / "test.json"
        raw.parent.mkdir()
        raw.write_bytes(b"{}")
        source = {"path": "raw/test.json", "sha256": hashlib.sha256(raw.read_bytes()).hexdigest()}
        assets = [{"venue": venue, "instrument_id": "test"} for venue in ("delta", "mt5")]
        documents = {
            "scope.json": {"cutoff_utc": "2026-11-20T12:00:00Z", "instruments": assets,
                           "managed": [], "desk_positions": [],
                           "inventories": {a["venue"]: {"instrument_ids": ["test"], "source": source} for a in assets}},
            "screen_rows.json": {"rows": [{**a, "funnel": f, "status": "NO_HIT",
                                           "reason": "fixture", "source": source} for a in assets for f in sorted(FUNNELS)]},
            "telemetry_rows.json": {"rows": []},
            "gate_rows.json": {"rows": [{"venue": "round", "instrument_id": "round", "rule": f"C-{n:02d}",
                                          "status": "PASS", "observed": True, "threshold": True,
                                          "reason": "fixture", "source": source} for n in range(1, 11)]},
        }
        for name, payload in documents.items():
            payload.update(round_id="R1", spec_sha256=self.spec["sha256"])
            (self.directory / name).write_text(json.dumps(payload), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
