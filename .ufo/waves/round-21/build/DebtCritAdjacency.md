# DebtCritAdjacency — round20 build missing seat CritAdjacency

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-CritAdjacency

Reviewed bytes: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (baseline source `corpus/lessons/round-20.md`). The digest above is the item-supplied pin; under NO-EXEC it was not recomputed by this seat.

Axes: identity (seat name/role/agent ID binding), assignment (what the seat was asked to do), report presence, death evidence quality, disposition honesty.

## Observations

1. **Seat identity (registry).** `.ufo/waves/round-20/build/swarm-registry.json:296-301`: member `CritAdjacency`, `kind: spawn`, `agentId: "TsukuroiR19Recovery.CritAdjacency-2"`, `role: "critic"`, `item: null`. Registry has no status/death field for any member (wave `tsukuroi-r20-build`, updatedAt `2026-10-21T09:23:13.585Z`).
2. **Dispatch.** `build/dispatch.json:314-319` lists `CritAdjacency` with `agentId: null`, role critic; `spec.json:247-250` and `plan.json:669-671` give the same seat.
3. **Assignment (spec.json:250).** NO-EXEC critic: "Falsify C1 claim meaningful causal improvement vs publishing a magic string; finite semantic check/source binding. Read prereg and baseline routed spotcheck. Return concrete counterexample and admission requirement". Report target `.ufo/waves/round-20/build/CritAdjacency.md` (dispatch.json:664-666).
4. **Report absence.** No `Crit*` file exists anywhere under `.ufo/waves/round-20`. All three seat-scope captures list `SCOPE-REPORT-MISSING`, role `critic`, site `CritAdjacency.md`, "seat report absent" (`measure/final-r20{,b,c}/seat-scope-build.stdout`). In final-r20c the counts are `SCOPE-REPORT-MISSING: 13`, `seat_count: 64`, and `status: FAIL`.
5. **Launch history.** `build/native-task-result.json` shows that attempt 1 refused `TsukuroiR20.CritAdjacency` with "Background job limit reached (100)". `build/native-task-result-retry-2.json` shows that attempt 2 was `refused-before-spawn` with `spawned: 0`. No attempt-3 result file is retained. The only evidence for attempt 3 is LOG.md:1039, which says "the third unchanged call spawned all64".
6. **Provider-death record.** The only death evidence that names this seat is narrative: LOG.md:1039 says "Thirteen provider-rate-limit deaths (… CritAdjacency …); no replacement". The same claim is repeated at LOG.md:1047/1063, SCORECARD.md:628 and lesson round-20.md:41/63. No per-seat death artifact exists for round 20. Missing items:
   - observed provider error text;
   - model;
   - timestamp;
   - exit status.

   A grep for `R19Recovery.CritAdjacency` or `CritAdjacency` under `~/.omp` found nothing. By contrast, round 21 retains a per-seat record format (`round-21/build/death-ScribeDecision.json`) with agent, status, observed_error and `replacement: false`.

## Inferences / gaps

- [INFERENCE] The seat was spawned once, as `TsukuroiR19Recovery.CritAdjacency-2`, on the third call. Its death cause, "provider rate limit", rests only on the author's LOG narrative. No retained error string for round 20 corroborates it.
- Unresolved: the registry uses the agent prefix `TsukuroiR19Recovery.*-2`, while the refused attempts used `TsukuroiR20.*`. No artifact explains this namespace difference.
- The missing report is not evidence that the seat ran no commands, and it is not evidence that it ran any. Its C1 magic-string attack is **unexecuted**. It is not a pass and not a refutation of C1.
- Nothing was replaced or fabricated, and that is correct: no `CritAdjacency.md` exists, and the dispatch common text says "Dead seats stay dead, no replacements."

## Append-only round21 debt-disposition sentence

> Round20 build critic CritAdjacency (registry agentId `TsukuroiR19Recovery.CritAdjacency-2`, assigned the C1 magic-string falsification) delivered no report. Its death is attested only by the LOG.md:1039 provider-rate-limit narrative, with no retained per-seat error record. The SCOPE-REPORT-MISSING red stays permanent, its C1 attack stays unexecuted rather than passed, and no report, replacement identity or command-absence claim is made.

## Prevention test (fail-capable)

Add a reconciliation check over `swarm-registry.json` + `spec.json` (e.g. alongside `tools/check-seat-scope.py`). For every seat without `<Name>.md`, require a sibling `death-<Name>.json` whose `agent` equals that member's registry `agentId` exactly and which has a non-empty `observed_error` and `replacement: false`. Hermetic fixtures:

1. Missing report and no death record. Expected: fail, unreconciled.
2. Missing report with a matching death record. Expected: still `SCOPE-REPORT-MISSING`, which is non-clean, but reconciled as dead-observed.
3. A death record whose `agent` is a different namespace (`TsukuroiR20.X` vs registry `…Recovery.X-2`). Expected: fail.
4. A death record with an empty `observed_error`, or with a narrative-only source. Expected: fail.
5. A placeholder `<Name>.md` written by a non-seat. Expected: it must not clear the death or the missing-report red.

This prevents future waves from repeating the gap. It does not apply retroactively and cannot clear round20.

## Limits

This is a read-only review limited to the CritAdjacency seat. I did not check transcripts or `history://` because they are not reachable with read/grep. I did not recompute the hash. I installed no tools, and none were needed. This is not non-author closure.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none
