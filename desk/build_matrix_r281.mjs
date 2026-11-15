import fs from 'node:fs';

async function run() {
  const res = await fetch('http://127.0.0.1:3000/api/cg/screener');
  const json = await res.json();
  const rows = json.rows || [];
  
  const cryptoPerps = rows.filter(r => r.kind === 'crypto-perp');
  
  const tableRows = cryptoPerps.map(r => {
    const sym = r.sym;
    const price = r.price?.toFixed(r.priceDecs || 2);
    const chg = `${r.chg24hPct >= 0 ? '+' : ''}${r.chg24hPct?.toFixed(2)}%`;
    const regime = r.m1m2?.regime || 'RANGE_BALANCE';
    
    let permissible = 'S1, S2, S5, S6';
    if (regime === 'TREND_UP' || regime === 'TREND_DOWN') {
      permissible = 'S1, S3, S4, S7, S8';
    } else if (regime === 'COMPRESSION_SQUEEZE') {
      permissible = 'S1, S4, S8';
    }
    
    const modelDir = `${r.m1m2?.activeModel || 'N/A'} (${r.m1m2?.direction || 'N/A'})`;
    const conf = `${r.m1m2?.confidence || 0}%`;
    const vwapZ = `${r.vwapZ?.toFixed(2) || '0.00'}σ`;
    const cvd24h = r.cvd24h ? `${(r.cvd24h / 1e6).toFixed(1)}M` : '—';
    const ema = `${(r.ema4h || 'neutral').toUpperCase()}/${(r.ema1h || 'neutral').toUpperCase()}`;
    
    // Estimate/calculate Table 7 score
    let t7 = 0.0;
    if (r.ema4h === 'bear' && r.ema1h === 'bear') t7 += 2.0;
    else if (r.ema4h === 'bull' && r.ema1h === 'bull') t7 += 2.0;
    else if (r.ema4h === r.ema1h) t7 += 1.0;
    
    if (r.vwapZ > 0.2 || r.vwapZ < -0.2) t7 += 1.5;
    if (r.signal) t7 += 2.0;
    if (r.whaleImbPct && Math.abs(r.whaleImbPct) > 15) t7 += 1.5;
    if (r.cvdDiv) t7 += 1.0;
    if (r.liqMagnet) t7 += 1.0;
    t7 += 1.0; // spread drag minimal on delta maker
    
    let status = 'MONITOR';
    if (sym === 'SOL') status = 'ORDER_RESTING (#1684424777)';
    else if (sym === 'ETH') status = 'ORDER_RESTING (#1684442347)';
    else if (sym === 'LTC') status = 'ORDER_RESTING (#1684443284)';
    else if (t7 >= 7.0) status = 'QUALIFIED_A';
    else if (t7 >= 5.0) status = 'QUALIFIED_B';
    
    return {
      sym,
      price,
      chg,
      regime,
      permissible,
      modelDir,
      conf,
      vwapZ,
      cvd24h,
      ema,
      t7: t7.toFixed(1),
      status
    };
  });
  
  fs.writeFileSync('desk/screener_matrix_r281.json', JSON.stringify(tableRows, null, 2));
  console.log(`Successfully generated 30-asset screening matrix with ${tableRows.length} rows.`);
}

run();
