---
description: Loads the canonical execution runbook for Antigravity trading rounds.
trigger: always_on
---

# Antigravity workspace instructions

For a trading wake, operator-requested trade audit, or scheduled desk round, load
[the launch prompt](desk/CANONICAL_PROMPT.txt) and run it against
[the canonical specification](desk/CANONICAL_MASTER_SPECIFICATION.md). The Kernel
defines the precedence, twelve-step workflow, evidence and authorization rules.
Start with its wake command. Before each step, repeat the pinned `--step`
reader until it reports no remaining anchors. On a reader or evidence error,
report the current round as `INCOMPLETE` and preserve its files.

For repository engineering work, follow the user's request and the repository
instructions. Keep trading bootstrap, order operations and timer scheduling
scoped to trading rounds. Confirm tool outputs before reporting completion.
