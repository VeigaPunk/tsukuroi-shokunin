# Crit23fInflation — metric-inflation attack on C1/C2/C3 (round23 attempt1, falsify)

Seat: TsukuroiR23-2.Crit23fInflation-2 (critic, leaf). Mode: NO-EXEC, NO-FETCH. No tool installed or updated.
Target: `.ufo/waves/round-23/preregister.json`. The digest in the receipt is the supplied identity only. I did not compute it.
skill://godspeed: I read the copied directive at `.ufo/waves/round-23/sources/godspeed-directive.txt`.

Files read (all declared): preregister.json, godspeed-directive.txt, candidate/corpus/lessons/round-23.md, sources/r22-closure.json, candidate/corpus/knowledge/path-reconciliation-r23.md, candidate/corpus/knowledge/structured-edit-r23.md. The report file did not exist before this write.
Not readable in this seat: S086 `structured-edit-observations.json`, the checkers under `tools/`, `path-reconciliation.json`, SCORECARD and the round23 events/bindings. Any finding that depends on those files is marked `[INFERENCE]` or "bounded: not verifiable here".

## Axes named

Axes: depth (C1), operability (C2), calibration (C3). Cross-cutting checks: whether each claim is labelled as a new document or as repaired behaviour, provenance, double counting, and whether a before/after count is comparable.

## Verdict summary

| Claim | Metric | New-document count or repaired behaviour? | Labelled so at the authority (preregister)? | Inflation defect |
|---|---|---|---|---|
| C1 | validated_edit_decisions 0→8 | New-document count: eight policy rows the author wrote | Yes, in preregister C1 scope | Fixable: the evidence column overstates its source, and three rows restate the C2 rule |
| C2 | structured_edit_mode 0→1 | New-instrument availability. Before=0 by construction | Yes, in preregister C2 scope and the knowledge doc | Fixable: no label says round23 v2 violation counts can't be compared with round22 v1 counts. The lesson calls the policy grant a "Fix" |
| C3 | unexplained_cohorts 2→0 | New explanation of frozen history. No behaviour changes | Yes, in preregister C3 scope and the knowledge doc | Fixable: the outside verifier already gave the hypothesis. The disposition rule nearly forces the target |

None of these is a tradeoff the judge must reject. Preregister `ordinal_delta: 0`, `retired: []` and `capability_acquisition: false` show that no axis ordinal is claimed to rise. The inflation risk is therefore in downstream "improved" verdicts and in wording, not in the preregistered numbers.

## C1 — eight edit-contract decisions (depth)

Claim attacked: C1 says 0→8 "validated_edit_decisions" is depth progress.

Labelling: Correct at the authority. Preregister C1 scope says: "new document contract, not eight repaired runtime behaviors." The knowledge doc says it "deepens held … ground, not an uncovered frontier, repertoire addition or outside promotion". The 8 is a count of rows the author wrote. The target equals the length of the preregister's own `edit_decisions` array, so a faithful copy reaches the target by construction. Only the row-level discriminating controls can make "validated" mean anything. I can't read those controls here (bounded).

Falsifier F1 (false provenance):
- In `structured-edit-r23.md`, all eight rows cite `Evidence: S086`. S086 is scoped to "Observed structured path metadata and recorded adapter steps only". The only observed shapes the doc describes are `path` with `stream_content` or `old_string`/`new_string`, plus report reads and writes under the same parent call.
- The r22 closure attributes the typo paths and the internal URI to out-of-binding reads, not to edits.
- So EDIT_TRAVERSAL, EDIT_EXTERNAL and likely OPAQUE_PATCH are normative negative controls with no observed edit instance `[INFERENCE: S086 not readable in this seat]`. Citing S086 on those rows makes policy look source-grounded.
- Impacted axes: depth, calibration of provenance.

Falsifier F2 (one rule counted on two axes):
- DECLARED_EDIT, READ_ONLY_EDIT and WRITE_ONLY_EDIT are the same predicate as C2's v2 rule. C2's rule says `edit_paths` must be a canonical literal subset of both read and write targets, as stated in Bounded procedure step 1 of the C1 doc itself.
- Preregister `separability` separates what each checker reads. It does not separate what the claims mean.
- Counterexample: a single defect in the subset rule, such as accepting an edit target that is only in write_paths, would turn red both C1's WRITE_ONLY_EDIT row and the C2 v2 audit result. Conversely, one rule design earns credit on both depth (3 of 8 rows) and operability (mode 1).
- The knowledge doc even describes C1 as deepening "evidence-operability ground", which is C2's axis, while preregister assigns C1 to depth.
- Impacted axes: depth, operability.

Smallest in-scope remedy (C1):
1. Split the Evidence column into "S086 observed" and "normative control, no observed instance", and mark each row honestly.
2. Add one sentence: "DECLARED/READ_ONLY/WRITE_ONLY restate the C2 v2 subset rule; C1 depth credit for them is not independent of C2." Alternatively, the judge counts C1 as 5 independent rows plus 3 shared rows.
3. Change "evidence-operability ground" to "depth".

## C2 — v2 edit audit authority (operability)

Claim attacked: C2 says structured_edit_mode 0→1 is operability progress.

Labelling: Correct at the authority. Preregister C2 scope says: "New explicit schema-v2 audit authority … legacy schema-v1 policy and historical reds unchanged … no native enforcement/effects claim". The knowledge doc says: "Numeric mode availability is not compliance." The metric is binary availability of a newly named mode, so before=0 holds by definition. r22 already used the same pattern ("request_audit_mode 0→1", accepted as operability improved in r22-closure). Minting a fresh mode name with before=0 each round inflates operability by construction unless the judge credits only the instrument's discriminating controls.

Falsifier F3 (relabelling by policy widening):
- r22's retained reds include edit16/17 classified as unknown-tool (r22-closure rechecks and notes).
- Round23's 64 build seats run under exact schema-v2 report read+write+edit declarations (lesson, Mechanics).
- So a round23 seat that behaves exactly like an r22 seat, using `edit` on its own report, now counts as clean. Any r22→r23 drop in unknown-tool or edit violation counts would come from widened authority, not from repaired seat behaviour.
- The lesson's own gate row says v2 exists to "accommodate observed native editor shapes". Its Mistakes row R23-EDIT-AUTHORITY puts "Predeclare exact future read+write+edit authority in v2" in the "Fix" column. That calls a permission grant a fix.
- The no-retroactivity labels ("Retrospectively allow r22 … reject"; "No grant is retroactive") protect the old counts. No label prevents the prospective comparison.
- Bounded: SCORECARD and the round23 events are not readable here, so I can't tell whether such a comparison has already been asserted.
- Impacted axes: operability, calibration.

Smallest in-scope remedy (C2):
1. In R23-EDIT-AUTHORITY, change "Fix" to "policy accommodation; seat edit behaviour unchanged; r22 reds stay".
2. Add one line to the knowledge doc or SCORECARD: "Round23 v2 violation counts are not comparable to r22 v1 counts (41/46); any cross-round comparison must replay round23 events under v1 or report both."

## C3 — path-census reconciliation (calibration)

Claim attacked: C3 says unexplained_cohorts 2→0 is calibration progress.

Labelling: Correct at the authority. Preregister C3 scope says: "does not relabel old violations or retry historic checks". The knowledge doc says: "Row creation itself is neither expansion nor a quality-trend improvement", and also "Any actual scope violation remains a violation". The work is a new explanation of frozen historical counts. No behaviour is repaired.

Arithmetic check (from the doc table, all consistent):
- build: 376 agree + 2 selector-normalization = 378 recorded requests, and 25 − 23 = 2 − 0.
- falsify: 991 agree + 4 selector-normalization = 995 recorded requests, and 33 − 29 = 4 − 0.
- No arithmetic falsifier found.

Falsifier F4 (before=2 overstates prior ignorance, and the provenance is missing):
- r22-closure `verification.rechecks` already said: "approximate own path-binding census 25/33 vs checker 23/29 (selector-normalization differences, not decisive)".
- So the outside verifier had already explained the gap as selector normalization at the cohort level, with no per-event detail. Round23 confirms that hypothesis per event.
- The knowledge doc does say "no event-level explanation", which is the precise wording. But neither the knowledge doc nor lesson R23-RAW-ORDER credits the outside hypothesis.
- R23-RAW-ORDER says two wave-1 seats "independently located" the 2+4 events. They are independent of each other, but both come after the outside hypothesis, which was in their source packet.
- Impacted axes: calibration (provenance).

Falsifier F5 (the disposition rule nearly forces the target):
- `selector-normalization` requires that rough flags the event, canonical and retained clear it, and the rough-stripped spelling differs from the canonical base.
- The third condition follows from the first two. If the canonical base is bound and the rough-stripped spelling is not, the two spellings must differ.
- So every rough-only event with canonical = retained clear is classed as "explained", whatever the real reason.
- Counterexample: suppose the canonical selector grammar, which is the lane's own instrument and the thing being calibrated, over-accepted a non-benign selector. That event would land in selector-normalization, not unexplained. With the constraint canonical = retained, "unexplained" can only come from disagreements on the retained side.
- This round's result is still grounded concretely: the doc names all six events as `:raw:N-M`, with bare paths literally bound, and a `mixed-raw-range-order` selftest. But that grounding sits in the prose and selftest, not in the disposition rule that gives the 0.
- Bounded: I can't read the checker or ledger code here, so I can't tell whether the checker requires the stripped residue to be canonical selector tokens.
- Impacted axes: calibration.

Smallest in-scope remedy (C3):
1. Add one sentence to `path-reconciliation-r23.md`: "The outside closure already attributed the gap to selector normalization (not decisive); round23 supplies the per-event confirmation."
2. Tighten `selector-normalization` so that the rough-stripped spelling must equal the canonical base followed only by canonical selector tokens (`raw`/`img`/`conflicts`/range). Any other residue is `unexplained`.
3. If the checker already enforces item 2, state that in the contract text.

## Bounded search, no falsifier found

- None of the three preregister scopes claims behaviour repair. Each is explicitly labelled as a new document, a new schema or a new explanation.
- No ordinal inflation: `ordinal_delta: 0` and all ordinals are unchanged.
- The lesson rejects crediting an instrument's existence as quality (R23-QUALITY-TREND) and accepts the outside "quality unchanged" verdict.
- No claim of native enforcement appears in any of the six files read.

## Impacted axes, overall

Depth (F1, F2), operability (F2, F3), calibration (F3, F4, F5). Every remedy is a wording or labelling change in the round23 candidate docs or lesson. F5 also allows a one-predicate tightening. None needs rewriting historical r22 material.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23f-crit23finflation
Scope: executed=none
