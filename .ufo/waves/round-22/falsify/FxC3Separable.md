# FxC3Separable — round 22 C3 separability falsification

Seat: FxC3Separable. Target: `.ufo/waves/round-22/candidate/tools/check-review-cohort.py` (164 lines), declared digest 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0. Source-only: no execution, no fetch, no production edits. The digest is the assignment declaration; NO-EXEC forbids local recomputation, so the receipt below records the declared digest, not a measured one.

## Predicate under attack

Three conjuncts:

1. C3 reads no C1/C2 content.
2. `delivered_conformant` is explicitly receipt-only.
3. Audit contradictions are separate.

## Evidence

### 1. Content separation — holds

- Cohort imports (lines 3–14) are stdlib plus `_revision`; lines 17–18 dynamically load only `tools/check-review-snapshots.py`. A grep of the whole file for boundary|seat|audit|event|binding|contradict|violation|request matches only settlement `seats` (38, 41, 74) and the receipt literal `executed=none` inside the scope string (19). No `check-boundary-contract`, no `check-seat-bindings`, no `bindings.json`, no `events.json`, no decision-table key.
- `_revision.py:30–39` imports stdlib only; its docstring (26–28) states the module only reads git ref/commit state. `check-review-snapshots.py:2–15` imports stdlib plus the same helper; its output scope (128) is snapshot and predicate declarations, explicitly "not proof of reading, chronology or command nonexecution".
- `main` reads exactly three classes of bytes at the bound revision (152–154): the manifest, the settlement, and per-row `source`/`report` paths through the same `git_read` closure (55; strict 85 and 93). Source bytes are consumed only by `hashlib.sha256` (strict 90) and are never parsed as policy.
- Every git subprocess runs under `_revision.clean_env()`, which strips ambient `GIT_*` state (cohort 125, 128).

Bounded reason it holds: C3's entire input surface is the two CLI paths plus manifest-declared source/report paths, and the only consumer of source bytes is a digest comparison. There is no code path that opens a C1/C2 artifact for semantics. Shared `_revision`/git plumbing means repository faults move all three tools to CANNOT_EVALUATE together, which is substrate sharing, not content reading. Residual, non-semantic case: a planner could point a manifest `source` at a C1/C2 artifact and C3 would hash its bytes; that still consumes no C1/C2 field or verdict.

### 2. Receipt-only derivation — holds for the category, fails the "explicitly" qualifier at the machine boundary

- Line 55 reads the report; 56 builds a single-review manifest; 57 calls `strict.evaluate` on that one review. Line 61 sets `delivered_conformant` iff `one_code == 0`. Settlement `outcome` enters only the absent branch (58–59); `agent` and `error` enter only stored row metadata (63–64). Nothing request-shaped feeds the category.
- Strict returns 0 only when: source digest matches (90), report decodes UTF-8 (102–105), exactly one digest line equals the declared value (108–114), exactly one predicate line equals the declared value (110–116), and exactly one scope line equals the literal `Scope: executed=none` (112–118).

Concrete source-visible counterexample to "explicitly": line 19 denies request-scope conformity, reading, no-harm, and native enforcement, but omits the one non-claim that strict itself makes twice — command nonexecution (strict 2 and 128). The literal C3 validates is precisely the nonexecution declaration (strict 117). Therefore a seat that made an observed forbidden request but delivered a clean receipt is counted `delivered_conformant` at 61, and a JSON-only consumer of the `scope` field receives no in-band denial that the nonexecution declaration was verified. The round-22 knowledge file (seat-boundary-r22.md, "What is enforced and what is not") carries the contradiction rule, but that text is not in the machine-readable output. The receipt-only *semantics* hold; the *disclaimer* is incomplete for the claim this round is about.

### 3. Audit separation — holds structurally, with one producer obligation

- C3's `findings` list receives only cohort-local ids: COHORT-MANIFEST-MISSING (24), COHORT-UNRESOLVED and COHORT-STRICT-UNAVAILABLE (66–69), COHORT-SCHEMA (76), COHORT-READ (78).
- Strict findings are copied verbatim into `strict_receipt_findings` (72) and per-row `strict_findings` (64); none are filtered, merged, or converted.
- Settlement rows are validated with `row.get` (42) and no key-set equality, so extra keys are tolerated. That is a natural separate channel for sanitized request metadata, and it never enters a C3 computation.
- Constraint: `completed` with non-empty `error` raises (46–47) and the whole run becomes CANNOT_EVALUATE (76). `error` is reserved for failure attribution; an audit anomaly encoded there poisons the entire accounting instead of being reported separately. Separation is fail-closed but depends on the settlement producer honoring the channel split.

## Bounded calibration caveats (no verdict change, stated as contradictions)

1. Absent settlement is reported as COHORT-SCHEMA: `git_read` returns `None` for a path absent from the committed tree (130), `json.loads(None)` raises TypeError at 31, caught at 75–76. Absent manifest instead gets a dedicated FAIL finding and mode 0 (23–24). One input-completeness class carries two labels.
2. `cohort_accounting_mode` is 0 only when the manifest is missing (24) and 1 on schema/read failures (76, 78). The preregister metric is the scalar field; a consumer reading only that field sees 1 on a run that produced no accounting. `status` and exit code disambiguate, and per-seat encoding errors still produce real partial accounting, so forcing 0 would be worse — this is a consumer-contract risk, not a defect to "fix" blindly.
3. `delivered_faulty` collapses strict exit 1 and exit 2 (61; the encoding fixture at 103 encodes this expectation). The row preserves `strict_exit` and `strict_findings`, so no data is lost, but the four-way category alone does not distinguish a faulty receipt from an unevaluable one.
4. Denominator: the population is `reviews` only (36–37, 71). A seat dispatched but omitted from reviews.json is outside C3, and the tool can still PASS with `accounted == total`. Freezing reviews.json pre-dispatch is checklist item 1 in the knowledge file, not a C3 check, and preregister.json carries no digest of reviews.json. This is the structural cost of conjunct 1: no C1/C2 roster cross-check exists by design.

## Expected fixture verdict vs observed runtime

Hand-traced every declared selftest case against the source; each declared expectation is consistent with the code path.

| Case | Declared expectation | Source-derived consistency |
|---|---|---|
| clean | 0, delivered_conformant, strict_exit 0 | consistent (55–61, strict 90–118) |
| dead-missing | 0, absent_dead, strict_exit 1 | consistent (58–59) |
| partial-failed | 0, delivered_faulty, strict_exit 1 | consistent (61) |
| missing-unresolved | 1, absent_unresolved, COHORT-UNRESOLVED, strict_exit 1 | consistent (59, 66–67) |
| period / predicate / digest | 0, delivered_faulty, strict_exit 1 | consistent (strict 113–118) |
| duplicate-receipt | 0, delivered_faulty, strict_exit 1 | consistent (strict 108–114) |
| crlf | 0, delivered_conformant, strict_exit 0 | consistent (strict physical_lines) |
| unicode | 0, delivered_faulty, strict_exit 1 | consistent (scope equality, strict 117) |
| encoding | 2, delivered_faulty, COHORT-STRICT-UNAVAILABLE, strict_exit 2 | consistent (strict 102–105, 121; cohort 68–70) |
| dropped / duplicate / unknown / false-death | 2, COHORT-SCHEMA | consistent (38–51, 75–76) |
| manifest-missing | 1, COHORT-MANIFEST-MISSING | consistent (23–24) |
| duplicate-manifest | 2, COHORT-SCHEMA | consistent (strict schema gate, 34–35) |
| duplicate-json-key | 2, COHORT-SCHEMA | consistent (31, 75–76) |

Expected selftest verdict: PASS, cases 18, failed 0. Observed runtime: none — executed=none, so no PASS/FAIL was produced or observed.

Unexercised branches (fixture gaps, not proven behavior): outcome `unknown` (the case named unknown at 104 renames the seat, and missing-unresolved uses `completed`); a settlement document absent at the revision; settlement extra keys; the COHORT-READ path (77–78); and source-pin mismatch (strict 90) with a present report — the digest fixture mutates the report's digest line, not the source bytes.

## Second-order effects

- Runtime: no C1/C2 module is imported or executed inside C3, so C1/C2 changes cannot move C3 rows. `strict.evaluate` runs once for the full manifest (33) and once per seat (57), so snapshot semantics have one implementation and one failure mode; a snapshot change moves all rows and `strict_conformance` together by design.
- Contract: `status`, `strict_conformance`, `strict_receipt_exit`, per-row `strict_findings`, and `scope` are separate fields; no field merges an audit verdict. The settlement contract reserves `error` and tolerates extra keys.
- Substrate: reviews.json is the sole denominator; the seat roster is invisible; git history is the only audit trail for post-hoc population edits.
- Verification: the PASS-with-failed-strict-receipt path is directly encoded (period/predicate/digest expect code 0 with strict_exit 1), so the docstring promise "without converting strict receipt faults to passes" is exercised at the accounting level. The gaps listed above are not.

## Affected axes

- Calibration (+): the machine-readable scope currently omits the nonexecution denial that the validated literal invites.
- Operability (0/+): aligning the JSON scope with the knowledge doc removes an inferential gap for JSON-only consumers; no schema shape change.
- Depth, adjacency: unchanged; C1/C2 are neither read nor modified.

## Proposed move (one, bounded)

Change only the scope literal at line 19 to add the missing non-claim, matching strict 128:

`'Cohort accounting of strict receipt declarations only; delivered_conformant means receipt-well-formed, not request-scope conformity, reading, command nonexecution, no-harm or native enforcement.'`

No category, finding, exit-code, or fixture change. It makes the JSON deny the inference that `delivered_conformant` confirms `executed=none`, without pretending to enforce anything.

Risks:

- Exact-string consumers of `scope` would see a new value. None appear in this seat's declared read set, but the seat cannot search outside it.
- The edit must land before the prereg measurement revision, or the measured JSON lacks the clause; any golden output pinning C3 stdout would need regeneration (not visible here).
- Documentary only: it must never be cited as preventive enforcement or as proof of nonexecution.

## Verification for main (not performed here)

1. `python3 tools/check-review-cohort.py --selftest` → expect exit 0, 18 cases, 0 failed; a string-only edit should not move any fixture.
2. At the landed revision, run the prereg C3 command and inspect: exit code, `.status`, `.cohort_accounting_mode`, `.strict_conformance`, and `.scope` containing "command nonexecution".
3. Confirm the four counts sum to `.total` and that strict findings remain only under the separate strict keys.

## Residual unknowns

- The declared digest was not recomputed under NO-EXEC; all citations are to the file read at the declared absolute path.
- Whether round 22's reviews.json pins this file with the same digest is outside this seat's read paths.
- No runtime output was observed or produced.

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3separable
Scope: executed=none

Lane bounds: leaf member — no subagent dispatch.
