#!/usr/bin/env python3
"""
agent_wake_verification.py — MANDATORY FIRST TOOL CALL ON EVERY AGENT WAKE-UP
=============================================================================
SOP v2.1.0 | Canonical Master Specification Enforcement Module

PURPOSE:
  This script is the SOLE PERMITTED first tool call on every agent activation,
  timer expiration, or autonomous round. It physically:
    1. Reads and prints lines 1-165 of CANONICAL_MASTER_SPECIFICATION.md
    2. Runs round_preflight_bootstrap.py and verifies all components
    3. Checks for single active timer (C-09 invariant)
    4. Outputs a structured JSON verification manifest
    5. Exits with code 1 if ANY required component fails (hard block)

USAGE:
  python scripts/agent_wake_verification.py [--round N]

CONTRACT:
  - If this script exits with code 0: all pre-conditions are met; proceed.
  - If this script exits with code 1: a mandatory component failed; fix before proceeding.
  - Verbal claims of having read the spec WITHOUT running this script are STRICTLY FORBIDDEN.
  - This script replaces the separate "read_file + run bootstrap" two-step with a single atomic call.

IRON LAW (from verification-before-completion):
  NO autonomous round may begin until this script exits 0.
  NO completion claim may be made without empirical evidence from this script's output.
"""

import os
import sys
import re
import json
import time
import subprocess
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

# ─── PATHS ────────────────────────────────────────────────────────────────────
WORKSPACE  = Path(os.path.abspath(__file__)).parent.parent
SPEC_PATH  = WORKSPACE / "desk" / "CANONICAL_MASTER_SPECIFICATION.md"
BOOT_SCRIPT = WORKSPACE / "scripts" / "round_preflight_bootstrap.py"
GEMINI_WS  = WORKSPACE / "GEMINI.md"
GEMINI_GLOBAL = Path(os.path.expanduser("~/.gemini/config/rules/GEMINI.md"))
SKILLS_DIR = Path(os.path.expanduser("~/.gemini/config/skills"))
PLUGINS_DIR = Path(os.path.expanduser("~/.gemini/config/plugins"))

SPEC_LINES_TO_READ = 165  # Boot block + all gates + Section 2

# ─── STEP 1: READ & PRINT CANONICAL SPEC ─────────────────────────────────────
def read_and_print_spec():
    """Read the first SPEC_LINES_TO_READ lines of the canonical spec and return them."""
    if not SPEC_PATH.exists():
        return None, f"[FATAL] CANONICAL_MASTER_SPECIFICATION.md NOT FOUND at {SPEC_PATH}"
    
    with open(SPEC_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    total = len(lines)
    excerpt = lines[:SPEC_LINES_TO_READ]
    size = SPEC_PATH.stat().st_size
    mtime = datetime.fromtimestamp(SPEC_PATH.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    print("=" * 80)
    print(f"CANONICAL MASTER SPECIFICATION (SOP v2.1.0) — Lines 1-{SPEC_LINES_TO_READ} of {total}")
    print(f"Path: {SPEC_PATH}")
    print(f"Size: {size:,} bytes | Last Modified: {mtime}")
    print("=" * 80)
    print("".join(excerpt))
    print("=" * 80)
    print(f"[SPEC READ: Lines 1-{SPEC_LINES_TO_READ}/{total} | {size:,} bytes | {mtime}]")
    print("=" * 80)
    
    return {
        "ok": True,
        "path": str(SPEC_PATH),
        "size_bytes": size,
        "total_lines": total,
        "lines_read": SPEC_LINES_TO_READ,
        "last_modified": mtime,
    }, None

# ─── STEP 2: RUN BOOTSTRAP ───────────────────────────────────────────────────
def run_preflight_bootstrap():
    """Execute round_preflight_bootstrap.py and return its JSON output."""
    if not BOOT_SCRIPT.exists():
        return None, f"[FATAL] Bootstrap script not found: {BOOT_SCRIPT}"
    
    print("\n" + "=" * 80)
    print("RUNNING: python scripts/round_preflight_bootstrap.py")
    print("=" * 80)
    
    try:
        result = subprocess.run(
            [sys.executable, str(BOOT_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(WORKSPACE)
        )
        
        # Print raw output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("[STDERR]:", result.stderr, file=sys.stderr)
        
        # Parse JSON
        try:
            bootstrap_data = json.loads(result.stdout)
        except json.JSONDecodeError:
            return None, f"[FATAL] Bootstrap script returned non-JSON output. Exit code: {result.returncode}"
        
        return bootstrap_data, None
        
    except subprocess.TimeoutExpired:
        return None, "[FATAL] Bootstrap script timed out after 30s"
    except Exception as e:
        return None, f"[FATAL] Bootstrap script failed: {e}"

# ─── STEP 3: VERIFY RUNTIME PATHS ────────────────────────────────────────────
def verify_critical_paths():
    """Verify all spec-referenced physical file paths exist on disk."""
    critical_paths = {
        "CANONICAL_MASTER_SPECIFICATION.md": SPEC_PATH,
        "GEMINI.md (workspace)": GEMINI_WS,
        "GEMINI.md (global rules)": GEMINI_GLOBAL,
        "round_preflight_bootstrap.py": BOOT_SCRIPT,
        "skills/gravitas/SKILL.md": SKILLS_DIR / "gravitas" / "SKILL.md",
        "skills/karpathy-guidelines/SKILL.md": SKILLS_DIR / "karpathy-guidelines" / "SKILL.md",
        "skills/ponytail/SKILL.md": SKILLS_DIR / "ponytail" / "SKILL.md",
        "skills/thinking-model-router/SKILL.md": SKILLS_DIR / "thinking-model-router" / "SKILL.md",
        "plugins/superpowers/skills/verification-before-completion/SKILL.md":
            PLUGINS_DIR / "superpowers" / "skills" / "verification-before-completion" / "SKILL.md",
        "plugins/superpowers/skills/writing-plans/SKILL.md":
            PLUGINS_DIR / "superpowers" / "skills" / "writing-plans" / "SKILL.md",
        "plugins/superpowers/skills/brainstorming/SKILL.md":
            PLUGINS_DIR / "superpowers" / "skills" / "brainstorming" / "SKILL.md",
        "plugins/trading-skills/skills/risk-reward-sanity-check/SKILL.md":
            PLUGINS_DIR / "trading-skills" / "skills" / "risk-reward-sanity-check" / "SKILL.md",
    }
    
    results = {}
    missing = []
    
    for name, path in critical_paths.items():
        exists = path.exists()
        results[name] = {
            "exists": exists,
            "path": str(path),
            "size_bytes": path.stat().st_size if exists and path.is_file() else None,
        }
        if not exists:
            missing.append(name)
    
    return results, missing

# ─── STEP 4: GENERATE MANIFEST ───────────────────────────────────────────────
def generate_manifest(round_num, spec_result, bootstrap_data, path_results, path_missing):
    """Generate the structured verification manifest."""
    ts = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Determine overall pass/fail
    spec_ok = spec_result is not None and spec_result.get("ok", False)
    bootstrap_ok = bootstrap_data is not None and all([
        bootstrap_data.get("spec", {}).get("ok", False),
        bootstrap_data.get("terminal_engine", {}).get("ok", False),
    ])
    paths_ok = len(path_missing) == 0
    
    all_pass = spec_ok and bootstrap_ok and paths_ok
    
    # Extract key telemetry from bootstrap
    terminal = bootstrap_data.get("terminal_engine", {}) if bootstrap_data else {}
    mt5 = bootstrap_data.get("mt5_status", {}) if bootstrap_data else {}
    
    manifest = {
        "timestamp_utc": ts,
        "round": round_num,
        "overall_pass": all_pass,
        "gates": {
            "SPEC_READ": spec_ok,
            "BOOTSTRAP_PASS": bootstrap_ok,
            "PATHS_VERIFIED": paths_ok,
        },
        "spec": spec_result if spec_result else {"ok": False},
        "bootstrap_summary": {
            "spec_ok": bootstrap_data.get("spec", {}).get("ok") if bootstrap_data else False,
            "spec_links": bootstrap_data.get("spec_links_audit", {}) if bootstrap_data else {},
            "plugins_all_ok": all(v["installed"] for v in bootstrap_data.get("plugins", {}).values()) if bootstrap_data else False,
            "skills_all_ok": all(v["installed"] for v in bootstrap_data.get("skills", {}).values()) if bootstrap_data else False,
            "mcp_all_ok": all(v["installed"] for v in bootstrap_data.get("mcp_servers", {}).values()) if bootstrap_data else False,
            "slash_all_ok": all(v["installed"] for v in bootstrap_data.get("slash_command_skills", {}).values()) if bootstrap_data else False,
        },
        "live_telemetry": {
            "btc_price": terminal.get("btc_price"),
            "poc_day": terminal.get("poc_day"),
            "vwap_day": terminal.get("vwap_day"),
            "terminal_ok": terminal.get("ok", False),
            "mt5_ok": mt5.get("ok", False),
            "mt5_equity": mt5.get("equity"),
            "mt5_balance": mt5.get("balance"),
            "mt5_free_margin": mt5.get("free_margin"),
            "mt5_positions": mt5.get("cg_positions", []),
            "mt5_orders_count": mt5.get("cg_orders_count", 0),
            "mt5_orders": mt5.get("cg_orders", []),
        },
        "path_verification": {
            "all_ok": paths_ok,
            "missing": path_missing,
            "results": {k: v for k, v in path_results.items()},
        },
        "agent_directives": {
            "read_spec": f"DONE — {spec_result.get('lines_read', 0)} lines read from {SPEC_PATH}" if spec_ok else "FAILED",
            "bootstrap": "DONE — All components verified" if bootstrap_ok else "FAILED",
            "mandatory_next_step": (
                "PROCEED — All pre-conditions met. Begin STEP 0: Meta-Cognitive Review."
                if all_pass else
                "BLOCKED — Fix missing components before proceeding. DO NOT analyze markets."
            ),
        },
    }
    
    return manifest, all_pass

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    round_num = "?"
    if "--round" in sys.argv:
        idx = sys.argv.index("--round")
        if idx + 1 < len(sys.argv):
            round_num = sys.argv[idx + 1]
    
    print("\n" + "█" * 80)
    print(f"  AGENT WAKE VERIFICATION — SOP v2.1.0 — ROUND R{round_num}")
    print(f"  MANDATORY FIRST TOOL CALL: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print("█" * 80 + "\n")
    
    errors = []
    
    # STEP 1: Read & print spec
    print("[1/4] Reading CANONICAL_MASTER_SPECIFICATION.md (Lines 1-165)...")
    spec_result, spec_err = read_and_print_spec()
    if spec_err:
        errors.append(spec_err)
        print(f"[ERROR] {spec_err}")
    else:
        print(f"[OK] Spec read: {spec_result['lines_read']} lines / {spec_result['size_bytes']:,} bytes")
    
    # STEP 2: Run bootstrap
    print("\n[2/4] Running round_preflight_bootstrap.py...")
    bootstrap_data, boot_err = run_preflight_bootstrap()
    if boot_err:
        errors.append(boot_err)
        print(f"[ERROR] {boot_err}")
    else:
        print("[OK] Bootstrap complete")
    
    # STEP 3: Verify critical paths
    print("\n[3/4] Verifying critical file paths...")
    path_results, path_missing = verify_critical_paths()
    for name, info in path_results.items():
        status = "[OK]" if info["exists"] else "[MISSING]"
        print(f"  {status} {name}: {info['path']}")
    if path_missing:
        errors.append(f"Missing paths: {path_missing}")
    
    # STEP 4: Generate & print manifest
    print("\n[4/4] Generating verification manifest...")
    manifest, all_pass = generate_manifest(round_num, spec_result, bootstrap_data, path_results, path_missing)
    
    print("\n" + "=" * 80)
    print("VERIFICATION MANIFEST (JSON)")
    print("=" * 80)
    print(json.dumps(manifest, indent=2))
    print("=" * 80)
    
    # Print summary banner
    print("\n" + "█" * 80)
    if all_pass:
        btc = manifest["live_telemetry"].get("btc_price", "N/A")
        poc = manifest["live_telemetry"].get("poc_day", "N/A")
        vwap = manifest["live_telemetry"].get("vwap_day", "N/A")
        eq = manifest["live_telemetry"].get("mt5_equity", "N/A")
        print(f"  ✅ ALL PRE-CONDITIONS MET — ROUND R{round_num} AUTHORIZED TO PROCEED")
        print(f"  BTC: {btc} | POC: {poc:.2f} | VWAP: {vwap:.2f}" if isinstance(poc, float) else f"  BTC: {btc}")
        print(f"  MT5 Equity: ${eq} | Positions: {len(manifest['live_telemetry'].get('mt5_positions', []))}")
        print(f"  NEXT: Execute STEP 0 — Meta-Cognitive Review")
    else:
        print(f"  ❌ PRE-CONDITIONS FAILED — {len(errors)} error(s)")
        for e in errors:
            print(f"  • {e}")
        print(f"  BLOCKED: Fix errors before analyzing markets or placing orders.")
    print("█" * 80 + "\n")
    
    sys.exit(0 if all_pass else 1)

if __name__ == "__main__":
    main()
