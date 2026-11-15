import fs from 'fs';

async function fetchJson(endpoint) {
  try {
    const res = await fetch(`http://127.0.0.1:3000${endpoint}`, { signal: AbortSignal.timeout(4000) });
    if (!res.ok) return null;
    return await res.json();
  } catch (e) {
    return null;
  }
}

async function audit(sym, s) {
  console.log(`\n=================== DETAILED AUDIT FOR ${sym} ===================`);
  const [mkt, fp, liq, sig, nar, cvd] = await Promise.all([
    fetchJson(`/api/cg/market?sym=${sym}`),
    fetchJson(`/api/cg/fp?sym=${sym}`),
    fetchJson(`/api/cg/liqlevels?sym=${sym}`),
    fetchJson(`/api/cg/signals?sym=${sym}`),
    fetchJson(`/api/cg/narrative?sym=${sym}`),
    fetchJson(`/api/cg/cvd?sym=${sym}`)
  ]);

  const price = Number(mkt.price.last);
  const entry = s.entry;
  const sl = s.sl;
  const tp = s.tp;
  const risk = sl - entry;
  const reward = entry - tp;
  const rMult = reward / risk;

  const dayPoc = Number(mkt.auction?.day?.poc || 0);
  const dayVah = Number(mkt.auction?.day?.vah || 0);
  const dayVal = Number(mkt.auction?.day?.val || 0);
  const sessPoc = Number(mkt.auction?.session?.poc || 0);
  const vwap = Number(mkt.vwap?.vwap || 0);

  // Gate 1: Check SL distance from 8h POC, Day POC, VWAP
  const dDay = Math.abs(sl - dayPoc) / dayPoc * 100;
  const dSess = Math.abs(sl - sessPoc) / sessPoc * 100;
  const dVwap = Math.abs(sl - vwap) / vwap * 100;
  const g1Pass = dDay >= 0.8 && dSess >= 0.8 && dVwap >= 0.8;

  // Active footprint bar POCs in last 32 bars
  const bars = fp?.bars || [];
  let activeHvn = 0;
  for (const b of bars.slice(-32)) {
    const pocP = Number(b.poc || b.p || 0);
    if (pocP > 0 && Math.abs(sl - pocP) / pocP * 100 < 0.5) {
      activeHvn++;
    }
  }

  // Gate 2: Liquidation risk
  const keyLevels = liq?.stats?.keyLevels || {};
  const above = keyLevels.above || [];
  const traversal = above.filter(c => price <= Number(c.price) && Number(c.price) <= entry);
  const hazard = above.filter(c => entry < Number(c.price) && Number(c.price) <= sl * 1.005);
  const traversalUsd = traversal.reduce((acc, c) => acc + Number(c.usd || 0), 0);
  const hazardUsd = hazard.reduce((acc, c) => acc + Number(c.usd || 0), 0);
  const g2Pass = hazardUsd < 2000000;

  console.log(`Price: $${price} | Day VAH: $${dayVah} | Day POC: $${dayPoc} | Day VAL: $${dayVal} | Sess POC: $${sessPoc} | VWAP: $${vwap.toFixed(4)}`);
  console.log(`Proposed Setup: Entry=$${entry} | SL=$${sl} | TP=$${tp} | R=${rMult.toFixed(2)}R`);
  console.log(`Gate 1: Day POC dist=${dDay.toFixed(2)}%, Sess POC dist=${dSess.toFixed(2)}%, VWAP dist=${dVwap.toFixed(2)}%, Active HVNs=${activeHvn} -> ${g1Pass && activeHvn === 0 ? 'PASS' : 'FAIL'}`);
  console.log(`Gate 2: Traversal Fuel=$${Math.round(traversalUsd).toLocaleString()} | Hazard USD=$${Math.round(hazardUsd).toLocaleString()} -> ${g2Pass ? 'PASS' : 'FAIL'}`);

  return { sym, g1Pass: g1Pass && activeHvn === 0, g2Pass, rMult, traversalUsd, hazardUsd, dDay, dSess, dVwap };
}

async function main() {
  // LTC: Sell Limit at 45.48 (at/above Day VAH 45.38, Sess POC 45.46), SL 45.85, TP 44.65 (Day POC retest)
  const ltc = await audit('LTC', { entry: 45.48, sl: 45.85, tp: 44.65 });

  // XRP: Sell Limit at 0.9780 (at Day VAH 0.9782, trap cluster 0.9777), SL 0.9860, TP 0.9620 (Day POC retest)
  const xrp = await audit('XRP', { entry: 0.9780, sl: 0.9860, tp: 0.9620 });
}

main();
