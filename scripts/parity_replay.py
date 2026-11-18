#!/usr/bin/env python3
"""
Parity replay: feed the TS playbook engine the REAL Binance dump bars and diff
its emitted cards against the backtest signal lists (entries/stops/targets).

For each symbol we take K sliding windows ending at bars where the backtest
fired a signal, run runPlaybook on the trailing 1500 bars (like the live route),
and check that the matching backtest signal appears as a card with identical
numbers (small float tolerance).
"""
import json, subprocess, sys
import numpy as np
import pandas as pd

sys.path.insert(0, "/home/z/my-project/scripts")
from backtest_ea import load_symbol, add_features, running_session, prior_levels
from backtest_portfolio import gen_ea6

OUT = "/home/z/my-project/data/backtest"
SYMS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
WINDOW = 4500  # 3x the live fetch: matches the production route's 4500-bar kline window
TOL = 1e-6

def h4_bias_nolookahead(df):
    t = df["open_time"].values; c = df["close"].values; n = len(df)
    e13 = np.full(n, np.nan); e89 = np.full(n, np.nan)
    e13c = e89c = None; cur_bt = None
    for i in range(n):
        bt = t[i] // (4 * 3_600_000)
        if cur_bt is None:
            cur_bt = bt
        elif bt != cur_bt:
            cc = c[i - 1]
            if e13c is None: e13c = e89c = cc
            else:
                e13c = cc * (2/14) + e13c * (12/14)
                e89c = cc * (2/90) + e89c * (88/90)
            cur_bt = bt
        e13[i] = c[i] if e13c is None else c[i] * (2/14) + e13c * (12/14)
        e89[i] = c[i] if e89c is None else c[i] * (2/90) + e89c * (88/90)
    return e13, e89


def t1_of(side, rpoc_or_rval, c_m, stop):
    """actual T1 as computed for the card (parity with the engine)."""
    if side == "L":
        return rpoc_or_rval if rpoc_or_rval > c_m else c_m + 2 * (c_m - stop)
    return rpoc_or_rval if rpoc_or_rval < c_m else c_m - 2 * (stop - c_m)

def build_signals(sym):
    df = load_symbol(sym)
    df = add_features(df)
    df = running_session(df)
    df = prior_levels(df)
    df["h4e13"], df["h4e89"] = h4_bias_nolookahead(df)
    sigs = []
    # EA-2 (from backtest_ea gen_signals — re-run inline, no-lookahead-safe: uses no EMA)
    o,h,l,c,v = df.open.values, df.high.values, df.low.values, df.close.values, df.volume.values
    atr, dp = df.atr.values, df["delta_pct"].values
    rpoc, rvah, rval = df["rPOC"].values, df["rVAH"].values, df["rVAL"].values
    ph, pl = df["d_ph"].values, df["d_pl"].values
    pvah, pval = df["d_pvah"].values, df["d_pval"].values
    pwh, pwl = df["d_pwh"].values, df["d_pwl"].values
    v_sma20 = df["volume"].rolling(20).mean().values
    day = df["day"].values
    n = len(df)
    lvl_names = [("ph","PDH"),("pl","PDL"),("pvah","PD-VAH"),("pval","PD-VAL"),("pwh","PWH"),("pwl","PWL")]
    last_sweep = {}
    for j in range(30, n-3):
        if np.isnan(atr[j]) or np.isnan(v_sma20[j]) or v[j] < 1.5*v_sma20[j]: continue
        for lv, name in lvl_names:
            L = {"ph":ph,"pl":pl,"pvah":pvah,"pval":pval,"pwh":pwh,"pwl":pwl}[lv][j]
            if np.isnan(L): continue
            if last_sweep.get(name) == day[j]: continue
            if c[j] < L and l[j] < L and h[j] >= L and (L-l[j])/atr[j] <= 1.5:
                for m in range(j+1, min(j+4, n)):
                    if c[m] > L and dp[m] > 0.15 and c[m] > o[m]:
                        stop = l[j:m+1].min() - 0.05*atr[m]
                        sigs.append({"ea":"EA2","i":m,"side":"L","px":c[m],"stop":stop,
                                     "t1":(_t1:=rpoc[m] if rpoc[m]>c[m] else c[m]+2*(c[m]-stop)),
                                     "t2":rvah[m] if rvah[m]>_t1 else c[m]+2.5*(c[m]-stop),
                                     "t3":c[m]+3*(c[m]-stop)})
                        last_sweep[name] = day[j]; break
            if c[j] > L and h[j] > L and l[j] <= L and (h[j]-L)/atr[j] <= 1.5:
                for m in range(j+1, min(j+4, n)):
                    if c[m] < L and dp[m] < -0.15 and c[m] < o[m]:
                        stop = h[j:m+1].max() + 0.05*atr[m]
                        sigs.append({"ea":"EA2","i":m,"side":"S","px":c[m],"stop":stop,
                                     "t1":(_t1:=rpoc[m] if rpoc[m]<c[m] else c[m]-2*(stop-c[m])),
                                     "t2":rval[m] if rval[m]<_t1 else c[m]-2.5*(stop-c[m]),
                                     "t3":c[m]-3*(stop-c[m])})
                        last_sweep[name] = day[j]; break
    # EA-5 (ETH/SOL only)
    vz = df["vz"].values; vwap = df["vwap"].values
    if sym in ("ETHUSDT","SOLUSDT"):
        cascade_day = {}
        for j in range(30, n-5):
            if np.isnan(vz[j]) or vz[j] < 3.0: continue
            d = day[j]
            if c[j] < min(l[max(0,j-12):j]) and c[j] < vwap[j]:
                key=("L",d)
                if cascade_day.get(key,0)>=1: continue
                for m in range(j+1, min(j+6, n)):
                    dp3 = dp[m-2:m+1].sum()
                    if dp3 > 0.05 and c[m] > l[m]+0.5*(h[m]-l[m]) and c[m] > c[m-1]:
                        stop = l[j:m+1].min() - 0.1*atr[m]
                        sigs.append({"ea":"EA5","i":m,"side":"L","px":c[m],"stop":stop,
                                     "t1":vwap[m],
                                     "t2":rpoc[m] if rpoc[m]>vwap[m] else vwap[m]+(vwap[m]-stop)*1.5,
                                     "t3":c[m]+2*(c[m]-stop)})
                        cascade_day[key]=cascade_day.get(key,0)+1; break
            if c[j] > max(h[max(0,j-12):j]) and c[j] > vwap[j]:
                key=("S",d)
                if cascade_day.get(key,0)>=1: continue
                for m in range(j+1, min(j+6, n)):
                    dp3 = dp[m-2:m+1].sum()
                    if dp3 < -0.05 and c[m] < h[m]-0.5*(h[m]-l[m]) and c[m] < c[m-1]:
                        stop = h[j:m+1].max() + 0.1*atr[m]
                        sigs.append({"ea":"EA5","i":m,"side":"S","px":c[m],"stop":stop,
                                     "t1":vwap[m],
                                     "t2":rpoc[m] if rpoc[m]<vwap[m] else vwap[m]-(stop-vwap[m])*1.5,
                                     "t3":c[m]-2*(stop-c[m])})
                        cascade_day[key]=cascade_day.get(key,0)+1; break
    # EA-6 (no-lookahead)
    sigs6 = gen_ea6(df)
    for s in sigs6:
        sigs.append({"ea":"EA6","i":s["i"],"side":"L" if s["side"]=="L" else "S","px":s["px"],"stop":s["stop"],
                     "t1":s["t1"],"t2":s["t2"],"t3":s["t3"]})
    return df, sigs

def main():
    report = {}
    for sym in SYMS:
        df, sigs = build_signals(sym)
        # dedupe signals by (ea, i, side) keeping first
        seen = set(); uniq = []
        for s in sigs:
            k = (s["ea"], s["i"], s["side"])
            if k in seen: continue
            seen.add(k); uniq.append(s)
        # pick test points: spread ~40 signal indices across the dataset, at least 600 bars in
        idxs = [s["i"] for s in uniq if s["i"] > WINDOW + 50]
        if not idxs:
            report[sym] = {"tested": 0}; continue
        step = max(1, len(idxs) // 40)
        test_idx = sorted(set(idxs[::step]))[:40]
        bars = df[["open_time","open","high","low","close","volume","taker_buy_base"]].values
        matched, missed, total = 0, 0, 0
        misses = []
        for ti in test_idx:
            window = bars[ti-WINDOW+1:ti+1]
            candle_json = json.dumps({
                "sym": sym,
                "candles": [
                    {"t": int(r[0]), "o": float(r[1]), "h": float(r[2]), "l": float(r[3]),
                     "c": float(r[4]), "v": float(r[5]), "tbb": float(r[6])}
                    for r in window
                ],
            })
            proc = subprocess.run(
                ["node", "--no-warnings", "/home/z/my-project/scripts/parity_engine.mjs"],
                input=candle_json, capture_output=True, text=True, timeout=120,
            )
            if proc.returncode != 0:
                print("ENGINE ERROR at", ti, proc.stderr[:400]); missed += 1; total += 1; continue
            cards = json.loads(proc.stdout)["cards"]
            # signals expected in the last 12 bars of this window
            expected = [s for s in uniq if ti - 7 <= s["i"] <= ti]
            total += 1
            ok_all = True
            for e in expected:
                card = next((cd for cd in cards if cd["engine"] == e["ea"] and cd["signalTs"] == int(bars[e["i"]][0]) and
                             (cd["side"] == ("long" if e["side"] == "L" else "short"))), None)
                if card is None:
                    ok_all = False; misses.append({"type": "missing", "ea": e["ea"], "i": e["i"], "sym": sym}); continue
                def close(a, b): return abs(a - b) <= max(TOL, abs(b) * 1e-9)
                if not (close(card["entry"], e["px"]) and close(card["stop"], e["stop"]) and
                        close(card["targets"][0], e["t1"]) and close(card["targets"][1], e["t2"]) and close(card["targets"][2], e["t3"])):
                    ok_all = False
                    misses.append({"type": "mismatch", "ea": e["ea"], "i": e["i"], "sym": sym,
                                   "ts": card["entry"], "want_px": e["px"], "card_stop": card["stop"], "want_stop": e["stop"],
                                   "card_t": list(card["targets"]), "want_t": [e["t1"], e["t2"], e["t3"]]})
            # phantom check: cards that are NOT expected (excluding ARM previews)
            phantom = [cd for cd in cards if not cd["id"].startswith("EA2-ARM-") and
                       not any(cd["engine"] == e["ea"] and cd["signalTs"] == int(bars[e["i"]][0]) for e in expected)]
            if phantom:
                ok_all = False
                misses.append({"type": "phantom", "sym": sym, "i": ti, "ids": [p["id"] for p in phantom][:4]})
            if ok_all: matched += 1
            else: missed += 1
        report[sym] = {"windows_tested": total, "matched": matched, "missed": missed,
                       "n_signals_total": len(uniq), "sample_misses": misses[:8]}
        print(f"{sym}: windows={total} matched={matched} missed={missed} (signals in dataset: {len(uniq)})")
        for m in misses[:8]:
            print("   ", json.dumps(m)[:220])
    json.dump(report, open(f"{OUT}/parity_report.json", "w"), indent=1)
    tot_m = sum(r.get("matched", 0) for r in report.values())
    tot = sum(r.get("windows_tested", 0) for r in report.values())
    print(f"TOTAL windows={tot} matched={tot_m} ({100*tot_m/max(tot,1):.0f}%)")

if __name__ == "__main__":
    main()
