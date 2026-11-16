import urllib.request
import json

def fetch_json(endpoint):
    url = f'http://127.0.0.1:3000{endpoint}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AdversarialAuditor/3.4'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f'Error fetching {endpoint}: {e}')
        return None

def audit_setup(sym, entry, sl, tp, side='sell'):
    print(f"\n=================== AUDIT FOR {sym} ===================")
    mkt = fetch_json(f'/api/cg/market?sym={sym}')
    fp = fetch_json(f'/api/cg/fp?sym={sym}')
    liq = fetch_json(f'/api/cg/liqlevels?sym={sym}&range=3d&lvR=4')
    sig = fetch_json(f'/api/cg/signals?sym={sym}')
    bw = fetch_json(f'/api/cg/bookwalls?sym={sym}')
    
    last_p = mkt.get('price', {}).get('last', 0)
    sess_poc = mkt.get('auction', {}).get('session', {}).get('poc', 0)
    sess_vah = mkt.get('auction', {}).get('session', {}).get('vah', 0)
    sess_val = mkt.get('auction', {}).get('session', {}).get('val', 0)
    day_poc = mkt.get('auction', {}).get('day', {}).get('poc', 0)
    day_vah = mkt.get('auction', {}).get('day', {}).get('vah', 0)
    day_val = mkt.get('auction', {}).get('day', {}).get('val', 0)
    vwap = mkt.get('vwap', {}).get('vwap', 0)
    
    print(f"Price: {last_p} | Entry: {entry} | SL: {sl} | TP: {tp}")
    risk = abs(sl - entry)
    reward = abs(entry - tp)
    r_mult = reward / risk if risk else 0
    print(f"Risk: {risk:.4f} | Reward: {reward:.4f} | R: {r_mult:.2f}R")
    
    # Gate 1
    d_sess_poc = abs(sl - sess_poc) / sess_poc * 100 if sess_poc else 99
    d_day_poc = abs(sl - day_poc) / day_poc * 100 if day_poc else 99
    d_vwap = abs(sl - vwap) / vwap * 100 if vwap else 99
    print(f"Gate 1 Clearance: SessPOC={d_sess_poc:.2f}% | DayPOC={d_day_poc:.2f}% | VWAP={d_vwap:.2f}%")
    
    # Gate 2: Liquidation Geometry
    stats = liq.get('stats', {}) if liq else {}
    above = stats.get('keyLevels', {}).get('above', [])
    below = stats.get('keyLevels', {}).get('below', [])
    
    # Risk zone hazard: clusters between entry and sl
    lo_rz = min(entry, sl)
    hi_rz = max(entry, sl)
    rz_hazard = 0
    for l in above:
        p = l.get('price', 0)
        if lo_rz <= p <= hi_rz:
            rz_hazard += l.get('usd', 0)
    print(f"Gate 2 Risk Zone [{lo_rz} - {hi_rz}] Hazard: ${rz_hazard:,.2f}")
    
    totals = stats.get('totals', {})
    sh = totals.get('shorts', 0)
    lg = totals.get('longs', 0)
    lsr = sh / lg if lg else 1.0
    print(f"3d LSR: {lsr:.2f}:1 (Shorts: ${sh:,.0f} | Longs: ${lg:,.0f})")

audit_setup('ETH', 1828.50, 1845.50, 1792.50)
audit_setup('LTC', 45.300, 45.680, 44.500)
