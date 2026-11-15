const targets = [
  { sym: 'LTC', deltaSym: 'LTCUSD', prodId: 15040, contractVal: 0.1, tick: 0.01 },
  { sym: 'AVAX', deltaSym: 'AVAXUSD', prodId: 14830, contractVal: 1.0, tick: 0.0001 },
  { sym: 'DOGE', deltaSym: 'DOGEUSD', prodId: 14745, contractVal: 100.0, tick: 0.000001 },
  { sym: 'ADA', deltaSym: 'ADAUSD', prodId: 16614, contractVal: 1.0, tick: 0.00001 },
  { sym: 'XRP', deltaSym: 'XRPUSD', prodId: 14969, contractVal: 1.0, tick: 0.0001 },
  { sym: 'DOT', deltaSym: 'DOTUSD', prodId: 15304, contractVal: 1.0, tick: 0.001 },
  { sym: 'NEAR', deltaSym: 'NEARUSD', prodId: 16615, contractVal: 1.0, tick: 0.0001 },
  { sym: 'UNI', deltaSym: 'UNIUSD', prodId: 15303, contractVal: 1.0, tick: 0.0001 },
  { sym: 'SOL', deltaSym: 'SOLUSD', prodId: 14823, contractVal: 1.0, tick: 0.0001 },
  { sym: 'TRX', deltaSym: 'TRXUSD', prodId: 20193, contractVal: 1.0, tick: 0.00001 }
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
  const [mkt, nar, liq, cvd, sig] = await Promise.all([
    fetchJson(`/api/cg/market?sym=${t.sym}`),
    fetchJson(`/api/cg/narrative?sym=${t.sym}`),
    fetchJson(`/api/cg/liqlevels?sym=${t.sym}`),
    fetchJson(`/api/cg/cvd?sym=${t.sym}`),
    fetchJson(`/api/cg/signals?sym=${t.sym}`)
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

  // Liquidation keyLevels
  const keyLevels = liq?.stats?.keyLevels || {};
  const aboveClusters = keyLevels.above || [];
  const belowClusters = keyLevels.below || [];
  const bandsLiq = liq?.stats?.bands || [];

  let shorts2pct = 0;
  let longs2pct = 0;
  if (bandsLiq.length >= 2) {
    shorts2pct = Number(bandsLiq[0]?.up || 0) + Number(bandsLiq[1]?.up || 0);
    longs2pct = Number(bandsLiq[0]?.down || 0) + Number(bandsLiq[1]?.down || 0);
  }
  const lsr = longs2pct > 0 ? shorts2pct / longs2pct : (shorts2pct > 0 ? 99 : 1);

  // Footprint Signals
  const allSigs = [];
  if (sig?.sets) {
    for (const s of sig.sets) {
      if (s.sigs) allSigs.push(...s.sigs);
    }
  }
  allSigs.sort((a, b) => b.ts - a.ts);
  const recentBearSigs = allSigs.filter(s => ['sell', 'bear'].includes(s.side) && ['abs', 'sdiv', 'div', 'trap', 'exh'].includes(s.t));

  // Candidate Setup: SHORT S1
  const entry = Math.max(dayVah, price * 1.008);
  const sl = entry * 1.022;
  let tp = dayPoc < price ? dayPoc : (dayVal < price ? dayVal : price * 0.97);
  const risk = sl - entry;
  const reward = entry - tp;
  const rMult = risk > 0 ? reward / risk : 0;

  // Gate 1: SL clearance
  const g1DistDay = Math.abs(sl - dayPoc) / sl;
  const g1DistSess = Math.abs(sl - sessPoc) / sl;
  const g1DistVwap = Math.abs(sl - vwap) / sl;
  const g1Pass = g1DistDay >= 0.008 && g1DistSess >= 0.008 && g1DistVwap >= 0.008;

  // Gate 2: Liquidation risk
  const traversalClusters = aboveClusters.filter(c => price <= Number(c.price) && Number(c.price) <= entry);
  const hazardClusters = aboveClusters.filter(c => entry < Number(c.price) && Number(c.price) <= sl * 1.005);
  const traversalFuel = traversalClusters.reduce((acc, c) => acc + Number(c.usd || 0), 0);
  const hazardUsd = hazardClusters.reduce((acc, c) => acc + Number(c.usd || 0), 0);
  const maxHazard = hazardClusters.length > 0 ? Math.max(...hazardClusters.map(c => Number(c.usd || 0))) : 0;
  const g2Pass = maxHazard < 3000000 && (lsr < 2.5 || traversalFuel > hazardUsd);

  // Table 7 Scoring
  let t7 = 0;
  // Trend
  if (regime !== 'RANGE_BALANCE' && h4Trend === 'DOWN' && d1Trend === 'DOWN') t7 += 2.0;
  // VWAP
  if (z >= 1.0) t7 += 1.5;
  else if (z >= 0.5) t7 += 1.0;
  // Signal
  let sigBonus = 0;
  for (const s of recentBearSigs.slice(0, 5)) {
    const sp = Number(s.p || 0);
    if (Math.abs(sp - entry) / entry <= 0.02) {
      sigBonus = 2.0;
      break;
    } else if (Math.abs(sp - price) / price <= 0.015) {
      sigBonus = 1.0;
      break;
    }
  }
  t7 += sigBonus;
  // CVD
  const cvdDelta = Number(cvd?.cvd?.delta24h || 0);
  if (cvdDelta < 0) t7 += 1.0;
  // Magnet
  if (g2Pass && (traversalFuel > 0 || lsr < 2.0)) t7 += 1.5;
  // Spread
  t7 += 1.0;

  const notional1Contract = price * t.contractVal;
  const margin25x = notional1Contract / 25;
  const margin50x = notional1Contract / 50;

  const viable = g1Pass && g2Pass && t7 >= 5.0 && rMult >= 1.5 && margin25x <= 0.90;

  return {
    ...t,
    price,
    regime,
    z,
    h4Trend,
    dayPoc,
    dayVah,
    dayVal,
    sessPoc,
    vwap,
    lsr,
    entry,
    sl,
    tp,
    rMult,
    g1Pass,
    g2Pass,
    traversalFuel,
    hazardUsd,
    maxHazard,
    t7,
    sigBonus,
    margin25x,
    margin50x,
    viable
  };
}

async function main() {
  console.log('Auditing 10 tradable candidate assets in parallel (v2)...');
  const audits = await Promise.all(targets.map(auditAsset));
  const valid = audits.filter(Boolean);

  console.log('\n| Symbol | Price | VWAP z | LSR (±2%) | Sig | G1 | G2 | Table 7 | R-Mult | Margin 25x | Status |');
  console.log('| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |');

  for (const a of valid) {
    const status = a.viable ? '**ELIGIBLE (GRADE A/B)**' : (a.t7 < 5.0 ? 'GATED (T7<5.0)' : (a.margin25x > 0.90 ? 'GATED (MARGIN)' : 'GATED (R/GATE)'));
    console.log(
      `| ${a.sym} | $${a.price} | ${a.z.toFixed(2)}σ | ${a.lsr.toFixed(2)}:1 | +${a.sigBonus.toFixed(1)} | ${a.g1Pass ? 'PASS' : 'FAIL'} | ${a.g2Pass ? 'PASS' : 'FAIL'} | ${a.t7.toFixed(1)} | ${a.rMult.toFixed(2)}R | $${a.margin25x.toFixed(3)} | ${status} |`
    );
  }
}

main().catch(console.error);
