import urllib.request
import json
import time

def fetch_json(endpoint):
    url = f"http://127.0.0.1:3000{endpoint}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return None

def analyze_single_asset(sym):
    print(f"\n=======================================================")
    print(f"INDIVIDUAL DEEP ASSET AUDIT: {sym}")
    print(f"=======================================================")
    
    # 1. Market Overview
    market = fetch_json(f"/api/cg/market?sym={sym}")
    price_info = market.get('price', {}) if market else {}
    last_price = price_info.get('last')
    day_poc = market.get('dayPoc') if market else None
    day_vwap = market.get('dayVwap') if market else None
    print(f"1. Market Overview  : Last={last_price} | Day POC={day_poc} | Day VWAP={day_vwap}")
    
    # 2. Footprint Signals
    signals = fetch_json(f"/api/cg/signals?sym={sym}")
    sig_list = signals.get('signals', []) if signals else []
    print(f"2. Footprint Signals: Total discrete signals={len(sig_list)}")
    if sig_list:
        for s in sig_list[:3]:
            print(f"   -> {s.get('type')} ({s.get('side')}) @ {s.get('price')} (bar: {s.get('barTime')})")
            
    # 3. Liquidation Levels & LSR
    liq = fetch_json(f"/api/cg/liqlevels?sym={sym}")
    clusters = liq.get('clusters', []) if liq else []
    lsr = liq.get('lsr') if liq else None
    print(f"3. Liq Levels & LSR : LSR={lsr} | Total Clusters={len(clusters)}")
    if clusters:
        for c in clusters[:2]:
            print(f"   -> Pool: ${c.get('volUsd', 0):,.0f} @ {c.get('price')} (dist: {c.get('distPct')}%)")
            
    # 4. Book Walls
    walls = fetch_json(f"/api/cg/bookwalls?sym={sym}")
    bids = walls.get('bids', []) if walls else []
    asks = walls.get('asks', []) if walls else []
    print(f"4. Order Book Walls : Bids={len(bids)} | Asks={len(asks)}")
    
    # 5. CVD State
    cvd = fetch_json(f"/api/cg/cvd?sym={sym}")
    cvd_delta = cvd.get('delta24h') if cvd else None
    taker_buy = cvd.get('takerBuyShare') if cvd else None
    print(f"5. CVD Telemetry    : 24h Delta={cvd_delta} | Taker Buy Share={taker_buy}%")
    
    # 6. Narrative & Regime
    narrative = fetch_json(f"/api/cg/narrative?sym={sym}")
    regime = narrative.get('regime') if narrative else None
    active_model = narrative.get('activeModel') if narrative else None
    ladder = narrative.get('ladder', {}) if narrative else {}
    print(f"6. Narrative Regime : Regime={regime} | Model={active_model}")
    print(f"   -> Ladder: L1={ladder.get('L1')} | L2={ladder.get('L2')} | SL={ladder.get('SL')} | T1={ladder.get('T1')}")

if __name__ == '__main__':
    assets_to_audit = ['MSFT', 'AVGO', 'NVDA', 'BTC', 'APT', 'ADA', 'ARB', 'SEI', 'TIA']
    for a in assets_to_audit:
        analyze_single_asset(a)
        time.sleep(0.2)
