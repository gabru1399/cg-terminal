/**
 * R384 — Quantitative Architecture Inquest Response (zai-desk)
 * Delivers the 5-challenge analysis to the human operator in document form.
 * Cover: R2 (Double-Rule Frame), IG-1 palette (finance) — same validated recipe as QR report.
 */
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, WidthType, BorderStyle,
  ShadingType, TableOfContents, PageBreak, PageNumber, TableLayoutType,
} = require("docx");
const fs = require("fs");

const P = {
  bg: "1A1A1A", accent: "C9A84C",
  cover: { titleColor: "FFFFFF", subtitleColor: "B0B8C0", metaColor: "90989F", footerColor: "687078" },
  table: { headerBg: "C9A84C", headerText: "1A1A1A", accentLine: "C9A84C", innerLine: "DDD5C0", surface: "F5F2E8" },
};

const noBorders = { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } };
const allNoBorders = { ...noBorders, insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE } };

function splitTitleLines(title, charsPerLine) {
  if (title.length <= charsPerLine) return [title];
  const breakAfter = new Set([..."，。、；：！？", ..."的与和及之在于为", ..."-_—–·/ \t:"]);
  const lines = []; let remaining = title;
  while (remaining.length > charsPerLine) {
    let breakAt = -1;
    for (let i = Math.min(charsPerLine, remaining.length - 1); i >= Math.floor(charsPerLine * 0.6); i--) {
      if (breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
    }
    if (breakAt === -1) breakAt = charsPerLine;
    lines.push(remaining.slice(0, breakAt).trim());
    remaining = remaining.slice(breakAt).trim();
  }
  if (remaining) lines.push(remaining);
  if (lines.length >= 2 && lines[lines.length - 1].length <= 4) {
    const last = lines.pop(); lines[lines.length - 1] += " " + last;
  }
  return lines;
}
function calcTitleLayout(title, maxWidthTwips, preferredPt = 40, minPt = 24) {
  const charsPerLine = (pt) => Math.floor(maxWidthTwips / (pt * 20));
  let titlePt = preferredPt, lines;
  while (titlePt >= minPt) {
    const cpl = charsPerLine(titlePt);
    if (cpl < 2) { titlePt -= 2; continue; }
    lines = splitTitleLines(title, cpl);
    if (lines.length <= 3) break;
    titlePt -= 2;
  }
  if (!lines || lines.length > 3) { lines = splitTitleLines(title, charsPerLine(minPt)); titlePt = minPt; }
  return { titlePt, titleLines: lines };
}
function calcCoverSpacing(p) {
  const { titleLineCount = 1, titlePt = 36, hasSubtitle = false, hasEnglishLabel = false, metaLineCount = 0, fixedHeight = 800, pageHeight = 16838 } = p;
  const SAFETY = 1200;
  const usableHeight = pageHeight - SAFETY;
  const titleHeight = titleLineCount * (titlePt * 23 + 200);
  const subtitleHeight = hasSubtitle ? (12 * 23 + 600) : 0;
  const englishLabelHeight = hasEnglishLabel ? (9 * 23 + 600) : 0;
  const metaHeight = metaLineCount * (10 * 23 + 100);
  const contentHeight = titleHeight + subtitleHeight + englishLabelHeight + metaHeight + fixedHeight + 900;
  const safeRemaining = Math.max(usableHeight - contentHeight, 400);
  const FOOTER_MIN = 800;
  const rawTop = Math.floor(safeRemaining * 0.45), rawBottom = Math.floor(safeRemaining * 0.45);
  const bottomSpacing = Math.max(rawBottom, FOOTER_MIN);
  const topSpacing = Math.max(rawTop - Math.max(0, FOOTER_MIN - rawBottom), 400);
  return { topSpacing, bottomSpacing };
}

function buildCoverR2(config) {
  const C = config.palette;
  const padL = 1400, padR = 1000;
  const availableWidth = 11906 - padL - padR - 300;
  const { titlePt, titleLines } = calcTitleLayout(config.title, availableWidth, 36, 22);
  const titleSize = titlePt * 2;
  const spacing = calcCoverSpacing({ titleLineCount: titleLines.length, titlePt, hasSubtitle: !!config.subtitle, hasEnglishLabel: !!config.englishLabel, metaLineCount: (config.metaLines || []).length, fixedHeight: 500 });
  const rule = { style: BorderStyle.SINGLE, size: 12, color: C.accent, space: 10 };
  const children = [];
  children.push(new Paragraph({ spacing: { before: spacing.topSpacing } }));
  children.push(new Paragraph({ indent: { left: padL, right: padR }, border: { bottom: { ...rule, size: 18 } }, spacing: { after: 120 } }));
  children.push(new Paragraph({ indent: { left: padL + 600, right: padR + 600 }, border: { bottom: { ...rule, size: 4 } }, spacing: { after: 600 } }));
  if (config.englishLabel) {
    children.push(new Paragraph({ indent: { left: padL }, spacing: { after: 300 }, children: [new TextRun({ text: config.englishLabel.split("").join("  "), size: 19, color: C.accent, font: { ascii: "Calibri", eastAsia: "SimHei" }, characterSpacing: 40 })] }));
  }
  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({ indent: { left: padL }, spacing: { after: i < titleLines.length - 1 ? 100 : 300, line: Math.ceil(titlePt * 23), lineRule: "atLeast" }, children: [new TextRun({ text: titleLines[i], size: titleSize, bold: true, color: C.cover.titleColor, font: { eastAsia: "SimHei", ascii: "Arial" } })] }));
  }
  if (config.subtitle) {
    children.push(new Paragraph({ indent: { left: padL }, spacing: { after: 700 }, children: [new TextRun({ text: config.subtitle, size: 24, color: C.cover.subtitleColor, font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })] }));
  }
  for (const line of (config.metaLines || [])) {
    children.push(new Paragraph({ indent: { left: padL }, spacing: { after: 90 }, children: [new TextRun({ text: line, size: 22, color: C.cover.metaColor, font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })] }));
  }
  children.push(new Paragraph({ spacing: { before: spacing.bottomSpacing } }));
  children.push(new Paragraph({ indent: { left: padL + 600, right: padR + 600 }, border: { top: { ...rule, size: 4 } }, spacing: { after: 100 } }));
  children.push(new Paragraph({ indent: { left: padL, right: padR }, border: { top: { ...rule, size: 18 } }, spacing: { before: 100 }, children: [
    new TextRun({ text: config.footerLeft || "", size: 17, color: C.cover.footerColor, font: { ascii: "Arial" } }),
    new TextRun({ text: "                                                  " }),
    new TextRun({ text: config.footerRight || "", size: 17, color: C.cover.footerColor, font: { ascii: "Arial" } }),
  ] }));
  return [new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, layout: TableLayoutType.FIXED, borders: allNoBorders, rows: [new TableRow({ height: { value: 16838, rule: "exact" }, children: [new TableCell({ shading: { type: ShadingType.CLEAR, fill: C.bg }, borders: noBorders, children })] })] })];
}

const EN = { ascii: "Times New Roman", eastAsia: "SimSun" };
const HEAD = { ascii: "Arial", eastAsia: "SimHei" };

function h1(text) { return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 400, after: 180, line: 312 }, children: [new TextRun({ text, bold: true, size: 30, color: "000000", font: HEAD })] }); }
function h2(text) { return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 130, line: 312 }, children: [new TextRun({ text, bold: true, size: 26, color: "000000", font: HEAD })] }); }
function body(text) {
  const runs = Array.isArray(text) ? text : [{ text }];
  return new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { line: 312, after: 100 }, children: runs.map(r => new TextRun({ text: r.text, bold: !!r.bold, size: 22, color: "000000", font: EN })) });
}
function bullet(text, level = 0) { return new Paragraph({ bullet: { level }, spacing: { line: 312, after: 60 }, children: [new TextRun({ text, size: 22, color: "000000", font: EN })] }); }
function caption(text) { return new Paragraph({ keepNext: true, spacing: { before: 160, after: 80 }, children: [new TextRun({ text, bold: true, size: 20, color: "404040", font: EN })] }); }
function cell(text, opts = {}) {
  return new TableCell({
    children: [new Paragraph({ alignment: opts.align || AlignmentType.LEFT, spacing: { line: 276 }, children: [new TextRun({ text: String(text), bold: !!opts.bold, size: opts.size || 19, color: opts.color || "000000", font: EN })] })],
    shading: opts.fill ? { type: ShadingType.CLEAR, fill: opts.fill } : undefined,
    margins: { top: 70, bottom: 70, left: 110, right: 110 },
    width: opts.width ? { size: opts.width, type: WidthType.PERCENTAGE } : undefined,
    verticalAlign: "center",
  });
}
function table(headers, rows, widths) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 6, color: P.table.accentLine },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: P.table.accentLine },
      left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: P.table.innerLine },
      insideVertical: { style: BorderStyle.NONE },
    },
    rows: [
      new TableRow({ tableHeader: true, cantSplit: true, children: headers.map((t, i) => cell(t, { bold: true, fill: P.table.headerBg, color: P.table.headerText, width: widths ? widths[i] : undefined })) }),
      ...rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((t, i) => cell(t, { width: widths ? widths[i] : undefined, fill: ri % 2 === 1 ? P.table.surface : undefined })) })),
    ],
  });
}

const B = [];

// 1 Executive summary
B.push(h1("1. Executive Summary"));
B.push(body([{ text: "This report is the zai-desk response to the trade desk's quantitative inquest on the Canonical Master Specification (SOP v2.0.0), delivered at desk round R384. The analysis is grounded entirely in live telemetry pulled from the local terminal during this session: narrative and market data for twenty assets, liquidation clusters, book-wall depth, fresh footprint signals, two-hour taker deltas, and a twenty-asset beta panel estimated from 129 hourly returns reconstructed from local m15 klines. The same content has been posted to the desk coordination files (desk/inbox/WAKE.md and desk/log.md, commit 1dcf1d74) for the execution agent." }]));
B.push(body([{ text: "The central diagnosis: the desk's execution apathy is not a risk-governance failure but a " }, { text: "scoring architecture failure", bold: true }, { text: ". Table 7 zeroes its largest factor (Directional Trend, 2.0 points) in range regimes and its GEX factor is inapplicable to 59 of 61 assets, so consolidation days are structurally untradeable regardless of how good individual rotation setups are. The proposed remedy is a three-sleeve regime-adaptive scorecard system — Trend (unchanged Table 7), Range rotation, and Liquidity Sweep — plus a measured beta framework, a TradFi template family, an exact capital-scaling staircase, and a Bayesian likelihood-ratio overlay that converts the additive point score into a calibrated win probability and expected-value gate. Hard safety gates (minimum-lot veto, beta budget, BTC macro filter, heat cap) remain binary and untouched." }]));

// 2 Appraisal
B.push(h1("2. Appraisal of SOP v2.0.0, the 11 Gates and the 10 Pitfalls"));
B.push(body("The specification is structurally sound and its post-R334 additions trace cleanly to the loss mechanics they address: the LINK minimum-lot catastrophe to Gate 7, the correlated double-beta stop-out to Gate 9, the bottom-tick shorting trap to Gate 10, and the market-stop slippage to Gate 11's 1.20x buffer. The verdict on the framework is therefore endorsement with three calibration findings."));
B.push(bullet("Table 7's arithmetic is the apathy generator. In RANGE_BALANCE, Factor 1 zeroes and Factor 7 (options GEX) applies only to BTC and ETH, leaving micro-assets an effective 8.5-point menu against a 5.0-point floor while the two largest factors are regime-discounted. A day with BTC at VWAP z = -0.18 (today) is a rotation day, and SOP v2.0.0 cannot trade rotation by design."));
B.push(bullet("Gates 3, 8 and 12 (the LSR magnet gate, the cascade climax gate and telemetry Dimension 12) all fire on the same underlying cascade state. Four overlapping gates on one risk produce roughly four times the false-block rate of one well-calibrated gate. They should consolidate into a Passive-Ban condition and a Sweep-Confirm condition."));
B.push(bullet("Gate 9's sector labels are falsified by measured betas. MSTR, a TradFi BUSD contract, carries beta 1.28 to BTC with R-squared 0.71 — a crypto-correlated asset wearing an equity label. A crypto short paired with an MSTR long is the R334 avalanche with different letters. The gate must move from sector labels to a beta budget."));
B.push(body("Gates 5, 6, 10 and 11 (time stop, breakeven invariant, BTC macro anchor, friction multiplier) are endorsed without reservation; Gate 10 in particular is the single most valuable addition since the post-mortem. The 16-dimension audit is retained as the record of due diligence, but the decision layer moves to a three-question reduction and a probabilistic overlay described in Section 6."));

// 3 Sleeves
B.push(h1("3. Challenge 1 — Regime-Adaptive Multi-Sleeve Scorecards"));
B.push(body([{ text: "The principle: one scoreboard per regime, because the question the scorecard answers differs by regime. Trend asks whether a pullback is entering in the trend direction. Range asks whether rotation is extreme and defended. Sweep asks whether a cascade has exhausted. The 5.0/7.0 thresholds and the Grade A/B risk allocations (1.0% and 0.5%) carry over unchanged, so every position-sizing invariant survives intact. The narrative tab already classifies regimes and acts as the sleeve selector; a liquidity-skew or cascade condition overrides into the Sweep sleeve regardless of tape regime." }]));
B.push(caption("Table 1 — Sleeve R: Range Rotation / Mean-Reversion scorecard (10.0 max)"));
B.push(table(
  ["#", "Factor", "Grounding condition", "Max"],
  [
    ["R1", "Value-Area Extreme Rejection", "Price tags or pierces Day VAL (long) / VAH (short), then a 15m bar closes back inside the Value Area", "2.0"],
    ["R2", "VWAP Band Stretch", "z <= -1.5 sigma at entry for longs (>= +1.5 for shorts); the existing |z| >= 2.0 continuation ban stays in force for the Trend sleeve only", "1.5"],
    ["R3", "Footprint Absorption at the Extreme", "Absorption signal at or near the VA extreme within 8 hours, or two-hour aggregate taker delta opposing the extreme-side move", "2.0"],
    ["R4", "Book-Wall Defense", "Confirmed resting wall >= $1M (micro-asset scale) within 0.5% beyond the extreme, aged over 1 hour, not pulled", "1.5"],
    ["R5", "Auction Gravity", "Day POC on the far side of the Value Area with entry-to-POC >= 1.5R reversion reach", "1.0"],
    ["R6", "CVD Non-Confirmation", "Spot CVD flat or rising while price prints the extreme low (for longs) — no capitulation acceleration", "1.0"],
    ["R7", "Friction", "Gate 4 spread rule unchanged", "1.0"],
  ],
  [6, 26, 56, 12]
));
B.push(body("A sweep-adjacent guard operates inside Sleeve R: if the nearest liquidation cluster sits within 1.0R beyond the Value Area extreme — between entry and stop — the setup is reclassified to Sleeve S or rejected outright. Today's ADA is the live example: its 0.1499 cluster at -1.56% with strength 91 sits inside any natural stop path toward deeper supports, which is exactly the geometry that must not be traded as plain rotation."));
B.push(caption("Table 2 — Sleeve S: Liquidity Sweep Reversal state machine (10.0 max)"));
B.push(table(
  ["#", "Factor", "Grounding condition", "Max"],
  [
    ["S1", "Cascade Visited the Magnet", "Price has traded INTO the major liquidation cluster (>= $1M or strength >= 50 within ±4%) — the magnet is consumed, not ahead", "2.0"],
    ["S2", "Exhaustion Wick Printed", "15m wick >= 1.5x body through the cluster closing back on the pre-sweep side, or an exhaustion signal at the sweep extreme within 2 hours", "2.0"],
    ["S3", "Taker Delta Flip", "Footprint delta flips against the cascade direction on the sweep bar or the bar after — the aggressors are exhausted", "2.0"],
    ["S4", "Cascade Pace Decayed", "Liq 5m has fallen at least 50% from cascade peak — Gate 8's own metric re-used as a decay measurement", "1.5"],
    ["S5", "BTC Anchor Unblocked", "Gate 10 satisfied in the post-sweep direction", "1.0"],
    ["S6", "Re-Entry Structure", "Post-only limit at the wick's 50% retrace or the swept level; stop beyond the wick extreme plus 1.20x buffer", "1.5"],
  ],
  [6, 26, 56, 12]
));
B.push(body("The not-getting-run-over mechanics deserve emphasis because they are the desk's explicit worry. The resting order does not exist until S2 and S3 are both true — it is only ever placed in a confirmed-exhaustion world, never during the cascade. S4 converts Gate 8 from an unmeasurable wait into a re-arm condition on a measurable decay. The stop beyond the wick plus buffer means a continuation cascade must print a new structural extreme to stop the position, which contradicts the evidence that S1 through S3 just recorded. And if filled and re-pierced, that is structural invalidation — no averaging, no widening. On expected effect: today's tape is untradeable under v2.0.0 but scoreable under Sleeve R — MSFT (RANGE_BALANCE, z -0.64, fresh exhaustion and strong-divergence buy prints at the 523-524 shelf, POC 525.24 about +0.35% away) scores roughly 5.5 and becomes a legitimate Grade B rotation candidate once its Value Area low tags. That is the pipeline restoration working as intended, with every safety gate still armed."));

// 4 Beta
B.push(h1("4. Challenge 2 — Beta-Conditioned Alpha and Pairs"));
B.push(body("Betas were estimated this session by ordinary least squares on 129 hourly returns per asset against BTC, reconstructed from the local m15 kline series (518 bars, about 5.4 days). The panel below carries the four numbers that matter for governance: beta (exposure per unit BTC move), correlation, R-squared (the share of variance BTC explains), and idiosyncratic volatility (the annualized residual)."));
B.push(caption("Table 3 — Measured beta panel vs BTC (129 hourly returns, this session)"));
B.push(table(
  ["Asset", "Beta", "Corr", "R2", "Idio vol (ann.)", "24h idio alpha", "Class"],
  [
    ["ETH", "1.26", "0.95", "0.91", "26%", "+0.87%", "BTC proxy"],
    ["SOL", "1.30", "0.91", "0.82", "39%", "-0.30%", "BTC proxy"],
    ["DOGE", "1.27", "0.90", "0.80", "41%", "+0.76%", "BTC proxy"],
    ["MSTR", "1.28", "0.84", "0.71", "54%", "+4.19%", "Crypto-beta equity"],
    ["ADA", "1.23", "0.86", "0.75", "47%", "-0.12%", "High-beta alt"],
    ["APT", "1.32", "0.80", "0.64", "65%", "+2.19%", "Half-idio alt"],
    ["SEI", "1.25", "0.81", "0.65", "60%", "+0.73%", "Half-idio alt"],
    ["VET", "1.09", "0.83", "0.70", "47%", "+1.64%", "Accumulator (24h)"],
    ["TIA", "1.04", "0.60", "0.36", "91%", "-1.66%", "Idio-driven"],
    ["NVDA", "0.71", "0.42", "0.18", "100%", "-0.29%", "Half-crypto equity"],
    ["MU", "0.54", "0.45", "0.20", "70%", "-3.76%", "Half-crypto equity"],
    ["MSFT", "0.03", "0.07", "0.01", "31%", "+0.38%", "True decorrelator"],
    ["META", "0.17", "0.30", "0.09", "35%", "-1.19%", "True decorrelator"],
    ["XAU", "0.12", "0.34", "0.11", "22%", "+0.96%", "True decorrelator"],
    ["XAG", "0.30", "0.46", "0.21", "38%", "-1.77%", "True decorrelator"],
  ],
  [12, 10, 10, 8, 16, 16, 28]
));
B.push(body([{ text: "Three governance consequences follow. First, " }, { text: "Gate 9 becomes Gate 9-beta", bold: true }, { text: ": a slot pair is permissible only when the portfolio's absolute beta-weighted sum is at most 0.35 — a net beta budget. At the current $2.77 equity, that means slot 2 must be cash or a sub-0.35-beta TradFi name (MSFT, META, XAU, XAG), and MSTR is reclassified as crypto-beta for gating purposes. Second, R-squared ranks tradability for the BTC filter: TIA's R-squared of 0.36 means 64% of its variance is idiosyncratic, so local footprint signals on TIA are more trustworthy than on DOGE, where BTC drowns everything. The proposed signal-trust multiplier tau = 1 - R2 scales the footprint factor's maximum points per asset — local evidence is not discarded, it is discounted by how much BTC explains. Third, the alpha-decorrelation screen: an asset's idiosyncratic alpha is its return minus beta times BTC's return; today VET (+1.64%), APT (+2.19%) and SEI (+0.73%) accumulated positive alpha while BTC fell 1.1%, versus ARB (-1.56%) and TIA (-1.66%) in distribution. Positive 24h alpha with non-negative spot CVD upgrades Sleeve R longs on those names; alpha below minus two daily idio standard deviations blocks Sleeve S longs. The screen conditions entries; it never generates them alone." }]));
B.push(body("Beta-hedged pairs are formally designed but deferred: at this equity the risk budget cannot fund two legs without violating the minimum-lot gate on both. The pair template is codified for equity >= $50 — legs chosen so the beta-weighted net is within 25% of the long leg's beta, each leg independently sleeve-qualified, entries within two bars of each other, shared invalidation. Until then the beta budget handles the job single-legged."));

// 5 TradFi
B.push(h1("5. Challenge 3 — TradFi Sleeve on Delta Exchange India"));
B.push(body("The telemetry asymmetry is real but smaller than assumed: upstream taker footprint is absent for equities, yet the discrete signal engine still returns footprint-derived events for TradFi symbols (NVDA 48 signals, MSFT 63, MSTR 42, AVGO 96 today), auction profiles and VWAP bands are full-fidelity, and Delta's own level-2 book is native depth. The sleeve is built on what exists: auction rotation, VWAP stretch, discrete signals and the venue's own book. Four templates:"));
B.push(bullet("T-ORB (Opening Range Breakout): mark the opening range as the first two 15m bars after the 13:30 UTC US cash open; a breakout is valid only with a closing bar outside the range, relative volume at least 1.5x, and level-2 book imbalance of at least 0.20 on the breaking side. Entry stop-limit just beyond the range; stop at the opposite side (or range midline if the range exceeds 1.2x the 15m ATR); target one range projection then the Day VAH/VAL. Ranges wider than twice the ATR are news-gap days — no ORB. No entries in the last 30 minutes before the US close."));
B.push(bullet("T-VAR (Value-Area Rotation): the Sleeve R factor table applied to TradFi with wall thresholds scaled to the observable $0.2-3M prints, using $1M and one-hour age. MSFT today is the live template — it fails R4 (the book is contested, -0.031 imbalance), which is the sleeve correctly declining, not failing."));
B.push(bullet("T-VWAP-sigma (session band fade): fade 2-sigma touches only with a same-side fresh exhaustion or strong-divergence signal, and only when the session has not one-wayed through three consecutive VWAP touches — one-way tapes are bans, not fades."));
B.push(bullet("T-Gap (overnight gap): the perps trade while US spot is closed, so session opens gap against the prior US close. Fade gaps under 0.5x the daily ATR that land inside the prior Day Value Area; follow gaps beyond 1.5x the daily ATR that clear the Value Area entirely."));
B.push(body("Slot-2 qualification under the beta budget resolves to MSFT, META, XAU and XAG only. NVDA, SNDK, MU and AMD — with betas of 0.5 to 0.7 and idiosyncratic volatilities of 70-100% — are half-crypto-correlated high-octane names and count at half weight toward the crypto budget. One execution flag is raised to the desk agent: BUSD contract specs (lot size, step, tick value) must be verified per symbol through get_symbol before any TradFi card becomes an order, because the Gate 7 minimum-lot arithmetic applies to TradFi exactly as it does to crypto, and XAU at roughly $3,868 per ounce notional is almost certainly blocked at this equity."));

// 6 sizing
B.push(h1("6. Challenge 4 — Sizing Staircase and Discretization"));
B.push(body("The sizing formula is unchanged: contracts = floor(equity x risk% / (stop% x notional-per-lot x 1.20)). The discretization problem is what floor() returns zero. Two mechanisms answer it. First, a stop-geometry widening ladder with structural-only steps: if the structural stop yields zero lots, widen to the next structural level — the far Value Area edge, then the 2-sigma VWAP band, then the sweep wick — each permissible only if the composite R-multiple stays at or above 1.5 and the total stop stays under 4.0%. If zero lots persist at the third step, the trade does not exist; risk is never forced to fit. Second, the exact equity staircase, computed at a 1.5% structural stop with the 1.20x buffer under the 1.0% cap:"));
B.push(caption("Table 4 — Equity milestones at which each asset clears Gate 7 (1.5% stop, 1.20x buffer)"));
B.push(table(
  ["Asset (min lot notional)", "Minimum equity", "Status at $2.77"],
  [
    ["VET (~$0.005)", "$0.01", "Tradeable"],
    ["SEI (~$0.04)", "$0.07", "Tradeable"],
    ["ADA (~$0.15)", "$0.27", "Tradeable"],
    ["TIA (~$0.35)", "$0.63", "Tradeable"],
    ["DOGE (~$0.06)", "$0.11", "Tradeable"],
    ["APT (~$0.46)", "$0.83", "Tradeable"],
    ["ETH 0.001 lot (~$1.82)", "$3.02", "Gate 7 name-ban applies (< $15)"],
    ["LINK 1 contract ($9.12)", "$15.32", "Blocked — first real unlock"],
    ["BNB 0.1 lot ($59)", "$99.12", "Blocked"],
    ["BTC 0.001 lot (~$64.6)", "$109.20", "Blocked"],
    ["SOL 1 contract (~$150)", "$252.00", "Blocked"],
  ],
  [40, 25, 35]
));
B.push(body("The R334 verification falls out of the same arithmetic: one LINK contract at a 1.4% stop with the buffer is $0.153 of risk against a $0.0277 cap — 5.5x over, which is precisely the 5.10% equity loss the post-mortem recorded. The operator's milestone question resolves exactly: at $5 and $10 and $25 and $50 nothing new opens beyond the micro-assets already available; LINK unlocks at $15.32, BNB and BTC around $100-110, SOL at $252. And the account is genuinely tradeable today — VET permits three lots within cap, APT and TIA one lot each with real structural stops — confirming that the apathy was never mechanical. It was scoring. On compounding: at an average realized +1.5R on 0.5-1.0% risk, equity doubles roughly every 70-100 trades; the Kelly-optimal fraction at a 40% win rate and 2R average is 10%, so the 1% cap is ten times sub-Kelly. The binding constraint on compounding is the entry rate, not the risk cap — which is the deepest argument for widening the sleeve set rather than loosening any gate."));

// 7 epistemics
B.push(h1("7. Challenge 5 — Thinking-Chain Epistemics"));
B.push(body([{ text: "False precision dissolves under a three-question reduction run before any 16-dimension audit: who is the counterparty being trapped; where is the resting liquidity whose consumption moves price; and what single print falsifies the thesis. If those cannot each be answered in one sentence, no telemetry stack saves the trade — and when they can, half the dimensions are redundant confirmation. The 16-dimension sheet remains the audit record; the decision runs on the triad. Today's XAU card is the worked example: the counterparty is the VWAP-band chaser, the liquidity is the $3.7M bid stack at 3855-3860, and the falsifier is the 3855.4 wall pulling or the 3800 cluster sweeping." }]));
B.push(body("Execution apathy versus compounding resolves the way institutional desks resolve it — through opportunity-set honesty rather than threshold-cutting. Regime-matched sleeves restore scoreable candidates (three to eight per week is the design target, where scoreable means the pipeline produces a decision and NO is a decision). Sample-size accounting makes the goal explicit: a strategy needing 30-plus trades for significance cannot be evaluated at one trade per week. And unfilled-card accounting converts cash-defense days into calibration data: every quality limit that never fills is logged with its would-have-been outcome, building a fill-probability model, because EV = P(fill) x P(win | fill) x win - (1 - P(win)) x loss makes limit placement a free EV multiplier that no signal quality can buy."));
B.push(body([{ text: "The Bayesian overlay is the calibrated successor to the 5.0-point cutoff. The Table 7 factors survive as features; the gate becomes a posterior probability. The prior is the base win rate (0.40, updated quarterly from the desk ledger). Each factor carries a likelihood ratio estimated from the trade log once twenty outcomes exist per sleeve, initialized at 1.35 per point so the 5-point Grade B bar corresponds to a posterior near 0.69 under the 0.40 prior. The posterior logit is the prior logit plus the sum of logged likelihood ratios; Grade A requires P >= 0.65, Grade B sits in [0.52, 0.65]. The expected-value gate replaces the point gate entirely: EV = P(win | x) x E[win R] x P(fill) - (1 - P(win | x)) x 1R >= 0.25R, with the 1.20x friction already inside the R definition. Because likelihood ratios are estimated jointly on outcomes, the model learns which dimensions actually pay — walls and large resting orders will show near-1.0 ratios and stop double-counting. Calibration discipline is a quarterly reliability diagram in five bins with a hard floor of twenty observations per bin; below that, no tuning. And the hard cutoffs that stay hard are exactly the survival layer: minimum-lot veto, beta budget, BTC macro filter, heat cap, breakeven invariant, time stop, post-only mandate. Bayes replaces the scoring of entry quality; it never replaces the binary physics of survival." }]));

// 8 cards
B.push(h1("8. Actionable Cards for Upcoming Rounds"));
B.push(body("Four cards were posted to the desk wake file, every one a watch or conditional — zero orders. The market is mid-rotation (BTC z = -0.18, TREND_DOWN at 85 confidence but with no sweep-confirmed structure anywhere in the permitted universe), so cash defense remains correct today; the cards specify exactly what would change that verdict."));
B.push(caption("Table 5 — Card register (live data, 2026-11-16 15:55-16:00 UTC)"));
B.push(table(
  ["Card", "Asset / Side", "Sleeve", "Status & trigger"],
  [
    ["AC-1", "MSFT long", "T-VAR (Sleeve R)", "4.5 hold. Trigger: 15m close <= 523.0 tagging VAL with buy absorption activates R1 to 6.5, Grade B; entry 523.1, stop 521.8, T1 525.2 (POC), T2 527.9 (VAH)"],
    ["AC-2", "TIA short", "Sleeve T", "NO TRADE — 0.3421 strength-100 magnet below makes the stop path radioactive (Gate 2). Only path: sweep of 0.3421 plus exhaustion wick plus delta flip, then a Sleeve S long card"],
    ["AC-3", "VET long", "Sleeve R", "NO TRADE yet — the tape's highest-quality setup in development: 24h alpha +1.64%, 2h footprint delta +5.0%, depth imbalance +0.105 all agree; the 0.0048 strength-74 magnet blocks the geometry. Arm on sweep-and-exhaustion or a POC retest with absorption"],
    ["AC-4", "XAU short", "Sleeve T", "6.0 Grade B contingent on the XAUTUSD minimum-lot check (likely blocked at this equity). Post-only 3883-3886 at VAH rejection, stop 3897, T1 3860 (bid stack), T2 3837"],
  ],
  [7, 14, 14, 65]
));
B.push(body("Directives accompanying the cards: no orders as-is; verify Delta contract specifications for MSFTBUSD (158126), TIAUSD, VETUSD and XAUTUSD (131253) and post them back; begin logging unfilled-card outcomes to seed the fill-probability dataset; treat TIA and VET magnet sweeps as Sleeve S triggers in upcoming rounds; and reply with contract specs plus any beta-budget exceptions, after which the SOP v2.1.0-RC1 diff (sleeve tables, Gate 9-beta, cascade-decay re-arm, Bayesian overlay as Section 5B/6 amendments) is drafted for desk review before anything becomes canonical."));

// doc
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: EN, size: 22, color: "000000" }, paragraph: { spacing: { line: 312 } } },
      heading1: { run: { font: HEAD, size: 30, bold: true, color: "000000" }, paragraph: { spacing: { before: 400, after: 180, line: 312 } } },
      heading2: { run: { font: HEAD, size: 26, bold: true, color: "000000" }, paragraph: { spacing: { before: 280, after: 130, line: 312 } } },
    },
  },
  sections: [
    {
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
      children: buildCoverR2({
        title: "Quantitative Architecture Inquest Response",
        subtitle: "Regime Sleeves, Beta Governance, TradFi Integration & Bayesian Calibration — SOP v2.1.0-RC1 Proposal",
        englishLabel: "DESK ROUND R384",
        metaLines: [
          "Prepared by: zai-desk (Quantitative Analysis Brain)",
          "For: atg-exec & Human Operator — Trade Desk",
          "Venue: Delta Exchange India (india_prod, Account #26902927)",
          "Basis: live session telemetry + 20-asset measured beta panel",
          "Date: 16 November 2026",
        ],
        footerLeft: "R384 · zai-desk",
        footerRight: "cg-terminal · 2026-11-16",
        palette: { bg: P.bg, accent: P.accent, cover: P.cover },
      }),
    },
    {
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 } } },
      children: [
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 480, after: 360 }, children: [new TextRun({ text: "Table of Contents", bold: true, size: 32, font: HEAD, color: "000000" })] }),
        new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }),
        new Paragraph({ spacing: { before: 200 }, children: [new TextRun({ text: "Note: This Table of Contents is generated via field codes. To ensure page number accuracy after editing, please right-click the TOC and select \"Update Field.\"", italics: true, size: 18, color: "888888", font: EN })] }),
        new Paragraph({ children: [new PageBreak()] }),
      ],
    },
    {
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 }, pageNumbers: { start: 1 } } },
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "R384 · Quantitative Inquest Response · zai-desk", size: 18, color: "808080", font: EN })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "808080", font: EN })] })] }) },
      children: B,
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/z/my-project/download/R384_Quant_Inquest_Response_zai-desk.docx", buf);
  console.log("written:", buf.length, "bytes");
});
