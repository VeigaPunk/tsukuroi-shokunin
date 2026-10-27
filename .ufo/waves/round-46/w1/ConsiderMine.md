VERDICT: draft

# F-8 — considerthese mining: burst-aware reading

Seat `ConsiderMine`, round 46 / w1. Lane reads only; every write is under
`.ufo/waves/round-46/w1/ConsiderMine/`. Item: mine ONE still-unimplemented proposal from
`considerthese/`, ground it through the lane's bar, and land it as a draft lesson section or QUALITY
criterion text citing `considerthese/2026-10-26.md` + date, as exact Markdown.

## 1. Which proposal is still unmined (verified, not inherited)

| Proposal in `considerthese/2026-10-26.md` | Mined | Evidence |
|---|---|---|
| Counter-attack scoreboard | round 41 | `SKILL.md:3833` "## Counter-attack scoreboard — rounds 40-41", `:3835` names the proposal; `corpus/lessons/round-41.md:99` |
| Downstream patch-offset check | round 42 | `corpus/lessons/round-42.md:53` "### considerthese — downstream patch-offset check (`considerthese/2026-10-26.md`, proposal 4)"; script `w1/ConsiderPatchOffset/patch-offset.py` |
| Cross-note correction propagation map | round 43 | `corpus/lessons/round-43.md:83` "### considerthese — cross-note correction propagation map" |
| Seat-harm incident log | round 45 | `corpus/lessons/round-45.md:124` heading, ten-row ledger, receipts `a2w1/ConsiderMine/` |
| **Burst-aware reading** | **not mined** | `grep -ric 'burst' SKILL.md` → `0`; `grep -ril 'burst' corpus/lessons/` → no output; the only prose occurrences are `considerthese/2026-10-26.md:17` and two seat reports (`.ufo/waves/round-44/w1/ConsiderMine.md:15` "not implemented"; `.ufo/waves/round-45/a2w1/ConsiderMine.md:20` "unimplemented, but it is a change to how a daily reflection is read; no round-45 surface grounds it") |

The round-45 seat declined because it saw no surface. The surface exists and is measured below: the
rounds-43-45 `LOG.md` entries against their verifier spot-checks, which is exactly what the proposal
points at ("read each round's LOG entry and verifier spot-check first, then sample commits only where
the two disagree").

## 2. What the proposal points at, measured

Window and read cost (`window.txt`, commands in `commands.txt`):

| Round | LOG heading commit | Commits in round | Files changed | Insertions | Two-document read (LOG entry + spot-check + lesson lines) |
|---|---|---|---|---|---|
| 43 | `a87249c7` 2026-10-26T20:29:07-03:00 | 12 | 628 | 124,551 | 27 + 159 + 141 = 327 |
| 44 | `ae337aab` 2026-10-26T22:34:48-03:00 | 15 | 1,000 | 105,557 | 11 + 217 + 69 = 297 |
| 45 | `bb1a24e5` 2026-10-27T01:30:46-03:00 | 12 | 689 | 88,941 | 29 + 217 + 176 = 422 |
| **43-45** | span **5 h 01 m 39 s** | **39** | **2,317** | **319,049** | **1,046** |

The five-round window the lane actually holds now — `git log --format='%cI %h %s' -- LOG.md | awk
'substr($0,1,16) >= "2026-10-26T15:00"' | wc -l` → `5` (rounds 41-45, 2026-10-26T15:32:33 to
2026-10-27T01:30:46, 9 h 58 m 13 s) — is 63 commits, 4,223 file changes and 551,718 insertions
(`git log --oneline e3bc9340..bb1a24e5 | wc -l` → 63; `git diff --shortstat e3bc9340 bb1a24e5`). The
proposal's premise (a burst outruns a commit-by-commit read) holds at the scale it names and a little
beyond: the two-document read for three rounds is 1,046 lines against 39 commits / 2,317 file changes.

## 3. How many disagreements a round's LOG has with its spot-check

**Unit of comparison.** One row per statement both documents can speak to. A statement is comparable
when the LOG entry asserts or implies it *and* the spot-check re-measures or re-grades it: claim
verdicts, counter values and counts, axis grades, freshness, quality criteria and routed-defect
states. **Excluded by construction:** a defect the closure routes *after* the LOG entry is written
(e.g. round 43's `R43-SR1-LIMITS-CONTRADICTION`) — the LOG cannot carry it, so counting it would
measure the order of writing, not disagreement. Extraction is hand-keyed, one line per row, in
`log-vs-spotcheck.jsonl` (28 rows); `tally.py` tallies it (`tally.txt`):

| Round | Comparable rows | Match | Mismatch |
|---|---|---|---|
| 43 | 9 | 9 | **0** |
| 44 | 7 | 5 | **2** |
| 45 | 12 | 11 | **1** |
| total | 28 | 25 | **3** |

`TSUKUROI_BURST_READ: rows=28 mismatch=3 rounds=3 mismatch_rounds=2`, `tally.py` exit 1.

The three disagreements, verbatim:

1. **R44, axis grade omitted.** The closure grades `adjacency` **harmed**
   (`corpus/lessons/round-44-verifier-spotcheck.md:137`: "| adjacency | harmed | anchors gate
   PASS→FAIL (committed receipts), IN-109 drift re-measured at tip |") and closes the round
   `rejected-harmed` (`:139`); the round-44 `LOG.md` entry (`LOG.md:1615-1625`) never contains the word
   `adjacency` and its incidents list names only the fleet-root fixture, the two unreported seats and
   the FIFO grep. The round's closing verdict is the one sentence the reflection most needs, and it is
   absent from the LOG.
2. **R44, trend grade omitted.** `quality **harmed**` (`:145`) has no counterpart in the LOG entry,
   although the round-43 entry does carry `QUALITY 92` (`LOG.md:1606`) — so the LOG speaks when quality
   moves, and stayed silent when it was harmed.
3. **R45, disposed state overstated.** `LOG.md:1645` "Routed defects: D1-D6, D8-D10 closed, D7
   partial" against `round-45-verifier-spotcheck.md:184` "D1 R45C-D3-R44-MARK-SWEEP. Round-44 D3 is
   only half closed", and the lane's own lesson already says so: `corpus/lessons/round-45.md:94` states
   `D3 ... | closed` while `:108` records "marks D3 'done' on the entry alone; `corpus/README.md:434`
   and the `SKILL.md` row that D3 also names are unchanged from base".

**What the class breakdown says.** Every number agrees: 11 of 11 `measurement` rows (counter values,
selftest totals, row counts, census rows, `40 W04`, `249` vs `245`) and 6 of 6 `verdict` rows match
exactly. All three misses are `axis-grade` (1 of 3), `trend-grade` (1 of 1) and `defect-status` (1 of 3)
— status and harm wording, never a count, and none of them a contradiction: each is an **omission or an
overstatement**. That is the finding the proposal needs: "sample commits only where the two disagree"
works as the second half of the method, but "disagree" has to be a **field-by-field** comparison (axis
table, trend verdicts, disposition table), because a reader who diffs the two documents' prose finds
only a missing line, and one of the missing lines is `rejected-harmed`.

**Reproduced mechanically, 2 of 3.** `check-log-axis-coverage.py` (read-only over the lane) checks (A)
every axis graded `improved`/`harmed` in a spot-check per-axis table is named in that round's LOG entry
and (B) no routed-defect row stating `closed` is contradicted by a same-id bullet in the lesson's
"Conflicts recorded verbatim" block. Run:

```
AXIS-GRADE-OMITTED corpus/lessons/round-44-verifier-spotcheck.md:137: adjacency graded harmed but the
  round-44 LOG entry (LOG.md:1615-1625) never names it
DISPOSITION-CONFLICT corpus/lessons/round-45.md:94: D3 stated 'closed' while :108 names D3 as unchanged / half closed
SKIPPED corpus/lessons/round-43.md:110 numbered-list disposition (not table-shaped): needs a reader
SKIPPED corpus/lessons/round-44.md:50 numbered-list disposition (not table-shaped): needs a reader
TSUKUROI_BURST_READ_CHECK: findings=2 axes_checked=5 disposition_rows_checked=10 skipped_sections=2
```

exit 1, with no finding on rounds 43/45 axes or on the other 9 disposition rows (no false positive).
`run-fixtures.py` builds four synthetic lanes and returns `cases=4 failed=0` — a harmed axis missing
from the LOG (must fire, fires), a named one (must stay quiet, quiet), a `closed` row contradicted
(must fire, fires), a `closed` row with an unrelated conflict bullet (must stay quiet, quiet). Disagreement 2
(the r44 quality trend) is **not** mechanised: it needs the trend-verdict section, which the lane never
carries in a LOG entry in this window — the reading catches it, the check does not, and the draft says so.

## 4. Draft A — lesson section, exact Markdown

Proposed for `corpus/lessons/round-46.md`, after the existing `## Assimilation and considerthese` prose.
Heading style follows `round-45.md:124`.

```markdown
### considerthese — burst-aware reading (`considerthese/2026-10-26.md`, proposal "Burst-aware reading", 2026-10-26)

Mined: "Four rounds in about 13 hours is more than a commit-by-commit read can cover well. In a burst, I
could read each round's LOG entry and verifier spot-check first, then sample commits only where the two
disagree, and say up front how many rounds the window holds." Measured on rounds 43-45 (headings landed
2026-10-26T20:29:07, 2026-10-26T22:34:48, 2026-10-27T01:30:46 -03; 5 h 01 m 39 s): 39 commits, 2,317
file changes and 319,049 inserted lines (`git log --oneline <prev>..<head> | wc -l`, `git diff
--shortstat`), against 1,046 lines of `LOG.md` entry, verifier spot-check and lesson for the same three
rounds. The window the lane holds at the time of writing is five rounds in 9 h 58 m 13 s (rounds 41-45,
63 commits, 551,718 inserted lines), so the first clause of the proposal is not a preference but a
budget: `git log --format='%cI %h %s' -- LOG.md | awk 'substr($0,1,16) >= "<window start>"' | wc -l`
prints how many rounds a window holds, and the read opens with that number.

Disagreements between a round's `LOG.md` entry and its verifier spot-check, counted over every statement
both documents can speak to (verdicts, counter values, axis grades, freshness, quality, routed-defect
states; a defect the closure routes after the entry is written is excluded because the LOG cannot carry
it) — 28 comparable statements over the three rounds, 3 disagreements, all three in status or harm
wording and none in a number:

| Round | Comparable | Disagree | Disagreement |
|---|---|---|---|
| 43 | 9 | 0 | — |
| 44 | 7 | 2 | `adjacency` graded `harmed` and the round closed `rejected-harmed`, neither named in the LOG entry; `quality` graded `harmed`, unnamed |
| 45 | 12 | 1 | the entry reports `D1-D6, D8-D10 closed` while `round-45-verifier-spotcheck.md:184` says round-44 D3 is "only half closed" and the lesson's own conflict bullet (`round-45.md:108`) names README:434 and the SKILL row unchanged |

All 11 numeric statements and all 6 claim verdicts agree, so the sample supports the proposal's order
(LOG + spot-check first) and sharpens its second half: the comparison is field by field — every axis the
spot-check grades `improved` or `harmed`, every trend verdict, every routed-defect state — because a
prose diff between the two documents shows these misses only as a missing line, and the largest of them
is the round's closing verdict. `python3 tools/check-log-vs-spot.py --lane <LANE> --round 43 44 45`
checks the two mechanical halves of that comparison (axis grades, disposition/conflict) and exits 1 with
one finding per miss; four fixture lanes (must-fire and must-stay-quiet) accompany it.

Limits. The disposition table form exists only from round 45 (`round-43.md:110` and `round-44.md:50`
dispose by numbered list), so the conflict half has one live instance. The sample is three rounds, and
a LOG entry and its closure share the round's own counters, so the two documents cannot disagree about
a number the closure copied from the LOG — agreement on numbers is weak evidence of correctness, and
this reading never replaces a counter receipt (QUALITY 77). The closure's routed-defect list (`§5`) is
not LOG-checkable by construction.
```

## 5. Draft B — QUALITY criterion, exact Markdown (optional, lands with Draft A or instead of the check sentence)

Proposed as the next criterion in `corpus/QUALITY.md` (currently ends at 93). The item asks for a draft
lesson section **or** criterion text; both are given so the integrator can take either, and Draft A is
the recommended minimum.

```markdown
94. **A round's LOG entry names every axis its closure graded `improved` or `harmed`, and a routed defect the entry reports closed is the state the closure's defect list leaves it in (R46-BURST-READ):** for each axis the round's `corpus/lessons/round-<N>-verifier-spotcheck.md` per-axis table grades `improved` or `harmed`, the round-`<N>` `LOG.md` entry names the axis and its grade; for each routed-defect row the round's lesson states `closed`, no bullet in the same lesson's "Conflicts recorded verbatim" block names that id as unchanged, half closed or not closed; and `python3 tools/check-log-vs-spot.py --lane <LANE> --round <N-2> <N-1> <N>` exits 0, with its must-fire and must-stay-quiet fixture lanes green. Failing examples (rounds 43-45): round 44's closure grades `adjacency | harmed` (`round-44-verifier-spotcheck.md:137`, admission `rejected-harmed` at `:139`) while the round-44 entry (`LOG.md:1615-1625`) never names adjacency; round 45's entry reports "D1-D6, D8-D10 closed" (`LOG.md:1645`) while `round-45-verifier-spotcheck.md:184` opens "Round-44 D3 is only half closed" and `corpus/lessons/round-45.md:108` names README:434 and the SKILL row unchanged against the `closed` row at `:94`. Lesson: `corpus/lessons/round-46.md`; proposal `considerthese/2026-10-26.md` (2026-10-26).
```

Relative to the round-45 precedent (`QUALITY 93` cites a lesson plus proposal), this criterion adds no
obligation on a claim: it constrains the round's own record, which is why it is separable from the
reading method in Draft A.

## 6. Receipts

`.ufo/waves/round-46/w1/ConsiderMine/`:

| File | What it is |
|---|---|
| `log-vs-spotcheck.jsonl` | the 28 hand-keyed comparable statements (round, class, both quotes, both refs, match) |
| `tally.py`, `tally.txt` | tally of the extraction; exit 1, `rows=28 mismatch=3 rounds=3 mismatch_rounds=2` |
| `check-log-axis-coverage.py` | the read-only mechanical check (axis grades, disposition/conflict); exit 1, `findings=2 axes_checked=5 disposition_rows_checked=10 skipped_sections=2` |
| `axis-coverage.txt` | its output over the lane at the current tip |
| `run-fixtures.py`, `fixtures.txt` | four synthetic lanes; `cases=4 failed=0` |
| `window.txt` | round-heading commits, per-round commit/diff counts, two-document line counts, five-round window |
| `commands.txt` | every command above with its observed output |

No tool was installed or upgraded for this seat (pacman is paused host-wide; nothing was needed).

## 7. Touch, limits, and what I did not do

- **Touched:** the report and the receipt directory only. No lane file was created, edited or deleted;
  no git or jj mutation; no counter, census selftest or gate was run; no host state was touched (lane
  reads only). The lane's `git status --porcelain` shows only other seats' round-46 work in progress.
- **Did not run:** the round's C1/C2 counters or any census selftest (not this item's surface, and the
  seat cost rule allows one C1 run at a time). The three frozen counters these rounds scored were
  verified only through their committed receipts, as the spot-checks themselves do.
- **Counting method is hand-keyed.** The 28-row denominator is a judgement: each row names both quotes
  and both refs so a re-reader can dispute a row rather than the total. Two of the three misses are
  separately reproduced by a script; the third (r44 quality trend) is not.
- **Not claimed:** that burst-aware reading would have caught the missed items *before* the closure
  graded them — it reads the closure's own verdict table. It makes the burst *auditable* in 1,046 lines
  instead of 39 commits, and it names the two record defects (round 44's missing harm lines, round 45's
  `D3 closed` overstatement) that a commit-by-commit read of the diff would have had to notice among
  319,049 inserted lines.
- **Sequence for the integrator:** Draft A into `corpus/lessons/round-46.md`, optional Draft B into
  `corpus/QUALITY.md`, and, if Draft B lands, `check-log-axis-coverage.py` into `tools/check-log-vs-spot.py`
  with its registry row (QUALITY 70) and the fixture harness beside it.
