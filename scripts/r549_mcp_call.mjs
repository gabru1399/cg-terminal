/**
 * R549 round — MCP client: speaks JSON-RPC over stdio to mcp/server.mjs.
 * Usage: node scripts/r549_mcp_call.mjs <tool> [jsonArgs]
 */
import { spawn } from "node:child_process";

const name = process.argv[2];
const args = process.argv[3] ? JSON.parse(process.argv[3]) : {};
const p = spawn("node", ["mcp/server.mjs"], { stdio: ["pipe", "pipe", "pipe"] });

let buf = "";
const send = (obj) => p.stdin.write(JSON.stringify(obj) + "\n");

p.stdout.on("data", (d) => {
  buf += d.toString();
  let idx;
  while ((idx = buf.indexOf("\n")) >= 0) {
    const line = buf.slice(0, idx).trim();
    buf = buf.slice(idx + 1);
    if (!line) continue;
    try {
      const msg = JSON.parse(line);
      if (msg.id === 1) {
        send({ jsonrpc: "2.0", method: "tools/call", id: 2, params: { name, arguments: args } });
      } else if (msg.id === 2) {
        const text = (msg.result?.content ?? []).map((c) => c.text).join("\n");
        console.log(text.slice(0, 12_000));
        p.kill();
        process.exit(0);
      }
    } catch {
      // non-JSON preamble line — skip
    }
  }
});
p.stderr.on("data", () => {}); // readiness banner
setTimeout(() => {
  console.error("timeout waiting for MCP response");
  p.kill();
  process.exit(1);
}, 45_000);

send({ jsonrpc: "2.0", method: "initialize", id: 1, params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "r549-sweep", version: "1.0" } } });
