#!/usr/bin/env python3
"""Extract nearest liquidation magnets (above/below) + LSR for card candidates."""
import json, urllib.request

BASE = "http://127.0.0.1:3000/api/cg"

def get(path, timeout=25):
    with urllib.request.urlopen(f"{BASE}{path}", timeout=timeout) as r:
        return json.load(r)

out = {}
for sym in ["APT", "ADA", "ARB", "TIA", "SEI", "DOGE", "VET", "BTC", "NVDA", "XAU", "MSFT", "MSTR", "AVGO"]:
    try:
        d = get(f"/liqlevels?sym={sym}")
        st = d.get("stats", {})
        last = st.get("last")
        above = st.get("keyLevels", {}).get("above", [])
        below = st.get("keyLevels", {}).get("below", [])
        lsr = d.get("lsr") or st.get("lsr") or d.get("skew") or st.get("skew")
        def fmt(cl):
            return {"p": cl.get("price"), "distPct": cl.get("distPct"), "strength": cl.get("strength"), "usd": round((cl.get("usd") or 0) / 1e6, 2)}
        out[sym] = {
            "last": last,
            "above": [fmt(c) for c in above[:3]],
            "below": [fmt(c) for c in below[:3]],
            "lsr": lsr,
        }
        a = out[sym]["above"][0] if above else None
        b = out[sym]["below"][0] if below else None
        print(f"{sym:6} last={last} | above {json.dumps(a)} | below {json.dumps(b)} | lsr={lsr}")
    except Exception as e:
        print(f"{sym:6} ERR {str(e)[:60]}")

with open("/tmp/inquest_liq.json", "w") as f:
    json.dump(out, f, indent=1)
print("saved")
