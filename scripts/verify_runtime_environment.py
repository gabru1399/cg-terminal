#!/usr/bin/env python3
"""
scripts/verify_runtime_environment.py — Comprehensive Diagnostic Sentry for Plugins, Skills, MCP Servers & Venues.

Author: Antigravity Autonomous Trading Intelligence (Trading AGI v4.0)
Verifies:
  1. Skill definition files (SKILL.md) on disk.
  2. Plugin installations & rules files.
  3. Live Next.js Order-Flow Terminal (http://127.0.0.1:3000).
  4. Blueberry Funded MetaTrader 5 Terminal (#5126976).
  5. Canonical Master Specification (desk/CANONICAL_MASTER_SPECIFICATION.md).
"""

import os
import sys
import json
import requests

def check_file(path, label):
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    return {
        "label": label,
        "path": path,
        "exists": exists,
        "size_bytes": size,
        "status": "PASS" if exists and size > 0 else "FAIL"
    }

def check_terminal_api():
    url = "http://127.0.0.1:3000/api/cg/market?sym=BTC"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return {"status": "PASS", "details": f"Next.js Terminal Live (HTTP 200, BTC {r.json().get('market', {}).get('price')})"}
        return {"status": "FAIL", "details": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"status": "FAIL", "details": str(e)}

def check_mt5():
    try:
        import MetaTrader5 as mt5
        if not mt5.initialize(timeout=5000):
            return {"status": "FAIL", "details": f"mt5.initialize failed: {mt5.last_error()}"}
        acc = mt5.account_info()
        if not acc:
            mt5.shutdown()
            return {"status": "FAIL", "details": "account_info returned None"}
        res = {
            "status": "PASS",
            "login": acc.login,
            "balance": acc.balance,
            "equity": acc.equity,
            "margin_free": acc.margin_free
        }
        mt5.shutdown()
        return res
    except ImportError:
        return {"status": "FAIL", "details": "MetaTrader5 package not installed"}
    except Exception as e:
        return {"status": "FAIL", "details": str(e)}

def run_diagnostics():
    print("=" * 80)
    print("ANTIGRAVITY RUNTIME & DEPENDENCY VERIFICATION REPORT")
    print("=" * 80)

    skills_to_check = [
        (r"C:\Users\SIGMA\.gemini\config\plugins\gravitas-native\skills\gravitas\SKILL.md", "gravitas"),
        (r"C:\Users\SIGMA\.gemini\config\skills\karpathy-guidelines\SKILL.md", "karpathy-guidelines"),
        (r"C:\Users\SIGMA\.gemini\config\skills\ponytail\SKILL.md", "ponytail"),
        (r"C:\Users\SIGMA\.gemini\config\skills\quant-analyst\SKILL.md", "quant-analyst"),
        (r"C:\Users\SIGMA\.gemini\config\skills\backtesting-frameworks\SKILL.md", "backtesting-frameworks"),
        (r"C:\Users\SIGMA\.gemini\config\plugins\trading-skills\skills\market-regime-analysis\SKILL.md", "market-regime-analysis"),
        (r"C:\Users\SIGMA\.gemini\config\plugins\trading-skills\skills\risk-reward-sanity-check\SKILL.md", "risk-reward-sanity-check"),
        (r"C:\Users\SIGMA\.gemini\config\plugins\superpowers\skills\systematic-debugging\SKILL.md", "systematic-debugging"),
        (r"c:\Users\SIGMA\Documents\cg-terminal\desk\CANONICAL_MASTER_SPECIFICATION.md", "CANONICAL_MASTER_SPECIFICATION")
    ]

    print("\n[1] SKILLS & SPECIFICATIONS INTEGRITY:")
    all_skills_pass = True
    for path, label in skills_to_check:
        res = check_file(path, label)
        print(f"  [{res['status']}] {label:<30} ({res['size_bytes']} bytes) -> {path}")
        if res["status"] != "PASS":
            all_skills_pass = False

    print("\n[2] LOCAL TERMINAL ENGINE (PORT 3000):")
    term_res = check_terminal_api()
    print(f"  [{term_res['status']}] {term_res.get('details')}")

    print("\n[3] BLUEBERRY FUNDED MT5 TERMINAL:")
    mt5_res = check_mt5()
    if mt5_res["status"] == "PASS":
        print(f"  [PASS] MT5 Login #{mt5_res['login']} | Balance: ${mt5_res['balance']:.2f} | Equity: ${mt5_res['equity']:.2f} | Free Margin: ${mt5_res['margin_free']:.2f}")
    else:
        print(f"  [FAIL] MT5 Connection: {mt5_res.get('details')}")

    print("\n" + "=" * 80)
    overall = all_skills_pass and term_res["status"] == "PASS" and mt5_res["status"] == "PASS"
    print(f"OVERALL RUNTIME STATUS: {'[ALL SYSTEMS OPERATIONAL]' if overall else '[DEGRADED / ACTION REQUIRED]'}")
    print("=" * 80)
    return overall

if __name__ == "__main__":
    success = run_diagnostics()
    sys.exit(0 if success else 1)
