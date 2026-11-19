import { createHash, createPrivateKey, createPublicKey, randomUUID, sign, verify } from "node:crypto";
import { closeSync, existsSync, fsyncSync, linkSync, mkdirSync, openSync, readFileSync, unlinkSync,
  writeFileSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { join } from "node:path";
import { performance } from "node:perf_hooks";
import { DIMENSIONS, POLICY_ID, evaluateIntent, protectionGates,
  validFeature, validRuntime } from "./round_policy.mjs";

const SCHEMA = new URL("./market_telemetry.sql", import.meta.url);
const DOMAIN = Buffer.from("cg-terminal:round-evidence:v1\0", "utf8");
const ASSET_COUNT = 231;
const asserted = (condition, message) => { if (!condition) throw new Error(message); };
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const hex = (s) => typeof s === "string" && /^[a-f0-9]{64}$/.test(s);
const timestamp = (n) => Number.isSafeInteger(n) && n >= 0;
const ttl = (n) => timestamp(n) && n > 0;
const slug = (s) => typeof s === "string" && /^[A-Za-z0-9_-]{1,80}$/.test(s);
const ordered = (a, b) => a < b ? -1 : a > b ? 1 : 0;
const plain = (v) => v !== null && typeof v === "object" && !Array.isArray(v);
const readJson = (path) => JSON.parse(readFileSync(path, "utf8"));

// Restricted JCS profile: safe integers for ticks/cents/ms, strings for
// decimals, and Unicode scalar text. JS's sort uses JCS UTF-16 key order.
function canonical(value) {
  if (value === null || typeof value === "boolean") return JSON.stringify(value);
  if (typeof value === "number") {
    asserted(Number.isSafeInteger(value), "Non-integer or unsafe signed numeric field");
    return JSON.stringify(value);
  }
  if (typeof value === "string") {
    asserted(value.isWellFormed(), "Invalid Unicode in signed text");
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  asserted(plain(value), "Unsupported signed value");
  return `{${Object.keys(value).sort().map((k) => `${canonical(k)}:${canonical(value[k])}`).join(",")}}`;
}

const stableHash = (value) => sha(canonical(value));
const BUILD = stableHash(Object.fromEntries(["round_compiler.mjs", "round_policy.mjs",
  "market_telemetry.sql"].map((name) => [name, sha(readFileSync(new URL(name, import.meta.url)))])));

function manifestFrom(path) {
  const m = readJson(path);
  asserted(m.policy_id === POLICY_ID && ttl(m.runtime_max_age_ms) && ttl(m.btc_macro_max_age_ms) &&
    Array.isArray(m.assets) && m.assets.length === ASSET_COUNT, "Wrong policy or universe size");
  const ids = m.assets.map((asset) => asset.id);
  asserted(ids.every(slug) && new Set(ids).size === ASSET_COUNT &&
    ids.every((id, index) => index === 0 || ids[index - 1] < id), "Sort and deduplicate asset IDs");
  for (const asset of m.assets) {
    asserted(Array.isArray(asset.routes) && new Set(asset.routes).size === asset.routes.length &&
      asset.routes.every((v) => ["MT5", "DELTA"].includes(v)) &&
      [asset.alt, asset.crypto, asset.grade_b_allowed].every((v) => typeof v === "boolean") &&
      ttl(asset.min_wall_cents) && timestamp(asset.max_entry_tolerance_ticks) &&
      typeof asset.tick_unit === "string" && /^(?:0|[1-9]\d*)(?:\.\d+)?$/.test(asset.tick_unit) &&
      /[1-9]/.test(asset.tick_unit), "Missing asset metadata");
    asserted(plain(asset.dimensions) && Object.keys(asset.dimensions).length === DIMENSIONS.length,
      "Exactly 16 dimension rules required");
    for (const dim of DIMENSIONS) {
      const rule = asset.dimensions[dim];
      if (rule?.applies === false) {
        const maySkip = !asset.routes.length || (dim === 13 && !["BTC", "ETH"].includes(asset.id));
        asserted(maySkip && typeof rule.reason === "string" && rule.reason.trim().length > 0,
          "Unauthorized dimension exemption");
        continue;
      }
      asserted(rule?.applies === true && ttl(rule.max_age_ms) && plain(rule.subfeeds) &&
        Object.keys(rule.subfeeds).length > 0 &&
        Object.entries(rule.subfeeds).every(([id, age]) => slug(id) && ttl(age)),
      "Missing required subfeed contract");
      if (asset.routes.length && [8, 11].includes(dim)) {
        const required = dim === 8 ? ["spot", "perp"] : ["3d", "7d", "30d"];
        asserted(required.every((name) => Object.hasOwn(rule.subfeeds, name)), "Missing hard subfeeds");
      }
    }
  }
  return m;
}

function requestFrom(path, manifest) {
  const r = readJson(path);
  const now = Date.now();
  asserted(slug(r.round_id) && typeof r.nonce === "string" && /^[a-f0-9]{32,128}$/.test(r.nonce) &&
    timestamp(r.cutoff_ms) && timestamp(r.expires_ms) && r.cutoff_ms <= now && now < r.expires_ms &&
    r.expires_ms - r.cutoff_ms <= 120_000 &&
    r.manifest_sha256 === stableHash(manifest) && r.build_sha256 === BUILD, "Untrusted or expired round request");
  return r;
}

const WANTED = `
  SELECT json_extract(value, '$[0]') AS asset_id, json_extract(value, '$[1]') AS dim
  FROM json_each(?)
`;
const SNAPSHOT_SQL = `
  WITH wanted AS (${WANTED})
  SELECT wanted.asset_id, wanted.dim AS dimension, f.revision,
         f.observed_ms, f.received_ms, f.state, f.body
  FROM wanted
  LEFT JOIN latest_feature AS f ON f.revision = (
    SELECT candidate.revision FROM latest_feature AS candidate
    WHERE candidate.asset_id = wanted.asset_id AND candidate.dimension = wanted.dim
      AND candidate.received_ms <= ?
    ORDER BY candidate.received_ms DESC, candidate.revision DESC
    LIMIT 1
  )
  ORDER BY wanted.asset_id COLLATE BINARY, wanted.dim
`;

function subfeedState(body, rule, cutoff, receive) {
  if (!plain(body) || !plain(body.subfeeds)) return "FAILED";
  for (const [id, age] of Object.entries(rule.subfeeds)) {
    const sub = body.subfeeds[id];
    if (!sub || sub.state !== "VALID") return "INSUFFICIENT_COVERAGE";
    if (!hex(sub.sha256) || !timestamp(sub.observed_ms) || !timestamp(sub.received_ms) ||
        sub.observed_ms > sub.received_ms || sub.received_ms > receive ||
        typeof sub.source !== "string" || !sub.source) return "FAILED";
    if (cutoff - sub.observed_ms > age) return "STALE";
  }
  return "VALID";
}

function cellFor(row, rule, cutoff) {
  const id = { asset_id: row.asset_id, dimension: row.dimension };
  if (!rule.applies) return { ...id, state: "NOT_APPLICABLE", reason: rule.reason };
  if (row.revision === null) return { ...id, state: "MISSING" };
  const cell = { ...id, revision: row.revision, observed_ms: row.observed_ms,
    received_ms: row.received_ms };
  if (row.state !== "VALID") return { ...cell,
    state: row.state === "UNSUPPORTED" ? "UNSUPPORTED_REQUIRED" : row.state };
  if (cutoff - row.observed_ms > rule.max_age_ms) return { ...cell, state: "STALE" };
  try {
    const body = JSON.parse(row.body);
    canonical(body);
    const state = subfeedState(body, rule, cutoff, row.received_ms);
    if (state !== "VALID") return { ...cell, state };
    if (validFeature(row.dimension, body.data, cutoff))
      return { ...cell, state: "VALID", subfeeds: body.subfeeds, data: body.data };
  } catch {
    // Incomplete provider rows stay visible. They cannot produce trade evidence.
  }
  return { ...cell, state: "FAILED" };
}

function plannerComplete(runtime, manifest) {
  if (!Array.isArray(runtime.planner) || runtime.planner.length !== manifest.assets.length) return false;
  const intents = new Map();
  for (const intent of runtime.intents) {
    const list = intents.get(intent.asset_id) ?? [];
    list.push(intent.id);
    intents.set(intent.asset_id, list);
  }
  return manifest.assets.every((asset, index) => {
    const row = runtime.planner[index];
    const proposed = intents.get(asset.id) ?? [];
    if (row?.asset_id !== asset.id || !hex(row.evidence_sha256) ||
        !Array.isArray(row.intent_ids) || typeof row.reason_code !== "string" ||
        !/^[A-Z][A-Z0-9_]{1,79}$/.test(row.reason_code) ||
        canonical([...proposed].sort()) !== canonical(row.intent_ids)) return false;
    if (!asset.routes.length) return row.state === "OBSERVE_ONLY" && proposed.length === 0;
    return row.state === (proposed.length ? "PROPOSED" : "NO_SETUP");
  });
}

function readSnapshot(db, manifest, cutoff) {
  const assets = new Map(manifest.assets.map((asset) => [asset.id, asset]));
  const wanted = manifest.assets.flatMap((asset) => DIMENSIONS.map((dimension) => [asset.id, dimension]));
  wanted.push(["@runtime", 0]);
  let rows;
  const started = performance.now();
  db.exec("BEGIN");
  try {
    rows = db.prepare(SNAPSHOT_SQL).all(JSON.stringify(wanted), cutoff);
    db.exec("COMMIT");
  } catch (error) {
    db.exec("ROLLBACK");
    throw error;
  }
  const extractionMs = performance.now() - started;
  const runtimeRow = rows.shift();
  asserted(runtimeRow.asset_id === "@runtime" && rows.length === ASSET_COUNT * DIMENSIONS.length,
    "Snapshot lost an expected cell");
  const cells = rows.map((row) => cellFor(row, assets.get(row.asset_id).dimensions[row.dimension], cutoff));
  let runtime = null;
  if (runtimeRow.state === "VALID" && cutoff - runtimeRow.observed_ms <= manifest.runtime_max_age_ms) {
    try {
      const body = JSON.parse(runtimeRow.body);
      canonical(body);
      if (validRuntime(body, cutoff, manifest.runtime_max_age_ms) &&
          body.intents.every((intent) => assets.has(intent.asset_id)) &&
          body.btc_max_age_ms === manifest.btc_macro_max_age_ms) {
        runtime = { observed_ms: runtimeRow.observed_ms, received_ms: runtimeRow.received_ms,
          revision: runtimeRow.revision, data: body };
      }
    } catch {
      // A malformed runtime record freezes new intents and protection attestation.
    }
  }
  return { cells, runtime, extractionMs };
}

function outcomes(manifest, cells, runtime, cutoff) {
  const map = new Map();
  const coverage = {};
  let index = 0;
  for (const asset of manifest.assets) {
    const group = [];
    for (const dimension of DIMENSIONS) {
      const cell = cells[index++];
      const rule = asset.dimensions[dimension];
      asserted(cell?.asset_id === asset.id && cell.dimension === dimension, "Incorrect cell set or order");
      if (cell.state === "VALID") {
        asserted(rule.applies && timestamp(cell.observed_ms) && timestamp(cell.received_ms) &&
          cell.observed_ms <= cell.received_ms && cell.received_ms <= cutoff &&
          cutoff - cell.observed_ms <= rule.max_age_ms &&
          subfeedState(cell, rule, cutoff, cell.received_ms) === "VALID" &&
          validFeature(dimension, cell.data, cutoff), "Invalid signed evidence");
      } else if (cell.state === "NOT_APPLICABLE") {
        asserted(!rule.applies && cell.reason === rule.reason, "Unapproved applicability override");
      } else {
        asserted(rule.applies && ["MISSING", "STALE", "FAILED", "INSUFFICIENT_COVERAGE",
          "UNSUPPORTED_REQUIRED"].includes(cell.state), "Invalid cell state");
      }
      coverage[cell.state] = (coverage[cell.state] ?? 0) + 1;
      group.push(cell);
    }
    map.set(asset.id, { asset, cells: group });
  }
  asserted(index === cells.length, "Extra cell");
  if (runtime !== null) {
    asserted(timestamp(runtime.observed_ms) && timestamp(runtime.received_ms) &&
      runtime.observed_ms <= runtime.received_ms && runtime.received_ms <= cutoff &&
      cutoff - runtime.observed_ms <= manifest.runtime_max_age_ms &&
      validRuntime(runtime.data, cutoff, manifest.runtime_max_age_ms) &&
      runtime.data.btc_max_age_ms === manifest.btc_macro_max_age_ms, "Invalid runtime evidence");
  }
  const protections = protectionGates(runtime?.data);
  const planner_complete = runtime !== null && plannerComplete(runtime.data, manifest);
  const complete = planner_complete && (coverage.VALID ?? 0) + (coverage.NOT_APPLICABLE ?? 0) === cells.length;
  const candidates = [...(runtime?.data.intents ?? [])].sort((a, b) => ordered(a.id, b.id)).map((intent) => {
    const entry = map.get(intent.asset_id);
    asserted(entry, "Intent outside universe");
    const tested = evaluateIntent(intent, entry.asset, entry.cells, runtime.data, protections, cutoff);
    return { ...tested, rule_eligible: tested.eligible, eligible: complete && tested.eligible };
  });
  const eligible = candidates.filter((c) => c.eligible).map((c) => c.intent.id);
  return { coverage, planner_complete, protections, candidates, eligible_ids: eligible,
    state: !complete ? "AUDIT_INCOMPLETE" : eligible.length
      ? "AUDIT_COMPLETE_CANDIDATES" : "AUDIT_COMPLETE_NO_CANDIDATES" };
}

function keyId(key) {
  asserted(key.asymmetricKeyType === "ed25519", "Ed25519 key required");
  return sha(key.export({ type: "spki", format: "der" }));
}

const signedMessage = (digest) => Buffer.concat([DOMAIN, Buffer.from(digest, "hex")]);

function verifyEnvelope(raw, publicKey, request, manifest) {
  const { payload, digest, signature, key_id } = JSON.parse(raw);
  asserted(raw === canonical({ payload, digest, signature, key_id }), "Noncanonical envelope");
  asserted(key_id === keyId(publicKey) && hex(digest) && digest === stableHash(payload) &&
    typeof signature === "string" && /^[A-Za-z0-9_-]{86}$/.test(signature) &&
    verify(null, signedMessage(digest), publicKey, Buffer.from(signature, "base64url")), "Invalid signature");
  for (const field of ["round_id", "nonce", "cutoff_ms", "expires_ms", "manifest_sha256", "build_sha256"])
    asserted(payload[field] === request[field], `Wrong round binding: ${field}`);
  asserted(payload.policy_id === POLICY_ID && payload.schema_version === 1, "Unsupported schema/policy");
  const expected = outcomes(manifest, payload.cells, payload.runtime, request.cutoff_ms);
  asserted(canonical(expected) === canonical(payload.outcomes) && Date.now() < request.expires_ms,
    "Outcome mismatch or expired report");
  return { digest, state: expected.state };
}

function publish(directory, roundId, bytes) {
  mkdirSync(directory, { recursive: true, mode: 0o700 });
  const target = join(directory, `round_${roundId}.json`);
  const temp = join(directory, `.${randomUUID()}.tmp`);
  const fd = openSync(temp, "wx", 0o600);
  try {
    try {
      writeFileSync(fd, bytes);
      fsyncSync(fd);
    } finally {
      closeSync(fd);
    }
    try {
      linkSync(temp, target); // Atomic no-overwrite publication on NTFS/local POSIX.
    } catch (error) {
      if (error.code !== "EEXIST" || readFileSync(target, "utf8") !== bytes) throw error;
    }
  } finally {
    unlinkSync(temp);
  }
  return target;
}

function compile(dbPath, manifest, request, keyPath, outDir) {
  const privateKey = createPrivateKey(readFileSync(keyPath));
  const publicKey = createPublicKey(privateKey);
  asserted(existsSync(dbPath), "Run schema initialization first");
  const db = new DatabaseSync(dbPath);
  try {
    db.exec("PRAGMA foreign_keys = ON; PRAGMA synchronous = FULL; PRAGMA busy_timeout = 3000;");
    asserted(db.prepare("PRAGMA user_version").get().user_version === 1 &&
      db.prepare("PRAGMA journal_mode").get().journal_mode === "wal", "Run schema initialization first");
    const find = db.prepare("SELECT envelope FROM round WHERE round_id = ?");
    const existing = find.get(request.round_id);
    if (existing) {
      const summary = verifyEnvelope(existing.envelope, publicKey, request, manifest);
      return { ...summary, path: publish(outDir, request.round_id, existing.envelope), reused: true };
    }
    const { cells, runtime, extractionMs } = readSnapshot(db, manifest, request.cutoff_ms);
    const result = outcomes(manifest, cells, runtime, request.cutoff_ms);
    const { round_id, nonce, cutoff_ms, expires_ms, manifest_sha256, build_sha256 } = request;
    const payload = { schema_version: 1, policy_id: POLICY_ID, round_id, nonce, cutoff_ms,
      expires_ms, manifest_sha256, build_sha256, cells, runtime, outcomes: result };
    const digest = stableHash(payload);
    const signature = sign(null, signedMessage(digest), privateKey).toString("base64url");
    const envelope = canonical({ payload, digest, key_id: keyId(publicKey), signature });
    const write = db.prepare(`INSERT INTO round_cell
      (round_id, asset_id, dimension, state, observed_ms, received_ms, cell_digest)
      VALUES (?, ?, ?, ?, ?, ?, ?)`);
    const indexRows = cells.map((cell) => [round_id, cell.asset_id, cell.dimension, cell.state,
      cell.observed_ms ?? null, cell.received_ms ?? null, stableHash(cell)]);
    let sealed = envelope;
    db.exec("BEGIN IMMEDIATE");
    try {
      const winner = find.get(round_id);
      if (winner) {
        sealed = winner.envelope;
        verifyEnvelope(sealed, publicKey, request, manifest);
      } else {
        asserted(Date.now() < expires_ms, "Round expired before commit");
        db.prepare(`INSERT INTO round(round_id, nonce, cutoff_ms, expires_ms, digest, envelope, cell_count, state)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?)`)
          .run(round_id, nonce, cutoff_ms, expires_ms, digest, envelope, cells.length, result.state);
        for (const row of indexRows) write.run(...row);
      }
      db.exec("COMMIT");
    } catch (error) {
      db.exec("ROLLBACK");
      throw error;
    }
    const summary = sealed === envelope ? { digest, state: result.state }
      : verifyEnvelope(sealed, publicKey, request, manifest);
    return { ...summary, path: publish(outDir, round_id, sealed),
      extraction_ms: Math.round(extractionMs * 1000) / 1000, cells: cells.length };
  } finally {
    db.close();
  }
}

function main([command, ...args]) {
  if (command === "init" && args.length === 1) {
    const db = new DatabaseSync(args[0]);
    try {
      const { user_version } = db.prepare("PRAGMA user_version").get();
      asserted([0, 1].includes(user_version), "Use a reviewed database migration");
      db.exec(readFileSync(SCHEMA, "utf8"));
      return { schema_version: 1, path: args[0] };
    } finally {
      db.close();
    }
  }
  if (command === "fingerprint" && args.length === 1)
    return { manifest_sha256: stableHash(manifestFrom(args[0])), build_sha256: BUILD };
  if (command === "compile" && args.length === 5) {
    const [db, manifestPath, requestPath, key, outDir] = args;
    const m = manifestFrom(manifestPath);
    return compile(db, m, requestFrom(requestPath, m), key, outDir);
  }
  if (command === "verify" && args.length === 4) {
    const [report, manifestPath, requestPath, pubKey] = args;
    const m = manifestFrom(manifestPath);
    return verifyEnvelope(readFileSync(report, "utf8"), createPublicKey(readFileSync(pubKey)),
      requestFrom(requestPath, m), m);
  }
  throw new Error("Usage: init DB | fingerprint MANIFEST | compile DB MANIFEST REQUEST PRIVATE_KEY OUTDIR | verify REPORT MANIFEST REQUEST PUBLIC_KEY");
}

try {
  console.log(JSON.stringify(main(process.argv.slice(2))));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
