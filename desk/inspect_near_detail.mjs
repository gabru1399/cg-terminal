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

async function auditNEAR() {
  const sym = 'NEAR';
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

  console.log(`NEAR Price: $${price} | Day VAH: $${dayVah} | Day POC: $${dayPoc} | Day VAL: $${dayVal} | Sess POC: $${sessPoc} | VWAP: $${vwap.toFixed(4)}`);

  const above = liq?.stats?.keyLevels?.above || [];
  const below = liq?.stats?.keyLevels?.below || [];
  console.log(`Above Liq Levels:`, above.slice(0, 5));
  console.log(`Below Liq Levels:`, below.slice(0, 5));

  // Check signals
  const sigs = (sig?.sets || []).flatMap(s => s.sigs || []);
  const now = Date.now() / 1000;
  const recent = sigs.filter(s => (now - s.ts) <= 8 * 3600);
  console.log(`Recent 8h Signals (${recent.length}):`, recent.slice(-5));
}

auditNEAR();
