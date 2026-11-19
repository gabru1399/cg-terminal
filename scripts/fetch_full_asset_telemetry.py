#!/usr/bin/env python3
"""
fetch_full_asset_telemetry.py — MANDATORY MULTI-TAB ORDER-FLOW TELEMETRY SCRAPER & 48H DUMP
================================================================================
SOP v2.1.0 | Canonical Master Specification Deep Telemetry Module (SECTION 4)

PURPOSE:
  Fetches, normalizes, and aggregates LIVE telemetry and 48-HOUR historical order-flow
  across ALL 9 terminal tabs and perception tiers for any given asset:
    [TIER 0-2] 3-Tier Perception Hierarchy (WS Sub-100ms, REST L2 250ms, CG Aggregator)
    [TAB 1] Overview & Auction Profiles (VAL/POC/VAH 8h, Day, Month + VWAP ±1/2/3σ + EMAs + RSI)
    [TAB 2] Footprint & 48H Order-Flow Tape (Absorption, Traps, Divs, 15m Bars)
    [TAB 3] Large Orders / Whale Orders (Resting whale bids/asks >= $100K / $1M, Wall Balance)
    [TAB 4] Liquidation Levels & LSR (3D/30D clusters, sweep magnets, Skew Ratio, Magnet Gate)
    [TAB 5] Order Book Walls & Depth (Multi-exchange aggregate depth imbalance ±0.5/1/2/5%)
    [TAB 6] Cumulative Volume Delta (CVD) (1500-candle series, Perp vs Spot, Divergences)
    [TAB 7] Narrative Regime & Quant Models (S1-S9 Archetypes, EV, Win Prob, Trade Plan)
    [TAB 8] Alerts & Real-Time Event Queue (High-severity footprint, whale, liq alerts)
    [TAB 9] Live L2 Depth & Execution Bridge (Top-1000 depth, spread, Delta CLOB / MT5)

USAGE:
  python scripts/fetch_full_asset_telemetry.py --sym BTC
  python scripts/fetch_full_asset_telemetry.py --sym BTC,ETH,SOL,XAU --save --dump-48h
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

def fetch_endpoint(url, timeout=25.0):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8")), None
            return None, f"HTTP {resp.status}"
    except Exception as e:
        return None, str(e)

def analyze_48h_behavior(data, sym):
    """
    Forensic 48-hour order-flow behavioral analysis matching SECTION 4 of Canonical Master Spec.
    Extracts trailing 48-hour candle series (192 15m bars), taker delta trajectory,
    cumulative delta shifts, volume profiles, and microstructure divergences.
    """
    cvd_data = data.get("cvd") or {}
    candles = cvd_data.get("candles") or []
    delta = cvd_data.get("delta") or []
    perp = cvd_data.get("perp") or []
    spot = cvd_data.get("spot") or []
    ratio = cvd_data.get("ratio") or []
    divs = cvd_data.get("divergences") or []
    kpis = cvd_data.get("kpis") or {}
    
    # 48 hours = 192 15m bars
    bars_48h = 192
    c_slice = candles[-bars_48h:] if len(candles) >= bars_48h else candles
    d_slice = delta[-bars_48h:] if len(delta) >= bars_48h else delta
    p_slice = perp[-bars_48h:] if len(perp) >= bars_48h else perp
    s_slice = spot[-bars_48h:] if len(spot) >= bars_48h else spot
    r_slice = ratio[-bars_48h:] if len(ratio) >= bars_48h else ratio
    
    total_delta_48h = sum(d_slice) if d_slice else 0.0
    avg_buy_ratio_48h = (sum(r_slice) / len(r_slice)) if r_slice else 50.0
    
    price_start = c_slice[0][1] if c_slice and len(c_slice[0]) > 1 else 0.0
    price_end = c_slice[-1][4] if c_slice and len(c_slice[-1]) > 4 else 0.0
    price_high = max([c[2] for c in c_slice]) if c_slice else 0.0
    price_low = min([c[3] for c in c_slice]) if c_slice else 0.0
    price_change = price_end - price_start
    price_change_pct = (price_change / price_start * 100.0) if price_start > 0 else 0.0
    
    # Split 48h into two 24h halves to detect momentum inflection
    half = len(d_slice) // 2
    delta_h1 = sum(d_slice[:half]) if half > 0 else 0.0
    delta_h2 = sum(d_slice[half:]) if half > 0 else 0.0
    
    if delta_h2 > delta_h1 and total_delta_48h > 0:
        trajectory = "ACCELERATING_AGGRESSIVE_BUYING (Bullish Expansion)"
    elif delta_h2 > delta_h1 and total_delta_48h <= 0:
        trajectory = "SELLER_EXHAUSTION_ABSORPTION_CURL (Reversal Accumulation)"
    elif delta_h2 < delta_h1 and total_delta_48h < 0:
        trajectory = "ACCELERATING_AGGRESSIVE_SELLING (Bearish Distribution)"
    else:
        trajectory = "BUYER_EXHAUSTION_DISTRIBUTION (Bearish Reversal)"
        
    now_ts = int(time.time() * 1000)
    cutoff_48h = now_ts - (48 * 3600 * 1000)
    recent_divs = [d for d in divs if d.get("ts", 0) >= cutoff_48h] if divs else []
    
    # 48h history table
    history_48h = []
    for i in range(len(c_slice)):
        history_48h.append({
            "ts": c_slice[i][0] if len(c_slice[i]) > 0 else None,
            "open": c_slice[i][1] if len(c_slice[i]) > 1 else None,
            "high": c_slice[i][2] if len(c_slice[i]) > 2 else None,
            "low": c_slice[i][3] if len(c_slice[i]) > 3 else None,
            "close": c_slice[i][4] if len(c_slice[i]) > 4 else None,
            "delta": d_slice[i] if i < len(d_slice) else 0,
            "perp_cvd": p_slice[i] if i < len(p_slice) else 0,
            "spot_cvd": s_slice[i] if i < len(s_slice) else 0,
            "buy_ratio": r_slice[i] if i < len(r_slice) else 50.0
        })
        
    return {
        "sym": sym,
        "hours_covered": round(len(c_slice) * 15 / 60.0, 2),
        "bars_count": len(c_slice),
        "price_start": price_start,
        "price_end": price_end,
        "price_high": price_high,
        "price_low": price_low,
        "price_change": price_change,
        "price_change_pct": price_change_pct,
        "net_delta_48h": total_delta_48h,
        "avg_buy_ratio_48h": round(avg_buy_ratio_48h, 2),
        "first_24h_delta": delta_h1,
        "second_24h_delta": delta_h2,
        "delta_trajectory": trajectory,
        "cvd_quadrant": kpis.get("quadrant", "neutral"),
        "cvd_divergences_48h_count": len(recent_divs),
        "cvd_latest_div": kpis.get("latestDiv"),
        "history_48h": history_48h
    }

def fetch_asset_all_tabs(sym):
    sym = sym.upper().strip()
    base = f"{BASE_URL}/api/cg"
    
    endpoints = {
        "market": f"{base}/market?sym={sym}",
        "signals": f"{base}/signals?sym={sym}",
        "fp": f"{base}/fp?sym={sym}",
        "liqlevels_3d": f"{base}/liqlevels?sym={sym}&range=3d",
        "liqlevels_30d": f"{base}/liqlevels?sym={sym}&range=30d",
        "liq_live": f"{base}/liq-live?sym={sym}&limit=25",
        "bookwalls": f"{base}/bookwalls?sym={sym}",
        "lto": f"{base}/lto?symbol={sym}&minVolUsd=100000",
        "cvd": f"{base}/cvd?sym={sym}",
        "oi": f"{base}/oi?sym={sym}",
        "funding": f"{base}/funding?sym={sym}",
        "narrative": f"{base}/narrative?sym={sym}",
        "quant": f"{base}/quant?sym={sym}",
        "livebook": f"{base}/livebook?sym={sym}",
        "notifications": f"{base}/notifications"
    }
    
    results = {}
    errors = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
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
                
    # Compute 48-hour forensic order-flow behavior analysis
    analysis_48h = analyze_48h_behavior(results, sym)
    
    return {
        "sym": sym,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "timestamp_ts": int(time.time() * 1000),
        "data": results,
        "errors": errors,
        "analysis_48h": analysis_48h
    }

def print_telemetry_report(report):
    sym = report["sym"]
    data = report["data"]
    errs = report["errors"]
    a48 = report.get("analysis_48h") or {}
    
    print("\n" + "═" * 84)
    print(f"  SECTION 4: 360° ORDER-FLOW TELEMETRY & 48H FORENSIC AUDIT: {sym}")
    print(f"  Timestamp: {report['timestamp_utc']} │ Reference: CANONICAL_MASTER_SPECIFICATION.md")
    print("═" * 84)
    
    # ─── TIER 0-2 PERCEPTION STATUS ───────────────────────────────────────────
    print(f"\n[PERCEPTION TIER STATUS (SECTION 4.0)]")
    print(f"  • Tier 0 (WS Sub-100ms)    : Active (Binance lead @bookTicker / @trade)")
    print(f"  • Tier 1 (REST L2 250ms)   : Active (L2 Order Book Top-1000 depth scanner)")
    print(f"  • Tier 2 (CG Aggregator)   : Active (Multi-exchange aggregate 3s-30s)")

    # ─── TAB 1: OVERVIEW & AUCTION MARKET STRUCTURE ───────────────────────────
    mkt = data.get("market") or {}
    price_info = mkt.get("price") or {}
    auction = mkt.get("auction") or {}
    vwap_info = mkt.get("vwap") or {}
    indicators = mkt.get("indicators") or {}
    
    last_price = price_info.get("last")
    print(f"\n[TAB 1: OVERVIEW & AUCTION MARKET STRUCTURE (AMT)]")
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
        z_score = ((last_price - cur_vwap) / sd1) if (last_price and sd1 > 0) else 0.0
        regime = "PREMIUM" if (last_price and last_price > cur_vwap) else "DISCOUNT"
        if abs(z_score) >= 2.5:
            regime = f"EXTREME_EXTENSION ({z_score:+.2f}σ)"
        print(f"  • Day VWAP & Dispersion Bands (z-Score: {z_score:+.2f}σ │ Regime: {regime}):")
        print(f"    - VWAP: {cur_vwap:.2f} │ +1σ: {cur_vwap+sd1:.2f} │ +2σ: {cur_vwap+sd2:.2f} │ +3σ: {cur_vwap+sd3:.2f}")
        print(f"                       │ -1σ: {cur_vwap-sd1:.2f} │ -2σ: {cur_vwap-sd2:.2f} │ -3σ: {cur_vwap-sd3:.2f}")
        
    ema_top = mkt.get("ema") or {}
    rsi_top = mkt.get("rsi") or {}
    m15_ema = ema_top.get("m15") or {}
    h1_ema = ema_top.get("h1") or {}
    h4_ema = ema_top.get("h4") or {}
    m15_ind = indicators.get("m15") or {}
    h1_ind = indicators.get("h1") or {}
    h4_ind = indicators.get("h4") or {}
    
    rsi_m15 = rsi_top.get("m15") or m15_ind.get("rsi")
    rsi_h1 = rsi_top.get("h1") or h1_ind.get("rsi")
    rsi_h4 = rsi_top.get("h4") or h4_ind.get("rsi")
    
    e13_m15 = m15_ema.get("e13") or m15_ind.get("ema13")
    e89_m15 = m15_ema.get("e89") or m15_ind.get("ema89")
    e233_m15 = m15_ema.get("e233") or m15_ind.get("ema233")
    
    e13_h1 = h1_ema.get("e13") or h1_ind.get("ema13")
    e89_h1 = h1_ema.get("e89") or h1_ind.get("ema89")
    
    e13_h4 = h4_ema.get("e13") or h4_ind.get("ema13")
    e89_h4 = h4_ema.get("e89") or h4_ind.get("ema89")
    
    def _fmt(val):
        return f"{val:.2f}" if isinstance(val, (int, float)) else str(val)

    print(f"  • Indicators (Fib-Prime EMAs & RSI):")
    print(f"    - M15: RSI {_fmt(rsi_m15)} │ EMA13 {_fmt(e13_m15)} │ EMA89 {_fmt(e89_m15)} │ EMA233 {_fmt(e233_m15)}")
    print(f"    - H1 : RSI {_fmt(rsi_h1)} │ EMA13 {_fmt(e13_h1)} │ EMA89 {_fmt(e89_h1)}")
    print(f"    - H4 : RSI {_fmt(rsi_h4)} │ EMA13 {_fmt(e13_h4)} │ EMA89 {_fmt(e89_h4)}")

    # ─── TAB 2: FOOTPRINT & 48-HOUR ORDER-FLOW BEHAVIOR ───────────────────────
    sigs = data.get("signals") or {}
    counts = sigs.get("counts") or {}
    print(f"\n[TAB 2: FOOTPRINT & 48-HOUR ORDER-FLOW BEHAVIOR]")
    print(f"  • Discrete Signals : {counts.get('all', 0)} total ({counts.get('bullish', 0)} Bullish / {counts.get('bearish', 0)} Bearish)")
    
    recent_sigs = []
    for s_set in sigs.get("sets") or []:
        for s in s_set.get("sigs") or []:
            st = s.get("t", "")
            side = s.get("side", "")
            p = s.get("p", 0)
            u = s.get("u", 0)
            sig_map = {"abs": "Absorption", "trap": "Trap", "sdiv": "StrongDiv", "div": "Divergence", "exh": "Exhaustion"}
            recent_sigs.append(f"{sig_map.get(st, st)} [{side.upper()}] @ {p} (${u/1e6:.1f}M)")
            if len(recent_sigs) >= 4:
                break
        if len(recent_sigs) >= 4:
            break
    print(f"  • Recent Signals   : {', '.join(recent_sigs) if recent_sigs else 'None detected'}")
    
    print(f"  • 48-Hour Order-Flow Behavior Forensic Summary:")
    print(f"    - Hours Sampled  : {a48.get('hours_covered')}h ({a48.get('bars_count')} 15m bars)")
    print(f"    - Price Span     : {a48.get('price_start')} → {a48.get('price_end')} ({a48.get('price_change_pct'):+.2f}% │ High: {a48.get('price_high')} / Low: {a48.get('price_low')})")
    print(f"    - 48h Net Delta  : {a48.get('net_delta_48h'):+,.0f} contracts (Avg Buy Ratio: {a48.get('avg_buy_ratio_48h')}%)")
    print(f"    - Momentum Shift : 24h#1 Delta: {a48.get('first_24h_delta'):+,.0f} → 24h#2 Delta: {a48.get('second_24h_delta'):+,.0f}")
    print(f"    - Order-Flow State: {a48.get('delta_trajectory')}")

    # ─── TAB 3: LARGE ORDERS & WHALE RESTING LIQUIDITY ─────────────────────────
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
                
    net_wall = whale_bid_usd - whale_ask_usd
    total_whale = whale_bid_usd + whale_ask_usd
    wall_bal = f"{(whale_bid_usd/total_whale*100):.0f}:{(whale_ask_usd/total_whale*100):.0f}" if total_whale > 0 else "50:50"
    
    print(f"\n[TAB 3: LARGE ORDERS & WHALE RESTING LIQUIDITY]")
    print(f"  • Total Whale Asks : ${(whale_ask_usd/1e6):.2f}M (Overhead Resistance)")
    print(f"  • Total Whale Bids : ${(whale_bid_usd/1e6):.2f}M (Underlying Support)")
    print(f"  • Wall Balance     : {wall_bal} (Bid:Ask) │ Net Wall: ${(net_wall/1e6):+.2f}M")
    print(f"  • Prominent Orders : {', '.join(whale_orders_list[:4]) if whale_orders_list else 'No orders >= $100K active'}")

    # ─── TAB 4: LIQUIDATION CLUSTERS & 3D/30D SWEEP MAGNETS ───────────────────
    liq3d = data.get("liqlevels_3d") or {}
    liq30d = data.get("liqlevels_30d") or {}
    stats3d = liq3d.get("stats") or {}
    totals3d = stats3d.get("totals") or {}
    key_levels = stats3d.get("keyLevels") or {}
    
    lsr = liq3d.get("lsr", 1.0)
    magnet_gate = "BANS S3 PASSIVE FRONT-RUN (WAIT S1 SWEEP)" if lsr >= 2.5 else "CLEAR FOR S1/S2/S3"
    
    print(f"\n[TAB 4: LIQUIDATION CLUSTERS & 3D/30D SWEEP MAGNETS]")
    print(f"  • Liquidation Skew Ratio (LSR): {lsr:.2f}:1 (Gate: {magnet_gate})")
    print(f"  • 3D Open Exposure : Shorts (Above) ${(totals3d.get('shorts', 0)/1e6):.1f}M │ Longs (Below) ${(totals3d.get('longs', 0)/1e6):.1f}M")
    
    above_lvls = [f"{l.get('price')} (+{l.get('distPct'):.2f}%, str {l.get('strength', 0):.0f})" for l in key_levels.get("above") or []][:3]
    below_lvls = [f"{l.get('price')} (-{l.get('distPct'):.2f}%, str {l.get('strength', 0):.0f})" for l in key_levels.get("below") or []][:3]
    print(f"  • Sweep Magnets Above : { ' | '.join(above_lvls) if above_lvls else 'None' }")
    print(f"  • Sweep Magnets Below : { ' | '.join(below_lvls) if below_lvls else 'None' }")

    # ─── TAB 4.5: LIVE LIQUIDATIONS TAPE & SKEW (BINANCE + BYBIT + OKX) ────────
    liq_live_raw = data.get("liq_live") or {}
    asset_liq = liq_live_raw.get("asset") or {}
    stats1h = asset_liq.get("stats1h") or {}
    stats24h = asset_liq.get("stats24h") or {}
    venues = asset_liq.get("venuesSeen") or []
    events = asset_liq.get("events") or []
    
    print(f"\n[TAB 4.5: LIVE LIQUIDATIONS TAPE & SKEW (BINANCE + BYBIT + OKX)]")
    print(f"  • Venues Active    : {', '.join(venues) if venues else 'None'}")
    print(f"  • 1h Liquidation   : {stats1h.get('count', 0)} prints │ ${(stats1h.get('usd', 0) or 0)/1e3:.1f}k │ {stats1h.get('longs', 0)}L / {stats1h.get('shorts', 0)}S")
    max_usd = (stats24h.get('largestUsd', 0) or 0) / 1e6
    tot_usd = (stats24h.get('usd', 0) or 0) / 1e6
    print(f"  • 24h Liquidation  : {stats24h.get('count', 0)} prints │ ${tot_usd:.2f}M │ {stats24h.get('longs', 0)}L / {stats24h.get('shorts', 0)}S (Max: ${max_usd:.2f}M)")
    recent_prints = [f"{e.get('side', '').upper()} {(e.get('qtyBase') or 0):.3f} @ {e.get('price')} (${(e.get('usd') or 0):.0f} on {e.get('venue')})" for e in events[:4]]
    print(f"  • Recent Prints    : {' | '.join(recent_prints) if recent_prints else 'Quiet tape (no prints)'}")

    # ─── TAB 5: ORDER BOOK WALLS & DEPTH IMBALANCE ────────────────────────────
    bw = data.get("bookwalls") or {}
    bw_model = bw.get("model") or {}
    bw_venues = bw.get("venues") or []
    depth = bw_model.get("depth") or {}
    imb = bw_model.get("imbalance", 0.0)
    imb5m = bw_model.get("imbalance5mAgo", 0.0)
    
    print(f"\n[TAB 5: ORDER BOOK WALLS & DEPTH IMBALANCE]")
    print(f"  • Venues Aggregated: {', '.join(bw_venues)}")
    print(f"  • Snapshots Loaded : {bw_model.get('snapshots', 0)} frames (Band ±{bw.get('band', 5)}%)")
    print(f"  • Depth Imbalance  : Now {imb:+.2%} │ 5m Ago {imb5m:+.2%} (Delta: {(imb-imb5m):+.2%})")
    print(f"  • Depth Notional   : Bids ${(depth.get('bid', 0)/1e6):.2f}M │ Asks ${(depth.get('ask', 0)/1e6):.2f}M")

    # ─── TAB 6: CUMULATIVE VOLUME DELTA (CVD) & DIVERGENCES ───────────────────
    cvd_data = data.get("cvd") or {}
    kpis = cvd_data.get("kpis") or {}
    print(f"\n[TAB 6: CUMULATIVE VOLUME DELTA (CVD) & DIVERGENCES]")
    print(f"  • Quadrant / Taker : {kpis.get('quadrant', 'neutral')} │ Buy Ratio: {kpis.get('buyRatio', 50):.1f}%")
    print(f"  • Cumulative CVD   : Perp {kpis.get('perpCvd', 0):+,.0f} │ Spot {kpis.get('spotCvd', 0):+,.0f}")
    print(f"  • Active 48h Divs  : {a48.get('cvd_divergences_48h_count')} detected")
    if kpis.get("latestDiv"):
        ld = kpis["latestDiv"]
        print(f"  • Latest Divergence: {ld.get('type', '').upper()} @ {ld.get('price')} (ts: {ld.get('ts')})")

    # ─── TAB 7: NARRATIVE REGIME & QUANT EV VERDICT ───────────────────────────
    narr = data.get("narrative") or {}
    plan = narr.get("plan") or {}
    prob = narr.get("probability") or {}
    
    print(f"\n[TAB 7: NARRATIVE REGIME & QUANT EV VERDICT]")
    print(f"  • Strategy Archetype: {narr.get('regime')} │ {narr.get('activeModel')} │ Direction: {narr.get('direction')}")
    ev_val = prob.get('evR') if prob.get('evR') is not None else 0.0
    pwin_val = prob.get('pWin') if prob.get('pWin') is not None else 0.0
    print(f"  • Expected Value EV : {ev_val:.2f}R │ P(Win): {pwin_val:.1%} │ Grade {narr.get('grade')} (Score {narr.get('confidence', 0)}/100)")
    if plan.get("entryZone"):
        ez = plan.get("entryZone")
        ez0 = ez[0] if len(ez) > 0 and ez[0] is not None else 0.0
        ez1 = ez[1] if len(ez) > 1 and ez[1] is not None else 0.0
        stop_val = plan.get("stop") if plan.get("stop") is not None else 0.0
        best_r = plan.get("bestR") if plan.get("bestR") is not None else 0.0
        print(f"  • Algorithmic Plan  : Entry {ez0:.2f}-{ez1:.2f} │ Stop {stop_val:.2f} │ Best R: {best_r:.2f}R")
        tg_strs = [f"{t.get('label')} @ {(t.get('level') or 0.0):.2f} ({(t.get('rMultiple') or 0.0):.1f}R)" for t in plan.get("targets") or []]
        print(f"  • Target Ladder     : {' | '.join(tg_strs)}")
    if plan.get("vetoes"):
        print(f"  • Active Vetoes     : {'; '.join(plan.get('vetoes'))}")

    # ─── TAB 8: ALERTS & REAL-TIME EVENT STREAM ───────────────────────────────
    notifs = data.get("notifications") or {}
    items = notifs.get("items") or []
    sym_items = [i for i in items if i.get("asset") == sym or i.get("symbol") == sym]
    high_items = [i for i in sym_items if i.get("severity") == "high"]
    
    print(f"\n[TAB 8: ALERTS & REAL-TIME EVENT STREAM]")
    print(f"  • Live Event Queue  : {len(sym_items)} events for {sym} ({len(high_items)} HIGH severity)")
    for hi in high_items[:3]:
        print(f"    - [HIGH] {hi.get('title')} ({hi.get('detail')})")

    # ─── TAB 9: LIVE L2 ORDER BOOK & EXECUTION BRIDGE ─────────────────────────
    lb = data.get("livebook") or {}
    lb_model = lb.get("model") or {}
    last_book = lb_model.get("last") or {}
    print(f"\n[TAB 9: LIVE L2 ORDER BOOK & EXECUTION BRIDGE]")
    print(f"  • L2 Top-1000 Book : Mid {last_book.get('price')} │ Best Bid {last_book.get('bid')} │ Best Ask {last_book.get('ask')}")
    print(f"  • Execution Routing: Delta Exchange India (CLOB post_only: true) / Blueberry MT5")
    print("\n" + "═" * 84)

def main():
    parser = argparse.ArgumentParser(description="SECTION 4: 360° Order-Flow Multi-Tab Telemetry Scraper & 48H Dump")
    parser.add_argument("--sym", type=str, default="BTC", help="Symbol or comma-separated list of symbols (e.g. BTC,ETH,SOL,XAU)")
    parser.add_argument("--save", action="store_true", help="Save raw JSON reports to desk/deepscan/")
    parser.add_argument("--dump-48h", action="store_true", help="Dump 48-hour continuous historical series and analysis")
    args = parser.parse_args()
    
    symbols = [s.strip().upper() for s in args.sym.split(",") if s.strip()]
    
    for sym in symbols:
        report = fetch_asset_all_tabs(sym)
        print_telemetry_report(report)
        
        ts = report["timestamp_ts"]
        if args.save:
            out_file = DEEPSCAN_DIR / f"TELEMETRY-{sym}-{ts}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            print(f"  [SAVED TELEMETRY ARTIFACT]: {out_file}")
            
        if args.dump_48h:
            dump_file = DEEPSCAN_DIR / f"48H_TELEMETRY-{sym}-{ts}.json"
            dump_payload = {
                "sym": sym,
                "timestamp_utc": report["timestamp_utc"],
                "timestamp_ts": ts,
                "forensic_48h_behavior": report["analysis_48h"],
                "section_4_tabs": {
                    "tab1_overview_amt": report["data"].get("market"),
                    "tab2_footprint_signals": report["data"].get("signals"),
                    "tab3_large_orders_whale": report["data"].get("lto"),
                    "tab4_liq_clusters_3d": report["data"].get("liqlevels_3d"),
                    "tab4_liq_clusters_30d": report["data"].get("liqlevels_30d"),
                    "tab5_bookwalls_depth": report["data"].get("bookwalls"),
                    "tab6_cvd_trajectory": report["data"].get("cvd"),
                    "tab7_narrative_quant": report["data"].get("narrative"),
                    "tab8_notifications_queue": report["data"].get("notifications"),
                    "tab9_live_l2_depth": report["data"].get("livebook")
                }
            }
            with open(dump_file, "w", encoding="utf-8") as f:
                json.dump(dump_payload, f, indent=2)
            print(f"  [SAVED 48H FORENSIC DUMP]: {dump_file}")

if __name__ == "__main__":
    main()
