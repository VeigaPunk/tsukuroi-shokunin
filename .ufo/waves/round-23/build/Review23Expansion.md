# Review23Expansion -- scoped review of the EXPANSION structured-edit decision (round 23)

Seat: Review23Expansion (reviewer, leaf member; no subagents dispatched, no commands executed).
Review object: preregister row 8 of the C1 decision table (EXPANSION / CHECK_EACH) and its interaction with C2, read against the declared structured-edit census.

Declared inputs read (no other path opened, no fetch, no execution):
- .ufo/waves/round-23/sources/structured-edit-observations.json (schema tsukuroi-structured-edit-observations-v1, accessed 2026-10-21)
- .ufo/waves/round-23/preregister.json (schema tsukuroi-round23-preregister-v1)
- .ufo/waves/round-23/snapshot/tools/check-review-cohort.py
- .ufo/waves/round-23/sources/godspeed-directive.txt and skill://godspeed (posture only; no execution implied)

The declared source digest is treated as supplied identity. It was not recomputed.

Axes named for this review (godspeed): (a) enumeration completeness of recorded adapter events, (b) target-identity decidability between read and edit/write, (c) verdict-vocabulary coherence of the eight decision rows, (d) temporal/as-of correctness of authority, (e) honest saturation of the "source-grounded" claim, (f) observer-signal honesty in the reviewer cohort accounting. All findings below are contract-text or record-shape findings. No native enforcement, runtime prevention, effect, reading proof, or universal tool/patch semantics is claimed anywhere in this report; the census itself disclaims those at its scope line (structured-edit-observations.json:101) and the preregister disclaims them at preregister.json:111-113.

---

## Findings by severity

### HIGH -- F1. The enumerated event surface contains only edit requests; read and write steps exist solely as nested entries, so "every recorded adapter read or write" has no flat list to iterate.

Evidence: the census enumerates four observations, and every one of them has tool "edit" (structured-edit-observations.json:11, 37, 60, 83). The only read step (line 12, tool read, CritRuntime.md:raw -- lines 19-23) and the only write step (line 13, tool write, CritRuntime.md -- lines 24-28) are reachable only by descending into observation[0].recorded_starts. At top level the census therefore shows 4 edit events and 0 read/write events.

Impact: the EXPANSION row's promise ("Every recorded adapter read or write remains separately scoped", preregister.json:93-95) cannot be discharged by a checker that iterates the observation list, because it never sees the read or the write. A checker that instead walks recorded_starts sees a heterogeneous, non-uniform structure in which read/write/edit entries are not first-class and carry different field sets. Either way the "every" quantifier is unbacked by a declared enumeration surface.

Bounded recommendation (source-only): define one flat event record shape in the decision contract -- every recorded adapter step (read, write, edit) as a first-class record carrying seat, tool, resolved target, selector, transcript, and line -- and require the CHECK_EACH check to iterate that single flat list, with the census re-shaped to match (read and write steps promoted out of nested recorded_starts).

### HIGH -- F2. Target identity is not normalized between read and edit/write in the very transcript the DECLARED_EDIT row constrains, so "exact target predeclared for edit and for both read and write" is not decidable as written.

Evidence: for CritRuntime the recorded read target is the selector-qualified string ".../round-22/build/CritRuntime.md:raw" (structured-edit-observations.json:22) while the write target (line 27) and the edit target (line 16) are the bare ".../round-22/build/CritRuntime.md". Same file, two distinct target strings, one transcript.

Impact: DECLARED_EDIT (preregister.json:57-61) requires the exact target to be predeclared for edit and for both read and write. Under exact string equality the read half of that conjunction fails for the only transcript that contains a read; under a normalization that drops the selector, "exact predeclared" no longer constrains which region of the file was read, and the same normalization would also admit a selector that was never declared. The two readings of "exact target" are mutually exclusive and the contract does not choose between them. This is a contract-definition defect, independent of any runtime.

Bounded recommendation: state in the decision contract whether the authority target is the filesystem path or the path plus selector, and record both fields separately in the event record so the equality in DECLARED_EDIT is decidable without guessing. If the intent is path-level authority, say "path-level authority; selector is not an authority surface" explicitly rather than leaving it to the implementation.

### HIGH -- F3. Two incompatible structured edit argument shapes are observed, and no row states which shape an edit-authority declaration binds.

Evidence: CritRuntime's edit carries argument_keys ["path","stream_content"] (structured-edit-observations.json:12-15) -- a whole-content replacement with no old_string anchor. Each OraclePathArtifact edit carries ["i","new_string","old_string","path"] (lines 38-43, 61-66, 84-89). CritRuntime additionally used a plain write step to the same file (lines 24-28).

Impact: if v2 authority is declared per shape, one of the two observed shapes is silently unauthorized and the C1 table's DECLARED_EDIT row is under-specified. If it is declared shape-agnostically on "path" alone, a stream_content (full overwrite) edit inherits authority from a declaration that a reader may have intended for the anchored old/new form. The C2 scope calls the new authority "for exact predeclared structured edit targets" (preregister.json:43) without stating the binding granularity, so both readings survive the contract text.

Bounded recommendation: state that authority binds to the resolved filesystem target path, that argument shape (stream_content versus old_string/new_string) neither creates nor withholds authority, and that the audit record must capture the observed shape id so a divergence between declared and observed shape remains visible instead of being silently absorbed.

### MEDIUM -- F4. EXPANSION is the only row whose verdict is outside the ALLOW/DENY/UNKNOWN vocabulary; the table mixes a per-target verdict with a procedural requirement.

Evidence: rows 1-7 use ALLOW, DENY, UNKNOWN, DENY, DENY, DENY, DENY (preregister.json:57-91) and row 8 uses CHECK_EACH (preregister.json:92-95).

Impact: if the eight-row contract is validated row-wise as "each row classifies a target into one verdict", row 8 has nothing to classify: it either passes vacuously because no event is classified into it, or it is rejected by a schema validator restricted to three verdict values. The latter would block the C1 target of eight validated decisions (preregister.json:31-33) outright. The census makes the vacuous-pass reading reachable: the six rows other than DECLARED_EDIT and EXPANSION have no instance in the census (see F7), so an event-driven checker has almost nothing to classify.

Bounded recommendation: declare the verdict vocabulary explicitly as {ALLOW, DENY, UNKNOWN, CHECK_EACH} and define CHECK_EACH as a per-recorded-event-pair requirement evaluated over the flat event list from F1, distinct from a per-target verdict. Keep the row count at eight; change only the vocabulary and the evaluation rule.

### MEDIUM -- F5. The scope axis of "separately scoped" is undeclared, and the census's own ordering field contradicts the reading its name suggests.

Evidence: the OraclePathArtifact edits are at request lines 30, 33, 36 (lines 35, 58, 81) and each one's recorded_starts points at line 31, 34, 37 respectively (lines 46-51, 69-74, 92-97) -- a later line in the same transcript, another edit to the same path. CritRuntime's recorded_starts point at lines 12 and 13 (lines 18-28) against request line 15 -- earlier lines. So "recorded_starts" contains preceding steps in one transcript and a following step in another.

Impact: a checker that reads recorded_starts as "the steps that preceded this request" will mis-order the Oracle transcript and may wrongly treat a subsequent edit as authorization evidence for the current one. Under per-target scoping the three Oracle edits to one path collapse to a single target; under per-event scoping they are three separate authorities; the row does not say which. The census disclaims universal tool semantics (line 101), but the ordering relation and the scope key are exactly the two properties the CHECK_EACH rule depends on.

Bounded recommendation: declare the scope key explicitly (seat, resolved target, direction, event id) and state that recorded_starts is an unordered set of recorded adapter steps observed for the same transcript and target, not a chronological or causal prefix; then define CHECK_EACH over (event, recorded step) pairs with no ordering assumption.

### MEDIUM -- F6. The contract has no as-of clause, so "predeclare report/draft read AND write" can silently retroactively authorize historical unauthorized reads.

Evidence: the C1 row requires read and write authority on the exact target (preregister.json:57-61) and the assignment for this review requires never erasing old unauthorized reads. The preregister limits forbid retrospective authorization and historical manifest/report rewrite (preregister.json:113), and C2 requires legacy schema-v1 policy and historical reds to stay unchanged (preregister.json:43). Nothing in the eight-row table states which declaration set applies to which recorded event.

Impact: this is the concrete mechanism by which an expansion rule erases an old red. If r23 events are rescored against the union of r22 and r23 declarations, a previously unauthorized read or edit flips to authorized without any historical record being rewritten -- the ledger looks intact while the classification underneath changed. The r22 census is exactly the material that would be reinterpreted: three OraclePathArtifact edits and one CritRuntime edit/read/write on round-22 build paths (structured-edit-observations.json:16, 22, 27, 44, 67, 90), none of them accompanied by any authority record in the census, whose scope line explicitly disclaims native permission enforcement (line 101).

Bounded recommendation: add an as-of clause to the contract -- each recorded event is scored against the declaration set that was in force when the event was recorded, identified by an explicit declaration revision id carried on both the event record and the authority record. Events whose declaration revision cannot be identified are UNKNOWN, never authorized by default. This preserves both C2's "historical reds unchanged" and the requirement that old unauthorized reads survive.

### LOW -- F7. Six of the eight rows have no observed instance in the declared source, so "source-grounded" overstates the grounding for those rows.

Evidence: the census contains two seats, two transcripts, four edit requests, two argument shapes, one read step, one write step, one target per seat (structured-edit-observations.json:6-99). It contains no undeclared-target edit, no read-only or write-only authority case, no opaque patch body (all bodies are "omitted; no report text copied", lines 17, 45, 68, 91), no dot-segment or alternate spelling path, and no URI-shaped target. Those are exactly the six non-EXPANSION, non-DECLARED_EDIT rows (preregister.json:62-90). The source is declared prospective, for "observed structured edit request keys and recorded adapter steps" (preregister.json:119).

Impact: for UNDECLARED_EDIT, READ_ONLY_EDIT, WRITE_ONLY_EDIT, OPAQUE_PATCH, EDIT_TRAVERSAL and EDIT_EXTERNAL the grounding available in the declared source is normative prose, not an observed instance. The C1 scope says "Eight finite source-grounded structured-edit authority decisions" (preregister.json:34). Read as "all eight instantiated by the census" that is not supportable; read as "eight decisions over source-grounded vocabulary" it is. The ambiguity is the defect.

Bounded recommendation: give each row a declared grounding type (observed instance in S086 versus normative rule over S086 vocabulary versus normative only), and tighten the C1 scope sentence to say which rows are instance-grounded and which are rule-only. A validator that treats all eight identically will overstate coverage either way.

### LOW -- F8. The reviewer cohort's headline status is PASS even when seats are receipt-faulty; citing cohort green as edit-contract conformance would be a false signal.

Evidence: check-review-cohort.py classifies per-seat outcomes into delivered_conformant / delivered_faulty / absent_dead / absent_unresolved and records delivered_faulty only in the counters; findings are raised for COHORT-UNRESOLVED, COHORT-REPORT-DRIFT, COHORT-READ, COHORT-SCHEMA and COHORT-STRICT-UNAVAILABLE only (check-review-cohort.py:60-89). The exit code is 0 whenever no such finding exists, while strict_conformance is reported separately as FAIL (line 99). The tool's own docstring states it must not convert strict receipt faults to passes (line 2), and the selftest pins that expectation: a receipt-faulty seat yields exit 0 with category delivered_faulty (case 'partial-failed', line 122; also 'period', 'predicate', 'digest', 'duplicate-receipt', 'unicode' at lines 125-129).

Impact: a caller that reads only the process exit status or the word PASS will conclude conformance for a cohort in which every seat is faulty. The fault is not lost -- per-seat strict_findings and strict_conformance are reported (lines 83, 98-99) -- but the summary is not a conformance signal.

Bounded recommendation: any round-23 or later write-up that cites reviewer-cohort results must cite delivered_faulty counts and strict_conformance explicitly alongside the status, and must not describe a green cohort exit as evidence about edit-contract conformance.

### LOW -- F9. The strict evaluator is invoked with two different input types across call paths, so production and selftest behavior may diverge; unverifiable within this seat's read scope.

Evidence: the production path passes manifest bytes obtained from git_read into strict.evaluate (check-review-cohort.py:205, 207 via git_read returning subprocess stdout), the selftest passes a JSON string (line 161), and the per-seat re-evaluation passes a freshly re-serialized single-review JSON string (line 61, line 62). The per-seat manifest is also structurally reduced to schema plus one review, dropping whatever other manifest-level fields the strict evaluator may require (line 61).

Impact: if the strict evaluator's parsing depends on the input type, or on manifest fields beyond schema and reviews, the per-seat verdict used for delivered_conformant versus delivered_faulty (line 78) is computed under weaker or differently typed input than the whole-manifest verdict used for strict_receipt_exit (line 33). A KeyError or similar in the per-seat call would surface as COHORT-SCHEMA and CANNOT_EVALUATE via the broad except at lines 92-93, which is at least loud; a silent divergence is not. The strict evaluator module itself is outside this seat's declared read paths, so the magnitude of the risk could not be determined here.

Bounded recommendation: make the call sites type-consistent and pass the per-seat manifest through the same serialization and field set as the whole manifest, then re-run the cohort selftest. Recorded as an open verification gap rather than a demonstrated defect.

---

## Residual risk

- The eight-row contract is prose plus a JSON decision table. Whether the referenced validators exist and implement these rules as read here could not be checked: check-edit-contract.py (C1 command, preregister.json:33) and check-seat-bindings.py (C2 command, preregister.json:42) are outside this seat's declared read paths, and no filesystem search or execution was permitted. Every statement above about checker behavior is therefore a statement about what the contract text leaves unstated, not an observed checker failure.
- The census is four observations from two seats in one prior wave. It can show that structured edit requests exist and that two argument shapes occur; it cannot show prevalence, and no rate, coverage percentage, or "exhaustive" characterization of real edit traffic is asserted here.
- No authority, binding, or settlement data accompanies the census, so the r22 events it records cannot be classified as authorized or unauthorized from this source alone. F6 states the risk of rescoring them under a newer declaration set; it does not claim any particular r22 event was unauthorized.
- Reviewer-cohort accounting covers receipt well-formedness only, by the tool's own scope statement (check-review-cohort.py:20): not request-scope conformity, command nonexecution, reading, chronology, no-harm, or native enforcement.

## Verification gaps

1. check-edit-contract.py and check-seat-bindings.py not readable in this seat; C1 and C2 pass/fail behavior unverified. Action owner: the executor or main integrator.
2. check-review-snapshots.py, the strict evaluator imported at check-review-cohort.py:17, is not a declared read path; F9 rests on call-site inspection only.
3. Round-23 bindings.json and events.json are referenced by the C2 command (preregister.json:42) but were not read; whether the v2 authority record carries a selector field, an argument-shape field, and a declaration-revision id -- the three fields F2, F3, and F6 ask for -- is unknown.
4. No event-level order or causality can be established from the census, per F5; a chronology claim would require the raw transcripts, which are outside this seat's declared read scope and were not opened.
5. Report digest is the supplied declaration; it was not independently computed, per the receipt contract.

Reviewed-SHA256: 19d85129bf0f7fd71f5aea93c35660b21d305150500dc63b58104019851af12a
Predicate: r23-review23expansion
Scope: executed=none
