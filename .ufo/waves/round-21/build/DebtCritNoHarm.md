# DebtCritNoHarm — round20 build missing seat CritNoHarm

Seat: `TsukuroiR21.DebtCritNoHarm-5` (scout, leaf, NO-EXEC). Author-dispatched; not non-author closure, not outside promotion.

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-CritNoHarm

Reviewed bytes: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (baseline source `corpus/lessons/round-20.md`). The digest is the one supplied by the item and listed in `.ufo/waves/round-21/reviews.json:369-373`; under NO-EXEC I did not recompute it.

## Axes

The audit checked five things: whether the role and assignment are exact, whether the report is absent, which provider-death record is available, whether any identity was replaced, and whether the lesson prose is faithful to the receipts.

## Observations

1. **Role and assignment.** `.ufo/waves/round-20/build/spec.json:263-265` lists the item as `name: CritNoHarm` with `role: critic`. Its prompt is NO-EXEC: "Falsify no ordinal uplift/capability/boot freshness certificate; preserve rejected/UNKNOWN history and author/non-author distinction. Read prereg and baseline routed spotcheck." In `dispatch.json:679-681`, the task sets the report target to `.ufo/waves/round-20/build/CritNoHarm.md` and adds "Lane bounds: leaf member — no subagent dispatch." `plan.json:684-686` carries the same text. The dispatch-time member at `dispatch.json:332-336` has `agentId: null`.
2. **Identity.** `swarm-registry.json:314-318` records `CritNoHarm` with `kind: spawn`, `agentId: "TsukuroiR19Recovery.CritNoHarm-2"`, `role: critic` and `item: null`. The registry window runs from `createdAt 2026-10-21T08:18:06.158Z` to `updatedAt 09:23:13.585Z`. That agent ID appears in no other file under the lane.
3. **Earlier spawn attempts.** In `native-task-result.json`, `TsukuroiR20.CritNoHarm` failed with "Background job limit reached (100)" and `results: []`. In `native-task-result-retry-2.json`, attempt 2 has `status: refused-before-spawn`, `spawned: 0` and the same error. Neither is a provider death; each records a failure to start. Neither file contains the registered identity `TsukuroiR19Recovery.CritNoHarm-2`.
4. **Report absence.** Globbing `Crit*` under `.ufo/waves/round-20` returns 0 files, so `build/CritNoHarm.md` does not exist. The receipt `measure/final-r20c/seat-scope-build.stdout` (revision `fc2a0085…`, `seat_count 64`, `status FAIL`) contains `{"id":"SCOPE-REPORT-MISSING","role":"critic","site":"CritNoHarm.md","detail":"seat report absent"}`, one of 13 `SCOPE-REPORT-MISSING`. The `final-r20` and `final-r20b` receipts carry the same row. The gate's own `evidence_class` reads "self-reported declarations; no independent absence-of-execution proof".
5. **Provider-death record.** No per-seat death record exists for round 20. Globbing `**/death*` across `.ufo/waves` finds only the round-21 file `round-21/build/death-ScribeDecision.json`. Grep finds no "rate limit" text anywhere under `round-20/`. The only attribution of the death is aggregate lesson prose: snapshot line 41 (R20-SEAT-DEBT, "13 build reports missing from provider-rate-limit deaths") and line 63 ("build reports13 provider-rate-limit deaths as missing"). Neither line names `CritNoHarm`, an observed error, or a time.
6. **No replacement.** The spec, plan and dispatch all say "Dead seats stay dead, no replacements." I found no second registry identity and no substitute report for this seat.

## Inferences

- [INFERENCE] The registered identity `TsukuroiR19Recovery.CritNoHarm-2` came from a third spawn that was not recorded. Its parent was a recovery session rather than the `TsukuroiR20` session refused in observations 3, and no spawn or result receipt for it is retained in `round-20/build`.
- [INFERENCE] The cause "provider rate limit" for this specific seat rests only on the author's aggregate claim in lesson lines 41 and 63. It is plausible given the 13-seat count, but no receipt in the lane substantiates it.

## Limits

- The missing report is not evidence about what this seat executed or did not execute. The seat-scope count is a count of declarations, and an absent report declares nothing, so the absence proves neither that proof commands were never run nor that they ran.
- The death cause is not established for this seat. The counterexample and admission requirement that CritNoHarm was supposed to produce are absent, and nothing here reconstructs them.
- The other 12 missing seats are out of scope. The SHA was supplied, not recomputed. I read no history or provider logs outside the lane.

## Append-only round21 debt-disposition sentence

Round20 build seat `CritNoHarm` (critic; NO-EXEC falsifier for the no-uplift/capability/boot-freshness-certificate claim; registry identity `TsukuroiR19Recovery.CritNoHarm-2`) produced no `.ufo/waves/round-20/build/CritNoHarm.md`. Its `SCOPE-REPORT-MISSING` red in `measure/final-r20c/seat-scope-build.stdout` is retained unchanged. Its provider-rate-limit death is attributed only by the aggregate round-20 lesson prose, with no per-seat death record. The identity is not replaced and no report is backfilled. Its absence is evidence neither that commands ran nor that they did not, and its falsification duty remains undischarged.

## Prevention test

The prevention test has three parts: a finding rule for the wave-close or seat-scope gate, five hermetic fixtures, and the expected output against round 20.

**Finding rule.** For every registry seat flagged `SCOPE-REPORT-MISSING`, the gate requires a sibling `death-<Name>.json`, like the round-21 `death-ScribeDecision.json`. That file must contain:

- `name == <Name>`
- `agent` equal to the registry `members[<Name>].agentId`, non-null
- a non-empty `observed_error`
- `replacement: false`

Missing or mismatched records emit a new `SCOPE-DEATH-UNRECORDED` finding. The `SCOPE-REPORT-MISSING` red stays either way, because a death record attributes the absence and never passes the seat.

**Fixtures.**

| Fixture | Expected result |
|---|---|
| Seat `CritNoHarm` with agentId `X`, no report, no death file | FAIL with both `SCOPE-REPORT-MISSING` and `SCOPE-DEATH-UNRECORDED` |
| Same seat with a death file whose `agent != X` | FAIL with both findings |
| Same seat with a death file whose `replacement: true`, or with a second registry member for the same report stem | FAIL |
| Same seat with a matching death file | FAIL with `SCOPE-REPORT-MISSING` only, still exit 1 |
| Same seat with both a matching death file and a `CritNoHarm.md` report | FAIL as a death/report conflict; a report from a dead identity is not accepted |

**Expected run against round 20.** Running the rule on `.ufo/waves/round-20/build` must report `CritNoHarm` with `SCOPE-DEATH-UNRECORDED`.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none
