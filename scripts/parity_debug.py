#!/usr/bin/env python3
"""Debug specific parity misses: dump engine cards near the missed signal + backtest internals."""
import json, subprocess, sys
import numpy as np

sys.path.insert(0, "/home/z/my-project/scripts")
from parity_replay import build_signals, WINDOW

def run_engine(bars, sym, lo, hi):
    window = bars[lo:hi+1]
    payload = json.dumps({"sym": sym, "candles": [
        {"t": int(r[0]), "o": float(r[1]), "h": float(r[2]), "l": float(r[3]),
         "c": float(r[4]), "v": float(r[5]), "tbb": float(r[6])} for r in window]})
    proc = subprocess.run(["node", "--no-warnings", "/home/z/my-project/scripts/parity_engine.mjs"],
                          input=payload, capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        print("ENGINE ERR:", proc.stderr[:300]); return []
    return json.loads(proc.stdout)["cards"]

def main():
    sym = sys.argv[1] if len(sys.argv) > 1 else "ETHUSDT"
    df, sigs = build_signals(sym)
    seen = set(); uniq = []
    for s in sigs:
        k = (s["ea"], s["i"], s["side"])
        if k in seen: continue
        seen.add(k); uniq.append(s)
    bars = df[["open_time","open","high","low","close","volume","taker_buy_base"]].values
    misses = [(5416,"EA6"), (6177,"EA2"), (6724,"EA6")] if sym == "BTCUSDT" else [(2444,"EA5"), (4632,"EA2"), (4741,"EA6")]
    for i_want, ea in misses:
        s = next((x for x in uniq if x["i"] == i_want and x["ea"] == ea), None)
        if s is None:
            print(f"{sym} {ea}@{i_want}: not a unique backtest signal, skip"); continue
        cards = run_engine(bars, sym, i_want - WINDOW + 1, i_want)
        near = [c for c in cards if abs(c["signalTs"] - int(bars[i_want][0])) <= 8 * 900_000]
        print(f"\n=== {sym} {ea} @bar {i_want} ts={bars[i_want][0]} side={s['side']} px={s['px']:.2f} stop={s['stop']:.2f}")
        print(f"    engine cards in window: {len(cards)}; near ts: {len(near)}")
        for c in near:
            print(f"    -> {c['id']} {c['side']} entry={c['entry']:.2f} status={c['status']}")
        if not near:
            # how far is the nearest card of that engine?
            same_ea = [c for c in cards if c["engine"] == ea]
            if same_ea:
                nearest = min(same_ea, key=lambda c: abs(c["signalTs"] - int(bars[i_want][0])))
                dt_bars = (int(bars[i_want][0]) - nearest["signalTs"]) / 900_000
                print(f"    nearest {ea} card: {dt_bars:.0f} bars earlier, entry={nearest['entry']:.2f} side={nearest['side']}")
            else:
                print(f"    no {ea} card at all in the last 8 bars")

if __name__ == "__main__":
    main()
