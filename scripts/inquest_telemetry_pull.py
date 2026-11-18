#!/usr/bin/env python3
"""Per-asset telemetry pull for the quant inquest response (zai-desk R383).
Reads live terminal endpoints for the Gate-7 permitted micro-assets plus
TradFi slot-2 candidates; prints compact JSON lines for grounding cards."""
import json, urllib.request, sys

BASE = "http://127.0.0.1:3000/api/cg"

def get(path, timeout=25):
    with urllib.request.urlopen(f"{BASE}{path}", timeout=timeout) as r:
        return json.load(r)

def zscore(mk):
    """Compute day-VWAP z from market payload (vwap dict with mid/sd1)."""
    vw = mk.get("vwap") or {}
    mid = vw.get("vwap") or vw.get("mid")
    sd1 = vw.get("sd1") or vw.get("band")
    px = mk["price"]["last"]
    if mid and sd1:
        return round((px - mid) / sd1, 2), round(mid, 6), round(sd1, 6)
    return None, mid, sd1

def liq_nearest(sym):
    try:
        d = get(f"/liqlevels?sym={sym}")
        rows = []
        for w in ("3d", "7d", "30d"):
            for cl in (d.get(w) or d.get("clusters", {}).get(w) or []):
                if isinstance(cl, dict):
                    rows.append((w, cl.get("price"), cl.get("strength"), cl.get("liqUsd") or cl.get("usd")))
        rows = [r for r in rows if r[1]]
        rows.sort(key=lambda r: abs(r[1]))
        return rows[:4]
    except Exception as e:
        return f"ERR {str(e)[:40]}"

def cvd_snap(sym):
    try:
        d = get(f"/cvd?sym={sym}")
        keep = {k: d.get(k) for k in ("perpCvd", "spotCvd", "takerBuyRatio", "takerBuyShare", "quadrant") if k in d}
        if not keep:
            keep = {k: d.get(k) for k in list(d.keys())[:6]}
        return keep
    except Exception as e:
        return f"ERR {str(e)[:40]}"

def sig_counts(sym):
    try:
        d = get(f"/signals?sym={sym}")
        c = d.get("counts", {})
        return f"bull {c.get('bullish')}/bear {c.get('bearish')} (n={c.get('all')})"
    except Exception as e:
        return f"ERR {str(e)[:40]}"

for sym in ["APT", "ADA", "ARB", "TIA", "SEI", "DOGE", "VET", "BTC", "NVDA", "XAU", "MSFT", "MSTR", "AVGO"]:
    try:
        mk = get(f"/market?sym={sym}")
        z, mid, sd1 = zscore(mk)
        px = mk["price"]["last"]
        day = mk.get("auction", {}).get("day", {})
        out = {
            "sym": sym, "px": px, "z": z, "vwap": mid, "sd1": sd1,
            "dayPOC": round(day.get("poc", 0), 6) if day.get("poc") else None,
            "dayVAH": round(day.get("vah", 0), 6) if day.get("vah") else None,
            "dayVAL": round(day.get("val", 0), 6) if day.get("val") else None,
            "chgDay": round(mk["price"].get("chgDayPct", 0), 2),
            "dayLow": mk["price"].get("dayLow"), "dayHigh": mk["price"].get("dayHigh"),
            "liq": liq_nearest(sym), "cvd": cvd_snap(sym), "sigs": sig_counts(sym),
        }
        print(json.dumps(out))
    except Exception as e:
        print(json.dumps({"sym": sym, "err": str(e)[:80]}))
