"""
Autonomous Dual-Venue Execution & Risk Pipeline (SOP v2.0.0)
Deterministic orchestrator for Delta Exchange India & Blueberry Funded MT5.
Executes fresh on every round without cached shortcuts.
"""

import os
import sys
import json
import time
import requests
import MetaTrader5 as mt5

TERMINAL_API = "http://localhost:3000"
DELTA_API_URL = "https://cdn.india.delta.exchange"
CG_COMMENT = "cg_terminal"
MAGIC_NUMBER = 42001

def check_terminal_health():
    try:
        r = requests.get(f"{TERMINAL_API}/api/cg/market?sym=BTC", timeout=5)
        return r.status_code == 200
    except Exception:
        return False

def audit_mt5():
    if not mt5.initialize():
        return {"error": "Failed to initialize MT5"}
    
    acc = mt5.account_info()
    if not acc:
        mt5.shutdown()
        return {"error": "Failed to get account info"}
        
    positions = mt5.positions_get() or ()
    orders = mt5.orders_get() or ()
    
    cg_positions = [p for p in positions if p.comment == CG_COMMENT or p.magic == MAGIC_NUMBER]
    other_positions = [p for p in positions if p.comment != CG_COMMENT and p.magic != MAGIC_NUMBER]
    
    cg_orders = [o for o in orders if o.comment == CG_COMMENT or o.magic == MAGIC_NUMBER]
    other_orders = [o for o in orders if o.comment != CG_COMMENT and o.magic != MAGIC_NUMBER]
    
    pos_data = []
    for p in positions:
        pos_data.append({
            "ticket": p.ticket,
            "symbol": p.symbol,
            "type": "BUY" if p.type == mt5.ORDER_TYPE_BUY else "SELL",
            "volume": p.volume,
            "price_open": p.price_open,
            "price_current": p.price_current,
            "sl": p.sl,
            "tp": p.tp,
            "profit": round(p.profit, 2),
            "comment": p.comment,
            "is_cg": p.comment == CG_COMMENT or p.magic == MAGIC_NUMBER
        })
        
    ord_data = []
    for o in orders:
        ord_data.append({
            "ticket": o.ticket,
            "symbol": o.symbol,
            "type": o.type,
            "volume": o.volume_current,
            "price_open": o.price_open,
            "sl": o.sl,
            "tp": o.tp,
            "comment": o.comment,
            "is_cg": o.comment == CG_COMMENT or o.magic == MAGIC_NUMBER
        })
        
    res = {
        "account": {
            "login": acc.login,
            "balance": acc.balance,
            "equity": acc.equity,
            "free_margin": acc.margin_free,
            "leverage": acc.leverage,
            "drawdown_usd": max(0.0, 2500.0 - acc.equity)
        },
        "cg_positions": len(cg_positions),
        "other_positions": len(other_positions),
        "cg_orders": len(cg_orders),
        "positions": pos_data,
        "orders": ord_data
    }
    mt5.shutdown()
    return res

def check_liquidation_cold_zone(symbol_raw, current_price, current_sl, is_short=True):
    """
    Checks if current SL is within 0.5% of any high-density liquidation cluster.
    Returns (is_safe, nearest_cluster_price, recommended_cold_sl).
    """
    sym = symbol_raw.replace(".p", "").replace(".pi", "").replace("USD", "")
    try:
        r = requests.get(f"{TERMINAL_API}/api/cg/liqlevels?sym={sym}", timeout=4)
        if r.status_code == 200:
            d = r.json()
            stats = d.get("stats", {})
            key_levels = stats.get("keyLevels", {})
            clusters = key_levels.get("above" if is_short else "below", [])
            
            for c in clusters:
                c_price = c.get("price")
                if c_price and abs(current_sl - c_price) / c_price < 0.005:
                    # Trapped inside cluster!
                    buffer = 0.008 if is_short else -0.008
                    recommended_sl = round(c_price * (1.0 + buffer), 4)
                    return False, c_price, recommended_sl
    except Exception:
        pass
    return True, None, current_sl

def run_pipeline():
    terminal_up = check_terminal_health()
    mt5_data = audit_mt5()
    
    # Audit SLs of all running positions
    sl_audits = []
    if "positions" in mt5_data:
        for p in mt5_data["positions"]:
            is_short = p["type"] == "SELL"
            safe, cluster_p, rec_sl = check_liquidation_cold_zone(
                p["symbol"], p["price_current"], p["sl"], is_short=is_short
            )
            sl_audits.append({
                "ticket": p["ticket"],
                "symbol": p["symbol"],
                "comment": p["comment"],
                "current_sl": p["sl"],
                "is_cold_zone_safe": safe,
                "cluster_price": cluster_p,
                "recommended_sl": rec_sl
            })
            
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "terminal_live": terminal_up,
        "mt5": mt5_data.get("account", {}),
        "positions_count": len(mt5_data.get("positions", [])),
        "orders_count": len(mt5_data.get("orders", [])),
        "cg_orders": [o for o in mt5_data.get("orders", []) if o["is_cg"]],
        "sl_audits": sl_audits
    }
    return report

if __name__ == "__main__":
    rep = run_pipeline()
    print(json.dumps(rep, indent=2))
