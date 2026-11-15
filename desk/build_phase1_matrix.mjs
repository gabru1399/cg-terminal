import fs from 'fs';

async function run() {
  const res = await fetch('http://127.0.0.1:3000/api/cg/screener');
  const d = await res.json();
  const cryptoRows = d.rows.filter(r => r.kind === 'crypto-perp');

  console.log('Found crypto-perp rows:', cryptoRows.length);

  function getPermissible(regime) {
    if (regime === 'RANGE_BALANCE') return 'S1, S2, S5, S6';
    if (regime === 'TREND_UP' || regime === 'TREND_DOWN') return 'S7, S8, S4, S3, S1';
    if (regime === 'COMPRESSION_SQUEEZE') return 'S4, S8, S1';
    return 'S1, S2, S5';
  }

  let table = '| Symbol | Price | 24h % | Regime (Tab 7) | Permissible Setups | Model & Dir | Conf % | VWAP z | 24h CVD | EMA 4H/1H | Table 7 | Status |\n';
  table += '|---|---|---|---|---|---|---|---|---|---|---|---|\n';

  const rows = [];
  for (const r of cryptoRows) {
    const sym = r.sym;
    const price = r.price !== null && r.price !== undefined ? r.price : 'n/a';
    const chg = r.chg24hPct !== null && r.chg24hPct !== undefined ? (r.chg24hPct > 0 ? '+' : '') + r.chg24hPct.toFixed(2) + '%' : '0.00%';
    const regime = r.m1m2 ? r.m1m2.regime || 'RANGE_BALANCE' : 'RANGE_BALANCE';
    const permissible = getPermissible(regime);
    const modelDir = r.m1m2 ? (r.m1m2.activeModel || 'NONE') + ' ' + (r.m1m2.direction || '') : 'NONE';
    const conf = r.m1m2 && r.m1m2.confidence !== null && r.m1m2.confidence !== undefined ? r.m1m2.confidence + '%' : '0%';
    const vwapZ = r.vwapZ !== null && r.vwapZ !== undefined ? r.vwapZ.toFixed(2) : '0.00';
    const cvd = r.cvd24h !== null && r.cvd24h !== undefined ? (r.cvd24h > 0 ? '+' : '') + (r.cvd24h / 1e6).toFixed(1) + 'M' : 'n/a';
    const ema = (r.ema4h || 'flat') + '/' + (r.ema1h || 'flat');
    const t7 = r.confluence && r.confluence.score !== null && r.confluence.score !== undefined ? r.confluence.score.toFixed(2) : '0.00';
    let status = 'MONITOR';
    if (['LINK', 'DOT', 'AVAX', 'UNI'].includes(sym)) {
      status = 'ACTIVE_CLOB';
    } else if (Number(t7) >= 5.0) {
      status = 'QUALIFIED';
    }
    table += `| ${sym} | ${price} | ${chg} | ${regime} | ${permissible} | ${modelDir} | ${conf} | ${vwapZ} | ${cvd} | ${ema} | ${t7} | ${status} |\n`;
    rows.push({ sym, price, chg, regime, permissible, modelDir, conf, vwapZ, cvd, ema, t7, status });
  }

  fs.writeFileSync('desk/phase1_matrix.json', JSON.stringify({ table, rows }, null, 2));
  console.log('Matrix generated with', rows.length, 'rows');
}

run();
