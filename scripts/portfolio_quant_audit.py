import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timezone

mt5.initialize()
acc = mt5.account_info()
positions = mt5.positions_get()

print("="*105)
print(f"JANE STREET / CITADEL STYLE PORTFOLIO RISK AUDIT — BLUEBERRY MARKETS (LOGIN: {acc.login})")
print(f"Balance: ${acc.balance:,.2f} | Equity: ${acc.equity:,.2f} | Margin: ${acc.margin:,.2f} | Free Margin: ${acc.margin_free:,.2f}")
print(f"Total Floating PnL: ${acc.equity - acc.balance:+,.2f} USD | Phase 1 Distance ($2,700): ${2700.0 - acc.equity:,.2f} USD")
print("="*105)

records = []
now = datetime.now(timezone.utc).timestamp()

for p in positions:
    dur = (now - p.time) / 3600.0
    sym_info = mt5.symbol_info(p.symbol)
    point = sym_info.point if sym_info else 0.00001
    digits = sym_info.digits if sym_info else 5
    spread_pts = sym_info.spread if sym_info else 0
    
    # Distance to SL & TP
    if p.type == 0: # BUY
        dist_sl_pts = (p.price_current - p.sl) / point if p.sl > 0 else 0
        dist_tp_pts = (p.tp - p.price_current) / point if p.tp > 0 else 0
        pnl_pts = (p.price_current - p.price_open) / point
    else: # SELL
        dist_sl_pts = (p.sl - p.price_current) / point if p.sl > 0 else 0
        dist_tp_pts = (p.price_current - p.tp) / point if p.tp > 0 else 0
        pnl_pts = (p.price_open - p.price_current) / point

    # Ownership
    owner = "CG_TERMINAL" if (p.magic == 42001 or p.comment == "cg_terminal") else "ALPHA_FIBONACCI"
    
    # Recommendation logic
    rec = "HOLD"
    if p.profit > 5.0 and dist_tp_pts < 150:
        rec = "PROTECT_TRAIL_TP_NEAR"
    elif "GBPNOK" in p.symbol and p.profit < 0:
        rec = "PRUNE_EXOTIC_BLEED"
    elif "CHFJPY" in p.symbol and p.profit < -1.0:
        rec = "PRUNE_ADVERSE_TREND"
    elif p.symbol == "EURUSD.pi" and p.type == 0 and p.profit < 0:
        rec = "PRUNE_COUNTER_TREND_BUY"
    elif p.profit > 1.0:
        rec = "HOLD_WINNER"
    elif p.profit < -1.0:
        rec = "MONITOR_SL"

    records.append({
        'ticket': p.ticket,
        'sym': p.symbol,
        'side': 'BUY' if p.type == 0 else 'SELL',
        'vol': p.volume,
        'open': p.price_open,
        'cur': p.price_current,
        'sl': p.sl,
        'tp': p.tp,
        'pnl_$': round(p.profit, 2),
        'pnl_pts': round(pnl_pts, 0),
        'dist_tp_pts': round(dist_tp_pts, 0),
        'dur_h': round(dur, 1),
        'owner': owner,
        'recommendation': rec
    })

df = pd.DataFrame(records)
df = df.sort_values(by='pnl_$', ascending=False)
print(df.to_string(index=False))

print("\n" + "="*105)
print("AGGREGATE EXPOSURE & SCENARIO ANALYSIS:")
# Sum by owner
cg_pnl = df[df['owner'] == 'CG_TERMINAL']['pnl_$'].sum()
alpha_pnl = df[df['owner'] == 'ALPHA_FIBONACCI']['pnl_$'].sum()
print(f"CG-Terminal Desk PnL: ${cg_pnl:+,.2f} USD ({len(df[df['owner'] == 'CG_TERMINAL'])} pos)")
print(f"Alpha-Fibonacci Desk PnL: ${alpha_pnl:+,.2f} USD ({len(df[df['owner'] == 'ALPHA_FIBONACCI'])} pos)")

# Toxic prune scenario
toxic_mask = df['recommendation'].str.startswith('PRUNE')
toxic_pnl = df[toxic_mask]['pnl_$'].sum()
toxic_tickets = df[toxic_mask]['ticket'].tolist()
print(f"\nToxic / Counter-trend Drag Positions: {len(toxic_tickets)} tickets | Drag: ${toxic_pnl:+,.2f} USD")
for _, r in df[toxic_mask].iterrows():
    print(f"  Ticket #{r['ticket']} {r['sym']} {r['side']} ({r['owner']}): ${r['pnl_$']} USD [{r['recommendation']}]")

post_prune_equity = acc.equity - toxic_pnl
print(f"\nIf Toxic Drag is Pruned: Immediate Margin Released: ~${len(toxic_tickets)*15:.2f} USD | Net PnL delta: ${toxic_pnl:+,.2f} USD")
print("="*105)

mt5.shutdown()
