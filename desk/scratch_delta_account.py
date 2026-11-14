import os, time, hmac, hashlib, json, requests
from pathlib import Path

env_dict = {}
env_path = Path.home() / '.delta-exchange-mcp' / 'config.env'
for line in env_path.read_text().splitlines():
    if '=' in line:
        k, v = line.split('=', 1)
        env_dict[k.strip()] = v.strip()

key = env_dict.get('DELTA_LIVE_PROD_KEY')
secret = env_dict.get('DELTA_LIVE_PROD_SECRET')
base_url = 'https://api.india.delta.exchange'

def request(method, path, body=''):
    ts = str(int(time.time()))
    payload = method + ts + path + body
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    headers = {
        'api-key': key,
        'timestamp': ts,
        'signature': sig,
        'Content-Type': 'application/json'
    }
    url = base_url + path
    if method == 'GET':
        r = requests.get(url, headers=headers, timeout=10)
    elif method == 'POST':
        r = requests.post(url, headers=headers, data=body, timeout=10)
    elif method == 'DELETE':
        r = requests.delete(url, headers=headers, timeout=10)
    return r.status_code, r.json()

s, res = request('GET', '/v2/positions/margined')
print("POSITIONS:", json.dumps(res, indent=2))

s2, res2 = request('GET', '/v2/orders?state=open')
print("OPEN ORDERS:", json.dumps(res2, indent=2))

s3, res3 = request('GET', '/v2/wallet/balances')
print("BALANCES:", json.dumps(res3, indent=2))
