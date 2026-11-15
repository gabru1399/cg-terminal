import fs from 'fs';

async function main() {
  const res = await fetch('http://127.0.0.1:3000/api/cg/screener');
  const d = await res.json();
  const cryptos = d.rows.filter(r => r.kind === 'crypto-perp');
  console.log('| Asset | Price | 24h % | Regime | Model & Dir | Conf | VWAP z | 24h CVD | EMA 4H/1H | RSI 15m/1H | Score | Status |');
  console.log('| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |');
  for (const c of cryptos) {
    const dir = c.m1m2?.direction || 'NEUTRAL';
    const model = c.m1m2?.activeModel || 'WAIT';
    const conf = c.m1m2?.confidence ? c.m1m2.confidence + '%' : 'N/A';
    const z = c.vwapZ !== null ? c.vwapZ.toFixed(2) : 'N/A';
    const cvd = c.cvd24h ? (c.cvd24h > 0 ? '+' : '') + (c.cvd24h / 1e6).toFixed(1) + 'M' : 'N/A';
    const ema = (c.ema4h || 'N/A') + ' / ' + (c.ema1h || 'N/A');
    const rsi = (c.rsi15m !== null ? c.rsi15m.toFixed(1) : 'N/A') + ' / ' + (c.rsi1h !== null ? c.rsi1h.toFixed(1) : 'N/A');
    const score = c.confluence?.score !== undefined ? c.confluence.score.toFixed(2) : '0.00';
    const regime = c.m1m2?.regime || 'RANGE';
    let status = 'MONITOR';
    if (['ETH', 'LINK', 'SUI', 'LTC'].includes(c.sym)) status = 'ACTIVE LIMIT (CLOB)';
    else if (c.sym === 'BTC') status = 'GATED LIMIT (DEPOSIT)';
    console.log(`| ${c.sym} | $${c.price} | ${c.chg24hPct}% | ${regime} | ${model} (${dir}) | ${conf} | ${z} | ${cvd} | ${ema} | ${rsi} | ${score} | ${status} |`);
  }
}

main().catch(console.error);
