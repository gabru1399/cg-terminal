import sys
sys.path.insert(0, "CG-Terminal/scripts")
import delta_direct
import json

# 1. Open orders on Delta
ords = delta_direct.request_delta("GET", "/v2/orders", query="?state=open")
print("=== Delta Open Orders ===")
if ords.get("success"):
    res = ords.get("result", [])
    print(f"Total Delta open orders: {len(res)}")
    for o in res:
        print(f"ID: {o.get('id')} | Product: {o.get('product_symbol')} (ID {o.get('product_id')}) | Side: {o.get('side')} | Size: {o.get('size')} | Limit: {o.get('limit_price')} | State: {o.get('state')} | StopOrderType: {o.get('stop_order_type')}")
else:
    print("Failed to get open orders:", ords)

# 2. Check product info for BTC, ETH, SOL, BNB, XAU/GOLD
prods = delta_direct.request_delta("GET", "/v2/products")
target_syms = ["BTCUSD", "ETHUSD", "SOLUSD", "BNBUSD", "XAUUSD", "PAXGUSD", "XAUTUSD"]
if prods.get("success"):
    print("\n=== Target Products on Delta ===")
    for p in prods.get("result", []):
        sym = p.get("symbol")
        if sym in target_syms or "GOLD" in sym or "XAU" in sym:
            print(f"ID: {p.get('id'):<6} | Symbol: {sym:<10} | Type: {p.get('contract_type')} | TickSize: {p.get('tick_size')} | ContractVal: {p.get('contract_value')} | QuotingAsset: {p.get('quoting_asset', {}).get('symbol')}")
