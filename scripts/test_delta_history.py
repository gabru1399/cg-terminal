import urllib.request
import json
import time

now = int(time.time())
# 1 year ago
one_year_ago = now - (365 * 24 * 3600)

url = f"https://api.india.delta.exchange/v2/chart/history?symbol=BTCUSD&resolution=60&from={one_year_ago}&to={now}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    result = data.get('result', {})
    t = result.get('t', [])
    print(f"Candles returned for BTCUSD (1H): {len(t)}")
    if t:
        print(f"Earliest candle: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t[0]))}")
        print(f"Latest candle:   {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t[-1]))}")
except Exception as e:
    print(f"Error: {e}")
