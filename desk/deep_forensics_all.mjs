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

async function inspect(sym) {
  const [mkt, nar, liq, cvd, sig, bw] = await Promise.all([
    fetchJson(`/api/cg/market?sym=${sym}`),
    fetchJson(`/api/cg/narrative?sym=${sym}`),
    fetchJson(`/api/cg/liqlevels?sym=${sym}`),
    fetchJson(`/api/cg/cvd?sym=${sym}`),
    fetchJson(`/api/cg/signals?sym=${sym}`),
    fetchJson(`/api/cg/bookwalls?sym=${sym}`)
  ]);

  return { sym, mkt, nar, liq, cvd, sig, bw };
}

async function run() {
  const syms = ['LINK', 'DOT', 'AVAX', 'UNI', 'TRX', 'DOGE', 'LTC', 'ADA', 'NEAR', 'XRP'];
  const results = {};

  for (const s of syms) {
    results[s] = await inspect(s);
    console.log(`Inspected ${s}`);
  }

  fs.writeFileSync('desk/deep_telemetry.json', JSON.stringify(results, null, 2));
  console.log('Saved desk/deep_telemetry.json');
}

run();
