import urllib.request
import json

base_url = "http://127.0.0.1:3000"

# Fetch DOT footprint
req = urllib.request.Request(f"{base_url}/api/cg/fp?sym=DOT&limit=20")
with urllib.request.urlopen(req) as resp:
    fp_data = json.loads(resp.read().decode('utf-8'))

bars = fp_data.get("bars", [])
pocs = []
for b in bars:
    fp = b.get("fp")
    if not fp:
        continue
    lo = fp.get("lo", 0)
    tick = fp.get("tick", 1)
    buys = fp.get("b", [])
    sells = fp.get("s", [])
    max_v = -1
    poc_p = None
    for i in range(min(len(buys), len(sells))):
        v = buys[i] + sells[i]
        if v > max_v:
            max_v = v
            poc_p = lo + i * tick
    if poc_p:
        pocs.append({"poc": poc_p, "vol": max_v, "ts": b.get("ts")})

entry = 0.7480
sl = 0.7550
tp = 0.7180

# Gate 1: Check SL distance from all session POCs
print(f"Proposed Trade: SELL LIMIT @ {entry} | SL @ {sl} | TP @ {tp}")
print(f"Risk: {sl - entry:.4f} ({(sl-entry)/entry*100:.2f}%) | Reward: {entry - tp:.4f} ({(entry-tp)/entry*100:.2f}%) | R:R = {(entry-tp)/(sl-entry):.2f}R")

gate1_pass = True
min_dist_pct = 999.0
colliding_poc = None

for p in pocs:
    dist_pct = abs(sl - p["poc"]) / p["poc"] * 100
    if dist_pct < min_dist_pct:
        min_dist_pct = dist_pct
        colliding_poc = p
    if dist_pct < 0.25:
        gate1_pass = False

print(f"\nGate 1 (Active Session POC Clearance):")
print(f"  Nearest Session POC: {colliding_poc['poc']} | Distance to SL: {min_dist_pct:.3f}% (Threshold: >0.25%)")
print(f"  Result: {'PASS' if gate1_pass else 'FAIL'}")

# Gate 2: Risk Zone Purity (0.7480 to 0.7550)
hazard_pocs = [p for p in pocs if entry <= p["poc"] <= sl]
gate2_pass = len(hazard_pocs) == 0
print(f"\nGate 2 (Risk Zone Purity [0.7480 - 0.7550]):")
print(f"  POCs inside Risk Zone: {len(hazard_pocs)}")
for h in hazard_pocs:
    print(f"    Hazard POC: {h['poc']} (Vol: {h['vol']:.1f})")
print(f"  Result: {'PASS' if gate2_pass else 'FAIL'}")

if gate1_pass and gate2_pass:
    print("\nALL CANONICAL AUDIT GATES PASSED! TRADE IS VERIFIED FOR CLOB PLACEMENT.")
else:
    print("\nAUDIT FAILED! DO NOT PLACE ORDER.")
