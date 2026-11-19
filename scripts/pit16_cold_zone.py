"""PIT-16 reference solver. Prices and quantities use Decimal. Run --example."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from typing import Callable, Mapping, Sequence


D = Decimal
RISK_CAP = {"MT5": D("6.00"), "DELTA": D("0.50")}
WINDOWS = ("3d", "7d", "30d")


class Rejected(ValueError):
    """No order can be proposed from the supplied inputs."""


@dataclass(frozen=True)
class Feed:
    # Supply a full, verified snapshot with gap-free declared price coverage.
    # Times are source/effective timestamps, never HTTP response timestamps.
    evidence_id: str
    as_of_ms: int
    max_age_ms: int
    low: D
    high: D
    half_bin: D
    rows: Sequence[Mapping[str, object]]


@dataclass(frozen=True)
class RiskModel:
    min_qty: D
    qty_step: D
    max_qty: D
    free_margin_usd: D
    # Both functions use the verified symbol, account and direction. Their
    # outputs must be nondecreasing in quantity across the supported lot grid.
    loss_usd: Callable[[D, D, D], object]  # qty, executable entry, stressed exit
    margin_usd: Callable[[D, D], object]  # qty, executable entry


@dataclass(frozen=True)
class Solution:
    cold_zone_sl: D
    structural_distance: D
    risk_distance: D
    stressed_exit: D
    quantity: D
    modeled_loss_usd: D
    margin_usd: D
    risk_budget_usd: D
    spread_to_stop: D
    clearance: D
    limiting_edge: D
    checked_feeds: tuple[str, ...]
    hazards: tuple[str, ...]


def decimal(value, name):
    try:
        result = D(str(value))
    except (ArithmeticError, ValueError, TypeError) as error:
        raise Rejected(f"INVALID_{name}") from error
    if not result.is_finite():
        raise Rejected(f"INVALID_{name}")
    return result


def validate_feed(feed, start, end, now_ms):
    if (not feed.evidence_id or feed.as_of_ms < 0
            or not 0 <= now_ms - feed.as_of_ms <= feed.max_age_ms):
        raise Rejected("STALE_OR_UNVERIFIED_HAZARD_FEED")
    bounds = (feed.low, feed.high, feed.half_bin)
    if (any(not isinstance(value, D) or not value.is_finite() for value in bounds)
            or not 0 < feed.low < feed.high or feed.half_bin < 0):
        raise Rejected("INVALID_SHAPE_OF_HAZARD_FEED")
    if feed.low > min(start, end) or feed.high < max(start, end):
        raise Rejected("INSUFFICIENT_HAZARD_COVERAGE")


def hazard_edges(feed, side, source, start, direction, horizon, wall_min):
    """Yield the adverse outer edge of each qualifying interval in the corridor."""
    is_book = source == "book"
    valid_sides = ("bid", "ask") if is_book else ("long", "short")
    rows = feed.rows
    if is_book:
        value_key = "usdNotional"
    else:
        value_key = "intensity" if any("intensity" in row for row in rows) else "volUsd"
        if value_key == "intensity" and any("volUsd" in row for row in rows):
            raise Rejected("MIXED_LIQUIDATION_UNITS")
    values = [decimal(row.get(value_key), value_key) for row in rows]
    if any(value < 0 for value in values):
        raise Rejected("NEGATIVE_HAZARD_METRIC")
    peak = max(values, default=D(0))

    for index, (row, value) in enumerate(zip(rows, values, strict=True)):
        price = decimal(row.get("price"), "HAZARD_PRICE")
        low = decimal(row.get("low", price - feed.half_bin), "HAZARD_LOW")
        high = decimal(row.get("high", price + feed.half_bin), "HAZARD_HIGH")
        row_side = row.get("side")
        if row_side not in valid_sides or not 0 < low <= price <= high:
            raise Rejected("INVALID_HAZARD_ROW")
        if is_book:
            significant = value >= wall_min
        else:
            # Some providers give a normalized strength on a 0–100 scale.
            strength = decimal(row["strength"], "STRENGTH") if "strength" in row else (
                100 * value / peak if peak else D(0)
            )
            if not 0 <= strength <= 100:
                raise Rejected("INVALID_STRENGTH")
            significant = strength >= 40
        if row_side != side or not significant:
            continue
        near, far = sorted((direction * (low - start), direction * (high - start)))
        if near <= horizon and far >= 0:
            yield far, f"{source}:{feed.evidence_id}:{index}"


def solve(
    *, venue: str, side: str, entry_price: D, entry_reference: D,
    live_trigger_price: D, spread: D, atr: D, tick_size: D,
    structural_anchor: D, max_stop_distance: D, min_stop_distance: D,
    exit_slippage: D, wall_min_usd: D, now_ms: int, book: Feed,
    liquidation: Mapping[str, Feed], risk: RiskModel, available_risk_usd: D,
) -> Solution:
    """Solve a proposed new entry on the venue's stop-trigger price axis.

    Feeds, anchor, entry reference and live trigger use the same axis.
    Entry price is the actual order price. Spread is the stressed full spread.
    Exit slippage includes remaining adverse trigger-to-fill basis where needed.
    The horizon is precommitted by the strategy/payoff gate.
    """
    if venue not in RISK_CAP or side not in ("short", "long"):
        raise Rejected("INVALID_VENUE_OR_SIDE")
    for value in (
        entry_price, entry_reference, live_trigger_price, spread, atr, tick_size,
        structural_anchor, max_stop_distance, min_stop_distance, exit_slippage,
        wall_min_usd, available_risk_usd, risk.min_qty, risk.max_qty, risk.qty_step,
        risk.free_margin_usd,
    ):
        if not isinstance(value, D) or not value.is_finite() or value < 0:
            raise Rejected("INVALID_DECIMAL_INPUT")
    if min(entry_price, entry_reference, live_trigger_price, structural_anchor,
           atr, tick_size, max_stop_distance, wall_min_usd, risk.min_qty, risk.qty_step) <= 0:
        raise Rejected("NONPOSITIVE_PRICE_OR_POLICY")
    if entry_price % tick_size or risk.max_qty < risk.min_qty:
        raise Rejected("INVALID_ENTRY_TICK_OR_QUANTITY_GRID")
    if set(liquidation) != set(WINDOWS):
        raise Rejected("MISSING_LIQUIDATION_WINDOW")

    direction = D(1) if side == "short" else D(-1)
    anchor_distance = direction * (structural_anchor - entry_reference)
    if not 0 < anchor_distance < max_stop_distance:
        raise Rejected("ANCHOR_OUTSIDE_ADVERSE_CORRIDOR")
    end = entry_reference + direction * max_stop_distance
    feeds = (book, *(liquidation[window] for window in WINDOWS))
    for feed in feeds:
        validate_feed(feed, entry_reference, end, now_ms)

    wall_side = "ask" if side == "short" else "bid"
    hazards = list(hazard_edges(
        book, wall_side, "book", entry_reference, direction, max_stop_distance, wall_min_usd,
    ))
    for window in WINDOWS:
        hazards.extend(hazard_edges(
            liquidation[window], side, window, entry_reference, direction,
            max_stop_distance, wall_min_usd,
        ))
    edge_distance = max([anchor_distance, *(distance for distance, _ in hazards)])
    edge = entry_reference + direction * edge_distance
    structural_buffer = max(2 * tick_size, D("0.25") * atr, D("0.0015") * abs(edge))
    clearance = max(structural_buffer, 2 * spread)
    rounding = ROUND_CEILING if side == "short" else ROUND_FLOOR
    unrounded_stop = edge + direction * clearance
    stop = (unrounded_stop / tick_size).to_integral_value(rounding=rounding) * tick_size
    distance = direction * (stop - entry_reference)
    if stop <= 0 or distance + tick_size > max_stop_distance:
        raise Rejected("NO_COLD_ZONE_INSIDE_CORRIDOR")
    if (direction * (stop - live_trigger_price) <= 0
            or direction * (stop - live_trigger_price) < min_stop_distance
            or direction * (stop - entry_price) <= 0
            or direction * (stop - entry_price) < min_stop_distance):
        raise Rejected("STOP_INVALID_AT_ENTRY_OR_LIVE_TRIGGER")
    # Use the spread-independent structural distance for the routing test.
    # A wider spread cannot manufacture its own eligibility by moving the stop.
    spread_ratio = spread / (edge_distance + structural_buffer)
    if venue == "MT5" and spread_ratio > D("0.20"):
        raise Rejected("PIT18_SPREAD_TOO_WIDE")

    stressed_exit = stop + direction * exit_slippage
    if stressed_exit <= 0:
        raise Rejected("INVALID_STRESSED_EXIT")
    budget = min(RISK_CAP[venue], available_risk_usd)
    if budget <= 0:
        raise Rejected("NO_RISK_HEADROOM")

    def assess(step):
        qty = risk.min_qty + step * risk.qty_step
        loss = decimal(risk.loss_usd(qty, entry_price, stressed_exit), "VENUE_LOSS")
        margin = decimal(risk.margin_usd(qty, entry_price), "VENUE_MARGIN")
        if loss <= 0 or margin <= 0:
            raise Rejected("INVALID_VENUE_VALUATION")
        return qty, loss, margin

    best = assess(0)
    if best[1] > budget or best[2] > risk.free_margin_usd:
        raise Rejected("MIN_QTY_EXCEEDS_RISK_OR_MARGIN")
    lower = 1
    upper = int((risk.max_qty - risk.min_qty) // risk.qty_step)
    while lower <= upper:
        middle = (lower + upper) // 2
        candidate = assess(middle)
        if candidate[1] <= budget and candidate[2] <= risk.free_margin_usd:
            best = candidate
            lower = middle + 1
        else:
            upper = middle - 1
    quantity, loss, margin = best
    return Solution(
        stop, distance, abs(entry_price - stressed_exit), stressed_exit, quantity,
        loss, margin, budget, spread_ratio, abs(stop - edge), edge,
        tuple(feed.evidence_id for feed in feeds), tuple(label for _, label in hazards),
    )


def mt5_pricers(mt5, symbol, side, fees_usd):
    """Read-only valuation adapter for an initialized and verified MT5 session."""
    account = mt5.account_info()
    if account is None or account.currency != "USD" or side not in ("long", "short"):
        raise Rejected("MT5_USD_VALUATION_UNAVAILABLE")
    action = mt5.ORDER_TYPE_BUY if side == "long" else mt5.ORDER_TYPE_SELL

    def loss(qty, entry, exit_price):
        pnl = mt5.order_calc_profit(action, symbol, float(qty), float(entry), float(exit_price))
        fees = decimal(fees_usd(qty, entry, exit_price), "MT5_FEES")
        if fees < 0:
            raise Rejected("INVALID_MT5_FEES")
        return -decimal(pnl, "MT5_PROFIT") + fees

    def margin(qty, entry):
        return mt5.order_calc_margin(action, symbol, float(qty), float(entry))

    return loss, margin


def linear_usd_delta_pricers(
    *, base_units_per_contract: D, entry_fee: D, exit_fee: D,
    funding_per_contract_usd: D, margin_per_contract_usd: D,
):
    """Only for verified USD-linear products. Fee rates include tax and discounts."""
    values = (base_units_per_contract, entry_fee, exit_fee,
              funding_per_contract_usd, margin_per_contract_usd)
    if any(not value.is_finite() or value < 0 for value in values):
        raise Rejected("INVALID_DELTA_PRODUCT_METADATA")
    if base_units_per_contract <= 0 or margin_per_contract_usd <= 0:
        raise Rejected("INVALID_DELTA_CONTRACT_OR_MARGIN")

    def loss(qty, entry, exit_price):
        price_loss = abs(entry - exit_price)
        fees = entry * entry_fee + exit_price * exit_fee
        return qty * (base_units_per_contract * (price_loss + fees) + funding_per_contract_usd)

    def margin(qty, _entry):
        return qty * margin_per_contract_usd

    return loss, margin


def example():
    """Synthetic coverage, fees, ATR and lot metadata for the supplied ETH wall."""
    now = 1_000_000
    book = Feed("example-book", now, 5_000, D("1800"), D("1870"), D(0), (
        {"price": "1856.00", "usdNotional": "10750000", "side": "ask"},
    ))
    liquidation = {
        window: Feed(f"example-{window}", now, 60_000, D("1800"), D("1870"), D(0), ())
        for window in WINDOWS
    }
    pricers = linear_usd_delta_pricers(
        base_units_per_contract=D("0.01"), entry_fee=D("0.000236"),
        exit_fee=D("0.00059"), funding_per_contract_usd=D("0.005"),
        margin_per_contract_usd=D("1"),
    )
    return solve(
        venue="DELTA", side="short", entry_price=D("1838.50"), entry_reference=D("1838.50"),
        live_trigger_price=D("1838.00"), spread=D("0.09"), atr=D("2"), tick_size=D("0.05"),
        structural_anchor=D("1854.50"), max_stop_distance=D("25"),
        min_stop_distance=D("0.05"), exit_slippage=D("0.10"), wall_min_usd=D("5000000"),
        now_ms=now, book=book, liquidation=liquidation,
        risk=RiskModel(D(1), D(1), D(10), D("2.90"), *pricers), available_risk_usd=D("0.50"),
    )


if __name__ == "__main__":
    import argparse
    import json
    from dataclasses import asdict

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--example", action="store_true", required=True)
    parser.parse_args()
    print(json.dumps(asdict(example()), default=str, indent=2))
