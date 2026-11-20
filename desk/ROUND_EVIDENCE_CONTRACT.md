# Round evidence contract

Save the audit locally under `data/round-evidence/<round-id>/`. Use the exact R-prefixed ID and the SOP digest returned by the wake tool. The verifier reads these files and prints its verdict to stdout. It does not modify the bundle or call a venue.

| File | Required contents |
|---|---|
| `wake_receipt.json`, `section_receipts/*.json` | Original outputs automatically saved by the wake tool. Repeat `--step <n>` until its remaining anchors are empty. The receipt chain binds to the original wake ID, canonical spec, launch prompt and this contract. Before formulation, require `--require-formulation-reads` to pass and record the full SOP line count. Older or mixed-wake receipts require a new round ID. |
| `scope.json` | `instruments` array keyed by `venue,instrument_id`, using `delta` and `mt5`. Include `inventories.delta` and `inventories.mt5` with `instrument_ids` from the respective raw broker inventories and a `source` reference. Include `managed` rows using the same key and source reference for the reconciled orders and positions, and a single UTC `cutoff_utc`. |
| `screen_rows.json` | `rows`, one per scope key and `funnel` from `FUNNEL-01` to `FUNNEL-05`. Include `status`, `reason` and `source`. Give every hit a dossier. For `NOT_APPLICABLE`, cite the predeclared scope condition. |
| `telemetry_rows.json` | `rows`, keyed by `venue,instrument_id,dimension`. Include all D01–D16 per funnel hit or managed symbol. Attach `source`, `status`, `value`, `unit`, `source_event_utc`, `received_utc` and policy-derived `freshness_seconds`. For D13 inapplicability give the rule and source. For D11 add `windows` with a raw reference for each of `3d`, `7d` and `30d`. For D16 use USD and `window_seconds: 300`. |
| `gate_rows.json` | `rows`, keyed by `venue,instrument_id,rule`, with `status` (`PASS`, `FAIL`, or justified `N/A`), measured inputs, threshold, `reason`, and `source`. Use `round,round` for C-01–C-10. For each funnel hit include the eleven GATE, ten INQ and twenty-two PIT rule rows. Record a market-dependent rule as unresolved when its data is missing. |

The four manifest files include `round_id` and `spec_sha256`. In `scope.json`, also list `desk_positions` with `venue`, `ticket` (string), `instrument_id`, `asset_class` (`crypto` or `tradfi`) and `source` for each owned open position from either venue. Use an empty array only for a broker-confirmed empty desk book. In the gate rows name the input `observed` and the limit `threshold`.

A source reference is an object with a relative `path` under `raw/` and the `sha256` of the original bytes. Use the read-only capture tool for venue inventories and terminal data. It binds receipts in `captures/` to this wake, feed, actual request and receipt time. Preserve tool errors as unresolved evidence.

```powershell
python scripts/capture_round_evidence.py --round <round-id> --feed delta-inventory
python scripts/capture_round_evidence.py --round <round-id> --feed mt5-inventory
python scripts/capture_round_evidence.py --round <round-id> --feed market --symbol BTC
python scripts/capture_round_evidence.py --round <round-id> --feed liqlevels --symbol BTC --range 7d
```

Delta keys use exchange product IDs from the captured live perpetual inventory. MT5 keys use broker symbol names from the configured account's enabled inventory. Never substitute a hand-picked watchlist for the inventory.
Each managed instrument must join to that inventory and cite the live orders or positions payload containing the exact venue instrument ID and symbol. A catalog, ticker, or prior round cannot stand in for the broker book.

For each resolved funnel row record `checks` with `feed`, optional `range`, `source`, JSON `pointer`, `observed`, `op` (`gte`, `gt`, `lte`, `lt`, or `eq`) and `threshold`. Use the §17 trigger conditions with enough per-feed observations to justify each result. Slot or heat restrictions belong in the gate records and cannot populate the screen.

For each direct telemetry value supply `value_pointer`; the verifier resolves it in the correct captured payload. Use the source's data timestamp as `source_event_utc` and its capture receipt time as `received_utc`. D11 checks the actual symbol and window in each response. D16 recomputes the five-minute sum using captured events, and rejects incomplete or capped coverage. Where a dimension needs a derivation not covered by the verifier, report it as unresolved until an executable derivation or trusted materializer is available. Never fill a missing value from a different instrument.

Keep the full SOP step artifacts in addition to these verifier inputs. Each gate result should state the observed value, threshold, and consequence. Reconcile scope across both venues before classifying any orders. Separate gross target-to-stop geometry, stressed payoff after costs, and EV backed by a calibrated outcome model. Protect original-risk and age evidence for open positions. If the account audit shows a slot or risk limit breached, the gate cannot be PASS even when the order is already resting.

`python scripts/verify_round_evidence.py --round <round-id>` returns `INCOMPLETE` with exit 1 on a failed check. A successful evidence check returns `EVIDENCE_CHECKS_PASSED` with `round_outcome: UNATTESTED`. The check verifies the receipt and source contract, observed values, and selected contradictions. Keep the round outcome unresolved until actual rule calculations and ownership are independently verified. Only signed admission through the gateway can enable live action.

## R641 correction

The section reader delivered the required anchors. The reported `DONE` verdict is superseded by `INCOMPLETE`. The builder used hard-coded venue inventories, slot capacity as the discovery result, and BTC payloads and fabricated timestamps for other instruments. Preserve the original files. Use a new round for a fresh capture. Record a timer as read-only only if its actual payload contains no venue mutation or system-control actions.

## R640 correction

Treat the original R640 report as superseded by an `INCOMPLETE` verdict. The original evidence remains available for review. Its screen has counts and symbol lists without exact per-instrument disposition rows. D16 contains Oracle output. Its own reconciliation shows three desk positions including two crypto positions, against limits of two and one. TRX was reported eligible with Oracle 45 above the Delta short ceiling of 35. The recorded prices yield 2.76R on the unstressed distance and 2.30R on the 1.20× stressed distance before costs. The stated EV has no saved calibration evidence. Present missing inputs as missing and describe resting orders as observed until their lifecycle checks are supported.
