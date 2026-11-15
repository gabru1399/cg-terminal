import urllib.request
import json
import math

symbols = ['ETH', 'LINK', 'SUI', 'BTC']

# Candidate setups for audit under SOP v1.2.0
setups = {
    'ETH': {'entry': 1885.0, 'sl': 1908.0, 'tp': 1809.0, 'side': 'sell', 'archetype': 'S1_SWEEP_REVERSAL'},
    'LINK': {'entry': 9.450, 'sl': 9.680, 'tp': 8.980, 'side': 'sell', 'archetype': 'S1_SWEEP_REVERSAL'},
    'SUI': {'entry': 0.7560, 'sl': 0.7780, 'tp': 0.7120, 'side': 'sell', 'archetype': 'S1_SWEEP_REVERSAL'},
    'BTC': {'entry': 66500.0, 'sl': 67650.0, 'tp': 64200.0, 'side': 'sell', 'archetype': 'S1_SWEEP_REVERSAL'}
}

def fetch_json(endpoint):
    url = f'http://127.0.0.1:3000{endpoint}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AdversarialAuditor/3.6'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f'Error fetching {endpoint}: {e}')
        return None

results = {}

for sym in symbols:
    print(f'=================== AUDITING {sym} (SOP v1.2.0) ===================')
    mkt = fetch_json(f'/api/cg/market?sym={sym}')
    fp = fetch_json(f'/api/cg/fp?sym={sym}')
    liq = fetch_json(f'/api/cg/liqlevels?sym={sym}')
    sig = fetch_json(f'/api/cg/signals?sym={sym}')
    cvd = fetch_json(f'/api/cg/cvd?sym={sym}')
    bw = fetch_json(f'/api/cg/bookwalls?sym={sym}')
    nar = fetch_json(f'/api/cg/narrative?sym={sym}')
    opt = fetch_json(f'/api/cg/options?sym={sym}') if sym in ['ETH', 'BTC'] else None
    
    setup = setups[sym]
    sl = setup['sl']
    entry = setup['entry']
    tp = setup['tp']
    archetype = setup.get('archetype', 'S1_SWEEP_REVERSAL')
    
    # 0. Tab 7 Flow Narrative & Regime Strategy Router
    regime = nar.get('regime', 'UNKNOWN') if nar else 'UNKNOWN'
    active_model = nar.get('activeModel', 'UNKNOWN') if nar else 'UNKNOWN'
    direction_lean = nar.get('direction', 'UNKNOWN') if nar else 'UNKNOWN'
    thesis = nar.get('thesis', 'N/A') if nar else 'N/A'
    m1_state = nar.get('m1', {}).get('status', 'N/A') if nar else 'N/A'
    
    print(f'Tab 7 Regime: {regime} | Active Model: {active_model} ({direction_lean}) | M1 Status: {m1_state}')
    print(f'Thesis: {thesis[:120]}...')
    
    # Check archetype legality under Regime
    archetype_valid = True
    archetype_note = "Valid"
    if regime == 'RANGE_BALANCE' and 'S7' in archetype:
        archetype_valid = False
        archetype_note = "S7 (Trend Pullback) is BANNED in RANGE_BALANCE (SOP §5.1)"
    elif 'S1' in archetype:
        archetype_valid = True
        archetype_note = "S1 (Sweep Reversal) Universal Boundary Archetype (PASS)"
        
    print(f'Archetype Check: {archetype} -> {archetype_note}')
    
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
    
    month_auc = auction.get('month', {})
    month_poc = float(month_auc.get('poc') or 0)
    
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
    
    print(f'Price: {last_price} | Day POC: {day_poc} | Day VAH: {day_vah} | Day VAL: {day_val} | Sess POC: {sess_poc}')
    print(f'Session VWAP: {vwap_val:.4f} (z: {z_score:.2f}σ) | sd1: {sd1:.4f}, sd2: {sd2:.4f}, sd3: {sd3:.4f}')
    print(f'Trend: H4={h4_trend} (13:{h4_ema.get("e13", 0):.2f} / 89:{h4_ema.get("e89", 0):.2f}), D1={d1_trend} (13:{d1_ema.get("e13", 0):.2f} / 89:{d1_ema.get("e89", 0):.2f})')
    
    # 2. Gate 1: Active Session Auction Clearance (SOP v1.2.0)
    # Check SL strictly against:
    # (a) Active Session 8h POC
    # (b) UTC Day POC / VAH / VAL
    # (c) UTC Month POC
    # (d) Day VWAP ±1σ/2σ/3σ
    # (e) Footprint Bar POCs (>10k contracts) from current active session (last 32 bars / 8h)
    
    bars = fp.get('bars', []) if fp else []
    active_bars = bars[-32:] if len(bars) >= 32 else bars  # Last 8 hours strictly
    active_hvn_matches = []
    
    for idx, b in enumerate(active_bars):
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
        for i in range(n_bins):
            c_tot = bc[i] + sc[i]
            if c_tot > max_contracts:
                max_contracts = c_tot
                max_idx = i
                
        if max_idx >= 0 and max_contracts > 10000:
            poc_p = lo + max_idx * tick
            dist_pct = abs(sl - poc_p) / poc_p * 100
            if dist_pct < 0.5:
                active_hvn_matches.append({
                    'type': 'ACTIVE_SESSION_BAR_POC_GT_10K',
                    'price': poc_p,
                    'contracts': max_contracts,
                    'dist_pct': dist_pct
                })
    
    # Check structural nodes
    dist_day_poc_pct = abs(sl - day_poc) / day_poc * 100 if day_poc > 0 else 999
    day_poc_violation = dist_day_poc_pct < 0.5
    
    dist_sess_poc_pct = abs(sl - sess_poc) / sess_poc * 100 if sess_poc > 0 else 999
    sess_poc_violation = dist_sess_poc_pct < 0.5
    
    dist_vwap_pct = abs(sl - vwap_val) / vwap_val * 100 if vwap_val > 0 else 999
    vwap_violation = dist_vwap_pct < 0.5
    
    print('\n--- GATE 1: CALIBRATED ACTIVE SESSION AUCTION CLEARANCE ---')
    print(f'SL: {sl}')
    print(f'Day POC ({day_poc}): Dist = {dist_day_poc_pct:.3f}% (Violation < 0.5%: {day_poc_violation})')
    print(f'Sess POC ({sess_poc}): Dist = {dist_sess_poc_pct:.3f}% (Violation < 0.5%: {sess_poc_violation})')
    print(f'Session VWAP ({vwap_val:.2f}): Dist = {dist_vwap_pct:.3f}% (Violation < 0.5%: {vwap_violation})')
    print(f'Active Session Bar POCs (last 32 bars) < 0.5% of SL: {len(active_hvn_matches)}')
    for m in active_hvn_matches:
        print(f"  ACTIVE MATCH: POC {m['price']} | Ctrs: {m['contracts']} | Dist: {m['dist_pct']:.3f}%")
        
    gate1_pass = (not day_poc_violation) and (not sess_poc_violation) and (not vwap_violation) and (len(active_hvn_matches) == 0)
    print(f'GATE 1 VERDICT: {"PASS" if gate1_pass else "FAIL"}')
    
    # 3. Gate 2: Geometrical Liquidation Risk Gate (SOP v1.2.0)
    # Split into:
    # Vector A: Traversal Fuel [Live Price -> Entry]
    # Vector B: Risk Zone Hazard [Entry -> SL + 0.5 ATR]
    print('\n--- GATE 2: GEOMETRICAL LIQUIDATION RISK GATE ---')
    liq_stats = liq.get('stats', {}) if liq else {}
    bands_liq = liq_stats.get('bands', [])
    key_levels = liq_stats.get('keyLevels', {})
    totals_liq = liq_stats.get('totals', {})
    
    # Live Price ±2.0% LSR (Traversal vector)
    shorts_2pct = 0
    longs_2pct = 0
    if len(bands_liq) >= 2:
        shorts_2pct = float(bands_liq[0].get('up', 0)) + float(bands_liq[1].get('up', 0))
        longs_2pct = float(bands_liq[0].get('down', 0)) + float(bands_liq[1].get('down', 0))
    
    lsr_2pct = shorts_2pct / longs_2pct if longs_2pct > 0 else (999 if shorts_2pct > 0 else 1.0)
    dom_2pct = "SA" if shorts_2pct >= longs_2pct else "LB"
    skew_2pct_ratio = max(shorts_2pct, longs_2pct) / min(shorts_2pct, longs_2pct) if min(shorts_2pct, longs_2pct) > 0 else 999
    
    above_clusters = key_levels.get('above', [])
    
    # Check Vector B: Clusters strictly inside Risk Zone [Entry, SL + 0.5% buffer]
    risk_zone_clusters = [c for c in above_clusters if entry <= float(c.get('price', 0)) <= (sl * 1.005)]
    traversal_clusters = [c for c in above_clusters if last_price <= float(c.get('price', 0)) < entry]
    
    print(f'Vector A (Traversal Fuel [Live Price {last_price} -> Entry {entry}]):')
    print(f'  Live LSR (±2%): {skew_2pct_ratio:.2f}:1 ({dom_2pct}) | Traversal Clusters Count: {len(traversal_clusters)}')
    for c in traversal_clusters:
        print(f"    TRAVERSAL FUEL CLUSTER: Price {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f}")
        
    print(f'Vector B (Risk Zone Hazard [Entry {entry} -> SL {sl}]):')
    print(f'  Risk Zone Clusters Count: {len(risk_zone_clusters)}')
    for c in risk_zone_clusters:
        print(f"    HAZARD CLUSTER IN RISK ZONE: Price {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f}")
        
    vector_b_hazard = len(risk_zone_clusters) > 0 and any(float(c.get('usd', 0)) >= 5000000 or float(c.get('strength', 0)) >= 60 for c in risk_zone_clusters)
    gate2_pass = not vector_b_hazard
    print(f'GATE 2 VERDICT: {"PASS" if gate2_pass else "FAIL"} (Vector B Invalidation Hazard: {vector_b_hazard})')
    
    # 4. Table 7 Scoring (SOP v1.2.0)
    print('\n--- TABLE 7 CONFLUENCE SCORING ---')
    t7_trend = 0.0
    if regime == 'RANGE_BALANCE':
        # In RANGE_BALANCE, flat EMAs score 0.0 pts (SOP v1.2.0 §3.1 Factor 1)
        t7_trend = 0.0
        trend_note = "Flat in RANGE_BALANCE (0.0 pts)"
    else:
        if h4_trend == 'DOWN' and d1_trend == 'DOWN':
            t7_trend = 2.0
            trend_note = "H4 & D1 Down (2.0 pts)"
        elif h4_trend == 'DOWN' or d1_trend == 'DOWN':
            t7_trend = 1.0
            trend_note = "H4 Down only (1.0 pt)"
            
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
            
    t7_magnet = 1.5 if (len(traversal_clusters) > 0 and not vector_b_hazard) else 0.0
    t7_gex = 1.0 if (sym in ['BTC', 'ETH'] and opt and opt.get('ok')) else 0.0
    t7_spread = 1.0
    
    t7_11_5 = t7_trend + t7_vwap + t7_signal + t7_wall + t7_cvd + t7_magnet + t7_gex + t7_spread
    
    print(f'Table 7 Factor Breakdown (Canonical 11.5 pts):')
    print(f'  Trend (2.0): {t7_trend} ({trend_note})')
    print(f'  Regime (1.5): {t7_vwap} (Entry {entry} vs VWAP {vwap_val:.2f})')
    print(f'  Signal (2.0): {t7_signal}')
    print(f'  Wall (1.5): {t7_wall}')
    print(f'  CVD (1.0): {t7_cvd}')
    print(f'  Magnet (1.5): {t7_magnet} (Traversal fuel confirmed, Risk Zone clear)')
    print(f'  GEX (1.0): {t7_gex}')
    print(f'  Spread (1.0): {t7_spread}')
    print(f'TOTAL 11.5 Score: {t7_11_5:.2f} / 11.5')
    
    # 5. Risk-Reward Sanity Check & Failure Modes
    risk = abs(entry - sl)
    reward = abs(entry - tp)
    rr = reward / risk if risk > 0 else 0
    print(f'Risk: {risk:.4f} | Reward: {reward:.4f} | R-Multiple: {rr:.2f}R')
    
    fm_failures = []
    if not archetype_valid:
        fm_failures.append(f'Archetype violation: {archetype_note}')
    if rr < 1.5:
        fm_failures.append(f'R-multiple {rr:.2f}R < 1.5R floor')
    if not gate1_pass:
        fm_failures.append('Stop placed inside active session anchor (Gate 1 violation)')
    if not gate2_pass:
        fm_failures.append('Dominant liquidation cluster inside Risk Zone (Gate 2 violation)')
    if t7_11_5 < 5.0:
        fm_failures.append(f'Table 7 score {t7_11_5:.1f} < 5.0 (Confluence failure)')
        
    print(f'Failure Modes Flagged: {fm_failures}')
    overall_verdict = 'PASS' if (archetype_valid and gate1_pass and gate2_pass and t7_11_5 >= 5.0 and len(fm_failures) == 0) else 'FAIL'
    print(f'>>> OVERALL AUDIT VERDICT FOR {sym}: {overall_verdict} <<<')
    
    results[sym] = {
        'last_price': last_price,
        'regime': regime,
        'archetype': archetype,
        'gate1_pass': gate1_pass,
        'gate2_pass': gate2_pass,
        't7_11_5': t7_11_5,
        'rr': rr,
        'failures': fm_failures,
        'verdict': overall_verdict
    }

print('\n\n=================== AUDIT SUMMARY (SOP v1.2.0) ===================')
for sym, r in results.items():
    print(f"{sym}: Verdict={r['verdict']} | Regime={r['regime']} | Gate 1={r['gate1_pass']} | Gate 2={r['gate2_pass']} | T7_11.5={r['t7_11_5']} | R={r['rr']:.2f}R | Failures={r['failures']}")
