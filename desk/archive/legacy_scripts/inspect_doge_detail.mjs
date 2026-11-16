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

async function auditDOGE() {
  const sym = 'DOGE';
  const [mkt, fp, liq, sig, nar] = await Promise.all([
    fetchJson(`/api/cg/market?sym=${sym}`),
    fetchJson(`/api/cg/fp?sym=${sym}`),
    fetchJson(`/api/cg/liqlevels?sym=${sym}`),
    fetchJson(`/api/cg/signals?sym=${sym}`),
    fetchJson(`/api/cg/narrative?sym=${sym}`)
  ]);

  const price = Number(mkt.price.last);
  const dayPoc = Number(mkt.auction?.day?.poc || 0);
  const dayVah = Number(mkt.auction?.day?.vah || 0);
  const dayVal = Number(mkt.auction?.day?.val || 0);
  const sessPoc = Number(mkt.auction?.session?.poc || 0);
  const vwap = Number(mkt.vwap?.vwap || 0);

  console.log(`DOGE Price: $${price} | Day VAH: $${dayVah} | Day POC: $${dayPoc} | Day VAL: $${dayVal} | Sess POC: $${sessPoc} | VWAP: $${vwap.toFixed(5)}`);

  // Candidate setup: Sell limit at 0.05945 (Day VAH / SDIV sell extreme)
  const entry = 0.05945;
  const sl = 0.05990; // above 0.05980 Day High + buffer
  const tp = 0.05850; // Day POC / VAL path
  const risk = sl - entry;
  const reward = entry - tp;
  const rMult = reward / risk;

  console.log(`Setup: Entry=$${entry} | SL=$${sl} | TP=$${tp} | Risk=$${risk.toFixed(5)} | Reward=$${reward.toFixed(5)} | R=${rMult.toFixed(2)}R`);

  // Gate 1 clearance
  const dDay = Math.abs(sl - dayPoc) / dayPoc * 100;
  const dSess = Math.abs(sl - sessPoc) / sessPoc * 100;
  const dVwap = Math.abs(sl - vwap) / vwap * 100;

  // Active footprint bar POCs in last 32 bars
  const bars = fp?.bars || [];
  let activeHvn = 0;
  for (const b of bars.slice(-32)) {
    const pocP = Number(b.poc || b.p || 0);
    if (pocP > 0 && Math.abs(sl - pocP) / pocP * 100 < 0.5) {
      activeHvn++;
    }
  }

  // Gate 2 liquidation
  const above = liq?.stats?.keyLevels?.above || [];
  const hazard = above.filter(c => entry < Number(c.price) && Number(c.price) <= sl * 1.005);
  const hazardUsd = hazard.reduce((acc, c) => acc + Number(c.usd || 0), 0);

  console.log(`Gate 1: Day POC dist=${dDay.toFixed(2)}%, Sess POC dist=${dSess.toFixed(2)}%, VWAP dist=${dVwap.toFixed(2)}%, Active HVNs=${activeHvn}`);
  console.log(`Gate 2: Hazard USD=$${hazardUsd.toLocaleString()}`);
  console.log(`All Above Liq Levels:`, above);
}

auditDOGE();
