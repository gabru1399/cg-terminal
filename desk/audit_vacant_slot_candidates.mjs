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

async function auditCandidate(sym, prodId, contractVal, tick) {
  console.log(`\n=================== AUDITING CANDIDATE: ${sym} ===================`);
  const [mkt, fp, liq, sig, nar, bw] = await Promise.all([
    fetchJson(`/api/cg/market?sym=${sym}`),
    fetchJson(`/api/cg/fp?sym=${sym}`),
    fetchJson(`/api/cg/liqlevels?sym=${sym}`),
    fetchJson(`/api/cg/signals?sym=${sym}`),
    fetchJson(`/api/cg/narrative?sym=${sym}`),
    fetchJson(`/api/cg/bookwalls?sym=${sym}`)
  ]);

  if (!mkt || !mkt.price) {
    console.log(`Failed to load market data for ${sym}`);
    return null;
  }

  const price = Number(mkt.price.last);
  const dayPoc = Number(mkt.auction?.day?.poc || 0);
  const dayVah = Number(mkt.auction?.day?.vah || 0);
  const dayVal = Number(mkt.auction?.day?.val || 0);
  const sessPoc = Number(mkt.auction?.session?.poc || 0);
  const vwap = Number(mkt.vwap?.vwap || 0);
  const vwapSd1 = Number(mkt.vwap?.bands?.sd1 || 0);

  // Recent discrete footprint signals (last 8h)
  const sigs = (sig && sig.sets) ? sig.sets.flatMap(s => s.sigs || []) : [];
  const recentSigs = sigs.filter(s => (Date.now() / 1000 - s.ts) <= 8 * 3600);

  // Liquidation key levels
  const keyLevels = liq?.stats?.keyLevels || {};
  const above = keyLevels.above || [];
  const below = keyLevels.below || [];

  console.log(`Price: $${price} | Day VAH: $${dayVah} | Day POC: $${dayPoc} | Day VAL: $${dayVal} | Sess POC: $${sessPoc} | VWAP: $${vwap.toFixed(4)}`);
  console.log(`Recent Signals (${recentSigs.length}):`, recentSigs.map(s => `${s.title}/${s.side} @ ${s.price} (${Math.round((Date.now()/1000 - s.ts)/60)}m ago)`).join(' | ') || 'none');

  // Let's test a mean-reversion short from Day VAH / +1sd VWAP back to Day POC
  // Or a sweep reversal if there's absorption
  const absSells = recentSigs.filter(s => s.side === 'sell' && (s.title === 'Absorption' || s.title === 'Strong Divergence'));
  console.log(`Bearish Absorption/SDIV signals count: ${absSells.length}`);

  return { sym, prodId, contractVal, tick, price, dayPoc, dayVah, dayVal, sessPoc, vwap, vwapSd1, recentSigs, above, below };
}

async function main() {
  const candidates = [
    { sym: 'LTC', prodId: 15040, contractVal: 0.1, tick: 0.01 },
    { sym: 'DOGE', prodId: 14745, contractVal: 100.0, tick: 0.000001 },
    { sym: 'XRP', prodId: 14969, contractVal: 1.0, tick: 0.0001 },
    { sym: 'NEAR', prodId: 16615, contractVal: 1.0, tick: 0.0001 },
    { sym: 'TRX', prodId: 20193, contractVal: 1.0, tick: 0.00001 }
  ];

  const results = [];
  for (const c of candidates) {
    const res = await auditCandidate(c.sym, c.prodId, c.contractVal, c.tick);
    if (res) results.push(res);
  }

  fs.writeFileSync('desk/vacant_candidates.json', JSON.stringify(results, null, 2));
}

main();
