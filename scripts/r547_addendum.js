/**
 * R547 — Portfolio Expansion & Punch-Trade Integration (zai-desk addendum to R546)
 * Cover: R2 (Double-Rule Frame), IG-1 palette — same validated recipe as R546.
 */
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, WidthType, BorderStyle,
  ShadingType, TableOfContents, PageBreak, PageNumber, TableLayoutType, ImageRun,
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
      for (let i = charsPerLine + 1; i <= Math.min(remaining.length, charsPerLine + 4); i++) {
        if (breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
      }
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
function img(path, w, h, capText) {
  const buf = fs.readFileSync(path);
  return [
    caption(capText),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new ImageRun({ type: "png", data: buf, transformation: { width: w, height: h } })] }),
  ];
}
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

B.push(h1("1. Executive Summary"));
B.push(body([{ text: "This addendum completes the request: the desk now runs a hedge-fund-style multi-strategy portfolio, fully integrated into the terminal, with a working Punch-Trade execution layer. The answer to 'is it final and optimized' is now yes — with the honest caveat that 'final' means validated on 201 days of real data and continuously audited, not permanently immutable. Three engines earn, three more candidates were tested and two of them failed, and the portfolio combines the survivors with inverse-drawdown risk parity." }]));
B.push(body([{ text: "The portfolio expansion round tested three new archetypes on the same real Binance USDT-M 15m data (May 1 – November 17, 2026, 57,819 bars per symbol, net of fees and slippage, stop-first worst-case fills). The SMC structure engine (EA-6: break-of-structure plus fair-value-gap retest) validated strongly: 945 trades, +206.9R, profit factor 1.40, profitable on all three symbols. The VWAP 2-sigma climax reversion (EA-7, PF 0.49) and the momentum-burst continuation (EA-8, PF 0.26) both failed and are suspended with autopsies. The three-engine portfolio — EA-5 at 46.7% risk weight, EA-2 at 30.0%, EA-6 at 23.3% — produces +130.8R weighted, profit factor 1.51, maximum drawdown 25.6R (versus 45.1R for the two-engine R546 set), engine correlations of at most 0.12, and six of seven positive months." }]));
B.push(body([{ text: "The terminal now carries the Playbook ▸ Punch tab: live candidate cards are generated by a 1:1 port of the validated rules operating on closed 15m Binance bars, and the PUNCH button queues the order through the desk's own wake protocol — the order lands in desk/state.json with status 'suggested' and a WAKE section for atg-exec, which executes on Delta Exchange India and writes the ticket back. Nothing about the desk contract changed; the human simply gains a one-click path from validated signal to execution queue. The build compiles clean, the cards route was verified against live Binance data, and the punch route was smoke-tested end-to-end." }]));

B.push(h1("2. Portfolio Expansion: What Was Tested"));
B.push(caption("Table 1 — New archetypes on real data, 201 days, net of costs"));
B.push(table(
  ["Engine", "Verdict", "n", "Net R", "Win rate", "PF", "maxDD"],
  [
    ["EA-6 SMC BOS + FVG retest", "LIVE — 3rd sleeve", "945", "+206.9", "47.7%", "1.40", "65.6R"],
    ["EA-6 per symbol (BTC/ETH/SOL)", "—", "316/320/309", "+37.5/+74.1/+95.3", "—", "—", "—"],
    ["EA-7 VWAP 2σ climax reversion", "SUSPENDED", "148", "−68.9", "38.5%", "0.49", "69.1R"],
    ["EA-8 Momentum-burst continuation", "SUSPENDED", "539", "−284.3", "50.3%", "0.26", "288.0R"],
  ],
  [26, 15, 13, 18, 10, 7, 11]
));
B.push(body("EA-6's rules: a confirmed swing structure (fractal pivots), a break of structure close, and a limit entry at the midpoint of the fair-value gap formed on the impulse leg, gated by the h4 EMA13×89 bias; stop beyond the gap low and the impulse swing, targets at BOS high + 0.5 ATR, then +2R and +3R. It earns on every symbol and diversifies because its entries are passive (limits inside retests) rather than the taker confirmations of EA-2 — the two engines' daily return correlation is 0.03."));
B.push(body("The failures teach the same lesson from two directions. EA-8 buys the strongest closes at taker cost — precisely the EA-1A pathology — and bleeds 284R across every month. EA-7 fades 2σ VWAP-band climaxes, but its re-entry confirmation prints after the bounce has already paid, so winners are thin and losers full-size. Both autopsies are recorded in desk/PLAYBOOK-EA-VALIDATED.md V2 and both engines are structurally excluded from the live detector."));
B.push(...img("/home/z/my-project/download/charts/r547_portfolio_equity.png", 580, 296, "Figure 1 — Weighted portfolio equity versus each engine individually"));

B.push(h1("3. The Three-Engine Portfolio"));
B.push(caption("Table 2 — Risk weights (inverse-maxDD parity) and evidence"));
B.push(table(
  ["Sleeve", "Weight", "PF", "Net R", "Standalone maxDD"],
  [
    ["EA-5 cascade-exhaustion (ETH/SOL only)", "0.467", "1.69", "+104.2", "lowest of the set"],
    ["EA-2 sweep-acceptance (all syms)", "0.300", "1.51", "+113.1", "19.9R"],
    ["EA-6 SMC BOS + FVG (all syms)", "0.233", "1.40", "+206.9", "65.6R"],
    ["PORTFOLIO (weighted)", "1.000", "1.51", "+130.8", "25.6R"],
  ],
  [36, 12, 12, 14, 26]
));
B.push(body("The portfolio's maximum drawdown of 25.6R is barely more than EA-2's standalone 19.9R while carrying +130.8R of weighted return — the diversification is doing real work, visible in Figure 1 where the green portfolio line compounds more smoothly than any single engine. Monthly stability: May −2.2 (effectively flat), June +35.0, July +15.0, August +16.3, September +25.4, October +24.2, November +17.0 through the 17th — six positive months out of seven. At roughly 8.7 weighted trades per day the desk has ample capacity on the majors, and the daily Sharpe of the R stream is 0.199 (about 3.1 annualized if the regime held, which we do not assume)."));
B.push(body("Execution of the weights is deliberately simple: each punched trade carries its engine's weight, so a 0.25% risk setting means EA-2 cards risk 0.075% of equity, EA-5 cards 0.117%, EA-6 cards 0.058%, with the Canonical Specification's heat caps (two same-direction crypto positions, ≤1.0% total) unchanged. The 50-real-fill likelihood-ratio gate remains the only mechanism by which any weight or threshold moves."));

B.push(h1("4. The Punch-Trade Layer — How to Use It"));
B.push(body("The terminal's new Playbook ▸ Punch tab turns the validated engines into an execution queue in four steps. First, the session context strip shows the running day VWAP, ±1σ band, POC, VAH/VAL, prior-day extremes and the h4 bias — the same map the engines read. Second, when a validated trigger prints on a closed 15m bar, a card appears with its engine badge, direction, exact entry, structural stop, the 40/40/20 target ladder, planned R, and a quantity hint computed as equity × risk% × engine weight ÷ stop distance; cards show as confirmed (trigger just printed), armed (setup developing, awaiting the confirmation close) or pending-fill (EA-6 limit resting at the FVG midpoint, 8-bar validity). Third, PUNCH queues the order: it is appended to desk/state.json as status 'suggested' with a WAKE.md section for atg-exec, which executes on Delta India and writes back status and ticket — the lifecycle table under the cards tracks it until fill. Fourth, nothing is invented: when no trigger conditions are met, the panel says so explicitly."));
B.push(bullet("Engine port: src/lib/strategy/playbook.ts — pure function of klines, closed bars only, stops and targets frozen at signal time exactly as backtested; suspended engines (EA-1/3/4/7/8) are structurally never emitted."));
B.push(bullet("Data path: GET /api/strategy/cards — the terminal's own fapi fetch chain with the taker-buy split for honest delta, through the shared circuit breaker; verified live (ok:true on real BTC klines) in this session."));
B.push(bullet("Execution bridge: POST /api/desk/punch — appends to desk/state.json orders[] (config never touched) and desk/inbox/WAKE.md; protected by the terminal's same-origin and host-allowlist proxy; smoke-tested end-to-end (order tp-… written with correct qty hint, then desk files restored)."));
B.push(bullet("UI: Playbook ▸ Punch tab (badge R547) in src/components/cg/playbook-desk.tsx; tsc and next build both green; classics show a not-applicable notice, matching the terminal's order-flow convention."));

B.push(h1("5. What Changed vs R546, and the Honest Limits"));
B.push(body("Relative to R546: the engine count goes from two to three (EA-6 added, +206.9R evidence), two more candidates were formally suspended (EA-7, EA-8), the risk framework gained explicit portfolio weights and a measured drawdown floor of 25.6R, and the terminal gained the punch layer — the desk contract, risk caps and the 50-fill scale-up gate are unchanged. The playbook file (desk/PLAYBOOK-EA-VALIDATED.md V2) remains the sole card-generation source, now bound to the three-engine portfolio."));
B.push(body("Limits, unchanged in kind from R546 and stated plainly: the validation is bar-level with conservative stop-first fills (the hftbacktest tick harness remains the next rung and could move EA-6's passive fills either way); funding is not modeled; the window covers one regime era; and Delta India's fees and spreads are the live friction the 0.25% live-start sizing is sized against. The R547 digest with directives is pushed to the desk; the daemon and atg-exec pick up the new intake rules (three engines, two more suspensions, weights) on their next activation."));

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
        title: "Portfolio & Punch-Trade",
        subtitle: "R547 Addendum — Three-Engine Portfolio, New Validations and Suspensions, and the Terminal Execution Layer",
        englishLabel: "DESK ROUND R547",
        metaLines: [
          "Prepared by: zai-desk (Quantitative Analysis Brain)",
          "For: atg-exec & Human Operator — Trade Desk",
          "Portfolio: +130.8R weighted · PF 1.51 · maxDD 25.6R · correlations ≤ 0.12",
          "New sleeve: EA-6 SMC BOS+FVG · +206.9R · PF 1.40 (real data, 201 days)",
          "Terminal: Playbook ▸ Punch tab live — cards → desk queue → Delta execution",
          "Date: 18 November 2026",
        ],
        footerLeft: "R547 · zai-desk",
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
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "R547 · Portfolio & Punch-Trade · zai-desk", size: 18, color: "808080", font: EN })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "808080", font: EN })] })] }) },
      children: B,
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/z/my-project/download/R547_Portfolio_PunchTrade_Addendum.docx", buf);
  console.log("written:", buf.length, "bytes");
});
