import json
import time

with open("desk/state.json", "r") as f:
    state = json.load(f)

for o in state.get("orders", []):
    t = o.get("ticket")
    if t == 1680974187:
        o["entry"] = 1844.0
        o["stop"] = 1875.0
        o["targets"] = [1780.0]
        o["r_multiple"] = 2.06
        o["notes"] = "Tuned to Day VAL shelf retest (shallow pullback optimization)"
        o["updated_at"] = int(time.time() * 1000)
    elif t == 1680977628:
        o["entry"] = 9.280
        o["stop"] = 9.450
        o["targets"] = [8.900]
        o["r_multiple"] = 2.23
        o["notes"] = "Tuned to Day VAL shelf retest (shallow pullback optimization)"
        o["updated_at"] = int(time.time() * 1000)
    elif t == 1681187234:
        o["entry"] = 0.7420
        o["stop"] = 0.7620
        o["targets"] = [0.6980]
        o["r_multiple"] = 2.20
        o["notes"] = "Tuned to Day VAL shelf retest (shallow pullback optimization)"
        o["updated_at"] = int(time.time() * 1000)
    elif t == 1681189148:
        o["entry"] = 46.25
        o["stop"] = 47.10
        o["targets"] = [44.10]
        o["r_multiple"] = 2.53
        o["notes"] = "Tuned to Day VAL shelf retest (shallow pullback optimization)"
        o["updated_at"] = int(time.time() * 1000)

with open("desk/state.json", "w") as f:
    json.dump(state, f, indent=2)

print("Updated desk/state.json successfully!")
