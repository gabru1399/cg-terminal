import urllib.request
import json
import math

symbols = ['ETH', 'LINK', 'SUI', 'BTC']

setups = {
    'ETH': {'entry': 1885.0, 'sl': 1908.0, 'tp': 1809.0, 'side': 'sell'},
    'LINK': {'entry': 9.450, 'sl': 9.680, 'tp': 8.980, 'side': 'sell'},
    'SUI': {'entry': 0.7560, 'sl': 0.7780, 'tp': 0.7120, 'side': 'sell'},
    'BTC': {'entry': 66500.0, 'sl': 67650.0, 'tp': 64200.0, 'side': 'sell'}
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
    print(f'=================== AUDITING {sym} ===================')
    mkt = fetch_json(f'/api/cg/market?sym={sym}')
    fp = fetch_json(f'/api/cg/fp?sym={sym}')
    liq = fetch_json(f'/api/cg/liqlevels?sym={sym}')
    sig = fetch_json(f'/api/cg/signals?sym={sym}')
    cvd = fetch_json(f'/api/cg/cvd?sym={sym}')
    bw = fetch_json(f'/api/cg/bookwalls?sym={sym}')
    opt = fetch_json(f'/api/cg/options?sym={sym}') if sym in ['ETH', 'BTC'] else None
    
    setup = setups[sym]
    sl = setup['sl']
    entry = setup['entry']
    tp = setup['tp']
    
    # 1. Market Telemetry
    price_info = mkt.get('price', {}) if mkt else {}
    last_price = float(price_info.get('last') or 0)
    auction = mkt.get('auction', {}) if mkt else {}
    day_auc = auction.get('day', {})
    day_poc = float(day_auc.get('poc') or 0)
    day_vah = float(day_auc.get('vah') or 0)
    day_val = float(day_auc.get('val') or 0)
    
    sess_auc = auction.get('session', {})
    sess_poc = float(sess_auc.get('poc') or 0)
    
    vwap_info = mkt.get('vwap', {}) if mkt else {}
    vwap_val = float(vwap_info.get('vwap') or 0)
    bands = vwap_info.get('bands', {})
    sd1 = float(bands.get('sd1') or 0)
    sd2 = float(bands.get('sd2') or 0)
    sd3 = float(bands.get('sd3') or 0)
    z_score = (last_price - vwap_val) / sd1 if sd1 > 0 else 0
    
    emas = mkt.get('ema', {}) if mkt else {}
    h4_ema = emas.get('h4', {})
    d1_ema = emas.get('d1', {})
    h4_trend = 'DOWN' if h4_ema.get('e13', 0) < h4_ema.get('e89', 0) else 'UP'
    d1_trend = 'DOWN' if d1_ema.get('e13', 0) < d1_ema.get('e89', 0) else 'UP'
    
    rsis = mkt.get('rsi', {}) if mkt else {}
    
    print(f'Price: {last_price} | Day POC: {day_poc} | Day VAH: {day_vah} | Day VAL: {day_val}')
    print(f'Session VWAP: {vwap_val:.4f} (z: {z_score:.2f}σ) | sd1: {sd1:.4f}, sd2: {sd2:.4f}, sd3: {sd3:.4f}')
    print(f'Trend: H4={h4_trend} (13:{h4_ema.get("e13", 0):.2f} / 89:{h4_ema.get("e89", 0):.2f}), D1={d1_trend} (13:{d1_ema.get("e13", 0):.2f} / 89:{d1_ema.get("e89", 0):.2f})')
    print(f'RSI: M15={rsis.get("m15"):.1f}, H1={rsis.get("h1"):.1f}, H4={rsis.get("h4"):.1f}')
    
    # 2. Gate 1: Footprint HVN Clearance
    # Check if SL is within ±0.8% of:
    # a) primary Footprint Bar POC (>10k contracts)
    # b) Day POC
    # c) Session VWAP
    
    bars = fp.get('bars', []) if fp else []
    hvn_matches = []
    all_bar_pocs = []
    
    for idx, b in enumerate(bars):
        b_fp = b.get('fp', {})
        tick = float(b_fp.get('tick') or 0)
        lo = float(b_fp.get('lo') or 0)
        bc = b_fp.get('bc', [])
        sc = b_fp.get('sc', [])
        b_vol = b_fp.get('b', [])
        s_vol = b_fp.get('s', [])
        
        if not bc or not sc or tick == 0:
            continue
            
        n_bins = min(len(bc), len(sc))
        max_contracts = -1
        max_idx = -1
        max_vol = -1
        
        for i in range(n_bins):
            c_tot = bc[i] + sc[i]
            v_tot = (b_vol[i] if i < len(b_vol) else 0) + (s_vol[i] if i < len(s_vol) else 0)
            if c_tot > max_contracts:
                max_contracts = c_tot
                max_idx = i
                max_vol = v_tot
                
        if max_idx >= 0:
            poc_p = lo + max_idx * tick
            all_bar_pocs.append({
                'bar_idx': idx,
                'ts': b.get('ts'),
                'poc_price': poc_p,
                'contracts': max_contracts,
                'volume': max_vol
            })
            
            # Check >10k contracts
            if max_contracts > 10000:
                dist_pct = abs(sl - poc_p) / poc_p * 100
                if dist_pct <= 0.8:
                    hvn_matches.append({
                        'type': 'BAR_POC_GT_10K',
                        'price': poc_p,
                        'contracts': max_contracts,
                        'volume': max_vol,
                        'dist_pct': dist_pct,
                        'ts': b.get('ts')
                    })
    
    # Check Day POC clearance
    dist_day_poc_pct = abs(sl - day_poc) / day_poc * 100 if day_poc > 0 else 999
    day_poc_violation = dist_day_poc_pct <= 0.8
    
    # Check Session VWAP clearance
    dist_vwap_pct = abs(sl - vwap_val) / vwap_val * 100 if vwap_val > 0 else 999
    vwap_violation = dist_vwap_pct <= 0.8
    
    print('\n--- GATE 1: FOOTPRINT HVN CLEARANCE AUDIT ---')
    print(f'SL: {sl}')
    print(f'Day POC: {day_poc} -> Distance to SL: {dist_day_poc_pct:.3f}% (Violation <= 0.8%: {day_poc_violation})')
    print(f'Session VWAP: {vwap_val:.4f} -> Distance to SL: {dist_vwap_pct:.3f}% (Violation <= 0.8%: {vwap_violation})')
    print(f'Total bars analyzed: {len(bars)} | Bars with POC > 10k contracts: {len([p for p in all_bar_pocs if p["contracts"] > 10000])}')
    
    top_pocs = sorted(all_bar_pocs, key=lambda x: x['contracts'], reverse=True)[:5]
    print('Top 5 Footprint Bar POCs by contracts:')
    for p in top_pocs:
        d = abs(sl - p['poc_price']) / p['poc_price'] * 100
        print(f"  POC {p['poc_price']} | Contracts: {p['contracts']} | Vol: {p['volume']:.1f} | Dist to SL: {d:.3f}%")
        
    print(f'Footprint Bar POCs (>10k contracts) within ±0.8% of SL: {len(hvn_matches)}')
    for m in hvn_matches:
        print(f"  MATCH: POC {m['price']} | Contracts: {m['contracts']} | Dist: {m['dist_pct']:.3f}%")
        
    gate1_pass = (not day_poc_violation) and (not vwap_violation) and (len(hvn_matches) == 0)
    print(f'GATE 1 VERDICT: {"PASS" if gate1_pass else "FAIL"}')
    
    # 3. Gate 2: Liquidation Skew Ratio (LSR) & Overhead Short Squeeze Magnet
    print('\n--- GATE 2: POST-SWEEP RELIEF MAGNET (LSR) AUDIT ---')
    liq_stats = liq.get('stats', {}) if liq else {}
    bands_liq = liq_stats.get('bands', [])
    key_levels = liq_stats.get('keyLevels', {})
    totals_liq = liq_stats.get('totals', {})
    
    # Calculate ±2.0% LSR
    # bands[0] is 0-1%, bands[1] is 1-2%
    shorts_2pct = 0
    longs_2pct = 0
    if len(bands_liq) >= 2:
        shorts_2pct = float(bands_liq[0].get('up', 0)) + float(bands_liq[1].get('up', 0))
        longs_2pct = float(bands_liq[0].get('down', 0)) + float(bands_liq[1].get('down', 0))
    
    lsr_2pct = shorts_2pct / longs_2pct if longs_2pct > 0 else (999 if shorts_2pct > 0 else 1.0)
    dom_2pct = "SA" if shorts_2pct >= longs_2pct else "LB"
    skew_2pct_ratio = max(shorts_2pct, longs_2pct) / min(shorts_2pct, longs_2pct) if min(shorts_2pct, longs_2pct) > 0 else 999
    
    # Overall totals in range (±4%)
    shorts_tot = float(totals_liq.get('shorts') or 0)
    longs_tot = float(totals_liq.get('longs') or 0)
    overall_lsr = shorts_tot / longs_tot if longs_tot > 0 else (999 if shorts_tot > 0 else 1.0)
    
    print(f'Liquidation ±2% window: Shorts Above = ${shorts_2pct:,.2f} | Longs Below = ${longs_2pct:,.2f}')
    print(f'LSR (±2%): {skew_2pct_ratio:.2f}:1 (Dominant: {dom_2pct}) | Shorts/Longs: {lsr_2pct:.2f}')
    print(f'Overall (±4%): Shorts = ${shorts_tot:,.2f} | Longs = ${longs_tot:,.2f} | Ratio = {overall_lsr:.2f}:1')
    
    # Check overhead short squeeze magnets at or above entry
    above_clusters = key_levels.get('above', [])
    overhead_magnets = []
    for c in above_clusters:
        cp = float(c.get('price') or 0)
        c_str = float(c.get('strength') or 0)
        c_usd = float(c.get('usd') or 0)
        overhead_magnets.append(c)
        print(f"  Overhead cluster: Price {cp} | Str: {c_str} | USD: ${c_usd:,.2f} | Dist from last: {c.get('distPct')}%")
        
    clusters_between_entry_sl = [c for c in above_clusters if entry <= float(c.get('price', 0)) <= sl]
    clusters_near_entry = [c for c in above_clusters if abs(float(c.get('price', 0)) - entry) / entry <= 0.01]
    
    print(f'Clusters between Entry ({entry}) and SL ({sl}): {len(clusters_between_entry_sl)}')
    for c in clusters_between_entry_sl:
        print(f"  BETWEEN ENTRY & SL: Price {c.get('price')} | Str: {c.get('strength')} | USD: ${c.get('usd')}")
    print(f'Clusters within ±1% of Entry ({entry}): {len(clusters_near_entry)}')
    for c in clusters_near_entry:
        print(f"  NEAR ENTRY: Price {c.get('price')} | Str: {c.get('strength')} | USD: ${c.get('usd')}")

    lsr_gate_breached = (skew_2pct_ratio >= 2.5 and dom_2pct == "SA")
    gate2_pass = not lsr_gate_breached and len(clusters_between_entry_sl) == 0
    print(f'GATE 2 VERDICT: {"PASS" if gate2_pass else "FAIL"} (LSR Breached: {lsr_gate_breached}, Squeeze Magnet in Risk Zone: {len(clusters_between_entry_sl) > 0})')

    # 4. Table 7 Scoring: Re-score from 0.0 to 8.0 pts (and canonical 11.5)
    print('\n--- TABLE 7 CONFLUENCE SCORING ---')
    t7_trend = 0.0
    if h4_trend == 'DOWN' and d1_trend == 'DOWN':
        t7_trend = 2.0
    elif h4_trend == 'DOWN' or d1_trend == 'DOWN':
        t7_trend = 1.0
        
    t7_vwap = 0.0
    if entry >= vwap_val:
        t7_vwap = 1.5
    elif z_score > -0.5:
        t7_vwap = 0.5
        
    signals_list = sig.get('signals', []) if sig else []
    t7_signal = 0.0
    qual_sig = None
    for s in signals_list[:15]:
        st = s.get('type', '').lower()
        sd = s.get('dir', '').upper()
        sp = float(s.get('price') or 0)
        if ('abs' in st or 'div' in st or 'trap' in st or 'exh' in st):
            if sd in ['SELL', 'SHORT', 'BEAR']:
                if abs(sp - entry) / entry <= 0.02:
                    t7_signal = 2.0
                    qual_sig = s
                    break
                elif t7_signal == 0:
                    t7_signal = 1.0
                    qual_sig = s
                    
    min_wall = 5000000 if sym in ['BTC', 'ETH'] else 1000000
    walls = bw.get('model', {}).get('confirmedWalls', []) if bw else []
    t7_wall = 0.0
    defending_wall = None
    for w in walls:
        w_usd = float(w.get('usd') or 0)
        w_side = w.get('side', '').lower()
        wp = float(w.get('price') or 0)
        if w_usd >= min_wall and w_side == 'ask':
            if wp >= entry and (wp - entry) / entry <= 0.02:
                t7_wall = 1.5
                defending_wall = w
                break
            elif t7_wall == 0:
                t7_wall = 0.5
                defending_wall = w
                
    divs = cvd.get('divergences', []) if cvd else []
    t7_cvd = 0.0
    active_div = None
    for d in divs:
        dt = d.get('type', '').lower()
        if 'bear' in dt or 'sell' in dt:
            t7_cvd = 1.0
            active_div = d
            break
            
    t7_magnet = 0.0
    if dom_2pct == "LB":
        if skew_2pct_ratio >= 2.5:
            t7_magnet = 1.5
        elif skew_2pct_ratio >= 1.5:
            t7_magnet = 1.0
        else:
            t7_magnet = 0.5
    else:
        t7_magnet = 0.0
        
    t7_gex = 0.0
    if sym in ['BTC', 'ETH'] and opt and opt.get('ok'):
        reg = opt.get('regime', '')
        if 'NEGATIVE' in reg or 'POSITIVE' in reg:
            t7_gex = 1.0
            
    t7_spread = 1.0
    
    t7_11_5 = t7_trend + t7_vwap + t7_signal + t7_wall + t7_cvd + t7_magnet + t7_gex + t7_spread
    
    f_trend = 1.0 if t7_trend >= 1.5 else (0.5 if t7_trend > 0 else 0.0)
    f_regime = 1.0 if t7_vwap >= 1.0 else (0.5 if t7_vwap > 0 else 0.0)
    f_signal = 1.0 if t7_signal >= 1.5 else (0.5 if t7_signal > 0 else 0.0)
    f_wall = 1.0 if t7_wall >= 1.0 else (0.5 if t7_wall > 0 else 0.0)
    f_cvd = 1.0 if t7_cvd >= 1.0 else 0.0
    f_magnet = 1.0 if t7_magnet >= 1.0 else (0.5 if t7_magnet > 0 else 0.0)
    f_gex = 1.0 if t7_gex >= 1.0 else 0.0
    f_spread = 1.0 if t7_spread >= 1.0 else 0.0
    score_8_0 = f_trend + f_regime + f_signal + f_wall + f_cvd + f_magnet + f_gex + f_spread
    
    print(f'Table 7 Factor Breakdown (Canonical 11.5 pts):')
    print(f'  Trend (2.0): {t7_trend} (H4={h4_trend}, D1={d1_trend})')
    print(f'  Regime (1.5): {t7_vwap} (Entry {entry} vs VWAP {vwap_val:.2f})')
    print(f'  Signal (2.0): {t7_signal} ({qual_sig})')
    print(f'  Wall (1.5): {t7_wall} ({defending_wall})')
    print(f'  CVD (1.0): {t7_cvd} ({active_div})')
    print(f'  Magnet (1.5): {t7_magnet} (Dom: {dom_2pct}, Ratio: {skew_2pct_ratio:.2f}:1)')
    print(f'  GEX (1.0): {t7_gex}')
    print(f'  Spread (1.0): {t7_spread}')
    print(f'TOTAL 11.5 Score: {t7_11_5:.2f} / 11.5')
    print(f'TOTAL 8.0 Normalized Score: {score_8_0:.2f} / 8.0')
    
    # 5. Risk-Reward Sanity Check & Failure Modes
    print('\n--- RISK-REWARD SANITY CHECK & FAILURE MODES ---')
    risk = abs(entry - sl)
    reward = abs(entry - tp)
    rr = reward / risk if risk > 0 else 0
    print(f'Risk: {risk:.4f} | Reward: {reward:.4f} | R-Multiple: {rr:.2f}R')
    
    fm_failures = []
    if rr < 1.5:
        fm_failures.append(f'R-multiple {rr:.2f}R < 1.5R floor')
    if not gate1_pass:
        fm_failures.append('Stop placed inside HVN / POC / VWAP noise (Gate 1 violation)')
    if not gate2_pass:
        fm_failures.append('Entry front-runs overhead short squeeze magnet / adverse LSR (Gate 2 violation)')
    if t7_11_5 < 5.0:
        fm_failures.append(f'Table 7 score {t7_11_5:.1f} < 5.0 (Confluence failure)')
        
    print(f'Failure Modes Flagged: {fm_failures}')
    
    overall_verdict = 'PASS' if (gate1_pass and gate2_pass and t7_11_5 >= 5.0 and len(fm_failures) == 0) else 'FAIL'
    print(f'>>> OVERALL AUDIT VERDICT FOR {sym}: {overall_verdict} <<<')
    
    results[sym] = {
        'last_price': last_price,
        'day_poc': day_poc,
        'vwap': vwap_val,
        'gate1_pass': gate1_pass,
        'day_poc_violation': day_poc_violation,
        'vwap_violation': vwap_violation,
        'hvn_matches': hvn_matches,
        'gate2_pass': gate2_pass,
        'lsr_2pct': skew_2pct_ratio,
        'dom_2pct': dom_2pct,
        'clusters_between_entry_sl': clusters_between_entry_sl,
        't7_11_5': t7_11_5,
        'score_8_0': score_8_0,
        'rr': rr,
        'fm_failures': fm_failures,
        'verdict': overall_verdict
    }

print('\n\n=================== AUDIT SUMMARY ===================')
for sym, r in results.items():
    print(f"{sym}: Verdict={r['verdict']} | Gate 1={r['gate1_pass']} | Gate 2={r['gate2_pass']} | T7_11.5={r['t7_11_5']} | Score_8={r['score_8_0']} | R={r['rr']:.2f}R | Failures={r['fm_failures']}")
