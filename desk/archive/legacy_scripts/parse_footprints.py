import urllib.request
import json

def get_footprint_pocs(sym, limit=20):
    req = urllib.request.Request(f'http://127.0.0.1:3000/api/cg/fp?sym={sym}&limit={limit}')
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    
    bars = data.get('bars', [])
    pocs = []
    for b in bars:
        fp_data = b.get('fp')
        if not fp_data:
            continue
        lo = fp_data.get('lo', 0)
        tick = fp_data.get('tick', 1)
        buys = fp_data.get('b', [])
        sells = fp_data.get('s', [])
        
        max_v = -1
        poc_price = None
        for i in range(min(len(buys), len(sells))):
            v = buys[i] + sells[i]
            if v > max_v:
                max_v = v
                poc_price = lo + i * tick
        if poc_price is not None:
            pocs.append({
                'ts': b.get('ts'),
                'poc': poc_price,
                'vol': max_v,
                'close': b.get('c'),
                'high': b.get('h'),
                'low': b.get('l')
            })
    return pocs

for s in ['BTC', 'ETH', 'SOL', 'LTC', 'DOT']:
    pocs = get_footprint_pocs(s, limit=10)
    print(f"\n{s} ({len(pocs)} bars parsed):")
    for p in pocs[:4]:
        print(f"  ts={p['ts']}: POC={p['poc']} | High={p['high']} | Low={p['low']} | MaxVol={p['vol']:.2f}")
