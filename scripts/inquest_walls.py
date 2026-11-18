#!/usr/bin/env python3
"""Aggregate bookwall depth imbalance + confirmed walls (model.depth / model.walls)."""
import json

out = {}
for s in ['TIA','ADA','ARB','SEI','APT','DOGE','VET','NVDA','XAU','MSFT','MSTR','AVGO']:
    try:
        d = json.load(open(f'/tmp/bw_{s}.json'))
        m = d.get('model', {})
        depth = m.get('depth', {})
        bid, ask = depth.get('bidUsd', 0), depth.get('askUsd', 0)
        imb = round((bid - ask) / (bid + ask), 3) if (bid + ask) else None
        walls = m.get('walls') or []
        ws = []
        for w in walls[:4]:
            ws.append(f"{w.get('side')} {w.get('price')} ${round((w.get('usd') or 0)/1e6, 2)}M {round((w.get('ageMs') or 0)/3.6e6, 1)}h {'T' if w.get('touched') else '-'}")
        out[s] = {"imb": imb, "bidUsd_M": round(bid/1e6, 2), "askUsd_M": round(ask/1e6, 2), "walls": ws}
        print(f"{s:5} imb±5%={imb} bid${round(bid/1e6,1)}M ask${round(ask/1e6,1)}M | walls: {ws}")
    except Exception as e:
        print(s, 'ERR', str(e)[:50])

json.dump(out, open('/tmp/inquest_walls.json', 'w'), indent=1)
print('saved')
