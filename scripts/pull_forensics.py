import urllib.request
import json
import sys

symbols = ['1000PEPE', 'BTC', 'TRX']

for sym in symbols:
    print(f"=== FORENSICS FOR {sym} ===")
    for ep in ['market', 'narrative', 'signals', 'bookwalls', 'liqlevels', 'cvd']:
        try:
            url = f"http://127.0.0.1:3000/api/cg/{ep}?sym={sym}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                if ep == 'market':
                    auc = data.get('auction', {})
                    vw = data.get('vwap', {})
                    print(f"  [market] Price: {data.get('price')}, 8h POC: {auc.get('session',{}).get('poc')}, Day POC: {auc.get('day',{}).get('poc')}, Day VAH: {auc.get('day',{}).get('vah')}, Day VAL: {auc.get('day',{}).get('val')}, VWAP: {vw.get('vwap')}, z: {vw.get('z')}")
                elif ep == 'narrative':
                    reg = data.get('regime', {})
                    print(f"  [narrative] Regime: {reg.get('macro')}, Model: {data.get('activeModel')}, Direction: {data.get('direction')}, Conf: {data.get('confidence')}")
                elif ep == 'signals':
                    sigs = data.get('signals', [])
                    print(f"  [signals] Count: {len(sigs)}, Recent: {[{'type': s.get('type'), 'dir': s.get('dir'), 'price': s.get('price')} for s in sigs[:3]]}")
                elif ep == 'bookwalls':
                    walls = data.get('walls', [])
                    print(f"  [bookwalls] Walls count: {len(walls)}, Depth Imbalance: {data.get('imbalance')}")
                elif ep == 'liqlevels':
                    pools = data.get('levels', [])
                    print(f"  [liqlevels] Levels count: {len(pools)}, LSR: {data.get('lsr')}, Skew: {data.get('skew')}")
                elif ep == 'cvd':
                    print(f"  [cvd] Divergence: {data.get('divergence')}, TakerBuyShare: {data.get('takerBuyShare')}, Perp Delta: {data.get('perpDelta')}")
        except Exception as e:
            print(f"  [{ep}] Error: {e}")
