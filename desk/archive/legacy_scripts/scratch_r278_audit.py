import urllib.request
import json
import math

symbols = ['UNI', 'LTC', 'XRP', 'AVAX', 'DOT', 'LINK']

orders = {
    'UNI': {'id': 1684181417, 'status': 'cancelled', 'entry': 5.240, 'sl': 5.350, 'tp': 5.020, 'side': 'sell'},
    'LTC': {'id': 1684220876, 'status': 'open', 'entry': 45.480, 'sl': 45.850, 'tp': 44.650, 'side': 'sell', 'tick': 0.01, 'claimed_t7': 6.25},
    'XRP': {'id': 1684221233, 'status': 'open', 'entry': 0.9780, 'sl': 0.9860, 'tp': 0.9620, 'side': 'sell', 'tick': 0.0001, 'claimed_t7': 6.00},
    'AVAX': {'id': 1684181155, 'status': 'open', 'entry': 7.420, 'sl': 7.580, 'tp': 7.020, 'side': 'sell', 'tick': 0.0001},
    'DOT': {'id': 1684152529, 'status': 'open', 'entry': 0.748, 'sl': 0.762, 'tp': 0.718, 'side': 'sell', 'tick': 0.001},
    'LINK': {'id': 1683969432, 'status': 'open', 'entry': 9.450, 'sl': 9.680, 'tp': 8.980, 'side': 'sell', 'tick': 0.001}
}

def fetch_json(endpoint):
    url = f'http://127.0.0.1:3000{endpoint}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AdversarialAuditor/3.4'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f'Error fetching {endpoint}: {e}')
        return None

results = {}

for sym in symbols:
    print(f'======================================================================')
    print(f'                     AUDITING TELEMETRY FOR {sym}                      ')
    print(f'======================================================================')
    mkt = fetch_json(f'/api/cg/market?sym={sym}')
    fp = fetch_json(f'/api/cg/fp?sym={sym}')
    liq = fetch_json(f'/api/cg/liqlevels?sym={sym}')
    sig = fetch_json(f'/api/cg/signals?sym={sym}')
    cvd = fetch_json(f'/api/cg/cvd?sym={sym}')
    bw = fetch_json(f'/api/cg/bookwalls?sym={sym}')

    price_info = mkt.get('price', {}) if mkt else {}
    last_price = float(price_info.get('last') or 0)
    
    auction = mkt.get('auction', {}) if mkt else {}
    sess_auc = auction.get('session', {})
    sess_poc = float(sess_auc.get('poc') or 0)
    sess_vah = float(sess_auc.get('vah') or 0)
    sess_val = float(sess_auc.get('val') or 0)
    
    day_auc = auction.get('day', {})
    day_poc = float(day_auc.get('poc') or 0)
    day_vah = float(day_auc.get('vah') or 0)
    day_val = float(day_auc.get('val') or 0)
    
    month_auc = auction.get('month', {})
    month_poc = float(month_auc.get('poc') or 0)
    
    vwap_info = mkt.get('vwap', {}) if mkt else {}
    vwap_val = float(vwap_info.get('vwap') or 0)
    bands = vwap_info.get('bands', {})
    sd1 = float(bands.get('sd1') or 0)
    z_score = (last_price - vwap_val) / sd1 if sd1 > 0 else 0
    
    emas = mkt.get('ema', {}) if mkt else {}
    h4_ema = emas.get('h4', {})
    d1_ema = emas.get('d1', {})
    h4_trend = 'DOWN' if h4_ema.get('e13', 0) < h4_ema.get('e89', 0) else 'UP'
    d1_trend = 'DOWN' if d1_ema.get('e13', 0) < d1_ema.get('e89', 0) else 'UP'
    
    rsis = mkt.get('rsi', {}) if mkt else {}
    
    print(f'Live Price: {last_price}')
    print(f'Session (8h) POC: {sess_poc:.4f} | VAH: {sess_vah:.4f} | VAL: {sess_val:.4f}')
    print(f'Day POC: {day_poc:.4f} | VAH: {day_vah:.4f} | VAL: {day_val:.4f}')
    print(f'Month POC: {month_poc:.4f}')
    print(f'Session VWAP: {vwap_val:.4f} (z: {z_score:.2f}σ)')
    print(f'Trend: H4={h4_trend} (13:{h4_ema.get("e13", 0):.2f}/89:{h4_ema.get("e89", 0):.2f}), D1={d1_trend} (13:{d1_ema.get("e13", 0):.2f}/89:{d1_ema.get("e89", 0):.2f})')
    
    ord_info = orders[sym]
    entry = ord_info['entry']
    sl = ord_info['sl']
    tp = ord_info.get('tp')
    
    # 1. Tick Compliance
    tick = ord_info.get('tick')
    tick_compliant = True
    if tick:
        # Check if entry, sl, tp are integer multiples of tick
        def is_multiple(val, t):
            rem = round(val / t, 6)
            return abs(rem - round(rem)) < 1e-4
        entry_tick_ok = is_multiple(entry, tick)
        sl_tick_ok = is_multiple(sl, tick)
        tp_tick_ok = is_multiple(tp, tick) if tp else True
        tick_compliant = entry_tick_ok and sl_tick_ok and tp_tick_ok
        print(f'Tick Compliance (tick={tick}): Entry={entry_tick_ok}, SL={sl_tick_ok}, TP={tp_tick_ok} -> {"PASS" if tick_compliant else "FAIL"}')
        
    # 2. Gate 1: Profile & Footprint HVN Clearance
    dist_sess_poc = abs(sl - sess_poc) / sess_poc * 100
    dist_day_poc = abs(sl - day_poc) / day_poc * 100
    dist_month_poc = abs(sl - month_poc) / month_poc * 100
    dist_vwap = abs(sl - vwap_val) / vwap_val * 100
    
    print(f'\n--- GATE 1 CLEARANCE FOR SL={sl} ---')
    print(f'  Dist to Session (8h) POC ({sess_poc:.4f}): {dist_sess_poc:.3f}% (Clearance >0.8%: {dist_sess_poc > 0.8})')
    print(f'  Dist to Day POC ({day_poc:.4f}): {dist_day_poc:.3f}% (Clearance >0.8%: {dist_day_poc > 0.8})')
    print(f'  Dist to Month POC ({month_poc:.4f}): {dist_month_poc:.3f}% (Clearance >0.8%: {dist_month_poc > 0.8})')
    print(f'  Dist to Session VWAP ({vwap_val:.4f}): {dist_vwap:.3f}% (Clearance >0.8%: {dist_vwap > 0.8})')
    
    bars = fp.get('bars', []) if fp else []
    fp_hvn_matches = []
    for idx, b in enumerate(bars):
        b_fp = b.get('fp', {})
        tick_fp = float(b_fp.get('tick') or 0)
        lo = float(b_fp.get('lo') or 0)
        bc = b_fp.get('bc', [])
        sc = b_fp.get('sc', [])
        b_vol = b_fp.get('b', [])
        s_vol = b_fp.get('s', [])
        if not bc or not sc or tick_fp == 0: continue
        
        n_bins = min(len(bc), len(sc))
        max_c = -1
        max_i = -1
        max_v = -1
        for i in range(n_bins):
            c_tot = bc[i] + sc[i]
            v_tot = (b_vol[i] if i < len(b_vol) else 0) + (s_vol[i] if i < len(s_vol) else 0)
            if c_tot > max_c:
                max_c = c_tot
                max_i = i
                max_v = v_tot
        if max_i >= 0 and max_c > 10000:
            p_poc = lo + max_i * tick_fp
            d_pct = abs(sl - p_poc) / p_poc * 100
            if d_pct <= 0.8:
                fp_hvn_matches.append({
                    'price': p_poc,
                    'contracts': max_c,
                    'vol': max_v,
                    'dist_pct': d_pct,
                    'ts': b.get('ts')
                })
    print(f'  Footprint Bar POCs (>10k contracts) within ±0.8%: {len(fp_hvn_matches)}')
    for m in fp_hvn_matches:
        print(f"    MATCH: Bar POC {m['price']} | Contracts: {m['contracts']} | Dist: {m['dist_pct']:.3f}%")
        
    gate1_pass = (dist_sess_poc > 0.8) and (dist_day_poc > 0.8) and (dist_month_poc > 0.8) and (dist_vwap > 0.8) and (len(fp_hvn_matches) == 0)
    print(f'GATE 1 VERDICT: {"PASS" if gate1_pass else "FAIL"}')

    # 3. Gate 2: Liquidation Geometry (Vector A vs Vector B)
    print(f'\n--- GATE 2 LIQUIDATION GEOMETRY ---')
    liq_stats = liq.get('stats', {}) if liq else {}
    bands_liq = liq_stats.get('bands', [])
    key_levels = liq_stats.get('keyLevels', {})
    
    below_clusters = key_levels.get('below', [])
    vector_a_clusters = [c for c in below_clusters if tp and tp <= float(c.get('price', 0)) <= entry]
    vector_a_usd = sum(float(c.get('usd', 0)) for c in vector_a_clusters)
    print(f'Vector A Traversal Fuel (toward TP {tp}):')
    print(f'  Clusters between Entry ({entry}) and TP ({tp}): {len(vector_a_clusters)} (Total: ${vector_a_usd:,.2f})')
    for c in vector_a_clusters:
        print(f"    Cluster @ {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f}")
        
    above_clusters = key_levels.get('above', [])
    vector_b_clusters = [c for c in above_clusters if entry <= float(c.get('price', 0)) <= sl]
    vector_b_usd = sum(float(c.get('usd', 0)) for c in vector_b_clusters)
    print(f'Vector B Risk Zone Hazard (between Entry {entry} and SL {sl}):')
    print(f'  Clusters in Risk Zone: {len(vector_b_clusters)} (Total: ${vector_b_usd:,.2f})')
    for c in vector_b_clusters:
        print(f"    HAZARD Cluster @ {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f}")
        
    shorts_2pct = 0
    longs_2pct = 0
    if len(bands_liq) >= 2:
        shorts_2pct = float(bands_liq[0].get('up', 0)) + float(bands_liq[1].get('up', 0))
        longs_2pct = float(bands_liq[0].get('down', 0)) + float(bands_liq[1].get('down', 0))
    dom_2pct = "SA" if shorts_2pct >= longs_2pct else "LB"
    skew_2pct_ratio = max(shorts_2pct, longs_2pct) / min(shorts_2pct, longs_2pct) if min(shorts_2pct, longs_2pct) > 0 else 999
    print(f'±2% Liquidation Skew: {skew_2pct_ratio:.2f}:1 ({dom_2pct}) | Shorts Above: ${shorts_2pct:,.2f} | Longs Below: ${longs_2pct:,.2f}')

    gate2_breach_lsr = (skew_2pct_ratio >= 2.5 and dom_2pct == "SA")
    gate2_pass = (not gate2_breach_lsr) and (len(vector_b_clusters) == 0)
    print(f'GATE 2 VERDICT: {"PASS" if gate2_pass else "FAIL"} (LSR Breach: {gate2_breach_lsr}, Vector B Hazard: ${vector_b_usd:,.2f})')

    # 4. Table 7 Scoring
    print(f'\n--- TABLE 7 SCORING ---')
    t7_trend = 2.0 if (h4_trend == 'DOWN' and d1_trend == 'DOWN') else (1.0 if (h4_trend == 'DOWN' or d1_trend == 'DOWN') else 0.0)
    t7_vwap = 1.5 if entry >= vwap_val else (0.5 if z_score > -0.5 else 0.0)
    
    signals_list = sig.get('signals', []) if sig else []
    t7_signal = 0.0
    for s in signals_list[:15]:
        st = s.get('type', '').lower()
        sd = s.get('dir', '').upper()
        sp = float(s.get('price') or 0)
        if ('abs' in st or 'div' in st or 'trap' in st or 'exh' in st) and sd in ['SELL', 'SHORT', 'BEAR']:
            if abs(sp - entry) / entry <= 0.02:
                t7_signal = 2.0
                break
            elif t7_signal == 0:
                t7_signal = 1.0
                
    min_wall = 1000000 # alts
    walls = bw.get('model', {}).get('confirmedWalls', []) if bw else []
    t7_wall = 0.0
    for w in walls:
        w_usd = float(w.get('usd') or 0)
        w_side = w.get('side', '').lower()
        wp = float(w.get('price') or 0)
        if w_usd >= min_wall and w_side == 'ask':
            if wp >= entry and (wp - entry) / entry <= 0.02:
                t7_wall = 1.5
                break
            elif t7_wall == 0:
                t7_wall = 0.5
                
    divs = cvd.get('divergences', []) if cvd else []
    t7_cvd = 1.0 if any('bear' in d.get('type', '').lower() or 'sell' in d.get('type', '').lower() for d in divs) else 0.0
    
    t7_magnet = 0.0
    if dom_2pct == "LB":
        if skew_2pct_ratio >= 2.5: t7_magnet = 1.5
        elif skew_2pct_ratio >= 1.5: t7_magnet = 1.0
        else: t7_magnet = 0.5
        
    t7_gex = 0.0 # alts
    t7_spread = 1.0 # Delta spreads on these alts < 0.05%
    
    t7_total = t7_trend + t7_vwap + t7_signal + t7_wall + t7_cvd + t7_magnet + t7_gex + t7_spread
    
    print(f'Table 7 Scoring Breakdown (11.5 max):')
    print(f'  Trend (2.0): {t7_trend}')
    print(f'  Regime (1.5): {t7_vwap}')
    print(f'  Signal (2.0): {t7_signal}')
    print(f'  Wall (1.5): {t7_wall}')
    print(f'  CVD (1.0): {t7_cvd}')
    print(f'  Magnet (1.5): {t7_magnet}')
    print(f'  GEX (1.0): {t7_gex}')
    print(f'  Spread (1.0): {t7_spread}')
    print(f'TOTAL AUDITED SCORE: {t7_total:.2f} / 11.5 pts')
    
    if 'claimed_t7' in ord_info:
        diff = abs(t7_total - ord_info['claimed_t7'])
        print(f'Claimed Score: {ord_info["claimed_t7"]:.2f} | Diff: {diff:.2f} | Within 0.5: {diff <= 0.5}')
        
    if tp:
        risk = abs(entry - sl)
        reward = abs(entry - tp)
        r_mult = reward / risk if risk > 0 else 0
        print(f'R-Multiple: {r_mult:.2f}R (Risk: {risk:.4f}, Reward: {reward:.4f})')
        
    results[sym] = {
        'last_price': last_price,
        'entry': entry,
        'sl': sl,
        'tp': tp,
        'tick_compliant': tick_compliant,
        'gate1_pass': gate1_pass,
        'gate2_pass': gate2_pass,
        'vector_b_usd': vector_b_usd,
        'vector_a_usd': vector_a_usd,
        'lsr_ratio': skew_2pct_ratio,
        'lsr_dom': dom_2pct,
        't7_total': t7_total
    }

print('\n==================== AUDIT COMPLETED ====================')
