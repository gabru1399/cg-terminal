import os
import pandas as pd
import numpy as np
from delta_portfolio_simulator import run_event_driven_portfolio

baskets = {
    'Basket_10_Core': [
        'QQQXUSD', 'MUBUSD', 'METAXUSD', 'SLVONUSD', 'BTCUSD',
        'LTCUSD', 'AVAXUSD', 'NVDAXUSD', 'XAUTUSD', 'OILUSD'
    ],
    'Basket_15_Institutional_Alpha': [
        'QQQXUSD', 'MUBUSD', 'METAXUSD', 'NVDAXUSD', 'AMDBUSD',
        'SLVONUSD', 'XAUTUSD', 'OILUSD', 'BTCUSD', 'LTCUSD',
        'AVAXUSD', 'SOPHUSD', 'HUSD', 'AIOTUSD', 'BERAUSD'
    ],
    'Basket_20_Elite_Wealth': [
        'QQQXUSD', 'MUBUSD', 'METAXUSD', 'NVDAXUSD', 'AMDBUSD',
        'SLVONUSD', 'XAUTUSD', 'OILUSD', 'BTCUSD', 'LTCUSD',
        'AVAXUSD', 'SOPHUSD', 'HUSD', 'AIOTUSD', 'BERAUSD',
        'CBRSBUSD', 'PIEVERSEUSD', 'ARIAUSD', 'INITUSD', 'BMTUSD'
    ],
    'Basket_25_Max_Diversification': [
        'QQQXUSD', 'MUBUSD', 'METAXUSD', 'NVDAXUSD', 'AMDBUSD',
        'MSTRBUSD', 'SLVONUSD', 'XAUTUSD', 'OILUSD', 'BTCUSD',
        'LTCUSD', 'AVAXUSD', 'BNBUSD', 'INJUSD', 'SOPHUSD',
        'HUSD', 'AIOTUSD', 'BERAUSD', 'CBRSBUSD', 'PIEVERSEUSD',
        'ARIAUSD', 'INITUSD', 'BMTUSD', 'VVVUSD', 'GRIFFAINUSD'
    ]
}

print(f"{'Basket Name':<30} | {'Risk':<5} | {'Trades':<7} | {'Win %':<6} | {'Final Eq ($)':<12} | {'ROI %':<8} | {'Max DD %':<8} | {'$/Day':<7} | {'₹/Day'}")
print("-" * 110)

for bname, syms in baskets.items():
    for r_pct in [0.005, 0.01]:
        res = run_event_driven_portfolio(
            selected_symbols=syms,
            tf='1h',
            ribbon=(34, 89, 233),
            exit_type='trail_ema89',
            initial_capital=5000.0,
            risk_pct=r_pct,
            max_concurrent=6
        )
        if res:
            r_label = f"{r_pct*100:.1f}%"
            final_eq = f"${res['final_equity']:,.2f}"
            roi = f"{res['total_return_pct']:+.1f}%"
            mdd = f"{res['max_dd_pct']:.1f}%"
            d_usd = f"${res['daily_avg_dollar']:.2f}"
            d_inr = f"₹{res['daily_avg_inr']:,.0f}"
            print(f"{bname:<30} | {r_label:<5} | {res['total_trades']:<7} | {res['win_rate']:<6.1f} | {final_eq:<12} | {roi:<8} | {mdd:<8} | {d_usd:<7} | {d_inr}")
