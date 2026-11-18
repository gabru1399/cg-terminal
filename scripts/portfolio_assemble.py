#!/usr/bin/env python3
"""Portfolio assembly (R547): validated engines -> risk weights, combined stats, diversification."""
import json
import numpy as np
import pandas as pd

OUT = "/home/z/my-project/data/backtest"
r1 = pd.read_csv(f"{OUT}/trades.csv", parse_dates=["entry_dt", "exit_dt"]).dropna(subset=["exit_dt"])
r2 = pd.read_csv(f"{OUT}/trades_v2.csv", parse_dates=["entry_dt", "exit_dt"]).dropna(subset=["exit_dt"])
res = pd.concat([r1, r2], ignore_index=True)
res["day"] = pd.to_datetime(res.exit_dt).dt.date

# engines: EA-2 (all), EA-5 (ETH/SOL), EA-6 (all)
eng = {
    "EA2": res[res.ea == "EA2"],
    "EA5": res[(res.ea == "EA5") & (res.sym != "BTCUSDT")],
    "EA6": res[res.ea == "EA6"],
}
stats = {}
for k, sub in eng.items():
    rs = sub.sort_values("exit_dt").r.values
    eq = np.cumsum(rs); dd = float((np.maximum.accumulate(eq) - eq).max())
    wins = rs[rs > 0]; losses = rs[rs <= 0]
    stats[k] = {"n": int(len(rs)), "sumR": round(float(rs.sum()), 1), "pf": round(float(wins.sum() / abs(losses.sum())), 2),
                "wr": round(float((rs > 0).mean()), 3), "avgR": round(float(rs.mean()), 3), "maxDD_R": round(dd, 1)}

# inverse-DD risk weights (capped 0.5-1.5)
inv = {k: 1.0 / max(stats[k]["maxDD_R"], 1) for k in eng}
tot = sum(inv.values())
w_raw = {k: inv[k] / tot for k in inv}
w = {k: float(np.clip(w_raw[k] * (tot / 3) / w_raw[k] if False else w_raw[k] / max(w_raw.values()), 0.5, 1.5)) for k in w_raw}
wn = {k: round(v / sum(w.values()), 3) for k, v in w.items()}

# daily R per engine -> correlation matrix + portfolio daily series
daily = {}
for k, sub in eng.items():
    daily[k] = sub.groupby("day").r.sum()
ddf = pd.DataFrame(daily).fillna(0.0)
corr = ddf.corr().round(2)
port_daily = sum(ddf[k] * wn[k] for k in ddf.columns)
port_trades = pd.concat([sub.assign(w=wn[k]) for k, sub in eng.items()]).sort_values("exit_dt")
port_trades["wr_"] = port_trades.r * port_trades.w
rs_eq = port_trades.wr_.cumsum()
pdd = float((np.maximum.accumulate(rs_eq) - rs_eq).max())
psum = float(port_trades.wr_.sum())
pw = port_trades.wr_.values
wins = pw[pw > 0]; losses = pw[pw <= 0]
days = sorted(set(port_trades.exit_dt.dt.date))
ndays = (pd.Timestamp(max(days)) - pd.Timestamp(min(days))).days + 1
sharpe_d = float(port_daily.mean() / port_daily.std()) if port_daily.std() > 0 else None
monthly = port_trades.copy()
monthly["m"] = pd.to_datetime(monthly.exit_dt).dt.strftime("%Y-%m")
mstat = {m: {"R": round(g.wr_.sum(), 1), "n": int(len(g))} for m, g in monthly.groupby("m")}

out = {
    "engines": stats,
    "weights": wn,
    "portfolio": {"sumR_weighted": round(psum, 1), "pf": round(float(wins.sum() / abs(losses.sum())), 2),
                  "wr": round(float((pw > 0).mean()), 3), "maxDD_R": round(pdd, 1),
                  "n_trades": int(len(pw)), "trades_per_day": round(len(pw) / ndays, 2),
                  "daily_sharpe_R": round(sharpe_d, 3) if sharpe_d else None,
                  "avg_daily_R": round(float(port_daily.mean()), 3)},
    "correlation": corr.to_dict(),
    "monthly": mstat,
}
print(json.dumps(out, indent=1))
json.dump(out, open(f"{OUT}/portfolio.json", "w"), indent=1)

# portfolio equity curve for the chart
port_trades[["exit_dt", "wr_"]].rename(columns={"wr_": "r"}).to_csv(f"{OUT}/equity_portfolio.csv", index=False)
print("saved equity_portfolio.csv")
