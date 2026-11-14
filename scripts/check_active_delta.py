import urllib.request
import json

req = urllib.request.Request('https://api.india.delta.exchange/v2/tickers', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode('utf-8'))

tickers = data.get('result', [])
perps = [t for t in tickers if t.get('contract_type') == 'perpetual_futures']
# Filter out contracts with zero or negligible turnover
active_perps = [t for t in perps if float(t.get('turnover_usd') or 0) > 10000]
active_perps.sort(key=lambda x: float(x.get('turnover_usd') or 0), reverse=True)

print(f"Total active perpetuals (> $10k turnover): {len(active_perps)}")
symbols = [t['symbol'] for t in active_perps]
print("Top active symbols:", symbols[:30])
