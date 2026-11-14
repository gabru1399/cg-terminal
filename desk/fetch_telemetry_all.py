import urllib.request
import json
import time

curated_crypto = [
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC',
    'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR',
    'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB'
]

def fetch_json(url, retries=3, delay=0.5):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            if i == retries - 1:
                return {'error': str(e)}
            time.sleep(delay)
    return {'error': 'failed'}

print("1. Fetching Delta Exchange products...")
p_data = fetch_json('https://api.india.delta.exchange/v2/products')
delta_products = {p['symbol']: p for p in p_data.get('result', []) if p.get('contract_type') == 'perpetual_futures'}

print("2. Fetching Delta Exchange tickers...")
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

print("3. Sweeping terminal endpoints for all 30 crypto assets...")
telemetry = {}

for sym in curated_crypto:
    print(f"Sweeping {sym}...")
    t = {}
    t['narrative'] = fetch_json(f'http://127.0.0.1:3000/api/cg/narrative?sym={sym}')
    t['market'] = fetch_json(f'http://127.0.0.1:3000/api/cg/market?symbol={sym}')
    t['signals'] = fetch_json(f'http://127.0.0.1:3000/api/cg/signals?symbol={sym}')
    t['cvd'] = fetch_json(f'http://127.0.0.1:3000/api/cg/cvd?sym={sym}')
    t['bookwalls'] = fetch_json(f'http://127.0.0.1:3000/api/cg/bookwalls?symbol={sym}')
    t['liqlevels'] = fetch_json(f'http://127.0.0.1:3000/api/cg/liqlevels?symbol={sym}')
    t['options'] = fetch_json(f'http://127.0.0.1:3000/api/cg/options?symbol={sym}')
    
    # Delta Exchange L2 Orderbook
    contract = delta_contracts.get(sym)
    if contract:
        dsym = contract['symbol']
        t['delta_l2'] = fetch_json(f'https://api.india.delta.exchange/v2/l2orderbook/{dsym}')
        t['delta_ticker'] = delta_tickers.get(dsym)
    else:
        t['delta_l2'] = None
        t['delta_ticker'] = None
        
    telemetry[sym] = t

# Save full sweep cache
with open('desk/crypto_full_telemetry.json', 'w') as f:
    json.dump({
        'timestamp': time.time(),
        'delta_contracts': delta_contracts,
        'telemetry': telemetry
    }, f)

print("Full telemetry sweep finished and saved to desk/crypto_full_telemetry.json")
