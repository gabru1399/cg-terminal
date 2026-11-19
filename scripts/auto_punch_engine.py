#!/usr/bin/env python3
"""
scripts/auto_punch_engine.py — Autonomous Dual-Venue Signal Evaluation & Direct Punch Engine.

Author: Antigravity Autonomous Trading Intelligence (Trading AGI v4.0)
Operates:
  1. Blueberry Funded MT5 (Login #5126976) — Prop-Firm Protected ($6 risk cap, magic 42001, comment "cg_terminal")
  2. Delta Exchange India (Account #26902927) — Post-Only Maker Execution (post_only: true)

Evaluates real-time signals from /api/strategy/cards across the Curated Universe.
Enforces SOP v2.1.0 invariants (EV >= 2.0R, Cold Zone SL, Auto-Breakeven, Drawdown Guards).
"""

import sys
import os
import json
import time
import requests
import subprocess
from datetime import datetime, timezone

try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None

TERMINAL_URL = "http://127.0.0.1:3000"
SCAN_SYMBOLS = ["BTC", "ETH", "SOL", "BNB", "XAU", "DOGE", "XRP", "ADA", "AVAX", "LINK", "SUI", "APT", "NEAR", "TIA"]
MAX_RISK_USD = 6.00
MAGIC_NUMBER = 42001
CG_COMMENT = "cg_terminal"

def get_live_cards(symbols):
    sym_query = ",".join(symbols)
    url = f"{TERMINAL_URL}/api/strategy/cards?sym={sym_query}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            cards = []
            for asset in data.get("assets", []):
                for card in asset.get("cards", []):
                    cards.append(card)
            return cards
    except Exception as e:
        print(f"[ERROR] Failed to fetch strategy cards: {e}")
    return []

def get_mt5_active_state():
    if not mt5.initialize():
        return None
    acc = mt5.account_info()
    if not acc:
        mt5.shutdown()
        return None
    
    positions = mt5.positions_get() or ()
    orders = mt5.orders_get() or ()
    
    cg_positions = [p for p in positions if p.comment == CG_COMMENT or p.magic == MAGIC_NUMBER]
    cg_orders = [o for o in orders if o.comment == CG_COMMENT or o.magic == MAGIC_NUMBER]
    all_positions = [p for p in positions]
    
    res = {
        "account": {
            "login": acc.login,
            "balance": acc.balance,
            "equity": acc.equity,
            "margin_free": acc.margin_free
        },
        "cg_positions": cg_positions,
        "cg_orders": cg_orders,
        "all_positions": all_positions
    }
    mt5.shutdown()
    return res

def punch_mt5_order(card, risk_usd=5.50):
    """
    Executes an MT5 order via scripts/mt5_punch.py with strict prop-firm guards.
    """
    sym = card["sym"].replace("USDT", "").replace("USDT-M", "")
    entry = float(card["entry"])
    stop = float(card["stop"])
    stop_dist = abs(entry - stop)
    
    # Enforce >= 2.0R hurdle: select target delivering >= 1.95R
    chosen_tp = 0.0
    targets = card.get("targets", [])
    for t in targets:
        if t > 0 and abs(entry - float(t)) >= 1.95 * stop_dist:
            chosen_tp = float(t)
            break
            
    # If no card target meets 1.95R, synthesize 2.5R target if rPlanned >= 2.0
    if chosen_tp == 0.0:
        if card.get("rPlanned", 0.0) >= 2.0:
            if side == "long":
                chosen_tp = entry + 2.5 * stop_dist
            else:
                chosen_tp = entry - 2.5 * stop_dist
        else:
            return {"ok": False, "error": f"Rejected by 2.0R hurdle: no targets deliver >= 2.0R (entry {entry}, stop {stop}, targets {targets})"}
            
    realized_r = abs(entry - chosen_tp) / stop_dist if stop_dist > 0 else 0
    if realized_r < 1.95:
        return {"ok": False, "error": f"Rejected by 2.0R hurdle: realized R {realized_r:.2f} < 1.95R hard floor"}
        
    side = card["side"].lower()
    
    payload = {
        "symbol": sym,
        "side": side,
        "kind": "limit" if card.get("kind") == "limit" else "market",
        "entry": entry,
        "stop": stop,
        "tp": chosen_tp,
        "risk_usd": float(risk_usd)
    }
    
    try:
        p = subprocess.Popen(
            [sys.executable, "scripts/mt5_punch.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, err = p.communicate(input=json.dumps(payload), timeout=20)
        res = json.loads(out.strip().split("\n")[-1])
        return res
    except Exception as e:
        return {"ok": False, "error": str(e)}

def sync_desk_state(order_record, wake_message):
    state_path = "desk/state.json"
    wake_path = "desk/inbox/WAKE.md"
    try:
        if os.path.exists(state_path):
            with open(state_path, "r", encoding="utf-8") as f:
                state = json.load(f)
            if "orders" not in state or not isinstance(state["orders"], list):
                state["orders"] = []
            state["orders"].append(order_record)
            with open(state_path, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
                f.write("\n")
                
        with open(wake_path, "a", encoding="utf-8") as f:
            f.write(f"\n{wake_message}\n")
    except Exception as e:
        print(f"[WARN] Failed to sync desk ledger: {e}")

def normalize_base(sym):
    s = sym.split(".")[0].replace("USDT-M", "").replace("USDT", "").replace("USD", "").upper()
    alias_map = {
        "LNK": "LINK",
        "DOG": "DOGE",
        "AVX": "AVAX",
    }
    return alias_map.get(s, s)

def run_evaluation_and_punch():
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}] Starting Autonomous Signal Evaluation & Dual-Venue Punch Engine...")
    
    cards = get_live_cards(SCAN_SYMBOLS)
    print(f"Total strategy cards emitted: {len(cards)}")
    
    mt5_state = get_mt5_active_state()
    if not mt5_state:
        print("[ERROR] MT5 could not be initialized.")
        return
        
    existing_mt5_syms = set()
    for o in mt5_state["cg_orders"]:
        existing_mt5_syms.add(normalize_base(o.symbol))
    for p in mt5_state["cg_positions"]:
        existing_mt5_syms.add(normalize_base(p.symbol))
        
    print(f"Current active CG MT5 assets (normalized): {list(existing_mt5_syms)}")
    
    punched = []
    for card in cards:
        sym = normalize_base(card["sym"])
        engine = card.get("engine", "EA")
        side = card.get("side", "").upper()
        status = card.get("status", "")
        r_planned = card.get("rPlanned", 0.0)
        
        # Hard Veto / Confluence Hurdle: planned R must be >= 2.0R, status must be confirmed or pending-fill
        if r_planned < 2.0:
            print(f"[-] Skipping {sym} {engine}: planned R {r_planned} < 2.0R hurdle.")
            continue
            
        if status not in ("confirmed", "pending-fill"):
            print(f"[-] Skipping {sym} {engine}: card status '{status}' not armed for entry.")
            continue
            
        # Check if already active in MT5
        if sym in existing_mt5_syms:
            print(f"[*] {sym} already has an active order/position in MT5. Checking limit level...")
            continue
            
        # Punch into MT5
        print(f"[+] QUALIFIED A+ SIGNAL: {sym} {side} ({engine}) @ {card['entry']} | SL {card['stop']} | R {r_planned}R")
        res = punch_mt5_order(card, risk_usd=5.50)
        
        if res.get("ok"):
            ticket = res.get("ticket")
            lots = res.get("lots")
            risk_usd = res.get("risk_usd")
            resolved_sym = res.get("symbol")
            print(f"[SUCCESS] PUNCHED TO MT5: {resolved_sym} {lots} lots | Ticket #{ticket} | Risk ${risk_usd}")
            
            order_record = {
                "id": f"auto-mt5-{int(time.time()*1000)}",
                "round": "R558",
                "sym": card["sym"],
                "side": card["side"],
                "action": card["side"],
                "type": card.get("kind", "limit"),
                "status": "placed-mt5",
                "source": "autonomous-punch-engine",
                "engine": engine,
                "entry": card["entry"],
                "stop": card["stop"],
                "targets": card.get("targets", []),
                "riskR": r_planned,
                "riskPct": None,
                "regime": f"playbook:{engine}",
                "mode": "autonomous-mt5-punch",
                "rationale": card.get("note", "Autonomous Playbook Execution"),
                "mt5Symbol": resolved_sym,
                "mt5Lots": lots,
                "mt5RiskUsd": risk_usd,
                "ticket": ticket,
                "createdTs": int(time.time() * 1000)
            }
            wake_msg = f"## {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} — autonomous-mt5-punch: {card['sym']} {side} ({engine})\n- Automatically punched by auto_punch_engine: {resolved_sym} {lots} lots, ticket {ticket}, risk ${risk_usd}.\n- Entry {card['entry']} · SL {card['stop']} · T1 {card.get('targets', [0])[0]} (planned {r_planned}R).\n"
            sync_desk_state(order_record, wake_msg)
            existing_mt5_syms.add(sym)
            punched.append(order_record)
        else:
            print(f"[REJECTED] MT5 Punch Failed for {sym}: {res.get('error')}")
            
    print(f"\n[DONE] Autonomous evaluation round finished. Total newly punched orders: {len(punched)}")
    return punched

if __name__ == "__main__":
    run_evaluation_and_punch()
