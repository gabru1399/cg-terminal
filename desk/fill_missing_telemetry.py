import urllib.request
import json
import time

with open('desk/crypto_telemetry_bundle.json', 'r') as f:
    bundle = json.load(f)

all_data = bundle['all_data']

def fetch_json(url, timeout=12):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            if attempt == 1:
                return {'error': str(e)}
            time.sleep(0.5)

endpoints = {
    'cvd': 'http://127.0.0.1:3000/api/cg/cvd?sym={sym}',
    'bookwalls': 'http://127.0.0.1:3000/api/cg/bookwalls?sym={sym}',
    'liqlevels': 'http://127.0.0.1:3000/api/cg/liqlevels?sym={sym}'
}

print("Filling missing/error telemetry sequentially...", flush=True)
for sym, data in all_data.items():
    for key, url_pattern in endpoints.items():
        val = data.get(key)
        if not val or (isinstance(val, dict) and 'error' in val):
            url = url_pattern.format(sym=sym)
            t0 = time.time()
            res = fetch_json(url)
            elapsed = time.time() - t0
            data[key] = res
            status = 'OK' if ('error' not in res) else f"ERR: {res['error']}"
            print(f"[{sym}] {key}: {status} ({elapsed:.2f}s)", flush=True)

with open('desk/crypto_telemetry_bundle.json', 'w') as f:
    json.dump(bundle, f)

print("Saved updated telemetry bundle.", flush=True)
