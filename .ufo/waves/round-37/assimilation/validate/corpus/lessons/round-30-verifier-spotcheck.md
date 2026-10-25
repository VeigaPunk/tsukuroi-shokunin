author: hyaku closure (non-author integrator, @m_opus)

# tsukuroi round 30 — verifier spot-check (non-author)

Judged at lane tip `5bbd184185f77bba3e2f2eff1239348aa8ad0f18` (branch `master`, equal to `origin/master` by `git ls-remote origin refs/heads/master`), against base `fbfec6bdf8833e7513732a06000801a8ee9b690b`. Report `.ufo/reports/round-30/tsukuroi.md` (fleet commit `3610b2aa3b61f347c7e66d1ffa278d5029e9f3ed`). Dispatched prompt `.ufo/prompts/tsukuroi-round-30.md` (fleet commit `bdbd5db`).

Driver digest, copied from `.ufo/watchdog.log` (mutable; lines 765 and 772 when read):

    2026-10-22T17:56:55-03:00 launch tsukuroi round=30 pgid=4117763 driver=hyaku-inline attempt=1
    2026-10-22T19:16:41-03:00 complete tsukuroi round=30; hyaku-inline attempt=1

Method: I ran plain measurements over committed bytes (git, jq, grep, sha256sum). Five read-only seats ran in parallel: C1Remeasure, C1TrivialBaseline, C2Evidence, SpotcheckSources and GatesAndHarm. No lane tool, gate or counter was executed. Gate results below are evidence-verified from committed receipts. No jj command was run in the lane, and the keep-refs `refs/jj/keep/ee430cdf…` and `refs/jj/keep/a080e4efd961…` were not touched. Nothing was installed.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane identity | `git log --format='%an %ae %H %s' -- .ufo/reports/round-30/tsukuroi.md` | `tsukuroi-shokunin tsukuroi@shokunin.local 3610b2aa… round-30: tsukuroi report` | ok |
| `SHONEN` heading, one line per box | read report lines 130–135 | four `[~]` lines, each with a pointer | ok |
| Cited commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for `8fb2cef0`, `8976ca92`, `a3f19372`, `29bf87fa`, `7165f11e`, `85712671`, `b0cf50b9`, `32e5d848`, `a26057cf`, `5bbd1841` (and the round-29 cites `434a7903`, `d411c3d8`, `81a061a6`) | every hash exists and is an ancestor | ok |
| Pushed | `scripts/hyaku/jj-lane.sh state …/tsukuroi-shokunin` | `state branch=master local=5bbd1841… remote=5bbd1841… ahead=0 behind=0 head=detached tracked=0 untracked=3` | ok |
| Leftovers | `git -C …/tsukuroi-shokunin status --porcelain` | three `??` paths (below) | not round work |
| Prompt carries the template contract | `diff` of `kimi-shokunin/templates/round-prompt.md` (placeholders masked) against prompt lines 1–140 | only the 11 placeholder-substituted lines differ; sections 1–5 (mission/axes, claims, frontier step, L2 floor, report contract, commit/push scope, L0 channel) are verbatim; §6 is the hyaku addendum | ok |
| L2 route map | prompt §3 quotes no route table ("the route table, not this prompt, decides"); `MISSION.md` §L2 concurrency buckets | no quoted map, so nothing can mismatch | ok |
| Sources census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | 28 `W04` advisories (S155 and S158 are the round's two new ones), last line `tsukuroi ok …/corpus/SOURCES.md`, exit 0; rows 151 → 163 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at base and tip) | ok, matches report |

**The three uncommitted paths.** They are:

- `.ufo/waves/round-30/w1/CritCounterShapes/gitwork/G1-symlink-outside-tree/.ufo/waves/round-30/fixture/S900.txt`, a symlink to the absolute path `…/w1/CritCounterShapes/outside-snapshot.txt`;
- `…/G2-symlink-to-sibling/…/S900.txt`, a symlink to `real.txt`;
- `…/G3-dangling-symlink-whose-target-text-is-the-quote/…/S900.txt`, a dangling symlink whose link text is the fixture quote.

All three are wave-1 CritCounterShapes attack fixtures (`w1/CritCounterShapes.md:120-130`, shapes A21/A22 and G1–G3). They are not round content: committing them would plant the symlink attack itself in the tree. The report discloses them (report line 168). They are not uncommitted round work, but they are leftover debris (routed 4).

**Conformance defects (status-neutral).**
- `SCORECARD.md` at the tip carries `## Round 30 — declaration, attempt 1` twice: lines 1140–1153 and 1181–1194. The second copy is byte-identical to the first apart from a trailing blank line (`diff <(sed -n 1140,1154p) <(sed -n 1181,1194p)` → `15d14`). It was appended by `32e5d848`: the heading count is 1 at `b0cf50b9` and 2 at `32e5d848`.
- `corpus/QUALITY.md` 78 and 79 end "Lesson: `corpus/lessons/round-30.md` Mistakes R30-GIT-RESIDUAL-CHANNELS / R30-SOURCED-ROWS". Neither ID exists in the lesson (`git grep -n "GIT-RESIDUAL\|SOURCED-ROWS" 5bbd1841 -- corpus/lessons/round-30.md` → exit 1). The substance is in the lesson's C1 and C2 notes, so the pointers dangle but the lessons exist.
- The orchestrator's rule that a target must be able to fail on the quality it claims is not in the committed prompt bytes (`grep -n -i 'trivial\|able to fail\|baseline'` → only line 71, which is about mined-mistake fixes). Section 2 applies it as the orchestrator's dispatch contract, together with PROTOCOL §Gate standard ("A tool that cannot fail is a probe") and AXES ("Every claim carries its own falsifiable before→after"). This is noted for the orchestrator; it is not a lane defect.

## 2. Claims: re-check against `5bbd1841`

### C1 (depth): ten btrfs space rows D01–D10, counter `verified` 0 → 10

**Re-measured (plain, committed bytes).**
- `git show 5bbd1841:corpus/knowledge/btrfs-space-r30.json | jq '.rows|length'` → `10`, ids D01–D10. At the base the file is absent (`fatal: path … exists on disk, but not in 'fbfec6bd'`).
- For each row, `git show 5bbd1841:<snapshot> | sed -n '<line>p'` contains the row's `quote`: 10 of 10 ok.
- Cited sources: D01 S159, D02 S152, D03 S153, D04 S155, D05 S154, D06 S158, D07 S157, D08 S154, D09 S152, D10 S158. All are `A mined 2026-10-22` in `corpus/SOURCES.md` at the tip.
- `git show 5bbd1841:SKILL.md | grep -c '^| \[R30-D'` → `10`, one line per id (`SKILL.md:2606-2615`). At the base there are 0.

**Evidence-verified (counter receipts).**
- `git show 8fb2cef0:tools/check-btrfs-space-r30.py | sha256sum` → `1bf7ee14…`, the declared digest.
- Receipts: `measure/c1-before-8fb2cef0….jsonl` (revision `8fb2cef0`) reads 0 of 10, exit 1. `measure/after-a3f19372/c1-declared-v1.jsonl`, `measure/final/c1-declared-v1.jsonl` (revision `32e5d848`) and `measure/final-a26057cf/c1-declared-v1.jsonl` all read 10 of 10, exit 0.
- `git diff --stat a26057cf 5bbd1841 -- corpus/knowledge/btrfs-space-r30.json SKILL.md corpus/SOURCES.md tools/` is empty, so the last receipt holds at the tip.

The declared count reproduces: 10 of 10.

**Can the target fail on depth? No.** I verified the committed fixtures myself:
- Wave-1 CritClaimFraming fixture "self" (`w1/CritClaimFraming/fixture-self-btrfs-space-r30.json`, `out-self.txt`) scores 10 of 10 under the declared v1 (`1bf7ee14…`). It has no btrfs source: every row cites a made-up `S900` row, the "snapshot" is the counter's own source file, the quotes come from its `ROWS` comments, and the statements are filler words.
- Fixture "r26" (`out-r26.txt`) also scores 10 of 10 under v1.
- Wave-2 CritClaimFraming2 fixture "v2self" (`w2/CritClaimFraming2/out-v2self.txt`, `out-v2self-under-v1.txt`) scores 10 of 10 under both v2 (`4953203d…`) and v1.

Rules R1–R9 (`8fb2cef0:tools/check-btrfs-space-r30.py`, docstring) check JSON shape, a 12-word minimum, registry cells, the snapshot path and digest, the quote at its line, a token in the quote, any integer in the evidence directory, and one `SKILL.md` marker. None checks whether a row answers its question or is new to the lane. A trivial baseline therefore reaches the declared after-value. The 0 at the base is 0 by construction (no JSON file), not a measured absence of depth.

**What the round actually added.** For each row I grepped its core fact at the base (`git grep -n -i <token> fbfec6bd -- SKILL.md corpus/`):

| Row | Classification | Base evidence |
|---|---|---|
| D01 unallocated space and ENOSPC | new depth | `unallocated`, `free_chunk_space`: 0 hits |
| D02 global reserve | new depth | `global reserve`, `global_rsv`: 0 hits |
| D03 balance usage filters | new depth | `dusage`, `usage filter`: 0 hits |
| D04 metadata DUP | restates round 26 | `SOURCES.md:136` (S130), `SKILL.md:2367` row SH3 (dup metadata) |
| D05 block-group reclaim | thin new | `bg_reclaim_threshold` absent at base; one upstream sentence; the decision is "read only, no action" |
| D06 allocation sysfs directory | mostly restates round 26 | `SKILL.md:2367` names `allocation/{data,metadata,system}`; only the `global_rsv_*` attribute names are new |
| D07 snapshots keep extents allocated | new depth | snapshot/extent-sharing window: 0 hits |
| D08–D10 host values | captures (point in time) | literals absent at base; readings, not durable depth |

Real new depth: 4 firm rows (D01, D02, D03, D07), plus D05 thin and a small D06 delta. This matches the author's disclosure.

The `SKILL.md` section at 2600–2617 is actionable. It gives `Device unallocated` before `df`, a `balance start -dusage=0` ladder, and an error-patterns line, and it states the mori runway boundary.

**Ruling: C1 does not verify as a depth claim.** The counter output is reproduced, but the declared target cannot fail on the quality it claims: a sourceless fixture reaches it. By the author's own recount, 4 of the 10 counted rows are firm new depth. Narrowing to "4 firm rows" after landing is not admissible ("Never narrow a target after landing: a miss is an honest stop", prompt line 351).

C1 was not declared exploratory, so it cannot be admitted as `unprovable-but-better`. As an axis reading only, depth gained real sourced content that the declared measure cannot prove: `unprovable-but-better`.

### C2 (operability): eleven tools × three residual git channels, 17 of 30 (+1 harness error) → 0 of 33

**Evidence-verified (probe receipts).**
- `git show 8fb2cef0:tools/probe-git-env-residual-r30.py | sha256sum` → `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c`, the declared digest. `git diff --stat 8fb2cef0 5bbd1841 -- tools/probe-git-env-residual-r30.py` is empty.
- `measure/c2-before-8fb2cef0….jsonl`: pairs 30, leaking 17, `harness_errors` `[check-self-assessment.py]`, exit 2.
- `measure/after-a3f19372/c2-declared-probe.jsonl` and `measure/final/c2-declared-probe.jsonl` (revision `32e5d848`): pairs 33, leaking 0, `harness_errors` [], exit 0.
- `git diff --stat 32e5d848 5bbd1841 -- tools/` is empty.

**Re-measured (plain grep).** I counted the contract tokens (`GIT_CEILING_DIRECTORIES|GIT_CONFIG_NOSYSTEM|GIT_CONFIG_GLOBAL|XDG_CONFIG_HOME|core.hooksPath|/usr/bin/git|shutil.which|clean_env`) at base → tip in each of the 11 targets. Every target gains hits:

| Tool | Base → tip |
|---|---|
| check-adjacency-overlap | 1 → 4 |
| check-freshness-r17 | 1 → 7 |
| check-kernel-taint | 2 → 7 |
| check-memory-pressure | 2 → 7 |
| check-registry-coverage | 4 → 9 |
| check-storage-health | 2 → 8 |
| mutants-adjacency-overlap | 6 → 8 |
| mutants-kernel-taint | 7 → 9 |
| check-self-assessment | 1 → 4 |
| mutants-owed-statements-r29 | 0 → 3 |
| mutants-owed-statements-r29-landed | 1 → 3 |

The shared `tools/_revision.py` is unchanged.

**Declared versus honest before.** The declared before (17 of 30) is weaker than the honest before (at least 19 of 33). Three pairs were not evaluated because `check-self-assessment.py --selftest` exited 2 from an export (Mistake R30-UNSCREENED-TARGET). The two hidden pairs both leak (wave-1 CritClaimFraming finding 5), and CritProbeDesign counts at least 20.

This is a measurement defect, but it understates the delta and does not inflate it. Both values clear the declared fail floor (3), and the after-value is measured over all 33 pairs.

**Can the target fail?** Yes. The unmodified base tools leak on at least 17 pairs, and MutScrubChannels shows each fix is load-bearing per channel. The one exception is freshness-r17's HOME override, whose channel never leaked. Note that 10 of the 17 before-leaks are path-wrapper log hits with an unchanged exit code (hermeticity rather than outcome). The probe also does not compare stdout, so a hollow fix would score 0; the per-tool RevScrub* reviews, with byte-identical outputs, are the mitigation.

**Ruling: C2 verified.** Operability is `improved`.

### Owned-axis harm

`git diff fbfec6bd 5bbd1841 -- SCORECARD.md` is +56/−0: the declaration, the measured outcome, a round-30 axes table with identical ordinals, and the duplicate declaration copy. `git diff --numstat fbfec6bd 5bbd1841 | awk '$2>0'` lists only 12 `tools/*.py` files, all declared work (the C2 contract, counter v5, padding repair). `SKILL.md` (+74/−0), `corpus/SOURCES.md` (+12/−0), `corpus/QUALITY.md` (+6/−0) and `LOG.md` (+12/−0) are append-only, and `PROVINCE.md` is untouched. No pre-existing claim was removed or weakened.

One behaviour change goes beyond the env scrub: `check-self-assessment.py --selftest` now dispatches before the `.git` check. This is the named fix for the harness error.

### Gates (evidence-verified, never executed)

| Gate | Receipt | Revision | Committed result | Matches report |
|---|---|---|---|---|
| check-self-assessment | `measure/final-a26057cf/gate-self-assessment.jsonl`; base `w1/ExecGatesStart/self-assessment-live.jsonl` | `a26057cf`; base `8976ca92` (corpus bytes equal to base) | exit 0 PASS; base exit 1 FAIL, finding K10 | yes |
| check-registry-coverage | `final-a26057cf/gate-registry-coverage.jsonl` | `a26057cf` | exit 0, 43 of 43 | yes |
| check-recheck-commands | `final-a26057cf/gate-recheck-commands.jsonl` | `a26057cf` | exit 0, flagged 0 | yes |
| memory-pressure, storage-health, kernel-taint, adjacency-overlap, freshness-r17 | `final/gate-*.jsonl` | `32e5d848` | all exit 0 (freshness 48 of 48) | yes |
| owed-statements-r29 v5 | `final/gate-owed-statements-r29.jsonl` | `32e5d848` | exit 0, 12 of 12 ok | yes |
| probe-git-env-leak r29 | `final/r29-probe-git-env-leak.jsonl` | `32e5d848` | 0 of 8 | yes |
| census selftest | `final/gate-census-selftest.jsonl` | `32e5d848` | 97 passed, 0 failed | yes |
| report-receipts selftest | `final/gate-report-receipts-selftest.jsonl` | `32e5d848` | 2 of 2 | yes |

`git diff --stat 32e5d848 a26057cf -- tools/` is empty, so the `32e5d848` receipts stand for the tip's tools.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | `unprovable-but-better` | C1 does not verify as declared: its target is reachable by a sourceless fixture. Real additions are 4 firm sourced rows plus D05 thin; ordinal 8 → 8 |
| operability | `improved` | C2 verified: at least 17 (honest at least 19) → 0 of 33 |
| coverage | `unchanged` | `PROVINCE.md` and `corpus/README.md` untouched; ordinal 9 |
| freshness | `unchanged` | recheck gate PASS; no re-verification claim |
| calibration | `unchanged` | self-assessment FAIL → PASS is gate repair, not a claim; duplicate declaration and dangling QUALITY pointers are defects but not harm |
| adjacency | `unchanged` | mori runway boundary stated, nothing absorbed; adjacency gate OV1–OV6 empty |

**Admission: not admitted** (`rejected-honest-stop`). C1 does not verify, and no axis is harmed.

## 3. Discernment spot-check (LEARNING.md)

Sampled from `corpus/lessons/round-30.md` `## Gate`. Each source was re-opened live with curl on 2026-10-22 by seat SpotcheckSources, and the result was checked against the committed snapshots.

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S160 btrfs wiki FAQ (archived) | reject (tier C) | `https://archive.kernel.org/oldwiki/btrfs.wiki.kernel.org/index.php/FAQ.html`, HTTP 200, sha256 `961d9b6b…25cc` equals the recorded value and the snapshot | agree | Line 43 banner reads "OBSOLETE CONTENT"; the quote at line 536 is verbatim; line 892 dates the revision 1 June 2022; the live host 301s to the archive. Self-declared obsolete and unpinned. `-dlimit` has 0 hits in the tier-A S153 balance doc, which grounds the round's usage-filter decisions |
| S161 ArchWiki Btrfs | reject (tier B, redundant) | `https://wiki.archlinux.org/title/Btrfs`, HTTP 200, sha256 `73558a5c…5523` equals the recorded value and the snapshot (the `?oldid=887521` render was bot-gated) | agree | The quote at line 1846 is verbatim (21 words). Its `df` point is already carried by tier-A S152 (lines 22–23, 367–368). The frozen tokens `unallocated`, `Global reserve` and `permanently unusable` have 0 hits on the page |
| S156 Linux v7.2 `fs/btrfs/block-rsv.c` | admit (A, mined) | `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/block-rsv.c`, sha256 `3a135842…9121` equals the recorded value; 627 lines | agree | Line 332 reads "so the global reserve is never consumed. Mark it as full and skip" (13 words); `btrfs_update_global_block_rsv` is at 322–413. Primary source at the running kernel's tag |
| S157 btrfs-progs v7.1 `ch-subvolume-intro.rst` | admit (A, mined) | `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-subvolume-intro.rst`, sha256 `6dbdd94d…1e68` equals the recorded value | agree | The quote at line 40 is verbatim (12 words) and continues on line 41; grounds D07 |

**`SOURCES.md` row re-opened: S156** (also S152). The registry schema has no verbatim-quote column: `teaches` is a paraphrase of 78 and 86 words. The row's anchor names the snapshot, sha256 `3a135842…` (matching the live bytes) and line ranges 322–413 that contain the Gate quote. The located quote of 25 words or fewer lives in the Gate row: S156 is 13 words at line 332 and S152 is 9 words at line 398, both verbatim in the re-opened sources. This is not a defect under the committed schema.

**Census:** the command in section 1 gives exit 0, last line `tsukuroi ok …/corpus/SOURCES.md`.

The spot-check agrees with the gate on both rejects and both admits.

## 4. Trend verdicts

- **expansion: `unprovable-but-better`.** A new knowledge entry on btrfs space mechanism cites mined tier-A rows (S152–S159), and four of its rows are absent from the base corpus. But the entry cites no coverage-map row, `PROVINCE.md` and `corpus/README.md` are untouched, and D04 and D06 sit on round-26 ground (`storage-health-r26.md`, `SKILL.md:2367`). LEARNING's `improved` condition ("each citing its coverage-map row") is not met.
- **quality: `improved`.** Stronger tools replace weaker ones: eleven tools are closed to three git channels (C2 verified), the owed-statements counter v5 refuses the 11 v4 shapes with 0 of 19 controls refused, and padding shapes are refused 53 of 53. Round-29 routed defects 1, 2, 3 and 6 are closed with receipts. No admitted entry failed its re-check: 10 of 10 quotes are at their cited lines, and every sampled source agrees.
- **discernment: `unchanged`.** In favour, the outside spot-check agrees on 2 rejects and 2 admits, and the round's overclaims were corrected before closure. Against, the declared C1 measure cannot fail on depth. That was disclosed but not mined into a grounded `QUALITY.md` criterion; QUALITY 79 instead defines a depth row by format and provenance alone. The declaration's novelty sentence was false (R30-DECLARATION-OVERCLAIM), and the C2 targets were unscreened.

## 5. Routed defects (lane fixes next round)

1. **Able-to-fail depth target.** Before declaring a depth counter, show that a trivial or sourceless fixture scores below the target, with a committed receipt, and that the base scores below it by measurement rather than by construction. Amend QUALITY 79 (or add a criterion) so that a depth row must also answer its frozen question with a fact absent from the base corpus (a base `git grep` sweep recorded per row). Ground the criterion in a Mistakes row for this round's C1.
2. **Duplicate declaration.** `SCORECARD.md:1181-1194` repeats the round-30 declaration (appended by `32e5d848`). Append an erratum naming the duplicate; do not rewrite it in place.
3. **Dangling lesson pointers.** QUALITY 78 and 79 cite Mistakes `R30-GIT-RESIDUAL-CHANNELS` and `R30-SOURCED-ROWS`, which are absent from `corpus/lessons/round-30.md`. Point them at existing rows, or add the rows in the next lesson.
4. **Leftover attack fixtures.** Remove the three untracked symlinks under `.ufo/waves/round-30/w1/CritCounterShapes/gitwork/G1–G3`, or record them as intentionally untracked through an ignore rule. Also drop the committed `w1/CritCounterShapes/__pycache__/shapes.cpython-314.pyc`.
5. **C2 probe gaps** (owed by the lane):
   - stdout comparison (hollow fixes score 0);
   - `LD_PRELOAD`/`PYTHONPATH`;
   - a dropped `.git` pointer;
   - repository-local `include`/`core.fsmonitor`;
   - the system-config channel (the control sets `GIT_CONFIG_NOSYSTEM=1`);
   - the low-power enclosing-repo channel for both owed-statement batteries.
   Screen every target from an export before declaring (R30-UNSCREENED-TARGET).
6. **Carried owed items.** Counter v2 still accepts 33 shapes and refuses 9 legitimate layouts. `check-report-receipts.py` over-reports legacy receipts. The S155/S130 and S158/S133 duplicate authorities (W04) need merging. `run-receipt.py` has LOW findings.

## 6. SHONEN

All four boxes stay `[~]`, with author evidence plus wave-2 lane seats (still the lane). None is fully checkable by a non-author from this round's evidence, so promotion is not suggested.
