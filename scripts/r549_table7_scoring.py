#!/usr/bin/env python3
"""R549 — Table 7 confluence scoring + gate checks for the three live candidates.
All numbers are pasted from MCP tool responses fetched this round (no caching)."""

# ---- shared context (fresh this round) ----
BTC = {
    "price": 63394.8, "day_vwap": 62855.70, "sd1": 206.61, "day_low": 62360.0,
    "liq_above_usd": 128.81e9, "liq_below_usd": 77.91e9,  # stopmap 24h
    "whale_ask": 11.6e6, "whale_ask_px": 63624.0, "whale_bid": 11.6e6, "whale_bid_px": 62696.0,  # Hyperliquid walls
}

SUI = {
    "price": 0.7285, "day_vwap": 0.72, "sd": None, "vwap_sigma": 2.46,  # narrative: 2.46σ stretch
    # auctions
    "day_poc": 0.72, "day_vah": 0.72, "day_val": 0.71, "month_val": 0.67,
    # footprint (fresh, 03:37): BULL abs @ 0.7201 (vol bars) + 03:55 BULL abs (15m high of bar)
    "absorption": ("BULL", 0.7201, "03:37 vol-bar + 03:55 15m"),
    # CVD: buy share 48.5%, both-selling quadrant, bear div active 01:00
    "cvd_buyshare": 48.5, "cvd_quadrant": "both-selling", "cvd_active_div": "bear@01:00",
    # whales: aggregate bids $3.5M vs asks $1.02B (imbalance -99.3%); near walls all ASK side
    "whale_bid_wall": None, "whale_ask_walls": [73380.73, 10.0, 8.9],
    # liq: above str 60 @ ~0.745; below str 100 @ ~0.700 (-3.58%)
    "liq_above": {"px": 0.75, "str": 60, "dist_pct": 2.58}, "liq_below": {"px": 0.70, "str": 100, "dist_pct": -3.58},
    "trend": "h4 BEAR, d1 BEAR (13<89 both)",
}

INJ = {
    "price": 7.02, "day_vwap": 6.93, "sd": None, "vwap_sigma": 1.55,
    "day_poc": 6.90, "day_vah": 6.97, "day_val": 6.82, "month_val": 7.26, "month_poc": 8.13,
    "footprint": "BULL div @ 6.811 (03:00 15m) + BULL abs @ 6.876 (23:00 yesterday)",  # only div-level, not at current px
    "cvd_buyshare": 49.5, "cvd_quadrant": None, "cvd_active_div": None,
    "whale_bid_wall": None, "whale_ask_walls": [33.99, 35.0],  # far-away asks, nothing near
    "liq_below": {"px": 6.802, "str": 100, "usd": 238805.07, "dist_pct": -3.01},
    "liq_above_nearest": {"px": 7.108, "str": 40.6, "usd": 96980.42, "dist_pct": 1.36},
    "trend": "h4 BEAR, d1 BULL (conflict)",
}

def score_sui_short():
    s = {}
    # 1 Directional trend: h4+d1 EMA13<89 aligned SHORT, but regime RANGE_BALANCE -> 0 per Table 7
    s["1_trend"] = 0.0
    # 2 Auction/VWAP: short in premium requires |z|<=1.0; z=+2.46 -> 0
    s["2_auction"] = 0.0
    # 3 Footprint: fresh BULL absorption (opposite direction) = 0 for a short; not even a bear div at entry
    s["3_footprint"] = 0.0
    # 4 Whale wall backstop: no bid wall to lean on for a short; massive ask O/I overhead is not an entry backstop
    s["4_whale"] = 0.0
    # 5 CVD: bear divergence active + both-selling -> supports short +1.0
    s["5_cvd"] = 1.0
    # 6 Liquidity magnet: skew for shorts? shorts(above) $139.5M < longs(below) $173.1M -> magnet is DOWN, against a short
    s["6_liq"] = 0.0
    # 7 GEX: not BTC/ETH -> n/a 0
    s["7_gex"] = 0.0
    # 8 spread/friction: n/a unmeasured this round on Delta CLOB for SUI -> 0 (no caching)
    s["8_spread"] = 0.0
    return s

def score_inj_long():
    s = {}
    # 1 trend: d1 BULL but h4 BEAR -> not aligned -> 0
    s["1_trend"] = 0.0
    # 2 auction: long in discount needs px<vwap |z|<=1; px 7.02 is ABOVE vwap 6.93 (z=+1.55) -> 0
    s["2_auction"] = 0.0
    # 3 footprint: bull div @ 6.811 at 03:00 (1h ago, <=8h recency) +1.0 (div, not abs/sdiv)
    s["3_footprint"] = 1.0
    # 4 whale: no bid wall anywhere near -> 0
    s["4_whale"] = 0.0
    # 5 CVD: no active divergence, buy share 49.5% neutral -> 0
    s["5_cvd"] = 0.0
    # 6 liq magnet: long cluster below (6.802 str100) is a DOWN magnet, not up; shorts above are thinner (7.108 str 40)
    #    skew does NOT favor a long into 7.1+ -> 0
    s["6_liq"] = 0.0
    s["7_gex"] = 0.0
    s["8_spread"] = 0.0
    return s

def score_btc_short_pullback():
    s = {}
    # 1 trend: h4 BEAR + d1 BEAR (13<89), regime not RANGE per narrative (WATCH_EXHAUSTION on SUI only) -> +2.0
    s["1_trend"] = 2.0
    # 2 auction: px 63,395 vs vwap 62,856 -> z = +2.61 -> premium but |z|>1 -> 0
    s["2_auction"] = 0.0
    # 3 footprint: no fresh BTC abs/sdiv at entry zone this round (no HIGH footprint event on BTC in feed) -> 0
    s["3_footprint"] = 0.0
    # 4 whale: ask wall $11.6M @ 63,624 (HL, fresh 03:56, age<1h table requires >1h) -> 0 (age fail)
    s["4_whale"] = 0.0
    # 5 CVD: not pulled for BTC this round -> 0
    s["5_cvd"] = 0.0
    # 6 liq magnet: stopmap above $128.8B vs below $77.9B -> skew favors LONG (up-magnet), against short -> 0
    s["6_liq"] = 0.0
    s["7_gex"] = 0.0  # not pulled
    s["8_spread"] = 0.0
    return s

for name, fn in [("SUI SHORT (fade 2.46σ)", score_sui_short), ("INJ LONG (sweep-magnet ride)", score_inj_long), ("BTC SHORT (trend pullback)", score_btc_short_pullback)]:
    s = fn()
    total = sum(s.values())
    grade = "A" if total >= 7.0 else ("B" if total >= 5.0 else "NO TRADE")
    print(f"\n{name}: Table 7 total = {total:.1f} -> {grade}")
    for k, v in s.items():
        print(f"  {k}: {v}")

# ---- EV checks (Grade A required EV>=2.0R) ----
print("\n-- EV (R-multiple to first target) --")
print("SUI short: entry ~0.7285, structural stop above day high 0.7269/absorption high 0.7286 (invalid for short)")
print("  -> no valid structural stop BELOW a short entry at market; a fade limit needs a wall/level: none -> EV not computable")
print("INJ long: entry would be 6.93-6.97 (VAH/POC retest); stop below 6.81 cluster edge; T1 7.108 (short liq)")
print("  -> R = (7.108-6.95)/(6.95-6.81) = ", round((7.108 - 6.95) / (6.95 - 6.81), 2), "but score 1.0 = NO TRADE regardless")
print("BTC short: stopmap skew favors up-sweep; PIT-03 active (BTC +0.31% day, near VWAP+2.6s) -> knife-catching")
