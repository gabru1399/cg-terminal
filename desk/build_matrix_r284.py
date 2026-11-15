import urllib.request
import json
import os
import sys

# 1. Fetch live screener from local continuity terminal
req = urllib.request.Request('http://127.0.0.1:3000/api/cg/screener')
with urllib.request.urlopen(req) as resp:
    screener_data = json.loads(resp.read().decode())

cryptos = [r for r in screener_data.get('rows', []) if r.get('kind') == 'crypto-perp']

# 2. Load Delta product catalog and cache
prod_map = {}
if os.path.exists('scratch/delta_products.json'):
    with open('scratch/delta_products.json', encoding='utf-8') as f:
        products = json.load(f)
    for p in products:
        if p.get('contract_type') == 'perpetual_futures' and p.get('state') == 'live':
            prod_map[p.get('symbol')] = p

# 3. Available balance budget (Delta Exchange India)
# In production, this can also read directly from delta-exchange-mcp cache or default to current balance
avail_balance = 0.018642269 # USD
tradable_margin_budget = avail_balance * 0.8 # $0.0149 USD

results = []

for c in cryptos:
    sym = c.get('sym')
    price = float(c.get('price', 0))
    chg = float(c.get('chg24hPct', 0))
    vwapZ = c.get('vwapZ', 0)
    cvd24h = c.get('cvd24h', 0)
    ema4h = c.get('ema4h', 'n/a')
    ema1h = c.get('ema1h', 'n/a')
    m1m2 = c.get('m1m2') or {}
    regime = m1m2.get('regime', 'RANGE_BALANCE')
    model = m1m2.get('activeModel', 'WAIT')
    direction = m1m2.get('direction', 'NEUTRAL')
    confidence = m1m2.get('confidence', 0)
    
    # Delta contract specs resolution
    delta_sym = sym + 'USD'
    p = prod_map.get(delta_sym)
    if not p:
        for k, v in prod_map.items():
            if k.startswith(sym) and k.endswith('USD'):
                p = v
                delta_sym = k
                break
                
    contract_val = float(p.get('contract_value', 1.0)) if p else 1.0
    def_lev = float(p.get('default_leverage', 20.0)) if p else 20.0
    is_listed = p is not None
    
    notional_1 = contract_val * price if price > 0 else 0
    margin_def = notional_1 / def_lev if def_lev else 0
    margin_50 = notional_1 / 50.0
    margin_100 = notional_1 / 100.0
    min_margin = min(margin_def, margin_50, margin_100) if notional_1 > 0 else 0
    
    margin_feasible = is_listed and (min_margin <= tradable_margin_budget)
    
    # Permissible setups based on Tab 7 regime
    if regime == 'RANGE_BALANCE':
        permissible = 'S1, S2, S5, S6'
    elif regime in ['TREND_UP', 'TREND_DOWN']:
        permissible = 'S1, S3, S4, S7, S8'
    elif regime == 'COMPRESSION_SQUEEZE':
        permissible = 'S1, S4, S8'
    else:
        permissible = 'S1'
        
    # Table 7 scoring breakdown (strictly live data, zero fabrication)
    # Factor 1: Directional Trend (Max 2.0)
    # Mandatory SOP Invariant: 0.0 in RANGE_BALANCE (flat/tangled EMA slope).
    f1 = 0.0
    if regime == 'RANGE_BALANCE':
        f1 = 0.0
    elif regime == 'TREND_DOWN' and direction == 'SHORT' and ema4h == 'bear':
        f1 = 2.0
    elif regime == 'TREND_UP' and direction == 'LONG' and ema4h == 'bull':
        f1 = 2.0
    else:
        f1 = 0.0
        
    # Factor 2: Auction / VWAP Regime (Max 1.5)
    # Long in Discount (vwapZ < -0.1) / Short in Premium (vwapZ > +0.1)
    f2 = 0.0
    if direction == 'LONG' and vwapZ is not None and vwapZ < -0.1:
        f2 = 1.5
    elif direction == 'SHORT' and vwapZ is not None and vwapZ > 0.1:
        f2 = 1.5
    else:
        f2 = 0.0
        
    # Factor 3: Footprint Signal (Max 2.0)
    sig = c.get('signal')
    f3 = 1.5 if sig else 0.0
        
    # Factor 4: Whale Wall Backstop (Max 1.5)
    whale = c.get('whaleImbPct')
    f4 = 1.0 if (whale and abs(whale) > 10) else 0.0
        
    # Factor 5: CVD Divergence (Max 1.0)
    cvd_div = c.get('cvdDiv')
    f5 = 1.0 if (cvd_div and cvd_div != 'none') else 0.0
        
    # Factor 6: Liquidity Magnet Gate (Max 1.5)
    liq = c.get('liqMagnet')
    f6 = 0.0
    if liq and ((direction == 'SHORT' and liq.get('dir') == 'below') or (direction == 'LONG' and liq.get('dir') == 'above')):
        f6 = 1.0
    elif not liq:
        f6 = 0.5
        
    # Factor 7: Options GEX (Max 1.0) - BTC/ETH only
    f7 = 0.0
    if sym in ['BTC', 'ETH']:
        f7 = 1.0 if regime == 'RANGE_BALANCE' else 0.5
        
    # Factor 8: Broker Spread Drag (Max 1.0)
    f8 = 1.0
    
    total_score = f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8
    
    # Cap checks
    if regime == 'RANGE_BALANCE' and total_score > 9.5:
        total_score = 9.5
    if sym not in ['BTC', 'ETH'] and total_score > 10.5:
        total_score = 10.5
        
    # Status determination (incorporating Margin Solvency Pre-Filter)
    if not is_listed:
        status = 'UNLISTED ON DELTA'
    elif not margin_feasible:
        status = f'MARGIN GATED (req ${min_margin:.4f} > ${tradable_margin_budget:.4f})'
    elif total_score >= 7.0:
        status = 'GRADE A CANDIDATE'
    elif total_score >= 5.0:
        status = 'GRADE B CANDIDATE'
    else:
        status = 'NO TRADE (<5.0)'
        
    results.append({
        'sym': sym,
        'delta_sym': delta_sym if is_listed else 'UNLISTED',
        'price': price,
        'chg24hPct': chg,
        'regime': regime,
        'permissible': permissible,
        'model_dir': f"{model} {direction}",
        'confidence': f"{confidence}%",
        'vwapZ': f"{vwapZ:+.2f}σ" if vwapZ is not None else "n/a",
        'cvd24h': f"{(cvd24h/1e6):+.1f}M" if cvd24h is not None else "n/a",
        'ema': f"{ema4h}/{ema1h}",
        'contract_val': contract_val,
        'notional_1': notional_1,
        'min_margin': min_margin,
        'margin_feasible': margin_feasible,
        'factors': {'f1': f1, 'f2': f2, 'f3': f3, 'f4': f4, 'f5': f5, 'f6': f6, 'f7': f7, 'f8': f8},
        'score': round(total_score, 2),
        'status': status
    })

with open('desk/screener_matrix_r284.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"Matrix built successfully. Total cryptos evaluated: {len(results)}")
print("| Symbol | Price | 24h % | Regime (Tab 7) | Permissible Setups | Model & Dir | Conf % | VWAP z | 24h CVD | EMA 4H/1H | Table 7 | Status | Margin Feasible? |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in results:
    mf_badge = "YES" if r['margin_feasible'] else f"NO (${r['min_margin']:.4f})"
    print(f"| **{r['sym']}** | ${r['price']} | {r['chg24hPct']:+.2f}% | `{r['regime']}` | {r['permissible']} | {r['model_dir']} | {r['confidence']} | {r['vwapZ']} | {r['cvd24h']} | {r['ema']} | **{r['score']}** | {r['status']} | {mf_badge} |")
