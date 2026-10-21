# C3 independent oracle — calibration

## Source support before measurement

The source-backed proposition is narrow: **the schema-v2 live audit has no live `DEGRADED` outcome**. `tools/boot-chain-audit.sh` documents exits `0 CONSISTENT | 1 DEGRADED | 2 UNKNOWN`, then explicitly qualifies that no v2 verdict maps to `DEGRADED` and live exit 1 is never emitted (`:81–85`). Its live summary returns `2` when any input is unknown, no entries exist, or no kernel entry is evaluable; otherwise it returns `0` (`:794–806`). The separate selftest returns `0` on success and `1` on failed assertions (`:1216–1221`), and `main` dispatches `--selftest` separately from `--live` (`:1226–1266`). These rules support C3's semantic distinction: live `1 DEGRADED` is false; a selftest-only `1` is not a live verdict. They do **not** claim host readiness or boot safety.

Baseline provenance for this source is recorded as `tools/boot-chain-audit.sh` at `0cbc34dd6b20896085a8fb07943e3ea4027d8472` in `corpus/SOURCES.md:86`; this is also the preregistered baseline. The baseline registry checker selects the unique highest exact registry heading and rejects a duplicate highest heading (`tools/check-registry-coverage.py:133–145`); its generic checks only check code-token presence for probe maps (`:219–236`). Its baseline CLI has no `--audit-live-map` option (`:281–292`), so the source does not itself establish that new mode's finding ID, metric, or exit behavior.

**Support verdict:** C3's live-versus-selftest semantic expectation is source-supported. The exact checker contract (`REGISTRY-AUDIT-LIVE-MAP`, `audit_live_map_errors`, and its exit codes/counts) is specified by `preregister.expected.C3`, not independently derivable from the baseline checker source. It remains an oracle expectation for the unchanged evaluator, not a result observed here.

## Fixed input classes and expected outcomes

Use a structurally valid fixture with one unique highest complete `Gate and probe registry` table and one otherwise generic-coverage-clean `boot-chain-audit` row. Keep the command path `tools/boot-chain-audit.sh`, probe kind, and required `0`/`2` entries valid so unrelated registry findings cannot mask the C3 result. Use a distinct lower-numbered table only in the historical-row control. In every case bind the input revision once; let `H` denote that fixture's full resolved commit SHA returned by `bind()`. The checker emits the bound revision and branch tip (`check-registry-coverage.py:272–278, 312–331`); require `revision == H` (and the bound branch/tip), never substitute an unbound ref or a different revision. The source-pinned baseline SHA is `0cbc34dd6b20896085a8fb07943e3ea4027d8472`; no candidate or mutated-fixture commit SHA is asserted here.

| Fixed class | Only relevant operative-row distinction | Expected C3 result |
|---|---|---|
| `legacy_live_1` (red) | Highest row advertises live `0 CONSISTENT; 1 DEGRADED; 2 UNKNOWN`. | Exactly one C3 error: `REGISTRY-AUDIT-LIVE-MAP`; `audit_live_map_errors=1`; exit `1`. Output must remain bound to `H`. |
| `corrected_live_map` (green) | Highest row advertises live `0 CONSISTENT (observation); 2 UNKNOWN (could-not-evaluate)`; no live `1`. | `audit_live_map_errors=0`; exit `0`; no C3 finding. Output must remain bound to `H`. |
| `selftest1_only` (admit control) | Same corrected live map; code `1` is shown only as selftest failure, separately from the live map. | Allowed: `audit_live_map_errors=0`; exit `0`; do not classify it as live `DEGRADED`. Output must remain bound to `H`. |
| `historical_row_only_fix` (red control) | Lower historical row is corrected, but the unique highest row still advertises live `1 DEGRADED`. | Same rejection as `legacy_live_1`: `REGISTRY-AUDIT-LIVE-MAP`; `audit_live_map_errors=1`; exit `1`. Output must remain bound to `H`. |

For the selftest control, preserve the source's distinct selftest map (`0` pass, `1` failed assertions; harness/usage errors may be `2`), rather than relocating that `1` into the live map. For the historical control, only the selected highest row can establish the operative contract: a lower table correction cannot change that row. The preregistered C3 expected values are the source for these exact checker IDs/counts/exits; this review did not execute or inspect measurement outputs.

## Causal before → after criterion

The sole causal change is the **highest operative row's live map**: remove live `1 DEGRADED`, preserving live `0 CONSISTENT` and `2 UNKNOWN/could-not-evaluate`. Keep selftest `1` in its separate selftest field. Against the same semantic fixture and unchanged evaluator, this changes the one C3 error from `1` to `0`, removes `REGISTRY-AUDIT-LIVE-MAP`, and changes exit `1` to `0`. A historical-row-only edit must leave the highest-row failure unchanged. This tests calibration of the documented map to the baseline audit source; it is not a live invocation, host probe, or safety certificate.

## Scope and limitations

Reviewed only the C3 preregistration expectation and baseline registry/audit source; C1/C2 were not assessed. No candidate worktree source or measurement result was used. A broad read-only search surfaced round-20 build-document snippets; they were excluded as evidence. No execution or mutation was performed.

Scope: executed=none
