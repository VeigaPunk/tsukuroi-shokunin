# CriticClaims — round 99, wave w1 (lane tsukuroi)

Seat: CriticClaims. Scope: falsify C1/C2 **wording and sizing**, not their numbers. The numbers were
re-derived anyway (x1 canonical, not x3, and no clone — see §2); every frozen reading I could reach
reproduced exactly.

## 0. Axes named (Godspeed)

- **F1 predicate fidelity** — "exactly two changes", universal clauses ("a hybrid cell reads …",
  "a cell that mentions VARIANTS more than once reads …"), "each case asserts".
- **F2 twin / discrimination (QUALITY 136)** — does a claimed closure re-answer a case the r98 roster
  already covered, and how large is the marginal delta.
- **F3 do-nothing rule** — can the r98 control alone satisfy any target clause.
- **F4 closure sizing** — one command over committed bytes, or a multi-instrument campaign.
Impacted axes: **depth** (C1's field/twin structure) and **freshness** (C2's fail-closed sentence,
routed-limit disclosure, tally and provenance). No clause below asks for a number to move; every
correction is a narrowing sentence.

## 1. Instruments verified before any measurement

```
$ sha256sum -c .ufo/waves/round-99/before/instruments.sha256
… all 16 lines: OK
```

## 2. Frozen target lines, re-derived (PASS/FAIL per line)

All runs are `--runs 1`, canonical lane, scratch work dirs. x3 canonical / x3 clone are **not**
re-derived by this seat; receipts state `runs1`.

| frozen line | my reading | verdict |
|---|---|---|
| C1 landed gate `105/105` met, `failed_families []`, 0 error rows | `met 105/105`, failed `-`, 420 cases, 0 error rows (receipt 01, 27, 28) | PASS (x1) |
| C1 x3 canonical + x3 clone | not re-derived (x1 canonical) | UNEXECUTED by this seat |
| C1 `N09-y-era` `unmet 104/105`, exactly `[REFUSAL-VERSIONS-9DIGIT-Y]`, 0 errors | `unmet 104/105`, `['REFUSAL-VERSIONS-9DIGIT-Y']`, Y family 0/4 pass, 0 error rows (02) | PASS (x1) |
| C1 `N11-x-era` `unmet 103/105`, exactly `[EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]`, 0 errors | `unmet 103/105`, same set, X 0/4 and EXPLICIT-VERSION-ERA 3/4, 0 error rows (03) | PASS (x1) |
| C1 r98 control on landed gate `met 105/105` | `met 105/105`, 0 error rows (24) | PASS (x1) |
| C1 r98 control on N09 `met 105/105` (blind) | `met 105/105` (05) | PASS |
| C1 r98 control on N11 `unmet 104/105`, `[EXPLICIT-VERSION-ERA]` | `unmet 104/105`, `['EXPLICIT-VERSION-ERA']`, 1 case (04) | PASS |
| C1 `--selftest` without reference `PASS 5/5` | `selftest PASS 5/5`, rc 0 (12) | PASS |
| C1 both new lie kinds make the battery read unmet | `limine-version`: unmet 93/105; `visibility-era`: unmet 95/105; 0 error rows each (13, 14) | PASS |
| C2 landed `PASS`, `findings []`, `bindings 7` | `PASS`, 0 findings, bindings 7/7 on the working tree and at `f107da3a` (26) | PASS |
| C2 `--selftest PASS 17/17` | `selftest PASS 17/17`, rc 0 (08) | PASS |
| C2 M07 mutant `FAIL 16/17`, exactly `ancestor` red | `ancestor FAIL rc=0 … PASS`, `selftest FAIL 16/17` (11) | PASS |
| C2 r98 checker PASS on hybrid+restated, r99 FAIL one frozen finding each | r98 `PASS 7/7` on both; r99 hybrid `RC-CELL-MISSING` ×1, restated `RC-CELL-AMBIGUOUS` ×1 (07) | PASS |
| C2 coverage gate `PASS 160/160 findings 0` at pre-round tip | `PASS`, counts `registered 160, rows_total 160, tools_total 160, findings 0`, revision `f107da3a` (09) | PASS |

## 3. Clause-by-clause table

Legend: **holds** = sentence true as written; **narrow** = true for the named witness but false as a
universal/implied claim; **falsified** = sentence false against executed evidence.

### C1

| # | clause (claims.json + declaration) | counterexample attempted | outcome | proposed amendment |
|---|---|---|---|---|
| C1-1 | "is the r98 battery (roster unchanged at 105)" | AST count both files: `FAMILY_ROSTER` 105, `CASES_PER_FAMILY` 4 (420 cases), `FAMILIES == FAMILY_ROSTER` | holds | — |
| C1-2 | "with **exactly two** changes: (a)…, (b)…" | `diff -u r98 r99`: 7 hunks, 5 removed / 29 added; three **semantic** changes, not two — (a) X/Y flags, (b) two lie kinds, **(c) output schema token `tsukuroi-limine-pin-battery-r97-v1` → `…-r99-v1`** (receipt 19; emitted token in 01 vs 24). (c) is exactly the r98 amendment **A7** routed naming defect (`plan-amendments-r98.md:68`), closed silently | **falsified** | "…with exactly three changes: (a) X/Y `check_echo`+`check_era`; (b) `LIE_KINDS` gains the two kinds; (c) the successor schema token `tsukuroi-limine-pin-battery-r97-v1 → …-r99-v1` (closes the routed r98 A7 naming defect); docstring-only edits otherwise." |
| C1-3 | "(a) … set `check_echo` and `check_era`" | per-case generator table: X 4/4 and Y 4/4 have both flags True; every X case version `999999999.9.9`, Y cases alternate `12.999999999.4` / `0.999999999.0` (18) | holds | — |
| C1-4 | "so each case asserts the flag spelling echoed verbatim with source `flag`" | landed run: X observed `('999999999.9.9','flag')`; Y observed both spellings with `flag` (28). Twin leg: an X-spelling-only echo lie reads **r98 `unmet 104/105 [EXPLICIT-VERSION-ECHO]`**, X family 4/4 green (21); a Y-spelling-only echo lie reads **r98 `met 105/105`** (22), **r99 `unmet 104/105 [Y]`** (23) | holds; **X half is a twin, Y half is new** | "…each case asserts the echo; the X spelling was already echoed by `EXPLICIT-VERSION-ECHO`'s `999999999.9.9` member (r98 catches an X-only echo lie at `104/105`), the Y spellings are newly asserted." |
| C1-5 | "and the era label the whole tuple selects" | N09 (second-component cap) fails Y 4/4 on r99 and is invisible to r98; N11 (first-component cap) fails X 4/4 on r99 while r98 catches it only through `EXPLICIT-VERSION-ERA` (02–04) | holds (narrow) | add the family's own caveat: "the expected label is the whole tuple's; these two Y members do **not** discriminate an X-only era reader (the family docstring says so; `EXPLICIT-VERSION-ERA` does)". |
| C1-6 | "(b) `LIE_KINDS` gains `limine-version` and `visibility-era`" | AST: 12 → 14; both wrappers built from `LIE_WRAPPER` read unmet (13, 14) | holds | — |
| C1-7 | "so the `--selftest --reference` leg falsifies the two reported fields" | same wrappers as gates: 93/105 and 95/105 unmet, 0 errors. **But the r98 control battery reads `unmet 95/105` (15) and `unmet 97/105` (16) on the same two wrappers** | holds literally, **twin / do-nothing** | "…so the selftest leg falsifies the two fields; note both wrappers already read unmet on the r98 battery, so the leg witnesses the fields, not r99's added families." |
| C1-8 | "`--selftest` (no reference) `PASS 5/5`" | r99 `PASS 5/5` (12); r98 `PASS 5/5` with the identical five lines (25) | holds, **control-satisfied** | fold into the do-nothing list; it certifies no r99 change. |
| C1-9 | "the `--selftest --reference` leg cannot see an assertion removal"(round-98 scoreboard premise the plan says it closes) | B03-class mutant of r99 (Z family's `check_echo` removed) still reads **unmet 94/105** on `lie-limine-version`, with Z 4/4 **green** and X/Y/EXPLICIT-ECHO/LZ red (17). The kind is blanket, so other families supply the verdict | **closure not achieved at family level** (single leg executed; full 14-kind selftest PASS on that mutant is [INFERENCE]) | do not claim the structural gap closed by (b); say "a field lie anywhere now reads unmet — a per-family assertion removal is still invisible to `--selftest --reference`; only a spelling-targeted bend sees it." |
| C1-10 | "The r98 Frontier states both limits by name: … 'is bound to the two r97 families only' and 'the X leg rides on one EXPLICIT case' (amendment A5)" | `corpus/README.md:1241` holds the first sentence; the r98 Frontier bullets contain **no** X-leg bullet — the X-leg sentence is r98 amendment **A5** (`plan-amendments-r98.md:49`: "the X-cap's *field* fidelity rides on one EXPLICIT case") and the r99 section's own line at `README.md:1267` | narrow (false provenance of the second quote) | "the r98 Frontier names the metadata limit; the X-leg limit is the r98 **amendment A5**, not a Frontier bullet." |

### C2

| # | clause | counterexample attempted | outcome | proposed amendment |
|---|---|---|---|---|
| C2-1 | "is the r98 checker with **exactly two** changes" | `diff -u`: 11 hunks, 7 removed / 96 added; semantic changes: (a) guard+`unique`, (b) 14→17 selftest, **(c) payload schema `tsukuroi-registry-content-r97-v1` → `…-r99-v1`**, plus a dead `("ANCESTOR", None, None)` doctor exclusion and a tempdir-prefix rename (20; tokens in 07) | **falsified** | "…with exactly three changes: (a)…, (b)…, (c) the successor payload token `tsukuroi-registry-content-r97-v1 → …-r99-v1`; plus one dead `ANCESTOR` exclusion in `build_fixture` (no case uses it) and a tempdir-prefix rename." |
| C2-2 | "(a) the `RC-BEND-SPAN` capture carries a boundary guard `(?![0-9,-])` and the binding is marked unique" | source diff + `unique: True` present only on RC-BEND-SPAN (20) | holds | — |
| C2-3 | "so a hybrid cell (`VARIANTS N01-N04,N05`, the r98 A1 survivor …) reads `RC-CELL-MISSING`" | named shape: r99 FAIL 1 finding `RC-CELL-MISSING` (07, xv5). **Evasion executed: `VARIANTS N01-N04,N05 then VARIANTS N01,N03` → PASS 0 findings; `VARIANTS N01-N03 N05` → PASS 0 findings** (10-xv1, 10-xv2) | holds for the named survivor; **falsified as the fail-closed universal** of the declaration ("a legitimately-written registry cell that states two spans … must be rewritten") | "a cell whose span mention carries a trailing `[0-9,-]` reads `RC-CELL-MISSING`; a second label separated by a space, or a hybrid first mention followed by a valid one, still binds silently (measured PASS on both)." |
| C2-4 | "a cell that mentions VARIANTS more than once (the r98 same-cell-restatement survivor) reads `RC-CELL-AMBIGUOUS`" | survivor shape `VARIANTS N01,N03 then VARIANTS N01-N03` → AMBIGUOUS (07). **`VARIANTS N01-N03 then VARIANTS N01-N05,N06` → PASS 0 findings; two mentions, no finding** (10-xv3). Control: two guard-passing mentions → AMBIGUOUS (10-xv4) | holds for survivor; **falsified as written** — the code counts guarded *captures*, not mentions (`len(re.findall(capture, cell)) > 1`) | "a cell whose text matches the guarded capture twice reads `RC-CELL-AMBIGUOUS`; a second mention that fails the guard is not counted and the first capture binds (`VARIANTS … then VARIANTS …-…,…` reads PASS)." |
| C2-5 | "(b) `--selftest` gains `span-hybrid`, `span-restated`, `ancestor` (14 → 17)" | AST: `SELFTEST_CASES` 14 → 16, plus the separate `ancestor_case` append; run `PASS 17/17` (08) | holds | — |
| C2-6 | "the ancestor case running this file's real CLI … pristine rc 2 / CANNOT-EVALUATE; the M07 mutant reads rc 0 / PASS" | M07 = exactly the three-line merge-base deletion: `ancestor FAIL rc=0 registry-content: status PASS bindings 7/7`, `selftest FAIL 16/17` (11); pristine PASS 17/17 (08) | holds | — |
| C2-7 | "Landed status PASS, findings [], bindings 7" | r99 `PASS 7/7` on working tree and at `f107da3a`; **r98 also `PASS 7/7` on both** (26) | holds, **control-satisfied** | list it as a do-nothing equality, not an r99 result. |
| C2-8 | "coverage gate PASS 160/160 findings 0 at the pre-round tip" | executed `PASS`, `registered 160 / rows_total 160 / tools_total 160 / findings 0` at `f107da3a` (09); the gate bytes are unchanged by the round (manifest) | holds, **control-satisfied** (routed R99-D1 repair, not a C2 measurement) | move it out of C2's target into the R99-D1 repair sentence. |

## 4. Executed counterexample detail (the two that do not appear in the frozen texts)

Fixture base = `check-registry-content-r99.build_fixture`, cell substituted, real CLI on `--root`:

```
10-xv1  cell: VARIANTS N01-N04,N05 then VARIANTS N01,N03   rc=0  status PASS bindings 7/7 findings 0
10-xv2  cell: VARIANTS N01-N03 N05                         rc=0  status PASS bindings 7/7 findings 0
10-xv3  cell: VARIANTS N01-N03 then VARIANTS N01-N05,N06    rc=0  status PASS bindings 7/7 findings 0
10-xv4  cell: VARIANTS N01-N03 then VARIANTS N01-N05        rc=1  RC-CELL-AMBIGUOUS  findings 1
10-xv5  cell: VARIANTS N01-N04,N05                          rc=1  RC-CELL-MISSING    findings 1
```

`xv1` is the load-bearing one: it is simultaneously (i) a hybrid cell (contradicts C2-3 as a
universal) and (ii) a two-mention cell (contradicts C2-4 as written) and it **passes**, because
`re.search` skips the failed first mention and binds the second.

Twin legs for C1 (all 0 error rows):

```
21  r98 on X-spelling-only echo lie   unmet 104/105  ['EXPLICIT-VERSION-ECHO']   EXPLICIT-ECHO 3/4, X 4/4
22  r98 on Y-spelling-only echo lie   met   105/105  []                          (blind)
23  r99 on Y-spelling-only echo lie   unmet 104/105  ['REFUSAL-VERSIONS-9DIGIT-Y'] Y 0/4
15  r98 on lie-limine-version         unmet  95/105  (Z, EXPLICIT-ECHO, LZ + usage/auto families)
16  r98 on lie-visibility-era         unmet  97/105  (EXPLICIT-ERA, Z, LZ + usage/auto families)
17  B03-class r99 mutant on lie-limine-version  unmet 94/105, Z family 4/4 green
```

## 5. Twin / do-nothing count (QUALITY 136 + do-nothing rule)

Nine clause instances are twins (re-answer r98 coverage) or already satisfied by the r98 control:

| clause instance | twin | control-satisfied |
|---|---|---|
| X-family echo assertion (C1-4) — r98 `EXPLICIT-VERSION-ECHO` i=3 catches an X-only echo lie | ✔ | — |
| X-family era assertion (C1-5) — r98 `EXPLICIT-VERSION-ERA` i=3 catches the X-cap era lie | ✔ | — |
| `limine-version` lie kind (C1-6/7) — r98 battery already `unmet 95/105` | ✔ | ✔ |
| `visibility-era` lie kind (C1-6/7) — r98 battery already `unmet 97/105` | ✔ | ✔ |
| N11's `EXPLICIT-VERSION-ERA` family leg (C1 target) — carried by r98's own coverage | ✔ | — |
| C1 landed `105/105` clause — r98 control reads `105/105` | — | ✔ |
| C1 `--selftest` 5/5 clause — r98 reads the same five lines | — | ✔ |
| C2 landed `PASS` / `bindings 7` — r98 checker `PASS 7/7` on the same table and at `f107da3a` | — | ✔ |
| C2 coverage `160/160` — unchanged gate, no r99 bytes | — | ✔ |

**Count: 9 clause instances; 5 twins, 5 control-satisfied, 2 in both (the two lie kinds).** The
genuinely new discrimination in C1 is the **Y** family-field pair (era: N09 r98 met / r99 104/105;
echo: 22/23) plus the X family's *location* of an already-existing assertion — 2 of 4 added
family-field assertions are twins and both added lie kinds are control-satisfied.

## 6. Sizing (one command vs a campaign)

- **C1** is not one command. The counting command names the battery + `count-runs.py`; the target also
  needs the r98 do-nothing battery, `N09`, `N11`, the reference selftest (15 battery runs generated
  from `LIE_WRAPPER`) and a clone → ≥6 committed instruments/commands. My evidence is x1 canonical.
- **C2** is not one command: r99 checker + `make-fixtures.py` + r98 checker + coverage gate + the M07
  mutant. The M07 mutant of the **r99** file is not frozen under `before/`; only its *definition*
  survives as `w1/MutRegistry/receipts/M07.diff` (three deleted lines) against the r98 file. A
  closure must re-apply that diff to the r99 bytes; the claim's counting command does not name it.
  Smallest correction: name `M07.diff` + the target file digest in the counting command.

## 7. Additional provenance / tally defects found while executing the clauses

1. **Landed-row tally mismatch (QUALITY 105 class):** `SKILL.md:5947` (r99 battery row) says "with
   `--reference <GATE>` the **16** one-field lie kinds add `limine-version` and `visibility-era`",
   while `LIE_KINDS` is 12 → **14** (AST, both files). The row overstates by 2.
2. **Missing receipt path (r98 lesson, inherited by the C2 prose):**
   `corpus/lessons/round-98.md:126` cites `MutRegistry/probe-nonancestor.txt`; that file does not
   exist. The M07 evidence is `w1/ConnectorOverlap/m07-mutant-survival.txt` (pristine rc 2 vs mutant
   PASS 14/14) and the definition is `w1/MutRegistry/receipts/M07.diff`.
3. C1's citation of `w1/ReviewBattery/g6-y-era-r98.json` (met 105/105), C2's A1 citation
   (`ReviewRegistry/receipts/17-f-mixed.txt`: `PASS 7/7`) and the restatement citation
   (`16-extra-probes.txt`: `findings 0` on `VARIANTS N01,N03 see also VARIANTS N07,N09`) all check
   out — no drift there.

## 7b. Seat-to-seat harm — self-disclosure (QUALITY 110; evidence class: seat disclosure)

At ~11:23–11:24 -0300 I removed my own scratch dir `…/tsukuroi-r99/CriticClaims` (as required) and
then, by mistake, ran `rm -rf /fast/scratch/hyaku/tsukuroi-r99` — the **shared parent** — after an
`rmdir` on that parent failed. The `ls` immediately before that command showed sibling dirs
`ConnectorOverlap`, `MutRegistry`, `ReviewBattery-9`, `ScoutFrontier`, `ScribeKnowledge`,
`ScribeLesson` and `dev`; the recursive delete removed their contents (only `ScribeLesson` survived
the first pass because it was being written concurrently). Siblings re-created four dirs within a
minute (`ReviewBattery-9`, `ScoutFrontier`, `ScribeKnowledge`, `ScribeLesson`, mtime 11:24);
`ConnectorOverlap`, `MutRegistry` and `dev` were not yet re-created when I stopped. Any scratch
receipt those seats had not yet copied into their seat dirs is lost.

- Harmed (by my command): MutRegistry-3, ReviewBattery-9, ScoutFrontier, ScribeKnowledge-5,
  ScribeLesson-15, and the lane `dev` scratch dir (owner unknown). **ConnectorOverlap-29 reports no
  loss** (peer disclosure, message at this wave): that seat had already deleted its own scratch at
  11:23 and its eight receipts are intact in its lane seat dir. ScoutFrontier reports its copied
  receipts survived and its wiped artifacts re-derive byte-identically; ScribeLesson-15 lost
  first-pass N09/N11/N10 readings and is re-running them into its seat dir (peer disclosures, not my
  measurements). **MutRegistry-3 reports only scratch artefacts lost** (mutant copies, fixtures,
  drivers), all authoritative readings already in its seat dir; it regenerated the mutants with
  sha256 assertions and re-ran the interrupted N11 leg to `unmet 103/105 [EXPLICIT-VERSION-ERA,
  REFUSAL-VERSIONS-9DIGIT]`, 0 error rows (peer disclosure, matching my receipt 03).
- Command: `rm -rf /fast/scratch/hyaku/tsukuroi-r99` (single run; no retry). My own seat dir and all
  receipts in `.ufo/waves/round-99/w1/CriticClaims/receipts/` were already outside scratch and are
  intact.
- Isolation fix: a seat deletes only its own `<SeatName>` path and never a shared parent; a delete
  command is asserted to end in `/<SeatName>` before it runs. Reported to the L1; the round lesson's
  Seat harm table needs this row with the timestamp and this section as its disclosure.

## 8. Receipts (all under `.ufo/waves/round-99/w1/CriticClaims/receipts/`)

`01` landed r99 · `02` N09 r99 · `03` N11 r99 · `04` N11 r98 · `05` N09 r98 · `06` fixtures ·
`07` checker×fixture matrix · `08` r99 selftest · `09` coverage at f107da3a · `10-xv1..xv5` capture
evasions · `11` M07 mutant · `12` r99 selftest no-ref · `13`/`14` lie kinds on r99 · `15`/`16` lie
kinds on r98 · `17` B03 mutant leg · `18` per-case flag table · `19`/`20` instrument diffs ·
`21`/`22`/`23` echo-lie legs · `24` landed r98 · `25` r98 selftest no-ref · `26` both checkers at
f107da3a · `27` count-runs · `28` case-level detail · `29` scratch-artifact definitions and sha256s.

Tool installs: none.

{"seat":"CriticClaims","verdict":"findings","notes":"All frozen C1/C2 numbers re-derived at x1 canonical (landed 105/105; N09 104/105 [Y]; N11 103/105 [EXPLICIT-ERA,X]; r98 105/105 on landed+N09, 104/105 [EXPLICIT-ERA] on N11; selftest 5/5 and 17/17; M07 FAIL 16/17 ancestor red; hybrid/restated r98 PASS 7/7 vs r99 FAIL 1 finding; coverage 160/160). Falsified wording: both 'exactly two changes' predicates (undeclared successor schema token rename in each, plus dead ANCESTOR guard and tempdir rename in C2); C2's fail-closed universals ('a hybrid cell reads RC-CELL-MISSING', 'mentions VARIANTS more than once reads RC-CELL-AMBIGUOUS') evaded by executed fixtures xv1/xv2/xv3 that read PASS 0 findings; C1's 'Frontier states both limits by name' second quote is r98 amendment A5, not a Frontier bullet; C1's lie-kind closure does not see a per-family assertion removal (B03 mutant still unmet 94/105 with Z green). Nine clause instances are twins or control-satisfied (5 twin, 5 control, 2 both). Sizing: each target needs 4-6 instruments/commands, not one; C2's M07 mutant of r99 bytes is unfrozen (only M07.diff). Two landed provenance/tally defects reported, not fixed: SKILL.md:5947 says 16 lie kinds (actual 14); corpus/lessons/round-98.md:126 cites a nonexistent MutRegistry/probe-nonancestor.txt."}
