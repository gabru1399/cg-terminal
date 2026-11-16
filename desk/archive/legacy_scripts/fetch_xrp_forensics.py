import urllib.request
import json

def fetch_json(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {'error': str(e)}

sym = 'XRP'
print(f"=== FETCHING 9-TAB FORENSICS FOR {sym} ===")
market = fetch_json(f'http://127.0.0.1:3000/api/cg/market?sym={sym}')
signals = fetch_json(f'http://127.0.0.1:3000/api/cg/signals?sym={sym}')
fp = fetch_json(f'http://127.0.0.1:3000/api/cg/fp?sym={sym}')
lto = fetch_json(f'http://127.0.0.1:3000/api/cg/lto?sym={sym}')
liq = fetch_json(f'http://127.0.0.1:3000/api/cg/liqlevels?sym={sym}')
bookwalls = fetch_json(f'http://127.0.0.1:3000/api/cg/bookwalls?sym={sym}')
cvd = fetch_json(f'http://127.0.0.1:3000/api/cg/cvd?sym={sym}')
narrative = fetch_json(f'http://127.0.0.1:3000/api/cg/narrative?sym={sym}')

summary = {
    'market': {
        'price': market.get('price'),
        'auction': market.get('auction'),
        'vwap': market.get('vwap'),
        'ema': market.get('ema'),
        'rsi': market.get('rsi')
    },
    'signals_count': len(signals.get('signals', [])) if isinstance(signals.get('signals'), list) else 0,
    'fp_bars': len(fp.get('bars', [])) if isinstance(fp.get('bars'), list) else 0,
    'liq': {
        'totalLong': liq.get('totalLongUsd'),
        'totalShort': liq.get('totalShortUsd'),
        'skew': liq.get('skewRatio'),
        'clusters': len(liq.get('clusters', [])) if isinstance(liq.get('clusters'), list) else 0
    },
    'bookwalls': {
        'bidTotal': bookwalls.get('bidTotalUsd'),
        'askTotal': bookwalls.get('askTotalUsd'),
        'imbalance': bookwalls.get('imbalance')
    },
    'cvd': {
        'perpCvd': cvd.get('perpCvd'),
        'spotCvd': cvd.get('spotCvd'),
        'takerBuyPct': cvd.get('takerBuyShare')
    },
    'narrative': {
        'regime': narrative.get('regime'),
        'activeModel': narrative.get('activeModel'),
        'bias': narrative.get('bias'),
        'checklist': narrative.get('checklist')
    }
}

with open('desk/xrp_forensics.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
