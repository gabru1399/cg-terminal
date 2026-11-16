import json

with open(r"c:\Users\SIGMA\Documents\cg-terminal\desk\candidates_telemetry.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for sym, info in data.items():
    print(f"\n==================== {sym} ====================")
    if "error" in info:
        print(f"Error: {info['error']}")
        continue
    
    market = info.get("market", {})
    last_price = market.get("price")
    vwap = market.get("vwap", {})
    day_vwap = vwap.get("day", {}).get("val")
    day_sd1_pos = vwap.get("day", {}).get("sd1_pos")
    day_sd2_pos = vwap.get("day", {}).get("sd2_pos")
    day_sd1_neg = vwap.get("day", {}).get("sd1_neg")
    day_sd2_neg = vwap.get("day", {}).get("sd2_neg")
    
    auction = market.get("auction", {})
    day_vah = auction.get("day", {}).get("vah")
    day_poc = auction.get("day", {}).get("poc")
    day_val = auction.get("day", {}).get("val")
    sess_vah = auction.get("session", {}).get("vah")
    sess_poc = auction.get("session", {}).get("poc")
    sess_val = auction.get("session", {}).get("val")
    
    emas = market.get("emas", {})
    h4_ema13 = emas.get("h4", {}).get("ema13")
    h4_ema89 = emas.get("h4", {}).get("ema89")
    h4_ema233 = emas.get("h4", {}).get("ema233")
    
    liq = info.get("liq", {})
    levels = liq.get("levels", [])
    
    above_vol = sum(lvl.get("vol", 0) for lvl in levels if lvl.get("price", 0) > (last_price or 0))
    below_vol = sum(lvl.get("vol", 0) for lvl in levels if lvl.get("price", 0) < (last_price or 0))
    skew = below_vol / max(above_vol, 1.0)
    
    print(f"Price: {last_price}")
    print(f"Day Auction: VAH={day_vah}, POC={day_poc}, VAL={day_val}")
    print(f"Session Auction: VAH={sess_vah}, POC={sess_poc}, VAL={sess_val}")
    print(f"Day VWAP: {day_vwap} (SD+1: {day_sd1_pos}, SD+2: {day_sd2_pos}, SD-1: {day_sd1_neg}, SD-2: {day_sd2_neg})")
    print(f"H4 EMAs: 13={h4_ema13}, 89={h4_ema89}, 233={h4_ema233}")
    print(f"Liq Skew (Below/Above): {skew:.2f}:1 (Below: ${below_vol/1e3:.1f}k, Above: ${above_vol/1e3:.1f}k)")
