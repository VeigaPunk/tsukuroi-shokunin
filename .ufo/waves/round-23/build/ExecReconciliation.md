# ExecReconciliation — round23 attempt1 report (C3)

Seat: `TsukuroiR23-2.ExecReconciliation-7` · leaf executor · branch `round23/ExecReconciliation` · baseline `ae01e50f582016384e620022be38bf5367000e2e` · scope `executed=none`.

## Deliverable

- `../../worktrees/ExecReconciliation/draft/check-path-reconciliation.py` — complete standard-library-only Python draft (676 lines), intended for `tools/` placement after L1 integration. Not executed, imported, compiled, linted or formatted here, per NO-EXEC.

## What the draft implements

1. **Rough classifier, reimplemented literally** from `../../sources/r22-rough-census.txt` (never executed): `ROUGH_STRIP` is the exact `strip_sel` regex; components split on `;` for grep/glob; one path failure per event (`rough_path_failures` is 0/1, `rough_first_bad` records the first failing value). Exec/unknown cohorts counted as classes, never as path.
2. **Canonical classifier (old-v1 literal authority, independently authored)**: exact read/write membership after stripping valid selector tokens. `CANON_TOKEN` accepts `raw` and the digit/range family `\d[\d\-+,:]*` / `-\d+` / `\d+-` repeatable in **any order** at the tail — so `:raw:N-M` (raw-first) and `:N-M:raw` (range-first) are both valid. Skill URIs are literal members; a `component_rejected` guard denies empty, dot-segment and control-character spellings outright. Per-component indices and counts are recorded (`canonical_bad_indices`, `canonical_path_failures`).
3. **`derive(wave, events, bindings, audit)`** — reproducible per-wave ledger: one row per event (including non-path), each with seat, 0-based index, tool, raw identity digest (SHA-256 over a canonical JSON array of wave/seat/index/tool/raw path), rough class/first-bad/count, canonical bad indices/count, retained site count, and bounded disposition: `non-path`, `agreement`, `selector-normalization`, `unit-difference`. Exposed for L1 to construct the record later.
4. **Gate**: `evaluate()` hashes **all** frozen input bytes first; any digest mismatch → exit 2 `SNAPSHOT-TAMPERED` (read failure → `SNAPSHOT-READ-FAILED`). Strict duplicate-key parsing everywhere (`unique_object`), schema checks for frozen manifest/events/bindings (the audits carry no schema field and are shape-checked), roster identity across events/bindings/audit. Missing record → exit 1, `unexplained_cohorts=2`, `RECONCILIATION-MISSING`. Otherwise it recomputes both ledgers, requires exact equality with `.ufo/waves/round-23/path-reconciliation.json`, validates per-lane arithmetic and dispositions, and reaches `unexplained_cohorts=0`/exit 0 only when both full ledgers validate. CLI: `--revision HEX` / `--branch master` (via the shared `tools/_revision.py` binding, `sys.dont_write_bytecode=True` before import) / `--selftest`.
5. **Selftest (literal, unrun)**: 12 in-memory cases with hand-derived exits and finding IDs — clean PASS(0); missing record 1/`RECONCILIATION-MISSING`/2; retained-digest manifest tamper 2/`SNAPSHOT-TAMPERED`; dropped row, duplicate row, wrong disposition, unknown disposition (1, `RECONCILIATION-MISMATCH`+`RECONCILIATION-ARITHMETIC`, cohort unexplained); wrong arithmetic/wrong unexplained (1, `RECONCILIATION-ARITHMETIC`); malformed record and duplicate JSON key (2, `RECONCILIATION-SCHEMA`); roster mismatch (2, `SNAPSHOT-SCHEMA`); stale manifest digests (2, `SNAPSHOT-TAMPERED`). Fixture controls: mixed `:raw:2-4` vs `:2-4:raw` order, one-per-event (`rough_first_bad`, break) versus per-component (canonical count 2 against one rough failure and one retained site).

## Reconciliation facts retained (from the frozen bytes; no recomputation executed)

- Rough source counts are given: build 25, falsify 33 (`rough_as_reported` in `../../frozen/reconciliation-inputs.json`; also `outside_round22.path_counts_as_reported.rough` in `../../preregister.json`).
- Retained lane sites, recounted by hand from the frozen audits: build **23** SCOPE-PATH-DENIED sites, falsify **29** — matching `expected.lane_retained`.
- Audit finding sites are **0-based** event indices (`OracleFetchHTTPS:2` = the `edit` probe, `:3` = read of the write-only report with `:raw`); per-seat `violations` arrays are in site order.
- Every violating seat checked event-by-event (FetchBare, PathDotDot, PathArtifact, WriteOther, WritePrefix, ParallelFetch/Local/Malformed, TraceMissing, ReceiptPeriod/Digest, CohortDuplicate, DebtBash, CritSeparable/NoHarm/Runtime in build; falsify analogues) reconciles under: denied ⇔ path value not an exact binding member after selector stripping; bash→`SCOPE-EXEC-DENIED`, unknown tools→`SCOPE-TOOL-UNKNOWN`, both outside the path cohort.
- **Surplus rough flags are exactly the raw-first selectors**: build has two `round-21.md:raw:58-58` reads (DebtSixReceipts, ReviewReservation — both lane-clean seats) ⇒ 23+2=25; falsify has four `:raw:N-M` reads (`check-boundary-contract.py:raw:15-60/58-102/103-175` in FxC1LocalRead, `_revision.py:raw:172-193`) ⇒ 29+4=33. Rough's `strip_sel` only handles range-then-`raw`, which is why it flags them and the lane did not. This is the classifier difference C3 must explain, and `selector-normalization` is its bounded label.
- Cancellation caution honored: net difference (2+4=6) is not forced to mean 6 unique records; the ledger reports per-event/per-component counts as computed and any `unit-difference` row makes its lane unexplained rather than being absorbed.

## Verification status

- No execution, import, compile, test, lint, format, hash or wc was run (NO-EXEC seat; `commands: []`, `fetches: []`). No installs (tooling directive noted; nothing needed or authorized under this seat's scope).
- Hand-verified: the selftest's expected exits/IDs against the code paths; fixture derivation (rough 4, retained 3, dispositions per row); the full evaluate flow order (hash → schema → roster → derive → record equality → arithmetic). Reads of the frozen inputs were performed with the seat's read tools only.
- Digest `0df78ded55bd88f7f484fefe2744f9d8924bf30132a93ab657e3fcfbcd98eb3c` is the supplied identity of `r22-rough-census.txt`, declared, not independently computed.

## Risks / blockers for L1 integration

- The canonical grammar covers every selector spelling observed in the frozen events; if any unseen spelling appears, `lane_valid` fails closed (exit 1) rather than guessing — the correct behavior, but the record construction must use `derive()` output verbatim.
- The audits were assumed schema-less (verified in both frozen audit files); if L1 expects a `schema` field on audits, `parse_audit` is the place to adjust.
- Real-data equality of canonical-denied events with the 23/29 retained sites is derived from my seat-by-seat reading, not machine-verified here; the gate itself enforces it at integration time.
- No `path-reconciliation.json` exists yet; `derive()` is the intended generator. First integration run should be exit 1 `RECONCILIATION-MISSING`, then 0 after the record lands.
