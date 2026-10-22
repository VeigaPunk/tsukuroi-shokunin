# Round 25, wave 2 — mutation test of `tools/check-memory-pressure.py` against the real integrated entry

Seat: `TsukuroiR25.MutC2Rules`. Date: 2026-10-22. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Measured revision under test: `5e7c04ecb02735491456de2b8bc44550d0db4609` (the lane `HEAD` at the time of the run).

Verdict: partly holds. The checker kills 8 of 17 mutants and 9 survive; every survivor is in the quote rules (R3) or the SKILL.md rule (R5), plus the row-counting rule, so the declared `verified_rows` count of 6 does not react to a quote the cited page does not supply, to a missing SKILL.md decision row, or to a duplicated entry row. The source, pointer and capture rules all killed their mutants.

## 1. Method and baseline

1. [obs] Every mutant is a full sandbox built from `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 5e7c04ecb02735491456de2b8bc44550d0db4609 | tar -x -C <dir>`, then `git init` with no remote, one mutation applied, `git add -A`, one commit, and measured with the sandbox's own tool: `python3 tools/check-memory-pressure.py --revision <commit>`. The harness is `/fast/scratch/hyaku/tsukuroi-r25/w2/MutC2Rules/harness.py`, copied to `.ufo/waves/round-25/w2/MutC2Rules/harness.py`; the catalogue is `.ufo/waves/round-25/w2/MutC2Rules/catalogue-w2.json`.
2. [obs] The pristine baseline is green: `status PASS, verified_rows 6, declared_rows 6, findings []`, exit 0. A green baseline makes every kill meaningful; a red baseline would have made every mutant inconclusive.
3. [obs] The lane working tree is byte-identical to the archive at the measured revision for every file the checker reads: `corpus/knowledge/memory-pressure-r25.json` `152517e9…`, `corpus/SOURCES.md` `f08cbda8…`, `corpus/lessons/round-25.md` `5e6817be…`, `SKILL.md` `f0ed6d2f…`, `.ufo/waves/round-25/capture/capture.txt` `e60f1bbc…`, `tools/check-memory-pressure.py` `077bd484…`. No lane file was written by this seat; no `git` or `jj` write command was run against the lane; `git -C <lane> rev-parse HEAD` is still `5e7c04ec…`. The sandboxes are disposable copies under `/fast/scratch/hyaku/tsukuroi-r25/w2/MutC2Rules/`, so restoration is the untouched lane tree plus the identical hashes above.

## 2. Wave-1 catalogue re-run against the real baseline

Command: `python3 run-mutations.py --tool /fast/scratch/hyaku/tsukuroi-r25/w2/MutC2Rules/base/tools/check-memory-pressure.py --catalogue /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutMemPressurePlan/fixtures/mutations.json --baseline-repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --baseline-rev 5e7c04ecb02735491456de2b8bc44550d0db4609 --out result-w1sweep.json`. The runner was copied to my seat directory with only its `SCRATCH` constant redirected (`/fast/scratch/hyaku/tsukuroi-r25/w2/MutC2Rules/run-mutations.py`, sha256 `392a89aa…`; the lane's working-tree copy is `39f4e130…` and the committed copy is `f9fca4b5…`). Full record: `.ufo/waves/round-25/w2/MutC2Rules/result-w1sweep.json`.

| id | mutation | verdict | exit | verified_rows | findings |
|---|---|---|---|---|---|
| M01 | S115 status → queued | KILLED | 1 | 4 | MP-SOURCE-STATUS-NOT-MINED ×2 |
| M02 | S116 used-by → another file | KILLED | 1 | 5 | MP-SOURCE-USED-BY-MISSING |
| M03 | S117 opened → 2026-10-21 | KILLED | 1 | 5 | MP-SOURCE-OPENED-STALE, MP-QUOTE-MISMATCH |
| M04 | S118 Gate quote → 26 words | SURVIVED | 0 | 6 | none |
| M05 | MP1 pointer → capture header | KILLED | 1 | 5 | MP-CAPTURE-POINTER-HEADER, MP-CAPTURE-POINTER-UNUSABLE |
| M06 | MP2 pointer → command echo | KILLED | 1 | 5 | MP-CAPTURE-POINTER-ECHO, MP-CAPTURE-POINTER-UNUSABLE |
| M07 | MP3 pointer → exit line | KILLED | 1 | 5 | MP-CAPTURE-POINTER-EXIT, MP-CAPTURE-POINTER-UNUSABLE |
| M08 | MP6 pointer → duplicated line | KILLED | 1 | 5 | MP-CAPTURE-POINTER-NOT-UNIQUE, MP-CAPTURE-POINTER-UNUSABLE |
| M09 | capture byte appended | KILLED | 2 | 0 | CAPTURE-TAMPERED |
| M10 | SKILL.md row MP6 deleted | SURVIVED | 0 | 6 | none |
| M11 | MP4 quote for S118 replaced | INCONCLUSIVE | – | – | mutation could not be applied: row MP4 carries no quote for S118 |
| M12 | S115 `teaches` cell dropped | KILLED-OTHER | 1 | 4 | MP-SOURCE-STATUS-NOT-MINED, MP-SOURCE-USED-BY-MISSING, MP-SOURCE-OPENED-STALE |

4. [obs] M04 survives with no finding at all, because the wave-1 operation writes the long quote into cell index 2 of the Gate row, which in the real lesson is the URL column (`corpus/lessons/round-25.md:11` header `| Source | URL | Opened | Located quote (at most 25 words) | Location |`, quote is cell 3). The tool reads the quote from the header-named column, so nothing changed for it. The same defect is reproduced deliberately below as N04, written into the real quote column.
5. [obs] M11 is inapplicable to the integrated entry: the real row MP4 cites S121, S122 and S123 and carries no S118 quote; S118 belongs to MP3 and MP6. The wave-1 catalogue's row/source pairing does not hold against the landed entry.
6. [obs] M12 expects a finding id `MP-SOURCE-ROW-SHAPE` that the tool never emits. The tool reads the registry by header names (`tools/check-memory-pressure.py:249-292`), so a dropped cell shifts the columns and the row is read as status-not-mined, used-by-missing and opened-stale. The mutant is detected, but by other ids than the catalogue names.
7. [obs] M01 drops two rows, not one: S115 is cited by MP1 and MP2, so `verified_rows` goes 6 → 4. The catalogue's `expected_verified_rows: 5` for M01 does not hold against the real tree.
8. [obs] M03 also removes a Gate row as a side effect: the wave-1 operation deletes every lesson line that contains the source id and an arrow, and the S117 Gate quote contains `cgrp->psi`. The row still fails only because of the opened date; the lost Gate quote alone did not break it (see finding 11).

## 3. Wave-2 mutants against the real integrated entry

Harness: `.ufo/waves/round-25/w2/MutC2Rules/harness.py`, catalogue `.ufo/waves/round-25/w2/MutC2Rules/catalogue-w2.json`, results `.ufo/waves/round-25/w2/MutC2Rules/result-w2.json`.

| id | mutation (real file) | expected finding | verdict | exit | verified_rows | findings emitted |
|---|---|---|---|---|---|---|
| N01 | `corpus/SOURCES.md` S115 status `mined` → `queued` | MP-SOURCE-STATUS-NOT-MINED | KILLED | 1 | 4 | MP-SOURCE-STATUS-NOT-MINED ×2 |
| N02 | `corpus/SOURCES.md` S116 used-by emptied | MP-SOURCE-USED-BY-MISSING | KILLED | 1 | 5 | MP-SOURCE-USED-BY-MISSING |
| N03 | `corpus/SOURCES.md` S117 opened → `2026-10-21` | MP-SOURCE-OPENED-STALE | KILLED | 1 | 5 | MP-SOURCE-OPENED-STALE |
| N04 | `corpus/lessons/round-25.md` S118 Gate quote → 26 words (real quote column) | MP-QUOTE-TOO-LONG | SURVIVED | 0 | 6 | MP-QUOTE-MISMATCH |
| N05 | entry JSON MP1 pointer → capture line 12 (header) | MP-CAPTURE-POINTER-HEADER | KILLED | 1 | 5 | MP-CAPTURE-POINTER-HEADER, MP-CAPTURE-POINTER-UNUSABLE |
| N06 | entry JSON MP6 pointer → capture line 21 (text twice) | MP-CAPTURE-POINTER-NOT-UNIQUE | KILLED | 1 | 5 | MP-CAPTURE-POINTER-NOT-UNIQUE, MP-CAPTURE-POINTER-UNUSABLE |
| N07 | entry JSON MP1 pointer token → `nonexistenttoken` | MP-CAPTURE-POINTER-TOKEN-ABSENT | KILLED | 1 | 5 | MP-CAPTURE-POINTER-TOKEN-ABSENT, MP-CAPTURE-POINTER-UNUSABLE |
| N08 | capture bytes appended (sha256 `e60f1bbc…` → `6459b6cc…`) | CAPTURE-TAMPERED | KILLED | 2 | 0 | CAPTURE-TAMPERED |
| N09 | `SKILL.md` decision row `MP6` deleted | MP-SKILL-ROW-MISSING | SURVIVED | 0 | 6 | none |
| N10 | lesson S118 Gate quote `Shows…` → `shows…` (one character) | MP-QUOTE-MISMATCH | SURVIVED | 0 | 6 | MP-QUOTE-MISMATCH |
| N11 | entry MP6 quote `The number…` → `the number…` (one character) | MP-QUOTE-MISMATCH | SURVIVED | 0 | 6 | MP-QUOTE-MISMATCH |
| N12 | entry MP6 quote replaced by unrelated text | MP-QUOTE-MISMATCH | SURVIVED | 0 | 6 | MP-QUOTE-MISMATCH |
| N13 | entry MP3 quote source `S117` → `S119` (not a source of the row) | MP-QUOTE-SOURCE-UNKNOWN | SURVIVED | 0 | 6 | MP-QUOTE-SOURCE-UNKNOWN, MP-QUOTE-MISMATCH |
| N14 | entry JSON duplicates row MP6 | MP-ROW-ID-DUPLICATE | SURVIVED | 0 | 6 | MP-ROW-ID-DUPLICATE |
| N15 | `SKILL.md` decision row id `MP6` → `MPX` | MP-SKILL-ROW-MISSING | SURVIVED | 0 | 6 | none |
| N16 | every Gate quote of S117 and S118 → 26 words | MP-QUOTE-TOO-LONG | KILLED | 1 | 5 | MP-QUOTE-TOO-LONG + 3 × MP-QUOTE-MISMATCH |
| N17 | lesson Gate quote and entry quote for MP3/S118 both set to a text no page supplies | (none) | SURVIVED | 0 | 6 | none |

Summary line of the harness run: `summary: killed=8 survived=9 inconclusive-or-other=0`, with `BASELINE: PASS exit=0 verified_rows=6 findings=[]`.

## 4. What the checker really enforces, and what it does not

9. [obs] The source rules hold: a source whose status is not `mined`, whose used-by cell does not name the entry, or whose opened date is not 2026-10-22 with no logged in-place recheck, disqualifies its row and drops the count (N01, N02, N03). Evidence: `tools/check-memory-pressure.py:566-572`, exit 1 and `verified_rows` 4 or 5 in each case.
10. [obs] The capture-pointer rules hold: header, command echo, exit line, non-unique text and a token the line does not carry are each fatal for the row, and the capture digest is checked before anything else (N05, N06, N07, N08). Evidence: `tools/check-memory-pressure.py:413-445` and `:474`.
11. [obs] **A quote that the cited page does not supply does not change the count.** `MP-QUOTE-MISMATCH` and `MP-QUOTE-SOURCE-UNKNOWN` are raised with `blocking=False` (`tools/check-memory-pressure.py:600` and `:605`), and a row is verified when it carries no blocking finding (`:634`). A Gate quote that differs from the entry quote by one character (N10), an entry quote that differs from the Gate quote by one character (N11), a replaced quote (N12), and a quote attributed to a source the row does not list (N13) all leave the counting command at exit 0 with `verified_rows` 6. The finding text is printed, but the declared field does not move.
12. [obs] **The 25-word cap is enforced per row, not per quote.** A Gate quote longer than 25 words is only recorded in `quote_detail`; the finding `MP-QUOTE-TOO-LONG` is raised only when the row has no qualifying (short) quote left among all its sources (`tools/check-memory-pressure.py:580-609`). N04 (one S118 Gate quote of 26 words) survives with exit 0. N16, which lengthens every Gate quote of both MP3 sources, is killed with `MP-QUOTE-TOO-LONG` and exit 1. So the rule as implemented is "at least one Gate quote of one cited source is at most 25 words", not "the located quote is at most 25 words".
13. [obs] **The SKILL.md rule is satisfied by any table line that mentions the row id.** The rule is `skill_hit = any(id_in_line(line, row_id) for line in skill_table)` over every line of SKILL.md that starts with `|` (`tools/check-memory-pressure.py:627`), not over the decision table. After the decision row for MP6 is deleted (N09) or renamed to `MPX` (N15), the gate-registry row (`SKILL.md:2355` in the measured tree, line 2354 after the deletion) still reads `0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid`, so `MP6` is still "in" SKILL.md and the row stays verified. Evidence: the N09 mutant's SKILL.md holds 5 decision rows (`grep -c "^| MP[1-6] |" = 5`) and one surviving `MP6` occurrence, and the checker returns `status PASS verified_rows 6 findings []`. The wave-1 M10 mutant dies of the same cause.
14. [obs] **A duplicated row id is reported but does not change the count.** The entry may hold seven rows (`['MP1','MP2','MP3','MP4','MP5','MP6','MP6']` in the N14 mutant); `MP-ROW-ID-DUPLICATE` is raised on the second copy (`:537`), but `verified_rows` counts *rows* that are verified, not distinct ids (`:670`), so six rows are still verified, `verified_rows` is 6, and the command exits 0 with `status PASS`. Evidence: `status PASS verified_rows 6 declared_rows 6 rows 7 findings ['MP-ROW-ID-DUPLICATE']`.
15. [obs] **The checker never opens a cited page.** It compares the entry's quote with the lesson's Gate copy of the same quote; the URLs in the Gate are never fetched. N17 changes both sides together to a text no source supplies — `the kernel accounts stall time in microseconds per cgroup since boot`, written into the Gate row and into the entry's MP3 quote — and the checker returns `status PASS verified_rows 6 findings []`. [inf] The "sourced" half of the C2 rule is therefore a consistency check between two local files, not a source check; only the non-author closure can close that half, and the round-25 lesson says as much (`corpus/lessons/round-25.md:40`, "Spot-check result: owed to the non-author closure; not self-granted").
16. [inf] Coverage summary for the L1: the checker detects every mutation that removes a *source*, a *pointer* or the *capture*, and does not detect any mutation that leaves the entry and the lesson mutually consistent. Making `MP-QUOTE-MISMATCH` and `MP-QUOTE-SOURCE-UNKNOWN` blocking, counting distinct row ids in `verified_rows`, and restricting the SKILL.md rule to the decision-table rows would close findings 11 to 14. I did not change the contract or the tool; this is a coverage report only.

## 5. Reproduction

17. [obs] Reproduce the wave-2 sweep with `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC2Rules/harness.py --catalogue /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC2Rules/catalogue-w2.json --out /fast/scratch/hyaku/tsukuroi-r25/w2/MutC2Rules/result-w2.json`; it creates its sandboxes under `/fast/scratch/hyaku/tsukuroi-r25/w2/MutC2Rules/work/`. The two survivor sandboxes for the most informative cases (N09, N14) are kept there for inspection; the rest were deleted after their records were written.
18. [obs] Nothing in this seat touched the fleet repo, a sibling lane repo, `MANIFEST.json`, `.ufo/state`, the lane jj state or the lane Git index. No clone of the lane was made and nothing was pushed. The only writes are the seat paths named below.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin (SCORECARD.md round-25 sections, tools/check-memory-pressure.py, corpus/knowledge/memory-pressure-r25.json and .md, corpus/SOURCES.md, corpus/lessons/round-25.md, SKILL.md, .ufo/waves/round-25/capture/capture.txt, .ufo/waves/round-25/w1/MutMemPressurePlan/fixtures/run-mutations.py and mutations.json), /home/vgpnk/.omp/agent/RULES.md, skill://godspeed; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC2Rules.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC2Rules/{harness.py,catalogue-w2.json,result-w2.json,result-w1sweep.json}, /fast/scratch/hyaku/tsukuroi-r25/w2/MutC2Rules/{harness.py,catalogue-w2.json,run-mutations.py,result-w2.json,result-w1sweep.json,base/,work/N09,work/N14}; executed=git archive 5e7c04ec into /fast/scratch/hyaku/tsukuroi-r25/w2/MutC2Rules/base, git init plus git add and git commit inside each disposable sandbox (no remote), python3 tools/check-memory-pressure.py --revision <commit> inside each sandbox (17 wave-2 mutants plus one baseline, and the wave-1 catalogue's 12 mutants plus one baseline), python3 harness.py --catalogue catalogue-w2.json --out result-w2.json, python3 run-mutations.py --baseline-repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --baseline-rev 5e7c04ecb02735491456de2b8bc44550d0db4609 --out result-w1sweep.json, read-only git rev-parse HEAD and git status --porcelain, sha256sum on the lane files and on the archive copies
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
