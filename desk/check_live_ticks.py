import urllib.request
import json

base_url = "http://127.0.0.1:3000"

targets = [
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC', 
    'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR', 
    'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB'
]

standing_orders = {
    'DOT': {'entry': 0.7480, 'order_id': 1684506647},
    'LTC': {'entry': 45.480, 'order_id': 1684443284},
    'ETH': {'entry': 1838.50, 'order_id': 1684442347},
    'SOL': {'entry': 72.450, 'order_id': 1684424777}
}

print("=== LIVE TICKER CHECK FOR STANDING ORDERS ===")
for sym, order_info in standing_orders.items():
    try:
        req = urllib.request.Request(f"{base_url}/api/cg/market?sym={sym}")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        last_price = data.get("price", {}).get("last")
        entry = order_info['entry']
        dist_pct = (entry - last_price) / last_price * 100
        print(f"{sym} (Order #{order_info['order_id']}): Live Price = {last_price} | Entry Limit = {entry} | Distance to Fill = {dist_pct:+.2f}%")
    except Exception as e:
        print(f"{sym} error: {e}")
