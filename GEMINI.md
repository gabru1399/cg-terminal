---
description: Loads the canonical execution runbook for Antigravity trading rounds.
trigger: always_on
---

# Antigravity workspace instructions

For a trading wake, trade review, trade formulation, or scheduled desk round, load
[the launch prompt](desk/CANONICAL_PROMPT.txt) and run it against
[the canonical specification](desk/CANONICAL_MASTER_SPECIFICATION.md). The Kernel
defines the precedence, twelve-step workflow, evidence and authorization rules.
Start with its wake command. Before each step, repeat the pinned `--step`
reader until it reports no remaining anchors. On a reader or evidence error,
report the current round as `INCOMPLETE` and preserve its files.
Open the Kernel of `desk/CANONICAL_MASTER_SPECIFICATION.md` by that filename
in the current turn, using the wake receipt's line bounds. Name and link the
specification at the top of the report, and distinguish a resumed round.
Require complete SOP coverage from line 1 through Appendix F before trade
formulation. Use `--require-formulation-reads` after the Step 5 reads.
Reject a timer payload that mixes `AUDIT` and venue mutations or process
control. Report the conflict and task ID without creating a replacement timer.

For repository engineering work, follow the user's request and the repository
instructions. Keep trading bootstrap, order operations and timer scheduling
scoped to trading rounds. Confirm tool outputs before reporting completion.
