# Routed defect 1 — round-25 spot-check line 103 — evidence and draft correction

Seat: ScribeRouted1Scorecard51. Scope: read-only evidence for the round-25 verifier spot-check line 103 (`corpus/lessons/round-25-verifier-spotcheck.md:103`) plus draft text for the appended correction and the lesson Mistakes row. The lane was not edited by this seat.

## Verdict

Partly holds as stated in the routed defect, and is now complete in the lane. The change to `SCORECARD.md:51` is exactly one line, made by exactly one commit (`c93bd70f`), and the sweep of the five canonical files finds no other non-append change in round 25 besides that line and the already-disclosed `SHONEN.md` box 2 line. [obs]

## Findings

### 1. `SCORECARD.md` line 51 — original text at the round-25 base

Command: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show b9046016831237cd04d38da11ba76e50d5380c53:SCORECARD.md | sed -n 51p` (exit 0).

```
| calibration | 9 | `calibration-synthesis.md` (463 `wc -l`) — the claim→re-measure→append→supersede→rule loop with its mismeasure rows; errata kept visible rather than rewritten (r1's four retractions; the "5-plane" numerals; the AUD-X7 credit correction — appended precision in this record's LOG entry); `closeout-r11.md` §3 register. Ceiling: the D13 verification debts still open (`closeout-r11.md` §3.2). | r10 |
```

### 2. `SCORECARD.md` line 51 — text at `c93bd70f` and at `e9f5356c` (identical)

Commands: `git show c93bd70f:SCORECARD.md | sed -n 51p` and `git show e9f5356c:SCORECARD.md | sed -n 51p` (both exit 0).

```
| calibration | 9 | `calibration-synthesis.md` (463 `wc -l`) — the claim→re-measure→append→supersede→rule loop for rounds 1 to 9; errata kept visible rather than rewritten (r1's four retractions; the "5-plane" numerals; the AUD-X7 credit correction — appended precision in this record's LOG entry); `closeout-r11.md` §3 register. Ceiling: the D13 verification debts still open (`closeout-r11.md` §3.2). | r10 |
```

The two lines differ in exactly one span: `with its mismeasure rows;` became `for rounds 1 to 9;`. Every other byte of the line, including the `r10` last-change cell and the score `9`, is unchanged. [obs]

The byte-level diff of that single line (word diff of base vs head line 51) reports one `replace` opcode and nothing else, so no second, hidden edit rides inside the same line. [obs]

### 3. Every commit that changed line 51

Command: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --format='%H %s' -L51,51:SCORECARD.md b9046016..e9f5356c` (exit 0) prints exactly one commit:

```
c93bd70ffd780119c5fdea5cb93e18efd5a47ba1 round-25: wave-2 repairs (r8 notice, entry corrections, superseding rows S126-S127, search log, table prose, QUALITY clarifications, lesson mistakes), wave-1 final and wave-2 evidence, measure receipts
```

The pickaxe confirms the same single commit: `git log --format='%H %s' -S'loop for rounds 1 to 9' b9046016..e9f5356c -- SCORECARD.md` returns only `c93bd70f`. [obs]

Full-history context (no range): `git log --format='%H %s' -L51,51:SCORECARD.md` lists four commits that ever occupied that line: `fac745b2` (r9), `af8adf15` (r10), `0ecf3ff1` (r11, which created the current line) and `c93bd70f` (r25). The line was byte-identical at `0ecf3ff1` and at the round-25 base `b9046016` (checked with a byte comparison), so the round-11 wording survived untouched for twelve rounds and was rewritten only at `c93bd70f`. [obs]

### 4. Sweep for every other non-append change in round 25

Command: `git diff --numstat b9046016 e9f5356c -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md` (exit 0):

```
12	0	LOG.md
91	1	SCORECARD.md
1	1	SHONEN.md
9	0	corpus/QUALITY.md
15	0	corpus/SOURCES.md
```

Only two files lose a line, one line each. Command: `git diff --numstat b9046016 e9f5356c | awk '$2!=0'` over the whole repository prints the same two lines and nothing else, so no other lane file in round 25 had a line removed or rewritten in place. [obs]

Command: `git diff -U0 b9046016 e9f5356c -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md | grep -E '^-[^-]'` prints exactly two removed lines (exit 0, count 2): the `SCORECARD.md:51` calibration row and the `SHONEN.md` box 2 evidence line (`current sanitized observation/request TSUKUROI-F1-MEM-01` → `current sanitized observation and request TSUKUROI-F1-MEM-01`). The `SHONEN.md` edit was made in `5e7c04ec` (`git log --format='%H %s' -L8,8:SHONEN.md b9046016..e9f5356c` names `5e7c04ec` alone) and it is the one the round-25 lesson discloses at `corpus/lessons/round-25.md:84`. The `SCORECARD.md:51` edit was not disclosed there. [obs]

Within-round edits that touched bytes this lane also appends, and which the round-25 lesson and SCORECARD already disclose or which are edits to files this round itself created: `SKILL.md` (3 lines, sha256 transposition fix on the three `36ae3e47…` copies, `c93bd70f`), `corpus/knowledge/memory-pressure-r25.json` (9 lines, `c93bd70f`), and `corpus/lessons/round-25.md` (1 line, `d70af4a`, the wording fix for the checker parse, disclosed in `SCORECARD.md` "Round 25 measured outcome"). These are in-place edits of files the round-25 wave itself wrote, not rewrites of pre-existing lane rows; the routed defect concerns the round-11 historical row, and that is the only pre-existing row rewritten. [obs] [inf]

### 4b. Residual: the sweep list in QUALITY 60 does not cover every file round 25 edited in place

Round 25 also edited, in place and without an append, `SKILL.md` (3 lines, `c93bd70f`, the `36ae3e47…` sha256 transposition on the three MP-row copies — disclosed in the round-25 lesson `## Gate errata after wave 2` as "the three copies in this round's SKILL.md section were corrected in place") and `corpus/knowledge/memory-pressure-r25.json` (9 lines, `c93bd70f`, swapping the `oom-event-plane.md` supersession row for a `kill-event-deep-r8.md` row and rewriting one `reason` cell — `grep -n "kill-event-deep-r8\|oom-event-plane" corpus/lessons/round-25.md` returns 0 matches, so this one is not listed anywhere in the round-25 lesson). Both are edits to bytes round 25 itself created, so neither is the round-11 historical row the routed defect names, and neither breaks append-only for content that predates the round. [obs]

The consequence for the repair: QUALITY 60's sweep list is `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SHONEN.md` (`corpus/QUALITY.md:124`), and it therefore prints 2 lines for round 25 while the round-25 lesson's total in-place edits are 5 (2 in the sweep list, plus `SKILL.md`, the entry JSON and `corpus/lessons/round-25.md:72`, itself reworded at `d70af4a` and disclosed in `SCORECARD.md` "Round 25 measured outcome"). If QUALITY 60 is meant to make the disclosure checkable against every lane file, its file list is narrower than the failure it describes; if it is meant to cover only the append-only and canonical files, the criterion should say so in words, because the round-25 lesson's own heading "Record of the one in-place edit" did not draw that line either. [inf]

### 5. The routed defect's own claim about the lesson record

`corpus/lessons/round-25.md:82` is the heading `## Record of the one in-place edit (appended after wave 2)` and `:84` names only the `SHONEN.md` box 2 edit. `grep -n "rounds 1 to 9" LOG.md corpus/lessons/round-25.md corpus/QUALITY.md` returns no hit in the lane's own records (only the spot-check line 103 that raised the defect), so the `SCORECARD.md:51` rewrite was never disclosed. [obs]

### 6. State of the lane at the time of this report

The L1 has already written the correction into the working tree of `SCORECARD.md` under the heading `## Round 26 correction to the round-25 record — two in-place edits, not one (appended 2026-10-22)`, naming both edits, quoting the original wording, and giving the same sweep command. The round-26 lesson `corpus/lessons/round-26.md` carries Mistakes row `R26-UNDISCLOSED-INPLACE` (class `disclosure`) and a "Routed defects from the round-25 spot-check" table whose row 1 records the fix. The working tree also carries the new `corpus/QUALITY.md:124` criterion 60 (R26-UNDISCLOSED-INPLACE), whose failing example names `SCORECARD.md:51` and `SHONEN.md` box 2 and whose lesson pointer is `corpus/lessons/round-26.md`. [obs]

Two points the L1 may want to check against the landed text before commit. First, the landed row-51 sentence says "The original stands as the round-11 record; the round-25 wording is withdrawn as an undisclosed in-place rewrite." The row's bytes at line 51 are still the round-25 wording in the committed tree, so "withdrawn" is a claim about which wording the lane treats as the record, not a byte change; if the lane wants line 51 to carry the round-11 wording, that is a second in-place edit and should be declared as such. [inf] Second, `SCORECARD.md` now contains a section heading that does not contain the string `measured outcome`; under the v2 checker the ordinal reference reads only sections whose heading carries `measured outcome`, so the appended correction cannot itself supply an ordinal transition, and the axes table for round 26 is still to be appended separately. [inf]

## Draft text (for the L1; the working tree already carries a version)

### A. Appended correction for the end of `SCORECARD.md`

```markdown
## Round 26 correction to the round-25 record — two in-place edits, not one (appended 2026-10-22)

Routed defect 1 of `corpus/lessons/round-25-verifier-spotcheck.md`. Round 25 made two in-place edits to files this lane keeps append-only or canonical, and its lesson section "Record of the one in-place edit" named only the second, so that record was incomplete.

1. `SCORECARD.md:51`, the calibration row of the round-11 axes table, changed in commit `c93bd70f`. Original wording at `b9046016`: "the claim→re-measure→append→supersede→rule loop with its mismeasure rows". Wording after `c93bd70f`: "the claim→re-measure→append→supersede→rule loop for rounds 1 to 9". The original stands as the round-11 record; the round-25 wording is withdrawn as an undisclosed in-place rewrite. This correction is appended and line 51 is not edited again.
2. `SHONEN.md` box 2 evidence line, `observation/request` changed to `observation and request` (disclosed in the round-25 lesson).

Sweep that finds them: `git diff -U0 b9046016 e9f5356c -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md | grep -E '^-[^-]'` prints exactly these two removed lines. Round 26's own in-place edits are the three SHONEN.md evidence lines of boxes 1, 3 and 4, recorded in `corpus/lessons/round-26.md`.
```

### B. Matching lesson Mistakes row (for the `## Mistakes` table of `corpus/lessons/round-26.md`)

```markdown
| R26-UNDISCLOSED-INPLACE | disclosure | `c93bd70f` changed `SCORECARD.md:51` ("loop with its mismeasure rows" to "loop for rounds 1 to 9"); the round-25 lesson recorded only the SHONEN edit | none (the append-only rule in PROTOCOL covers LOG.md; no lane check compared disclosed edits with the diff) | QUALITY 60: the lesson lists every removed line of the append-only and canonical files, and the sweep command above must print exactly that list. Red before: at `b9046016..e9f5356c` the sweep prints 2 lines while the round-25 lesson disclosed 1. |
```

## Scope

Read-only. No lane file was edited by this seat; the only file written is this report at `.ufo/waves/round-26/w1/ScribeRouted1Scorecard51.md`. Commands run: `git show` (base, `c93bd70f`, `e9f5356c` for `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `corpus/knowledge/memory-pressure-r25.md`, `corpus/knowledge/calibration-synthesis.md`, `.ufo/waves/round-25/w2/RevC1TableByHand.md`), `git log -L51,51:SCORECARD.md` (full history and `b9046016..e9f5356c`), `git log -L8,8:SHONEN.md`, `git log -S` pickaxe on both phrases, `git diff --numstat` and `git diff -U0` over `b9046016..e9f5356c` for the five files and for the whole repository, `git diff -U0 5e7c04ec c93bd70f` for `SCORECARD.md`, `SKILL.md` and the round-25 entry JSON, `git diff -U0 c93bd70f e9f5356c` for `corpus/lessons/round-25.md`, `git status --porcelain`, `grep` over the lane records, plus read-only inspection of `corpus/lessons/round-25.md`, `corpus/lessons/round-26.md`, `corpus/lessons/round-25-verifier-spotcheck.md` and the working-tree `SCORECARD.md`. Scratch diff files were written only under `/fast/scratch/hyaku/tsuku26/ScribeRouted1Scorecard51/`. Installs: none.

Scope: read=lane repository at base b9046016, c93bd70f, e9f5356c, b13e991f and the working tree (SCORECARD.md line 51 and its full line history, SHONEN.md box 2, LOG.md, corpus/QUALITY.md, corpus/SOURCES.md, corpus/lessons/round-25.md, corpus/lessons/round-25-verifier-spotcheck.md, corpus/lessons/round-26.md, .ufo/waves/round-25/w2/RevC1TableByHand.md, corpus/knowledge/calibration-synthesis.md, corpus/knowledge/memory-pressure-r25.json); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/ScribeRouted1Scorecard51.md; executed=git show, git log -L, git log -S, git diff --numstat, git diff -U0, git status --porcelain, grep, sed -n, python3 byte comparison (all read-only, exit 0)
Model: not exposed
Installs: none
