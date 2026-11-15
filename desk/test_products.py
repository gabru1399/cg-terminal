import urllib.request
import json

symbols = ['SOLUSD', 'ADAUSD', 'DOGEUSD', 'AVAXUSD', 'LTCUSD', 'XRPUSD', 'NEARUSD', 'DOTUSD', 'TRXUSD', 'UNIUSD']
for s in symbols:
    try:
        url = f'https://api.india.delta.exchange/v2/products/{s}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            d = json.loads(resp.read().decode())['result']
            print(f"{s}: id={d['id']}, contract_val={d['contract_value']}, tick={d['tick_size']}")
    except Exception as e:
        print(f"{s}: Error {e}")
