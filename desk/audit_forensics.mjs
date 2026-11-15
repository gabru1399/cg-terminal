import fs from 'fs';

function runAudit() {
  if (!fs.existsSync('desk/deep_telemetry.json')) {
    console.log('deep_telemetry.json not found yet');
    return;
  }

  const data = JSON.parse(fs.readFileSync('desk/deep_telemetry.json', 'utf8'));

  const orders = [
    { sym: 'LINK', entry: 9.450, sl: 9.680, tp: 8.980, side: 'sell' },
    { sym: 'DOT', entry: 0.748, sl: 0.762, tp: 0.718, side: 'sell' },
    { sym: 'AVAX', entry: 7.420, sl: 7.580, tp: 7.020, side: 'sell' },
    { sym: 'UNI', entry: 5.240, sl: 5.350, tp: 5.010, side: 'sell' }
  ];

  console.log('=== AUDIT OF 4 ACTIVE STANDING ORDERS ===\n');

  for (const o of orders) {
    const item = data[o.sym];
    if (!item || !item.mkt) {
      console.log(`[${o.sym}] No market data`);
      continue;
    }

    const price = Number(item.mkt.price.last);
    const dayPoc = item.mkt.auction && item.mkt.auction.day ? item.mkt.auction.day.poc : null;
    const sessPoc = item.mkt.auction && item.mkt.auction.session ? item.mkt.auction.session.poc : null;
    const vwap = item.mkt.vwap ? item.mkt.vwap.vwap : null;

    // Gate 1 clearance
    const distDayPoc = dayPoc ? (Math.abs(o.sl - dayPoc) / dayPoc * 100).toFixed(2) + '%' : 'n/a';
    const distSessPoc = sessPoc ? (Math.abs(o.sl - sessPoc) / sessPoc * 100).toFixed(2) + '%' : 'n/a';
    const distVwap = vwap ? (Math.abs(o.sl - vwap) / vwap * 100).toFixed(2) + '%' : 'n/a';

    // Gate 2 Liquidation geometry
    let vectorAFuel = 0;
    let vectorBHazard = 0;
    const liqAbove = (item.liq && item.liq.stats && item.liq.stats.keyLevels && item.liq.stats.keyLevels.above) || [];

    for (const lvl of liqAbove) {
      const p = Number(lvl.price);
      const usd = Number(lvl.usd);
      if (p >= price && p <= o.entry) {
        vectorAFuel += usd;
      } else if (p > o.entry && p <= o.sl * 1.01) {
        vectorBHazard += usd;
      }
    }

    const distToEntry = ((o.entry - price) / price * 100).toFixed(2) + '%';
    const g1Pass = (parseFloat(distDayPoc) >= 0.5 && parseFloat(distSessPoc) >= 0.5);
    const g2Pass = (vectorBHazard < 2000000);

    console.log(`SYMBOL: ${o.sym}`);
    console.log(`  Live Price: ${price} | Entry Limit: ${o.entry} (${distToEntry} away) | SL: ${o.sl} | TP: ${o.tp}`);
    console.log(`  Gate 1 Clearance: Day POC dist=${distDayPoc}, Sess POC dist=${distSessPoc}, VWAP dist=${distVwap} -> ${g1Pass ? 'PASS' : 'WARN'}`);
    console.log(`  Gate 2 Liquidation: Vector A (Fuel to entry)=$${Math.round(vectorAFuel).toLocaleString()} | Vector B (Hazard in Risk Zone)=$${Math.round(vectorBHazard).toLocaleString()} -> ${g2Pass ? 'PASS' : 'VETO'}`);
    console.log(`  Standing Order Status: ${g1Pass && g2Pass ? 'CONFIRMED VALID - HOLD STANDING' : 'NEEDS ACTION'}\n`);
  }

  console.log('=== SCREENING REMAINING CANDIDATES ===\n');
  const others = ['TRX', 'DOGE', 'LTC', 'ADA', 'NEAR', 'XRP'];
  for (const sym of others) {
    const item = data[sym];
    if (!item || !item.mkt) continue;
    const price = Number(item.mkt.price.last);
    const sigs = (item.sig && item.sig.sets) ? item.sig.sets.flatMap(s => s.sigs || []) : [];
    const recentSigs = sigs.filter(s => (Date.now() / 1000 - s.ts) <= 8 * 3600);

    let vectorBHazard = 0;
    const liqAbove = (item.liq && item.liq.stats && item.liq.stats.keyLevels && item.liq.stats.keyLevels.above) || [];
    for (const lvl of liqAbove) {
      const p = Number(lvl.price);
      const usd = Number(lvl.usd);
      if (p >= price && p <= price * 1.03) {
        vectorBHazard += usd;
      }
    }

    console.log(`Candidate: ${sym} (Price: ${price})`);
    console.log(`  Recent 8h Signals (${recentSigs.length}):`, recentSigs.slice(-3).map(s => `${s.title}/${s.side} @ ${s.price}`).join(', ') || 'none');
    console.log(`  Overhead Liq Cluster (0-3%): $${Math.round(vectorBHazard).toLocaleString()}`);
  }
}

runAudit();
