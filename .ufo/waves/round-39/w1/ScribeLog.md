VERDICT: draft

# A-9 — round-39 `LOG.md` entry draft

Read-only seat. No lane file was created, edited or deleted except this report; no git/jj mutating command ran; no
package, service, mount or sysfs action ran; no tool was installed. All commands below are reads (`read`, `grep`,
`git log/show/diff/status`, `sed`, `ls`, `wc`, `cat`, `head`, `fold`, `date`, `python3 -c` on lane files).

## Evidence used

| # | Claim in the draft | Evidence |
|---|---|---|
| E1 | Round 38 admitted; closure §6.1/§6.2 routed R38-Q82-LEAK and R38-ABSENT-ROOT | `corpus/lessons/round-38-verifier-spotcheck.md:169` heading; item 1 at `:171-173`, item 2 at `:174-175`; admission at `:186-188`; round-38 defects table rows at `corpus/lessons/round-38.md:88-89` |
| E2 | Round-38 Gate flip condition for `pacman-hook-timing-r25.md` | `corpus/lessons/round-38.md:48`: “Flip: a lane-authored entry that applies C1–C9, re-points each citation by document to new lane rows opened in that round, and adds the propositions the lane does not hold (upgrade order old-Pre → scriptlets → new-Post; provider lifecycle)” |
| E3 | Routed defect 4 (S210 anchor) | `corpus/lessons/round-38-verifier-spotcheck.md:181`: “the anchor names the non-existent `_alpm_trans_commit`. Land a new row whose `teaches` opens `supersedes S210 —` with anchor `alpm_trans_commit` (`trans.c:167`, 201-240). Do not rewrite S210.” |
| E4 | C1 arm and its exact grammar | `tools/tsukuroi-census.sh:1903-1915` (`if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]`, `mounts:btrfs-without-sysfs`, `mounts:unreadable`); header supersede note `:365-368`; `PROC_MOUNTS` at `:460` |
| E5 | Four selftest cases; 113 → 117 | `tools/tsukuroi-census.sh:2974,2979,2984,2989`; `.ufo/waves/round-39/after/selftest-49cc53c.txt` = `TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)`; `git log --oneline -3 -- tools/tsukuroi-census.sh` shows `02eeed0 round-38: storage arm hardening (bad-devid, unlistable root; 113 selftest cases)…`; `git log b0005ae9..0eff65b -- tools/tsukuroi-census.sh` = empty |
| E6 | IN-109 re-pin 2425 → 2447 | `git show 49cc53c -- corpus/knowledge/adjacency-anchors-r19.json` = `- "found_line": 2425` / `+ "found_line": 2447` |
| E7 | Views built in the child namespace from stdin | `tools/score-storage-hidden-r39.py:7-10` (“every view is a tmpfs mounted INSIDE the child's unprivileged user+mount namespace (`unshare -rm`) and filled from data the child reads on stdin”); legs H1/H2 at `:15-16`; `:196-202` |
| E8 | C2 entry, TO rows, provenance | `corpus/knowledge/pacman-transaction-order-r39.md:1` (`source:` row), `:24-31` (TO1–TO8), `:53` (`## QUALITY check`); `corpus/SOURCES.md:222-227` (S213–S218); S217 row contains `supersedes S210 — the commit function is \`alpm_trans_commit\` (trans.c:167), not \`_alpm_trans_commit\``; `git show 4078eb2 -- corpus/SOURCES.md` shows S208 used-by gained the new entry and S210's row unchanged |
| E9 | SOURCES 212 → 218 | `git show 0eff65b:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3} '` = 212; `grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` = 218 |
| E10 | Before receipts | `.ufo/waves/round-39/before/c1-before.jsonl`: revision `0eff65b…`, hidden 0, views 3, fixtures 2, live 1, six 1, result FAIL exit 1; hidden legs H1/H2 both `… state=HEALTHY filesystems=0 devices=0 nonzero=0`. `.ufo/waves/round-39/before/c2-before.jsonl`: `entry_present false`, rules 0, source_ok 0, counts_ok 0, FAIL exit 1 |
| E11 | Author after receipts | `.ufo/waves/round-39/after/c1-after-49cc53c.jsonl`: hidden 2, views 3, fixtures 5, live 1, six 1, PASS exit 0, `branch_tip 4078eb2…`. `.ufo/waves/round-39/after/c2-after-4078eb2.jsonl`: rules 8, dup rows 0, dup headings 0, source_ok 1, counts_ok 2, oracle 0, PASS exit 0, `host {windows 86, transactions_started 60, scriptlet_tag_outside_commit 252, scriptlet_tag_total 441, running_inside_commit 0}`. Both under commit `2e1c2a4` (`git show --stat --oneline 2e1c2a4`) |
| E12 | Pre-seat controls | `.ufo/waves/round-39/controls/controls.jsonl` (12 rows): C1 K0 hidden 0/fixtures 2 FAIL; K1 hidden 0/fixtures 5 FAIL; K2 hidden 2/fixtures 4 FAIL; K3 hidden 2/fixtures 2 FAIL; K4 PASS. C2 K0 rules 0/counts 0 FAIL; E1 rules 0 FAIL; E2 rules 0 FAIL; E3 rules 5 FAIL; E4 rules 8 FAIL; E5 rules 8/counts 0 FAIL; E6 PASS |
| E13 | Commit provenance | `git show -s --format='%h %aI %cI %s'` on `6a08925 93fddb2 49cc53c 4078eb2 2e1c2a4 394e1ba`; authors/committers 02:34–03:01 -03:00 |
| E14 | Wave shape | `.ufo/waves/round-39/w1-spec.json` = dict with `items` of length 70, `wave` string, `maxLanes 100`; `git show --stat --oneline 394e1ba` lists `w1-spec.json`, `w1-dispatch.json`, `w1.ready`; `w1-results.json` absent at read time; 16 `w1/*.md` reports present |
| E15 | Declaration and side-effect prediction | `SCORECARD.md:2209` heading; C1 row `:2220`, C2 row `:2221`; controls paragraph `:2223-2230`; predicted side effect `:2232-2234` |

## Findings

1. **The declaration heading stamp is not an observed time.** `SCORECARD.md:2209` says
   `2026-10-26T06:20Z`. At read time `date -u` returned `2026-10-26T06:05:30Z`, and the commits that carry the
   declaration and both implementations carry author/committer times `02:59:31`/`02:59:31` (`93fddb2`),
   `02:59:31`/`02:59:37` (`49cc53c`), `02:59:37`/`02:59:39` (`4078eb2`) and `03:00:47`/`03:00:47` (`2e1c2a4`)
   `-03:00`, i.e. `05:59:31Z` through `06:00:47Z`. The claimed stamp is
   ~19 minutes after the read and ~20 minutes after the declaration's own commit. This is the round-36 bad-heading
   class (`LOG.md:1389` erratum) with a different failure: a valid-looking time that no observation supports.
   The draft below does **not** repeat `06:20Z`; its heading uses the observed `date -u` value, which must be
   re-stamped if the entry is appended later.
   `git show -s --format='%h %aI %cI' 49cc53c 93fddb2 4078eb2 2e1c2a4`; `date -u`.

2. **The round-39 SKILL and PROVINCE sections were uncommitted at draft time.** `git status --porcelain` shows
   ` M PROVINCE.md` and ` M SKILL.md`; `git diff --stat` = `PROVINCE.md 14 +`, `SKILL.md 21 +`. Their last commits are
   `b0005ae` (PROVINCE) and `6a08925` (SKILL), so the round-39 limit-closure section (`PROVINCE.md:225ff`) and the
   round-39 storage-arm table (`SKILL.md` diff at `@@ -3201,3 +3201,24 @@`) are working-tree only. The draft therefore
   lists integration under `‹INTEGRATION-COMMIT›` and does not claim those edits landed.

3. **The C2 entry does not evidence the whole round-38 flip condition, and its own cross-reference dangles at draft
   time.** `grep -c provider corpus/knowledge/pacman-transaction-order-r39.md` = 0, and the flip condition asks the
   entry to add “provider lifecycle” (`corpus/lessons/round-38.md:48`); the entry's header narrows its own claim to
   “the transaction-order propositions”. It also points at `corpus/lessons/round-39.md` (`:17-18`) and that file does
   not exist (`ls corpus/lessons/round-39*` → no match). The draft therefore says C2 “works the … surface the closure
   named” and “re-grounds that entry's transaction-order propositions”, not that C2 closes the flip condition. If the
   lesson lands with an integration commit the reference resolves; whether it records what the entry's header promises
   is the closure's reading, not this draft's.

4. **`SOURCES.md` row S208 was touched by the C2 commit** (its used-by cell gained
   `corpus/knowledge/pacman-transaction-order-r39.md`), while S210's row is byte-identical to its round-38 text
   (`git show 4078eb2 -- corpus/SOURCES.md`). The draft's sentence “S210 is not rewritten” is exact; it does not say
   “no existing row changed”.

5. **Live-leg reading vs exit code.** The C1 live leg matches `state=HEALTHY filesystems=1 devices=1 nonzero=0` with
   `six_planes: true` and `census_exit: 2` (`after/c1-after-49cc53c.jsonl`), i.e. the STORAGE line is clean while the
   overall census exits 2 for another plane. The draft states the live match and `six_planes_all 1` and does not
   present exit 2 as a C1 failure.

## Proposed entry — exact markdown

Insert after the round-38 entry's final paragraph (`LOG.md:1455`), matching its single-heading, single-block shape.

~~~~markdown
## Round 39 — storage-arm repair and the libalpm transaction order (hyaku run 8), 2026-10-26T06:05:30Z

Round 38 was admitted (`corpus/lessons/round-38-verifier-spotcheck.md`), and its closure routed the two storage-arm
defects this round takes: §6.1 R38-Q82-LEAK and §6.2 R38-ABSENT-ROOT (`:171-175`), both recorded unfixed at
`corpus/lessons/round-38.md:88-89` — a Q82 counter that admitted four arms reaching the view tree through
`$HOME`/`$TMPDIR` siblings and `/proc/self/mountinfo`'s mount root, and an absent `/sys/fs/btrfs` that read
`HEALTHY 0/0/0` in a namespace hiding it while btrfs was mounted. C1 operability addresses both in
`tools/tsukuroi-census.sh` `probe_storage_arm` (`:1903-1915`): with no fsid entry under the root the arm reads the
mount table (`TSUKUROI_PROC_MOUNTS`, default `/proc/self/mounts`) and prints `BLOCKED … detail=mounts:btrfs-without-sysfs`
when a btrfs mount is listed, `detail=mounts:unreadable` when the table cannot be read; a root with fsid entries never
reads the table, and the STORAGE line stays verdict-neutral. Four selftest cases (`storage-hidden-absent`,
`storage-hidden-empty`, `storage-mounts-unreadable`, `storage-mounted-populated`, `:2974-2992`) take the census
selftest 113 → 117; the insertion moved IN-109's anchored case 2425 → 2447, re-pinned in the same commit. The
counter's three production-path views are tmpfs mounts filled from the child's stdin inside an `unshare -rm` child,
so no host path, bind source or argv carries a view.

C2 depth (sourced) works the update-safety surface the round-38 closure named: the Gate flip condition for the
refused staged entry `pacman-hook-timing-r25.md` (`corpus/lessons/round-38.md:48`) and routed defect 4 — the S210
anchor naming the non-existent `_alpm_trans_commit` (`corpus/lessons/round-38-verifier-spotcheck.md:181`).
`corpus/knowledge/pacman-transaction-order-r39.md` re-grounds that entry's transaction-order propositions at pacman
`54d9411` and states TO1–TO8 (`:24-31`): Pre hooks before `transaction started`, removals before adds, per-package
pre-scriptlet → files → log line → post-scriptlet, new-version-first scriptlet arguments, hook directories re-read per
phase, `ldconfig` once, removal order, and every chroot child's output tagged `ALPM-SCRIPTLET`. The rules sit on new
rows S213–S218 plus S208 (`corpus/SOURCES.md:217, 222-227`), with S217 the `supersedes S210 —` row anchored at
`alpm_trans_commit` (`trans.c:167`, 201-240); S210 is not rewritten, and `.ufo/waves/round-39/frozen/txcapture/`
(MANIFEST sha256 `cb5cb4f4…`) supplies the host column. SOURCES 212 → 218.

Claims frozen at `6a08925d` and declared at `93fddb2c` on base `0eff65b2`: C1
`python3 tools/score-storage-hidden-r39.py --revision <REV>` (sha256 `75a9e8ab…`) — hidden 2/2, views 3/3, fixtures
5/5, live 1, six 1; C2 `python3 tools/check-transaction-order-r39.py --revision <REV>` (sha256 `f1c97836…`) — rules
8/8, no duplicate row or heading, source_ok 1, counts_ok 2, oracle_violations 0. C2's declared kill rule is per row:
a TO row judged FALSE against the pinned source at its cited lines kills the claim (QUALITY 81), and the counter
checks quote position, not truth. Controls before any seat (`controls/controls.jsonl`, clone with origin removed): C1
do-nothing, fixture-gated, over-block and mountinfo-keyed FAIL; C2 do-nothing, no-upstream-row, lines-shifted,
S-id-dropped, block-duplicated and host-counts-wrong FAIL; no wrong arm meets either target.

Before at base `0eff65b2` (`.ufo/waves/round-39/before/`): C1 hidden 0/2, views 3/3, fixtures 2/5, live 1, six 1, FAIL
exit 1, both hidden legs `HEALTHY 0/0/0`; C2 entry absent, rules 0/8, source_ok 0, counts_ok 0, FAIL exit 1. Author
after receipts, committed at `2e1c2a4` (`.ufo/waves/round-39/after/`): C1 at `49cc53c7` hidden 2/2, views 3/3,
fixtures 5/5, live 1, six 1, PASS exit 0, census selftest 117/117 (`selftest-49cc53c.txt`); C2 at `4078eb23` rules
8/8, duplicate_rows 0, duplicate_headings 0, source_ok 1, counts_ok 2, oracle_violations 0 over 60
`transaction started` lines in 86 `Running` windows, PASS exit 0. Wave: one v2 wave of 70 seats
(`.ufo/waves/round-39/w1-spec.json`, dispatch `394e1ba`; reports in `w1/`).

Final measured at `‹FINAL-REV›` after the wave and integration: C1 `hidden_matched` ‹C1-HIDDEN›/2, `views_matched`
‹C1-VIEWS›/3, `fixtures_matched` ‹C1-FIXTURES›/5, `live_match` ‹C1-LIVE›, `six_planes_all` ‹C1-SIX›, ‹C1-RESULT› exit
‹C1-EXIT›; C2 `rules_verified` ‹C2-RULES›/8, `duplicate_rows` ‹C2-DUPROWS›, `duplicate_headings` ‹C2-DUPHEADINGS›,
`source_ok` ‹C2-SOURCEOK›, `counts_ok` ‹C2-COUNTSOK›/2, `oracle_violations` ‹C2-ORACLE›, ‹C2-RESULT› exit ‹C2-EXIT›;
SOURCES 218 → ‹SOURCES-AFTER›, census exit ‹CENSUS-EXIT›; wave ‹SEATS-SETTLED›/70 settled, ‹SEATS-ERRORS› error rows.

Landed changes: `6a08925d` freeze (both counters, six libalpm snapshots, the transaction capture, registry rows);
`93fddb2c` declaration, before receipts and pre-seat controls; `49cc53c7` C1 arm and IN-109 re-pin; `4078eb23` C2
entry and S213–S218; `2e1c2a4` after receipts; `394e1ba` w1 spec and dispatch; `‹INTEGRATION-COMMIT›` integration
(SKILL, PROVINCE, README, QUALITY, lesson, wave evidence); this entry with the SCORECARD outcome. The declaration
predicted (`SCORECARD.md:2232-2234`) that the round-38 v1 counter's fixture F06 now reads `BLOCKED` and
`score-storage-arm-r38.py` fails ‹R38V1-FAILS›/10 by construction, the round-38 claim staying measured at
`b0005ae9`. Counter or knowledge defects found by the wave and not repaired in-round: ‹COUNTER-DEFECTS›.
~~~~

## Placeholder legend (fill at filing; nothing else in the block is a placeholder)

| Token | Value source |
|---|---|
| `‹FINAL-REV›` | the lane tip named in the SCORECARD "Round 39 — measured outcome" section, declared before the final after-run |
| `‹C1-HIDDEN›/‹C1-VIEWS›/‹C1-FIXTURES›/‹C1-LIVE›/‹C1-SIX›/‹C1-RESULT›/‹C1-EXIT›, `‹C2-*›` | the final `score-storage-hidden-r39.py` / `check-transaction-order-r39.py` receipts at `‹FINAL-REV›` |
| `‹SOURCES-AFTER›`, `‹CENSUS-EXIT›` | the round-end registry census (218 at the C2 commit) |
| `‹SEATS-SETTLED›`, `‹SEATS-ERRORS›` | `w1-results.json` once it exists (absent at draft time) |
| `‹INTEGRATION-COMMIT›` | the commit that lands SKILL/PROVINCE/README/QUALITY/lesson/wave evidence (working-tree only at draft time, finding 2) |
| `‹R38V1-FAILS›` | the observed `score-storage-arm-r38.py` count at a post-`49cc53c7` revision (declared prediction only; no receipt read at draft time) |
| `‹COUNTER-DEFECTS›` | wave-found counter/knowledge defects not repaired in-round; if the wave finds none, read `none` |

The heading stamp `2026-10-26T06:05:30Z` is my observed `date -u` at write, not a filing time: re-stamp it if the
entry is appended later (round-36 precedent, `LOG.md:1379`).

## Not done / out of scope

- I did not run either round-39 counter, the census, the selftest, or any gate: the values in the draft come from the
  committed receipts, the committed tool text and `git`/`grep` reads, and are attributed as such.
- I did not judge any TO row and do not judge C1/C2: the wave was still running (16 `w1/*.md` present, no
  `w1-results.json`, `C1ExecR38Counters/` empty), so no reviewer verdict existed to fold in.
- I did not fill the outcome numbers; findings 1–3 are routed for the L1/closure, not repaired by this seat.
- I did not create the seat receipt directory: every citation above is a committed lane path or a command whose output
  is quoted inline, so no copy needed to be preserved.
