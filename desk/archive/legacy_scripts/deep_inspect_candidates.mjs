async function deepInspect(sym) {
  const [mktRes, narRes, liqRes, cvdRes, bwRes] = await Promise.all([
    fetch(`http://127.0.0.1:3000/api/cg/market?sym=${sym}`),
    fetch(`http://127.0.0.1:3000/api/cg/narrative?sym=${sym}`),
    fetch(`http://127.0.0.1:3000/api/cg/liqlevels?sym=${sym}`),
    fetch(`http://127.0.0.1:3000/api/cg/cvd?sym=${sym}`),
    fetch(`http://127.0.0.1:3000/api/cg/bookwalls?sym=${sym}`)
  ]);
  const mkt = await mktRes.json();
  const nar = await narRes.json();
  const liq = await liqRes.json();
  const cvd = await cvdRes.json();
  const bw = await bwRes.json();

  console.log(`\n============================= ${sym} DEEP DIVE =============================`);
  console.log(`Price: ${mkt.price.last}`);
  console.log(`Auction Day: POC=${mkt.auction?.day?.poc}, VAH=${mkt.auction?.day?.vah}, VAL=${mkt.auction?.day?.val}`);
  console.log(`Auction Sess: POC=${mkt.auction?.session?.poc}, Month POC=${mkt.auction?.month?.poc}`);
  console.log(`VWAP: ${mkt.vwap?.vwap} (sd1=${mkt.vwap?.bands?.sd1}, sd2=${mkt.vwap?.bands?.sd2}, sd3=${mkt.vwap?.bands?.sd3})`);
  const z = (Number(mkt.price.last) - Number(mkt.vwap?.vwap)) / Number(mkt.vwap?.bands?.sd1);
  console.log(`VWAP z-score: ${z.toFixed(2)}σ`);
  console.log(`CVD 24h: ${cvd.cvd?.delta24h}, Taker Buy Share: ${cvd.cvd?.takerBuyShare}%`);
  console.log(`BookWalls: Bid Depth=${bw.bidDepth}, Ask Depth=${bw.askDepth}, Imbalance=${bw.imbalance}`);
  console.log(`BookWalls Confirmed Count: ${bw.walls?.length || 0}`);
  if (bw.walls?.length > 0) {
    console.log(`Walls:`, bw.walls.slice(0, 3));
  }

  const clusters = liq.clusters || [];
  console.log(`Liquidation Clusters Count: ${clusters.length}`);
  const price = Number(mkt.price.last);
  const above = clusters.filter(c => Number(c.price) > price);
  const below = clusters.filter(c => Number(c.price) < price);
  console.log(`Clusters Above Price (${above.length}):`);
  above.slice(0, 5).forEach(c => console.log(`   Price: ${c.price} | USD: $${Number(c.usd).toLocaleString()} | Str: ${c.strength}`));
  console.log(`Clusters Below Price (${below.length}):`);
  below.slice(0, 5).forEach(c => console.log(`   Price: ${c.price} | USD: $${Number(c.usd).toLocaleString()} | Str: ${c.strength}`));
}

async function main() {
  await deepInspect('ADA');
  await deepInspect('DOT');
  await deepInspect('LTC');
}

main().catch(console.error);
