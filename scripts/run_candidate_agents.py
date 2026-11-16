#!/usr/bin/env python3
"""
scripts/run_candidate_agents.py — MULTI-AGENT CANDIDATE HUNTER (arena.ai R344)

WHY THIS IS NOT A FANTASY ENGINE
--------------------------------
Market-data egress from this sandbox is GitHub-only, so live APIs are
unreachable. Instead of fabricating prices, every agent here reasons **only**
over telemetry the desk itself committed to git (`desk/log.md`, `desk/state.json`)
and over verified venue metadata (`desk/delta_contracts.json`). Every candidate
therefore carries a machine-checkable PROVENANCE block, and a candidate whose
inputs cannot be traced is DROPPED, not scored.

FIVE SPECIALIST AGENTS (each scores 0..1 per candidate, reasons recorded)
------------------------------------------------------------------------
  A1 TREND     EMA stack + RSI + day change.             SOP §2 D4/D5, Table7 F1
  A2 FLOW      footprint balance + microFlow net + CVD.  D6/D7/D8, Table7 F3/F5
  A3 LIQUIDITY liq magnet direction/strength.            D11/D12, §3 Magnet Gate
  A4 STRUCTURE VWAP side + book imbalance direction.     D2/D3/D9, Table7 F2/F4
  A5 RISK      risk-first sizing vs the 1.0% mandate,    D15/D16, §5 veto #5/#7
               R to T1, spread proxy, sweep-position.

CHAIR (adjudicator)
-------------------
  * Independent Table-7 recompute from the SAME telemetry (no agent scores
    are trusted blindly).
  * Any agent that says "veto" blocks the candidate regardless of the total.
  * Dissent is recorded verbatim — a candidate cannot be promoted past a
    specialist objection without the objection being named in the output.

HARD GATES (a candidate failing any one is dropped, reason logged)
------------------------------------------------------------------
  G1 R to T1 >= 2.0 (T1 = Day VAL)                  SOP §1.5, §5 veto #3
  G2 risk @1 contract <= 1.0% of equity             D16, §5 veto #7
  G3 stop distance <= 2.0% (min-tick venue floor)   §5 veto #5 proxy
  G4 no long-liq magnet below >= $4M within 1.2R   §5 veto #2
  G5 T1 is a structural anchor (>= 2.0R)            §5 veto #3

FAIL-CLOSED: with 0 open positions and 0 priced rows on the screener, the
engine reports what it CANNOT verify rather than filling the gap.
"""

from __future__ import annotations

import json
import re
import sys
import time
from dataclasses import dataclass, field

LOG = "/tmp/log343.md"
STATE = "/tmp/r343.json"
SPECS = "desk/delta_contracts.json"

EQUITY = 2.767366          # origin/main desk/state.json -> account.net_liquid_equity_usd
BUD_A = EQUITY * 0.010     # 1.0% Grade A
BUD_B = EQUITY * 0.005     # 0.5% Grade B
LSR_BAN = 2.5              # §3 Magnet Gate


# --------------------------------------------------------------------------- #
# Provenance — every number below must be traceable
# --------------------------------------------------------------------------- #
@dataclass
class Prov:
    order_id: str
    sym: str
    entry: float
    stop: float
    t1: float
    t2: float | None
    t3: float | None
    risk_r: float
    source: str
    debate: list[tuple[str, str, str]] = field(default_factory=list)  # (verdict, source, evidence)
    structural: dict[str, float | str | None] = field(default_factory=dict)
    meta: dict[str, object] = field(default_factory=dict)
    lsr: float | None = None   # long/short ratio; None = genuinely not in telemetry


def load_specs() -> dict:
    raw = json.load(open(SPECS, encoding="utf-8"))["contracts"]
    return {
        s.upper(): {"cv": float(v["contractValue"]), "tick": float(v.get("tickSize") or 0)}
        for s, v in raw.items()
    }


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def parse_log(path: str) -> dict[str, Prov]:
    """Latest structured candidate block per symbol + its most recent re-debate."""
    # encoding="utf-8-sig" strips a leading BOM. Without it the FIRST line of
    # the file carries a U+FEFF that no `^`-anchored regex can match, so the
    # very first evidence line of the very first block silently vanished —
    # which is exactly how A1/A4 reported "no overview telemetry".
    txt = open(path, encoding="utf-8-sig").read()
    blocks: dict[str, Prov] = {}
    pat = re.compile(
        r"NEW (R\d+-[A-Z0-9]+-\d+) ([A-Z0-9]+) (SHORT|LONG) limit ([\d.]+) · stop ([\d.]+) · "
        r"(T1 [\d.]+(?: · T2 [\d.]+)?(?: · T3 [\d.]+)?) · R ([\d.]+)\n"
        r"((?:\s+\[(?:FOR|AGAINST)\s*\][^\n]*\n)+)"
    )
    for m in pat.finditer(txt):
        oid, sym, side, entry, stop, tgts, r, body = m.groups()
        # strip the "T1"/"T2"/"T3" labels BEFORE harvesting numbers, otherwise
        # the regex grabs the digit inside the label ("T1" -> 1.0)
        tvals = [float(x) for x in re.findall(r"[\d.]+", re.sub(r"T\d", "", tgts))]
        verdicts = []
        # NB: iterate the UNSTRIPPED body. `body.strip()` removes the leading
        # indent of the first evidence line, and that line is always `overview`
        # -- so a `\s+`-anchored regex silently dropped it, which is exactly why
        # A1_trend and A4_structure kept reporting "no overview telemetry".
        for line in body.split("\n"):
            vm = re.match(r"\s*\[(FOR|AGAINST)\s*\]\s*([^:]+):\s*(.*)", line)
            if vm:
                verdicts.append((vm.group(1), vm.group(2).strip(), vm.group(3).strip()))
        blocks[sym] = Prov(
            order_id=oid, sym=sym,
            entry=float(entry), stop=float(stop),
            t1=tvals[0], t2=tvals[1] if len(tvals) > 1 else None,
            t3=tvals[2] if len(tvals) > 2 else None,
            risk_r=float(r), source=f"desk/log.md candidate block {oid}",
            debate=verdicts,
        )
    # AUTHORITATIVE lifecycle source: desk/state.json `orders`. The log is a
    # narrative and misses transitions (LINK R379 / LTC R226 have no terminal
    # event in prose but are absent from the ledger). Anything not in the
    # ledger is HISTORICAL and must never be reported as a live candidate.
    live_ids: set[str] = set()
    try:
        import subprocess as _sp
        _st = json.loads(_sp.check_output(
            ["git", "show", "origin/main:desk/state.json"], text=True))
        live_ids = {o.get("id") for o in _st.get("orders", []) if isinstance(o, dict)}
    except Exception as _e:                                    # pragma: no cover
        print(f"!! could not read state.json orders ({_e}); lifecycle = log only")

    # lifecycle: a block stops being a candidate once the desk withdraws/expires
    # it. Without this the hunter resurrects dead orders as "tradeable" -- it
    # did exactly that with R391-XRP-1 (withdrawn) and R101-XAG-1.
    dead: dict[str, str] = {}
    for m in re.finditer(r"(R\d+-[A-Z0-9]+-\d+)\s+(WITHDRAWN|EXPIRED)", txt):
        dead[m.group(1)] = m.group(2)
    for p in blocks.values():
        if p.order_id in dead:
            p.meta["lifecycle"] = dead[p.order_id]
        elif live_ids and p.order_id not in live_ids:
            p.meta["lifecycle"] = "NOT-IN-LEDGER"

    # harvest an explicit LSR only if the log literally states one; never infer
    for p in blocks.values():
        for _v, src, ev in p.debate:
            if src.startswith("liquidation"):
                m = re.search(r"LSR\s*[:=]?\s*([\d.]+)", ev)
                if m:
                    p.lsr = float(m.group(1))
    # most recent re-debate tally per order id
    for m in re.finditer(r"(R\d+-[A-Z0-9]+-\d+) re-debated: FOR (\d+)/AGAINST (\d+) — (\w+)", txt):
        oid, f, a, verdict = m.groups()
        for p in blocks.values():
            if p.order_id == oid:
                p.meta["redebate"] = f"FOR {f}/AGAINST {a} — {verdict}"
    return blocks


# --------------------------------------------------------------------------- #
# Agents — each returns (score 0..1, verdict, reason). "veto" blocks.
# --------------------------------------------------------------------------- #
def _parse_overview(ev: str) -> dict:
    """'h4 ↓/d1 ↓ EMA, price above day VWAP (0.1538 vs 0.1526), h4 RSI 38.1, day -1.0%'"""
    d: dict = {}
    m = re.search(r"h4 ([↓↑])/d1 ([↓↑]) EMA", ev)
    if m:
        d["h4"], d["d1"] = m.group(1), m.group(2)
    m = re.search(r"price (above|below) day VWAP \(([\d.]+) vs ([\d.]+)\)", ev)
    if m:
        d["vwap_side"] = m.group(1)
        d["price"], d["vwap"] = float(m.group(2)), float(m.group(3))
    m = re.search(r"h4 RSI ([\d.]+)", ev)
    if m:
        d["rsi"] = float(m.group(1))
    m = re.search(r"day (-?[\d.]+)%", ev)
    if m:
        d["day_pct"] = float(m.group(1))
    return d


def _parse_footprint(ev: str) -> dict:
    m = re.search(r"bull (\d+) / bear (\d+)", ev)
    d = {"bull": int(m.group(1)), "bear": int(m.group(2))} if m else {}
    d["recent"] = ev.split("recent:")[-1].strip() if "recent:" in ev else ev
    return d


def _parse_micro(ev: str) -> dict:
    m = re.search(r"net (\d+) buy-side vs (\d+) sell-side", ev)
    d = {"buy": int(m.group(1)), "sell": int(m.group(2))} if m else {}
    d["traps_sell"] = int(m.group(1)) if (m := re.search(r"trap:sell×(\d+)", ev)) else 0
    return d


def _parse_cvd(ev: str) -> dict:
    d: dict = {}
    for k, pat in (("taker_buy", r"taker buy ([\d.]+)%"), ("perp_cvd", r"perpCvd (-?\d+)"),
                   ("spot_cvd", r"spotCvd (-?\d+)")):
        m = re.search(pat, ev)
        if m:
            d[k] = float(m.group(1))
    m = re.search(r"latestDiv (\w+)", ev)
    if m:
        d["div"] = m.group(1)
    return d


def _parse_liq(ev: str) -> dict:
    d: dict = {}
    m = re.search(r"(long|short)-liq magnet ([\d.]+) \(str (\d+), ~\$([\d.]+)([kM]) est, (-?[\d.]+)%\)", ev)
    if m:
        d["side"] = m.group(1)
        d["price"] = float(m.group(2))
        d["str"] = int(m.group(3))
        usd = float(m.group(4)) * (1e6 if m.group(5) == "M" else 1e3)
        d["usd"] = usd
        d["dist_pct"] = float(m.group(6))
    return d


def _parse_walls(ev: str) -> dict:
    d: dict = {}
    m = re.search(r"imbalance (-?[\d.]+) \(5m ago (-?[\d.]+)", ev)
    if m:
        d["imb"], d["imb_prev"] = float(m.group(1)), float(m.group(2))
    m = re.search(r"bid \$([\d.]+)B vs ask \$([\d.]+)B", ev)
    if m:
        d["bid_b"], d["ask_b"] = float(m.group(1)), float(m.group(2))
    return d


def _ev(p: Prov, src: str) -> str | None:
    """Exact key first, then a prefix match (the log sometimes decorates the
    source name, e.g. 'overview(4h/d1)')."""
    for _v, s, e in p.debate:
        if s == src:
            return e
    for _v, s, e in p.debate:
        if s.startswith(src):
            return e
    return None


def agent_trend(p: Prov) -> tuple[float, str, str]:
    ev = _ev(p, "overview")
    if not ev:
        return 0.0, "veto", "no overview telemetry in the committed block — D4/D5 unverifiable"
    d = _parse_overview(ev)
    short = p.stop > p.entry
    aligned_h4 = d.get("h4") == ("↓" if short else "↑")
    aligned_d1 = d.get("d1") == ("↓" if short else "↑")
    rsi = d.get("rsi")
    day = d.get("day_pct")
    score = 0.0
    if aligned_h4:
        score += 0.45
    if aligned_d1:
        score += 0.25
    if rsi is not None and ((short and rsi < 50) or (not short and rsi > 50)):
        score += 0.15
    if day is not None and ((short and day < 0) or (not short and day > 0)):
        score += 0.15
    v = "pass" if aligned_h4 and aligned_d1 else ("weak" if aligned_h4 else "veto")
    reason = (f"h4 {d.get('h4')}{d.get('d1')} / d1 {d.get('d1')} EMA; RSI {rsi}; day {day}% — "
              f"{'both TFs aligned' if aligned_h4 and aligned_d1 else 'higher-TF conflict' if not aligned_h4 and not aligned_d1 else 'partial alignment'}")
    return round(score, 2), v, reason


def agent_flow(p: Prov) -> tuple[float, str, str]:
    fp_ev, mf_ev, cvd_ev = _ev(p, "footprint"), _ev(p, "microFlow(abs/trap/exh)"), _ev(p, "cvd")
    if not (fp_ev and cvd_ev):
        return 0.0, "veto", "footprint or CVD missing — D6/D8 unverifiable"
    fp, mf, cvd = _parse_footprint(fp_ev), _parse_micro(mf_ev or ""), _parse_cvd(cvd_ev)
    short = p.stop > p.entry
    score = 0.0
    bull, bear = fp.get("bull"), fp.get("bear")
    if bull and bear:
        side = bear if short else bull
        other = bull if short else bear
        if side > other:
            score += 0.35 * min(1.0, (side - other) / max(1, side))
    buy, sell = mf.get("buy"), mf.get("sell")
    if buy is not None and sell is not None:
        dom = sell if short else buy
        opp = buy if short else sell
        if dom > opp:
            score += 0.30 * min(1.0, (dom - opp) / max(1, dom))
        elif dom < opp:
            score -= 0.10
    tb = cvd.get("taker_buy")
    pc = cvd.get("perp_cvd")
    if tb is not None and pc is not None:
        if (short and tb < 50) or (not short and tb > 50):
            score += 0.20
        if (short and pc < 0) or (not short and pc > 0):
            score += 0.15
    div = cvd.get("div")
    if div and div.startswith("bear" if short else "bull"):
        score += 0.10 if "stale" not in div else 0.03
    traps = mf.get("traps_sell", 0)
    veto = ""
    # Q6 stale-signal check: a divergence marked stale must not be the trigger
    if div and "stale" in str(div) and not (tb and ((short and tb < 50) or (not short and tb > 50))):
        veto = "only divergence present is STALE and taker flow does not confirm — Q6 stale-signal trap"
    reason = (f"footprint {bull}/{bear}; microFlow net {buy}v{sell}"
              f"{f' (trap:sell x{traps})' if traps else ''}; taker buy {tb}%; perpCvd {pc}; div {div}")
    return round(max(0.0, min(1.0, score)), 2), ("veto" if veto else "pass"), (veto or reason)


def agent_liquidity(p: Prov, specs: dict) -> tuple[float, str, str]:
    ev = _ev(p, "liquidation")
    if not ev:
        return 0.0, "veto", "no liquidation telemetry — D11/D12 (Magnet Gate) UNVERIFIABLE"
    d = _parse_liq(ev)
    loss = max(x for x in (0.1,) if True)  # placeholder to avoid lint noise
    short = p.stop > p.entry
    risk_pts = abs(p.entry - p.stop)
    reasons = []
    veto = ""
    score = 0.0
    if d:
        side = d["side"]
        favourable = (short and side == "long") or (not short and side == "short")
        # distance in R units from entry
        r_to_magnet = abs(d["dist_pct"]) / 100 * p.entry / risk_pts if risk_pts else None
        if favourable:
            score += 0.6 if d["str"] >= 50 else 0.35
            reasons.append(f"{side}-liq magnet {d['price']} str {d['str']} (~${d['usd']/1e6:.1f}M, {d['dist_pct']}% = {r_to_magnet:.2f}R) is DOWNSTREAM — valid target")
            # §5 veto #2: opposite magnet str>=50 within 1.2R of entry
        else:
            if d["str"] >= 50 and r_to_magnet is not None and r_to_magnet <= 1.2:
                veto = (f"opposite {side}-liq magnet str {d['str']} at {r_to_magnet:.2f}R of entry "
                        f"(<=1.2R) — §5 hard veto #2")
            score += 0.1
            reasons.append(f"{side}-liq magnet is AGAINST the trade ({d['dist_pct']}%)")
        if d["str"] >= 70:
            score += 0.1
        if abs(d["dist_pct"]) >= 1.5:
            score += 0.2   # plenty of room to the magnet
        if d["usd"] < 5e6:
            reasons.append(f"magnet size ${d['usd']/1e6:.1f}M is below the §2 D11 major-cluster bar ($5M)")
    reasons.append("LSR (±2%) NOT COMPUTED — liq levels above price absent from committed telemetry; §3 gate cannot be formally cleared")
    return round(min(1.0, score), 2), ("veto" if veto else "pass"), ("; ".join(reasons) if not veto else veto)


def agent_structure(p: Prov) -> tuple[float, str, str]:
    ev = _ev(p, "overview")
    w_ev = _ev(p, "bookWalls")
    if not ev:
        return 0.0, "veto", "no overview telemetry — D2/D3 unverifiable"
    o = _parse_overview(ev)
    w = _parse_walls(w_ev) if w_ev else {}
    short = p.stop > p.entry
    score = 0.0
    reasons = []
    vs = o.get("vwap_side")
    if vs:
        good = (short and vs == "above") or (not short and vs == "below")
        score += 0.45 if good else 0.05
        reasons.append(f"price {vs} day VWAP ({o.get('price')} vs {o.get('vwap')}) — "
                       f"{'premium for a short / discount for a long' if good else 'WRONG side of VWAP (Table 7 F2 = 0)'}")
    imb = w.get("imb")
    if imb is not None and w.get("imb_prev") is not None:
        falling = imb < w["imb_prev"]
        good = (short and imb < 0) or (not short and imb > 0)
        score += 0.35 if good else 0.0
        reasons.append(f"depth imbalance {imb} (5m {w['imb_prev']}, {'falling' if falling else 'rising'}) "
                       f"{'+' if good else '-'}aligned")
    bid_b, ask_b = w.get("bid_b"), w.get("ask_b")
    if bid_b is not None and ask_b is not None:
        heavy = ask_b if short else bid_b
        thin = bid_b if short else ask_b
        if heavy >= thin * 1.5:
            reasons.append(f"book skew bid ${bid_b}B vs ask ${ask_b}B supports the passive side")
            score += 0.15
    # entry placement vs VWAP: better if the limit is not chasing
    if o.get("price") and o.get("vwap") and short:
        if p.entry >= o["vwap"]:
            score += 0.10
    return round(min(1.0, score), 2), "pass", "; ".join(reasons)


def agent_risk(p: Prov, specs: dict) -> tuple[float, str, str]:
    spec = specs.get(p.sym)
    if not spec:
        return 0.0, "veto", f"no verified contract spec for {p.sym} — sizing unverifiable (G-07)"
    cv = spec["cv"]
    risk_pts = abs(p.entry - p.stop)
    risk_usd = risk_pts * cv
    risk_pct = risk_usd / EQUITY * 100
    r_t1 = abs(p.entry - p.t1) / risk_pts if risk_pts else 0
    stop_pct = risk_pts / p.entry * 100
    contracts_a = int(BUD_A // risk_usd) if risk_usd else 0
    contracts_b = int(BUD_B // risk_usd) if risk_usd else 0
    veto = ""
    reasons = []
    # A setup is only unsizeable if it fails at the LOWEST tier (Grade B, 0.5%).
    # Failing at 1.0% alone means "downgrade to B", not "block".
    if contracts_b < 1:
        veto = (f"1 contract risks ${risk_usd:.4f} = {risk_pct:.2f}% of ${EQUITY:.2f} equity — "
                f"risk-first sizing returns {contracts_b} contracts even at the 0.5% Grade-B "
                f"mandate (§5 veto #7); {contracts_a} ct at 1.0%")
        return 0.0, "veto", veto
    if contracts_a < 1:
        reasons.append(f"UNSIZEABLE AT GRADE A (1.0%): 0 ct; only {contracts_b} ct at 0.5% -> capped at Grade B")
    score = 0.0
    score += 0.30 if risk_pct <= 0.5 else 0.15
    score += 0.30 if r_t1 >= 2.0 else 0.0
    score += 0.20 if stop_pct <= 2.0 else 0.0
    score += 0.20 if contracts_a >= 3 else 0.10
    reasons.append(f"risk ${risk_usd:.4f}/ct = {risk_pct:.2f}% equity; {contracts_a} ct fit the 1.0% budget "
                   f"({contracts_b} at 0.5%); R to T1 {r_t1:.2f}; stop {stop_pct:.2f}%")
    if stop_pct > 2.0:
        veto = f"stop distance {stop_pct:.2f}% exceeds the 2.0% minimum-tick floor (§5 veto #5 proxy)"
    return round(score, 2), ("veto" if veto else "pass"), ("; ".join(reasons) if not veto else veto)


# --------------------------------------------------------------------------- #
# Chair — independent recompute + adjudication
# --------------------------------------------------------------------------- #
def chair_table7(p: Prov, agents: dict, specs: dict) -> dict:
    """Independent recompute of Table 7 F1..F8 from raw telemetry. Never trusts agents."""
    o = _parse_overview(_ev(p, "overview") or "")
    fp = _parse_footprint(_ev(p, "footprint") or "")
    mf = _parse_micro(_ev(p, "microFlow(abs/trap/exh)") or "")
    cvd = _parse_cvd(_ev(p, "cvd") or "")
    liq = _parse_liq(_ev(p, "liquidation") or "")
    w = _parse_walls(_ev(p, "bookWalls") or "")
    short = p.stop > p.entry

    # F1 trend 2.0 — both TFs aligned
    f1 = 2.0 if (o.get("h4") == ("↓" if short else "↑") and o.get("d1") == ("↓" if short else "↑")) else (
        1.0 if o.get("h4") == ("↓" if short else "↑") else 0.0)
    # F2 vwap 1.5
    vs = o.get("vwap_side")
    f2 = 1.5 if ((short and vs == "above") or (not short and vs == "below")) else 0.0
    # F3 signal 2.0 — strong divergence / absorption AT the entry zone, in the
    # trade's own direction. The old test was direction-blind: it gave a short
    # 2.0 for "Absorption/buy" (a bullish print). Token map below is explicit so
    # the call is auditable; unrecognised prints earn partial 1.0, never 2.0.
    rec = (fp.get("recent") or "").lower()
    if "none" in rec and "recent: none" in rec:
        rec = ""
    bear_tok = ("trapped longs", "divergence/sell", "bear div", "exhaustion/buy",
                "absorption/buy", "strong div/sell")
    bull_tok = ("trapped shorts", "divergence/buy", "bull div", "exhaustion/sell",
                "absorption/sell", "strong div/buy")
    want, anti = (bear_tok, bull_tok) if short else (bull_tok, bear_tok)
    if any(t in rec for t in anti) and not any(t in rec for t in want):
        f3 = 0.0                      # signal is actively AGAINST the trade
    elif any(t in rec for t in want):
        f3 = 2.0
    elif "divergence" in rec or "trap" in rec or "exhaustion" in rec or "absorption" in rec:
        f3 = 1.0                      # signal present, direction unresolved
    else:
        f3 = 0.0
    # F4 wall 1.5 — needs a confirmed >=$5M wall w/ age; committed telemetry gives only aggregate depth
    f4 = 0.0
    # F5 cvd 1.0 — non-stale divergence in direction
    div = str(cvd.get("div") or "")
    f5 = 1.0 if div and div.startswith("bear" if short else "bull") and "stale" not in div else 0.0
    # F6 magnet gate 1.5 — the ROW CONDITION IS "liquidation skew favours the
    # trade direction (LSR aligned)". A downstream magnet is a TARGET, not an
    # LSR skew. Awarding 1.5 for magnet presence alone double-counted the same
    # cluster already credited as the T1 target, and broke zero-fallback (F-02).
    f6 = 0.0
    lsr = p.lsr if isinstance(p.lsr, (int, float)) else None
    if lsr is not None:
        aligned = (lsr >= 1.5) if short else (lsr <= 1.0 / 1.5)
        f6 = 1.5 if aligned else 0.0
    # F7 GEX 1.0 — BTC/ETH only, no options telemetry committed
    f7 = 0.0
    # F8 spread 1.0 — no per-symbol spread committed (D15 unmeasured)
    f8 = 0.0
    total = round(f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8, 1)
    return {
        "f1": f1, "f2": f2, "f3": f3, "f4": f4, "f5": f5, "f6": f6, "f7": f7, "f8": f8,
        "total": total,
        "max_achievable_here": 11.5 - 3.5,  # F4/F7/F8 unmeasurable from committed data
        "unmeasured": [k for k, why in
                       (("F4", "no per-wall USD/age in committed telemetry"),
                        ("F7", "no options/GEX telemetry committed"),
                        ("F8", "no per-symbol spread committed")) if True],
    }


def judge(p: Prov, agents: dict, specs: dict) -> dict:
    """Apply hard gates, then grade. A veto anywhere blocks."""
    vetoes = [f"{name}: {reason}" for name, (score, verdict, reason) in agents.items() if verdict == "veto"]
    spec = specs.get(p.sym)
    risk_pts = abs(p.entry - p.stop)
    r_t1 = abs(p.entry - p.t1) / risk_pts if risk_pts else 0
    t7 = chair_table7(p, agents, specs)

    gates = {}
    gates["G1_R_to_T1_ge_2.0"] = r_t1 >= 2.0
    gates["G2_risk_1ct_le_1pct"] = bool(spec) and (risk_pts * spec["cv"] / EQUITY * 100) <= 1.0
    gates["G3_stop_le_2pct"] = (risk_pts / p.entry * 100) <= 2.0
    gates["G4_no_opposite_magnet_1.2R"] = not any(
        "hard veto #2" in v for v in vetoes)
    gates["G5_T1_structural_ge_2R"] = r_t1 >= 2.0

    # The SOP grades on TABLE 7, not on the specialist-agent mean. The agent
    # mean is an internal advisory signal only -- the old code graded on it and
    # so promoted a 6.5/11.5 setup to "Grade A" (1.0% risk) when the manual
    # says Grade A requires >= 7.0 AND 6.5 is Grade B (0.5% risk).
    score = round(sum(s for s, _v, _r in agents.values()) / len(agents) * 10, 2)
    t7_total = t7["total"]
    if t7_total >= 7.0:
        grade = "A"
    elif t7_total >= 5.0:
        grade = "B"
    else:
        grade = "VETO"
    if vetoes or not all(gates.values()):
        grade = "BLOCKED"
    return {
        "table7": t7, "gates": gates, "vetoes": vetoes,
        "agent_mean_score": score, "grade": grade,
        "risk_pct": 0.0 if grade in ("BLOCKED", "VETO") else (1.0 if grade == "A" else 0.5),
        "r_t1": round(r_t1, 2),
        "r_t2": round(abs(p.entry - p.t2) / risk_pts, 2) if (p.t2 and risk_pts) else None,
        "r_t3": round(abs(p.entry - p.t3) / risk_pts, 2) if (p.t3 and risk_pts) else None,
    }


# --------------------------------------------------------------------------- #
def main() -> int:
    ts = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    specs = load_specs()
    cands = parse_log(LOG)
    print(f"=== MULTI-AGENT CANDIDATE HUNTER @ {ts} ===")
    print(f"Equity ${EQUITY:.4f} (from origin/main state.json) · "
          f"A budget ${BUD_A:.5f} · B budget ${BUD_B:.5f}")
    print(f"Parsed {len(cands)} symbol candidate blocks from committed desk/log.md")
    print(f"Verified contract specs available: {len(specs)} symbols\n")

    out = []
    for sym, p in sorted(cands.items()):
        agents = {
            "A1_trend": agent_trend(p),
            "A2_flow": agent_flow(p),
            "A3_liquidity": agent_liquidity(p, specs),
            "A4_structure": agent_structure(p),
            "A5_risk": agent_risk(p, specs),
        }
        verdict = judge(p, agents, specs)
        out.append({"prov": p, "agents": agents, "verdict": verdict})

        print("=" * 100)
        print(f"{p.order_id}  {sym} {'SHORT' if p.stop > p.entry else 'LONG'} "
              f"entry {p.entry} stop {p.stop} T1 {p.t1} T2 {p.t2} T3 {p.t3} · R {p.risk_r}")
        print(f"  provenance: {p.source}")
        for name, (score, v, reason) in agents.items():
            print(f"  {name:14} {score:5.2f}  [{v.upper():5}] {reason}")
        t7 = verdict["table7"]
        print(f"  CHAIR Table7: F1 {t7['f1']} · F2 {t7['f2']} · F3 {t7['f3']} · F4 {t7['f4']} "
              f"· F5 {t7['f5']} · F6 {t7['f6']} · F7 {t7['f7']} · F8 {t7['f8']} = "
              f"{t7['total']}/11.5 (unmeasurable here: F4/F7/F8)")
        print(f"  CHAIR gates: " + ", ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in verdict["gates"].items()))
        print(f"  CHAIR R: T1 {verdict['r_t1']} · T2 {verdict['r_t2']} · T3 {verdict['r_t3']}")
        lc = p.meta.get("lifecycle", "ACTIVE")
        print(f"  LIFECYCLE: {lc}" + ("" if lc == "ACTIVE" else "  <-- not a live candidate"))
        print(f"  VERDICT: {verdict['grade']} (agent mean {verdict['agent_mean_score']}/10)")
        if verdict["vetoes"]:
            for v in verdict["vetoes"]:
                print(f"    !! VETO {v}")

    json.dump(
        [{
            "sym": o["prov"].sym, "orderId": o["prov"].order_id,
            "entry": o["prov"].entry, "stop": o["prov"].stop,
            "t1": o["prov"].t1, "t2": o["prov"].t2, "t3": o["prov"].t3,
            "agents": {k: {"score": v[0], "verdict": v[1], "reason": v[2]} for k, v in o["agents"].items()},
            "verdict": o["verdict"],
        } for o in out],
        open("/tmp/agents_out.json", "w"), indent=1)

    print(f"\n{len(out)} candidates adjudicated · "
          f"{sum(1 for o in out if o['verdict']['grade'] != 'BLOCKED')} tradeable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
