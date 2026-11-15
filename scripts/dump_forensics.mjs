import fs from 'fs';

const syms = ['ETH', 'LINK', 'SUI', 'LTC', 'BTC'];

async function getJson(url) {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 3500);
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeout);
    if (!res.ok) return null;
    return await res.json();
  } catch (e) {
    return null;
  }
}

async function main() {
  const results = {};
  for (const sym of syms) {
    console.log(`Fetching ${sym}...`);
    const market = await getJson(`http://127.0.0.1:3000/api/cg/market?sym=${sym}`);
    const signals = await getJson(`http://127.0.0.1:3000/api/cg/signals?sym=${sym}`);
    const fp = await getJson(`http://127.0.0.1:3000/api/cg/fp?sym=${sym}`);
    const liq = await getJson(`http://127.0.0.1:3000/api/cg/liqlevels?sym=${sym}`);
    const bookwalls = await getJson(`http://127.0.0.1:3000/api/cg/bookwalls?sym=${sym}`);
    const cvd = await getJson(`http://127.0.0.1:3000/api/cg/cvd?sym=${sym}`);
    results[sym] = { market, signals, fp, liq, bookwalls, cvd };
  }
  fs.writeFileSync('scripts/forensics_dump.json', JSON.stringify(results, null, 2));
  console.log('Forensics dump written successfully.');
}

main().catch(console.error);
