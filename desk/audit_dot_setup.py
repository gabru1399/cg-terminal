import urllib.request
import json

base_url = "http://127.0.0.1:3000"

# Fetch DOT market, fp, bookwalls, liqlevels
def fetch(endpoint):
    req = urllib.request.Request(f"{base_url}{endpoint}")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode('utf-8'))

market = fetch("/api/cg/market?sym=DOT")
fp = fetch("/api/cg/fp?sym=DOT&limit=20")
bookwalls = fetch("/api/cg/bookwalls?sym=DOT")
liq = fetch("/api/cg/liqlevels?sym=DOT")

last_price = market.get("price", {}).get("last", 0.7325)
auction = market.get("auction", {})
day_vah = auction.get("day", {}).get("vah")
day_poc = auction.get("day", {}).get("poc")
day_val = auction.get("day", {}).get("val")

sess_vah = auction.get("session", {}).get("vah")
sess_poc = auction.get("session", {}).get("poc")
sess_val = auction.get("session", {}).get("val")

month_poc = auction.get("month", {}).get("poc")

vwap = market.get("vwap", {})
v_val = vwap.get("vwap")
sd1 = vwap.get("bands", {}).get("sd1", 0)
sd2 = vwap.get("bands", {}).get("sd2", 0)
sd3 = vwap.get("bands", {}).get("sd3", 0)

vwap_p1 = v_val + sd1
vwap_p2 = v_val + sd2
vwap_p3 = v_val + sd3

print(f"DOT Price: {last_price}")
print(f"Day Auction: VAH={day_vah}, POC={day_poc}, VAL={day_val}")
print(f"Session Auction: VAH={sess_vah}, POC={sess_poc}, VAL={sess_val}")
print(f"Month POC: {month_poc}")
print(f"Day VWAP: {v_val:.4f} (+1σ: {vwap_p1:.4f}, +2σ: {vwap_p2:.4f}, +3σ: {vwap_p3:.4f})")

# Book walls
confirmed_walls = bookwalls.get("walls", {}).get("confirmed", [])
print(f"\nConfirmed Book Walls ({len(confirmed_walls)} total):")
for w in confirmed_walls[:8]:
    print(f"  Side: {w.get('side')} | Price: {w.get('price')} | Notional: ${w.get('notional', 0)/1e3:.1f}k | Dist: {w.get('distPct')}%")

# Footprint Bars & POCs
bars = fp.get("bars", [])
print(f"\nRecent Footprint Bars ({len(bars)} bars):")
session_pocs = []
for i, b in enumerate(bars[:10]):
    bar_poc = b.get("pocPrice")
    bar_vol = b.get("totalVolumeUsd", 0)
    session_pocs.append(bar_poc)
    print(f"  Bar {i} (ts={b.get('ts')}): POC={bar_poc} | Vol=${bar_vol/1e3:.1f}k | Delta={b.get('deltaPct')}%")

# Liq key levels
key_above = liq.get("stats", {}).get("keyLevels", {}).get("above", [])
key_below = liq.get("stats", {}).get("keyLevels", {}).get("below", [])
print(f"\nLiq Key Levels Above:")
for k in key_above[:5]:
    print(f"  Price: {k.get('price')} | Vol: ${k.get('usd', 0)/1e3:.1f}k | Dist: {k.get('distPct')}%")
print(f"Liq Key Levels Below:")
for k in key_below[:5]:
    print(f"  Price: {k.get('price')} | Vol: ${k.get('usd', 0)/1e3:.1f}k | Dist: {k.get('distPct')}%")
