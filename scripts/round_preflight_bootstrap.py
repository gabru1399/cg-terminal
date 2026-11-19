#!/usr/bin/env python3
"""
round_preflight_bootstrap.py — Deterministic Physical Pre-Flight Runner
Codifies SOP v2.1.0 & Gravitas Invariants into a zero-token-waste,
unforgeable pre-flight audit executed at the start of every autonomous round.
"""

import os
import sys
import re
import json
import time
import hashlib
import urllib.request
from pathlib import Path

WORKSPACE = Path(os.path.abspath(__file__)).parent.parent
PLUGINS_DIR = Path(os.path.expanduser("~/.gemini/config/plugins"))
SKILLS_DIR = Path(os.path.expanduser("~/.gemini/config/skills"))
MCP_DIR = Path(os.path.expanduser("~/.gemini/antigravity/mcp"))
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

def audit_mcp_servers():
    required_mcp = [
        "delta-exchange-mcp",
        "agent-memory",
        "chrome-devtools",
        "godkiller-verification",
        "code-review-graph",
        "link-extension",
        "sqlite"
    ]
    status = {}
    for m in required_mcp:
        m_path = MCP_DIR / m
        exists = m_path.exists()
        schemas = list(m_path.glob("*.json")) if exists else []
        status[m] = {
            "installed": exists,
            "tool_schemas_count": len(schemas),
            "path": str(m_path) if exists else None
        }
    return status

def audit_slash_command_skills():
    slash_skills = {
        "/plan": PLUGINS_DIR / "superpowers" / "skills" / "writing-plans" / "SKILL.md",
        "/brainstorming": PLUGINS_DIR / "superpowers" / "skills" / "brainstorming" / "SKILL.md",
        "/executing-plans": PLUGINS_DIR / "superpowers" / "skills" / "executing-plans" / "SKILL.md",
        "/karpathy-guidelines": SKILLS_DIR / "karpathy-guidelines" / "SKILL.md",
        "/thinking-model-router": SKILLS_DIR / "thinking-model-router" / "SKILL.md",
        "/gravitas": SKILLS_DIR / "gravitas" / "SKILL.md",
        "/verification-before-completion": PLUGINS_DIR / "superpowers" / "skills" / "verification-before-completion" / "SKILL.md",
    }
    status = {}
    for cmd, p in slash_skills.items():
        status[cmd] = {
            "installed": p.exists(),
            "size_bytes": p.stat().st_size if p.exists() else 0,
            "path": str(p) if p.exists() else None
        }
    return status

def audit_all_spec_links():
    if not SPEC_PATH.exists():
        return {"ok": False, "error": "Spec not found"}
    with open(SPEC_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    links = re.findall(r'\[([^\]]+)\]\((file:///[^)]+)\)', content)
    
    t0 = time.perf_counter()
    broken = []
    total_bytes = 0
    for label, url in links:
        raw_path = url.replace("file:///", "")
        p = Path(raw_path)
        if not p.exists():
            broken.append({"label": label, "url": url, "path": str(p)})
        elif p.is_file():
            total_bytes += p.stat().st_size
            
    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    return {
        "ok": len(broken) == 0,
        "total_links": len(links),
        "valid_links": len(links) - len(broken),
        "broken_count": len(broken),
        "broken_links": broken,
        "total_kb_read": round(total_bytes / 1024.0, 2),
        "load_time_ms": elapsed_ms
    }

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
    for base in ["http://localhost:3000", "http://127.0.0.1:3000"]:
        try:
            url = f"{base}/api/cg/market?sym=BTC"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=35) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {
                    "ok": True,
                    "btc_price": data.get("price", {}).get("last"),
                    "poc_day": data.get("auction", {}).get("day", {}).get("poc"),
                    "vwap_day": data.get("vwap", {}).get("vwap")
                }
        except Exception:
            try:
                url_live = f"{base}/api/cg/live?sym=BTC"
                req_live = urllib.request.Request(url_live, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req_live, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    return {
                        "ok": True,
                        "btc_price": data.get("price"),
                        "poc_day": None,
                        "vwap_day": None
                    }
            except Exception:
                continue
    return {"ok": False, "error": "terminal unreachable"}

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
            is_sell = (p.type == mt5.ORDER_TYPE_SELL)
            current_move = (p.price_open - p.price_current) if is_sell else (p.price_current - p.price_open)
            risk_pts = abs(p.price_open - p.sl)
            r_mult = round(current_move / risk_pts, 2) if risk_pts > 0 else "BE_LOCKED"
            be_results.append({
                "ticket": p.ticket,
                "symbol": p.symbol,
                "type": "SELL" if is_sell else "BUY",
                "open": p.price_open,
                "current": p.price_current,
                "sl": p.sl,
                "r_multiple": r_mult,
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
        "spec_links_audit": audit_all_spec_links(),
        "plugins": audit_plugins(),
        "skills": audit_skills(),
        "mcp_servers": audit_mcp_servers(),
        "slash_command_skills": audit_slash_command_skills(),
        "terminal_engine": audit_terminal(),
        "mt5_status": audit_mt5()
    }
    
    # Print formatted JSON for machine consumption
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
