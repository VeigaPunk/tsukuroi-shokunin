# FxRefusalShape

Axes: one-finding refusal shape; fatal-Git classification; JSON `revision`/`branch_tip`.

## Findings

- **Medium — FAILS: fatal Git errors are misclassified in the independent judge.** `tools/check-revision-binding.py:127-128` treats every nonzero `rev-parse` as “absent”; `:131-135` maps every nonzero commit parse to `E-REVISION-INVALID`; and `:149-157` maps any failed `check-ref-format` command to `E-BRANCH-INVALID` or `E-BRANCH-MISSING`. Only `ancestor()` distinguishes ordinary rc=1 from fatal rc>=2 (`:138-144`). Those paths still emit one finding, but not `E-GIT-FAILED` as required by `tools/_revision.py:23-24`. The origin-blob probe tests only the `merge-base` fatal path (`:399-405`).

- **Medium — FAILS: refusal `branch_tip` can be false and is not graded.** The helper describes the tip as informational and returns `None` when unavailable (`tools/_revision.py:126-132`). With a valid branch and unlanded/unpushed revision, `check-boot-chain.py:1531-1544` leaves it null; `check-appended-notices.py:475,499-502` likewise emits null because `binding` was never assigned. `check-section-citations.py:911-927`, `check-source-scope-correction.py:634-649`, and `check-seat-scope.py:633-647` also leave it unset on binding refusal. In contrast, `check-recheck-commands.py:1263-1264` explicitly expects the local tip on an unlanded refusal. The C2 judge checks only canonical `revision` on accepted output (`check-revision-binding.py:348-356`) and refusal count/ID (`:411-416`); it cannot catch these wrong fields. Refusal `revision` semantics are also unasserted.

- **SURVIVES — one-finding shape, statically:** shared binding raises one `RevisionError`; consumer adapters shown above produce one-element finding lists. C2’s `strict-refusals` requires exactly one finding and exactly one expected binding ID for its enumerated refusal probes (`check-revision-binding.py:367-416`). This is source evidence, not a runtime result for 68a8ae0.

## Existing evidence and gaps

`RerunHarness-selftest.txt:1-3` records 40/40, exit 0; `MutateShared.md:9-24` records restored 37/37. Their provenance is the prerequisite 51dd9ee, not integrated target 68a8ae0 (`RerunHarness.md:4-5`, `MutateShared.md:5`); no reviewer runs were made. `xd://lsp` is unavailable (“No such tool”); read/grep was literal fallback, not semantic proof. Target runtime outputs remain unverified.

Scope: executed=none