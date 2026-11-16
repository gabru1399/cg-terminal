import json

data = json.load(open('C:/Users/SIGMA/.gemini/antigravity/brain/566267b2-a02c-4896-b021-b1e756f57654/.system_generated/steps/15809/output.txt', encoding='utf-8'))
prods = data.get('result', [])
perps = [p for p in prods if p.get('contract_type') == 'perpetual_futures']
print(f"Total Delta Perps: {len(perps)}")
for p in sorted(perps, key=lambda x: x['symbol']):
    sym = p['symbol']
    pid = p['id']
    tick = p.get('tick_size')
    val = p.get('contract_value')
    quoting = p.get('quoting_asset', {}).get('symbol')
    print(f"{sym:<14} | ID: {pid:<6} | Tick: {str(tick):<8} | Val: {str(val):<6} | Quoting: {quoting}")
