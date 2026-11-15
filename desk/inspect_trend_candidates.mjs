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

async function inspect(sym, prodId, contractVal, tick) {
  console.log(`\n=================== AUDIT CANDIDATE: ${sym} ===================`);
  const [mkt, fp, liq, sig, nar] = await Promise.all([
    fetchJson(`/api/cg/market?sym=${sym}`),
    fetchJson(`/api/cg/fp?sym=${sym}`),
    fetchJson(`/api/cg/liqlevels?sym=${sym}`),
    fetchJson(`/api/cg/signals?sym=${sym}`),
    fetchJson(`/api/cg/narrative?sym=${sym}`)
  ]);

  if (!mkt || !mkt.price) {
    console.log(`No market data for ${sym}`);
    return;
  }

  const price = Number(mkt.price.last);
  const dayPoc = Number(mkt.auction?.day?.poc || 0);
  const dayVah = Number(mkt.auction?.day?.vah || 0);
  const dayVal = Number(mkt.auction?.day?.val || 0);
  const sessPoc = Number(mkt.auction?.session?.poc || 0);
  const vwap = Number(mkt.vwap?.vwap || 0);

  console.log(`Price: $${price} | Day VAH: $${dayVah} | Day POC: $${dayPoc} | Day VAL: $${dayVal} | Sess POC: $${sessPoc} | VWAP: $${vwap.toFixed(5)}`);
  console.log(`Regime: ${nar?.m1m2?.regime} | Model: ${nar?.m1m2?.activeModel} ${nar?.m1m2?.direction} (${nar?.m1m2?.confidence}%)`);

  const sigs = (sig?.sets || []).flatMap(s => s.sigs || []);
  const now = Date.now() / 1000;
  const recentSigs = sigs.filter(s => (now - s.ts) <= 8 * 3600);
  console.log(`Recent 8h Signals (${recentSigs.length}):`);
  for (const s of recentSigs.slice(-6)) {
    const age = Math.round((now - s.ts) / 60);
    console.log(`  [${s.t.toUpperCase()} ${s.side.toUpperCase()}] @ $${s.p} ($${Math.round(s.u || 0).toLocaleString()} USD, ${age}m ago, ${s.bt})`);
  }

  const above = liq?.stats?.keyLevels?.above || [];
  const below = liq?.stats?.keyLevels?.below || [];
  console.log('Overhead Liq Levels (above):', above.slice(0, 4));
  console.log('Downside Liq Levels (below):', below.slice(0, 4));
}

async function main() {
  await inspect('FIL', 19617, 1.0, 0.0001);
  await inspect('APT', 20196, 1.0, 0.0001);
  await inspect('OP', 19618, 0.1, 0.0001);
}

main();
