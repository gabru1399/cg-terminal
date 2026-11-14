import os
import time
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from datetime import datetime

DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"
MT5_DIR = os.path.join(DELTA_DIR, "MT5_Broker_Assets")

os.makedirs(DELTA_DIR, exist_ok=True)
os.makedirs(MT5_DIR, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_delta_candles(symbol, resolution, start_ts, end_ts):
    """Fetch paginated candles from Delta Exchange India."""
    all_candles = []
    curr_to = end_ts
    
    # Paginate up to 10 pages (~40,000 candles)
    for _ in range(10):
        url = f"https://api.india.delta.exchange/v2/chart/history?symbol={symbol}&resolution={resolution}&from={start_ts}&to={curr_to}"
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
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
            
            # Combine
            batch = list(zip(t, o, h, l, c, v))
            all_candles = batch + all_candles
            
            if t[0] <= start_ts or len(t) < 50:
                break
            curr_to = t[0] - 1
            time.sleep(0.1)
        except Exception as e:
            # print(f"Error fetching {symbol} {resolution}: {e}")
            break
            
    if not all_candles:
        return None
        
    # Deduplicate by timestamp
    df = pd.DataFrame(all_candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df = df.drop_duplicates(subset=['timestamp']).sort_values('timestamp').reset_index(drop=True)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df[['timestamp', 'datetime', 'open', 'high', 'low', 'close', 'volume']]
    return df

def download_delta_symbol(symbol, start_ts, end_ts):
    results = {}
    for res_name, res_code in [('1h', '60'), ('4h', '240')]:
        df = fetch_delta_candles(symbol, res_code, start_ts, end_ts)
        if df is not None and len(df) > 100:
            csv_path = os.path.join(DELTA_DIR, f"{symbol}_{res_name}.csv")
            df.to_csv(csv_path, index=False)
            results[res_name] = len(df)
    return symbol, results

def get_top_delta_symbols():
    url = 'https://api.india.delta.exchange/v2/tickers'
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    tickers = data.get('result', [])
    perps = [t for t in tickers if t.get('contract_type') == 'perpetual_futures']
    
    # Filter active perps with turnover > $10,000
    active = [t for t in perps if float(t.get('turnover_usd') or 0) > 10000]
    active.sort(key=lambda x: float(x.get('turnover_usd') or 0), reverse=True)
    
    # Priority universe: Top 60 symbols
    top_syms = [t['symbol'] for t in active[:60]]
    # Ensure key majors and tradfi perps are included
    must_have = [
        'BTCUSD', 'ETHUSD', 'SOLUSD', 'XRPUSD', 'DOGEUSD', 'BNBUSD', 'SUIUSD', 'LINKUSD',
        'LTCUSD', 'AVAXUSD', 'NEARUSD', 'ADAUSD', 'INJUSD', 'DOTUSD', 'BCHUSD', 'AAVEUSD',
        'UNIUSD', 'HYPEUSD', 'ARBUSD', 'OPUSD', 'TIAUSD', 'SEIUSD', '1000PEPEUSD',
        'XAUTUSD', 'PAXGUSD', 'SLVONUSD', 'NVDAXUSD', 'QQQXUSD', 'OILUSD', 'MUBUSD', 'SOXLBUSD'
    ]
    all_syms = list(dict.fromkeys(top_syms + [s for s in must_have if any(t['symbol'] == s for t in perps)]))
    return all_syms

def dump_mt5_assets():
    import MetaTrader5 as mt5
    if not mt5.initialize():
        print("Failed to initialize MT5")
        return 0
    symbols = mt5.symbols_get()
    print(f"Dumping {len(symbols)} MT5 symbols to {MT5_DIR}...")
    saved = 0
    for s in symbols:
        name = s.name
        # 1H
        rates_1h = mt5.copy_rates_from_pos(name, mt5.TIMEFRAME_H1, 0, 5000)
        if rates_1h is not None and len(rates_1h) > 50:
            df = pd.DataFrame(rates_1h)
            df['datetime'] = pd.to_datetime(df['time'], unit='s')
            df.rename(columns={'time': 'timestamp'}, inplace=True)
            df = df[['timestamp', 'datetime', 'open', 'high', 'low', 'close', 'tick_volume']]
            df.to_csv(os.path.join(MT5_DIR, f"{name}_1h.csv"), index=False)
            saved += 1
    mt5.shutdown()
    return saved

def main():
    print(f"Target Delta Directory: {DELTA_DIR}")
    print(f"Target MT5 Directory:   {MT5_DIR}")
    
    # 1. Fetch Delta symbols
    delta_symbols = get_top_delta_symbols()
    print(f"Selected {len(delta_symbols)} top liquid Delta Exchange assets for download.")
    
    now = int(time.time())
    start_ts = int(time.mktime(time.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")))
    
    print("Starting multithreaded download of Delta Exchange candles (1H & 4H)...")
    downloaded = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download_delta_symbol, sym, start_ts, now): sym for sym in delta_symbols}
        for fut in as_completed(futures):
            sym, res = fut.result()
            if res:
                downloaded += 1
                counts = ", ".join([f"{k}: {v} bars" for k, v in res.items()])
                print(f"  [+] {sym:<12} -> {counts}")
            else:
                print(f"  [-] {sym:<12} -> No candle data returned")
                
    print(f"\nDelta Exchange Download Complete: {downloaded}/{len(delta_symbols)} assets saved to {DELTA_DIR}")
    
    # 2. Dump MT5 assets
    mt5_saved = dump_mt5_assets()
    print(f"MT5 Dump Complete: {mt5_saved} symbols saved to {MT5_DIR}")

if __name__ == '__main__':
    main()
