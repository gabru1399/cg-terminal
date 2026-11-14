import urllib.request
import json
import time

curated_crypto = [
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC',
    'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR',
    'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB'
]

# 1. Pull Delta Exchange products to map contracts
print("Pulling Delta Exchange products...")
req_p = urllib.request.Request('https://api.india.delta.exchange/v2/products', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req_p, timeout=5) as resp:
        products = json.loads(resp.read().decode()).get('result', [])
        delta_perps = {p['symbol']: p for p in products if p.get('contract_type') == 'perpetual_futures'}
except Exception as e:
    print("Error fetching Delta products:", e)
    delta_perps = {}

# 2. Pull Delta Exchange tickers
print("Pulling Delta Exchange tickers...")
req_t = urllib.request.Request('https://api.india.delta.exchange/v2/tickers', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req_t, timeout=5) as resp:
        tickers = {t['symbol']: t for t in json.loads(resp.read().decode()).get('result', [])}
except Exception as e:
    print("Error fetching Delta tickers:", e)
    tickers = {}

# Map curated crypto to Delta symbol
delta_map = {}
for sym in curated_crypto:
    clean_sym = sym.replace('1000', '')
    candidates = [f'{sym}USD', f'{sym}USDT', f'{clean_sym}USD', f'{clean_sym}USDT', f'1000{clean_sym}USD']
    matched = None
    for c in candidates:
        if c in delta_perps:
            matched = delta_perps[c]
            break
    delta_map[sym] = matched

print(f"Mapped {sum(1 for v in delta_map.values() if v)} of {len(curated_crypto)} to Delta Exchange perps.")

# 3. Sweep all 30 crypto assets via narrative endpoint and liqlevels
narratives = {}
liqlevels = {}
markets = {}

for sym in curated_crypto:
    # Narrative
    url_n = f'http://127.0.0.1:3000/api/cg/narrative?sym={sym}'
    try:
        req = urllib.request.Request(url_n, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            narratives[sym] = json.loads(resp.read().decode())
    except Exception as e:
        narratives[sym] = {'error': str(e)}

    # Liqlevels
    url_l = f'http://127.0.0.1:3000/api/cg/liqlevels?symbol={sym}'
    try:
        req = urllib.request.Request(url_l, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            liqlevels[sym] = json.loads(resp.read().decode())
    except Exception as e:
        liqlevels[sym] = {'error': str(e)}

    # Market
    url_m = f'http://127.0.0.1:3000/api/cg/market?symbol={sym}'
    try:
        req = urllib.request.Request(url_m, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            markets[sym] = json.loads(resp.read().decode())
    except Exception as e:
        markets[sym] = {'error': str(e)}

# Save raw sweep to desk/crypto_raw_sweep.json
sweep_data = {
    'timestamp': time.time(),
    'narratives': narratives,
    'liqlevels': liqlevels,
    'markets': markets,
    'delta_map': {k: (v['symbol'] if v else None) for k, v in delta_map.items()},
    'delta_contracts': {k: v for k, v in delta_map.items() if v},
    'delta_tickers': {k: tickers.get(v['symbol']) for k, v in delta_map.items() if v and v['symbol'] in tickers}
}

with open('desk/crypto_raw_sweep.json', 'w') as f:
    json.dump(sweep_data, f, indent=2)

print("Sweep complete. Saved to desk/crypto_raw_sweep.json")
