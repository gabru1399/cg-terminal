import requests
import json

r = requests.get('https://api.india.delta.exchange/v2/products')
products = r.json().get('result', [])
targets = ['BTCUSD', 'ETHUSD', 'SOLUSD', 'BNBUSD', 'XRPUSD']
for p in products:
    sym = p.get('symbol')
    if sym in targets:
        print(f"{sym}: id={p.get('id')}, contract_value={p.get('contract_value')}, contract_type={p.get('contract_type')}, tick_size={p.get('tick_size')}, min_size={p.get('min_order_size')}, max_leverage={p.get('max_leverage_notional')}")
