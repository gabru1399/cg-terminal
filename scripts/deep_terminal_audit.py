import urllib.request
import json

base = "http://127.0.0.1:3000"

def get(path):
    try:
        req = urllib.request.Request(f"{base}{path}", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

screener = get("/api/cg/screener")
rows = screener.get('rows', [])
print(f"Total screener rows ingested from local terminal: {len(rows)}")

grade_a = [r for r in rows if r.get('m1m2', {}).get('grade') in ['A', 'A+'] or (r.get('confluence') and 'A' in str(r.get('confluence')))]
print(f"Grade A / A+ candidates found in terminal screener: {len(grade_a)}")

for r in rows:
    sym = r.get('sym')
    if sym in ['BNB', 'LINK', 'ARB', 'ADA', 'TIA', 'SEI', 'ETC', 'XLM', 'BTC', 'ETH']:
        m1m2 = r.get('m1m2') or {}
        sig = r.get('signal') or {}
        liq = r.get('liqMagnet') or {}
        conf = r.get('confluence')
        print(f"Asset: {sym:5} | Price: {r.get('price')} | 24h: {r.get('chg24hPct')}% | EV(R): {m1m2.get('evR')} | Grade: {m1m2.get('grade')} | Conf: {conf} | Sig: {sig.get('type')} ({sig.get('bar')}) | LiqMag: {liq.get('distPct')}% (${liq.get('usd')})")
