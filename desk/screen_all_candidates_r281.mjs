import fs from 'node:fs';

const candidates = ['BTC', 'ETH', 'LTC', 'AVAX', 'LINK', 'UNI', 'DOGE', 'TRX', 'DOT', 'FIL', 'APT', 'ARB', 'SUI', 'TIA', 'ADA', 'XRP'];

async function fetchJson(endpoint) {
  try {
    const res = await fetch(`http://127.0.0.1:3000${endpoint}`, { signal: AbortSignal.timeout(4000) });
    return await res.json();
  } catch (e) {
    return null;
  }
}

async function inspect(sym) {
  const [mkt, liq, sig, bw] = await Promise.all([
    fetchJson(`/api/cg/market?sym=${sym}`),
    fetchJson(`/api/cg/liqlevels?sym=${sym}&range=3d&lvR=4`),
    fetchJson(`/api/cg/signals?sym=${sym}`),
    fetchJson(`/api/cg/bookwalls?sym=${sym}`)
  ]);

  if (!mkt || !mkt.ok) return null;

  const price = mkt.price?.last || 0;
  const auction = mkt.auction || {};
  const day_poc = auction.day?.poc || 0;
  const day_vah = auction.day?.vah || 0;
  const day_val = auction.day?.val || 0;
  const vwap = mkt.vwap?.vwap || 0;
  const sd1 = mkt.vwap?.bands?.sd1 || 1;
  const z = sd1 ? (price - vwap) / sd1 : 0;

  const ema = mkt.ema || {};
  const h4_trend = (ema.h4?.e13 || 0) > (ema.h4?.e89 || 0) ? 'BULL' : 'BEAR';
  const d1_trend = (ema.d1?.e13 || 0) > (ema.d1?.e89 || 0) ? 'BULL' : 'BEAR';
  const rsi_15m = mkt.rsi?.m15 || 50;

  let lsr = 1.0;
  let shorts_above = 0;
  let longs_below = 0;
  let clusters_above = [];
  let clusters_below = [];
  if (liq && liq.ok) {
    const stats = liq.stats || {};
    shorts_above = stats.totals?.shorts || 0;
    longs_below = stats.totals?.longs || 0;
    if (longs_below > 0) lsr = shorts_above / longs_below;
    clusters_above = stats.keyLevels?.above || [];
    clusters_below = stats.keyLevels?.below || [];
  }

  const sig_count = sig?.ok ? (sig.counts?.all || 0) : 0;
  const ask_walls = [];
  const bid_walls = [];
  if (bw && bw.ok) {
    for (const w of bw.walls || []) {
      if (w.side === 'ask' && (w.usd || 0) >= 300000) {
        ask_walls.push(`$${(w.usd/1e6).toFixed(1)}M@${w.price}`);
      } else if (w.side === 'bid' && (w.usd || 0) >= 300000) {
        bid_walls.push(`$${(w.usd/1e6).toFixed(1)}M@${w.price}`);
      }
    }
  }

  return {
    sym,
    price,
    h4_trend,
    d1_trend,
    z: +z.toFixed(2),
    vwap: +vwap.toFixed(4),
    day_poc: +day_poc.toFixed(4),
    day_vah: +day_vah.toFixed(4),
    day_val: +day_val.toFixed(4),
    lsr: +lsr.toFixed(2),
    shorts_above_k: +(shorts_above / 1000).toFixed(1),
    longs_below_k: +(longs_below / 1000).toFixed(1),
    sig_count,
    ask_walls: ask_walls.slice(0, 2),
    bid_walls: bid_walls.slice(0, 2),
    clusters_above_cnt: clusters_above.length,
    clusters_below_cnt: clusters_below.length
  };
}

async function run() {
  console.log('Running fast concurrent screen...');
  const results = (await Promise.all(candidates.map(inspect))).filter(Boolean);
  console.table(results.map(r => ({
    SYM: r.sym,
    Price: r.price,
    H4: r.h4_trend,
    D1: r.d1_trend,
    z: r.z,
    LSR: r.lsr,
    ShAbove: `${r.shorts_above_k}k`,
    LgBelow: `${r.longs_below_k}k`,
    Walls: [...r.ask_walls, ...r.bid_walls].join(' | ') || 'none'
  })));
  fs.writeFileSync('desk/candidate_screen_r281.json', JSON.stringify(results, null, 2));
}

run();
