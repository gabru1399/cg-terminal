import fs from 'fs';

const data = JSON.parse(fs.readFileSync('scripts/forensics_dump.json', 'utf8'));

for (const sym of ['ETH', 'LINK', 'SUI', 'LTC', 'BTC']) {
  const d = data[sym];
  console.log('==================== ' + sym + ' ====================');
  console.log('Price:', d.market?.price?.last, 'Low:', d.market?.price?.dayLow, 'High:', d.market?.price?.dayHigh);
  console.log('Day VAL/POC/VAH:', d.market?.auction?.day?.val, d.market?.auction?.day?.poc, d.market?.auction?.day?.vah);
  console.log('Session VAL/POC/VAH:', d.market?.auction?.session?.val, d.market?.auction?.session?.poc, d.market?.auction?.session?.vah);
  console.log('Month VAL/POC/VAH:', d.market?.auction?.month?.val, d.market?.auction?.month?.poc, d.market?.auction?.month?.vah);
  console.log('VWAP:', d.market?.vwap);
  console.log('EMA Stacks:', d.market?.indicators?.ema);
  console.log('RSI:', d.market?.indicators?.rsi);
  console.log('ATR:', d.market?.indicators?.atr);
  console.log('Signals keys:', d.signals ? Object.keys(d.signals) : null);
  if (d.signals?.signals) {
    console.log('Recent signals:', d.signals.signals.slice(0, 3));
  }
  console.log('Liq keys:', d.liq ? Object.keys(d.liq) : null);
  if (d.liq) {
    console.log('Liq summary:', {
      lsr: d.liq.lsr,
      totalLongUsd: d.liq.totalLongUsd,
      totalShortUsd: d.liq.totalShortUsd,
      clusters: d.liq.clusters?.slice(0, 3)
    });
  }
  console.log('Bookwalls keys:', d.bookwalls ? Object.keys(d.bookwalls) : null);
  if (d.bookwalls) {
    console.log('Bookwalls summary:', {
      imbalance: d.bookwalls.imbalance,
      askWalls: d.bookwalls.askWalls?.slice(0, 2),
      bidWalls: d.bookwalls.bidWalls?.slice(0, 2)
    });
  }
  console.log('CVD keys:', d.cvd ? Object.keys(d.cvd) : null);
  if (d.cvd) {
    console.log('CVD summary:', {
      delta24h: d.cvd.delta24h,
      takerBuyShare: d.cvd.takerBuyShare,
      divergences: d.cvd.divergences
    });
  }
}
