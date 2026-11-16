import urllib.request
import json

base = "http://127.0.0.1:3000"

def get(path):
    try:
        req = urllib.request.Request(f"{base}{path}", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4.0) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

scr = get("/api/cg/screener")
rows = scr.get("rows", [])
print(f"Total rows: {len(rows)}")
if rows:
    print("Row keys:", list(rows[0].keys()))
    for r in rows[:12]:
        print(f"Asset: {r.get('asset')} | Price: {r.get('price')} | EV: {r.get('evR')} | z: {r.get('vwapZ')} | RVOL: {r.get('rvol')} | Signal: {r.get('footprintSignal')} | Grade: {r.get('grade')} | Conf: {r.get('confluence')}")
