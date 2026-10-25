# Round 25 — verifier spot-check (tsukuroi, non-author)

author: hyaku closure (non-author integrator, @m_opus)

Closure agent HyakuCloseTsukuroi25, a fresh `task` dispatched by the hyaku orchestrator; exposed runtime model `anthropic/claude-opus-5-5`. One read-only reviewer seat (HyakuCloseTsukuroi25.C2RowTruth, self-reported model `zai/glm-5.3-flash`) re-opened the C2 primary sources; every other check below was run by this closure. Installs: none. Date 2026-10-22.

Judged revisions: base `b9046016831237cd04d38da11ba76e50d5380c53`, head `157ee2556a75bf4d1ae4893d4a06c020ae531ac0` (measured production revision `d70af4aaba890320fe2326509ffad13f2018172e`; `git diff --stat d70af4aa 157ee255` touches only `.ufo/waves/round-25/measure/final2/` receipts and two `LOG.md` lines, so no measured input differs between them).

Driver digest (copied from `.ufo/watchdog.log`):

- `2026-10-22T06:59:30-03:00 launch tsukuroi round=25 pgid=2526458 driver=hyaku-inline attempt=1`
- `2026-10-22T09:14:48-03:00 complete tsukuroi round=25; hyaku-inline attempt=1`

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane | `git log --format='%an %H' -- .ufo/reports/round-25/tsukuroi.md` (fleet root) | `tsukuroi-shokunin f61aaaf65a9e17afd25e50b92505af6c9fc0d518` | conformant |
| SHONEN heading, one line per box | report lines 55-60; `git show 157ee255:SHONEN.md \| grep -c '^- \['` | 4 `[~]` lines for 4 boxes | conformant |
| Cited hashes exist and are ancestors | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for `6c580b15`, `0cd9b28b`, `5e7c04ec`, `c93bd70f`, `d70af4aa`, `157ee255`, base `b9046016` | all `commit`, all ancestors | conformant |
| Pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain` | `branch=master local=remote=157ee255… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | conformant |
| Prompt carries the template contract | `.ufo/prompts/tsukuroi-round-25.md` (350 lines, committed `853e671b`) | MISSION/AXES binding (l.5), 1–3 claims (l.11), frontier step (§2b), L2 floor (§3), report path, SHONEN, commit-hash and landed-changes items (l.101-118), commit/push scope and L0 channel (§5), write scope (l.251), Claim sizing (l.342) | conformant |
| Lane commits by lane identity | `git log --format='%an <%ae> \| %cn' b9046016..157ee255` | 6 commits, all `tsukuroi-shokunin <tsukuroi@shokunin.local>` | conformant |

Marker test: real report with six checkable lane commits, so status `ok`.

### VCS incident — seat push into the lane's local `master` (conformance defect)

Observed with read-only git: `git reflog show master` lists `master@{8..5}` = `push` of `d2e9a7a`, `9e9a97d`, `d70cbd0`, `d5e6481` (authors `t <t@x>` and `r20 <r20@example.invalid>`), then `master@{4}` = `0cd9b28 round-25 L1: undo seat push of 4 scratch commits (DraftSkillTable)`, then jj exports `5e7c04e` … `157ee25`. `git merge-base --is-ancestor d5e64812 master` exits 1; `git branch -a --contains d5e64812` prints nothing; `git ls-remote origin refs/heads/master` = `157ee2556a75…`; `git fsck --connectivity-only` exits 0 (three dangling trees only). The four commits never reached a helper commit or the remote.

Classification: **conformance defect, status-neutral.** A wave-1 seat wrote a ref in the lane repo outside `jj-lane.sh`, which the boundary forbids; the L1's `git update-ref` repair was itself a git write outside the helper, but a correct compare-and-swap reset before any jj import, disclosed (lesson Mistakes R25-SEAT-PUSH) and bound by new QUALITY 59. No integrity failure remains.

### Round-24 stray-seat leftovers (verified as reported)

`git diff --quiet b9046016 157ee255 -- .ufo/waves/round-24` exits 0 and `git diff --quiet 157ee255 -- <path>` exits 0 for the three restored files (`ExecPauseGateChecker/check-pause-gate.py`, `RevGateSchema.md`, `ScribeGateEntry/pause-lift-gate-r24.json`): restored to the committed bytes. The two untracked files (`ScribeGateEntry/p2-measured-probe.txt`, `zero-probes-measured.txt`) are absent from disk; their recorded sha256 values cannot be re-derived because the bytes are gone (no copy under `/fast/scratch/hyaku/`). Three restored, two deleted: agree.

## Per-claim re-check

### C1 — calibration: self-assessment mismatches 13 of 23 → 0 of 23

Re-measured by plain git/regex over committed bytes (not by the lane's tool):

| Check | Base `b9046016` (round-11 table stated → observed) | Head `157ee255` (round-25 table stated = observed) | How observed |
|---|---|---|---|
| K07 notes | 24 → 46 | 47 | `git ls-tree -r --name-only <rev>` matching `corpus/knowledge/[^/]+\.md` |
| K08 `SKILL.md` lines | 1631 → 2301 | 2355 | newline count of `git show <rev>:SKILL.md` |
| K09 table lines | 55 → 259 | 297 | lines starting `\|` |
| K10 lesson files | 0 → 25 | 26 | ls-tree under `corpus/lessons/` |
| K11 README lines | 20 → 231 | 231 | newline count |
| K12 PROVINCE sections | absent → present | present | `## Core` :6, `## Adjacent` :35, `## Frontier` :75 |
| K14 `--identity` | absent → absent (match) | absent | 0 occurrences in `tools/tsukuroi-census.sh` |
| K15 overlap table | absent → present | present | `\| ID \| Finding` at `PROVINCE.md:44` |
| K16-K19, K20-K23 paths | 2 path mismatches (K17, K21) | 0 | `git cat-file -e 157ee255:<path>` for all 12 cited paths: all exist |
| K13 census cases | 80 → 97 | 97 | evidence-verified, not executed (Gate standard): `w1/ExecHermeticSelftests/census-selftest-0cd9b28.out` prints `PASS (97 cases, 97 passed, 0 failed)`; `tools/tsukuroi-census.sh` unchanged base→head |
| K01-K06 ordinals | coverage 8→9, freshness 8→9, adjacency 7→8 mismatch | all match | the declared regex over SCORECARD lines outside the current table |

Committed receipts agree: `.ufo/waves/round-25/measure/c1-b9046016.json` `mismatches` 13, `final2/c1-d70af4aa.json` 0; exits 1 and 0.

Rulings asked of this closure:

- **Valid calibration claim: yes.** It counts mismatches between the lane's self-assessment (SCORECARD axes and Capabilities tables, SHONEN.md) and repository state at a named revision, with the 23 checks and the path grammar fixed at `0cd9b28` before any round-25 measurement. That is the form the session Claim sizing rule prescribes.
- **Self-reference in K01-K06.** At head, K01, K04 and K05 resolve to this round's declaration text (SCORECARD lines 793, 807, 792; K04 to the refinement example `freshness (actual 9 → 9`). Restricting the same regex to the 782 lines that existed at the base gives the same values (depth 8 at :759, freshness 9 at :772, calibration 9 at :771; coverage 9 :224, operability 9 :621, adjacency 8 :620), so the zero does not depend on the self-referential lines. The weakness is real for future rounds (the check can be satisfied by the round's own prose) and is routed below.
- **SHONEN rewording: neither a narrowing nor a gamed after-value that carries the claim.** The target (0 of 23), the check set and the grammar were not changed; the rewording landed in `5e7c04ec`, after they were frozen. `observation/request` → `observation and request` keeps the meaning (`corpus/knowledge/adjacency-handoffs-fleet-r1.md` §3 is an observation packet plus a request). It removes one checker false positive (K21), so it adds no calibration value. It is disclosed in the lesson. Excluding K21, the base holds 12 genuinely mismatching checks (K17 also carried the real 80-vs-97 count), and the claim stands at 12 → 0. On the 17 repository-state checks alone (K07-K23, K21 excluded) it is 9 → 0.

Verdict: **verified, re-measured.** Calibration: **improved** (ordinal unchanged at 9 as declared).

### C2 — depth: memory-pressure entry, verified rows 0 → 6 of 6

Re-measured by plain parsing of committed bytes, independent of `tools/check-memory-pressure.py`: for each row in `corpus/knowledge/memory-pressure-r25.json` I checked a non-empty statement, verdict and action; a source that is `mined`, opened 2026-10-22, with `used-by` naming the entry (`corpus/SOURCES.md` at head); a ≤25-word quote for that source in the lesson `## Gate`; a capture pointer whose line is unique in `capture/capture.txt` (sha256 `e60f1bbc…447136`, matches the declaration), not a header, echo or exit line, and contains its token; and a `SKILL.md` table line appended this round naming the id (`SKILL.md` at head is base bytes plus an append). Result: MP1 to MP6 all count, 6 distinct ids, each with a tier-A source, and each id in the first cell of a round-25 SKILL row. That is 6 of 6 under the declared rule and under the stricter variants wave 2 proposed. Base: `git cat-file -e b9046016:corpus/knowledge/memory-pressure-r25.json` fails (entry and capture absent), so 0. Receipts agree: `measure/c2-b9046016.json` exit 2 CAPTURE-MISSING, `final2/c2-d70af4aa.json` exit 0, 6 rows.

What the count proves: evidence-link completeness, which is what the declaration counted. It does not prove the rows are true; MutC2Rules killed 8 of 17 mutants. Truth was therefore reviewed row by row from re-opened primary sources (seat C2RowTruth; S120, S121 and S123 also re-opened by this closure):

- MP1 holds (psi.rst:45-49; oomd reads `full avg10`, oomd.conf.xml:95-96). MP2 holds (psi.rst:62-63, psi.c:409-411). MP3 holds as corrected (psi.h:39; the withdrawn "parent total is not the sum" sentence is correctly marked). MP4 holds as corrected (systemd.resource-control.xml:1531, 1545-1548; the `OOMRules=` exception at :1633-1644 is marked in the appended correction). MP5 holds (oomd.conf.xml:172 "Defaults to 90%.", :190 "Defaults to 60%.", :202 "Defaults to 30 seconds when unset or 0."; 5 percent floor, oomd-manager.h:30). MP6 holds as corrected (oom_kill.c:935-936; cgroup-v2.rst:1506-1508).
- Unmarked false statements in the entry or its SKILL section: none found. Residuals, not harms: the MP6 pointer table keeps the pre-correction reason for capture line 50 (the correction governs), and the S119 anchor says line 942 where `do_send_sig_info` is at 943.
- New knowledge versus mori `system-pressure-r24.md` (`4f05dd5a`, 0 oomd mentions): MP4 and MP5 are new, and so are the oomd consequences carried in MP1 to MP3. The generic PSI facts restate mori's ground and cite it. This agrees with the L1's "MP4 and part of MP5" as a lower bound.

Verdict: **verified, re-measured; substance reviewed.** Depth: **improved** (ordinal unchanged at 8 as declared).

### No owned axis harmed

`git diff b9046016 157ee255 -- SCORECARD.md`: appended sections only, plus one in-place line (below). The current axes table holds the same ordinals as the pre-round move records (depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8); no score fell and no capability row was removed. Refuted-claim sweep: `git grep -n -i -E 'would likely have acted|oomd[^|]{0,60}before the kernel|ManagedOOM… already set' 157ee255 -- corpus SKILL.md PROVINCE.md` hits only `oom-event-plane.md:344` and `kill-event-deep-r8.md:255`, now carrying the R25 notices at `oom-event-plane.md:471-475` and `kill-event-deep-r8.md:379-381`, plus the new entry's own supersession text. Per-axis: calibration improved; depth improved; coverage, operability, freshness, adjacency unchanged. Freshness duty met: the LOG re-verification line cites ExecRecapture.

## Discernment spot-check

| Item | Gate decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S121 systemd v262 `systemd.resource-control.xml` | admit (tier A, mined) | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml fetched 2026-10-22; sha256 `d57641df…0587d8` = row anchor; line 1531 "the unit becomes a candidate for monitoring by", lines 1545-1546 "will not actively use this cgroup's data for monitoring and detection." | agree | A version-matched primary source, and the quotes sit at the stated lines. The row's teaches cell ("only kill") is too broad (`OOMRules=`, ancestor `kill`). The lane recorded that, and the entry's correction carries it. |
| S123 systemd v262 `src/oom/oomd-manager.c` | admit (tier A, mined) | https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.c line 124 `if (message.mode == MANAGED_OOM_AUTO) {` followed by removal from the monitor hashmap | agree | The code confirms that `auto` unsubscribes from monitoring. Quote and line exact. |
| Arch rendered `oomd.conf.5` (and siblings) | reject (opened, not registered) | https://man.archlinux.org/man/oomd.conf.5.en fetched 2026-10-22: footer `systemd 262.1`; host `pacman -Q systemd` = `262-1`; the three default sentences are identical to the v262 XML | agree | The upstream v262 XML is the version-matched authority, and the render adds nothing the registered row lacks. The flip condition is sound. |
| New row S126 (supersedes S120) | admit (correction row) | same oomd.conf.xml URL: fetched bytes hash `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617` = S126; S120's anchor has `…5632d4a6…` | agree | The append-only correction is right, and the S120 transposition is real. Cost: W04 21 → 22, disclosed. |
| New row S127 (supersedes S125) | admit (tier B, boundary only) | `mori-shokunin` `4f05dd5a:corpus/knowledge/system-pressure-r24.md`: blob `d4ccce4262d8…` and sha256 `5d3a322a…c019ce5` both reproduce; Scope quote "This note records what those files are, exactly which shapes the kernel emits" located (it wraps across a line) | agree on content | The row is accurate and correctly tier B. Defect: the lesson `## Gate` has no record of S127, with no URL/path, access date or quote (`grep -c S127 corpus/lessons/round-25.md` = 0). CORPUS SOURCES rule 1 requires one for every new row. Routed. |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → `tsukuroi ok`, exit 0, 22 W04 warnings (the added one is S126). Rows 114 → 127 by the frozen count.

## Trend verdicts

- **expansion: unchanged.** The new entry sits on held coverage-map ground: the OOM and memory plane is already covered by `oom-event-plane.md` and `kill-event-deep-r8.md`. No new coverage row, frontier area or capability.
- **quality: improved.** A sourced entry supersedes the refuted current-use claim at `oom-event-plane.md:344` and `kill-event-deep-r8.md:255`. Both are marked. MP4's basis was re-opened here (S121:1545-1546; S123:124). No admitted entry failed its re-check (C2RowTruth: no unmarked false statement). The stale round-11 self-assessment was superseded by a measured table.
- **discernment: improved.** This outside spot-check agrees with the gate on two admits (S121, S123), one reject (the Arch rendered pages) and both new correction rows. QUALITY 57-59 each cite a lesson (R25-STALE-AXES-TABLE, round-24 spot-check line 69 plus lesson Routed defects, R25-SEAT-PUSH). No criterion was added without a lesson.

## Routed defects (the lane fixes these next round; all status-neutral)

1. Undisclosed in-place edit of the round-11 historical axes row: `c93bd70f` changed `SCORECARD.md:51` from "loop with its mismeasure rows" to "loop for rounds 1 to 9". The lesson section "Record of the one in-place edit" names only SHONEN box 2, so that record is false. Append a correction that quotes the original wording and names both edits.
2. S127 (and S126) lack their own lesson `## Gate` record (URL or path, access date, ≤25-word quote with location). Append one.
3. The C1 ordinal checks can be satisfied by the round's own declaration prose (K01, K04, K05 at head). Exclude the declaring round's lines, or bind to dated move records. Separately, the current table's live counts drift with every commit: this spot-check's own commit makes K10 read 27 files against the stated 26. Pin the counts to the measured revision, or re-measure each round.
4. Harden the C2 checker as the lane planned. Wave 2 found 9 surviving mutants. At `c93bd70f` the checker crashed on lesson prose, and the lesson text was reworded rather than the tool fixed.
5. The seat push (R25-SEAT-PUSH) and seat wake-writes (R25-SEAT-WAKE-WRITES): show the QUALITY 59 bound (clones without a lane push path, `ahead=0` before each helper commit) and a no-seat-messaging rule in round-26 contexts.
6. R25-LATE-CANONICAL-LOAD recurs for the third time (rounds 21, 24, 25): record canonical sha256 values in the declaration commit before any wave.
7. SHONEN boxes 3 and 4 cite superseded or untested notes (RevShonen). All four boxes stay `[~]`, and none is yet checkable by a non-author for promotion.
8. The S121/S122 teaches cells overstate "only kill" and S118's omits the hierarchy. Correct them with superseding rows or logged in-place notes.
