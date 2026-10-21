# DebtCritCalibration — round20 build missing seat CritCalibration

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-CritCalibration
Lane bounds: leaf member — no subagent dispatch.

Reviewed bytes: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (pinned digest above, as given by item and `.ufo/waves/round-21/reviews.json` lines 362–366; digest not recomputed under NO-EXEC). Historical round20 evidence read-only.

## Axes

- A1 identity: exact role, assignment, agent id and report path of the seat.
- A2 absence: whether the report exists and how gates classify it.
- A3 death provenance: what record of provider death exists, and at what granularity.
- A4 non-inference: what the absence does and does not prove.

## Observations

1. A1 role/assignment. `.ufo/waves/round-20/build/spec.json` line 258–260: `"name": "CritCalibration"`, `"role": "critic"`, prompt "Falsify C3 false-erratum correction vs history rewrite and exact live/selftest map. Read prereg and baseline routed spotcheck. Return concrete counterexample and admission requirement, not broad review." NO-EXEC read/grep/glob with literal `Scope: executed=none` trailer required. `dispatch.json` lines 673–676 add `"agent": "critic"`, `Lane bounds: leaf member — no subagent dispatch.` and `Report: write your scoped findings to .ufo/waves/round-20/build/CritCalibration.md`. `dispatch.json` lines 326–330 hold the pre-spawn slot with `"agentId": null`.
2. A1 identity. `.ufo/waves/round-20/build/swarm-registry.json` lines 308–313: `"kind": "spawn"`, `"agentId": "TsukuroiR19Recovery.CritCalibration-2"`, `"role": "critic"`, `"item": null`. The registry has no status, exit, or error field for any member.
3. A2 absence. No `.ufo/waves/round-20/build/CritCalibration.md` exists (glob `build/Crit*` returns 0 files). All three seat-scope captures list it: `measure/final-r20{,b,c}/seat-scope-build.stdout` contain `{"detail": "seat report absent", "id": "SCOPE-REPORT-MISSING", "role": "critic", "site": "CritCalibration.md"}`; final-r20c totals `SCOPE-REPORT-MISSING: 13`, `status: FAIL`, at revision `fc2a0085088cedb3ab59dc3fff16523c0f42a6b4`, with `evidence_class` "self-reported declarations; no independent absence-of-execution proof".
4. A3 death record. The only seat-named death record is aggregate prose: `LOG.md` line 1039, "Thirteen provider-rate-limit deaths (… CritCalibration …); no replacement." Corroborated by `LOG.md` lines 1047, 1063, `SCORECARD.md` line 628, and snapshot `round-20.md` R20-SEAT-DEBT row and §Final measured outcome ("build reports13 provider-rate-limit deaths as missing").
5. A3 no per-seat artifact. Round20 `build/` keeps only six JSON files (dispatch, plan, spec, swarm-registry, native-task-result, native-task-result-retry-2). Grep for `CritCalibration-2` or `rate.?limit` under `.ufo/waves/round-20` matches only the registry agentId. No observed provider error text, exit code, timestamp, model, or retry-after value exists for this seat. Round21 now uses a per-seat format (`round-21/build/death-ScribeDecision.json` with `agent`, `status`, verbatim `observed_error`, and `replacement: false`). Round20 has no equivalent.
6. A3 refusals are not deaths. `native-task-result.json` lists `TsukuroiR20.CritCalibration: Background job limit reached (100)` under "Failed to start background task jobs". `native-task-result-retry-2.json` shows `"spawned": 0, "status": "refused-before-spawn"`. Both are pre-spawn refusals for every seat. The third, spawning call (LOG line 1039) has no retained result file.
7. A1 naming drift. The refusal records name `TsukuroiR20.CritCalibration`, but the registry records `TsukuroiR19Recovery.CritCalibration-2`. Grep of `/home/vgpnk/.omp` found no transcript for that id.

## Inferences

- [INFERENCE] The rate-limit death attribution rests on L1's LOG assertion, not on a retained provider error for this seat. It is credible but unverifiable from repo bytes.
- [INFERENCE] The C3 critic falsification this seat was assigned (false erratum versus history rewrite, exact live/selftest map) produced no build-wave counterexample. Whether other build or falsify seats covered it is outside this seat's scope and unresolved here.

## Not proven by absence

The missing report proves neither that commands ran nor that they did not. It is not a failed or passed C3 critique. It does not make the declared proof commands absent: the seat was assigned NO-EXEC and no execution declaration exists to evaluate. No report is invented, the dead identity is not replaced, and no trailer is rewritten.

## Round21 debt-disposition sentence (append-only)

Round21 disposition: round20 build seat CritCalibration (critic; registry agentId `TsukuroiR19Recovery.CritCalibration-2`; assigned NO-EXEC falsification of C3 false-erratum correction versus history rewrite and exact live/selftest map; required report `.ufo/waves/round-20/build/CritCalibration.md`) stays a retained `SCOPE-REPORT-MISSING` red. Its provider-rate-limit death is attested only by the aggregate thirteen-seat list in `LOG.md` line 1039, with no per-seat error record, and the two retained `Background job limit reached (100)` files are pre-spawn refusals, not death evidence. No report is authored, no replacement seat is dispatched, and the absence is not evidence of command execution or non-execution.

## Prevention test

A finite seat-death-record check, run beside `seat-scope` per wave:

- Inputs: `swarm-registry.json` and the wave's report directory.
- Rule: every registry member whose `<name>.md` is absent MUST have `death-<name>.json` with `agent` byte-equal to the registry `agentId`, a non-empty verbatim `observed_error`, and `replacement: false`.
- It never decrements `SCOPE-REPORT-MISSING`. A recorded death attributes the red; it does not clear it.

Fixtures:

| Fixture | Expected |
|---|---|
| Missing report, no death file (round20 CritCalibration as-is) | RED `DEATH-RECORD-MISSING` |
| Death file `agent: TsukuroiR20.CritCalibration` against registry `TsukuroiR19Recovery.CritCalibration-2` | RED `DEATH-AGENT-MISMATCH` |
| Death file whose `observed_error` is only `Background job limit reached (100)` or a `refused-before-spawn` status | RED `DEATH-IS-PRESPAWN-REFUSAL` |
| `replacement: true`, or a later `CritCalibration.md` authored by a different agent id | RED `DEATH-REPLACED` |
| Matching agent, verbatim 429 error, `replacement: false` | PASS for the death check; `SCOPE-REPORT-MISSING` still counted |

Also retain each spawning task-call result (e.g. `native-task-result-retry-3.json`) so the per-seat outcome stays traceable.

## Limits

Digest taken from the item, not recomputed. No transcripts were available for the seat id. No process, provider, or host state was probed. Tool installs: none (no need; NO-EXEC seat).

Scope: executed=none
