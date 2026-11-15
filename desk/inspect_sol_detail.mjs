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

async function inspectSOL() {
  const sym = 'SOL';
  const [mkt, fp, liq, sig, nar, cvd, bw] = await Promise.all([
    fetchJson(`/api/cg/market?sym=${sym}`),
    fetchJson(`/api/cg/fp?sym=${sym}`),
    fetchJson(`/api/cg/liqlevels?sym=${sym}`),
    fetchJson(`/api/cg/signals?sym=${sym}`),
    fetchJson(`/api/cg/narrative?sym=${sym}`),
    fetchJson(`/api/cg/cvd?sym=${sym}`),
    fetchJson(`/api/cg/bookwalls?sym=${sym}`)
  ]);

  console.log('=== SOL TELEMETRY ===');
  console.log('Price:', mkt?.price?.last);
  console.log('Auction Profile: Day VAH:', mkt?.auction?.day?.vah, 'Day POC:', mkt?.auction?.day?.poc, 'Day VAL:', mkt?.auction?.day?.val, 'Sess POC:', mkt?.auction?.session?.poc, 'VWAP:', mkt?.vwap?.vwap);
  console.log('Regime:', nar?.m1m2?.regime, 'Active Model:', nar?.m1m2?.activeModel, 'Dir:', nar?.m1m2?.direction, 'Conf:', nar?.m1m2?.confidence);

  const sigs = (sig?.sets || []).flatMap(s => s.sigs || []);
  const now = Date.now() / 1000;
  const recentSigs = sigs.filter(s => (now - s.ts) <= 8 * 3600);
  console.log(`Recent 8h Signals (${recentSigs.length}):`);
  for (const s of recentSigs.slice(-8)) {
    const age = Math.round((now - s.ts) / 60);
    console.log(`  [${s.t.toUpperCase()} ${s.side.toUpperCase()}] @ $${s.p} ($${Math.round(s.u || 0).toLocaleString()} USD, ${age}m ago, ${s.bt})`);
  }

  const above = liq?.stats?.keyLevels?.above || [];
  const below = liq?.stats?.keyLevels?.below || [];
  console.log('Overhead Liq Levels (above):', above.slice(0, 5));
  console.log('Downside Liq Levels (below):', below.slice(0, 5));
}

inspectSOL();
