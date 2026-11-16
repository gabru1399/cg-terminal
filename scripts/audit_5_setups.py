import urllib.request
import json
from concurrent.futures import ThreadPoolExecutor

base = "http://127.0.0.1:3000"

def get(path):
    try:
        req = urllib.request.Request(f"{base}{path}", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3.0) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

symbols = ['BNB', 'LINK', 'ARB', 'ADA', 'TIA']
orders = {
    'BNB': {'entry': 589.5, 'sl': 596.5, 'tp': 572.0, 'side': 'SHORT'},
    'LINK': {'entry': 9.12, 'sl': 9.25, 'tp': 8.80, 'side': 'SHORT'},
    'ARB': {'entry': 0.1335, 'sl': 0.1360, 'tp': 0.1270, 'side': 'SHORT'},
    'ADA': {'entry': 0.1524, 'sl': 0.1542, 'tp': 0.1479, 'side': 'SHORT'},
    'TIA': {'entry': 0.3475, 'sl': 0.3530, 'tp': 0.3340, 'side': 'SHORT'},
}

def audit_symbol(sym):
    m = get(f"/api/cg/market?sym={sym}")
    sig = get(f"/api/cg/signals?sym={sym}")
    cvd = get(f"/api/cg/cvd?sym={sym}&itv=15m")
    walls = get(f"/api/cg/bookwalls?sym={sym}")
    liq = get(f"/api/cg/liqlevels?sym={sym}")
    narr = get(f"/api/cg/narrative?sym={sym}")
    
    price = m.get('price', {}).get('last', 0.0)
    day_auc = m.get('auction', {}).get('day', {})
    sess_auc = m.get('auction', {}).get('session', {})
    vw = m.get('vwap', {})
    ema = m.get('ema', {})
    rsi = m.get('rsi', {})
    
    plan = orders[sym]
    entry = plan['entry']
    sl = plan['sl']
    tp = plan['tp']
    
    sess_poc = sess_auc.get('poc', 0.0)
    day_poc = day_auc.get('poc', 0.0)
    day_vwap = vw.get('vwap', 0.0)
    
    clear_sess = abs(sl - sess_poc) / sess_poc * 100 if sess_poc else 0.0
    clear_day = abs(sl - day_poc) / day_poc * 100 if day_poc else 0.0
    clear_vwap = abs(sl - day_vwap) / day_vwap * 100 if day_vwap else 0.0
    
    clusters = liq.get('clusters', []) if isinstance(liq.get('clusters'), list) else []
    risk_zone_clusters = [c for c in clusters if entry < c.get('price', 0.0) <= sl * 1.005]
    magnet_clusters = [c for c in clusters if tp <= c.get('price', 0.0) < entry]
            
    regime = narr.get('regime', 'RANGE_BALANCE')
    f1 = 0.0
    h4_13 = ema.get('h4', {}).get('e13')
    h4_89 = ema.get('h4', {}).get('e89')
    d1_13 = ema.get('d1', {}).get('e13')
    d1_89 = ema.get('d1', {}).get('e89')
    if regime in ['TREND_DOWN'] and h4_13 and h4_89 and h4_13 < h4_89:
        f1 = 2.0 if (d1_13 and d1_89 and d1_13 < d1_89) else 1.0
        
    sd1 = vw.get('bands', {}).get('sd1', 0.0)
    z = (entry - day_vwap) / sd1 if (day_vwap and sd1 and sd1 > 0) else 0.0
    f2 = 1.5 if z > 1.0 else (0.5 if z >= -0.5 else 0.0)
        
    f3 = 0.0
    sigs_list = [s.get('type') for st in sig.get('sets', []) for s in st.get('sigs', [])]
    for stype in sigs_list:
        if stype in ['Absorption', 'Strong Divergence']:
            f3 = max(f3, 2.0)
        elif stype in ['Divergence', 'Trap', 'Exhaustion']:
            f3 = max(f3, 1.0)
            
    f4 = 1.0 if walls.get('ok') else 0.0
    f5 = 1.0 if cvd.get('ok') else 0.0
    f6 = 1.5 if len(magnet_clusters) > 0 else 0.5
    f7 = 0.5 if sym in ['BNB'] else 0.0
    f8 = 1.0
    
    total_score = f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8
    
    return sym, {
        'price': price,
        'entry': entry,
        'sl': sl,
        'tp': tp,
        'r_mult': round((entry - tp) / (sl - entry), 2),
        'sess_poc': sess_poc,
        'day_poc': day_poc,
        'day_vwap': day_vwap,
        'vwap_z': round(z, 2),
        'clear_sess_pct': round(clear_sess, 2),
        'clear_day_pct': round(clear_day, 2),
        'gate1_pass': clear_sess >= 0.5 and clear_day >= 0.5,
        'gate2_hazard_count': len(risk_zone_clusters),
        'gate2_pass': len(risk_zone_clusters) == 0,
        'f1_trend': f1,
        'f2_vwap': f2,
        'f3_sig': f3,
        'f4_wall': f4,
        'f5_cvd': f5,
        'f6_liq': f6,
        'f7_tier': f7,
        'f8_fric': f8,
        'table7_total': round(total_score, 1),
        'grade': 'A' if total_score >= 7.0 else ('B' if total_score >= 5.0 else 'NO_TRADE'),
        'signals': sigs_list[:4],
        'model': narr.get('activeModel'),
        'narr_grade': narr.get('grade'),
        'narr_evR': narr.get('evR')
    }

with ThreadPoolExecutor(max_workers=5) as ex:
    results = dict(ex.map(audit_symbol, symbols))

print(json.dumps(results, indent=2))
