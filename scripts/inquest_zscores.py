#!/usr/bin/env python3
"""Compute day-VWAP z-scores + regime table for inquest cards (fix: bands.sd1)."""
import json, urllib.request

BASE = "http://127.0.0.1:3000/api/cg"

def get(path, timeout=25):
    with urllib.request.urlopen(f"{BASE}{path}", timeout=timeout) as r:
        return json.load(r)

def zparts(mk):
    vw = mk.get("vwap") or {}
    mid = vw.get("vwap")
    b = (vw.get("bands") or {})
    sd1 = b.get("sd1")
    return mid, sd1

print(f"{'sym':6} {'px':>10} {'z':>6} {'dist2dayLo%':>11} {'vs POC%':>8} regime")
rows = []
for sym in ["APT","ADA","ARB","TIA","SEI","DOGE","VET","BTC","ETH","NVDA","XAU","MSFT","MSTR","AVGO","SNDK","MU"]:
    try:
        mk = get(f"/market?sym={sym}")
        narr = get(f"/narrative?sym={sym}")
        px = mk["price"]["last"]
        mid, sd1 = zparts(mk)
        z = round((px - mid) / sd1, 2) if (mid and sd1) else None
        lo = mk["price"]["dayLow"]
        poc = mk["auction"]["day"]["poc"]
        dist_lo = round((px - lo) / lo * 100, 2) if lo else None
        vs_poc = round((px - poc) / poc * 100, 2) if poc else None
        print(f"{sym:6} {px:>10} {str(z):>6} {str(dist_lo):>11} {str(vs_poc):>8} {narr.get('regime')}")
        rows.append({"sym": sym, "px": px, "z": z, "dist_dayLow_pct": dist_lo, "vs_dayPOC_pct": vs_poc,
                     "regime": narr.get("regime"), "dir": narr.get("direction"), "conf": narr.get("confidence")})
    except Exception as e:
        print(f"{sym:6} ERR {str(e)[:60]}")

with open("/tmp/inquest_z.json", "w") as f:
    json.dump(rows, f, indent=1)
print("saved /tmp/inquest_z.json")
