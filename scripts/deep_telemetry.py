#!/usr/bin/env python3
"""Deep 9-tab telemetry for the A+ candidates (BTC BNB ADA DOGE AVAX UNI ARB SUI).
Pulls: market (auction/VWAP/EMA/RSI), signals, liqlevels (LSR gate), bookwalls,
cvd, lto, backtest, notifications. Applies Gate 0.1 (stale forming bar caveat)."""
import json, urllib.request, time
from datetime import datetime, timezone

BASE = "http://127.0.0.1:3000"
SYMS = "BTC BNB ADA DOGE AVAX UNI ARB SUI".split()

def get(path, timeout=25):
    try:
        with urllib.request.urlopen(f"{BASE}{path}", timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

out = {}
for sym in SYMS:
    d = {}
    m = get(f"/api/cg/market?sym={sym}")
    d["market"] = m
    d["signals"] = get(f"/api/cg/signals?sym={sym}")
    d["liqlevels"] = get(f"/api/cg/liqlevels?sym={sym}")
    d["bookwalls"] = get(f"/api/cg/bookwalls?sym={sym}")
    d["cvd"] = get(f"/api/cg/cvd?sym={sym}")
    d["lto"] = get(f"/api/cg/lto?sym={sym}")
    d["backtest"] = get(f"/api/cg/backtest?sym={sym}")
    out[sym] = d
    time.sleep(0.3)

# compact digest
for sym, d in out.items():
    m = d["market"]
    px = m.get("price", {}).get("last")
    au = m.get("auction", {})
    day = au.get("day", {}) if isinstance(au, dict) else {}
    vw = m.get("vwap", {}) if isinstance(m.get("vwap"), dict) else {}
    print(f"\n===== {sym} · px {px} =====")
    if day:
        print(f"  day VAL {day.get('val')} / POC {day.get('poc')} / VAH {day.get('vah')}  · sess POC {au.get('session',{}).get('poc')}")
    if vw:
        print(f"  VWAP mid {vw.get('mid')} · z {vw.get('z')} · bands {[vw.get(k) for k in ('s1','s2','s3')] if vw.get('s1') else ''}")
    ind = m.get("indicators") or {}
    if ind:
        h4 = ind.get("h4", {}) if isinstance(ind.get("h4"), dict) else {}
        print(f"  RSI m15 {ind.get('m15',{}).get('rsi')} h1 {ind.get('h1',{}).get('rsi')} h4 {h4.get('rsi')}")
    # signals
    sig = d["signals"]
    sl = sig.get("signals") or sig.get("list") or [] if isinstance(sig, dict) else []
    hi = [s for s in sl if str(s.get("severity","")).upper().startswith("HIGH") or s.get("kind") in ("Absorption","Trap","Strong Divergence")] if isinstance(sl, list) else []
    print(f"  signals: {len(sl) if isinstance(sl,list) else 'n/a'} · HIGH/strong: {[(s.get('kind'), s.get('tf') or s.get('interval'), str(s.get('t') or s.get('ts'))[:16]) for s in hi[:4]]}")
    # liq levels + LSR
    ll = d["liqlevels"]
    lsr = ll.get("lsr") or ll.get("liqSkewRatio") or ll.get("skewRatio")
    clusters = ll.get("clusters") or ll.get("levels") or []
    print(f"  LSR: {lsr} · clusters: {len(clusters) if isinstance(clusters,list) else 'n/a'}")
    if isinstance(clusters, list) and clusters:
        for c in clusters[:3]:
            usd = c.get("usd") or c.get("size") or 0
            usd_str = f"${usd/1e6:.2f}M" if usd > 1e6 else f"${usd:,.0f}"
            print(f"    {c.get('price')} · {usd_str} · {c.get('side') or c.get('dir')} · {c.get('window') or c.get('range')}")
    # cvd
    cv = d["cvd"]
    print(f"  CVD: perp {cv.get('perp24h') or cv.get('perp')} · spot {cv.get('spot24h') or cv.get('spot')} · takerBuy {cv.get('takerBuyShare')}% · quadrant {cv.get('quadrant')} · div {cv.get('divergences') or cv.get('activeDivergences')}")
    # backtest
    bt = d["backtest"]
    if isinstance(bt, dict) and not bt.get("error"):
        print(f"  backtest: {json.dumps({k:v for k,v in bt.items() if k not in ('rows','history')})[:300]}")

json.dump(out, open("/tmp/deep_telemetry.json", "w"), indent=1)
print("\nsaved /tmp/deep_telemetry.json")
