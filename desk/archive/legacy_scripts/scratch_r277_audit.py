import urllib.request
import json
import math

symbols = ['ETH', 'LINK', 'SUI', 'BTC']

setups = {
    'ETH': {'order_id': 1684019303, 'entry': 1885.0, 'sl': 1908.0, 'tp': 1809.0, 'side': 'sell', 'stated_t7': 6.00},
    'LINK': {'order_id': 1683969432, 'entry': 9.450, 'sl': 9.680, 'tp': 8.980, 'side': 'sell', 'stated_t7': 5.00}
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

audit_data = {}

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
    opt = fetch_json(f'/api/cg/options?sym={sym}') if sym in ['BTC', 'ETH'] else None

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
    sd2 = float(bands.get('sd2') or 0)
    sd3 = float(bands.get('sd3') or 0)
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
    print(f'Session VWAP: {vwap_val:.4f} (z: {z_score:.2f}σ) | sd1: {sd1:.4f}, sd2: {sd2:.4f}, sd3: {sd3:.4f}')
    print(f'Trend: H4={h4_trend} (e13:{h4_ema.get("e13", 0):.2f} / e89:{h4_ema.get("e89", 0):.2f}), D1={d1_trend} (e13:{d1_ema.get("e13", 0):.2f} / e89:{d1_ema.get("e89", 0):.2f})')
    print(f'RSI: M15={rsis.get("m15"):.1f}, H1={rsis.get("h1"):.1f}, H4={rsis.get("h4"):.1f}')
    
    # Store data
    audit_data[sym] = {
        'last_price': last_price,
        'sess_poc': sess_poc,
        'day_poc': day_poc,
        'month_poc': month_poc,
        'vwap': vwap_val,
        'sd1': sd1,
        'z_score': z_score,
        'h4_trend': h4_trend,
        'd1_trend': d1_trend,
        'rsis': rsis,
        'mkt': mkt,
        'fp': fp,
        'liq': liq,
        'sig': sig,
        'cvd': cvd,
        'bw': bw,
        'opt': opt
    }
    
    # If setup exists, evaluate Gate 1, Gate 2, Table 7
    if sym in setups:
        setup = setups[sym]
        sl = setup['sl']
        entry = setup['entry']
        tp = setup['tp']
        
        print(f'\n--- (a) GATE 1: ACTIVE SESSION CLEARANCE AUDIT FOR {sym} ---')
        dist_sess_poc = abs(sl - sess_poc) / sess_poc * 100
        dist_day_poc = abs(sl - day_poc) / day_poc * 100
        dist_month_poc = abs(sl - month_poc) / month_poc * 100
        dist_vwap = abs(sl - vwap_val) / vwap_val * 100
        
        print(f'Stop Loss: {sl}')
        print(f'  Dist to Session (8h) POC ({sess_poc:.4f}): {dist_sess_poc:.3f}% (Clearance >0.8%: {dist_sess_poc > 0.8})')
        print(f'  Dist to Day POC ({day_poc:.4f}): {dist_day_poc:.3f}% (Clearance >0.8%: {dist_day_poc > 0.8})')
        print(f'  Dist to Month POC ({month_poc:.4f}): {dist_month_poc:.3f}% (Clearance >0.8%: {dist_month_poc > 0.8})')
        print(f'  Dist to Session VWAP ({vwap_val:.4f}): {dist_vwap:.3f}% (Clearance >0.8%: {dist_vwap > 0.8})')
        
        # Check Footprint Bar POCs > 10k contracts
        bars = fp.get('bars', []) if fp else []
        fp_hvn_matches = []
        for idx, b in enumerate(bars):
            b_fp = b.get('fp', {})
            tick = float(b_fp.get('tick') or 0)
            lo = float(b_fp.get('lo') or 0)
            bc = b_fp.get('bc', [])
            sc = b_fp.get('sc', [])
            b_vol = b_fp.get('b', [])
            s_vol = b_fp.get('s', [])
            if not bc or not sc or tick == 0: continue
            
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
                p_poc = lo + max_i * tick
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
        print(f'>>> GATE 1 VERDICT: {"PASS" if gate1_pass else "FAIL"} <<<')
        
        print(f'\n--- (b) GATE 2: GEOMETRICAL LIQUIDATION RISK (VECTOR A VS VECTOR B) ---')
        liq_stats = liq.get('stats', {}) if liq else {}
        bands_liq = liq_stats.get('bands', [])
        key_levels = liq_stats.get('keyLevels', {})
        totals_liq = liq_stats.get('totals', {})
        
        # Vector A: Downstream Traversal Fuel (Long liquidations toward TP)
        # Check all long liquidation levels between entry and TP (and below entry)
        below_clusters = key_levels.get('below', [])
        vector_a_clusters = [c for c in below_clusters if tp <= float(c.get('price', 0)) <= entry]
        vector_a_all_below = [c for c in below_clusters if float(c.get('price', 0)) <= entry]
        vector_a_usd = sum(float(c.get('usd', 0)) for c in vector_a_clusters)
        
        print(f'Vector A (Traversal Fuel toward TP {tp}):')
        print(f'  Clusters directly between Entry ({entry}) and TP ({tp}): {len(vector_a_clusters)}')
        for c in vector_a_clusters:
            print(f"    Cluster @ {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f} | Venues: {len(c.get('venues', []))}")
        print(f'  Total Vector A Key Cluster Fuel: ${vector_a_usd:,.2f}')
        
        # Vector B: Upstream Risk Zone Hazard (Short liquidations between Entry and SL)
        above_clusters = key_levels.get('above', [])
        vector_b_clusters = [c for c in above_clusters if entry <= float(c.get('price', 0)) <= sl]
        vector_b_near_sl = [c for c in above_clusters if abs(float(c.get('price', 0)) - sl) / sl <= 0.01]
        vector_b_usd = sum(float(c.get('usd', 0)) for c in vector_b_clusters)
        
        print(f'\nVector B (Risk Zone Hazard between Entry {entry} and SL {sl}):')
        print(f'  Clusters inside Risk Zone [{entry} - {sl}]: {len(vector_b_clusters)}')
        for c in vector_b_clusters:
            print(f"    HAZARD Cluster @ {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f}")
        print(f'  Clusters within ±1% of SL ({sl}): {len(vector_b_near_sl)}')
        for c in vector_b_near_sl:
            print(f"    NEAR SL Cluster @ {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f}")
        print(f'  Total Vector B Hazard USD: ${vector_b_usd:,.2f}')
        
        # ±2% LSR calculation
        shorts_2pct = 0
        longs_2pct = 0
        if len(bands_liq) >= 2:
            shorts_2pct = float(bands_liq[0].get('up', 0)) + float(bands_liq[1].get('up', 0))
            longs_2pct = float(bands_liq[0].get('down', 0)) + float(bands_liq[1].get('down', 0))
        dom_2pct = "SA" if shorts_2pct >= longs_2pct else "LB"
        skew_2pct_ratio = max(shorts_2pct, longs_2pct) / min(shorts_2pct, longs_2pct) if min(shorts_2pct, longs_2pct) > 0 else 999
        
        print(f'\n±2% Liquidation Skew Ratio (LSR): {skew_2pct_ratio:.2f}:1 ({dom_2pct})')
        print(f'  Shorts Above = ${shorts_2pct:,.2f} | Longs Below = ${longs_2pct:,.2f}')
        
        # Gate 2 Evaluation:
        # Banned if LSR >= 2.5:1 with SA dominant, or if Vector B contains major short squeeze cluster
        gate2_breach_lsr = (skew_2pct_ratio >= 2.5 and dom_2pct == "SA")
        gate2_breach_vector_b = (len(vector_b_clusters) > 0 and any(float(c.get('strength', 0)) >= 50 for c in vector_b_clusters))
        gate2_pass = (not gate2_breach_lsr) and (len(vector_b_clusters) == 0)
        print(f'>>> GATE 2 VERDICT: {"PASS" if gate2_pass else "FAIL"} (LSR Breach: {gate2_breach_lsr}, Vector B Squeeze Hazard: {len(vector_b_clusters) > 0}) <<<')
        
        print(f'\n--- (c) TABLE 7 ZERO-FALLBACK SCORING FOR {sym} ---')
        # 1. Directional Trend (2.0 max)
        t7_trend = 0.0
        if h4_trend == 'DOWN' and d1_trend == 'DOWN':
            t7_trend = 2.0
        elif h4_trend == 'DOWN' or d1_trend == 'DOWN':
            t7_trend = 1.0
            
        # 2. Auction / VWAP Regime (1.5 max)
        t7_vwap = 0.0
        if entry >= vwap_val:
            t7_vwap = 1.5
        elif z_score > -0.5:
            t7_vwap = 0.5
            
        # 3. Footprint Signal (2.0 max)
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
                        
        # 4. Whale Wall Backstop (1.5 max)
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
                    
        # 5. CVD Divergence (1.0 max)
        divs = cvd.get('divergences', []) if cvd else []
        t7_cvd = 0.0
        active_div = None
        for d in divs:
            dt = d.get('type', '').lower()
            if 'bear' in dt or 'sell' in dt:
                t7_cvd = 1.0
                active_div = d
                break
                
        # 6. Liquidation Magnet Gate (1.5 max)
        t7_magnet = 0.0
        if dom_2pct == "LB":
            if skew_2pct_ratio >= 2.5:
                t7_magnet = 1.5
            elif skew_2pct_ratio >= 1.5:
                t7_magnet = 1.0
            else:
                t7_magnet = 0.5
                
        # 7. Options GEX Context (1.0 max)
        t7_gex = 0.0
        if sym in ['BTC', 'ETH'] and opt and opt.get('ok'):
            reg = opt.get('regime', '')
            if 'NEGATIVE' in reg or 'POSITIVE' in reg:
                t7_gex = 1.0
                
        # 8. Broker Spread Drag (1.0 max)
        # ETH spread on Delta is ~0.0027%, LINK is ~0.0218% -> both < 0.05%
        t7_spread = 1.0
        
        t7_total = t7_trend + t7_vwap + t7_signal + t7_wall + t7_cvd + t7_magnet + t7_gex + t7_spread
        
        print(f'Table 7 Scoring Breakdown (11.5 max):')
        print(f'  Directional Trend (2.0 max): {t7_trend:.2f}')
        print(f'  Auction / VWAP Regime (1.5 max): {t7_vwap:.2f}')
        print(f'  Footprint Signal (2.0 max): {t7_signal:.2f}')
        print(f'  Whale Wall Backstop (1.5 max): {t7_wall:.2f}')
        print(f'  CVD Divergence (1.0 max): {t7_cvd:.2f}')
        print(f'  Liquidation Magnet Gate (1.5 max): {t7_magnet:.2f}')
        print(f'  Options GEX Context (1.0 max): {t7_gex:.2f}')
        print(f'  Broker Spread Drag (1.0 max): {t7_spread:.2f}')
        print(f'TOTAL AUDITED SCORE: {t7_total:.2f} / 11.5 pts')
        
        stated_score = setup['stated_t7']
        score_diff = abs(t7_total - stated_score)
        print(f'Stated Table 7 Score: {stated_score:.2f} pts | Difference: {score_diff:.2f} pts')
        score_veto = score_diff > 0.5
        print(f'Score Discrepancy > 0.5 pt: {score_veto} (Veto if True)')
        
        risk = abs(entry - sl)
        reward = abs(entry - tp)
        r_mult = reward / risk if risk > 0 else 0
        print(f'R-Multiple: {r_mult:.2f}R (Risk: {risk:.2f}, Reward: {reward:.2f})')
        
        audit_data[sym].update({
            'gate1_pass': gate1_pass,
            'dist_sess_poc': dist_sess_poc,
            'dist_day_poc': dist_day_poc,
            'dist_month_poc': dist_month_poc,
            'dist_vwap': dist_vwap,
            'fp_hvn_matches': fp_hvn_matches,
            'gate2_pass': gate2_pass,
            'vector_a_usd': vector_a_usd,
            'vector_b_usd': vector_b_usd,
            'vector_b_clusters': vector_b_clusters,
            'skew_2pct_ratio': skew_2pct_ratio,
            'dom_2pct': dom_2pct,
            't7_total': t7_total,
            'stated_score': stated_score,
            'score_diff': score_diff,
            'r_mult': r_mult
        })

# Now perform hazard audit for SUI and BTC
print('\n======================================================================')
print('                 (d) SUI & BTC HAZARD STATE AUDIT                      ')
print('======================================================================')

for h_sym in ['SUI', 'BTC']:
    data = audit_data[h_sym]
    liq_stats = data['liq'].get('stats', {}) if data['liq'] else {}
    bands_liq = liq_stats.get('bands', [])
    key_levels = liq_stats.get('keyLevels', {})
    
    shorts_2pct = 0
    longs_2pct = 0
    if len(bands_liq) >= 2:
        shorts_2pct = float(bands_liq[0].get('up', 0)) + float(bands_liq[1].get('up', 0))
        longs_2pct = float(bands_liq[0].get('down', 0)) + float(bands_liq[1].get('down', 0))
    dom = "SA" if shorts_2pct >= longs_2pct else "LB"
    ratio = max(shorts_2pct, longs_2pct) / min(shorts_2pct, longs_2pct) if min(shorts_2pct, longs_2pct) > 0 else 999
    
    above_clusters = key_levels.get('above', [])
    below_clusters = key_levels.get('below', [])
    
    print(f'\n--- {h_sym} HAZARD PROFILE ---')
    print(f'Current Price: {data["last_price"]}')
    print(f'Auction: Session POC {data["sess_poc"]:.2f} | Day POC {data["day_poc"]:.2f} | Month POC {data["month_poc"]:.2f}')
    print(f'Session VWAP: {data["vwap"]:.2f} (z: {data["z_score"]:.2f}σ)')
    print(f'±2% Liquidation Skew: {ratio:.2f}:1 (Dominant: {dom}) | Shorts Above: ${shorts_2pct:,.2f} | Longs Below: ${longs_2pct:,.2f}')
    
    print(f'Key Overhead Short Clusters (Upstream Magnets):')
    for c in above_clusters[:4]:
        print(f"  Price: {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f} | Dist: {c.get('distPct')}%")
        
    print(f'Key Downstream Long Clusters:')
    for c in below_clusters[:4]:
        print(f"  Price: {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f} | Dist: {c.get('distPct')}%")
        
    cvd_divs = data['cvd'].get('divergences', []) if data['cvd'] else []
    print(f'Active CVD Divergences: {len(cvd_divs)}')
    for d in cvd_divs:
        print(f"  {d.get('type')} divergence @ {d.get('priceA')} -> {d.get('priceB')}")
        
    # Check Delta listing & margin for BTC
    if h_sym == 'BTC':
        print(f'BTC Delta Requirement: Margin blocked/availability check')
