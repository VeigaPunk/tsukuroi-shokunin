VERDICT: draft

# R49ScribeLesson — `## Mistakes` draft for `corpus/lessons/round-49.md` (item F-5)

Axes: (1) evidence fidelity — every row carries a path:line or an observed command; (2) candidate disposition — each
of the four candidates confirmed, re-scoped or dropped with the sentence saying why; (3) reusability — the table is
drop-in replacement text for `corpus/lessons/round-49.md:21-29`, same four columns the file already uses.

Report text only: no lane file was edited, no counter or selftest was run (this seat is EXEC-AUTHORIZED for reads
only), no fixture repo was created. One scratch file (`/fast/scratch/hyaku/tsukuroi-r49/R49ScribeLesson/r48counter.py`,
a `git show` copy used for line numbering) was removed after the line numbers were read.

## Candidate dispositions

**1. Correction demanded by a counted negative re-read only a round later — CONFIRMED.**
`.ufo/waves/round-48/after/c2-final.json` (`revision 76066487…`, `verdict FAIL`): `GR1 row_ok=False blocking=['R48CritGR1a']`
with that seat `partly`; `GR2 row_ok=False blocking=['R48RevGR2a','R48CritGR2a']`, both `partly`; `GR3 row_ok=True`
(receipt `.ufo/waves/round-49/w1/R49ScribeLesson/r48-c2-final-summary.txt`). `SCORECARD.md:3117` records it ("GR1 and GR2
have current-hash `partly` reports"). The seven named corrections then land pre-freeze and are re-read by a fresh
18-seat cohort only in round 49 — `.ufo/waves/round-49/frozen/FROZEN.md:15` ("the seven corrections the round-48 counted
seats named (CritGR1a ×2, CritGR2a ×4, RevGR2a ×2 as one list of seven) are in the bytes ... a fresh 18-seat cohort of one
wave re-reads the corrected rows `holds`"). `captured-by: none` is right, and the nearest existing rule is weaker than the
candidate assumes: `corpus/QUALITY.md:179` (criterion 91, R42-ADOPTED-UNREAD) says only "changed rows are re-read by a
counted seat" — it neither excludes the demanding seat nor binds the re-read to the round, so a corrigible row costs a
whole round. Fix = F-2(b) (`make-w1-spec.py:168`: "a correction demanded by a counted negative must be re-read by a NEW
cohort, never by the demanding seat"), and the round's counter already enforces both halves: `corr_ok`
(`tools/check-scrub-admission-r49.py:348`) and `seats_ok == 18` (`:383`, predicate `:94-95`).

**2. r48 counter vs `w2-results.json` — CONFIRMED IN CLASS, RE-SCOPED; the wording "did not require the seat to exist"
is refuted.**
`tools/check-scrub-admission-r48.py:185-190` (bytes at the r49 freeze `55c07cd3` are identical to its own freeze
`ae99f021` and to the `76066487` measurement rev — empty `git diff --stat`, receipt `refs-counters.txt`) loads
`w2-results.json` and returns `'not exactly one results entry'` unless the seat is a single `results` entry with its role.
`w2-results.json` has keys `lane, round, wave, seats, results`, so the counter read the correct list too. The defect is
cohort completeness, not schema: the frozen predicate had no cohort term (`c2-final.json` `predicate` =
`structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`; key list has no `seats_ok`), while the A3
docstring (`:15-17`) asks only ">=3 credited seats" per row of 6 — so an absent or unbound seat shrank the cohort silently
instead of failing it. Class: "declared cohort not bound by the predicate". Fix = `seats_ok == 18` with control K6
(`.ufo/waves/round-49/frozen/FROZEN.md:45`: "reports present but results entries absent (FAIL: `seats_ok < 18`)"). Because
of this finding the current file's row 1 headline ("Frozen counter ignored the schema it claimed to consume") is not
supported and the draft replaces it; the "only counted `results` entries" clause in the current row is also imprecise —
presence was required per bound seat.

**3. Stale `builds a /tmp fixture tree` comment — CONFIRMED, duration corrected.**
Present in the bytes under test at base: `6256760d:tools/tsukuroi-census.sh:415` "… builds a /tmp fixture tree with a
dispatcher stub for" (receipt `census-base-415.txt`); gone at the freeze, `55c07cd3:tools/tsukuroi-census.sh:415` now reads
"builds a fixture tree under the resolved base", literal count 0. It is *not* a two-round defect: introduced by `5f906451`
(2026-10-14, `git log -S`), sighted in `.ufo/waves/round-38/w1/C1ScoutTmpSweep.md:19` ("STALE WORDING, see nit 1") and
`:50`, sighted again in `.ufo/waves/round-48/w2/TExecLint.md:83` and `TRevFix.md:39` ("Doc drift only"), and routed-not-
patched in `corpus/lessons/round-48.md:31`. `captured-by: none` — the r48 static leg skips comments
(`tools/score-selftest-tmpdir-r48.py:152-153`) and greps only the `or /tmp itself` promise (`:156`); round 38 filed the
sentence under "Nits (not /tmp-write defects)". Fix = C3's `stale_ok` (`tools/check-fd-band-r49.py:44` `STALE`, `:91`), and
its control K2 restores the literal and returns `stale_ok 0` FAIL next to K-pass 167 cases
(`.ufo/waves/round-49/controls/battery-summary-r49-c3.jsonl`, read in full).

**4. ADJ ownership column kept bare ranges for 30 rounds — CONFIRMED.**
Base `6256760d:PROVINCE.md:46-52` holds exactly 9 sibling locators — `../kama-shokunin/PROVINCE.md:3-24`,
`../kagi-shokunin/PROVINCE.md:3-6,10-17,32-34,54`, mado `:3-16`, mori `:3-16`, kumitate `:3-6`, mori `:12-16`,
kaidoku `:3-6,88-100`, revenger `:3-7,19-25`, tameshi `:3-18` (receipt `province-base-46-52.txt`). The rows date to the
round-19 commit `7cc59c8e:PROVINCE.md:46`, the same round that wrote the rule: `corpus/QUALITY.md:53-57` (criterion 32,
R19-ADJ-POINTERS) — "A bare `path:N-M` is not a locator". At the freeze the same cells name `OUT-002`…`OUT-010` and 0
sibling ranges. `captured-by: none` — `tools/check-adjacency-anchors.py` validates only the OUT anchor table
(`PROVINCE_SECTION` `:27`); every `ADJ-` token in it is the ADJ-06 arbitration context (`:57`, `:75-76`, `:211-213`), never
the ADJ ownership cells. Fix = C2's legs (`tools/check-adjacency-table-r49.py:17-27`); controls K0 `bare_ranges 9` FAIL,
K1 linked-but-still-ranged FAIL, K2 a wrong anchor FAIL, K-pass PASS (`.ufo/waves/round-49/controls/battery-summary-r49-c2.jsonl`).

**No candidate dropped.** Two rows of the current section are carried forward but their evidence pointers are corrected:
row 4's `.ufo/waves/round-49/w1-validate.log` is **0 bytes** and no file under `.ufo/waves/round-49/` contains the string
`is not a swarm role` (grep 2026-10-28, `refs.txt`), so that row is L1-reported only and the draft says so; row 5 is
confirmed by the final C3 battery rows only (the first-draft drift it narrates has no file pointer).

## Proposed replacement text for `corpus/lessons/round-49.md:21-29`

```markdown
## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| Declared counted cohort not bound by the counter's predicate — a row needed 3 credited seats of 6, so an absent or unbound seat shrank the cohort silently instead of failing | `.ufo/waves/round-48/after/c2-final.json` `predicate` = `structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`, no `seats_ok` key; `tools/check-scrub-admission-r48.py:185-190` does require exactly one `results` entry per bound seat, while its A3 docstring (`:15-17`) asks only ≥3 credited; `SCORECARD.md:3117` | `none` — no rule bound the declared 18-seat cohort to the frozen predicate; presence was checked per seat, cohort completeness was never counted | `tools/check-scrub-admission-r49.py:383` counts bound seats and the predicate (`:94-95`) requires `seats_ok == 18`; control K6 (`.ufo/waves/round-49/frozen/FROZEN.md:45`) removes only the results entries and fails `seats_ok < 18` |
| A correction demanded by a counted negative was re-read only in a later round, so the negative bought a second round of work | `.ufo/waves/round-48/after/c2-final.json`: GR1 `blocking ["R48CritGR1a"]` (`partly`), GR2 `blocking ["R48RevGR2a","R48CritGR2a"]` (both `partly`), GR3 `row_ok true`; `SCORECARD.md:3117`; the seven corrections land pre-freeze and are re-read by a fresh cohort only then (`.ufo/waves/round-49/frozen/FROZEN.md:15`) | `none` — `corpus/QUALITY.md:179` (criterion 91, R42-ADOPTED-UNREAD) requires only that "changed rows are re-read by a counted seat"; it neither excludes the seat that demanded the change nor binds the re-read to the round | F-2(b) criterion candidate (`make-w1-spec.py:168`): a correction demanded by a counted negative is re-read by a NEW cohort, never by the demanding seat. C1 enforces both halves: `corr_ok` (`tools/check-scrub-admission-r49.py:348`) and `seats_ok == 18` (`:383`) |
| Documentation drift — a stale `/tmp` comment contradicted the behaviour for ten rounds through three separate sightings | base `6256760d:tools/tsukuroi-census.sh:415` "builds a /tmp fixture tree"; present since `5f906451` (2026-10-14); sighted at `.ufo/waves/round-38/w1/C1ScoutTmpSweep.md:19,50` (filed as a nit), `.ufo/waves/round-48/w2/TExecLint.md:83` and `TRevFix.md:39`; routed, not patched, in `corpus/lessons/round-48.md:31`; gone at `55c07cd3:tools/tsukuroi-census.sh:415` | `none` — the r48 static leg skips comment lines (`tools/score-selftest-tmpdir-r48.py:152-153`) and greps only the literal `or /tmp itself` (`:156`) | C3's `stale_ok` (`tools/check-fd-band-r49.py:44,91`) fails on the literal; K2 restores it and returns `stale_ok 0` FAIL while K-pass passes 167 cases (`.ufo/waves/round-49/controls/battery-summary-r49-c3.jsonl`) |
| A table ignored the portability rule its own round wrote — the ADJ-01..07 Ownership column kept bare sibling ranges for 30 rounds | base `6256760d:PROVINCE.md:46-52` carries 9 sibling locators (`../kama-shokunin/PROVINCE.md:3-24` … `../tameshi-shokunin/PROVINCE.md:3-18`), the rows the round-19 commit `7cc59c8e:PROVINCE.md:46` wrote; `corpus/QUALITY.md:53-57` (criterion 32, R19-ADJ-POINTERS): "A bare `path:N-M` is not a locator"; at `55c07cd3:PROVINCE.md:46-52` the same cells name `OUT-002`…`OUT-010`, 0 sibling ranges | `none` — `tools/check-adjacency-anchors.py` validates only the OUT anchor table (`PROVINCE_SECTION` `:27`; every `ADJ-` reference is the ADJ-06 arbitration context, `:57`, `:75-76`, `:211-213`) | C2's `bare_ranges == 0` / `linked_rows == 7` legs (`tools/check-adjacency-table-r49.py:17-27`); K0 `bare_ranges 9` FAIL, K1 linked-but-ranged FAIL, K2 wrong anchor FAIL, K-pass PASS (`.ufo/waves/round-49/controls/battery-summary-r49-c2.jsonl`) |
| Wave spec offered roles the policy does not admit (L1-reported; no file carries the refusal text) | `.ufo/waves/round-49/w1-validate.log` is 0 bytes and no file under `.ufo/waves/round-49/` contains `is not a swarm role` (grep 2026-10-28); the accepted run is stamped by `w1-spec.json` and `w1.ready` | the validator, before any seat — the cheapest possible capture | roles chosen from the validator's admitted set at spec time; labrat work rides an executor item |
| Control fixtures drifted from the bytes they claimed to mutate | `.ufo/waves/round-49/controls/battery-summary-r49-c3.jsonl` final state: K0 (`stale_ok 0, diag_ok 0, cases 166`) FAIL, K1 (`band_ok 0`; selftest `166 cases, 165 passed, 1 failed`) FAIL, K2 (`stale_ok 0`) FAIL, K-pass (`167 cases`) PASS | the battery itself: a control that does not fail is visibly wrong next to K-pass | K1 selects the `(R49-C3)` case line; K2 asserts the stale literal is present in the mutated fixture before scoring |
```

## Findings that change the current section (for the L1 when pasting)

1. Current row 1 headline must go: the r48 counter did read `w2-results.json` and required a results entry per bound seat
   (`tools/check-scrub-admission-r48.py:185-190`). Replacement keeps the falsifiable part (no cohort term in the
   predicate) and cites the A3 quorum.
2. Current row 2's "survived two rounds" understates it: `git log -S'builds a /tmp fixture tree'` puts the literal at
   `5f906451` (2026-10-14), and `.ufo/waves/round-38/w1/C1ScoutTmpSweep.md:19` already names it.
3. Current row 4's evidence pointer (`.ufo/waves/round-49/w1-validate.log` "records the accepted run only") cannot be
   checked: the file is 0 bytes. The row now declares the gap instead of citing it.
4. Current row 3's "9 occurrences at base" is confirmed by count; its "30 rounds" is confirmed by the round-19 commit
   `7cc59c8e` carrying the same rows.

## Not done (limits)

- No counter, selftest, battery or census run of my own; every number above is read from a receipt or from `git show` of
  the named revision. The C1 battery (`battery-summary-r49-c1.jsonl`) was not opened (K6's behaviour is cited from
  `FROZEN.md:45`, not from its receipt).
- The GR1/GR2 corrections themselves (the seven strings) were not re-verified against the grounding row; that is C1's
  counter's job (`corr_ok`), not this seat's.
- Nothing was verified about whether any QC criterion exists that requires a cohort term (I read `QUALITY.md:53` and
  `:179` and grepped `cohort` — one hit, criterion 51, unrelated); if F-2 adds criterion 94 the number in the fix column
  will need the L1's confirmation.

## Artifacts

- Report: `.ufo/waves/round-49/w1/R49ScribeLesson.md`
- Receipts: `.ufo/waves/round-49/w1/R49ScribeLesson/{r48-c2-final-summary.txt, r49-c2-battery.txt, census-base-415.txt, province-base-46-52.txt, refs.txt, refs-counters.txt}`
