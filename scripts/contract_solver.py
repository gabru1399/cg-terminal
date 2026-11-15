import math
import json
import os
import sys

def solve_contract_order(symbol, side, entry_price, stop_loss, take_profit, equity=1.4925, avail_cash=0.0186, risk_pct=0.5, leverage=None):
    """
    Deterministic Integer Contract Grid Solver for Delta Exchange India.
    Integrates Canonical SOP v1.4.0 risk limits, discrete tick quantization, and margin solvency.
    """
    # Load product specs
    prod = None
    if os.path.exists('scratch/delta_products.json'):
        with open('scratch/delta_products.json', encoding='utf-8') as f:
            products = json.load(f)
        for p in products:
            if p.get('contract_type') == 'perpetual_futures' and p.get('state') == 'live':
                if p.get('symbol') == symbol or p.get('symbol') == symbol + 'USD':
                    prod = p
                    break

    if not prod:
        return {"ok": False, "error": f"Product {symbol} not found in live Delta catalog."}

    delta_symbol = prod.get('symbol')
    contract_val = float(prod.get('contract_value', 1.0))
    tick_size = float(prod.get('tick_size', 0.0001))
    default_lev = float(prod.get('default_leverage', 20.0))
    active_lev = float(leverage) if leverage else default_lev

    # Quantize prices to tick size
    tick_decimals = max(0, -int(math.floor(math.log10(tick_size))))
    q_entry = round(round(entry_price / tick_size) * tick_size, tick_decimals)
    q_stop = round(round(stop_loss / tick_size) * tick_size, tick_decimals)
    q_tp = round(round(take_profit / tick_size) * tick_size, tick_decimals)

    stop_dist = abs(q_entry - q_stop)
    tp_dist = abs(q_tp - q_entry)

    if stop_dist <= 0:
        return {"ok": False, "error": "Stop loss cannot be identical to entry price."}

    r_multiple = tp_dist / stop_dist

    # Directional logic check
    if side.upper() == 'BUY':
        if q_stop >= q_entry:
            return {"ok": False, "error": "Stop loss for BUY must be strictly below entry."}
        if q_tp <= q_entry:
            return {"ok": False, "error": "Take profit for BUY must be strictly above entry."}
    elif side.upper() == 'SELL':
        if q_stop <= q_entry:
            return {"ok": False, "error": "Stop loss for SELL must be strictly above entry."}
        if q_tp >= q_entry:
            return {"ok": False, "error": "Take profit for SELL must be strictly below entry."}

    # Sizing
    dollar_risk_target = equity * (risk_pct / 100.0)
    risk_per_contract = stop_dist * contract_val

    raw_contracts = dollar_risk_target / risk_per_contract
    num_contracts = math.floor(raw_contracts)

    # Minimum lot size is 1 contract
    if num_contracts < 1:
        # Check if 1 contract risk is acceptable (up to max 1.0% equity)
        one_lot_risk_pct = (risk_per_contract / equity) * 100.0
        if one_lot_risk_pct <= 1.0:
            num_contracts = 1
        else:
            return {
                "ok": False,
                "error": f"Account equity (${equity:.2f}) too small for 1 contract stop distance. 1-lot risk = {one_lot_risk_pct:.2f}% (max allowed: 1.0%)."
            }

    notional = num_contracts * q_entry * contract_val
    margin_req = notional / active_lev
    max_margin_budget = avail_cash * 0.8

    margin_passed = margin_req <= max_margin_budget

    return {
        "ok": True,
        "symbol": delta_symbol,
        "side": side.upper(),
        "entry": q_entry,
        "stop_loss": q_stop,
        "take_profit": q_tp,
        "r_multiple": round(r_multiple, 2),
        "contracts": num_contracts,
        "contract_value": contract_val,
        "notional_usd": round(notional, 4),
        "leverage": active_lev,
        "margin_required_usd": round(margin_req, 4),
        "available_cash_usd": round(avail_cash, 4),
        "margin_budget_usd": round(max_margin_budget, 4),
        "margin_solvency": "PASS" if margin_passed else "FAIL (Insufficient Cash)",
        "dollar_risk": round(num_contracts * risk_per_contract, 4),
        "actual_risk_pct": round(((num_contracts * risk_per_contract) / equity) * 100.0, 2)
    }

if __name__ == '__main__':
    # Test sample run for SUIUSD Short
    res = solve_contract_order(
        symbol='SUI',
        side='SELL',
        entry_price=0.7300,
        stop_loss=0.7450,
        take_profit=0.6900,
        equity=1.4925,
        avail_cash=0.0186,
        risk_pct=0.5,
        leverage=50.0
    )
    print(json.dumps(res, indent=2))
