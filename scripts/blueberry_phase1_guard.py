#!/usr/bin/env python3
"""
scripts/blueberry_phase1_guard.py — Blueberry Funded Phase 1 Target Invariant Monitor & Executioner.

Target: $2,700.00 Equity (+$200 profit on $2,500 initial balance).
Invariant: As soon as account equity >= $2,700.00, immediately:
  1. Liquidate all active positions (market close) to lock in profit / crystallize cash.
  2. Cancel all resting limit / pending orders.
  3. Write persistent achievement manifest to desk/PHASE1_ACHIEVED.json.
  4. Log event to desk/log.md and desk/inbox/WAKE.md.
"""

import sys
import os
import json
import time
from datetime import datetime, timezone

try:
    import MetaTrader5 as mt5
except ImportError:
    print(json.dumps({"ok": False, "error": "MetaTrader5 not installed"}))
    sys.exit(1)

TARGET_EQUITY_USD = 2700.00
DESK_LOG_PATH = "desk/log.md"
WAKE_PATH = "desk/inbox/WAKE.md"
ACHIEVEMENT_PATH = "desk/PHASE1_ACHIEVED.json"

def check_and_enforce_phase1(close_all_if_achieved=True):
    if not mt5.initialize(timeout=15_000):
        return {"ok": False, "error": f"mt5.initialize failed: {mt5.last_error()}"}
    
    try:
        acc = mt5.account_info()
        if not acc:
            return {"ok": False, "error": f"mt5.account_info failed: {mt5.last_error()}"}
        
        equity = float(acc.equity)
        balance = float(acc.balance)
        profit = float(acc.profit)
        
        positions = mt5.positions_get() or ()
        orders = mt5.orders_get() or ()
        
        status = {
            "ok": True,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "login": acc.login,
            "balance": balance,
            "equity": equity,
            "floating_profit": profit,
            "target_equity": TARGET_EQUITY_USD,
            "distance_to_target": round(TARGET_EQUITY_USD - equity, 2),
            "phase1_achieved": equity >= TARGET_EQUITY_USD,
            "open_positions_count": len(positions),
            "pending_orders_count": len(orders)
        }
        
        if equity >= TARGET_EQUITY_USD and close_all_if_achieved:
            print(f"\n🔥🔥🔥 [PHASE 1 TARGET ACHIEVED] Equity: ${equity:.2f} >= ${TARGET_EQUITY_USD:.2f}! Bagging all cash now...")
            
            closed_positions = []
            for p in positions:
                sym_info = mt5.symbol_info(p.symbol)
                tick = mt5.symbol_info_tick(p.symbol)
                if not tick or not sym_info:
                    print(f"[WARN] Could not get tick/info for {p.symbol}")
                    continue
                
                close_type = mt5.ORDER_TYPE_SELL if p.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
                close_price = tick.bid if p.type == mt5.ORDER_TYPE_BUY else tick.ask
                
                filling_type = mt5.ORDER_FILLING_IOC
                if hasattr(sym_info, "filling_mode"):
                    if sym_info.filling_mode & 1:
                        filling_type = mt5.ORDER_FILLING_FOK
                    elif sym_info.filling_mode & 2:
                        filling_type = mt5.ORDER_FILLING_IOC
                
                req = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "position": p.ticket,
                    "symbol": p.symbol,
                    "volume": p.volume,
                    "type": close_type,
                    "price": close_price,
                    "deviation": 30,
                    "magic": p.magic,
                    "comment": "phase1_target_achieved",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": filling_type,
                }
                res = mt5.order_send(req)
                closed_positions.append({
                    "ticket": p.ticket,
                    "symbol": p.symbol,
                    "volume": p.volume,
                    "retcode": getattr(res, "retcode", None),
                    "comment": getattr(res, "comment", None)
                })
                print(f"  -> Closed position #{p.ticket} {p.symbol} {p.volume} lots: retcode={getattr(res, 'retcode', None)}")
                time.sleep(0.1)
                
            cancelled_orders = []
            for o in orders:
                req = {
                    "action": mt5.TRADE_ACTION_REMOVE,
                    "order": o.ticket,
                    "comment": "phase1_cancel_all"
                }
                res = mt5.order_send(req)
                cancelled_orders.append({
                    "ticket": o.ticket,
                    "symbol": o.symbol,
                    "retcode": getattr(res, "retcode", None)
                })
                print(f"  -> Cancelled order #{o.ticket} {o.symbol}: retcode={getattr(res, 'retcode', None)}")
                time.sleep(0.1)
                
            # Re-read account state after closure
            acc_post = mt5.account_info()
            status["final_balance"] = getattr(acc_post, "balance", balance)
            status["final_equity"] = getattr(acc_post, "equity", equity)
            status["closed_positions"] = closed_positions
            status["cancelled_orders"] = cancelled_orders
            
            # Persist Phase 1 Achievement Manifest
            with open(ACHIEVEMENT_PATH, "w", encoding="utf-8") as f:
                json.dump(status, f, indent=2)
                
            wake_msg = (
                f"\n## {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} — 🏆 BLUEBERRY FUNDED PHASE 1 TARGET ACHIEVED!\n"
                f"- **Final Balance**: ${status['final_balance']:.2f}\n"
                f"- **Final Equity**: ${status['final_equity']:.2f} (Target: ${TARGET_EQUITY_USD:.2f})\n"
                f"- **Action**: Closed {len(closed_positions)} positions, cancelled {len(cancelled_orders)} pending orders.\n"
                f"- **Phase 1 Status**: PASSED. Cash bagged. Trading halted.\n"
            )
            with open(WAKE_PATH, "a", encoding="utf-8") as f:
                f.write(wake_msg)
            with open(DESK_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(wake_msg)
                
        return status
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    close_flag = "--close-if-achieved" in sys.argv or "--enforce" in sys.argv
    res = check_and_enforce_phase1(close_all_if_achieved=close_flag)
    print(json.dumps(res, indent=2))
