import os
import time
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

DATA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Fibonacci_Institutional_Business\data"
os.makedirs(DATA_DIR, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def get_all_delta_perpetual_symbols():
    url = "https://api.india.delta.exchange/v2/products"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    products = data.get('result', [])
    perps = [p['symbol'] for p in products if p.get('contract_type') == 'perpetual_futures']
    return sorted(list(set(perps)))

def fetch_delta_candles(symbol, resolution, start_ts, end_ts):
    all_candles = []
    curr_to = end_ts
    
    # Paginate up to 6 pages (~24,000 candles)
    for _ in range(6):
        url = f"https://api.india.delta.exchange/v2/chart/history?symbol={symbol}&resolution={resolution}&from={start_ts}&to={curr_to}"
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            result = data.get('result', {})
            t = result.get('t', [])
            if not t or len(t) == 0:
                break
            
            o = result.get('o', [])
            h = result.get('h', [])
            l = result.get('l', [])
            c = result.get('c', [])
            v = result.get('v', [])
            
            batch = list(zip(t, o, h, l, c, v))
            all_candles = batch + all_candles
            
            if t[0] <= start_ts or len(t) < 50:
                break
            curr_to = t[0] - 1
            time.sleep(0.05)
        except Exception:
            break
            
    if not all_candles:
        return None
        
    df = pd.DataFrame(all_candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df = df.drop_duplicates(subset=['timestamp']).sort_values('timestamp').reset_index(drop=True)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df[['timestamp', 'datetime', 'open', 'high', 'low', 'close', 'volume']]
    return df

def download_symbol(sym, start_ts, now_ts):
    res_dict = {}
    for r_label, r_code in [('1h', '60'), ('4h', '240')]:
        target_f = os.path.join(DATA_DIR, f"{sym}_{r_label}.csv")
        # Check if already downloaded in Delta_Exchange folder to save time
        alt_f = os.path.join(r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange", f"{sym}_{r_label}.csv")
        if os.path.exists(alt_f):
            # Copy over
            df = pd.read_csv(alt_f)
            df.to_csv(target_f, index=False)
            res_dict[r_label] = len(df)
            continue
            
        df = fetch_delta_candles(sym, r_code, start_ts, now_ts)
        if df is not None and len(df) > 100:
            df.to_csv(target_f, index=False)
            res_dict[r_label] = len(df)
    return sym, res_dict

def main():
    symbols = get_all_delta_perpetual_symbols()
    print(f"Discovered {len(symbols)} perpetual contracts on Delta Exchange India.")
    
    now_ts = int(time.time())
    start_ts = int(time.mktime(time.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")))
    
    print("Downloading historical candles for all perpetuals with 12 workers...")
    successful = 0
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(download_symbol, s, start_ts, now_ts): s for s in symbols}
        for fut in as_completed(futures):
            sym, res = fut.result()
            if res:
                successful += 1
                counts = ", ".join([f"{k}: {v}" for k, v in res.items()])
                print(f"  [+] {sym:<14} -> {counts}")
            else:
                pass
                
    print(f"\nCompleted: {successful}/{len(symbols)} assets saved in {DATA_DIR}")

if __name__ == '__main__':
    main()
