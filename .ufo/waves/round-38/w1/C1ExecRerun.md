VERDICT: supports

# Seat C1ExecRerun — item C1-8: re-run the frozen C1 counter, compare with the author receipt

Independently re-ran `tools/score-storage-arm-r38.py` at the implementation commit and at
current lane master, and compared both JSON records field by field with
`.ufo/waves/round-38/after/c1-after-52ffd65.json`. The author's PASS reproduces exactly:
every substantive field (all 10 fixture records, the live record, predicate counters,
`euid_root`, `six_planes_all`) is identical. Only `branch_tip` (informational, advances with
master) and `revision` (the argument I passed) differ. A discrimination control at the base
revision FAILs, so the re-run is not trivially green. Nothing in the claim is falsified.

## 1. Counter identity — claimed == freeze commit == working tree

```
$ sha256sum tools/score-storage-arm-r38.py
e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218  tools/score-storage-arm-r38.py
$ git show 7cbaeb6317cb9f7323d2619eec02db4e4da29449:tools/score-storage-arm-r38.py | sha256sum
e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218  -
```
Claimed sha256 `e649bfb3...` (freeze 7cbaeb63, SCORECARD Round 38 declaration): matches both.
Working tree is unmodified for that path (`git status --porcelain --untracked-files=no` is empty).

The vehicle the counter actually executes is the census at `--revision`, not the worktree copy
(`tools/score-storage-arm-r38.py:198`, `git show f'{b.sha}:{CENSUS}'`). Its bytes are
identical at the implementation commit and at master, so the two re-runs exercise identical code:

```
$ for r in 52ffd65… 5edb6c2… 7cbaeb63…; do git show $r:tools/tsukuroi-census.sh | sha256sum; done
52ffd65f868431f021b8615ab281efd87195eac6  8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c
5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf  8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c
7cbaeb6317cb9f7323d2619eec02db4e4da29449  62c0e39a135bdda68cb6fd1a42936de2f33e15b7d5e4e49591d60aa5755482ac
```
`git diff --stat 52ffd65..5edb6c2 -- tools/` = `tools/score-storage-arm-r38-q82.py | 147 +++++`
only — no census or v1-counter change landed between the implementation commit and master.
Lane master at run time: `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` (`git rev-parse master`).

## 2. The two required re-runs — both PASS, exit 0

```
TMPDIR=/fast/scratch/hyaku/tsukuroi-r38/C1ExecRerun python3 tools/score-storage-arm-r38.py \
  --repo <lane> --revision 52ffd65f868431f021b8615ab281efd87195eac6 \
  --scratch /fast/scratch/hyaku/tsukuroi-r38/C1ExecRerun      → exit 0, 33.1s
… --revision 5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf …     → exit 0, 34.3s
```
Both wrote empty stderr. Records saved (absolute, seat dir):
`.ufo/waves/round-38/w1/C1ExecRerun/rerun-52ffd65.json` (sha256 `994740e1…f1763cd0`) and
`.ufo/waves/round-38/w1/C1ExecRerun/rerun-master.json` (sha256 `5c37c732…55e21032`).

| record | revision | branch_tip | fixtures_matched/expected | live_match | six_planes_all | euid_root | result | exit |
|---|---|---|---|---|---|---|---|---|
| author `after/c1-after-52ffd65.json` | 52ffd65 | 52ffd65 | 10/10 | 1 | 1 | false | PASS | 0 |
| my rerun | 52ffd65 | 5edb6c2 | 10/10 | 1 | 1 | false | PASS | 0 |
| my rerun | 5edb6c2 | 5edb6c2 | 10/10 | 1 | 1 | false | PASS | 0 |

Predicate (`tools/score-storage-arm-r38.py:230`): `fixtures_matched == FIXTURES_EXPECTED and
live_match == 1 and six_planes_all` → true in both re-runs.

## 3. Field-by-field comparison — only informational fields differ

Scripted flatten of both JSON trees (`compare.json`, written from the same records; sha256
`204162c9…8bb090f`):

- author ↔ rerun@52ffd65: `only_in_author=[]`, `only_in_rerun=[]`, **1 value diff**:
  `/branch_tip` `52ffd65 → 5edb6c2`. `branch_tip` is informational only
  (`_revision.py:163-170 branch_tip`, recorded at `score-storage-arm-r38.py:231-233`) and is
  *expected* to advance because master moved after the author run; nothing in the predicate reads it.
- rerun@52ffd65 ↔ rerun@master: **1 value diff**: `/revision` `52ffd65 → 5edb6c2` (the argument).
- author ↔ rerun@master: the same two fields, nothing else.

All 10 fixture entries compare equal on `expected`, `got`, `storage_lines`, `six_planes`,
`census_exit` and `match`; the `live` block compares equal on all six keys
(`expected=(HEALTHY,1,1,0)`, `got=(HEALTHY,1,1,0)`,
`STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`, `six_planes=true`,
`census_exit=2`, `match=true`). Verdict/`predicate`/`counter`/`fixtures_expected` strings match
verbatim.

Live leg cross-checked against the host sysfs myself (read-only):
`/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/error_stats` = five counters, all
`0` → independent expectation HEALTHY/1/1/0, matching both `expected` and `got`. `id -u` = 1000,
so the non-root `euid_root=false` gate holds and F10 (mode-000 fixture) is legitimately credited
(counter `score-storage-arm-r38.py:215-216` refuses to credit it under root).

## 4. Discrimination control — the re-run is not vacuously green

Same counter, base revision from the seat brief (`git merge-base --is-ancestor → yes`):

```
… --revision 8bd001f58bfda29c92d90d2a7a413825c0ca9fcb …  → exit 1
{"revision":"8bd001f5…","fixtures_matched":0,"live_match":0,"six_planes_all":1,"result":"FAIL"}
live: {"expected":["HEALTHY",1,1,0],"got":null,"storage_lines":[],"six_planes":true,"match":false}
```
Saved as `.ufo/waves/round-38/w1/C1ExecRerun/control-base.json` (sha256 `679e756f…27d6c9`). So the
counter separates pre-arm (no `STORAGE` line at all → 0/10 fixtures, live miss) from post-arm
(10/10, live hit) on the same host minutes apart; the PASS is a property of the revision, not of
the environment.

Supporting claim detail — "6 selftest cases" for the arm at 52ffd65: six `case_home='storage-*'`
blocks in `tools/tsukuroi-census.sh:2889, 2893, 2899, 2906, 2913, 2919`. I did **not** run
`--selftest` (out of item C1-8 scope; a sibling seat's scratch dir `C1ExecSelftestTmp` shows it is
covered elsewhere).

## 5. Observed, not a defect: `census_exit == 2` in all 11 legs

Every fixture record and the live record carry `census_exit=2`. That is the census's own rollup
code, not a failure of the storage plane: `tools/tsukuroi-census.sh:3022-3025`
(`HEALTHY) exit 0 ;; DEGRADED) exit 1 ;; BLOCKED) exit 2`). My own hermetic live run of the pinned
census (no `TSUKUROI_BTRFS_SYSFS`) gives `STORAGE … state=HEALTHY filesystems=1 devices=1 nonzero=0`
with rollup `TSUKUROI_CENSUS: BLOCKED (… systemd=BLOCKED …)` — the systemd plane is BLOCKED only
because the counter's child env is stripped (`CHILD_ENV_BASE` at `score-storage-arm-r38.py:59`, no
`DBUS_SESSION_BUS_ADDRESS` → `systemctl --user` unusable). Receipt:
`.ufo/waves/round-38/w1/C1ExecRerun/live-census-planes.txt` (sha256 `92981362…f9dac06f`).

Consistency check: this is exactly the declared "verdict-neutral census arm" — the counter reads
only the single `STORAGE` line (`score-storage-arm-r38.py:164-173`) and never the exit code, so a
BLOCKED systemd/oom plane cannot gate C1 in either direction. Related, worth knowing when reading
`six_planes_all`: it asserts *structure* (exactly 6 `PLANE` lines + 1 `TSUKUROI_CENSUS:` line,
`score-storage-arm-r38.py:173`), not plane health; my live run shows 6 `PLANE` lines. No
implication that the arm's credit is vacuous — the F01–F10 fixtures and the live/expected pair are
what carry the signal, and the base control above demonstrates it.

## 6. Limits of this item

- Not run by me: `tools/score-storage-arm-r38-q82.py` (QUALITY 82 production-path counter). Item
  C1-8 names only the v1 counter; the q82 leg of the pre-seat amendment is another seat's item, so
  this report does **not** attest C1's amended PASS — only that the v1 half reproduces.
- No `unshare`/namespace leg attempted (same reason).
- I did not re-author or edit anything; no counter or census bytes were touched.
- Tooling: nothing installed or upgraded. Scratch `TMPDIR=/fast/scratch/hyaku/tsukuroi-r38/C1ExecRerun`
  (removed after receipts were copied into the seat dir); no `/tmp` evidence used.

## 7. Lane hygiene

`git -C <lane> status --porcelain --untracked-files=no` → empty (no tracked file modified, index and
jj state untouched). All my writes are under `.ufo/waves/round-38/w1/C1ExecRerun/` (untracked, which
already existed as `?? .ufo/waves/round-38/w1/`): `rerun-52ffd65.json`, `rerun-master.json`,
`control-base.json`, `compare.json`, `live-census-planes.txt`, plus this report.

## Proposed text (one line, for the wave report's C1 row)

> C1-8 (independent re-run): counter sha256 `e649bfb3…` = freeze commit = worktree; PASS reproduced
> at 52ffd65 (`10/10`, live 1, six_planes 1, exit 0) and at master 5edb6c2 (same), byte-identical
> census (`8e0084f6…`) at both; author receipt differs only in `branch_tip`; base 8bd001f5 FAILs
> (`0/10`, live 0, exit 1).
