import os
import pandas as pd
import numpy as np
from test_calibrated_baskets import get_asset_trades

trades = get_asset_trades('CBRSBUSD', '1H', 'Prime_21_55_144', 'trail_ema55')
df = pd.DataFrame(trades)
print("CBRSBUSD trades count:", len(df))
print(df.sort_values('r_mult', ascending=False).head(5))

# Let's inspect the raw candle for trade #18
fpath = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange\CBRSBUSD_1h.csv"
candles = pd.read_csv(fpath)
print("\nFirst few candles of CBRSBUSD:")
print(candles.head(10))
