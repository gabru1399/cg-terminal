import urllib.request
import json

base = "http://127.0.0.1:3000"

def get(path):
    try:
        req = urllib.request.Request(f"{base}{path}", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

for sym in ['TIA', 'ADA', 'XRP']:
    m = get(f"/api/cg/market?sym={sym}")
    sig = get(f"/api/cg/signals?sym={sym}")
    n = get(f"/api/cg/narrative?sym={sym}")
    l = get(f"/api/cg/liqlevels?sym={sym}")
    print(f"=== {sym} ===")
    print("Market price:", m.get('price', {}).get('last'))
    print("Auction Day:", m.get('auction', {}).get('day'))
    print("Auction Sess:", m.get('auction', {}).get('session'))
    print("VWAP:", m.get('vwap', {}).get('vwap'))
    print("EMA H4:", m.get('ema', {}).get('h4'))
    print("RSI H4:", m.get('rsi', {}).get('h4'))
    print("Signals:", [s.get('type') for st in sig.get('sets', []) for s in st.get('sigs', [])])
    print("Narrative Model/Grade:", n.get('activeModel'), n.get('grade'), n.get('confidence'), n.get('evR'))
    print("Liq Magnet:", l.get('clusters', [])[:2] if isinstance(l.get('clusters'), list) else l.get('ok'))
