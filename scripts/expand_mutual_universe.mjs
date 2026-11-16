import fs from "fs";

// Load the audit data
const audit = JSON.parse(fs.readFileSync("docs/MUTUAL_ASSETS_AUDIT.json", "utf8"));
const missingCrypto = audit.missingCrypto;
const missingTradFi = audit.missingTradFi;

console.log("Missing crypto count:", missingCrypto.length);
console.log("Missing TradFi count:", missingTradFi.length);

// Let's create sensible metadata mapping for the most popular assets
const KNOWN_META = {
  // L1 & L2
  POL: { name: "Polygon Ecosystem", sub: "Ethereum L2" },
  SONIC: { name: "Sonic (Fantom)", sub: "Smart Contract L1" },
  S: { name: "Sonic Network", sub: "Smart Contract L1" },
  MANTA: { name: "Manta Network", sub: "Modular L2" },
  STRK: { name: "Starknet", sub: "ZK-Rollup L2" },
  ZK: { name: "zkSync", sub: "ZK-Rollup L2" },
  BERA: { name: "Berachain", sub: "PoL L1" },
  MOVE: { name: "Movement", sub: "Move-EVM L2" },
  DYDX: { name: "dYdX", sub: "DeFi AppChain" },
  RUNE: { name: "THORChain", sub: "Cross-Chain DEX" },
  STX: { name: "Stacks", sub: "Bitcoin L2" },
  BCH: { name: "Bitcoin Cash", sub: "Payments L1" },
  ZEC: { name: "Zcash", sub: "Privacy L1" },
  IOTA: { name: "IOTA", sub: "IoT DLT" },
  KSM: { name: "Kusama", sub: "Polkadot Canary" },
  EIGEN: { name: "EigenLayer", sub: "Restaking Protocol" },
  ALT: { name: "AltLayer", sub: "Restaked Rollups" },
  MOVR: { name: "Moonriver", sub: "Kusama EVM" },
  ARK: { name: "Ark", sub: "Interoperability" },
  
  // DeFi
  AAVE: { name: "Aave", sub: "DeFi Lending" },
  PENDLE: { name: "Pendle", sub: "Yield Tokenization" },
  LDO: { name: "Lido DAO", sub: "Liquid Staking" },
  ENA: { name: "Ethena", sub: "Synthetic Dollar" },
  ETHFI: { name: "Ether.fi", sub: "Liquid Restaking" },
  SUSHI: { name: "SushiSwap", sub: "DeFi DEX" },
  CAKE: { name: "PancakeSwap", sub: "DeFi DEX" },
  ONDO: { name: "Ondo Finance", sub: "RWA / Treasuries" },
  JUP: { name: "Jupiter", sub: "Solana DEX Aggregator" },
  RSR: { name: "Reserve Rights", sub: "Asset-Backed Currency" },
  GALA: { name: "Gala Games", sub: "Gaming & Entertainment" },
  MANA: { name: "Decentraland", sub: "Metaverse" },
  AXS: { name: "Axie Infinity", sub: "Gaming" },

  // AI & DePIN
  TAO: { name: "Bittensor", sub: "Decentralized AI" },
  IO: { name: "io.net", sub: "Decentralized GPU Cloud" },
  VIRTUAL: { name: "Virtuals Protocol", sub: "AI Agents" },
  AIXBT: { name: "aixbt by Virtuals", sub: "AI Agent Alpha" },
  AIOT: { name: "AIoT Network", sub: "AI + IoT" },
  KAITO: { name: "Kaito AI", sub: "AI Search & Attention" },
  ACT: { name: "Act I : The AI Prophecy", sub: "AI Agent Collective" },

  // Memes & High Volatility
  "1000BONK": { name: "Bonk (1000x perp)", sub: "Solana Meme" },
  WIF: { name: "dogwifhat", sub: "Solana Meme" },
  POPCAT: { name: "Popcat", sub: "Solana Meme" },
  PNUT: { name: "Peanut the Squirrel", sub: "Meme" },
  GOAT: { name: "Goatseus Maximus", sub: "AI Meme" },
  MOODENG: { name: "Moo Deng", sub: "Meme" },
  FARTCOIN: { name: "Fartcoin", sub: "AI Meme" },
  "1000FLOKI": { name: "Floki (1000x perp)", sub: "Meme" },
  "1000SATS": { name: "Sats (1000x Ordinals)", sub: "BRC-20 Inscription" },
  DOGS: { name: "Dogs Community", sub: "TON Meme" },
  PENGU: { name: "Pudgy Penguins", sub: "NFT Ecosystem" },
  TRUMP: { name: "Official Trump", sub: "Political Meme" },
  MELANIA: { name: "Melania Meme", sub: "Political Meme" },
  GIGGLE: { name: "Giggle Academy", sub: "Charity Meme" },
  NOT: { name: "Notcoin", sub: "TON Gaming" },
  PEOPLE: { name: "ConstitutionDAO", sub: "DAO / Meme" },
  MEME: { name: "Memecoin (Memeland)", sub: "Meme Ecosystem" },
  ORDI: { name: "Ordinals", sub: "BRC-20 Inscription" },
  JASMY: { name: "JasmyCoin", sub: "IoT Data Democracy" },
  WLD: { name: "Worldcoin", sub: "Proof of Personhood" },

  // Metals / Gold Tokens on Delta
  XAUT: { name: "Tether Gold Perp", sub: "Tokenized Gold" },
  PAXG: { name: "Paxos Gold Perp", sub: "Tokenized Gold" }
};

const newEntries = [];

for (const m of missingCrypto) {
  const meta = KNOWN_META[m.base] || {
    name: m.base + " Token",
    sub: "DeFi / Altcoin"
  };
  newEntries.push({
    sym: m.base,
    pair: m.binancePair,
    kind: "crypto-perp",
    category: "Crypto",
    name: meta.name,
    sub: meta.sub,
    punchable: true,
    origin: "fill"
  });
}

for (const m of missingTradFi) {
  newEntries.push({
    sym: m.base,
    pair: m.binancePair,
    kind: "tradfi-perp",
    category: "TradFi",
    name: m.base + " bStocks Token",
    sub: "Tokenized Equity",
    punchable: true,
    origin: "fill"
  });
}

console.log("Total new Curated entries generated:", newEntries.length);
fs.writeFileSync("docs/EXPANDED_CURATED_ENTRIES.json", JSON.stringify(newEntries, null, 2));
console.log("Written to docs/EXPANDED_CURATED_ENTRIES.json");
