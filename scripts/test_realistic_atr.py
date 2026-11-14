import os
import pandas as pd
import numpy as np

DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"

def calculate_ema(series, span):
    return series.ewm(span=span, adjust=False).mean().to_numpy()

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

def backtest_realistic(csv_path, ribbon=(34, 89, 233), exit_model='canonical_scaleout'):
    df = pd.read_csv(csv_path)
    if len(df) < 300:
        return None
        
    opens = df['open'].to_numpy(dtype=float)
    highs = df['high'].to_numpy(dtype=float)
    lows = df['low'].to_numpy(dtype=float)
    closes = df['close'].to_numpy(dtype=float)
    atr = calculate_atr(df, 14)
    n = len(closes)
    
    fast_s, mid_s, slow_s = ribbon
    ema_fast = calculate_ema(df['close'], fast_s)
    ema_mid = calculate_ema(df['close'], mid_s)
    ema_slow = calculate_ema(df['close'], slow_s)
    ema_55 = calculate_ema(df['close'], 55)
    ema_89 = calculate_ema(df['close'], 89)
    
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
        curr_atr = atr[i]
        
        if in_pos:
            r_mult = 0.0
            closed = False
            
            if pos_side == 1:
                if h > highest_p:
                    highest_p = h
                
                # Canonical Breakeven: move to entry when >= +1.0R
                if not be_triggered and (highest_p - entry_p) >= init_risk:
                    stop_p = entry_p
                    be_triggered = True
                    
                # Stop hit
                if l <= stop_p:
                    exit_p = min(o, stop_p) if o < stop_p else stop_p
                    r_mult = (exit_p - entry_p) / init_risk
                    closed = True
                else:
                    if exit_model == 'trail_ema89':
                        if c < ema_89[i]:
                            r_mult = (c - entry_p) / init_risk
                            closed = True
                    elif exit_model == 'trail_ema55':
                        if c < ema_55[i]:
                            r_mult = (c - entry_p) / init_risk
                            closed = True
                    elif exit_model == 'canonical_scaleout':
                        # 40% @ 1.5R, 40% @ 2.5R, 20% runner trailing EMA 55
                        # If reached 1.5R and then stopped at BE: locked 0.4 * 1.5 = +0.6R
                        # If reached 2.5R: locked 0.4*1.5 + 0.4*2.5 = +1.6R
                        if highest_p >= entry_p + (2.5 * init_risk):
                            if c < ema_55[i] or l <= entry_p + (1.5 * init_risk):
                                exit_runner = max(l, entry_p + (1.5 * init_risk)) if l <= entry_p + (1.5 * init_risk) else c
                                runner_r = (exit_runner - entry_p) / init_risk
                                r_mult = (0.4 * 1.5) + (0.4 * 2.5) + (0.2 * runner_r)
                                closed = True
                        elif highest_p >= entry_p + (1.5 * init_risk):
                            if l <= stop_p: # stopped out at BE
                                r_mult = 0.4 * 1.5 # +0.6R profit on first target
                                closed = True
                            elif c < ema_55[i]:
                                r_mult = (0.4 * 1.5) + (0.6 * ((c - entry_p) / init_risk))
                                closed = True
                        elif c < ema_89[i]:
                            r_mult = (c - entry_p) / init_risk
                            closed = True
                            
            elif pos_side == -1:
                if l < lowest_p:
                    lowest_p = l
                    
                if not be_triggered and (entry_p - lowest_p) >= init_risk:
                    stop_p = entry_p
                    be_triggered = True
                    
                if h >= stop_p:
                    exit_p = max(o, stop_p) if o > stop_p else stop_p
                    r_mult = (entry_p - exit_p) / init_risk
                    closed = True
                else:
                    if exit_model == 'trail_ema89':
                        if c > ema_89[i]:
                            r_mult = (entry_p - c) / init_risk
                            closed = True
                    elif exit_model == 'trail_ema55':
                        if c > ema_55[i]:
                            r_mult = (entry_p - c) / init_risk
                            closed = True
                    elif exit_model == 'canonical_scaleout':
                        if lowest_p <= entry_p - (2.5 * init_risk):
                            if c > ema_55[i] or h >= entry_p - (1.5 * init_risk):
                                exit_runner = min(h, entry_p - (1.5 * init_risk)) if h >= entry_p - (1.5 * init_risk) else c
                                runner_r = (entry_p - exit_runner) / init_risk
                                r_mult = (0.4 * 1.5) + (0.4 * 2.5) + (0.2 * runner_r)
                                closed = True
                        elif lowest_p <= entry_p - (1.5 * init_risk):
                            if h >= stop_p:
                                r_mult = 0.4 * 1.5
                                closed = True
                            elif c > ema_55[i]:
                                r_mult = (0.4 * 1.5) + (0.6 * ((entry_p - c) / init_risk))
                                closed = True
                        elif c > ema_89[i]:
                            r_mult = (entry_p - c) / init_risk
                            closed = True
                            
            if closed:
                trades.append(r_mult)
                in_pos = False
                continue

        if not in_pos:
            rng = h - l
            if rng <= 0:
                continue
                
            # Realistic minimum stop buffer: max(0.15 * range, 0.5 * ATR, 0.005 * price)
            min_stop_buf = max(0.15 * rng, 0.5 * curr_atr, 0.005 * c)
            
            if ema_fast[i] > ema_mid[i] > ema_slow[i]:
                if l <= ema_fast[i] and c > ema_mid[i]:
                    lower_wick = min(o, c) - l
                    if (lower_wick / rng) >= 0.25 and c > o:
                        in_pos = True
                        pos_side = 1
                        entry_p = c
                        stop_p = min(l - (0.1 * rng), entry_p - min_stop_buf)
                        init_risk = entry_p - stop_p
                        if init_risk <= 0:
                            in_pos = False
                            continue
                        highest_p = h
                        be_triggered = False
            elif ema_fast[i] < ema_mid[i] < ema_slow[i]:
                if h >= ema_fast[i] and c < ema_mid[i]:
                    upper_wick = h - max(o, c)
                    if (upper_wick / rng) >= 0.25 and c < o:
                        in_pos = True
                        pos_side = -1
                        entry_p = c
                        stop_p = max(h + (0.1 * rng), entry_p + min_stop_buf)
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
    losses = trades[trades < 0]
    bes = trades[trades == 0]
    
    win_rate = len(wins) / len(trades) * 100.0
    be_rate = len(bes) / len(trades) * 100.0
    loss_rate = len(losses) / len(trades) * 100.0
    
    gross_g = wins.sum() if len(wins) > 0 else 0
    gross_l = abs(losses.sum()) if len(losses) > 0 else 0.0001
    pf = gross_g / gross_l
    net_r = trades.sum()
    
    cum_r = np.cumsum(trades)
    max_dd = np.max(np.maximum.accumulate(cum_r) - cum_r)
    
    return {
        'trades': len(trades),
        'win_rate': win_rate,
        'be_rate': be_rate,
        'loss_rate': loss_rate,
        'profit_factor': pf,
        'net_r': net_r,
        'max_dd': max_dd,
        'avg_win_r': wins.mean() if len(wins) > 0 else 0,
        'avg_loss_r': losses.mean() if len(losses) > 0 else 0
    }

def main():
    best_df = pd.read_csv(os.path.join(DELTA_DIR, "delta_best_per_asset.csv"))
    pos_df = best_df[best_df['net_r'] > 0].copy()
    b20 = pos_df.head(20)
    
    print("=" * 110)
    print("REALISTIC ATR-BUFFERED CANONICAL SCALEOUT VS TRAILING EXITS")
    print("=" * 110)
    print(f"{'Exit Model':<25} | {'Trades':<7} | {'Win %':<6} | {'BE %':<6} | {'Loss %':<7} | {'Avg Win':<8} | {'Avg Loss':<8} | {'PF':<6} | {'Net R'}")
    print("-" * 110)
    
    for model in ['canonical_scaleout', 'trail_ema55', 'trail_ema89']:
        tot_t = 0
        tot_w = 0
        tot_be = 0
        tot_l = 0
        tot_net = 0.0
        tot_gw = 0.0
        tot_gl = 0.0
        
        for _, row in b20.iterrows():
            fpath = os.path.join(DELTA_DIR, f"{row['symbol']}_{row['timeframe'].lower()}.csv")
            res = backtest_realistic(fpath, ribbon=(34, 89, 233), exit_model=model)
            if res:
                tot_t += res['trades']
                tot_w += int(res['trades'] * (res['win_rate'] / 100.0))
                tot_be += int(res['trades'] * (res['be_rate'] / 100.0))
                tot_l += int(res['trades'] * (res['loss_rate'] / 100.0))
                tot_net += res['net_r']
                tot_gw += res['avg_win_r'] * (res['win_rate'] / 100.0 * res['trades'])
                tot_gl += abs(res['avg_loss_r']) * (res['loss_rate'] / 100.0 * res['trades'])
                
        wr = tot_w / max(1, tot_t) * 100.0
        ber = tot_be / max(1, tot_t) * 100.0
        lr = tot_l / max(1, tot_t) * 100.0
        pf = tot_gw / max(0.001, tot_gl)
        avg_w = tot_gw / max(1, tot_w)
        avg_l = tot_gl / max(1, tot_l)
        
        print(f"{model:<25} | {tot_t:<7} | {wr:<6.1f} | {ber:<6.1f} | {lr:<7.1f} | {avg_w:<8.2f} | {avg_l:<8.2f} | {pf:<6.2f} | {tot_net:<10.1f}")

if __name__ == '__main__':
    main()
