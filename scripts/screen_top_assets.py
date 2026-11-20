import urllib.request, json

symbols = ['BTC', 'ETH', 'SOL', 'XRP', 'ENA', 'BERA', 'TRX', 'DOGE', 'SUI', 'XAU']
print(f"{'SYM':<6} | {'PRICE':<10} | {'POC':<10} | {'VWAP':<10} | {'RSI_15M':<8} | {'RSI_1H':<8} | {'ATR_ST':<10} | {'TREND':<12}")
print('-'*85)

for sym in symbols:
    url = f'http://127.0.0.1:3000/api/cg/market?sym={sym}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Antigravity'})
        with urllib.request.urlopen(req, timeout=5) as res:
            d = json.loads(res.read().decode())
            price = d.get('price', {}).get('last', 0)
            poc = d.get('auction', {}).get('session', {}).get('poc', 0)
            vwap = d.get('vwap', {}).get('vwap', 0)
            rsi_15m = d.get('rsi', {}).get('m15', 0)
            rsi_1h = d.get('rsi', {}).get('h1', 0)
            atr_st = d.get('vol', {}).get('atrState', 'N/A')
            
            # EMA alignment
            ema = d.get('ema', {}).get('m15', {})
            e13 = ema.get('e13', 0)
            e89 = ema.get('e89', 0)
            e233 = ema.get('e233', 0)
            trend = 'BEAR_STACK' if (e13 < e89 and e89 < e233) else ('BULL_STACK' if (e13 > e89 and e89 > e233) else 'MIXED')
            
            print(f"{sym:<6} | {price:<10.4f} | {poc:<10.4f} | {vwap:<10.4f} | {rsi_15m:<8.1f} | {rsi_1h:<8.1f} | {atr_st:<10} | {trend:<12}")
    except Exception as e:
        print(f"{sym:<6} | Error: {e}")
