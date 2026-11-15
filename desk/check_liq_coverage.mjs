const symbols = [
  'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC',
  'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR',
  'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB'
];

async function checkLiq() {
  for (const sym of symbols) {
    try {
      const res = await fetch(`http://127.0.0.1:3000/api/cg/liqlevels?sym=${sym}`);
      if (res.ok) {
        const d = await res.json();
        const clusters = d.clusters || [];
        if (clusters.length > 0) {
          console.log(`[LIQ DATA FOUND] ${sym}: ${clusters.length} clusters!`);
        }
      }
    } catch (e) {}
  }
}

checkLiq();
