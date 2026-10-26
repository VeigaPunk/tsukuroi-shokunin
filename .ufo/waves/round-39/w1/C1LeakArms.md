VERDICT: supports

# C1-2 — the four round-38 Q82 leak arms as should-fail controls on the round-39 counter

All four arms ported verbatim onto the census at `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` and scored with the
frozen round-39 counter (`tools/score-storage-hidden-r39.py`, sha256
`75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`, verified inside the scratch clone before the
first run) **FAIL**. None PASSes. Every arm reaches the constant production branch
`STORAGE … state=HEALTHY filesystems=1 devices=1 nonzero=0`; no arm reads a view value, which is exactly what the
round-39 tmpfs-in-namespace design intends.

## 1. Scores (`scores.jsonl`, raw counter output per arm in `<arm>.counter.json`)

| arm | variant commit | hidden | views | fixtures | live | six | result |
|---|---|---|---|---|---|---|---|
| `home-sibling-leak` | `63450d0ee2da164ae4af796c5b699cfa7dfdac78` | 0/2 | **0/3** | 5/5 | 1 | 1 | **FAIL** exit 1 |
| `features-empty-leak` | `85d729a25551e285891154ac79cb1a5a8e278be2` | 0/2 | **1/3** | 5/5 | 1 | 1 | **FAIL** exit 1 |
| `fsid-shape-leak` | `ee1a84e4ed0463b58be8d7652dfba2fef61aa663` | 0/2 | **0/3** | 5/5 | 1 | 1 | **FAIL** exit 1 |
| `mountinfo-leak` | `cd77e2d1af41f0ed9c0ea82f37321e67a9efd30d` | 0/2 | **0/3** | 5/5 | 1 | 1 | **FAIL** exit 1 |

Patches: `home-sibling-leak.diff`, `features-empty-leak.diff`, `fsid-shape-leak.diff`, `mountinfo-leak.diff`
(each inserts at the top of `probe_storage_arm`, anchor line
`local root=$BTRFS_SYSFS fsd dev f k v extra fs8 fsn=0 devn=0 nz=0 blocked=0 nd seen nk dnz ddet detail=''`,
census `tools/tsukuroi-census.sh:1863` at the arm commit — diff hunk header `@@ -1861,6 +1861,22 @@`).
Harness: `harness.py` (scratch clone of the lane, `origin` removed, toplevel asserted, fixture identity, variant
committed on `master`, `--repo <clone> --revision <sha> --scratch <seat>/s`).

Every arm's view and hidden legs print the same constant; e.g. `mountinfo-leak` (seed `03df91c3c99e705b08440d8a80d1364c`):

```
view 0 zero     exp ['HEALTHY', 1, 3, 0]   got ['HEALTHY', 1, 1, 0]   match False
view 1 nonzero  exp ['DEGRADED', 3, 8, 22] got ['HEALTHY', 1, 1, 0]   match False
view 2 any      exp ['DEGRADED', 3, 4, 7]  got ['HEALTHY', 1, 1, 0]   match False
H1-hidden-empty  exp BLOCKED…mounts:btrfs-without-sysfs  got HEALTHY 1/1/0  match False
H2-hidden-absent exp BLOCKED…mounts:btrfs-without-sysfs  got HEALTHY 1/1/0  match False
```

`features-empty-leak`'s single view match is a **value coincidence, not a leak**: its `zero` view drew exactly
one fsid, one device and all-zero counters, i.e. the tuple the constant prints
(`exp ['HEALTHY', 1, 1, 0]` vs the constant). Views 1 and 2 missed. Since the predicate also needs
`hidden_matched == 2` (`tools/score-storage-hidden-r39.py:28,265`) and a constant branch can never print
`BLOCKED`, no seed or coincidence can carry any of these arms to PASS.

## 2. Why each channel is shut (first-hand observation, `channel-observation.txt`)

Same mechanism as the counter's `ns_run` (`tools/score-storage-hidden-r39.py:195-198`: `mount -t tmpfs tsk "$1"`
then a builder fed the spec on stdin), probed from inside the child:

```
== mountinfo /sys/fs/btrfs
833 809 0:121 / /sys/fs/btrfs rw,relatime - tmpfs tsk rw,uid=1000,gid=1000,inode64,huge=advise
== field4 (root)   /
== siblings of HOME:  home  tmp
== any host path named view* under HOME: none
== features entries under view:  no_holes            (real views: five files, :94)
== inode of /sys/fs/btrfs: 119:1
```

- **home-sibling-leak** — `$HOME/../view*` no longer exists: `$HOME` is `<work>/home` and its parent holds only
  `home`, `tmp` (and the script/`fx`), never a view. 0/3.
- **features-empty-leak** — `draw_view` always writes the five feature files
  (`tools/score-storage-hidden-r39.py:93-94`), so the empty-`features/` fixture tell is gone. 0 leak matches.
- **fsid-shape-leak** — the generator formats the UUID version nibble explicitly (`'%08x-%04x-4%03x-…'`,
  `tools/score-storage-hidden-r39.py:98`), so no drawn fsid is non-v4 and the tell no longer fires. 0/3.
- **mountinfo-leak** — the view is a tmpfs mounted *directly* at `/sys/fs/btrfs` with root field `/`, so there is
  no bind source to reconstruct (`[ "$r" != "/" ]` is false). 0/3.

Both Q82 value channels from round 38 (home sibling by inode, mountinfo bind source) are closed by construction at
this revision; the two gate-only channels (empty features, non-v4 fsid) no longer correlate with a fixture.

## 3. Positive control on the same host and scratch (not an environment artifact)

`declared-arm-control.json`: the declared census at the arm commit, run from the same clone and scratch minutes
apart from the variants —

```
PASS exit 0  hidden_matched 2  views_matched 3  fixtures_matched 5  live_match 1  six_planes_all 1
revision 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82
```

So the counter can PASS here; the four FAILs are attributable to the arms.

## 4. Two secondary observations (not claimed as defects)

1. **`live_match 1` for a constant arm is not evidence of reading.** This host's live tuple is
   `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/error_stats` all zero, one device → expected
   `HEALTHY 1 1 0`, which is precisely the arms' constant (verified: the control's `live.got` is that same line).
   On a host with any nonzero counter the live leg would also fail these arms. Harmless because the predicate
   also requires `hidden_matched 2` and `views_matched 3`.
2. **Untested residual channel [INFERENCE, not exercised]:** inside `unshare -r` the child's uid 0 maps to the
   invoking uid (`uid_map` observed ` 0 1000 1`), so a same-uid arm could in principle read the *parent* counter
   process's memory/argv via `/proc`. I did not build such an arm — it is outside the four assigned ports and no
   host path holds the view tree.

## 5. What I did not do

- Did not edit, create or delete any tracked lane file; no `git add/commit/stash/checkout/reset/push` and no jj
  command ran in the lane. The clone is a `--shared` scratch clone with `origin` removed; variants live only in
  `/fast/scratch/hyaku/tsukuroi-r39/C1LeakArms/`, removed after the receipts were copied here
  (`rm -rf` executed; the scratch parent now holds only sibling seats' dirs).
- Did not build any arm beyond the four assigned ports; did not weaken or re-tune the counter; did not implement a
  corrected arm.
- Did not run build/lint/tests or the census selftest; did not touch the host (no pacman, no service, no mount
  outside `unshare -rm`, no sysfs edit, no sudo). Installed nothing — no tool/version/channel to record.
- Lane tree state at seat end (not mine, present before this seat started): `git status --porcelain` shows
  `M PROVINCE.md`, `M SKILL.md` plus untracked `.ufo/waves/round-39/w1*` paths. My only writes are this report
  and `.ufo/waves/round-39/w1/C1LeakArms/`.

Receipts (`.ufo/waves/round-39/w1/C1LeakArms/`): `scores.jsonl`, `harness.py`, four `*.diff`, four
`*.counter.json` + `*.counter.err`, `declared-arm-control.json`, `channel-observation.txt`.
