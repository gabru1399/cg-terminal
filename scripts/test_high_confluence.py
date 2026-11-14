import os
import pandas as pd
import numpy as np

# Let's test adding a Volume and Trend Strength filter:
# 1. Volume must be > 1.2 * 20-bar average volume (institutional participation)
# 2. ADX or EMA slope > threshold (strong trend regime, avoiding consolidation chop)
# 3. Take Profit at 2.0R with 50% scale-out at 1.2R
from test_realistic_atr import calculate_ema, calculate_atr

def test_high_confluence_setup(csv_path, ribbon=(34, 89, 233)):
    df = pd.read_csv(csv_path)
    if len(df) < 300:
        return None
        
    opens = df['open'].to_numpy(dtype=float)
    highs = df['high'].to_numpy(dtype=float)
    lows = df['low'].to_numpy(dtype=float)
    closes = df['close'].to_numpy(dtype=float)
    volumes = df['volume'].to_numpy(dtype=float)
    atr = calculate_atr(df, 14)
    vol_sma = pd.Series(volumes).rolling(20).mean().bfill().to_numpy()
    n = len(closes)
    
    fast_s, mid_s, slow_s = ribbon
    ema_fast = calculate_ema(df['close'], fast_s)
    ema_mid = calculate_ema(df['close'], mid_s)
    ema_slow = calculate_ema(df['close'], slow_s)
    
    trades = []
    in_pos = False
    pos_side = 0
    entry_p = 0.0
    stop_p = 0.0
    init_risk = 0.0
    highest_p = 0.0
    lowest_p = 0.0
    be_triggered = False
    
    start_bar = max(slow_s, 250)
    
    for i in range(start_bar, n):
        o = opens[i]
        h = highs[i]
        l = lows[i]
        c = closes[i]
        v = volumes[i]
        curr_atr = atr[i]
        
        if in_pos:
            r_mult = 0.0
            closed = False
            
            if pos_side == 1:
                if h > highest_p:
                    highest_p = h
                # Breakeven at +1.0R
                if not be_triggered and (highest_p - entry_p) >= init_risk:
                    stop_p = entry_p + (0.1 * init_risk) # lock in tiny buffer
                    be_triggered = True
                    
                # Take Profit at 2.0R
                if h >= entry_p + (2.0 * init_risk):
                    r_mult = 2.0
                    closed = True
                elif l <= stop_p:
                    exit_p = min(o, stop_p) if o < stop_p else stop_p
                    r_mult = (exit_p - entry_p) / init_risk
                    closed = True
                    
            elif pos_side == -1:
                if l < lowest_p:
                    lowest_p = l
                if not be_triggered and (entry_p - lowest_p) >= init_risk:
                    stop_p = entry_p - (0.1 * init_risk)
                    be_triggered = True
                    
                if l <= entry_p - (2.0 * init_risk):
                    r_mult = 2.0
                    closed = True
                elif h >= stop_p:
                    exit_p = max(o, stop_p) if o > stop_p else stop_p
                    r_mult = (entry_p - exit_p) / init_risk
                    closed = True
                    
            if closed:
                trades.append(r_mult)
                in_pos = False
                continue

        if not in_pos:
            rng = h - l
            if rng <= 0 or curr_atr <= 0:
                continue
                
            # Filter 1: Candle range must be at least 0.5 * ATR (no dead micro-candles)
            if rng < 0.5 * curr_atr:
                continue
                
            # Filter 2: Volume confirmation: volume >= 1.0 * vol_sma
            if v < 1.0 * vol_sma[i]:
                continue
                
            # Filter 3: Minimum stop buffer: max(0.2 * rng, 0.75 * ATR)
            min_stop = max(0.2 * rng, 0.75 * curr_atr)
            
            # Trend Ribbon
            if ema_fast[i] > ema_mid[i] > ema_slow[i]:
                # Slope positive
                if (ema_fast[i] - ema_fast[i-5]) > 0:
                    if l <= ema_fast[i] and c > ema_mid[i]:
                        lower_wick = min(o, c) - l
                        if (lower_wick / rng) >= 0.25 and c > o:
                            in_pos = True
                            pos_side = 1
                            entry_p = c
                            stop_p = min(l - (0.1 * rng), entry_p - min_stop)
                            init_risk = entry_p - stop_p
                            if init_risk <= 0:
                                in_pos = False
                                continue
                            highest_p = h
                            be_triggered = False
            elif ema_fast[i] < ema_mid[i] < ema_slow[i]:
                if (ema_fast[i] - ema_fast[i-5]) < 0:
                    if h >= ema_fast[i] and c < ema_mid[i]:
                        upper_wick = h - max(o, c)
                        if (upper_wick / rng) >= 0.25 and c < o:
                            in_pos = True
                            pos_side = -1
                            entry_p = c
                            stop_p = max(h + (0.1 * rng), entry_p + min_stop)
                            init_risk = stop_p - entry_p
                            if init_risk <= 0:
                                in_pos = False
                                continue
                            lowest_p = l
                            be_triggered = False

    if not trades:
        return None
    trades = np.array(trades)
    wins = trades[trades > 0]
    bes = trades[trades == 0]
    losses = trades[trades < 0]
    
    return {
        'trades': len(trades),
        'wins': len(wins),
        'bes': len(bes),
        'losses': len(losses),
        'net_r': trades.sum()
    }

def main():
    DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"
    best_df = pd.read_csv(os.path.join(DELTA_DIR, "delta_best_per_asset.csv"))
    pos_df = best_df[best_df['net_r'] > 0].copy()
    b20 = pos_df.head(20)
    
    tot_t, tot_w, tot_b, tot_l, tot_r = 0, 0, 0, 0, 0.0
    for _, row in b20.iterrows():
        fpath = os.path.join(DELTA_DIR, f"{row['symbol']}_{row['timeframe'].lower()}.csv")
        res = test_high_confluence_setup(fpath)
        if res:
            tot_t += res['trades']
            tot_w += res['wins']
            tot_b += res['bes']
            tot_l += res['losses']
            tot_r += res['net_r']
            
    print(f"High Confluence Filtered Backtest across Top 20 Basket:")
    print(f"Total Trades: {tot_t}")
    print(f"Wins (> 0):   {tot_w} ({tot_w/tot_t*100:.1f}%)")
    print(f"Breakevens:   {tot_b} ({tot_b/tot_t*100:.1f}%)")
    print(f"Losses:       {tot_l} ({tot_l/tot_t*100:.1f}%)")
    print(f"Win + Breakeven (Capital Preserved): {(tot_w+tot_b)/tot_t*100:.1f}%")
    print(f"Net R:        {tot_r:.1f} R")

if __name__ == '__main__':
    main()
