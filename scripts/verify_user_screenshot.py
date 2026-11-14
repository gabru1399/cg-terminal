import os
import pandas as pd
import numpy as np

fpath = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange\LINKUSD_4h.csv"
if not os.path.exists(fpath):
    fpath = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange\LINKUSD_1h.csv"

df = pd.read_csv(fpath)
closes = df['close']
ema89 = closes.ewm(span=89, adjust=False).mean()
ema233 = closes.ewm(span=233, adjust=False).mean()

# Check: In MT5 logic, for a SHORT to be valid:
# ema89 must be STRICTLY LESS THAN ema233!
df['ema89'] = ema89
df['ema233'] = ema233
df['regime_short_allowed'] = df['ema89'] < df['ema233']
df['regime_long_allowed'] = df['ema89'] > df['ema233']

# Find rows where price was around 11.800 and 11.146
target_rows = df[(df['close'] >= 10.5) & (df['close'] <= 13.5)]
print(f"Total bars matching price range: {len(target_rows)}")
sample = target_rows.tail(10)
print(sample[['datetime', 'close', 'ema89', 'ema233', 'regime_short_allowed', 'regime_long_allowed']])
