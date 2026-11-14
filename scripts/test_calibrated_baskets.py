import os
import pandas as pd
import numpy as np

DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"

def get_asset_trades(symbol, tf, ribbon_name, exit_type):
    from delta_quant_optimizer import calculate_ema
    ribbon_map = {
        'Prime_21_55_144': (21, 55, 144),
        'Prime_34_89_233': (34, 89, 233),
        'Prime_55_89_233': (55, 89, 233),
        'Classic_50_100_200': (50, 100, 200)
    }
    ribbon = ribbon_map[ribbon_name]
    fpath = os.path.join(DELTA_DIR, f"{symbol}_{tf.lower()}.csv")
    if not os.path.exists(fpath):
        return []
    
    df = pd.read_csv(fpath)
    if len(df) < 300:
        return []
        
    opens = df['open'].to_numpy(dtype=float)
    highs = df['high'].to_numpy(dtype=float)
    lows = df['low'].to_numpy(dtype=float)
    closes = df['close'].to_numpy(dtype=float)
    timestamps = df['timestamp'].to_numpy(dtype=int)
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
    entry_idx = 0
    entry_price = 0.0
    stop_price = 0.0
    initial_risk = 0.0
    highest_price = 0.0
    lowest_price = 0.0
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
                if h > highest_price:
                    highest_price = h
                if not be_triggered and (highest_price - entry_price) >= initial_risk:
                    stop_price = entry_price
                    be_triggered = True
                if l <= stop_price:
                    exit_p = min(o, stop_price) if o < stop_price else stop_price
                    r_mult = (exit_p - entry_price) / initial_risk
                    closed = True
                else:
                    if exit_type == 'trail_ema89' and c < ema_89[i]:
                        exit_p = c
                        r_mult = (exit_p - entry_price) / initial_risk
                        closed = True
                    elif exit_type == 'trail_ema55' and c < ema_55[i]:
                        exit_p = c
                        r_mult = (exit_p - entry_price) / initial_risk
                        closed = True
                    elif exit_type == 'fixed_2.5r_be1r' and h >= entry_price + (2.5 * initial_risk):
                        exit_p = entry_price + (2.5 * initial_risk)
                        r_mult = 2.5
                        closed = True
                    elif exit_type == 'asymmetric_step':
                        if highest_price >= entry_price + (2.5 * initial_risk):
                            t_stop = entry_price + (1.8 * initial_risk)
                            if l <= t_stop or c < ema_55[i]:
                                exit_p = max(l, t_stop) if l <= t_stop else c
                                r_mult = (exit_p - entry_price) / initial_risk
                                closed = True
                        elif c < ema_89[i] and (c - entry_price) > 0:
                            exit_p = c
                            r_mult = (exit_p - entry_price) / initial_risk
                            closed = True
            elif pos_side == -1:
                if l < lowest_price:
                    lowest_price = l
                if not be_triggered and (entry_price - lowest_price) >= initial_risk:
                    stop_price = entry_price
                    be_triggered = True
                if h >= stop_price:
                    exit_p = max(o, stop_price) if o > stop_price else stop_price
                    r_mult = (entry_price - exit_p) / initial_risk
                    closed = True
                else:
                    if exit_type == 'trail_ema89' and c > ema_89[i]:
                        exit_p = c
                        r_mult = (entry_price - exit_p) / initial_risk
                        closed = True
                    elif exit_type == 'trail_ema55' and c > ema_55[i]:
                        exit_p = c
                        r_mult = (entry_price - exit_p) / initial_risk
                        closed = True
                    elif exit_type == 'fixed_2.5r_be1r' and l <= entry_price - (2.5 * initial_risk):
                        exit_p = entry_price - (2.5 * initial_risk)
                        r_mult = 2.5
                        closed = True
                    elif exit_type == 'asymmetric_step':
                        if lowest_price <= entry_price - (2.5 * initial_risk):
                            t_stop = entry_price - (1.8 * initial_risk)
                            if h >= t_stop or c > ema_55[i]:
                                exit_p = min(h, t_stop) if h >= t_stop else c
                                r_mult = (entry_price - exit_p) / initial_risk
                                closed = True
                        elif c > ema_89[i] and (entry_price - c) > 0:
                            exit_p = c
                            r_mult = (entry_price - exit_p) / initial_risk
                            closed = True
                            
            if closed:
                trades.append({
                    'symbol': symbol,
                    'entry_ts': timestamps[entry_idx],
                    'exit_ts': timestamps[i],
                    'r_mult': r_mult,
                    'side': pos_side
                })
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
                        entry_price = c
                        stop_price = l - (0.1 * rng)
                        initial_risk = entry_price - stop_price
                        if initial_risk <= 0:
                            in_pos = False
                            continue
                        highest_price = h
                        be_triggered = False
            elif ema_fast[i] < ema_mid[i] < ema_slow[i]:
                if h >= ema_fast[i] and c < ema_mid[i]:
                    upper_wick = h - max(o, c)
                    if (upper_wick / rng) >= 0.25 and c < o:
                        in_pos = True
                        pos_side = -1
                        entry_idx = i
                        entry_price = c
                        stop_price = h + (0.1 * rng)
                        initial_risk = stop_price - entry_price
                        if initial_risk <= 0:
                            in_pos = False
                            continue
                        lowest_price = l
                        be_triggered = False
                        
    return trades

def simulate_portfolio(assets_df, initial_capital=5000.0, risk_pct=0.005, max_concurrent=6):
    all_trades = []
    for _, row in assets_df.iterrows():
        t_list = get_asset_trades(row['symbol'], row['timeframe'], row['ribbon'], row['exit_type'])
        all_trades.extend(t_list)
        
    if not all_trades:
        return None
        
    all_trades.sort(key=lambda x: x['entry_ts'])
    
    equity = initial_capital
    active_positions = []
    executed = []
    eq_curve = [(all_trades[0]['entry_ts'], equity)]
    
    for t in all_trades:
        t_entry = t['entry_ts']
        active_positions = [pos for pos in active_positions if pos['exit_ts'] > t_entry]
        if len(active_positions) >= max_concurrent:
            continue
            
        dollar_risk = equity * risk_pct
        pnl = dollar_risk * t['r_mult']
        # Exchange fee & slip: 0.05% of position ~ 0.04 * dollar_risk
        fee = dollar_risk * 0.04
        net_pnl = pnl - fee
        equity += net_pnl
        eq_curve.append((t['exit_ts'], equity))
        
        t['net_pnl'] = net_pnl
        t['equity_after'] = equity
        executed.append(t)
        active_positions.append(t)
        
    df_exec = pd.DataFrame(executed)
    if len(df_exec) == 0:
        return None
        
    wins = df_exec[df_exec['r_mult'] > 0]
    total_days = (df_exec['exit_ts'].max() - df_exec['entry_ts'].min()) / 86400.0
    
    eq_vals = [pt[1] for pt in eq_curve]
    cummax = np.maximum.accumulate(eq_vals)
    dd = (cummax - eq_vals) / cummax
    max_dd_pct = np.max(dd) * 100.0
    
    daily_dollar = (equity - initial_capital) / max(total_days, 1.0)
    
    return {
        'total_trades': len(df_exec),
        'win_rate': len(wins) / len(df_exec) * 100.0,
        'final_equity': equity,
        'roi_pct': ((equity - initial_capital) / initial_capital) * 100.0,
        'max_dd_pct': max_dd_pct,
        'daily_dollar': daily_dollar,
        'daily_inr': daily_dollar * 87.0,
        'total_days': total_days,
        'trades_per_day': len(df_exec) / max(total_days, 1.0)
    }

def main():
    best_df = pd.read_csv(os.path.join(DELTA_DIR, "delta_best_per_asset.csv"))
    # Filter for positive net R assets
    pos_df = best_df[best_df['net_r'] > 0].copy()
    
    print(f"Total positive assets available: {len(pos_df)}")
    
    # Test different basket sizes
    # Basket 1: Top 10 by Quality Ratio
    b10 = pos_df.head(10)
    # Basket 2: Top 15 Balanced
    b15 = pos_df.head(15)
    # Basket 3: Top 20 Elite Wealth
    b20 = pos_df.head(20)
    # Basket 4: Top 25
    b25 = pos_df.head(25)
    
    print(f"\n{'Basket':<20} | {'Risk':<5} | {'Trades':<7} | {'Win %':<6} | {'Final Eq ($)':<14} | {'ROI %':<10} | {'Max DD %':<8} | {'$/Day':<8} | {'₹/Day'}")
    print("-" * 115)
    
    for name, bdf in [('Top 10 Basket', b10), ('Top 15 Basket', b15), ('Top 20 Wealth Basket', b20), ('Top 25 Basket', b25)]:
        for r in [0.005, 0.01]:
            res = simulate_portfolio(bdf, initial_capital=5000.0, risk_pct=r, max_concurrent=6)
            if res:
                r_str = f"{r*100:.1f}%"
                feq = f"${res['final_equity']:,.2f}"
                roi = f"{res['roi_pct']:+,.1f}%"
                mdd = f"{res['max_dd_pct']:.1f}%"
                d_usd = f"${res['daily_dollar']:.2f}"
                d_inr = f"₹{res['daily_inr']:,.0f}"
                print(f"{name:<20} | {r_str:<5} | {res['total_trades']:<7} | {res['win_rate']:<6.1f} | {feq:<14} | {roi:<10} | {mdd:<8} | {d_usd:<8} | {d_inr}")

if __name__ == '__main__':
    main()
