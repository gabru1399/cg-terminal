import os
import pandas as pd
import numpy as np
from test_calibrated_baskets import get_asset_trades

DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"

def simulate_fixed_vs_compounding(assets_df, initial_capital=5000.0, max_concurrent=6):
    all_trades = []
    for _, row in assets_df.iterrows():
        t_list = get_asset_trades(row['symbol'], row['timeframe'], row['ribbon'], row['exit_type'])
        all_trades.extend(t_list)
        
    all_trades.sort(key=lambda x: x['entry_ts'])
    
    results = {}
    
    # 1. Fixed Risk 0.5% ($25 / trade)
    for risk_label, fixed_dollar, pct_risk in [
        ('Fixed $25 (0.5%)', 25.0, None),
        ('Fixed $50 (1.0%)', 50.0, None),
        ('Compounding 0.5%', None, 0.005),
        ('Compounding 1.0%', None, 0.01)
    ]:
        equity = initial_capital
        active_positions = []
        executed = []
        eq_curve = [(all_trades[0]['entry_ts'], equity)]
        
        for t in all_trades:
            t_entry = t['entry_ts']
            active_positions = [pos for pos in active_positions if pos['exit_ts'] > t_entry]
            if len(active_positions) >= max_concurrent:
                continue
                
            dollar_risk = fixed_dollar if fixed_dollar is not None else equity * pct_risk
            pnl = dollar_risk * t['r_mult']
            fee = dollar_risk * 0.04
            net_pnl = pnl - fee
            equity += net_pnl
            eq_curve.append((t['exit_ts'], equity))
            executed.append(t)
            active_positions.append(t)
            
        df_exec = pd.DataFrame(executed)
        wins = df_exec[df_exec['r_mult'] > 0]
        total_days = (df_exec['exit_ts'].max() - df_exec['entry_ts'].min()) / 86400.0
        
        eq_vals = [pt[1] for pt in eq_curve]
        cummax = np.maximum.accumulate(eq_vals)
        dd = (cummax - eq_vals) / cummax
        max_dd_pct = np.max(dd) * 100.0
        
        profit = equity - initial_capital
        daily_usd = profit / max(total_days, 1.0)
        daily_inr = daily_usd * 87.0
        
        results[risk_label] = {
            'trades': len(df_exec),
            'win_rate': len(wins) / len(df_exec) * 100.0,
            'final_equity': equity,
            'profit': profit,
            'roi_pct': (profit / initial_capital) * 100.0,
            'max_dd_pct': max_dd_pct,
            'daily_usd': daily_usd,
            'daily_inr': daily_inr,
            'total_days': total_days
        }
    return results

def main():
    best_df = pd.read_csv(os.path.join(DELTA_DIR, "delta_best_per_asset.csv"))
    pos_df = best_df[best_df['net_r'] > 0].copy()
    
    b20 = pos_df.head(20)
    
    print("=" * 115)
    print("SIMULATION ON TOP 20 DELTA EXCHANGE WEALTH BASKET ($5,000 CAPITAL)")
    print("=" * 115)
    print(f"{'Risk Model':<20} | {'Trades':<7} | {'Win %':<6} | {'Final Eq ($)':<14} | {'Net Profit ($)':<14} | {'ROI %':<10} | {'Max DD %':<8} | {'$/Day':<8} | {'₹/Day'}")
    print("-" * 115)
    
    res = simulate_fixed_vs_compounding(b20, initial_capital=5000.0, max_concurrent=6)
    for model, d in res.items():
        feq = f"${d['final_equity']:,.2f}"
        nprof = f"${d['profit']:,.2f}"
        roi = f"{d['roi_pct']:+,.1f}%"
        mdd = f"{d['max_dd_pct']:.1f}%"
        d_usd = f"${d['daily_usd']:.2f}"
        d_inr = f"₹{d['daily_inr']:,.0f}"
        print(f"{model:<20} | {d['trades']:<7} | {d['win_rate']:<6.1f} | {feq:<14} | {nprof:<14} | {roi:<10} | {mdd:<8} | {d_usd:<8} | {d_inr}")

if __name__ == '__main__':
    main()
