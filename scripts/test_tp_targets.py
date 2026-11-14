import os
import pandas as pd
import numpy as np

DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"

def calculate_ema(series, span):
    return series.ewm(span=span, adjust=False).mean().to_numpy()

def backtest_tp_targets(csv_path, ribbon=(34, 89, 233), tp_mult=2.0, be_at=1.0):
    df = pd.read_csv(csv_path)
    if len(df) < 300:
        return None
        
    opens = df['open'].to_numpy(dtype=float)
    highs = df['high'].to_numpy(dtype=float)
    lows = df['low'].to_numpy(dtype=float)
    closes = df['close'].to_numpy(dtype=float)
    n = len(closes)
    
    fast_s, mid_s, slow_s = ribbon
    ema_fast = calculate_ema(df['close'], fast_s)
    ema_mid = calculate_ema(df['close'], mid_s)
    ema_slow = calculate_ema(df['close'], slow_s)
    
    trades = []
    in_pos = False
    pos_side = 0
    entry_idx = 0
    entry_p = 0.0
    stop_p = 0.0
    target_p = 0.0
    initial_risk = 0.0
    highest_p = 0.0
    lowest_p = 0.0
    be_triggered = False
    
    start_bar = max(slow_s, 250)
    
    for i in range(start_bar, n):
        o = opens[i]
        h = highs[i]
        l = lows[i]
        c = closes[i]
        
        if in_pos:
            r_mult = 0.0
            closed = False
            
            if pos_side == 1:
                if h > highest_p:
                    highest_p = h
                # Breakeven
                if not be_triggered and be_at is not None and (highest_p - entry_p) >= (be_at * initial_risk):
                    stop_p = entry_p
                    be_triggered = True
                # Target check
                if h >= target_p:
                    exit_p = target_p
                    r_mult = tp_mult
                    closed = True
                elif l <= stop_p:
                    exit_p = min(o, stop_p) if o < stop_p else stop_p
                    r_mult = (exit_p - entry_p) / initial_risk
                    closed = True
            elif pos_side == -1:
                if l < lowest_p:
                    lowest_p = l
                # Breakeven
                if not be_triggered and be_at is not None and (entry_p - lowest_p) >= (be_at * initial_risk):
                    stop_p = entry_p
                    be_triggered = True
                # Target check
                if l <= target_p:
                    exit_p = target_p
                    r_mult = tp_mult
                    closed = True
                elif h >= stop_p:
                    exit_p = max(o, stop_p) if o > stop_p else stop_p
                    r_mult = (entry_p - exit_p) / initial_risk
                    closed = True
                    
            if closed:
                trades.append(r_mult)
                in_pos = False
                continue

        if not in_pos:
            rng = h - l
            if rng <= 0:
                continue
            if ema_fast[i] > ema_mid[i] > ema_slow[i]:
                if l <= ema_fast[i] and c > ema_mid[i]:
                    lower_wick = min(o, c) - l
                    if (lower_wick / rng) >= 0.25 and c > o:
                        in_pos = True
                        pos_side = 1
                        entry_idx = i
                        entry_p = c
                        stop_p = l - (0.1 * rng)
                        initial_risk = entry_p - stop_p
                        if initial_risk <= 0:
                            in_pos = False
                            continue
                        target_p = entry_p + (tp_mult * initial_risk)
                        highest_p = h
                        be_triggered = False
            elif ema_fast[i] < ema_mid[i] < ema_slow[i]:
                if h >= ema_fast[i] and c < ema_mid[i]:
                    upper_wick = h - max(o, c)
                    if (upper_wick / rng) >= 0.25 and c < o:
                        in_pos = True
                        pos_side = -1
                        entry_idx = i
                        entry_p = c
                        stop_p = h + (0.1 * rng)
                        initial_risk = stop_p - entry_p
                        if initial_risk <= 0:
                            in_pos = False
                            continue
                        target_p = entry_p - (tp_mult * initial_risk)
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
    
    gross_gain = wins.sum() if len(wins) > 0 else 0
    gross_loss = abs(losses.sum()) if len(losses) > 0 else 0.0001
    pf = gross_gain / gross_loss
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
        'max_dd': max_dd
    }

def main():
    best_df = pd.read_csv(os.path.join(DELTA_DIR, "delta_best_per_asset.csv"))
    pos_df = best_df[best_df['net_r'] > 0].copy()
    b20 = pos_df.head(20)
    
    print(f"{'Target Strategy':<25} | {'Trades':<7} | {'Win Rate %':<11} | {'Breakeven %':<12} | {'Loss %':<8} | {'Profit Factor':<14} | {'Net R':<10} | {'Max DD (R)'}")
    print("-" * 115)
    
    for tp_val, be_val, desc in [
        (1.5, 0.8, "Quick Scalp (TP 1.5R, BE @ 0.8R)"),
        (2.0, 1.0, "Standard 2.0R (TP 2.0R, BE @ 1.0R)"),
        (2.5, 1.0, "Extended 2.5R (TP 2.5R, BE @ 1.0R)"),
        (3.0, 1.2, "Swing 3.0R (TP 3.0R, BE @ 1.2R)"),
        (2.0, None, "Pure 2.0R (No Breakeven move)"),
        (2.5, None, "Pure 2.5R (No Breakeven move)")
    ]:
        tot_trades = 0
        tot_wins = 0
        tot_bes = 0
        tot_losses = 0
        tot_net_r = 0.0
        gross_w = 0.0
        gross_l = 0.0
        
        for _, row in b20.iterrows():
            fpath = os.path.join(DELTA_DIR, f"{row['symbol']}_{row['timeframe'].lower()}.csv")
            res = backtest_tp_targets(fpath, ribbon=(34, 89, 233), tp_mult=tp_val, be_at=be_val)
            if res:
                tot_trades += res['trades']
                tot_wins += int(res['trades'] * (res['win_rate'] / 100.0))
                tot_bes += int(res['trades'] * (res['be_rate'] / 100.0))
                tot_losses += int(res['trades'] * (res['loss_rate'] / 100.0))
                tot_net_r += res['net_r']
                if res['net_r'] > 0:
                    gross_w += res['net_r'] # approximate
                    
        wr = tot_wins / tot_trades * 100.0
        ber = tot_bes / tot_trades * 100.0
        lr = tot_losses / tot_trades * 100.0
        print(f"{desc:<25} | {tot_trades:<7} | {wr:<11.1f} | {ber:<12.1f} | {lr:<8.1f} | {gross_w/max(1, tot_trades):<14.2f} | {tot_net_r:<10.1f} | -")

if __name__ == '__main__':
    main()
