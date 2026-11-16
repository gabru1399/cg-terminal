#!/usr/bin/env python3
"""Table 7 zero-fallback confluence scoring for the 8 A+ SHORT candidates.
Inputs: /tmp/deep_telemetry.json + live notifications feed.
Gate 0.1: backtest missing -> 0.0 pts (honest zero). LSR >= 2.5 bans passive S3."""
import json, urllib.request, time
from datetime import datetime, timezone

d = json.load(open("/tmp/deep_telemetry.json"))

# notifications feed
try:
    with urllib.request.urlopen("http://127.0.0.1:3000/api/cg/notifications", timeout=20) as r:
        notif = json.loads(r.read())
except Exception as e:
    notif = {"error": str(e)}
notif_rows = notif.get("events") or notif.get("rows") or [] if isinstance(notif, dict) else []
print(f"notifications: {len(notif_rows)} events")

def f(x, nd=4):
    try: return f"{float(x):,.{nd}g}"
    except Exception: return str(x)

scores = []
for sym, t in d.items():
    m = t["market"]; au = m["auction"]; vw = m["vwap"]
    px = m["price"]["last"]
    day = au["day"]; sess = au["session"]
    rsi = m["rsi"]; ema = m["ema"]
    ll = t["liqlevels"]; stats = ll.get("stats", {})
    tot = stats.get("totals", {})
    short_usd = tot.get("shorts", 0); long_usd = tot.get("longs", 0)
    lsr = short_usd / long_usd if long_usd else None
    cv = t["cvd"]; kpis = cv.get("kpis", {})
    sig = t["signals"]; counts = sig.get("counts", {})
    bt = t["backtest"].get("result")

    pts = {}  # Table 7 itemized, zero-fallback
    # F1 Trend alignment (EMA13<EMA89<EMA233 on h4 + d1) — TREND_DOWN confirmed
    h4 = ema.get("h4", {}); d1 = ema.get("d1", {})
    stack_h4 = h4.get("e13", 0) < h4.get("e89", 0) < h4.get("e233", 1e18)
    stack_d1 = d1.get("e13", 0) < d1.get("e89", 0) < d1.get("e233", 1e18)
    pts["F1_trend_stack"] = 1.5 if (stack_h4 and stack_d1) else (1.0 if stack_h4 else 0.0)
    # F2 VWAP regime (price below day VWAP = discount bearish)
    vwap = vw.get("vwap")
    pts["F2_vwap_regime"] = 1.0 if (vwap and px < vwap) else 0.0
    # F3 Auction location (price inside/below day value for shorts)
    if px < day.get("val", 0): pts["F3_auction"] = 1.0       # breakdown below VAL
    elif px <= day.get("poc", 1e18): pts["F3_auction"] = 0.5 # lower half of value
    else: pts["F3_auction"] = 0.0
    # F4 RSI h4/d1 oversold-continuation (30-50 band = momentum room)
    r_h4, r_d1 = rsi.get("h4", 50), rsi.get("d1", 50)
    pts["F4_rsi"] = 1.0 if (r_h4 < 45 and r_d1 < 35) else (0.5 if r_h4 < 50 else 0.0)
    # F5 liquidation magnet asymmetry (shorts clustered above = squeeze fuel)
    pts["F5_liq_skew"] = 1.0 if (lsr and lsr >= 1.5) else 0.0
    # F6 CVD confirmation (both-selling / buy ratio < 50)
    pts["F6_cvd"] = 1.0 if (kpis.get("buyRatio", 50) < 50 or kpis.get("quadrant") == "both-selling") else 0.0
    # F7 footprint signals (bear count >= bull count on the live sets)
    bull, bear = counts.get("bullish", 0), counts.get("bearish", 0)
    pts["F7_signals"] = 1.0 if bear >= bull and bear > 0 else 0.0
    # F8 backtest expectancy — HONEST ZERO when not computed
    pts["F8_backtest"] = 0.0 if bt is None else 0.5
    # F9 [HIGH] alerts for this sym in the feed
    hi = [e for e in notif_rows if isinstance(e, dict) and e.get("sym") == sym
          and str(e.get("severity", "")).upper().startswith("HIGH")]
    pts["F9_alerts"] = 0.5 if hi else 0.0

    total = sum(pts.values())
    # Liquidation Magnet Gate: >= 2.5 bans passive front-run (S3)
    gate = "BANNED-S3" if (lsr and lsr >= 2.5) else "clear"
    grade = "A+" if total >= 7.0 else ("A" if total >= 6.5 else ("B" if total >= 5.0 else "VETO"))

    scores.append(dict(sym=sym, px=px, pts=pts, total=round(total, 2), lsr=round(lsr, 2) if lsr else None,
                       gate=gate, grade=grade, day=day, sess=sess, vwap=vwap, rsi=rsi,
                       short_usd=short_usd, long_usd=long_usd, bt=bt))

for s in sorted(scores, key=lambda x: -x["total"]):
    print(f"\n{s['sym']} · {s['total']:.1f} pts · grade {s['grade']} · LSR {s['lsr']} ({s['gate']})")
    print(f"  px {f(s['px'])} · day VAL {f(s['day']['val'])} POC {f(s['day']['poc'])} VAH {f(s['day']['vah'])} · VWAP {f(s['vwap'])}")
    print(f"  RSI h4 {s['rsi'].get('h4',0):.1f} d1 {s['rsi'].get('d1',0):.1f} · liq above ${s['short_usd']/1e6:.2f}M vs below ${s['long_usd']/1e6:.2f}M")
    print("  " + " · ".join(f"{k.replace('_',' ')} {v}" for k, v in s["pts"].items()))

json.dump(scores, open("/tmp/table7_scores.json", "w"), indent=1, default=str)
print("\nsaved /tmp/table7_scores.json")
