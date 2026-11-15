import urllib.request
import json

def fetch(ep, sym):
    url = f"http://127.0.0.1:3000/api/cg/{ep}?sym={sym}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

for sym in ['1000PEPE', 'BTC', 'TRX']:
    print(f"================== {sym} ==================")
    narr = fetch('narrative', sym)
    print("Regime:", narr.get('regime'))
    print("Active Model:", narr.get('activeModel'))
    print("Direction:", narr.get('direction'))
    print("Grade:", narr.get('grade'), "Conf:", narr.get('confidence'))
    print("Thesis:", narr.get('thesis'))
    
    sigs = fetch('signals', sym)
    sets = sigs.get('sets', [])
    print("Signal sets count:", len(sets))
    for s in sets:
        sig_list = s.get('sigs', [])
        if sig_list:
            print(f"  BarType {s.get('barType')} {s.get('interval')}: {len(sig_list)} signals -> {[x.get('type') for x in sig_list[:3]]}")
            
    bw = fetch('bookwalls', sym)
    print("Bookwalls model:", bw.get('model', {}).get('depthImbalance'), "Walls:", len(bw.get('model', {}).get('walls', [])))
    
    liq = fetch('liqlevels', sym)
    print("Liq stats:", liq.get('stats'))
    
    cvd = fetch('cvd', sym)
    print("CVD divs:", cvd.get('divergences'), "Ratio:", cvd.get('ratio'))
