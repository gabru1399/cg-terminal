import urllib.request
import json

targets = [
    {'sym': 'LTC', 'delta_sym': 'LTCUSD', 'prod_id': 15040, 'contract_val': 0.1},
    {'sym': 'AVAX', 'delta_sym': 'AVAXUSD', 'prod_id': 14830, 'contract_val': 1.0},
    {'sym': 'DOGE', 'delta_sym': 'DOGEUSD', 'prod_id': 14745, 'contract_val': 100.0},
    {'sym': 'ADA', 'delta_sym': 'ADAUSD', 'prod_id': 16614, 'contract_val': 1.0},
    {'sym': 'XRP', 'delta_sym': 'XRPUSD', 'prod_id': 14969, 'contract_val': 1.0},
    {'sym': 'DOT', 'delta_sym': 'DOTUSD', 'prod_id': 15304, 'contract_val': 1.0},
    {'sym': 'NEAR', 'delta_sym': 'NEARUSD', 'prod_id': 16615, 'contract_val': 1.0},
    {'sym': 'UNI', 'delta_sym': 'UNIUSD', 'prod_id': 15303, 'contract_val': 1.0},
    {'sym': 'TRX', 'delta_sym': 'TRXUSD', 'prod_id': 20193, 'contract_val': 1.0}
]

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Auditor/2.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

print("Auditing tradable altcoin candidates on Delta Exchange India CLOB...")

viable = []

for t in targets:
    sym = t['sym']
    mkt = fetch_json(f'http://127.0.0.1:3000/api/cg/market?sym={sym}')
    nar = fetch_json(f'http://127.0.0.1:3000/api/cg/narrative?sym={sym}')
    liq = fetch_json(f'http://127.0.0.1:3000/api/cg/liqlevels?sym={sym}')
    cvd = fetch_json(f'http://127.0.0.1:3000/api/cg/cvd?sym={sym}')
    bw = fetch_json(f'http://127.0.0.1:3000/api/cg/bookwalls?sym={sym}')
    sig = fetch_json(f'http://127.0.0.1:3000/api/cg/signals?sym={sym}')
    
    if not mkt or not nar:
        continue
        
    price = float(mkt.get('price', {}).get('last') or 0)
    if price <= 0:
        continue
        
    regime = nar.get('regime', 'UNKNOWN')
    active_model = nar.get('activeModel', 'UNKNOWN')
    
    auction = mkt.get('auction', {})
    day_auc = auction.get('day', {})
    day_poc = float(day_auc.get('poc') or 0)
    day_vah = float(day_auc.get('vah') or 0)
    day_val = float(day_auc.get('val') or 0)
    
    sess_auc = auction.get('session', {})
    sess_poc = float(sess_auc.get('poc') or 0)
    
    month_auc = auction.get('month', {})
    month_poc = float(month_auc.get('poc') or 0)
    
    vwap_info = mkt.get('vwap', {})
    vwap = float(vwap_info.get('vwap') or 0)
    sd1 = float(vwap_info.get('bands', {}).get('sd1') or 0)
    z = (price - vwap) / sd1 if sd1 > 0 else 0
    
    emas = mkt.get('ema', {})
    h4_trend = 'DOWN' if emas.get('h4', {}).get('e13', 0) < emas.get('h4', {}).get('e89', 0) else 'UP'
    d1_trend = 'DOWN' if emas.get('d1', {}).get('e13', 0) < emas.get('d1', {}).get('e89', 0) else 'UP'
    
    # Liquidation clusters
    clusters = liq.get('clusters', []) if liq else []
    
    # Calculate ±2% LSR
    sa_2pct = sum(float(c.get('usd', 0)) for c in clusters if price < float(c.get('price', 0)) <= price * 1.02)
    lb_2pct = sum(float(c.get('usd', 0)) for c in clusters if price * 0.98 <= float(c.get('price', 0)) < price)
    lsr_2pct = sa_2pct / lb_2pct if lb_2pct > 0 else (99.0 if sa_2pct > 0 else 1.0)
    
    # Let's test a Short Setup S1 / S2 / S5
    # S1 entry: above Day VAH, front-running upper resistance / wall, targeting Day POC / VAL
    entry = max(day_vah, price * 1.008)
    sl = entry * 1.022  # ~2.2% stop
    tp = day_poc if day_poc < price else vwap
    
    # If Day POC is above price, target Day VAL
    if tp >= entry or (entry - tp) / entry < 0.01:
        tp = day_val if day_val < price else price * 0.97
        
    risk = sl - entry
    reward = entry - tp
    r_mult = reward / risk if risk > 0 else 0
    
    # Check Gate 1: SL distance from Day POC, Sess POC, Month POC, VWAP
    g1_dist_day = abs(sl - day_poc) / sl if sl > 0 else 0
    g1_dist_sess = abs(sl - sess_poc) / sl if sl > 0 else 0
    g1_dist_vwap = abs(sl - vwap) / sl if sl > 0 else 0
    g1_pass = g1_dist_day >= 0.008 and g1_dist_sess >= 0.008 and g1_dist_vwap >= 0.008
    
    # Check Gate 2:
    # Vector A (Traversal Fuel: clusters between price and entry)
    traversal_clusters = [c for c in clusters if price < float(c.get('price', 0)) <= entry]
    traversal_fuel = sum(float(c.get('usd', 0)) for c in traversal_clusters)
    
    # Vector B (Risk Zone Hazard: clusters between entry and sl)
    hazard_clusters = [c for c in clusters if entry < float(c.get('price', 0)) <= sl]
    hazard_usd = sum(float(c.get('usd', 0)) for c in hazard_clusters)
    max_hazard_usd = max([float(c.get('usd', 0)) for c in hazard_clusters]) if hazard_clusters else 0
    
    g2_pass = (max_hazard_usd < 2000000) and (hazard_usd / (traversal_fuel + 1) < 2.5)
    
    # Confluence Table 7 scoring:
    t7 = 0.0
    # 1. Trend
    if h4_trend == 'DOWN' and d1_trend == 'DOWN':
        t7 += 0.0 if regime == 'RANGE_BALANCE' else 2.0  # Regime penalty
    # 2. VWAP Regime
    if z >= 1.0:
        t7 += 1.5
    elif z >= 0.5:
        t7 += 1.0
    # 3. Footprint signal
    # 4. Whale wall
    # 5. CVD
    cvd_delta = float(cvd.get('cvd', {}).get('delta24h', 0)) if cvd else 0
    if cvd_delta < 0:
        t7 += 1.0  # Bearish CVD alignment / divergence
    # 6. Magnet Gate
    if g2_pass and traversal_fuel > 0:
        t7 += 1.5
    # 7. GEX (altcoin n/a = 0)
    # 8. Spread
    t7 += 1.0  # Standard liquid crypto perp on Delta
    
    margin_25x = (price * t['contract_val']) / 25.0
    
    print(f"\n================ {sym} ({t['delta_sym']}) ================")
    print(f"Price: {price} | Day POC: {day_poc} | Day VAH: {day_vah} | Day VAL: {day_val} | Sess POC: {sess_poc}")
    print(f"VWAP: {vwap:.4f} (z = {z:.2f}σ) | Regime: {regime} | H4: {h4_trend}, D1: {d1_trend}")
    print(f"LSR (±2%): {lsr_2pct:.2f}:1 (Shorts Above: ${sa_2pct:,.0f} vs Longs Below: ${lb_2pct:,.0f})")
    print(f"Proposed Short Setup: Entry={entry:.4f}, SL={sl:.4f}, TP={tp:.4f} -> R={r_mult:.2f}R")
    print(f"Gate 1: Day dist={g1_dist_day*100:.1f}%, Sess dist={g1_dist_sess*100:.1f}%, VWAP dist={g1_dist_vwap*100:.1f}% -> {'PASS' if g1_pass else 'FAIL'}")
    print(f"Gate 2: Traversal Fuel=${traversal_fuel:,.0f} ({len(traversal_clusters)} clusters) | Hazard USD=${hazard_usd:,.0f} (Max=${max_hazard_usd:,.0f}) -> {'PASS' if g2_pass else 'FAIL'}")
    print(f"Table 7 Confluence Score: {t7:.2f} / 11.5 pts")
    print(f"Margin 25x for 1 contract: ${margin_25x:.4f} USD (Available: $0.9534 USD)")
    
    if g1_pass and g2_pass and t7 >= 5.0 and r_mult >= 1.5 and margin_25x <= 0.80:
        viable.append({
            'sym': sym,
            'delta_sym': t['delta_sym'],
            'prod_id': t['prod_id'],
            'contract_val': t['contract_val'],
            'price': price,
            'entry': entry,
            'sl': sl,
            'tp': tp,
            'r_mult': r_mult,
            't7': t7,
            'margin_25x': margin_25x,
            'lsr_2pct': lsr_2pct,
            'traversal_fuel': traversal_fuel,
            'hazard_usd': hazard_usd,
            'z': z
        })

print("\n" + "="*60)
print(f"VIABLE HIGH-CONFLUENCE CANDIDATES: {len(viable)}")
for v in viable:
    print(f"--> {v['sym']} ({v['delta_sym']}): Entry={v['entry']:.4f}, SL={v['sl']:.4f}, TP={v['tp']:.4f}, R={v['r_mult']:.2f}R, T7={v['t7']:.1f} pts, Margin=${v['margin_25x']:.3f}")
