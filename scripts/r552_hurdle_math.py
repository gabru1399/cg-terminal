#!/usr/bin/env python3
"""R552 strict hurdle math — LDO S1 sweep-fade, XAU recheck, GOOGL watch.
All inputs from this round's live MCP pulls (11:01-11:07 UTC)."""

# ---- LDO SHORT (Delta India LDOUSDT) — S1 sweep-and-fade ----
# px 0.2686 · 4-TF BEAR · engine A+ conf 92 · BEAR abs 09:15/07:30/04:45 @ 0.2701/0.2723/0.2740 (in-zone, fresh)
# above-shelf boundary (3D max 0.2794, 7D max ~0.2790, 30D max 0.2794) + 0.3% alt buffer -> 0.2802
# ask-wall ladder 0.272-0.278 confirmed (ages 420-1980 min) · below magnets: 0.2654 str87 / 0.2640 str100 / 0.2618 str98 (3D)
ldo = {
    "trigger_entry": 0.2800,   # S1: sweep of the 0.2794-0.28 shelf + 15m rejection close back below 0.2794
    "stop": 0.2845,            # beyond terminal above-shelf 0.2794 + 0.3% buffer (0.2802) + sweep-wick allowance
    "t1": 0.2720,              # ask-wall shelf floor / day POC 0.27
    "t2": 0.2654,              # 3D long-liq cluster str 87
    "t3": 0.2618,              # 3D long-liq cluster str 98
    "lsr_7d": 101983366 / 39845334,
    "lsr_30d": 415862311 / 45935848,
}
ldo["risk"] = ldo["stop"] - ldo["trigger_entry"]
for k in ("t1", "t2", "t3"):
    ldo[f"r_{k}"] = (ldo["trigger_entry"] - ldo[k]) / ldo["risk"]
print("LDO SHORT — S1 ARMED (punch only on sweep-and-reject trigger):")
print(f"  LSR 7D {ldo['lsr_7d']:.2f}:1 · 30D {ldo['lsr_30d']:.2f}:1 -> D12 bans passive entry BELOW shelf; S1 mandatory")
print(f"  entry {ldo['trigger_entry']} · SL {ldo['stop']} (cold: beyond 0.2794+0.3%+wick) · risk {ldo['risk']*100:.2f} raw pts")
print(f"  R: T1 {ldo['r_t1']:.2f} · T2 {ldo['r_t2']:.2f} · T3 {ldo['r_t3']:.2f} (floor 2.00 -> T2-weighted PASS)")
# Table 7 strict: f1 4-TF BEAR 2.0 · f2 entry-at-premium post-sweep 1.5 · f3 bear-abs cluster in-zone 2.0
# f4 ask-wall ladder above 1.5 · f5 CVD no active div 0.0 · f6 skew AGAINST short (up-magnet) 0.0
# f7 gex n/a 0.0 · f8 PIT-18 conditional 0.5
print(f"  Table 7 strict = {2.0+1.5+2.0+1.5+0.0+0.0+0.0+0.5:.1f} (A-range; D12 + payoff only clear AFTER trigger)")
# sizing: Delta equity ~$2.91, 1% = $0.029; 1 ct = 1 LDO -> risk/ct = stop dist in $
print(f"  sizing: ~{0.029/ldo['risk']:.0f} contracts risks $0.029 = 1.0% equity (Delta min-lot OK)")
print(f"  PIT-18: need spread <= {ldo['risk']*0.05:.4f} at punch (5% of {ldo['risk']:.4f} stop) — VERIFY LIVE, else SKIP")

# ---- XAU SHORT recheck (fresh BEAR vol-bar div 10:48 in zone) ----
# cold SL 3784 (beyond 30D above-shelf 3777.37 + 0.15% + 2.5sigma 3780.8) — entry variants:
for entry in (3748.0, 3753.0):
    risk = 3784 - entry
    t2r = (entry - 3698.7) / risk
    t1r = (entry - 3727.8) / risk
    print(f"XAU entry {entry}: SL 3784 · T1 {t1r:.2f}R · T2 {t2r:.2f}R -> {'PASS' if t2r>=2 else 'FAIL'} floor 2.00")

# ---- GOOGL LONG watch (abs 10:50 but engine gate unsatisfied) ----
print("GOOGL: RSI m15 90 / h1 78.8, 1.70sigma stretch, conf 35, h4/d1 BEAR — chase FORBIDDEN until")
print("  3sigma flush 297.98+ print or exhaustion at 295-298 with defending bid wall. WATCH only.")
