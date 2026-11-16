#!/usr/bin/env node
/**
 * Production start wrapper — runs .next/standalone/server.js.
 *
 * BIND ADDRESS: defaults to 0.0.0.0, NOT loopback.
 *
 * History (2026-11-16): this wrapper used to default to `127.0.0.1` on the
 * theory that a loopback bind is "safer". In this deployment that is wrong —
 * the terminal is shown through a per-port preview proxy that connects from
 * outside the loopback interface. A loopback-only bind answers `curl` inside
 * the sandbox and looks healthy, while the preview panel shows
 * "Connecting to sandbox…" forever, because the proxy cannot reach 127.0.0.1.
 * The platform had to override HOSTNAME=0.0.0.0 on every relaunch, and any
 * relaunch that missed the override silently produced an unreachable preview.
 *
 * Exposure is NOT controlled by the bind address here — the preview proxy is
 * the only path in, and the sandbox has no public inbound. Local-only use is
 * still available explicitly:  HOSTNAME=127.0.0.1 npm start
 *
 * BUILD GUARD: if the prebuilt `.next/standalone/server.js` is missing (a
 * recycled sandbox loses node_modules/.next — both are gitignored), this
 * wrapper BUILDS instead of exiting 1. Previously the platform auto-start ran
 * `node scripts/start-server.mjs` against an empty tree, printed
 * "✗ ... run `npm run build` first", exited 1, and the preview was permanently
 * dead until a human shelled in.
 */
import { spawn, spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { join } from "node:path";

if (typeof process.loadEnvFile === "function" && existsSync(".env")) {
  try {
    process.loadEnvFile(".env");
  } catch (err) {
    console.warn("⚠️ Could not load .env file:", err.message);
  }
}

const server = join(process.cwd(), ".next", "standalone", "server.js");
const standaloneMissing = () => !existsSync(server);

/** Build (deps first when node_modules is absent). Returns true on success. */
function build() {
  if (!existsSync(join(process.cwd(), "node_modules"))) {
    console.log("⚙  node_modules missing — installing dependencies first");
    const install = spawnSync("npm", ["ci", "--no-audit", "--no-fund"], {
      stdio: "inherit",
      shell: process.platform === "win32",
    });
    if (install.status !== 0) {
      console.error("✗ npm ci failed — cannot start without dependencies");
      return false;
    }
  }
  console.log("⚙  .next/standalone missing — building (this takes ~30-60s)");
  const b = spawnSync("npm", ["run", "build"], {
    stdio: "inherit",
    shell: process.platform === "win32",
    env: { ...process.env, NODE_ENV: "production", NEXT_TELEMETRY_DISABLED: "1" },
  });
  if (b.status !== 0) {
    console.error("✗ build failed — see the output above");
    return false;
  }
  return true;
}

if (standaloneMissing() && !build()) process.exit(1);
if (standaloneMissing()) {
  console.error("✗ .next/standalone/server.js still missing after a build");
  process.exit(1);
}

// Bind all interfaces by default: the per-port preview proxy arrives from
// outside loopback. Override with HOSTNAME=127.0.0.1 for local-only use.
// `??=` alone is not enough — `HOSTNAME=` in a launcher script yields "",
// which Next treats as unset and logs an unhelpful ":3000".
if (!process.env.HOSTNAME) process.env.HOSTNAME = "0.0.0.0";
process.env.NODE_ENV ||= "production";
// The platform edge proxy routes preview traffic to port 3000 by default; any
// other port is unreachable from the public URL. Pin the default unless the
// caller sets PORT explicitly.
if (!process.env.PORT) process.env.PORT = "3000";

console.log(
  `▲ starting standalone server on ${process.env.HOSTNAME}:${process.env.PORT}`
);

/**
 * PORT ALREADY SERVING: a stale server on the port is the normal state after a
 * container restart (the platform relaunches this wrapper while the old
 * standalone process is still holding :3000). Crashing with EADDRINUSE there
 * produces a preview that looks dead even though something is answering — or,
 * worse, silently leaves the OLD code serving while the operator believes a
 * fresh build went live. Detect it and say so plainly instead.
 */
const probe = await probePort(process.env.HOSTNAME, Number(process.env.PORT));
if (probe.serving) {
  console.log(
    `▲ ${process.env.HOSTNAME}:${process.env.PORT} is already serving ` +
      `(GET /api/health -> ${probe.status}` +
      (probe.uptimeSec != null ? `, uptime ${probe.uptimeSec}s` : "") +
      ")"
  );
  console.log("▲ reusing the running server — not spawning a duplicate");
  // Stay alive so the platform keeps a live process handle; the existing
  // server keeps serving. Exiting would make the preview look crashed.
  setInterval(() => {}, 1 << 30);
} else {
  const child = spawn(process.execPath, [server], {
    stdio: "inherit",
    env: process.env,
  });
  child.on("exit", (code, signal) => {
    if (signal) process.kill(process.pid, signal);
    else process.exit(code ?? 0);
  });
}

/** Cheap liveness probe of the configured port. Never throws. */
async function probePort(host, port) {
  const h = host === "0.0.0.0" || host === "::" ? "127.0.0.1" : host;
  try {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), 1500);
    const r = await fetch(`http://${h}:${port}/api/health`, { signal: ctl.signal });
    clearTimeout(t);
    let uptimeSec = null;
    if (r.ok) {
      try {
        uptimeSec = (await r.json())?.uptimeSec ?? null;
      } catch {
        /* non-JSON on the port is still "something is serving" */
      }
    }
    return { serving: true, status: r.status, uptimeSec };
  } catch {
    return { serving: false, status: null, uptimeSec: null };
  }
}
