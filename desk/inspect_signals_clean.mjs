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

async function inspectSignals(sym) {
  const [mkt, sig, liq] = await Promise.all([
    fetchJson(`/api/cg/market?sym=${sym}`),
    fetchJson(`/api/cg/signals?sym=${sym}`),
    fetchJson(`/api/cg/liqlevels?sym=${sym}`)
  ]);

  const price = Number(mkt?.price?.last || 0);
  const sets = sig?.sets || [];
  const allSigs = sets.flatMap(s => s.sigs || []);
  const now = Date.now() / 1000;
  const recent = allSigs.filter(s => (now - s.ts) <= 8 * 3600);

  console.log(`\n=== SIGNALS FOR ${sym} (Live Price: $${price}) ===`);
  console.log(`Total 8h signals: ${recent.length}`);
  for (const s of recent.slice(-8)) {
    const ageMin = Math.round((now - s.ts) / 60);
    console.log(`  [${s.t.toUpperCase()} ${s.side.toUpperCase()}] @ $${s.p} ($${Math.round(s.u || 0).toLocaleString()} USD, ${ageMin}m ago, ${s.bt})`);
  }

  // Check liquidations
  const above = liq?.stats?.keyLevels?.above || [];
  const below = liq?.stats?.keyLevels?.below || [];
  const liqAbove1Pct = above.filter(l => Number(l.price) <= price * 1.02).reduce((a, b) => a + Number(b.usd || 0), 0);
  const liqBelow1Pct = below.filter(l => Number(l.price) >= price * 0.98).reduce((a, b) => a + Number(b.usd || 0), 0);
  console.log(`Liquidation context: Overhead (0-2%) = $${Math.round(liqAbove1Pct).toLocaleString()} | Below (0-2%) = $${Math.round(liqBelow1Pct).toLocaleString()}`);
}

async function main() {
  for (const s of ['LTC', 'DOGE', 'XRP', 'NEAR', 'TRX', 'SOL']) {
    await inspectSignals(s);
  }
}

main();
