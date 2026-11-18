#!/usr/bin/env python3
"""Compute per-bar footprint deltas (taker buy vs sell) from /api/cg/fp for card candidates."""
import json, urllib.request

def get(path, timeout=30):
    with urllib.request.urlopen(f"http://127.0.0.1:3000/api/cg{path}", timeout=timeout) as r:
        return json.load(r)

out = {}
for sym in ["APT", "ADA", "ARB", "TIA", "SEI", "DOGE", "VET", "NVDA", "XAU", "MSFT", "MSTR", "AVGO"]:
    try:
        d = get(f"/fp?sym={sym}")
        bars = d.get("bars", [])[-8:]  # last 2h of 15m bars
        tot_buy, tot_sell = 0.0, 0.0
        per_bar = []
        for b in bars:
            fp = b.get("fp", {})
            bv = sum(x for x in fp.get("b", []) if x)
            sv = sum(x for x in fp.get("s", []) if x)
            tot_buy += bv; tot_sell += sv
            per_bar.append(round((bv - sv) / (bv + sv) * 100, 1) if (bv + sv) else 0)
        delta_pct = round((tot_buy - tot_sell) / (tot_buy + tot_sell) * 100, 1) if (tot_buy + tot_sell) else None
        out[sym] = {"buyUsd": round(tot_buy, 0), "sellUsd": round(tot_sell, 0), "deltaPct2h": delta_pct,
                    "perBarDeltaPct": per_bar}
        print(f"{sym:5} 2h taker buy {tot_buy:>10.0f} sell {tot_sell:>10.0f} delta {delta_pct:>6}% | bars {per_bar}")
    except Exception as e:
        print(f"{sym:5} ERR {str(e)[:60]}")

json.dump(out, open("/tmp/inquest_fp.json", "w"), indent=1)
print("saved")
