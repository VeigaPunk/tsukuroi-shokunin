# FxC3Manifest falsification: check-review-cohort.py duplicate handling

Source-only. Nothing executed, fetched, installed, or edited outside this report.

Bottom line: duplicate names, duplicate report paths, and duplicate JSON keys (manifest and settlement) are rejected before classification, as the attack claims. Duplicate source rows are accepted by design and by the source's own fixture, which contradicts the attack premise. Two counterexamples remain: byte-identical reports across rows are counted as separate seats (F3), and the rejection path emits the C3 metric's target value (F1).

## Binding and limits

- Target: `candidate/tools/check-review-cohort.py`, read in full (164 lines, hashline tag ADD3).
- Co-read declared sources: `candidate/tools/check-review-snapshots.py` (full, 278 lines, tag DA85), `preregister.json`, `sources/host-tool-boundary.json`, `candidate/corpus/knowledge/seat-boundary-r22.json` and `.md`. `candidate/tools/_revision.py` was read as an outline only; it is not on the duplicate path.
- SHA-256 pin `34b532dd...4c92e0`: carried from the assignment and NOT recomputed. Computing a digest needs execution, which NO-EXEC forbids. The ADD3 tag is a hashline tag, not a digest.
- Not inspected: `.ufo/waves/round-22/build/reviews.json` and `settlement.json`. They are outside the declared read paths, so no real manifest content was examined.
- Executed: none. No selftest, import, git command, or fetch. Fixture verdicts below are derived from source text. Observed runtime is listed as not run.
- Installs or updates: none. No peers messaged; leaf member, no child dispatch.

## Verdicts on the attack claims

| Claim | Verdict | Source basis |
|---|---|---|
| Duplicate manifest names rejected before classification | Holds | snapshots L72 and L78 raise on `row["name"] in names`; cohort L34-35 re-raises; classification starts at cohort L52 |
| Duplicate manifest report paths rejected before classification | Holds for identical path strings. Does not cover identical report bytes at distinct paths (F3). | snapshots L73 and L80 |
| Duplicate source rows rejected before classification | Does not hold for identical `source` alone: accepted by the source and its own fixture (F2). Holds for identical (source, report) pairs, which share a report path and are rejected. | snapshots L81, L126, L210-222 |
| Duplicate JSON keys rejected before classification | Holds: manifest and settlement, every object depth, escaped forms included | cohort L30-31; snapshots L37 and L61 |
| Rejections precede classification and reads | Holds: no report or source read occurs before the identity loop (snapshots L69-80 precede L85 and L93); rejected results carry no counts or rows (cohort L76, L78) | cohort L30-51 precede L52-65 |
| Rejections are non-accounting results | Does not hold for the metric field (F1): schema and read rejections set `cohort_accounting_mode: 1` | cohort L76, L78 |

## Findings

### F1 - Medium (conditional on gate reading the field): rejections carry the C3 metric's target value

- The field is not uniform across non-accounting exits. Manifest absent returns 0 (cohort L24). Schema rejection (L76) and read rejection (L78) return 1. Path and revision rejections (L149, L156, L158) omit the key.
- `preregister.json` L7 defines C3 as metric `cohort_accounting_mode`, before 0, target 1.
- Consequence: a duplicate-manifest or duplicate-JSON rejection presents the target value. Exit 2 and `status: CANNOT_EVALUATE` (cohort L79) contradict it. A gate reading only the field would pass a rejected run.
- Fixture gap: cohort selftest L112-118 checks code, category, finding ID, and strict exit only. No case asserts the mode field.
- Expected fixture verdict (source-derived): `duplicate-manifest` exits 2 with COHORT-SCHEMA; mode not asserted by the fixture, source value 1. Observed runtime: not run.

### F2 - Premise mismatch: duplicate source rows are accepted by design

- Counterexample to the premise: two manifest rows sharing `source` and `sha256`, with distinct `name` and `report`. Both pass the identity loop.
- `distinct_source_files` (snapshots L81, reported at L126) only has meaning if sources are shared.
- snapshots L210-212 build this exact two-row shared-source manifest (`snapshot/tool.py`, rows One and Two). L221-222 expect exit 2 with only REVIEW-REPORT-MISSING and REVIEW-READ-FAILED. L233-235 expect total 2 and pinned 0. No identity rejection is expected.
- `preregister.json` L9 (C3_bound) requires per-seat accounting. It does not require distinct sources.
- Expected verdict (source-derived): each row is classified independently (cohort L52-62). The attack's expected rejection contradicts the source's own fixture. Observed runtime: not run.
- Either the premise is wrong, or a distinct-source requirement is missing and must be added deliberately. Not a code defect under the current contract.

### F3 - Medium, scope-bounded: identical report bytes are not rejected; one review can count as two seats

- Rejection is keyed on path strings (snapshots L73, L80). No check compares report content across rows. The cohort emits `report_sha256` per row (cohort L65) but never tests it for uniqueness.
- Counterexample (source-derived): rows A and B share source S (digest H) and predicate P, with distinct names and distinct report paths. Both reports are byte-identical and contain exactly one physical `Reviewed-SHA256: H` line, one `Predicate: P` line, and one `Scope: executed=none` line. Settlement has two completed rows with distinct agents and empty errors.
- Expected verdict (source-derived): exit 0, status PASS, `delivered_conformant` 2, `strict_conformance` PASS, no findings. Observed runtime: not run.
- The cohort SCOPE (cohort L19) limits `delivered_conformant` to receipt well-formedness and does not name report independence. This is a stated limit being read as a rejection claim. The code violates no written invariant. It remains a residual unless the round requires independence.

### F4 - Low: duplicate-name guard is single-point

- cohort L37 builds `names` as a set comprehension, which silently collapses duplicates. The only manifest-level guard is strict's identity loop (snapshots L72), surfaced by cohort L34-35. The settlement checks (cohort L42, L50-51) do not guard manifest duplicates.
- If that guard were relaxed, two rows named A would both be classified against the single settlement row for A (L50-51 still pass; L52-62 count both), and `accounted` would equal `total` (L71). Nothing local would catch it.
- Holds today; fragile for maintenance.

### F5 - Low: cross-role path collisions are accepted

- snapshots L72-73 and L80 check `report` only against earlier report values. A report path equal to any row's `source` passes.
- Same-row collision (`source == report`) would need a SHA-256 fixed point: the file must contain its own digest. Infeasible in practice.
- Cross-row collision needs the source file to already contain the other row's exact receipt lines. Low, but unchecked.

### F6 - Low: mislabeled rejections

- A deeply nested manifest raises RecursionError inside `json.loads` (cohort L30). RecursionError is a RuntimeError subclass. L75 does not catch it; L77 does and reports COHORT-READ instead of COHORT-SCHEMA. Still exit 2.
- An absent settlement reaches `json.loads(None)` (L31, then TypeError, then L75) and reports COHORT-SCHEMA. An absent manifest gets COHORT-MANIFEST-MISSING (L23-24); there is no settlement-missing finding.
- Schema rejections drop the strict detail: L76 emits `{'id': 'COHORT-SCHEMA', 'site': 'input'}` and does not say which name or report duplicated.

### F7 - Info: `status` PASS alongside strict receipt failures is by design

- cohort L70 exits 0 when strict receipts fail and no row is unresolved. L73 reports `strict_conformance` FAIL. Selftest `partial-failed` (cohort L96) expects exit 0. This matches C3_bound.
- A reader of `status` alone sees PASS. seat-boundary-r22.md L24 says clean accounting is never a clean strict verdict. Labeling risk only.

## Fixture expectations vs observed runtime

| Fixture | Source | Expected (source-derived) | Observed |
|---|---|---|---|
| cohort `duplicate-manifest` | cohort L108-109 | exit 2, COHORT-SCHEMA | not run |
| cohort `duplicate` (settlement row) | cohort L104 | exit 2, COHORT-SCHEMA | not run |
| cohort `duplicate-json-key` (settlement) | cohort L110 | exit 2, COHORT-SCHEMA | not run |
| strict `duplicate` | snapshots L163, L169 | exit 2, REVIEW-MANIFEST-SCHEMA | not run |
| strict `duplicate-json-key` (manifest) | snapshots L204-208 | exit 2, REVIEW-MANIFEST-SCHEMA | not run |
| strict `read-failed-retains-missing` (shared source) | snapshots L210-235 | exit 2; {REVIEW-REPORT-MISSING, REVIEW-READ-FAILED}; total 2; pinned 0 | not run |
| F3 counterexample | derived; no fixture exists | exit 0; PASS; delivered_conformant 2 | not run |
| F1 mode field on `duplicate-manifest` | cohort L76 | mode 1; not asserted by fixture | not run |

Fixture gaps: no cohort-level manifest duplicate-JSON fixture (strict covers it at snapshots L204-208; the cohort path at L30 is untested). No byte-identical cross-row fixture. No assertion on the mode field. I did not trace every selftest case; only the duplicate-related ones above.

## Residual risk and verification gaps

- SHA-256 pin unverified (NO-EXEC).
- Chronology is not checked. Whether rows were added after dispatch, or population was inflated with shared-source rows and matching settlement rows, is not visible at a single revision (snapshots L128 disclaims chronology).
- Identity uses exact string equality. `A` and `a`, or `agent-A` and `agent-A ` (trailing space), are distinct seats.
- Build manifests and settlement were not examined. `_revision.bind` was not traced; it is not on the duplicate path.

## Checks for main (run once after landing; not run here)

1. `python3 tools/check-review-snapshots.py --selftest`: source-derived expectation for duplicate-related cases is exit 2 with REVIEW-MANIFEST-SCHEMA; `read-failed-retains-missing` expects total 2 and pinned 0.
2. `python3 tools/check-review-cohort.py --selftest`: source-derived expectation for duplicate-related cases is exit 2 with COHORT-SCHEMA.
3. Decide F1 before the C3 gate reads the field. Rejections should not report the target value, or the gate should check exit status and status as well.
4. Decide F2 and F3 against the round contract: whether shared sources or byte-identical reports must be rejected. The current C3 text does not require it.

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3manifest
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
