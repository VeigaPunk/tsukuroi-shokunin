# Scout: misroot sweep after integration (round 25, wave 2)

Verdict: holds. The fleet root gained exactly two porcelain paths since the L1 baseline, and neither names tsukuroi round 25; the lane has zero untracked or modified files outside `.ufo/waves/round-25/`, and its HEAD is the measured revision `5e7c04ec`.

Capture times. Fleet and lane porcelain were taken at 2026-10-22 08:47:54 -0300, after the wave-1 seat wrote its own capture at 07:27:45 and after the L1 committed and pushed `5e7c04ec`. The fleet baseline file `/fast/scratch/hyaku/tsukuroi-r25/fleet-porcelain-before.txt` is dated 2026-10-22 07:09:46 -0300, 613 bytes, 17 lines.

## 1. Fleet porcelain delta: two lines added, none removed

[obs] `diff -u /fast/scratch/hyaku/tsukuroi-r25/fleet-porcelain-before.txt <git -C /home/vgpnk/Projects/shokunin status --porcelain>` exits 1 with exactly two added lines and no deletions:

```
+ M .ufo/state/mado.report-baseline
+?? .ufo/waves/round-49/
```

[obs] Re-running with `--untracked-files=all` yields the same delta at file granularity, so the `??` line is not hiding a collapsed subtree:

```
+ M .ufo/state/mado.report-baseline
+?? .ufo/waves/round-49/falsify/RowGameDev2d.md
```

[obs] No baseline line disappeared or changed status. The fleet HEAD moved during the sweep from `f1a75c9` (wave 1) to `c301de3` ("round-26: hyaku closure dispatch for tameshi", 2026-10-22T08:50:06-03:00); that commit touched no path relevant to this round.

## 2. `/home/vgpnk/Projects/shokunin/.ufo/state/mado.report-baseline` — no tsukuroi round-25 content, mado round 23

[obs] Working content is the single line `23 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; at fleet HEAD the same file is `22 e3b0c44…`. Working sha256 is `330bcaf9ab26161f387744a9124f83ed05fcb5fd683e83a6890ff707e570d1ee`; mtime 2026-10-22 07:43:09 -0300.

[obs] The round-25 token test used by wave 1 (`grep -a -i -c -E 'tsukuroi|round[ -]?25|r25'`, where exit 1 means no match) returns match count 0, exit 1. The file holds only a round number and a digest.

[obs] The digest is sha256 of the empty string: `printf '' | sha256sum` prints `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Per `/home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh:31`, this state file "holds \"round SHA256\" for the report bytes".

[obs] `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` records `2026-10-22T07:43:10-03:00 launch mado round=23 pgid=555711 driver=hyaku-inline attempt=1`, one second after the state file mtime. `/home/vgpnk/Projects/shokunin/mado-shokunin` is at `4de4464` with its own `round-23` wave files untracked and `PROVINCE.md` plus `corpus/SOURCES.md` modified.

[inf] The change is mado's own round-23 launch baseline (22 to 23, empty report digest), written by the fleet watchdog before launch. It is not a tsukuroi write and carries no tsukuroi or round-25 token.

## 3. `/home/vgpnk/Projects/shokunin/.ufo/waves/round-49/falsify/RowGameDev2d.md` — no tsukuroi round-25 content, kotoba round 49

[obs] The untracked tree holds exactly one file: `.ufo/waves/round-49/falsify/RowGameDev2d.md`, 13630 bytes, sha256 `37aaa836a5d650b658484cf99d3722acff55cd569a7410a36c588d60aaedce99`, mtime 2026-10-22 08:38:25 -0300; the directory was created 08:37:50.

[obs] `grep -a -i -c -E 'tsukuroi|round[ -]?25|r25'` on it returns 0, exit 1. The same test against the fleet dispatcher prompt (below) returns matches, so the pattern is live and the file is genuinely free of tsukuroi and round-25 tokens.

[obs] Its opening lines name another lane and round: "seat RowGameDev2d", "kotoba master c48793dbe5eb30cd661f42ecad7399ae94e3d7ad", and the row `game-dev-2d` of `corpus/knowledge/sibling-overlap-census-round49.md`. The file also cites `.ufo/waves/round-49/build/*.md` as its own lane's build artifacts.

[obs] `.ufo/watchdog.log` has `2026-10-22T06:30:28-03:00 launch kotoba round=49 …` and `2026-10-22T08:48:49-03:00 complete kotoba round=49 …`.

[inf] This is a kotoba round-49 falsification report written into the fleet tree, not a tsukuroi round-25 product.

## 4. The wave-1 seat's "zero plain untracked entries" is now superseded, not false

[obs] The wave-1 report `.ufo/waves/round-25/w1/ScoutMisrootBaseline.md:3` states "there are zero plain `??` untracked entries", and section 1 shows the porcelain identical to the baseline. Its own snapshots `/fast/scratch/hyaku/tsukuroi-r25/ScoutMisrootBaseline_porcelain-now.txt` and `…-after.txt` are 613 bytes, 17 lines, mtime 07:20:08 and 07:27:45, and are byte-identical to the baseline.

[inf] That statement was true when captured at 07:27:45. The two new entries postdate it: the mado baseline changed at 07:43:09 and the kotoba round-49 file appeared at 08:37:50 to 08:38:25. Anyone quoting the wave-1 sentence now must date it; the correct current statement is "two plain/untracked delta entries, neither tsukuroi round 25".

## 5. Fleet-root paths that do name tsukuroi round 25 are sanctioned dispatch artifacts, not new

[obs] `/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-25.md` exists (26259 bytes, mtime 06:59:28), is tracked at fleet HEAD as blob `669bbec548658b6b323533313458bb95b03f34af`, and the worktree blob equals the HEAD blob. It is not in the porcelain delta.

[obs] Its first line reads "You are the tsukuroi L1, round 25. Working dir: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin." It is the dispatcher's input, committed as `853e671 round-25: tsukuroi dispatch evidence (hyaku inline attempt 1)`.

[obs] `/home/vgpnk/Projects/shokunin/.ufo/state/tsukuroi.report-baseline` reads `25 e3b0c44…` in the worktree and `22 e3b0c44…` at fleet HEAD, mtime 06:59:28. It is already ` M` in the baseline file, so it did not change during wave 1 or 2, and its round number 25 matches `06:59:30 … launch tsukuroi round=25` in `.ufo/watchdog.log`.

[obs] The sanctioned fleet report path from the prompt (`Write the round report at /home/vgpnk/Projects/shokunin/.ufo/reports/round-25/tsukuroi.md`, prompt line 101) does not exist yet; `.ufo/reports/round-25/` holds nine sibling lane reports and no `tsukuroi.md`.

[inf] So the fleet root names tsukuroi round 25 only in the three sanctioned places (prompt, launch baseline, and the not-yet-written report). None of them is a misroot, and none appeared in the delta.

## 6. Empty directories escape `git status`, including one named round-25 at the fleet root

[obs] `/home/vgpnk/Projects/shokunin/.ufo/waves/round-25/` exists at the fleet root but has no porcelain line because its only content is an empty directory `build/` (0 bytes, mtime 2026-10-21T04:32:22). Its parent directory mtime is 2026-10-22T07:55:34, after the baseline capture.

[obs] `/home/vgpnk/Projects/shokunin/.ufo/waves/round-29/` is likewise empty and invisible to git status; it was created 08:30 today. `git log -- .ufo/waves/round-25` prints nothing, so this fleet-root round-25 directory was never tracked.

[obs] `grep -rn -i tsukuroi .ufo/waves/round-25` finds no file and therefore no match. `git check-ignore -v` exits 1 for both directories, so they are not ignored; they are simply empty.

[inf] These are fleet-round namespace directories for other lanes' rounds (the fleet log shows `kama round=25` and `tameshi round=25` launches and completions), not this lane's round-25 tree, which lives inside `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/`.

[unk] What changed the fleet `.ufo/waves/round-25/` parent mtime at 07:55:34 cannot be recovered from the current tree: no file remains under it and nothing in the fleet log names a path. A child created and removed there would leave exactly this trace. No content survives, so it cannot name tsukuroi round 25 now, but the transient cannot be ruled out from filesystem state.

## 7. Lane: zero files outside `.ufo/waves/round-25/` are untracked or modified

[obs] `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain` exits 0 with 30 lines: 15 ` M` and 15 `??`. Filtering with `grep -vE '^.{3}\.ufo/waves/round-25/'` exits 1 and prints nothing, so every entry is inside that tree. The same filter over `--untracked-files=all` also prints nothing.

[obs] `git rev-parse HEAD` prints `5e7c04ecb02735491456de2b8bc44550d0db4609`, equal to the measured revision, and `git merge-base --is-ancestor` confirms the relationship. `git status --porcelain -- tools/` and `git status --porcelain -- corpus/ SKILL.md SHONEN.md PROVINCE.md SCORECARD.md README.md` both print nothing, so all judged surfaces equal the pushed revision.

[obs] The committed fix is present at the measured revision: `git show 5e7c04ec:SCORECARD.md | grep -n` finds `## Axes — current self-assessment (round 25)` at line 815 and `## Capabilities — current (round 25)` at line 840.

[obs] Untracked paths include the seven `measure/` receipts, `w2-spec.json`, `w2-dispatch.json`, `w2-dispatch-result.txt`, the wave-1 `DraftRoutedRepairs.md` and `SrcMoriSibling.md`, and the `w2/` seat outputs. They are inside round-25, so they fall outside the asked class, but they are not in the pushed revision.

[inf] A later verifier working only from `5e7c04ec` gets the SCORECARD and SHONEN bytes but not the `measure/` receipts, because those were never committed. That is a provenance gap for the L1 to close, not a misroot.

## 8. Lane ignored paths outside round-25 are all older than this round

[obs] `git status --porcelain --ignored=matching --untracked-files=all` lists `.jj/.gitignore` and `.jj/repo/`, `.jj/working_copy/`, `.ufo/interactive-sessions/`, and `.ufo/waves/round-24/w1/ExecPauseGateChecker/__pycache__/` outside round-25. Mtimes are 2026-10-20 for `.jj`, 2026-10-15 for `.ufo/interactive-sessions`, and 2026-10-22 06:50:13 for the round-24 `.pyc` (61766 bytes).

[obs] The round-24 bytecode mtime 06:50:13 precedes the `06:59:30 … launch tsukuroi round=25` line in the fleet watchdog log, so it is round-24 closeout work, not a round-25 artifact.

## 9. Wave-2 rewrites of tracked wave-1 files (inside round-25, flagged for the L1)

[obs] 15 tracked files under `.ufo/waves/round-25/w1/` are modified in the working tree, `git diff --stat` totals 15 files, +961 −277, with mtimes from 08:37:32 to 08:48:39. The set includes `ExecMemPressureTool/check-memory-pressure.py`, `ExecMemPressureTool/selftest.json`, all five `MutMemPressurePlan/fixtures/` scripts and `sweep-result.json`, and four wave-1 markdown reports.

[obs] Neither counting tool is in that set: `tools/check-self-assessment.py` and `tools/check-memory-pressure.py` are unmodified at HEAD. The measured values therefore still come from committed bytes.

[inf] The working tree no longer equals `5e7c04ec`, and wave-1 evidence copies are being rewritten during wave 2. Whether those writes belong to wave-2 seats or to the L1 is outside this seat's question, but the L1 should rule on it before quoting any wave-1 fixture from the working tree instead of from the revision.

## 10. Method notes and residual unknowns

[obs] All fleet and lane queries were read-only git subcommands (`status`, `rev-parse`, `merge-base`, `show`, `ls-files`, `hash-object`, `log`, `diff`, `check-ignore`) plus `find`, `stat`, `grep`, `sha256sum` and `diff`. No git write command ran against the fleet root or the lane, no jj command ran at all, and nothing was moved or deleted.

[obs] The mado baseline round number is explained by the watchdog log, but the fleet-root `.ufo/waves/round-25/` mtime bump is not explained by any retained file; that is the one unresolved item in this sweep.

[unk] Any uncommitted or ignored change inside the sibling lane repositories other than the mado and kotoba artifacts cannot be excluded by this sweep, because the assignment scoped the fleet comparison to `git status --porcelain` at the fleet root, which does not descend into nested repositories. The mado and round-49 signal was pursued only far enough to attribute the two delta paths.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ScoutMisrootBaseline.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/measure/exits.txt, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2-spec.json, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SHONEN.md at 5e7c04ec, /home/vgpnk/Projects/shokunin/.ufo/state/mado.report-baseline, /home/vgpnk/Projects/shokunin/.ufo/state/tsukuroi.report-baseline, /home/vgpnk/Projects/shokunin/.ufo/waves/round-49/falsify/RowGameDev2d.md, /home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-25.md, /home/vgpnk/Projects/shokunin/.ufo/watchdog.log, /home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh, /fast/scratch/hyaku/tsukuroi-r25/fleet-porcelain-before.txt, /fast/scratch/hyaku/tsukuroi-r25/ScoutMisrootBaseline_porcelain-now.txt, /fast/scratch/hyaku/tsukuroi-r25/ScoutMisrootBaseline_porcelain-after.txt, /home/vgpnk/Projects/shokunin/mado-shokunin (status only); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/ScoutMisrootAfter.md, /fast/scratch/hyaku/tsukuroi-r25/w2/ScoutMisrootAfter/fleet-after-scoutmisroot.txt, /fast/scratch/hyaku/tsukuroi-r25/w2/ScoutMisrootAfter/fleet-after-all.txt, /fast/scratch/hyaku/tsukuroi-r25/w2/ScoutMisrootAfter/lane-after-scoutmisroot.txt; executed=git status --porcelain (fleet, lane, -uall, ignored, scoped), git rev-parse HEAD, git merge-base --is-ancestor, git show, git ls-files, git hash-object, git log, git diff --stat, git check-ignore, diff, find, stat, grep, sha256sum, printf | sha256sum
Model: not exposed
Installs: none
