import json
import urllib.request

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode('utf-8')).get('result', [])

def find_tradeable():
    products = fetch_json("https://cdn.india.deltaex.org/v2/products")
    tickers = {t['symbol']: float(t.get('mark_price') or t.get('close') or 0.0) 
               for t in fetch_json("https://cdn.india.deltaex.org/v2/tickers")}
    
    perps = [p for p in products if p.get('contract_type') == 'perpetual_futures']
    
    equity = 2.767366
    max_risk_cap = equity * 0.01  # $0.0277
    
    tradeable = []
    
    for p in perps:
        sym = p['symbol']
        pid = p['id']
        cv = float(p.get('contract_value', 1.0))
        px = tickers.get(sym, 0.0)
        if px == 0.0:
            continue
        notional_1lot = px * cv
        # Standard 1.5% stop distance * 1.20x buffer
        sl_risk_1lot = notional_1lot * 0.015 * 1.20
        
        if sl_risk_1lot <= max_risk_cap:
            tradeable.append({
                'symbol': sym,
                'id': pid,
                'price': px,
                'cv': cv,
                'notional': notional_1lot,
                'sl_risk': sl_risk_1lot,
                'pct_equity': (sl_risk_1lot / equity) * 100
            })
            
    tradeable.sort(key=lambda x: x['notional'])
    
    print(f"Total Tradeable Perps on Delta India for ${equity:.2f} Equity (Risk <= ${max_risk_cap:.4f}): {len(tradeable)}")
    print("=" * 95)
    print(f"{'SYMBOL':<14} | {'ID':<6} | {'PRICE':<10} | {'CV':<10} | {'NOTIONAL ($)':<12} | {'1.5% SL RISK':<14} | {'% EQUITY'}")
    print("-" * 95)
    for t in tradeable:
        print(f"{t['symbol']:<14} | {t['id']:<6} | ${t['price']:<9.4f} | {t['cv']:<10} | ${t['notional']:<11.4f} | ${t['sl_risk']:<13.4f} | {t['pct_equity']:.2f}%")

if __name__ == '__main__':
    find_tradeable()
