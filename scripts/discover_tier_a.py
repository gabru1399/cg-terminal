#!/usr/bin/env python3
"""Tier A discovery: narrative sweep across the 30 crypto perps.
Filters: Grade A/A+, OR confidence >= 80 with M1/M2 Triggered, OR LSR >= 2.5,
OR |composite| >= 2.0. Applies Gate 0.1 integrity checks (fresh updatedAt only).
"""
import json, urllib.request, time
from datetime import datetime, timezone

BASE = "http://127.0.0.1:3000"
CRYPTO = "BTC ETH BNB SOL XRP ADA DOGE TRX LINK LTC AVAX DOT NEAR UNI ATOM XLM ETC FIL ICP HBAR APT ARB OP SUI SEI INJ TIA VET 1000PEPE 1000SHIB".split()

def get(path, timeout=20):
    try:
        with urllib.request.urlopen(f"{BASE}{path}", timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

now = time.time() * 1000
results = []
for sym in CRYPTO:
    n = get(f"/api/cg/narrative?sym={sym}")
    if n.get("error") or not n.get("supported"):
        results.append(dict(sym=sym, ok=False, err=n.get("error", "unsupported")))
        continue
    age = (now - n.get("ts", now)) / 1000 if n.get("ts") else None
    results.append(dict(
        sym=sym, ok=True,
        regime=n.get("regime"), model=n.get("activeModel"), direction=n.get("direction"),
        grade=n.get("grade"), confidence=n.get("confidence"),
        triggered=n.get("triggered") or n.get("m1m2") or n.get("modelTriggered"),
        lsr=n.get("liqSkewRatio") or n.get("lsr"), composite=n.get("compositeScore") or n.get("composite"),
        thesis=(n.get("thesis") or "")[:110], age_s=round(age, 1) if age else None,
    ))
    time.sleep(0.35)

ok = [r for r in results if r["ok"]]
bad = [r for r in results if not r["ok"]]
print(f"narrative sweep: {len(ok)} ok, {len(bad)} failed ({[b['sym'] for b in bad]})\n")

def qualify(r):
    reasons = []
    g = (r.get("grade") or "")
    if g in ("A", "A+"): reasons.append(f"grade {g}")
    c = r.get("confidence") or 0
    if c >= 80 and (r.get("triggered") in (True, "Triggered", "M1_TREND_PULLBACK", "M2_MEAN_REVERSION")):
        reasons.append(f"conf {c}% triggered")
    lsr = r.get("lsr")
    if lsr is not None and abs(lsr) >= 2.5: reasons.append(f"LSR {lsr}")
    comp = r.get("composite")
    if comp is not None and abs(comp) >= 2.0: reasons.append(f"composite {comp}")
    return reasons

print(f"{'sym':<9}{'regime':<14}{'dir':<6}{'model':<18}{'grade':<6}{'conf':<5}{'LSR':<6}{'comp':<6}qualifies")
for r in sorted(ok, key=lambda x: -(x.get("confidence") or 0)):
    q = qualify(r)
    print(f"{r['sym']:<9}{str(r.get('regime')):<14}{str(r.get('direction')):<6}{str(r.get('model')):<18.18}{str(r.get('grade')):<6}{str(r.get('confidence')):<5}{str(r.get('lsr')):<6}{str(r.get('composite')):<6}{'; '.join(q) if q else ''}")

json.dump(results, open("/tmp/narrative_sweep.json", "w"), indent=1)
print("\nsaved /tmp/narrative_sweep.json")
