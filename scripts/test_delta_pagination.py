import urllib.request
import json
import time

def fetch_chunk(symbol, resolution, start_ts, end_ts):
    url = f"https://api.india.delta.exchange/v2/chart/history?symbol={symbol}&resolution={resolution}&from={start_ts}&to={end_ts}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        return data.get('result', {})
    except Exception as e:
        print(f"Error fetching: {e}")
        return {}

now = int(time.time())
all_t = []
curr_to = now
target_from = int(time.mktime(time.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")))

for page in range(5):
    res = fetch_chunk('BTCUSD', '60', target_from, curr_to)
    t = res.get('t', [])
    if not t:
        print(f"No more candles returned at page {page}")
        break
    all_t.extend(t)
    print(f"Page {page}: got {len(t)} candles. Earliest: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t[0]))} to {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t[-1]))}")
    if t[0] <= target_from or len(t) < 100:
        break
    curr_to = t[0] - 1
    time.sleep(0.2)
