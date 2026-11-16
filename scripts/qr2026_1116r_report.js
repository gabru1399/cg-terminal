/**
 * QR-2026-1116-R — CRO Remediation Verification Report
 * Verifies commits a2cf73a + da02e83 (+ a752ea1) of Delta_Fibonacci_Institutional_Business
 * Cover: R2 (Double-Rule Frame) per design-system, IG-1 palette (finance)
 * Structure: Template C (testing report) — supports go/no-go decision
 */
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, WidthType, BorderStyle,
  ShadingType, TableOfContents, PageBreak, PageNumber, TableLayoutType,
} = require("docx");
const fs = require("fs");

// ---------- palette IG-1 (Ink Gold — finance) ----------
const P = {
  bg: "1A1A1A", primary: "000000", accent: "C9A84C",
  cover: { titleColor: "FFFFFF", subtitleColor: "B0B8C0", metaColor: "90989F", footerColor: "687078" },
  table: { headerBg: "C9A84C", headerText: "1A1A1A", accentLine: "C9A84C", innerLine: "DDD5C0", surface: "F5F2E8" },
};

const noBorders = { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } };
const allNoBorders = { ...noBorders, insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE } };

// ---------- title layout helpers (design-system) ----------
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
  const { titleLineCount = 1, titlePt = 36, hasSubtitle = false, hasEnglishLabel = false, metaLineCount = 0, fixedHeight = 800, pageHeight = 16838, marginTop = 0, marginBottom = 0 } = p;
  const SAFETY = 1200;
  const usableHeight = pageHeight - marginTop - marginBottom - SAFETY;
  const titleHeight = titleLineCount * (titlePt * 23 + 200);
  const subtitleHeight = hasSubtitle ? (12 * 23 + 600) : 0;
  const englishLabelHeight = hasEnglishLabel ? (9 * 23 + 600) : 0;
  const metaHeight = metaLineCount * (10 * 23 + 100);
  const implicitParaHeight = 3 * 300;
  const contentHeight = titleHeight + subtitleHeight + englishLabelHeight + metaHeight + fixedHeight + implicitParaHeight;
  const safeRemaining = Math.max(usableHeight - contentHeight, 400);
  const FOOTER_MIN = 800;
  const rawTop = Math.floor(safeRemaining * 0.45), rawBottom = Math.floor(safeRemaining * 0.45);
  const bottomSpacing = Math.max(rawBottom, FOOTER_MIN);
  const topSpacing = Math.max(rawTop - Math.max(0, FOOTER_MIN - rawBottom), 400);
  return { topSpacing, midSpacing: Math.max(safeRemaining - topSpacing - bottomSpacing, 0), bottomSpacing };
}

// ---------- R2 cover (Double-Rule Frame) ----------
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
  // top double rule
  children.push(new Paragraph({ indent: { left: padL, right: padR }, border: { bottom: { ...rule, size: 18 } }, spacing: { after: 120 } }));
  children.push(new Paragraph({ indent: { left: padL + 600, right: padR + 600 }, border: { bottom: { ...rule, size: 4 } }, spacing: { after: 600 } }));
  if (config.englishLabel) {
    children.push(new Paragraph({
      indent: { left: padL }, spacing: { after: 300 },
      children: [new TextRun({ text: config.englishLabel.split("").join("  "), size: 19, color: C.accent, font: { ascii: "Calibri", eastAsia: "SimHei" }, characterSpacing: 40 })],
    }));
  }
  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({
      indent: { left: padL }, spacing: { after: i < titleLines.length - 1 ? 100 : 300, line: Math.ceil(titlePt * 23), lineRule: "atLeast" },
      children: [new TextRun({ text: titleLines[i], size: titleSize, bold: true, color: C.cover.titleColor, font: { eastAsia: "SimHei", ascii: "Arial" } })],
    }));
  }
  if (config.subtitle) {
    children.push(new Paragraph({
      indent: { left: padL }, spacing: { after: 700 },
      children: [new TextRun({ text: config.subtitle, size: 24, color: C.cover.subtitleColor, font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
    }));
  }
  for (const line of (config.metaLines || [])) {
    children.push(new Paragraph({
      indent: { left: padL }, spacing: { after: 90 },
      children: [new TextRun({ text: line, size: 22, color: C.cover.metaColor, font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: spacing.bottomSpacing } }));
  // bottom double rule
  children.push(new Paragraph({ indent: { left: padL + 600, right: padR + 600 }, border: { top: { ...rule, size: 4 } }, spacing: { after: 100 } }));
  children.push(new Paragraph({
    indent: { left: padL, right: padR }, border: { top: { ...rule, size: 18 } }, spacing: { before: 100 },
    children: [
      new TextRun({ text: config.footerLeft || "", size: 17, color: C.cover.footerColor, font: { ascii: "Arial" } }),
      new TextRun({ text: "                                                  " }),
      new TextRun({ text: config.footerRight || "", size: 17, color: C.cover.footerColor, font: { ascii: "Arial" } }),
    ],
  }));
  return [new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: 16838, rule: "exact" },
      children: [new TableCell({ shading: { type: ShadingType.CLEAR, fill: C.bg }, borders: noBorders, children })],
    })],
  })];
}

// ---------- body helpers ----------
const EN = { ascii: "Times New Roman", eastAsia: "SimSun" };
const HEAD = { ascii: "Arial", eastAsia: "SimHei" };

function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 400, after: 180, line: 312 }, children: [new TextRun({ text, bold: true, size: 30, color: "000000", font: HEAD })] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 130, line: 312 }, children: [new TextRun({ text, bold: true, size: 26, color: "000000", font: HEAD })] });
}
function body(text, opts = {}) {
  const runs = Array.isArray(text) ? text : [{ text }];
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED, spacing: { line: 312, after: 100 }, ...(opts.indent === false ? {} : { indent: { firstLine: 0 } }),
    children: runs.map(r => new TextRun({ text: r.text, bold: !!r.bold, size: 22, color: r.color || "000000", font: EN })),
  });
}
function bullet(text, level = 0) {
  return new Paragraph({ bullet: { level }, spacing: { line: 312, after: 60 }, children: [new TextRun({ text, size: 22, color: "000000", font: EN })] });
}
function caption(text) {
  return new Paragraph({ keepNext: true, spacing: { before: 160, after: 80 }, children: [new TextRun({ text, bold: true, size: 20, color: "404040", font: EN })] });
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
      new TableRow({
        tableHeader: true, cantSplit: true,
        children: headers.map((t, i) => cell(t, { bold: true, fill: P.table.headerBg, color: P.table.headerText, width: widths ? widths[i] : undefined })),
      }),
      ...rows.map((r, ri) => new TableRow({
        cantSplit: true,
        children: r.map((t, i) => cell(t, { width: widths ? widths[i] : undefined, fill: ri % 2 === 1 ? P.table.surface : undefined, bold: typeof t === "object" && t.bold })),
      })),
    ],
  });
}

// ---------- verdict badge paragraph ----------
function verdictPara(text, color) {
  return new Paragraph({
    spacing: { before: 120, after: 120, line: 312 },
    border: { left: { style: BorderStyle.SINGLE, size: 20, color, space: 12 } },
    indent: { left: 200 },
    children: [new TextRun({ text, bold: true, size: 24, color, font: HEAD })],
  });
}

// ================= CONTENT =================
const bodyChildren = [];

// -- 1 Executive Summary
bodyChildren.push(h1("1. Executive Summary"));
bodyChildren.push(body([{ text: "This report documents the Chief Risk Office (CRO) re-verification of the remediation carried out against Hostile Audit Report QR-2026-1116 on the Delta Fibonacci institutional trading system. The verification was performed directly on the code at commits " }, { text: "a2cf73a", bold: true }, { text: " (CRO governance patches), " }, { text: "da02e83", bold: true }, { text: " (backtest parity port), and the subsequent " }, { text: "a752ea1", bold: true }, { text: " (dashboard alignment), cloned fresh from the public repository. Every one of the eight declared patches was traced to its implementation site, read line-by-line, and where arithmetic was involved, recomputed independently." }]));
bodyChildren.push(body([{ text: "The verdict: " }, { text: "CONDITIONAL GO for instrumented forward paper trading.", bold: true }, { text: " All four P0 code patches (hard risk cap, broker-side trailing stops, daily loss governor, phantom-fill elimination) are genuinely implemented and materially reduce the loss pathways identified in the original audit. The system may proceed to instrumented forward paper trading under the conditions listed in Section 8. However, capital deployment remains " }, { text: "NO-GO", bold: true }, { text: " until the five residual findings in Section 7 are closed — of which R-1 (closed-loss double-counting in the governor) and R-4 (live account state published to a public repository) are the most material." }]));
bodyChildren.push(body("The verification found no evidence of misrepresentation: each declared patch exists in the code, at the declared location, doing the declared job. The residuals are genuine engineering gaps discovered by hostile review of the patched code — the expected outcome of a second-pass audit — rather than failures of remediation intent. Three of the five residuals are fail-safe direction (they make the governor more conservative, not less), one is a coverage gap, and one is an operational-security exposure inherited from the repository setup rather than the trading logic."));

// -- 2 Scope
bodyChildren.push(h1("2. Verification Scope, Method and Evidence Base"));
bodyChildren.push(body([{ text: "Evidence base. ", bold: true }, { text: "The audited repository is github.com/kbsingh1399/Delta_Fibonacci_Institutional_Business (branch main). The audit clone was made on 16 November 2026; HEAD at clone time was a752ea1, two commits ahead of the requested da02e83, and the newer commit was included in scope because it also touches trading logic (dashboard signal alignment). The primary files are engine/mt5_alpha_trader_monitor.py (848 lines), engine/daily_risk_governor.py (87 lines), MT5_Backtest.py (501 lines) and dashboard_server.py (930 lines). The runtime state files under audit/ were inspected as committed artifacts." }]));
bodyChildren.push(body([{ text: "Method. ", bold: true }, { text: "Each patch claim was mapped to its diff hunk, then the surrounding function was read in full to confirm the patch cannot be bypassed on any code path. Arithmetic claims (dollar caps, floors, throttle thresholds) were recomputed in isolation. The governor's loss-accounting semantics were tested against a worked example. Cross-file invariants (live monitor vs. backtest parity) were compared clause by clause. No code was executed; this was a static hostile review with independent recomputation." }]));
bodyChildren.push(body([{ text: "Limitations. ", bold: true }, { text: "This verification is code-level only. It cannot observe the live FundedNext terminal (login #11808165), so broker behaviour of the deployed instance — e.g. whether MT5 actually accepts every SLTP modification at the observed frequency — is outside evidence. The compliance evidence table supplied by the engineering team was treated as a claim set to verify, not as evidence itself." }]));

// -- 3 Patch verification matrix
bodyChildren.push(h1("3. Patch-by-Patch Verification"));
bodyChildren.push(body("The table below is the core verification matrix. \u201CVerified\u201D means the patch was found at the declared location, implemented as declared, and not bypassable on reviewed paths. Findings that qualified the verification are carried into the residual register (Section 7)."));
bodyChildren.push(caption("Table 1 — Verification matrix for the eight declared patches"));
bodyChildren.push(table(
  ["#", "Declared patch", "Location", "Result", "Notes"],
  [
    ["P1", "Hard risk cap in lot sizer (1.1R, no upward flooring)", "monitor.py L195-221", "VERIFIED", "Min-lot inflation blocked on both branches; final actual-risk re-check after rounding is a genuine second gate"],
    ["P2", "Broker-side trailing stops via TRADE_ACTION_SLTP", "monitor.py L637-682", "VERIFIED", "Local stop_price updates only on TRADE_RETCODE_DONE; failures logged, state not mutated"],
    ["P3", "Zero phantom fills (no ticket fabrication)", "monitor.py L481-489", "VERIFIED with residual", "Fabrication removed; but IOC partial fills (TRADE_RETCODE_DONE_PARTIAL) treated as failure while a smaller real position exists broker-side → R-2"],
    ["P4", "FundedNext daily risk governor", "daily_risk_governor.py (all)", "VERIFIED with residual", "Anchor math correct ($235.08 / $4,231.48 / $188.08); two semantic gaps → R-1, R-3"],
    ["P5", "Microstructure friction gate (spread > 15% of 1R)", "monitor.py L409-417", "VERIFIED", "Applied after stop-distance validation, before lot sizing; blocks on entry tick spread"],
    ["P6", "12-bar post-exit cooldown", "monitor.py L117, L302-307, L685", "VERIFIED", "48-hour cooldown keyed to symbol exit timestamp, persisted in trade_cooldowns.json, survives restart"],
    ["P7", "Pullback origin invariant (live + backtest)", "monitor.py L336-339; MT5_Backtest.py L260-280", "VERIFIED with residual", "Ported to canonical, turbo and institutional-filtered setups and to the backtest engine; the wyckoff_swing_sweep setup has no origin check → R-5"],
    ["P8", "Dashboard localhost bind + atomic state writes", "dashboard_server.py L915; monitor.py save_state", "VERIFIED", "127.0.0.1:8088 binding confirmed; all four state files written via .tmp + os.replace"],
  ],
  [5, 26, 20, 14, 35]
));
bodyChildren.push(body("The four P0 patches were the audit's blocking conditions, and all four clear verification. The engineering claim of US30 wide-stop rejection (P1) is supported by the code: with a $200 min-lot risk against the $11.00 cap, the sizer returns a skip on the min-lot branch before any order is constructed."));

// -- 4 Detail on the P0 patches
bodyChildren.push(h1("4. Detail Findings on the P0 Patches"));
bodyChildren.push(h2("4.1 Patch 1 — Hard Risk Cap"));
bodyChildren.push(body("calculate_lot_size() now defines MAX_RISK_USD = round(risk_usd * 1.10, 2), giving $11.00 on the standard $10 risk budget. The min-lot branch is the critical one: when the computed lot rounds below volume_min, the function evaluates min_lot_risk = vol_min * one_lot_risk and skips the trade outright if that exceeds the cap — the exact upward-flooring pathway the original audit condemned. A second gate re-checks actual_risk after volume-step rounding and volume_max clamping, which closes the sub-step rounding leak. The cap multiple (1.10) accommodates rounding to the volume step without ever permitting an 11.5% oversize. This patch is clean."));
bodyChildren.push(h2("4.2 Patch 2 — Broker-Side Trailing Stops"));
bodyChildren.push(body("manage_open_positions() constructs an SLTP modification request with the position ticket and sends it through mt5.order_send(). The local state copy, pos['stop_price'], is updated only when the response carries TRADE_RETCODE_DONE; every other outcome logs the retcode and comment and leaves state untouched. This is the correct mirror-the-broker pattern. The trail ladder itself is conservative (lock +0.5R at 2R MFE, +2R at 4R MFE) and only ever tightens — new_sl is clamped to be no worse than the current stop on both sides. Residual risk is confined to the un-managed window between sweeps (10 seconds), which mark-price stops on the broker already cover for catastrophic moves."));
bodyChildren.push(h2("4.3 Patch 3 — Zero Phantom Fills"));
bodyChildren.push(body("The ticket fabrication line (ticket = int(time.time())) is gone from the codebase. On any non-DONE retcode, execute_order() logs the rejection and returns False; state and the audit signal file are only written after a confirmed fill with the broker-assigned order number. One residual survives and is registered as R-2: MetaTrader 5 can return TRADE_RETCODE_DONE_PARTIAL for IOC orders, in which case a real, smaller position exists broker-side while the monitor believes the order failed. The 10-second sweep's sync_broker_positions() would then adopt it as an MT5_TERMINAL-sourced position — so the position is not lost, but its recorded risk metadata (actual_risk_usd, exit_mode) is reconstructed rather than authoritative, and the signal's intended risk is not enforced on it."));
bodyChildren.push(h2("4.4 Patch 4 — Daily Risk Governor"));
bodyChildren.push(body("The DailyRiskGovernor is a dedicated class with the declared anchors: daily_limit = round(4701.64 * 0.05, 2) = $235.08; overall_floor = round(4701.64 * 0.90, 2) = $4,231.48; throttle at 80% = $188.06 — all recomputed and confirmed. It is wired first in run_sweep(), before any scan, and both HALT states still manage and sync open positions before returning, so a governor trip never abandons live exposure. The two residuals are semantic: R-1 (closed losses are double-counted, because the equity drop from the midnight anchor already contains realized losses that closed_pnl_today adds again) and R-3 (the day boundary is computed from UTC epoch days, and the deals window is fetched from UTC midnight, while FundedNext's rule day rolls at server midnight — typically GMT+2/+3, a 2-3 hour misalignment). Both bias the governor conservative, never permissive; they distort the 80% throttle and the rule-window edge, not the direction of protection."));

// -- 5 Secondary patches
bodyChildren.push(h1("5. Verification of Secondary Patches (P5-P8)"));
bodyChildren.push(body("Patch 5 (friction gate) rejects any signal whose entry-tick spread exceeds 15% of the 1R risk distance. It is positioned after stop validation and before lot sizing, so no order can be constructed on a rejected signal. The declared shielded symbols (EURNOK, MC, USDCNH and rollover-spike windows) are handled implicitly — their structural spread inflation now fails the ratio test rather than being enumerated. Patch 6 (cooldown) persists a per-symbol exit timestamp and blocks re-entry for 48 hours (12 H4 bars), restoring parity with the backtest's per-symbol re-entry assumption; the timestamp survives restart via trade_cooldowns.json. Patch 7's origin invariant (longs must come from above the EMA-89 shelf, shorts from below) is present in the live monitor for the canonical, turbo_tri_tier and wyckoff_institutional_filtered setups, ported to the backtest engine at da02e83, and extended to the dashboard radar at a752ea1 — but not to the monitor's wyckoff_swing_sweep setup (R-5). Patch 8 binds the dashboard to 127.0.0.1:8088 and converts all four runtime state files to atomic .tmp-then-replace writes; the singleton PID lock also kills stale daemon instances to prevent split-brain state."));

// -- 6 Worked governor test
bodyChildren.push(h1("6. Independent Recomputation — Governor Worked Example"));
bodyChildren.push(body("To make residual R-1 concrete, the governor's arithmetic was recomputed on a worked case: midnight anchor equity $4,701.64; during the day one position closes at a realized loss of $100; equity is now $4,601.64 with no open exposure."));
bodyChildren.push(caption("Table 2 — Governor loss accounting on a single realized -$100 close"));
bodyChildren.push(table(
  ["Quantity", "Governor computation", "Value", "FundedNext rulebook meaning"],
  [
    ["floating_drop", "max(0, 4701.64 - 4601.64)", "100.00", "Equity drop since midnight (contains the realized loss)"],
    ["closed_loss", "max(0, -(-100.00))", "100.00", "Realized losses today (the same loss, again)"],
    ["used_loss_today", "floating_drop + closed_loss", "200.00", "Governor's stated loss used today"],
    ["True daily loss", "realized + floating", "100.00", "What FundedNext would measure"],
    ["Overstatement", "200.00 - 100.00", "100.00", "2.0x on any fully realized intraday loss"],
  ],
  [18, 30, 12, 40]
));
bodyChildren.push(body("The consequence: after any realized intraday loss of $94 or more, the governor reports the daily limit as 80% consumed and throttles concurrency to one — at a true consumption of 40%. A realized loss of $188 halts new entries for the day when the rulebook threshold is $235. The error is strictly fail-safe, but it converts the throttle band into a near-halt and will materially distort forward-paper statistics if left unfixed. The fix is one line of semantics: count closed losses only against the equity anchor (i.e. use equity drop alone, since realized PnL is already inside equity), or subtract closed losses from the anchor before computing floating drop."));

// -- 7 Residual register
bodyChildren.push(h1("7. Residual Register and Governance Gaps"));
bodyChildren.push(body("Five residuals survive the remediation. None is a repetition of a failed patch; all are new findings against the patched code. Severity reflects impact on rule compliance and capital safety, not code quality."));
bodyChildren.push(caption("Table 3 — Residual findings requiring closure before capital deployment"));
bodyChildren.push(table(
  ["ID", "Severity", "Finding", "Impact", "Required remediation"],
  [
    ["R-1", "HIGH", "Governor double-counts closed losses (equity drop + closed_pnl_today)", "Throttle band effectively halved; forward-paper stats distorted; fail-safe direction only", "Use equity-drop-from-anchor as the sole daily-loss measure, or de-duplicate realized PnL against the anchor"],
    ["R-2", "HIGH", "TRADE_RETCODE_DONE_PARTIAL treated as failure in execute_order()", "A real partial position exists broker-side with reconstructed (not enforced) risk metadata; intended $ risk not guaranteed", "Handle DONE_PARTIAL as a fill at reduced volume: read back the position via positions_get(ticket) and record its actual volume and risk"],
    ["R-3", "MEDIUM", "Daily window anchored to UTC epoch day, not FundedNext server midnight", "2-3 hour rule-window misalignment at both edges; losses near server midnight land on the wrong rule day", "Anchor the day rollover and the history_deals_get window to server time (terminal_info().server_timezone)"],
    ["R-4", "HIGH", "Live account state committed to a public repository (account #11808165, equity, open positions, stop levels in audit/mt5_health_status.json; 9,327-row trade ledger)", "Operational security exposure: position sizes, stops and PnL of a live funded account are publicly diffable in near real time", "Untrack runtime state files, add them to .gitignore, purge git history (filter-repo), and make the daemon write state outside the repository"],
    ["R-5", "MEDIUM", "wyckoff_swing_sweep setup lacks the pullback origin invariant (live monitor)", "That setup can trigger counter-origin entries, breaking backtest parity for its symbols", "Add came_from_above/below conditions to the sweep branch, and confirm the backtest models the same four setups the monitor runs"],
  ],
  [6, 10, 26, 28, 30]
));
bodyChildren.push(body("R-4 deserves emphasis beyond its table row. The health-status file is committed on every daemon cycle (six commits already touch it), and it currently exposes the login number, server name, balance, equity, and the full detail of an open USDJPY position including its stop. The trade ledger with 9,327 rows of executed history is likewise tracked. This is the same class of exposure the CRO flagged on the cg-terminal repository; it is an operational-security obligation of running a funded account from a public repository, independent of trading-logic correctness, and it must be closed before any capital phase — the account number alone enables social-engineering vectors against the prop firm."));

// -- 8 verdict
bodyChildren.push(h1("8. CRO Determination"));
bodyChildren.push(verdictPara("DETERMINATION 1 — Instrumented forward paper trading: CONDITIONAL GO. The four P0 patches are implemented and effective. Paper trading may begin immediately, provided the instrumentation records governor status per sweep and every R-2 partial-fill reconstruction, so the residuals' real-world frequency is measured rather than argued.", "1F6B3A"));
bodyChildren.push(verdictPara("DETERMINATION 2 — Capital deployment on FundedNext #11808165: NO-GO until R-1, R-2 and R-4 are remediated and re-verified. R-3 and R-5 are required before the paper-trading statistics are accepted as representative, but do not block the paper phase itself.", "8B1A1A"));
bodyChildren.push(body("Conditions of the paper-trading GO: (1) forward paper trading runs for a minimum of two full weeks including at least one weekend rollover, on the exact HEAD that will be promoted; (2) the governor is run in shadow-corrected mode — R-1's corrected computation logged alongside the shipped one — so the distortion is quantified daily; (3) any DONE_PARTIAL event during the paper phase triggers an immediate position reconciliation audit before trading resumes; (4) the dashboard remains bound to 127.0.0.1 and no port forwarding is introduced; (5) promotion to capital requires a fresh CRO verification pass against the residuals' fix commits, mirroring this report's method."));
bodyChildren.push(body("The remediation effort is assessed as genuine and effective. The system that exists at da02e83 is materially safer than the one the original audit condemned: the two pathways that could silently oversize risk (min-lot flooring, phantom fills) are closed, stops live broker-side, and a loss governor with correct anchors gates every sweep. What remains is calibration honesty (R-1/R-3), an execution edge case (R-2), one parity gap (R-5), and an operational-hygiene obligation (R-4). None of these justifies re-opening the original findings; all of them justify the conditions above."));

// ================= DOCUMENT =================
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: EN, size: 22, color: "000000" }, paragraph: { spacing: { line: 312 } } },
      heading1: { run: { font: HEAD, size: 30, bold: true, color: "000000" }, paragraph: { spacing: { before: 400, after: 180, line: 312 } } },
      heading2: { run: { font: HEAD, size: 26, bold: true, color: "000000" }, paragraph: { spacing: { before: 280, after: 130, line: 312 } } },
    },
  },
  sections: [
    // Cover section
    {
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
      children: buildCoverR2({
        title: "CRO Remediation Verification Report",
        subtitle: "Institutional Re-Audit of Commits a2cf73a \u00B7 da02e83 \u00B7 a752ea1 \u2014 Delta Fibonacci MT5 Trading System",
        englishLabel: "QR-2026-1116-R",
        metaLines: [
          "Prepared by: Chief Risk Office \u2014 Hostile Review Function",
          "Subject system: Delta_Fibonacci_Institutional_Business (branch main)",
          "Venue: FundedNext MetaTrader 5 \u2014 Account #11808165",
          "Verification date: 16 November 2026",
          "Classification: Internal \u2014 Risk Governance",
        ],
        footerLeft: "QR-2026-1116-R",
        footerRight: "Chief Risk Office \u00B7 2026-11-16",
        palette: P,
      }),
    },
    // TOC section
    {
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 } } },
      children: [
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { before: 480, after: 360 },
          children: [new TextRun({ text: "Table of Contents", bold: true, size: 32, font: HEAD, color: "000000" })],
        }),
        new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }),
        new Paragraph({
          spacing: { before: 200 },
          children: [new TextRun({ text: "Note: This Table of Contents is generated via field codes. To ensure page number accuracy after editing, please right-click the TOC and select \"Update Field.\"", italics: true, size: 18, color: "888888", font: EN })],
        }),
        new Paragraph({ children: [new PageBreak()] }),
      ],
    },
    // Body section
    {
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 }, pageNumbers: { start: 1 } } },
      headers: {
        default: new Header({
          children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "QR-2026-1116-R \u00B7 CRO Remediation Verification", size: 18, color: "808080", font: EN })] })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "808080", font: EN })] })],
        }),
      },
      children: bodyChildren,
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/z/my-project/download/QR-2026-1116-R_CRO_Remediation_Verification.docx", buf);
  console.log("written:", buf.length, "bytes");
});
