import json
import urllib.request

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode('utf-8')).get('result', [])

def audit():
    products = fetch_json("https://cdn.india.deltaex.org/v2/products")
    tickers = {t['symbol']: float(t.get('mark_price') or t.get('close') or 0.0) 
               for t in fetch_json("https://cdn.india.deltaex.org/v2/tickers")}
    
    perps = {p['symbol']: p for p in products if p.get('contract_type') == 'perpetual_futures'}
    
    target_symbols = [
        # TradFi / Metals
        'MSFTBUSD', 'AVGOBUSD', 'NVDABUSD', 'METABUSD', 'MSTRBUSD', 'OILUSD', 'XAUTUSD', 'XAGUSD',
        # Permitted Micro-Crypto
        'VETUSD', 'SEIUSD', 'ADAUSD', 'TIAUSD', 'APTUSD', 'DOGEUSD', 'ARBUSD', 'SUIUSD', 'OPUSD',
        # Other Crypto
        'LINKUSD', 'BNBUSD', 'SOLUSD', 'BTCUSD', 'ETHUSD'
    ]
    
    equity = 2.767366
    max_risk_cap = equity * 0.01  # $0.0277
    
    print("=" * 105)
    print(f"DELTA EXCHANGE INDIA SPECIFICATION & GATE 7 AUDIT (EQUITY: ${equity:.4f} | MAX RISK: ${max_risk_cap:.4f})")
    print("=" * 105)
    print(f"{'SYMBOL':<10} | {'ID':<6} | {'MARK PX':<10} | {'CV (Units)':<12} | {'NOTIONAL ($)':<12} | {'1.5% SL RISK':<14} | {'GATE 7 STATUS'}")
    print("-" * 105)
    
    for sym in target_symbols:
        p = perps.get(sym)
        if not p:
            continue
        pid = p['id']
        cv = float(p.get('contract_value', 1.0))
        px = tickers.get(sym, 0.0)
        notional_1lot = px * cv
        
        # Standard 1.5% stop distance * 1.20x slippage buffer
        sl_risk_1lot = notional_1lot * 0.015 * 1.20
        
        status = "PASS (TRADEABLE)" if sl_risk_1lot <= max_risk_cap else f"BANNED (Risk: ${sl_risk_1lot:.4f})"
        
        print(f"{sym:<10} | {pid:<6} | ${px:<9.2f} | {str(cv):<12} | ${notional_1lot:<11.2f} | ${sl_risk_1lot:<13.4f} | {status}")

if __name__ == '__main__':
    audit()
