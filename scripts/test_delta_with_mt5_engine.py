import os
import glob
import pandas as pd
import numpy as np

DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"

# Import or copy exact simulate_fast from run_fast_96_opt.py
def calculate_ema_dict(closes, spans):
    res = {}
    s = pd.Series(closes)
    for sp in spans:
        res[sp] = s.ewm(span=sp, adjust=False).mean().to_numpy()
    return res

def calculate_atr(highs, lows, closes, period=14):
    n = len(closes)
    tr = np.zeros(n)
    tr[0] = highs[0] - lows[0]
    for i in range(1, n):
        tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
    atr = pd.Series(tr).rolling(period).mean().bfill().to_numpy()
    return atr

def simulate_mt5_exact(df, fast_p=34, mid_p=89, slow_p=233, exit_mode="fixed_2.0", spread_cost_r=0.04):
    opens = df['open'].to_numpy(dtype=float)
    highs = df['high'].to_numpy(dtype=float)
    lows = df['low'].to_numpy(dtype=float)
    closes = df['close'].to_numpy(dtype=float)
    n = len(closes)
    
    if n < 300:
        return None
        
    rng = highs - lows
    rng = np.where(rng <= 0, 1e-6, rng)
    
    # Rejection wicks
    body_tops = np.maximum(opens, closes)
    body_bots = np.minimum(opens, closes)
    u_wicks = (highs - body_tops) / rng
    l_wicks = (body_bots - lows) / rng
    
    atrs = calculate_atr(highs, lows, closes, 14)
    ema_dict = calculate_ema_dict(closes, [21, 34, 50, 55, 89, 100, 144, 200, 233])
    
    start_idx = max(fast_p, mid_p, slow_p) + 10
    
    ef = ema_dict[fast_p]
    em = ema_dict[mid_p]
    es = ema_dict[slow_p]
    
    trades_r = []
    in_trade = False
    trade_side = 0
    entry_p = 0.0
    sl_p = 0.0
    r_dist = 0.0
    entry_i = 0
    max_fav_r = 0.0
    
    is_fixed = exit_mode.startswith("fixed_")
    fixed_rr = float(exit_mode.split("_")[1]) if is_fixed else 0.0
    
    for i in range(start_idx, n - 1):
        if in_trade:
            bh = highs[i]; bl = lows[i]; bc = closes[i]
            exited = False
            exit_r = 0.0
            
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
                        new_sl = min(sl_p, ema_dict[34][i])
                        sl_p = new_sl
                    elif max_fav_r >= 4.0:
                        new_sl = entry_p - (2.0 * r_dist)
                        if new_sl < sl_p: sl_p = new_sl
                    elif max_fav_r >= 2.0:
                        new_sl = entry_p - (0.5 * r_dist)
                        if new_sl < sl_p: sl_p = new_sl
                    if bh >= sl_p:
                        exit_r = (entry_p - sl_p) / r_dist
                        exited = True
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
                        new_sl = max(sl_p, ema_dict[34][i])
                        sl_p = new_sl
                    elif max_fav_r >= 4.0:
                        new_sl = entry_p + (2.0 * r_dist)
                        if new_sl > sl_p: sl_p = new_sl
                    elif max_fav_r >= 2.0:
                        new_sl = entry_p + (0.5 * r_dist)
                        if new_sl > sl_p: sl_p = new_sl
                    if bl <= sl_p:
                        exit_r = (sl_p - entry_p) / r_dist
                        exited = True
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
                trades_r.append(exit_r - spread_cost_r)
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
            
    if not trades_r:
        return None
        
    arr = np.array(trades_r)
    wins = np.sum(arr > 0)
    tot = len(arr)
    wr = (wins / tot) * 100
    gw = np.sum(arr[arr > 0])
    gl = abs(np.sum(arr[arr < 0]))
    pf = (gw / gl) if gl > 0 else 999.0
    net_r = np.sum(arr)
    avg_r = net_r / tot
    
    cum = np.cumsum(arr)
    peak = np.maximum.accumulate(cum)
    max_dd = np.max(peak - cum) if len(cum) > 0 else 0.0
    
    return {
        "trades": tot,
        "win_rate": round(float(wr), 1),
        "pf": round(float(pf), 2),
        "net_r": round(float(net_r), 2),
        "avg_r": round(float(avg_r), 3),
        "max_dd_r": round(float(max_dd), 2)
    }

def main():
    # Test on key assets available on Delta Exchange (both 4H and 1H)
    test_assets = [
        ('BTCUSD', '4h'), ('ETHUSD', '4h'), ('LTCUSD', '4h'), ('AVAXUSD', '4h'),
        ('SOLUSD', '4h'), ('XRPUSD', '4h'), ('DOGEUSD', '4h'), ('BNBUSD', '4h'),
        ('XAUTUSD', '4h'), ('SLVONUSD', '4h'), ('QQQXUSD', '1h'), ('NVDAXUSD', '1h')
    ]
    
    print("=" * 110)
    print("TESTING EXACT MT5 STRATEGY ALGORITHM ON DELTA EXCHANGE ASSETS")
    print("=" * 110)
    print(f"{'Asset':<10} | {'TF':<4} | {'Strategy Mode':<18} | {'Ribbon':<15} | {'Trades':<7} | {'Win %':<7} | {'Profit Factor':<14} | {'Net R':<10} | {'Max DD (R)'}")
    print("-" * 110)
    
    for sym, tf in test_assets:
        fpath = os.path.join(DELTA_DIR, f"{sym}_{tf}.csv")
        if not os.path.exists(fpath):
            continue
        df = pd.read_csv(fpath)
        
        # Test Fixed 2.0R, Fixed 2.5R, Step Trail, and Trail 89
        for mode in ['fixed_2.0', 'fixed_2.5', 'step_trail', 'trail_89']:
            for rib_name, fast_p, mid_p, slow_p in [
                ('Fib 89/233', 55, 89, 233),
                ('Fib 34/89', 34, 89, 233),
                ('Fib 21/55', 21, 55, 144)
            ]:
                res = simulate_mt5_exact(df, fast_p, mid_p, slow_p, exit_mode=mode)
                if res and res['trades'] >= 15:
                    if res['net_r'] > 0 and res['win_rate'] >= 30.0:
                        print(f"{sym:<10} | {tf.upper():<4} | {mode:<18} | {rib_name:<15} | {res['trades']:<7} | {res['win_rate']:<7.1f} | {res['pf']:<14.2f} | {res['net_r']:<10.1f} | {res['max_dd_r']}")

if __name__ == '__main__':
    main()
