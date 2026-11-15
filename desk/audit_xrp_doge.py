import urllib.request
import json

base_url = "http://127.0.0.1:3000"

def fetch(endpoint):
    req = urllib.request.Request(f"{base_url}{endpoint}")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode('utf-8'))

for sym in ["XRP", "DOGE"]:
    market = fetch(f"/api/cg/market?sym={sym}")
    fp = fetch(f"/api/cg/fp?sym={sym}&limit=10")
    bookwalls = fetch(f"/api/cg/bookwalls?sym={sym}")
    liq = fetch(f"/api/cg/liqlevels?sym={sym}")

    last_price = market.get("price", {}).get("last")
    auction = market.get("auction", {})
    day_vah = auction.get("day", {}).get("vah")
    day_poc = auction.get("day", {}).get("poc")
    day_val = auction.get("day", {}).get("val")

    sess_vah = auction.get("session", {}).get("vah")
    sess_poc = auction.get("session", {}).get("poc")
    sess_val = auction.get("session", {}).get("val")

    vwap = market.get("vwap", {})
    v_val = vwap.get("vwap")
    sd1 = vwap.get("bands", {}).get("sd1", 0)
    sd2 = vwap.get("bands", {}).get("sd2", 0)

    print(f"\n==================== {sym} ====================")
    print(f"Price: {last_price}")
    print(f"Day Auction: VAH={day_vah}, POC={day_poc}, VAL={day_val}")
    print(f"Session Auction: VAH={sess_vah}, POC={sess_poc}, VAL={sess_val}")
    print(f"Day VWAP: {v_val:.4f} (+1σ: {v_val+sd1:.4f}, +2σ: {v_val+sd2:.4f})")

    confirmed_walls = bookwalls.get("walls", {}).get("confirmed", [])
    print(f"Confirmed Book Walls ({len(confirmed_walls)} total):")
    for w in confirmed_walls[:5]:
        print(f"  Side: {w.get('side')} | Price: {w.get('price')} | Notional: ${w.get('notional', 0)/1e3:.1f}k | Dist: {w.get('distPct')}%")

    bars = fp.get("bars", [])
    valid_pocs = [b.get("pocPrice") for b in bars if b.get("pocPrice") is not None]
    print(f"Footprint Bars: {len(bars)} bars, valid POCs: {len(valid_pocs)}")
    for b in bars[:3]:
        print(f"  POC: {b.get('pocPrice')} | Vol: ${b.get('totalVolumeUsd', 0)/1e3:.1f}k")
