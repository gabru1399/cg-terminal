import urllib.request
import json

req = urllib.request.Request('https://api.india.delta.exchange/v2/tickers', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    tickers = data.get('result', [])
    perp_tickers = [t for t in tickers if t.get('contract_type') == 'perpetual_futures']
    
    # Sort by turnover_usd
    sorted_perps = sorted(perp_tickers, key=lambda x: float(x.get('turnover_usd') or 0), reverse=True)
    
    print(f"{'Symbol':<15} | {'Price':<10} | {'Turnover USD':<15} | {'OI USD':<15} | {'Top Tag':<10} | {'Description'}")
    print("-" * 85)
    for t in sorted_perps[:50]:
        price = str(t.get('close') or t.get('mark_price') or '')
        turnover = f"${float(t.get('turnover_usd') or 0):,.0f}"
        oi = f"${float(t.get('oi_value_usd') or 0):,.0f}"
        tag = str(t.get('top_tag') or '')
        desc = str(t.get('description') or '')
        print(f"{t['symbol']:<15} | {price:<10} | {turnover:<15} | {oi:<15} | {tag:<10} | {desc}")

except Exception as e:
    print(f"Error: {e}")
