# DebtOwnAnchor10 — round20 build missing seat OwnAnchor10

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-OwnAnchor10

Reviewed snapshot: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (digest as supplied by the item and `.ufo/waves/round-21/reviews.json:333-338`; not recomputed — NO-EXEC).

## Axes

1. Identity fidelity: exact seat name, role, assignment, and agent id as recorded, with no replacement.
2. Absence fidelity: the report is absent, which is not the same as "no commands ran".
3. Death-record provenance: what records the death, and how strong that record is.
4. Append-only disposition: a round21 sentence that rewrites nothing.
5. Prevention: a finite test that keeps this class red and honest.

## Observations (source-grounded)

- **Seat and role.** `round-20/build/spec.json:88-90` declares `name: "OwnAnchor10"`, `role: "scout"`. The NO-EXEC prompt assigns "C1 source/ownership review of OUT-010 ONLY in PROVINCE portable anchors and adjacency-anchors-r19.json/sibling snapshot", asks the seat to recommend whether the R20-OUT009 clarification affects this row, and requires a closing literal `Scope: executed=none`. `plan.json:136-140,509-511` and `dispatch.json:122-126,504-506` carry the same seat. Both list `agentId: null` before spawn, and the dispatch prompt names the report target `.ufo/waves/round-20/build/OwnAnchor10.md`.
- **Spawned identity.** `round-20/build/swarm-registry.json:104-108` has `kind: "spawn"`, `agentId: "TsukuroiR19Recovery.OwnAnchor10-2"`, `role: "scout"`, `item: null`. The registry window is `createdAt 2026-10-21T08:18:06.158Z` to `updatedAt 09:23:13.585Z` (lines 4-5). The registry has no status, exit, or death field for this member.
- **Report absence.** A glob of `round-20/build/OwnAnchor*` returns 01–07 and 09. `OwnAnchor10.md` is absent, as is `OwnAnchor08.md`. No file anywhere in the lane contains the string `TsukuroiR19Recovery.OwnAnchor10-2` except the registry. A grep of `~/.omp` also found nothing; transcripts reachable only through `history://` were not readable with this seat's tools.
- **Gate record.** `measure/final-r20c/seat-scope-build.stdout` at revision `fc2a0085088cedb3ab59dc3fff16523c0f42a6b4` reports `{"id":"SCOPE-REPORT-MISSING","role":"scout","site":"OwnAnchor10.md","detail":"seat report absent"}` as one of 13 missing reports (status FAIL, seat_count 64). The earlier `final-r20` and `final-r20b` captures show the same finding. Its `evidence_class` is "self-reported declarations; no independent absence-of-execution proof". `tools/check-seat-scope.py:70-73` emits REPORT-MISSING when the report is absent, before any trailer parse. A missing report is therefore never scored as `executed=none`.
- **Provider-death record (the only one available).** `LOG.md:1039` says the third unchanged task call spawned all 64 seats. It then lists "Thirteen provider-rate-limit deaths (… OwnAnchor08, OwnAnchor10, AdjBoundary02, RevSelectorMechanism); no replacement." `LOG.md:1047` repeats "13 known rate-limit exits", and `LOG.md:1063` and lesson `round-20.md` lines 41 and 62 restate the 13 provider-rate-limit deaths.
- **Not a death record.** `native-task-result.json`, which lists OwnAnchor10 with "Background job limit reached (100)", and `native-task-result-retry-2.json` (`status: refused-before-spawn`, `spawned: 0`) record attempts one and two, which were refused before any seat spawned. They are not OwnAnchor10's death. No raw result for the third, successful call is retained under `round-20/build`.

## Inferences

- [INFERENCE] The seat spawned (its registry agentId is non-null) and ended without writing a report. The cause is attested only by the L1-authored LOG narrative. No retained provider/tool record carries a per-seat rate-limit error, exit time, or transcript excerpt.
- [INFERENCE] OUT-010's C1 ownership row got no OwnAnchor10-seat review in round20. Whether other build or falsify seats (for example `falsify/C1AppendOnly.md` and `C1ExactSection.md`, which mention OUT-010) cover it is outside this seat's scope and was not judged.

## Limits

- Nothing was executed. Digests are taken as supplied, not recomputed, and the gate stdout is quoted as retained, not re-run.
- Whether OwnAnchor10 ran any command before dying is unknown. Report absence proves neither execution nor non-execution.
- The death cause rests on one secondary narrative source, the LOG. The primary provider record for attempt three is unretained.

## Round21 debt disposition (append-only sentence)

> Round21 disposition, appended: round20 build seat `OwnAnchor10` (scout, NO-EXEC C1 OUT-010 anchor review, spawned as `TsukuroiR19Recovery.OwnAnchor10-2` per `round-20/build/swarm-registry.json:104-108`) left no `OwnAnchor10.md`. Its only death record is the L1 narrative `LOG.md:1039` ("provider-rate-limit deaths … no replacement"), with no retained per-seat provider result. The round20 `SCOPE-REPORT-MISSING` red at `final-r20c` therefore stays red as historical process debt: the seat is not replaced or re-run under its identity, no report is synthesized or backdated, its execution scope stays unknown rather than `none`, and OUT-010 round20 seat review stays unperformed.

## Prevention test

A finite fixture for `check-seat-scope` (selftest) or a wave-close check:

1. **Missing-report red.** A registry member `Alpha` with a non-null agentId and no `Alpha.md` must yield exactly `SCOPE-REPORT-MISSING` (exit 1) and never `PASS` or `SCOPE-UNDECLARED`. This matches the existing `report-missing` and registry-only fixtures at `check-seat-scope.py:344-345,397`, so it should be kept.
2. **Death-record binding (new).** At wave close, every `SCOPE-REPORT-MISSING` seat must map to a retained per-seat death record that names seat, agentId, and cause, written beside `swarm-registry.json`. This record comes from the provider or task result, not only from LOG prose. If the record is absent, the check fails with a distinct id, for example `SCOPE-DEATH-UNRECORDED`. Negative controls:
   - A synthesized `Alpha.md` whose agentId differs from the registry's must not clear the finding.
   - A replacement seat `Alpha-r` must not clear the original `Alpha`.
   - A death record must not convert the finding to PASS: the red stays, and only its cause is evidenced.
3. **Attempt separation.** Refused-before-spawn results (`spawned: 0`) must not be accepted as seat death records.

Lane bounds: leaf member — no subagent dispatch.
Tool installs: none (NO-EXEC seat; none needed).

Scope: executed=none
