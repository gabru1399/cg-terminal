import urllib.request
import json

for s in ['BTC', 'ETH', 'SOL', 'LTC']:
    try:
        req = urllib.request.Request(f'http://127.0.0.1:3000/api/cg/fp?sym={s}&limit=5')
        with urllib.request.urlopen(req, timeout=5) as resp:
            fp = json.loads(resp.read().decode('utf-8'))
        valid = sum(1 for b in fp.get('bars', []) if b.get('pocPrice') is not None)
        print(f"{s}: {len(fp.get('bars', []))} bars, {valid} with valid POC")
    except Exception as e:
        print(f"{s} error: {e}")
