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
        with urllib.request.urlopen(req, timeout=3.5) as resp:
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
        "cvd": f"http://127.0.0.1:3000/api/cg/cvd?sym={sym}"
    }
    res = {}
    for k, u in endpoints.items():
        res[k] = fetch_json(u)
    return sym, res

results = {}
t0 = time.time()
print(f"Starting parallel sweep across {len(CRYPTO_30)} crypto assets...", flush=True)

with ThreadPoolExecutor(max_workers=6) as executor:
    futures = {executor.submit(fetch_sym, sym): sym for sym in CRYPTO_30}
    for future in as_completed(futures):
        sym = futures[future]
        try:
            s, data = future.result()
            results[s] = data
            price = data.get("market", {}).get("price", {}).get("last")
            print(f"  [DONE] {sym:8s} | Price: {price}", flush=True)
        except Exception as exc:
            print(f"  [FAIL] {sym:8s} | Exception: {exc}", flush=True)

with open("desk/crypto_sweep_r275.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Sweep finished in {time.time()-t0:.2f}s and saved to desk/crypto_sweep_r275.json", flush=True)

# Print active assets summary
print("\n--- ACTIVE ASSETS MICROSTRUCTURE (CURRENT vs VAL/POC/VAH) ---", flush=True)
for sym in ["ETH", "LINK", "SUI", "LTC", "BTC", "SOL", "BNB", "XRP", "DOGE", "ADA"]:
    m = results.get(sym, {}).get("market", {})
    auc = m.get("auction", {})
    day = auc.get("day", {})
    sess = auc.get("session", {})
    vwap = m.get("vwap", {})
    p = m.get("price", {})
    price = p.get("last") if isinstance(p, dict) else p
    mid = vwap.get("mid")
    bands = vwap.get("bands", {})
    sd1 = bands.get("sd1", 0)
    vwap_val = vwap.get("vwap", 0)
    z = (price - vwap_val)/sd1 if (price and vwap_val and sd1) else 0
    val_v = day.get('val')
    poc_v = day.get('poc')
    vah_v = day.get('vah')
    spoc_v = sess.get('poc')
    val_str = f"{val_v:.2f}" if isinstance(val_v, (int, float)) else str(val_v)
    poc_str = f"{poc_v:.2f}" if isinstance(poc_v, (int, float)) else str(poc_v)
    vah_str = f"{vah_v:.2f}" if isinstance(vah_v, (int, float)) else str(vah_v)
    spoc_str = f"{spoc_v:.2f}" if isinstance(spoc_v, (int, float)) else str(spoc_v)
    print(f"[{sym:5s}] Price: {price} | Day VAL: {val_str} | Day POC: {poc_str} | Day VAH: {vah_str} | Sess POC: {spoc_str} | VWAP: {vwap_val:.2f} | z: {z:.2f}σ", flush=True)
