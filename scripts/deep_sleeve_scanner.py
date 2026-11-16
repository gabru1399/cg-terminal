import json
import urllib.request
import time

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception:
        return None

def scan_sleeves():
    candidates = [
        'XRP', 'DOT', 'SUI', 'FIL', 'ETC', 'APT', 'TIA', 'ADA', 'XLM', 'ARB', 'SEI', 'OP', 'HBAR',
        'CRCL', 'COIN', 'SPCX', 'NVDA', 'MSFT', 'XAU'
    ]
    
    print("=" * 115)
    print("DEEP SLEEVE SCANNER (SLEEVE R: RANGE ROTATION | SLEEVE S: LIQUIDITY SWEEP | SLEEVE T: TREND)")
    print("=" * 115)
    print(f"{'SYM':<6} | {'PRICE':<10} | {'REGIME':<12} | {'VWAP z':<8} | {'DAY POC':<10} | {'VAL / VAH':<18} | {'ABS/EXH':<10} | {'BUY%':<6} | {'SLV R':<6} | {'STATUS'}")
    print("-" * 115)
    
    results = []
    
    for sym in candidates:
        mkt = fetch_json(f"http://127.0.0.1:3000/api/cg/market?sym={sym}")
        sigs = fetch_json(f"http://127.0.0.1:3000/api/cg/signals?sym={sym}")
        cvd = fetch_json(f"http://127.0.0.1:3000/api/cg/cvd?sym={sym}")
        
        if not mkt:
            continue
            
        px_val = mkt.get('price')
        if isinstance(px_val, dict):
            px = float(px_val.get('last') or px_val.get('price') or 0.0)
        elif px_val is not None:
            px = float(px_val)
        else:
            px = float(mkt.get('data', {}).get('price', 0.0))
            
        if px <= 0:
            continue
            
        vwap = mkt.get('vwap', {})
        vwap_mid = float(vwap.get('vwap', px))
        dev = float(vwap.get('stdDev', 1.0))
        z = (px - vwap_mid) / dev if dev and dev > 0 else 0.0
        
        auc = mkt.get('auction', {})
        day_auc = auc.get('day', {})
        val = float(day_auc.get('val', 0.0))
        poc = float(day_auc.get('poc', 0.0))
        vah = float(day_auc.get('vah', 0.0))
        
        # Signals
        sig_items = sigs.get('signals', []) if sigs else []
        now_ms = time.time() * 1000
        recent_sigs = [s for s in sig_items if (now_ms - s.get('time', 0)) < 8 * 3600 * 1000]
        abs_sigs = [s for s in recent_sigs if s.get('type') in ['abs', 'sdiv', 'exh', 'trap', 'div']]
        
        # CVD
        cvd_data = cvd.get('data', {}) if cvd else {}
        buy_ratio = float(cvd_data.get('takerBuyRatio', 50.0)) if isinstance(cvd_data, dict) else 50.0
        
        # Sleeve R score calculation:
        # R1: Value Area Extreme rejection (+2.0)
        # R2: VWAP stretch |z| >= 1.5 (+1.5)
        # R3: Footprint absorption / discrete signal (+2.0)
        # R4: Book wall defense (+1.5) -> assume 1.0 baseline
        # R5: Auction gravity (POC distance >= 1.0R) (+1.0)
        # R6: CVD non-confirmation (+1.0)
        # R7: Friction (+1.0)
        r_score = 0.0
        setup_type = "NONE"
        
        # R2: VWAP stretch
        if abs(z) >= 1.5:
            r_score += 1.5
        elif abs(z) >= 1.0:
            r_score += 1.0
            
        # R1: Extreme Rejection
        if val > 0 and vah > 0:
            if px <= val * 1.005:  # Value Area Low test
                r_score += 2.0
                setup_type = "LONG_VAL_BOUNCE"
            elif px >= vah * 0.995: # Value Area High test
                r_score += 2.0
                setup_type = "SHORT_VAH_FADE"
                
        # R3: Signals
        if abs_sigs:
            r_score += 1.5
            
        # R5: POC distance
        if poc > 0:
            dist_to_poc = abs(px - poc) / px * 100
            if dist_to_poc >= 0.5:
                r_score += 1.0
                
        # R6: CVD non-confirm
        if z < -0.8 and buy_ratio >= 48.5:
            r_score += 1.0
        elif z > 0.8 and buy_ratio <= 51.5:
            r_score += 1.0
            
        r_score += 1.0  # Friction pass
        
        status = f"QUALIFIED ({setup_type})" if r_score >= 5.0 and setup_type != "NONE" else "HOLD / WATCH"
        
        val_vah_str = f"{val:.2f} / {vah:.2f}" if val else "n/a"
        sig_count = len(abs_sigs)
        
        print(f"{sym:<6} | ${px:<9.4f} | {'RANGE':<12} | {z:<+8.2f} | {poc:<10.4f} | {val_vah_str:<18} | {sig_count:<10} | {buy_ratio:<5.1f}% | {r_score:<6.1f} | {status}")
        
        if r_score >= 4.5:
            results.append({
                'sym': sym,
                'px': px,
                'z': z,
                'poc': poc,
                'val': val,
                'vah': vah,
                'r_score': r_score,
                'setup_type': setup_type,
                'status': status
            })

    print("=" * 115)
    print(f"Top High-Confluence Setups in Expanded Universe (Score >= 4.5): {len(results)}")
    for r in results:
        print(f"-> {r['sym']}: Score {r['r_score']:.1f} | Type: {r['setup_type']} | px: ${r['px']:.4f} | z: {r['z']:+.2f} | POC: {r['poc']:.4f} | Status: {r['status']}")

if __name__ == '__main__':
    scan_sleeves()
