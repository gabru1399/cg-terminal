import urllib.request
import json

base_url = "http://127.0.0.1:3000"

candidates = ["DOT", "SUI", "NEAR", "XRP", "FIL"]
results = {}

for sym in candidates:
    try:
        # Snapshot
        req = urllib.request.Request(f"{base_url}/api/cg/market?sym={sym}")
        with urllib.request.urlopen(req, timeout=5) as resp:
            market = json.loads(resp.read().decode('utf-8'))
        
        # Signals
        req_sig = urllib.request.Request(f"{base_url}/api/cg/signals?sym={sym}")
        with urllib.request.urlopen(req_sig, timeout=5) as resp:
            signals = json.loads(resp.read().decode('utf-8'))
            
        # Liq levels
        req_liq = urllib.request.Request(f"{base_url}/api/cg/liqlevels?sym={sym}")
        with urllib.request.urlopen(req_liq, timeout=5) as resp:
            liq = json.loads(resp.read().decode('utf-8'))

        # Footprint
        req_fp = urllib.request.Request(f"{base_url}/api/cg/footprint?sym={sym}&limit=10")
        with urllib.request.urlopen(req_fp, timeout=5) as resp:
            fp = json.loads(resp.read().decode('utf-8'))
            
        results[sym] = {
            "market": market,
            "signals": signals,
            "liq": liq,
            "fp_bars": len(fp.get("bars", [])) if isinstance(fp, dict) else 0
        }
    except Exception as e:
        results[sym] = {"error": str(e)}

with open("desk/candidates_telemetry.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Telemetry fetched for:", list(results.keys()))
