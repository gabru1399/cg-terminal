import urllib.request
import json
import time

candidates = ['BTC', 'ETH', 'LTC', 'AVAX', 'LINK', 'UNI', 'DOGE', 'TRX', 'DOT', 'FIL', 'APT', 'ARB', 'SUI', 'TIA', 'ADA', 'XRP']

def fetch_json(url):
    try:
        req = urllib.request.Request(f'http://127.0.0.1:3000{url}', headers={'User-Agent': 'Hunter/2.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

results = []

for sym in candidates:
    mkt = fetch_json(f'/api/cg/market?sym={sym}')
    if not mkt or not mkt.get('ok'):
        continue
    price = mkt.get('price', {}).get('last', 0)
    auction = mkt.get('auction', {})
    day_poc = auction.get('day', {}).get('poc', 0)
    day_vah = auction.get('day', {}).get('vah', 0)
    day_val = auction.get('day', {}).get('val', 0)
    vwap = mkt.get('vwap', {}).get('vwap', 0)
    bands = mkt.get('vwap', {}).get('bands', {})
    sd1 = bands.get('sd1', 1)
    z = (price - vwap) / sd1 if sd1 else 0
    
    ema = mkt.get('ema', {})
    h4_trend = 'BULL' if ema.get('h4', {}).get('e13', 0) > ema.get('h4', {}).get('e89', 0) else 'BEAR'
    d1_trend = 'BULL' if ema.get('d1', {}).get('e13', 0) > ema.get('d1', {}).get('e89', 0) else 'BEAR'
    rsi_15m = mkt.get('rsi', {}).get('m15', 50)
    
    liq = fetch_json(f'/api/cg/liqlevels?sym={sym}&range=3d&lvR=4')
    lsr = 1.0
    shorts_above = 0
    longs_below = 0
    clusters_above = []
    clusters_below = []
    if liq and liq.get('ok'):
        stats = liq.get('stats', {})
        shorts_above = stats.get('totals', {}).get('shorts', 0)
        longs_below = stats.get('totals', {}).get('longs', 0)
        if longs_below > 0:
            lsr = shorts_above / longs_below
        key_levels = stats.get('keyLevels', {})
        clusters_above = key_levels.get('above', [])
        clusters_below = key_levels.get('below', [])
        
    sig = fetch_json(f'/api/cg/signals?sym={sym}')
    sig_count = 0
    recent_sigs = []
    if sig and sig.get('ok'):
        sig_count = sig.get('counts', {}).get('all', 0)
        for s_set in sig.get('sets', []):
            for s in s_set.get('sigs', [])[-3:]:
                recent_sigs.append(f"{s.get('side')}:{s.get('t')}@{s.get('p')}")
                
    bw = fetch_json(f'/api/cg/bookwalls?sym={sym}')
    ask_walls = []
    bid_walls = []
    if bw and bw.get('ok'):
        for w in bw.get('walls', []):
            if w.get('side') == 'ask' and w.get('usd', 0) >= 500000:
                ask_walls.append(f"${w.get('usd')/1e6:.1f}M@{w.get('price')}")
            elif w.get('side') == 'bid' and w.get('usd', 0) >= 500000:
                bid_walls.append(f"${w.get('usd')/1e6:.1f}M@{w.get('price')}")
                
    results.append({
        'sym': sym,
        'price': price,
        'h4_trend': h4_trend,
        'd1_trend': d1_trend,
        'z': round(z, 2),
        'vwap': round(vwap, 4),
        'day_poc': round(day_poc, 4),
        'day_vah': round(day_vah, 4),
        'day_val': round(day_val, 4),
        'lsr': round(lsr, 2),
        'shorts_above_k': round(shorts_above / 1000, 1),
        'longs_below_k': round(longs_below / 1000, 1),
        'sig_count': sig_count,
        'recent_sigs': recent_sigs[:3],
        'ask_walls': ask_walls[:2],
        'bid_walls': bid_walls[:2],
        'clusters_above_cnt': len(clusters_above),
        'clusters_below_cnt': len(clusters_below),
    })

print(f"{'SYM':6} | {'Price':10} | {'H4':4} | {'D1':4} | {'z-sc':5} | {'LSR':5} | {'ShAbove':8} | {'LgBelow':8} | {'AskWalls':12} | {'BidWalls':12}")
print("-" * 95)
for r in results:
    aw = ', '.join(r['ask_walls']) if r['ask_walls'] else 'none'
    bw = ', '.join(r['bid_walls']) if r['bid_walls'] else 'none'
    print(f"{r['sym']:6} | {r['price']:10.4f} | {r['h4_trend']:4} | {r['d1_trend']:4} | {r['z']:5.2f} | {r['lsr']:5.2f} | {r['shorts_above_k']:8.1f}k | {r['longs_below_k']:8.1f}k | {aw[:12]:12} | {bw[:12]:12}")

with open('desk/candidate_screen_r281.json', 'w') as f:
    json.dump(results, f, indent=2)
