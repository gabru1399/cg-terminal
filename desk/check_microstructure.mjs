const symbols = ['SOL', 'ADA', 'DOGE', 'AVAX', 'LTC', 'XRP', 'DOT', 'NEAR', 'UNI', 'TRX'];

async function checkDetails() {
  for (const sym of symbols) {
    try {
      const [sigRes, bwRes, ltoRes, mktRes] = await Promise.all([
        fetch(`http://127.0.0.1:3000/api/cg/signals?sym=${sym}`),
        fetch(`http://127.0.0.1:3000/api/cg/bookwalls?sym=${sym}`),
        fetch(`http://127.0.0.1:3000/api/cg/lto?sym=${sym}`),
        fetch(`http://127.0.0.1:3000/api/cg/market?sym=${sym}`)
      ]);
      const sig = sigRes.ok ? await sigRes.json() : null;
      const bw = bwRes.ok ? await bwRes.json() : null;
      const lto = ltoRes.ok ? await ltoRes.json() : null;
      const mkt = mktRes.ok ? await mktRes.json() : null;

      const signalsList = sig?.signals || sig?.items || [];
      const wallsList = bw?.walls || [];
      const ltoList = lto?.orders || lto?.items || [];
      const price = mkt?.price?.last;

      console.log(`=== ${sym} (Price: ${price}) ===`);
      console.log(`Signals count: ${signalsList.length}`);
      if (signalsList.length > 0) {
        console.log(`Recent signals:`, JSON.stringify(signalsList.slice(0, 3)));
      }
      console.log(`Book walls count: ${wallsList.length}`);
      if (wallsList.length > 0) {
        console.log(`Top walls:`, JSON.stringify(wallsList.slice(0, 2)));
      }
      console.log(`LTO orders count: ${ltoList.length}`);
      if (ltoList.length > 0) {
        console.log(`Top LTO:`, JSON.stringify(ltoList.slice(0, 2)));
      }
    } catch (e) {
      console.log(`${sym} Error:`, e.message);
    }
  }
}

checkDetails();
