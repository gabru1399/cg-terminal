import json

data = json.load(open('C:/Users/SIGMA/.gemini/antigravity/brain/566267b2-a02c-4896-b021-b1e756f57654/.system_generated/steps/15141/output.txt', encoding='utf-8'))
prods = data.get('result', [])
for p in prods:
    sym = p.get('symbol', '')
    print(f"ID: {p['id']} | Sym: {sym} | Type: {p.get('contract_type')} | ContVal: {p.get('contract_value')}")
