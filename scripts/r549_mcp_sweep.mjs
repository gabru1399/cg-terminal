/**
 * R549 round — MCP tool sweep via mcp/server.mjs (same data the Antigravity agent sees).
 * Usage: node scripts/r549_mcp_sweep.mjs <tool> [jsonArgs]
 */
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import path from "node:path";

const require = createRequire(import.meta.url);
const serverPath = path.resolve("mcp/server.mjs");
const mod = await import(pathToFileURL(serverPath).href);

// MCP server may export tools registry or handle() — probe common shapes
const tools = mod.tools ?? mod.TOOLS ?? mod.default?.tools;
const handle = mod.handle ?? mod.callTool ?? mod.default?.handle ?? mod.default?.callTool;

const name = process.argv[2];
const args = process.argv[3] ? JSON.parse(process.argv[3]) : {};

if (!name) {
  console.log("exports:", Object.keys(mod).join(", "));
  console.log("tools:", tools ? (Array.isArray(tools) ? tools.map((t) => t.name).join(", ") : Object.keys(tools).join(", ")) : "n/a");
  process.exit(0);
}

if (typeof handle !== "function") {
  console.error("no handle/callTool export found; exports were:", Object.keys(mod).join(", "));
  process.exit(2);
}

try {
  const res = await handle(name, args);
  console.log(typeof res === "string" ? res : JSON.stringify(res));
} catch (e) {
  console.error("tool error:", e.message);
  process.exit(1);
}
