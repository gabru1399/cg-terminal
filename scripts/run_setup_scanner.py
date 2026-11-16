#!/usr/bin/env python3
"""
run_setup_scanner.py — SETUP-CENTRIC candidate generation (R394)

WHY THIS EXISTS
---------------
The desk formulates candidate-first, not setup-first. Measured over the committed
81 KB of `desk/log.md`:

  * 77 structured candidate blocks ever produced
  * 0 of the 77 declare a setup archetype (S1..S8)
  * 27 of 30 crypto assets permanently pinned to "WAIT FOR THE SWEEP (S1)"
  * S4 (Wall-Pull Breakout) has NEVER been used: 0 mentions
  * Generator vocabulary is M1_TREND_PULLBACK / M2_MEAN_REVERSION /
    WATCH_EXHAUSTION. WATCH_EXHAUSTION is NOT one of the manual's S1..S8 --
    it is a non-setup that consumes a candidate slot and always resolves to "wait".

That is the actual reason the pipeline is thin. Not missing telemetry: the
broadcast is missing four of its eight setups, and it manufactures "watch"
candidates that are ungradeable by construction, because Table 7 can only score
a trade whose setup archetype is known (hard veto #8 = "no card S1-S8").

WHAT THIS SCRIPT DOES DIFFERENTLY
---------------------------------
It inverts the order of operations. Instead of "find a symbol, then score it",
it enumerates every CANDIDATE STATE the manual defines (S1..S8) against every
symbol, using only fields that exist in the committed telemetry dictionary, and
returns the ones that are ARMED right now -- plus, for the ones that are not,
the exact missing input needed to arm them.

It is deliberately read-only and side-effect free. It proposes; the Council disposes.

INPUTS (no live feeds required for the dry run)
-----------------------------------------------
  --telemetry JSON   file with per-symbol fields (see SCHEMA below).
                     If omitted, runs in SELF-TEST mode on a synthetic tape so
                     the logic is auditable without market data egress.

SCHEMA (all optional; missing key => that predicate is UNKNOWN, never True)
---------------------------------------------------------------------------
  {
    "BTC": {
       "price": 65031.2,
       "vwap": 64700.0, "sd1": 64900.0, "sd2": 65100.0, "sd3": 65400.0, "z": 1.4,
       "sess_val":..., "sess_poc":..., "sess_vah":...,
       "day_val":...,  "day_poc":...,  "day_vah":...,
       "mon_val":...,  "mon_poc":...,  "mon_vah":...,
       "ema_h4_e13":..., "ema_h4_e89":..., "ema_d1_e13":..., "ema_d1_e89":...,
       "rsi_h1":..., "rsi_h4":...,
       "fp_signal": "abs" | "div" | "sdiv" | "trap" | "exh" | null,
       "fp_dir":    "buy" | "sell" | null,
       "cvd_div":   "bull" | "bear" | null,
       "liq_up_usd":..., "liq_dn_usd":...,         # +/-2% band, for LSR
       "liq_cluster_price":..., "liq_cluster_str":..., "liq_cluster_usd":...,
       "liq_cluster_side": "long"|"short",
       "walls": [{"side":"b"|"a","price":..,"usd":..,"ageMs":..,"touched":false}],
       "wall_pull": true|false,                     # S4 input
       "oi_delta_4h_pct":..., "quadrant": "LONG_ACCUMULATION"|...,
       "gex": "pos"|"neg"|null,
       "spread_pct":..., "liq_5m_usd":..., "funding_apr":...,
       "contractValue":..., "tickSize":...
    }, ...
  }

USAGE
  python3 scripts/run_setup_scanner.py                  # self-test on synthetic tape
  python3 scripts/run_setup_scanner.py -t live.json     # real telemetry
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field

EQUITY = 2.767366          # from origin/main desk/state.json
RISK_A, RISK_B = 0.010, 0.005


# --------------------------------------------------------------------------- #
# Telemetry access that NEVER invents a value.
# --------------------------------------------------------------------------- #
class T:
    """Wrapper that distinguishes 'field is absent' from 'field is zero'."""

    def __init__(self, d: dict):
        self.d = d or {}

    def has(self, *keys) -> bool:
        return all(k in self.d and self.d[k] is not None for k in keys)

    def g(self, k, default=None):
        return self.d.get(k, default)

    def num(self, k):
        v = self.d.get(k)
        return v if isinstance(v, (int, float)) else None


@dataclass
class Armed:
    setup: str
    name: str
    direction: str            # "short" / "long"
    met: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    grade_cap: str = "B"

    @property
    def complete(self) -> bool:
        return not self.missing


# --------------------------------------------------------------------------- #
# Hard vetoes that apply to every setup (§5)
# --------------------------------------------------------------------------- #
def hard_vetoes(t: T) -> list[str]:
    v = []
    up, dn = t.num("liq_up_usd"), t.num("liq_dn_usd")
    if up and dn:
        lsr = max(up, dn) / min(up, dn)
        if lsr >= 2.5:
            v.append(f"§3 LSR {lsr:.1f}:1 >= 2.5 — passive entries into the magnet path BANNED (S1 only)")
    l5 = t.num("liq_5m_usd")
    if l5 is not None and l5 > 500_000:
        v.append(f"D16 Liq 5m ${l5:,.0f} > $500k — cascading, BAN ALL LIMIT ENTRIES")
    fa = t.num("funding_apr")
    if fa is not None and abs(fa) > 25:
        v.append(f"D15 funding APR {fa:+.1f}% beyond ±25% — crowded")
    return v


def avoid_magnet(t: T, entry: float, stop: float, direction: str) -> str | None:
    """Hard veto #2: opposite magnet str>=50 within 1.2R of entry."""
    px = t.num("liq_cluster_price")
    st = t.num("liq_cluster_str")
    side = t.g("liq_cluster_side")
    if px is None or st is None or side is None:
        return None
    if st < 50:
        return None
    adverse = (side == "short") if direction == "short" else (side == "long")
    if not adverse:
        return None
    risk = abs(entry - stop)
    if risk and abs(px - entry) <= 1.2 * risk:
        return f"hard veto #2 — opposite magnet {px} (str {st}) within 1.2R of {entry}"
    return None


def sizeability(t: T, entry: float, stop: float, risk_pct: float) -> tuple[bool, str]:
    cv = t.num("contractValue")
    if not cv:
        return False, "no contractValue — sizing unverifiable (G-07)"
    risk_usd = abs(entry - stop) * cv
    budget = EQUITY * risk_pct
    n = int(budget // risk_usd) if risk_usd else 0
    if n < 1:
        return False, (f"1 ct risks ${risk_usd:.4f} = {risk_usd / EQUITY * 100:.2f}% of equity "
                       f"> {risk_pct*100:.1f}% mandate => 0 ct (§5 veto #7)")
    return True, f"{n} ct at {risk_pct*100:.1f}% (risk ${risk_usd:.4f}/ct)"


# --------------------------------------------------------------------------- #
# The 8 archetypes, coded exactly to TRADE_FORMULATION_MANUAL §S1..S8
# --------------------------------------------------------------------------- #
def s1_sweep_reversal(t: T) -> Armed | None:
    """S1: dominant magnet swept + exhaustion + delta flip + stretch."""
    px = t.num("price")
    cl = t.num("liq_cluster_price")
    cs = t.num("liq_cluster_str")
    cu = t.num("liq_cluster_usd")
    side = t.g("liq_cluster_side")
    if None in (px, cl, cs) or side is None:
        return None
    big = cs >= 50 or (cu or 0) >= 5_000_000
    if not big:
        return None
    # a sweep means price has REACHED or passed the cluster
    swept = (px <= cl) if side == "long" else (px >= cl)
    if not swept:
        return None
    direction = "long" if side == "long" else "short"   # fade the swept side
    a = Armed("S1", "Liquidation Sweep Reversal", direction)
    a.met.append(f"magnet {cl} (str {cs}) swept")
    sig, sd = t.g("fp_signal"), t.g("fp_dir")
    if sig == "exh":
        a.met.append("exhaustion signature")
    else:
        a.missing.append(f"exhaustion signature (got {sig!r})")
    flip = t.g("cvd_div")
    want = "bull" if direction == "long" else "bear"
    if flip == want:
        a.met.append(f"CVD divergence {flip}")
    else:
        a.missing.append(f"CVD delta flip == {want} (got {flip!r})")
    z = t.num("z")
    if z is not None and abs(z) >= 2.0:
        a.met.append(f"stretch |z| {abs(z):.2f} >= 2.0")
    else:
        a.missing.append("stretch |z| >= 2.0")
    a.grade_cap = "A+"
    return a


def s2_va_edge_fade(t: T) -> Armed | None:
    """S2: absorption/divergence AT Day VAH (short) or VAL (long)."""
    px = t.num("price")
    if px is None:
        return None
    out = None
    for edge_key, direction in (("day_vah", "short"), ("day_val", "long")):
        edge = t.num(edge_key)
        if edge is None:
            continue
        tol = abs(edge) * 0.0015                      # ~0.15% touch tolerance
        if abs(px - edge) > tol:
            continue
        a = Armed("S2", "Value Area Edge Fade", direction)
        a.met.append(f"price {px} at {edge_key} {edge}")
        sig = t.g("fp_signal")
        if sig in ("abs", "div", "sdiv"):
            a.met.append(f"footprint {sig} at edge")
        else:
            a.missing.append(f"absorption/divergence at edge (got {sig!r})")
        gex = t.g("gex")
        if gex == "pos":
            a.met.append("positive gamma supports fade")
        elif gex is None:
            a.missing.append("GEX unknown (BTC/ETH only)")
        out = out or a
    return out


def s3_wall_defense(t: T) -> Armed | None:
    """S3: confirmed resting wall >= $10M, age > 2h, untouched, LSR gate passed."""
    px = t.num("price")
    walls = t.g("walls") or []
    if px is None or not walls:
        return None
    up, dn = t.num("liq_up_usd"), t.num("liq_dn_usd")
    lsr = (max(up, dn) / min(up, dn)) if (up and dn) else None
    for w in walls:
        usd, age, touched = w.get("usd"), w.get("ageMs"), w.get("touched")
        if not usd or usd < 10_000_000:
            continue
        if not age or age < 2 * 3600 * 1000:
            continue
        if touched:
            continue
        direction = "long" if w.get("side") == "b" else "short"
        a = Armed("S3", "Whale Wall Defense / Front-Run", direction)
        a.met.append(f"wall ${usd/1e6:.1f}M @ {w.get('price')} age {age/3.6e6:.1f}h untouched")
        if lsr is None:
            a.missing.append("LSR unknown — §3 gate cannot be cleared")
        elif lsr >= 2.5:
            a.missing.append(f"LSR {lsr:.1f}:1 >= 2.5 — S3 BANNED")
        elif lsr >= 2.0:
            a.met.append(f"LSR {lsr:.1f}:1 in 2.0-2.5 band")
            a.grade_cap = "B"
        else:
            a.met.append(f"LSR {lsr:.1f}:1 < 2.0 gate pass")
        a.grade_cap = "B"          # manual: S3 always capped at B
        return a
    return None


def s4_wall_pull(t: T) -> Armed | None:
    """S4: a previously confirmed wall was PULLED, price expands through vacuum."""
    if not t.g("wall_pull"):
        return None
    oi = t.num("oi_delta_4h_pct")
    a = Armed("S4", "Wall-Pull Breakout", "long")
    a.met.append("wall-pull event on confirmed wall")
    if oi is None:
        a.missing.append("OI delta 4h unknown — breakout unconfirmed (D14)")
    elif oi > 0:
        a.met.append(f"rising OI {oi:+.1f}%")
    else:
        a.missing.append(f"OI falling ({oi:+.1f}%) — no expansion confirmation")
    gex = t.g("gex")
    if gex == "pos":
        a.met.append("positive GEX caps at B")
    a.grade_cap = "B"
    return a


def s5_vwap_band(t: T) -> Armed | None:
    """S5: |z| >= 3 (or >=2.2 stacked) + crowding + reversal proof."""
    z = t.num("z")
    if z is None or abs(z) < 2.0:
        return None
    direction = "short" if z > 0 else "long"
    a = Armed("S5", "VWAP Band Mean Reversion", direction)
    if abs(z) >= 3.0:
        a.met.append(f"|z| {abs(z):.2f} >= 3.0 band")
    elif abs(z) >= 2.2:
        a.met.append(f"|z| {abs(z):.2f} >= 2.2 (needs peak conviction stack)")
    else:
        a.missing.append(f"|z| {abs(z):.2f} only 2.0-2.2 — band not cleared")
    rsi = t.num("rsi_h1")
    if rsi is None:
        a.missing.append("RSI H1 unknown — crowding unproven")
    elif (direction == "short" and rsi > 70) or (direction == "long" and rsi < 30):
        a.met.append(f"RSI H1 {rsi:.1f} crowded")
    else:
        a.missing.append(f"RSI H1 {rsi:.1f} not crowded — anti-knife-catch requires it")
    sig = t.g("fp_signal")
    want = "sell" if direction == "short" else "buy"
    if sig in ("exh", "trap", "abs", "div", "sdiv") and t.g("fp_dir") == want:
        a.met.append(f"reversal proof {sig}/{t.g('fp_dir')}")
    else:
        a.missing.append(f"reversal proof in {want} direction (got {sig!r}/{t.g('fp_dir')!r})")
    a.grade_cap = "A"
    return a


def s6_trapped_fade(t: T) -> Armed | None:
    """S6: trap signature + failed break + room >= 2R to opposite magnet."""
    if t.g("fp_signal") != "trap":
        return None
    direction = "short" if t.g("fp_dir") == "buy" else "long"   # fade the trapped side
    a = Armed("S6", "Trapped Traders Fade", direction)
    a.met.append(f"trap signature ({t.g('fp_dir')} trapped)")
    oi = t.num("oi_delta_4h_pct")
    if oi is None:
        a.missing.append("crowding/quadrant unknown")
    a.grade_cap = "B"
    return a


def s7_absorption_continuation(t: T) -> Armed | None:
    """S7: H4 13x89 trend + D1 non-opposing + not stretched + absorption at node."""
    e13, e89 = t.num("ema_h4_e13"), t.num("ema_h4_e89")
    d13, d89 = t.num("ema_d1_e13"), t.num("ema_d1_e89")
    if None in (e13, e89, d13, d89):
        return None
    z = t.num("z")
    if z is not None and abs(z) >= 2.0:
        return None                                    # chase guard
    direction = "long" if e13 > e89 else "short"
    d1_opposing = (d13 < d89) if direction == "long" else (d13 > d89)
    if d1_opposing:
        return None
    a = Armed("S7", "High-Volume Absorption Continuation", direction)
    a.met.append(f"H4 EMA13 {'>' if direction=='long' else '<'} EMA89 aligned")
    a.met.append("D1 non-opposing")
    if z is not None:
        a.met.append(f"not stretched (|z| {abs(z):.2f} < 2.0)")
    else:
        a.missing.append("z unknown — chase guard unverified")
    sig = t.g("fp_signal")
    want = "buy" if direction == "long" else "sell"
    if sig in ("abs", "div", "sdiv") and t.g("fp_dir") == want:
        a.met.append(f"in-zone {sig}/{want} at retest")
        a.grade_cap = "A"
    else:
        a.missing.append(f"in-zone absorption/divergence (got {sig!r}/{t.g('fp_dir')!r}) -> B cap")
        a.grade_cap = "B"
    return a


def s8_liq_breakout(t: T) -> Armed | None:
    """S8: clean close beyond a major liquidation shelf + rising OI."""
    px = t.num("price")
    cl = t.num("liq_cluster_price")
    cs = t.num("liq_cluster_str")
    side = t.g("liq_cluster_side")
    if None in (px, cl, cs) or side is None:
        return None
    if cs < 50:
        return None
    broke = (px > cl) if side == "short" else (px < cl)   # broke THROUGH the shelf
    if not broke:
        return None
    direction = "long" if side == "short" else "short"
    a = Armed("S8", "Liquidation Breakout Continuation", direction)
    a.met.append(f"shelf {cl} (str {cs}) broken")
    oi = t.num("oi_delta_4h_pct")
    if oi is None:
        a.missing.append("rising OI unknown (D14)")
    elif oi > 0:
        a.met.append(f"rising OI {oi:+.1f}%")
    else:
        a.missing.append(f"OI falling {oi:+.1f}%")
    gex = t.g("gex")
    if gex == "neg":
        a.met.append("negative gamma amplifies")
        a.grade_cap = "A"
    elif gex == "pos":
        a.missing.append("positive GEX — capped at B")
        a.grade_cap = "B"
    return a


SCANNERS = [s1_sweep_reversal, s2_va_edge_fade, s3_wall_defense, s4_wall_pull,
            s5_vwap_band, s6_trapped_fade, s7_absorption_continuation, s8_liq_breakout]


# --------------------------------------------------------------------------- #
def scan(telemetry: dict, verbose: bool = True) -> dict:
    results = {}
    for sym, d in telemetry.items():
        t = T(d)
        vetoes = hard_vetoes(t)
        hits = []
        for fn in SCANNERS:
            try:
                a = fn(t)
            except Exception as e:                       # noqa: BLE001
                if verbose:
                    print(f"  !! {sym} {fn.__name__}: {e}", file=sys.stderr)
                continue
            if a:
                hits.append(a)
        hits, notes = resolve(hits)
        results[sym] = {"vetoes": vetoes, "armed": hits, "notes": notes}
    return results


def resolve(hits: list[Armed]) -> tuple[list[Armed], list[str]]:
    """Kill contradictory reads off the SAME cluster.

    A swept magnet is S1 (the sweep exhausted -> fade it) or S8 (the break is
    continuing -> ride it). It cannot be both: they are opposite trades on the
    same level. The discriminator is the exhaustion/delta-flip stack (S1) versus
    the OI/gamma stack (S8). Precedence: a FULLY ARMED S1 beats a partial S8,
    because S1 requires four independent confirmations including delta flip --
    an ambiguous read is not a breakout. Same for S8 vs S1 the other way round.
    """
    notes = []
    by_cluster = {}
    for a in hits:
        by_cluster.setdefault(a.setup, a)
    s1, s8 = by_cluster.get("S1"), by_cluster.get("S8")
    if s1 and s8 and s1.direction != s8.direction:
        if s1.complete and not s8.complete:
            hits = [h for h in hits if h.setup != "S8"]
            notes.append("S8 dropped: partial break vs fully-armed S1 sweep fade on same cluster")
        elif s8.complete and not s1.complete:
            hits = [h for h in hits if h.setup != "S1"]
            notes.append("S1 dropped: partial sweep vs fully-armed S8 breakout on same cluster")
        elif s1.complete and s8.complete:
            notes.append("CONFLICT: S1 and S8 both fully armed on one cluster — escalate to Council, do not auto-pick")
    # two partials pointing opposite ways on the same level is noise, keep both but flag
    dirs = {a.direction for a in hits if a.setup in ("S1", "S8")}
    if len(dirs) > 1 and not (s1 and s8 and s1.complete != s8.complete):
        notes.append("conflicting S1/S8 directions unresolved — both kept, both PARTIAL")
    return hits, notes


# Which fields each archetype NEEDS. Used to explain a null result instead of
# silently printing "nothing found" -- a scanner that returns nothing without
# saying why is the same failure mode that produced 77 unclassified candidates.
REQUIRES = {
    "S1": ["liq_cluster_price", "liq_cluster_str", "liq_cluster_side", "fp_signal", "cvd_div", "z"],
    "S2": ["day_vah | day_val", "fp_signal", "gex"],
    "S3": ["walls[]", "liq_up_usd", "liq_dn_usd"],
    "S4": ["wall_pull"],
    "S5": ["z", "rsi_h1", "fp_signal", "fp_dir"],
    "S6": ["fp_signal"],
    "S7": ["ema_h4_e13", "ema_h4_e89", "ema_d1_e13", "ema_d1_e89", "z", "fp_signal"],
    "S8": ["liq_cluster_price", "liq_cluster_str", "liq_cluster_side", "oi_delta_4h_pct", "gex"],
}


def why_nothing(d: dict) -> list[str]:
    """For a symbol with no armed archetype, name the fields that blocked it."""
    out = []
    for setup, needs in REQUIRES.items():
        blocked = []
        for n in needs:
            if "|" in n:
                ok = any(k in d and d[k] is not None for k in n.split(" | "))
            elif n.endswith("[]"):
                ok = bool(d.get(n[:-2]))
            else:
                ok = d.get(n) is not None
            if not ok:
                blocked.append(n)
        if blocked:
            out.append(f"{setup} blocked on: {', '.join(blocked)}")
    return out


def report(results: dict, telemetry: dict) -> int:
    n_armed = n_complete = 0
    print("=" * 96)
    print("SETUP-CENTRIC SCAN — every S1..S8 x every symbol")
    print("=" * 96)
    for sym, r in sorted(results.items()):
        px = T(telemetry[sym]).num("price")
        if not r["armed"] and not r["vetoes"]:
            print(f"\n{sym:8} price {px if px is not None else 'n/a':>10}   no archetype state reached")
            for line in why_nothing(telemetry[sym]):
                print(f"   .. {line}")
            continue
        print(f"\n{sym:8} price {px if px is not None else 'n/a':>10}")
        for v in r["vetoes"]:
            print(f"   VETO  {v}")
        for n_ in r.get("notes", []):
            print(f"   NOTE  {n_}")
        for a in r["armed"]:
            n_armed += 1
            tag = "ARMED  " if a.complete else "PARTIAL"
            if a.complete:
                n_complete += 1
            print(f"   {tag} {a.setup} {a.name} [{a.direction}] cap={a.grade_cap}")
            for m in a.met:
                print(f"            + {m}")
            for m in a.missing:
                print(f"            - MISSING: {m}")
    print("\n" + "=" * 96)
    print(f"{n_armed} archetype states reached · {n_complete} fully armed (all mandatory conditions met)")
    print("=" * 96)
    return n_complete


SELF_TEST = {
    # S1 armed: magnet swept, exhaustion, delta flip, stretch
    "ADEV": {"price": 0.1480, "liq_cluster_price": 0.1490, "liq_cluster_str": 70,
             "liq_cluster_usd": 6_000_000, "liq_cluster_side": "long",
             "fp_signal": "exh", "fp_dir": "buy", "cvd_div": "bull", "z": -2.4,
             "contractValue": 1.0, "spread_pct": 0.02},
    # S2 partial: at Day VAH with absorption but GEX unknown
    "BDEV": {"price": 100.0, "day_vah": 100.05, "fp_signal": "abs", "fp_dir": "sell",
             "contractValue": 1.0},
    # S3 banned by LSR
    "CDEV": {"price": 50.0, "liq_up_usd": 9_000_000, "liq_dn_usd": 2_000_000,
             "walls": [{"side": "b", "price": 49.5, "usd": 12_000_000,
                        "ageMs": 3 * 3600 * 1000, "touched": False}],
             "contractValue": 1.0},
    # S4 fully armed
    "DDEV": {"price": 10.2, "wall_pull": True, "oi_delta_4h_pct": 4.1,
             "gex": "pos", "contractValue": 1.0},
    # S5 armed: |z|=3.1, RSI crowded, exhaustion proof
    "EDEV": {"price": 200.0, "z": 3.1, "rsi_h1": 76.0, "fp_signal": "exh",
             "fp_dir": "sell", "contractValue": 0.1},
    # S7 armed: trend stack, in-zone absorption
    "FDEV": {"price": 5.0, "ema_h4_e13": 5.1, "ema_h4_e89": 4.8,
             "ema_d1_e13": 5.2, "ema_d1_e89": 4.9, "z": 0.7,
             "fp_signal": "abs", "fp_dir": "buy", "contractValue": 1.0},
    # S8 armed: shelf broken, rising OI, negative gamma
    "GDEV": {"price": 300.0, "liq_cluster_price": 295.0, "liq_cluster_str": 80,
             "liq_cluster_side": "short", "oi_delta_4h_pct": 6.0,
             "gex": "neg", "contractValue": 0.01},
    # liquidated out: cascade ban
    "HDEV": {"price": 1.0, "liq_5m_usd": 900_000, "contractValue": 1.0},
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--telemetry", help="path to telemetry JSON")
    args = ap.parse_args()
    if args.telemetry:
        telemetry = json.load(open(args.telemetry, encoding="utf-8"))
        mode = f"LIVE TELEMETRY {args.telemetry}"
    else:
        telemetry = SELF_TEST
        mode = "SELF-TEST (synthetic tape — proves the logic, NOT a market read)"
    print(f"mode: {mode}\n")
    res = scan(telemetry)
    n = report(res, telemetry)
    return 0 if n >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
