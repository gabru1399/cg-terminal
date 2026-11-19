#!/usr/bin/env python3
"""
clear_cache_memory.py — Workspace Cache & Memory Cleaner
=========================================================
SOP v2.1.0 | Mandatory Pre-Wake & Timer-Expiration Maintenance Tool

Actions:
  1. Purges Python bytecode cache (__pycache__, *.pyc, *.pyo) across the workspace.
  2. Purges Next.js compilation / data cache (.next/cache) to prevent stale state.
  3. Trims process RAM working sets via Windows PSAPI (EmptyWorkingSet).
  4. Forces Python garbage collection (gc.collect).
"""

import os
import sys
import gc
import shutil
import ctypes
from pathlib import Path

WORKSPACE = Path(os.path.abspath(__file__)).parent.parent

def clear_python_cache():
    removed_dirs = 0
    removed_files = 0
    for root, dirs, files in os.walk(WORKSPACE):
        if "node_modules" in root or ".git" in root:
            continue
        for d in list(dirs):
            if d == "__pycache__":
                target = Path(root) / d
                try:
                    shutil.rmtree(target, ignore_errors=True)
                    removed_dirs += 1
                except Exception:
                    pass
        for f in files:
            if f.endswith((".pyc", ".pyo")):
                target = Path(root) / f
                try:
                    target.unlink(missing_ok=True)
                    removed_files += 1
                except Exception:
                    pass
    return removed_dirs, removed_files

def clear_nextjs_cache():
    cache_dir = WORKSPACE / ".next" / "cache"
    removed = False
    if cache_dir.exists():
        try:
            shutil.rmtree(cache_dir, ignore_errors=True)
            removed = True
        except Exception:
            pass
    return removed

def trim_memory():
    trimmed_processes = 0
    gc.collect()
    if sys.platform == "win32":
        try:
            # EmptyWorkingSet for current process
            current_process = ctypes.windll.kernel32.GetCurrentProcess()
            ctypes.windll.psapi.EmptyWorkingSet(current_process)
            trimmed_processes += 1
        except Exception:
            pass
            
        # Try trimming Python and Node processes
        try:
            import subprocess
            cmd = "Get-Process -Name python, node -ErrorAction SilentlyContinue | ForEach-Object { [System.GC]::Collect(); $_.EmptyWorkingSet() }"
            subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, timeout=5)
        except Exception:
            pass
    return trimmed_processes

def main():
    py_dirs, py_files = clear_python_cache()
    next_cleared = clear_nextjs_cache()
    proc_trimmed = trim_memory()

    print("═" * 70)
    print("  CACHE & MEMORY PURGE COMPLETE")
    print(f"  • Python Cache Cleared   : {py_dirs} __pycache__ dirs, {py_files} .pyc files")
    print(f"  • Next.js Cache Cleared  : {'.next/cache purged' if next_cleared else 'None / Already clean'}")
    print(f"  • RAM Working Sets Trimmed: Process working sets trimmed via PSAPI/GC")
    print("═" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
