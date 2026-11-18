import urllib.request
import json
import sys

def get(path, timeout=3.0):
    try:
        url = "http://127.0.0.1:3000/api/cg" + path
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

symbols = ["BTC", "ETH", "BNB", "XAU"]
print("=" * 80, flush=True)
print("DEEP GRANULAR TELEMETRY EXTRACTION (ZERO ABSTRACTIONS)", flush=True)
print("=" * 80, flush=True)

for sym in symbols:
    m = get(f"/market?sym={sym}")
    vwap_data = m.get("vwap", {})
    auction = m.get("auction", {})
    ema = m.get("ema", {})
    rsi = m.get("rsi", {})
    price_info = m.get("price", {})
    
    print(f"\n>>> ASSET: {sym} <<<", flush=True)
    print(f"  Price: {price_info.get('last')} | 24h Chg: {price_info.get('chgDayPct')}%", flush=True)
    print(f"  Auction Session: VAL={auction.get('session', {}).get('val')}, POC={auction.get('session', {}).get('poc')}, VAH={auction.get('session', {}).get('vah')}", flush=True)
    print(f"  Auction Day:     VAL={auction.get('day', {}).get('val')}, POC={auction.get('day', {}).get('poc')}, VAH={auction.get('day', {}).get('vah')}", flush=True)
    print(f"  Auction Month:   VAL={auction.get('month', {}).get('val')}, POC={auction.get('month', {}).get('poc')}, VAH={auction.get('month', {}).get('vah')}", flush=True)
    print(f"  Day VWAP:        {vwap_data.get('vwap')} | +1sd={vwap_data.get('bands', {}).get('sd1')} | -1sd={vwap_data.get('bands', {}).get('sd1Neg')}", flush=True)
    print(f"  EMA Spine:", flush=True)
    for tf in ["m15", "h1", "h4", "d1"]:
        e = ema.get(tf, {})
        print(f"    {tf:4s} -> EMA13: {e.get('e13')}, EMA89: {e.get('e89')}, EMA233: {e.get('e233')}, RSI(14): {rsi.get(tf)}", flush=True)

    # Inspect bookwalls
    bw = get(f"/bookwalls?sym={sym}&interval=1m")
    if bw.get("ok"):
        depth = bw.get("depth", {})
        print(f"  Book Walls: Imbalance={depth.get('imbalance')}, Bid USD=${(depth.get('bidUsd') or 0)/1e6:.2f}M, Ask USD=${(depth.get('askUsd') or 0)/1e6:.2f}M", flush=True)
    else:
        print(f"  Book Walls: {bw.get('error') or bw.get('reason')}", flush=True)

print("\n" + "=" * 80, flush=True)
