import json
import time

path = 'desk/state.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

orders = data.get('orders', [])

# TIA order
orders.append({
    "id": "1686483354",
    "symbol": "TIAUSD",
    "product_id": 17330,
    "side": "sell",
    "order_type": "limit_order",
    "size": 2,
    "price": 0.3465,
    "sl": 0.3520,
    "tp": 0.3340,
    "status": "pending",
    "ticket": 1686483354,
    "ts": int(time.time() * 1000),
    "reason": "Terminal Screener Grade A SELL Divergence pullback fade (EV +0.67R, 2.27R reward)"
})

# ADA order
orders.append({
    "id": "1686484401",
    "symbol": "ADAUSD",
    "product_id": 16614,
    "side": "sell",
    "order_type": "limit_order",
    "size": 10,
    "price": 0.1524,
    "sl": 0.1542,
    "tp": 0.1479,
    "status": "pending",
    "ticket": 1686484401,
    "ts": int(time.time() * 1000),
    "reason": "Terminal Screener Grade B SELL Exhaustion pullback fade (EV +0.30R, 2.50R reward)"
})

data['orders'] = orders

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Updated desk/state.json successfully.")
