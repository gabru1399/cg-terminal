#!/usr/bin/env python3
"""
End-to-end backtest of the desk's EA-1..EA-5 entry archetypes on REAL
Binance USDT-M futures 15m klines (data.binance.vision dump, 2026-05-01..2026-11-17).

Honesty rules encoded in the engine:
- No lookahead: every signal at bar i uses data <= i only. VA levels update on
  bars-so-far (running value area), prior-day/week levels are finalized values.
- Conservative fills: market entries at signal-bar close; limit entries fill on
  touch (no price improvement); if a bar touches BOTH stop and a target, the
  STOP fills first (worst case); stop exits get slippage.
- Costs: maker 0.02%, taker 0.05%, stop slippage 0.02% — net-of-cost stats.
- Spec invariants: breakeven stop move at +1R excursion, 8-bar (2h) time stop
  below +0.5R, 40/40/20 scale-out ladder.
- Archetype rules are pre-registered here BEFORE seeing results; any later
  recalibration must be logged as such.
"""
import glob, json, os, zipfile, io
import numpy as np
import pandas as pd

RAW = "/home/z/my-project/data/backtest/raw"
OUT = "/home/z/my-project/data/backtest"
SYMS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
FEE_MAKER, FEE_TAKER, SLIP = 0.0002, 0.0005, 0.0002
RISK = 100.0  # $ risked per trade for $P&L stats (1R = 100)

COLS = ["open_time","open","high","low","close","volume","close_time","quote_vol",
        "trades","taker_buy_base","taker_buy_quote","ignore"]

def load_symbol(sym):
    files = sorted(glob.glob(f"{RAW}/{sym}-15m-*.zip"))
    assert len(files) == 23, f"{sym}: expected 23 archives, got {len(files)}"
    frames = []
    for f in files:
        with zipfile.ZipFile(f) as z:
            name = z.namelist()[0]
            with z.open(name) as fh:
                df = pd.read_csv(fh, header=None, names=COLS)
        if df.iloc[0, 0] == "open_time":  # header row variant
            df = pd.read_csv(io.BytesIO(open(f,'rb').read() and zipfile.ZipFile(f).read(name)), header=1, names=COLS)
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    for c in COLS[:10]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open_time","open","high","low","close","volume"]).reset_index(drop=True)
    df["dt"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df = df.drop_duplicates("open_time").sort_values("open_time").reset_index(drop=True)
    # integrity: contiguous 15m grid
    gaps = df["open_time"].diff().dropna().ne(900_000).sum()
    print(f"{sym}: {len(df)} bars {df.dt.iloc[0]} -> {df.dt.iloc[-1]} | gaps={gaps} | zerovol={(df.volume==0).sum()}")
    return df

def add_features(df):
    o,h,l,c,v = df.open, df.high, df.low, df.close, df.volume
    tp = (h + l + c) / 3.0
    df["tp"] = tp
    delta = 2*df.taker_buy_base - v
    df["delta"] = delta                                      # signed taker flow, base units
    v_sma = v.rolling(20).mean(); v_std = v.rolling(20).std()
    df["vz"] = (v - v_sma) / v_std.replace(0, np.nan)          # volume z-score
    df["of"] = (delta.rolling(3).sum()) / (v.rolling(3).sum().replace(0, np.nan))  # 3-bar OFI proxy [-1,1]
    df["delta_pct"] = delta / v.replace(0, np.nan)
    # ATR14
    pc = c.shift(1)
    tr = pd.concat([h-l, (h-pc).abs(), (l-pc).abs()], axis=1).max(axis=1)
    df["atr"] = tr.rolling(14).mean()
    # EMAs
    for n in (13, 89):
        df[f"ema{n}"] = c.ewm(span=n, adjust=False).mean()
    # h1/h4 EMA via resample
    for per, tag in (("1h","h1"), ("4h","h4")):
        r = df.set_index("dt")[["open","high","low","close"]].resample(per).agg(
            {"open":"first","high":"max","low":"min","close":"last"}).dropna()
        for n in (13, 89):
            r[f"e{n}"] = r["close"].ewm(span=n, adjust=False).mean()
        m = pd.Series(r.index, index=r.index).to_frame("edge")
        df[f"{tag}e13"] = df["dt"].map(lambda t: r[f"e13"].asof(t))
        df[f"{tag}e89"] = df["dt"].map(lambda t: r[f"e89"].asof(t))
    # daily session id (UTC) and running VWAP + running value area
    df["day"] = df["dt"].dt.floor("D")
    # RVOL: same time-of-day slot vs trailing 20-day mean of that slot
    df["slot"] = df["dt"].dt.strftime("%H:%M")
    slot_mean = df.groupby("slot")["volume"].transform(lambda s: s.shift(1).rolling(20, min_periods=10).mean())
    df["rvol_slot"] = v / slot_mean.replace(0, np.nan)
    # ORB baseline: prior-20-day mean of first-2-bar (00:00-00:30 UTC) volume
    first2 = df.groupby("day")["volume"].apply(lambda g: g.iloc[:2].sum())
    df["orb_base"] = df["day"].map(first2.shift(1).rolling(20, min_periods=10).mean())
    df["swing_hi"] = (h > h.shift(1)) & (h > h.shift(2)) & (h > h.shift(-1)) & (h > h.shift(-2))
    df["swing_lo"] = (l < l.shift(1)) & (l < l.shift(2)) & (l < l.shift(-1)) & (l < l.shift(-2))
    df["fvg_bull"] = l > h.shift(2)
    df["fvg_bear"] = h < l.shift(2)
    return df

def running_session(df):
    """Per bar: running VWAP, sigma, POC/VAH/VAL of the CURRENT session (bars so far) — live-terminal semantics."""
    n = len(df); vwap = np.full(n, np.nan); sig = np.full(n, np.nan)
    poc = np.full(n, np.nan); vah = np.full(n, np.nan); val = np.full(n, np.nan)
    day_ids = df["day"].values
    tp = df["tp"].values; v = df["volume"].values; h = df["high"].values; l = df["low"].values
    i = 0
    while i < n:
        j = i
        while j < n and day_ids[j] == day_ids[i]:
            j += 1
        cv = np.cumsum(v[i:j]); ctpv = np.cumsum(tp[i:j]*v[i:j])
        vw = ctpv / np.maximum(cv, 1e-12)
        dev = tp[i:j] - vw
        sd = np.sqrt(np.maximum(np.cumsum(dev*dev*v[i:j]) / np.maximum(cv, 1e-12), 0))
        # running volume profile: 48 bins across the session-so-far price range
        for k in range(i, j):
            kk = k - i + 1
            vw_k = vw[kk-1]; sd_k = sd[kk-1]
            vwap[k] = vw_k; sig[k] = sd_k
            lo_p, hi_p = l[i:k+1].min(), h[i:k+1].max()
            if hi_p <= lo_p or v[i:k+1].sum() <= 0:
                poc[k] = vah[k] = val[k] = tp[k]; continue
            bins = np.clip(((tp[i:k+1]-lo_p)/(hi_p-lo_p)*47).astype(int), 0, 47)
            prof = np.bincount(bins, weights=v[i:k+1], minlength=48)
            p = int(np.argmax(prof)); total = prof.sum()
            va = prof[p]/total; lo_i = hi_i = p
            while va < 0.70 and (lo_i > 0 or hi_i < 47):
                up = prof[hi_i+1] if hi_i < 47 else -1
                dn = prof[lo_i-1] if lo_i > 0 else -1
                if up >= dn and hi_i < 47: hi_i += 1; va += prof[hi_i]/total
                elif lo_i > 0:             lo_i -= 1; va += prof[lo_i]/total
                else:                      hi_i += 1; va += prof[hi_i]/total
            bw = (hi_p-lo_p)/48
            poc[k] = lo_p + (p+0.5)*bw
            vah[k] = lo_p + (hi_i+1)*bw
            val[k] = lo_p + lo_i*bw
        i = j
    df["vwap"], df["sigma"] = vwap, sig
    df["rPOC"], df["rVAH"], df["rVAL"] = poc, vah, val
    return df

def prior_levels(df):
    """Finalized prior-day H/L/VAH/VAL/POC (known at 00:00) and prior ISO-week H/L."""
    g = df.groupby("day")
    daily = g.agg(hi=("high","max"), lo=("low","min"), vw=("vwap","last"),
                  poc=("rPOC","last"), vah=("rVAH","last"), val=("rVAL","last"))
    daily["ph"] = daily["hi"].shift(1); daily["pl"] = daily["lo"].shift(1)
    daily["pvah"] = daily["vah"].shift(1); daily["pval"] = daily["val"].shift(1)
    daily["ppoc"] = daily["poc"].shift(1)
    wk = daily["hi"].resample("W-MON", label="left", closed="left").max()
    wkl = daily["lo"].resample("W-MON", label="left", closed="left").min()
    daily["pwh"] = wk.shift(1).reindex(daily.index, method="ffill")
    daily["pwl"] = wkl.shift(1).reindex(daily.index, method="ffill")
    for c in daily.columns:
        df["d_"+c] = df["day"].map(daily[c])
    return df

# ---------- execution engine ----------
class Trade:
    __slots__ = ("ea","sym","side","entry_i","entry_px","stop","t1","t2","t3",
                 "rem","r_done","be","closed","close_i","close_px","r","fees_r","bars_held","exit_reason")
    def __init__(self, ea, sym, side, ei, px, stop, t1, t2, t3):
        self.ea, self.sym, self.side = ea, sym, side
        self.entry_i, self.entry_px, self.stop = ei, px, stop
        self.t1, self.t2, self.t3 = t1, t2, t3
        sd = abs(px - stop)
        self.rem = {"t1": 0.40, "t2": 0.40, "t3": 0.20}
        self.r_done = 0.0; self.be = False
        self.closed = False; self.close_i = None; self.close_px = None
        self.r = 0.0; self.fees_r = 0.0; self.bars_held = 0; self.exit_reason = ""

def r_of(tr, px):
    return (px - tr.entry_px)/tr.sd if tr.side=="L" else (tr.entry_px - px)/tr.sd

Trade.sd = property(lambda self: abs(self.entry_px - self.stop))

def simulate(df, sym, signals, max_hold=96, time_stop_bars=8, eod_flat=False, max_per_day=99):
    """signals: list of dicts {ea, i, side, kind('mkt'|'lim'), px, stop, t1, t2, t3}"""
    trades = []; pending = []
    o,h,l,c,v = df.open.values, df.high.values, df.low.values, df.close.values, df.volume.values
    days = df["day"].values
    sig_by_i = {}
    for s in signals:
        sig_by_i.setdefault(s["i"], []).append(s)
    per_day_count = {}
    n = len(df)
    for i in range(n):
        # --- manage open trades first (worst-case: stop before target) ---
        for tr in [t for t in trades if not t.closed]:
            tr.bars_held += 1
            held = i - tr.entry_i
            # EOD flat
            day_end = (i+1 >= n) or (days[i+1] != days[i])
            if eod_flat and day_end:
                px = c[i]
                rem_total = sum(tr.rem.values())
                tr.r += r_of(tr, px) * rem_total
                tr.fees_r += FEE_TAKER * px/tr.sd * rem_total
                tr.rem = {}
                tr.closed = True; tr.close_i = i; tr.close_px = px; tr.exit_reason = "eod"
                continue
            # time stop (spec): after 8 bars below +0.5R
            if held >= time_stop_bars and not tr.closed and r_of(tr, c[i]) < 0.5 and tr.bars_held >= time_stop_bars:
                px = c[i]; rem_total = sum(tr.rem.values())
                tr.r += r_of(tr, px) * rem_total
                tr.fees_r += FEE_TAKER * px/tr.sd * rem_total
                tr.rem = {}
                tr.closed = True; tr.close_i = i; tr.close_px = px; tr.exit_reason = "time_stop"
                continue
            if held >= max_hold:
                px = c[i]; rem_total = sum(tr.rem.values())
                tr.r += r_of(tr, px) * rem_total
                tr.fees_r += FEE_TAKER * px/tr.sd * rem_total
                tr.rem = {}
                tr.closed = True; tr.close_i = i; tr.close_px = px; tr.exit_reason = "max_hold"
                continue
            side = tr.side
            # breakeven invariant: +1R excursion -> stop to entry (+fees)
            if not tr.be:
                exc = (h[i]-tr.entry_px)/tr.sd if side=="L" else (tr.entry_px-l[i])/tr.sd
                if exc >= 1.0:
                    tr.stop = tr.entry_px * (1 + 3*FEE_TAKER) if side=="L" else tr.entry_px * (1 - 3*FEE_TAKER)
                    tr.be = True
            stop_hit = l[i] <= tr.stop if side=="L" else h[i] >= tr.stop
            # targets (check AFTER stop decision within same bar = worst case)
            for tg in ("t1","t2","t3"):
                if tr.rem.get(tg, 0) <= 0: continue
                px = tr.__getattribute__(tg)
                hit = h[i] >= px if side=="L" else l[i] <= px
                if stop_hit and hit: hit = False  # stop first
            # sequence: stop first
            if stop_hit:
                px = tr.stop * (1 - SLIP) if side=="L" else tr.stop * (1 + SLIP)
                rem_total = sum(tr.rem.values())
                tr.r += r_of(tr, px) * rem_total
                tr.fees_r += (FEE_TAKER + SLIP) * px/tr.sd * rem_total
                tr.rem = {}
                tr.closed = True; tr.close_i = i; tr.close_px = px; tr.exit_reason = "stop_be" if tr.be else "stop"
                continue
            for tg in ("t1","t2","t3"):
                if tr.rem.get(tg, 0) <= 0: continue
                px = tr.__getattribute__(tg)
                hit = h[i] >= px if side=="L" else l[i] <= px
                if hit:
                    w = tr.rem.pop(tg)
                    tr.r += r_of(tr, px) * w
                    tr.fees_r += FEE_TAKER * px/tr.sd * w
                    if not tr.rem:
                        tr.closed = True; tr.close_i = i; tr.close_px = px; tr.exit_reason = "t3" if tg=="t3" else tg+"_full"
                        break
        # --- place pending limit orders (active for 8 bars) ---
        still_pending = []
        for p in pending:
            if i - p["i"] > 8: continue
            filled = l[i] <= p["px"] if p["side"]=="L" else h[i] >= p["px"]
            if filled:
                fee = FEE_MAKER if p["kind"]=="lim" else FEE_TAKER
                key = (p["ea"], days[i], p["side"])
                if per_day_count.get(key,0) >= max_per_day: continue
                tr = Trade(p["ea"], sym, p["side"], i, p["px"], p["stop"], p["t1"], p["t2"], p["t3"])
                tr.fees_r += fee * p["px"]/tr.sd
                trades.append(tr); per_day_count[key] = per_day_count.get(key,0)+1
            else:
                still_pending.append(p)
        pending = still_pending
        # --- new signals on this bar's close ---
        for s in sig_by_i.get(i, []):
            if any((not t.closed) and t.ea==s["ea"] for t in trades):  # one position per EA
                continue
            if eod_flat and df.dt.iloc[i].strftime("%H:%M") >= "23:30":  # no fresh entries near EOD
                continue
            if s["kind"] == "lim":
                pending.append(s)
            else:
                key = (s["ea"], days[i], s["side"])
                if per_day_count.get(key,0) >= max_per_day: continue
                tr = Trade(s["ea"], sym, s["side"], i, c[i], s["stop"], s["t1"], s["t2"], s["t3"])
                tr.fees_r += FEE_TAKER * c[i]/tr.sd
                trades.append(tr); per_day_count[key] = per_day_count.get(key,0)+1
    return trades

def stats(trades, label):
    rs = np.array([t.r - t.fees_r for t in trades])
    if len(rs)==0:
        return {"label":label,"n":0}
    wins = rs[rs>0]; losses = rs[rs<=0]
    eq = np.cumsum(rs); dd = (np.maximum.accumulate(eq)-eq).max() if len(eq) else 0
    return {"label":label,"n":len(rs),"winrate":round(len(wins)/len(rs),3),
            "avgR":round(rs.mean(),3),"sumR":round(rs.sum(),1),
            "pf":round(wins.sum()/abs(losses.sum()),2) if losses.sum()!=0 else None,
            "maxDD_R":round(float(dd),1),"medianR":round(float(np.median(rs)),3)}

# ---------- signal generators (pre-registered rules) ----------
def gen_signals(df, sym):
    sigs = []
    o,h,l,c,v = df.open.values, df.high.values, df.low.values, df.close.values, df.volume.values
    atr, of, dp, ema13 = df.atr.values, df["of"].values, df["delta_pct"].values, df["ema13"].values
    vwap, sig_ = df["vwap"].values, df["sigma"].values
    rpoc, rvah, rval = df["rPOC"].values, df["rVAH"].values, df["rVAL"].values
    ph, pl = df["d_ph"].values, df["d_pl"].values
    pvah, pval, ppoc = df["d_pvah"].values, df["d_pval"].values, df["d_ppoc"].values
    pwh, pwl = df["d_pwh"].values, df["d_pwl"].values
    h1e13, h1e89 = df["h1e13"].values, df["h1e89"].values
    vz, v_sma20 = df["vz"].values, df["volume"].rolling(20).mean().values
    day = df["day"].values; hhmm = df["dt"].dt.strftime("%H:%M").values
    n = len(df)

    # EA-1: trend-OFI pullback
    for i in range(30, n):
        if any(np.isnan([atr[i], vwap[i], h1e13[i], h1e89[i], of[i]])): continue
        if hhmm[i] >= "23:30": continue
        recent_low = l[max(0,i-6):i+1].min(); recent_high = h[max(0,i-6):i+1].max()
        pull_long = (l[i] <= ema13[i]) and (c[i] > ema13[i])
        pull_short = (h[i] >= ema13[i]) and (c[i] < ema13[i])
        if h1e13[i] > h1e89[i] and c[i] > vwap[i] and pull_long and of[i] >= 0.25 and c[i] > o[i]:
            stop = recent_low - 0.1*atr[i]
            t1 = rvah[i] if rvah[i] > c[i] else c[i] + 2*(c[i]-stop)
            t2 = ph[i] if ph[i] > t1 else c[i] + 2.5*(c[i]-stop)
            t3 = c[i] + 3*(c[i]-stop)
            sigs.append({"ea":"EA1","i":i,"side":"L","kind":"mkt","stop":stop,"t1":t1,"t2":t2,"t3":t3})
        if h1e13[i] < h1e89[i] and c[i] < vwap[i] and pull_short and of[i] <= -0.25 and c[i] < o[i]:
            stop = recent_high + 0.1*atr[i]
            t1 = rval[i] if rval[i] < c[i] else c[i] - 2*(stop-c[i])
            t2 = pl[i] if pl[i] < t1 else c[i] - 2.5*(stop-c[i])
            t3 = c[i] - 3*(stop-c[i])
            sigs.append({"ea":"EA1","i":i,"side":"S","kind":"mkt","stop":stop,"t1":t1,"t2":t2,"t3":t3})
    # EA-1A ablation: same WITHOUT OFI filter
    sigsA = []
    for i in range(30, n):
        if any(np.isnan([atr[i], vwap[i], h1e13[i], h1e89[i]])): continue
        if hhmm[i] >= "23:30": continue
        recent_low = l[max(0,i-6):i+1].min(); recent_high = h[max(0,i-6):i+1].max()
        if h1e13[i] > h1e89[i] and c[i] > vwap[i] and (l[i] <= ema13[i]) and (c[i] > ema13[i]) and c[i] > o[i]:
            stop = recent_low - 0.1*atr[i]
            sigsA.append({"ea":"EA1A","i":i,"side":"L","kind":"mkt","stop":stop,
                          "t1":rvah[i] if rvah[i]>c[i] else c[i]+2*(c[i]-stop),
                          "t2":ph[i] if ph[i]>c[i]+2*(c[i]-stop) else c[i]+2.5*(c[i]-stop),
                          "t3":c[i]+3*(c[i]-stop)})
        if h1e13[i] < h1e89[i] and c[i] < vwap[i] and (h[i] >= ema13[i]) and (c[i] < ema13[i]) and c[i] < o[i]:
            stop = recent_high + 0.1*atr[i]
            sigsA.append({"ea":"EA1A","i":i,"side":"S","kind":"mkt","stop":stop,
                          "t1":rval[i] if rval[i]<c[i] else c[i]-2*(stop-c[i]),
                          "t2":pl[i] if pl[i]<c[i]-2*(stop-c[i]) else c[i]-2.5*(stop-c[i]),
                          "t3":c[i]-3*(stop-c[i])})

    # EA-2: sweep-acceptance
    lvl_names = [("ph","PDH"),("pl","PDL"),("pvah","PD-VAH"),("pval","PD-VAL"),("pwh","PWH"),("pwl","PWL")]
    last_sweep = {}
    for j in range(30, n-3):
        if any(np.isnan([atr[j], v_sma20[j]])) or v[j] < 1.5*v_sma20[j]: continue
        hhmmj = hhmm[j]
        for lv, name in lvl_names:
            L = eval(lv)[j]  # noqa: per-bar level value
            if np.isnan(L): continue
            key = (name, day[j])
            if last_sweep.get(name, None) == day[j]: continue  # one sweep per level per day
            # downside sweep -> long
            if c[j] < L and l[j] < L and h[j] >= L:
                depth = (L - l[j]) / atr[j]
                if depth > 1.5: continue  # cascade-like, skip
                for m in range(j+1, min(j+4, n)):
                    if c[m] > L and dp[m] > 0.15 and c[m] > o[m]:
                        stop = l[j:m+1].min() - 0.05*atr[m]
                        t1 = rpoc[m] if rpoc[m] > c[m] else c[m]+2*(c[m]-stop)
                        t2 = rvah[m] if rvah[m] > t1 else c[m]+2.5*(c[m]-stop)
                        t3 = c[m]+3*(c[m]-stop)
                        sigs.append({"ea":"EA2","i":m,"side":"L","kind":"mkt","stop":stop,"t1":t1,"t2":t2,"t3":t3,"lvl":name})
                        last_sweep[name] = day[j]
                        break
            # upside sweep -> short
            if c[j] > L and h[j] > L and l[j] <= L:
                depth = (h[j] - L) / atr[j]
                if depth > 1.5: continue
                for m in range(j+1, min(j+4, n)):
                    if c[m] < L and dp[m] < -0.15 and c[m] < o[m]:
                        stop = h[j:m+1].max() + 0.05*atr[m]
                        t1 = rpoc[m] if rpoc[m] < c[m] else c[m]-2*(stop-c[m])
                        t2 = rval[m] if rval[m] < t1 else c[m]-2.5*(stop-c[m])
                        t3 = c[m]-3*(stop-c[m])
                        sigs.append({"ea":"EA2","i":m,"side":"S","kind":"mkt","stop":stop,"t1":t1,"t2":t2,"t3":t3,"lvl":name})
                        last_sweep[name] = day[j]
                        break

    # EA-3: prior-day VA extreme reversion (limit at level, first touch per day/side)
    touched = {}
    for i in range(30, n):
        if any(np.isnan([atr[i], pval[i], pvah[i]])): continue
        if hhmm[i] <= "00:30" or hhmm[i] >= "23:30": continue
        sd_long = ("L", day[i]); sd_short = ("S", day[i])
        if l[i] <= pval[i] and not touched.get(sd_long):
            touched[sd_long] = True
            if c[i] >= pval[i] and dp[i] > -0.10:  # held + selling exhausted
                stop = pval[i] - 0.25*(pvah[i]-pval[i])
                sigs.append({"ea":"EA3","i":i,"side":"L","kind":"lim","px":pval[i],"stop":stop,
                             "t1":ppoc[i],"t2":pvah[i],"t3":pval[i]+ (pvah[i]-pval[i])*1.5})
        if h[i] >= pvah[i] and not touched.get(sd_short):
            touched[sd_short] = True
            if c[i] <= pvah[i] and dp[i] < 0.10:
                stop = pvah[i] + 0.25*(pvah[i]-pval[i])
                sigs.append({"ea":"EA3","i":i,"side":"S","kind":"lim","px":pvah[i],"stop":stop,
                             "t1":ppoc[i],"t2":pval[i],"t3":pvah[i]- (pvah[i]-pval[i])*1.5})
    df_ea3 = df  # eod flat handled via flag below

    # EA-4: UTC ORB with RVOL gate (crypto proxy for Zarattini's session ORB)
    orb2 = {}
    for i in range(30, n):
        d = day[i]; t = hhmm[i]
        if t < "00:30" or t >= "23:45": continue
        if d not in orb2:
            idx = np.where(day == d)[0]
            if len(idx) < 2: continue
            f0, f1 = idx[0], idx[1]
            base = df["orb_base"].iloc[f0]
            orb2[d] = {"hi": h[f0:f1+1].max(), "lo": l[f0:f1+1].min(), "done": False,
                       "rvol30": v[f0:f1+1].sum() / max(base, 1e-9)}
        o_ = orb2[d]
        if o_["done"]: continue
        if o_["rvol30"] >= 1.5:
            if c[i] > o_["hi"] and o_["lo"] > 0:
                stop = max(o_["lo"], c[i] - 0.10*df["atr_d"].iloc[i] if not np.isnan(df["atr_d"].iloc[i]) else o_["lo"])
                sigs.append({"ea":"EA4","i":i,"side":"L","kind":"mkt","stop":stop,
                             "t1":c[i]+(c[i]-stop),"t2":c[i]+2*(c[i]-stop),"t3":c[i]+3*(c[i]-stop)})
                o_["done"] = True
            elif c[i] < o_["lo"]:
                stop = min(o_["hi"], c[i] + 0.10*df["atr_d"].iloc[i] if not np.isnan(df["atr_d"].iloc[i]) else o_["hi"])
                sigs.append({"ea":"EA4","i":i,"side":"S","kind":"mkt","stop":stop,
                             "t1":c[i]-(stop-c[i]),"t2":c[i]-2*(stop-c[i]),"t3":c[i]-3*(stop-c[i])})
                o_["done"] = True

    # EA-5: cascade exhaustion
    cascade_day = {}
    for j in range(30, n-5):
        if np.isnan(vz[j]) or vz[j] < 3.0: continue
        d = day[j]
        # long: cascade down bar
        if c[j] < min(l[max(0,j-12):j]) and c[j] < vwap[j]:
            key = ("L", d)
            if cascade_day.get(key, 0) >= 1: continue
            for m in range(j+1, min(j+6, n)):
                dp3 = dp[m-2:m+1].sum()
                if dp3 > 0.05 and c[m] > l[m] + 0.5*(h[m]-l[m]) and c[m] > c[m-1]:
                    stop = l[j:m+1].min() - 0.1*atr[m]
                    sigs.append({"ea":"EA5","i":m,"side":"L","kind":"mkt","stop":stop,
                                 "t1":vwap[m],"t2":rpoc[m] if rpoc[m]>vwap[m] else vwap[m]+(vwap[m]-stop)*1.5,
                                 "t3":c[m]+2*(c[m]-stop)})
                    cascade_day[key] = cascade_day.get(key,0)+1
                    break
        # short: cascade up bar
        if c[j] > max(h[max(0,j-12):j]) and c[j] > vwap[j]:
            key = ("S", d)
            if cascade_day.get(key, 0) >= 1: continue
            for m in range(j+1, min(j+6, n)):
                dp3 = dp[m-2:m+1].sum()
                if dp3 < -0.05 and c[m] < h[m] - 0.5*(h[m]-l[m]) and c[m] < c[m-1]:
                    stop = h[j:m+1].max() + 0.1*atr[m]
                    sigs.append({"ea":"EA5","i":m,"side":"S","kind":"mkt","stop":stop,
                                 "t1":vwap[m],"t2":rpoc[m] if rpoc[m]<vwap[m] else vwap[m]-(stop-vwap[m])*1.5,
                                 "t3":c[m]-2*(stop-c[m])})
                    cascade_day[key] = cascade_day.get(key,0)+1
                    break
    return sigs, sigsA

def main():
    all_rows = []
    summary = {}
    for sym in SYMS:
        df = load_symbol(sym)
        df = add_features(df)
        # daily ATR for ORB stop
        d1 = df.set_index("dt")[["high","low","close"]].resample("1D").agg({"high":"max","low":"min","close":"last"}).dropna()
        pc = d1["close"].shift(1)
        tr1 = pd.concat([d1["high"]-d1["low"], (d1["high"]-pc).abs(), (d1["low"]-pc).abs()], axis=1).max(axis=1)
        df["atr_d"] = df["dt"].dt.floor("D").map(tr1.rolling(14).mean())
        df = running_session(df)
        df = prior_levels(df)
        sigs, sigsA = gen_signals(df, sym)
        for s in sigs: s["sym"] = sym
        for s in sigsA: s["sym"] = sym
        # EA-3/EA-4 are EOD-flat archetypes
        for ea, eod in (("EA3", True), ("EA4", True)):
            sub = [s for s in sigs if s["ea"]==ea]
            trs = simulate(df, sym, sub, eod_flat=eod, max_hold=92 if eod else 96,
                           time_stop_bars=999 if ea=="EA4" else 8)
            for t in trs: all_rows.append(row_from_trade(t, df))
        for ea in ("EA1","EA2","EA5"):
            sub = [s for s in sigs if s["ea"]==ea]
            trs = simulate(df, sym, sub, max_hold=96)
            for t in trs: all_rows.append(row_from_trade(t, df))
        subA = [s for s in sigsA if s["ea"]=="EA1A"]
        trsA = simulate(df, sym, subA, max_hold=96)
        for t in trsA: all_rows.append(row_from_trade(t, df))
        df.to_pickle(f"{OUT}/{sym}.pkl")
    res = pd.DataFrame(all_rows)
    res.to_csv(f"{OUT}/trades.csv", index=False)
    out = {}
    for ea in ["EA1","EA1A","EA2","EA3","EA4","EA5"]:
        sub = res[res.ea==ea]
        rs = sub["r"].values
        if len(rs)==0:
            out[ea] = {"n":0}; continue
        wins = rs[rs>0]; losses = rs[rs<=0]
        eq = np.cumsum(rs); dd = (np.maximum.accumulate(eq)-eq).max() if len(eq) else 0
        out[ea] = {"n":int(len(rs)), "winrate":round(float((rs>0).mean()),3),
                   "avgR":round(float(rs.mean()),3), "sumR":round(float(rs.sum()),1),
                   "pf":round(float(wins.sum()/abs(losses.sum())),2) if losses.sum()!=0 else None,
                   "maxDD_R":round(float(dd),1)}
    out["by_symbol"] = {s: {ea: out[ea].get("n",0) for ea in out if ea!="by_symbol"} for s in SYMS}
    # per-symbol per-EA sumR
    bss = {}
    for s in SYMS:
        bss[s] = {}
        for ea in ["EA1","EA1A","EA2","EA3","EA4","EA5"]:
            sub = res[(res.ea==ea)&(res.sym==s)]
            bss[s][ea] = {"n":int(len(sub)), "sumR":round(float(sub["r"].sum()),1) if len(sub) else 0,
                          "wr":round(float((sub["r"]>0).mean()),2) if len(sub) else None}
    out["by_symbol_detail"] = bss
    with open(f"{OUT}/results.json","w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k:v for k,v in out.items() if not k.startswith("by_")}, indent=1))
    print(json.dumps(bss, indent=1))

def row_from_trade(t, df):
    return {"ea":t.ea,"sym":t.sym,"side":t.side,"entry_dt":df.dt.iloc[t.entry_i],
            "exit_dt":df.dt.iloc[t.close_i] if t.close_i is not None else None,
            "entry":t.entry_px,"stop0":None,"exit":t.close_px,"r":t.r - t.fees_r,
            "reason":t.exit_reason,"bars":t.bars_held}

if __name__ == "__main__":
    main()
