import urllib.request, json

sym = 'NDX100'
for ep in ['market', 'fp', 'largeorder', 'liqlevels', 'bookwalls', 'cvd', 'classic', 'cot']:
    try:
        url = f'http://127.0.0.1:3000/api/cg/{ep}?sym={sym}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(ep + ": ok=" + str(data.get("ok")) + " supported=" + str(data.get("supported")) + " keys=" + str(list(data.keys())[:5]))
    except Exception as e:
        print(ep + " error: " + str(e))

print("\n--- Testing COT for BTC, ETH, SOL, NVDA, NDX100 ---")
for s in ['BTC', 'ETH', 'SOL', 'NVDA', 'NDX100', 'XAU']:
    try:
        url = 'http://127.0.0.1:3000/api/cg/cot?sym=' + s
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(s + " cot: ok=" + str(data.get("ok")) + " source=" + str(data.get("source")) + " contract=" + str(data.get("contract")))
    except Exception as e:
        print(s + " cot error: " + str(e))
