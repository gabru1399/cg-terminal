import urllib.request
import json

base = "http://127.0.0.1:3000"

def get(p):
    try:
        req = urllib.request.Request(f"{base}{p}", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3.0) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

sym = "APT"
narr = get(f"/api/cg/narrative?sym={sym}")
m = get(f"/api/cg/market?sym={sym}")
sig = get(f"/api/cg/signals?sym={sym}")
cvd = get(f"/api/cg/cvd?sym={sym}&itv=15m")
walls = get(f"/api/cg/bookwalls?sym={sym}")
liq = get(f"/api/cg/liqlevels?sym={sym}")

print("=== NARRATIVE ===")
print(json.dumps(narr, indent=2))
print("\n=== MARKET STRUCTURE ===")
print("Price:", m.get("price"))
print("Session Auction:", m.get("auction", {}).get("session"))
print("Day Auction:", m.get("auction", {}).get("day"))
print("Month Auction:", m.get("auction", {}).get("month"))
print("VWAP:", m.get("vwap"))
print("EMA:", m.get("ema"))
print("\n=== SIGNALS ===")
print(json.dumps(sig, indent=2))
print("\n=== CVD ===")
print(json.dumps(cvd, indent=2))
print("\n=== LIQUIDATION CLUSTERS ===")
clusters = liq.get("clusters", []) if isinstance(liq.get("clusters"), list) else []
print(f"Total clusters: {len(clusters)}")
for c in clusters[:10]:
    print(c)
