import json
import time

path = 'desk/state.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

orders = data.get('orders', [])

# Update BTC and ETH as closed
for o in orders:
    if o.get('symbol') == 'BTCUSD' and o.get('ticket') == 1686273067:
        o['status'] = 'closed'
        o['exit_price'] = 64050.5
        o['realized_pnl'] = 0.6995
        o['reason'] = 'Take profit hit @ 64050.5 (+0.70 USD gain)'
    elif o.get('symbol') == 'ETHUSD' and o.get('ticket') == 1686273813:
        o['status'] = 'closed'
        o['exit_price'] = 1792.6
        o['realized_pnl'] = 0.1990
        o['reason'] = 'Take profit hit @ 1792.6 (+0.20 USD gain)'

# Add the 5 new live maker limit orders
new_orders = [
    {
        "id": "1686518888",
        "symbol": "BNBUSD",
        "product_id": 15042,
        "side": "sell",
        "order_type": "limit_order",
        "size": 1,
        "price": 589.5,
        "sl": 596.5,
        "tp": 572.0,
        "status": "open",
        "ticket": 1686518888,
        "ts": int(time.time() * 1000),
        "reason": "Terminal Screener Grade A+ SELL Absorption (vol) at VWAP -2σ (2.50R)"
    },
    {
        "id": "1686521123",
        "symbol": "LINKUSD",
        "product_id": 15041,
        "side": "sell",
        "order_type": "limit_order",
        "size": 1,
        "price": 9.12,
        "sl": 9.25,
        "tp": 8.80,
        "status": "open",
        "ticket": 1686521123,
        "ts": int(time.time() * 1000),
        "reason": "Terminal Screener Grade A SELL Divergence (time) 4H EMA- Below VWAP (2.46R)"
    },
    {
        "id": "1686521803",
        "symbol": "ARBUSD",
        "product_id": 17331,
        "side": "sell",
        "order_type": "limit_order",
        "size": 10,
        "price": 0.1335,
        "sl": 0.1360,
        "tp": 0.1270,
        "status": "open",
        "ticket": 1686521803,
        "ts": int(time.time() * 1000),
        "reason": "Terminal Screener Grade A SELL Divergence (range) 4H EMA- Below VWAP (2.60R)"
    },
    {
        "id": "1686522407",
        "symbol": "ADAUSD",
        "product_id": 16614,
        "side": "sell",
        "order_type": "limit_order",
        "size": 10,
        "price": 0.1524,
        "sl": 0.1542,
        "tp": 0.1479,
        "status": "open",
        "ticket": 1686522407,
        "ts": int(time.time() * 1000),
        "reason": "Terminal Screener Grade A+ SELL Absorption (vol) 4H EMA- Below VWAP (2.50R)"
    },
    {
        "id": "1686523065",
        "symbol": "TIAUSD",
        "product_id": 17330,
        "side": "sell",
        "order_type": "limit_order",
        "size": 2,
        "price": 0.3475,
        "sl": 0.3530,
        "tp": 0.3340,
        "status": "open",
        "ticket": 1686523065,
        "ts": int(time.time() * 1000),
        "reason": "Terminal Screener Grade A SELL Divergence (vol) EV +0.86R (2.45R)"
    }
]

# Avoid duplicates
existing_ids = {str(o.get('id')) for o in orders}
for no in new_orders:
    if str(no['id']) not in existing_ids:
        orders.append(no)

data['orders'] = orders

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Updated desk/state.json with all 5 new orders and 2 closed trades.")
