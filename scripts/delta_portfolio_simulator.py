import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime

DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"

# Load best parameters or execute chronological event-driven portfolio backtest
def run_event_driven_portfolio(selected_symbols, tf='1h', ribbon=(34, 89, 233), exit_type='trail_ema89',
                               initial_capital=5000.0, risk_pct=0.005, max_concurrent=6, fee_pct=0.0005):
    """
    Event-driven unified portfolio backtest across selected Delta Exchange assets.
    Enforces exact timestamp ordering and max_concurrent positions governor.
    """
    from delta_quant_optimizer import calculate_ema
    
    # 1. Generate trade candidate list with timestamps across all selected assets
    candidate_trades = []
    fast_s, mid_s, slow_s = ribbon
    
    for sym in selected_symbols:
        fpath = os.path.join(DELTA_DIR, f"{sym}_{tf.lower()}.csv")
        if not os.path.exists(fpath):
            continue
        df = pd.read_csv(fpath)
        if len(df) < 300:
            continue
            
        opens = df['open'].to_numpy(dtype=float)
        highs = df['high'].to_numpy(dtype=float)
        lows = df['low'].to_numpy(dtype=float)
        closes = df['close'].to_numpy(dtype=float)
        timestamps = df['timestamp'].to_numpy(dtype=int)
        n = len(closes)
        
        ema_f = calculate_ema(df['close'], fast_s)
        ema_m = calculate_ema(df['close'], mid_s)
        ema_s = calculate_ema(df['close'], slow_s)
        ema_55 = calculate_ema(df['close'], 55)
        ema_89 = calculate_ema(df['close'], 89)
        
        start_bar = max(slow_s, 250)
        i = start_bar
        while i < n - 1:
            o = opens[i]
            h = highs[i]
            l = lows[i]
            c = closes[i]
            rng = h - l
            if rng <= 0:
                i += 1
                continue
                
            signal_side = 0
            if ema_f[i] > ema_m[i] > ema_s[i]:
                if l <= ema_f[i] and c > ema_m[i]:
                    lower_wick = min(o, c) - l
                    if (lower_wick / rng) >= 0.25 and c > o:
                        signal_side = 1
            elif ema_f[i] < ema_m[i] < ema_s[i]:
                if h >= ema_f[i] and c < ema_m[i]:
                    upper_wick = h - max(o, c)
                    if (upper_wick / rng) >= 0.25 and c < o:
                        signal_side = -1
                        
            if signal_side != 0:
                # Forward simulate trade to find exit bar
                entry_idx = i
                entry_ts = timestamps[i]
                entry_p = c
                if signal_side == 1:
                    stop_p = l - (0.1 * rng)
                    init_risk = entry_p - stop_p
                else:
                    stop_p = h + (0.1 * rng)
                    init_risk = stop_p - entry_p
                    
                if init_risk <= 0:
                    i += 1
                    continue
                    
                # Track forward until exit
                exit_idx = i + 1
                exit_ts = timestamps[min(i + 1, n - 1)]
                highest_p = h
                lowest_p = l
                curr_stop = stop_p
                be_hit = False
                r_result = 0.0
                
                for j in range(i + 1, n):
                    oj = opens[j]
                    hj = highs[j]
                    lj = lows[j]
                    cj = closes[j]
                    exit_idx = j
                    exit_ts = timestamps[j]
                    
                    if signal_side == 1:
                        if hj > highest_p:
                            highest_p = hj
                        if not be_hit and (highest_p - entry_p) >= init_risk:
                            curr_stop = entry_p
                            be_hit = True
                        if lj <= curr_stop:
                            exit_p = min(oj, curr_stop) if oj < curr_stop else curr_stop
                            r_result = (exit_p - entry_p) / init_risk
                            break
                        if exit_type == 'trail_ema89' and cj < ema_89[j]:
                            r_result = (cj - entry_p) / init_risk
                            break
                        elif exit_type == 'trail_ema55' and cj < ema_55[j]:
                            r_result = (cj - entry_p) / init_risk
                            break
                        elif exit_type == 'fixed_2.5r_be1r' and hj >= entry_p + (2.5 * init_risk):
                            r_result = 2.5
                            break
                        elif exit_type == 'asymmetric_step':
                            if highest_p >= entry_p + (2.5 * init_risk):
                                t_stop = entry_p + (1.8 * init_risk)
                                if lj <= t_stop or cj < ema_55[j]:
                                    r_result = (max(lj, t_stop) - entry_p) / init_risk
                                    break
                            elif cj < ema_89[j] and (cj - entry_p) > 0:
                                r_result = (cj - entry_p) / init_risk
                                break
                    else:
                        # Short
                        if lj < lowest_p:
                            lowest_p = lj
                        if not be_hit and (entry_p - lowest_p) >= init_risk:
                            curr_stop = entry_p
                            be_hit = True
                        if hj >= curr_stop:
                            exit_p = max(oj, curr_stop) if oj > curr_stop else curr_stop
                            r_result = (entry_p - exit_p) / init_risk
                            break
                        if exit_type == 'trail_ema89' and cj > ema_89[j]:
                            r_result = (entry_p - cj) / init_risk
                            break
                        elif exit_type == 'trail_ema55' and cj > ema_55[j]:
                            r_result = (entry_p - cj) / init_risk
                            break
                        elif exit_type == 'fixed_2.5r_be1r' and lj <= entry_p - (2.5 * init_risk):
                            r_result = 2.5
                            break
                        elif exit_type == 'asymmetric_step':
                            if lowest_p <= entry_p - (2.5 * init_risk):
                                t_stop = entry_p - (1.8 * init_risk)
                                if hj >= t_stop or cj > ema_55[j]:
                                    r_result = (entry_p - min(hj, t_stop)) / init_risk
                                    break
                            elif cj > ema_89[j] and (entry_p - cj) > 0:
                                r_result = (entry_p - cj) / init_risk
                                break
                                
                candidate_trades.append({
                    'symbol': sym,
                    'side': signal_side,
                    'entry_ts': entry_ts,
                    'exit_ts': exit_ts,
                    'r_result': r_result
                })
                # Move forward past exit
                i = exit_idx + 1
            else:
                i += 1
                
    if not candidate_trades:
        return None
        
    # 2. Sort candidate trades strictly by entry_ts
    candidate_trades.sort(key=lambda x: x['entry_ts'])
    
    # 3. Simulate live portfolio execution with concurrency governor
    equity = initial_capital
    equity_curve = [(candidate_trades[0]['entry_ts'], equity)]
    active_positions = [] # list of (exit_ts, trade_info)
    executed_trades = []
    
    for trade in candidate_trades:
        t_entry = trade['entry_ts']
        
        # Purge closed positions
        active_positions = [pos for pos in active_positions if pos['exit_ts'] > t_entry]
        
        # Check concurrency governor
        if len(active_positions) >= max_concurrent:
            continue # Skip trade due to full portfolio heat
            
        # Accept trade
        dollar_risk = equity * risk_pct
        pnl = dollar_risk * trade['r_result']
        # Friction deduction (taker fee 0.05% in + 0.05% out ~ 0.1% of position size)
        friction = dollar_risk * 0.08
        net_pnl = pnl - friction
        
        equity += net_pnl
        equity_curve.append((trade['exit_ts'], equity))
        
        trade['net_pnl'] = net_pnl
        trade['equity_after'] = equity
        executed_trades.append(trade)
        active_positions.append(trade)
        
    df_exec = pd.DataFrame(executed_trades)
    if len(df_exec) == 0:
        return None
        
    wins = df_exec[df_exec['r_result'] > 0]
    total_days = (df_exec['exit_ts'].max() - df_exec['entry_ts'].min()) / 86400.0
    
    total_return_pct = ((equity - initial_capital) / initial_capital) * 100.0
    daily_avg_dollar = (equity - initial_capital) / max(total_days, 1.0)
    
    # Max drawdown
    eq_values = [pt[1] for pt in equity_curve]
    cummax = np.maximum.accumulate(eq_values)
    drawdowns = (cummax - eq_values) / cummax
    max_dd_pct = np.max(drawdowns) * 100.0
    
    return {
        'total_trades': len(df_exec),
        'win_rate': len(wins) / len(df_exec) * 100.0,
        'final_equity': equity,
        'net_profit_dollar': equity - initial_capital,
        'total_return_pct': total_return_pct,
        'max_dd_pct': max_dd_pct,
        'daily_avg_dollar': daily_avg_dollar,
        'daily_avg_inr': daily_avg_dollar * 87.0, # USDINR ~ 87
        'total_days': total_days,
        'trades_per_day': len(df_exec) / max(total_days, 1.0)
    }
