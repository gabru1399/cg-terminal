// Round inputs use safe integers: per-asset ticks, cents, basis points and UTC ms.
// Profiles define evidence requirements. This module defines decision rules.
export const POLICY_ID = "cg-terminal/phase2-shadow-v1";
export const DIMENSIONS = Array.from({ length: 16 }, (_, index) => index + 1);
const HOUR_MS = 3_600_000;
const isInt = Number.isSafeInteger;
const positive = (value) => isInt(value) && value > 0;
const nonnegative = (value) => isInt(value) && value >= 0;
const member = (value, allowed) => allowed.includes(value);
const digest = (value) => typeof value === "string" && /^[a-f0-9]{64}$/.test(value);
const side = (value) => member(value, ["LONG", "SHORT"]);
const direction = (value) => member(value, [-1, 0, 1]);
const interval = (value) => positive(value?.lo) && positive(value?.hi) && value.lo <= value.hi;
const list = (value, check) => Array.isArray(value) && value.every(check);

const validate = [
  null,
  (d) => isInt(d.basis_bp),
  (d) => [d.session_poc, d.day_poc, d.atr_ticks].every(positive) &&
    list(d.high_volume_nodes, interval),
  (d) => positive(d.day_vwap) && isInt(d.z_bp),
  (d) => [d.m15, d.h1, d.h4, d.d1].every(direction) &&
    member(d.regime, ["TREND_UP", "TREND_DOWN", "RANGE_BALANCE", "TRANSITION"]),
  (d) => [d.h1_rsi_bp, d.h4_rsi_bp].every((n) => nonnegative(n) && n <= 10_000) &&
    direction(d.divergence),
  (d) => isInt(d.delta_cents) && positive(d.poc) && nonnegative(d.volume_cents),
  (d) => list(d.signals, (s) => positive(s?.price) && nonnegative(s?.at_ms) && side(s?.side) &&
    member(s.kind, ["abs", "sdiv", "div", "exh", "trap"])),
  (d) => isInt(d.spot_delta_cents) && isInt(d.perp_delta_cents) && direction(d.price_swing) &&
    member(d.absorption, ["LONG", "SHORT", "NONE"]),
  (d) => list(d.walls, (w) => interval(w) && member(w.side, ["BID", "ASK"]) &&
    nonnegative(w.usd_cents) && nonnegative(w.share_bp) && w.share_bp <= 10_000 &&
    nonnegative(w.age_ms) && typeof w.confirmed === "boolean"),
  (d) => list(d.orders, (o) => positive(o?.price) && nonnegative(o?.usd_cents) &&
    member(o.side, ["BID", "ASK"])),
  (d) => list(d.hazards, interval),
  (d) => member(d.dominant, ["ABOVE", "BELOW", "NONE"]) && (d.ratio_milli === null
    ? d.dominant !== "NONE" && d.one_sided === true
    : isInt(d.ratio_milli) && d.ratio_milli >= 1000 && d.one_sided === false),
  (d) => direction(d.gamma),
  (d) => isInt(d.oi_change_bp) && isInt(d.price_change_bp),
  (d) => isInt(d.funding_apr_bp),
  (d) => nonnegative(d.liq_5m_cents),
];

export function validFeature(dimension, data, cutoff) {
  return data !== null && typeof data === "object" && !Array.isArray(data) &&
    validate[dimension](data) &&
    (dimension !== 7 || data.signals.every((signal) => signal.at_ms <= cutoff));
}

const verdict = (passed, note) => ({ state: passed ? "PASS" : "VETO", note });
const unknown = (note) => ({ state: "INDETERMINATE", note });
const unsigned = (cents) => {
  if (!nonnegative(cents)) throw new Error("Expected nonnegative integer cents");
  return BigInt(cents);
};

// For a fresh, reconciled account snapshot. Each scenario must value the same
// entire open book mark-to-stressed-exit in USD cents, including exit costs.
// Unknown coverage/limits return zero. Pending reserves exclude filled slices.
export function sharedHeadroom(snapshot) {
  if (snapshot?.verified !== true || snapshot?.account_coverage_complete !== true)
    return { budget_cents: 0, reason: "UNVERIFIED_ACCOUNT_RISK" };
  try {
    const { equity_cents, daily_floor_cents, internal_floor_cents, total_floor_cents,
      pending_reserve_cents, shock_reserve_cents, epsilon_cents, scenarios,
      open_ticket_ids, remaining_heat_cents } = snapshot;
    const floor = Math.max(daily_floor_cents, internal_floor_cents, total_floor_cents);
    [daily_floor_cents, internal_floor_cents, total_floor_cents, equity_cents,
      pending_reserve_cents, remaining_heat_cents, shock_reserve_cents].forEach(unsigned);
    if (!positive(epsilon_cents) || !Array.isArray(scenarios) || !scenarios.length ||
        !Array.isArray(open_ticket_ids) ||
        open_ticket_ids.some((id) => typeof id !== "string" || !id) ||
        new Set(open_ticket_ids).size !== open_ticket_ids.length) throw new Error("Bad scenario scope");
    let stressed = 0n;
    for (const scenario of scenarios) {
      if (Object.keys(scenario).length !== open_ticket_ids.length ||
          !open_ticket_ids.every((id) => Object.hasOwn(scenario, id))) throw new Error("Missing ticket");
      const loss = open_ticket_ids.reduce((sum, id) => sum + unsigned(scenario[id]), 0n);
      if (loss > stressed) stressed = loss;
    }
    const spare = unsigned(equity_cents) - unsigned(floor) - stressed
      - unsigned(pending_reserve_cents) - unsigned(shock_reserve_cents) - unsigned(epsilon_cents);
    const budget = spare < unsigned(remaining_heat_cents) ? spare : unsigned(remaining_heat_cents);
    return { budget_cents: budget > 0n ? Number(budget) : 0, binding_floor_cents: floor,
      stressed_open_cents: stressed.toString(), reason: budget > 0n ? "MODELED_HEADROOM" : "NO_HEADROOM" };
  } catch {
    return { budget_cents: 0, reason: "UNVERIFIED_ACCOUNT_RISK" };
  }
}

function ownedPosition(position) {
  return typeof position?.ticket === "string" && position.ticket.length > 0 &&
    side(position.side) && member(position.venue, ["MT5", "DELTA"]) &&
    position.owned_verified === true &&
    digest(position.evidence_sha256) &&
    (position.venue !== "MT5" || (position.comment === "cg_terminal" && position.magic === 42001)) &&
    [position.stop, position.initial_r_ticks, position.breakeven_stop,
      position.time_stop_minimum].every(positive) &&
    nonnegative(position.bars_held) && nonnegative(position.mfe_ticks);
}

export function validRuntime(runtime, cutoff, maxAge) {
  return runtime?.reconciled === true && runtime?.ownership_complete === true &&
    digest(runtime.snapshot_sha256) &&
    list(runtime.positions, ownedPosition) &&
    new Set(runtime.positions.map((p) => `${p.venue}:${p.ticket}`)).size === runtime.positions.length &&
    list(runtime.intents, (i) => typeof i?.asset_id === "string" && side(i.side) &&
      member(i.venue, ["MT5", "DELTA"]) && typeof i.id === "string" && i.id.length > 0 &&
      /^S[1-9]$/.test(i.setup) && member(i.phase, ["PASSIVE", "CONFIRMED_SWEEP", "OTHER"]) &&
      [i.entry, i.stop, i.target, i.stop_distance_without_spread, i.stressed_exit,
        i.risk_cents, i.reward_cents, i.bid, i.ask].every(positive) &&
      i.ask >= i.bid && typeof i.post_only === "boolean" &&
      digest(i.valuation_sha256) && digest(i.plan_sha256) &&
      [i.quote_at_ms, i.valued_at_ms].every((ts) =>
        nonnegative(ts) && ts <= cutoff && cutoff - ts <= maxAge) &&
      (i.venue === "MT5" ? positive(i.session_p95_spread_ticks) : nonnegative(i.session_p95_spread_ticks)) &&
      nonnegative(i.entry_tolerance_ticks) &&
      (i.oracle === null || (nonnegative(i.oracle) && i.oracle <= 100)) &&
      typeof i.exhaustion_confirmed === "boolean") &&
    new Set(runtime.intents.map((i) => i.id)).size === runtime.intents.length &&
    member("MT5", Object.keys(runtime.accounts ?? {})) &&
    member("DELTA", Object.keys(runtime.accounts ?? {})) &&
    ["MT5", "DELTA"].every((venue) => {
      const a = runtime.accounts[venue];
      return a?.verified === true && a?.reservations_reconciled === true &&
        digest(a.evidence_sha256) &&
        [a.equity_cents, a.headroom_cents, a.heat_available_cents, a.occupied_slots, a.slot_limit,
          a.crypto_long_slots, a.crypto_short_slots].every(nonnegative) && a.slot_limit > 0;
    });
}

export function protectionGates(runtime) {
  if (!runtime) return {
    "05": unknown("Fresh reconciled protection snapshot required"),
    "06": unknown("Fresh reconciled protection snapshot required"),
  };
  const failsTime = [];
  const failsBE = [];
  for (const p of runtime.positions) {
    const tighter = (stop) => p.side === "LONG" ? p.stop >= stop : p.stop <= stop;
    if (p.bars_held >= 8 && 2n * BigInt(p.mfe_ticks) < BigInt(p.initial_r_ticks) &&
        !tighter(p.time_stop_minimum)) failsTime.push(p.ticket);
    if (p.mfe_ticks >= p.initial_r_ticks && !tighter(p.breakeven_stop)) failsBE.push(p.ticket);
  }
  return {
    "05": { ...verdict(!failsTime.length, "Eight-bar time-stop check"), affected_tickets: failsTime.sort() },
    "06": { ...verdict(!failsBE.length, "Fee-aware breakeven check"), affected_tickets: failsBE.sort() },
  };
}

const abs = (val) => val < 0n ? -val : val;
const bi = (val) => BigInt(val);
const distance = (a, b) => abs(bi(a) - bi(b));
const intersects = (zone, low, high) => zone.lo <= high && low <= zone.hi;
const GATES = Array.from({ length: 11 }, (_, index) => String(index + 1).padStart(2, "0"));

export function evaluateIntent(intent, asset, cells, runtime, protection, cutoff) {
  const evidence = cells.map(({ dimension, state }) => ({ dimension, state }));
  const base = { intent, evidence };
  const vetoes = [];
  if (!asset.routes.includes(intent.venue)) vetoes.push("ROUTE_NOT_AUTHORIZED");
  if (cells.some((cell) => !member(cell.state, ["VALID", "NOT_APPLICABLE"])))
    vetoes.push("INCOMPLETE_ASSET_EVIDENCE");
  if (vetoes.length) return { ...base, vetoes, score_x2: null, grade: null,
    gates: GATES.map((id) => ({ id, ...(protection[id] ?? unknown("Missing authorized inputs")) })),
    eligible: false };

  const d = Object.fromEntries(cells.map((cell) => [cell.dimension, cell.data]));
  const sign = intent.side === "LONG" ? 1 : -1;
  const trip = bi(sign) * (bi(intent.entry) - bi(intent.stop));
  const target = bi(sign) * (bi(intent.target) - bi(intent.entry));
  const spread = bi(intent.ask) - bi(intent.bid);
  const stressedSpread = spread > bi(intent.session_p95_spread_ticks)
    ? spread : bi(intent.session_p95_spread_ticks);
  const structural = bi(intent.stop_distance_without_spread);
  const twiceMid = bi(intent.ask) + bi(intent.bid);
  const delta = intent.venue === "DELTA";
  const spreadFits = delta ? 5n * spread < structural && 20_000n * spread < 15n * twiceMid
    : 5n * stressedSpread <= structural;
  const pocClear = [d[2].session_poc, d[2].day_poc, d[3].day_vwap].every((p) =>
    200n * distance(p, intent.stop) >= bi(p) || distance(p, intent.stop) >= bi(d[2].atr_ticks));
  const noPool = !d[11].hazards.some((h) =>
    intersects(h, Math.min(intent.stop, intent.entry), Math.max(intent.stop, intent.entry)));
  const pathName = sign === 1 ? "ABOVE" : "BELOW";
  const highSkew = d[12].one_sided || d[12].ratio_milli >= 2500;
  const passive = intent.phase === "PASSIVE";
  const sameDirectionCvd = Math.sign(d[8].spot_delta_cents) === sign &&
    Math.sign(d[8].perp_delta_cents) === sign && d[8].price_swing === sign;
  const goodCvd = sameDirectionCvd || d[8].absorption === intent.side;
  const qualifiedWalls = d[9].walls.filter((w) => w.confirmed && w.age_ms > HOUR_MS &&
    (w.usd_cents >= asset.min_wall_cents || w.share_bp >= 2000));
  const inEntry = (lo, hi) =>
    bi(lo) <= bi(intent.entry) + bi(intent.entry_tolerance_ticks) &&
    bi(hi) >= bi(intent.entry) - bi(intent.entry_tolerance_ticks);
  const footprint = d[7].signals.filter((s) => s.side === intent.side &&
    cutoff - s.at_ms <= 8 * HOUR_MS && inEntry(s.price, s.price));
  const trendCompatible = d[4].regime === (sign === 1 ? "TREND_UP" : "TREND_DOWN");
  const discountOrPremium = Math.sign(d[3].z_bp) === -sign && Math.abs(d[3].z_bp) <= 10_000;
  const meanRetest = intent.entry === d[3].day_vwap || intent.entry === d[2].day_poc;
  const wallBackstop = qualifiedWalls.some((w) =>
    w.side === (sign === 1 ? "BID" : "ASK") && inEntry(w.lo, w.hi));
  const opposingWall = qualifiedWalls.some((w) => {
    if (w.side !== (sign === 1 ? "ASK" : "BID")) return false;
    const near = sign === 1 ? bi(w.lo) - bi(intent.entry) : bi(intent.entry) - bi(w.hi);
    const far = sign === 1 ? bi(w.hi) - bi(intent.entry) : bi(intent.entry) - bi(w.lo);
    return far >= 0n && 2n * near <= 3n * trip;
  });
  const gamma = d[13]?.gamma;
  const factors = [
    trendCompatible && d[4].h4 === sign && d[4].d1 === sign ? 4 : 0,
    discountOrPremium || meanRetest ? 3 : 0,
    footprint.some((s) => member(s.kind, ["abs", "sdiv"])) ? 4
      : footprint.some((s) => member(s.kind, ["div", "exh"])) ? 2 : 0,
    wallBackstop ? 3 : 0,
    goodCvd ? 2 : 0,
    !highSkew && noPool && d[12].dominant === pathName ? 3 : 0,
    (gamma === 1 && member(intent.setup, ["S2", "S5"])) ||
      (gamma === -1 && member(intent.setup, ["S1", "S8"])) ? 2 : 0,
    delta && intent.post_only && 5n * spread < structural && 20_000n * spread < 5n * twiceMid ? 2 : 0,
  ];
  const score = factors.reduce((total, points) => total + points, 0);
  const grade = score >= 14 ? "A" : score >= 10 ? "B" : "NO_TRADE";
  const account = runtime.accounts[intent.venue];
  const gradeBudget = bi(account.equity_cents) * (grade === "A" ? 100n : 50n) / 10_000n;
  const loss = bi(intent.risk_cents);
  const reward = bi(intent.reward_cents);
  const makerAtQuote = intent.post_only &&
    (intent.side === "LONG" ? intent.entry < intent.ask : intent.entry > intent.bid);
  const spreadValid = trip > 0n && structural <= trip && spreadFits && (!delta || makerAtQuote);
  const stressDistance = bi(sign) * (bi(intent.entry) - bi(intent.stressed_exit));
  const riskFits = loss <= (delta ? 50n : 600n) && loss <= gradeBudget &&
    loss <= bi(account.headroom_cents) && loss <= bi(account.heat_available_cents);
  const qualifiedB = grade !== "B" || asset.grade_b_allowed;
  const netPayoff = delta && grade === "A" ? 2n * reward >= 5n * loss : reward >= 2n * loss;
  const oracle = !(delta && grade === "A") ||
    (intent.oracle !== null && (intent.oracle <= 35 || intent.oracle >= 65));
  const slots = account.occupied_slots < (grade === "B"
    ? Math.min(2, account.slot_limit) : account.slot_limit);
  const correlated = !asset.crypto ||
    (sign === 1 ? account.crypto_long_slots : account.crypto_short_slots) < 2;
  const gate10 = asset.alt && sign === -1
    ? runtime.btc?.verified === true && nonnegative(runtime.btc.distance_from_low_bp) &&
      digest(runtime.btc.evidence_sha256) && nonnegative(runtime.btc.at_ms) &&
      runtime.btc.at_ms <= cutoff && cutoff - runtime.btc.at_ms <= runtime.btc_max_age_ms &&
      nonnegative(runtime.btc_max_age_ms) &&
      isInt(runtime.btc.vwap_z_bp) && typeof runtime.btc.macro_support_test === "boolean"
      ? verdict(runtime.btc.distance_from_low_bp > 75 && runtime.btc.vwap_z_bp >= -20_000 &&
        !runtime.btc.macro_support_test, "BTC macro anchor")
      : unknown("Fresh BTC macro anchor required")
    : verdict(true, "BTC alt-short restriction inapplicable");
  if (Math.abs(d[1].basis_bp) > 50) vetoes.push("D01_BASIS");
  if (intent.entry_tolerance_ticks > asset.max_entry_tolerance_ticks)
    vetoes.push("ENTRY_ZONE_EXCEEDS_POLICY");
  if (d[8].spot_delta_cents > 0 && d[8].perp_delta_cents < 0 && sign === -1)
    vetoes.push("D08_SPOT_BUYING_PERP_SELLING");
  if (opposingWall) vetoes.push("D09_OPPOSING_WALL_WITHIN_1_5R");
  if (member(intent.setup, ["S7", "S8"]) && sign * d[3].z_bp >= 20_000)
    vetoes.push("D03_EXTENDED_CONTINUATION");
  const gates = {
    "01": verdict(pocClear && !d[2].high_volume_nodes.some((h) => intersects(h, intent.stop, intent.stop)),
      "Auction clearance in ticks"),
    "02": verdict(noPool, "No qualified liquidation shelf intersects the stop path"),
    "03": verdict(!(highSkew && d[12].dominant === pathName && intent.phase !== "CONFIRMED_SWEEP") &&
      (intent.phase !== "CONFIRMED_SWEEP" || intent.setup === "S1"), "Directional LSR restriction"),
    "04": verdict(spreadValid, "Venue spread and planned stop"),
    ...protection,
    "07": verdict(grade !== "NO_TRADE" && target > 0n && riskFits && qualifiedB && netPayoff && oracle,
      "Confluence, conservative caps and net payoff"),
    "08": verdict(d[16].liq_5m_cents <= 50_000_000 ||
      (!passive && intent.phase === "CONFIRMED_SWEEP" && intent.exhaustion_confirmed),
      "Five-minute cascade restriction"),
    "09": verdict(slots && correlated, "Occupied and reserved venue slots"),
    "10": gate10,
    "11": verdict(trip > 0n && 5n * stressDistance >= 6n * trip,
      "Venue valuation uses at least 120% of the executable stop distance"),
  };
  return { ...base, factors_x2: factors, score_x2: score, grade, vetoes,
    gates: GATES.map((id) => ({ id, ...gates[id] })),
    eligible: !vetoes.length && Object.values(gates).every((gate) => gate.state === "PASS") };
}
