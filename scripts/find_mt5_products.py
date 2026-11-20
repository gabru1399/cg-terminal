import json

p = json.load(open('data/round-evidence/R646/raw/mt5-inventory-all-all-02fd7296c9aa70a6.json'))
print("MT5 inventory payload type:", type(p))
if isinstance(p, dict):
    print("Keys:", p.keys())
    symbols = p.get('symbols', p.get('result', []))
elif isinstance(p, list):
    symbols = p
print(f"Total MT5 symbols: {len(symbols)}")
check = ['BTCUSD', 'ETHUSD', 'BNBUSD', 'SOLUSD', 'EURUSD', 'XAUUSD', 'XAGUSD', 'NDX100', 'SPX500']
for s in check:
    matches = [x for x in symbols if s in (x if isinstance(x, str) else x.get('name', ''))]
    print(f"{s:<10} matches in MT5: {matches[:3]}")
