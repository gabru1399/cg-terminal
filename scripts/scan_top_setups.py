import urllib.request
import json

data = json.loads(urllib.request.urlopen('http://127.0.0.1:3000/api/cg/screener').read().decode())
rows = data.get('rows', [])

print("=== BULLISH IN-TREND / REVERSAL CANDIDATES ===")
bulls = []
for r in rows:
    c = r.get('confluence') or {}
    m = r.get('m1m2') or {}
    if c.get('bias') == 'BULL' or m.get('direction') == 'LONG' or m.get('regime') == 'TREND_UP':
        bulls.append((r, c, m))

bulls.sort(key=lambda x: (x[1].get('readiness') == 'A+', x[2].get('grade') in ('A+', 'A'), x[2].get('evR') or 0), reverse=True)
print(f"Total bull rows: {len(bulls)}")
for r, c, m in bulls[:15]:
    ev_val = m.get('evR')
    ev_str = f"{ev_val:.2f}" if isinstance(ev_val, (int, float)) else str(ev_val)
    print(f"{r.get('sym'):<8} | {r.get('kind'):<11} | Bias: {str(c.get('bias')):<5} | Ready: {str(c.get('readiness')):<5} | Grade: {str(m.get('grade')):<5} | Regime: {str(m.get('regime')):<18} | EV: {ev_str:<5} | Factors: {c.get('factors')}")

print("\n=== BEARISH IN-TREND CANDIDATES (TREND_DOWN) ===")
bears = []
for r in rows:
    c = r.get('confluence') or {}
    m = r.get('m1m2') or {}
    if m.get('regime') == 'TREND_DOWN' and (c.get('bias') == 'BEAR' or m.get('direction') == 'SHORT'):
        bears.append((r, c, m))

bears.sort(key=lambda x: (x[1].get('readiness') == 'A+', x[2].get('grade') in ('A+', 'A'), x[2].get('evR') or 0), reverse=True)
print(f"Total bear trend rows: {len(bears)}")
for r, c, m in bears[:15]:
    ev_val = m.get('evR')
    ev_str = f"{ev_val:.2f}" if isinstance(ev_val, (int, float)) else str(ev_val)
    print(f"{r.get('sym'):<8} | {r.get('kind'):<11} | Bias: {str(c.get('bias')):<5} | Ready: {str(c.get('readiness')):<5} | Grade: {str(m.get('grade')):<5} | EV: {ev_str:<5} | Factors: {c.get('factors')}")
