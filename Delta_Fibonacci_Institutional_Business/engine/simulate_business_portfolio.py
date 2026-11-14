import os
import pandas as pd
import numpy as np

BASE_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Fibonacci_Institutional_Business"
DATA_DIR = os.path.join(BASE_DIR, "data")
AUDIT_DIR = os.path.join(BASE_DIR, "audit")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

from delta_master_calmar_optimizer import calculate_atr, calculate_ema_dict

def get_asset_trades_for_portfolio(symbol, tf, fast_p, mid_p, slow_p, exit_mode, spread_cost_r=0.04):
    fpath = os.path.join(DATA_DIR, f"{symbol}_{tf.lower()}.csv")
    if not os.path.exists(fpath):
        return []
    try:
        df = pd.read_csv(fpath)
    except Exception:
        return []
    if len(df) < 300:
        return []
        
    opens = df['open'].to_numpy(dtype=float)
    highs = df['high'].to_numpy(dtype=float)
    lows = df['low'].to_numpy(dtype=float)
    closes = df['close'].to_numpy(dtype=float)
    timestamps = df['timestamp'].to_numpy(dtype=int)
    n = len(closes)
    
    rng = highs - lows
    rng = np.where(rng <= 0, 1e-6, rng)
    body_tops = np.maximum(opens, closes)
    body_bots = np.minimum(opens, closes)
    u_wicks = (highs - body_tops) / rng
    l_wicks = (body_bots - lows) / rng
    
    atrs = calculate_atr(highs, lows, closes, 14)
    ema_dict = calculate_ema_dict(closes, [21, 34, 50, 55, 89, 100, 144, 200, 233])
    
    start_idx = max(fast_p, mid_p, slow_p) + 10
    ef = ema_dict[fast_p]; em = ema_dict[mid_p]; es = ema_dict[slow_p]
    
    is_fixed = exit_mode.startswith("fixed_")
    fixed_rr = float(exit_mode.split("_")[1]) if is_fixed else 0.0
    
    trades = []
    in_trade = False
    trade_side = 0
    entry_p = 0.0; sl_p = 0.0; r_dist = 0.0; entry_i = 0
    max_fav_r = 0.0
    
    for i in range(start_idx, n - 1):
        if in_trade:
            bh = highs[i]; bl = lows[i]; bc = closes[i]
            exited = False; exit_r = 0.0
            
            cur_r = (entry_p - bl) / r_dist if trade_side == -1 else (bh - entry_p) / r_dist
            if cur_r > max_fav_r: max_fav_r = cur_r
            
            if trade_side == -1: # SHORT
                if is_fixed:
                    if bh >= sl_p:
                        exit_r = -1.0; exited = True
                    elif bl <= (entry_p - fixed_rr * r_dist):
                        exit_r = fixed_rr; exited = True
                elif exit_mode == "step_trail":
                    if max_fav_r >= 6.0:
                        sl_p = min(sl_p, ema_dict[34][i])
                    elif max_fav_r >= 4.0:
                        sl_p = min(sl_p, entry_p - 2.0 * r_dist)
                    elif max_fav_r >= 2.0:
                        sl_p = min(sl_p, entry_p - 0.5 * r_dist)
                    if bh >= sl_p:
                        exit_r = (entry_p - sl_p) / r_dist; exited = True
                elif exit_mode == "trail_89":
                    if bc > ema_dict[89][i]:
                        exit_r = (entry_p - bc) / r_dist; exited = True
                    elif bh >= sl_p:
                        exit_r = -1.0; exited = True
                elif exit_mode == "trail_55":
                    if bc > ema_dict[55][i]:
                        exit_r = (entry_p - bc) / r_dist; exited = True
                    elif bh >= sl_p:
                        exit_r = -1.0; exited = True
            elif trade_side == 1: # LONG
                if is_fixed:
                    if bl <= sl_p:
                        exit_r = -1.0; exited = True
                    elif bh >= (entry_p + fixed_rr * r_dist):
                        exit_r = fixed_rr; exited = True
                elif exit_mode == "step_trail":
                    if max_fav_r >= 6.0:
                        sl_p = max(sl_p, ema_dict[34][i])
                    elif max_fav_r >= 4.0:
                        sl_p = max(sl_p, entry_p + 2.0 * r_dist)
                    elif max_fav_r >= 2.0:
                        sl_p = max(sl_p, entry_p + 0.5 * r_dist)
                    if bl <= sl_p:
                        exit_r = (sl_p - entry_p) / r_dist; exited = True
                elif exit_mode == "trail_89":
                    if bc < ema_dict[89][i]:
                        exit_r = (bc - entry_p) / r_dist; exited = True
                    elif bl <= sl_p:
                        exit_r = -1.0; exited = True
                elif exit_mode == "trail_55":
                    if bc < ema_dict[55][i]:
                        exit_r = (bc - entry_p) / r_dist; exited = True
                    elif bl <= sl_p:
                        exit_r = -1.0; exited = True
                        
            if exited:
                capped_r = min(exit_r, 15.0) - spread_cost_r
                trades.append({
                    'symbol': symbol,
                    'entry_ts': timestamps[entry_i],
                    'exit_ts': timestamps[i],
                    'r': capped_r
                })
                in_trade = False
            continue
            
        c_c = closes[i]; c_p = closes[i-1]
        h_i = highs[i]; l_i = lows[i]; a_i = atrs[i]
        
        sig = 0
        if (ef[i] < em[i]) and (em[i] < es[i]):
            if c_p < ef[i]:
                if (h_i >= ef[i]*0.999 or h_i >= em[i]*0.999 or h_i >= es[i]*0.999) and (c_c < em[i]):
                    if u_wicks[i] >= 0.25:
                        sig = -1
        elif (ef[i] > em[i]) and (em[i] > es[i]):
            if c_p > ef[i]:
                if (l_i <= ef[i]*1.001 or l_i <= em[i]*1.001 or l_i <= es[i]*1.001) and (c_c > em[i]):
                    if l_wicks[i] >= 0.25:
                        sig = 1
                        
        if sig != 0:
            next_i = i + 1
            if next_i >= n: break
            ep = opens[next_i]
            
            if is_fixed:
                sp = (h_i + 0.3 * a_i) if sig == -1 else (l_i - 0.3 * a_i)
            else:
                sp = (max(es[i], h_i) + 0.5 * a_i) if sig == -1 else (min(es[i], l_i) - 0.5 * a_i)
                
            rd = abs(ep - sp)
            if rd <= 0: continue
            
            in_trade = True
            trade_side = sig
            entry_p = ep; sl_p = sp; r_dist = rd; entry_i = next_i
            max_fav_r = 0.0
            
    return trades

def simulate_portfolio(assets_df, initial_capital=5000.0, max_concurrent=6):
    ribbon_map = {
        'Fib_89_233': (55, 89, 233),
        'Fib_34_89': (34, 89, 233),
        'Fib_21_55': (21, 55, 144),
        'Classic_50_200': (50, 100, 200)
    }
    
    all_trades = []
    for _, row in assets_df.iterrows():
        f_p, m_p, s_p = ribbon_map[row['ribbon']]
        t_list = get_asset_trades_for_portfolio(row['symbol'], row['timeframe'], f_p, m_p, s_p, row['strategy'])
        all_trades.extend(t_list)
        
    if not all_trades:
        return {}
        
    all_trades.sort(key=lambda x: x['entry_ts'])
    
    results = {}
    for r_label, fixed_dollar, pct_risk in [
        ('Fixed $25 (0.5%)', 25.0, None),
        ('Fixed $50 (1.0%)', 50.0, None),
        ('Compounding 0.5%', None, 0.005),
        ('Compounding 1.0%', None, 0.01)
    ]:
        equity = initial_capital
        active_pos = []
        executed = []
        eq_curve = [(all_trades[0]['entry_ts'], equity)]
        
        for t in all_trades:
            t_entry = t['entry_ts']
            active_pos = [p for p in active_pos if p['exit_ts'] > t_entry]
            if len(active_pos) >= max_concurrent:
                continue
                
            dollar_risk = fixed_dollar if fixed_dollar is not None else equity * pct_risk
            pnl = dollar_risk * t['r']
            equity += pnl
            eq_curve.append((t['exit_ts'], equity))
            executed.append(t)
            active_pos.append(t)
            
        df_exec = pd.DataFrame(executed)
        wins = df_exec[df_exec['r'] > 0]
        total_days = max(1.0, (df_exec['exit_ts'].max() - df_exec['entry_ts'].min()) / 86400.0)
        
        eq_vals = [pt[1] for pt in eq_curve]
        cummax = np.maximum.accumulate(eq_vals)
        dd = (cummax - eq_vals) / cummax
        max_dd_pct = np.max(dd) * 100.0
        
        profit = equity - initial_capital
        roi_pct = (profit / initial_capital) * 100.0
        
        # Annualized ROI & Calmar
        annualized_roi = ((equity / initial_capital) ** (365.25 / total_days) - 1.0) * 100.0
        calmar = annualized_roi / max(max_dd_pct, 1.0)
        
        daily_usd = profit / total_days
        daily_inr = daily_usd * 87.0
        monthly_usd = daily_usd * 30.0
        monthly_inr = daily_inr * 30.0
        
        results[r_label] = {
            'trades': len(df_exec),
            'win_rate': round(len(wins) / len(df_exec) * 100.0, 1),
            'final_equity': round(equity, 2),
            'profit': round(profit, 2),
            'roi_pct': round(roi_pct, 1),
            'annualized_roi': round(annualized_roi, 1),
            'max_dd_pct': round(max_dd_pct, 1),
            'calmar_ratio': round(calmar, 2),
            'daily_usd': round(daily_usd, 2),
            'daily_inr': round(daily_inr, 0),
            'monthly_usd': round(monthly_usd, 2),
            'monthly_inr': round(monthly_inr, 0),
            'total_days': round(total_days, 1)
        }
    return results
