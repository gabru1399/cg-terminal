#!/usr/bin/env python3
"""Read-only dependency, terminal, and MT5 probes for the round wake receipt."""

import os
import re
import json
import time
import math
import urllib.request
from pathlib import Path

WORKSPACE = Path(os.path.abspath(__file__)).parent.parent
PLUGINS_DIR = Path(os.path.expanduser("~/.gemini/config/plugins"))
SKILLS_DIR = Path(os.path.expanduser("~/.gemini/config/skills"))
MCP_DIR = Path(os.path.expanduser("~/.gemini/antigravity/mcp"))
SPEC_PATH = WORKSPACE / "desk" / "CANONICAL_MASTER_SPECIFICATION.md"
EXPECTED_MT5_LOGIN = 5126976

def audit_plugins():
    required_plugins = ["trading-skills", "superpowers", "coderabbit", "gravitas-native",
                        "chrome-devtools-plugin", "harness-antigravity"]
    status = {}
    for p in required_plugins:
        p_path = PLUGINS_DIR / p
        status[p] = {
            "installed": p_path.is_dir(),
            "path": str(p_path),
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
            "installed": s_path.is_file(),
            "size_bytes": s_path.stat().st_size if s_path.is_file() else 0,
            "path": str(s_path),
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
        exists = m_path.is_dir()
        schemas = list(m_path.glob("*.json")) if exists else []
        status[m] = {
            "installed": exists,
            "tool_schemas_count": len(schemas),
            "path": str(m_path),
            "runtime_checked": False,
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
            "installed": p.is_file(),
            "size_bytes": p.stat().st_size if p.is_file() else 0,
            "path": str(p),
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
        "total_kb_on_disk": round(total_bytes / 1024.0, 2),
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

def positive_number(value):
    return type(value) in (int, float) and math.isfinite(value) and value > 0


def audit_terminal():
    base = "http://127.0.0.1:3000/api/cg"
    attempts = []
    for endpoint, timeout in (("market", 35), ("live", 10)):
        url = f"{base}/{endpoint}?sym=BTC"
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                data = json.load(response)
            if data.get("ok") is not True or data.get("stale") is True:
                raise ValueError(data.get("error") or "Unusable terminal payload")
            if endpoint == "market":
                price = (data.get("price") or {}).get("last")
                poc = ((data.get("auction") or {}).get("day") or {}).get("poc")
                vwap = (data.get("vwap") or {}).get("vwap")
            else:
                price, poc, vwap = data.get("price"), None, None
            if not positive_number(price):
                raise ValueError("BTC price missing or invalid")
            poc = poc if positive_number(poc) else None
            vwap = vwap if positive_number(vwap) else None
            return {
                "ok": True,
                "state": "FIELDS_PRESENT" if poc is not None and vwap is not None else "PARTIAL",
                "endpoint": url,
                "btc_price": price,
                "poc_day": poc,
                "vwap_day": vwap,
                "response_timestamp_ms": data.get("updatedAt", data.get("fetchedAt")),
                "source": data.get("source"),
                "earlier_failures": attempts,
            }
        except (OSError, ValueError, AttributeError) as exc:
            attempts.append({"endpoint": url, "error": str(exc)})
    return {"ok": False, "state": "UNAVAILABLE", "failures": attempts}


def audit_mt5():
    try:
        import MetaTrader5 as mt5
    except ImportError as exc:
        return {"ok": False, "error": str(exc)}

    try:
        if not mt5.initialize():
            return {"ok": False, "error": f"mt5.initialize() failed: {mt5.last_error()}"}
        try:
            account = mt5.account_info()
            if account is None:
                return {"ok": False, "error": f"MT5 account lookup failed: {mt5.last_error()}"}
            if account.login != EXPECTED_MT5_LOGIN:
                return {"ok": False, "error": "Unexpected MT5 account login"}
            positions = mt5.positions_get()
            if positions is None:
                return {"ok": False, "error": f"MT5 positions lookup failed: {mt5.last_error()}"}
            orders = mt5.orders_get()
            if orders is None:
                return {"ok": False, "error": f"MT5 pending orders lookup failed: {mt5.last_error()}"}

            def owned(item):
                return item.comment == "cg_terminal" and item.magic == 42001

            cg_positions = [p for p in positions if owned(p)]
            cg_orders = [o for o in orders if owned(o)]
            return {
                "ok": True,
                "login": account.login,
                "server": account.server,
                "account_currency": account.currency,
                "balance": account.balance,
                "equity": account.equity,
                "margin": account.margin,
                "free_margin": account.margin_free,
                "positions_count": len(positions),
                "orders_count": len(orders),
                "cg_position_tickets": [p.ticket for p in cg_positions],
                "cg_order_tickets": [o.ticket for o in cg_orders],
                "other_algos_count": len(positions) - len(cg_positions),
                "other_orders_count": len(orders) - len(cg_orders),
            }
        finally:
            mt5.shutdown()
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


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
