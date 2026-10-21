# DebtAdjBoundary02 — round20 build missing seat AdjBoundary02

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-AdjBoundary02

The SHA-256 value above is the one supplied by this item. It was not recomputed because this seat is NO-EXEC. The reviewed file is the read-only snapshot `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md`.

## Axes

- **Identity:** which seat it was, and which agent identity was recorded for it.
- **Assignment:** the role and the exact question the seat was given.
- **Report absence:** where the report was expected and which measured red shows it is missing.
- **Death evidence:** what record of the seat's death exists, and how strong that record is.
- **Disposition and prevention:** an append-only debt sentence and a finite test, with no repair of the gap.

## Observations

1. **Seat and role.** The round20 build `spec.json` (line 98) names the seat `AdjBoundary02` with role `reviewer`. `swarm-registry.json` lines 116–121 record `kind: spawn`, `agentId: "TsukuroiR19Recovery.AdjBoundary02-2"`, `role: reviewer` and `item: null`. The registry has no status, death or cause field. `dispatch.json` lines 134–138 record the same seat with `agentId: null`.
2. **Assignment.** `spec.json` line 100 and `dispatch.json` line 516 assign: "C1 no-write locality review ADJ-02 ONLY (PROVINCE handoff trigger/retained evidence/minimum packet)…". The task is to check whether question-based routing implies remedial permission or recipient acceptance, to identify phrasing that must stay, and to give a finite negative control that prevents ownership transfer. The prompt is NO-EXEC, requires the trailer `Scope: executed=none`, and says: "Report: write your scoped findings to .ufo/waves/round-20/build/AdjBoundary02.md".
3. **Report absence.** The round20 build directory contains AdjBoundary01 and AdjBoundary03–07 reports, but no `AdjBoundary02.md`.
   - All three seat-scope captures (`measure/final-r20`, `final-r20b` and `final-r20c` `seat-scope-build.stdout`) list `{"id": "SCOPE-REPORT-MISSING", "role": "reviewer", "site": "AdjBoundary02.md", "detail": "seat report absent"}`.
   - The final capture at `fc2a0085…` reports 13 missing reports and `status: FAIL`.
   - Its own evidence class is "self-reported declarations; no independent absence-of-execution proof".
   - No `.md` file under round-20 mentions `ADJ-02`, so no other seat answered this question.
4. **Launch failures are not the death.** `native-task-result.json` line 2 records `TsukuroiR20.AdjBoundary02: Background job limit reached (100)…` for the batch launch that failed. LOG.md line 1039 says two task-call attempts were refused before spawn and that the third call spawned all 64 seats. This launch failure belongs to a different identity (`TsukuroiR20.*`), not the spawned `TsukuroiR19Recovery.AdjBoundary02-2`.
5. **The only death record.** LOG.md line 1039 says: "Thirteen provider-rate-limit deaths (… OwnAnchor08, OwnAnchor10, AdjBoundary02, RevSelectorMechanism); no replacement." LOG.md lines 1047 and 1063 and the snapshot (`R20-SEAT-DEBT`, plus "build reports13 provider-rate-limit deaths as missing") restate the count without naming the seat.
   - No raw provider error, transcript or exit receipt for this identity exists under `.ufo/waves/round-20`.
   - A grep of `~/.omp` for `TsukuroiR19Recovery.AdjBoundary02` found no files.

## Inferences

- [INFERENCE] The rate-limit cause rests only on the author's prose in LOG.md. No artifact in the repository or under `~/.omp` independently records it, so the cause is attributed, not proven.
- [INFERENCE] The agent id uses the `TsukuroiR19Recovery.*-2` namespace even though this is a round20 wave. That suggests a recovered parent session spawned it. This is an oddity in the identity's provenance, not evidence about whether the seat ran.
- The missing report says nothing either way about whether the dead seat executed commands. The NO-EXEC prompt is an instruction, not a receipt.

## Limits

- Nothing was executed. No hash was recomputed, and no checker or selftest was run.
- No report was invented, and no dead identity was replaced or re-dispatched.
- The ADJ-02 locality question (whether question-based routing implies permission or acceptance) remains **unanswered**. This seat does not answer it.
- No non-author closure or outside promotion is claimed.

## Round21 debt disposition (append-only sentence)

Round21 disposition, appended without rewriting round20 records: round20 build seat `AdjBoundary02` (reviewer, registry `agentId` `TsukuroiR19Recovery.AdjBoundary02-2`, assigned the C1 no-write locality review ADJ-02 with report path `.ufo/waves/round-20/build/AdjBoundary02.md`) delivered no report. Its only death record is LOG.md line 1039, an author statement listing it among thirteen provider-rate-limit deaths with no replacement and no retained provider receipt. `SCOPE-REPORT-MISSING` for `AdjBoundary02.md` therefore stays a retained round20 red; the ADJ-02 review question stays open, not passed; and nothing about command execution or its absence is inferred for that seat.

## Prevention test (finite)

Add a selftest fixture to `tools/check-seat-scope.py`, which today emits `SCOPE-REPORT-MISSING` at line 72 from the union of registry and spec seats. It has three cases, and every case MUST give exit 1 with exactly `{SCOPE-REPORT-MISSING}` at site `AdjBoundary02.md`, role `reviewer`:

1. The registry holds `AdjBoundary02` (reviewer) and there is no report.
2. The same registry also records a death annotation (for example `status: dead`, `cause: provider-rate-limit`). A death record must explain the gap, not clear it.
3. A report named `AdjBoundary02.md` exists only in a different wave directory (round-21), or a debt report exists under another name such as `DebtAdjBoundary02.md`. Neither may close the round20 seat, because the gate reads only the round20 wave directory.

Process-side companion, recorded as a requirement and not implemented here: at dispatch, the registry SHOULD record a per-seat terminal state (`delivered`, or `dead` with a cause and an evidence path). Then a missing report is tied to a stored record, not to prose in LOG.md.

No tool install or update was needed or performed.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none
