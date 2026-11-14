import os
import sys
import pandas as pd

sys.path.append(r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Fibonacci_Institutional_Business\engine")
from simulate_business_portfolio import simulate_portfolio

LEADERBOARD_PATH = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Fibonacci_Institutional_Business\audit\delta_calmar_leaderboard.csv"
df = pd.read_csv(LEADERBOARD_PATH)

# Select top 20 diversified assets by Calmar Ratio
top20 = df.head(20)

print("=" * 115)
print("UNIFIED PORTFOLIO SIMULATION: TOP 20 CALMAR WEALTH BASKET ($5,000 CAPITAL)")
print("=" * 115)
print(f"{'Risk Model':<20} | {'Trades':<7} | {'Win %':<6} | {'Final Eq ($)':<14} | {'Net Profit ($)':<14} | {'ROI %':<10} | {'Max DD %':<8} | {'Calmar':<8} | {'$/Day':<8} | {'₹/Day'}")
print("-" * 125)

results = simulate_portfolio(top20, initial_capital=5000.0, max_concurrent=6)
for model, d in results.items():
    feq = f"${d['final_equity']:,.2f}"
    nprof = f"${d['profit']:,.2f}"
    roi = f"{d['roi_pct']:+,.1f}%"
    mdd = f"{d['max_dd_pct']:.1f}%"
    calmar = f"{d['calmar_ratio']:.2f}"
    d_usd = f"${d['daily_usd']:.2f}"
    d_inr = f"₹{d['daily_inr']:,.0f}"
    print(f"{model:<20} | {d['trades']:<7} | {d['win_rate']:<6.1f} | {feq:<14} | {nprof:<14} | {roi:<10} | {mdd:<8} | {calmar:<8} | {d_usd:<8} | {d_inr}")

# Also print monthly income
print("\n" + "="*85)
print("PROJECTED MONTHLY REVENUE (INDIA RESIDENT ON DELTA EXCHANGE)")
print("="*85)
for model, d in results.items():
    m_usd = f"${d['monthly_usd']:,.2f}/mo"
    m_inr = f"₹{d['monthly_inr']:,.0f}/mo"
    print(f"{model:<22} -> {m_usd:<18} ({m_inr}) | Max Drawdown: {d['max_dd_pct']}% | Calmar: {d['calmar_ratio']}")
