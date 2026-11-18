#!/usr/bin/env python3
"""Beta panel: rolling betas vs BTC from local m15 klines (518 bars ~5.4 days).
Outputs beta, corr, R2, idiosyncratic vol, and today's realized alpha for all
Gate-7 micro-assets + TradFi slot-2 candidates."""
import json, numpy as np, os

DIR = "/home/z/my-project/data/cg-series"

def load(sym):
    rows = []
    with open(f"{DIR}/kline_Binance_{sym}USDT_m15.jsonl") as f:
        for line in f:
            r = json.loads(line)
            rows.append((r["t"], r["c"]))
    return dict(rows)

btc = load("BTC")
syms = ["APT","ADA","ARB","TIA","SEI","DOGE","VET","LINK","SOL","ETH",
        "NVDA","MSFT","AVGO","MSTR","XAU","XAG","SNDK","MU","AMD","META"]

out = {}
print(f"{'sym':6} {'beta':>6} {'corr':>6} {'R2':>5} {'idio_vol_ann':>12} {'alpha_24h(%IDIO)':>16} {'n':>4}")
for s in syms:
    try:
        px = load(s)
        common = sorted(set(btc) & set(px))
        # 1h returns from m15 (every 4th bar) to cut m15 noise
        ts = common[::4]
        rets_s, rets_b = [], []
        for i in range(1, len(ts)):
            rets_s.append(px[ts[i]] / px[ts[i-1]] - 1)
            rets_b.append(btc[ts[i]] / btc[ts[i-1]] - 1)
        a = np.array(rets_s); b = np.array(rets_b)
        n = len(a)
        beta = np.cov(a, b)[0, 1] / np.var(b)
        corr = np.corrcoef(a, b)[0, 1]
        r2 = corr ** 2
        resid = a - beta * b
        idio_vol_h = np.std(resid)
        idio_vol_ann = idio_vol_h * np.sqrt(24 * 365) * 100
        # last 24h realized idio alpha (sum of residuals, last 24 hourly bars)
        alpha24 = resid[-24:].sum() * 100
        out[s] = {"beta": round(float(beta), 2), "corr": round(float(corr), 2),
                  "r2": round(float(r2), 2), "idio_vol_ann_pct": round(float(idio_vol_ann), 1),
                  "alpha_24h_pct": round(float(alpha24), 2), "n": n}
        print(f"{s:6} {beta:>6.2f} {corr:>6.2f} {r2:>5.2f} {idio_vol_ann:>12.1f} {alpha24:>16.2f} {n:>4}")
    except FileNotFoundError:
        print(f"{s:6} no data")

json.dump(out, open("/tmp/inquest_beta.json", "w"), indent=1)
print("saved /tmp/inquest_beta.json")
