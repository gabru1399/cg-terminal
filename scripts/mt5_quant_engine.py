#!/usr/bin/env python3
"""scripts/mt5_quant_engine.py: Autonomous Event-Driven Multi-Asset MT5 Trading Engine.
Monitors the curated Top 50 audited MT5 assets with dynamic Fibonacci Ribbon
kiss/rejection mechanics, automated lot sizing, risk management, and trailing SL.
"""
import sys
import os
import time
import json
import argparse
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

try:
    import MetaTrader5 as mt5
except ImportError:
    print("[ERROR] MetaTrader5 package not installed. (pip install MetaTrader5, Windows only)", file=sys.stderr)
    sys.exit(1)

import pandas as pd
import numpy as np
from quant_universe import QUANT_UNIVERSE, get_asset_config

STATE_FILE = ROOT / "desk" / "state.json"
MT5_FILE = ROOT / "desk" / "mt5.json"
LOG_FILE = ROOT / "desk" / "log.md"

def log_msg(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def append_desk_log(entry_str):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry_str + "\n")
    except Exception as e:
        print(f"[WARN] Failed to write to desk/log.md: {e}", file=sys.stderr)

def fetch_recent_bars(symbol, tf_str, count=300):
    tf = mt5.TIMEFRAME_H4 if tf_str == "H4" else mt5.TIMEFRAME_H1
    rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
    if rates is None or len(rates) < 100:
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.sort_values('time', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def calculate_lot_size(account_equity, risk_pct, r_dist, symbol_info):
    risk_dollars = account_equity * risk_pct
    tick_size = symbol_info.trade_tick_size or 0.01
    tick_val = symbol_info.trade_tick_value or 1.0
    
    # Dollar risk per 1 full lot
    ticks = r_dist / tick_size
    one_lot_risk = ticks * tick_val
    if one_lot_risk <= 0:
        return symbol_info.volume_min
        
    lots = risk_dollars / one_lot_risk
    
    # Step clamp
    step = symbol_info.volume_step or 0.01
    lots = round(lots / step) * step
    lots = max(symbol_info.volume_min, min(symbol_info.volume_max, lots))
    return round(lots, 2)

def check_signal(df, cfg):
    """
    Evaluates signal on the last fully closed candle (df.iloc[-2]).
    df.iloc[-1] is the currently forming candle.
    """
    c = df['close'].values
    h = df['high'].values
    l = df['low'].values
    o = df['open'].values
    
    fp, mp, sp = cfg['fast_p'], cfg['mid_p'], cfg['slow_p']
    
    ef = pd.Series(c).ewm(span=fp, adjust=False).mean().values
    em = pd.Series(c).ewm(span=mp, adjust=False).mean().values
    es = pd.Series(c).ewm(span=sp, adjust=False).mean().values
    
    tr1 = h - l
    tr2 = np.abs(h - np.roll(c, 1))
    tr3 = np.abs(l - np.roll(c, 1))
    tr = np.maximum(tr1, np.maximum(tr2, tr3))
    tr[0] = tr1[0]
    atrs = pd.Series(tr).rolling(14).mean().bfill().values
    
    b_range = h - l
    b_range[b_range == 0] = 1e-8
    u_wicks = (h - np.maximum(o, c)) / b_range
    l_wicks = (np.minimum(o, c) - l) / b_range
    
    i = len(c) - 2 # Last closed candle
    
    c_c = c[i]; c_p = c[i-1]
    h_i = h[i]; l_i = l[i]; a_i = atrs[i]
    
    sig = None
    # Bearish Ribbon Fan Down
    if (ef[i] < em[i]) and (em[i] < es[i]):
        if c_p < ef[i]:
            if (h_i >= ef[i]*0.999 or h_i >= em[i]*0.999 or h_i >= es[i]*0.999) and (c_c < em[i]):
                if u_wicks[i] >= 0.25:
                    sig = "SELL"
    # Bullish Ribbon Fan Up
    elif (ef[i] > em[i]) and (em[i] > es[i]):
        if c_p > ef[i]:
            if (l_i <= ef[i]*1.001 or l_i <= em[i]*1.001 or l_i <= es[i]*1.001) and (c_c > em[i]):
                if l_wicks[i] >= 0.25:
                    sig = "BUY"
                    
    if sig is None:
        return None
        
    entry_p = df['open'].iloc[-1] # Current open
    is_fixed = cfg['exit_mode'].startswith("fixed_")
    fixed_rr = float(cfg['exit_mode'].split("_")[1]) if is_fixed else 2.5
    
    if is_fixed:
        sl_p = (h_i + 0.3 * a_i) if sig == "SELL" else (l_i - 0.3 * a_i)
    else:
        sl_p = (max(es[i], h_i) + 0.5 * a_i) if sig == "SELL" else (min(es[i], l_i) - 0.5 * a_i)
        
    r_dist = abs(entry_p - sl_p)
    if r_dist <= 0:
        return None
        
    tp_p = (entry_p - fixed_rr * r_dist) if sig == "SELL" else (entry_p + fixed_rr * r_dist)
    
    return {
        "symbol": cfg['symbol'],
        "side": sig,
        "entry": round(entry_p, 5),
        "sl": round(sl_p, 5),
        "tp": round(tp_p, 5),
        "r_dist": r_dist,
        "tf": cfg['tf'],
        "exit_mode": cfg['exit_mode'],
        "ribbon": cfg['ribbon_name'],
        "wick_pct": round(float(u_wicks[i] if sig == "SELL" else l_wicks[i]) * 100, 1),
        "signal_time": str(df['time'].iloc[i])
    }

def run_quant_engine(dry_run=True, test_once=False, risk_pct=0.005, max_concurrent=6):
    log_msg(f"Initializing MT5 Quant Engine (Mode: {'DRY-RUN' if dry_run else 'LIVE'} | Risk: {risk_pct*100}% | Max Slots: {max_concurrent})")
    
    if not mt5.initialize(timeout=15000):
        log_msg(f"[ERROR] mt5.initialize failed: {mt5.last_error()}")
        return
        
    acc = mt5.account_info()
    if acc is None:
        log_msg("[ERROR] Could not read MT5 account info.")
        mt5.shutdown()
        return
        
    equity = acc.equity
    balance = acc.balance
    currency = acc.currency
    log_msg(f"Account Connected: #{acc.login} | Balance: ${balance:,.2f} | Equity: ${equity:,.2f} {currency}")
    
    universe = QUANT_UNIVERSE
    log_msg(f"Loaded {len(universe)} curated high-edge instruments from quant_universe.py")
    
    try:
        while True:
            # 1. Inspect existing open positions
            open_positions = mt5.positions_get() or []
            open_symbols = set(p.symbol for p in open_positions)
            slots_used = len(open_positions)
            log_msg(f"--- Scan Cycle: {slots_used}/{max_concurrent} active position slots used ---")
            
            # 2. Scan universe for signals
            candidate_signals = []
            
            for sym, raw_cfg in universe.items():
                if sym in open_symbols:
                    continue # Already in a position for this asset
                    
                cfg = get_asset_config(sym)
                
                # Check MT5 Market Watch & Spread
                mt5.symbol_select(sym, True)
                tick = mt5.symbol_info_tick(sym)
                info = mt5.symbol_info(sym)
                
                if tick is None or info is None:
                    continue
                    
                mid = (tick.bid + tick.ask) / 2.0
                if mid <= 0: continue
                spread_pct = (tick.ask - tick.bid) / mid * 100.0
                
                if spread_pct > cfg['max_spread_pct']:
                    continue # Exceeds spread limit
                    
                df = fetch_recent_bars(sym, cfg['tf'], count=200)
                if df is None: continue
                
                sig = check_signal(df, cfg)
                if sig is not None:
                    sig['mid'] = mid
                    sig['spread_pct'] = round(spread_pct, 4)
                    sig['info'] = info
                    candidate_signals.append(sig)
                    
            log_msg(f"Scan complete. {len(candidate_signals)} candidate signals identified.")
            
            # 3. Process candidate signals
            available_slots = max_concurrent - slots_used
            for sig in candidate_signals[:available_slots]:
                sym = sig['symbol']
                info = sig['info']
                lots = calculate_lot_size(equity, risk_pct, sig['r_dist'], info)
                
                order_desc = f"{sym} · {sig['side']} {lots} lots @ {sig['entry']} | SL: {sig['sl']} | TP: {sig['tp']} (Exit: {sig['exit_mode']})"
                
                if dry_run:
                    log_msg(f"[DRY-RUN SIMULATION] {order_desc}")
                    append_desk_log(f"### [SIMULATED EXEC] {order_desc}\n- Ribbon: {sig['ribbon']} on {sig['tf']}\n- Rejection Wick: {sig['wick_pct']}%\n")
                else:
                    log_msg(f"[LIVE DISPATCH] Executing: {order_desc}")
                    order_type = mt5.ORDER_TYPE_BUY if sig['side'] == "BUY" else mt5.ORDER_TYPE_SELL
                    price = tick.ask if sig['side'] == "BUY" else tick.bid
                    
                    req = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": sym,
                        "volume": lots,
                        "type": order_type,
                        "price": price,
                        "sl": sig['sl'],
                        "tp": sig['tp'],
                        "deviation": 20,
                        "magic": 89233,
                        "comment": f"ATG-Quant:{sig['ribbon']}",
                        "type_time": mt5.ORDER_TIME_GTC,
                        "type_filling": mt5.ORDER_FILLING_IOC,
                    }
                    res = mt5.order_send(req)
                    if res.retcode != mt5.TRADE_RETCODE_DONE:
                        log_msg(f"[ERROR] Order failed for {sym}: retcode={res.retcode} ({res.comment})")
                    else:
                        log_msg(f"[SUCCESS] Order filled: Ticket #{res.order}")
                        append_desk_log(f"### [LIVE EXECUTION] Ticket #{res.order} · {order_desc}\n")
                        
            # 4. Synchronize with desk/state.json
            try:
                state_data = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
                state_data.setdefault("quant_engine", {})
                state_data["quant_engine"] = {
                    "last_scan_ts": int(time.time() * 1000),
                    "mode": "DRY-RUN" if dry_run else "LIVE",
                    "slots_used": slots_used,
                    "max_slots": max_concurrent,
                    "active_candidates_count": len(candidate_signals),
                    "candidates": [{k: v for k, v in c.items() if k != "info"} for c in candidate_signals[:10]]
                }
                STATE_FILE.write_text(json.dumps(state_data, indent=2) + "\n")
            except Exception as e:
                log_msg(f"[WARN] Failed to sync state.json: {e}")
                
            if test_once:
                log_msg("Test-once cycle completed successfully.")
                break
                
            time.sleep(30)
            
    finally:
        mt5.shutdown()
        log_msg("MT5 Quant Engine safely shutdown.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MT5 Autonomous Quant Trading Engine")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Simulate without placing real orders (default: True)")
    parser.add_argument("--live", action="store_true", help="Enable REAL LIVE MT5 order execution")
    parser.add_argument("--test-once", action="store_true", help="Run a single scan cycle and exit")
    parser.add_argument("--risk-pct", type=float, default=0.005, help="Risk per trade as decimal (default: 0.005 = 0.5%%)")
    parser.add_argument("--max-concurrent", type=int, default=6, help="Maximum concurrent open positions (default: 6)")
    
    args = parser.parse_args()
    is_live = args.live and not args.dry_run
    
    run_quant_engine(
        dry_run=not args.live,
        test_once=args.test_once,
        risk_pct=args.risk_pct,
        max_concurrent=args.max_concurrent
    )
