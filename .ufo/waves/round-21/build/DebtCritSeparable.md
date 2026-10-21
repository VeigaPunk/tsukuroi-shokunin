# DebtCritSeparable — round20 build missing seat CritSeparable

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-CritSeparable

Reviewed object: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (baseline source `corpus/lessons/round-20.md`). The SHA256 above is the dispatch-supplied pin (also in `.ufo/waves/round-21/reviews.json` lines 376–380); under NO-EXEC I did not recompute it.

Axes: (A) seat identity and assignment, (B) report absence, (C) evidence for the cause of death, (D) honesty of the debt accounting.

## Observations

| Axis | Observation | Location |
|---|---|---|
| A | Seat `CritSeparable`, role `critic`, assignment: "Falsify C1/C2/C3 independent production artifacts and evaluators; shared binder does not mask other claim failures. Read prereg and baseline routed spotcheck. Return concrete counterexample and admission requirement, not broad review. No candidate implementation output required." NO-EXEC preamble with the literal `Scope: executed=none` requirement | `.ufo/waves/round-20/build/spec.json` lines 268–270 |
| A | Report target: `.ufo/waves/round-20/build/CritSeparable.md`; leaf, no subagent dispatch | `build/dispatch.json` line 684–686; `build/plan.json` line 689–691 |
| A | Pre-spawn registry copies have `agentId: null` | `build/dispatch.json` lines 338–342; `build/plan.json` line 352–355 |
| A | Spawned identity `TsukuroiR19Recovery.CritSeparable-2`, kind `spawn`, role `critic`, item `null`; registry createdAt `2026-10-21T08:18:06.158Z`, updatedAt `09:23:13.585Z` | `build/swarm-registry.json` lines 3–5, 320–325 |
| B | No `Crit*` file exists anywhere under `.ufo/waves/round-20` (glob returned 0 files) | glob |
| B | All three final seat-scope captures list `{"id":"SCOPE-REPORT-MISSING","role":"critic","site":"CritSeparable.md","detail":"seat report absent"}`. The final capture is at `branch_tip fc2a0085088cedb3ab59dc3fff16523c0f42a6b4`, counts `SCOPE-REPORT-MISSING: 13`, evidence_class "self-reported declarations; no independent absence-of-execution proof" | `measure/final-r20/`, `final-r20b/`, `final-r20c/seat-scope-build.stdout` |
| C | The only per-seat cause statement is in LOG.md line 1039: "Thirteen provider-rate-limit deaths (… CritSeparable …); no replacement." Later restatements at LOG lines 1047 and 1063 ("13 known rate-limit exits") and the snapshot lesson (R20-SEAT-DEBT, §Final measured outcome) do not name the seat individually | `LOG.md`; snapshot lines 41, 64 |
| C | The two retained native task results are pre-spawn refusals, not death records. `native-task-result.json` covers attempt 1, uses `TsukuroiR20.*` names, and reports "Background job limit reached (100)" for every seat, including `TsukuroiR20.CritSeparable`, with `results: []` and `totalDurationMs: 0`. `native-task-result-retry-2.json` covers attempt 2 with `status: refused-before-spawn`, `spawned: 0`, and the same error | `build/native-task-result*.json` |
| C | No result file was retained for attempt 3, the call that actually spawned the seats, and no per-seat exit or provider-error record exists for `TsukuroiR19Recovery.CritSeparable-2` in `.ufo/waves/round-20`. A read-only search of `/home/vgpnk/.omp` for that agentId found nothing | grep |

## Inferences

- [INFERENCE] `TsukuroiR19Recovery` is the namespace of the parent session that dispatched round 20: all 64 registry members carry it with a `-2` suffix. It is not a round19 seat, so it is not an identity mismatch specific to this seat.
- [INFERENCE] The job-limit refusals happened before spawn and name a different cause, so they cannot serve as the CritSeparable death record. Calling them that would mislabel the cause.
- Axis D: the claim that CritSeparable died from a provider rate limit is an L1 attestation in LOG, not a retained provider record. Report absence is evidenced; the cause of death is attested only. The lesson's wording "13 build reports missing from provider-rate-limit deaths" is therefore stronger than the retained artifacts support for this seat.
- The separability falsification assigned to this seat was not performed in the build wave. Whether another seat covered it is outside this scope and is not claimed.

## Limits

- The `.omp` search may be limited by ignore rules or by where transcripts are stored. `history://` cannot be read with this seat's tools, so an unretained transcript may exist.
- Absence of a report proves nothing about which commands the seat ran or did not run.
- I wrote no report for the dead seat, replaced no identity, and edited no round20 artifact.

## Append-only round21 debt-disposition sentence

Round21 disposition (CritSeparable): the round20 build critic seat `CritSeparable` (agentId `TsukuroiR19Recovery.CritSeparable-2`, assigned to falsify the C1/C2/C3 independent production artifacts and evaluators so the shared binder cannot mask other claim failures) delivered no report. `.ufo/waves/round-20/build/CritSeparable.md` is absent, and the final-r20c seat-scope check at `fc2a0085088cedb3ab59dc3fff16523c0f42a6b4` retains SCOPE-REPORT-MISSING. Its provider-rate-limit cause is attested only by the LOG round20 dispatch entry; no per-seat provider-death record was retained, and the two retained native-task-result files are pre-spawn job-limit refusals, not that record. The red stays red, the seat is not replaced, no report is reconstructed, its separability falsification is recorded as unperformed, and the missing report is not evidence about whether any commands ran.

## Prevention test (proposal; L1 owns implementation)

Add a wave-close death-record check, for example as hermetic fixtures in `tools/check-seat-scope.py --selftest`, next to the existing SCOPE-REPORT-MISSING path at lines 69–73. Expected results:

1. A registry member with a non-null agentId, no report, and no retained per-seat death record (agentId, UTC timestamp, verbatim provider error) must produce a new red ID (for example `SCOPE-DEATH-UNRECORDED`) and exit 1.
2. The same member with a matching death record still produces SCOPE-REPORT-MISSING, now classed as dead-recorded. The record must never clear the missing-report red.
3. A record that is a pre-spawn refusal (`spawned: 0` or `results: []`), or whose agentId differs from the registry entry (for example `TsukuroiR20.CritSeparable` vs `TsukuroiR19Recovery.CritSeparable-2`), must still produce `SCOPE-DEATH-UNRECORDED`.
4. A cause class written in LOG prose without a matching record must not satisfy the check.

Lane bounds: leaf member — no subagent dispatch.
Tooling: none installed or needed (NO-EXEC; pacman paused).

Scope: executed=none
