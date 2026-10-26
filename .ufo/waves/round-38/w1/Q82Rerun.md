VERDICT: supports

# Seat Q82Rerun — Item C1-17 (amendment counter re-run)

## Claim under test
Pre-seat amendment (commit 9c9bb6477951b3a52ac49ed83db4395765dfcf1a) requires
`tools/score-storage-arm-r38-q82.py` (sha256 a183ff58...) to PASS on the C1 arm:
`ns_views_matched == VIEWS (3)` and `ns_available == 1`, where the census runs with no
override inside `unshare -rm` with a random tree bind-mounted over `/sys/fs/btrfs`.

## 1. Counter digest
```
$ sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-storage-arm-r38-q82.py
a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3  .../tools/score-storage-arm-r38-q82.py
```
Matches the expected digest exactly (re-checked after the runs; identical).
Relevant source lines confirming the predicate and seed channel:
- `tools/score-storage-arm-r38-q82.py:33` — `VIEWS = 3`
- `tools/score-storage-arm-r38-q82.py:110` — `seed = os.urandom(16).hex()` (new seed per run)
- `tools/score-storage-arm-r38-q82.py:129` — `verdict = matched == VIEWS and available == 1`
- `tools/score-storage-arm-r38-q82.py:118` — bind: `mount --bind "$1" /sys/fs/btrfs`

Revision bound by the mandated command: `git -C .../tsukuroi-shokunin rev-parse master`
= `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` (branch_tip also 5edb6c2...).
`git merge-base --is-ancestor 52ffd65f868431f021b8615ab281efd87195eac6 master` → yes,
and `git show master:tools/tsukuroi-census.sh` contains 10 matches for
`probe_storage_arm|STORAGE btrfs-device-stats` — the arm is present at the scored revision.

## 2. Three runs (each a fresh `os.urandom` seed)
Command form (exactly as assigned; `--scratch` = `/fast/scratch/hyaku/tsukuroi-r38/Q82Rerun`,
`TMPDIR` set to the same):

| run | seed | ns_views_matched | ns_available | result | exit |
|-----|------|------------------|--------------|--------|------|
| 1 | `b0b54ea4e081cb8c6c4e53e6e16d3095` | 3/3 | 1 | PASS | 0 |
| 2 | `570b6920476906ab9837ef018b2ecbeb` | 3/3 | 1 | PASS | 0 |
| 3 | `f5cfcafbffdc164b2a5f6628a9348315` | 3/3 | 1 | PASS | 0 |

Seeds are pairwise distinct (3 unique). No view mismatch in any run:

- run1: view0 `zero` exp `[HEALTHY,2,4,0]` got identical; view1 `nonzero` exp `[DEGRADED,3,6,11]` got identical; view2 `any` exp `[DEGRADED,2,2,9]` got identical; `six_planes=True` for all three.
- run2: view0 `zero` `[HEALTHY,1,2,0]`; view1 `nonzero` `[DEGRADED,2,4,6]`; view2 `any` `[DEGRADED,3,8,12]`; all equal, `six_planes=True`.
- run3: view0 `zero` `[HEALTHY,3,7,0]`; view1 `nonzero` `[DEGRADED,2,3,6]`; view2 `any` `[DEGRADED,2,3,9]`; all equal, `six_planes=True`.

Per-run `stderr` empty (0 bytes each). Fixture fsids differ per view and per run, so the
three runs exercised 9 independent random trees (e.g. run1: `42bc4318`, `69cd1ad4`,
`b82f33fe`, `80893bc7`, `8c1c815d`; run3: `14af3839`, `adb645a6`, `210ccb8e`, `797f1e59`).

Receipts: `.ufo/waves/round-38/w1/Q82Rerun/run{1,2,3}.json`
sha256 `89666e15…`, `ab3b2643…`, `398626f6…` respectively.

## 3. Host `/sys/fs/btrfs` leak check (after every run)
Before run 1 and after each of the three runs (and after the extra inspection run), the host
listed exactly the real fsid:
```
$ ls /sys/fs/btrfs/      # before run1, after run1, after run2, after run3, final
1d02a454-c549-4a35-b567-89d60902af8e
features
```
Host device view intact: `ls /sys/fs/btrfs/1d02a454-.../devinfo/` → `1`, and its
`error_stats` still reads `write_errs 0 … generation_errs 0` — i.e. the real single-device
root, never a fixture tree. No fixture fsid from any run appeared on the host, and the bind
mount did not escape the namespace.

## 4. Observation (not a defect against the declared predicate)
Every view reports `census_exit == 2`. Traced to the rollup mapping
`tools/tsukuroi-census.sh:3022-3025` (`HEALTHY→0, DEGRADED→1, BLOCKED→2`): the overall
rollup inside `unshare -rm` is BLOCKED by an unrelated plane:
`.ufo/waves/round-38/w1/Q82Rerun/ns-full.txt:5` →
`PLANE journal: BLOCKED (boot target probe unusable rc=1 [Failed to connect to system scope bus via local transport: Operation not permitt…])`
and `ns-full.txt:11` → `TSUKUROI_CENSUS: BLOCKED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=BLOCKED update-safety=DEGRADED oom=DEGRADED)`.
The storage plane itself is exact against the fixture in the same run:
`ns-full.txt:10` → `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`.
So exit 2 is a namespace-environment artefact of the journal plane, and the q82 predicate is
deliberately plane-scoped (`ns_views_matched`, `ns_available`), not rollup-scoped; the
declared predicate is met without relying on the exit code. Recorded for the reviewers'
understanding; no action taken.

## 5. Scoring context
`controls/controls-q82.jsonl` (already scored, read for cross-reference) shows the expected
discrimination, consistent with these runs: `C1-real-arm` q82 `ns_views_matched:3` PASS;
`C1-fixture-gated` q82 `0` FAIL; `C1-cached-live` q82 `1` FAIL. My three runs reproduce the
`C1-real-arm` outcome on three new seeds.

## 6. Constraints honoured
- Lane read-only: no tracked file created/modified/deleted; no git/jj mutation. `git status
  --porcelain` shows only pre-existing untracked wave artefacts (`?? .ufo/waves/round-38/…`),
  nothing introduced by this seat.
- Host untouched: no sudo, no package/service/sysfs/hook/counter-reset; the only privileged
  action was the in-namespace `mount --bind` performed by the counter itself under
  `unshare -rm`, verified not to leak.
- Scratch confined to `/fast/scratch/hyaku/tsukuroi-r38/Q82Rerun` (removed at end); receipts
  copied into this seat dir first.
- No agents spawned, no `agent://all`.
- No tool installs were needed (python3 3.14.8, util-linux 2.42.4 `unshare` preinstalled).

## 7. Not done
- Did not run the v1 counter, the 6-case census selftest, or mutate an arm to re-derive the
  negative controls (other seats / already-scored controls cover those). This seat measured
  only the three repeat runs and the leak check it was assigned.
- Did not judge whether the plane-scoped predicate is the right design; only recorded the
  exit-2 cause so the declaration's wording can be read correctly.
