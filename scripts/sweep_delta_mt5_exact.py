import os
import glob
import pandas as pd
import numpy as np
from test_delta_with_mt5_engine import simulate_mt5_exact

DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"

csv_4h = glob.glob(os.path.join(DELTA_DIR, "*_4h.csv"))
csv_1h = glob.glob(os.path.join(DELTA_DIR, "*_1h.csv"))

all_runs = []

for tf_label, file_list in [('4H', csv_4h), ('1H', csv_1h)]:
    for fpath in file_list:
        symbol = os.path.basename(fpath).split('_')[0]
        df = pd.read_csv(fpath)
        if len(df) < 300:
            continue
            
        for mode in ['fixed_2.0', 'fixed_2.5', 'step_trail', 'trail_89', 'trail_55']:
            for rib_name, f_p, m_p, s_p in [
                ('Fib_89_233', 55, 89, 233),
                ('Fib_34_89', 34, 89, 233),
                ('Fib_21_55', 21, 55, 144),
                ('Classic_50_200', 50, 100, 200)
            ]:
                res = simulate_mt5_exact(df, f_p, m_p, s_p, exit_mode=mode)
                if res and res['trades'] >= 15:
                    all_runs.append({
                        'symbol': symbol,
                        'tf': tf_label,
                        'strategy': mode,
                        'ribbon': rib_name,
                        'trades': res['trades'],
                        'win_rate': res['win_rate'],
                        'pf': res['pf'],
                        'net_r': res['net_r'],
                        'avg_r': res['avg_r'],
                        'max_dd_r': res['max_dd_r'],
                        'quality_ratio': round(res['net_r'] / max(res['max_dd_r'], 1.0), 2)
                    })

df_runs = pd.DataFrame(all_runs)
print(f"Total simulations completed: {len(df_runs)}")

# Filter profitable
pos_runs = df_runs[df_runs['net_r'] > 0].copy()
print(f"Profitable setups: {len(pos_runs)}")

# Best setup per symbol by Quality Ratio
idx_best = pos_runs.groupby('symbol')['quality_ratio'].idxmax()
best_df = pos_runs.loc[idx_best].sort_values('quality_ratio', ascending=False).reset_index(drop=True)

out_path = os.path.join(DELTA_DIR, "delta_mt5_exact_best_universe.csv")
best_df.to_csv(out_path, index=False)

print("\n" + "="*115)
print("TOP 30 DELTA EXCHANGE ASSETS USING THE EXACT MT5 QUANT ENGINE")
print("="*115)
print(best_df[['symbol', 'tf', 'strategy', 'ribbon', 'trades', 'win_rate', 'pf', 'net_r', 'max_dd_r', 'quality_ratio']].head(30).to_string(index=False))
