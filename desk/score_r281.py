import json

with open("desk/crypto_sweep_r281.json", "r") as f:
    sweep = json.load(f)

print(f"Loaded {len(sweep)} assets from R281 sweep.")

# Let's inspect Table 7 scoring for top candidates: ETH, LINK, SUI, LTC, BTC, SOL
candidates = ["ETH", "LINK", "SUI", "LTC", "BTC", "SOL"]

for sym in candidates:
    d = sweep.get(sym, {})
    m = d.get("market", {})
    price = m.get("price", {}).get("last")
    ema = m.get("ema", {})
    m15_ema = ema.get("m15", {})
    h1_ema = ema.get("h1", {})
    h4_ema = ema.get("h4", {})
    d1_ema = ema.get("d1", {})
    
    # Trend alignment: H1/H4/D1 EMA13 < EMA89
    h1_bear = h1_ema.get("e13", 0) < h1_ema.get("e89", 0)
    h4_bear = h4_ema.get("e13", 0) < h4_ema.get("e89", 0)
    d1_bear = d1_ema.get("e13", 0) < d1_ema.get("e89", 0)
    trend_pts = 2.0 if (h1_bear and h4_bear and d1_bear) else (1.0 if (h1_bear and h4_bear) else 0.0)
    
    # Regime: Price < Day VAL, z < -1.0
    auc = m.get("auction", {})
    day = auc.get("day", {})
    val = day.get("val", 0)
    poc = day.get("poc", 0)
    vah = day.get("vah", 0)
    vwap = m.get("vwap", {})
    vwap_val = vwap.get("vwap", 0)
    sd1 = vwap.get("bands", {}).get("sd1", 1)
    z = (price - vwap_val) / sd1 if (price and vwap_val and sd1) else 0
    regime_pts = 1.5 if (price < val and z < -1.0) else 1.0
    
    # Footprint signal
    sig = d.get("signals", {})
    recent_sigs = sig.get("signals", [])
    footprint_pts = 1.5 if len(recent_sigs) > 0 else 1.0
    
    # Bookwalls
    bw = d.get("bookwalls", {})
    imb = bw.get("imbalance", 0)
    walls_pts = 1.0 if imb < 0.1 else 0.5
    
    # CVD
    cvd = d.get("cvd", {})
    taker_buy = cvd.get("takerBuyShare", 50)
    cvd_pts = 1.0 if taker_buy < 50 else 0.0
    
    # Liq magnet
    liq = d.get("liq", {})
    lsr = liq.get("lsr", 1.0)
    liq_pts = 1.0 if lsr < 2.0 else 0.5
    
    # Delta CLOB spread
    clob_pts = 1.0
    
    total_score = trend_pts + regime_pts + footprint_pts + walls_pts + cvd_pts + liq_pts + clob_pts
    print(f"[{sym:5s}] Price: {price} | Trend: {trend_pts} | Regime: {regime_pts} | FP: {footprint_pts} | Wall: {walls_pts} | CVD: {cvd_pts} | Liq: {liq_pts} | Score: {total_score:.1f} / 11.5 | Grade: {'A' if total_score>=7.0 else ('B' if total_score>=5.0 else 'VETO')}")
