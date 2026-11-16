import urllib.request
import json

targets = [
    {'sym': 'LTC', 'delta_sym': 'LTCUSD', 'prod_id': 15040, 'contract_val': 0.1, 'tick': 0.01},
    {'sym': 'AVAX', 'delta_sym': 'AVAXUSD', 'prod_id': 14830, 'contract_val': 1.0, 'tick': 0.0001},
    {'sym': 'DOGE', 'delta_sym': 'DOGEUSD', 'prod_id': 14745, 'contract_val': 100.0, 'tick': 0.000001},
    {'sym': 'ADA', 'delta_sym': 'ADAUSD', 'prod_id': 16614, 'contract_val': 1.0, 'tick': 0.00001},
    {'sym': 'XRP', 'delta_sym': 'XRPUSD', 'prod_id': 14969, 'contract_val': 1.0, 'tick': 0.0001},
    {'sym': 'DOT', 'delta_sym': 'DOTUSD', 'prod_id': 15304, 'contract_val': 1.0, 'tick': 0.001},
    {'sym': 'NEAR', 'delta_sym': 'NEARUSD', 'prod_id': 16615, 'contract_val': 1.0, 'tick': 0.0001},
    {'sym': 'UNI', 'delta_sym': 'UNIUSD', 'prod_id': 15303, 'contract_val': 1.0, 'tick': 0.0001},
    {'sym': 'SOL', 'delta_sym': 'SOLUSD', 'prod_id': 14823, 'contract_val': 1.0, 'tick': 0.0001},
    {'sym': 'TRX', 'delta_sym': 'TRXUSD', 'prod_id': 20193, 'contract_val': 1.0, 'tick': 0.00001}
]

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Auditor/2.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

print("=== SCREENING ALL TRADABLE ALTCOINS FOR SOP v1.2.0 CONFLUENCE ===")

candidates = []

for t in targets:
    sym = t['sym']
    mkt = fetch_json(f'http://127.0.0.1:3000/api/cg/market?sym={sym}')
    nar = fetch_json(f'http://127.0.0.1:3000/api/cg/narrative?sym={sym}')
    liq = fetch_json(f'http://127.0.0.1:3000/api/cg/liqlevels?sym={sym}')
    cvd = fetch_json(f'http://127.0.0.1:3000/api/cg/cvd?sym={sym}')
    sig = fetch_json(f'http://127.0.0.1:3000/api/cg/signals?sym={sym}')
    bw = fetch_json(f'http://127.0.0.1:3000/api/cg/bookwalls?sym={sym}')
    
    if not mkt or not mkt.get('price'):
        continue
        
    last_price = float(mkt['price'].get('last') or 0)
    if last_price <= 0:
        continue
        
    regime = nar.get('regime', 'UNKNOWN') if nar else 'UNKNOWN'
    
    # Auction
    day_auc = mkt.get('auction', {}).get('day', {})
    day_poc = float(day_auc.get('poc') or 0)
    day_vah = float(day_auc.get('vah') or 0)
    day_val = float(day_auc.get('val') or 0)
    sess_poc = float(mkt.get('auction', {}).get('session', {}).get('poc') or 0)
    
    vwap_val = float(mkt.get('vwap', {}).get('vwap') or 0)
    sd1 = float(mkt.get('vwap', {}).get('bands', {}).get('sd1') or 0)
    z_score = (last_price - vwap_val) / sd1 if sd1 > 0 else 0
    
    emas = mkt.get('ema', {})
    h4_trend = 'DOWN' if emas.get('h4', {}).get('e13', 0) < emas.get('h4', {}).get('e89', 0) else 'UP'
    d1_trend = 'DOWN' if emas.get('d1', {}).get('e13', 0) < emas.get('d1', {}).get('e89', 0) else 'UP'
    
    # Liq keyLevels
    liq_stats = liq.get('stats', {}) if liq else {}
    bands_liq = liq_stats.get('bands', [])
    key_levels = liq_stats.get('keyLevels', {})
    above_clusters = key_levels.get('above', [])
    below_clusters = key_levels.get('below', [])
    
    shorts_2pct = 0
    longs_2pct = 0
    if len(bands_liq) >= 2:
        shorts_2pct = float(bands_liq[0].get('up', 0)) + float(bands_liq[1].get('up', 0))
        longs_2pct = float(bands_liq[0].get('down', 0)) + float(bands_liq[1].get('down', 0))
    lsr_2pct = shorts_2pct / longs_2pct if longs_2pct > 0 else (99.0 if shorts_2pct > 0 else 1.0)
    
    # Check signals
    all_sigs = []
    if sig and sig.get('sets'):
        for s in sig['sets']:
            if s.get('sigs'):
                all_sigs.extend(s['sigs'])
    all_sigs.sort(key=lambda x: x.get('ts', 0), reverse=True)
    recent_bear_sigs = [s for s in all_sigs if s.get('side') in ['sell', 'bear'] and s.get('t') in ['abs', 'sdiv', 'div', 'trap', 'exh']]
    
    # Propose Short Setup S1
    # Entry at upper resistance (day VAH or nearest upper cluster)
    entry = max(day_vah, last_price * 1.008)
    sl = entry * 1.022
    tp = day_poc if day_poc < last_price else (day_val if day_val < last_price else last_price * 0.97)
    
    risk = sl - entry
    reward = entry - tp
    r_mult = reward / risk if risk > 0 else 0
    
    # Gate 1
    g1_dist_day = abs(sl - day_poc) / sl if sl > 0 else 0
    g1_dist_sess = abs(sl - sess_poc) / sl if sl > 0 else 0
    g1_dist_vwap = abs(sl - vwap_val) / sl if sl > 0 else 0
    gate1_pass = g1_dist_day >= 0.008 and g1_dist_sess >= 0.008 and g1_dist_vwap >= 0.008
    
    # Gate 2
    traversal_clusters = [c for c in above_clusters if last_price <= float(c.get('price', 0)) <= entry]
    risk_zone_clusters = [c for c in above_clusters if entry < float(c.get('price', 0)) <= (sl * 1.005)]
    traversal_fuel = sum(float(c.get('usd', 0)) for c in traversal_clusters)
    hazard_usd = sum(float(c.get('usd', 0)) for c in risk_zone_clusters)
    max_hazard = max([float(c.get('usd', 0)) for c in risk_zone_clusters]) if risk_zone_clusters else 0
    gate2_pass = (max_hazard < 3000000) and (lsr_2pct < 2.5 or traversal_fuel > hazard_usd)
    
    # Table 7 scoring
    t7 = 0.0
    # Trend
    if regime == 'RANGE_BALANCE':
        t7 += 0.0
    else:
        if h4_trend == 'DOWN' and d1_trend == 'DOWN':
            t7 += 2.0
    # VWAP
    if z_score >= 1.0:
        t7 += 1.5
    elif z_score >= 0.5:
        t7 += 1.0
    # Signal
    sig_bonus = 0.0
    for s in recent_bear_sigs[:5]:
        sp = float(s.get('p') or 0)
        if abs(sp - entry) / entry <= 0.02:
            sig_bonus = 2.0
            break
        elif abs(sp - last_price) / last_price <= 0.015:
            sig_bonus = 1.0
            break
    t7 += sig_bonus
    # Wall
    # CVD
    cvd_delta = float(cvd.get('cvd', {}).get('delta24h', 0)) if cvd else 0
    if cvd_delta < 0:
        t7 += 1.0
    # Magnet
    if gate2_pass and (traversal_fuel > 0 or lsr_2pct < 2.0):
        t7 += 1.5
    # Spread
    t7 += 1.0
    
    margin_25x = (last_price * t['contract_val']) / 25.0
    margin_50x = (last_price * t['contract_val']) / 50.0
    
    candidates.append({
        'sym': sym,
        'delta_sym': t['delta_sym'],
        'prod_id': t['prod_id'],
        'contract_val': t['contract_val'],
        'tick': t['tick'],
        'price': last_price,
        'entry': entry,
        'sl': sl,
        'tp': tp,
        'r_mult': r_mult,
        'vwap_z': z_score,
        'regime': regime,
        'lsr': lsr_2pct,
        'g1_pass': gate1_pass,
        'g2_pass': gate2_pass,
        'traversal_fuel': traversal_fuel,
        'hazard_usd': hazard_usd,
        't7': t7,
        'sig_bonus': sig_bonus,
        'margin_25x': margin_25x,
        'margin_50x': margin_50x
    })

print(f"\n{'SYM':<6} | {'PRICE':<9} | {'VWAP z':<7} | {'LSR':<7} | {'SIG':<4} | {'G1':<4} | {'G2':<4} | {'T7':<4} | {'R':<5} | {'MARG 25x':<9} | {'STATUS'}")
print("-" * 80)
for c in candidates:
    viable = c['g1_pass'] and c['g2_pass'] and c['t7'] >= 5.0 and c['r_mult'] >= 1.5 and c['margin_25x'] <= 0.90
    stat = "ELIGIBLE (GRADE A/B)" if viable else ("GATED (T7<5.0)" if c['t7'] < 5.0 else ("GATED (MARGIN)" if c['margin_25x'] > 0.90 else "GATED (R/GATE)"))
    print(f"{c['sym']:<6} | ${c['price']:<8.4f} | {c['vwap_z']:<5.2f}σ | {c['lsr']:<5.2f}:1 | {c['sig_bonus']:<4.1f} | {'PASS' if c['g1_pass'] else 'FAIL':<4} | {'PASS' if c['g2_pass'] else 'FAIL':<4} | {c['t7']:<4.1f} | {c['r_mult']:<4.2f}R | ${c['margin_25x']:<8.4f} | {stat}")
