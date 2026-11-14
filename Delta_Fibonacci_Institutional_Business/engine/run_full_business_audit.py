import os
import glob
import pandas as pd
import numpy as np
import time
from delta_master_calmar_optimizer import simulate_asset_calmar

BASE_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Fibonacci_Institutional_Business"
DATA_DIR = os.path.join(BASE_DIR, "data")
AUDIT_DIR = os.path.join(BASE_DIR, "audit")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(AUDIT_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

RIBBONS = [
    ('Fib_89_233', 55, 89, 233),
    ('Fib_34_89', 34, 89, 233),
    ('Fib_21_55', 21, 55, 144),
    ('Classic_50_200', 50, 100, 200)
]

STRATEGIES = ['fixed_2.0', 'fixed_2.5', 'fixed_3.0', 'step_trail', 'trail_89', 'trail_55']

def main():
    csv_4h = glob.glob(os.path.join(DATA_DIR, "*_4h.csv"))
    csv_1h = glob.glob(os.path.join(DATA_DIR, "*_1h.csv"))
    
    print(f"Discovered {len(csv_4h)} 4H files and {len(csv_1h)} 1H files in data directory.")
    
    all_simulations = []
    
    start_time = time.time()
    
    for tf_label, file_list in [('4H', csv_4h), ('1H', csv_1h)]:
        for fpath in file_list:
            symbol = os.path.basename(fpath).split('_')[0]
            try:
                df = pd.read_csv(fpath)
            except Exception:
                continue
            if len(df) < 300:
                continue
                
            for mode in STRATEGIES:
                for rib_name, f_p, m_p, s_p in RIBBONS:
                    res = simulate_asset_calmar(df, f_p, m_p, s_p, exit_mode=mode)
                    if res and res['trades'] >= 12:
                        all_simulations.append({
                            'symbol': symbol,
                            'timeframe': tf_label,
                            'strategy': mode,
                            'ribbon': rib_name,
                            'trades': res['trades'],
                            'win_rate': res['win_rate'],
                            'profit_factor': res['pf'],
                            'net_r': res['net_r'],
                            'annualized_net_r': res['annualized_net_r'],
                            'max_dd_r': res['max_dd_r'],
                            'calmar_ratio': res['calmar_ratio'],
                            'quality_ratio': res['quality_ratio'],
                            'avg_r': res['avg_r'],
                            'total_days': res['total_days']
                        })
                        
    elapsed = time.time() - start_time
    print(f"Completed {len(all_simulations)} backtest simulations across Delta Exchange in {elapsed:.1f}s.")
    
    df_all = pd.DataFrame(all_simulations)
    master_csv = os.path.join(AUDIT_DIR, "delta_full_master_audit.csv")
    df_all.to_csv(master_csv, index=False)
    print(f"Master audit database saved to {master_csv}")
    
    # Filter profitable assets
    pos_df = df_all[df_all['net_r'] > 0].copy()
    print(f"Total profitable setups found: {len(pos_df)}")
    
    # Leaderboard by Calmar Ratio (primary) and Quality Ratio (secondary)
    idx_best = pos_df.groupby('symbol')['calmar_ratio'].idxmax()
    leaderboard = pos_df.loc[idx_best].sort_values('calmar_ratio', ascending=False).reset_index(drop=True)
    
    leaderboard_csv = os.path.join(AUDIT_DIR, "delta_calmar_leaderboard.csv")
    leaderboard.to_csv(leaderboard_csv, index=False)
    print(f"Calmar leaderboard saved to {leaderboard_csv}")
    
    print("\n" + "="*125)
    print("TOP 35 DELTA EXCHANGE ASSETS RANKED BY CALMAR RATIO (EXACT MT5 QUANT ENGINE)")
    print("="*125)
    print(leaderboard[['symbol', 'timeframe', 'strategy', 'ribbon', 'trades', 'win_rate', 'profit_factor', 'net_r', 'max_dd_r', 'annualized_net_r', 'calmar_ratio']].head(35).to_string(index=False))

if __name__ == '__main__':
    main()
