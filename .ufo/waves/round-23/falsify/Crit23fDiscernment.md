# Crit23fDiscernment — round23 falsify, attempt1

Seat: critic, leaf member, no subagent dispatch. NO-EXEC, NO-FETCH. I read only the eight declared paths. The seat-local report path did not exist before this write. `skill://godspeed` was not used; I read the copied directive at `.ufo/waves/round-23/sources/godspeed-directive.txt`. Nothing was installed or updated.

Axes attacked: discernment trend, C3 calibration, and false provenance or duplicate authority in the mined-mistake ledger.

## Verdict

R23-QUALITY-TREND and R23-PATH-UNIT both point at real disagreements, but neither is a new in-round catch with its own fail-capable fix.

- **R23-QUALITY-TREND** re-records an outside catch. Its fix is a norm only and has no failure control.
- **R23-PATH-UNIT** names a cause (counting unit) that the round's own ledger refutes. The real catch is already recorded as R23-RAW-ORDER, so the finding is counted twice.

Neither defect harms C1, C2 or C3 as preregistered measures, and the candidate texts do not claim a trend themselves. Both are fixable labelling and provenance defects that the judge should see before it credits discernment.

A third, separate finding concerns the C3 contract: the `agree` disposition is not defined at component level. This is a definitional gap, not an observed failure.

## Finding 1 — R23-QUALITY-TREND is an inherited outside catch, and its fix cannot fail

**Attacked claim:** the discernment trend, namely that the round mined R23-QUALITY-TREND with a fix.

**Evidence:**

- `sources/r22-closure.json` `trends.quality` is `"unchanged"`. Its `notes` say "Quality trend unchanged: in-round gate hardening and registry repair concern new material; no prior entry superseded or re-verified".
- `preregister.json` `outside_round22.trends.quality` is `"unchanged"`.
- The outside verifier CloseKaidoku22 made this catch at rounds[422]. The lane did not. The lesson itself admits this in "Outside round22 disposition", which says the outside label "supersedes the author's earlier improved label".

**Counterexample 1, provenance:** the lesson's Evidence cell cites only `r22-closure.json` for "r22 author quality improved". That file contains only the outside `unchanged` verdict. The author-side `improved` label is not located in any cited source, so one half of the claimed disagreement has no cited evidence.

**Counterexample 2, fail-capability:** the fix cell says "Append the outside correction … do not credit an instrument's existence as corpus quality. New criterion cites this outside disagreement".

- None of these clauses names a check, selftest or mutant that fails when a later lesson credits a quality improvement without a superseded or re-verified prior entry.
- The lesson's own rule, "No fix is counted before observed failure controls", therefore either excludes this row or is violated by it.
- The "new criterion" is not named. LEARNING and QUALITY are not in my read paths, so I could not locate it. [INFERENCE] As written, the criterion is prose that cannot go red.

**Impacted axes:** the discernment trend (credit for a catch by the outside verifier) and calibration (false provenance).

**Smallest safe correction (L1, lesson text only, no r22 rewrite):**

1. Set Captured-by to `outside CloseKaidoku22 rounds[422]`.
2. Cite the exact author-side location of the r22 `improved` label, for example the r22 lesson or report line.
3. Mark the fix as `norm-only, not counted` until a named failure control exists.
4. Alternatively, add one literal gate case to an existing checker: a lesson that asserts `quality: improved` with zero superseded or re-verified prior entries must fail. Then cite that case.

## Finding 2 — R23-PATH-UNIT names a refuted cause and double-counts R23-RAW-ORDER

**Attacked claim:** the discernment trend and C3. R23-PATH-UNIT is presented as a mined counting/calibration mistake with a fix.

**Evidence:**

- `knowledge/path-reconciliation-r23.md` §Finding says: "The per-event versus per-component counting unit made no difference in these cohorts: no event had more than one denied component. The 2- and 4-event gaps are therefore entirely selector normalization."
- The table shows unit-difference events of 0 for build and 0 for falsify.
- The lesson's R23-RAW-ORDER row records that same root cause, the `:raw:N-M` order that the outside regex leaves as `<path>:raw`. It has its own captured-by (QUALITY51), its own selftest (`mixed-raw-range-order`) and its own unit (`rough-misses-raw-first`).

**Counterexample 1, refuted cause:**

- The named hypothesis, that the counting unit explains the gap, is falsified on all 1373 real events by the round's own ledger.
- The Gate row rejecting "Rough25/33 minus lane23/29 proves exactly 6 missing unsafe events" shows sound discernment.
- Recording a separate *mistake* called PATH-UNIT whose unit term is 0 everywhere, though, relabels the outside approximate count (`approximate own path-binding census 25/33 vs checker23/29 (selector-normalization differences, not decisive)` in r22-closure) as a lane mistake. The lane's 23/29 was correct.
- The actual lane deficit was C3 `before: 2` (no event-level explanation). That is a coverage gap, not a counting mistake.

**Counterexample 2, duplicate authority:**

- R23-PATH-UNIT and R23-RAW-ORDER have the same evidence cohorts, the same six events and the same fix surface (`check-path-reconciliation.py`).
- Counting both inflates the mined-mistake count by one for a single cause.
- On real data, the only fail-capable content unique to R23-PATH-UNIT is the unit term. That term is exercised only by the synthetic "per-component units" selftest named in the knowledge doc, never by observed data.
- The claimed controls (forged dispositions, dropped or duplicate rows, L1 mutants killed in `measure/l1-mutation.json`) are outside my read paths. [INFERENCE] I treat them as asserted, not verified.

**Impacted axes:** the discernment trend (double count), calibration (lane-mistake provenance on an outside approximation) and C3 (the label suggests a unit effect that the data shows is zero).

**Smallest safe correction (L1, lesson text):**

1. Merge R23-PATH-UNIT into R23-RAW-ORDER, or rename it to something like `R23-PATH-EXPLAIN` with class `coverage` and evidence `C3 before 2`.
2. Record that the unit hypothesis was tested and found to be 0 on both cohorts.
3. Cite the unit-difference selftest as a synthetic control only.
4. Do not count it as a second in-round discernment catch.

## Finding 3 — `agree` is undefined at component level, so cancelling disagreements can hide

**Attacked claim:** C3. The contract claims "exhaustive per-event/component explanation" with 0 unexplained.

**Evidence:**

- `knowledge/path-reconciliation-r23.md` §Reconciliation contract records "the rough category and first bad component, the canonical bad component indices". It then lists the disposition `agree` without saying whether the two indices must match.
- The lesson's Gate row requires that "cancelling disagreements must be examined per event/component".

**Counterexample (constructed, not observed):**

- Take an event with components A and B.
- The rough rule breaks on A, a raw-order false positive, and stops at the first failure.
- Canonical v1 denies only B.
- Both methods flag the event once, so it is classed `agree` with rough minus retained equal to 0, and the identity `rough − retained = SN − Σ(unit extra)` still holds.
- Yet the methods disagree on both components. The rough rule hides a real denial behind a spurious one.

**Search bound:** the knowledge doc states only that no event had more than one *canonical* denied component. That statement does not exclude this case, because canonical denies one component here. I could not inspect `path-reconciliation.json` (not declared), so I did not observe the case.

**Related gap:** `selector-normalization` is defined as "rough flags, canonical and retained clear, and the rough-stripped spelling differs from the canonical base". That is effectively a catch-all for every rough false positive, not a cause-specific label. The specific `:raw` cause is proved only by R23-RAW-ORDER's selftest.

**Impacted axes:** C3 calibration and false provenance (the disposition name implies a cause).

**Smallest safe correction:**

1. Define `agree` so that the rough first-bad index is in the set of canonical bad indices, or both are empty.
2. Classify a mismatch as `unexplained`.
3. Add one literal selftest, `cancelling-component`, for the constructed event above.
4. Require `selector-normalization` rows to record the exact stripped residue (for example `:raw`) and the grammar rule it matches.

## Bounded search and limits

- **Read:** preregister, the godspeed directive copy, the round-23 lesson, r22-closure, the path-reconciliation knowledge doc and the structured-edit knowledge doc.
- **Not checked:** I found no defect in the C1 decision table or the C2 v2 authority text that bears on these two mined mistakes. The eight `edit_decisions` in the preregister match the knowledge table row for row, in decision and reason.
- **Possible conflict:** the lesson says "Body fields remain opaque data". The knowledge doc requires the "one of the two observed finite argument-key shapes". These are consistent. Key names are metadata and are not body interpretation.
- **Not verifiable from my scope:** QUALITY or LEARNING criteria, `path-reconciliation.json`, `l1-mutation.json`, gate source, and the r22 author report. Every claim about them above is marked as inference or as asserted.
- **Supplied identity:** the digest below is the supplied declaration. I did not compute it.
- **Lane bounds:** leaf member, no subagent dispatch.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23f-crit23fdiscernment
Scope: executed=none
