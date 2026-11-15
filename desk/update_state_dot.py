import json
import time

# 1. Update desk/state.json
with open("desk/state.json", "r", encoding="utf-8") as f:
    state = json.load(f)

dot_order = {
    "id": "DELTA-1684506647",
    "symbol": "DOT",
    "product_symbol": "DOTUSD",
    "product_id": 15304,
    "side": "sell",
    "size": 1,
    "contract_value": "1 DOT",
    "status": "placed",
    "ticket": 1684506647,
    "entry": 0.7480,
    "stop": 0.7550,
    "targets": [0.7180],
    "venue": "Delta Exchange India",
    "account": 26902927,
    "margin_mode": "isolated",
    "leverage": 50,
    "post_only": True,
    "created_at": int(time.time() * 1000),
    "r_multiple": 4.29,
    "notes": "Canonical Setup S1: Short Liquidity Sweep & Reclaim. Entry @ 0.7480 tags the $2.05M short liq cluster sweep @ 0.7479 + VWAP +2.1σ. SL @ 0.7550 shielded in structural vacuum (Gate 1 distance 1.931%, Gate 2 $0.00 hazard). TP @ 0.7180 (Day POC/VWAP). 4.29R, Confluence 10.5/11.5 Grade A."
}

# Avoid duplicate
existing_ids = [o.get("id") for o in state.get("orders", [])]
if dot_order["id"] not in existing_ids:
    state["orders"].append(dot_order)

with open("desk/state.json", "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)

print("Updated desk/state.json successfully.")

# 2. Update desk/screener_matrix_r281.json
with open("desk/screener_matrix_r281.json", "r", encoding="utf-8") as f:
    matrix = json.load(f)

for row in matrix:
    if row.get("sym") == "DOT":
        row["status"] = "ORDER_RESTING (#1684506647)"
        row["t7"] = "10.5"

with open("desk/screener_matrix_r281.json", "w", encoding="utf-8") as f:
    json.dump(matrix, f, indent=2)

print("Updated desk/screener_matrix_r281.json successfully.")
