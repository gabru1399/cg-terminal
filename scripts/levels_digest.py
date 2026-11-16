#!/usr/bin/env python3
"""Extract depth imbalance + nearest liq clusters for the top-4 setups."""
import json

d = json.load(open("/tmp/deep_telemetry.json"))
S = json.load(open("/tmp/table7_scores.json"))

print("depth ±5% (bookwalls, 150 snapshots):")
for sym in ("BTC", "DOGE", "AVAX", "SUI", "ADA", "BNB", "ARB"):
    mod = d[sym]["bookwalls"].get("model", {})
    dep = mod.get("depth", {})
    bid, ask = dep.get("bidUsd", 0), dep.get("askUsd", 0)
    print(f"  {sym:<5} bid ${bid/1e6:8.1f}M · ask ${ask/1e6:8.1f}M · bid/ask {bid/ask:.3f}")

print("\nnearest liq clusters (sweep magnets):")
for s in sorted(S, key=lambda x: -x["total"])[:5]:
    sym = s["sym"]
    kl = d[sym]["liqlevels"]["stats"]["keyLevels"]
    def fmt(x):
        return f"{x['price']:g} ({x['distPct']:+.2f}%, ${x['usd']/1e3:.0f}k, str {x['strength']}, {x['lev']})"
    print(f"  {sym} px {s['px']:.5g}")
    for x in kl["above"][:3]:
        print(f"    ↑ {fmt(x)}")
    for x in kl["below"][:3]:
        print(f"    ↓ {fmt(x)}")
