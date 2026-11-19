#!/usr/bin/env python3
"""R550 Tri-Council hurdle enforcement on the four deep-dived candidates.
All figures from THIS round's MCP responses (10:33-10:40 UTC window)."""

# ---------------- XAG SHORT (silver, MT5 XAGUSD + Delta XAGUSD perps) ----------------
# telemetry: px 45.35 · day VWAP 45.36 (+1σ 45.65, +2σ 45.94, +3σ 46.22)
# narrative: TREND_DOWN M1 SHORT grade B conf 92, zone 45.177-45.383, stop 45.935, T1 44.934
# trend: m15/h1/h4/d1 ALL BEAR (13<89 every TF) · below day VWAP
# liq: shorts(above) $29.2M vs longs(below) $8.75M -> 3.34:1 skew favors SHORT
# whales: bid shelf $6.5M@45.0 + $6.2M@44.8 + $5.8M@45.2 vs ask $7.3M@45.5 — target INTO bids
# footprint @ zone: BULL abs @45.38 (07:45) + BULL divs — COUNTER to short -> factor 3 capped at 1.0
xag = {
    "entry": 45.30,       # mid of engine zone 45.177-45.383, below ask wall 45.5
    "stop": 46.00,        # beyond +3σ 46.22? NO -> beyond engine structural 45.935 + sweep of 46.27 str-100 magnet
    "t1": 45.00,          # into the $6.5M bid wall (sweep)
    "t2": 44.44,          # long-liq cluster str 72 shelf 44.25-44.44
    "spread_pts": 0.03,   # XAGUSD.p typical 2-3c spread (user-quoted 2¢-10¢ band on metals)
    "score": {"1_trend_all_TF_BEAR": 2.0, "2_below_VWAP_discount": 1.5, "3_footprint_counter_bull_abs": 1.0,
              "4_no_bid_backstop_for_short": 0.0, "5_cvd_not_checked": 0.0, "6_liq_skew_3.34_to_1": 1.5,
              "7_gex_na": 0.0, "8_spread_0.03_on_0.70_stop": 1.0},
    "sl_dist": None, "risk_basis": None,
}
xag["sl_dist"] = xag["stop"] - xag["entry"]           # 0.70
xag["t1_R"] = (xag["entry"] - xag["t1"]) / xag["sl_dist"]
xag["t2_R"] = (xag["entry"] - xag["t2"]) / xag["sl_dist"]
xag["score_total"] = sum(xag["score"].values())
xag["spread_pct"] = xag["spread_pts"] / xag["sl_dist"] * 100
# sizing: $6 cap, 0.01 lot = 50 oz XAG -> $/pt = 0.50 per 0.01 lot
xag["lots_for_6usd"] = 6.0 / (xag["sl_dist"] * 50 * 1.2)  # 1.20x slippage stress
print("XAG SHORT (MT5 XAGUSD.p):")
print(f"  Table 7 = {xag['score_total']:.1f} -> {'A' if xag['score_total']>=7 else 'B' if xag['score_total']>=5 else 'NO'}")
print(f"  R to T1 {xag['t1_R']:.2f} · R to T2 {xag['t2_R']:.2f} (floor 2.00)")
print(f"  spread drag {xag['spread_pct']:.1f}% of stop (cap 5.0%)")
print(f"  sizing: {xag['lots_for_6usd']:.3f} lots of 0.01 steps (incl 1.2x slippage) -> "
      f"{'0.01 OK' if xag['lots_for_6usd']>=0.01 else 'MIN LOT BREACH'} risk @0.01 lot = ${xag['sl_dist']*50*1.2:.2f}")

# ---------------- XAU SHORT (gold; engine bias -5 TRANSIENT) ----------------
# px 3740.21 · VWAP 3737.06 (z +0.22, |z|<1 premium-lite) · h4/d1 BEAR, m15/h1 BEAR
# whales: ASK stack 3744-3753 $16.8M (6 walls) vs bids $11.5M mostly deep (3333)
# liq: shorts above $1.06M vs longs below $275k -> 3.84:1 skew favors SHORT (gold perp venues)
# footprint: none fresh at zone this round (no HIGH events) -> factor 3 = 0
xau = {
    "entry": 3748.0,      # inside the ask-wall cluster 3744-3753 (fade into the stack)
    "stop": 3766.5,       # beyond +2σ 3766.06 and above the wall shelf high 3753
    "t1": 3727.8,         # day VAL 3727.79
    "t2": 3698.7,         # long-liq shelf 3694-3699 (str 70-78)
    "spread_pts": 0.35,   # XAUUSD.pi ~35c typical
    "score": {"1_trend_h4_d1_BEAR": 2.0, "2_premium_z0.22": 1.5, "3_no_fresh_footprint": 0.0,
              "4_ask_wall_backstop": 1.5, "5_cvd_not_checked": 0.0, "6_liq_skew_3.84_to_1": 1.5,
              "7_gex_na_metal": 0.0, "8_spread_ok": 1.0},
}
xau["sl_dist"] = xau["stop"] - xau["entry"]
xau["t1_R"] = (xau["entry"] - xau["t1"]) / xau["sl_dist"]
xau["t2_R"] = (xau["entry"] - xau["t2"]) / xau["sl_dist"]
xau["score_total"] = sum(xau["score"].values())
xau["spread_pct"] = xau["spread_pts"] / xau["sl_dist"] * 100
xau["lots_for_6usd"] = 6.0 / (xau["sl_dist"] * 100 * 1.2)  # 0.01 lot = 1 oz -> $1/pt per 0.01... wait 1 oz = $1/pt
print("\nXAU SHORT (MT5 XAUUSD.pi):")
print(f"  Table 7 = {xau['score_total']:.1f} -> {'A' if xau['score_total']>=7 else 'B' if xau['score_total']>=5 else 'NO'}")
print(f"  R to T1 {xau['t1_R']:.2f} · R to T2 {xau['t2_R']:.2f} (floor 2.00)")
print(f"  spread drag {xau['spread_pct']:.1f}% (cap 5.0%)")
print(f"  sizing: {xau['lots_for_6usd']:.3f} lots (0.01 steps, 1.2x stress) risk @0.01 = ${xau['sl_dist']*1*1.2:.2f}")

# ---------------- BNB SHORT (refresh of resting #20240006) ----------------
# px 591.15 vs resting entry 593.5 · h1/h4/d1 BEAR, m15 BULL (counter)
# footprint: BEAR sdiv 09:00 + BEAR exh 09:00 + BEAR trap 10:16 + BEAR div 10:16 @ ~591
# CVD: bear div active (10:39 event) · whales: bid $1.6M@582 / $1.2M@587.5 vs ask $1.4M@596
# liq: longs below 573.6-574.6 str 77-83 ($8K est each) — magnets DOWN
bnb = {
    "entry": 593.5,       # existing resting level (VWAP+2σ 593.43 confluence)
    "stop": 601.1,        # existing (beyond +3σ 597.2 and ask wall 596)
    "t1": 582.0,          # into $1.6M bid wall (Gate)
    "t2": 574.6,          # long-liq shelf str 77-83
    "score": {"1_trend_h1_h4_d1_BEAR_m15_counter": 2.0, "2_premium_entry_VWAP2s": 1.5,
              "3_bear_sdiv_exh_trap_cluster": 2.0, "4_ask_wall_596_backstop": 1.0,
              "5_cvd_bear_div_active": 1.0, "6_liq_magnet_down_str77_83": 1.5,
              "7_gex_na": 0.0, "8_spread_na_mt5": 0.5},
}
bnb["sl_dist"] = bnb["stop"] - bnb["entry"]
bnb["t1_R"] = (bnb["entry"] - bnb["t1"]) / bnb["sl_dist"]
bnb["t2_R"] = (bnb["entry"] - bnb["t2"]) / bnb["sl_dist"]
bnb["score_total"] = sum(bnb["score"].values())
print("\nBNB SHORT (MT5 BNBUSD.p — resting #20240006 refresh):")
print(f"  Table 7 = {bnb['score_total']:.1f} -> {'A' if bnb['score_total']>=7 else 'B' if bnb['score_total']>=5 else 'NO'}")
print(f"  R to T1 {bnb['t1_R']:.2f} · R to T2 {bnb['t2_R']:.2f}")

# ---------------- SOL SHORT hedge-check (running position #20277826) ----------------
# px 74.53 · position short 0.07 @ 73.28 SL 74.06 — price ABOVE stop already: position at risk
# m15 EMA13>89 BULL flip + long-liq magnets BELOW (71.68-71.99) -> trend has turned against the short
print("\nSOL #20277826 (running): live 74.53 > SL 74.06 — the stop is INSIDE price action; m15 BULL.")
print("  Directive stands: tighten to structure or exit on next pullback <= 74.2; long-magnets 71.7-72.0 now target.")

# ---------------- BTC (context for PIT-03 gate on all shorts) ----------------
print("\nBTC macro filter: 63,807 (+1.2%), above day VWAP — altcoin SHORTS now anti-magnet (down-magnets 61.8-61.9k).")
print("  BTC itself: h4/d1 BEAR but price +1.2% — shorting here = fading a VWAP reclaim; PIT-03 CAUTION flag on all crypto shorts.")
