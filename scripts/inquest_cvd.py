#!/usr/bin/env python3
"""Compute 24h CVD deltas (perp & spot) + taker share from /cvd candles for card candidates."""
import json, urllib.request

BASE = "http://127.0.0.1:3000/api/cg"

def get(path, timeout=30):
    with urllib.request.urlopen(f"{BASE}{path}", timeout=timeout) as r:
        return json.load(r)

# 24h of m15 bars = 96; use last 96 entries
W = 96
out = {}
for sym in ["APT", "ADA", "ARB", "TIA", "SEI", "DOGE", "VET", "BTC", "NVDA", "XAU", "MSFT", "MSTR", "AVGO"]:
    try:
        d = get(f"/cvd?sym={sym}&itv=m15&mode=total")
        perp = d.get("perp") or []
        spot = d.get("spot") or []
        if len(perp) > W:
            p24 = perp[-1] - perp[-1 - W]
        else:
            p24 = perp[-1] - perp[0] if perp else None
        if spot and len(spot) > W:
            s24 = spot[-1] - spot[-1 - W]
        elif spot:
            s24 = spot[-1] - spot[0]
        else:
            s24 = None
        # taker buy share if present
        tb = d.get("takerBuyRatio") or d.get("takerBuyShare")
        out[sym] = {"perpCvd24h": round(p24, 1) if p24 is not None else None,
                    "spotCvd24h": round(s24, 1) if s24 is not None else None,
                    "n": d.get("n")}
        print(f"{sym:6} perpCvd24h={out[sym]['perpCvd24h']} spotCvd24h={out[sym]['spotCvd24h']} n={d.get('n')}")
    except Exception as e:
        print(f"{sym:6} ERR {str(e)[:60]}")

with open("/tmp/inquest_cvd.json", "w") as f:
    json.dump(out, f, indent=1)
print("saved")
