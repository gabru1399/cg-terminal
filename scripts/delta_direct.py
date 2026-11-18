import time
import hmac
import hashlib
import json
import urllib.request
import email.utils

API_KEY = "RrPSJVABou8UAT4BIl5ExCctYWV6dp"
API_SECRET = "1a0HWlsQfoeyv7J0rPx5mXWP0rEoL85RCWxUQmsI06aMS65cuQOhcUwjAiks"
BASE_URL = "https://api.india.delta.exchange"

_server_time_offset = 0.0

def get_server_time_offset():
    global _server_time_offset
    try:
        req = urllib.request.Request(f"{BASE_URL}/v2/products", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            date_hdr = resp.headers.get("Date")
            if date_hdr:
                server_ts = email.utils.parsedate_to_datetime(date_hdr).timestamp()
                _server_time_offset = server_ts - time.time()
                return _server_time_offset
    except Exception as e:
        print("Failed to sync server time:", e)
    return _server_time_offset

def sign(secret, method, timestamp, path, query, body):
    payload = f"{method}{timestamp}{path}{query}{body}"
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

def request_delta(method, path, query="", body=""):
    global _server_time_offset
    if _server_time_offset == 0.0:
        get_server_time_offset()

    ts = str(int(time.time() + _server_time_offset))
    sig = sign(API_SECRET, method, ts, path, query, body)

    headers = {
        "api-key": API_KEY,
        "signature": sig,
        "timestamp": ts,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }

    url = f"{BASE_URL}{path}{query}"
    data = body.encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            date_hdr = resp.headers.get("Date")
            if date_hdr:
                server_ts = email.utils.parsedate_to_datetime(date_hdr).timestamp()
                _server_time_offset = server_ts - time.time()
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            err_json = json.loads(err_body)
            # Check for expired signature
            if err_json.get("error", {}).get("code") == "expired_signature":
                ctx = err_json.get("error", {}).get("context", {})
                if "server_time" in ctx:
                    _server_time_offset = float(ctx["server_time"]) - time.time()
                    print(f"Signature expired! Resynced offset to {_server_time_offset:.2f}s, retrying...")
                    # Retry once
                    return request_delta(method, path, query, body)
        except Exception:
            pass
        return {"ok": False, "status": e.code, "error": err_body}

if __name__ == "__main__":
    print(f"Initial server time offset: {get_server_time_offset():.2f}s")
    
    print("\n--- WALLET BALANCES ---")
    wb = request_delta("GET", "/v2/wallet/balances")
    if wb.get("success"):
        for b in wb.get("result", []):
            if float(b.get("balance", 0)) > 0:
                print(f"Asset: {b.get('asset_symbol')} | Balance: {b.get('balance')} | Available: {b.get('available_balance')} | Order Margin: {b.get('order_margin')} | Position Margin: {b.get('position_margin')}")
    else:
        print("Error fetching balances:", wb)

    print("\n--- MARGINED POSITIONS ---")
    pos = request_delta("GET", "/v2/positions/margined")
    if pos.get("success"):
        for p in pos.get("result", []):
            print(f"Product: {p.get('product_symbol')} | Size: {p.get('size')} | Entry: {p.get('entry_price')} | Mark: {p.get('mark_price')} | PnL: ${float(p.get('unrealized_pnl', 0)):.4f} USD")
    else:
        print("Error fetching positions:", pos)

    print("\n--- OPEN ORDERS ---")
    orders = request_delta("GET", "/v2/orders", query="?state=open")
    if orders.get("success"):
        for o in orders.get("result", []):
            print(f"ID: {o.get('id')} | Sym: {o.get('product_symbol')} | Side: {o.get('side')} | Size: {o.get('size')} | Limit: ${o.get('limit_price')} | Bracket SL: ${o.get('bracket_stop_loss_price')} | Bracket TP: ${o.get('bracket_take_profit_price')}")
    else:
        print("Error fetching orders:", orders)
