import urllib.request
import json
import math
import datetime

standing_orders = {
    'DOT': {
        'id': 1684506647,
        'sym': 'DOT',
        'entry': 0.7480,
        'sl': 0.7550,
        'tp': 0.7180,
        'min_wall': 200000
    },
    'LTC': {
        'id': 1684443284,
        'sym': 'LTC',
        'entry': 45.480,
        'sl': 45.880,
        'tp': 44.500,
        'min_wall': 500000
    },
    'ETH': {
        'id': 1684442347,
        'sym': 'ETH',
        'entry': 1838.50,
        'sl': 1858.50,
        'tp': 1792.50,
        'min_wall': 5000000
    },
    'SOL': {
        'id': 1684424777,
        'sym': 'SOL',
        'entry': 72.450,
        'sl': 73.150,
        'tp': 70.750,
        'min_wall': 1000000
    }
}

def fetch_json(endpoint):
    url = f'http://127.0.0.1:3000{endpoint}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AdversarialAuditor/3.8'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f'Error fetching {endpoint}: {e}')
        return None

results = {}

for sym, ord_info in standing_orders.items():
    print(f"\n=================== AUDITING {sym} (Order #{ord_info['id']}) ===================")
    entry = ord_info['entry']
    sl = ord_info['sl']
    tp = ord_info['tp']
    risk = sl - entry
    reward = entry - tp
    r_mult = reward / risk
    
    mkt = fetch_json(f'/api/cg/market?sym={sym}')
    fp = fetch_json(f'/api/cg/fp?sym={sym}')
    liq = fetch_json(f'/api/cg/liqlevels?sym={sym}')
    sig = fetch_json(f'/api/cg/signals?sym={sym}')
    cvd = fetch_json(f'/api/cg/cvd?sym={sym}')
    bw = fetch_json(f'/api/cg/bookwalls?sym={sym}')
    nar = fetch_json(f'/api/cg/narrative?sym={sym}')
    
    # Tab 7 Narrative
    regime = nar.get('regime', 'UNKNOWN') if nar else 'UNKNOWN'
    m1_status = nar.get('m1', {}).get('status', 'N/A') if nar else 'N/A'
    
    # Market & Auction
    p_info = mkt.get('price', {}) if mkt else {}
    last_p = float(p_info.get('last') or 0)
    
    auc = mkt.get('auction', {}) if mkt else {}
    sess_poc = float(auc.get('session', {}).get('poc') or 0)
    sess_vah = float(auc.get('session', {}).get('vah') or 0)
    sess_val = float(auc.get('session', {}).get('val') or 0)
    
    day_poc = float(auc.get('day', {}).get('poc') or 0)
    day_vah = float(auc.get('day', {}).get('vah') or 0)
    day_val = float(auc.get('day', {}).get('val') or 0)
    
    month_poc = float(auc.get('month', {}).get('poc') or 0)
    
    vwap_info = mkt.get('vwap', {}) if mkt else {}
    vwap_val = float(vwap_info.get('vwap') or 0)
    bands = vwap_info.get('bands', {})
    sd1 = float(bands.get('sd1') or 0)
    z_score = (last_p - vwap_val) / sd1 if sd1 > 0 else 0
    
    emas = mkt.get('ema', {}) if mkt else {}
    h4_ema = emas.get('h4', {})
    d1_ema = emas.get('d1', {})
    h4_trend = 'DOWN' if h4_ema.get('e13', 0) < h4_ema.get('e89', 0) else 'UP'
    d1_trend = 'DOWN' if d1_ema.get('e13', 0) < d1_ema.get('e89', 0) else 'UP'
    
    print(f"Price: {last_p} | Regime: {regime} | M1: {m1_status} | H4: {h4_trend} | D1: {d1_trend}")
    print(f"Sess POC: {sess_poc:.4f} | VAH: {sess_vah:.4f} | VAL: {sess_val:.4f}")
    print(f"Day POC: {day_poc:.4f} | VAH: {day_vah:.4f} | VAL: {day_val:.4f} | Month POC: {month_poc:.4f}")
    print(f"VWAP: {vwap_val:.4f} (z: {z_score:.2f}σ)")
    
    # Gate 1 Clearance
    dist_sess_poc = abs(sl - sess_poc) / sess_poc * 100
    dist_day_poc = abs(sl - day_poc) / day_poc * 100
    dist_month_poc = abs(sl - month_poc) / month_poc * 100
    dist_vwap = abs(sl - vwap_val) / vwap_val * 100
    dist_sess_vah = (sl - sess_vah) / sess_vah * 100
    dist_day_vah = (sl - day_vah) / day_vah * 100
    
    bars = fp.get('bars', []) if fp else []
    active_session_bars = bars[-32:] if len(bars) >= 32 else bars
    
    fp_hvn_matches_session = []
    for idx, b in enumerate(active_session_bars):
        b_fp = b.get('fp', {})
        tick_fp = float(b_fp.get('tick') or 0)
        lo = float(b_fp.get('lo') or 0)
        bc = b_fp.get('bc', [])
        sc = b_fp.get('sc', [])
        if not bc or not sc or tick_fp == 0: continue
        
        max_c = -1
        max_i = -1
        for i in range(min(len(bc), len(sc))):
            c_tot = bc[i] + sc[i]
            if c_tot > max_c:
                max_c = c_tot
                max_i = i
        if max_i >= 0 and max_c > 10000:
            p_poc = lo + max_i * tick_fp
            d_pct = abs(sl - p_poc) / p_poc * 100
            if d_pct <= 0.8:
                fp_hvn_matches_session.append({
                    'ts': b.get('ts'),
                    'price': p_poc,
                    'contracts': max_c,
                    'dist_pct': d_pct
                })
                
    print(f"\n--- GATE 1 CLEARANCE (SL={sl}) ---")
    print(f"  Sess POC ({sess_poc:.4f}) dist: {dist_sess_poc:.3f}% (Cleared >=0.5%: {dist_sess_poc >= 0.5})")
    print(f"  Day POC ({day_poc:.4f}) dist: {dist_day_poc:.3f}% (Cleared >=0.5%: {dist_day_poc >= 0.5})")
    print(f"  Month POC ({month_poc:.4f}) dist: {dist_month_poc:.3f}% (Cleared >=0.5%: {dist_month_poc >= 0.5})")
    print(f"  VWAP ({vwap_val:.4f}) dist: {dist_vwap:.3f}% (Cleared >=0.5%: {dist_vwap >= 0.5})")
    print(f"  SL position vs Sess VAH ({sess_vah:.4f}): {dist_sess_vah:+.3f}% (Above VAH: {sl >= sess_vah})")
    print(f"  SL position vs Day VAH ({day_vah:.4f}): {dist_day_vah:+.3f}% (Above VAH: {sl >= day_vah})")
    print(f"  Active Session (last 8h) Footprint HVNs (>10k contracts) within ±0.8%: {len(fp_hvn_matches_session)}")
    for m in fp_hvn_matches_session:
        print(f"    COLLISION: POC {m['price']:.4f} | {m['contracts']} contracts | Dist: {m['dist_pct']:.3f}%")
        
    gate1_pass = (dist_sess_poc >= 0.5) and (dist_day_poc >= 0.5) and (dist_month_poc >= 0.5) and (dist_vwap >= 0.5) and (sl >= min(sess_vah, day_vah)) and (len(fp_hvn_matches_session) == 0)
    print(f"  GATE 1 RESULT: {'PASS' if gate1_pass else 'FAIL'}")
    
    # Gate 2 Liquidation Geometry
    liq_stats = liq.get('stats', {}) if liq else {}
    bands_liq = liq_stats.get('bands', [])
    key_levels = liq_stats.get('keyLevels', {})
    
    below_clusters = key_levels.get('below', [])
    vector_a_clusters = [c for c in below_clusters if float(c.get('price', 0)) <= entry]
    vector_a_usd = sum(float(c.get('usd', 0)) for c in vector_a_clusters)
    
    above_clusters = key_levels.get('above', [])
    vector_b_clusters = [c for c in above_clusters if entry <= float(c.get('price', 0)) <= sl]
    vector_b_usd = sum(float(c.get('usd', 0)) for c in vector_b_clusters)
    
    shorts_2pct = 0
    longs_2pct = 0
    if len(bands_liq) >= 2:
        shorts_2pct = float(bands_liq[0].get('up', 0)) + float(bands_liq[1].get('up', 0))
        longs_2pct = float(bands_liq[0].get('down', 0)) + float(bands_liq[1].get('down', 0))
    dom_2pct = "SA" if shorts_2pct >= longs_2pct else "LB"
    skew_2pct_ratio = max(shorts_2pct, longs_2pct) / min(shorts_2pct, longs_2pct) if min(shorts_2pct, longs_2pct) > 0 else 999
    
    print(f"\n--- GATE 2 LIQUIDATION GEOMETRY ---")
    print(f"  Vector A Downside Fuel (below Entry {entry}): {len(vector_a_clusters)} clusters (${vector_a_usd:,.2f})")
    print(f"  Vector B Risk Zone Hazard [Entry {entry} to SL {sl}]: {len(vector_b_clusters)} clusters (${vector_b_usd:,.2f})")
    for c in vector_b_clusters:
        print(f"    HAZARD: Cluster @ {c.get('price')} | USD: ${float(c.get('usd', 0)):,.2f}")
    print(f"  ±2% LSR: {skew_2pct_ratio:.2f}:1 ({dom_2pct}) | Shorts Above: ${shorts_2pct:,.2f} | Longs Below: ${longs_2pct:,.2f}")
    
    lsr_breached = (skew_2pct_ratio >= 2.5 and dom_2pct == "SA")
    gate2_pass = (not lsr_breached) and (vector_b_usd == 0)
    print(f"  GATE 2 RESULT: {'PASS' if gate2_pass else 'FAIL'}")
    
    # Table 7 Confluence Scoring
    t7_trend = 2.0 if (h4_trend == 'DOWN' and d1_trend == 'DOWN') else (1.0 if (h4_trend == 'DOWN' or d1_trend == 'DOWN') else 0.0)
    t7_vwap = 1.5 if entry >= vwap_val else (0.5 if z_score > -0.5 else 0.0)
    
    all_sigs = []
    for s_set in (sig.get('sets', []) if sig else []):
        for s in s_set.get('sigs', []):
            all_sigs.append(s)
            
    t7_signal = 0.0
    for s in all_sigs:
        st = s.get('t', '').lower()
        sd = s.get('side', '').lower()
        sp = float(s.get('p') or 0)
        if st in ['abs', 'div', 'sdiv', 'trap', 'exh'] and sd in ['sell', 'short', 'bear']:
            if abs(sp - entry) / entry <= 0.02:
                t7_signal = 2.0
                break
            elif t7_signal == 0:
                t7_signal = 1.0
                
    walls = bw.get('model', {}).get('walls', []) if bw else []
    t7_wall = 0.0
    wall_matches = []
    for w in walls:
        w_usd = float(w.get('usd') or 0)
        w_side = w.get('side', '').lower()
        wp = float(w.get('price') or 0)
        if w_usd >= ord_info['min_wall'] and w_side == 'a':
            wall_matches.append(w)
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
        
    t7_gex = 1.0 if sym in ['ETH', 'BTC'] else 0.0
    t7_spread = 1.0
    
    t7_total = t7_trend + t7_vwap + t7_signal + t7_wall + t7_cvd + t7_magnet + t7_gex + t7_spread
    
    # Normalized 8.0 score
    f_trend = 1.0 if t7_trend >= 1.5 else (0.5 if t7_trend > 0 else 0.0)
    f_regime = 1.0 if t7_vwap >= 1.0 else (0.5 if t7_vwap > 0 else 0.0)
    f_signal = 1.0 if t7_signal >= 1.5 else (0.5 if t7_signal > 0 else 0.0)
    f_wall = 1.0 if t7_wall >= 1.0 else (0.5 if t7_wall > 0 else 0.0)
    f_cvd = 1.0 if t7_cvd >= 1.0 else 0.0
    f_magnet = 1.0 if t7_magnet >= 1.0 else (0.5 if t7_magnet > 0 else 0.0)
    f_gex = 1.0 if t7_gex >= 1.0 else 0.0
    f_spread = 1.0 if t7_spread >= 1.0 else 0.0
    score_8_0 = f_trend + f_regime + f_signal + f_wall + f_cvd + f_magnet + f_gex + f_spread
    
    print(f"\n--- TABLE 7 CONFLUENCE SCORING ---")
    print(f"  Canonical Score: {t7_total:.2f} / 11.5 pts")
    print(f"  Normalized Score: {score_8_0:.2f} / 8.0 pts")
    print(f"  Risk: {risk:.4f} | Reward: {reward:.4f} | R: {r_mult:.2f}R")
    
    overall_pass = gate1_pass and gate2_pass and (t7_total >= 5.0) and (r_mult >= 1.5)
    print(f"\n>>> ORDER #{ord_info['id']} ({sym}) VERDICT: {'PASS' if overall_pass else 'VETO'} <<<")
    
    results[sym] = {
        'id': ord_info['id'],
        'gate1_pass': gate1_pass,
        'gate2_pass': gate2_pass,
        't7_total': t7_total,
        'score_8_0': score_8_0,
        'r_mult': r_mult,
        'overall_pass': overall_pass
    }
