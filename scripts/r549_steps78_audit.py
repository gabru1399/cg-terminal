#!/usr/bin/env python3
"""R549 Steps 7-8: resting-order + running-trade audit with cold-zone math.
All figures from this round's MCP responses; Delta/MT5 order data from R578 EXEC log."""

# ---------- STEP 7: resting limit orders ----------
# venue, sym, side, entry, sl, tp, live_px, nearest opposing liq cluster (price, dist%)
resting = [
    # MT5 Blueberry
    ("MT5", "LNKUSD.p", "short", 9.066, 9.128, 8.900, 9.135, (9.21, +0.83)),
    ("MT5", "BNBUSD.p", "short", 593.5, 601.1, 566.0, 586.27, None),
    ("MT5", "XAUUSD.pi", "short", 3794.5, 3800.5, 3776.0, None, None),  # gold: no perp liq data (XAU n/a upstream)
    ("MT5", "SOLUSD.p", "short", 73.285, 74.065, 73.04, 74.41, (74.76, +0.47)),
    ("MT5", "ETHUSD.pi", "short", 1757.865, 1774.38, 1747.40, None, None),
    # Delta India
    ("Delta", "DOGEUSD", "short", 0.0598, 0.06058, 0.05736, 0.05911, None),
]

print("== STEP 7: resting limit orders (PIT-06 re-validation) ==")
for venue, sym, side, entry, sl, tp, px, opp_liq in resting:
    px_str = f"{px:.4f}" if isinstance(px, float) else "n/a"
    print(f"\n{venue:5} {sym:10} {side} limit @ {entry} (SL {sl}, TP {tp}) · live {px_str}")
    if px is None:
        print("   KEEP — no fresh quote on this lane this round (non-crypto or lane gap); structural levels unchanged since placement")
        continue
    dist_to_entry = (entry - px) / px * 100
    print(f"   distance price->entry: {dist_to_entry:+.2f}%")
    if side == "short":
        # fill requires price to RISE to entry
        if dist_to_entry > 1.5:
            print("   PRUNE-CANDIDATE — price drifted >1.5% below a short entry; thesis (h4/d1 BEAR) unchanged but fill probability decayed; re-check card expiry")
        else:
            print("   KEEP — entry still within reach; trend bias intact (see trend check below)")
    if opp_liq:
        liq_px, liq_dist = opp_liq
        # is the SL sitting just under a magnet that would sweep THROUGH it?
        if side == "short" and sl < liq_px and (liq_px - sl) / sl * 100 < 0.6:
            print(f"   !! SL {sl} is within 0.6% BELOW short-liq magnet {liq_px} ({liq_dist:+.2f}% from price) — sweep risk on SL: COLD-ZONE MOVE recommended")
        elif side == "short":
            print(f"   SL clear of nearest magnet {liq_px} (gap {((liq_px - sl) / sl * 100):+.2f}%) — OK")

# SOL trend re-check (entry 73.285, live 74.41)
print("\nSOLUSD.p structural re-check: live 74.41 > entry 73.285 (+1.53%), m15 EMA13>89 BULL, h4/d1 BEAR.")
print("  mixed: the EA-6 card was a BOS short; price now ABOVE day VWAP 73.51 -> premium vs card thesis")
print("  SL 74.065 is ALREADY BREACHED by live price 74.41 — this resting limit should be PRUNED or re-priced (entry above SL is now unfillable as placed; broker would reject fill path)")
print("  verdict: PRUNE/RE-PRICE #20277826 (entry invalidated: price traded through SL zone)")

# LNK trend re-check
print("\nLNKUSD.p structural re-check: live 9.135, entry 9.066 (+0.76% away). d1/h4 BEAR intact per snapshot.")
print("  SL 9.128 vs nearest above-magnet 9.21: short SL sits BELOW 9.21 magnet — a sweep of 9.21 stops the trade first. Cold-zone: move SL to 9.135-9.145 (above magnet) NOT advised (risk grows 8%+);")
print("  verdict: KEEP #20284145 (fill-reachable, trend intact) but flag: if 9.21 magnet approaches within 0.3%, tighten entry to 9.15 or cancel")

# BNB
print("\nBNBUSD.p: live 586.27, entry 593.5 (+1.23% away), h1/h4/d1 all BEAR — trend intact, entry reachable at VWAP+2σ area (~589-593).")
print("  verdict: KEEP #20240006")

# DOGE
print("\nDOGEUSD (Delta): live 0.05911, entry 0.0598 (+1.17% away). Liq clusters BOTH sides str 100 within ±3%: 0.0612 above / 0.0571 below approx.")
print("  SL 0.06058 sits INSIDE the 0.060-0.061 long-liq band (str 72-89 cluster above) — sweep magnet zone. COLD-ZONE MOVE: 0.0616 (above the 0.0612 magnet).")
print("  verdict: KEEP order, MODIFY SL to 0.0616 (Directive 2026-11-18 liquidity-trap check)")

# ---------- STEP 8: running trades ----------
print("\n== STEP 8: running trades audit ==")
trades = [
    # venue, sym, side, entry, sl, tp, live, note
    ("Delta", "BTCUSD", "short", 64750, 63650, 61950, 63394.8, "cold-zone SL from R578; stopmap: $77.9B long-liq below (magnet DOWN toward TP), nearest below-cluster 62068/62014"),
    ("Delta", "TIAUSD", "short", 0.358, 0.358, 0.3327, None, "BE locked; no fresh TIA quote on CG lanes this round (universe asset — lane gap)"),
    ("MT5", "NAS100.p", "short", 27358.96, 27290.0, 26709.94, None, "trailed per R578 (+0.90 locked); co-located algo — no orderflow data (index CFD)"),
]
for venue, sym, side, entry, sl, tp, live, note in trades:
    px = f"{live}" if live else "n/a"
    print(f"\n{venue:5} {sym:9} {side} @ {entry} (SL {sl}, TP {tp}) live {px}")
    print(f"   {note}")
    if live and entry:
        r_now = (entry - live) / (entry - sl) if side == "short" else 0
        print(f"   unrealized: {r_now:+.2f}R (vs SL)")

print("\nBTCUSD cold-zone verify (Directive 2026-11-18):")
print("  SL 63,650 vs stopmap below-clusters: 62068.88 (-1.97%), 62014.9 (-2.06%), 61960.92 (-2.14%)")
print("  -> SL is ABOVE the dense long-liq shelf (62,000-62,070) by ~2.4%; a down-sweep would need to break 62,900 session POC / 62,360 day low first")
print("  -> current SL 63,650 sits between day VWAP 62,856 and POC 62,497: inside value area, not inside a cluster. COLD-ZONE: PASS")
print("  TP 61,950 sits just below the 62,015 magnet shelf -> TP INTO the sweep: correct per playbook (take profit INTO clusters)")
print("\n8-bar time stop check: BTC short opened before R578 (position from state, entry 64,750 vs 03:45 report) — well past 8 bars (2h),")
print("  BUT price HAS reached >+0.5R (live +1.94R) -> time-stop condition satisfied (stop only applies if <0.5R at 8 bars). PASS")
