import os
import pandas as pd
import numpy as np
from test_calibrated_baskets import get_asset_trades

DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"

best_df = pd.read_csv(os.path.join(DELTA_DIR, "delta_best_per_asset.csv"))
pos_df = best_df[best_df['net_r'] > 0].copy()
b20 = pos_df.head(20)

all_trades = []
for _, row in b20.iterrows():
    t_list = get_asset_trades(row['symbol'], row['timeframe'], row['ribbon'], row['exit_type'])
    all_trades.extend(t_list)

df = pd.DataFrame(all_trades)
print(f"Total trades: {len(df)}")

# Breakdown of r_mult
losses_full = df[df['r_mult'] <= -0.9]
losses_small = df[(df['r_mult'] > -0.9) & (df['r_mult'] < 0)]
breakeven = df[df['r_mult'] == 0]
small_wins = df[(df['r_mult'] > 0) & (df['r_mult'] <= 1.0)]
medium_wins = df[(df['r_mult'] > 1.0) & (df['r_mult'] <= 3.0)]
large_wins = df[(df['r_mult'] > 3.0) & (df['r_mult'] <= 10.0)]
huge_wins = df[df['r_mult'] > 10.0]

print(f"Full Losses (-1.0R):     {len(losses_full)} ({len(losses_full)/len(df)*100:.1f}%)")
print(f"Partial Losses (< -0.1R): {len(losses_small)} ({len(losses_small)/len(df)*100:.1f}%)")
print(f"Exact Breakeven (0.0R):  {len(breakeven)} ({len(breakeven)/len(df)*100:.1f}%)")
print(f"Small Wins (0 to 1R):    {len(small_wins)} ({len(small_wins)/len(df)*100:.1f}%)")
print(f"Medium Wins (1R to 3R):  {len(medium_wins)} ({len(medium_wins)/len(df)*100:.1f}%)")
print(f"Large Wins (3R to 10R):  {len(large_wins)} ({len(large_wins)/len(df)*100:.1f}%)")
print(f"Huge Runners (> 10R):    {len(huge_wins)} ({len(huge_wins)/len(df)*100:.1f}%)")

print("\nTop 15 winning trades:")
print(df.sort_values('r_mult', ascending=False).head(15)[['symbol', 'r_mult']])
