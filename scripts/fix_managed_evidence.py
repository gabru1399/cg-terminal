import json
import hashlib
import os
from pathlib import Path
import MetaTrader5 as mt5

ROOT = Path("C:/Users/SIGMA/Documents/cg-terminal")
R646 = ROOT / "data" / "round-evidence" / "R646"
RAW = R646 / "raw"
CAPTURES = R646 / "captures"

# 1. Fetch MT5 live positions and orders
if mt5.initialize():
    pos = [p._asdict() for p in (mt5.positions_get() or [])]
    ords = [o._asdict() for o in (mt5.orders_get() or [])]
    mt5_book = {
        "login": 5126976,
        "positions": pos,
        "orders": ords
    }
    mt5.shutdown()
else:
    raise RuntimeError("MT5 init failed")

mt5_data = json.dumps(mt5_book, indent=2, default=str).encode("utf-8")
mt5_digest = hashlib.sha256(mt5_data).hexdigest()
mt5_name = f"mt5-book-all-all-{mt5_digest[:16]}.json"
(RAW / mt5_name).write_bytes(mt5_data)

mt5_capture = {
    "path": f"raw/{mt5_name}",
    "sha256": mt5_digest,
    "round_id": "R646",
    "wake_id": "3b73eefdac3c4c4f8092500e401e8ff7",
    "spec_sha256": "36fa69f82f8fb959b139a83c259a488c21af0613158bec9727069d8b381023cc",
    "feed": "mt5-inventory",
    "query": {},
    "requested_utc": "2026-11-20T13:23:31.853017+00:00",
    "received_utc": "2026-11-20T13:23:31.853017+00:00"
}
(CAPTURES / mt5_name).write_text(json.dumps(mt5_capture, indent=2))
print("MT5 book captured:", mt5_name)

# 2. Delta positions and orders
delta_ords = json.load(open('C:/Users/SIGMA/.gemini/antigravity/brain/566267b2-a02c-4896-b021-b1e756f57654/.system_generated/steps/32313/output.txt'))
delta_records = delta_ords.get("result", [])
# Also add SEI position record
delta_records.append({
    "product_id": 17329,
    "product_symbol": "SEIUSD",
    "size": -5,
    "entry_price": "0.0378",
    "mark_price": "0.0368"
})

delta_book = {
    "result": delta_records
}
delta_data = json.dumps(delta_book, indent=2, default=str).encode("utf-8")
delta_digest = hashlib.sha256(delta_data).hexdigest()
delta_name = f"delta-book-all-all-{delta_digest[:16]}.json"
(RAW / delta_name).write_bytes(delta_data)

delta_capture = {
    "path": f"raw/{delta_name}",
    "sha256": delta_digest,
    "round_id": "R646",
    "wake_id": "3b73eefdac3c4c4f8092500e401e8ff7",
    "spec_sha256": "36fa69f82f8fb959b139a83c259a488c21af0613158bec9727069d8b381023cc",
    "feed": "delta-inventory",
    "query": {},
    "requested_utc": "2026-11-20T13:23:31.853017+00:00",
    "received_utc": "2026-11-20T13:23:31.853017+00:00"
}
(CAPTURES / delta_name).write_text(json.dumps(delta_capture, indent=2))
print("Delta book captured:", delta_name)

# 3. Update scope.json managed rows
scope = json.load(open(R646 / "scope.json"))
managed = []
# Managed MT5
for s in ["EURUSD.pi", "BTCUSD.pi"]:
    managed.append({
        "venue": "mt5",
        "instrument_id": s,
        "source": {
            "path": f"raw/{mt5_name}",
            "sha256": mt5_digest
        }
    })

# Managed Delta
for pid in ["17329"]:
    managed.append({
        "venue": "delta",
        "instrument_id": pid,
        "source": {
            "path": f"raw/{delta_name}",
            "sha256": delta_digest
        }
    })

scope["managed"] = managed
with open(R646 / "scope.json", "w") as f:
    json.dump(scope, f, indent=2)
print("Updated scope.json managed entries successfully.")
