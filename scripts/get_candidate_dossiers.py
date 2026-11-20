import urllib.request
import json

symbols = ['BERA', 'ENA', 'BNB', 'XAG', 'SOL', 'BTC']
base = 'http://127.0.0.1:3000/api/cg'

for sym in symbols:
    print(f"\n==================== {sym} FORENSIC DOSSIER ====================")
    try:
        m_req = urllib.request.urlopen(f"{base}/market?sym={sym}")
        m = json.loads(m_req.read().decode())
        price = m.get('price')
        vwap = m.get('vwap') or (m.get('vwapDay') or {}).get('vwap')
        poc = m.get('poc') or (m.get('auctionDay') or {}).get('poc')
        print(f"Price: {price} | Day VWAP: {vwap} | Day POC: {poc}")
    except Exception as e:
        print(f"Market fetch error: {e}")

    try:
        s_req = urllib.request.urlopen(f"{base}/signals?sym={sym}")
        s = json.loads(s_req.read().decode())
        signals = s.get('signals', s.get('result', []))
        print(f"Signals: {len(signals)} found")
        for sig in signals[:3]:
            print(f"  -> {sig.get('title')} ({sig.get('side')}) | bar_type={sig.get('bar_type')} | tf={sig.get('timeframe')}")
    except Exception as e:
        print(f"Signals fetch error: {e}")

    try:
        b_req = urllib.request.urlopen(f"{base}/bookwalls?sym={sym}")
        b = json.loads(b_req.read().decode())
        walls = b.get('walls', [])
        print(f"Bookwalls: {len(walls)} walls found")
        for w in walls[:4]:
            print(f"  -> Wall: side={w.get('side')}, price={w.get('price')}, notional={w.get('notionalUsd')}, distPct={w.get('distPct')}")
    except Exception as e:
        print(f"Bookwalls fetch error: {e}")

    try:
        l_req = urllib.request.urlopen(f"{base}/liqlevels?sym={sym}&range=3d")
        l = json.loads(l_req.read().decode())
        clusters = l.get('clusters', l.get('levels', []))
        print(f"3D Liq Clusters: {len(clusters)} clusters")
        for c in clusters[:4]:
            print(f"  -> Liq: side={c.get('side')}, price={c.get('price')}, volUsd={c.get('volUsd') or c.get('usd')}")
    except Exception as e:
        print(f"Liq fetch error: {e}")
