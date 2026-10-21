# DebtCritOperability — round20 build missing seat CritOperability

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-CritOperability

Reviewed snapshot: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (baseline source `corpus/lessons/round-20.md`). The digest line above is the one given in the item and in `.ufo/waves/round-21/reviews.json:355-359`. This seat could not hash the file itself under NO-EXEC; the cited lines below were read from the snapshot.

Axes: role/assignment identity, report presence, death-record provenance, and disposition honesty (no replacement, no inferred execution absence).

## Observations

1. **Role and assignment.** `.ufo/waves/round-20/build/spec.json:253-255` declares item `CritOperability` with role `critic` and a NO-EXEC prompt. The prompt says: "Falsify C2 object-only selection not arbitrary shell security or universality; original9 continuity and discovered tools separated." `dispatch.json:669-671` repeats it with agent `critic` and trailer `Report: write your scoped findings to .ufo/waves/round-20/build/CritOperability.md`.
2. **Identity.** `swarm-registry.json:302-307` records `kind: spawn`, `agentId: TsukuroiR19Recovery.CritOperability-2`, `role: critic` and `item: null`. The pre-spawn records `dispatch.json:320-324` and `plan.json:334-338` still have `agentId: null`.
3. **Report absence.** There is no `CritOperability.md` anywhere under `.ufo/waves/round-20` (glob `Crit*` returned 0 files). All three final seat-scope captures list it: `measure/final-r20{,b,c}/seat-scope-build.stdout` each contain `{"detail": "seat report absent", "id": "SCOPE-REPORT-MISSING", "role": "critic", "site": "CritOperability.md"}`. The final-r20c capture is pinned to `fc2a0085088cedb3ab59dc3fff16523c0f42a6b4` with `SCOPE-REPORT-MISSING: 13` and `evidence_class: "self-reported declarations; no independent absence-of-execution proof"`.
4. **Death record.** The only available record is aggregate. `LOG.md:1039` lists CritOperability among "Thirteen provider-rate-limit deaths (...); no replacement." Lesson snapshot lines 41 and 63 repeat the count of 13 without naming seats. Round20 has no per-seat death file with error text: glob `**/*death*` under `.ufo/waves` finds only `round-21/build/death-ScribeDecision.json`. No transcript for `TsukuroiR19Recovery.CritOperability-2` was found under `~/.omp`.
5. **Spawn-refusal records are not the death.** `native-task-result.json` (attempt 1) shows `TsukuroiR20.CritOperability: Background job limit reached (100)`, refused before spawn. `native-task-result-retry-2.json` shows `spawned: 0` and `status: refused-before-spawn`. `LOG.md:1039` says the third unchanged call spawned all 64 seats, but no result file for that third call is retained. These are job-limit refusals, not provider-rate-limit deaths.

## Inferences

- [INFERENCE] The death happened after the third-call spawn under the registry identity `TsukuroiR19Recovery.CritOperability-2`. Its provider, model and error text are unrecorded, so the "provider-rate-limit" label rests only on L1's LOG assertion. Attempt 1 used a different prefix (`TsukuroiR20.` versus `TsukuroiR19Recovery.`); that drift is observed but its cause is not explained by any retained record.
- [INFERENCE] The C2 falsification this seat was asked for was never delivered. Its subject is the narrowness of the C2 consumer matrix and the separation of the original nine tools from discovered tools. That subject overlaps the round20 limit R20-BIND-TARGET-TYPE (snapshot line 46) and round21's new C2 target-type matrix, but no other round20 build report is attributed as its substitute.

## Limits

The missing report proves nothing about whether any command ran. The seat-scope gate grades declarations only. This report does not create a CritOperability report, does not reassign or replace the dead identity, does not clear `SCOPE-REPORT-MISSING`, and does not claim non-author closure.

## Append-only round21 debt-disposition sentence

Round21 disposition (append-only): round20 build seat `CritOperability` (role critic, registry agentId `TsukuroiR19Recovery.CritOperability-2`, assigned report `.ufo/waves/round-20/build/CritOperability.md`) produced no report. Its only retained death evidence is the aggregate `LOG.md` round20 dispatch entry naming it among thirteen provider-rate-limit deaths, with no per-seat error record. The `SCOPE-REPORT-MISSING` red stays red, the seat is not replaced, its C2 falsification remains undelivered, and the absence of a report is not evidence of whether any command ran.

## Prevention test

The round21 practice `death-<Name>.json` with `name`, `agent`, `status`, `observed_error` and `replacement` (see `round-21/build/death-ScribeDecision.json`) should become a gate-checked requirement in `tools/check-seat-scope.py` or the wave-close check. Each seat with `SCOPE-REPORT-MISSING` must have a lane-retained per-seat death record whose `agent` equals the registry `agentId`, whose `observed_error` is non-empty and whose `replacement` is `false`. Hermetic selftest fixtures for registry seat `CritOperability`, role critic:

- No report and no death record: FAIL with `SCOPE-REPORT-MISSING` plus a new `SCOPE-DEATH-UNRECORDED`.
- No report and a matching death record: FAIL with `SCOPE-REPORT-MISSING` only. The death record never clears the missing red.
- Death record with a different agent (for example `TsukuroiR20.CritOperability`), empty error, or `replacement: true`: FAIL with `SCOPE-DEATH-INVALID`.
- Death record present together with a report that says `Scope: executed=none`: the report is graded normally, and the death record is never read as an execution-absence proof.
- Spawn-refusal results (`refused-before-spawn`, `spawned: 0`) do not count as death records.

Tooling: no installs or updates; none needed.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none
