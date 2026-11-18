#!/usr/bin/env python3
"""
Portfolio expansion round (R547): three NEW archetypes backtested on the same
real Binance 15m data, then hedge-fund-style portfolio assembly.

Pre-registered rules (before any result seen):
- EA-6  SMC structure: BOS + FVG 50% retest (limit), h4-EMA bias gate.
- EA-7  VWAP 2-sigma climax reversion: climax bar beyond band + re-entry confirm.
- EA-8  Momentum burst continuation: climax-volume burst bar + strong close.

Engine reuses scripts/backtest_ea.py (stop-first worst-case fills, fees, invariants).
"""
import sys, json, os
sys.path.insert(0, "/home/z/my-project/scripts")
import numpy as np
import pandas as pd
from backtest_ea import (load_symbol, add_features, running_session, prior_levels,
                         simulate, FEE_TAKER, OUT, SYMS)

# ---------- EA-6: BOS + FVG retest ----------
def gen_ea6(df):
    sigs = []
    o,h,l,c = df.open.values, df.high.values, df.low.values, df.close.values
    atr = df.atr.values
    h4e13, h4e89 = df["h4e13"].values, df["h4e89"].values
    shi, slo = df["swing_hi"].values, df["swing_lo"].values
    fvgb, fvgs = df["fvg_bull"].values, df["fvg_bear"].values
    hhmm = df["dt"].dt.strftime("%H:%M").values
    n = len(df)
    LSH = LSL = None; LSH_i = LSL_i = -1
    fvg_zone = None      # (lo, hi) of last FVG before BOS
    bos_armed = None     # (side, bos_i, impulse_low, impulse_high)
    for i in range(30, n):
        # update swings (confirmed 2 bars after the pivot)
        if i >= 2 and shi[i-2]: LSH, LSH_i = h[i-2], i-2
        if i >= 2 and slo[i-2]: LSL, LSL_i = l[i-2], i-2
        # record FVGs (3-bar imbalance) as potential retest zones
        if i >= 2 and fvgb[i]: fvg_zone = ("L", l[i-2], h[i])   # gap between high[i-2] and low[i]
        if i >= 2 and fvgs[i]: fvg_zone = ("S", l[i], h[i-2])
        if np.isnan(atr[i]) or hhmm[i] >= "23:30": continue
        # BOS detection
        if LSH is not None and c[i] > LSH and (bos_armed is None or bos_armed[1] < i - 1):
            # bullish BOS: impulse low = most recent swing low
            if LSL is not None and LSL_i < i and h4e13[i] > h4e89[i] and fvg_zone and fvg_zone[0] == "L":
                flo = fvg_zone[1]
                if l[i] >= flo * 0.999 or True:  # zone recorded from the leg; keep if plausible
                    stop = min(flo, LSL) - 0.05*atr[i]
                    mid = (fvg_zone[1] + fvg_zone[2]) / 2
                    t1 = LSH + 0.5*atr[i]
                    t2 = c[i] + 2*(mid - stop) if c[i] + 2*(mid-stop) > t1 else c[i] + 2*(mid-stop)
                    t3 = mid + 3*(mid - stop)
                    sigs.append({"ea":"EA6","i":i,"side":"L","kind":"lim","px":mid,"stop":stop,"t1":t1,"t2":max(t2,t1),"t3":max(t3,t2)})
                    bos_armed = ("L", i)
            LSH = None  # consumed
        if LSL is not None and c[i] < LSL and (bos_armed is None or bos_armed[1] < i - 1):
            if LSH is not None and LSH_i < i and h4e13[i] < h4e89[i] and fvg_zone and fvg_zone[0] == "S":
                fhi = fvg_zone[2]
                stop = max(fhi, LSH) + 0.05*atr[i]
                mid = (fvg_zone[1] + fvg_zone[2]) / 2
                t1 = LSL - 0.5*atr[i]
                t2 = c[i] - 2*(stop - mid)
                t3 = mid - 3*(stop - mid)
                sigs.append({"ea":"EA6","i":i,"side":"S","kind":"lim","px":mid,"stop":stop,"t1":t1,"t2":min(t2,t1),"t3":min(t3,t2)})
                bos_armed = ("S", i)
            LSL = None
    return sigs

# ---------- EA-7: VWAP 2-sigma climax reversion ----------
def gen_ea7(df):
    sigs = []
    o,h,l,c = df.open.values, df.high.values, df.low.values, df.close.values
    vwap, sg, vz, dp = df["vwap"].values, df["sigma"].values, df["vz"].values, df["delta_pct"].values
    hhmm = df["dt"].dt.strftime("%H:%M").values
    day = df["day"].values
    n = len(df)
    armed = {}   # day -> (side, setup_low, setup_i)
    done = {}
    for i in range(30, n):
        d = day[i]
        if np.isnan(vwap[i]) or np.isnan(sg[i]) or sg[i] <= 0: continue
        if hhmm[i] <= "00:30" or hhmm[i] >= "23:30": continue
        # arm on climax beyond band
        if c[i] < vwap[i] - 2*sg[i] and vz[i] >= 2 and dp[i] <= -0.30:
            prev = armed.get((d,"L"))
            armed[(d,"L")] = ("L", min(l[i], prev[1]) if prev else l[i], i)
        if c[i] > vwap[i] + 2*sg[i] and vz[i] >= 2 and dp[i] >= 0.30:
            prev = armed.get((d,"S"))
            armed[(d,"S")] = ("S", max(h[i], prev[1]) if prev else h[i], i)
        # re-entry confirmation within 5 bars of arming
        for (dd, side), (s, sloc, si) in list(armed.items()):
            if dd != d or done.get((d, side)): continue
            if i - si > 5 or i <= si: continue
            if side == "L" and c[i] > vwap[i] - 2*sg[i] and c[i] > o[i]:
                if done.get((d, side)): continue
                stop = sloc - 0.25*sg[i]
                risk = c[i] - stop
                if risk <= 0: continue
                sigs.append({"ea":"EA7","i":i,"side":"L","kind":"mkt","stop":stop,
                             "t1":vwap[i],"t2":vwap[i]+sg[i],"t3":min(vwap[i]+2*sg[i], c[i]+3*risk)})
                done[(d, side)] = True
                armed.pop((dd, side), None)
            if side == "S" and c[i] < vwap[i] + 2*sg[i] and c[i] < o[i]:
                if done.get((d, side)): continue
                stop = sloc + 0.25*sg[i]
                risk = stop - c[i]
                if risk <= 0: continue
                sigs.append({"ea":"EA7","i":i,"side":"S","kind":"mkt","stop":stop,
                             "t1":vwap[i],"t2":vwap[i]-sg[i],"t3":max(vwap[i]-2*sg[i], c[i]-3*risk)})
                done[(d, side)] = True
                armed.pop((dd, side), None)
    return sigs

# ---------- EA-8: momentum burst continuation ----------
def gen_ea8(df):
    sigs = []
    o,h,l,c = df.open.values, df.high.values, df.low.values, df.close.values
    atr, vz, vwap = df.atr.values, df["vz"].values, df["vwap"].values
    rng = h - l
    cp = np.where(rng > 0, (c - l) / np.maximum(rng, 1e-12), 0.5)
    hhmm = df["dt"].dt.strftime("%H:%M").values
    day = df["day"].values
    n = len(df)
    done = {}
    for i in range(30, n):
        d = day[i]
        if np.isnan(atr[i]) or np.isnan(vz[i]) or np.isnan(vwap[i]): continue
        if hhmm[i] >= "23:30": continue
        if rng[i] < 1.5*atr[i] or vz[i] < 2.5: continue
        key = ("L", d)
        if cp[i] >= 0.80 and c[i] > vwap[i] and not done.get(key):
            mid = (h[i] + l[i]) / 2
            stop = mid - 0.02*atr[i]
            risk = c[i] - stop
            if risk <= 0: continue
            sigs.append({"ea":"EA8","i":i,"side":"L","kind":"mkt","stop":stop,
                         "t1":c[i]+risk,"t2":c[i]+2*risk,"t3":c[i]+3*risk})
            done[key] = True
        key = ("S", d)
        if cp[i] <= 0.20 and c[i] < vwap[i] and not done.get(key):
            mid = (h[i] + l[i]) / 2
            stop = mid + 0.02*atr[i]
            risk = stop - c[i]
            if risk <= 0: continue
            sigs.append({"ea":"EA8","i":i,"side":"S","kind":"mkt","stop":stop,
                         "t1":c[i]-risk,"t2":c[i]-2*risk,"t3":c[i]-3*risk})
            done[key] = True
    return sigs

def main():
    rows = []
    for sym in SYMS:
        df = load_symbol(sym)
        df = add_features(df)
        d1 = df.set_index("dt")[["high","low","close"]].resample("1D").agg({"high":"max","low":"min","close":"last"}).dropna()
        pc = d1["close"].shift(1)
        tr1 = pd.concat([d1["high"]-d1["low"], (d1["high"]-pc).abs(), (d1["low"]-pc).abs()], axis=1).max(axis=1)
        df["atr_d"] = df["dt"].dt.floor("D").map(tr1.rolling(14).mean())
        df = running_session(df)
        df = prior_levels(df)
        for gen, thold, mh in ((gen_ea6, 8, 96), (gen_ea7, 16, 32), (gen_ea8, 8, 48)):
            sigs = gen(df)
            for s in sigs: s["sym"] = sym
            trs = simulate(df, sym, sigs, max_hold=mh, time_stop_bars=thold)
            for t in trs:
                rows.append({"ea":t.ea,"sym":sym,"side":t.side,
                             "entry_dt":df.dt.iloc[t.entry_i],
                             "exit_dt":df.dt.iloc[t.close_i] if t.close_i is not None else None,
                             "r":t.r - t.fees_r,"reason":t.exit_reason,"bars":t.bars_held})
        df.to_pickle(f"{OUT}/{sym}.pkl")  # refresh pickles (same schema as R546)
    res = pd.DataFrame(rows).dropna(subset=["exit_dt"])
    res.to_csv(f"{OUT}/trades_v2.csv", index=False)
    out = {}
    for ea in ["EA6","EA7","EA8"]:
        sub = res[res.ea==ea]
        rs = sub["r"].values
        if not len(rs): out[ea]={"n":0}; continue
        wins = rs[rs>0]; losses = rs[rs<=0]
        eq = np.cumsum(rs); dd = float((np.maximum.accumulate(eq)-eq).max())
        out[ea] = {"n":int(len(rs)),"winrate":round(float((rs>0).mean()),3),
                   "avgR":round(float(rs.mean()),3),"sumR":round(float(rs.sum()),1),
                   "pf":round(float(wins.sum()/abs(losses.sum())),2) if losses.sum()!=0 else None,
                   "maxDD_R":round(dd,1)}
        for s in SYMS:
            ss = sub[sub.sym==s]["r"]
            out[ea][s] = {"n":int(len(ss)),"sumR":round(float(ss.sum()),1),
                          "wr":round(float((ss>0).mean()),2) if len(ss) else None}
        bym = sub.copy(); bym["m"] = pd.to_datetime(bym.entry_dt).dt.strftime("%Y-%m")
        out[ea]["by_month"] = {m: round(g.r.sum(),1) for m, g in bym.groupby("m")}
    print(json.dumps(out, indent=1))
    json.dump(out, open(f"{OUT}/results_v2.json","w"), indent=1)

if __name__ == "__main__":
    main()
