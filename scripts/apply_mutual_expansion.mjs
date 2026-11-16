import fs from "fs";

const curatedFile = "src/lib/universe/curated.ts";
let content = fs.readFileSync(curatedFile, "utf8");

const expanded = JSON.parse(fs.readFileSync("docs/EXPANDED_CURATED_ENTRIES.json", "utf8"));
console.log("Loading", expanded.length, "expanded entries...");

// Check if already added
if (content.includes("MUTUAL DELTA & BINANCE EXPANSION")) {
  console.log("Already expanded!");
  process.exit(0);
}

// Format new entries
const lines = [
  "",
  "  // ─── MUTUAL DELTA & BINANCE EXPANSION (173 assets) ──────────────────────"
];

for (const a of expanded) {
  lines.push(
    `  { sym: "${a.sym}", pair: "${a.pair}", kind: "${a.kind}", category: "${a.category}", name: "${a.name.replace(/"/g, '\\"')}", sub: "${a.sub.replace(/"/g, '\\"')}", punchable: true, origin: "fill" },`
  );
}

const insertionPoint = `  // ─── CLASSIC 3 (no Binance perp — Yahoo/tradeXYZ venues) ──────────────`;
if (!content.includes(insertionPoint)) {
  console.error("Insertion point not found!");
  process.exit(1);
}

content = content.replace(insertionPoint, lines.join("\n") + "\n\n" + insertionPoint);

fs.writeFileSync(curatedFile, content);
console.log("Updated", curatedFile, "successfully!");
