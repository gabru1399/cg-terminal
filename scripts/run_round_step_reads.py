#!/usr/bin/env python3
"""Execute all step reads for any round sequentially until all anchors are satisfied."""
import subprocess
import sys
import json
import argparse

def run_step(round_id, step):
    cmd = [sys.executable, "scripts/agent_wake_verification.py", "--round", round_id, "--step", str(step)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error on step {step}: {res.stderr}")
        return False, None
    for line in res.stdout.splitlines():
        if line.startswith("WAKE_RECEIPT"):
            data = json.loads(line[len("WAKE_RECEIPT "):])
            return True, data
    return True, None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", required=True)
    args = parser.parse_args()
    round_id = args.round

    for s in range(12):
        print(f"=== Reading Step {s} ===")
        while True:
            ok, data = run_step(round_id, s)
            if not ok or not data:
                print(f"Failed to read step {s}")
                break
            remaining = data.get("remaining_anchors", [])
            print(f"Step {s}: remaining_anchors = {remaining}")
            if not remaining:
                break
    
    print("=== Running --require-formulation-reads ===")
    cmd = [sys.executable, "scripts/agent_wake_verification.py", "--round", round_id, "--require-formulation-reads"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("STDERR:", res.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
