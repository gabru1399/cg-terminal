#!/usr/bin/env python3
"""
EA-6 re-validation with NO-LOOKAHEAD h4 EMA bias (R548 verification round).

Finding: R547's EA-6 used h4e13/h4e89 computed via pandas resample().asof(t),
which returns the EMA including the CONTAINING 4h bucket's FINAL close — i.e.
up to 3h45m of future data at signal time. EA-2/EA-5 use no EMA gates (clean).
This script recomputes the h4 bias with the forming bucket's close-so-far
(exactly what a live trader sees) and re-runs the IDENTICAL EA-6 rules.
Everything else (swings, FVG wide zone, BOS, stops, targets, sim) is unchanged
from scripts/backtest_portfolio.py.
"""
import sys, json
sys.path.insert(0, "/home/z/my-project/scripts")
import numpy as np
import pandas as pd
from backtest_ea import load_symbol, add_features, running_session, prior_levels, simulate, FEE_TAKER
from backtest_portfolio import gen_ea6, OUT, SYMS

K13, K89 = 2 / 14, 2 / 90

def h4_bias_nolookahead(df):
    """Per-bar h4 EMA13/89 with the forming bucket's close-so-far (no future data)."""
    t = df["open_time"].values
    c = df["close"].values
    n = len(df)
    e13 = np.full(n, np.nan); e89 = np.full(n, np.nan)
    e13c = e89c = None
    cur_bt = None
    for i in range(n):
        bt = t[i] // (4 * 3_600_000)
        if cur_bt is None:
            cur_bt = bt
        elif bt != cur_bt:
            cc = c[i - 1]  # previous bucket completed with its final close
            if e13c is None:
                e13c = e89c = cc
            else:
                e13c = cc * K13 + e13c * (1 - K13)
                e89c = cc * K89 + e89c * (1 - K89)
            cur_bt = bt
        if e13c is None:
            e13[i] = e89[i] = c[i]
        else:
            e13[i] = c[i] * K13 + e13c * (1 - K13)
            e89[i] = c[i] * K89 + e89c * (1 - K89)
    return e13, e89

def main():
    rows = []
    for sym in SYMS:
        df = load_symbol(sym)
        df = add_features(df)
        d1 = df.set_index("dt")[["high", "low", "close"]].resample("1D").agg({"high": "max", "low": "min", "close": "last"}).dropna()
        pc = d1["close"].shift(1)
        tr1 = pd.concat([d1["high"] - d1["low"], (d1["high"] - pc).abs(), (d1["low"] - pc).abs()], axis=1).max(axis=1)
        df["atr_d"] = df["dt"].dt.floor("D").map(tr1.rolling(14).mean())
        df = running_session(df)
        df = prior_levels(df)
        # corrected bias
        df["h4e13"], df["h4e89"] = h4_bias_nolookahead(df)
        sigs = gen_ea6(df)
        for s in sigs:
            s["sym"] = sym
        trs = simulate(df, sym, sigs, max_hold=96, time_stop_bars=8)
        for tr in trs:
            rows.append({"ea": "EA6nl", "sym": sym, "side": tr.side,
                         "entry_dt": df.dt.iloc[tr.entry_i],
                         "exit_dt": df.dt.iloc[tr.close_i] if tr.close_i is not None else None,
                         "r": tr.r - tr.fees_r, "reason": tr.exit_reason, "bars": tr.bars_held})
    res = pd.DataFrame(rows).dropna(subset=["exit_dt"])
    res.to_csv(f"{OUT}/trades_ea6_nolookahead.csv", index=False)
    rs = res["r"].values
    wins = rs[rs > 0]; losses = rs[rs <= 0]
    eq = np.cumsum(rs); dd = float((np.maximum.accumulate(eq) - eq).max())
    out = {"n": int(len(rs)), "winrate": round(float((rs > 0).mean()), 3),
           "avgR": round(float(rs.mean()), 3), "sumR": round(float(rs.sum()), 1),
           "pf": round(float(wins.sum() / abs(losses.sum())), 2),
           "maxDD_R": round(dd, 1)}
    print("EA-6 NO-LOOKAHEAD:", json.dumps(out))
    for s in SYMS:
        ss = res[res.sym == s]["r"]
        print(f"  {s}: n={len(ss)} sumR={ss.sum():.1f} wr={(ss > 0).mean():.3f}")
    # month breakdown
    res["m"] = pd.to_datetime(res.entry_dt).dt.strftime("%Y-%m")
    print("  by_month:", {m: round(g.r.sum(), 1) for m, g in res.groupby("m")})
    # how often did the corrected bias flip vs the lookahead one?
    flips = 0
    for sym in SYMS:
        df = pd.read_pickle(f"{OUT}/{sym}.pkl")
        e13, e89 = h4_bias_nolookahead(df)
        old_up = (df["h4e13"] > df["h4e89"]).values
        new_up = e13 > e89
        flips += int((old_up != new_up).sum())
    print(f"  bias-flip bars (old vs new): {flips}")

if __name__ == "__main__":
    main()
