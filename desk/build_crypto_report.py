import json
import time
from datetime import datetime, timezone

with open('desk/crypto_telemetry_bundle.json', 'r') as f:
    bundle = json.load(f)

curated_crypto = [
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC',
    'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR',
    'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB'
]

sectors = {
    'BTC': 'Store of Value', 'ETH': 'Smart Contract L1', 'BNB': 'Exchange Token',
    'SOL': 'Smart Contract L1', 'XRP': 'Payments', 'ADA': 'Smart Contract L1',
    'DOGE': 'Meme', 'TRX': 'Smart Contract L1', 'LINK': 'Oracle', 'LTC': 'Payments',
    'AVAX': 'Smart Contract L1', 'DOT': 'Interoperability', 'NEAR': 'Smart Contract L1',
    'UNI': 'DeFi DEX', 'ATOM': 'Interoperability', 'XLM': 'Payments', 'ETC': 'Smart Contract L1',
    'FIL': 'Storage', 'ICP': 'Smart Contract L1', 'HBAR': 'Enterprise L1', 'APT': 'Smart Contract L1',
    'ARB': 'Ethereum L2', 'OP': 'Ethereum L2', 'SUI': 'Smart Contract L1', 'SEI': 'Smart Contract L1',
    'INJ': 'DeFi L1', 'TIA': 'Modular DA', 'VET': 'Supply Chain', '1000PEPE': 'Meme', '1000SHIB': 'Meme'
}

all_data = bundle['all_data']
delta_contracts = bundle['delta_contracts']

def parse_asset(sym):
    data = all_data[sym]
    nar = data.get('narrative', {})
    mkt = data.get('market', {})
    sig = data.get('signals', {})
    cvd = data.get('cvd', {})
    bw = data.get('bookwalls', {})
    liq = data.get('liqlevels', {})
    opt = data.get('options', {})
    dl2 = data.get('delta_l2', {})
    dtick = data.get('delta_ticker', {})
    contract = delta_contracts.get(sym)

    # Price & Context
    ctx = nar.get('context', {})
    price = float(ctx.get('price') or mkt.get('price') or 0)
    vwap_z = float(ctx.get('vwapZ') or mkt.get('vwap', {}).get('z') or 0)
    regime = nar.get('regime') or mkt.get('regime') or 'RANGE_BALANCE'
    direction = nar.get('direction') or 'NEUTRAL'
    grade = nar.get('grade') or 'B'
    conf = int(nar.get('confidence') or 0)
    m1_stat = nar.get('m1', {}).get('status', 'OFF')
    m2_stat = nar.get('m2', {}).get('status', 'OFF')
    m_status = f"M1:{m1_stat}" if m1_stat != 'OFF' else (f"M2:{m2_stat}" if m2_stat != 'OFF' else "OFF")

    # Delta CLOB
    if contract and dtick:
        dsym = contract['symbol']
        c_val = float(contract.get('contract_value', 1))
        tick_sz = float(contract.get('tick_size', 0.01))
        quotes = dtick.get('quotes', {})
        d_mark = float(dtick.get('mark_price') or price)
        best_bid = float(quotes.get('best_bid') or 0)
        best_ask = float(quotes.get('best_ask') or 0)
        d_spread = best_ask - best_bid if (best_ask and best_bid) else 0
        d_spread_pct = (d_spread / d_mark * 100) if d_mark > 0 else 0
        listed = True
    else:
        dsym = 'NOT LISTED'
        c_val = None
        tick_sz = None
        d_mark = price
        best_bid = 0
        best_ask = 0
        d_spread = 0
        d_spread_pct = 0
        listed = False

    # Liq LSR
    stats = liq.get('stats', {}) if isinstance(liq, dict) else {}
    bands = stats.get('bands', [])
    up2 = sum(b.get('up', 0) for b in bands[:2])
    down2 = sum(b.get('down', 0) for b in bands[:2])
    if up2 >= down2:
        r = (up2 / down2) if down2 > 0 else 99.0
        lsr_str = f"{r:.1f}:1 (SA)"
        lsr_val = r
        dom = "SA"
    else:
        r = (down2 / up2) if up2 > 0 else 99.0
        lsr_str = f"{r:.1f}:1 (LB)"
        lsr_val = r
        dom = "LB"

    # Table 7 Confluence Scoring (11.5 max)
    # 1. Directional Trend (2.0 max): H4 & D1 EMA 13x89 aligned
    emas = mkt.get('emas', {})
    h4_down = emas.get('h4', {}).get('ema13', 0) < emas.get('h4', {}).get('ema89', 0)
    d1_down = emas.get('d1', {}).get('ema13', 0) < emas.get('d1', {}).get('ema89', 0)
    h4_up = emas.get('h4', {}).get('ema13', 0) > emas.get('h4', {}).get('ema89', 0)
    d1_up = emas.get('d1', {}).get('ema13', 0) > emas.get('d1', {}).get('ema89', 0)

    t7_trend = 0.0
    if direction == 'SHORT' and h4_down and d1_down:
        t7_trend = 2.0
    elif direction == 'LONG' and h4_up and d1_up:
        t7_trend = 2.0
    elif (direction == 'SHORT' and (h4_down or d1_down)) or (direction == 'LONG' and (h4_up or d1_up)):
        t7_trend = 1.0

    # 2. Auction / VWAP Regime (1.5 max): Short in premium (price > vwap), Long in discount (price < vwap)
    vwap_mid = float(mkt.get('vwap', {}).get('mid') or price)
    t7_vwap = 0.0
    if direction == 'SHORT' and price >= vwap_mid:
        t7_vwap = 1.5
    elif direction == 'LONG' and price <= vwap_mid:
        t7_vwap = 1.5
    elif direction == 'SHORT' and vwap_z > -0.5: # near mid
        t7_vwap = 0.5
    elif direction == 'LONG' and vwap_z < 0.5:
        t7_vwap = 0.5

    # 3. Footprint Signal (2.0 max)
    # Check if discrete abs/div/trap fired in direction
    signals_list = sig.get('signals', []) if isinstance(sig, dict) else []
    recent_signals = signals_list[:10]
    t7_signal = 0.0
    sig_desc = "No qualifying signal at zone"
    for s in recent_signals:
        stype = s.get('type', '').lower()
        sdir = s.get('dir', '').upper()
        if 'abs' in stype or 'div' in stype or 'trap' in stype:
            if direction == 'SHORT' and sdir in ['SELL', 'SHORT', 'BEAR']:
                t7_signal = 2.0
                sig_desc = f"{s.get('type')} ({sdir}) @ {s.get('price')}"
                break
            elif direction == 'LONG' and sdir in ['BUY', 'LONG', 'BULL']:
                t7_signal = 2.0
                sig_desc = f"{s.get('type')} ({sdir}) @ {s.get('price')}"
                break
    if t7_signal == 0.0 and len(signals_list) > 0:
        # Check narrative checklist
        cl = {item['key']: item for item in nar.get('checklist', [])}
        if cl.get('footprint', {}).get('pass'):
            t7_signal = 1.5
            sig_desc = cl['footprint'].get('value', 'Narrative footprint confirmation')

    # 4. Whale Wall Backstop (1.5 max)
    # Check resting wall >= $5M (BTC/ETH) or >= $1M (alts)
    min_wall = 5000000 if sym in ['BTC', 'ETH'] else 1000000
    walls = bw.get('model', {}).get('confirmedWalls', []) if isinstance(bw, dict) else []
    t7_wall = 0.0
    wall_desc = "No confirmed wall defense"
    for w in walls:
        w_usd = float(w.get('usd') or 0)
        w_side = w.get('side', '').lower()
        if w_usd >= min_wall:
            if direction == 'SHORT' and w_side == 'ask':
                t7_wall = 1.5
                wall_desc = f"Ask Wall ${w_usd/1e6:.2f}M @ {w.get('price')}"
                break
            elif direction == 'LONG' and w_side == 'bid':
                t7_wall = 1.5
                wall_desc = f"Bid Wall ${w_usd/1e6:.2f}M @ {w.get('price')}"
                break
    if t7_wall == 0.0:
        # Check Delta L2 depth for large resting wall
        if dl2 and 'result' in dl2:
            ob = dl2['result']
            side_key = 'sell' if direction == 'SHORT' else 'buy'
            for lvl in ob.get(side_key, [])[:15]:
                lvl_usd = float(lvl.get('size', 0)) * c_val * float(lvl.get('price', 0))
                if lvl_usd >= min_wall * 0.1: # substantial Delta wall
                    t7_wall = 1.0
                    wall_desc = f"Delta L2 {side_key.upper()} Wall ${lvl_usd/1e3:.1f}k @ {lvl.get('price')}"
                    break

    # 5. CVD Divergence (1.0 max)
    divs = cvd.get('divergences', []) if isinstance(cvd, dict) else []
    t7_cvd = 0.0
    cvd_desc = "No active CVD divergence"
    for d in divs:
        dt = d.get('type', '').lower()
        if direction == 'SHORT' and ('bear' in dt or 'sell' in dt):
            t7_cvd = 1.0
            cvd_desc = f"Active BEAR CVD divergence ({d.get('span', '')})"
            break
        elif direction == 'LONG' and ('bull' in dt or 'buy' in dt):
            t7_cvd = 1.0
            cvd_desc = f"Active BULL CVD divergence ({d.get('span', '')})"
            break

    # 6. Liquidation Magnet Gate (1.5 max)
    t7_magnet = 0.0
    if lsr_val >= 2.5:
        # High skew: if aligned with trade direction (targets into magnet)
        if direction == 'SHORT' and dom == 'LB': # Longs Below = magnet for short target
            t7_magnet = 1.5
        elif direction == 'LONG' and dom == 'SA': # Shorts Above = magnet for long target
            t7_magnet = 1.5
    elif lsr_val >= 1.5:
        if (direction == 'SHORT' and dom == 'LB') or (direction == 'LONG' and dom == 'SA'):
            t7_magnet = 1.0

    # 7. Options GEX Context (1.0 max) - BTC/ETH only
    t7_gex = 0.0
    gex_desc = "non-BTC/ETH (0.0 pts n/a)"
    if sym in ['BTC', 'ETH'] and isinstance(opt, dict) and opt.get('ok'):
        gex_regime = opt.get('regime', '')
        if 'NEGATIVE_GAMMA' in gex_regime:
            t7_gex = 1.0
            gex_desc = f"Negative Gamma Expansion ({opt.get('flip')})"
        elif 'POSITIVE_GAMMA' in gex_regime:
            t7_gex = 1.0
            gex_desc = f"Positive Gamma Balance ({opt.get('flip')})"
    
    # 8. Broker Spread Drag (1.0 max) - on Delta Exchange!
    t7_spread = 0.0
    if not listed:
        t7_spread = 0.0
        spread_desc = "NOT LISTED ON DELTA (0.0 pts)"
    elif d_spread_pct < 0.05:
        t7_spread = 1.0
        spread_desc = f"{d_spread_pct:.4f}% < 0.05% (1.0 pt)"
    elif d_spread_pct <= 0.10:
        t7_spread = 0.5
        spread_desc = f"{d_spread_pct:.4f}% [0.05%-0.10%] (0.5 pts)"
    else:
        t7_spread = 0.0
        spread_desc = f"{d_spread_pct:.4f}% > 0.10% (0.0 pts)"

    total_score = t7_trend + t7_vwap + t7_signal + t7_wall + t7_cvd + t7_magnet + t7_gex + t7_spread

    # Active Vetoes
    vetoes = []
    if lsr_val >= 2.5:
        vetoes.append(f"LSR {lsr_val:.1f}:1 >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1)")
    if d_spread_pct > 0.15 and listed:
        vetoes.append(f"Delta spread {d_spread_pct:.4f}% > 0.15% — execution drag veto")
    if not listed:
        vetoes.append("Not listed on Delta Exchange")
    if total_score < 5.0:
        vetoes.append(f"Table 7 score {total_score:.1f} < 5.0 — HARD VETO (NO TRADE)")
    
    # Desk R-standard check from narrative plan
    plan = nar.get('plan', {})
    best_r = float(plan.get('bestR') or 0)
    if best_r > 0 and best_r < 1.5:
        vetoes.append(f"Model R {best_r:.2f} < 1.5 — reward does not pay risk")

    # Final Grade
    if total_score >= 7.0 and len([v for v in vetoes if 'HARD VETO' in v or 'Not listed' in v or 'spread' in v]) == 0:
        calc_grade = 'A'
    elif total_score >= 5.0 and len([v for v in vetoes if 'HARD VETO' in v or 'Not listed' in v or 'spread' in v]) == 0:
        calc_grade = 'B'
    else:
        calc_grade = 'VETO'

    qualifier = (calc_grade in ['A', 'B']) or (conf >= 80 and m1_stat == 'TRIGGERED') or (lsr_val >= 2.5) or (sym in ['BTC', 'ETH', 'SOL'])

    return {
        'sym': sym,
        'sector': sectors.get(sym, 'Crypto'),
        'price': price,
        'regime': regime,
        'direction': direction,
        'grade': calc_grade,
        'conf': conf,
        'm_status': m_status,
        'm1_stat': m1_stat,
        'm2_stat': m2_stat,
        'vwap_z': vwap_z,
        'vwap_mid': vwap_mid,
        'lsr_str': lsr_str,
        'lsr_val': lsr_val,
        'dom': dom,
        'contract': contract,
        'dsym': dsym,
        'c_val': c_val,
        'tick_sz': tick_sz,
        'd_mark': d_mark,
        'best_bid': best_bid,
        'best_ask': best_ask,
        'd_spread': d_spread,
        'd_spread_pct': d_spread_pct,
        'listed': listed,
        't7': {
            'trend': t7_trend,
            'vwap': t7_vwap,
            'signal': t7_signal,
            'wall': t7_wall,
            'cvd': t7_cvd,
            'magnet': t7_magnet,
            'gex': t7_gex,
            'spread': t7_spread,
            'total': total_score,
            'sig_desc': sig_desc,
            'wall_desc': wall_desc,
            'cvd_desc': cvd_desc,
            'gex_desc': gex_desc,
            'spread_desc': spread_desc
        },
        'vetoes': vetoes,
        'qualifier': qualifier,
        'plan': plan,
        'mkt': mkt,
        'nar': nar,
        'sig': sig,
        'cvd_data': cvd,
        'bw': bw,
        'liq': liq,
        'opt': opt,
        'dl2': dl2,
        'dtick': dtick
    }

parsed_all = [parse_asset(s) for s in curated_crypto]

print("=== SCREENING SUMMARY ===")
for p in parsed_all:
    d_info = f"{p['dsym']} ({p['d_spread_pct']:.4f}%)" if p['listed'] else "NOT LISTED"
    print(f"{p['sym']:10} | ${p['price']:<10.4f} | {p['direction']:<5} | T7: {p['t7']['total']:<4.1f} | Grade: {p['grade']:<4} | LSR: {p['lsr_str']:<11} | {d_info:<22} | Qual: {p['qualifier']}")

qualifiers = [p for p in parsed_all if p['qualifier']]
print(f"\nTotal Qualifiers: {len(qualifiers)}")
print("Qualifying assets:", [q['sym'] for q in qualifiers])
