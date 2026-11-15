import json

with open(r'C:\Users\SIGMA\.gemini\antigravity\brain\566267b2-a02c-4896-b021-b1e756f57654\.system_generated\steps\11595\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

perps = data.get('result', [])
print(f'Total perps found: {len(perps)}')

targets = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC', 'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR', 'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB']

found = {}
for p in perps:
    sym = p.get('symbol', '')
    for t in targets:
        # Match symbol formats
        if sym.upper() in [f'{t}USD', f'{t}USDT', f'{t}_USDT', f'{t}PERP', f'{t}-PERP']:
            found[t] = {
                'id': p.get('id'),
                'symbol': sym,
                'contract_value': p.get('contract_value'),
                'contract_unit': p.get('contract_unit_currency'),
                'tick_size': p.get('tick_size'),
                'quoting_asset': p.get('quoting_asset', {}).get('symbol')
            }

print(f'Matched {len(found)} of {len(targets)} targets')
for t in targets:
    if t in found:
        print(f"{t}: id={found[t]['id']} sym={found[t]['symbol']} cv={found[t]['contract_value']} tick={found[t]['tick_size']}")
    else:
        print(f'{t}: NOT FOUND')
