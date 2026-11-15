import urllib.request
import json

symbols = ['BTCUSD', 'ETHUSD', 'SOLUSD', 'ADAUSD', 'DOGEUSD', 'AVAXUSD', 'LTCUSD', 'XRPUSD', 'NEARUSD', 'DOTUSD', 'TRXUSD', 'UNIUSD', 'LINKUSD', 'SUIUSD', 'APTUSD', 'ARBUSD', 'OPUSD', 'TIAUSD', 'INJUSD', 'FILUSD']

print(f"{'Symbol':8} | {'ID':5} | {'C_Val':7} | {'Mark':8} | {'1_Notional':10} | {'Margin':8} | {'MaxLev'}")
print("-" * 65)

for s in symbols:
    try:
        url = f'https://api.india.delta.exchange/v2/products/{s}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            d = json.loads(resp.read().decode())['result']
            c_val = float(d.get('contract_value', 1))
            tick = d.get('tick_size')
            lev = float(d.get('default_leverage', 100))
            pid = d.get('id')
            
        url_t = f'https://api.india.delta.exchange/v2/tickers/{s}'
        with urllib.request.urlopen(urllib.request.Request(url_t, headers={'User-Agent': 'Mozilla/5.0'}), timeout=5) as resp_t:
            dt = json.loads(resp_t.read().decode())['result']
            mark = float(dt.get('mark_price', 0))
            
        notional = c_val * mark
        margin = notional / lev if lev else notional
        print(f"{s:8} | {pid:5} | {c_val:7.2f} | {mark:8.3f} | ${notional:8.2f} | ${margin:6.3f} | {lev:.0f}x")
    except Exception as e:
        print(f"{s:8} | error: {e}")
