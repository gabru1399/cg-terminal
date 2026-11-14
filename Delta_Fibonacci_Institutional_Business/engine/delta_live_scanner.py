"""delta_live_scanner.py: Live Institutional Scanner for Delta Exchange India.
Scans the Curated Elite Wealth Basket for genuine Fibonacci Prime 89/233 Rejection Setups.
Strictly enforces the Macro Regime Gate (No counter-trend trades).
"""

import urllib.request
import json
import time
import pandas as pd
import numpy as np

DELTA_API = "https://api.india.delta.exchange"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def calculate_ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def calculate_atr(df, period=14):
    high = df['high'].to_numpy(dtype=float)
    low = df['low'].to_numpy(dtype=float)
    close = df['close'].to_numpy(dtype=float)
    n = len(df)
    tr = np.zeros(n)
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr[i] = max(high[i] - low[i], abs(high[i] - close[i-1]), abs(low[i] - close[i-1]))
    atr = pd.Series(tr).rolling(period).mean().bfill().to_numpy()
    return atr

def fetch_recent_candles(symbol, resolution="240", count=300):
    now = int(time.time())
    start = now - (count * 4 * 3600 if resolution == "240" else count * 3600)
    url = f"{DELTA_API}/v2/chart/history?symbol={symbol}&resolution={resolution}&from={start}&to={now}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        res = data.get('result', {})
        t = res.get('t', [])
        if not t or len(t) < 50:
            return None
        df = pd.DataFrame({
            'timestamp': t,
            'open': res.get('o', []),
            'high': res.get('h', []),
            'low': res.get('l', []),
            'close': res.get('c', []),
            'volume': res.get('v', [])
        })
        df = df.sort_values('timestamp').reset_index(drop=True)
        return df
    except Exception as e:
        return None

def scan_asset_setup(symbol, tf="4H", equity=5000.0, risk_pct=0.005):
    res_code = "240" if tf == "4H" else "60"
    df = fetch_recent_candles(symbol, resolution=res_code, count=300)
    if df is None or len(df) < 250:
        return None
        
    closes = df['close']
    ema89 = calculate_ema(closes, 89).to_numpy()
    ema233 = calculate_ema(closes, 233).to_numpy()
    atr = calculate_atr(df, 14)
    
    i = len(df) - 1 # Last closed bar or forming bar
    # Check prior closed bar for confirmed signal
    prev = i - 1
    
    o = df['open'].iloc[prev]
    h = df['high'].iloc[prev]
    l = df['low'].iloc[prev]
    c = df['close'].iloc[prev]
    rng = h - l
    if rng <= 0:
        return None
        
    curr_89 = ema89[prev]
    curr_233 = ema233[prev]
    curr_atr = atr[prev]
    
    # 1. Macro Regime Gate
    regime = "NEUTRAL"
    if curr_89 > curr_233:
        regime = "BULLISH" # LONGS ONLY
    elif curr_89 < curr_233:
        regime = "BEARISH" # SHORTS ONLY
        
    setup = None
    
    # Bullish setup check
    if regime == "BULLISH":
        # Price must touch or pierce EMA 89 or 233 from above
        if l <= curr_89 * 1.002 or l <= curr_233 * 1.002:
            if c > min(curr_89, curr_233):
                lower_wick = min(o, c) - l
                wick_ratio = lower_wick / rng
                if wick_ratio >= 0.25 and c > o:
                    entry = df['close'].iloc[i] # Current market price
                    stop = l - (0.3 * curr_atr)
                    risk_dist = entry - stop
                    if risk_dist > 0:
                        dollar_risk = equity * risk_pct
                        pos_size = dollar_risk / risk_dist
                        setup = {
                            'symbol': symbol,
                            'tf': tf,
                            'regime': regime,
                            'action': 'BUY / LONG',
                            'entry': entry,
                            'stop': stop,
                            'risk_distance': risk_dist,
                            't1': entry + (1.5 * risk_dist),
                            't2': entry + (2.5 * risk_dist),
                            't3': entry + (4.0 * risk_dist),
                            'rr': 2.5,
                            'position_size_units': pos_size,
                            'dollar_risk': dollar_risk,
                            'wick_pct': wick_ratio * 100.0,
                            'ema89': curr_89,
                            'ema233': curr_233
                        }
                        
    # Bearish setup check
    elif regime == "BEARISH":
        if h >= curr_89 * 0.998 or h >= curr_233 * 0.998:
            if c < max(curr_89, curr_233):
                upper_wick = h - max(o, c)
                wick_ratio = upper_wick / rng
                if wick_ratio >= 0.25 and c < o:
                    entry = df['close'].iloc[i]
                    stop = h + (0.3 * curr_atr)
                    risk_dist = stop - entry
                    if risk_dist > 0:
                        dollar_risk = equity * risk_pct
                        pos_size = dollar_risk / risk_dist
                        setup = {
                            'symbol': symbol,
                            'tf': tf,
                            'regime': regime,
                            'action': 'SELL / SHORT',
                            'entry': entry,
                            'stop': stop,
                            'risk_distance': risk_dist,
                            't1': entry - (1.5 * risk_dist),
                            't2': entry - (2.5 * risk_dist),
                            't3': entry - (4.0 * risk_dist),
                            'rr': 2.5,
                            'position_size_units': pos_size,
                            'dollar_risk': dollar_risk,
                            'wick_pct': wick_ratio * 100.0,
                            'ema89': curr_89,
                            'ema233': curr_233
                        }
                        
    return setup
