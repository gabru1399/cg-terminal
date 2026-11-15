import json

with open(r"c:\Users\SIGMA\Documents\cg-terminal\desk\candidates_telemetry.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for sym in ["DOT", "SUI", "NEAR", "XRP", "FIL"]:
    info = data.get(sym, {})
    if "error" in info:
        continue
    
    market = info.get("market", {})
    last = market.get("price", {}).get("last")
    liq = info.get("liq", {})
    stats = liq.get("stats", {})
    totals = stats.get("totals", {})
    shorts = totals.get("shorts", 0) # above
    longs = totals.get("longs", 0)   # below
    
    auction = market.get("auction", {})
    day_vah = auction.get("day", {}).get("vah")
    day_poc = auction.get("day", {}).get("poc")
    day_val = auction.get("day", {}).get("val")
    sess_poc = auction.get("session", {}).get("poc")
    
    vwap = market.get("vwap", {})
    v_val = vwap.get("vwap")
    
    print(f"\n--- {sym} (Last: {last}) ---")
    print(f"Auction Day: VAH={day_vah}, POC={day_poc}, VAL={day_val} | Sess POC={sess_poc} | VWAP={v_val}")
    print(f"Liq Totals: Shorts Above=${shorts/1e6:.2f}M | Longs Below=${longs/1e6:.2f}M")
    if shorts > 0 and longs > 0:
        print(f"Long/Short Skew: {longs/shorts:.2f}:1 (Longs below vs Shorts above)")
        print(f"Short/Long Skew: {shorts/longs:.2f}:1 (Shorts above vs Longs below)")
    key_below = stats.get("keyLevels", {}).get("below", [])[:3]
    key_above = stats.get("keyLevels", {}).get("above", [])[:3]
    print("Top Key Above:", [(k.get('price'), f"${k.get('usd',0)/1e3:.0f}k") for k in key_above])
    print("Top Key Below:", [(k.get('price'), f"${k.get('usd',0)/1e3:.0f}k") for k in key_below])
