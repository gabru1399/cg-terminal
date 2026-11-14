"""
Delta Exchange India Live Execution Client.
Direct REST client using HMAC SHA-256 authentication against api.india.delta.exchange.
Provides exact parity with delta-exchange-mcp tools:
- get_margined_positions
- get_open_orders
- get_wallet_balances
- place_order (with bracket SL/TP and post_only)
- cancel_order
- set_product_leverage
- get_ticker
"""

import os
import time
import hmac
import hashlib
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

logger = logging.getLogger("DeltaClient")

class DeltaClient:
    def __init__(self, config_env_path: Optional[Path] = None):
        if config_env_path is None:
            config_env_path = Path.home() / ".delta-exchange-mcp" / "config.env"
        
        env_dict = {}
        if config_env_path.exists():
            for line in config_env_path.read_text().splitlines():
                if "=" in line:
                    k, v = line.split("=", 1)
                    env_dict[k.strip()] = v.strip()
        
        self.api_key = env_dict.get("DELTA_LIVE_PROD_KEY") or env_dict.get("DELTA_API_KEY") or os.environ.get("DELTA_API_KEY")
        self.api_secret = env_dict.get("DELTA_LIVE_PROD_SECRET") or env_dict.get("DELTA_API_SECRET") or os.environ.get("DELTA_API_SECRET")
        self.base_url = "https://api.india.delta.exchange"
        
        if not self.api_key or not self.api_secret:
            raise ValueError("Delta Exchange API key and secret must be configured in config.env or environment.")

    def _request(self, method: str, path: str, params: Optional[Dict] = None, body: Optional[Dict] = None) -> Dict[str, Any]:
        import requests
        ts = str(int(time.time()))
        query_str = ""
        if params:
            query_str = "?" + "&".join([f"{k}={v}" for k, v in sorted(params.items())])
        body_str = json.dumps(body) if body is not None else ""
        payload = method.upper() + ts + path + query_str + body_str
        signature = hmac.new(self.api_secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
        
        headers = {
            "api-key": self.api_key,
            "timestamp": ts,
            "signature": signature,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        url = self.base_url + path + query_str
        
        if method.upper() == "GET":
            r = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == "POST":
            r = requests.post(url, headers=headers, data=body_str, timeout=10)
        elif method.upper() == "DELETE":
            r = requests.delete(url, headers=headers, data=body_str if body_str else None, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        try:
            return r.json()
        except Exception:
            return {"success": False, "status_code": r.status_code, "text": r.text}

    def get_margined_positions(self) -> List[Dict[str, Any]]:
        res = self._request("GET", "/v2/positions/margined")
        if res.get("success"):
            return res.get("result", [])
        return []

    def get_open_orders(self) -> List[Dict[str, Any]]:
        res = self._request("GET", "/v2/orders", params={"state": "open"})
        if res.get("success"):
            return res.get("result", [])
        return []

    def get_wallet_balances(self) -> Dict[str, Any]:
        res = self._request("GET", "/v2/wallet/balances")
        return res

    def set_product_leverage(self, product_id: int, leverage: int) -> Dict[str, Any]:
        body = {"leverage": str(leverage)}
        res = self._request("POST", f"/v2/products/{product_id}/orders/leverage", body=body)
        return res

    def place_order(
        self,
        product_id: Optional[int] = None,
        product_symbol: Optional[str] = None,
        size: int = 1,
        side: str = "buy",
        order_type: str = "limit_order",
        limit_price: Optional[str] = None,
        post_only: bool = True,
        time_in_force: str = "gtc",
        bracket_stop_loss_price: Optional[str] = None,
        bracket_take_profit_price: Optional[str] = None,
        bracket_stop_trigger_method: str = "mark_price"
    ) -> Dict[str, Any]:
        body = {
            "size": size,
            "side": side,
            "order_type": order_type,
            "post_only": post_only,
            "time_in_force": time_in_force
        }
        if product_id is not None:
            body["product_id"] = product_id
        if product_symbol is not None:
            body["product_symbol"] = product_symbol
        if limit_price is not None:
            body["limit_price"] = str(limit_price)
        if bracket_stop_loss_price is not None:
            body["bracket_stop_loss_price"] = str(bracket_stop_loss_price)
            body["bracket_stop_trigger_method"] = bracket_stop_trigger_method
        if bracket_take_profit_price is not None:
            body["bracket_take_profit_price"] = str(bracket_take_profit_price)
        
        res = self._request("POST", "/v2/orders", body=body)
        return res

    def cancel_order(self, order_id: int, product_id: int) -> Dict[str, Any]:
        body = {"id": order_id, "product_id": product_id}
        res = self._request("DELETE", "/v2/orders", body=body)
        return res

if __name__ == "__main__":
    client = DeltaClient()
    print("Testing DeltaClient:")
    positions = client.get_margined_positions()
    print(f"Positions: {positions}")
    orders = client.get_open_orders()
    print(f"Open orders: {orders}")
    wallet = client.get_wallet_balances()
    print(f"Wallet balances: net_equity={wallet.get('meta', {}).get('net_equity')}")
