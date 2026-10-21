# DebtExecBinder — round20 build seat ExecBinder missing report

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-ExecBinder

Reviewed snapshot: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (baseline source `corpus/lessons/round-20.md`). The SHA256 above is the digest supplied with this item; NO-EXEC means I did not recompute it.

## Axes

- Identity: which seat, role, agent ID and assignment.
- Absence: whether a report exists and how gates recorded it.
- Death evidence: what provider-death record exists and how strong it is.
- Disposition: an append-only round21 sentence that neither repairs nor replaces anything.
- Prevention: a finite test that would have caught the gap.

## Observations

1. Identity and role. In `.ufo/waves/round-20/build/swarm-registry.json`, lines 8–12 list member `ExecBinder` as `kind: spawn`, `agentId: TsukuroiR19Recovery.ExecBinder-2`, `role: executor`, `item: null`. The registry was created at `2026-10-21T08:18:06.158Z` and updated at `09:23:13.585Z`. In `dispatch.json`, lines 26–31 show the same member with `agentId: null`.
2. Assignment. `spec.json` lines 8–10 and `dispatch.json` lines 424–426 give ExecBinder this assignment:
   - It was the only round20 binder executor.
   - It was EXEC-AUTHORIZED, but only for read-only `git -C <assigned-worktree> show|diff|rev-parse`.
   - Its worktree was `/tmp/tsukuroi-r20-binder-20261021` at base `0cbc34dd6b20896085a8fb07943e3ea4027d8472`.
   - It could edit ONLY `tools/_revision.py` and `tools/check-revision-binding.py`.
   - The task was the object-ID-first hex disambiguation work plus a judge `--object-selectors` mode (`object_selector_tools` 0→9).
   - Lane bounds were "no subagent dispatch except your single labrat".
   - Report target: `.ufo/waves/round-20/build/ExecBinder.md`.

   `seeded-implementation.json` line 6 also records that L1 pre-seeded `tools/_revision.py` with an object-ID-prefix lookup. It says "selftests and independent judge still assigned to ExecBinder".
3. The report is absent. A glob for `**/*ExecBinder*` under `.ufo/waves` finds no file, so `.ufo/waves/round-20/build/ExecBinder.md` does not exist. Each of `measure/final-r20`, `measure/final-r20b` and `measure/final-r20c` contains a `seat-scope-build.stdout` with `{"detail": "seat report absent", "id": "SCOPE-REPORT-MISSING", "role": "executor", "site": "ExecBinder.md"}`. The final-r20c run (revision `fc2a0085…`) reports `SCOPE-REPORT-MISSING: 13`, `status: FAIL` and `evidence_class: self-reported declarations; no independent absence-of-execution proof`. In `tools/check-seat-scope.py`, lines 70–73 emit this finding only because `reports.get(name)` is `None`.
4. Launch attempts. `native-task-result.json` (attempt 1) shows `TsukuroiR20.ExecBinder: Background job limit reached (100)`. `native-task-result-retry-2.json` records `status: refused-before-spawn`, `spawned: 0`. Both are pre-spawn refusals, not deaths. No result file for the third, successful call is retained in `round-20/build`.
5. The available provider-death record is `LOG.md:1039`: "Thirteen provider-rate-limit deaths (ExecBinder, ExecRegistry, … RevSelectorMechanism); no replacement." It is restated in `LOG.md:1046` ("13 known rate-limit exits plus parked `BindTagObject`"). The snapshot repeats it at `round-20.md:41` (R20-SEAT-DEBT), `:51` ("no dead seat is ever replaced") and `:63` ("build reports13 provider-rate-limit deaths as missing … neither is silently repaired or treated as proof that commands ran").
6. There is no per-seat death artifact for round20. A glob for `**/death*` under `.ufo` returns only `round-21/build/death-ScribeDecision.json`, which shows the round21 shape: agent, `status`, verbatim `observed_error`, `replacement: false`. No round20 file carries ExecBinder's exit status or provider error text.

## Inferences

- [INFERENCE] The cause "provider rate limit" for ExecBinder is an aggregate L1 log assertion. I found no retained per-seat observed error, so the cause is recorded but not independently evidenced here.
- [INFERENCE] The registry agent ID uses the `TsukuroiR19Recovery.…-2` namespace, while attempt 1 named `TsukuroiR20.ExecBinder`. Which identity actually spawned can only be settled from a transcript I did not read. The registry value is the binding one; nothing is renamed.
- The seat was EXEC-AUTHORIZED and allowed a labrat. Because no report exists, both of these are unknown: whether it ran any git command or spawned a labrat, and whether it edited the worktree before dying. A missing report proves neither that commands ran nor that none ran.
- Later binder work (R20-BIND-TARGET-TYPE, R20-C2-ORACLE, judge 62/62, `_revision` 57/57 at `round-20.md:46–47,63`) is not attributable to ExecBinder from this evidence.

## Round21 append-only debt disposition

R21 debt disposition (ExecBinder): the round20 build executor seat ExecBinder, registered as `TsukuroiR19Recovery.ExecBinder-2` and assigned EXEC-AUTHORIZED read-only git plus edits to `tools/_revision.py` and `tools/check-revision-binding.py` in `/tmp/tsukuroi-r20-binder-20261021`, delivered no `.ufo/waves/round-20/build/ExecBinder.md`. Its only death evidence is the aggregate L1 `LOG.md:1039` provider-rate-limit entry, with no retained per-seat error. Its `SCOPE-REPORT-MISSING` therefore stays red, the seat stays dead and unreplaced, and whether it executed commands, edited files or spawned a labrat stays unknown.

## Prevention test (proposal only; not implemented or run)

This is a finite `check-seat-scope.py`-style fixture. For each registry seat whose `<Name>.md` is missing, the test requires a sibling `death-<Name>.json`. That record must have:

- `agent` equal to the registry `agentId`;
- a non-empty verbatim `observed_error`;
- a `status`;
- `replacement: false`.

The record never clears `SCOPE-REPORT-MISSING`, and it never implies `executed=none`. Expected results:

| Fixture | Expected exit | Expected findings |
|---|---|---|
| Report absent and no death record | 1 | `SCOPE-REPORT-MISSING` plus a new `SCOPE-DEATH-UNRECORDED` |
| Report absent with a valid death record | 1 | `SCOPE-REPORT-MISSING` only (still red) |
| Death `agent` ≠ registry `agentId` (e.g. `TsukuroiR20.ExecBinder` vs `TsukuroiR19Recovery.ExecBinder-2`) | 1 | `SCOPE-DEATH-INVALID` |
| `replacement: true`, or a report present alongside a death record | 1 | `SCOPE-DEATH-INVALID` |
| Malformed death JSON | 2 | — |

## Limits

- I read only these sources:
  - the round-20 build registry, spec, dispatch and native-task results;
  - `seeded-implementation.json`;
  - the measure `seat-scope-build.stdout` files;
  - `LOG.md`;
  - `tools/check-seat-scope.py` lines 1–100;
  - the round-21 `death-ScribeDecision.json` and `reviews.json` entries.
- I did not read agent transcripts or inspect the `/tmp` worktree (no host probes), and I made no production edits.
- I reviewed one seat only. This is not a non-author closure or outside promotion.

Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
