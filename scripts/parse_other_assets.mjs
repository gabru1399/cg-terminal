import fs from 'fs';

const data = JSON.parse(fs.readFileSync('scripts/forensics_dump.json', 'utf8'));

for (const sym of ['LINK', 'SUI', 'LTC', 'BTC']) {
  const d = data[sym];
  console.log(`=== ${sym} ===`);
  console.log('Price:', d.market.price.last);
  console.log('Auction Day:', d.market.auction.day);
  console.log('Auction Session:', d.market.auction.session);
  console.log('VWAP:', d.market.vwap.vwap);
  console.log('EMA H4/H1:', d.market.ema.h4.e13, d.market.ema.h4.e89, d.market.ema.h1.e13, d.market.ema.h1.e89);
  console.log('RSI 15m/H1:', d.market.rsi.m15, d.market.rsi.h1);
  console.log('Liq totals:', d.liq?.stats?.totals);
  console.log('Bookwalls imb:', d.bookwalls?.model?.imbalance, '5mAgo:', d.bookwalls?.model?.imbalance5mAgo);
  console.log('CVD kpis:', d.cvd?.kpis?.perpCvd, d.cvd?.kpis?.spotCvd, d.cvd?.kpis?.buyRatio, d.cvd?.kpis?.quadrant);
}
