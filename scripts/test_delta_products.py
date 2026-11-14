import urllib.request
import json

req = urllib.request.Request('https://api.india.delta.exchange/v2/products', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    products = data.get('result', [])
    perps = [p for p in products if p.get('contract_type') == 'perpetual_futures']
    print(f"Total products: {len(products)}, Perpetual futures: {len(perps)}")
    for p in perps[:25]:
        quoting = p.get('quoting_asset', {}).get('symbol') if isinstance(p.get('quoting_asset'), dict) else p.get('quoting_asset')
        underlying = p.get('underlying_asset', {}).get('symbol') if isinstance(p.get('underlying_asset'), dict) else p.get('underlying_asset')
        print(f"{p['symbol']}: id={p['id']}, quoting={quoting}, underlying={underlying}")
except Exception as e:
    print(f"Error: {e}")
