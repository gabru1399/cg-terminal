#!/usr/bin/env python3
"""
scripts/auto_prompt_paster.py — Pure Clipboard Auto-Paster.
Pastes whatever text is ALREADY copied in your Windows Clipboard into Antigravity
and presses Enter. It NEVER overwrites your clipboard.

Runs on an interval (default 1200 seconds / 20 minutes).
"""

import os
import sys
import time
import subprocess
from datetime import datetime

INTERVAL_SECONDS = 1200

def run_paster_round():
    ps_cmd = [
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-NoProfile",
        "-File", "scripts/auto_prompt_paster.ps1",
        "-IntervalSeconds", "0" # One-shot execution per tick
    ]
    try:
        res = subprocess.run(ps_cmd, capture_output=True, text=True, timeout=15)
        if res.stdout:
            print(res.stdout.strip())
        if res.stderr:
            print(f"[WARN] {res.stderr.strip()}")
        return True
    except Exception as e:
        print(f"[ERROR] Paster execution failed: {e}")
        return False

def main():
    print(f"=== Antigravity Pure-Clipboard Auto-Paster (Interval: {INTERVAL_SECONDS}s) ===")
    print("Keep your prompt copied in Windows Clipboard. It will be pasted automatically.\n")
    while True:
        run_paster_round()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Sleeping for {INTERVAL_SECONDS} seconds until next paste...\n")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
