#!/usr/bin/env python3
"""R547 charts: portfolio equity vs engines."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT = "/home/z/my-project/data/backtest"
CH = "/home/z/my-project/download/charts"

r1 = pd.read_csv(f"{OUT}/trades.csv", parse_dates=["entry_dt", "exit_dt"]).dropna(subset=["exit_dt"])
r2 = pd.read_csv(f"{OUT}/trades_v2.csv", parse_dates=["entry_dt", "exit_dt"]).dropna(subset=["exit_dt"])
res = pd.concat([r1, r2], ignore_index=True)

port = pd.read_csv(f"{OUT}/equity_portfolio.csv", parse_dates=["exit_dt"]).sort_values("exit_dt")
GOLD, BLUE, GREEN, RED, GREY = "#C9A84C", "#4C6A9A", "#4C7A4C", "#A04C4C", "#8A8A8A"

fig, ax = plt.subplots(figsize=(9, 4.6), constrained_layout=True)
ax.plot(port.exit_dt, port.r.cumsum(), label="3-engine portfolio (weighted)  +130.8R · maxDD 25.6R", color=GREEN, lw=2.2)
for k, sub, col, lbl in [
    ("EA2", res[res.ea == "EA2"], GOLD, "EA-2 alone  +113.1R · maxDD 19.9R"),
    ("EA6", res[res.ea == "EA6"], BLUE, "EA-6 alone (SMC)  +206.9R · maxDD 65.6R"),
    ("EA5", res[(res.ea == "EA5") & (res.sym != "BTCUSDT")], RED, "EA-5 alone (ETH/SOL)  +104.2R"),
]:
    sub = sub.sort_values("exit_dt")
    ax.plot(sub.exit_dt, sub.r.cumsum(), label=lbl, color=col, lw=1.3, alpha=0.85)
ax.axhline(0, color=GREY, lw=0.8, ls="--")
ax.set_title("3-engine portfolio vs individual engines — real Binance 15m data, net R (2026-05-01 → 11-17)", fontsize=10)
ax.set_ylabel("cumulative R (weighted for portfolio)")
ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
ax.grid(alpha=0.25)
fig.savefig(f"{CH}/r547_portfolio_equity.png", dpi=150)
plt.close(fig)
from PIL import Image
im = Image.open(f"{CH}/r547_portfolio_equity.png").convert("L"); h = im.histogram()
print("r547_portfolio_equity.png", im.size, "non-white:", round(1 - h[255]/sum(h), 3))
