#!/usr/bin/env python3
"""Charts for the EA validation report: equity curves + per-symbol breakdown."""
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT = "/home/z/my-project/data/backtest"
CH = "/home/z/my-project/download/charts"
import os; os.makedirs(CH, exist_ok=True)

res = pd.read_csv(f"{OUT}/trades.csv", parse_dates=["entry_dt", "exit_dt"])
res["r"] = pd.to_numeric(res["r"], errors="coerce")
res = res.dropna(subset=["exit_dt"])  # open-at-end trades excluded from realized equity

GOLD = "#C9A84C"; DARK = "#1A1A1A"; GREY = "#8A8A8A"; GREEN = "#4C7A4C"; RED = "#A04C4C"; BLUE = "#4C6A9A"

# --- Chart 1: equity curves ---
fig, ax = plt.subplots(figsize=(9, 4.6), constrained_layout=True)
series = {
    "EA-2 sweep-acceptance (all 3 syms)": (res[res.ea == "EA2"], GOLD),
    "EA-5 cascade exhaustion (ETH+SOL)": (res[(res.ea == "EA5") & (res.sym != "BTCUSDT")], BLUE),
    "Combined live set": (res[((res.ea == "EA2") | ((res.ea == "EA5") & (res.sym != "BTCUSDT")))], GREEN),
    "EA-1/3/4 (suspended rules)": (res[res.ea.isin(["EA1", "EA3", "EA4"])], RED),
}
for name, (sub, color) in series.items():
    sub = sub.sort_values("exit_dt")
    ax.plot(sub.exit_dt, sub.r.cumsum(), label=f"{name}  ({sub.r.sum():+.0f}R)", color=color, lw=1.6 if "Combined" not in name else 2.2)
ax.axhline(0, color=GREY, lw=0.8, ls="--")
ax.set_title("Net R equity — real Binance USDT-M 15m data, 2026-05-01 → 11-17 (fees + slippage included)", fontsize=10)
ax.set_ylabel("cumulative R (1R = risked amount)")
ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
ax.grid(alpha=0.25)
fig.savefig(f"{CH}/ea_equity.png", dpi=150)
plt.close(fig)

# --- Chart 2: per-symbol sumR by EA ---
d = json.load(open(f"{OUT}/results.json"))["by_symbol_detail"]
eas = ["EA1", "EA2", "EA3", "EA4", "EA5"]
syms = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
x = np.arange(len(eas)); w = 0.26
fig, ax = plt.subplots(figsize=(9, 4.2), constrained_layout=True)
for k, (s, col) in enumerate(zip(syms, [DARK, BLUE, GOLD])):
    vals = [d[s][e]["sumR"] for e in eas]
    ax.bar(x + (k-1)*w, vals, w, label=s, color=col, alpha=0.9)
ax.axhline(0, color=GREY, lw=0.8)
ax.set_xticks(x); ax.set_xticklabels(["EA-1\nOFI trend", "EA-2\nsweep-acc", "EA-3\nVA reversion", "EA-4\nORB", "EA-5\ncascade"], fontsize=9)
ax.set_ylabel("net R per symbol (200 days)")
ax.set_title("Which archetype works where — per-symbol net R", fontsize=10)
ax.legend(fontsize=8); ax.grid(alpha=0.25, axis="y")
fig.savefig(f"{CH}/ea_by_symbol.png", dpi=150)
plt.close(fig)

for f in ["ea_equity.png", "ea_by_symbol.png"]:
    from PIL import Image
    im = Image.open(f"{CH}/{f}").convert("L")
    h = im.histogram()
    print(f, im.size, "non-white:", round(1 - h[255]/sum(h), 3))

# final portfolio math (printed, for the report)
live = res[(res.ea == "EA2") | ((res.ea == "EA5") & (res.sym != "BTCUSDT"))].sort_values("exit_dt")
rs = live.r
print("LIVE SET: n=", len(rs), "sumR=", round(rs.sum(),1), "wr=", round(float((rs>0).mean()),3),
      "avgR=", round(float(rs.mean()),3), "trades/day=", round(len(rs)/201,2))
eq = rs.cumsum(); print("maxDD_R=", round(float((np.maximum.accumulate(eq)-eq).max()),1))
rs2 = res[res.ea=="EA2"].r
print("EA2 daily-avg R:", round(rs2.sum()/201, 2), "| EA5 ethsol sumR:", round(res[(res.ea=="EA5")&(res.sym!="BTCUSDT")].r.sum(),1))
