import os
import glob
import pandas as pd
import numpy as np
from delta_quant_optimizer import backtest_asset

DELTA_DIR = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Exchange"

RIBBONS = {
    'Prime_21_55_144': (21, 55, 144),
    'Prime_34_89_233': (34, 89, 233),
    'Prime_55_89_233': (55, 89, 233),
    'Classic_50_100_200': (50, 100, 200)
}

EXITS = ['trail_ema89', 'trail_ema55', 'fixed_2.5r_be1r', 'asymmetric_step']

def main():
    csv_1h_files = glob.glob(os.path.join(DELTA_DIR, "*_1h.csv"))
    csv_4h_files = glob.glob(os.path.join(DELTA_DIR, "*_4h.csv"))
    
    print(f"Found {len(csv_1h_files)} 1H files and {len(csv_4h_files)} 4H files.")
    
    all_results = []
    
    # 1. Sweep all combinations
    for tf_label, file_list in [('1H', csv_1h_files), ('4H', csv_4h_files)]:
        for fpath in file_list:
            fname = os.path.basename(fpath)
            symbol = fname.split('_')[0]
            
            for ribbon_name, ribbon_tuple in RIBBONS.items():
                for exit_name in EXITS:
                    res = backtest_asset(fpath, ribbon_tuple, exit_name)
                    if res and res['trades_count'] >= 10:
                        all_results.append({
                            'symbol': symbol,
                            'timeframe': tf_label,
                            'ribbon': ribbon_name,
                            'exit_type': exit_name,
                            'trades': res['trades_count'],
                            'win_rate': res['win_rate'],
                            'profit_factor': res['profit_factor'],
                            'net_r': res['net_r'],
                            'max_dd_r': res['max_dd_r'],
                            'quality_ratio': res['quality_ratio'],
                            'avg_r': res['avg_r_per_trade'],
                            'avg_bars': res['avg_hold_bars']
                        })
                        
    df_res = pd.DataFrame(all_results)
    print(f"\nTotal simulations executed: {len(df_res)}")
    
    # Save raw master simulation results
    out_csv = os.path.join(DELTA_DIR, "delta_master_optimization_results.csv")
    df_res.to_csv(out_csv, index=False)
    print(f"Master simulation results saved to {out_csv}")
    
    # Compare Ribbons across all assets
    print("\n" + "="*70)
    print("RIBBON CONFIGURATION COMPARISON (AGGREGATE ACROSS DELTA ASSETS)")
    print("="*70)
    ribbon_summary = df_res.groupby('ribbon').agg({
        'net_r': 'mean',
        'profit_factor': 'mean',
        'win_rate': 'mean',
        'quality_ratio': 'mean',
        'trades': 'mean'
    }).reset_index()
    print(ribbon_summary.to_string(index=False))
    
    # Compare Exits across all assets
    print("\n" + "="*70)
    print("EXIT STRATEGY COMPARISON (AGGREGATE ACROSS DELTA ASSETS)")
    print("="*70)
    exit_summary = df_res.groupby('exit_type').agg({
        'net_r': 'mean',
        'profit_factor': 'mean',
        'win_rate': 'mean',
        'quality_ratio': 'mean'
    }).reset_index()
    print(exit_summary.to_string(index=False))
    
    # Compare Timeframes
    print("\n" + "="*70)
    print("TIMEFRAME COMPARISON (1H vs 4H)")
    print("="*70)
    tf_summary = df_res.groupby('timeframe').agg({
        'net_r': 'mean',
        'profit_factor': 'mean',
        'win_rate': 'mean',
        'quality_ratio': 'mean',
        'trades': 'mean'
    }).reset_index()
    print(tf_summary.to_string(index=False))
    
    # Best setup per asset
    print("\n" + "="*70)
    print("TOP PERFORMING DELTA EXCHANGE ASSETS (RANKED BY NET R & QUALITY)")
    print("="*70)
    
    # Group by symbol and find the best performing parameter set for each
    idx_best = df_res.groupby('symbol')['quality_ratio'].idxmax()
    best_per_asset = df_res.loc[idx_best].sort_values('quality_ratio', ascending=False).reset_index(drop=True)
    
    best_csv = os.path.join(DELTA_DIR, "delta_best_per_asset.csv")
    best_per_asset.to_csv(best_csv, index=False)
    
    print(best_per_asset[['symbol', 'timeframe', 'ribbon', 'exit_type', 'trades', 'win_rate', 'profit_factor', 'net_r', 'max_dd_r', 'quality_ratio']].head(30).to_string(index=False))

if __name__ == '__main__':
    main()
