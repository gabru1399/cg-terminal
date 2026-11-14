import json

with open('desk/crypto_raw_sweep.json', 'r') as f:
    data = json.load(f)

curated_crypto = [
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC',
    'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR',
    'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB'
]

narratives = data.get('narratives', {})
liqlevels = data.get('liqlevels', {})
delta_contracts = data.get('delta_contracts', {})
delta_tickers = data.get('delta_tickers', {})

qualifiers = []
print("=== TIER A FULL SCREENING TABLE ===")
for sym in curated_crypto:
    nar = narratives.get(sym, {})
    liq = liqlevels.get(sym, {})
    stats = liq.get('stats', {}) if isinstance(liq, dict) else {}
    bands = stats.get('bands', [])
    
    up2 = sum(b.get('up', 0) for b in bands[:2])
    down2 = sum(b.get('down', 0) for b in bands[:2])
    if up2 >= down2:
        r = (up2 / down2) if down2 > 0 else 99.0
        lsr_str = f"{r:.1f}:1 (SA)"
        lsr_val = r
    else:
        r = (down2 / up2) if up2 > 0 else 99.0
        lsr_str = f"{r:.1f}:1 (LB)"
        lsr_val = r
        
    ctx = nar.get('context', {})
    price = float(ctx.get('price') or 0)
    z = float(ctx.get('vwapZ') or 0)
    regime = nar.get('regime', 'n/a')
    direction = nar.get('direction', 'n/a')
    grade = nar.get('grade', 'n/a')
    conf = int(nar.get('confidence') or 0)
    m1 = nar.get('m1', {}).get('status', 'OFF')
    m2 = nar.get('m2', {}).get('status', 'OFF')
    m_status = f"M1:{m1}" if m1 != 'OFF' else (f"M2:{m2}" if m2 != 'OFF' else "OFF")
    
    contract = delta_contracts.get(sym)
    tick = delta_tickers.get(sym) or {}
    quotes = tick.get('quotes', {})
    mark = float(tick.get('mark_price') or 0)
    best_bid = float(quotes.get('best_bid') or 0)
    best_ask = float(quotes.get('best_ask') or 0)
    spread = best_ask - best_bid if (best_ask and best_bid) else 0
    spread_pct = (spread / mark * 100) if mark > 0 else 0
    
    delta_sym = contract['symbol'] if contract else None
    delta_str = f"{delta_sym} ({spread_pct:.4f}%)" if delta_sym else "NOT LISTED"
    
    vetoes = nar.get('plan', {}).get('vetoes', [])
    veto_str = vetoes[0] if vetoes else "None"
    
    qual = (grade in ['A', 'A+']) or (conf >= 80 and m1 == 'TRIGGERED') or (lsr_val >= 2.5) or (sym in ['BTC', 'ETH', 'SOL'])
    if qual:
        qualifiers.append(sym)
    
    print(f"{sym:10} | ${price:<10.4f} | {regime:<13} | {direction:<5} | {grade:<2} | {conf:<2}% | {m_status:<15} | {z:>+5.2f}σ | {lsr_str:<12} | {delta_str:<22} | {qual}")

print(f"\nTotal qualifiers: {len(qualifiers)}")
print("Qualifiers:", qualifiers)
