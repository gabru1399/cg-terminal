#!/usr/bin/env python3
"""Robustness diagnostics for the EA backtest results (pre-playbook)."""
import json
import pandas as pd
import numpy as np

OUT = "/home/z/my-project/data/backtest"
res = pd.read_csv(f"{OUT}/trades.csv", parse_dates=["entry_dt", "exit_dt"])
res["r"] = pd.to_numeric(res["r"], errors="coerce")
res["month"] = res["entry_dt"].dt.strftime("%Y-%m")

diag = {}
for ea in ["EA2", "EA5"]:
    sub = res[res.ea == ea]
    d = {}
    d["by_side"] = {s: {"n": int(len(g)), "sumR": round(g.r.sum(), 1), "wr": round(float((g.r > 0).mean()), 2)}
                    for s, g in sub.groupby("side")}
    d["by_exit"] = {k: {"n": int(len(g)), "sumR": round(g.r.sum(), 1)}
                    for k, g in sub.groupby("reason")}
    d["by_month"] = {m: {"n": int(len(g)), "sumR": round(g.r.sum(), 1), "wr": round(float((g.r > 0).mean()), 2)}
                     for m, g in sub.groupby("month")}
    d["median_bars"] = float(sub.bars.median())
    d["avg_bars"] = round(float(sub.bars.mean()), 1)
    d["stop_rate"] = round(float((sub.reason.str.startswith("stop")).mean()), 3)
    diag[ea] = d

# EA-2 per-level (levels were stored in trades? no — recompute from signal not possible here; skip)
print(json.dumps(diag, indent=1))
json.dump(diag, open(f"{OUT}/diag.json", "w"), indent=1)

# equity curves (cumulative R by exit date) for EA2, EA5, EA2+EA5, and the failed pool for contrast
eq = {}
for name, mask in [("EA2", res.ea == "EA2"), ("EA5", res.ea == "EA5"),
                   ("EA2+EA5", res.ea.isin(["EA2", "EA5"])), ("EA1+EA3+EA4", res.ea.isin(["EA1", "EA3", "EA4"]))]:
    sub = res[mask].sort_values("exit_dt")
    eq[name] = {"t": [t.isoformat() for t in sub.exit_dt], "r": [round(x, 2) for x in sub.r.cumsum()]}
json.dump(eq, open(f"{OUT}/equity.json", "w"))
print("equity curves saved; EA2+EA5 final R:", round(res[res.ea.isin(["EA2","EA5"])].r.sum(), 1))
