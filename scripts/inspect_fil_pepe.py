import urllib.request
import json

def fetch(ep, sym):
    url = f"http://127.0.0.1:3000/api/cg/{ep}?sym={sym}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

for sym in ['FIL', '1000PEPE']:
    print(f"================== FORENSICS FOR {sym} ==================")
    m = fetch('market', sym)
    auc = m.get('auction', {})
    vw = m.get('vwap', {})
    print(f"[market] Price: {m.get('price',{}).get('last')}, 8h POC: {auc.get('session',{}).get('poc')}, Day POC: {auc.get('day',{}).get('poc')}, Day VAH: {auc.get('day',{}).get('vah')}, Day VAL: {auc.get('day',{}).get('val')}, VWAP: {vw.get('vwap')}, z: {vw.get('z')}")
    
    narr = fetch('narrative', sym)
    print(f"[narrative] Regime: {narr.get('regime')}, Model: {narr.get('activeModel')}, Direction: {narr.get('direction')}, Conf: {narr.get('confidence')}")
    print(f"  Thesis: {narr.get('thesis')}")
    
    sigs = fetch('signals', sym)
    sets = sigs.get('sets', [])
    print(f"[signals] Sets: {len(sets)}")
    for s in sets:
        sig_list = s.get('sigs', [])
        if sig_list:
            print(f"  BarType {s.get('barType')} {s.get('interval')}: {len(sig_list)} signals -> {[x.get('type') for x in sig_list[:3]]}")
            
    bw = fetch('bookwalls', sym)
    print(f"[bookwalls] Walls count: {len(bw.get('model',{}).get('walls',[]))}, Imbalance: {bw.get('model',{}).get('depthImbalance')}")
    
    liq = fetch('liqlevels', sym)
    st = liq.get('stats', {})
    print(f"[liqlevels] Totals: shorts {st.get('totals',{}).get('shorts')}, longs {st.get('totals',{}).get('longs')}")
    print(f"  Key levels above: {st.get('keyLevels',{}).get('above',[])[:2]}")
    print(f"  Key levels below: {st.get('keyLevels',{}).get('below',[])[:2]}")
    print(f"  Bands: {st.get('bands',[])[:3]}")
    
    cvd = fetch('cvd', sym)
    print(f"[cvd] Divergences: {len(cvd.get('divergences',[]))}, Ratio: {cvd.get('ratio',[])[-1] if cvd.get('ratio') else 'n/a'}")
