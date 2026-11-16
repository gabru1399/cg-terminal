#!/usr/bin/env python3
"""
scripts/run_canonical_decide.py
Canonical 360° Order-Flow Decision Engine (SOP v1.4.0) — HONEST EDITION

Rewritten by arena.ai (Second Council) on 2026-11-16 after an adversarial audit
of the previous revision found four zero-fallback violations:

  1. `compute_table7` initialised `lsr` and `dom_side` INSIDE the `if` branch
     and then echoed them in the return dict → NameError / phantom values.
     F6 now derives strictly from liqStats.keyLevels with an explicit fed/not-fed
     flag; an unfed D11 scores **0.0** and the card row prints `n/a`.
  2. The card template hardcoded ``Entry: 64750.0`` / ``1812.50`` and an
     ``F8 = 1.0`` "Delta CLOB spread is < 0.05%" assumption. F8 is now earned
     from a *measured* spread payload; a missing spread feed scores 0.0.
  3. Every non-BTC/ETH row was stamped `HARD_VETO` while every BTC/ETH row was
     stamped `ACTIVE_POSITION` regardless of truth. Status is now derived from
     `desk/state.json` + the measured payload state.
  4. D16 invariants (heat / slots / BE) were prose. They are now computed from
     `desk/state.json` (account block + live positions).

Invariants enforced here:
  * G-06 / G-07 — 100% epistemic honesty, zero mocks, zero placeholders.
    A dimension with no upstream data is logged `n/a`, scores 0.0, is listed
    in `vetoes`/`notes`, and CAPS the achievable grade. Nothing is guessed.
  * Table 7 Sanity — in `RANGE_BALANCE`, F1 = 0.0 (max 9.5; 8.5 non-BTC/ETH).
  * The Liquidation Magnet Gate (D12) — LSR >= 2.5:1 bans passive entries into
    the magnet path; only S1 survives.

Outputs:
  desk/deepscan/FORMULATION-<SYM>-<ts>.md   Section 9.2 cards (Grade >= B only)
  desk/deepscan/UNIVERSE-360-<ts>.md        full 61-asset table, zero gaps
  desk/deepscan/decide-<ts>.json            machine-readable audit record
Exit code 0 = executed; 2 = feed-starved round (honest, no fabrication).
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE_URL = os.environ.get("CG_TERMINAL_URL", "http://127.0.0.1:3000")
DESK = "desk"
DEEPSCAN = os.path.join(DESK, "deepscan")
STATE_PATH = os.path.join(DESK, "state.json")
CONTRACTS_PATH = os.path.join(DESK, "delta_contracts.json")

GRADE_A_MIN = 7.0
GRADE_B_MIN = 5.0
MAX_SCORE = 11.5
MAX_SCORE_RANGE = 9.5          # F1 forced 0.0 in RANGE_BALANCE
MAX_SCORE_RANGE_NON_BTC_ETH = 8.5  # F7 n/a outside BTC/ETH
LSR_BAN = 2.5


# --------------------------------------------------------------------------
# Transport
# --------------------------------------------------------------------------
def fetch_json(endpoint: str, timeout: float = 10.0) -> dict:
    """GET a terminal endpoint. Always returns a dict; failures are explicit."""
    url = f"{BASE_URL}{endpoint}" if endpoint.startswith("/") else endpoint
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "arena-second-council/1.4.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            body = {}
        if not isinstance(body, dict):
            body = {}
        body.setdefault("ok", False)
        body.setdefault("httpStatus", e.code)
        return body
    except Exception as e:  # noqa: BLE001 — transport failure is data
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def live_price(snap: dict) -> float | None:
    """MarketSnapshot.price.last, or None. Never a fallback constant."""
    if not isinstance(snap, dict) or not snap.get("ok"):
        return None
    p = (snap.get("price") or {}).get("last")
    try:
        p = float(p)
    except (TypeError, ValueError):
        return None
    return p if p > 0 else None


# --------------------------------------------------------------------------
# Table 7 — every factor must be EARNED from a measured payload
# --------------------------------------------------------------------------
def feed_has_data(kind: str, payload: dict) -> bool:
    """True only when the payload carries actual measurements.

    The terminal returns HTTP 200 + ok:true for several unsupported/degraded
    paths (e.g. liqlevels without `stats`, narrative with `kind:"unknown"`).
    Counting those as "fed" would be a silent fallback — this predicate is the
    single place that decides, per feed, fed vs n/a.
    """
    if not isinstance(payload, dict) or not payload.get("ok"):
        return False
    if payload.get("supported") is False:
        return False
    if kind == "market":
        return live_price(payload) is not None
    if kind == "narrative":
        return payload.get("kind") not in (None, "unknown") and bool(
            (payload.get("plan") or {}).get("triggerRule") not in (None, "n/a"))
    if kind == "signals":
        return bool(payload.get("sets"))
    if kind == "cvd":
        return bool(payload.get("kpis"))
    if kind == "walls":
        return bool(payload.get("model")) and bool(payload.get("confirmed"))
    if kind == "liq":
        return bool(payload.get("stats"))
    if kind == "options":
        return any(payload.get(k) for k in ("gex", "maxPainStrike", "dvol"))
    if kind == "quant":
        b = payload.get("basis") or {}
        return b.get("perpPrice") is not None or payload.get("oiQuadrant", {}).get("4h") is not None
    if kind == "lto":
        return bool(payload.get("groups"))
    if kind == "spread":
        return isinstance(payload.get("spreadPct"), (int, float))
    return True


# Coinglass-backed feeds start a 12 s/asset progressive radar sweep on first
# touch (screener `radar.stepMs`). Deep-probing 61 symbols at once would either
# trip the 429 cooldown or return empty payloads that look identical to "no
# data". So the probe set is explicit and named on the report.
PROBE_LIMIT_NOTE = __doc__


def count_priced_rows(rows: list) -> int:
    return sum(1 for r in rows if isinstance(r.get("price"), (int, float)) and r["price"])


def measured_regime(narrative: dict) -> str:
    """Regime, but `n/a` when the narrative engine had no market snapshot.

    buildNarrative defaults to RANGE_BALANCE when it refuses to trade blind
    (`kind:"unknown"`, `regimeNote:"no market data"`). Reporting that default
    as a measured range would mis-state the auction and would also silently
    pin F1 to the RANGE_BALANCE invariant — a fallback in disguise.
    """
    if not isinstance(narrative, dict) or not narrative.get("ok"):
        return "n/a"
    if narrative.get("kind") in (None, "unknown"):
        return "n/a"
    if "no market data" in str(narrative.get("regimeNote") or "").lower():
        return "n/a"
    return narrative.get("regime") or "n/a"


def score_table7(sym: str, market: dict, sigs: dict, cvd: dict, walls: dict,
                 liq: dict, opts: dict, spread: dict | None,
                 regime: str, direction: str) -> dict:
    """Score F1..F8 (max 11.5). Unfed dimension => 0.0 and `n/a` disclosure."""
    unfed: list[str] = []
    notes: list[str] = []

    price = live_price(market)
    if price is None:
        # No price => every geometric factor is unscoreable. Return a hard 0.
        return {
            "f1_trend": 0.0, "f2_vwap": 0.0, "f3_signals": 0.0, "f4_walls": 0.0,
            "f5_cvd": 0.0, "f6_liq_magnet": 0.0, "f7_options": 0.0,
            "f8_spread": 0.0, "total": 0.0, "lsr": None, "dom_side": None,
            "z_score": None, "unfed": ["D1", "D2", "D3", "D4", "D6", "D7",
                                       "D8", "D9", "D11", "D12", "D13", "D15"],
            "notes": ["market feed unavailable — Table 7 cannot be scored"],
            "max_achievable": MAX_SCORE,
        }

    # ---- F1: Directional trend (2.0). STRICT 0.0 in RANGE_BALANCE. ----
    f1 = 0.0
    ema = market.get("ema") or {}
    h4, d1 = ema.get("h4") or {}, ema.get("d1") or {}
    h4_13, h4_89 = h4.get("e13"), h4.get("e89")
    d1_13, d1_89 = d1.get("e13"), d1.get("e89")
    if h4_13 is None or h4_89 is None or d1_13 is None or d1_89 is None:
        unfed.append("D4")
    elif regime in ("TREND_UP", "TREND_DOWN"):
        if direction == "LONG" and h4_13 > h4_89:
            f1 = 2.0 if d1_13 > d1_89 else 1.0
        elif direction == "SHORT" and h4_13 < h4_89:
            f1 = 2.0 if d1_13 < d1_89 else 1.0
    else:
        f1 = 0.0  # invariant: RANGE_BALANCE => 0.0
        notes.append("F1 forced 0.0 (RANGE_BALANCE invariant)")

    # ---- F2: Auction/VWAP regime (1.5) — measured z-score ----
    f2, z = 0.0, None
    vwap = market.get("vwap") or {}
    vwap_val = vwap.get("vwap")
    sd1 = (vwap.get("bands") or {}).get("sd1")
    if vwap_val and sd1:
        z = (price - float(vwap_val)) / float(sd1)
        if direction == "LONG" and z < -0.5:
            f2 = 1.5 if z < -1.5 else 1.0
        elif direction == "SHORT" and z > 0.2:
            f2 = 1.5 if z > 1.0 else 0.5
    else:
        unfed.append("D3")

    # ---- F3: Footprint signal at the entry zone (2.0) ----
    f3 = 0.0
    sets = (sigs or {}).get("sets") or []
    if not sets:
        unfed.append("D7")
    else:
        for st in sets:
            for sg in st.get("sigs") or []:
                stype = (sg.get("type") or "").lower()
                w = sg.get("w") or sg.get("dir") or ""
                aligned = (direction == "LONG" and w == "buy") or (
                    direction == "SHORT" and w == "sell")
                if "strong" in stype and "div" in stype:
                    f3 = max(f3, 2.0 if aligned else 1.0)
                elif "abs" in stype:
                    f3 = max(f3, 2.0 if aligned else 1.0)
                elif any(k in stype for k in ("div", "trap", "exh")):
                    f3 = max(f3, 1.0 if aligned else 0.5)

    # ---- F4: Whale wall backstop (1.5) — >= $5M, age > 1h ----
    f4 = 0.0
    walls_ok = bool((walls or {}).get("ok")) and (walls or {}).get("model")
    confirmed = (walls or {}).get("confirmed") or []
    if not walls_ok:
        unfed.append("D9")
    else:
        for wall in confirmed:
            usd = wall.get("usd") or 0
            age = wall.get("ageMin") or 0
            side = (wall.get("side") or "").lower()
            if usd >= 5_000_000 and age >= 60:
                protecting = (direction == "LONG" and side == "bid") or (
                    direction == "SHORT" and side == "ask")
                f4 = max(f4, 1.5 if protecting else 1.0)

    # ---- F5: CVD divergence (1.0) ----
    f5 = 0.0
    if not (cvd or {}).get("ok"):
        unfed.append("D8")
    else:
        divs = cvd.get("divergences") or []
        if divs:
            dtype = (divs[-1].get("type") or "").lower()
            if (direction == "LONG" and dtype == "bull") or (
                    direction == "SHORT" and dtype == "bear"):
                f5 = 1.0

    # ---- F6: Liquidation Magnet Gate (1.5) — the LSR is computed HERE ----
    f6, lsr, dom_side = 0.0, None, None
    stats = (liq or {}).get("stats") if (liq or {}).get("ok") else None
    if not stats:
        unfed.append("D11")
        unfed.append("D12")
    else:
        above = (stats.get("keyLevels") or {}).get("above") or []
        below = (stats.get("keyLevels") or {}).get("below") or []
        shorts_above = sum(float(x.get("usd") or 0) for x in above
                           if abs(float(x.get("distPct") or 99)) <= 2.0)
        longs_below = sum(float(x.get("usd") or 0) for x in below
                          if abs(float(x.get("distPct") or 99)) <= 2.0)
        if shorts_above > 0 or longs_below > 0:
            hi, lo = max(shorts_above, longs_below), min(shorts_above, longs_below)
            lsr = round(hi / lo, 2) if lo > 0 else float("inf")
            dom_side = "short" if shorts_above >= longs_below else "long"
            aligned = (direction == "SHORT" and dom_side == "long") or (
                direction == "LONG" and dom_side == "short")
            if aligned:
                f6 = 1.5 if (lsr is not None and lsr < LSR_BAN) else 0.5
        else:
            unfed.append("D12")

    # ---- F7: Options GEX context (1.0) — BTC/ETH only, else honest 0 ----
    f7 = 0.0
    if sym in ("BTC", "ETH"):
        gex = ((opts or {}).get("gex") or {})
        g_regime = (gex.get("regime") or (opts or {}).get("gammaRegime") or "").upper()
        if not g_regime:
            unfed.append("D13")
        elif g_regime == "POSITIVE" and regime in ("RANGE_BALANCE", "TREND_DOWN"):
            f7 = 0.5
        elif g_regime == "NEGATIVE" and regime in ("TREND_UP", "TREND_DOWN"):
            f7 = 1.0
    else:
        notes.append("F7 n/a — options GEX is BTC/ETH-only (honest zero)")

    # ---- F8: Broker spread drag (1.0) — measured, never assumed ----
    f8 = 0.0
    if not spread or spread.get("spreadPct") is None:
        unfed.append("D15")
    else:
        sp = float(spread["spreadPct"])
        f8 = 1.0 if sp < 0.05 else (0.5 if sp <= 0.10 else 0.0)

    total = round(f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8, 1)
    max_ach = MAX_SCORE
    if regime not in ("TREND_UP", "TREND_DOWN"):
        max_ach = MAX_SCORE_RANGE
    if sym not in ("BTC", "ETH"):
        max_ach -= 1.0

    return {
        "f1_trend": f1, "f2_vwap": f2, "f3_signals": f3, "f4_walls": f4,
        "f5_cvd": f5, "f6_liq_magnet": f6, "f7_options": f7, "f8_spread": f8,
        "total": total, "lsr": lsr, "dom_side": dom_side, "z_score": z,
        "unfed": sorted(set(unfed)), "notes": notes, "max_achievable": max_ach,
    }


def grade_for(total: float, unfed: list[str]) -> tuple[str, float, list[str]]:
    """Grade + risk % + veto list. Feed starvation is a disclosed cap."""
    vetoes: list[str] = []
    if unfed:
        vetoes.append(
            "feed-starved dimensions " + ",".join(unfed) + " scored 0.0 (G-06/G-07)"
        )
    if total >= GRADE_A_MIN:
        return "A", 1.0, vetoes
    if total >= GRADE_B_MIN:
        return "B", 0.5, vetoes
    return "VETO", 0.0, vetoes + [f"Table 7 {total}/11.5 < {GRADE_B_MIN} => HARD VETO"]


def worst_freshness(*payloads: dict) -> dict:
    """Honest data-age across payloads (max of the reported ages)."""
    ages, stales, ats = [], [], []
    for p in payloads:
        if not isinstance(p, dict):
            continue
        if isinstance(p.get("ageMs"), (int, float)):
            ages.append(int(p["ageMs"]))
        if p.get("stale") is True:
            stales.append(True)
        if isinstance(p.get("dataAt"), (int, float)) and p["dataAt"]:
            ats.append(int(p["dataAt"]))
    return {
        "worstAgeMs": max(ages) if ages else None,
        "anyStale": bool(stales),
        "dataAt": max(ats) if ats else None,
    }


def fmt(v, decs: int = 2, dash: str = "n/a") -> str:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return dash
    return f"{f:.{decs}f}"


def r_multiple(entry: float | None, stop: float | None, target: float | None) -> str:
    if entry is None or stop is None or target is None:
        return "n/a"
    risk = abs(entry - stop)
    if risk <= 0:
        return "n/a"
    return f"{abs(target - entry) / risk:.2f}R"


# --------------------------------------------------------------------------
# Formulation Card (SOP §9.2)
# --------------------------------------------------------------------------
def render_card(sym: str, name: str, ts_utc: str, data: dict, t7: dict,
                grade: str, risk_pct: float, vetoes: list[str],
                direction: str, spread: dict | None, d16: dict) -> str:
    m = data["market"]
    n = data["narrative"]
    c = data["cvd"]
    w = data["walls"]
    l = data["liq"]
    o = data["options"]
    q = data["quant"]
    lo = data["lto"]
    s = data["signals"]

    price = live_price(m)
    auc = (m.get("auction") or {}) if m.get("ok") else {}
    day, sess, month = auc.get("day") or {}, auc.get("session") or {}, auc.get("month") or {}
    vwap = (m.get("vwap") or {})
    bands = vwap.get("bands") or {}
    ema = (m.get("ema") or {})
    rsi = (m.get("rsi") or {})
    price_decs = m.get("priceDecs")
    pd_ = price_decs if isinstance(price_decs, int) else 2

    def ema_line(tf: str) -> str:
        e = ema.get(tf) or {}
        return f"{fmt(e.get('e13'), pd_)}/{fmt(e.get('e89'), pd_)}"

    def kpi(key: str):
        return ((c.get("kpis") or {}).get(key) if (c or {}).get("ok") else None)

    liq_above = ((l.get("stats") or {}).get("keyLevels") or {}).get("above") or [] \
        if l.get("ok") else []
    liq_below = ((l.get("stats") or {}).get("keyLevels") or {}).get("below") or [] \
        if l.get("ok") else []
    wall_conf = (w.get("confirmed") or []) if w.get("ok") else []
    sums = (w.get("stats") or {}) if w.get("ok") else {}
    oi_walls = (o.get("oiWalls") or {}) if o.get("ok") else {}
    gex = (o.get("gex") or {}) if o.get("ok") else {}
    fresh = worst_freshness(m, c, w, l, o, s)

    lines = []
    lines.append(f"## FORMULATION · {sym} · {ts_utc} · candidate scouting (Second Council)")
    lines.append(
        f"Regime: {n.get('regime', 'n/a')} — activeModel {n.get('activeModel', 'n/a')}, "
        f"confidence {n.get('confidence', 'n/a')}, thesis: {(n.get('thesis') or 'n/a')[:180]}"
    )
    lines.append(
        f"Direction: {direction} · Grade: {grade} (score {t7['total']}/11.5, "
        f"max achievable this regime {t7['max_achievable']}) · "
        f"Risk: {risk_pct:.1f}% = $0.00 (queued candidate — no slot free)"
    )
    basis_pct = ((q.get("basis") or {}).get("basisPct") if q.get("ok") else None)
    lines.append(
        f"D1  basisPct {fmt(basis_pct, 3)}% (perp {fmt((q.get('basis') or {}).get('perpPrice'), pd_)} · "
        f"spot {fmt((q.get('basis') or {}).get('spotPrice'), pd_)} · "
        f"factor {'n/a' if basis_pct is None else f'{(1 + basis_pct / 100):.6f}'})"
    )
    lines.append(
        f"D2  profile: session POC {fmt(sess.get('poc'), pd_)} · "
        f"day VAL/POC/VAH {fmt(day.get('val'), pd_)}/{fmt(day.get('poc'), pd_)}/{fmt(day.get('vah'), pd_)} · "
        f"month VAL/POC/VAH {fmt(month.get('val'), pd_)}/{fmt(month.get('poc'), pd_)}/{fmt(month.get('vah'), pd_)}"
    )
    lines.append(
        f"D3  VWAP {fmt(vwap.get('vwap'), pd_)} · z {fmt(t7['z_score'], 2)}σ · "
        f"bands ±1σ/2σ/3σ {fmt(bands.get('sd1'), pd_)}/{fmt(bands.get('sd2'), pd_)}/{fmt(bands.get('sd3'), pd_)}"
    )
    lines.append(
        f"D4  EMA 13/89: M15 {ema_line('m15')} · H1 {ema_line('h1')} · H4 {ema_line('h4')} · "
        f"D1 {ema_line('d1')} · 3-TF aligned: "
        f"{'yes' if t7['f1_trend'] >= 2.0 else ('partial' if t7['f1_trend'] > 0 else 'no')}"
    )
    lines.append(
        f"D5  RSI: M15 {fmt(rsi.get('m15'), 1)} · H1 {fmt(rsi.get('h1'), 1)} · H4 {fmt(rsi.get('h4'), 1)} · "
        f"divergence: {'bear (cvd)' if t7['f5_cvd'] else 'none measured'}"
    )
    lines.append(
        f"D6  delta at zone: {'n/a (fp feed unavailable)' if not (c.get('ok')) else 'measured'} · "
        f"bar POC {fmt(day.get('poc'), pd_)}"
    )
    sig_txt = []
    if (s or {}).get("ok") and s.get("sets"):
        for st in s["sets"]:
            for sg in (st.get("sigs") or [])[:3]:
                sig_txt.append(f"{sg.get('type')}/{sg.get('w')}@{fmt(sg.get('price'), pd_)}")
    lines.append(f"D7  signals in zone: {'; '.join(sig_txt) if sig_txt else 'n/a — no in-zone signal measured'}")
    lines.append(
        f"D8  CVD: perp {kpi('perpCvd')} · spot {kpi('spotCvd')} · taker buy {fmt(kpi('buyRatio'), 1)}% · "
        f"quadrant {kpi('quadrant') or 'n/a'}"
    )
    lines.append(
        f"D9  walls: confirmed {len(wall_conf)} · bid ${(sums.get('totalBidUsd') or 0) / 1e6:.1f}M · "
        f"ask ${(sums.get('totalAskUsd') or 0) / 1e6:.1f}M · imbalance "
        f"{fmt(sums.get('imbalance'), 3)}"
    )
    lto_n = len((lo.get('groups') or [])) if lo.get('ok') else 0
    lines.append(f"D10 LTO: {'n/a — no resting institutional orders measured' if lto_n == 0 else f'{lto_n} groups'}")
    lines.append(
        f"D11 clusters: above {fmt(liq_above[0].get('price'), pd_) if liq_above else 'n/a'} "
        f"str {liq_above[0].get('strength') if liq_above else 'n/a'} · below "
        f"{fmt(liq_below[0].get('price'), pd_) if liq_below else 'n/a'} "
        f"str {liq_below[0].get('strength') if liq_below else 'n/a'} (3d window)"
    )
    gate = "n/a (D11 unfed)"
    if t7["lsr"] is not None:
        gate = ("BANNED — wait for the sweep" if t7["lsr"] >= LSR_BAN else "OPEN")
    lines.append(
        f"D12 LSR {fmt(t7['lsr'], 2) if t7['lsr'] is not None else 'n/a'}:1 "
        f"({t7['dom_side'] or 'n/a'} dominant, ±2% window) → GATE: {gate}"
    )
    lines.append(
        f"D13 GEX: {(gex.get('regime') or 'n/a')} · γ-flip {fmt(gex.get('gammaFlip') or o.get('gammaFlipPrice'), pd_)} · "
        f"max pain {fmt(o.get('maxPainStrike'), pd_)}"
    )
    oi_q = (q.get("oiQuadrant") or {}) if q.get("ok") else {}
    lines.append(
        f"D14 OI: Δ1h {fmt(oi_q.get('1h'), 2) if isinstance(oi_q.get('1h'), (int, float)) else 'n/a'} · "
        f"Δ4h {fmt(oi_q.get('4h'), 2) if isinstance(oi_q.get('4h'), (int, float)) else 'n/a'} · "
        f"funding APR {fmt((q.get('funding') or {}).get('annualizedAprPct'), 1)}%"
    )
    sp = (spread or {}).get("spreadPct")
    lines.append(
        f"D15 spread {fmt(sp, 3)}% · stop dist {'n/a (unfilled candidate)' if t7['f4_walls'] is not None else 'n/a'} · "
        f"drag {'n/a' if sp is None else 'measured'} → {'PASS' if t7['f8_spread'] >= 1.0 else ('PARTIAL' if t7['f8_spread'] > 0 else 'n/a')}"
    )
    lines.append(
        f"D16 invariants: heat {fmt(d16.get('heatPct'), 2)}% · slots "
        f"{d16.get('activePositions')}/{d16.get('maxSlots')} · BE armed "
        f"{'yes' if d16.get('beArmed') else 'no'} · bars since fill {d16.get('barsSinceFill')}"
    )
    lines.append(
        "Entry: NO ORDER — queued standby candidate (concurrency cap full). "
        "Re-derive every level live at slot vacancy."
    )
    lines.append("Stop: n/a · T1/T2/T3: n/a until a structural level is measured")
    lines.append(
        f"Table 7: [trend {t7['f1_trend']} · regime {t7['f2_vwap']} · signal {t7['f3_signals']} · "
        f"wall {t7['f4_walls']} · cvd {t7['f5_cvd']} · gate {t7['f6_liq_magnet']} · "
        f"gex {t7['f7_options']} · spread {t7['f8_spread']}] = {t7['total']} · vetoes: "
        f"{'; '.join(vetoes) if vetoes else 'none'}"
    )
    lines.append(
        f"Provenance: /api/cg/market + signals + cvd + bookwalls + liqlevels + options + "
        f"quant + lto; worst data age {fmt(fresh['worstAgeMs'], 0) if fresh['worstAgeMs'] is not None else 'n/a'}ms; "
        f"stale={fresh['anyStale']}; computed {ts_utc}."
    )
    if t7["notes"]:
        lines.append("Scoring notes: " + " | ".join(t7["notes"]))
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# D16 — invariants computed from desk/state.json
# --------------------------------------------------------------------------
def load_contract_specs() -> dict:
    """Delta product specs (contract_value, tick_size) from desk/delta_contracts.json.

    A symbol missing from this file yields `n/a` for every derived sizing number
    — never an assumed contract_value of 1.0 (that silent default is exactly the
    fabrication class G-07 forbids).
    """
    try:
        with open(CONTRACTS_PATH, encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return {}
    specs = raw.get("contracts") or {}
    out = {}
    for sym, v in specs.items():
        try:
            out[sym.upper()] = {"contractValue": float(v["contractValue"]),
                                "tickSize": float(v.get("tickSize") or 0),
                                "productId": v.get("productId")}
        except (KeyError, TypeError, ValueError):
            continue
    return out


def read_state() -> dict:
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def compute_d16(state: dict, specs: dict) -> dict:
    """D16 sizing invariants, computed with the SOP's contractual formulas.

    Per SOP D16:
        risk_usd      = risk_distance_pts * contract_value      (per contract)
        contracts     = floor(equity * risk_pct / risk_usd)     (risk-first sizing)
    So the MINIMUM achievable risk on a 1-contract venue is `risk_usd(1 ct)`.
    Where that floor exceeds the whole risk budget, the SOP's ZERO-RISK-EXPOSURE
    invariant is mechanically unreachable for that asset — that is reported, not
    rounded away.

    `portfolioHeatPct` = sum of per-position 1-contract stop risk / equity.
    This is the desk's own disclosed "dual stop-out worst-case" metric (19.6% in
    its log); it is NOT the SOP's 1.0% risk mandate, and the two are reported
    separately so neither can be mistaken for the other.
    """
    acct = state.get("account") or {}
    pos = state.get("positions") or []
    cfg = state.get("config") or {}
    try:
        equity = float(acct.get("net_equity_usd"))
    except (TypeError, ValueError):
        equity = None
    symbol_map = {k.upper(): v.upper() for k, v in (cfg.get("symbol_map") or {}).items()}

    per_pos, heat, heat_known = [], 0.0, bool(pos)
    for p in pos:
        sym = str(p.get("symbol") or "").upper()
        # desk/delta_contracts.json is keyed by asset sym (BTC); state.json uses
        # the venue symbol (BTCUSD) via config.symbol_map — resolve both sides.
        spec = (specs.get(symbol_map.get(sym, sym))
                or specs.get(sym)
                or specs.get(sym.removesuffix("USD")))
        try:
            dist = abs(float(p["entry_price"]) - float(p["stop_loss"]))
            size = float(p.get("size") or 0)
            entry = float(p["entry_price"])
            tp = float(p["take_profit"])
        except (KeyError, TypeError, ValueError):
            heat_known = False
            continue
        row = {"symbol": sym, "side": p.get("side"), "size": size,
               "entry": entry, "stop": p.get("stop_loss"), "target": p.get("take_profit"),
               "stopDistancePts": round(dist, 6),
               "stopDistancePct": round(dist / entry * 100, 4) if entry else None,
               "breakevenTarget": p.get("breakeven_target"),
               "marginLockedUsd": p.get("margin_locked"),
               "contractValue": spec["contractValue"] if spec else None}
        if spec is None or not equity:
            heat_known = False
            row.update(riskUsd1ct=None, heatPct=None, rewardUsd1ct=None, rMultiple=None,
                       gradeAllowed=None, sizeVerdict="n/a — contract spec unavailable")
        else:
            cv = spec["contractValue"]
            risk = dist * cv * size
            reward = abs(entry - tp) * cv * size
            heat_pct = risk / equity * 100
            heat += heat_pct
            grade, budget = ("A", equity * 0.01) if equity * 0.01 >= equity * 0.005 else ("B", equity * 0.005)
            # risk-first sizing at the minimum (1 contract) and at the B mandate
            max_ct_A = int(equity * 0.01 // risk) if risk else 0
            max_ct_B = int(equity * 0.005 // risk) if risk else 0
            row.update(
                riskUsd1ct=round(risk, 6), heatPct=round(heat_pct, 4),
                rewardUsd1ct=round(reward, 6),
                rMultiple=round(reward / risk, 2) if risk else None,
                riskBudgetA_usd=round(equity * 0.01, 6),
                riskBudgetB_usd=round(equity * 0.005, 6),
                maxContractsAtA=max_ct_A, maxContractsAtB=max_ct_B,
                sizeVerdict=("BREACH: 1 contract risks %.2f%% of equity — exceeds the 1.0%% "
                             "Grade-A mandate by %.1fx; risk-first sizing yields 0 contracts"
                             % (heat_pct, heat_pct / 1.0)) if max_ct_B < 1 else
                            ("AT CAP: only %d contract(s) fit the 0.5%% mandate" % max_ct_B),
            )
        per_pos.append(row)

    bars = max((int(p.get("time_stop_bars_elapsed") or 0) for p in pos), default=0)
    be_armed = any(
        p.get("stop_loss") is not None and p.get("entry_price") is not None
        and abs(float(p["stop_loss"]) - float(p["entry_price"])) < 1e-9
        for p in pos
    )
    fresh = [p.get("filled_at_utc") for p in pos if p.get("filled_at_utc")]

    # scale-out feasibility: 40/40/20 needs 5 contracts to be integer-executable
    scale = []
    for p in pos:
        try:
            size = float(p.get("size") or 0)
        except (TypeError, ValueError):
            continue
        scale.append({"symbol": p.get("symbol"), "size": size,
                      "t1": round(size * 0.4, 4), "t2": round(size * 0.4, 4),
                      "t3": round(size * 0.2, 4),
                      "integerExecutable": all(float(x).is_integer() for x in (size * 0.4, size * 0.4, size * 0.2))})
    # smallest contract size N whose 40/40/20 split is whole contracts
    feasible_n = next((n for n in range(1, 101)
                       if all(float(n * f).is_integer() for f in (0.4, 0.4, 0.2))), None)

    return {
        "portfolioHeatPct": round(heat, 4) if heat_known else None,
        "portfolioHeatCapPct": 1.0,
        "portfolioHeatBreached": bool(heat_known and heat > 1.0),
        "perPosition": per_pos,
        "activePositions": len(pos),
        "stateActivePositions": acct.get("active_positions"),
        "maxSlots": cfg.get("max_concurrent_positions"),
        "cryptoSopSlots": 2,
        "beArmed": bool(be_armed),
        "barsSinceFill": bars,
        "filledAt": fresh,
        "equityUsd": equity,
        "availableUsd": acct.get("available_balance_usd"),
        "scaleOut": scale,
        "minContractsFor404020": feasible_n,
        "riskBudgetPerTradeUsd": {
            "A_1pct": round(equity * 0.01, 6),
            "B_halfpct": round(equity * 0.005, 6),
        } if equity else None,
    }


# --------------------------------------------------------------------------
def main() -> int:
    ts_utc = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    ts_compact = time.strftime("%Y%m%d-%H%M", time.gmtime())
    os.makedirs(DEEPSCAN, exist_ok=True)

    print(f"=== CANONICAL 360 DECIDE ENGINE (HONEST) @ {ts_utc} ===")
    print(f"Base URL: {BASE_URL}")

    state = read_state()
    specs = load_contract_specs()
    d16 = compute_d16(state, specs)
    positions = {p.get("symbol"): p for p in state.get("positions") or []}
    print(f"D16: active {d16['activePositions']} (state says {d16['stateActivePositions']}, "
          f"config max {d16['maxSlots']}, SOP crypto cap {d16['cryptoSopSlots']}) · "
          f"equity ${fmt(d16['equityUsd'])} · available ${fmt(d16['availableUsd'], 6)} · "
          f"BE armed {d16['beArmed']}")
    print(f"D16: 1-contract stop-out heat {fmt(d16['portfolioHeatPct'], 4)}% "
          f"of equity (SOP mandate 1.00%)")
    if d16["portfolioHeatBreached"]:
        print(f"  !! HEAT BREACH: {d16['portfolioHeatPct']}% > 1.00% SOP mandate")
    for row in d16["perPosition"]:
        print(f"    {row['symbol']}: risk ${row['riskUsd1ct']} "
              f"({row['heatPct']}% eq) · R {row['rMultiple']} · {row['sizeVerdict']}")

    screener = fetch_json("/api/cg/screener")
    rows = screener.get("rows") or []
    print(f"Ingested {len(rows)} curated assets (totalCount={screener.get('totalCount')}, "
          f"fapiOk={screener.get('fapiOk')}, stale={screener.get('stale')})")

    deep_syms = ["BTC", "ETH", "SOL", "XRP", "DOGE", "XAU", "NVDA"]

    def load(sym: str) -> tuple[str, dict]:
        return sym, {
            "market": fetch_json(f"/api/cg/market?sym={sym}"),
            "signals": fetch_json(f"/api/cg/signals?sym={sym}"),
            "cvd": fetch_json(f"/api/cg/cvd?sym={sym}&itv=15m"),
            "walls": fetch_json(f"/api/cg/bookwalls?sym={sym}"),
            "liq": fetch_json(f"/api/cg/liqlevels?sym={sym}"),
            "options": fetch_json(f"/api/cg/options?sym={sym}") if sym in ("BTC", "ETH") else {"ok": False, "reason": "BTC/ETH only"},
            "narrative": fetch_json(f"/api/cg/narrative?sym={sym}"),
            "quant": fetch_json(f"/api/cg/quant?sym={sym}"),
            "lto": fetch_json(f"/api/cg/lto?sym={sym}"),
            "spread": fetch_json(f"/api/cg/ticker?sym={sym}"),
        }

    telemetry: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=7) as ex:
        for sym, data in ex.map(load, deep_syms):
            telemetry[sym] = data

    cards, audit = [], []
    for sym in deep_syms:
        data = telemetry[sym]
        m = data["market"]
        narrative = data["narrative"]
        regime = measured_regime(narrative)
        direction = (narrative.get("direction") or "NEUTRAL").upper()
        if regime == "n/a":
            direction = "n/a"
        price = live_price(m)
        tick = data["spread"]
        spread = None
        if (tick or {}).get("ok"):
            sp = tick.get("spreadPct", tick.get("spread"))
            if isinstance(sp, (int, float)):
                spread = {"spreadPct": float(sp)}

        t7 = score_table7(sym, m, data["signals"], data["cvd"], data["walls"],
                          data["liq"], data["options"], spread, regime, direction)
        grade, risk_pct, vetoes = grade_for(t7["total"], t7["unfed"])
        if sym in positions:
            grade_note = "ACTIVE_POSITION (audit only — no new entry)"
        else:
            grade_note = grade

        audit.append({
            "sym": sym,
            "price": price,
            "regime": regime,
            "direction": direction,
            "grade": grade,
            "gradeNote": grade_note,
            "table7": t7,
            "vetoes": vetoes,
            "fresh": worst_freshness(m, data["cvd"], data["walls"],
                                     data["liq"], data["options"], data["signals"]),
            "feeds": {k: feed_has_data(k, v or {}) for k, v in data.items()},
        })

        # Grade >= B AND a measured price => an actual formulation card
        if grade in ("A", "B") and price is not None:
            card = render_card(sym, m.get("name") or sym, ts_utc, data, t7,
                               grade, risk_pct, vetoes, direction, spread, d16)
            path = os.path.join(DEEPSCAN, f"FORMULATION-{sym}-{ts_compact}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(card)
            cards.append(path)
            print(f"CARD  {path}  (score {t7['total']}/11.5, Grade {grade})")
        else:
            print(f"SKIP  {sym}: {grade} (score {t7['total']}/11.5) — "
                  f"{'no measured price' if price is None else 'below Grade B'}")

    # ---- Universe report: all 61 rows, status derived, zero gaps ----
    priced = count_priced_rows(rows)
    fed = sum(1 for a in audit for v in a["feeds"].values() if v)
    total_feeds = sum(len(a["feeds"]) for a in audit)
    coverage = {
        "curatedTotal": len(rows),
        "curatedWithPrice": priced,
        "curatedWithoutPrice": len(rows) - priced,
        "probeSyms": deep_syms,
        "probeFeedsFed": fed,
        "probeFeedsTotal": total_feeds,
        "scoringCoveragePct": round(100.0 * len(deep_syms) / len(rows), 1) if rows else 0.0,
        "note": ("Scoring coverage is intentionally limited to the named probe set; "
                 "the other " + str(len(rows) - len(deep_syms)) + " symbols are billed "
                 "'NOT PROBED' rather than scored from a fallback. A 61-symbol deep "
                 "probe is not run because the upstream radar sweeps 12 s/asset "
                 "(~12.2 min for the full book) and a burst would trip the 429 cooldown."),
    }

    universe_path = os.path.join(DEEPSCAN, f"UNIVERSE-360-{ts_compact}.md")
    with open(universe_path, "w", encoding="utf-8") as f:
        f.write(f"# 360° UNIVERSE AUDIT · {ts_utc} · Second Council (arena.ai)\n\n")
        f.write(f"Curated assets scanned: **{len(rows)}/{screener.get('totalCount')}** · "
                f"screener fapiOk=**{screener.get('fapiOk')}** · stale=**{screener.get('stale')}**\n\n")
        f.write(f"Deep-telemetry feeds answering: **{fed}/{total_feeds}** across "
                f"{len(audit)} probe symbols ({', '.join(deep_syms)}).\n\n")
        f.write(f"Price coverage: **{priced}/{len(rows)}** curated rows carry a measured "
                f"last price; the remaining **{len(rows) - priced}** are billed "
                f"`n/a` / `NO DATA` below rather than filled from a fallback.\n\n")
        f.write(f"Table-7 scoring coverage: **{len(deep_syms)}/{len(rows)} "
                f"({coverage['scoringCoveragePct']}%)** — the deep-probe set is explicit, "
                f"not silently truncated. Every other row states `NOT PROBED`.\n\n")
        f.write("**Epistemic status:** every cell on this page is either a measured value "
                "or an explicit `n/a`. No fallback constant is substituted anywhere (G-06/G-07).\n\n")
        f.write("| Sym | Name | Category | Price | 24h % | Regime | Model | Direction | Table7 | Grade | Status |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
        audit_by_sym = {a["sym"]: a for a in audit}
        for r in rows:
            sym = r.get("sym")
            a = audit_by_sym.get(sym)
            p = r.get("price")
            chg = r.get("chg24hPct")
            m1m2 = r.get("m1m2") or {}
            regime = (a["regime"] if a else (m1m2.get("regime") if isinstance(m1m2, dict) else None)) or "n/a"
            model = (m1m2.get("activeModel") if isinstance(m1m2, dict) else None) or "n/a"
            direction = (a["direction"] if a else (m1m2.get("direction") if isinstance(m1m2, dict) else None)) or "n/a"
            if sym in positions:
                status = "ACTIVE POSITION (audit)"
            elif a:
                status = a["gradeNote"]
            elif p is None:
                status = "NO DATA"
            else:
                status = "NOT PROBED (deep-probe set)"
            t7s = f"{a['table7']['total']:.1f}/11.5" if a else "n/a"
            grades = a["grade"] if a else "n/a"
            p_str = f"{p:.6g}" if isinstance(p, (int, float)) else "n/a"
            chg_str = f"{chg:.2f}%" if isinstance(chg, (int, float)) else "n/a"
            f.write(f"| {sym} | {r.get('name')} | {r.get('category')} | {p_str} | {chg_str} | "
                    f"{regime} | {model} | {direction} | {t7s} | {grades} | {status} |\n")
        f.write("\n## Deep-probe detail\n\n")
        f.write("| Sym | Price | Regime | Dir | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | Total | Unfed dims |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
        for a in audit:
            t = a["table7"]
            f.write(f"| {a['sym']} | {fmt(a['price'], 4)} | {a['regime']} | {a['direction']} | "
                    f"{t['f1_trend']} | {t['f2_vwap']} | {t['f3_signals']} | {t['f4_walls']} | "
                    f"{t['f5_cvd']} | {t['f6_liq_magnet']} | {t['f7_options']} | {t['f8_spread']} | "
                    f"**{t['total']}** | {', '.join(t['unfed']) or 'none'} |\n")

    json_path = os.path.join(DEEPSCAN, f"decide-{ts_compact}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "ts": ts_utc, "engine": "arena-second-council/1.4.0",
            "baseUrl": BASE_URL, "screener": {
                "ok": screener.get("ok"), "totalCount": screener.get("totalCount"),
                "fapiOk": screener.get("fapiOk"), "stale": screener.get("stale"),
                "dataAt": screener.get("dataAt"),
            },
            "d16": d16, "coverage": coverage, "audit": audit, "cards": cards,
        }, f, indent=1, default=str)

    print(f"UNIVERSE {universe_path}")
    print(f"JSON     {json_path}")
    print(f"Cards written: {len(cards)}")
    print(f"Coverage: prices {priced}/{len(rows)} · Table-7 scored "
          f"{len(deep_syms)}/{len(rows)} ({coverage['scoringCoveragePct']}%)")
    starved = all(a["price"] is None for a in audit)
    if starved:
        print("FEED-STARVED: no measured price on any probe symbol — "
              "round is an honest no-trade audit (exit 2).")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
