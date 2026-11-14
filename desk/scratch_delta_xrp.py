import requests
r = requests.get('https://api.india.delta.exchange/v2/products')
products = r.json().get('result', [])
for p in products:
    sym = p.get('symbol', '')
    if 'XRP' in sym:
        print(f"{sym}: id={p.get('id')}, contract_value={p.get('contract_value')}, type={p.get('contract_type')}")
