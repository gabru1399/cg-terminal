import urllib.request
import json
import time
from concurrent.futures import ThreadPoolExecutor

curated_crypto = [
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC',
    'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR',
    'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB'
]

sectors = {
    'BTC': 'Store of Value', 'ETH': 'Smart Contract L1', 'BNB': 'Exchange Token',
    'SOL': 'Smart Contract L1', 'XRP': 'Payments', 'ADA': 'Smart Contract L1',
    'DOGE': 'Meme', 'TRX': 'Smart Contract L1', 'LINK': 'Oracle', 'LTC': 'Payments',
    'AVAX': 'Smart Contract L1', 'DOT': 'Interoperability', 'NEAR': 'Smart Contract L1',
    'UNI': 'DeFi DEX', 'ATOM': 'Interoperability', 'XLM': 'Payments', 'ETC': 'Smart Contract L1',
    'FIL': 'Storage', 'ICP': 'Smart Contract L1', 'HBAR': 'Enterprise L1', 'APT': 'Smart Contract L1',
    'ARB': 'Ethereum L2', 'OP': 'Ethereum L2', 'SUI': 'Smart Contract L1', 'SEI': 'Smart Contract L1',
    'INJ': 'DeFi L1', 'TIA': 'Modular DA', 'VET': 'Supply Chain', '1000PEPE': 'Meme', '1000SHIB': 'Meme'
}

def fetch_json(url, timeout=4):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {'error': str(e)}

print("Fetching Delta products & tickers...", flush=True)
p_data = fetch_json('https://api.india.delta.exchange/v2/products')
delta_products = {p['symbol']: p for p in p_data.get('result', []) if p.get('contract_type') == 'perpetual_futures'}

t_data = fetch_json('https://api.india.delta.exchange/v2/tickers')
delta_tickers = {t['symbol']: t for t in t_data.get('result', [])}

delta_contracts = {}
for sym in curated_crypto:
    clean_sym = sym.replace('1000', '')
    candidates = [f'{sym}USD', f'{sym}USDT', f'{clean_sym}USD', f'{clean_sym}USDT', f'1000{clean_sym}USD']
    matched = None
    for c in candidates:
        if c in delta_products:
            matched = delta_products[c]
            break
    delta_contracts[sym] = matched

print(f"Mapped {sum(1 for v in delta_contracts.values() if v)} Delta contracts.", flush=True)

def fetch_asset_bundle(sym):
    endpoints = {
        'narrative': f'http://127.0.0.1:3000/api/cg/narrative?sym={sym}',
        'market': f'http://127.0.0.1:3000/api/cg/market?sym={sym}',
        'signals': f'http://127.0.0.1:3000/api/cg/signals?sym={sym}',
        'cvd': f'http://127.0.0.1:3000/api/cg/cvd?sym={sym}',
        'bookwalls': f'http://127.0.0.1:3000/api/cg/bookwalls?sym={sym}',
        'liqlevels': f'http://127.0.0.1:3000/api/cg/liqlevels?sym={sym}',
        'options': f'http://127.0.0.1:3000/api/cg/options?sym={sym}',
    }
    res = {}
    for k, url in endpoints.items():
        res[k] = fetch_json(url)
        
    contract = delta_contracts.get(sym)
    if contract:
        dsym = contract['symbol']
        res['delta_l2'] = fetch_json(f'https://api.india.delta.exchange/v2/l2orderbook/{dsym}')
        res['delta_ticker'] = delta_tickers.get(dsym)
    else:
        res['delta_l2'] = None
        res['delta_ticker'] = None
    return sym, res

print("Fetching telemetry for all 30 assets in parallel...", flush=True)
all_data = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    futures = [ex.submit(fetch_asset_bundle, sym) for sym in curated_crypto]
    for fut in futures:
        sym, data = fut.result()
        all_data[sym] = data
        print(f"Loaded {sym}", flush=True)

# Save intermediate cache
with open('desk/crypto_telemetry_bundle.json', 'w') as f:
    json.dump({'timestamp': time.time(), 'delta_contracts': delta_contracts, 'all_data': all_data}, f)

print("Saved telemetry bundle.", flush=True)
