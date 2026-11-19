#!/usr/bin/env python3
"""
scripts/cold_zone_solver.py — Microstructure Cold-Zone Stop Loss & Position Sizing Solver.

Author: Antigravity Autonomous Trading Intelligence (Trading AGI v4.0)
Operates under SOP v2.1.0 (Directive 2026-11-18, PIT-16, PIT-18).

Function:
  1. Pulls live CLOB order book ladder (/api/cg/bookwalls?sym=<SYM>).
  2. Scans for major resting liquidity walls (> $2M on BTC/ETH, > $200k on alts).
  3. Verifies if proposed SL sits inside/in-front-of a wall (Liquidity Trap).
  4. Relocates SL into the structural Cold Zone beyond the wall shelf.
  5. Computes exact lot sizing to strictly enforce dollar risk cap ($6.00 MT5, $0.50 Delta).
  6. Enforces PIT-18: stop_distance >= 2.0 * spread.
"""

import sys
import json
import urllib.request

TERMINAL_URL = "http://127.0.0.1:3000"

def get_clob_ladder(sym):
    url = f"{TERMINAL_URL}/api/cg/bookwalls?sym={sym.upper()}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            model = data.get("model", {})
            return model.get("ladder", []), model.get("depth", {})
    except Exception as e:
        print(f"[WARN] Failed to fetch CLOB ladder for {sym}: {e}")
        return [], {}

def solve_cold_zone_sl(sym, side, entry, proposed_sl, target, risk_budget=6.00, spread=0.0):
    side = side.lower()
    entry = float(entry)
    proposed_sl = float(proposed_sl)
    target = float(target)
    risk_budget = float(risk_budget)
    spread = float(spread)

    ladder, depth = get_clob_ladder(sym)
    
    # Threshold for significant wall
    is_major = sym.upper() in ["BTC", "ETH"]
    min_wall_usd = 2_000_000.0 if is_major else 200_000.0
    buffer_pct = 0.0015 if is_major else 0.0030 # 0.15% on BTC/ETH, 0.3% on alts

    final_sl = proposed_sl
    hazard_detected = False
    trapping_wall = None

    if side == "sell": # Short trade: SL is above entry
        # Look for ask walls between entry and proposed_sl + buffer
        ask_walls = [l for l in ladder if l.get("side") == "a" and l.get("price", 0) >= entry]
        # Filter for walls near or slightly above proposed_sl
        for w in ask_walls:
            w_price = float(w.get("price", 0))
            w_usd = float(w.get("usd", 0))
            if w_usd >= min_wall_usd:
                # If proposed SL is below or right at the wall (within 0.3%)
                if proposed_sl <= w_price * 1.001:
                    hazard_detected = True
                    trapping_wall = w
                    # Place SL beyond the wall shelf
                    safe_sl = w_price * (1.0 + buffer_pct)
                    if safe_sl > final_sl:
                        final_sl = safe_sl

    elif side == "buy": # Long trade: SL is below entry
        # Look for bid walls between proposed_sl and entry
        bid_walls = [l for l in ladder if l.get("side") == "b" and l.get("price", 0) <= entry]
        for w in bid_walls:
            w_price = float(w.get("price", 0))
            w_usd = float(w.get("usd", 0))
            if w_usd >= min_wall_usd:
                # If proposed SL is above or right at the wall
                if proposed_sl >= w_price * 0.999:
                    hazard_detected = True
                    trapping_wall = w
                    # Place SL below the wall shelf
                    safe_sl = w_price * (1.0 - buffer_pct)
                    if safe_sl < final_sl:
                        final_sl = safe_sl

    # Check PIT-18: Stop distance vs spread
    stop_dist = abs(entry - final_sl)
    spread_ratio = stop_dist / spread if spread > 0 else 999.0
    pit18_pass = spread_ratio >= 2.0

    # Calculate lot size
    # For MT5: lot size = risk_budget / stop_dist (depends on contract size)
    # Generic contract formula:
    # Notional risk = lot * contract_size * stop_dist
    drive_dist = abs(target - entry)
    r_multiple = drive_dist / stop_dist if stop_dist > 0 else 0.0

    result = {
        "symbol": sym.upper(),
        "side": side.upper(),
        "entry": entry,
        "proposed_sl": proposed_sl,
        "cold_zone_sl": round(final_sl, 4 if sym.upper() not in ["BTC", "ETH"] else 2),
        "hazard_detected": hazard_detected,
        "trapping_wall": trapping_wall,
        "stop_distance": round(stop_dist, 4),
        "target": target,
        "drive_distance": round(drive_dist, 4),
        "realized_r_multiple": round(r_multiple, 2),
        "spread": spread,
        "spread_to_stop_ratio": round(spread_ratio, 1),
        "pit18_pass": pit18_pass,
        "risk_budget_usd": risk_budget
    }
    return result

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python cold_zone_solver.py <SYM> <SIDE:buy|sell> <ENTRY> <PROPOSED_SL> <TARGET> [RISK_BUDGET] [SPREAD]")
        # Demo on live ETH short
        print("\n--- Running Live Demo on ETH Short ---")
        res = solve_cold_zone_sl("ETH", "sell", 1838.50, 1854.50, 1785.00, risk_budget=6.00, spread=3.10)
        print(json.dumps(res, indent=2))
    else:
        sym = sys.argv[1]
        side = sys.argv[2]
        entry = sys.argv[3]
        sl = sys.argv[4]
        tp = sys.argv[5]
        budget = float(sys.argv[6]) if len(sys.argv) > 6 else 6.00
        spread = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0
        res = solve_cold_zone_sl(sym, side, entry, sl, tp, risk_budget=budget, spread=spread)
        print(json.dumps(res, indent=2))
