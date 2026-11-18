#!/usr/bin/env python3
"""
scripts/mt5_punch.py — bridge the terminal's PUNCH button straight into MT5.

Reads a JSON punch request on stdin (written by /api/desk/mt5-punch):

{
  "symbol":  "BTCUSD.pi",     # RESOLVED MT5 symbol (broker-suffixed)
  "side":    "long"|"short",  # card side
  "kind":    "market"|"limit",
  "entry":   62800.0,         # limit price (market: ignored, uses current)
  "stop":    62400.0,
  "tp":      63400.0,         # T1 (the scale-out rung the bracket closes at)
  "risk_usd": 5.5,            # optional override; defaults to prop rules
  "order_id": "tp-1795033772528"
}

Safety rules (mirror scripts/mt5_cg_trader.py — Blueberry funded account):
  - risk per trade capped at $6.00 by default (prop: 0.20–0.24% of $2,500);
    risk_usd may only LOWER the cap, never raise it
  - every order carries comment "cg_terminal" + magic 42001 (account isolation)
  - daily 4% / overall 10% drawdown guards checked BEFORE placing
  - symbol must trade full (trade_mode 4) and be visible
Prints one JSON object on stdout: {ok, ticket, lots, risk_usd, price, retcode}
or {ok: false, error}. Exit code 0 only on success.
"""
import json
import sys
from pathlib import Path

try:
    import MetaTrader5 as mt5
except ImportError:
    print(json.dumps({"ok": False, "error": "MetaTrader5 python package not installed (Windows only: pip install MetaTrader5)"}))
    sys.exit(1)

MAX_RISK_USD = 6.00
MAGIC_NUMBER = 42001
CG_COMMENT = "cg_terminal"
MAX_DAILY_DRAWDOWN_USD = 100.00
MAX_OVERALL_DRAWDOWN_USD = 250.00
INITIAL_ACCOUNT_BALANCE = 2500.00


def main():
    req = json.loads(sys.stdin.read())

    if not mt5.initialize(timeout=15_000):
        print(json.dumps({"ok": False, "error": f"mt5.initialize failed: {mt5.last_error()} (is the MT5 terminal running?)"}))
        sys.exit(1)
    try:
        acc = mt5.account_info()
        if acc is None:
            print(json.dumps({"ok": False, "error": f"account_info failed: {mt5.last_error()}"}))
            sys.exit(1)

        # ---- drawdown guards (checked before anything else) ----
        overall_dd = max(0.0, INITIAL_ACCOUNT_BALANCE - acc.equity)
        if overall_dd >= MAX_OVERALL_DRAWDOWN_USD:
            print(json.dumps({"ok": False, "error": f"overall drawdown guard: equity {acc.equity:.2f} hit the ${MAX_OVERALL_DRAWDOWN_USD:.2f} floor"}))
            sys.exit(1)

        sym = req["symbol"]
        side = req["side"].lower()
        kind = req.get("kind", "market").lower()
        stop = float(req["stop"])
        tp = float(req["tp"]) if req.get("tp") else 0.0

        if not mt5.symbol_select(sym, True):
            print(json.dumps({"ok": False, "error": f"symbol_select failed for {sym} — check broker suffix"}))
            sys.exit(1)
        info = mt5.symbol_info(sym)
        if info is None:
            print(json.dumps({"ok": False, "error": f"symbol_info failed for {sym}"}))
            sys.exit(1)
        if info.trade_mode != 4:
            print(json.dumps({"ok": False, "error": f"{sym} not in full-trade mode (trade_mode={info.trade_mode})"}))
            sys.exit(1)

        tick = mt5.symbol_info_tick(sym)
        if tick is None:
            print(json.dumps({"ok": False, "error": f"no tick for {sym}"}))
            sys.exit(1)

        # ---- entry price ----
        if kind == "limit":
            entry = float(req["entry"])
        else:
            entry = tick.ask if side == "long" else tick.bid

        stop_dist = abs(entry - stop)
        if stop_dist <= 0:
            print(json.dumps({"ok": False, "error": "stop distance must be positive"}))
            sys.exit(1)

        # ---- sizing (risk_usd can only lower the prop cap) ----
        cap = MAX_RISK_USD
        if req.get("risk_usd"):
            cap = min(float(req["risk_usd"]), MAX_RISK_USD)
        tick_size = info.trade_tick_size or info.point
        tick_value = info.trade_tick_value or 0.01
        risk_per_lot = (stop_dist / tick_size) * tick_value if tick_size else 0.0
        if risk_per_lot <= 0:
            risk_per_lot = info.trade_contract_size * stop_dist
        if risk_per_lot <= 0:
            print(json.dumps({"ok": False, "error": "cannot compute per-lot risk for {sym}"}))
            sys.exit(1)

        raw = cap / risk_per_lot
        steps = round(raw / info.volume_step)
        lots = round(steps * info.volume_step, 2)
        min_lot_risk = info.volume_min * risk_per_lot
        if lots < info.volume_min:
            if min_lot_risk > MAX_RISK_USD + 0.50:
                print(json.dumps({"ok": False,
                                  "error": f"min lot {info.volume_min} would risk ${min_lot_risk:.2f} > ${MAX_RISK_USD:.2f} prop cap — stop too wide for this account"}))
                sys.exit(1)
            lots = info.volume_min
        lots = min(lots, info.volume_max)
        actual_risk = lots * risk_per_lot

        # ---- order type ----
        if kind == "limit":
            otype = mt5.ORDER_TYPE_BUY_LIMIT if side == "long" else mt5.ORDER_TYPE_SELL_LIMIT
            action = mt5.TRADE_ACTION_PENDING
        else:
            otype = mt5.ORDER_TYPE_BUY if side == "long" else mt5.ORDER_TYPE_SELL
            action = mt5.TRADE_ACTION_DEAL

        digits = info.digits
        request = {
            "action": action,
            "symbol": sym,
            "volume": lots,
            "type": otype,
            "price": round(entry, digits),
            "sl": round(stop, digits),
            "tp": round(tp, digits) if tp else 0.0,
            "deviation": 20,
            "magic": MAGIC_NUMBER,
            "comment": CG_COMMENT,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result is None:
            print(json.dumps({"ok": False, "error": f"order_send returned None: {mt5.last_error()}"}))
            sys.exit(1)
        # unsupported filling mode -> FOK fallback (same as mt5_cg_trader)
        if result.retcode not in (mt5.TRADE_RETCODE_DONE, mt5.TRADE_RETCODE_PLACED) and result.retcode == 10030:
            request["type_filling"] = mt5.ORDER_FILLING_FOK
            result = mt5.order_send(request)
        if result.retcode not in (mt5.TRADE_RETCODE_DONE, mt5.TRADE_RETCODE_PLACED):
            print(json.dumps({"ok": False, "error": f"order_send rejected: retcode {result.retcode} — {result.comment}"}))
            sys.exit(1)

        print(json.dumps({
            "ok": True,
            "ticket": result.order,
            "deal": result.deal,
            "lots": lots,
            "risk_usd": round(actual_risk, 2),
            "price": result.price,
            "retcode": result.retcode,
            "symbol": sym,
            "comment": CG_COMMENT,
        }))
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    main()
