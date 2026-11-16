import fs from 'node:fs';

async function fetchJson(endpoint) {
  try {
    const res = await fetch(`http://127.0.0.1:3000${endpoint}`, { signal: AbortSignal.timeout(4000) });
    return await res.json();
  } catch (e) {
    return null;
  }
}

async function deepInspect(sym) {
  console.log(`\n=================== DEEP INSPECTION FOR ${sym} ===================`);
  const [mkt, liq, sig, bw, cvd] = await Promise.all([
    fetchJson(`/api/cg/market?sym=${sym}`),
    fetchJson(`/api/cg/liqlevels?sym=${sym}&range=3d&lvR=4`),
    fetchJson(`/api/cg/signals?sym=${sym}`),
    fetchJson(`/api/cg/bookwalls?sym=${sym}`),
    fetchJson(`/api/cg/cvd?sym=${sym}`)
  ]);

  if (!mkt || !mkt.ok) {
    console.log(`Failed to fetch market for ${sym}`);
    return;
  }

  const p = mkt.price?.last;
  const a = mkt.auction || {};
  const v = mkt.vwap || {};
  const ema = mkt.ema || {};

  console.log(`Price: ${p}`);
  console.log(`Session(8h) POC: ${a.session?.poc} | VAH: ${a.session?.vah} | VAL: ${a.session?.val}`);
  console.log(`Day POC: ${a.day?.poc} | VAH: ${a.day?.vah} | VAL: ${a.day?.val}`);
  console.log(`Month POC: ${a.month?.poc}`);
  console.log(`VWAP: ${v.vwap} | +1s: ${v.vwap + v.bands?.sd1} | +2s: ${v.vwap + v.bands?.sd2} | -1s: ${v.vwap - v.bands?.sd1}`);
  console.log(`EMA: H4 13=${ema.h4?.e13}/89=${ema.h4?.e89} (${ema.h4?.e13 > ema.h4?.e89 ? 'BULL' : 'BEAR'}) | D1 13=${ema.d1?.e13}/89=${ema.d1?.e89} (${ema.d1?.e13 > ema.d1?.e89 ? 'BULL' : 'BEAR'})`);
  console.log(`RSI: M15=${mkt.rsi?.m15} | H1=${mkt.rsi?.h1} | H4=${mkt.rsi?.h4}`);

  if (liq && liq.ok) {
    const s = liq.stats || {};
    console.log(`Liq stats: shorts=${s.totals?.shorts} | longs=${s.totals?.longs}`);
    console.log('Strongest Above:');
    (s.keyLevels?.above || []).slice(0, 5).forEach(l => console.log(`  ${l.price} (+${l.distPct?.toFixed(2)}%, str ${l.strength?.toFixed(1)})`));
    console.log('Strongest Below:');
    (s.keyLevels?.below || []).slice(0, 5).forEach(l => console.log(`  ${l.price} (-${l.distPct?.toFixed(2)}%, str ${l.strength?.toFixed(1)})`));
  }

  if (sig && sig.ok) {
    console.log(`Signals: ${sig.counts?.all} total (${sig.counts?.bullish} bull / ${sig.counts?.bearish} bear)`);
    (sig.sets || []).forEach(set => {
      const lastSigs = (set.sigs || []).slice(-3);
      if (lastSigs.length) {
        console.log(`  [${set.label}]: ` + lastSigs.map(s => `${s.side}:${s.name || s.t}@${s.p}`).join(', '));
      }
    });
  }

  if (bw && bw.ok) {
    console.log('Bookwalls:');
    (bw.walls || []).slice(0, 5).forEach(w => console.log(`  ${w.side.toUpperCase()} $${(w.usd/1e6).toFixed(2)}M @ ${w.price}`));
  }
}

async function run() {
  await deepInspect('ETH');
  await deepInspect('UNI');
  await deepInspect('ARB');
}

run();
