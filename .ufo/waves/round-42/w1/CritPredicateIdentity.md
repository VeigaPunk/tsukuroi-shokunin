VERDICT: supports

# G-3 — predicate identity (C1, C2), round 42 w1

Seat: CritPredicateIdentity. Read-only review; no lane file written except this report and the
receipts in `.ufo/waves/round-42/w1/CritPredicateIdentity/`. Scratch
`/fast/scratch/hyaku/tsukuroi-r42/CritPredicateIdentity` removed at exit. No counter was run
(identity is textual/static; running is wave scoring and the host is loaded). No tool was installed.

Item: for C1 and C2, compare character for character the predicate in `SCORECARD.md`
"Round 42 — declaration" at `a84fc9dec860f8bea516dff7ddfdc98223cdae52`, the counter docstring, the
`predicate` string the counter prints, the condition the code evaluates (`verdict = …`), and the
`predicate` field of `.ufo/waves/round-42/before/c1-before.jsonl` / `c2-before.jsonl`; and confirm the
counters at `f50c28d83e1832ecd7eba765caace531f45d6b27` are byte-identical to the freeze.

## Result: identical on all five surfaces, both claims

Receipt: `.ufo/waves/round-42/w1/CritPredicateIdentity/compare-predicates.py` →
`compare-output.txt` (run with `python3`, output ends `RESULT: IDENTICAL`).
The script reads every source with `git show`/file read and does no normalisation other than
stripping the `PASS iff ` wrapper, a trailing full stop, and the two expression-level aliases in the
code condition (see §"Code condition" below).

### C1

| Surface | Location | Text |
|---|---|---|
| declaration | `SCORECARD.md:2573` at `a84fc9d` (bold target cell) | `PASS iff cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1` |
| docstring | `tools/score-size-invariance-r42.py:42-43` | same sentence + trailing `.` |
| printed `predicate` | `tools/score-size-invariance-r42.py:369-370` | `cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1` |
| before receipt | `.ufo/waves/round-42/before/c1-before.jsonl:2` | byte-identical to the printed literal |
| code condition | `tools/score-size-invariance-r42.py:365-366` | `len(CASES) == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1` |

Observed (`compare-output.txt`): `decl_body == docstring_body: True`,
`decl_body == printed_literal: True`, `decl_body == before_receipt: True`,
`verdict_expr(aliased) == sentence: True`, `conjunct_count_match: True` (5 conjuncts each).
The only character-level difference anywhere is the docstring's trailing full stop (the declaration
carries markdown bold `**…**` instead); the conjunct bodies are byte-identical.

### C2

| Surface | Location | Text |
|---|---|---|
| declaration | `SCORECARD.md:2574` at `a84fc9d` (bold target cell) | `PASS iff rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1 and verdicts_ok == 5 and novelty_base_hits == 0` |
| docstring | `tools/check-scrub-record-r42.py:29-31` | same sentence (wrapped) + trailing `.` |
| printed `predicate` | `tools/check-scrub-record-r42.py:244-245` | `rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1 and verdicts_ok == 5 and novelty_base_hits == 0` |
| before receipt | `.ufo/waves/round-42/before/c2-before.jsonl:2` | byte-identical to the printed literal |
| code condition | `tools/check-scrub-record-r42.py:240-241` | identical except the alias `base_hits` for `novelty_base_hits` |

Observed (`compare-output.txt`): all four equalities `True`, `conjunct_count_match: True`
(7 conjuncts each). The SCORECARD section contains exactly one predicate statement per claim
(`grep -n "cases == 10\|rows == 5"` hits only `:2573`/`:2574`), so no competing predicate text exists.

## Code condition: no conjunct added or dropped

* C1 — the condition (`:365-366`) evaluates `len(CASES) == 10`, the sentence says `cases == 10`; the
  same expression is what the counter emits as `'cases'` (`:372 'cases': len(CASES)`), so the sentence's
  `cases` names exactly the value the code tests. No other term appears in the condition; the emitted
  `non_invariant`, `ns_cases`, `per_case`, `token`, `selftest_label`, `selftest_rc` are not conjuncts
  (`non_invariant` is implied by `invariant == 10`, since `invariant += ok` runs once per case,
  `:328`).
* C2 — the condition (`:240-241`) evaluates `base_hits == 0`; the counter emits that same variable as
  `'novelty_base_hits': base_hits` (`:249`), and `base_hits` is the sum of per-token hit counts at
  `BASE` (`:167-171`). No other term appears in the condition.
* Emitted but not conjuncts, and their status: `snapshots_ok`, `capture_ok`, `sources`, `per_row`,
  `transcripts_bound`, `transcripts_checked`. `transcripts_bound` is *declared* outside the predicate
  in both places (`SCORECARD.md:2579-2580`; counter `:25-27`). `snapshots_ok`/`capture_ok` are not
  conjuncts, but at the tip they are implied: a digest-mismatched snapshot sets `src = None` for that
  file, and every quote on it becomes `bad` (`:192-204`) — the entry cites `scrub.c` throughout and
  `CHANGES` at S238 lines (entry `:126-130`), so a missing CHANGES snapshot fails `quotes_ok == 5`; a
  missing capture makes every host line fail (`:208-209`), so `host_ok` is 0 (< 3). Reverse direction:
  every conjunct in the sentences is evaluated; nothing is omitted.
* `verdicts_ok` binds only wave-2 seats through `w2-dispatch.json` + `w2-results.json` + the committed
  `w2/<name>.md` (`:119-136`; calls `bound(..., 'w2', 'C2RevSC<n>', 'reviewer'/'critic', ...)` and the
  residual `C2RevSC<n>c` through `residual-*`, `:211-218`), matching the declaration cell
  "(seats `C2RevSC<n>` reviewer and `C2CritSC<n>` critic; a `partly` needs a bound residual
  `C2RevSC<n>c` `holds`)". At dispatch time `w2-dispatch.json`, `w2-results.json` and `w2/` do not
  exist (`ls` → 3 `No such file`), so wave-1 C2 reviews are first falsifiers and cannot bind.
* Boundary outside the predicate, declared, not a divergence: exit 2 on usage/read error produces no
  verdict line (`c1.py:46`, `c2.py:34`; `SystemExit(2)`/`sys.exit(2)` at `c1.py:81,89,98` and
  `c2.py:79`, plus argparse's own usage exit). The table rows describe only PASS/FAIL; a receipt
  ending in exit 2 is "no verdict", not "FAIL", and must not be read as the kill rule firing.

No smallest safe correction is proposed: the predicates are identical and the counters are frozen.
Two notes for the L1, neither actionable this round without mutating a frozen counter:
(i) on a future entry that cites no `CHANGES` line, a tampered `CHANGES` snapshot would no longer fail
the predicate, because `snapshots_ok` is reported outside it (live today only through the S238 quotes);
(ii) the two name aliases (`cases`/`len(CASES)`, `novelty_base_hits`/`base_hits`) are intentional but
make a literal `grep` of the printed sentence against the condition fail — the alias emission lines are
the proof of identity.

## Counter byte-identity: `f50c28d8` == `a84fc9d` (and == HEAD, == working tree)

Receipt: `.ufo/waves/round-42/w1/CritPredicateIdentity/identity-check.txt`.

```
ls-tree freeze: 100755 blob bf7c16bdba29fe972848c1cc853248b0e62bb132  tools/score-size-invariance-r42.py
ls-tree f50c : 100755 blob bf7c16bdba29fe972848c1cc853248b0e62bb132  tools/score-size-invariance-r42.py
cmp freeze vs f50c: identical ; cmp f50c vs HEAD: identical ; cmp f50c vs working tree: identical
c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03  tools/score-size-invariance-r42.py

ls-tree freeze: 100755 blob 2903dee2f4ccbd2f5d3075154f8187a92fd0805b  tools/check-scrub-record-r42.py
ls-tree f50c : 100755 blob 2903dee2f4ccbd2f5d3075154f8187a92fd0805b  tools/check-scrub-record-r42.py
cmp freeze vs f50c: identical ; cmp f50c vs HEAD: identical ; cmp f50c vs working tree: identical
dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f  tools/check-scrub-record-r42.py
```

* Both sha256 values equal the ones printed in the declaration cells (`SCORECARD.md:2573`/`:2574`).
* `git log --oneline a84fc9d..HEAD -- SCORECARD.md tools/score-size-invariance-r42.py
  tools/check-scrub-record-r42.py` is empty; `git diff --stat a84fc9d HEAD -- SCORECARD.md` is empty;
  `git diff --stat a84fc9d HEAD -- tools/` shows only `tools/tsukuroi-census.sh` (33+/8−), i.e. the
  C1 surface, as declared. HEAD is `87c4f7c627e377e5f6d361498e8db9b3886d7953` (two commits after
  `f50c28d8`); the counters are unchanged there too, so the compared declaration is still operative.

## Before receipts were produced by the frozen counter

* `c1-before.jsonl:1` → `"tool_revision": "a84fc9de…"`, `"tool_sha256":
  "c511104a…"`; `:2` → `revision`/`base` `c8efaa3f…`, `verdict FAIL`, `cases 10, invariant 3,
  ns_invariant 0, selftest_pass 1, default_equal 1` — the declaration's "Before at base (expected)"
  cell and this seat's brief both state `invariant 3, ns 0, FAIL`.
* `c2-before.jsonl:1` → `"tool_revision": "a84fc9de…"`, `"tool_sha256": "dbe933ec…"`; `:2` →
  `rows 0, quotes_ok 0, novelty_ok 0, host_ok 0, sources_ok 0, verdicts_ok 0, novelty_base_hits 0,
  verdict FAIL` — the declaration's "entry absent: `rows 0`, FAIL".
* Evaluating each printed sentence on its own reported metrics reproduces `FAIL` in both files
  (sentence false under the values above), so the receipts are consistent with the predicates.
* Receipt sha256: `c1-before.jsonl` `e1155b98b81a3647f63116ec14223fd8b0e62135b7fb17c30700577ea10d1f77`,
  `c2-before.jsonl` `3c81c4db45fa3d9e1770ea3c6260f969f27012e6c34639de5168605d012f4e7a`.

## Impacted axes

operability (C1) and depth (C2): no change. The identity holds, so neither claim's target sentence is
weaker or stronger than the frozen code, and no axis can move on a predicate mismatch. Adjacency is
untouched (read-only review).

## Not done

No counter execution (C1 counter ~1–3 min, several CPUs; not needed to compare text and would not be
evidence of identity). No re-derivation of the metric definitions beyond the conjuncts (other seats own
the C1 fixtures/planes and the C2 rows). No lane write, no git/jj mutation, no host change.
