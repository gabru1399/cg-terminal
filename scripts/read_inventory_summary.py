import json

with open("data/round-evidence/R794/raw/delta-inventory-all-all-284ed8125859a94c.json", encoding="utf-8") as f:
    d = json.load(f)

print("Delta keys:", list(d.keys()))
for k, v in d.items():
    if isinstance(v, list):
        print(f"  {k}: list of {len(v)}")
    elif isinstance(v, dict):
        print(f"  {k}: dict with keys {list(v.keys())}")
    else:
        print(f"  {k}: {type(v)}")

with open("data/round-evidence/R794/raw/mt5-inventory-all-all-02fd7296c9aa70a6.json", encoding="utf-8") as f:
    m = json.load(f)

print("\nMT5 keys:", list(m.keys()))
for k, v in m.items():
    if isinstance(v, list):
        print(f"  {k}: list of {len(v)}")
    elif isinstance(v, dict):
        print(f"  {k}: dict with keys {list(v.keys())}")
    else:
        print(f"  {k}: {type(v)}")
