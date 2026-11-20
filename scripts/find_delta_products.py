import json

p = json.load(open('data/round-evidence/R646/raw/delta-inventory-all-all-5871322280f9c2cf.json'))
products = []
for page in p.get('pages', []):
    res = page.get('result', [])
    products.extend(res)

print(f"Total delta products extracted: {len(products)}")

check_syms = ['BERAUSD', 'ENAUSD', 'ARBUSD', 'BNBUSD', 'BTCUSD', 'ETHUSD', 'SOLUSD', 'TIAUSD', 'ADAUSD', 'SEIUSD', 'DOTUSD', 'TRXUSD']
for s in check_syms:
    matches = [x for x in products if x.get('symbol') == s]
    if matches:
        item = matches[0]
        print(f"{s:<10} | id={item.get('id')} | type={item.get('contract_type')} | tick={item.get('tick_size')} | contract_val={item.get('contract_value')} | max_leverage={item.get('max_leverage_notional')}")
    else:
        print(f"{s:<10} | NOT FOUND")
