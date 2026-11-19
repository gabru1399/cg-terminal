"""Shared MT5 pending-entry risk checks. The broker API is passed in for testing."""

from decimal import Decimal
from math import isfinite

STRESS = Decimal("1.20")
HARD_CAP_USD = Decimal("6.00")
ACCOUNT_LOGIN = 5126976


def validate_bracket(entry, stop, target, buy, bid, ask):
    if not all(isfinite(x) and x > 0 for x in (entry, stop, bid, ask)) or ask < bid:
        raise ValueError("Entry, stop and broker bid/ask must be valid")
    e, sl, b, a = map(lambda x: Decimal(str(x)), (entry, stop, bid, ask))
    direction = 1 if buy else -1
    distance = direction * (e - sl)
    if distance <= 0:
        raise ValueError("Stop must be beyond entry on the adverse side")
    if 5 * (a - b) > distance:
        raise ValueError("PIT-18 veto: broker spread exceeds 20% of stop distance")
    if target and (not isfinite(target) or target <= 0 or direction * (Decimal(str(target)) - e) < 2 * distance):
        raise ValueError("Supplied target must deliver at least 2.00R in the trade direction")


def size_order(mt5, info, entry, stop, buy, target_usd, cap_usd, lots=None):
    account = mt5.account_info()
    if account is None or account.login != ACCOUNT_LOGIN or account.currency != "USD":
        raise ValueError("Configured Blueberry USD account unavailable")
    if not all(isfinite(x) and x > 0 for x in (entry, stop, target_usd, cap_usd)):
        raise ValueError("Entry, stop and risk budgets must be positive and finite")
    cap = min(Decimal(str(cap_usd)), HARD_CAP_USD)
    budget = min(Decimal(str(target_usd)), cap)
    entry_decimal, stop_decimal = Decimal(str(entry)), Decimal(str(stop))
    if (buy and stop_decimal >= entry_decimal) or (not buy and stop_decimal <= entry_decimal):
        raise ValueError("Stop must be beyond entry on the adverse side")
    stressed_exit = entry_decimal + STRESS * (stop_decimal - entry_decimal)
    if stressed_exit <= 0:
        raise ValueError("Stressed exit price is invalid")
    if not all(isfinite(x) and x > 0 for x in (info.volume_min, info.volume_max, info.volume_step)):
        raise ValueError("MT5 volume metadata is invalid")
    minimum, maximum, step = (Decimal(str(x)) for x in (info.volume_min, info.volume_max, info.volume_step))
    if minimum > maximum:
        raise ValueError("MT5 volume bounds are invalid")
    side = mt5.ORDER_TYPE_BUY if buy else mt5.ORDER_TYPE_SELL

    def loss(volume):
        pnl = mt5.order_calc_profit(side, info.name, float(volume), entry, float(stressed_exit))
        if pnl is None or not isfinite(pnl) or pnl >= 0:
            raise ValueError("MT5 could not value the stressed loss in account currency")
        return Decimal(str(-pnl))

    def checked(volume, ceiling):
        estimated = loss(volume)
        if estimated > ceiling:
            raise ValueError(f"Gate 11 veto: {volume} lots risks ${estimated:.2f} against the ${ceiling:.2f} cap")
        return float(volume), float(estimated)

    if lots is not None:
        if not isfinite(lots):
            raise ValueError("Lot size must be finite")
        volume = Decimal(str(lots))
        if volume < minimum or volume > maximum or (volume - minimum) % step:
            raise ValueError("Lot size is outside the MT5 volume grid")
        return checked(volume, cap)

    best = checked(minimum, cap)
    low, high = 1, int((maximum - minimum) // step)
    while low <= high:
        middle = (low + high) // 2
        volume = minimum + step * middle
        estimated = loss(volume)
        if estimated <= budget:
            best = float(volume), float(estimated)
            low = middle + 1
        else:
            high = middle - 1
    return best
