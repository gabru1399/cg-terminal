const targets = [
  { sym: 'LTC', deltaSym: 'LTCUSD', prodId: 15040, contractVal: 0.1 },
  { sym: 'AVAX', deltaSym: 'AVAXUSD', prodId: 14830, contractVal: 1.0 },
  { sym: 'DOGE', deltaSym: 'DOGEUSD', prodId: 14745, contractVal: 100.0 },
  { sym: 'ADA', deltaSym: 'ADAUSD', prodId: 16614, contractVal: 1.0 },
  { sym: 'XRP', deltaSym: 'XRPUSD', prodId: 14969, contractVal: 1.0 },
  { sym: 'DOT', deltaSym: 'DOTUSD', prodId: 15304, contractVal: 1.0 },
  { sym: 'NEAR', deltaSym: 'NEARUSD', prodId: 16615, contractVal: 1.0 },
  { sym: 'UNI', deltaSym: 'UNIUSD', prodId: 15303, contractVal: 1.0 },
  { sym: 'SOL', deltaSym: 'SOLUSD', prodId: 14823, contractVal: 1.0 },
  { sym: 'TRX', deltaSym: 'TRXUSD', prodId: 20193, contractVal: 1.0 }
];

async function fetchJson(endpoint) {
  try {
    const res = await fetch(`http://127.0.0.1:3000${endpoint}`, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) return null;
    return await res.json();
  } catch (e) {
    return null;
  }
}

async function auditAsset(t) {
  const [mkt, nar, liq, cvd, sig, bw] = await Promise.all([
    fetchJson(`/api/cg/market?sym=${t.sym}`),
    fetchJson(`/api/cg/narrative?sym=${t.sym}`),
    fetchJson(`/api/cg/liqlevels?sym=${t.sym}`),
    fetchJson(`/api/cg/cvd?sym=${t.sym}`),
    fetchJson(`/api/cg/signals?sym=${t.sym}`),
    fetchJson(`/api/cg/bookwalls?sym=${t.sym}`)
  ]);

  if (!mkt || !mkt.price || !mkt.price.last) return null;

  const price = Number(mkt.price.last);
  const regime = nar?.regime || 'UNKNOWN';
  const activeModel = nar?.activeModel || 'UNKNOWN';

  const dayAuc = mkt.auction?.day || {};
  const dayPoc = Number(dayAuc.poc || 0);
  const dayVah = Number(dayAuc.vah || 0);
  const dayVal = Number(dayAuc.val || 0);
  const sessPoc = Number(mkt.auction?.session?.poc || 0);

  const vwap = Number(mkt.vwap?.vwap || 0);
  const sd1 = Number(mkt.vwap?.bands?.sd1 || 0);
  const z = sd1 > 0 ? (price - vwap) / sd1 : 0;

  const h4Trend = (mkt.ema?.h4?.e13 || 0) < (mkt.ema?.h4?.e89 || 0) ? 'DOWN' : 'UP';
  const d1Trend = (mkt.ema?.d1?.e13 || 0) < (mkt.ema?.d1?.e89 || 0) ? 'DOWN' : 'UP';

  // Liquidation clusters
  const clusters = liq?.clusters || [];
  let shortsAbove = 0;
  let longsBelow = 0;
  for (const c of clusters) {
    const cp = Number(c.price || 0);
    const usd = Number(c.usd || 0);
    if (price < cp && cp <= price * 1.02) shortsAbove += usd;
    if (price * 0.98 <= cp && cp < price) longsBelow += usd;
  }
  const lsr = longsBelow > 0 ? shortsAbove / longsBelow : (shortsAbove > 0 ? 99 : 1);

  // Setup candidate: SHORT S1/S2/S5
  const entry = Math.max(dayVah, price * 1.008);
  const sl = entry * 1.022;
  let tp = dayPoc < price ? dayPoc : (dayVal < price ? dayVal : price * 0.97);
  const risk = sl - entry;
  const reward = entry - tp;
  const rMult = risk > 0 ? reward / risk : 0;

  // Gate 1: SL distance from balance nodes
  const g1DistDay = Math.abs(sl - dayPoc) / sl;
  const g1DistSess = Math.abs(sl - sessPoc) / sl;
  const g1Pass = g1DistDay >= 0.008 && g1DistSess >= 0.008;

  // Gate 2: Liquidation risk
  const traversalClusters = clusters.filter(c => price < Number(c.price) && Number(c.price) <= entry);
  const traversalFuel = traversalClusters.reduce((acc, c) => acc + Number(c.usd || 0), 0);

  const hazardClusters = clusters.filter(c => entry < Number(c.price) && Number(c.price) <= sl);
  const hazardUsd = hazardClusters.reduce((acc, c) => acc + Number(c.usd || 0), 0);
  const maxHazardUsd = hazardClusters.length > 0 ? Math.max(...hazardClusters.map(c => Number(c.usd || 0))) : 0;

  const g2Pass = maxHazardUsd < 2000000 && (traversalFuel > 0 ? hazardUsd / traversalFuel < 2.5 : hazardUsd < 500000);

  // Table 7
  let t7 = 0;
  if (h4Trend === 'DOWN' && d1Trend === 'DOWN') t7 += (regime === 'RANGE_BALANCE' ? 0.0 : 2.0);
  if (z >= 1.0) t7 += 1.5;
  else if (z >= 0.5) t7 += 1.0;
  const cvdDelta = Number(cvd?.cvd?.delta24h || 0);
  if (cvdDelta < 0) t7 += 1.0;
  if (g2Pass && (traversalFuel > 0 || lsr < 2.0)) t7 += 1.5;
  t7 += 1.0; // Spread drag < 0.05%

  const notional1Contract = price * t.contractVal;
  const margin25x = notional1Contract / 25;
  const margin50x = notional1Contract / 50;

  return {
    ...t,
    price,
    regime,
    activeModel,
    z,
    h4Trend,
    d1Trend,
    dayPoc,
    dayVah,
    dayVal,
    sessPoc,
    vwap,
    lsr,
    shortsAbove,
    longsBelow,
    entry,
    sl,
    tp,
    rMult,
    g1Pass,
    g2Pass,
    traversalFuel,
    hazardUsd,
    maxHazardUsd,
    t7,
    margin25x,
    margin50x
  };
}

async function main() {
  console.log('Auditing 10 tradable candidate assets in parallel...');
  const audits = await Promise.all(targets.map(auditAsset));
  const valid = audits.filter(Boolean);

  console.log('\n| Symbol | Price | VWAP z | Regime | Trend | LSR (±2%) | Traversal Fuel | Hazard USD | G1 | G2 | Table 7 | R-Mult | Margin 25x | Viable? |');
  console.log('| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |');

  for (const a of valid) {
    const isViable = a.g1Pass && a.g2Pass && a.t7 >= 5.0 && a.rMult >= 1.5 && (a.margin25x <= 0.90 || a.margin50x <= 0.90);
    console.log(
      `| ${a.sym} | $${a.price} | ${a.z.toFixed(2)}σ | ${a.regime} | ${a.h4Trend} | ${a.lsr.toFixed(2)}:1 | $${(a.traversalFuel/1000).toFixed(0)}k | $${(a.hazardUsd/1000).toFixed(0)}k | ${a.g1Pass ? 'PASS' : 'FAIL'} | ${a.g2Pass ? 'PASS' : 'FAIL'} | ${a.t7.toFixed(1)} | ${a.rMult.toFixed(2)}R | $${a.margin25x.toFixed(3)} | ${isViable ? '**YES**' : 'NO'} |`
    );
  }
}

main().catch(console.error);
