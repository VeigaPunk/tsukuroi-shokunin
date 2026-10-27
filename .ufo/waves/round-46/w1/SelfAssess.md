VERDICT: draft

# F-12 — self-assessment receipts at base and IMPL, and the round-46 axes draft

Seat SelfAssess (executor, leaf). Item F-12. No lane file was written; the only lane writes are this
report and the two receipts under `.ufo/waves/round-46/w1/SelfAssess/`. Scratch
`/fast/scratch/hyaku/tsukuroi-r46/SelfAssess/` was removed after the receipts were copied.

## 1. Receipts (both run through `tools/run-receipt.py`, never from the working copy)

Command form (verbatim, both runs):

```
python3 tools/run-receipt.py --revision <REV> --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
  --out .ufo/waves/round-46/w1/SelfAssess/self-assessment-<rev8>.jsonl -- \
  tools/check-self-assessment.py --revision '{rev}' --scratch /fast/scratch/hyaku/tsukuroi-r46/SelfAssess/s
```

| Receipt | revision | tool_revision | tool_sha256 | exit | finished_utc |
|---|---|---|---|---|---|
| `.ufo/waves/round-46/w1/SelfAssess/self-assessment-2042117c.jsonl` | `2042117cfb724170772f4c128cc2ddba0b61d817` | same | `44b474fb5401559d9a4052f04f03145cd165a688a78455694d7dd25dba5838e6` | 1 | 2026-10-27T05:27:49Z |
| `.ufo/waves/round-46/w1/SelfAssess/self-assessment-a4477049.jsonl` | `a44770491eb5ca15ce9f8b3207309d1af683ffaf` | same | `44b474fb5401559d9a4052f04f03145cd165a688a78455694d7dd25dba5838e6` | 1 | 2026-10-27T05:26:31Z |

Both receipts carry the same `tool_sha256` (`check-self-assessment.py` is byte-identical at base and
IMPL: it is absent from `git diff --stat 2042117c a4477049`), so the mismatch delta below is
attributable to lane content, not to the checker. Wall times: base 57 s, IMPL 2 m 22 s (IMPL includes
the census selftest at 160 cases; both receipts ran the selftest serially, one at a time).

### 1a. Base `2042117c` — 1 of 27 mismatches, exit 1

| Check | stated | observed | reason (tool's own text) |
|---|---|---|---|
| K10 | 66 | 67 | depth row states 66 lesson files; corpus/lessons holds 67 files |

All other checks `match`: K01 8/8, K02 9/9, K03 9/9, K04 9/9, K05 9/9, K06 8/8, K07 66/66,
K08 4424/4424, K09 1241/1241, K11 466/466, K12 present/present, K13 154/154
(`TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)`), K14 absent/absent,
K15 present/present, K16-K27 match.

K10 is pre-existing and its cause is exact: the round-45 axes table states `corpus/lessons/` 66 files,
and the base commit itself adds the 67th (`git log -1 --stat 2042117c` →
`corpus/lessons/round-45-verifier-spotcheck.md | 217 +++++`, 1 file changed). It is not a round-46 harm.

### 1b. IMPL `a4477049` — 5 of 27 mismatches, exit 1

| Check | stated | observed | reason (tool's own text) |
|---|---|---|---|
| K07 | 66 | 67 | depth row states 66 notes; corpus/knowledge holds 67 .md files |
| K10 | 66 | 67 | depth row states 66 lesson files; corpus/lessons holds 67 files |
| K13 | 154 | 160 | operability row states 154 cases; the census selftest at this revision prints 160 cases (`TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)`) |
| K14 | absent | present | operability row states the mode is absent; the census script holds a `--identity` case arm: True |
| K17 | 154 (case count) | 160 | host-census-gate row states 154 cases; the census selftest at this revision prints 160 cases (its three named paths all still exist) |

Every other check `match` at IMPL, with the same values as base (K01-K06 8/9/9/9/9/8, K08 4424,
K09 1241, K11 466, K12/K15 present, K16-K27 match).

Delta base → IMPL: +4 mismatches (K07, K13, K14, K17), all four caused by round-46 C1 exactly as the
item predicted (notes 66→67 from `corpus/knowledge/census-identity-r46.md`; census cases 154→160; the
`--identity` arm at `tools/tsukuroi-census.sh:3498`). K10 is unchanged and inherited.

The 154→160 delta is confirmed statically against the same bytes: the six new cases are the five
`id_check` calls plus one `check_cli` labelled `(R46-C1)`
(`git show a4477049:tools/tsukuroi-census.sh | sed -n '3418,3448p'`: lines 3418, 3427, 3433, 3437,
3445, 3447; the other three `(R46-C1)` occurrences are `bad` assertions inside those cases and are not
counted as cases).

Exit codes: `check-self-assessment.py` exits 1 at both revisions. This is therefore not a
PASS→FAIL regression of the tool in the round's no-harm table (1 → 1), but the round-46 axes table must
repair all five ids at its landing commit or the calibration row's "mismatches 0" is false.

## 2. Re-derived counts (round-45 table commands, run in the lane working tree at IMPL)

The working tree at the time of the runs differed from `a4477049` only in untracked/modified `.ufo`
evidence (`git status --porcelain`), so these equal the committed values; the receipt in §1b confirms
K07-K11 from the committed tree (`git archive`), which is the authority. (At the end of the seat
`git status --porcelain` additionally shows ` M tools/tsukuroi-census.sh` — another seat's in-flight
C1 edit, not mine; my receipts read the committed bytes through `run-receipt.py`'s clone, never the
working copy.)

| Count | Command (round-45 table form) | Output |
|---|---|---|
| notes | `find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l` | 67 |
| SKILL.md lines | `wc -l < SKILL.md` | 4424 |
| SKILL.md table lines | `grep -c '^\|' SKILL.md` | 1241 |
| lesson files | `find corpus/lessons -type f \| wc -l` | 67 |
| corpus/README.md lines | `wc -l < corpus/README.md` | 466 |
| PROVINCE Core/Frontier/Adjacent | `grep -c '^## Core\|^## Frontier\|^## Adjacent' PROVINCE.md` | 7 (all three sections present) |
| formal overlap table | `grep -c '^\| ID \| Finding' PROVINCE.md` | 1 |
| census selftest | receipt §1b K13 | `PASS (160 cases, 160 passed, 0 failed)` |

At base the same commands on the committed tree give 66 notes, 4424 / 1241, 67 lesson files, 466
README lines (`git ls-tree`/`git show` at `2042117c`).

## 3. Draft — round-46 `## Axes — current self-assessment` table

Append as a new section after the round-45 table (`SCORECARD.md:2931`); it becomes the current table
because the checker takes the last `## Axes — …` section. The heading must name the round (`round 46`)
or the tool exits 2. Scores stay `8 / 9 / 9 / 9 / 9 / 8`: `reference_lines` excludes every section of
the declaring round, so the last eligible ordinal records remain depth 8 (`SCORECARD.md:2250`),
coverage 9 (`:2171`), operability 9 (`:2249`), freshness/calibration/adjacency 9/9/8 (`:1560`); a `9`
in the depth cell of this table would mismatch K01 until round 47's table carries it.

Angle brackets mark values that are **not derivable yet** (see §4). Replace each with the measured
integer at the commit that lands this table; a placeholder left in the committed table is a K07-K11
mismatch.

```
## Axes — current self-assessment (round 46 final measured surface)

Appended 2026-10-27 by round 46. This table supersedes the round-45 table as the lane's current
self-assessment; earlier tables stay as historical records. The ordinals are unchanged (the round-46
measured outcome records no ordinal move; a round's own outcome is never its own reference). Every
count was re-derived at the commit that lands this table with the command named in its cell; re-run
`python3 tools/check-self-assessment.py --revision <REV>` before treating any count here as current.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 67 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` <N_SKILL_LINES> `wc -l` / <N_SKILL_TABLE_LINES> table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` <N_LESSON_FILES> files (`find corpus/lessons -type f | wc -l`); round-46 C2 <ADMIT_OR_REFUSE> GR1-GR3 under `tools/check-scrub-admission-r46.py`; no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` <N_README_LINES> `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line; the scrub record's unprivileged view is Core since round 44 (SCRUB line; content and running state stay Frontier); round 46 <README_LINE: the `admitted round 46` line, or none if C2 is refused>. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (160 cases, 160 passed, 0 failed); `bash tools/boot-chain-audit.sh --selftest` prints `PASS total=49 failed=0`; round-46 C1 `--identity` landed (D12 closed: one `TSUKUROI_CENSUS_IDENTITY:` line names the bytes the running bash executes, read through the descriptor bash holds, `unverifiable`/`verified=no` for stdin, pipe and replaced-after-open). | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; round 46 re-fetched S246-S248, S237 and S242-S244 and re-ran the S249 capture (`.ufo/waves/round-46/w1/C2ExecLiveSources.md`, `C2ExecHostRecheck.md`); round 45 re-fetched S237 and S242-S244 byte-identical (`a2w1/SrcGateReopen.md`); round 43 re-fetched S237 and S240 byte-identical and checked the Arch kernel patch set (no `fs/` file). | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 required at the round-46 outcome commit (receipts at base `2042117c` and IMPL `a4477049`: `.ufo/waves/round-46/w1/SelfAssess/`). | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; the round-44 IN-109 harm repaired by the round-45 repin (`check-adjacency-anchors.py` PASS at `44560592`); round 46 moves no live sibling pin; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |
```

Parser simulation (run, not assumed): I fed the fenced block above, with stand-in integers
(4500 / 1260 / 68 / 467) in the placeholders, through the checker's own text helpers
(`find_section`, `table_blocks`, `pick_table`, `split_cells`, `number_after`) imported from
`tools/check-self-assessment.py`. Observed: declaring round 46; 6 axis rows, 4 cells each; K07 67,
K08 4500, K09 1260, K10 68, K11 467, K13 160; K14 `not landed` substring absent and `` `--identity`
landed `` present; K12 and K15 phrases present. So the shape is parseable and the only remaining work
is substituting the measured integers.

Notes on why the cells are worded that way (all from the checker source):

- K07 reads the first `(\d+)\s+notes\b` in the depth row → the row must open with `67 notes`.
- K08 needs the literal `` `SKILL.md` N `wc -l` ``; K09 needs `N table lines`; K11 needs
  `` `corpus/README.md` N `wc -l` ``; K10 reads the first `N files` after `corpus/lessons/`.
- K14 tests `` `--identity` not landed `` **before** `` `--identity` landed ``, so the operability row
  must not contain the backticked phrase `` `--identity` not landed `` anywhere. The draft says
  "`--identity` landed (D12 closed …)" and nothing else.
- K12/K15 need the phrases `Core, Frontier and Adjacent sections present` and
  `formal overlap table present` retained; the draft keeps both.

### 3a. Second surface that must change with it — the capabilities table (K17)

K17 re-reads the `host-census-gate` row of `## Capabilities — current full evidence set (round 45)`
(`SCORECARD.md:2949`) and compares its case count with the census selftest. Required change in that
row (nothing else in it):

```
selftest prints PASS (160 cases, 160 passed, 0 failed)
```

in place of `selftest prints PASS (154 cases, 154 passed, 0 failed)`. The row's three named paths
(`tools/tsukuroi-census.sh`, `.ufo/evidence/round-1-kaika/scout-live.md`,
`.ufo/evidence/round-1-kaika/after.md`) exist at IMPL and must stay untouched. Do **not** add a
round-46 evidence path to that row unless it is committed at the same revision — a path absent at the
revision is a K17 mismatch.

## 4. Which draft values depend on files not yet written

| Cell | Value today (committed at IMPL) | Depends on |
|---|---|---|
| depth, notes | 67 | nothing pending: `corpus/knowledge/census-identity-r46.md` is committed at IMPL; no further note is declared for round 46 (68 only if one is added) |
| depth, `SKILL.md` `wc -l` | 4424 | **unwritten**: the round-46 SKILL sections (C1 identity section, C2 `## Scrub grounding — round 46 admission`, round46 registry continuation). Precedent sizes: round-45 section 54 lines (`SKILL.md:4232-4285`), scrub section 61 lines (`:4286-4346`), registry continuation 78 lines (`:4347-4424`) — so the delta is ~100-200 lines, not derivable until written |
| depth, table lines | 1241 | **unwritten**: the registry continuation's header + one row per round-46 counter (2 new counters: `score-census-identity-r46.py`, `check-scrub-admission-r46.py`) |
| depth, lesson files | 67 | **unwritten**: `corpus/lessons/round-46.md` (ScribeLesson drafts it as text; the L1 commits it). 68 once it lands — the round-45 table's `66` was already stale by exactly this mechanism at base |
| coverage, README `wc -l` | 466 | **unwritten**: if C2 admits, the `admitted round 46` line appended → 467; if the stale pending sentence at `corpus/README.md:465-466` is edited in place → 466; if C2 is refused → 466 |
| operability, cases | 160 | nothing pending: 160 measured at IMPL; changes only if further `(R46-C1)`-class cases land |
| calibration, mismatches 0 | 5 mismatches at IMPL | **unwritten**: the table itself. It is 0 only when this table lands with every K07-K11 value filled at that commit |

Therefore the table must be written **last** in the round, after the SKILL/README/lesson appends, and
its K08/K09/K10/K11 cells filled by running the commands at that commit — not copied from round 45.

## 5. What I did not do

- No check was run beyond the two receipts: `check-adjacency-anchors.py`, `check-registry-coverage.py`
  and the other gates are other seats' items.
- I did not verify the census `--identity` behaviour itself (C1 seats own that); I only counted the
  case labels and read the K13/K14 observations the checker printed.
- I did not score a fixture variant of the draft table (that would need a clone plus another census
  run); the K01 caveat in §3 is derived from the checker's own `reference_lines` executed against the
  current SCORECARD at declaring rounds 45 and 46, which returns identical references
  (8, 9, 9, 9, 9, 8).
- No tool was installed or upgraded (none needed).

## 6. Risk for the L1

The four new mismatches (K07, K13, K14, K17) are *not* a regression the C1 kill rules name, but any
no-harm table that compares `check-self-assessment.py` base→IMPL will show 1 → 1 with four new ids;
state them, and land §3 + §3a at the same commit that appends the round-46 table so the round's own
calibration row is true.
