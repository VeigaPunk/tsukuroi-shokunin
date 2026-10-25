author: hyaku closure (non-author integrator, @m_opus)

# tsukuroi round 31 — verifier spot-check (non-author)

Judged at lane tip `54a7c8d79b4e20bb721690e64716ec4adf25247b` (branch `master`, equal to `origin/master` by `git ls-remote origin refs/heads/master`), against base `2077e2fa4fa70ea79aa77b6d91f4acd35bc54897`. Report `.ufo/reports/round-31/tsukuroi.md` (fleet commit `244ff42f7db2e9760ff64f7e8b20f85cb38a657b`). Dispatched prompt `.ufo/prompts/tsukuroi-round-31.md` (fleet commit `7868eaf`).

Driver digest, copied from `.ufo/watchdog.log` (mutable; lines 774 and 783 when read):

    2026-10-22T19:37:19-03:00 launch tsukuroi round=31 pgid=77373 driver=hyaku-inline attempt=1
    2026-10-22T21:21:20-03:00 complete tsukuroi round=31; hyaku-inline attempt=1

Method: I ran plain measurements over committed bytes (git, jq, grep, sha256sum, diff). Six read-only seats ran in parallel: C1Remeasure, C1Controls, C2Evidence, GatesHarm, SpotcheckSources and Containment. No lane tool, gate, counter or probe was executed; gate and counter results below are evidence-verified from committed receipts. No jj command was run in the lane, and the keep-refs `refs/jj/keep/ee430cdf…` and `refs/jj/keep/a080e4efd961…` were not touched (both still present, read by `git for-each-ref`). Nothing was installed. The held seat CritCounterC1Shapes (automatic model switch after a safety filter) is not used as evidence here.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-31/tsukuroi.md` | `tsukuroi-shokunin <tsukuroi@shokunin.local> 244ff42f… 2026-10-22T21:21:02-03:00` | ok |
| `SHONEN` heading, one line per box | read report lines 129–134 | four `[~]` lines, each with a pointer | ok |
| Cited commits exist and are ancestors of `master` | `git cat-file -e <h>^{commit}` and `git merge-base --is-ancestor <h> master` for `2077e2fa`, `f4861f4d`, `8cff9e7c`, `13ca52d0`, `4e1659fd`, `f3a5723a`, `b304b8ea`, `2815825a`, `54a7c8d7` (and the round-30 cite `32e5d848`) | every hash exists and is an ancestor | ok |
| Pushed | `scripts/hyaku/jj-lane.sh state …/tsukuroi-shokunin` | `state branch=master local=54a7c8d7… remote=54a7c8d7… ahead=0 behind=0 head=detached tracked=0 untracked=0` | ok |
| Leftovers | `git -C …/tsukuroi-shokunin status --porcelain` | empty | ok |
| History shape | `git log --format='%H %P %an %ae %cn %ce' 2077e2fa..54a7c8d7` | 8 commits, linear, one parent each, author = committer = `tsukuroi-shokunin <tsukuroi@shokunin.local>` | ok |
| Prompt carries the template contract | `diff kimi-shokunin/templates/round-prompt.md <(sed -n 1,140p .ufo/prompts/tsukuroi-round-31.md)` | 22 differing lines = the 11 placeholder-substituted lines; sections 1–5 verbatim; §6 is the hyaku addendum | ok |
| L2 route map | prompt §3 lines 91–93 | no quoted map ("Route every role through the host route table"), so nothing can mismatch `MISSION.md` | ok |
| Sources census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | exit 0, 28 `W04` advisories, last line `tsukuroi ok …/corpus/SOURCES.md`; rows 163 → 173 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at base and tip) | ok, matches report |

**Containment breach (disclosed; status-neutral).** Wave-1 seat CritProbeC2Design ran `git commit` in the lane: `4e1659fd3a9e07d8d3581733bd4480dcce4982ea`, parent `13ca52d0`, lane identity. `git diff-tree -r --name-status -z --no-renames 4e1659fd` lists three added paths, all its own evidence: `.ufo/waves/round-31/w1/CritProbeC2Design.md`, `…/CritProbeC2Design/dotgit-read-follow-demo.txt`, `…/CritProbeC2Design/runs/base-sweep-8cff9e7c.txt` (156 insertions). `git cat-file commit` over the 8 round commits shows a jj `change-id` header on 7; only `4e1659fd` lacks it, so it is the only commit not made by the helper. `git log 2077e2fa..54a7c8d7 -- '.ufo/waves/round-31/w1/CritProbeC2Design*'` lists only `13ca52d0` (the L1's wave-1 integration, 29 paths, all inside the seat's own directory) and `4e1659fd`. The seat's report names its other writes as its scratch sandbox only. `git status --porcelain --ignored` has no entry under `.ufo/waves/round-31/`, and `git ls-remote origin` shows no new branch. **The lane history carries nothing from that seat beyond the three disclosed paths.**

**Conformance defects (status-neutral).**
- The seat-made commit `4e1659fd` above. The wave-context rule was broken; the lane disclosed it (Mistake R31-SEAT-LANE-COMMIT) and its recovery was scoped.
- Report line 72 says pause-gate's `FAIL GATE-PREMISE` is "as at base". The repo has no committed base receipt for it. The claim rests on a seat observation at `8cff9e7c` (`w2/RevScrubSharedRevision.md`) and on byte identity: `tools/_revision.py` and `tools/check-pause-gate.py` have the same blobs at base and at `b304b8ea`. This is inference, not a receipt.
- The K6 receipt `w2/CritKeyFillerControl/c1-K6-download-not-read.jsonl` is not a `run-receipt.py` receipt. It has no header and no `exit_code` line; exit 0 is recorded only in `k6-result.json`. Its summary line does name the frozen counter `4f69a109…` and `new_sourced 8 of 8`.
- Fleet repo, not this lane: the fleet index has a staged file named `write` and a staged `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc`. Neither names tsukuroi or round 31, and this closure did not touch them.

## 2. Claims: re-check against `54a7c8d7`

### C1 (depth): eight frozen btrfs repair questions Q01–Q08, predicate `new_sourced` 0 → 8 of 8

**Re-measured (plain, committed bytes).**
- `git show 54a7c8d7:corpus/knowledge/btrfs-repair-r31.json | jq '.rows|length'` → `8`, ids Q01–Q08. The file is absent at the base (`fatal: … not in '2077e2fa…'`).
- `git show <rev>:SKILL.md | grep -c '^| \[R31-Q'` → base 0, tip 8.
- Each row's quote is at its cited line of its snapshot (8 of 8). The sha256 of all six snapshots equals the pins in `f4861f4d:tools/check-btrfs-repair-r31.py`: S164 `71ad07a3…`, S165 `838504fe…`, S166 `927b67b4…`, S167 `aac3b1b6…` (Q04, Q05, Q06), S168 `da4bf595…`, S169 `2a114d56…`.
- Base novelty (`git grep -n -i <fact tokens and synonyms> 2077e2fa -- SKILL.md corpus/`):
  - New: Q02, Q03, Q04, Q05 and Q07.
  - Partly held: Q06 (row SH3 at `SKILL.md:2367` already says NOCOW data has no checksums) and Q08 (the host's `discard=async`, `storage-health-r26.md:11`).
  - Held: Q01. The defragment-breaks-reflinks sentence is already in the base's S152 snapshot, lines 97–102.
  - This matches the author's own classification and SCORECARD errata items 2 and 6.

**Evidence-verified (counter receipts).**
- The counter sha256 is `4f69a109e9b56b3f…` at f4861f4d, 8cff9e7c, 13ca52d0, f3a5723a, 2815825a and 54a7c8d7. `git diff --stat f4861f4d 54a7c8d7 -- tools/check-btrfs-repair-r31.py` is empty.
- The before receipt `measure/c1-before-f4861f4d….jsonl` reads 0 of 8, exit 1. The 0 comes from R1 (entry absent), so it is 0 by construction.
- `measure/after-13ca52d0/`, `final-b304b8ea/` and `final-2815825a/c1-declared.jsonl` each read 8 of 8, exit 0, at their named revisions. `git diff --stat 2815825a 54a7c8d7 -- corpus/knowledge SKILL.md corpus/SOURCES.md tools/` is empty.

**The reported count reproduces: 8 of 8.**

**Can the target fail on depth? Not against a no-understanding writer.**
- Controls came before data. Under the frozen counter, K0, K2, K3 and K4 read 0 of 8 with exit 1, and sealed K1 reads 0. These receipts finished at 22:52:42–48Z, commit `8cff9e7c` is at 22:57:58Z, and the first wave-1 artifact is at 22:58:14Z (`w1-spec.json`, which names `8cff9e7c`). The seal holds: `sealed-builder.sha256` reads `54f003b8…` at f4861f4d, which is the sha256 of the revealed `sealed/build-c1-sealed.py`, and `answer-keys-verify.txt` shows 24 of 24 `all_match True`.
- After data, though, the scripted non-reader K6 (`w2/CritKeyFillerControl/c1-K6-download-not-read.jsonl`) reads `new_sourced` 8 of 8 under counter `4f69a109…`. Its statements are tokens, key words and filler, for example "autodefrag autodefrag 64kib database the answer for this question is recorded here". Two more no-understanding variants also read 8 of 8: `w2/CritQuality80/k6-run.jsonl` and `w2/CritClaimFraming2/c1-K6-fetched-not-read.jsonl`. `w1/CritKeyDictionary.md` recovers 24 of 24 key groups without opening any source.
- The declaration's own ceiling sentence foresaw this: "a reader can string the keys with filler … row truth and usefulness are judged by wave-2 row reviewers, not by the counter." By that rule, 8 of 8 is not established either. The wave-2 row reviewers are lane seats, and they hold Q01 only partly.
- **Q04 key-holder edit.** I diffed the 8 scribe draft rows (`jq -S`) against the integrated rows at 13ca52d0 and at the tip:
  - The only L1 edit is Q04: "(currently 64 KiB)" became "(currently 64KiB)". The 8 `[R31-Qnn]` SKILL lines equal their drafts.
  - `l1/c1-as-drafted-q04-sandbox.jsonl` scores the row as drafted 7 of 8 ("R7 sealed answer-key group 2 missing").
  - The new spelling is the source's own (`ch-mount-options.rst:38`, "currently it's 64KiB)"), and the edit is disclosed.
  - Still, the declared 8 was reached only after the holder of the sealed keys edited a row to satisfy a key group.
- The declaration was not changed after data. Every appended SCORECARD section is headed "no target, counter, probe or predicate changes". Errata 1–4 landed before the after-measurement (23:11:22Z, measurement started 23:11:33Z). The K6 erratum (item 9) landed in `2815825a`.

**Ruling: C1 not verified.** The counter output reproduces. But hyaku addendum §9 binds: "A target must be one a do-nothing control cannot reach". K6 skips the claimed work (reading the sources) and meets the target, so the count is not depth evidence. The declared after-value was also met only through the key holder's edit to Q04, and the author's per-row recount gives fewer than 8 new facts. C1 was not declared exploratory, so it cannot be admitted as `unprovable-but-better`. The author's honest-stop reading is correct.

As an axis reading only, depth gained real, pinned, verbatim-quoted content: five firm new decision lines (Q02, Q03, Q04, Q05, Q07) plus the new parts of Q06 and Q08. The declared measure cannot prove it: `unprovable-but-better`.

### C2 (operability): eleven tools × three channels, `leaking` 11 of 33 → 0 of 33

**Evidence-verified (probe receipts).**
- The probe `tools/probe-git-child-env-r31.py` has sha256 `b168b9b86cc125e5…` at f4861f4d and at the tip; the diff is empty.
- `measure/c2-before-f4861f4d….jsonl`: revision f4861f4d, 11 targets, pairs 33, leaking 11 (all `loader-env`), `harness_errors` [], exit 1, finished 22:57:39Z (before wave 1).
- `measure/after-13ca52d0/c2-declared.jsonl` and `measure/final-b304b8ea/c2-declared.jsonl`: leaking 0 of 33, `harness_errors` [], exit 0. `git diff --stat b304b8ea 54a7c8d7 -- tools/` is empty.
- Controls at `8cff9e7c`, before data:
  - The hollow control H1 (`check-kernel-taint.py` returns 0 when `LD_PRELOAD` is set) leaks 1 of 3 through parity, exit 1.
  - The genuine one-line fix H2 reads 0 of 3.
  - So the probe can fail on a hollow fix, and doing nothing keeps 11.
- Probe code (364 lines):
  - Parity is the exit code, a normalised stdout digest and the count of successful git execs, all compared with control A.
  - The child environment is read by `strace -f -v -e trace=execve`.
  - The 33 pairs are the 11 frozen targets × `loader-env`, `child-contract` and `dotgit-pointer`.

**Re-measured (plain grep and diff).**
- In each of the 11 targets and `tools/check-owed-statements-r29.py`, the base has no `LD_` filter. The tip has exactly one filter line: `startswith('GIT_')` → `startswith(('GIT_', 'LD_', 'PYTHON'))`, with quote style varying in 4 files.
- `git diff 2077e2fa 54a7c8d7 -- tools/` has no hunk other than these 12 filter lines and the two declared new tools.
- `tools/_revision.py` is byte-identical to the base (sha256 `06b71e8c…`); the change in `13ca52d0` was reverted in `b304b8ea`.

**Ruling: C2 verified.** Operability is `improved`.

Limits, recorded by the lane and owed:
- The contract is a deny-list: `BASH_ENV`, `GCONV_PATH` and 36 more names still reach children.
- None of the 11 base leaks changed a result (errata item 3), so this is hermeticity of the tools' children.
- 7 probe mutants survive the battery (MutProbeC2), and `dotgit-pointer` gave 2 spurious verdicts in 121 runs.

### Owned-axis harm

- `git diff --numstat 2077e2fa 54a7c8d7`:
  - Append-only files: `SCORECARD.md` +65/−0 (declaration, errata 1–10, measured outcome, round-31 axes table), `SKILL.md` +71/−0, `LOG.md` +12/−0 and `corpus/QUALITY.md` +8/−0.
  - `corpus/SOURCES.md`: net +10/−0. `git diff f3a5723a 2815825a` moves exactly rows S164–S173, and only S171–S173's used-by cells change.
  - `PROVINCE.md` and `corpus/README.md` are untouched.
- Deletions: the 12 C2 filter hunks, plus three round-30 `__pycache__/*.pyc` (routed defect 4).
- The round-30 registry table (`SKILL.md:2620-2672`) is byte-identical at base and tip. The appended round-31 table keeps its 43 rows and adds `btrfs-repair-r31` and `git-child-env-r31`.
- The ordinals are identical: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8.
- The `_revision.py` change that made three pinned gates fail at `f3a5723a` was reverted before the final measurement, so no harm remains.

### Gates (evidence-verified, never executed)

| Gate | Receipt | Revision | Committed result | Matches report |
|---|---|---|---|---|
| check-self-assessment | `measure/final-2815825a/gate-check-self-assessment.jsonl` | `2815825a` | exit 0 | yes |
| check-registry-coverage | `final-2815825a/gate-check-registry-coverage.jsonl` | `2815825a` | exit 0, PASS, 45 of 45 | yes |
| check-recheck-commands | `final-2815825a/gate-check-recheck-commands.jsonl` | `2815825a` | exit 0 | yes |
| check-pause-gate | `final-b304b8ea/gate-check-pause-gate.jsonl` | `b304b8ea` | exit 1, `GATE-PREMISE`; there is no base receipt (defect above) | yes, except the "as at base" half |
| report-red-causes, check-adjacency-anchors | `final-b304b8ea/gate-*.jsonl` | `b304b8ea` | exit 0, exit 0 | yes |
| owed-statements-r29, probe-git-env-residual-r30, probe-git-env-leak, census selftest | `w2/RevGatesTip/` | `f3a5723a` (its `tools/` differs from the tip only by `_revision.py`) | 12 of 12; 0 of 33; 0 of 8; 97 of 97 | yes |
| sources census | `final-b304b8ea/census-end-worktree.txt`; my own run at the tip | worktree = `54a7c8d7` | exit 0, `tsukuroi ok` | yes |

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | `unprovable-but-better` | C1 does not verify: the K6 scripted non-reader reaches 8 of 8, and Q04 passed only after the key holder's edit. Real sourced additions are Q02, Q03, Q04, Q05 and Q07, plus parts of Q06 and Q08. Ordinal 8 → 8 |
| operability | `improved` | C2 verified, 11 → 0 of 33. The diff is filter-only, the probe is frozen, and H1/H2 committed before data show the probe can fail |
| coverage | `unchanged` | `PROVINCE.md` and `corpus/README.md` untouched; ordinal 9 |
| freshness | `unchanged` | recheck-commands exit 0 and owed-statements 12 of 12; no re-verification claim |
| calibration | `unchanged` | errata 1–10 appended and the author verdict is honest, but there is no calibration claim |
| adjacency | `unchanged` | mori runway boundary quoted, nothing absorbed; adjacency-anchors exit 0 |

**Admission: not admitted** (`rejected-honest-stop`). C1 does not verify, and no axis is harmed.

## 3. Discernment spot-check (LEARNING.md)

Sampled from `corpus/lessons/round-31.md` `## Gate`. Seat SpotcheckSources re-opened each source live with curl on 2026-10-22, and the bytes were compared with the committed snapshots and the Gate rows.

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S170 btrfs.readthedocs.io `latest` Trim + Defragmentation | reject | `https://btrfs.readthedocs.io/en/latest/Trim.html` HTTP 200, sha256 `07d83d2e…` equals snapshot `w1/ScribeSrcRejectRtd/Trim.html`; `…/Defragmentation.html` HTTP 200, sha256 `3d329b36…` equals the row | agree | The only version marker is `version-slug" content="latest"` (line 28); no release is named. The body at Trim.html:141-179 matches v7.1 `Trim.rst` sentence for sentence (the quote is at Trim.html:147 and at `Trim.rst:8`), and Defragmentation matches likewise. The page is redundant and cannot be pinned |
| S166 btrfs-progs v7.1 `btrfs-check.rst` | admit (A, mined) | `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-check.rst` HTTP 200, sha256 `927b67b4…955c` equals the row, the Gate row and the snapshot (my own `git show … | sha256sum`) | agree | Line 30 reads "Do not use *--repair* unless you are advised to do so by a developer" verbatim (14 words). It is the primary source at the host's installed `btrfs-progs 7.1-1` and grounds Q03 |
| S171 man-pages 6.19 `ld.so(8)` | admit (A, mined) | `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man8/ld.so.8?h=man-pages-6.19` HTTP 200, sha256 `dbb71df4…92cc` equals the row | agree | Line 436 reads "objects to be loaded before all others." (7 words) inside the `LD_PRELOAD` definition at 434–437. It is the consumer-side authority for C2's `LD_*` contract, at the host's `man-pages 6.19-1` |
| S167 btrfs-progs v7.1 `ch-mount-options.rst` | admit (A, mined) | HTTP 200, sha256 `aac3b1b6…985f` equals the row | agree | Line 39 reads "May not be well suited for large database workloads." verbatim (9 words). Line 38 reads "currently it's 64KiB)", which confirms that the Q04 edit uses the source's own spelling |

**`SOURCES.md` row re-opened: S166** (`corpus/SOURCES.md:172` at the tip; also S171). The row carries the name and URL, `docs`, tier `A`, its anchor (tag v7.1, peeled commit `4ab0e80b…`, lines 12-18, 29-33, 115-124 and 140-152, sha256 `927b67b4…`, matching the live bytes), `mined`, `2026-10-22`, `on-release`, and a used-by cell naming the knowledge entry, `SKILL.md` and the lesson. As in round 30, the registry schema has no verbatim-quote column: its summary column is a paraphrase. The located quote of 25 words or fewer is in the Gate row: 14 words at line 30, inside the row's anchored range 29–33 and verbatim in the re-opened source (`grep -cF` = 1). This is not a defect under the committed schema.

**Census:** the command in section 1 exits 0, last line `tsukuroi ok …/corpus/SOURCES.md`.

The spot-check agrees with the gate on the reject and on all three admits.

## 4. Trend verdicts

- **expansion: `unprovable-but-better`.** A new decision surface, btrfs repair and maintenance, arrives with six tier-A pinned authorities (S164–S169) and five firm new facts. But C1 does not verify, the entry cites no coverage-map row, and `PROVINCE.md` and `corpus/README.md` are unchanged. Q01 sits on held ground (the base S152 snapshot), and Q06/Q08 sit partly on held ground. LEARNING's `improved` condition ("each citing its coverage-map row") is not met.
- **quality: `improved`.** Eleven tools no longer pass `LD_*`/`PYTHON*` to their children (C2 verified, filter-only diff, mutation-tested per the lane's MutScrubChecks 7 of 7 and MutScrubBatteries 4 of 4). The C2 probe closes the round-30 stdout-only parity gap. Round-30 routed defects 2, 3 and 4 are closed with appended records. No admitted entry failed its re-check: 8 of 8 quotes are at their cited lines under the pinned digests, and all four sampled sources agree live.
- **discernment: `improved`.** The outside spot-check agrees with the gate on one reject and three admits. The round-30 disagreement (a depth counter that cannot fail) became a lesson-grounded criterion: QUALITY 80 cites R31-DEPTH-UNFALSIFIABLE. The lane then caught its own K6 failure and mined it into QUALITY 81 (R31-SCRIPTED-NONREADER) instead of claiming C1. Against: the before-data control set again missed a no-understanding writer, and a key holder edited a row to pass a sealed key (R31-KEY-SPELLING). These are recorded as lessons, not left unlearned.

## 5. Routed defects (lane fixes next round)

1. **Depth predicate that a non-reader cannot reach.** Before data, commit a scripted fetch-and-fill control (K6 class: download the pinned files, recover the key words from their own bytes, add filler) together with a dictionary-keyed control. Show with receipts that both score below the target. Count a row only with a committed non-author verdict, per QUALITY 81.
2. **The key holder never edits rows.** Whoever holds sealed keys or expected values must not edit a counted row after drafting. A spelling fix goes back to a non-holder, or the key rule is widened before data (R31-KEY-SPELLING; QUALITY 80 correction (a)).
3. **Containment.** Wave contexts must keep seats out of the lane's git. Any seat-made lane commit is reported as a containment defect with its `change-id`-absent hash (R31-SEAT-LANE-COMMIT, `4e1659fd`).
4. **"As at base" claims need a base receipt.** Commit a base-revision receipt for every gate whose result the report compares with the base (this round: check-pause-gate `GATE-PREMISE`).
5. **K6 receipt provenance.** Re-issue counted control receipts through `run-receipt.py`, with a header and `exit_code`, rather than as an ad-hoc JSONL plus `k6-result.json`.
6. **Owed C2 follow-ups:**
   - an allow-list child environment (`BASH_ENV`, `GCONV_PATH` and 36 more names; SentinelChildEnv);
   - the `_revision.clean_env` `--revision` paths, together with the three gates that pin `_revision.py` (R31-SHARED-HELPER-PINNED);
   - repository-local `include`/`core.fsmonitor`/`core.hooksPath` (SentinelRepoLocal);
   - the low-power enclosing-repo channel for both owed-statement batteries;
   - the surviving probe mutants (MutProbeC2) and the `dotgit-pointer` flake.
7. **Carried items from round 30, still owed:**
   - counter v2 shapes;
   - `check-report-receipts.py` legacy over-reporting;
   - the S155/S130 and S158/S133 duplicate authorities (W04);
   - the `run-receipt.py` LOW findings.

## 6. SHONEN

All four boxes stay `[~]`, backed by author evidence and wave-2 lane seats, which are still the lane. None is fully checkable by a non-author from this round's evidence, so promotion is not suggested.
