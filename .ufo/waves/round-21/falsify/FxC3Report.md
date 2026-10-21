# FxC3Report — C3 `check-review-snapshots.py` falsify review (round 21)

Seat: TsukuroiR21.FxC3Report (leaf, NO-EXEC — read/grep/glob + this report write only; no bash/eval/import/compile/execution, no installs attempted, none needed; pacman transactions remain paused host-wide and this seat required none).

Review axes named: (a) missing-report detection correctness (the assigned predicate), (b) finding/evidence fidelity under adjacent failure classes, (c) denominator and count honesty, (d) disclosed-scope honesty. Everything below is a **source prediction from the pinned candidate bytes**; nothing was executed, so no runtime observation exists — each claim is labeled prediction or observation-of-source.

## Identity and dependencies

- Primary reviewed file: `tools/check-review-snapshots.py`, candidate revision `0a14952b59d20179e1c813af58befaecd6992a17`.

Reviewed-SHA256: 736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e

(standalone receipt above; byte digest of the primary file. Cross-checked against `candidate-files.json` entry for `tools/check-review-snapshots.py`, which records the same sha256 and revision — observation.)

- Auxiliary snapshot dependencies, all read from the frozen candidate tree only (never from live worktree paths): `tools/_revision.py` (imported at `check-review-snapshots.py:14`; supplies `bind`, `clean_env`, `RevisionError`), `candidate-files.json` (predispatch digest inventory), `corpus/lessons/round-21.md` (R21-MISSING13 / R21-REVIEW-BYTES; build-manifest disclosure), `SCORECARD.md` round-21 C3 row (preregistered counting command and metric), `corpus/QUALITY.md` criteria 42/44. No moving draft or production file was read for any verdict. One repo-root grep incidentally matched `.ufo/reports/round-19/mori.md` (historical, outside the candidate tree); it was excluded from evidence and is not a dependency.

## Predicate verdict — C3-report missing

**Prediction (from source control flow, not run): a manifest row whose report path is absent at the bound revision produces finding `REVIEW-REPORT-MISSING` with `site` = the row name, status FAIL, exit code 1 — exactly the disclosed expectedred1 for the dead ScribeDecision row.**

Evidence chain (all line numbers are the pinned candidate file):

1. `main` binds the revision then calls `evaluate(git_read(binding.sha, args.manifest), lambda path: git_read(binding.sha, path))` (`:153-156`). The `read_bytes` callback is `git_read` against the landed commit, so reports come from the pinned snapshot, not the worktree — consistent with the "exact pinned snapshots only" review contract.
2. `git_read` returns `None` exactly when `git show` fails and `git ls-tree` succeeds with empty output for the path (`:89-100`) — i.e., a genuinely absent committed path.
3. In `evaluate`, a `None` report adds `REVIEW-REPORT-MISSING` (`:63-64`) and the row cannot reach `pinned` (`:77-78` increments only when zero findings were added for that row). `code = 1 if findings else 0` (`:79`); `main` prints the payload and returns that code (`:164-165`), `sys.exit(main())` (`:168-169`). Any code ≥1 is non-green; the gate cannot pass while any report is missing.
4. Corollaries checked, no bypass found:
   - A present-but-empty (`b""`) report also fails (decodes, then all three exact-line checks mismatch, `:66-76`) — an empty stub is never a pass.
   - A substitute report under a different row cannot clear the dead row: names and report paths must be unique across rows (`:44-54`), and the dead row's own report check is independent (`:57-76`).
   - `total = len(reviews)` (`:55`) keeps every declared row in the denominator, so the retained dead ScribeDecision row stays counted: predicted payload `pinned_reviews=63, total_reviews=64` with one `REVIEW-REPORT-MISSING` for it. This matches the build-manifest disclosure that all 64 rows are retained with no dropped denominator or substitute (`corpus/lessons/round-21.md` § Build critique dispositions, CritNoHarm bullet), and the preregistered metric "pinned_reviews0→every delivered round21 review, with preregistered snapshot SHA-256 and exact predicate" (`SCORECARD.md` Round 21 table, C3 row).
   - The bundled selftest already pins this behavior: the `missing-report` case expects code 1 with exactly `REVIEW-REPORT-MISSING` (`:112`), so the gate is fail-capable for this class by its own control.

**Predicate result: HOLDS — source-verified. No execution was performed; L1 alone runs final checks.**

## Findings (severity-ordered)

### F1 — Medium: a later-row hard read failure discards earlier missing-report findings and demotes FAIL to CANNOT_EVALUATE

- `git_read` raises `RuntimeError` for any committed path it cannot read (`:99`). `evaluate` catches only `(ValueError, TypeError, UnicodeError)` (`:80`), and `read_bytes` for source and report runs inside the per-row loop (`:59-60`), so a `RuntimeError` from any later row propagates out of `evaluate` uncaught. `main` then catches `(OSError, RuntimeError, UnicodeError, subprocess.TimeoutExpired)` (`:161`) and **replaces** the accumulated code/payload wholesale with a single `E-READ` CANNOT_EVALUATE finding (`:162-163`).
- Predicted consequence: if the ScribeDecision row precedes any row whose committed source/report read hard-fails, the collected `REVIEW-REPORT-MISSING` evidence is erased from the output; the payload no longer names the missing report and the status changes from FAIL(1) to CANNOT_EVALUATE(2). Exit stays non-zero, so the gate stays red, but R21-MISSING13's "keep missing reports visible" property is lost in that payload and per-row attribution is destroyed.
- Trigger surface is wider than full absence: `safe_path` (`:20-23`) admits glob metacharacters; a row naming e.g. `a*b` makes `git ls-tree` (pathspec semantics) match a real file while `git show rev:a*b` treats it literally and fails — producing exactly this RuntimeError path instead of `REVIEW-REPORT-MISSING`.
- Adjacent same-shape defect: a present report that is not valid UTF-8 raises `UnicodeDecodeError` at `:66`; that is a `UnicodeError`, so the whole evaluation aborts to a single finding `REVIEW-MANIFEST-SCHEMA` with `str(exc)[:100]` (`:81`) — a broken **report** is mislabeled as a **manifest schema** defect, and every later row's findings are lost (earlier-row findings survive only because the payload is assigned, not reset, on this path). Both are predictions from control flow; neither arm was executed.

### F2 — Low: `safe_path` cannot reject a committed tree at the report path (classification noise, not a bypass)

- `safe_path` rejects traversal, absolute, empty and `.`/`..` components but has no type knowledge (`:20-23`). For a row whose `report` names a committed directory, `git show rev:<dir>` succeeds and prints the tree listing (`:90-100`), so the report counts as present and the row gets three MISMATCH findings (`:71-76`) instead of `REVIEW-REPORT-MISSING`. Outcome is red either way; the missing-report predicate itself is unaffected, but the finding ID misclassifies an absent report as a wrong one, which pollutes evidence the same way F1 does at lower severity.

### F3 — Low/residual (disclosed): report bytes are never bound

- The sha256 is bound only for the source snapshot (`:61`); the report is checked for presence plus exactly three declared lines (`:63-76`). A fabricated minimal file containing those three lines passes as a pinned review. This is the preregistered contract boundary, not a defect against the claim: the payload's own scope string says "primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution" (`:86`), QUALITY42 states a receipt is a declaration not proof of reading, and the round-21 gate table rows the same for C3. Recorded as residual risk that must stay in any C3 green claim.

### F4 — Low/residual (disclosed): the denominator is the manifest itself

- `total = len(reviews)` (`:55`); a dispatched seat absent from `reviews.json` leaves no trace inside this gate, and there is no reconciliation against a dispatch registry. Keeping all 64 rows (including the dead seat) in the manifest is a process control outside this file (`corpus/lessons/round-21.md` CritNoHarm disposition). The counts the gate does emit are honest for the declared population: `pinned_reviews` counts rows with zero findings (`:77-78`), `distinct_source_files` is reported beside review count (`:56, :84`), and neither inflates or hides a declared row.

### F5 — Info: output-schema drift on error paths

- Success-path payloads carry `distinct_source_files/pinned_reviews/total_reviews/findings/scope` (`:83-86`) plus revision fields (`:157`); the two `main`-level CANNOT_EVALUATE payloads (`:150-151, :158-163`) and the evaluate-internal schema payload (`:81-82`) carry different key sets (no `total_reviews`, no `scope` string). A consumer scripting against CANNOT_EVALUATE output cannot rely on the same keys. Cosmetic; no gate outcome changes.

## Checked and found harmless (predicate-relevant negatives)

- An entirely missing manifest file is FAIL(1) with `REVIEW-MANIFEST-MISSING` (`:32-34`), not CANNOT_EVALUATE — deliberate-looking split; does not touch the row-level predicate.
- Trailing extra lines after the declared ones are caught: each check uses exact list equality (`:71-76`), and the selftest's `duplicate-digest` case pins the doubled-digest red (`:114-117`).
- Predicate smuggling: `\r`/`\n` are rejected in the manifest predicate (`:51`); `splitlines()` (`:67`) additionally splits on `\v \f \x1c-\x1e \x85 \u2028 \u2029`, so any control character not rejected at `:51` still forces a `REVIEW-PREDICATE-MISMATCH`. I traced each split character class: no false-pass route exists.
- `--selftest` covers the missing-report class with the exact expected id and code (`:112`), so the fail-capability demanded by R21-MISSING13 is selftested inside the gate, not merely asserted.

## Residual risk and verification gaps

- F1 is the only finding that degrades evidence fidelity while keeping the gate red; if L1 wants per-row missing-report visibility guaranteed, `evaluate` should catch the read failure per row (or `git_read` should be total) so `REVIEW-REPORT-MISSING` already collected survives. Fix is a candidate-source change; this seat makes no production edits and offers it as a recommendation only.
- All results are static predictions; per the seat contract and the round's scope, no command, selftest, or mutant was run, and no runtime receipt exists for any claim in this report. L1's final measuring run is the only execution authority.
- The gate's own scope disclaimer (`:86`) and QUALITY42/44 bound what a C3 pass may claim; any admission language must keep "declaration, not proof of reading/nonexecution" attached.

Scope: executed=none
