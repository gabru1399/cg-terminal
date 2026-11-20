import MetaTrader5 as mt5
import pandas as pd
import numpy as np

mt5.initialize()

print("="*100)
print("QUANTITATIVE SPREAD & MARKET INCONSISTENCY EXPLORATION — BLUEBERRY MT5")
print("="*100)

# 1. Spread Analysis across Assets
symbols = [
    'EURUSD.pi', 'GBPUSD.pi', 'AUDUSD.pi', 'NZDUSD.pi', 'USDCAD.pi', 'USDCHF.pi', 'USDJPY.pi',
    'EURJPY.pi', 'GBPJPY.pi', 'EURGBP.pi', 'AUDCAD.pi', 'CHFJPY.pi',
    'XAUUSD.pi', 'XAGUSD.pi', 'BTCUSD.pi', 'ETHUSD.pi', 'SOLUSD.p', 'BNBUSD.p',
    'USWTI.p', 'UKBrent.p', 'NDX100.pi', 'US30.pi', 'US500.pi'
]

spread_data = []
for s in symbols:
    info = mt5.symbol_info(s)
    tick = mt5.symbol_info_tick(s)
    if info and tick:
        spread_pts = info.spread
        point = info.point
        spread_cash = spread_pts * point
        mid = (tick.bid + tick.ask) / 2.0
        spread_pct = (spread_cash / mid) * 100 if mid > 0 else 0
        spread_data.append({
            'symbol': s,
            'bid': tick.bid,
            'ask': tick.ask,
            'spread_pts': spread_pts,
            'point': point,
            'spread_cost': round(spread_cash, 5),
            'spread_bps': round(spread_pct * 100, 2), # basis points
            'trade_mode': info.trade_mode,
            'freeze_level': info.trade_freeze_level,
            'stops_level': info.trade_stops_level
        })

df_spread = pd.DataFrame(spread_data).sort_values(by='spread_bps')
print("\n--- 1. BROKER SPREAD FRICTION MATRIX (Sorted by Basis Points) ---")
print(df_spread[['symbol', 'bid', 'ask', 'spread_pts', 'spread_bps', 'stops_level']].to_string(index=False))

# 2. Triangular Inconsistency Check
print("\n--- 2. TRIANGULAR ARBITRAGE INCONSISTENCY CHECK ---")
triangles = [
    ('EURUSD.pi', 'USDJPY.pi', 'EURJPY.pi'), # EUR/USD * USD/JPY = EUR/JPY
    ('GBPUSD.pi', 'USDJPY.pi', 'GBPJPY.pi'), # GBP/USD * USD/JPY = GBP/JPY
    ('EURGBP.pi', 'GBPUSD.pi', 'EURUSD.pi'), # EUR/GBP * GBP/USD = EUR/USD
]

for leg1, leg2, cross in triangles:
    t1 = mt5.symbol_info_tick(leg1)
    t2 = mt5.symbol_info_tick(leg2)
    tc = mt5.symbol_info_tick(cross)
    if t1 and t2 and tc:
        # Synthetic Bid = Bid1 * Bid2; Synthetic Ask = Ask1 * Ask2
        if 'EURGBP' in leg1:
            synth_bid = t1.bid * t2.bid
            synth_ask = t1.ask * t2.ask
        else:
            synth_bid = t1.bid * t2.bid
            synth_ask = t1.ask * t2.ask
            
        cross_bid = tc.bid
        cross_ask = tc.ask
        
        # Arbitrage 1: Buy Synthetic, Sell Cross -> Needs Synth_Ask < Cross_Bid
        arb1 = cross_bid - synth_ask
        # Arbitrage 2: Buy Cross, Sell Synthetic -> Needs Cross_Ask < Synth_Bid
        arb2 = synth_bid - cross_ask
        
        print(f"Triangle ({leg1} x {leg2} vs {cross}):")
        print(f"  Synthetic Quote: [{synth_bid:.5f} / {synth_ask:.5f}]")
        print(f"  Direct Cross:    [{cross_bid:.5f} / {cross_ask:.5f}]")
        print(f"  Arb 1 (Cross Bid - Synth Ask): {arb1:+.5f} (Profitable if > 0)")
        print(f"  Arb 2 (Synth Bid - Cross Ask): {arb2:+.5f} (Profitable if > 0)")
        print(f"  Spread Friction Buffer: {synth_ask - synth_bid + cross_ask - cross_bid:.5f}")
        print()

# 3. Cointegration / Statistical Pair Spread (WTI vs Brent)
print("--- 3. STATISTICAL SPREAD (COMMODITY PAIR: WTI vs BRENT) ---")
wti_tick = mt5.symbol_info_tick('USWTI.p')
brent_tick = mt5.symbol_info_tick('UKBrent.p')
if wti_tick and brent_tick:
    diff = brent_tick.bid - wti_tick.ask
    print(f"Live Brent - WTI Crack Spread: ${diff:.3f} USD (Brent: {brent_tick.bid}, WTI: {wti_tick.ask})")

mt5.shutdown()
