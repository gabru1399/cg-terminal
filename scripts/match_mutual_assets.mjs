import fs from "fs";

async function match() {
  const dRes = await fetch("https://api.india.delta.exchange/v2/products");
  const dData = await dRes.json();
  const deltaPerps = (dData.result || []).filter(
    (p) => p.state === "live" && p.contract_type === "perpetual_futures"
  );

  const bRes = await fetch("https://fapi.binance.com/fapi/v1/exchangeInfo");
  const bData = await bRes.json();
  const binanceSymbols = new Set(
    (bData.symbols || [])
      .filter((s) => s.status === "TRADING" && s.contractType === "PERPETUAL")
      .map((s) => s.symbol)
  );

  const curatedContent = fs.readFileSync("src/lib/universe/curated.ts", "utf8");
  const curatedSyms = new Set();
  const regex = /sym:\s*"([^"]+)"/g;
  let match;
  while ((match = regex.exec(curatedContent)) !== null) {
    curatedSyms.add(match[1]);
  }

  console.log("Delta live perps count:", deltaPerps.length);
  console.log("Binance live perps count:", binanceSymbols.size);
  console.log("Terminal Curated count:", curatedSyms.size);

  const mutual = [];
  const missingFromCurated = [];

  for (const p of deltaPerps) {
    const sym = p.symbol;
    let base = "";
    let binancePair = "";

    if (sym.endsWith("BUSD")) {
      base = sym.replace("BUSD", "");
      binancePair = base + "USDT";
    } else if (sym.endsWith("USD")) {
      base = sym.replace("USD", "");
      binancePair = base + "USDT";
    }

    if (binanceSymbols.has(binancePair)) {
      const isCurated = curatedSyms.has(base) || curatedSyms.has(sym);
      const item = {
        deltaSymbol: sym,
        base,
        binancePair,
        contractValue: p.contract_value,
        tickSize: p.tick_size,
        inTerminal: isCurated,
        category: sym.endsWith("BUSD") ? "TradFi" : "Crypto"
      };
      mutual.push(item);
      if (!isCurated) {
        missingFromCurated.push(item);
      }
    }
  }

  console.log("Total Mutually Available (Delta + Binance):", mutual.length);
  console.log("Already in Terminal Curated:", mutual.length - missingFromCurated.length);
  console.log("MISSING from Terminal Curated:", missingFromCurated.length);

  // Group missing by category
  const missingCrypto = missingFromCurated.filter(m => m.category === "Crypto");
  const missingTradFi = missingFromCurated.filter(m => m.category === "TradFi");

  console.log("\n=== MISSING CRYPTO PERPS (" + missingCrypto.length + ") ===");
  console.log(missingCrypto.map(m => m.base).join(", "));

  console.log("\n=== MISSING TRADFI bStocks PERPS (" + missingTradFi.length + ") ===");
  console.log(missingTradFi.map(m => m.base).join(", "));

  fs.writeFileSync("docs/MUTUAL_ASSETS_AUDIT.json", JSON.stringify({
    summary: {
      deltaLivePerps: deltaPerps.length,
      binanceLivePerps: binanceSymbols.size,
      terminalCurated: curatedSyms.size,
      totalMutual: mutual.length,
      alreadyInTerminal: mutual.length - missingFromCurated.length,
      missingFromTerminal: missingFromCurated.length
    },
    missingCrypto,
    missingTradFi,
    allMutual: mutual
  }, null, 2));
}

match().catch(console.error);
