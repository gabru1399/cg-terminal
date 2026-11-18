#!/usr/bin/env python3
"""
scripts/auto_prompt_paster.py — Automates copying the canonical prompt, focusing Antigravity,
pasting via Ctrl+V, and hitting Enter.

Runs on an interval (default 1200 seconds / 20 minutes).
"""

import os
import sys
import time
import subprocess
from datetime import datetime, timezone

PROMPT_FILE = "desk/CANONICAL_PROMPT.txt"
INTERVAL_SECONDS = 1200

def get_prompt_text():
    if not os.path.exists(PROMPT_FILE):
        return None
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()

def run_paster_round():
    text = get_prompt_text()
    if not text:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: Prompt file {PROMPT_FILE} not found!")
        return False

    # Call PowerShell helper for rock-solid clipboard and window sendkeys
    ps_cmd = [
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-NoProfile",
        "-File", "scripts/auto_prompt_paster.ps1",
        "-IntervalSeconds", "0" # Run once
    ]
    try:
        res = subprocess.run(ps_cmd, capture_output=True, text=True, timeout=15)
        print(res.stdout)
        if res.stderr:
            print(f"[WARN] {res.stderr}")
        return True
    except Exception as e:
        print(f"[ERROR] Paster execution failed: {e}")
        return False

def main():
    print(f"=== Antigravity Auto Prompt Paster Loop Started (Interval: {INTERVAL_SECONDS}s) ===")
    while True:
        run_paster_round()
        print(f"Sleeping for {INTERVAL_SECONDS} seconds until next scheduled execution...\n")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
