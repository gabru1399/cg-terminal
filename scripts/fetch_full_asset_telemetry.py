#!/usr/bin/env python3
"""
fetch_full_asset_telemetry.py — MANDATORY MULTI-TAB ORDER-FLOW TELEMETRY SCRAPER
================================================================================
SOP v2.1.0 | Canonical Master Specification Deep Telemetry Module

PURPOSE:
  Fetches, normalizes, and aggregates LIVE telemetry across ALL 9 terminal tabs
  and endpoints for any given asset (or list of assets):
    [TAB 1] Overview & Auction Profiles (Session 8h, Day, Week, Month VAL/POC/VAH + VWAP Bands + EMAs + RSI)
    [TAB 2] Footprint Signals & Delta (Absorption, Divergence, StrongDiv, Trap, Exhaustion)
    [TAB 3] Liquidation Levels & LSR (3d, 7d, 30d clusters, sweep magnets, Skew Ratio)
    [TAB 4] Live Liquidation Tape (Binance, Bybit, OKX live prints & 24h totals)
    [TAB 5] Order Book Walls & Depth (Multi-exchange aggregate depth imbalance & confirmed walls)
    [TAB 6] Whale Orders / Large Orders (Resting whale bids/asks >= $100K / $1M)
    [TAB 7] Cumulative Volume Delta (CVD) (Spot vs Perp CVD & divergences)
    [TAB 8] Open Interest & Funding Rates (OI dynamics, 6h/24h changes, annualized funding)
    [TAB 9] Narrative Regime & Quant Models (M1/M2 models, win probability, EV, trade plan)

USAGE:
  python scripts/fetch_full_asset_telemetry.py --sym BTC
  python scripts/fetch_full_asset_telemetry.py --sym BTC,ETH,SOL,XAU --save
  python scripts/fetch_full_asset_telemetry.py --candidates  (scans top active/candidate assets)
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import concurrent.futures
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = Path(os.path.abspath(__file__)).parent.parent
DEEPSCAN_DIR = WORKSPACE / "desk" / "deepscan"
DEEPSCAN_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = os.environ.get("TERMINAL_URL", "http://localhost:3000")

def fetch_endpoint(url, timeout=12.0):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8")), None
            return None, f"HTTP {resp.status}"
    except Exception as e:
        return None, str(e)

def fetch_asset_all_tabs(sym):
    sym = sym.upper().strip()
    base = f"{BASE_URL}/api/cg"
    
    endpoints = {
        "market": f"{base}/market?sym={sym}",
        "signals": f"{base}/signals?sym={sym}",
        "liqlevels_3d": f"{base}/liqlevels?sym={sym}&range=3d",
        "liqlevels_30d": f"{base}/liqlevels?sym={sym}&range=30d",
        "liq_live": f"{base}/liq-live?sym={sym}&limit=25",
        "bookwalls": f"{base}/bookwalls?sym={sym}",
        "lto": f"{base}/lto?symbol={sym}&minVolUsd=100000",
        "cvd": f"{base}/cvd?sym={sym}",
        "oi": f"{base}/oi?sym={sym}",
        "funding": f"{base}/funding?sym={sym}",
        "narrative": f"{base}/narrative?sym={sym}",
        "quant": f"{base}/quant?sym={sym}"
    }
    
    results = {}
    errors = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        future_map = {executor.submit(fetch_endpoint, url): name for name, url in endpoints.items()}
        for future in concurrent.futures.as_completed(future_map):
            name = future_map[future]
            try:
                data, err = future.result()
                if data:
                    results[name] = data
                else:
                    errors[name] = err
            except Exception as e:
                errors[name] = str(e)
                
    return {
        "sym": sym,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "timestamp_ts": int(time.time() * 1000),
        "data": results,
        "errors": errors
    }

def print_telemetry_report(report):
    sym = report["sym"]
    data = report["data"]
    errs = report["errors"]
    
    print("\n" + "═" * 84)
    print(f"  360° ORDER-FLOW TELEMETRY AUDIT: {sym} — {report['timestamp_utc']}")
    print("═" * 84)
    
    # ─── TAB 1: OVERVIEW & AUCTION MARKET STRUCTURE ───────────────────────────
    mkt = data.get("market") or {}
    price_info = mkt.get("price") or {}
    auction = mkt.get("auction") or {}
    vwap_info = mkt.get("vwap") or {}
    indicators = mkt.get("indicators") or {}
    
    last_price = price_info.get("last")
    print(f"\n[TAB 1: OVERVIEW & AUCTION MARKET STRUCTURE]")
    print(f"  • Reference Price : {last_price} USD (Bid: {price_info.get('bid')} | Ask: {price_info.get('ask')})")
    
    sess = auction.get("session") or {}
    day = auction.get("day") or {}
    week = auction.get("week") or {}
    month = auction.get("month") or {}
    
    print(f"  • Auction Profiles:")
    print(f"    - Session (8h)  : VAL {sess.get('val')} │ POC {sess.get('poc')} │ VAH {sess.get('vah')} (Vol: ${(sess.get('volume', 0)/1e6):.1f}M)")
    print(f"    - Day (UTC)     : VAL {day.get('val')} │ POC {day.get('poc')} │ VAH {day.get('vah')} (Vol: ${(day.get('volume', 0)/1e6):.1f}M)")
    print(f"    - Week (UTC)    : VAL {week.get('val')} │ POC {week.get('poc')} │ VAH {week.get('vah')}")
    print(f"    - Month (UTC)   : VAL {month.get('val')} │ POC {month.get('poc')} │ VAH {month.get('vah')}")
    
    bands = vwap_info.get("bands") or {}
    cur_vwap = vwap_info.get("vwap")
    if cur_vwap and bands.get("sd1"):
        sd1, sd2, sd3 = bands["sd1"], bands["sd2"], bands["sd3"]
        print(f"  • Day VWAP & Bands:")
        print(f"    - VWAP: {cur_vwap:.2f} │ +1σ: {cur_vwap+sd1:.2f} │ +2σ: {cur_vwap+sd2:.2f} │ +3σ: {cur_vwap+sd3:.2f}")
        print(f"                       │ -1σ: {cur_vwap-sd1:.2f} │ -2σ: {cur_vwap-sd2:.2f} │ -3σ: {cur_vwap-sd3:.2f}")
        
    m15_ind = indicators.get("m15") or {}
    h1_ind = indicators.get("h1") or {}
    h4_ind = indicators.get("h4") or {}
    print(f"  • Indicators (Trend / RSI):")
    print(f"    - M15: RSI {m15_ind.get('rsi')} │ EMA13 {m15_ind.get('ema13')} │ EMA89 {m15_ind.get('ema89')}")
    print(f"    - H1 : RSI {h1_ind.get('rsi')} │ EMA13 {h1_ind.get('ema13')} │ EMA89 {h1_ind.get('ema89')}")
    print(f"    - H4 : RSI {h4_ind.get('rsi')} │ EMA13 {h4_ind.get('ema13')} │ EMA89 {h4_ind.get('ema89')}")

    # ─── TAB 2: FOOTPRINT SIGNALS & DELTA ─────────────────────────────────────
    sigs = data.get("signals") or {}
    counts = sigs.get("counts") or {}
    print(f"\n[TAB 2: FOOTPRINT SIGNALS & DELTA]")
    print(f"  • Signal Totals   : {counts.get('all', 0)} total ({counts.get('bullish', 0)} Bullish / {counts.get('bearish', 0)} Bearish)")
    
    recent_sigs = []
    for s_set in sigs.get("sets") or []:
        for s in s_set.get("sigs") or []:
            st = s.get("t", "")
            side = s.get("side", "")
            p = s.get("p", 0)
            u = s.get("u", 0)
            sig_map = {"abs": "Absorption", "trap": "Trap", "sdiv": "StrongDiv", "div": "Divergence", "exh": "Exhaustion"}
            recent_sigs.append(f"{sig_map.get(st, st)} [{side.upper()}] @ {p} (${u/1e6:.1f}M notional)")
            if len(recent_sigs) >= 4:
                break
        if len(recent_sigs) >= 4:
            break
    print(f"  • Recent Prints   : {', '.join(recent_sigs) if recent_sigs else 'None detected'}")

    # ─── TAB 3: LIQUIDATION CLUSTERS & LSR ────────────────────────────────────
    liq3d = data.get("liqlevels_3d") or {}
    stats = liq3d.get("stats") or {}
    totals = stats.get("totals") or {}
    key_levels = stats.get("keyLevels") or {}
    
    print(f"\n[TAB 3: LIQUIDATION CLUSTERS & LIQUIDITY MAGNETS]")
    lsr = liq3d.get("lsr", 1.0)
    print(f"  • Liquidation Skew Ratio (LSR): {lsr:.2f}:1 ({'BANS S3 PASSIVE FRONT-RUN' if lsr >= 2.5 else 'NORMAL SKEW'})")
    print(f"  • Open Exposure   : Shorts (Above) ${(totals.get('shorts', 0)/1e6):.1f}M │ Longs (Below) ${(totals.get('longs', 0)/1e6):.1f}M")
    
    above_lvls = [f"{l.get('price')} (+{l.get('distPct'):.2f}%, str {l.get('strength', 0):.0f})" for l in key_levels.get("above") or []][:3]
    below_lvls = [f"{l.get('price')} (-{l.get('distPct'):.2f}%, str {l.get('strength', 0):.0f})" for l in key_levels.get("below") or []][:3]
    print(f"  • Sweep Magnets Above : { ' | '.join(above_lvls) if above_lvls else 'None' }")
    print(f"  • Sweep Magnets Below : { ' | '.join(below_lvls) if below_lvls else 'None' }")

    # ─── TAB 4: LIVE LIQUIDATION PRINTS ───────────────────────────────────────
    liq_live = data.get("liq_live") or {}
    venues = liq_live.get("venues") or []
    events_stored = liq_live.get("universeEventsStored", 0)
    print(f"\n[TAB 4: LIVE LIQUIDATIONS TAPE]")
    print(f"  • Universe Events : {events_stored} recorded across Binance, Bybit, OKX")
    print(f"  • Active Venues   : {', '.join([v.get('venue', '') for v in venues if v.get('status') == 'open'])}")

    # ─── TAB 5: ORDER BOOK WALLS & DEPTH IMBALANCE ────────────────────────────
    bw = data.get("bookwalls") or {}
    bw_model = bw.get("model") or {}
    bw_venues = bw.get("venues") or []
    print(f"\n[TAB 5: ORDER BOOK WALLS & DEPTH IMBALANCE]")
    print(f"  • Venues Aggregated: {', '.join(bw_venues)}")
    print(f"  • Snapshots Loaded : {bw_model.get('snapshots', 0)} frames (Band ±{bw.get('band', 5)}%)")
    last_book = bw_model.get("last") or {}
    print(f"  • Book Mid State   : Last {last_book.get('price')} │ Best Bid {last_book.get('bid')} │ Best Ask {last_book.get('ask')}")

    # ─── TAB 6: WHALE ORDERS / LARGE ORDERS (LTO) ─────────────────────────────
    lto = data.get("lto") or {}
    groups = lto.get("groups") or []
    whale_ask_usd = 0
    whale_bid_usd = 0
    whale_orders_list = []
    for g in groups:
        for o in g.get("list") or []:
            vol = o.get("volUsd", 0)
            side = o.get("side")
            p = o.get("price")
            if side == 1:
                whale_ask_usd += vol
                whale_orders_list.append(f"ASK {p} (${vol/1e3:.0f}K on {g.get('exchangeName')})")
            elif side == 2:
                whale_bid_usd += vol
                whale_orders_list.append(f"BID {p} (${vol/1e3:.0f}K on {g.get('exchangeName')})")
                
    print(f"\n[TAB 6: WHALE ORDERS & LARGE RESTING LIQUIDITY]")
    print(f"  • Total Whale Asks : ${(whale_ask_usd/1e6):.2f}M (Sell Walls)")
    print(f"  • Total Whale Bids : ${(whale_bid_usd/1e6):.2f}M (Buy Walls)")
    print(f"  • Prominent Orders : {', '.join(whale_orders_list[:4]) if whale_orders_list else 'No orders >= $100K active'}")

    # ─── TAB 7: OPEN INTEREST & FUNDING RATES ─────────────────────────────────
    oi_data = data.get("oi") or {}
    fund_data = data.get("funding") or {}
    print(f"\n[TAB 7: OPEN INTEREST & FUNDING DYNAMICS]")
    print(f"  • Open Interest    : ${oi_data.get('oiUsd', 0)/1e6:.1f}M USD (Change 24h: {oi_data.get('oiChange24hPct', 0):+.2f}%)")
    print(f"  • Annualized Funding: {fund_data.get('predictedAnnualPct', fund_data.get('annualPct', 0)):+.2f}%")

    # ─── TAB 8: NARRATIVE & QUANT ENGINE VERDICT ──────────────────────────────
    narr = data.get("narrative") or {}
    plan = narr.get("plan") or {}
    prob = narr.get("probability") or {}
    
    print(f"\n[TAB 8: NARRATIVE REGIME & QUANT EV VERDICT]")
    print(f"  • Regime & Model   : {narr.get('regime')} │ {narr.get('activeModel')} │ Direction: {narr.get('direction')}")
    ev_val = prob.get('evR') if prob.get('evR') is not None else 0.0
    pwin_val = prob.get('pWin') if prob.get('pWin') is not None else 0.0
    print(f"  • Confidence / EV  : Grade {narr.get('grade')} (Score {narr.get('confidence', 0)}/100) │ EV: {ev_val:.2f}R │ P(Win): {pwin_val:.1%}")
    if plan.get("entryZone"):
        ez = plan.get("entryZone")
        ez0 = ez[0] if len(ez) > 0 and ez[0] is not None else 0.0
        ez1 = ez[1] if len(ez) > 1 and ez[1] is not None else 0.0
        stop_val = plan.get("stop") if plan.get("stop") is not None else 0.0
        best_r = plan.get("bestR") if plan.get("bestR") is not None else 0.0
        print(f"  • Algorithmic Plan : Entry {ez0:.2f}-{ez1:.2f} │ Stop {stop_val:.2f} │ Best R: {best_r:.2f}R")
        tg_strs = [f"{t.get('label')} @ {(t.get('level') or 0.0):.2f} ({(t.get('rMultiple') or 0.0):.1f}R)" for t in plan.get("targets") or []]
        print(f"  • Targets          : {' | '.join(tg_strs)}")
    if plan.get("vetoes"):
        print(f"  • Active Vetoes    : {'; '.join(plan.get('vetoes'))}")
        
    print("\n" + "═" * 84)

def main():
    parser = argparse.ArgumentParser(description="Mandatory 360° Order-Flow Multi-Tab Telemetry Scraper")
    parser.add_argument("--sym", type=str, default="BTC", help="Symbol or comma-separated list of symbols (e.g. BTC,ETH,SOL,XAU)")
    parser.add_argument("--save", action="store_true", help="Save raw JSON reports to desk/deepscan/")
    args = parser.parse_args()
    
    symbols = [s.strip().upper() for s in args.sym.split(",") if s.strip()]
    
    for sym in symbols:
        report = fetch_asset_all_tabs(sym)
        print_telemetry_report(report)
        
        if args.save:
            ts = report["timestamp_ts"]
            out_file = DEEPSCAN_DIR / f"TELEMETRY-{sym}-{ts}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            print(f"  [SAVED TELEMETRY ARTIFACT]: {out_file}")

if __name__ == "__main__":
    main()
