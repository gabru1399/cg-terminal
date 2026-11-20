import json

with open('desk/deepscan/LATEST_16D_TELEMETRY.json') as f:
    d = json.load(f)

trx = d['assets']['TRX']
print("=== TRX TELEMETRY ===")
print("Price:", trx.get("price"))
for k, v in trx.get("dimensions", {}).items():
    print(f"[{k}] {v.get('name')}:")
    for subk, subv in v.items():
        if subk not in ['dimension', 'name']:
            print(f"    {subk}: {subv}")
