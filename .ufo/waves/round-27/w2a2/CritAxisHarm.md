# CritAxisHarm — round 27 attempt 2, falsify wave 2

Verdict: partly holds. Round 27 harms operability: the lane's own registry-coverage gate turns from pass to fail. It also breaks calibration in two ways: it leaves a companion contradiction that its own new QUALITY 67 forbids, and the round-26 axes table now has five stale counts. No lane file lost content outside two in-place tool rewrites, and the three named operability selftests pass on an export.

Attacked revision: 099c7b3f42d073203d9448807860f04c175eccd7 (tip) against base 3beab8ddcf4ed2ae9fdf12eab6ac7f840c74e333. Exports are at /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/tree (tip) and /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/base (base). There is also a private git sandbox at /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/sb on `master`, built with archive and `git init`. In the sandbox, commit 19ca40d930493470c845c06cb88edcb4e02659d6 holds the base bytes and commit 3c12871e9de562862c3d05c90a62694ba88474ad holds the tip bytes.

## Findings

1. [obs] Lost lines: only two lane files outside `.ufo/` have deletions, and both are in-place rewrites, not lost content. No file is deleted or renamed anywhere, including under `.ufo/`. Command: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --numstat 3beab8dd 099c7b3f42d073203d9448807860f04c175eccd7`, filtered to rows with deletions outside `.ufo/`, gives exactly `45 13 tools/check-self-assessment.py` and `26 2 tools/check-storage-health.py`. `git diff --name-status` shows only A and M entries and no D entries. That means the two deleted 0-byte .err files were never tracked [inf].
   - [obs] In `tools/check-storage-health.py`, the 2 deleted lines are `start = spans[quote_col][0]` and the `if span_start >= start]` filter. They are replaced by a filter bounded to the quote cell plus a leading-pipe offset fix. `--selftest` on the export exits 0 with 44 cases and 0 failed. `--revision` output is byte-identical between the base and tip sandbox commits, and both exit 0.
   - [obs] In `tools/check-self-assessment.py`, the 13 deleted lines are the old `reference_lines` body and three fixture strings that say `(round 1)`. The fixture's declaring round moves from 1 to 2.
   - [inf] Side effect of the fixture move: the older cases `declaring-round-declaration-line` and `declaring-round-measured-outcome-line` still insert `Round 1` sections (/fast/scratch/hyaku/tsuku27a2/CritAxisHarm/tree/tools/check-self-assessment.py:934-948). They now test an earlier round's records, not the declaring round's, so their names and the comment "does record the round's move" are stale. The new case `own-round-outcome-depth-10` (line 896-901) covers the own-round exclusion.
   - [inf] The new `excluded` branch is never exercised by any selftest case. It handles a section of the declaring round nested inside an earlier measured-outcome section (lines 384-388). This is a minor gap, not a regression.

2. [obs] Operability regression: the registry-coverage gate goes from PASS to FAIL. The round adds `tools/check-kernel-taint.py` and `tools/check-adjacency-overlap.py` without a registry row. The operative registry is the highest `## Gate and probe registry — round<N> superseding current rows` table. That is still round 26's, at /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/tree/SKILL.md:2377. Its rows end at `storage-health` (SKILL.md:2415), and no round-27 table exists. The rule that requires the highest table is stated at SKILL.md:2062.
   - Command (in the sandbox): `python3 tools/check-registry-coverage.py --revision 19ca40d930493470c845c06cb88edcb4e02659d6` exits 0 with `PASS {'missing': 0, 'registered': 29, 'tools_total': 29}`.
   - Command: `python3 tools/check-registry-coverage.py --revision 3c12871e9de562862c3d05c90a62694ba88474ad` exits 1 with `FAIL {'missing': 2, 'registered': 29, 'tools_total': 31}` and two `REGISTRY-ROW-MISSING` findings at `tools/check-adjacency-overlap.py` and `tools/check-kernel-taint.py`.
   - Receipts: /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/regcov-19ca40d930493470c845c06cb88edcb4e02659d6.json and /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/regcov-3c12871e9de562862c3d05c90a62694ba88474ad.json.
   - [obs] The round-26 registry row for self-assessment (SKILL.md:2413) still describes "R26 fixed check set K01 to K27". The QUALITY 65 change in round 27 altered how K01 to K06 choose their reference, but the row does not say so.
   - Impacted axes: operability and calibration.

3. [obs] Sweep of every other gate: no other gate changes its result. I ran each `tools/check-*.py`, `tools/report-red-causes.py` and `tools/measure-update-recheck.py` with `--revision` at both sandbox commits; outputs are in /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/sweep/.
   - The only change from exit 0 to non-zero is `check-registry-coverage` (0 then 1).
   - `check-kernel-taint` (2 then 0) and `check-adjacency-overlap` (2 then 0) are the round's declared counters.
   - Nine gates exit 1 or 2 at both commits with byte-identical output once the revision hash is stripped. Their failures come from the sandbox's two-commit history, not from the round [inf]: `check-appended-notices`, `check-freshness-r17`, `check-pause-gate`, `check-review-snapshots`, `check-revision-binding`, `check-seat-bindings`, `check-seat-scope`, `check-section-citations` and `report-red-causes`.
   - `check-recheck-commands` exits 0 at both, with `file_count` 48 then 50 and `clean_count` 32 then 34, so the two new notes are clean.

4. [obs] Calibration harm: the round leaves an earlier companion statement contradicting its own appended withdrawal, which violates the round's own QUALITY 67.
   - The round appends an "R27 current-use notice" to /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/tree/corpus/knowledge/memory-pressure-r25.md:402. It says to "read the exception as withdrawn for this host", meaning earlyoom `--kernel-oom`.
   - The JSON companion `corpus/knowledge/memory-pressure-r25.json` is untouched by the round (it is absent from the numstat). Its row MP6 `notes` field (line 485) still says, unmarked: "A userspace killer moves neither kernel counter unless it asks the kernel to kill: earlyoom started with --kernel-oom does". Command: `grep -c kernel-oom corpus/knowledge/memory-pressure-r25.json` gives 1.
   - QUALITY 67, added by this round (/fast/scratch/hyaku/tsuku27a2/CritAxisHarm/tree/corpus/QUALITY.md:135), requires that "every appended correction is marked in each companion in the same commit" and that the entry header names its companions. `memory-pressure-r25.md` has no `companion:` line in its first 12 lines; neither does `storage-health-r26.md`.
   - The round's own lesson row R27-COMPANION-UNSWEPT (corpus/lessons/round-27.md:52) names only the storage JSON.
   - The new entries do comply: `kernel-taint-r27.md:6` and `adjacency-mori-oom-r27.md:5` carry `companion:` lines.
   - Impacted axes: calibration and adjacency (OV5 is the source of the notice).

5. [obs] No contradiction from the round's appends to `SKILL.md`, `PROVINCE.md` or `corpus/README.md` themselves. I grepped all three at the tip for `taint|unsigned|sig_enforce|out-of-tree|kernel-oom|earlyoom|module signing|signer|secure boot`.
   - `SKILL.md` never calls the nvidia modules "unsigned". The only hit, line 2436, is the new KT3 error-pattern row, and it is consistent with the new KT3 wording.
   - The driver-plane row at SKILL.md:49 states no signing claim.
   - The `SKILL.md` MP6 row (line 2318) states the universal "a userspace killer's SIGKILL moves neither counter" without the `--kernel-oom` exception, so the OV5 withdrawal does not make it false.
   - `PROVINCE.md` appends at the end (lines 178-189). The lines that mori's pointer now resolves to (30-33 and 44-53, per OV2) are unchanged. The Frontier acknowledgement bullet (PROVINCE.md:77) is restated as still open, which is consistent.
   - The claim in `corpus/README.md` that kernel taint is "deeper ground inside the existing driver and firmware Core area" matches the Core text at PROVINCE.md:12 ("driver/firmware plane (kernel modules, nvidia driver + GSP firmware").
   - The two "unsigned" statements at driver-firmware-plane.md:160 and 202 are reinterpreted by an appended note at line 311. They are not left standing silently.

6. [obs] The round-26 axes table is now stale on five counts at the tip, up from one at the base. The table is /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/tree/SCORECARD.md:976-981, under the second `## Axes — current self-assessment (round 26)` at line 970.
   - Command: `python3 <export>/tools/check-self-assessment.py --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision <REV>`.
   - **Base tool at the base revision:** exit 1, 1 of 27 (K10 states 28 lesson files, observes 29). This one was already stale before round 27.
   - **Base tool at the tip:** exit 1, 5 of 27:

     | Check | Count | Stated | Observed at tip |
     |---|---|---|---|
     | K07 | knowledge notes | 48 | 50 |
     | K08 | `SKILL.md` lines | 2418 | 2436 |
     | K09 | `SKILL.md` table lines | 336 | 348 |
     | K10 | lesson files | 28 | 30 |
     | K11 | `corpus/README.md` lines | 248 | 256 |

   - **Tip tool at the tip:** exit 1, 7 of 27. These are the five above plus K02 and K06, which report "no dated move record".
   - **Tip tool at the base:** exit 1, 3 of 27 (K02, K06, K10).
   - [obs] Under the base tool, K01 to K06 all read SCORECARD.md:960, the round-26 own-round record. Under the tip tool they read lines 730, 731, 772 and 771, and K02 (coverage) and K06 (adjacency) read nothing. K02 and K06 are therefore not new harm. QUALITY 65 exposes that the round-26 C2 "0 of 27" was self-agreement. They stay red until an axes table labeled round 27 makes the line-960 record (coverage 9 → 9, adjacency 8 → 8) an earlier-round reference [inf].
   - [obs] The freshness row's "all 48 notes now carry a `recheck:` line" is stale in number only: all 50 notes at the tip carry `recheck:` (a loop over `corpus/knowledge/*.md` lists none without it).
   - [unk] Whether the L1 plans to re-state the axes table at closure. The round-27 sections of `SCORECARD.md`, `corpus/lessons/round-27.md` and `LOG.md` contain no statement about the stale counts or the registry gap; I grepped for `registry|axes|stale|K07|mismatch|2418`.
   - Receipts: /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/sam-{base,tree}-{3beab8dd,099c7b3f…}.json.
   - Impacted axes: calibration and depth (the table's evidence pointers).

7. [obs] Operability selftests on the read-only export at the tip, run from /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/tree:

   | Command | Exit | Result |
   |---|---|---|
   | `python3 tools/check-storage-health.py --selftest` | 0 | 44 cases, 0 failed |
   | `python3 tools/check-memory-pressure.py --selftest` | 0 | 41 cases, 0 failed |
   | `bash tools/tsukuroi-census.sh --selftest` | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)` |
   | `python3 tools/check-kernel-taint.py --selftest` | 0 | 46 cases |
   | `python3 tools/check-adjacency-overlap.py --selftest` | 0 | 17 cases |

   - `python3 tools/check-self-assessment.py --selftest` exits 2 with `"error": "not a git repository"` on a plain export. The base export behaves the same way, so this is not a regression. In a `git init` copy it passes: 13 cases at the base and 15 at the tip, both `PASS`. [inf] The "hermetic" selftest still needs to run inside a git work tree. This is pre-existing.

## Smallest safe corrections (the L1 decides)

1. Append `## Gate and probe registry — round27 superseding current rows` to `SKILL.md`. It should carry every round-26 row forward and add rows for `tools/check-kernel-taint.py` and `tools/check-adjacency-overlap.py`. The self-assessment row should state the QUALITY 65 reference rule. Then re-run `check-registry-coverage.py --revision <new>` and expect exit 0 with 31 of 31 tools.
2. Append to `corpus/knowledge/memory-pressure-r25.json` a top-level corrections marker in the same shape as `corrections_r27` in the storage JSON, for the MP6 `notes` text containing `--kernel-oom`, pointing at memory-pressure-r25.md:402. Optionally add a `companion:` line notice to the `.md`. Alternatively, record in the round-27 lesson that QUALITY 67 is not yet applied to this pair.
3. Re-state the axes table as round 27 at closure with counts measured at the closing revision. At the tip those are 50 notes, 2436 `SKILL.md` lines, 348 table lines, 30 lesson files and 256 `corpus/README.md` lines. This also lets K02 and K06 read the round-26 record. Alternatively, record the five stale counts as known mismatches of the closing measurement.
4. Optionally rename the two `declaring-round-*` selftest cases, or move them to `Round 2`, so that they test the declaring round as named.

Scope: read=lane git objects at 3beab8dd and 099c7b3f (numstat, name-status, diffs, show), exported trees, SKILL.md, PROVINCE.md, corpus/README.md, SCORECARD.md, QUALITY.md, LOG.md, corpus/lessons/round-27.md, memory-pressure-r25.md and .json, driver-firmware-plane.md, kernel-taint-r27.md, adjacency-mori-oom-r27.md, tools/check-self-assessment.py, ~/.agents/skills/godspeed/directive.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/CritAxisHarm.md, /fast/scratch/hyaku/tsuku27a2/CritAxisHarm/ (exports, git sandboxes g-base, g-tree, sb, sweep outputs, JSON receipts); executed=git archive, git diff --numstat/--name-status, git log, git show (all read-only against the lane), selftests of check-storage-health, check-memory-pressure, tsukuroi-census, check-self-assessment, check-kernel-taint and check-adjacency-overlap on the export, check-self-assessment --repo lane --revision at base and tip with base and tip tools, every tools/check-*.py plus report-red-causes and measure-update-recheck with --revision at both sandbox commits, grep/sed/awk reads
Model: not exposed
Installs: none
