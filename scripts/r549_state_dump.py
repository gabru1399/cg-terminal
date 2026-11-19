#!/usr/bin/env python3
"""R549 ENGINE round — fresh sweep of desk state, orders, positions."""
import json, time

d = json.load(open("desk/state.json"))

def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None

upd = num(d.get("updatedAt"))
print("updatedAt:", d.get("updatedAt"), "| age min:", round((time.time() * 1000 - upd) / 60000, 1) if upd else "?")
print("== orders (last 12) ==")
for o in d.get("orders", [])[-12:]:
    print(f"  {str(o.get('id'))[:16]:16} {str(o.get('sym')):7} {str(o.get('side')):5} {str(o.get('type')):6} status={str(o.get('status')):12} ticket={o.get('ticket')}")
    print(f"     entry={o.get('entry')} sl={o.get('stop')} tp={o.get('targets')} venue={o.get('venue', '?')} src={o.get('source', o.get('mode', '?'))}")
print("== positions ==")
for p in d.get("positions", []):
    print(f"  {str(p.get('sym')):8} {str(p.get('side')):5} qty={p.get('qty')} entry={p.get('entry')} sl={p.get('sl', p.get('stop'))} tp={p.get('tp')} venue={p.get('venue', '?')} ticket={p.get('ticket')}")
print("== account ==")
print(json.dumps(d.get("account", {}), indent=1)[:400])
