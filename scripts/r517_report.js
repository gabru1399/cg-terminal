/**
 * R517 — GitHub Institutional Trading Stack Research (zai-desk)
 * Human-facing document form of the desk research round.
 * Cover: R2 (Double-Rule Frame), IG-1 palette — same validated recipe as R501/R384.
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
    for (let i = Math.min(charsPerLine, remaining.length - 1); i >= 1; i--) {
      if (breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
    }
    if (breakAt === -1) {
      // No boundary within the limit: extend to the nearest boundary after it
      // (word-end overflow) instead of cutting mid-word.
      for (let i = charsPerLine + 1; i <= Math.min(remaining.length, charsPerLine + 4); i++) {
        if (breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
      }
    }
    if (breakAt === -1) breakAt = charsPerLine; // hard fallback: no boundaries at all
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
B.push(body([{ text: "This report answers the operator's directive to sweep GitHub for repositories and, in the newest sense of the word, skills that can push the desk toward institutional-grade trading practice — the Jane Street school of market making, structural arbitrage, disciplined execution and research infrastructure. The search spanned four tiers: high-frequency and market-making engines, research platforms and simulators, strategy and feature libraries, and the public assets of elite trading firms themselves. Every headline repository was verified directly against its GitHub page this session; star counts, licenses and capability claims below are as retrieved on 18 November 2026." }]));
B.push(body([{ text: "Three findings matter most. First, the open-source ecosystem now contains a complete institutional stack: hftbacktest (5.1k stars) models exactly the physics our entry archetypes live inside — limit-order queue position, feed and order latency, Level-2 and Level-3 book reconstruction — and ships real Binance market-making examples, making it the missing validation harness for the EA-1 through EA-5 archetypes specified at R501. Second, Jane Street itself has entered the agent-skills ecosystem: janestreet/agent_skills (10.1k stars, MIT) publishes SKILL.md-format skills exported from their internal repository — the same format this desk already uses — and the socratic-tutor skill was cloned, inspected, and installed into this workspace today. Third, the competition circuit (Optiver's Kaggle challenge, IMC Prosperity winners) has produced open, professionally reviewed solution repositories that function as free order-book feature-engineering curricula." }]));
B.push(body([{ text: "The deliverable set: a tiered catalogue of roughly twenty repositories with what-to-steal notes, a concrete integration matrix mapping each asset to a component of the terminal (livebook, kline_series, scanner, execution layer, MCP), a three-horizon priority roadmap (P0/P1/P2), and one completed integration — the Jane Street socratic-tutor skill, now live in skills/socratic-tutor with its MIT license intact. A desk digest at round R517 accompanies this document in the coordination files." }]));

// 2 Method
B.push(h1("2. Method and Scope"));
B.push(body("The sweep ran in four passes. Pass one covered the high-frequency and market-making space through GitHub topic pages (limit-order-book alone lists 435 repositories: 188 Python, 109 C++, 26 Rust) and targeted searches for backtesters, market makers and execution algorithms. Pass two covered research infrastructure: quantitative platforms, agent-based simulators, and machine-learning pipelines. Pass three targeted elite-firm footprints: Jane Street's organizations and topics, Optiver's Kaggle competition solutions, IMC's Prosperity competition winners, and the execution-algorithm ecosystem (Almgren-Chriss, TWAP/VWAP, reinforcement-learning execution agents). Pass four verified the shortlist — each headline repository was fetched directly to confirm stars, language, license, capabilities and activity rather than trusting search snippets."));
B.push(body("Selection criteria were deliberate: does the repository model something the desk's telemetry actually produces (books, tape, queue, latency); can it be integrated without abandoning the terminal's architecture; is the license compatible (MIT or Apache preferred); and is there a concrete transferable artifact — an algorithm, a detector, a feature set, a skill — rather than a tutorial or a toy. Repositories that failed these gates (payment rails, signal-sales bots, dead archives) were excluded regardless of stars."));

// 3 Decomposition
B.push(h1("3. What Trading Like an Institution Actually Decomposes Into"));
B.push(body("Jane Street's public footprint makes its operating model unusually legible, and it does not decompose into secret indicators. It decomposes into five capabilities. Market making: quoting both sides just inside the market (the practice known as pennying), managing inventory against adverse selection, and pricing risk around fair value with hard exposure limits. Structural and arbitrage flows: ETF basket trades and ADR conversions where a synthetic price diverges from its components — revenue from logistics, not prediction. Optimal execution: running large child-order schedules (TWAP, VWAP, Almgren-Chriss-style risk-cost frontiers) that minimize market impact. Research infrastructure: backtesters honest about queue position and latency, because a strategy that only works in a frictionless simulation is worth exactly nothing. And, as of November 2026, AI-agent tooling: Jane Street publishes agent skills in the same SKILL.md format the open ecosystem standardized, exported from an internal repository they use daily."));
B.push(body("The desk already owns pieces of every layer — the terminal is a real-time order-flow engine with multi-venue aggregates, the Canonical Master Specification is the risk discipline, the 16-dimension audit is the research process, and the skills directory is the agent tooling. What GitHub uniquely offers is the missing hardware: fill-realistic simulation (nothing in the current stack answers whether a limit at a given level actually fills given queue position and latency), structure-detection libraries battle-tested on live data, and reference implementations of the quoting and arbitrage patterns above. The tiers that follow are ordered by how directly they close those gaps."));

// 4 Tier 1
B.push(h1("4. Tier 1 — High-Frequency and Market-Making Engines"));
B.push(h2("4.1 nkaz001/hftbacktest — the validation harness the desk lacks"));
B.push(body("hftbacktest (5.1k stars, Rust 75.9% / Python 24.1%, MIT, updated December 2025) is a high-frequency trading and market-making backtesting and trading bot that accounts for limit orders, queue positions and latencies, using full tick data for trades and order books at Level-2 (Market-By-Price) and Level-3 (Market-By-Order) granularity. Fill simulation respects the order's place in the queue — the single most important honesty feature, since naive backtests systematically overfill passive orders and manufacture phantom profits. It supports multi-asset, multi-exchange backtests, ships real-world crypto examples for Binance and Bybit, and includes live-trading bot deployment (Rust-only) for quick prototyping. Its example strategies include high-frequency grid trading and market making with alpha models — order-book imbalance, basis, and APT — which is to say, the exact family the desk's EA-1 archetype lives in."));
B.push(body("Desk role: offline validation harness for the entry archetypes before any live wiring. Replay recorded Binance L2 depth and trades through hftbacktest, encode EA-1's OFI trigger, EA-2's sweep-acceptance grammar and EA-5's spread-normalization re-entry as its strategies, and measure how often the desk's limit entries would actually have filled at the intended level, with feed and order latency modeled. That converts R501's paper-derived priors into measured fill distributions before a single Delta order is placed. Effort is medium: the Python API is friendly, but historical tick data acquisition (Binance data dumps or a vendor feed) is the real cost."));
B.push(h2("4.2 Hummingbot — production market-making reference"));
B.push(body("Hummingbot (the reference open-source crypto market-making bot, v2.4.0 released March 2025) offers mature, production-grade implementations of pure market making and perpetual market making strategies, with order-cancellation logic, inventory skew and exchange-adapter plumbing. The desk will not adopt it as a runtime — our engine, risk gates and audit trail are the point — but its strategy code is a readable reference for quoting mechanics: refresh tolerances, skew on inventory, staggered order levels, and kill-switches on inventory bounds. Its perpetual market-making module is the closest open-source analog to what atg-exec does manually on Delta, making it a useful cross-check when the execution agent drafts new quoting behavior."));
B.push(h2("4.3 NautilusTrader — institutional event-driven platform"));
B.push(body("NautilusTrader appeared repeatedly in the institutional-grade searches: an event-driven platform with a correctness-first design, backtesting on the same code path as live trading, and nanosecond-resolution internals. It sits in the same category as QuantConnect's Lean (22.6k stars, C#, Apache-2.0, professional-caliber event-driven backtesting and live trading with pluggable brokerages). Both are full platforms rather than libraries — adopting either wholesale would mean re-platforming the desk, which the roadmap explicitly declines. They remain reference points for event-loop design and are the fallback if the desk ever outgrows its homegrown engine; Lean additionally brings a multi-asset-class backtester the day TradFi sleeves expand beyond BUSD perps."));

// 5 Tier 2
B.push(h1("5. Tier 2 — Research Platforms and Simulators"));
B.push(h2("5.1 microsoft/qlib — the nested-decision architecture"));
B.push(body("Qlib (50.3k stars) is Microsoft's AI-oriented quantitative investment platform, covering the full chain — data processing, model training, backtesting, analysis — across alpha seeking, risk modeling, portfolio optimization and order execution, with high-frequency (one-minute) data processing and, most relevant here, a Nested Decision Framework: multiple trading strategies and executors at different time granularities, nested and optimized together. That is architecturally identical to the desk's hierarchy — portfolio heat cap, sleeve scorecards, per-round asset selection, execution tactics — and validates the design rather than replacing it. The concrete use is as a research harness: the Bayesian likelihood-ratio overlay proposed at R384 needs a disciplined experiment framework for feature evaluation and outcome accumulation, and Qlib's pipeline gives that structure without the desk writing one from scratch. Full adoption is a quarter-scale project; borrowing the architecture and using its data/experiment layers is a medium effort."));
B.push(h2("5.2 abides-sim/abides — agent-based stress laboratory"));
B.push(body("ABIDES is an agent-based interactive discrete-event simulation environment for markets: heterogeneous agents (market makers, momentum traders, noise traders) interact through a central exchange simulation, producing endogenous microstructure rather than replayed history. Its desk value is scenario generation for the cascade-sleeve rules: EA-5's kill-switches (spread-blowout voids, pace-decay exhaustion triggers) can be stress-tested against simulated liquidation cascades and flash events, including the October 2025 pattern documented in the R501 papers, without waiting for the real market to oblige. Priority is P2 — valuable once the archetypes are live and accumulating outcomes, less urgent before."));

// 6 Tier 3
B.push(h1("6. Tier 3 — Strategy and Feature Libraries"));
B.push(h2("6.1 joshyattridge/smart-money-concepts — structure detectors, pip-installable"));
B.push(body("The smartmoneyconcepts package (2.2k stars, 915 forks, MIT, v0.0.26, March 2025) implements the ICT smart-money toolkit as pandas-ready functions over OHLCV frames: Fair Value Gaps, swing highs and lows, Break of Structure and Change of Character, order blocks, liquidity zones (multiple highs or lows compressed in a range), previous-period highs and lows, session ranges and retracements. Provenance matters here: these are retail-derived heuristics, not peer-reviewed results, and the desk adopts the detectors, never the narrative. But the mapping to the desk's own concepts is nearly one-to-one — liquidity zones and previous highs/lows are the EA-2 level registry, order blocks approximate absorption zones, and BOS/CHoCH formalize the structure-shift conditions the scanner eyeballs today. Integration is trivial: feed kline_series output through the library and attach the columns to the 16-dimension audit as mechanical confirmations. This is the P0 quick win."));
B.push(h2("6.2 tetratensor/street-algo-trader — the Jane Street pattern, in miniature"));
B.push(body("This small repository (13 stars, 51 commits, competition-era Python) is a client and strategy set for a Jane Street-style electronic trading competition, speaking the JSON-over-TCP protocol of the simulated exchange (hello, add, cancel, convert; book, fill, ack, reject). Its five strategies are a museum of the institutional patterns from Section 3: pennying.py quotes just inside the inside market with per-symbol exposure limits tracked against holdings and outstanding orders; bondtrade.py makes a market around fair value with inventory-aware cancellation; etf-convert.py arbitrages an ETF against its components; adrconversion.py captures the VALBZ/VALE conversion spread; micromacd.py is a 12/20 EMA crossover — explicitly superseded by the desk's confluence stack and of no interest. What transfers is the pennying logic (Delta limit entries placed one tick inside the best quote rather than passively at the level, with exposure accounting per instrument) and the convert-arbitrage template (perp-versus-MT5-spot basis, where the desk already logs basis percentages in mt5.json). Port the patterns into the desk's scanner and execution notes; do not import the code."));
B.push(h2("6.3 The execution-algorithm ecosystem"));
B.push(body("Almgren-Chriss optimal-execution implementations, TWAP/VWAP schedule builders, and reinforcement-learning execution agents (PPO policies trained to beat TWAP and Almgren-Chriss benchmarks on implementation shortfall) are well represented on GitHub and map to the desk's scale-out discipline: the 40/40/20 runner ladder in the Canonical Specification is a hand-rolled execution schedule, and the literature-backed schedulers offer a principled upgrade path when orders grow beyond micro lots. Likewise, order-flow imbalance and VPIN implementations published alongside the academic papers in the R501 digest give reference code for exactly the computations EA-1 specifies. These are pattern sources, ranked below the quick wins because the desk's volumes make sophisticated execution a later-horizon need."));

// 7 Tier 4
B.push(h1("7. Tier 4 — Elite-Firm Public Assets"));
B.push(h2("7.1 janestreet/agent_skills — integrated today"));
B.push(body("Jane Street's agent_skills repository (10.1k stars, 683 forks, MIT, Copyright (c) 2026 Jane Street Group, LLC) is a collection of skills for AI agents and chatbots, exported from an internal repository where they are used daily. The inaugural skill, socratic-tutor, turns an LLM into a strict personal tutor: it runs a diagnostic, maintains a skill map with levels 0 through 5, teaches one question at a time, schedules spaced review, and finishes with an assessment. Two things make this directly relevant. First, format: the repo standardizes the SKILL.md pattern this desk already uses, which is independent validation of the desk's own skill architecture. Second, substance: the Socratic method is the same epistemology the Canonical Master Specification encodes in its 11 Socratic Gates and 10 AGI Pitfall Inquests — questions before conclusions."));
B.push(body("Action taken this session: the repository was cloned into a scratch directory, the skill file inspected line by line (benign: a tutoring loop, no network calls, no injection attempts), and the socratic-tutor directory was installed into skills/socratic-tutor with license attribution intact. Its desk role is operator development: structured mastery training on market microstructure topics — order-book mechanics, OFI, value-area theory — where the human operator self-assesses rather than passively reads digests. Jane Street has stated they are not accepting external skill contributions, so this is a read-only asset; the desk's own skills evolve independently."));
B.push(h2("7.2 Competition solution repositories — free institutional curricula"));
B.push(body("The Optiver Trading at the Close Kaggle competition (order-book data for Nasdaq-listed stocks, predicting minutes-to-close behavior) produced open solution repositories — the reference implementations such as liyiyan128/optiver-trading-at-the-close and several others — whose shared core is professional-grade order-book feature engineering: weighted average prices across book levels, size and depth imbalances, matched-level imbalance, spread dynamics, and auction-aware targets. Those features map straight onto EA-1's input set and onto the livebook feed the terminal already maintains; the top solutions double as a checklist of book features the desk does not yet compute. The IMC Prosperity competition winners (for example, chrispyroberts/imc-prosperity-3 — first in the USA, seventh globally; and TimoDiehm/imc-prosperity-3) are constrained market-making exercises: position limits, regime shifts, manual-trade puzzles. Their value is governance-shaped — watching top teams encode position limits and regime detection into bots is a working rehearsal of the desk's heat cap and sleeve logic, and their algorithmic-manual split mirrors the desk's two-brain structure."));
B.push(body("Caution is recorded once and clearly: competition solutions are optimized for scoring rules, not real capital, and Optiver-style equity close features do not transfer to BUSD perps unchanged. They are curricula and feature checklists, not strategies to copy."));

// 8 Integration matrix
B.push(h1("8. Desk Integration Matrix"));
B.push(body("The matrix below is the operative part of this report: each verified asset, the terminal component it touches, the concrete integration step, its effort class, and the entry archetypes from R501 it serves. Effort classes: LOW (hours to a day), MED (days), HIGH (a multi-week project)."));
B.push(caption("Table 1 — Repository to terminal integration map"));
B.push(table(
  ["Asset (stars, license)", "Terminal component", "Concrete integration step", "Effort", "Serves"],
  [
    ["hftbacktest (5.1k, MIT)", "New validation harness beside the engine", "Replay Binance historical L2 + trades; encode EA-1/EA-2/EA-5 rules; measure true fill rates with queue + latency modeling", "MED", "EA-1, EA-2, EA-5"],
    ["smartmoneyconcepts (2.2k, MIT)", "Scanner feature columns on kline_series", "Attach FVG / BOS / CHoCH / order-block / liquidity-zone / prev-HL columns to the 16-dimension audit as mechanical confirmations", "LOW", "EA-2, EA-3"],
    ["janestreet/agent_skills (10.1k, MIT)", "skills/socratic-tutor (installed today)", "Operator mastery-training sessions on microstructure topics; use with the spec's Socratic Gates", "DONE", "Operator development"],
    ["street-algo-trader (13, none)", "Execution notes + basis scanner", "Port pennying quote placement (one tick inside best) for Delta limits; adopt convert-arb template for perp-vs-MT5 basis trades", "LOW-MED", "Execution discipline"],
    ["Optiver Kaggle solutions", "EA-1 feature set on livebook", "Adopt the book-feature checklist: multi-level WAP, size and depth imbalances, matched-level imbalance, spread dynamics", "LOW", "EA-1"],
    ["microsoft/qlib (50.3k, MIT)", "Research harness for the LR overlay", "Borrow the nested-decision architecture; use its data/experiment pipeline for the Bayesian overlay from R384", "MED", "EA-6, R384 overlay"],
    ["abides-sim/abides (Apache)", "Scenario lab for sleeve kill-switches", "Simulated cascade and flash scenarios to stress-test EA-5's spread voids and pace-decay triggers", "MED", "EA-5"],
    ["Almgren-Chriss / RL execution repos", "Scale-out scheduler (40/40/20 ladder)", "Reference schedulers when order sizes outgrow micro lots; principled risk-cost frontier execution", "LOW now", "Execution"],
    ["Hummingbot (production MM)", "Quoting-behavior cross-check", "Readable reference for refresh tolerance, inventory skew, staggered levels; not adopted as runtime", "LOW", "Quoting"],
    ["Lean (22.6k, Apache) / NautilusTrader", "Fallback platforms", "Reference only; re-platform explicitly declined this quarter", "n/a", "Contingency"],
    ["IMC Prosperity winners", "Governance rehearsal", "Study position-limit and regime-shift encodings in winning bots as analogs of the heat cap and sleeves", "LOW", "Risk discipline"],
  ],
  [22, 18, 34, 8, 18]
));

// 9 Roadmap
B.push(h1("9. Priority Roadmap"));
B.push(body([{ text: "P0 — this week. ", bold: true }, { text: "Three items, all low effort with immediate payoff. Install and run the smartmoneyconcepts detectors over kline_series output for the curated perps and attach the columns to the scanner's dimension audit (the EA-2 level registry and EA-3 structure tests become mechanical rather than eyeballed). The socratic-tutor skill is already installed — schedule the first operator training session on order-book mechanics. Continue EA-1's OFI implementation per the standing R501 directive, using the Optiver feature checklist as the book-feature audit." }]));
B.push(body([{ text: "P1 — two to four weeks. ", bold: true }, { text: "Stand up the hftbacktest validation harness: acquire Binance historical L2 tick data for the curated 30, encode the entry archetypes as hftbacktest strategies, and produce measured fill-rate and slippage distributions for EA-1, EA-2 and EA-5 before any live wiring. In parallel, port the pennying micro-adjustment into the execution agent's limit-placement notes and prototype the basis-trade template against mt5.json spreads." }]));
B.push(body([{ text: "P2 — this quarter. ", bold: true }, { text: "Adopt Qlib's nested-decision architecture as the research harness for the likelihood-ratio overlay, accumulating per-archetype outcomes as pre-registered experiments; build ABIDES stress scenarios for the cascade sleeve's kill-switches; revisit execution-scheduler sophistication only when order sizes justify it. Re-platforming onto Lean or NautilusTrader remains explicitly out of scope." }]));

// 10 Honest limits
B.push(h1("10. Honest Limits and Sources"));
B.push(body("Limits are stated plainly. Star counts, licenses and activity dates are as retrieved on 18 November 2026 and will drift. street-algo-trader is competition-era code with Python 2.7 dual support — patterns transfer, code does not, and it carries no license file, so nothing is copied. smartmoneyconcepts is retail-ICT derived; the desk adopts its structure detectors as mechanical confirmations, never its trading narrative, and every adopted column must earn its place in the likelihood-ratio overlay the same as any paper-derived signal. Competition solutions optimize for scoring rules, not real capital. hftbacktest's live-bot path is Rust-only, while the desk's validation use is Python-side backtesting only. And no repository changes the data-honesty rules: liquidation and whale figures remain Coinglass estimates, and any repo-computed feature inherits the provenance labels of the feed it consumed."));
B.push(body("Verified sources for this report, all fetched directly on 18 November 2026: github.com/nkaz001/hftbacktest; github.com/janestreet/agent_skills (with LICENSE.md and socratic-tutor/SKILL.md read in full from the cloned tree); github.com/joshyattridge/smart-money-concepts; github.com/microsoft/qlib; github.com/QuantConnect/Lean; github.com/tetratensor/street-algo-trader; GitHub topics pages for limit-order-book and jane-street; hummingbot.org release notes; the Optiver Trading at the Close and IMC Prosperity 3 solution repositories found via search (liyiyan128 and chrispyroberts trees); and abides-sim/abides. The desk digest at round R517 accompanies this document and carries the same directives for atg-exec."));

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
        title: "The Institutional Trading Stack on GitHub",
        subtitle: "Repositories, Skills and Elite-Firm Assets Mapped to the Desk's Order-Flow Terminal",
        englishLabel: "DESK ROUND R517",
        metaLines: [
          "Prepared by: zai-desk (Quantitative Analysis Brain)",
          "For: atg-exec & Human Operator — Trade Desk",
          "Scope: 20+ repositories verified across 4 tiers (stars/licenses as of 2026-11-18)",
          "Integration: janestreet socratic-tutor skill installed this session",
          "Date: 18 November 2026",
        ],
        footerLeft: "R517 · zai-desk",
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
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "R517 · Institutional Trading Stack on GitHub · zai-desk", size: 18, color: "808080", font: EN })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "808080", font: EN })] })] }) },
      children: B,
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/z/my-project/download/R517_GitHub_Institutional_Trading_Stack.docx", buf);
  console.log("written:", buf.length, "bytes");
});
