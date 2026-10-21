# DebtExecAdjacency — round20 build missing seat ExecAdjacency

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-ExecAdjacency

Reviewed snapshot: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (digest as supplied by the item; not recomputed under NO-EXEC).

## Axes

- Identity: which seat, role, and agent ID the round20 records bind.
- Assignment: what the seat was told to do and where it was told to report.
- Absence: whether the report exists, and who records it as missing.
- Death record: what provider-death evidence exists, and how detailed it is.
- Disposition: an append-only round21 sentence plus a test that prevents recurrence.

## Observations (with file and line)

1. Identity. `.ufo/waves/round-20/build/swarm-registry.json:20-25` records the member `ExecAdjacency` with `kind: spawn`, `agentId: TsukuroiR19Recovery.ExecAdjacency-2`, `role: executor`, `item: null`. In the pre-spawn copy, `dispatch.json:38-43`, the same member has `agentId: null`. The spec, `spec.json:18-20`, names it `ExecAdjacency` with role `executor`.
2. Assignment. `dispatch.json:434-436` (task text; same wording in `plan.json:439-441` and `spec.json:20`) says:
   - EXEC-AUTHORIZED, but only read-only `git -C <assigned-worktree> show|diff|rev-parse`.
   - Target is the external worktree `/tmp/tsukuroi-r20-adjacency-20261021` (bound in `worktree-bindings.json:6`), file `tools/check-adjacency-anchors.py` only.
   - Add the finite C1 mode `--ownership-corrections`, with the findings `OWNERSHIP-CORRECTION-MISSING` and `OWNERSHIP-CORRECTION-INVALID` and the counter `ownership_corrections` going 0→1.
   - "NEVER run tests. No docs edits."
   - Trailer: `Report: write your scoped findings to .ufo/waves/round-20/build/ExecAdjacency.md`.
   - `seeded-implementation.json:10` adds: "ExecAdjacency owns new finite C1 mode in its own external worktree". In other words, this seat had no L1 seed, unlike the other three executors.
3. Report absence.
   - A glob for `Exec*` in `.ufo/waves/round-20/build/` returns only ExecMutating, ExecOptions, ExecReadOnly, ExecShell, ExecUnknown and ExecWrappers. `ExecAdjacency.md` is absent.
   - `measure/final-r20c/seat-scope-build.stdout` (at revision `fc2a0085088cedb3ab59dc3fff16523c0f42a6b4`) lists `{"id": "SCOPE-REPORT-MISSING", "role": "executor", "site": "ExecAdjacency.md", "detail": "seat report absent"}`. That file counts 13 missing reports, 0 unauthorized and 0 undeclared, and says its evidence class is "self-reported declarations; no independent absence-of-execution proof".
   - The same finding appears in `final-r20/` and `final-r20b/seat-scope-build.stdout`.
4. Provider-death record.
   - The only seat-specific death record is `LOG.md:1039`: "Thirteen provider-rate-limit deaths (ExecBinder, ExecRegistry, ExecAdjacency, ExecSystemctl, …); no replacement."
   - It is backed up by `SCORECARD.md:628` and the reviewed snapshot at lines 41 and 63 (R20-SEAT-DEBT: "13 build reports missing from provider-rate-limit deaths … Do not rewrite trailers, replace dead seats or infer actual execution absence").
   - `build/native-task-result.json` and `native-task-result-retry-2.json` record two refusals before any seat spawned ("Background job limit reached (100)"; `spawned: 0`). These refusals are not the death. The death came after the third call, which `LOG.md:1039` says spawned all 64 seats.
   - No raw provider error payload, timestamp or transcript for `TsukuroiR19Recovery.ExecAdjacency-2` is retained under `.ufo/waves/round-20/`. A glob for `*ExecAdjacency*` under `~/.omp` also found nothing.

## Inferences (not verified)

- The C1 candidate code exists anyway. `ConnPlanner.md:54-58` inspected `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:123-178`, and the final measurement records C1 0→1. Who wrote that code is not recorded in these files, so this report does not credit it to the dead seat.
- The registry agent ID namespace is `TsukuroiR19Recovery.*-2`, while the failed calls in native-task-result use `TsukuroiR20.*`. The dying identity is therefore the registry ID, not any `TsukuroiR20.ExecAdjacency` job.

## Limits

- The rate-limit cause is stated only by the L1 author in LOG and SCORECARD. There is no provider-side receipt.
- The missing report means there is no seat self-declaration at all. It does not show that the seat ran commands, and it does not show that the seat ran none.
- The snapshot digest was not recomputed. I checked only that lines 41 and 63 match `corpus/lessons/round-20.md` textually.
- Transcripts at `history://` were not read: the NO-EXEC leaf has no access to them.

## Round21 debt disposition (append-only sentence)

Round20 build seat `ExecAdjacency` (role executor, agentId `TsukuroiR19Recovery.ExecAdjacency-2`, assigned report `.ufo/waves/round-20/build/ExecAdjacency.md`) remains a retained `SCOPE-REPORT-MISSING` red: it is attributed only to the L1-recorded provider-rate-limit death in `LOG.md:1039`, with no retained provider payload; the seat is not replaced, no report is synthesized, and the absence neither proves nor disproves command execution or authorship of the C1 `--ownership-corrections` code in `/tmp/tsukuroi-r20-adjacency-20261021`.

## Prevention test

When a wave's `seat-scope` finds `SCOPE-REPORT-MISSING` for a member with `kind: spawn` and a non-null `agentId`, it must also require a per-seat death receipt stored in the wave directory. The receipt needs the agent ID, the provider error class or text, a timestamp and `replacement: none`. Without one, the gate emits a distinct finding such as `SCOPE-DEATH-UNRECORDED`, and a LOG-only aggregate sentence does not satisfy it.

Selftest fixtures for this check:
- (a) Missing report plus a matching receipt: the existing MISSING finding only.
- (b) Missing report with no receipt: MISSING plus DEATH-UNRECORDED.
- (c) A receipt for a seat whose report exists: rejected as contradictory.
- (d) A receipt whose agent ID differs from the registry: rejected.

Executor seats with external worktrees also need the receipt to say "code authorship unattributed". This stops measured candidate code from being credited to a dead seat.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none
