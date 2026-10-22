# Round 26, wave 1 — ExecMemCheckerHarden

Seat: `TsukuroiR26.ExecMemCheckerHarden`. Date: 2026-10-22. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Routed defect 4 (round-25 spot-check line 106): harden `tools/check-memory-pressure.py`.

Verdict: done. All six changes are implemented in the seat's own clone, the tool's selftest passes with 41 cases and 0 failures, the pristine baseline is 6 of 6 with exit 0 at both `157ee2556a75bf4d1ae4893d4a06c020ae531ac0` and `b13e991fb96972b423b868ba122187f75357368c`, and the 17 wave-2 mutants now score killed 16 / survived 1 (N17 only), with the wave-1 catalogue scoring killed 10 / survived 0 / other 2 (M11 inapplicable, M12 killed under other finding ids).

## 1. The hardened tool

- File: `tools/check-memory-pressure.py` in the seat clone `/fast/scratch/hyaku/tsuku26/ExecMemCheckerHarden/repo`.
- New sha256: `019a9fa5a446d65577ec3c7dd50ca59acbc29562b43d62fed0516067298edbd7`.
- Lane HEAD (`b13e991`) tool sha256 for comparison: `077bd4843ad54433a6bf705fa06631008f0b526b0c9cef86b93c86da0fdbabcf`.
- Seat commit: `5a55076a7bab3b44f5e9645a9d2fc3e40c8288a8` on branch `seat/ExecMemCheckerHarden` in the seat clone. The lane repository was not written to and nothing was pushed.
- Diff against the lane HEAD copy of the file: 159 insertions, 24 deletions (`git diff --stat`); the diff is kept at `/fast/scratch/hyaku/tsuku26/ExecMemCheckerHarden/tool.diff` (18681 bytes, sha256 `e2504ce5579bc11573c17a189bef3b33e4e21e8d01d5dbe9e84743154b89e6ee`).

## 2. The six changes, one by one

1. **A Gate or entry quote mismatch blocks the row.** `MP-QUOTE-MISMATCH` and `MP-QUOTE-SOURCE-UNKNOWN` were raised with `blocking=False`; they are now blocking findings, so a row whose entry quote is not the quote the lesson's Gate records for that source no longer verifies. Evidence: the previous behaviour is recorded at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-25.md:78` ("the 9 survivors are in the quote rule (a Gate or entry quote mismatch is a non-blocking finding)"), and the new behaviour is measured by mutants N10, N11, N12 and N13 in section 5.

2. **The Gate quote over 25 words blocks the row.** The old rule was "at least one Gate quote of at most 25 words exists for one of the row's sources", so one over-long quote was tolerated as long as a shorter quote existed elsewhere. The hardened rule is per quote: every Gate quote of every source the row cites must be at most 25 words, and an over-long one raises the blocking `MP-QUOTE-TOO-LONG` on that row. N04 (one S118 Gate quote of 26 words) now dies; it survived before. New finding site is the source id.

3. **The SKILL rule requires the id in the first cell of a table line inside the round-25 section.** The rule was `any(id_in_line(line, row_id) for line in skill_table)` over every table line of the whole file, so the gate-registry row that merely mentions "MP1 to MP6" satisfied it. The hardened reader takes the section headed `## Memory pressure and systemd-oomd — round 25` (heading matched after whitespace and dash normalisation, so the em dash in the file matches the constant), collects its table lines and reads only the **first cell** of each. N09 (row deleted) and N15 (row id renamed) now die; both survived before.

4. **Row ids must be distinct; a duplicate is an error.** A repeated row id is now raised as an entry-level `MP-ROW-ID-DUPLICATE` with `global_blocked = True`, so `verified_rows` is 0 and the exit code is 1. The per-row duplicate finding is still raised as well. N14 now dies; it survived before with `verified_rows` 6.

5. **Each row needs at least one tier-A source.** `corpus/SOURCES.md` has a `tier` column; the checker now reads it (by header name, with the positional fallback kept) and raises the blocking `MP-SOURCE-TIER-NOT-A` when no source the row lists is tier `A`. The rule applies to the sources the registry knows: a row whose only source is missing from the registry is already blocked by `MP-SOURCE-MISSING`, so the tier rule does not fire on top of it. S125 is tier B (sibling lane mori), which is the case the wave-2 critic flagged.

6. **Lesson prose lines with an S id and the word recheck but no arrow never crash the parser.** The crash at `c93bd70f` was reproduced here: `recheck_log()` reached `old.strip(...)` with `old` still `None` for a prose line that names a source and the word "recheck" but shows no `old -> new` change, raising `AttributeError: 'NoneType' object has no attribute 'strip'`. The reader now skips such a line. Reproduced and fixed at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-25-verifier-spotcheck.md:106` ("At `c93bd70f` the checker crashed on lesson prose, and the lesson text was reworded rather than the tool fixed").

## 3. Selftest

Command: `python3 tools/check-memory-pressure.py --selftest` in the seat clone.

Result: `PASS`, 41 cases, 0 failed. Full JSON at `/fast/scratch/hyaku/tsuku26/ExecMemCheckerHarden/selftest.json`, sha256 `dcb09f8dd7bf619190c31c4f9b3759129b204cacd4ee73ead5eee8a63fb32b9e`.

The nine new cases (one per new rule, plus the two skill-rule shapes):

| case | what it pins | expected |
|---|---|---|
| `source-tier-not-a` | a row whose only source is the tier-B S125 | exit 1, verified_rows 5, `MP-SOURCE-TIER-NOT-A` |
| `gate-quote-mismatch-blocks` | the Gate quote of a cited source differs from the entry quote | exit 1, verified_rows 5, `MP-QUOTE-MISMATCH` |
| `entry-quote-mismatch-blocks` | the entry quote is not the quote the Gate records | exit 1, verified_rows 5, `MP-QUOTE-MISMATCH` |
| `entry-quote-unknown-source-blocks` | the entry quote names a source the row does not list | exit 1, verified_rows 5, `MP-QUOTE-SOURCE-UNKNOWN` |
| `gate-quote-over-cap-blocks` | the Gate quote of a cited source is 26 words | exit 1, verified_rows 5, `MP-QUOTE-TOO-LONG` |
| `skill-row-id-not-in-first-cell` | the id sits in a later cell of the round-25 table | exit 1, verified_rows 5, `MP-SKILL-ROW-MISSING` |
| `skill-row-in-other-section-only` | the id sits in a table of another SKILL.md section | exit 1, verified_rows 5, `MP-SKILL-ROW-MISSING` |
| `duplicate-row-id` | the entry carries a row id twice | exit 1, verified_rows 0, `MP-ROW-ID-DUPLICATE` |
| `recheck-prose-without-arrow` | a lesson prose line naming a source and "recheck" with no arrow | exit 0, verified_rows 6, no findings (no crash) |

Two existing selftest expectations changed because the rules are now stricter, and both are recorded rather than papered over: `no-sources` now also reports `MP-QUOTE-SOURCE-UNKNOWN` (the row's quote names a source the row no longer lists), and `quote-missing` reports `MP-QUOTE-MISSING` without `MP-QUOTE-MISMATCH` (the mismatch is only raised against quotes the Gate actually carries, so a missing Gate quote is not double-counted as a mismatch).

## 4. Pristine baseline

Measured with the hardened tool through `git_reader` at the bound revision, on the lane repository, read-only:

| revision | exit | verified_rows | status | findings |
|---|---|---|---|---|
| `157ee2556a75bf4d1ae4893d4a06c020ae531ac0` | 0 | 6 | PASS | none |
| `b13e991fb96972b423b868ba122187f75357368c` | 0 | 6 | PASS | none |

The wave-2 harness baseline over the same tree also reports `BASELINE: PASS exit=0 verified_rows=6 findings=[]`, and the wave-1 runner reports `baseline: PASS (exit 0, verified_rows 6)`.

## 5. Mutant replay, wave-2 catalogue (17 mutants)

Harness: the committed `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC2Rules/harness.py` and `catalogue-w2.json`, copied to `/fast/scratch/hyaku/tsuku26/ExecMemCheckerHarden/`. Two constants were changed in the copy and nothing else: `REV` became `157ee2556a75bf4d1ae4893d4a06c020ae531ac0` (the revision the task names) and `SEAT` became this seat's directory; the copy also installs the hardened tool over the archived copy inside each sandbox, because the archive carries the lane's committed tool and the replay must measure the hardened one. Every sandbox is built by `git -C <lane> archive <rev> | tar -x` plus `git init`, with no remote.

Command: `python3 harness.py --catalogue catalogue-w2.json --out result-w2.json --workdir .../work`.
Result JSON: `/fast/scratch/hyaku/tsuku26/ExecMemCheckerHarden/result-w2.json`, sha256 `164406974d450487506618c7158bf1d6378f0016b8bb6e87bf563de51884995d`.

| id | mutation | wave-2 verdict (before) | verdict now | exit | verified_rows | findings now |
|---|---|---|---|---|---|---|
| N01 | S115 status `mined` -> `queued` | KILLED | KILLED | 1 | 4 | `MP-SOURCE-STATUS-NOT-MINED` x2 |
| N02 | S116 used-by emptied | KILLED | KILLED | 1 | 5 | `MP-SOURCE-USED-BY-MISSING` |
| N03 | S117 opened `2026-10-21` | KILLED | KILLED | 1 | 5 | `MP-SOURCE-OPENED-STALE` |
| N04 | S118 Gate quote -> 26 words | SURVIVED | **KILLED** | 1 | 4 | `MP-QUOTE-TOO-LONG`, `MP-QUOTE-MISMATCH` |
| N05 | MP1 pointer -> capture header | KILLED | KILLED | 1 | 5 | `MP-CAPTURE-POINTER-HEADER`, `MP-CAPTURE-POINTER-UNUSABLE` |
| N06 | MP6 pointer -> duplicated line | KILLED | KILLED | 1 | 5 | `MP-CAPTURE-POINTER-NOT-UNIQUE`, `MP-CAPTURE-POINTER-UNUSABLE` |
| N07 | MP1 pointer -> absent token | KILLED | KILLED | 1 | 5 | `MP-CAPTURE-POINTER-TOKEN-ABSENT`, `MP-CAPTURE-POINTER-UNUSABLE` |
| N08 | capture bytes appended | KILLED | KILLED | 2 | 0 | `CAPTURE-TAMPERED` |
| N09 | SKILL.md MP6 decision row deleted | SURVIVED | **KILLED** | 1 | 5 | `MP-SKILL-ROW-MISSING` |
| N10 | lesson S118 Gate quote, one character | SURVIVED | **KILLED** | 1 | 5 | `MP-QUOTE-MISMATCH` |
| N11 | entry MP6 S118 quote, one character | SURVIVED | **KILLED** | 1 | 5 | `MP-QUOTE-MISMATCH` |
| N12 | entry MP6 S118 quote replaced | SURVIVED | **KILLED** | 1 | 5 | `MP-QUOTE-MISMATCH` |
| N13 | entry MP3 quote source S117 -> S119 | SURVIVED | **KILLED** | 1 | 5 | `MP-QUOTE-SOURCE-UNKNOWN`, `MP-QUOTE-MISMATCH` |
| N14 | entry duplicates row MP6 | SURVIVED | **KILLED** | 1 | 0 | `MP-ROW-ID-DUPLICATE` |
| N15 | SKILL.md MP6 row id -> MPX | SURVIVED | **KILLED** | 1 | 5 | `MP-SKILL-ROW-MISSING` |
| N16 | every S117/S118 Gate quote -> 26 words | KILLED | KILLED | 1 | 4 | `MP-QUOTE-TOO-LONG` x4, `MP-QUOTE-MISMATCH` x3 |
| N17 | Gate quote and entry quote changed together | SURVIVED | SURVIVED | 0 | 6 | none |

**Kill count: 16 killed, 1 survived (N17), 0 inconclusive.**

N17 still survives and is expected to: it changes the lesson's Gate quote and the entry's quote to the same text, so the two agree with each other. The checker never opens a cited page, so a pair that agrees with itself but with no source is invisible to it. The wave-2 report stated this limit (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC2Rules.md:15`) and the round-25 lesson records that the "sourced" half of the C2 rule is owed to the non-author closure, not self-granted (`corpus/lessons/round-25.md:40`). Closing N17 needs an external read of the cited page, which is outside the six changes this seat was given and outside the lane's committed-bytes-only instrument.

## 6. Mutant replay, wave-1 catalogue (12 entries)

Runner: the committed `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutMemPressurePlan/fixtures/run-mutations.py` with `mutations.json`, copied to this seat and pointed at the hardened tool and at the real tree at `157ee2556a75bf4d1ae4893d4a06c020ae531ac0` (`--baseline-repo` / `--baseline-rev`). Only the two path constants were changed in the copy.

Command: `python3 run-mutations.py --tool .../base/tools/check-memory-pressure.py --catalogue mutations-w1.json --baseline-repo <lane> --baseline-rev 157ee255... --out result-w1.json`.
Result JSON: `/fast/scratch/hyaku/tsuku26/ExecMemCheckerHarden/result-w1.json`, sha256 `8d6a6759cf1a0460fe02fe03efcb74050e171199c19ae294ea10813542c3e8d2`.

| id | mutation | verdict | exit | verified_rows | findings |
|---|---|---|---|---|---|
| M01 | S115 status -> `queued` | KILLED | 1 | 4 | `MP-SOURCE-STATUS-NOT-MINED` x2 |
| M02 | S116 used-by -> another entry | KILLED | 1 | 5 | `MP-SOURCE-USED-BY-MISSING` |
| M03 | S117 opened -> `2026-10-21` | KILLED | 1 | 5 | `MP-SOURCE-OPENED-STALE`, `MP-QUOTE-MISSING` |
| M04 | S118 Gate quote -> 26 words (wave-1 op writes the quote cell) | KILLED | 1 | 4 | `MP-QUOTE-TOO-LONG` x2 |
| M05 | MP1 pointer -> capture header | KILLED | 1 | 5 | `MP-CAPTURE-POINTER-HEADER`, `MP-CAPTURE-POINTER-UNUSABLE` |
| M06 | MP2 pointer -> command echo | KILLED | 1 | 5 | `MP-CAPTURE-POINTER-ECHO`, `MP-CAPTURE-POINTER-UNUSABLE` |
| M07 | MP3 pointer -> exit line | KILLED | 1 | 5 | `MP-CAPTURE-POINTER-EXIT`, `MP-CAPTURE-POINTER-UNUSABLE` |
| M08 | MP6 pointer -> duplicated line | KILLED | 1 | 5 | `MP-CAPTURE-POINTER-NOT-UNIQUE`, `MP-CAPTURE-POINTER-UNUSABLE` |
| M09 | capture bytes appended | KILLED | 2 | 0 | `CAPTURE-TAMPERED` |
| M10 | SKILL.md decision row MP6 deleted | KILLED | 1 | 5 | `MP-SKILL-ROW-MISSING` |
| M11 | entry MP4 S118 quote replaced | INCONCLUSIVE | – | – | mutation could not be applied: row MP4 carries no quote for S118 (the wave-2 report recorded the same inapplicability) |
| M12 | S115 row drops the `teaches` cell | KILLED-OTHER | 1 | 4 | `MP-SOURCE-STATUS-NOT-MINED`, `MP-SOURCE-USED-BY-MISSING`, `MP-SOURCE-OPENED-STALE` (x2 each) |

**Kill count: 10 killed, 0 survived, 2 other (M11 inapplicable, M12 killed under other finding ids).** M12's catalogue expectation `MP-SOURCE-ROW-SHAPE` is a finding id the tool has never emitted, so the wave-1 runner records KILLED-OTHER; the mutation is detected, by other ids.

Both wave-1 survivors from the wave-2 report are now dead: M10 was a survivor before and is KILLED now (the SKILL first-cell rule).

## 7. What is not covered

- N17 (and the same shape in wave 1) is still invisible to the instrument: the checker compares the entry's quote with the lesson's Gate copy of it and never opens the cited page. This is a known, recorded limit of the committed-bytes instrument, not a gap introduced by this hardening.
- The tier-A rule reads the `tier` column of `corpus/SOURCES.md`. A registry without a `tier` column (or with a differently named one) yields an empty tier for every row and would block every row with `MP-SOURCE-TIER-NOT-A`. The lane's registry has the column, and the positional fallback keeps the reader working if the header line is ever renamed.
- The lane repository was not written to by this seat apart from this report file; the lane `git rev-parse HEAD` is still `b13e991fb96972b423b868ba122187f75357368c`. No `git` or `jj` write command was run against the lane, and nothing was pushed.

## 8. Evidence pointers

- Hardened tool: `/fast/scratch/hyaku/tsuku26/ExecMemCheckerHarden/repo/tools/check-memory-pressure.py`, sha256 `019a9fa5a446d65577ec3c7dd50ca59acbc29562b43d62fed0516067298edbd7`; seat commit `5a55076a7bab3b44f5e9645a9d2fc3e40c8288a8` on branch `seat/ExecMemCheckerHarden` of the seat clone.
- Selftest: `python3 tools/check-memory-pressure.py --selftest` -> `PASS`, 41 cases, 0 failed; JSON sha256 `dcb09f8dd7bf619190c31c4f9b3759129b204cacd4ee73ead5eee8a63fb32b9e`.
- Wave-2 replay: 16 killed, 1 survived, 0 inconclusive; `result-w2.json` sha256 `164406974d450487506618c7158bf1d6378f0016b8bb6e87bf563de51884995d`.
- Wave-1 replay: 10 killed, 0 survived, 2 other; `result-w1.json` sha256 `8d6a6759cf1a0460fe02fe03efcb74050e171199c19ae294ea10813542c3e8d2`.
- Baseline at `157ee2556a75bf4d1ae4893d4a06c020ae531ac0`: exit 0, verified_rows 6, PASS, no findings. At `b13e991fb96972b423b868ba122187f75357368c`: exit 0, verified_rows 6, PASS, no findings.
- Crash reproduced before the fix: `AttributeError: 'NoneType' object has no attribute 'strip'` raised by `recheck_log()` on the lesson prose line at `c93bd70f` (`corpus/lessons/round-25.md:72` of that revision), which names S120 and the word "recheck" and shows no `old -> new` change.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin (tools/check-memory-pressure.py, corpus/knowledge/memory-pressure-r25.json, corpus/SOURCES.md, corpus/lessons/round-25.md, corpus/lessons/round-25-verifier-spotcheck.md, SKILL.md, .ufo/waves/round-25/w2/MutC2Rules/harness.py, .ufo/waves/round-25/w2/MutC2Rules/catalogue-w2.json, .ufo/waves/round-25/w1/MutMemPressurePlan/fixtures/run-mutations.py, .ufo/waves/round-25/w1/MutMemPressurePlan/fixtures/mutations.json, .ufo/waves/round-25/capture/capture.txt), /home/vgpnk/.omp/agent/RULES.md, skill://godspeed; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/ExecMemCheckerHarden.md, /fast/scratch/hyaku/tsuku26/ExecMemCheckerHarden/repo/tools/check-memory-pressure.py (seat clone, commit 5a55076), /fast/scratch/hyaku/tsuku26/ExecMemCheckerHarden/{harness.py,catalogue-w2.json,run-mutations.py,mutations-w1.json,base/tools/check-memory-pressure.py,base/tools/_revision.py,result-w2.json,result-w1.json,selftest.json,tool.diff}; executed=git archive and read-only git show/merge-base against the lane, git init/add/commit in seat sandboxes only, python3 tools/check-memory-pressure.py --selftest, python3 harness.py --catalogue catalogue-w2.json --out result-w2.json, python3 run-mutations.py --tool ... --catalogue mutations-w1.json --baseline-repo ... --baseline-rev 157ee255 --out result-w1.json

Model: opencode-go/minimax-m3.1-flash-free
Installs: none
