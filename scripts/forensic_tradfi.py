import MetaTrader5 as mt5
import pandas as pd
import numpy as np

mt5.initialize()
pairs = ['GBPUSD.pi', 'EURUSD.pi', 'USDJPY.pi', 'XAUUSD.pi', 'XRPUSD.pi', 'BTCUSD.pi', 'ETHUSD.pi', 'SOLUSD.p']
for p in pairs:
    rates = mt5.copy_rates_from_pos(p, mt5.TIMEFRAME_M15, 0, 100)
    if rates is None or len(rates) == 0:
        continue
    df = pd.DataFrame(rates)
    e13 = df['close'].ewm(span=13).mean().iloc[-1]
    e89 = df['close'].ewm(span=89).mean().iloc[-1]
    e233 = df['close'].ewm(span=233).mean().iloc[-1]
    tr = np.maximum(df['high'] - df['low'], np.maximum(abs(df['high'] - df['close'].shift(1)), abs(df['low'] - df['close'].shift(1))))
    atr14 = tr.rolling(14).mean().iloc[-1]
    tick = mt5.symbol_info_tick(p)
    trend = "BEAR" if (e13 < e89 and e89 < e233) else ("BULL" if (e13 > e89 and e89 > e233) else "MIXED")
    print(f"{p:<12} | Bid={tick.bid:<9} | Ask={tick.ask:<9} | E13={e13:<9.4f} | E89={e89:<9.4f} | ATR14={atr14:<8.4f} | Trend={trend}")
mt5.shutdown()
