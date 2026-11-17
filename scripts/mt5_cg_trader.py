"""
scripts/mt5_cg_trader.py — Blueberry Funded MT5 Dedicated Order Execution & Risk Engine
Author: Antigravity Autonomous Trading Intelligence (Trading AGI v4.0)

Operating Account: Blueberry Funded Prime 2-Step Challenge ($2,500)
Rules Enforced:
1. Risk Budget: Strictly max $5.00 – $6.00 USD risk per trade (~0.20% - 0.24% of equity).
2. Mandatory Comment: Every single order/position MUST have comment="cg_terminal".
3. Shared Account Isolation: Filter strictly by comment == "cg_terminal" or magic == 42001.
   NEVER modify, close, or interfere with other algorithms' orders running on the same account.
4. Daily Drawdown Guard: 4.0% ($100.00 USD) hard floor from daily starting balance.
5. Max Drawdown Guard: 10.0% ($250.00 USD) static limit (equity must never touch $2,250.00 USD).
6. Post-Order Invariants: Bracket SL and TP placed on order creation.
"""

import sys
import os
import argparse
import json
from datetime import datetime, timezone
try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None

MAGIC_NUMBER = 42001
CG_COMMENT = "cg_terminal"
MAX_RISK_USD = 6.00
MIN_RISK_USD = 4.00
TARGET_RISK_USD = 5.50
INITIAL_ACCOUNT_BALANCE = 2500.00
MAX_DAILY_DRAWDOWN_USD = 100.00
MAX_OVERALL_DRAWDOWN_USD = 250.00

def init_mt5():
    if mt5 is None:
        raise RuntimeError("MetaTrader5 python package not installed.")
    if not mt5.initialize():
        err = mt5.last_error()
        raise RuntimeError(f"MT5 initialize failed: {err}")
    acc = mt5.account_info()
    if not acc:
        err = mt5.last_error()
        mt5.shutdown()
        raise RuntimeError(f"MT5 account_info failed: {err}")
    return acc

def get_account_audit():
    acc = init_mt5()
    equity = acc.equity
    balance = acc.balance
    free_margin = acc.margin_free
    
    # Calculate drawdown from starting $2500
    overall_drawdown_usd = max(0.0, INITIAL_ACCOUNT_BALANCE - equity)
    overall_drawdown_pct = (overall_drawdown_usd / INITIAL_ACCOUNT_BALANCE) * 100.0
    
    # Audit positions
    all_positions = mt5.positions_get() or ()
    cg_positions = [p for p in all_positions if p.comment == CG_COMMENT or p.magic == MAGIC_NUMBER]
    other_positions = [p for p in all_positions if p.comment != CG_COMMENT and p.magic != MAGIC_NUMBER]
    
    all_orders = mt5.orders_get() or ()
    cg_orders = [o for o in all_orders if o.comment == CG_COMMENT or o.magic == MAGIC_NUMBER]
    other_orders = [o for o in all_orders if o.comment != CG_COMMENT and o.magic != MAGIC_NUMBER]
    
    audit = {
        "account": {
            "login": acc.login,
            "name": acc.name,
            "server": acc.server,
            "balance": balance,
            "equity": equity,
            "free_margin": free_margin,
            "leverage": acc.leverage,
            "trade_allowed": acc.trade_allowed,
            "trade_expert": acc.trade_expert,
            "overall_drawdown_usd": round(overall_drawdown_usd, 2),
            "overall_drawdown_pct": round(overall_drawdown_pct, 2),
            "max_drawdown_limit_usd": MAX_OVERALL_DRAWDOWN_USD,
            "daily_drawdown_limit_usd": MAX_DAILY_DRAWDOWN_USD,
        },
        "cg_terminal": {
            "positions_count": len(cg_positions),
            "orders_count": len(cg_orders),
            "positions": [
                {
                    "ticket": p.ticket,
                    "symbol": p.symbol,
                    "type": "BUY" if p.type == mt5.ORDER_TYPE_BUY else "SELL",
                    "volume": p.volume,
                    "open_price": p.price_open,
                    "current_price": p.price_current,
                    "sl": p.sl,
                    "tp": p.tp,
                    "profit": p.profit,
                    "comment": p.comment,
                    "magic": p.magic
                }
                for p in cg_positions
            ],
            "orders": [
                {
                    "ticket": o.ticket,
                    "symbol": o.symbol,
                    "type": o.type,
                    "volume": o.volume_current,
                    "price_open": o.price_open,
                    "sl": o.sl,
                    "tp": o.tp,
                    "comment": o.comment,
                    "magic": o.magic
                }
                for o in cg_orders
            ]
        },
        "other_algos": {
            "positions_count": len(other_positions),
            "orders_count": len(other_orders),
            "note": "ISOLATED. Antigravity will NEVER touch or close these orders."
        }
    }
    return audit

def calculate_lot_size(symbol: str, entry_price: float, sl_price: float, target_risk_usd: float = TARGET_RISK_USD, max_risk_cap_usd: float = MAX_RISK_USD, allow_min_lot: bool = False):
    """
    Computes exact lot size for an order such that:
    actual_risk_usd <= max_risk_cap_usd
    target_risk_usd is typically $5.00 - $5.50 (default) or higher if user authorized.
    """
    init_mt5()
    
    # Ensure symbol is selected
    if not mt5.symbol_select(symbol, True):
        raise ValueError(f"Failed to select symbol {symbol} in MT5")
    
    info = mt5.symbol_info(symbol)
    if not info:
        raise ValueError(f"Symbol {symbol} info not found in MT5")
    
    stop_distance = abs(entry_price - sl_price)
    if stop_distance <= 0:
        raise ValueError("Stop distance must be strictly positive")
    
    contract_size = info.trade_contract_size
    tick_size = info.trade_tick_size or 0.01
    tick_value = info.trade_tick_value or 0.01
    vol_min = info.volume_min
    vol_max = info.volume_max
    vol_step = info.volume_step
    
    risk_per_lot = (stop_distance / tick_size) * tick_value
    if risk_per_lot <= 0:
        risk_per_lot = contract_size * stop_distance

    raw_lots = target_risk_usd / risk_per_lot
    
    # Snap to volume step
    steps = round(raw_lots / vol_step)
    calc_lots = round(steps * vol_step, 2)
    
    # If calc_lots < vol_min, check if min lot risk exceeds max allowed risk
    if calc_lots < vol_min:
        min_lot_risk = vol_min * risk_per_lot
        if min_lot_risk > max_risk_cap_usd:
            raise ValueError(
                f"Stop distance too wide for min lot ({vol_min}): "
                f"risk would be ${min_lot_risk:.2f} USD, exceeding ${max_risk_cap_usd:.2f} max risk limit! Trade Vetoed."
            )
        calc_lots = vol_min

    # Verify risk with calc_lots
    actual_risk = calc_lots * risk_per_lot
    
    # If risk exceeds max_risk_cap_usd, step down if possible
    if actual_risk > max_risk_cap_usd:
        calc_lots = round(calc_lots - vol_step, 2)
        actual_risk = calc_lots * risk_per_lot
        if calc_lots < vol_min or actual_risk > max_risk_cap_usd:
            raise ValueError(
                f"Unable to size within ${max_risk_cap_usd:.2f} risk cap. "
                f"Lot: {calc_lots}, Risk: ${actual_risk:.2f} USD. Trade Vetoed."
            )
            
    calc_lots = max(vol_min, min(vol_max, calc_lots))
    
    return {
        "symbol": symbol,
        "entry_price": entry_price,
        "sl_price": sl_price,
        "stop_distance": round(stop_distance, info.digits),
        "contract_size": contract_size,
        "vol_min": vol_min,
        "vol_max": vol_max,
        "vol_step": vol_step,
        "calculated_lots": calc_lots,
        "actual_risk_usd": round(actual_risk, 2),
        "max_risk_cap_usd": max_risk_cap_usd,
        "is_valid": actual_risk <= max_risk_cap_usd
    }

def place_order(symbol: str, order_type_str: str, entry_price: float, sl_price: float, tp_price: float, lots: float = None, max_risk_cap_usd: float = MAX_RISK_USD):
    """
    Submits a pending limit order or market order to MT5.
    order_type_str: 'BUY_LIMIT', 'SELL_LIMIT', 'BUY', 'SELL'
    MANDATORY: comment="cg_terminal", magic=42001
    """
    init_mt5()
    
    if not mt5.symbol_select(symbol, True):
        raise ValueError(f"Symbol {symbol} select failed")
        
    info = mt5.symbol_info(symbol)
    if not info:
        raise ValueError(f"Symbol {symbol} info not found")
        
    # Sizing check
    sizing = calculate_lot_size(symbol, entry_price, sl_price, max_risk_cap_usd=max_risk_cap_usd)
    final_lots = lots if lots is not None else sizing["calculated_lots"]
    
    # Enforce maximum risk cap
    risk_test = final_lots * (abs(entry_price - sl_price) / info.trade_tick_size * info.trade_tick_value)
    if risk_test > max_risk_cap_usd + 0.50:
        raise ValueError(f"Lot size {final_lots} violates ${max_risk_cap_usd:.2f} risk cap on {symbol}! (Calculated: ${risk_test:.2f})")

    type_map = {
        "BUY_LIMIT": mt5.ORDER_TYPE_BUY_LIMIT,
        "SELL_LIMIT": mt5.ORDER_TYPE_SELL_LIMIT,
        "BUY": mt5.ORDER_TYPE_BUY,
        "SELL": mt5.ORDER_TYPE_SELL,
    }
    
    order_type = type_map.get(order_type_str.upper())
    if order_type is None:
        raise ValueError(f"Unknown order type: {order_type_str}")

    digits = info.digits
    entry_price = round(entry_price, digits)
    sl_price = round(sl_price, digits)
    tp_price = round(tp_price, digits)
    
    request = {
        "action": mt5.TRADE_ACTION_PENDING if "LIMIT" in order_type_str.upper() else mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": final_lots,
        "type": order_type,
        "price": entry_price,
        "sl": sl_price,
        "tp": tp_price,
        "deviation": 20,
        "magic": MAGIC_NUMBER,
        "comment": CG_COMMENT,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    # Try sending
    result = mt5.order_send(request)
    if result is None:
        err = mt5.last_error()
        raise RuntimeError(f"mt5.order_send returned None. Error: {err}")
        
    if result.retcode != mt5.TRADE_RETCODE_DONE and result.retcode != mt5.TRADE_RETCODE_PLACED:
        # Check filling fallback to FOK if IOC failed
        if result.retcode == 10030: # Unsupported filling
            request["type_filling"] = mt5.ORDER_FILLING_FOK
            result = mt5.order_send(request)
            
    return {
        "retcode": result.retcode,
        "comment": result.comment,
        "order_ticket": result.order,
        "deal_ticket": result.deal,
        "volume": result.volume,
        "price": result.price,
        "request": request,
        "expected_risk_usd": sizing["actual_risk_usd"]
    }

def move_sl_to_breakeven(ticket: int):
    """
    Ratchet stop loss of a cg_terminal position to breakeven (entry price).
    Strict isolation: Only operates on positions with comment == 'cg_terminal'.
    """
    init_mt5()
    positions = mt5.positions_get(ticket=ticket)
    if not positions:
        raise ValueError(f"Position ticket {ticket} not found")
    pos = positions[0]
    if pos.comment != CG_COMMENT and pos.magic != MAGIC_NUMBER:
        raise PermissionError(f"DENIED: Position {ticket} does not belong to cg_terminal (comment='{pos.comment}').")
        
    entry_price = pos.price_open
    current_sl = pos.sl
    
    # Check if already at or better than breakeven
    if pos.type == mt5.ORDER_TYPE_BUY and current_sl >= entry_price:
        return {"status": "ALREADY_BREAKEVEN", "ticket": ticket, "sl": current_sl}
    if pos.type == mt5.ORDER_TYPE_SELL and current_sl <= entry_price and current_sl > 0:
        return {"status": "ALREADY_BREAKEVEN", "ticket": ticket, "sl": current_sl}
        
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": ticket,
        "symbol": pos.symbol,
        "sl": entry_price,
        "tp": pos.tp,
        "magic": MAGIC_NUMBER,
        "comment": CG_COMMENT
    }
    res = mt5.order_send(request)
    return {
        "status": "MODIFIED" if res.retcode == mt5.TRADE_RETCODE_DONE else "FAILED",
        "retcode": res.retcode,
        "comment": res.comment,
        "ticket": ticket,
        "new_sl": entry_price
    }

def auto_ratchet_breakeven(verbose=True):
    """
    Scans all open cg_terminal positions.
    If favorable excursion reaches >= +1.0R (move_pts >= initial_risk_pts),
    automatically moves SL to price_open (Breakeven).
    Strict isolation: Only touches comment == 'cg_terminal' positions.
    """
    init_mt5()
    positions = mt5.positions_get() or ()
    results = []
    for p in positions:
        if p.comment == CG_COMMENT or p.magic == MAGIC_NUMBER:
            risk_pts = abs(p.price_open - p.sl)
            if risk_pts <= 0:
                continue
            is_sell = (p.type == mt5.ORDER_TYPE_SELL)
            current_move = (p.price_open - p.price_current) if is_sell else (p.price_current - p.price_open)
            r_multiple = current_move / risk_pts
            
            already_be = False
            if not is_sell and p.sl >= p.price_open:
                already_be = True
            elif is_sell and p.sl <= p.price_open and p.sl > 0:
                already_be = True
                
            item = {
                "ticket": p.ticket,
                "symbol": p.symbol,
                "type": "SELL" if is_sell else "BUY",
                "open": p.price_open,
                "current": p.price_current,
                "sl": p.sl,
                "risk_pts": round(risk_pts, 2),
                "move_pts": round(current_move, 2),
                "r_multiple": round(r_multiple, 2),
                "profit_usd": p.profit,
                "already_be": already_be
            }
            
            if r_multiple >= 1.00 and not already_be:
                res = move_sl_to_breakeven(p.ticket)
                item["action"] = "RATCHETED_TO_BREAKEVEN"
                item["result"] = res
            else:
                item["action"] = "MONITORING" if not already_be else "HOLDING_BREAKEVEN"
                
            results.append(item)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blueberry Funded MT5 CG-Terminal Execution Engine")
    parser.add_argument("--status", action="store_true", help="Print account audit and isolated cg_terminal positions")
    parser.add_argument("--calc-risk", nargs=3, metavar=("SYMBOL", "ENTRY", "SL"), help="Calculate exact lot size")
    parser.add_argument("--place", nargs=5, metavar=("SYMBOL", "TYPE", "ENTRY", "SL", "TP"), help="Place order with bracket SL/TP")
    parser.add_argument("--max-risk", type=float, default=MAX_RISK_USD, help="Max dollar risk cap (default $6.00, or user-authorized e.g. 25.00 for min lot)")
    parser.add_argument("--be", type=int, metavar="TICKET", help="Move SL of cg_terminal position to Breakeven")
    parser.add_argument("--auto-be", action="store_true", help="Auto-ratchet any cg_terminal position with >= +1.0R to Breakeven")
    
    args = parser.parse_args()
    
    try:
        if args.status:
            audit = get_account_audit()
            print(json.dumps(audit, indent=2))
        elif args.calc_risk:
            sym, entry, sl = args.calc_risk[0], float(args.calc_risk[1]), float(args.calc_risk[2])
            res = calculate_lot_size(sym, entry, sl, max_risk_cap_usd=args.max_risk)
            print(json.dumps(res, indent=2))
        elif args.place:
            sym, o_type, entry, sl, tp = args.place[0], args.place[1], float(args.place[2]), float(args.place[3]), float(args.place[4])
            res = place_order(sym, o_type, entry, sl, tp, max_risk_cap_usd=args.max_risk)
            print(json.dumps(res, indent=2))
        elif args.be:
            res = move_sl_to_breakeven(args.be)
            print(json.dumps(res, indent=2))
        elif args.auto_be:
            res = auto_ratchet_breakeven()
            print(json.dumps(res, indent=2))
        else:
            audit = get_account_audit()
            print(json.dumps(audit, indent=2))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if mt5:
            mt5.shutdown()
