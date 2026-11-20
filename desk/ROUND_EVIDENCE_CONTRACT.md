# Round evidence contract

Save the audit locally under `data/round-evidence/<round-id>/`. Use the exact R-prefixed ID and the SOP digest returned by the wake tool. The verifier reads these files and prints its verdict to stdout. It does not modify the bundle or call a venue.

| File | Required contents |
|---|---|
| `wake_receipt.json`, `section_receipts/*.json` | Original outputs saved by the wake tool with `--save`. Add `--step <n>` to each section read. Save each step's own receipts before evaluating it. |
| `scope.json` | `instruments` array keyed by `venue,instrument_id`, using `delta` and `mt5`. Include `inventories.delta` and `inventories.mt5` with `instrument_ids` from the respective raw broker inventories and a `source` reference. Include `managed` rows using the same key and source reference for the reconciled orders and positions, and a single UTC `cutoff_utc`. |
| `screen_rows.json` | `rows`, one per scope key and `funnel` from `FUNNEL-01` to `FUNNEL-05`. Include `status`, `reason` and `source`. Give every hit a dossier. For `NOT_APPLICABLE`, cite the predeclared scope condition. |
| `telemetry_rows.json` | `rows`, keyed by `venue,instrument_id,dimension`. Include all D01–D16 per funnel hit or managed symbol. Attach `source`, `status`, `value`, `unit`, `source_event_utc`, `received_utc` and policy-derived `freshness_seconds`. For D13 inapplicability give the rule and source. For D11 add `windows` with a raw reference for each of `3d`, `7d` and `30d`. For D16 use USD and `window_seconds: 300`. |
| `gate_rows.json` | `rows`, keyed by `venue,instrument_id,rule`, with `status` (`PASS`, `FAIL`, or justified `N/A`), measured inputs, threshold, `reason`, and `source`. Use `round,round` for C-01–C-10. For each funnel hit include the eleven GATE, ten INQ and twenty-two PIT rule rows. Record a market-dependent rule as unresolved when its data is missing. |

The four manifest files include `round_id` and `spec_sha256`. A source reference is an object with a relative `path` under `raw/` and the `sha256` of the original bytes. Keep the raw payload and cite the precise field used. If a tool failed, preserve its error and record the affected row as unresolved. The same raw payload may support several rows if its key, field and timestamp match.

Keep the full SOP step artifacts in addition to these verifier inputs. Each gate result should state the observed value, threshold, and consequence. Reconcile scope across both venues before classifying any orders. Separate gross target-to-stop geometry, stressed payoff after costs, and EV backed by a calibrated outcome model. Protect original-risk and age evidence for open positions. If the account audit shows a slot or risk limit breached, the gate cannot be PASS even when the order is already resting.

`python scripts/verify_round_evidence.py --round <round-id>` returns `INCOMPLETE` with exit 1 on a failed check. This rejects prose-only evidence and checks file references, keys, timestamps, and selected contradictions. `EVIDENCE_CHECKS_PASSED` still requires independent verification of the actual rule calculations, data source authenticity, ownership, and official signed gateway admission before any live action.

## R640 correction

Treat the original R640 report as superseded by an `INCOMPLETE` verdict. The original evidence remains available for review. Its screen has counts and symbol lists without exact per-instrument disposition rows. D16 contains Oracle output. Its own reconciliation shows three desk positions including two crypto positions, against limits of two and one. TRX was reported eligible with Oracle 45 above the Delta short ceiling of 35. The recorded prices yield 2.76R on the unstressed distance and 2.30R on the 1.20× stressed distance before costs. The stated EV has no saved calibration evidence. Present missing inputs as missing and describe resting orders as observed until their lifecycle checks are supported.
