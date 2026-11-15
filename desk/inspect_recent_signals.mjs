const symbols = ['SOL', 'ADA', 'DOGE', 'AVAX', 'LTC', 'XRP', 'DOT', 'NEAR', 'UNI', 'TRX'];

async function run() {
  for (const sym of symbols) {
    try {
      const res = await fetch(`http://127.0.0.1:3000/api/cg/signals?sym=${sym}`);
      const data = await res.json();
      const allSigs = [];
      if (data.sets) {
        for (const s of data.sets) {
          if (s.sigs) allSigs.push(...s.sigs);
        }
      }
      allSigs.sort((a, b) => b.ts - a.ts);
      const recent = allSigs.slice(0, 3);
      console.log(`\n=== ${sym} (Total Sigs: ${data.counts?.all || 0}, Bull: ${data.counts?.bullish}, Bear: ${data.counts?.bearish}) ===`);
      for (const sig of recent) {
        const dateStr = new Date(sig.ts * 1000).toISOString();
        console.log(`  - Type: ${sig.t.toUpperCase()} | Side: ${sig.side} | Price: ${sig.p} | Bar: ${sig.bt} | Time: ${dateStr}`);
      }
    } catch (e) {
      console.log(`${sym} Error: ${e.message}`);
    }
  }
}

run();
