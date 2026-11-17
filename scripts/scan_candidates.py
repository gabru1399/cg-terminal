import urllib.request
import json

def run_scan():
    req = urllib.request.Request('http://localhost:3000/api/cg/screener', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode('utf-8'))

    rows = data.get('rows', [])
    print(f"Total screener rows evaluated: {len(rows)}")

    scored_rows = []
    for r in rows:
        sym = r.get('sym')
        conf = r.get('confluence')
        vwapZ = r.get('vwapZ')
        sig = r.get('signal')
        chg = r.get('chg24hPct')
        liq = r.get('liqMagnet')
        whale = r.get('whaleImbPct')
        cvd = r.get('cvdDiv')
        rsi = r.get('rsi15m')
        price = r.get('price')
        kind = r.get('kind')
        category = r.get('category')
        poc = r.get('poc')
        scored_rows.append({
            'sym': sym,
            'kind': kind,
            'category': category,
            'price': price,
            'poc': poc,
            'conf': conf,
            'vwapZ': vwapZ,
            'sig': sig,
            'chg': chg,
            'liq': liq,
            'whale': whale,
            'cvd': cvd,
            'rsi': rsi
        })

    print("\n=== TOP 20 EXTENSIONS BY ABSOLUTE VWAP Z-SCORE (|z| >= 1.5) ===")
    valid_z = [r for r in scored_rows if r['vwapZ'] is not None and abs(r['vwapZ']) >= 1.2]
    valid_z.sort(key=lambda x: abs(x['vwapZ']), reverse=True)
    for r in valid_z[:25]:
        print(f"{r['sym']:<10} {r['kind']:<8} price={r['price']:<10} vwapZ={r['vwapZ']:+.2f} rsi={str(r['rsi']):<6} chg={str(r['chg']):<7} sig={r['sig']}")

    print("\n=== CANDIDATES WITH ACTIVE FOOTPRINT / INDICATOR SIGNALS ===")
    with_sig = [r for r in scored_rows if r['sig'] is not None]
    for r in with_sig:
        print(f"{r['sym']:<10} {r['kind']:<8} price={r['price']:<10} sig={r['sig']} vwapZ={r['vwapZ']} rsi={r['rsi']}")

    print("\n=== CANDIDATES WITH LIQUIDATION MAGNET CLUSTERS ===")
    with_liq = [r for r in scored_rows if r['liq'] is not None]
    for r in with_liq[:15]:
        print(f"{r['sym']:<10} price={r['price']:<10} liqMagnet={r['liq']} whaleImb={r['whale']} vwapZ={r['vwapZ']}")

if __name__ == '__main__':
    run_scan()
