import urllib.request
import json
import math

symbols = [
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC',
    'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR',
    'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB'
]

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Scanner/1.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

# Fetch Delta products
delta_url = 'https://api.india.delta.exchange/v2/products'
delta_data = fetch_json(delta_url)
delta_products = {}
if delta_data and 'result' in delta_data:
    for p in delta_data['result']:
        if p.get('contract_type') == 'perpetual_futures':
            delta_products[p.get('symbol')] = p

print(f"Loaded {len(delta_products)} Delta Exchange perp products.")

results = []

for sym in symbols:
    mkt = fetch_json(f'http://127.0.0.1:3000/api/cg/market?sym={sym}')
    nar = fetch_json(f'http://127.0.0.1:3000/api/cg/narrative?sym={sym}')
    liq = fetch_json(f'http://127.0.0.1:3000/api/cg/liqlevels?sym={sym}')
    sig = fetch_json(f'http://127.0.0.1:3000/api/cg/signals?sym={sym}')
    cvd = fetch_json(f'http://127.0.0.1:3000/api/cg/cvd?sym={sym}')
    bw = fetch_json(f'http://127.0.0.1:3000/api/cg/bookwalls?sym={sym}')
    
    if not mkt or not nar:
        continue
        
    price_info = mkt.get('price', {})
    last_price = float(price_info.get('last') or 0)
    if last_price <= 0:
        continue
        
    regime = nar.get('regime', 'UNKNOWN')
    active_model = nar.get('activeModel', 'UNKNOWN')
    direction = nar.get('direction', 'UNKNOWN')
    
    # Check Delta product match
    # Usually <SYM>USD or <SYM>USDT
    delta_sym = f"{sym}USD"
    dp = delta_products.get(delta_sym)
    if not dp:
        delta_sym = f"{sym}USDT"
        dp = delta_products.get(delta_sym)
    if not dp and sym == '1000PEPE':
        dp = delta_products.get('PEPEUSD')
    if not dp and sym == '1000SHIB':
        dp = delta_products.get('SHIBUSD')
        
    contract_val = float(dp.get('contract_value', 0)) if dp else 0
    prod_id = dp.get('id') if dp else None
    
    # Required margin for 1 contract at 25x
    notional_1_contract = last_price * contract_val if contract_val > 0 else 0
    margin_25x = notional_1_contract / 25.0 if notional_1_contract > 0 else 999.0
    margin_50x = notional_1_contract / 50.0 if notional_1_contract > 0 else 999.0
    
    auction = mkt.get('auction', {})
    day_auc = auction.get('day', {})
    day_poc = float(day_auc.get('poc') or 0)
    day_vah = float(day_auc.get('vah') or 0)
    day_val = float(day_auc.get('val') or 0)
    
    sess_auc = auction.get('session', {})
    sess_poc = float(sess_auc.get('poc') or 0)
    
    vwap_info = mkt.get('vwap', {})
    vwap_val = float(vwap_info.get('vwap') or 0)
    bands = vwap_info.get('bands', {})
    sd1 = float(bands.get('sd1') or 0)
    sd2 = float(bands.get('sd2') or 0)
    sd3 = float(bands.get('sd3') or 0)
    z_score = (last_price - vwap_val) / sd1 if sd1 > 0 else 0
    
    emas = mkt.get('ema', {})
    h4_ema = emas.get('h4', {})
    d1_ema = emas.get('d1', {})
    h4_trend = 'DOWN' if h4_ema.get('e13', 0) < h4_ema.get('e89', 0) else 'UP'
    d1_trend = 'DOWN' if d1_ema.get('e13', 0) < d1_ema.get('e89', 0) else 'UP'
    
    # Liquidation Skew
    clusters = liq.get('clusters', []) if liq else []
    levels_data = liq.get('levels', {}) if liq else {}
    
    shorts_above = 0
    longs_below = 0
    for c in clusters:
        cp = float(c.get('price') or 0)
        c_usd = float(c.get('usd') or 0)
        if last_price < cp <= last_price * 1.02:
            shorts_above += c_usd
        elif last_price * 0.98 <= cp < last_price:
            longs_below += c_usd
            
    lsr = shorts_above / longs_below if longs_below > 0 else (99.0 if shorts_above > 0 else 1.0)
    
    results.append({
        'sym': sym,
        'price': last_price,
        'regime': regime,
        'active_model': active_model,
        'dir': direction,
        'vwap_z': z_score,
        'day_poc': day_poc,
        'day_vah': day_vah,
        'day_val': day_val,
        'sess_poc': sess_poc,
        'vwap': vwap_val,
        'h4_trend': h4_trend,
        'd1_trend': d1_trend,
        'shorts_above': shorts_above,
        'longs_below': longs_below,
        'lsr': lsr,
        'delta_sym': delta_sym if dp else None,
        'prod_id': prod_id,
        'contract_val': contract_val,
        'margin_25x': margin_25x,
        'margin_50x': margin_50x
    })

print(f"Scanned {len(results)} assets. Filtering candidates...")

# Candidate criteria:
# 1. Delta product exists and margin_25x <= $0.90 (or margin_50x <= $0.90)
# 2. VWAP z >= 1.0 (for Short S1/S2/S5) or z <= -1.0 (for Long S1/S2/S5)
# 3. Macro trend alignment
# 4. Liquidation hazard checks

candidates = []
for r in results:
    if not r['delta_sym']:
        continue
    if r['margin_25x'] > 0.95 and r['margin_50x'] > 0.95:
        continue
        
    print(f"\n--- Analyzing {r['sym']} ({r['delta_sym']}) ---")
    print(f"Price: {r['price']} | VWAP z: {r['vwap_z']:.2f} | Margin 25x: ${r['margin_25x']:.3f} | Margin 50x: ${r['margin_50x']:.3f}")
    print(f"Regime: {r['regime']} | Model: {r['active_model']} | H4: {r['h4_trend']}, D1: {r['d1_trend']}")
    print(f"LSR (±2%): {r['lsr']:.2f}:1 (Shorts Above: ${r['shorts_above']:,.0f} vs Longs Below: ${r['longs_below']:,.0f})")
    
    # Test Short S1 / S5
    if r['vwap_z'] >= 0.8:
        # Potential Short setup
        # Entry at or above Day VAH / +1.5σ VWAP / nearest upper cluster
        entry = max(r['day_vah'], r['vwap'] + 1.5 * (r['price'] - r['vwap'])/r['vwap_z']) if r['vwap_z'] > 0 else r['price'] * 1.01
        if entry <= r['price']:
            entry = r['price'] * 1.012
        sl = entry * 1.025
        tp = r['day_poc'] if r['day_poc'] < entry else r['vwap']
        risk = sl - entry
        reward = entry - tp
        r_mult = reward / risk if risk > 0 else 0
        
        candidates.append({
            'sym': r['sym'],
            'delta_sym': r['delta_sym'],
            'prod_id': r['prod_id'],
            'side': 'sell',
            'price': r['price'],
            'entry': entry,
            'sl': sl,
            'tp': tp,
            'r_mult': r_mult,
            'vwap_z': r['vwap_z'],
            'lsr': r['lsr'],
            'margin_25x': r['margin_25x'],
            'margin_50x': r['margin_50x'],
            'regime': r['regime'],
            'h4_trend': r['h4_trend']
        })

print(f"\nTotal potential candidates found: {len(candidates)}")
for c in candidates:
    print(f"{c['sym']}: {c['side'].upper()} @ {c['entry']:.4f} | SL: {c['sl']:.4f} | TP: {c['tp']:.4f} | R: {c['r_mult']:.2f}R | Margin 25x: ${c['margin_25x']:.3f} | LSR: {c['lsr']:.2f}:1")
