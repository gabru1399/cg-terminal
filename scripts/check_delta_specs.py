import json
import urllib.request

symbols = ['LINKUSD', 'ARBUSD', 'BNBUSD', 'ADAUSD', 'TIAUSD', 'SEIUSD']
for s in symbols:
    try:
        url = f"https://cdn.india.delta.exchange/v2/products/{s}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            res = json.loads(r.read().decode('utf-8')).get('result', {})
            print(f"Sym: {s:8} | ID: {res.get('id')} | ContVal: {res.get('contract_value')} | Quoting: {res.get('quoting_asset',{}).get('symbol')} | Tick: {res.get('tick_size')} | Status: {res.get('trading_status')}")
    except Exception as e:
        print(f"Sym: {s:8} | Error: {e}")
