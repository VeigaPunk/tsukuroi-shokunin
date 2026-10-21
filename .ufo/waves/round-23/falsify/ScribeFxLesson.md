# ScribeFxLesson — round-23 falsify wave (attempt 1) report

Seat: `TsukuroiR23-2.ScribeFxLesson-2` (scribe). Role: draft the falsify-wave section that L1 should append to the candidate lesson; report only. No product code, judge, sibling, fleet, git/jj, route/config, host/package/service/boot surface was touched. No subagent was dispatched (leaf member; lane bounds respected).

## Executed scope and method

Executed scope for this seat: none of the three preregistered commands was run, and no command, hash, list, count, import, compile, test or lint was executed at all. My seat binding carries empty command and fetch lists, which under the contract means NO-EXEC and NO-FETCH, so the only admissible moves were `read` of the four declared documents and this one `write`.

Documents read, and only these:

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/corpus/lessons/round-23.md` (the attacked artifact)
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json` (frozen claims, edit_decisions, limits, sources_opened)
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/r22-closure.json` (outside round-22 closure)
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/godspeed-directive.txt` and `skill://godspeed` (posture)

Everything below is therefore a documentary consistency attack: each finding is a textual comparison between two of those documents, or an arithmetic recomputation over digits printed in the lesson. No finding rests on an executed instrument, and none of the three preregistered commands was re-run. The declared digest is supplied identity; it was not computed, and no file was hashed, listed or counted to validate it. Where a claim can only be settled by running a preregistered instrument, I have written the falsifier for L1 or the canonical judge instead of asserting the outcome.

Axes named for this seat's own work, in the godspeed sense: depth (are the new decisions real and discriminating), operability (does the v2 authority do what the lesson says), calibration (does the round's accounting survive recomputation), coverage (is the claim scope actually covered), freshness (does the artifact describe the state it claims to describe), adjacency (does the round's output connect to the r22 record without rewriting it). The attack strategy was to keep every move cheap and parallel, harm no axis, and let the frontier be whatever the documents actually expose — which turned out to be the boundary between "the lesson's prose" and "the artifacts the lesson points at".

---

## Draft section for L1 to append to the lesson

Intended placement: a new top-level section after `## Mechanics and limits`, titled `## Falsify wave (round-23, attempt 1)`. The text below is the draft. Every statement in it is grounded in the four declared documents read by this seat; no executed result is claimed, because none was executed. The proposed `R23-*` labels are suggestions for L1 to renumber as it sees fit.

### What was attacked

The round-23 candidate lesson at `candidate/corpus/lessons/round-23.md` was attacked on all three registered claims and on the frontier claim, using only the preregistration, the round-22 outside closure, and the lesson's own bytes. C1 was attacked as the claim that eight typed structured-edit authority decisions are validated and discriminating: the preregistration fixes the metric `validated_edit_decisions`, before 0, target 8, and the instrument `python3 tools/check-edit-contract.py --revision <REV>`, but the lesson body never names the eight decisions, never names that metric, and never names that instrument. C2 was attacked as the claim that an explicit schema-v2 report/draft edit authority is prospective and exact, with legacy schema-v1 policy and historical reds unchanged: the lesson states the disposition but never names the metric `structured_edit_mode`, its before/target values, the instrument `python3 tools/check-seat-bindings.py --revision <REV> --manifest ... --events ...`, or the v1/v2 discriminator, and the seat binding payload delivered to this seat carries keys `name`, `root`, `read_paths`, `write_paths`, `edit_paths`, `commands`, `fetches` with no explicit schema-version field, so "legacy v1 bindings unchanged" is not auditable from payload shape alone. C3 was attacked as the claim that both fixed r22 cohorts have an exhaustive per-event/component explanation of the rough-versus-lane path counts: the lesson carries the outside counts (rough build 25 / falsify 33, lane build 23 / falsify 29, from `r22-closure.json` and the preregistration's `path_counts_as_reported`), the derived difference of six, and a citation to a ledger file, but it contains no per-event row, no explained-row count, and no statement of whether "exhaustive" means all fifty-eight rough observations, all fifty-two lane observations, or only the six differences. The frontier was attacked as the claim that the round's reach is worth its cost: the lesson never names the six axis labels that the preregistration and the round-22 closure both use (depth, adjacency, coverage, operability, freshness, calibration), never mentions the three axes the outside verifier left unchanged (coverage, freshness, adjacency), and records four rejects without recording a successor frontier.

The falsifiers are stated in the next subsection as bounded searches for the L1 or the canonical judge to run. This seat ran none of them.

### What survived

The outside-count arithmetic survived recomputation from the preregistration and the closure: rough build 25 minus lane build 23 is 2, rough falsify 33 minus lane falsify 29 is 4, and 2 + 4 = 6, which matches the lesson's R23-RAW-ORDER statement that wave-1 ReconBuild08 and ReconFalsify01 "independently located the same 2+4 events". The gate's rejection of "Rough25/33 minus lane23/29 proves exactly6missing unsafe events" therefore stands on its own terms: the six are accounted for as selector-form differences, not as missing unsafe events.

The no-enforcement posture survived, and survived the strongest available cross-check: the round-22 closure records `native_per_seat_allowlist=false` and the closure agent's own finding that the task schema's `tools` parameter has no restriction semantics, while the lesson keeps "post-hoc metadata authority, never native enforcement" in Mechanics and limits and rejects "Native per-seat prevention from prompt/tool extras". No sentence in the lesson upgrades a contract into a runtime capability.

The quality-trend correction survived: the closure carries `trends.quality = "unchanged"`, and the lesson's R23-QUALITY-TREND row records the author's earlier "improved" label as superseded by the outside assessment, appends rather than rewrites round 22, and refuses to credit an instrument's existence as corpus quality. That matches both the closure note and the preregistration's `outside_round22.scope`.

The receipt-format correction survived against the recorded faults: the closure spot-check names one report that emitted two digest receipt lines and another whose predicate line carried a trailing period, and the lesson's R23-RECEIPT-EXAMPLES responds by telling seats to indent example receipt lines, keep exactly one actual receipt, and never let a source-only string stand as proof of reading.

The Bash-request disposition survived: the closure records that the two requests were read-only `sha256sum` and `wc -l` calls judged non-harmful but still process noncompliance, and the lesson keeps exactly that framing, refusing retrospective authorization.

The two located source quotes survived the preregistered cap: the S085 cell and the S086 sentence are each within the stated twenty-five-word limit, and the S085 source is preserved as data and not as an executed method. The three-claim separability statement in the preregistration is not contradicted by the lesson's three claim descriptions.

### Open defects

First, the lesson binds the wrong revision. Its header says the claims were "landed56c8ba3840cc506e55c1211d7eed0676e69e7ac6 before any successful build spawn", while this falsify wave is stated to run against the integrated landed state `5a25c88b77f52e940bcad87825c4ac1cd529470d`. The header therefore describes a pre-build binding, but presents it as the round's landed state, and nothing in the lesson says which revision the C1, C2 and C3 candidate claims are to be measured at. Smallest in-scope remedy: state both revisions in the header with their roles, one being the preregistration-frozen pre-build binding and the other the post-build integrated state, and bind every metric line to the integrated one.

Second, the retry-spacing row is arithmetically wrong. The row lists the retried payload at 13:28:03, 13:28:48, 13:29:59, 13:31:43, 13:32:58 and 13:34:43 -03 and calls the gaps "45–104 s". Recomputing the consecutive gaps from those six printed timestamps gives 45, 71, 104, 75 and 105 seconds, so the true range is 45–105 s and the stated maximum understates the observed maximum by one second.

Third, the same row contradicts itself on refusal counts. It says the 180 s guard "refused three early calls", then, in the same cell, says "9 attempts in all: the predecessor's 2 refused, mine 1–6 refused, mine-7 spawned 64 at 13:38:13", which is six refusals by this L1's numbering, and the cited receipt set (one `refusal-03.json` plus `attempt-mine-2..6.json`) enumerates six attempts, not three. Smallest remedy: pick the count the receipts support and state it once, then give the gap range as recomputed.

Fourth, the refusal cause is left ambiguous. Mechanics says "First whole64-seat build call was refused at the100-job cap, spawning zero", while the mistakes table attributes the repeated refusals to the 180 s spacing guard, and the same paragraph names a second cap, "The fleet slot cap320 is Main's setting". Eight of nine attempts were refusals and only one refusal cause is explained; two different cap numbers are quoted without saying which one bound. Remedy: name the cap that bound, state the other as context, and attribute each refusal to a cause.

Fifth, C1's substance is absent from the lesson. The preregistration enumerates the eight decisions with their verdicts (DECLARED_EDIT ALLOW, UNDECLARED_EDIT DENY, READ_ONLY_EDIT DENY, WRITE_ONLY_EDIT DENY, OPAQUE_PATCH UNKNOWN, EDIT_TRAVERSAL DENY, EDIT_EXTERNAL DENY, EXPANSION CHECK_EACH); the lesson says only "Eight typed structured-edit authority decisions" and names neither the decisions, nor the metric `validated_edit_decisions` with its 0-to-8 move, nor `tools/check-edit-contract.py`. Of the three preregistered instruments, only `check-path-reconciliation.py` appears anywhere in the lesson. Remedy: add a compact eight-row table of the decision, its verdict and its one-line rule, plus a metrics line naming all three instruments and their before/target values.

Sixth, the eight-row table has a coverage hole and an overlap, which the R23-EDIT-AUTHORITY fix condition ("target/subset/opaque/extra-key/wrapper controls must be discriminating") does not close. A binding that declares a target for edit only, with neither read nor write authority, matches no row: DECLARED_EDIT fails for want of read and write, UNDECLARED_EDIT does not apply because the target is declared, READ_ONLY_EDIT and WRITE_ONLY_EDIT require an authority the binding does not have, and OPAQUE_PATCH, EDIT_TRAVERSAL and EDIT_EXTERNAL are not triggered. Separately, a target declared for edit and read but not write is matched by both DECLARED_EDIT (which fails) and READ_ONLY_EDIT (which denies), and the table states no tie-break or default. Remedy: state the default for an unmatched binding, deny by default unless a row names it, and add one row for the edit-only case, or state explicitly that the edit-only case is subsumed by the read-authority requirement.

Seventh, "validated" is never defined, and two of the eight verdicts are not authorizations. OPAQUE_PATCH resolves to UNKNOWN and EXPANSION resolves to CHECK_EACH, neither of which grants or denies an edit, yet the metric name is `validated_edit_decisions` with a target of 8. Neither the preregistration nor the lesson defines what makes a decision validated. Remedy: define validated as a row with a declared verdict and a discriminating rule, and state explicitly that UNKNOWN and CHECK_EACH are non-authorizing verdicts that still count as decisions; if the intended metric counted only ALLOW and DENY rows, then the reachable target is six and C1's target must be corrected in a later round, never by rewriting this one.

Eighth, the fail-capability standard is not uniform inside the mistakes table. The lesson's rule is "No fix is counted before observed failure controls", but R23-RAW-ORDER cites a killed mutant and specific test names, R23-RETRY-SPACING cites a guard that actually fired, R23-PRELUDE-SHADOW cites only the incident, where the shadowed kernel failed with an AttributeError, which demonstrates the violation is fatal rather than demonstrating the rule detecting a violation, and R23-PATH-UNIT, R23-EDIT-AUTHORITY and R23-RECEIPT-EXAMPLES state fail-capability conditions while citing no executed control at all. R23-PATH-UNIT names three discriminating classes, wrong arithmetic, dropped or duplicate identity, and forged disposition, but only one named unit, `rough-misses-raw-first`, plus the ordering selftest `mixed-raw-range-order`, is evidenced. Remedy: separate the column into fix applied and control pending, and attach one named control per discriminating class or mark the class as uncovered.

Ninth, C3's exhaustiveness cannot be checked from the lesson. The preregistered scope says both fixed cohorts have exhaustive per-event/component explanation, and the lesson's own evidence explains only the six difference events. The lesson contains no per-event row, no explained-row count, and no statement of the denominator, so "exhaustive" is unverifiable from the artifact a reader holds. Remedy: in the falsify section, state the explained-row count against each denominator, fifty-eight rough observations and fifty-two lane observations for the two cohorts as printed, or state that the reconciled scope is the six differences and why that satisfies the registered scope.

Tenth, the frontier is undeclared. The lesson never names the six axis labels, never notes that the outside verifier left coverage, freshness and adjacency unchanged while r23's three claims target depth, operability and calibration, and records four rejects with no successor hypothesis and no statement that the round deliberately declines to aim. Remedy: one paragraph naming the unchanged axes and either the next candidate frontier drawn from them or an explicit record that none was declared.

Eleventh, the path citations inside the lesson are not self-locating. The file lives at `candidate/corpus/lessons/round-23.md`, three directories below the repository root, but it cites `.ufo/waves/round-23/sources/r22-rough-census.txt`, `.ufo/waves/round-23/path-reconciliation.json`, `.ufo/waves/round-23/build/refusal-03.json` and `.ufo/waves/round-23/build/attempt-mine-2..6.json` in repository-root-relative form without saying so, so a reader resolving them relative to the lesson file fails, and the ledger cited for C3 may not exist at the cited path from the candidate tree. Remedy: state once that all internal citations are repository-root-relative, exactly as the report-trailer convention already does for this lane.

Twelfth, the C2 discriminator is unstated, as noted above. The lesson asserts that legacy v1 bindings and violations remain unchanged and that v2 accommodates observed native editor shapes, but it neither states the v1/v2 discriminator nor enumerates the observed shapes that S086 preserves in sanitized form, so both halves of the assertion are unfalsifiable from the lesson alone. Remedy: state the discriminator rule and enumerate the sanitized shape keys S086 preserves, keys and path and call identities only, never bodies.

Thirteenth, a scope tension is left for canonical judgment. The lesson reproduces the outside method's source cell verbatim in its S085 row while the preregistration's limits include "Raw command/fetch body content is not copied". The quoted cell comes from a source snapshot file rather than a transcript command body, so the two readings differ, and the lesson's own declaration that S085 is preserved as data and never executed verbatim is not by itself a resolution. This seat reports the tension verbatim and does not resolve it.

Fourteenth, a minor over-reading sits in the outside disposition. The lesson says the outside admission "reset the streak to0", while the closure records `admitted: true` and `rejection_streak_impact: 0`, which is an impact field, not a streak counter. Remedy: cite the field actually recorded.

Fifteenth, the lesson body carries a systematic missing-space defect class that degrades machine-readability of a corpus artifact: "Baselineae01e50f582016384e620022be38bf5367000e2e", "landed56c8ba3840cc506e55c1211d7eed0676e69e7ac6", "rounds[422]" in two places, "fleet4482c275f9381f219ee4d092e0324d417c3cb1e7", "admitsS083/S084", "expansionunchanged/qualityunchanged/discernmentimproved", "refused at the100-job cap", "fleet slot cap320" and "r22 author quality improved". Remedy: normalize spacing in the header fields at minimum; the lesson's own corpus role makes it a parsed artifact.

### Falsifiers for the L1 or the canonical judge, not executed here

Six bounded searches settle the open defects above. All are read-only instrument runs against the integrated revision and none was performed by this seat.

1. C1 metric reachability: run the edit-contract checker at the integrated revision and read the validated count together with the per-decision verdicts. If the count that includes the UNKNOWN and CHECK_EACH rows is eight and the ALLOW-and-DENY-only count is six, then C1's target is definitionally met only by the broader reading, and the metric definition must be fixed in a later round.
2. C1 table completeness: drive the classifier with three synthetic bindings, edit-only, edit plus read without write, and edit plus write without read, and record which named rule fires for each. The edit-only binding is predicted to produce no named rule.
3. C2 authority and legacy stability: run the seat-bindings checker for both the build and falsify waves at the integrated revision and confirm `structured_edit_mode` moves 0 to 1 while the legacy v1 event counts stay at their recorded values.
4. C3 exhaustiveness and arithmetic: run the path-reconciliation checker at the integrated revision, confirm `unexplained_cohorts` moves 2 to 0, count the ledger's explained rows against the fifty-eight and fifty-two denominators, and recompute the six retry gaps from the printed timestamps.
5. Revision binding: read the lesson at the integrated revision and confirm whether it still names the pre-build revision in its header.
6. Citation resolution: resolve every repository-root-relative path the lesson cites, from the candidate tree and from the repository root, and record which resolve.

---

## Report detail

### Conflicts, reported verbatim

- Lesson header: "Baselineae01e50f582016384e620022be38bf5367000e2e." and "landed56c8ba3840cc506e55c1211d7eed0676e69e7ac6 before any successful build spawn." — versus the wave-supplied integrated landed state `5a25c88b77f52e940bcad87825c4ac1cd529470d`.
- Lesson R23-RETRY-SPACING: "(gaps of 45–104 s), under the ~3-minute backoff" versus the same cell's "it refused three early calls" and "9 attempts in all: the predecessor's 2 refused, mine 1–6 refused, mine-7 spawned 64 at 13:38:13."
- Lesson R23-RETRY-SPACING: "A 180 s guard now refuses a retry before the interval elapses" versus Mechanics: "First whole64-seat build call was refused at the100-job cap, spawning zero" and "The fleet slot cap320 is Main's setting, not a configuration edit by this lane."
- Lesson Mistakes: "No fix is counted before observed failure controls." versus R23-PRELUDE-SHADOW's "The fix is shown able to fail: the shadowed kernel failed, and the reset kernel dispatched." and the three fix rows that cite no control.
- Lesson outside disposition: "reset the streak to0" versus closure fields `"rejection_streak_impact": 0` and `"admitted": true`.
- Preregistration limit "Raw command/fetch body content is not copied" versus the lesson S085 row's quoted source cell.
- Preregistration C3 scope "Both fixed r22 cohorts have exhaustive per-event/component explanation of rough-versus-lane path counts" versus the lesson's evidence covering only the six difference events.

### Gates observed

Read scope limited to the four declared documents plus `skill://godspeed`; write scope limited to this single report path; no fetch; no execution of any command; no delegation; no second report. The declared digest was treated as supplied identity and never computed. The generic tooling directive's installation permission is superseded by this seat's narrower NO-EXEC/NO-FETCH binding, which forbids installations, so no tool was installed or updated and no install record is owed.

### Touched surfaces

One file created: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/falsify/ScribeFxLesson.md`. Nothing else was written, edited, deleted, moved or committed.

### Out of scope for this seat

The three preregistered instruments were not run; the candidate corpus tree outside the lesson was not read; the bindings, events and ledger files were not read, since they are outside this seat's declared read paths and the falsifiers for them are written for the L1 instead; production code, the judge, sibling and fleet files, git and jj state, refs, routes and configuration, host, package, service and boot surfaces were untouched; no round 24 was started; no remote source was fetched.

### Findings carried forward for the canonical judge

The load-bearing ones are the stale revision binding, the eight-row table's edit-only coverage hole and default silence, the undefined meaning of "validated" against two non-authorizing verdicts, the C3 exhaustiveness denominator, the unstated C2 v1/v2 discriminator, the undeclared frontier, and the refusal-cause ambiguity in the retry record. These are documentary and decidable from the registered artifacts without new execution, except items 4 and 5 above, which need the instruments that the L1 owns.

### Artifact paths

- Report: `.ufo/waves/round-23/falsify/ScribeFxLesson.md` (absolute: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/falsify/ScribeFxLesson.md`)
- Attacked lesson: `.ufo/waves/round-23/candidate/corpus/lessons/round-23.md`
- Preregistration: `.ufo/waves/round-23/preregister.json`
- Outside closure: `.ufo/waves/round-23/sources/r22-closure.json`
- Directive copy: `.ufo/waves/round-23/sources/godspeed-directive.txt`

Reviewed-SHA256: b1ed78ac818ed5b1d9bd201de9c3a9c530f95a59944618133c4b51bf3b911199
Predicate: r23f-scribefxlesson
Scope: executed=none
