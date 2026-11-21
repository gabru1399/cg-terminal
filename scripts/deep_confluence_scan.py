import urllib.request
import json

symbols = ["BTC", "ETH", "SOL", "BNB", "XRP", "XAU"]
base_url = "http://127.0.0.1:3000"

print("================================================================================")
print("             DEEP MICROSTRUCTURE & HTF TREND CONFLUENCE SCANNER               ")
print("================================================================================")

for sym in symbols:
    print(f"\n>>> ASSET: {sym} <<<")
    # 1. Market & Trend
    try:
        m_req = urllib.request.urlopen(f"{base_url}/api/cg/market?sym={sym}")
        m_data = json.loads(m_req.read().decode())
        price = m_data.get("price") or m_data.get("close")
        vwap = m_data.get("vwap_day") or m_data.get("vwap")
        poc = m_data.get("poc_day") or m_data.get("poc")
        chg = m_data.get("chgDayPct")
        print(f"  [Price & Trend] Last: {price} | Day VWAP: {vwap} | Day POC: {poc} | 24h Chg: {chg}%")
    except Exception as e:
        print(f"  [Price] Error: {e}")

    # 2. CVD & Taker Flow
    try:
        c_req = urllib.request.urlopen(f"{base_url}/api/cg/cvd?sym={sym}")
        c_data = json.loads(c_req.read().decode())
        taker_delta = c_data.get("delta") or c_data.get("taker_buy_sell_ratio")
        slope = c_data.get("slope")
        divergence = c_data.get("divergence")
        print(f"  [CVD Flow] Delta: {taker_delta} | Slope: {slope} | Divergence: {divergence}")
    except Exception as e:
        print(f"  [CVD] Error: {e}")

    # 3. Bookwalls (Resting Liquidity)
    try:
        b_req = urllib.request.urlopen(f"{base_url}/api/cg/bookwalls?sym={sym}")
        b_data = json.loads(b_req.read().decode())
        asks = b_data.get("top_asks") or b_data.get("ask_walls", [])[:3]
        bids = b_data.get("top_bids") or b_data.get("bid_walls", [])[:3]
        print(f"  [Book Walls] Top Asks: {asks} | Top Bids: {bids}")
    except Exception as e:
        print(f"  [Bookwalls] Error: {e}")

    # 4. Liquidation Levels (7d / 3d)
    if sym != "XAU":
        try:
            l_req = urllib.request.urlopen(f"{base_url}/api/cg/liqlevels?sym={sym}&range=3d")
            l_data = json.loads(l_req.read().decode())
            venues = l_data.get("venues")
            partial = l_data.get("partial")
            fallback = l_data.get("rangeFallback")
            short_str = l_data.get("total_short_strength") or l_data.get("short_strength")
            long_str = l_data.get("total_long_strength") or l_data.get("long_strength")
            ratio = l_data.get("ratio")
            print(f"  [Liq Levels 3D] Venues: {venues} | Partial: {partial} | Fallback: {fallback}")
            print(f"  [Liq Magnet] Short Liq Str (Above): {short_str} | Long Liq Str (Below): {long_str} | S/L Ratio: {ratio}")
        except Exception as e:
            print(f"  [LiqLevels] Error: {e}")

    # 5. Signals & Tape Footprint
    try:
        s_req = urllib.request.urlopen(f"{base_url}/api/cg/signals?sym={sym}")
        s_data = json.loads(s_req.read().decode())
        signals = s_data.get("signals") or s_data.get("recent", [])[:3]
        print(f"  [Signals & Tape] Recent: {signals}")
    except Exception as e:
        print(f"  [Signals] Error: {e}")

print("\n================================================================================")
