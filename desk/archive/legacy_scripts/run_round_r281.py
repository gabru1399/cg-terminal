import urllib.request
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

CRYPTO_30 = [
    "BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "TRX", "LINK", "LTC",
    "AVAX", "DOT", "NEAR", "UNI", "ATOM", "XLM", "ETC", "FIL", "ICP", "HBAR",
    "APT", "ARB", "OP", "SUI", "SEI", "INJ", "TIA", "VET", "1000PEPE", "1000SHIB"
]

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

def fetch_sym(sym):
    endpoints = {
        "narrative": f"http://127.0.0.1:3000/api/cg/narrative?sym={sym}",
        "market": f"http://127.0.0.1:3000/api/cg/market?sym={sym}",
        "signals": f"http://127.0.0.1:3000/api/cg/signals?sym={sym}",
        "liq": f"http://127.0.0.1:3000/api/cg/liqlevels?sym={sym}",
        "bookwalls": f"http://127.0.0.1:3000/api/cg/bookwalls?sym={sym}",
        "cvd": f"http://127.0.0.1:3000/api/cg/cvd?sym={sym}",
        "backtest": f"http://127.0.0.1:3000/api/cg/backtest?sym={sym}"
    }
    res = {}
    for k, u in endpoints.items():
        res[k] = fetch_json(u)
    return sym, res

t0 = time.time()
results = {}
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(fetch_sym, sym): sym for sym in CRYPTO_30}
    for f in as_completed(futures):
        sym = futures[f]
        try:
            s, d = f.result()
            results[s] = d
        except Exception as e:
            pass

with open("desk/crypto_sweep_r281.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Sweep R281 complete in {time.time()-t0:.2f}s across {len(results)} assets.", flush=True)

# Print comparison for key assets
for sym in ["ETH", "LINK", "SUI", "LTC", "BTC", "SOL", "BNB"]:
    d = results.get(sym, {})
    m = d.get("market", {})
    p = m.get("price", {})
    price = p.get("last") if isinstance(p, dict) else p
    auc = m.get("auction", {})
    day = auc.get("day", {})
    sess = auc.get("session", {})
    vwap = m.get("vwap", {})
    vwap_val = vwap.get("vwap", 0)
    sd1 = vwap.get("bands", {}).get("sd1", 0)
    z = (price - vwap_val)/sd1 if (price and vwap_val and sd1) else 0
    print(f"[{sym:5s}] Price: {price} | Day VAL: {day.get('val')} | Day POC: {day.get('poc')} | Day VAH: {day.get('vah')} | Sess POC: {sess.get('poc')} | z: {z:.2f}σ", flush=True)
