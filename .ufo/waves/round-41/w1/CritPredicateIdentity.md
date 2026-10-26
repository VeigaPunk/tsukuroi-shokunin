VERDICT: defect-found

Item G-7 (predicate identity, C1 and C2). Read-only: no counter was run and no lane file was touched except this
report and its receipts dir. The predicate *sentence* is character-for-character identical in all four declared
places for both claims; the *evaluated condition* is not literally that sentence, and several behavioural conjuncts
that decide PASS are folded into the named variables and appear only in prose. No numeric value in the before
receipts changes because of this.

## 1. What is identical (observed)

C1, sentence `baseline_pass == 1 and neutral_pass == 3 and decoy_pass == 1 and mutants_applied == 13 and survivors == 0 and params == 4`:

| Location | Result |
|---|---|
| SCORECARD.md at d8b4d52, line 2465, Target column code span (git show d8b4d52:SCORECARD.md) | exact match to the literal (Python span extraction `span == lit` True; no non-ASCII in span) |
| counter docstring tools/score-selftest-mounts-r41.py:41-42 | match after whitespace normalisation (`== literal` True) |
| counter `predicate` literal tools/score-selftest-mounts-r41.py:298-299 (ast) | the literal itself |
| .ufo/waves/round-41/before/c1-before.jsonl:6 (`json.loads(...)["predicate"]`) | `== literal` True |

C2, sentence `rules_verified == 8 and verdicts_ok == 8 and host_ok == 6 and source_ok == 1 and duplicate_rows == 0 and duplicate_headings == 0 and novelty_base_hits == 0`:

| Location | Result |
|---|---|
| SCORECARD.md d8b4d52, line 2466, Target code span | exact match (`span == lit` True; no non-ASCII) |
| tools/check-package-anatomy-r41.py:34-35 docstring | match after whitespace normalisation |
| tools/check-package-anatomy-r41.py:314-315 literal | the literal itself |
| .ufo/waves/round-41/before/c2-before.jsonl:61 | `== literal` True |

The declaration section is unchanged at the lane tip: `diff` of the `## Round 41 — declaration` section between
d8b4d52 and 71851d6 shows only the 12 C1-control lines appended after the table (`28a29,40`); both claim rows are
byte-identical.

Byte identity of the counters at 71851d6 vs e479fdc — confirmed:

```
$ git -C <lane> rev-parse 71851d6:tools/score-selftest-mounts-r41.py 71851d6:tools/check-package-anatomy-r41.py
6351197f8d8ebd3311a06d93eb47d720b350cb82
325da18f027989c12ee0aaf4555e38d420d7bb2a
$ git -C <lane> rev-parse e479fdc:tools/score-selftest-mounts-r41.py e479fdc:tools/check-package-anatomy-r41.py
6351197f8d8ebd3311a06d93eb47d720b350cb82
325da18f027989c12ee0aaf4555e38d420d7bb2a
```
Worktree `sha256sum` is 8306d999…07355c and c83e29a4…ac1819f, matching the declared digests, and
`git status --porcelain -- <both counters>` is empty. Receipts: `.ufo/waves/round-41/w1/CritPredicateIdentity/receipts.txt`.

## 2. Differences found (the defect)

C1:

1. **The evaluated expression is not the sentence** (tools/score-selftest-mounts-r41.py:295-296, `ast.unparse`):
   `baseline_pass == 1 and neutral_pass == len(NEUTRAL) and (decoy_pass == 1) and (m_applied == len(MUTANTS)) and (not survivors) and (n_params == 4)`.
   `len(NEUTRAL)==3`, `len(MUTANTS)==13` (M1-M9, H5, H6, H9, H10; imported module), `not survivors` ≡
   `survivors == 0`, and `n_params` is the local written as `params` (line 302). At these frozen blobs the truth
   table is identical, but the receipt's predicate string would misdescribe any re-frozen counter whose list
   lengths changed — the code would PASS with 4 neutrals while the receipt still printed `neutral_pass == 3`.
2. **`survivors == 0` hides the kill definition.** A mutant is killed only if the run exits nonzero, its summary
   carries the baseline's case count, ≥1 stderr `FAIL <label>` names a label the baseline printed as PASS
   (`killed()`, lines 195-198), **and** a second run fails a common baseline label — `row['killed'] =
   killed(res[name], base) and bool(res[name].get('confirmed'))` (line 287), confirmation at 264-272. A mutation
   that genuinely fails once but flakes on the confirm is a survivor. This is declared in the docstring
   (lines 18-21) and in the SCORECARD Counter cell ("kill attribution on baseline labels confirmed by a second
   run"), but not in the predicate sentence.
3. **Retry-once is a measurement rule the sentence omits.** A failed baseline/capture/neutral/decoy run is re-run
   once serially and only the second verdict is kept (`# one serial retry`, lines 248-267; docstring 22-23).
   Baseline_pass, capture, neutral_pass and decoy_pass can all be values of a second run.
4. **`params == 4` silently entails capture_pass == 1**: `params` is computed only when the capture run passed
   (lines 273-275); `capture_pass` is recorded in the receipt (c1-before.jsonl:16) but is not a predicate conjunct.

C2:

5. **`ok` uses aliases** (tools/check-package-anatomy-r41.py:394-395): `verified`, `dup_rows`, `dup_heads`,
   `nov_total`. The record re-emits them under the sentence's names (lines 396-398), so identity holds at the
   receipt level, not in the expression.
6. **`verdicts_ok == 8` definition is absent from the sentence** (line 321): `sum(... if vd[k]['holds'] and not
   vd[k]['fails'])` over the 8 REQUIRED rows — ≥1 `holds` file and 0 `fails` files; `partly` is allowed when a
   `holds` exists and malformed files are ignored (parse at 269-286). Declared in docstring 18-21; not in the
   predicate.
7. **`source_ok == 1` definition is absent** (lines 327-331): non-empty header S-id set, every header id `mined`
   and naming the entry, and **any one** opened `2026-10-26` (`any(...)`, not `all`). The `any` is weaker than the
   declaration's "on rows S227-S236 opened this round": a `source:` line mixing one new row with old mined rows
   satisfies `source_ok`, though each *row-cited* id must independently be new+mined+opened (upstream check inside
   `rules_verified`). Not exercised at base (`source_ok 0`).
8. **The declaration target adds PASS locations outside the predicate**: C1 "at the C1 implementation commit and at
   the round tip" (SCORECARD.md:2465), C2 "at the commit that lands the wave's verdict files and at the round tip"
   (SCORECARD.md:2466). The before receipts were taken at revision `0e5805a1…` (c1-before.jsonl:4, c2-before.jsonl:4),
   so as written the predicate is necessary but not sufficient for the declared target.

## 3. Calibration

No PASS/FAIL flip is available from this finding at the pinned blobs: the conjunction's six (C1) / seven (C2)
conjuncts are the same set under the same names, values 13/3/4/8/6 check out, and the before receipts' predicate
fields equal the literal. What is defective is the identity of the *expression and definitions* with the one-line
sentence, not the round's measurements. Counter values required by the predicate (survivors 4, params 0; rules 0,
verdicts 0, host 0, source 0) match the "Before at base" cells and the receipts.

## 4. Impacted axes

- C1 operability: predicate attribution/documentation (kill confirmation, retry, capture) — definitional.
- C2 depth (sourced): `verdicts_ok` and `source_ok` definitions, and the `any` in `source_ok` vs the prose — definitional.
- No axis value moves; nothing here makes either counter unsound at its frozen revision.

## 5. Smallest safe correction

- Do not edit the frozen counters: the sha256 pins are the freeze, and both blobs are already identical at
  e479fdc and 71851d6.
- For this round, append a definitional line to the declaration (append-only, as the C1 control block already was):
  "`survivors` counts a mutant killed only when its run exits nonzero with the baseline's case count and a stderr
  FAIL that names a baseline PASS label, and a confirm run fails a common baseline label; a failed non-mutant run
  is retried once; `params == 4` requires a passing capture; `verdicts_ok` = ≥1 `holds` and 0 `fails` per row;
  `source_ok` = every header S-id mined and naming the entry, at least one opened 2026-10-26."
- On the next re-freeze, make `ok` spell the sentence's literals/names (3, 13, `survivors == 0`, `params`,
  `rules_verified`, `duplicate_rows`, …) so the expression cannot drift from the receipt string.
- For C2, either require every header S-id opened `2026-10-26` (matching "rows S227-S236 opened this round") or
  narrow that prose; no live effect on the current entry, which is absent at base.

## 6. Not done

- I did not run either counter; the item asks for a textual/semantic comparison and the before receipts are the
  frozen evidence. No `--jobs` run was started, so no host load was added.
- I did not evaluate the counters' correctness otherwise (mutant strength, fixture capture soundness, verdict
  quality); those belong to the C1/C2 execution and review seats.
