import MetaTrader5 as mt5
import pandas as pd
import os
from datetime import datetime

if not mt5.initialize():
    print(f"MT5 initialize failed: {mt5.last_error()}")
else:
    print("MT5 initialized successfully.")
    symbols = mt5.symbols_get()
    print(f"Total MT5 symbols: {len(symbols)}")
    mt5.shutdown()
