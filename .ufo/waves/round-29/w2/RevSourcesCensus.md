# RevSourcesCensus — wave 2 findings (round 29, tsukuroi)

Verdict: holds. The sources-census validate passes clean (exit 0, warnings only), rows S148-S150 each carry 11 cells under an unescaped-pipe split, S151's rejected row carries both a reason and a flip, and the S148-S151 additions plus the S133/S134 used-by changes are exactly the old→new set the lesson's registry-changes paragraph logs, with no unlogged registry change.

## Findings

1. [obs] Census validate passes: exit 0; 27 output lines = 26 W04 warnings + 1 final `ok` line. Last lines: `tsukuroi W04 S149 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes` then `ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`. No E-codes fired (per the script header an E or overdue finding exits 1; contract E01-E11 all clear, including E11 used-by paths existing on disk). Full capture: `/fast/scratch/hyaku/tsukuroi-r29/RevSourcesCensus/census-validate.txt`.

2. [obs] Cell-shape check: S148, S149 and S150 (corpus/SOURCES.md:154-156) each split into exactly 11 cells under the unescaped-pipe split `(?<!\\)\|` with leading/trailing empties dropped — matching the script's contract "11 columns => NF=13" (E01 NF!=13 would fail otherwise). S133, S134 (lines 139-140) and S151 (line 157) also split 11/11.

3. [obs] S151 rejected row carries both required parts (corpus/SOURCES.md:157): status cell `rejected`, tier `C`, used-by `corpus/lessons/round-29.md`; the teaches cell starts `REJECTED for this round:` with the reason (every 2009 scoring term absent from v7.2 `oom_badness` per S149, whole-file token counts for the old terms are 0, C1 rule M6 accepts only mined rows) and contains an explicit `flip:` clause (a claim explicitly historical, grounded in a version-pinned pre-`oom_score_adj` kernel file, article cited only as commentary). This matches the lesson's S151 gate row at corpus/lessons/round-29.md:14 (reject wording plus the Flip sentence). W02 (rejected row, thin teaches) correctly did not fire.

4. [obs] Registry changes vs the lesson's registry-changes paragraph (corpus/lessons/round-29.md:16) — every old→new is logged and nothing is unlogged. Cell-by-cell `git show` comparison of corpus/SOURCES.md between 3c94d730 and 10d5288fc1051364e711203855e7c53710dfcc21 (env GIT_* unset, read-only): the only row-level changes in the whole round diff are S148-S151 added (absent at 3c94d730) and S133/S134 changed in column 11 only: `corpus/knowledge/storage-health-r26.md` → `corpus/knowledge/storage-health-r26.md, corpus/knowledge/storage-health-r26.json`, exactly as the paragraph logs. Status (col 8, `mined`), opened (col 9, 2026-10-22) and recheck (col 10, `on-release`) are identical before and after for S133/S134, so the paragraph's closing claim "No status or recheck of an existing row changed" holds.

5. [obs] Used-by values in the new rows match the paragraph's logged list verbatim: S148/S149/S150 col 11 = `corpus/knowledge/oom-event-plane.md, corpus/knowledge/kill-event-deep-r8.md, SKILL.md, corpus/lessons/round-29.md` (paragraph's exact list), status `mined`, recheck `on-release`, tiers A/A/A/C as declared.

6. [obs, minor] The registry-changes paragraph logs S151's status and recheck but not its used-by value (`corpus/lessons/round-29.md`, SOURCES.md:157 col 11); the value is consistent with the lesson's own gate table, so this is a completeness nitpick, not a defect.

7. [obs, minor] The new S149 row triggers W04 (same URL across scopes) against existing S119 — both are v7.2 mm/oom_kill.c with the same raw-bytes sha256 452f1348… (SOURCES.md:125 vs :155) but different scopes (kill counting vs victim selection). Per the script contract W04 is a warning that never fails a lane (exit 0), and E04 (duplicate URL+scope without supersedes) correctly did not fire.

## Residual risk and verification gaps

- I did not re-fetch S148-S151 or recompute their sha256/line anchors; the census validates row shape, enums, dates and used-by path existence only. Content-level source verification is the scope of the RevSourceS148/S149 seats. [unk]
- One canonical runtime exercised: the lane registry discovered via `--root /home/vgpnk/Projects/shokunin` resolving to tsukuroi-shokunin/corpus/SOURCES.md; I did not run the fleet-level `shared` or `overdue` modes.
- Findings 4-5 rest on the diff between 3c94d730 and tip; I did not bisect which intermediate commit introduced the rows (immaterial to the paragraph-completeness question). [inf]

Scope: read=<scripts/sources-census.sh:1-60, tsukuroi-shokunin/corpus/SOURCES.md rows S133/S134/S148-S151 + header context, tsukuroi-shokunin/corpus/lessons/round-29.md:3-16, git diff 3c94d730..10d5288 corpus/SOURCES.md, git show cell comparison, census validate output x2>; wrote=<.ufo/waves/round-29/w2/RevSourcesCensus.md, /fast/scratch/hyaku/tsukuroi-r29/RevSourcesCensus/census-validate.txt>; executed=<sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi (exit 0, twice), git -C tsukuroi-shokunin diff 3c94d730..10d5288 -- corpus/SOURCES.md, git -C tsukuroi-shokunin show 3c94d730:corpus/SOURCES.md and tip comparison — all read-only, no GIT_* set to lane paths>
Model: zai/glm-5.3-flash
Installs: none
