#!/usr/bin/env python3
"""Read-only Blueberry Phase 1 equity and exposure status."""

import json
import sys
from datetime import datetime, timezone

TARGET_EQUITY_USD = 2700.00
EXPECTED_MT5_LOGIN = 5126976


def check_and_enforce_phase1(close_all_if_achieved=False):
    if close_all_if_achieved:
        return {"ok": False, "error": "Phase 1 monitor is read-only. Use the separately authorized LIVE gateway."}

    try:
        import MetaTrader5 as mt5
    except ImportError as exc:
        return {"ok": False, "error": str(exc)}

    if not mt5.initialize(timeout=15_000):
        return {"ok": False, "error": f"MT5 initialization failed: {mt5.last_error()}"}

    try:
        account = mt5.account_info()
        if account is None or account.login != EXPECTED_MT5_LOGIN:
            return {"ok": False, "error": "Expected MT5 account is unavailable"}
        positions, orders = mt5.positions_get(), mt5.orders_get()
        if positions is None or orders is None:
            return {"ok": False, "error": f"MT5 exposure lookup failed: {mt5.last_error()}"}
        equity = float(account.equity)
        return {
            "ok": True,
            "mode": "AUDIT",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "login": account.login,
            "balance": float(account.balance),
            "equity": equity,
            "floating_profit": float(account.profit),
            "target_equity": TARGET_EQUITY_USD,
            "distance_to_target": round(TARGET_EQUITY_USD - equity, 2),
            "phase1_achieved": equity >= TARGET_EQUITY_USD,
            "open_positions_count": len(positions),
            "pending_orders_count": len(orders),
        }
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    status = check_and_enforce_phase1(any(flag in sys.argv for flag in ("--close-if-achieved", "--enforce")))
    print(json.dumps(status, indent=2))
    sys.exit(0 if status["ok"] else 1)
