#!/usr/bin/env python3
"""
round_preflight_bootstrap.py — Deterministic Physical Pre-Flight Runner
Codifies SOP v2.1.0 & Gravitas Invariants into a zero-token-waste,
unforgeable pre-flight audit executed at the start of every autonomous round.
"""

import os
import sys
import json
import time
import hashlib
import urllib.request
from pathlib import Path

WORKSPACE = Path(os.path.abspath(__file__)).parent.parent
PLUGINS_DIR = Path(os.path.expanduser("~/.gemini/config/plugins"))
SKILLS_DIR = Path(os.path.expanduser("~/.gemini/config/skills"))
SPEC_PATH = WORKSPACE / "desk" / "CANONICAL_MASTER_SPECIFICATION.md"

def audit_plugins():
    required_plugins = ["trading-skills", "superpowers", "coderabbit", "gravitas-native", "chrome-devtools-plugin"]
    status = {}
    for p in required_plugins:
        p_path = PLUGINS_DIR / p
        status[p] = {
            "installed": p_path.exists(),
            "path": str(p_path) if p_path.exists() else None
        }
    return status

def audit_skills():
    required_skills = [
        "gravitas",
        "karpathy-guidelines",
        "ponytail",
        "quant-analyst",
        "backtesting-frameworks"
    ]
    status = {}
    for s in required_skills:
        s_path = SKILLS_DIR / s / "SKILL.md"
        status[s] = {
            "installed": s_path.exists(),
            "size_bytes": s_path.stat().st_size if s_path.exists() else 0
        }
    return status

def audit_spec():
    if not SPEC_PATH.exists():
        return {"ok": False, "error": "CANONICAL_MASTER_SPECIFICATION.md not found"}
    stat = SPEC_PATH.stat()
    return {
        "ok": True,
        "path": str(SPEC_PATH),
        "size_bytes": stat.st_size,
        "last_modified": time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(stat.st_mtime))
    }

def audit_terminal():
    try:
        url = "http://127.0.0.1:3000/api/cg/market?sym=BTC"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "ok": True,
                "btc_price": data.get("price", {}).get("last"),
                "poc_day": data.get("auction", {}).get("day", {}).get("poc"),
                "vwap_day": data.get("vwap", {}).get("vwap")
            }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def audit_mt5():
    try:
        import MetaTrader5 as mt5
        if not mt5.initialize():
            return {"ok": False, "error": f"mt5.initialize() failed: {mt5.last_error()}"}
        
        acc = mt5.account_info()
        if not acc:
            mt5.shutdown()
            return {"ok": False, "error": "account_info() failed"}
            
        all_positions = mt5.positions_get() or ()
        all_orders = mt5.orders_get() or ()
        
        def is_cg(item):
            return getattr(item, "comment", "") == "cg_terminal" and getattr(item, "magic", 0) == 42001
            
        cg_pos = [p for p in all_positions if is_cg(p)]
        cg_ord = [o for o in all_orders if is_cg(o)]
        other_pos = [p for p in all_positions if not is_cg(p)]
        
        # Auto-BE check
        be_results = []
        for p in cg_pos:
            risk_pts = abs(p.price_open - p.sl)
            if risk_pts > 0:
                is_sell = (p.type == mt5.ORDER_TYPE_SELL)
                current_move = (p.price_open - p.price_current) if is_sell else (p.price_current - p.price_open)
                r_mult = current_move / risk_pts
                be_results.append({
                    "ticket": p.ticket,
                    "symbol": p.symbol,
                    "type": "SELL" if is_sell else "BUY",
                    "open": p.price_open,
                    "current": p.price_current,
                    "sl": p.sl,
                    "r_multiple": round(r_mult, 2),
                    "profit_usd": round(p.profit, 2)
                })
        
        res = {
            "ok": True,
            "login": acc.login,
            "balance": acc.balance,
            "equity": acc.equity,
            "free_margin": acc.margin_free,
            "cg_positions": be_results,
            "cg_orders_count": len(cg_ord),
            "cg_orders": [{
                "ticket": o.ticket,
                "symbol": o.symbol,
                "price": o.price_open,
                "sl": o.sl,
                "tp": o.tp,
                "volume": getattr(o, "volume_current", getattr(o, "volume_initial", 0.0))
            } for o in cg_ord],
            "other_algos_count": len(other_pos)
        }
        mt5.shutdown()
        return res
    except Exception as e:
        return {"ok": False, "error": str(e)}

def main():
    report = {
        "timestamp_utc": time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        "spec": audit_spec(),
        "plugins": audit_plugins(),
        "skills": audit_skills(),
        "terminal_engine": audit_terminal(),
        "mt5_status": audit_mt5()
    }
    
    # Print formatted JSON for machine consumption
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
