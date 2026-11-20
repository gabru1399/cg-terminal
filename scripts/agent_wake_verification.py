#!/usr/bin/env python3
"""Read-only Antigravity wake check and digest-pinned SOP section reader."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "desk" / "CANONICAL_MASTER_SPECIFICATION.md"
BOOT = ROOT / "scripts" / "round_preflight_bootstrap.py"
ANCHOR = re.compile(r'<a id="([a-z0-9-]+)"></a>')
REQUIRED = {"kernel", "boot", "sec-4b", *(f"sec-{i}" for i in range(24)),
            *(f"appendix-{letter}" for letter in "abcdef")}


def load_spec(path):
    raw = path.read_bytes()
    lines = raw.decode("utf-8-sig").splitlines(keepends=True)
    starts = {}
    for i, line in enumerate(lines):
        match = ANCHOR.fullmatch(line.strip())
        if match is None:
            continue
        key = match.group(1)
        if key in starts or i == 0 or not lines[i - 1].startswith("## "):
            raise ValueError(f"Invalid or duplicate section anchor: {key}")
        starts[key] = i - 1
    missing = REQUIRED - starts.keys()
    if missing:
        raise ValueError(f"Missing section anchors: {', '.join(sorted(missing))}")

    sections = {}
    anchors = list(starts.items())
    for i, (key, start) in enumerate(anchors):
        end = anchors[i + 1][1] if i + 1 < len(anchors) else len(lines)
        # Part headings belong to the navigation, rather than the prior section.
        while end > start and (not lines[end - 1].strip()
                               or lines[end - 1].strip() == "---"
                               or lines[end - 1].startswith("# PART ")):
            end -= 1
        body = "".join(lines[start:end])
        sections[key] = {
            "start_line": start + 1,
            "end_line": end,
            "section_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "body": body,
        }
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
        "sections": sections,
    }


def section_index(spec):
    return {key: {field: value for field, value in section.items() if field != "body"}
            for key, section in spec["sections"].items()}


def bootstrap():
    started = time.monotonic()
    try:
        proc = subprocess.run(
            [sys.executable, "-X", "utf8", str(BOOT)],
            cwd=ROOT,
            capture_output=True,
            encoding="utf-8",
            timeout=90,
            check=True,
        )
        report = json.loads(proc.stdout)
        if not isinstance(report, dict):
            raise ValueError("Expected a JSON object from bootstrap")
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return {"state": "ERROR", "error": str(exc),
                "elapsed_ms": round((time.monotonic() - started) * 1000)}
    return {"state": "REPORTED", "elapsed_ms": round((time.monotonic() - started) * 1000),
            "report": report}


def emit(payload):
    print("WAKE_RECEIPT " + json.dumps(payload, ensure_ascii=False, allow_nan=False))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", required=True, help="Scheduler-supplied round ID")
    parser.add_argument("--section", action="append", help="Read one anchor, may be repeated")
    parser.add_argument("--expect-sha256", help="Specification SHA-256 from the wake receipt")
    args = parser.parse_args(argv)
    if args.section and not args.expect_sha256:
        parser.error("--section requires --expect-sha256 from the current wake receipt")

    payload = {"round_id": args.round, "kind": "section_read" if args.section else "wake"}
    try:
        spec = load_spec(SPEC)
        payload["spec_sha256"] = spec["sha256"]
        payload["spec_size_bytes"] = spec["size_bytes"]
        if args.expect_sha256 and args.expect_sha256 != spec["sha256"]:
            raise ValueError("Specification changed since wake; restart with a new round ID")
        requested = args.section or ["kernel"]
        unknown = set(requested) - spec["sections"].keys()
        if unknown:
            raise ValueError(f"Unknown section anchors: {', '.join(sorted(unknown))}")
        index = section_index(spec)
        for key in requested:
            print(f"--- SOP SECTION {key} ---")
            print(spec["sections"][key]["body"].rstrip("\r\n"))
        payload["sections_read"] = {key: index[key] for key in requested}
        payload["status"] = "OK"
        if not args.section:
            payload["section_index"] = index
            payload["bootstrap"] = bootstrap()
            payload["status"] = payload["bootstrap"]["state"]
            payload["unchecked"] = [
                "skill_loading", "delta_mcp_call", "venue_reconciliation", "telemetry_coverage",
                "risk_gates", "execution_authorization", "scheduler",
            ]
    except (OSError, ValueError) as exc:
        payload.update(status="ERROR", error=str(exc))
    emit(payload)
    return int(payload["status"] == "ERROR")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
