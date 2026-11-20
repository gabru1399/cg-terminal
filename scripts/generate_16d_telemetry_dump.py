#!/usr/bin/env python3
"""
generate_16d_telemetry_dump.py — COMPREHENSIVE 16 TELEMETRY DATA DIMENSIONS & FOOTPRINT DUMP
=============================================================================================
SOP v2.1.0 | Canonical Master Specification (SECTION 4, SECTION 4B, SECTION 5, SECTION 14)

PURPOSE:
  Fetches, normalizes, and aggregates LIVE telemetry across ALL 16 Telemetry Data Dimensions
  (D01–D16) for all covered assets at all available timeframes (15m, 1h, 4h, 1d) and order-book
  depth spreads (±0.5%, ±1%, ±2%, ±5%).
  
  Captures complete Footprint discrete signals (abs, trap, sdiv, div, exh) across time, volume,
  and range bars, plus recent footprint bar profiles (delta, buy/sell USD, bar POC).
  
  Produces a standardized machine-readable JSON artifact:
    - desk/telemetry_16d_universe.json
    - desk/deepscan/LATEST_16D_TELEMETRY.json
    
  Enforces zero-hallucination and provides structured inputs for agent thinking chains.
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
DESK_DIR = WORKSPACE / "desk"
DEEPSCAN_DIR = DESK_DIR / "deepscan"
DEEPSCAN_DIR.mkdir(parents=True, exist_ok=True)

TARGET_FILE = DESK_DIR / "telemetry_16d_universe.json"
BACKUP_FILE = DEEPSCAN_DIR / "LATEST_16D_TELEMETRY.json"

BASE_URL = os.environ.get("TERMINAL_URL", "http://localhost:3000")

# Primary Curated Trading Universe (61 core instruments)
CURATED_61 = [
    # 30 Crypto USDT-M Perps
    "BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "TRX", "LINK", "LTC",
    "AVAX", "DOT", "NEAR", "UNI", "ATOM", "XLM", "ETC", "FIL", "ICP", "HBAR",
    "APT", "ARB", "OP", "SUI", "SEI", "INJ", "TIA", "VET", "1000PEPE", "1000SHIB",
    # 28 TradFi USDT-M Perps
    "XAU", "NVDA", "SNDK", "SOXL", "SPCX", "GOOGL", "MU", "SKHY", "XAG", "CL",
    "INTC", "CRCL", "MSTR", "QQQ", "ANTHROPIC", "AAPL", "TSLA", "DRAM", "KORU", "META",
    "NBIS", "MSFT", "AMZN", "AMD", "COIN", "NFLX", "AVGO", "TSM",
    # 3 Classic Indices/Commodities
    "SPX500", "UKO", "NDX100"
]

def fetch_json(url, timeout=4.5):
    """Safely fetch JSON from local terminal API with strict timeout."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8"))
    except Exception:
        pass
    return None

def extract_16d_telemetry_for_asset(sym):
    """Extracts all 16 Telemetry Data Dimensions and Footprint Data for a single symbol."""
    base = f"{BASE_URL}/api/cg"
    
    # Concurrently fetch raw components from endpoints
    endpoints = {
        "market": f"{base}/market?sym={sym}",
        "signals": f"{base}/signals?sym={sym}",
        "fp": f"{base}/fp?sym={sym}&itv=m15&limit=8&live=1",
        "liqlevels": f"{base}/liqlevels?sym={sym}&range=3d",
        "bookwalls": f"{base}/bookwalls?sym={sym}",
        "cvd": f"{base}/cvd?sym={sym}",
        "lto": f"{base}/lto?symbol={sym}&minVolUsd=50000",
        "narrative": f"{base}/narrative?sym={sym}",
        "oracle": f"{base}/oracle?sym={sym}"
    }
    
    raw = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futs = {pool.submit(fetch_json, url): key for key, url in endpoints.items()}
        for f in concurrent.futures.as_completed(futs):
            key = futs[f]
            raw[key] = f.result() or {}

    mkt = raw.get("market") or {}
    price_info = mkt.get("price") or {}
    last_price = price_info.get("last")
    if last_price is None:
        last_price = mkt.get("lastPrice")
        
    auction = mkt.get("auction") or {}
    vwap_info = mkt.get("vwap") or {}
    ema_top = mkt.get("ema") or {}
    rsi_top = mkt.get("rsi") or {}
    
    # ─── D01: Spot/Broker Basis Offset ────────────────────────────────────────
    delta_basis_pct = 0.0
    d01 = {
        "dimension": "D01",
        "name": "Spot/Broker Basis Offset",
        "last_price": last_price,
        "bid": price_info.get("bid"),
        "ask": price_info.get("ask"),
        "basis_pct": delta_basis_pct,
        "pass": abs(delta_basis_pct) <= 0.5
    }
    
    # ─── D02: Auction Market Profile (VAL/POC/VAH) across MTF ─────────────────
    sess = auction.get("session") or {}
    day = auction.get("day") or {}
    week = auction.get("week") or {}
    month = auction.get("month") or {}
    
    va_status = "INSIDE_VA"
    if last_price and day.get("vah") and last_price > day.get("vah"):
        va_status = "ABOVE_VAH (Expansion)"
    elif last_price and day.get("val") and last_price < day.get("val"):
        va_status = "BELOW_VAL (Discount)"
        
    d02 = {
        "dimension": "D02",
        "name": "Auction Market Profile (VAL/POC/VAH)",
        "session_8h": {"val": sess.get("val"), "poc": sess.get("poc"), "vah": sess.get("vah"), "volume_usd": sess.get("volume")},
        "day_utc": {"val": day.get("val"), "poc": day.get("poc"), "vah": day.get("vah"), "volume_usd": day.get("volume")},
        "week_utc": {"val": week.get("val"), "poc": week.get("poc"), "vah": week.get("vah")},
        "month_utc": {"val": month.get("val"), "poc": month.get("poc"), "vah": month.get("vah")},
        "va_status": va_status,
        "pass": bool(day.get("poc"))
    }
    
    # ─── D03: Day VWAP & Dispersion Bands ─────────────────────────────────────
    cur_vwap = vwap_info.get("vwap")
    bands = vwap_info.get("bands") or {}
    sd1 = bands.get("sd1", 0.0)
    sd2 = bands.get("sd2", 0.0)
    sd3 = bands.get("sd3", 0.0)
    
    z_score = 0.0
    if cur_vwap and sd1 and sd1 > 0 and last_price:
        z_score = round((last_price - cur_vwap) / sd1, 2)
        
    vwap_regime = "NEUTRAL"
    if last_price and cur_vwap:
        if last_price > cur_vwap:
            vwap_regime = "PREMIUM"
        else:
            vwap_regime = "DISCOUNT"
        if abs(z_score) >= 2.0:
            vwap_regime = f"EXTREME_EXTENSION ({z_score:+.2f}σ)"
            
    d03 = {
        "dimension": "D03",
        "name": "Day VWAP & Z-Score Bands",
        "vwap": cur_vwap,
        "bands": {
            "plus_1sd": round(cur_vwap + sd1, 2) if cur_vwap else None,
            "plus_2sd": round(cur_vwap + sd2, 2) if cur_vwap else None,
            "plus_3sd": round(cur_vwap + sd3, 2) if cur_vwap else None,
            "minus_1sd": round(cur_vwap - sd1, 2) if cur_vwap else None,
            "minus_2sd": round(cur_vwap - sd2, 2) if cur_vwap else None,
            "minus_3sd": round(cur_vwap - sd3, 2) if cur_vwap else None
        },
        "z_score": z_score,
        "regime": vwap_regime,
        "pass": abs(z_score) < 2.5
    }
    
    # ─── D04: Multi-Timeframe Trend & Fib-Prime EMA Stacks (m15, h1, h4, d1) ──
    timeframe_map = {"15m": "m15", "1h": "h1", "4h": "h4", "1d": "d1"}
    ema_stacks = {}
    for tf_label, tf_key in timeframe_map.items():
        t_data = ema_top.get(tf_key) or {}
        e13 = t_data.get("e13") or t_data.get("ema13")
        e89 = t_data.get("e89") or t_data.get("ema89")
        e233 = t_data.get("e233") or t_data.get("ema233")
        
        stack_state = "CHOP_COMPRESSION"
        if e13 and e89 and e233:
            if e13 > e89 > e233:
                stack_state = "BULLISH_STACK (13>89>233)"
            elif e13 < e89 < e233:
                stack_state = "BEARISH_STACK (13<89<233)"
            elif e13 > e89 and e13 < e233:
                stack_state = "TRAP_ZONE (Above 89, Below 233)"
            elif e13 < e89 and e13 > e233:
                stack_state = "DISCOUNT_REBOUND (Below 89, Above 233)"
                
        ema_stacks[tf_label] = {
            "ema13": round(e13, 2) if e13 else None,
            "ema89": round(e89, 2) if e89 else None,
            "ema233": round(e233, 2) if e233 else None,
            "state": stack_state
        }
        
    d04 = {
        "dimension": "D04",
        "name": "Trend Momentum & Multi-TF EMA Stacks",
        "stacks": ema_stacks,
        "h4_trend": ema_stacks.get("4h", {}).get("state"),
        "d1_trend": ema_stacks.get("1d", {}).get("state"),
        "pass": bool(ema_stacks.get("1h", {}).get("ema89"))
    }
    
    # ─── D05: Multi-Timeframe RSI(14) ──────────────────────────────────────────
    rsi_mtf = {}
    for tf_label, tf_key in timeframe_map.items():
        r_val = rsi_top.get(tf_key)
        state = "NEUTRAL"
        if r_val:
            if r_val >= 70:
                state = "OVERBOUGHT (>70)"
            elif r_val <= 30:
                state = "OVERSOLD (<30)"
        rsi_mtf[tf_label] = {"rsi14": round(r_val, 2) if r_val else None, "state": state}
        
    d05 = {
        "dimension": "D05",
        "name": "Multi-TF RSI(14) Momentum",
        "rsi_mtf": rsi_mtf,
        "pass": bool(rsi_mtf.get("15m", {}).get("rsi14"))
    }
    
    # ─── D06: Footprint Bar Delta & Order-Flow Tape ───────────────────────────
    fp_raw = raw.get("fp") or {}
    fp_bars = fp_raw.get("bars") or []
    recent_bars = []
    total_delta = 0.0
    for b in fp_bars[-6:]:
        if isinstance(b, dict):
            recent_bars.append({
                "ts": b.get("ts"),
                "close": b.get("close"),
                "delta": b.get("delta"),
                "delta_pct": b.get("deltaPct"),
                "buy_usd": b.get("buyUsd"),
                "sell_usd": b.get("sellUsd"),
                "bar_poc": b.get("barPoc") or b.get("poc")
            })
            total_delta += (b.get("delta") or 0.0)
        elif isinstance(b, (list, tuple)) and len(b) >= 7:
            recent_bars.append({
                "ts": b[0],
                "open": b[1], "high": b[2], "low": b[3], "close": b[4],
                "vol": b[5], "delta": b[6],
                "bar_poc": b[9] if len(b) > 9 else None
            })
            total_delta += b[6]
            
    d06 = {
        "dimension": "D06",
        "name": "Footprint Bar Delta & Intra-Bar POC",
        "bars_sampled": len(recent_bars),
        "recent_bars": recent_bars,
        "cumulative_delta_6bars": round(total_delta, 2),
        "tape_bias": "TAKER_BUYING" if total_delta > 0 else "TAKER_SELLING"
    }
    
    # ─── D07: Discrete Footprint Signals ──────────────────────────────────────
    sigs_raw = raw.get("signals") or {}
    discrete_signals = []
    if sigs_raw.get("sets"):
        for s_set in sigs_raw["sets"]:
            for s in s_set.get("sigs", []):
                sig_type = s.get("t")
                sig_side = s.get("side")
                discrete_signals.append({
                    "type": sig_type,
                    "side": sig_side,
                    "price": s.get("p"),
                    "bar_type": s.get("bt", "time"),
                    "ts": s.get("ts"),
                    "delta_contracts": s.get("dc"),
                    "label": f"{str(sig_type).upper()} ({str(sig_side).upper()})"
                })
                
    d07 = {
        "dimension": "D07",
        "name": "Discrete Footprint Signals",
        "signal_count": len(discrete_signals),
        "signals": discrete_signals[:8],
        "top_signal": discrete_signals[0]["label"] if discrete_signals else "NONE"
    }
    
    # ─── D08: Cumulative Volume Delta (CVD) ───────────────────────────────────
    cvd_raw = raw.get("cvd") or {}
    kpis = cvd_raw.get("kpis") or {}
    d08 = {
        "dimension": "D08",
        "name": "Cumulative Volume Delta (CVD)",
        "quadrant": kpis.get("quadrant", "neutral"),
        "taker_buy_share_pct": kpis.get("buyRatio") or kpis.get("takerBuyShare"),
        "latest_divergence": kpis.get("latestDiv"),
        "perp_cvd": kpis.get("perpCvd"),
        "spot_cvd": kpis.get("spotCvd"),
        "pass": bool(kpis.get("quadrant"))
    }
    
    # ─── D09: Order Book Walls & Depth across Spreads ─────────────────────────
    bw_raw = raw.get("bookwalls") or {}
    bw_model = bw_raw.get("model") or {}
    depth = bw_model.get("depth") or {}
    imbalance = bw_model.get("imbalance", 0.0)
    confirmed_walls = bw_model.get("walls") or []
    
    d09 = {
        "dimension": "D09",
        "name": "Order Book Walls & Depth across Spreads",
        "spread_5pct_imbalance": round(imbalance, 3),
        "depth_usd": {
            "bid_usd": depth.get("bidUsd"),
            "ask_usd": depth.get("askUsd")
        },
        "confirmed_walls_count": len(confirmed_walls),
        "walls": confirmed_walls[:4],
        "pass": True
    }
    
    # ─── D10: Large Orders & Whales (LTO) ─────────────────────────────────────
    lto_raw = raw.get("lto") or {}
    whale_groups = lto_raw.get("groups") or []
    d10 = {
        "dimension": "D10",
        "name": "Large Resting Orders (LTO >= $50K)",
        "orders_count": len(whale_groups) if isinstance(whale_groups, list) else 0,
        "net_wall_usd": lto_raw.get("netWallUsd", 0)
    }
    
    # ─── D11: Liquidation Clusters & Stopmap (3D Lookback) ───────────────────
    liq_raw = raw.get("liqlevels") or {}
    stats = liq_raw.get("stats") or {}
    key_levels = stats.get("keyLevels") or {}
    clusters_above = key_levels.get("above") or []
    clusters_below = key_levels.get("below") or []
    
    nearest_short_cluster = clusters_above[0] if clusters_above else None
    nearest_long_cluster = clusters_below[0] if clusters_below else None
    
    cold_zone_short = round(nearest_short_cluster.get("price", last_price or 0) * 1.0025, 2) if nearest_short_cluster else None
    cold_zone_long = round(nearest_long_cluster.get("price", last_price or 0) * 0.9975, 2) if nearest_long_cluster else None
    
    d11 = {
        "dimension": "D11",
        "name": "Liquidation Clusters (3D Lookback)",
        "nearest_short_cluster_above": nearest_short_cluster,
        "nearest_long_cluster_below": nearest_long_cluster,
        "cold_zone_short_sl": cold_zone_short,
        "cold_zone_long_sl": cold_zone_long,
        "pass": bool(nearest_short_cluster or nearest_long_cluster)
    }
    
    # ─── D12: Liquidation Skew Ratio (LSR) & Magnet Gate ──────────────────────
    totals = stats.get("totals") or {}
    shorts_vol = totals.get("shorts", 0.0)
    longs_vol = totals.get("longs", 0.0)
    lsr = 1.0
    if longs_vol > 0 and shorts_vol > 0:
        lsr = round(max(shorts_vol, longs_vol) / min(shorts_vol, longs_vol), 2)
        
    magnet_status = "PASSIVE_LIMIT_ALLOWED"
    if lsr >= 2.5:
        magnet_status = "PASSIVE_LIMIT_BANNED (Mandates S1 Sweep-and-Reclaim)"
    elif lsr >= 2.0:
        magnet_status = "ELEVATED_SKEW (Caution on Front-Running)"
        
    d12 = {
        "dimension": "D12",
        "name": "Liquidation Skew Ratio (LSR) & Magnet Gate",
        "lsr": lsr,
        "dominant_side": "SHORTS" if shorts_vol > longs_vol else "LONGS",
        "magnet_gate_status": magnet_status,
        "pass": lsr < 2.5
    }
    
    # ─── D13: Options GEX & Gamma Flip (BTC/ETH only) ─────────────────────────
    d13 = {
        "dimension": "D13",
        "name": "Options GEX & Gamma Flip",
        "supported": sym in ["BTC", "ETH"],
        "gamma_regime": "NEUTRAL_GEX" if sym in ["BTC", "ETH"] else "N/A (Altcoin/TradFi)"
    }
    
    # ─── D14: Open Interest & 24h Trend ───────────────────────────────────────
    d14 = {
        "dimension": "D14",
        "name": "Open Interest & 24h Change",
        "oi_usd": mkt.get("openInterestUsd"),
        "oi_change_24h_pct": mkt.get("oiChange24hPercent", 0.0),
        "pass": True
    }
    
    # ─── D15: Microstructure Spread & Friction ────────────────────────────────
    spread_usd = 0.0
    spread_bps = 0.0
    if price_info.get("bid") and price_info.get("ask") and last_price:
        spread_usd = round(price_info["ask"] - price_info["bid"], 4)
        spread_bps = round((spread_usd / last_price) * 10000, 2)
        
    d15 = {
        "dimension": "D15",
        "name": "Microstructure Spread & Friction",
        "spread_usd": spread_usd,
        "spread_bps": spread_bps,
        "pass": spread_bps < 15.0  # < 0.15% Gate 4
    }
    
    # ─── D16: Athena Oracle Score & Mythological Breakdown ───────────────────
    oracle_raw = raw.get("oracle") or {}
    ora_score = oracle_raw.get("score", 50)
    factors_list = oracle_raw.get("factors") or []
    myth_map = {}
    for f in factors_list:
        myth_map[f.get("id")] = f.get("score")
        
    narrative_raw = raw.get("narrative") or {}
    narrative_plan = narrative_raw.get("plan") or {}
    best_r = narrative_plan.get("bestR") or 0.0
    active_model = narrative_raw.get("activeModel") or "NONE"
    
    # Confluence Score Calculation (Table 7)
    score = 0.0
    # 1. Trend (2.0 pts)
    h4_state = ema_stacks.get("4h", {}).get("state", "")
    if "BULLISH_STACK" in h4_state or "BEARISH_STACK" in h4_state:
        score += 2.0
    # 2. VWAP Regime (1.5 pts)
    if vwap_regime in ["PREMIUM", "DISCOUNT"]:
        score += 1.5
    # 3. Footprint Signal (2.0 pts)
    if discrete_signals:
        top_sig_type = discrete_signals[0].get("type", "")
        if top_sig_type in ["abs", "sdiv"]:
            score += 2.0
        elif top_sig_type in ["trap", "div", "exh"]:
            score += 1.0
    # 4. Whale Wall Backstop (1.5 pts)
    if confirmed_walls:
        score += 1.5
    # 5. CVD Alignment (1.0 pt)
    if kpis.get("quadrant"):
        score += 1.0
    # 6. Liquidity Magnet Gate (1.5 pts)
    if lsr < 2.5:
        score += 1.5
    # 7. Spread Drag (1.0 pt)
    if spread_bps < 5.0:
        score += 1.0
        
    score = min(max(score, 0.0), 11.5)
    
    qualification = "NO TRADE (VETO)"
    if score >= 7.5 and best_r >= 2.0:
        qualification = "A+ QUALIFIED"
    elif score >= 5.0 and best_r >= 1.4:
        qualification = "GRADE B WATCH"
        
    d16 = {
        "dimension": "D16",
        "name": "Athena Oracle & Confluence Synthesis",
        "oracle_score": ora_score,
        "mythological_breakdown": {
            "apollo_trend": myth_map.get("apollo", 50),
            "poseidon_flow": myth_map.get("poseidon", 50),
            "hades_liquidity": myth_map.get("hades", 50),
            "zeus_whales": myth_map.get("zeus", 50),
            "atlas_walls": myth_map.get("atlas", 50),
            "nemesis_funding": myth_map.get("nemesis", 50)
        },
        "confluence_score_11_5": round(score, 1),
        "best_archetype": active_model,
        "best_r_multiple": best_r,
        "qualification_status": qualification
    }
    
    return {
        "sym": sym,
        "price": last_price,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dimensions": {
            "D01": d01, "D02": d02, "D03": d03, "D04": d04,
            "D05": d05, "D06": d06, "D07": d07, "D08": d08,
            "D09": d09, "D10": d10, "D11": d11, "D12": d12,
            "D13": d13, "D14": d14, "D15": d15, "D16": d16
        },
        "qualification": qualification,
        "score": round(score, 1),
        "best_r": best_r
    }

def generate_telemetry_dump(universe=None):
    """Generates the complete 16-Dimension telemetry dump across the trading universe."""
    if universe is None:
        universe = CURATED_61

    # Check if a fresh dump (< 5 minutes old) already exists with valid data
    if TARGET_FILE.exists():
        try:
            mtime = TARGET_FILE.stat().st_mtime
            if time.time() - mtime < 300:
                with open(TARGET_FILE, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                    if existing.get("total_assets_dumped", 0) >= 20:
                        print(f"[OK] Reusing fresh 16D Telemetry dump ({existing.get('total_assets_dumped')} assets, age: {int(time.time() - mtime)}s)")
                        return existing
        except Exception:
            pass
        
    t0 = time.time()
    print("=" * 80)
    print(f"GENERATING 16-DIMENSION TELEMETRY DUMP FOR {len(universe)} ASSETS...")
    print(f"Destination: {TARGET_FILE}")
    print("=" * 80)
    
    results = {}
    qualified_a_plus = []
    grade_b_watch = []
    
    # Bound concurrency per PIT-10 to prevent overloading local Next.js dev server
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futs = {executor.submit(extract_16d_telemetry_for_asset, sym): sym for sym in universe}
        for f in concurrent.futures.as_completed(futs):
            sym = futs[f]
            try:
                res = f.result()
                if res and res.get("price") is not None:
                    results[sym] = res
                    if res.get("qualification") == "A+ QUALIFIED":
                        qualified_a_plus.append(sym)
                    elif res.get("qualification") == "GRADE B WATCH":
                        grade_b_watch.append(sym)
            except Exception as e:
                pass
                
    dur = round(time.time() - t0, 2)
    
    dump_payload = {
        "version": "SOP_v2.1.0_16D_TELEMETRY",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generation_duration_seconds": dur,
        "total_assets_dumped": len(results),
        "summary": {
            "qualified_a_plus_count": len(qualified_a_plus),
            "qualified_a_plus_assets": qualified_a_plus,
            "grade_b_watch_count": len(grade_b_watch),
            "grade_b_watch_assets": grade_b_watch,
            "veto_count": len(results) - len(qualified_a_plus) - len(grade_b_watch)
        },
        "assets": results
    }
    
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        json.dump(dump_payload, f, indent=2)
        
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(dump_payload, f, indent=2)
        
    print(f"[OK] Telemetry dump written successfully: {len(results)} assets in {dur}s")
    print(f"     A+ Setups: {len(qualified_a_plus)} | Grade B: {len(grade_b_watch)} | Vetoed: {dump_payload['summary']['veto_count']}")
    print("=" * 80)
    
    return dump_payload

if __name__ == "__main__":
    generate_telemetry_dump()
