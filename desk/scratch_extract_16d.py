import json

with open('desk/deepscan/LATEST_16D_TELEMETRY.json') as f:
    d = json.load(f)

print(f"Total assets: {len(d.get('assets', {}))}")
print(f"Summary: {d.get('summary')}")

targets = ['BTC', 'ETH', 'TRX', 'SOL', 'ADA', 'BNB', 'GOOGL', 'SEI']
for sym in targets:
    item = d.get('assets', {}).get(sym)
    if not item:
        print(f"\n==========================================")
        print(f"=== {sym}: NOT IN DATASET ===")
        print(f"==========================================")
        continue
    dims = item.get('dimensions', {})
    d16 = dims.get('D16', {})
    print(f"\n==========================================")
    print(f"=== {sym} (Price: {item.get('price')}) ===")
    print(f"==========================================")
    print(f"  Score: {d16.get('composite_score')}, Grade: {d16.get('execution_grade')}, Bias: {d16.get('bias')}")
    print(f"  Vetoes: {d16.get('veto_reasons')}")
    for code in [f"D{i:02d}" for i in range(1, 17)]:
        dim_data = dims.get(code, {})
        print(f"  [{code}] {dim_data.get('name')}: pass={dim_data.get('pass')}")
        # print non-trivial items
        for k, v in dim_data.items():
            if k not in ['dimension', 'name', 'pass']:
                print(f"      {k}: {v}")
