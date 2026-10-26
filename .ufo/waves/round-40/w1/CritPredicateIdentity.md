VERDICT: supports

Item G-7 (claim-sizing rule: one predicate, same sentence in plan, counter code and receipt). Scope: C1 and C2
compared across five places — SCORECARD declaration at `758a4b08`, counter docstring, counter `predicate` string,
the `ok = ...` condition the code evaluates, and the `predicate` field of the two after receipts — plus
byte-identity of both counters at `f951f28` against the freeze revision `a447b67`. Read-only; no lane file
touched. Scratch removed; comparison receipt kept at
`.ufo/waves/round-40/w1/CritPredicateIdentity/five-place-compare.txt` (sha256
`fbbaa5560f479a9f6ad78abbfd0b8449dd3c998081f4f31808b71c44480be7b4`).

## 1. Five-place comparison, character for character

Normalization applied (stated so the claim is checkable): strip backticks, collapse every run of whitespace to
one space, strip the docstrings' trailing `-> PASS, exit 0` marker (that marker is not part of the predicate).
No other character is changed. Raw differences are therefore only the backtick quoting in SCORECARD and the
line wrapping in the docstring/code string literals — no token differs.

C1 — one sentence, four artifacts:

| Place | Location | Normalized text |
|---|---|---|
| plan (declaration) | `SCORECARD.md:2303` col 6 (`Target (predicate)`) | `baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0 and selfref == 5` |
| counter docstring | `tools/score-selftest-literals-r40.py:28-29` | identical |
| counter `predicate` string | `tools/score-selftest-literals-r40.py:164-165` | identical |
| receipt | `.ufo/waves/round-40/after/c1-after-c707e35.jsonl:6` | identical |

C2 — one sentence, four artifacts:

| Place | Location | Normalized text |
|---|---|---|
| plan (declaration) | `SCORECARD.md:2304` col 6 | `rules_verified == 8 and duplicate_rows == 0 and duplicate_headings == 0 and source_ok == 1 and counts_ok == 2 and novelty_base_hits == 0` |
| counter docstring | `tools/check-exec-environment-r40.py:40-41` | identical |
| counter `predicate` string | `tools/check-exec-environment-r40.py:247-248` | identical |
| receipt | `.ufo/waves/round-40/after/c2-after-bf23805.jsonl:32` | identical |

Observed (receipt `five-place-compare.txt`): `decl==doc True  decl==code True` and `match_decl=True` for both
claims; both after receipts carry exactly one predicate-bearing object, `result=PASS exit=0`, at
`revision=c707e35…` / `bf23805…` with wrapper `tool_revision=a447b67…`. The receipt's sentence is emitted by the
counter itself (obj 1 is the counter's stdout JSON), so receipt↔code identity is structural, not a hand copy.

## 2. The condition the code actually evaluates

C1, `tools/score-selftest-literals-r40.py:161-162`:

    ok = (baseline_pass == 1 and neutral_pass == len(NEUTRAL) and m_applied == len(MUTANTS)
          and survivors == 0 and selfref == SELFREF_BASE)

C2, `tools/check-exec-environment-r40.py:328-329`:

    ok = (verified == 8 and dup_rows == 0 and dup_heads == 0 and source_ok == 1 and counts_ok == 2
          and nov_total == 0)

Conjunct sets are 1:1 with the sentences; **no conjunct is checked that the sentence omits**, and none is
named that the code does not evaluate. Name mapping in the code path (local names only; the printed predicate
uses the sentence names): C1 `m_applied`→`mutants_applied`, `SELFREF_BASE`→`5`; C2
`verified`→`rules_verified`, `dup_rows`→`duplicate_rows`, `dup_heads`→`duplicate_headings`,
`nov_total`→`novelty_base_hits` (`rec.update` at `check-exec-environment-r40.py:330-331` sets the sentence
name from that local, and `nov_total = sum(nov.values())`). The four C2 counters are the record fields of the
same names; the three C1 counters likewise (`score-selftest-literals-r40.py:163-169`).

The one textual gap, reported as an observation and not a defect: C1's code compares against the *symbolic*
bounds `len(NEUTRAL)`, `len(MUTANTS)`, `SELFREF_BASE` where the frozen sentence states the literals `3`, `9`,
`5`. Measured values at the measured revision (imported from the committed file):
`len(MUTANTS)=9, len(NEUTRAL)=3, SELFREF_BASE=5`, with mutant names M1–M9 and neutral names N1–N3 — so the
evaluated predicate is extensionally identical to the sentence at every revision in this round. The gap would
only open if the frozen tables were edited, and the declaration pins each counter by sha256, so such an edit
changes the pin and is detectable. C2's literal `8` matches `len(REQUIRED)=8` for the same reason.

Strongest counterexample I could construct from local evidence: make the code's predicate differ from the
sentence by editing a frozen table. It cannot be reached without changing the counter bytes, hence the
declared sha256; within the pinned bytes there is no state where the two disagree. Tested as a hypothesis, not
by mutation (the counter is the measured surface of this item and is read-only for a critic seat).

## 3. Byte-identity of the counters at the tip

Commands and observed output (all in the lane, read-only):

    git diff --exit-code a447b67b… f951f288… -- tools/score-selftest-literals-r40.py tools/check-exec-environment-r40.py
      -> diff_exit=0 (no output)
    git ls-tree -r <rev> -- tools/…   at a447b67 and at f951f28:
      100755 blob 7be847464e069e4e228d95369918ce59ab394da1  tools/check-exec-environment-r40.py
      100755 blob 38e955b211ecd6cea3f7c42b2eda7a24ab6a2eb1  tools/score-selftest-literals-r40.py
    git log --oneline a447b67..f951f28 -- <both counters>   -> no commits (untouched)
    sha256 of `git show <rev>:<path>` at 758a4b08, a447b67, f951f28:
      score-selftest-literals-r40.py  8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159  (all three)
      check-exec-environment-r40.py   d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d  (all three)

Both equal the sha256 printed in `SCORECARD.md:2303-2304` and the `tool_sha256` recorded in each receipt's
wrapper object. Lineage check: `git rev-list --count 758a4b08..a447b67` = 0 and
`git merge-base --is-ancestor 758a4b08 f951f28` = true, i.e. freeze ≤ declaration ≤ tip; `SCORECARD.md` is
unchanged across `758a4b08..f951f28` (`git diff --stat` empty), so the declaration rows read at the working
tree are the declaration rows at `758a4b08`. **Byte-identical: confirmed.**

## 4. Impacted axes and correction

Impacted axes: operability (C1) and depth (C2) — neither harmed by this finding. No correction required for
round 40; the predicate identity holds as declared. If a later round re-opens these counters, the smallest safe
tightening is to generate the C1 sentence from the same constants the code compares
(`f'… neutral_pass == {len(NEUTRAL)} … mutants_applied == {len(MUTANTS)} … selfref == {SELFREF_BASE}'`), so the
sentence cannot outlive a table edit. Editing the frozen counters in round 40 would invalidate the declared
sha256 pins and is therefore not proposed here.

## 5. Not done

I did not run either counter (the item is identity, not re-measurement; the receipts already carry the
measured values, and I did not confirm those values independently — I read them:
C1 `baseline_pass=1 neutral_pass=3 mutants_applied=9 survivors=0 selfref=5`; C2 `rules_verified=8
duplicate_rows=0 duplicate_headings=0 source_ok=1 counts_ok=2 novelty_base_hits=0`, both `result=PASS`).
I did not evaluate whether the C1 mutants are sufficient or the C2 rule cells are true — those are other
seats' items. No tool installed, no host change, no pacman transaction.
