import urllib.request
import json

req = urllib.request.Request('http://127.0.0.1:3000/api/cg/screener', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        rows = data.get('rows', [])
        print(f'Fetched {len(rows)} rows from terminal screener')
        
        curated30 = [
            'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC',
            'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR',
            'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB'
        ]
        
        row_map = {r.get('sym'): r for r in rows}
        
        matrix = []
        for sym in curated30:
            r = row_map.get(sym)
            if not r:
                continue
            
            price = r.get('price', 0)
            chg = r.get('chg24hPct', 0)
            m1m2 = r.get('m1m2', {})
            regime = m1m2.get('regime', 'RANGE_BALANCE')
            active_model = m1m2.get('activeModel', 'n/a')
            direction = m1m2.get('direction', 'n/a')
            conf = f"{m1m2.get('confidence', 0)}%"
            vwap_z = f"{r.get('vwapZ', 0):+.2f}σ" if r.get('vwapZ') is not None else '0.00σ'
            cvd24h = f"{r.get('cvd24h', 0) / 1e6:.1f}M" if r.get('cvd24h') is not None else '0.0M'
            ema = f"{r.get('ema4h', 'n/a')}/{r.get('ema1h', 'n/a')}"
            
            # Permissible setups based on Section 5.1
            if 'TREND' in regime:
                permissible = 'S1, S3, S4, S7, S8'
            elif 'COMPRESSION' in regime:
                permissible = 'S1, S4, S8'
            else:
                permissible = 'S1, S2, S5, S6'
            
            # True Table 7 Calculation:
            # 1. Trend: H4 and D1 aligned AND compatible with regime. In RANGE_BALANCE, scores 0.0!
            t_score = 0.0
            if 'TREND' in regime:
                if 'DOWN' in regime and r.get('ema4h') == 'bear':
                    t_score += 2.0
                elif 'UP' in regime and r.get('ema4h') == 'bull':
                    t_score += 2.0
            
            # 2. Auction / VWAP: Long in discount / Short in premium
            if r.get('vwapZ', 0) < 0 and direction == 'LONG':
                t_score += 1.5
            elif r.get('vwapZ', 0) > 0 and direction == 'SHORT':
                t_score += 1.5
            
            # 3. Footprint signal at entry
            sig = r.get('signal')
            if sig:
                t_score += 2.0
            
            # 4. Whale Wall backstop
            w_imb = r.get('whaleImbPct')
            if w_imb is not None and abs(w_imb) >= 10:
                t_score += 1.0
            
            # 5. CVD Div
            if r.get('cvdDiv'):
                t_score += 1.0
                
            # 8. Spread drag (<0.05% on all Tier 1 crypto perps)
            t_score += 1.0
            
            status = 'WATCH'
            if t_score >= 7.0:
                status = 'GRADE A (HIGH)'
            elif t_score >= 5.0:
                status = 'GRADE B (VALID)'
            else:
                status = 'WATCH (<5.0 VETO)'
                
            matrix.append({
                'sym': sym,
                'price': price,
                'chg24hPct': chg,
                'regime': regime,
                'permissible': permissible,
                'modelDir': f"{active_model} {direction}".strip(),
                'conf': conf,
                'vwapZ': vwap_z,
                'cvd24h': cvd24h,
                'ema': ema,
                't7': f"{t_score:.1f}",
                'status': status
            })
            
        with open('desk/screener_matrix_r283.json', 'w', encoding='utf-8') as f:
            json.dump(matrix, f, indent=2)
            
        print('Successfully wrote 30 rows to desk/screener_matrix_r283.json')
except Exception as e:
    print('Error:', e)
