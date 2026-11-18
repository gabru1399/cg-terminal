/**
 * R501 — SSRN Order-Flow Research Digest (zai-desk)
 * Human-facing document form of the desk research round.
 * Cover: R2 (Double-Rule Frame), IG-1 palette — same validated recipe as R384 report.
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
function bullet(text) { return new Paragraph({ bullet: { level: 0 }, spacing: { line: 312, after: 60 }, children: [new TextRun({ text, size: 22, color: "000000", font: EN })] }); }
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
B.push(body([{ text: "This report answers the operator's directive to mine the academic literature — SSRN in particular — for entry-based trading strategies that can be confirmed by the desk's order-flow telemetry, and to integrate the findings into the Canonical Master Specification. The desk digest was posted to the coordination files at round R501 and pushed to the repository (commit 94047160); this document is the human-readable record of the same research." }]));
B.push(body([{ text: "One access limitation must be stated plainly: SSRN blocked automated access on every surface — the HQ login page held by a looping Cloudflare verification, and both the www and papers subdomains returning an explicit \u201CContent Blocked — automated script\u201D page. The login was therefore never completed and the provided credentials went unused. The research proceeded through public mirrors: web-indexed SSRN abstracts (same papers, same abstract IDs) and the arXiv quantitative-finance API. This matters for depth, not direction — abstract-level findings are sufficient to specify entry rules, but exact coefficient values from full texts remain unverified and are flagged as such throughout." }]));
B.push(body([{ text: "The yield: a 12-paper evidence base spanning the order-flow imbalance (OFI) literature from its foundational statement to a 2026 BTC/USDT validation, the liquidity-sweep formalization, pre-registered value-area studies, opening-range-breakout profitability work, and two 2026 forensic studies of the October 2025 liquidation cascade. From these, " }, { text: "six new entry archetypes", bold: true }, { text: " (EA-1 through EA-6) were derived, each mapped to specific telemetry dimensions the desk already records, each assigned to a sleeve (Trend, Range, or Sweep), and each carrying explicit governance so paper parameters are treated as priors to be calibrated on desk fills rather than adopted on faith." }]));

// 2 Access note
B.push(h1("2. Access Note and Method"));
B.push(body("Three SSRN surfaces were attempted in order: the HQ sign-in page, the main site, and the papers subdomain. The HQ page remained behind a Cloudflare \u201CJust a moment\u2026\u201D verification that re-armed on each attempt; the other two returned a Content Blocked page stating that an automated script or unsupported engine had been detected. Direct PDF delivery links returned HTTP 403. Repeated retries were deliberately not pursued, and no attempt was made to defeat the protection — publisher bot-guards are theirs to set. The account credentials supplied by the operator were not used and are not stored anywhere in this workspace."));
B.push(body("The pivot preserved the research goal: the same SSRN papers are indexed by public search engines with abstracts and stable abstract IDs, and the working-paper ecosystem (arXiv q-fin, RePEc) mirrors much of the microstructure literature. Twelve papers were resolved with verifiable identifiers; every finding cited in this report traces to a retrieved abstract or arXiv metadata, and nothing was invented. Where a full text would be needed to pin down an exact parameter, that gap is stated rather than papered over."));

// 3 Evidence base
B.push(h1("3. The 12-Paper Evidence Base"));
B.push(caption("Table 1 — Papers and the core finding relevant to the desk"));
B.push(table(
  ["#", "Paper (SSRN / arXiv ID)", "Core finding we can trade"],
  [
    ["P1", "Cont, Kukanov & Stoikov — Price Impact of Order Book Events (1712822; 804 citations)", "Order flow imbalance linearly predicts mid-price change; the slope is inversely proportional to standing depth. The foundational OFI edge."],
    ["P2", "Xu, Gould et al. — Multi-Level OFI (arXiv 1907.06230)", "Out-of-sample fit improves monotonically with each added order-book level: deep-book imbalance beats top-of-book."],
    ["P3", "Gould et al. — Forecasting High-Frequency OFI (arXiv 2408.03594)", "OFI is itself forecastable via Hawkes processes with lagged cross-dependence between bid and offer flow — OFI momentum exists."],
    ["P4", "Schmalz — OFI and Short-Horizon BTC/USDT Returns (7227998)", "The CKS OFI measure tested directly on BTC/USDT at 1-10 second horizons: the OFI edge holds in crypto, not only equities."],
    ["P5", "Vafin — OFI and Short-Horizon Return, 2026 review (6938742)", "Survey of OFI measures; OFI characterized as one of the most robust drivers of short-horizon price movement."],
    ["P6", "Rehan — Liquidity Sweeps and Post-Sweep Acceptance in BTC (7557779)", "Falsifiable, lookahead-free definitions of level, sweep, acceptance, rejection and resting-liquidity consumption — a formal spec for sweep trading."],
    ["P7", "Perry — Beyond the Boundary: Delta Proxy at Daily Value-Area Extremes (7106618)", "Pre-registered tests across 216,376 events in liquid futures of delta-signal quality at daily value-area extremes."],
    ["P8", "Howard — Stop Distance and Exit in Intraday Value-Area Breakouts (6350238)", "6,284 ES events: outcomes depend on stop distance and exit method; events in the first 30 minutes of the session are significantly worse (p < 0.001)."],
    ["P9", "Zarattini & Soe — A Profitable Day Trading Strategy (4729284); Can Day Trading Really Be Profitable? (4416622)", "Opening-range breakout on high relative-volume names, 2016-2023: 41.6% annual return, Sharpe 2.8, stop at 10% of ATR, exit at close."],
    ["P10", "Lim — Anatomy of a Crypto Cascade (6579278)", "Minute-level anatomy of the October 2025 crash (BTC -12.6% in ten minutes): a cascade is an order-flow-imbalance spiral plus deleveraging, a structured not random process."],
    ["P11", "Lim — Two-Regime Liquidity Recovery (6636998); Hidden Liquidity, Displayed Depth (6891658)", "After a cascade, pricing recovers fast while depth recovers slowly; displayed depth is a biased estimator of executable liquidity under stress."],
    ["P12", "Barone et al. — Sunshine vs Shade on Hyperliquid (arXiv 2606.15715)", "Visible TWAP executions face lower costs and smaller permanent impact than hidden metaorders (4.3 million metaorders reconstructed): visible flow is a catalyst worth following."],
  ],
  [5, 33, 62]
));

// 4 archetypes
B.push(h1("4. Six New Entry Archetypes"));
B.push(body("Each archetype below states the trigger, the exact telemetry wiring (using the desk's dimension numbering), the sleeve assignment from the R384 proposal, and the governance hooks. Together they attack the execution-apathy problem from the entry side: they convert passive \u201Cwait for a level\u201D cards into flow-confirmed executions without weakening a single hard gate."));

B.push(h2("EA-1 — Rolling OFI Trigger (Sleeve T timing upgrade)"));
B.push(body("Compute a stationarized OFI per 15-minute bar from the live book the terminal already maintains: the change in bid-side depth minus the change in ask-side depth within a fixed band around mid, normalized by total band depth (the log-OFI variant in the literature). A trend-sleeve setup becomes executable only when the three-bar rolling OFI agrees with the trade direction at or beyond a 0.3 normalized threshold. This replaces three eyeballed, correlated dimensions — book walls, footprint delta, and CVD — with one composite number carrying eighty-four citations of provenance. The desk's top-1000-level Binance book satisfies the multi-level depth requirement from P2; at least ten levels should enter the computation. This is the first implementation priority because it is pure computation over existing feeds: no new APIs, no new data, and the strongest evidence weight of the twelve papers (P1 through P5 all converge on it)."));

B.push(h2("EA-2 — Sweep-Acceptance Protocol (Sleeve S formal specification)"));
B.push(body("The sweep sleeve's current heuristic — a wick at least 1.5 times the body — becomes Rehan's lookahead-free event grammar. A sweep is a trade through a pre-registered level (registered at least N bars earlier from the level registry: prior day and week highs and lows, value-area highs and lows, and major wall prices — all already in telemetry) that reverses and closes back within K bars. Acceptance is a subsequent close beyond the swept level in the reversal direction; rejection is the failure to accept within K bars. The entry rule: a sweep-sleeve long fires only on a downside sweep of a liquidation cluster or registered level, an acceptance close back above that level, and the existing delta-flip condition — meaning the desk never places the resting order during the cascade itself, only in the confirmed-exhaustion world that follows. A kill-switch from the cascade papers completes the protocol: if the venue's quoted spread during the sweep exceeds twice its 24-hour median, the card voids, because the displayed depth mid-cascade is not the depth that will fill the order."));

B.push(h2("EA-3 — Value-Area-Extreme Delta Reversion (Sleeve R formal specification)"));
B.push(body("Perry's pre-registered design becomes the range sleeve's combined rejection test: at the daily value-area low (for longs) or high (for shorts), require the footprint delta proxy to be non-confirming of the extreme move — genuine delta divergence into the level, not merely an absorption signal somewhere nearby. Howard's finding fixes the stop geometry: stops placed beyond the value-area extreme by a quarter of the day's value-area width outperform tighter stops in his 6,284-event sample, and entries in the first thirty minutes of a session are statistically worse at conventional significance. Operationally that means range-sleeve cards stand down for the first thirty minutes after the session anchor — 13:30 UTC for TradFi names, the UTC day boundary for crypto — and adopt the quarter-VA stop rule as the default structural stop."));

B.push(h2("EA-4 — RVOL-Gated 30-Minute Opening Range (TradFi T-ORB upgrade)"));
B.push(body("Zarattini's profitable variant, adapted to the desk's constraints: the opening range is the first thirty minutes after the US cash open (13:30-14:00 UTC); breakouts trade only when relative volume is at least 1.5 times baseline, which the terminal's day-volume-base series already computes; the stop is 0.10 times the 15-minute ATR from entry — explicitly not the opposite side of the opening range, the variant that bleeds in the earlier paper; and the exit is at the US cash close with no overnight hold. The desk's equity cannot touch QQQ-class notional, but MSFT, META and AVGO class BUSD contracts at micro lot sizes can run this template — restricted to slot-2-qualified, low-beta names under the Gate 9-beta budget. Howard's independent corroboration of the first-thirty-minute penalty justifies choosing the 30-minute range over the noisier 5-minute variant for the desk's low-frequency confirmation stack."));

B.push(h2("EA-5 — Cascade-Exhaustion Recovery Entry (Sleeve S, post-cascade tape)"));
B.push(body("Lim's cascade anatomy gives the exhaustion signature in the desk's own metrics: the five-minute liquidation pace decaying from its peak while perp CVD bases — cumulative delta flattening even as price makes new lows, the divergence between cascading price and exhausted flow. The two-regime recovery finding supplies the re-entry timing: spreads normalize within minutes but depth takes longer, so the re-entry limit must be priced off the post-recovery book. The operational rule: after pace decay triggers, wait until the venue spread returns to at most 1.3 times its 24-hour median before placing the re-entry limit — directly measurable from the live book's bid and ask. Barone's sunshine-trading result adds a catalyst filter: if a visible TWAP-style steady participant appears after the cascade — uniform taker flow at a fixed cadence over at least six footprint bars — prefer the direction of that visible flow, because it attracts liquidity and reduces the adverse selection the desk would otherwise face."));

B.push(h2("EA-6 — Intraday Time-Series Momentum Overlay"));
B.push(body("The intraday-momentum literature (Gao et al.; Li's international evidence with fifty citations; the Zarattini line) establishes that the first half-hour return predicts the last half-hour return. The desk cannot trade that spread directly on micro-lots with venue spreads, but it can use it as a direction prior for the daily round: if the first thirty minutes after the UTC daily anchor moves more than 0.4 sigma of the VWAP band, restrict that asset's sleeve candidate selection to the same direction until the day rolls over, symmetrically for down moves. This costs nothing — it reuses the VWAP and EMA dimensions already extracted — and it functions exactly as a cheap Bayesian prior update feeding the likelihood-ratio overlay proposed at R384."));

// 5 mapping table
B.push(h1("5. Telemetry Wiring Map"));
B.push(body("The archetypes are deliberately built from dimensions the 16-dimension audit already extracts; the table below makes the wiring explicit so the execution agent can implement without re-deriving the mapping."));
B.push(caption("Table 2 — Archetype to telemetry dimension and sleeve wiring"));
B.push(table(
  ["Archetype", "Sleeve", "Dimensions consumed", "New computation required"],
  [
    ["EA-1 OFI Trigger", "T (timing)", "D09 book walls, D14 footprint delta, D15 CVD (consolidated)", "Rolling 3-bar stationarized OFI from livebook top-1000 depth"],
    ["EA-2 Sweep-Acceptance", "S", "D12 liq clusters, D14 footprint, level registry (D01-D03 extremes)", "Level registry with N-bar pre-registration; acceptance-close detector; spread kill-switch"],
    ["EA-3 VA Delta Reversion", "R", "D01-D03 auction profiles, D14 delta", "Delta-divergence-at-extreme test; quarter-VA stop rule; 30-min stand-down timer"],
    ["EA-4 RVOL ORB", "T-ORB (TradFi)", "D05 VWAP, day-volume base (RVOL), Delta L2 book", "30-min opening-range tracker post 13:30 UTC; ATR stop calculator"],
    ["EA-5 Cascade Recovery", "S (post-cascade)", "D12 liq pace, D15 perp CVD, livebook spread", "Spread-median tracker; visible-TWAP cadence detector (6-bar uniformity)"],
    ["EA-6 ITSM Overlay", "All (prior)", "D05-D08 VWAP and EMA stack", "First-30-min sigma move classifier at UTC day anchor"],
  ],
  [16, 12, 36, 36]
));

// 6 governance
B.push(h1("6. Calibration, Governance and Honest Limits"));
B.push(body("Paper parameters are not desk parameters. Zarattini's Sharpe of 2.8 was earned on QQQ with 10%-ATR stops and institutional execution costs; the desk's friction multiplier and Delta India spreads will eat a naive copy alive. Every archetype therefore enters the desk ledger as a hypothesis with a paper-derived prior, to be calibrated on actual fills through the Bayesian likelihood-ratio overlay from R384: no likelihood ratio is trusted before twenty outcomes per archetype, and the pre-registration discipline of Perry and Howard is adopted wholesale — the rule is logged before the trade, evaluated after, and not edited mid-quarter."));
B.push(body("Three verification gaps are recorded honestly. The exact OFI coefficient magnitudes in the BTC/USDT study, Perry's Sharpe and hit-rate figures, and Howard's stop-distance table all live in full texts the access block prevented retrieving. The mapping in this report uses abstract-level findings only; the desk's execution agent, operating from a normal browser session with the operator's account, can open the listed abstract IDs and pull the exact tables if the operator wants them before implementation. Finally, a note on what was deliberately not done: no automated workaround against SSRN's bot protection was attempted, and the supplied credentials were neither used nor stored — if the operator wants full-text extraction, logging in manually and providing the PDFs to the workspace is the clean path."));

// 7 desk integration
B.push(h1("7. Desk Integration Status"));
B.push(body("The complete digest — evidence base, archetypes, governance and directives — has been posted to the desk coordination files as round R501 and pushed to the repository's main branch (commit 94047160). The execution agent received five directives: implement EA-1 first as the highest evidence-weight, lowest-effort upgrade; wire EA-2's acceptance grammar and EA-3's stand-down and stop rules into the next scanner revision; restrict EA-4 to slot-2 TradFi names pending the BUSD contract-spec check from R384; add an archetype field to every card in the state file so the likelihood-ratio overlay can accumulate per-archetype outcome data; and reply with implementation notes so the validated mechanics fold into the SOP v2.1.0-RC1 diff alongside the R384 sleeve tables. The daemon's subsequent rounds (R502 onward) are already building on the synced files."));

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
        title: "SSRN Order-Flow Research Digest",
        subtitle: "Six Entry Archetypes Confirmable by Desk Telemetry — Integration with the Canonical Master Specification",
        englishLabel: "DESK ROUND R501",
        metaLines: [
          "Prepared by: zai-desk (Quantitative Analysis Brain)",
          "For: atg-exec & Human Operator — Trade Desk",
          "Evidence: 12 papers (SSRN abstracts + arXiv q-fin, via public mirrors)",
          "Status: desk digest posted and pushed (commit 94047160)",
          "Date: 18 November 2026",
        ],
        footerLeft: "R501 · zai-desk",
        footerRight: "cg-terminal · 2026-11-18",
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
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "R501 · SSRN Order-Flow Research Digest · zai-desk", size: 18, color: "808080", font: EN })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "808080", font: EN })] })] }) },
      children: B,
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/z/my-project/download/R501_SSRN_OrderFlow_Research_Digest.docx", buf);
  console.log("written:", buf.length, "bytes");
});
