# FxC3Dead — `absent_dead` mapping vs retained strict missing-report finding

Target bytes: `.ufo/waves/round-22/candidate/tools/check-review-cohort.py`
SHA256 `34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0`
Source-only review. Nothing was executed, imported, or mutated.

**Claim under attack (P).** A settlement seat with `outcome == "failed"` and a non-blank observed
`error` whose report read returns `None` is accounted as `absent_dead`, while the strict
missing-report finding `REVIEW-REPORT-MISSING` remains retained in that seat's `strict_findings`
and in the top-level `strict_receipt_findings`.

## Observed facts

1. **Single mapping site.** `check-review-cohort.py:57-59` reads the report and assigns
   `category = 'absent_dead' if outcome['outcome'] == 'failed' else 'absent_unresolved'` only when
   `report is None`. `check-review-cohort.py:51-52` rejects a `failed` row whose error is blank
   (`'failure without observed error'`), and `:53-54` rejects a `completed` row carrying any error.
   There is no other `absent_dead` assignment in the file. Given `report is None` and a validated
   `failed` row, the category is deterministic.

2. **Retention on the canonical path holds.** `check-review-snapshots.py:98-99` adds
   `REVIEW-REPORT-MISSING` whenever `report is None` and the preceding source read did not raise.
   `check-review-cohort.py:64` stores `one['findings']` verbatim in the seat row and `:72` stores
   `strict_result['findings']` verbatim in the result. On a deterministic `read_bytes` (the CLI's
   `git_read`, `check-review-cohort.py:124-131`) with a readable source, both halves of **P** hold:
   the seat is `absent_dead` and `REVIEW-REPORT-MISSING` is present at both levels.

3. **Counterexample A — retention lost, mapping intact.** `check-review-snapshots.py:85-89` wraps
   only the *source* read; on `OSError`/`RuntimeError`/`TimeoutExpired` it appends
   `REVIEW-READ-FAILED` and `continue`s, so the report read at `:93` never runs and
   `REVIEW-REPORT-MISSING` is never emitted for that review. The cohort loop's own report read at
   `check-review-cohort.py:57` is independent and can still return `None`. Concrete source-visible
   fixture: manifest `{name:'A', source:'s', report:'r', …}`, settlement row
   `{name:'A', outcome:'failed', error:'observed provider failure'}`, `read_bytes('s')` raises
   `RuntimeError`, `read_bytes('r')` returns `None`. Source-derived result: `absent_dead == 1`,
   `seats[0]['strict_findings'] == [{'id':'REVIEW-READ-FAILED', …}]`, top-level
   `strict_receipt_findings` likewise without `REVIEW-REPORT-MISSING`, exit 2 via
   `COHORT-STRICT-UNAVAILABLE` (`check-review-cohort.py:70-71`). The mapping half survives; the
   "strictmissing retained" half is falsified. Fail-closed, so no false PASS.

4. **Counterexample B — the whole partition and every strict finding are discarded.**
   `check-review-cohort.py:57` is the only read in `evaluate` with no `try` around it. If
   `read_bytes(review['report'])` raises, the exception unwinds to `:77-78` and replaces the whole
   result with `{'cohort_accounting_mode': 1, 'findings': [{'id':'COHORT-READ','site':'input'}],
   'scope': SCOPE}`. Concrete source-visible fixture: two reviews `A` (`failed`, non-blank error,
   report `None`) and `B` (`completed`, report read raises `RuntimeError`). The wrapped strict
   evaluator on the identical inputs returns code 2 *while retaining both* `REVIEW-REPORT-MISSING`
   (A) and `REVIEW-READ-FAILED` (B) — behaviour pinned by that tool's own
   `read-failed-retains-missing` fixture, `check-review-snapshots.py:210-222`. Cohort output instead
   has no `absent_dead` key, no `seats`, no `strict_receipt_findings`, no `strict_receipt_exit`, and
   no `total`/`accounted`. This contradicts the C3 bound "account for every declared seat …,
   preserving strict receipt findings" and the seat-boundary rule "mark incomplete trace coverage
   could-not-evaluate, not zero activity": the verdict is fail-closed but the evidence is dropped,
   an asymmetry against the strict tool it wraps.

5. **Fixture coverage gap.** The cohort selftest contains no raising-read case at all. Its `case()`
   helper (`check-review-cohort.py:91-92`) checks only exit code, one category count, a cohort
   finding id, and `strict_receipt_exit`; it never inspects `strict_findings` or
   `strict_receipt_findings`. So retention, the second half of **P**, is asserted by no fixed
   negative fixture. The `dead-missing` case (`:95`) expects exit 0 — i.e. `status: PASS` in cohort
   mode while `strict_receipt_exit` is 1 and `strict_conformance` is `FAIL` (`:72-73`). Segregation
   is field-level, not exit-level: a consumer keying on exit status alone reads PASS.

6. **Adjacent definitional boundary.** `absent_dead` keys on `read_bytes(...) is None`, not on path
   absence. `git show <rev>:<dir>` succeeds for a tree, so a dead seat whose report path is a
   directory maps `delivered_faulty` rather than `absent_dead`; the category is "report path did not
   resolve to file bytes", which the fixture does not distinguish.

## Inference (labelled)

- [INFERENCE] Counterexamples A and B are reachable through the CLI, not merely fixture-only:
  `git_read` raises `RuntimeError` at `check-review-cohort.py:131` when the committed path exists in
  `ls-tree` but `git show` fails (gitlink/submodule entries and similar unshowable objects), and
  `subprocess.TimeoutExpired` is possible at the 30 s bound (`:125`, `:128`).

## Expected fixture verdict vs observed runtime

- **Expected verdict** for the existing `dead-missing` fixture (`check-review-cohort.py:95`):
  exit 0; `absent_dead == 1`; `strict_receipt_exit == 1`; and, by source derivation,
  `seats[0]['strict_findings'] == strict_receipt_findings == [REVIEW-REPORT-MISSING]`.
  This matches **P** on the canonical single-seat path.
- **Observed runtime:** none. `executed=none` — no selftest, import, or command was run, per seat
  binding. Every verdict above is derived solely from the named source bytes; counterexample A and B
  are expected source-derived outcomes, not measurements.

## Verdict

**P holds** as a bounded rule on the canonical path: deterministic `read_bytes`, readable source,
missing report, failed row with non-blank error. It is **falsified as a general claim** by
counterexample A (missing-report finding silently absent while `absent_dead` is still emitted) and
by counterexample B (the entire cohort partition and all strict findings discarded on a raising
report read). Both failures are exit-code 2, so neither converts a strict fault into a pass; the
defect is loss of retained evidence, plus an unasserted retention half in the fixture suite.

## Remaining unknowns

- Whether any landed round-22 `build/reviews.json` or `build/settlement.json` actually contains a
  seat hitting A or B. Those paths are outside this seat's declared read_paths and were not read.
- `_revision.py` binding behaviour was not examined beyond confirming `git_read` is the CLI reader;
  revision-binding failure paths (`main`, `:156-158`) are out of scope for this predicate.

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3dead
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
