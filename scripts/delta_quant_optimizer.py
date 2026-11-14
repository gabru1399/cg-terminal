import os
import glob
import pandas as pd
import numpy as np

DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"

def calculate_ema(series, span):
    return series.ewm(span=span, adjust=False).mean().to_numpy()

def backtest_asset(csv_path, ribbon_tuple=(34, 89, 233), exit_type='trail_ema89'):
    """
    Vectorized & fast simulation of Fibonacci EMA Rejection.
    ribbon_tuple: (fast_span, mid_span, slow_span)
    exit_type: 'trail_ema89', 'trail_ema55', 'fixed_2.5r_be1r', 'asymmetric_step'
    """
    df = pd.read_csv(csv_path)
    if len(df) < 300:
        return None
        
    opens = df['open'].to_numpy(dtype=float)
    highs = df['high'].to_numpy(dtype=float)
    lows = df['low'].to_numpy(dtype=float)
    closes = df['close'].to_numpy(dtype=float)
    n = len(closes)
    
    fast_span, mid_span, slow_span = ribbon_tuple
    ema_fast = calculate_ema(df['close'], fast_span)
    ema_mid = calculate_ema(df['close'], mid_span)
    ema_slow = calculate_ema(df['close'], slow_span)
    
    # Pre-calculate auxiliary EMAs for trailing
    ema_55 = calculate_ema(df['close'], 55)
    ema_89 = calculate_ema(df['close'], 89)
    
    trades = []
    in_pos = False
    pos_side = 0 # +1 Long, -1 Short
    entry_idx = 0
    entry_price = 0.0
    stop_price = 0.0
    risk_unit = 0.0
    initial_risk = 0.0
    highest_price = 0.0
    lowest_price = 0.0
    be_triggered = False
    
    # Warmup
    start_bar = max(slow_span, 250)
    
    for i in range(start_bar, n):
        o = opens[i]
        h = highs[i]
        l = lows[i]
        c = closes[i]
        
        # 1. Manage open position
        if in_pos:
            r_mult = 0.0
            closed = False
            
            if pos_side == 1:
                # LONG position management
                if h > highest_price:
                    highest_price = h
                
                # Check Breakeven trigger at +1.0R
                if not be_triggered and (highest_price - entry_price) >= initial_risk:
                    stop_price = entry_price # Move to Breakeven
                    be_triggered = True
                
                # Check Stop Loss
                if l <= stop_price:
                    exit_p = min(o, stop_price) if o < stop_price else stop_price
                    r_mult = (exit_p - entry_price) / initial_risk
                    closed = True
                else:
                    # Strategy specific exits
                    if exit_type == 'trail_ema89':
                        if c < ema_89[i]:
                            exit_p = c
                            r_mult = (exit_p - entry_price) / initial_risk
                            closed = True
                    elif exit_type == 'trail_ema55':
                        if c < ema_55[i]:
                            exit_p = c
                            r_mult = (exit_p - entry_price) / initial_risk
                            closed = True
                    elif exit_type == 'fixed_2.5r_be1r':
                        if h >= entry_price + (2.5 * initial_risk):
                            exit_p = entry_price + (2.5 * initial_risk)
                            r_mult = 2.5
                            closed = True
                    elif exit_type == 'asymmetric_step':
                        # Scale-out / Step: if reached +2.5R, lock in 2.0R trailing
                        if highest_price >= entry_price + (2.5 * initial_risk):
                            trail_stop = entry_price + (1.8 * initial_risk)
                            if l <= trail_stop or c < ema_55[i]:
                                exit_p = max(l, trail_stop) if l <= trail_stop else c
                                r_mult = (exit_p - entry_price) / initial_risk
                                closed = True
                        elif c < ema_89[i] and (c - entry_price) > 0:
                            exit_p = c
                            r_mult = (exit_p - entry_price) / initial_risk
                            closed = True
                            
            elif pos_side == -1:
                # SHORT position management
                if l < lowest_price:
                    lowest_price = l
                
                # Check Breakeven trigger at +1.0R
                if not be_triggered and (entry_price - lowest_price) >= initial_risk:
                    stop_price = entry_price
                    be_triggered = True
                    
                # Check Stop Loss
                if h >= stop_price:
                    exit_p = max(o, stop_price) if o > stop_price else stop_price
                    r_mult = (entry_price - exit_p) / initial_risk
                    closed = True
                else:
                    if exit_type == 'trail_ema89':
                        if c > ema_89[i]:
                            exit_p = c
                            r_mult = (entry_price - exit_p) / initial_risk
                            closed = True
                    elif exit_type == 'trail_ema55':
                        if c > ema_55[i]:
                            exit_p = c
                            r_mult = (entry_price - exit_p) / initial_risk
                            closed = True
                    elif exit_type == 'fixed_2.5r_be1r':
                        if l <= entry_price - (2.5 * initial_risk):
                            exit_p = entry_price - (2.5 * initial_risk)
                            r_mult = 2.5
                            closed = True
                    elif exit_type == 'asymmetric_step':
                        if lowest_price <= entry_price - (2.5 * initial_risk):
                            trail_stop = entry_price - (1.8 * initial_risk)
                            if h >= trail_stop or c > ema_55[i]:
                                exit_p = min(h, trail_stop) if h >= trail_stop else c
                                r_mult = (entry_price - exit_p) / initial_risk
                                closed = True
                        elif c > ema_89[i] and (entry_price - c) > 0:
                            exit_p = c
                            r_mult = (entry_price - exit_p) / initial_risk
                            closed = True
                            
            if closed:
                trades.append({
                    'entry_idx': entry_idx,
                    'exit_idx': i,
                    'side': pos_side,
                    'r_mult': r_mult,
                    'hold_bars': i - entry_idx
                })
                in_pos = False
                continue

        # 2. Check new entry signals (only if not already in position)
        if not in_pos:
            rng = h - l
            if rng <= 0:
                continue
                
            # Bullish Trend: Fast > Mid > Slow
            if ema_fast[i] > ema_mid[i] > ema_slow[i]:
                # Rejection: Tested ribbon (Low <= Fast EMA) and closed in upper half with lower wick >= 25%
                if l <= ema_fast[i] and c > ema_mid[i]:
                    lower_wick = min(o, c) - l
                    if (lower_wick / rng) >= 0.25 and c > o:
                        # Valid Bullish Rejection
                        in_pos = True
                        pos_side = 1
                        entry_idx = i
                        entry_price = c
                        stop_price = l - (0.1 * rng) # Just below rejection wick
                        initial_risk = entry_price - stop_price
                        if initial_risk <= 0:
                            in_pos = False
                            continue
                        highest_price = h
                        be_triggered = False
                        continue
                        
            # Bearish Trend: Fast < Mid < Slow
            elif ema_fast[i] < ema_mid[i] < ema_slow[i]:
                # Rejection: Tested ribbon (High >= Fast EMA) and closed in lower half with upper wick >= 25%
                if h >= ema_fast[i] and c < ema_mid[i]:
                    upper_wick = h - max(o, c)
                    if (upper_wick / rng) >= 0.25 and c < o:
                        # Valid Bearish Rejection
                        in_pos = True
                        pos_side = -1
                        entry_idx = i
                        entry_price = c
                        stop_price = h + (0.1 * rng) # Just above rejection wick
                        initial_risk = stop_price - entry_price
                        if initial_risk <= 0:
                            in_pos = False
                            continue
                        lowest_price = l
                        be_triggered = False
                        continue

    if not trades:
        return {
            'trades_count': 0,
            'win_rate': 0.0,
            'profit_factor': 0.0,
            'net_r': 0.0,
            'max_dd_r': 0.0,
            'quality_ratio': 0.0
        }
        
    df_trades = pd.DataFrame(trades)
    wins = df_trades[df_trades['r_mult'] > 0]
    losses = df_trades[df_trades['r_mult'] <= 0]
    
    win_rate = len(wins) / len(df_trades) * 100.0
    gross_gain = wins['r_mult'].sum() if len(wins) > 0 else 0.0
    gross_loss = abs(losses['r_mult'].sum()) if len(losses) > 0 else 0.0001
    pf = gross_gain / gross_loss
    net_r = df_trades['r_mult'].sum()
    
    # Calculate Max Drawdown in R
    cum_r = df_trades['r_mult'].cumsum()
    peak = cum_r.cummax()
    dd = peak - cum_r
    max_dd_r = dd.max() if len(dd) > 0 else 0.0
    
    quality_ratio = net_r / max_dd_r if max_dd_r > 0 else net_r
    
    return {
        'trades_count': len(df_trades),
        'win_rate': win_rate,
        'profit_factor': pf,
        'net_r': net_r,
        'max_dd_r': max_dd_r,
        'quality_ratio': quality_ratio,
        'avg_r_per_trade': net_r / len(df_trades),
        'avg_hold_bars': df_trades['hold_bars'].mean()
    }
