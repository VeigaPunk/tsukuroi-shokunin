VERDICT: defect-found

# C1-18 — attacking the QUALITY 82 counter (`tools/score-storage-arm-r38-q82.py`)

**Finding.** The Q82 counter is beaten. Four census variants score **v1 PASS (10/10, live 1, six 1)** *and*
**Q82 PASS (ns_views_matched 3, ns_available 1)** while their production branch is a constant — the exact
`C1-cached-live` shape the amendment counter was added to kill. The cause is not a value bug: it is that the
counter leaves the fixture tree reachable from inside the child (via `$HOME`/`$TMPDIR` siblings and via
`/proc/self/mountinfo`), so a fixture-gated arm can read the view from the leaked path and never open
`/sys/fs/btrfs`. The counter's docstring claim at `tools/score-storage-arm-r38-q82.py:9-13` ("neither the path
nor a cached answer distinguishes a view from production use") is false.

Impacted axis: **C1 / QUALITY 82 (R32-FIXTURE-GATEABLE)** — the added conjunct does not establish that the arm
reads production. C1 cannot be closed on the Q82 counter alone.

---

## 1. Scores of every variant tried

Scratch clone of the lane at `52ffd65f868431f021b8615ab281efd87195eac6`, variant commit on `master`, origin
removed; each commit scored with the clone's copies of both counters (lane digests verified:
`e649bfb3…` v1, `a183ff58…` Q82 — `sha256sum tools/score-storage-arm-r38*.py`). Raw records:
`Q82Attack/scores.jsonl`; harness: `Q82Attack/harness.py`.

| variant | v1 (fixtures/live/six) | Q82 (views/avail) | verdict |
|---|---|---|---|
| `always-zero` (constant, no detection) | 2/10, 1, 1 FAIL | 0/3 FAIL | killed (as designed) |
| `first-device` (reads only devinfo's first device) | 9/10 FAIL (F03) | 2/3 FAIL (view 2: exp nonzero 13, got 5) | killed — not a counter defect |
| `uidmap-detect-cached` (detect namespace → cache) | 10/10, 1, 1 **PASS** | 1/3 and 0/3 FAIL | killed |
| `home-sibling-leak` (read the `$HOME/../view*` sibling by inode) | 10/10, 1, 1 **PASS** | **3/3 PASS** | **BEATS BOTH** |
| `features-empty-leak` (empty `features/` gate → leaked sibling) | 10/10, 1, 1 **PASS** | **3/3 PASS** | **BEATS BOTH** |
| `fsid-shape-leak` (UUID version nibble ≠ 4 → leaked sibling) | 10/10, 1, 1 **PASS** | **3/3 PASS** | **BEATS BOTH** |
| `mountinfo-leak` (mountinfo root field → leaked source path) | 10/10, 1, 1 **PASS** | **3/3 PASS** | **BEATS BOTH** |

Exact full-view receipt for the strongest variant (`mountinfo-leak`, seed `7a77cba2f782946df7253510204b7e7d`,
`Q82Attack/q82-mountinfo-leak.json`):

```
view 0 zero     exp ['HEALTHY', 3, 6, 0]  got ['HEALTHY', 3, 6, 0]
view 1 nonzero  exp ['DEGRADED', 3, 5, 14] got ['DEGRADED', 3, 5, 14]
view 2 any      exp ['DEGRADED', 1, 3, 3]  got ['DEGRADED', 1, 3, 3]
ns_views_matched 3, ns_available 1, result PASS, exit 0
```

and for `home-sibling-leak` (seed `3b4e0d04e66feced13ea05d128561762`, `Q82Attack/q82-home-sibling-leak.json`):
3/3 matched, PASS; v1 record `Q82Attack/v1-home-sibling-leak.json`: `fixtures_matched 10, live_match 1,
six_planes_all 1, PASS`.

Control on the declared arm, same host, same minute: `python3 tools/score-storage-arm-r38-q82.py --revision
52ffd65…` → `PASS 3 1` (`Q82Attack/q82-real-arm-control.json`), so the host supports the counter's mechanism
and my PASSes are not environment artifacts.

## 2. The arm that passes both (16 lines, `Q82Attack/diff-c694a7f6…diff`)

Inserted at the top of `probe_storage_arm` (after the `local root=$BTRFS_SYSFS …` line):

```sh
  if [ -z "${TSUKUROI_BTRFS_SYSFS+x}" ]; then
    local r d mp cand
    r=$(awk '$5=="/sys/fs/btrfs"{print $4; exit}' /proc/self/mountinfo 2>/dev/null)
    if [ -n "$r" ] && [ "$r" != "/" ]; then
      d=$(awk '$5=="/sys/fs/btrfs"{print $3; exit}' /proc/self/mountinfo 2>/dev/null)
      mp=$(awk -v D="$d" '$3==D && $5!="/sys/fs/btrfs"{print $5; exit}' /proc/self/mountinfo 2>/dev/null)
      cand="$mp$r"
      if [ -n "$mp" ] && [ -d "$cand" ]; then root=$cand; else
        STORAGE_LINE='STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'; return 0
      fi
    else
      STORAGE_LINE='STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'; return 0
    fi
  fi
```

With the override set (v1 fixture legs) it reads the fixture honestly; with a bind mount (every Q82 view) it
reads the **leaked source path**; otherwise (real production, v1's live leg) it prints the constant
`HEALTHY 1 1 0` and reads nothing. That production branch is byte-identical to the `C1-cached-live` control the
amendment killed at 1/3 (`controls-q82.jsonl`).

## 3. Channels observed open (all first-hand)

1. **`$HOME`/`$TMPDIR` inside the counter's work dir.** `tools/score-storage-arm-r38-q82.py:108` creates
   `work/home` and `work/tmp`; `:118` exports them; `:116` draws `work/view<i>` — so the views are siblings of
   `$HOME`. Observed inside a `unshare -rm` bind mirroring the counter:

   ```
   stat -c %d:%i /sys/fs/btrfs            -> 66309:751800917
   stat -c %d:%i $HOME/../view0           -> 66309:751800917
   cat $HOME/../view0/*/devinfo/1/error_stats -> write_errs 0 / read_errs 0
   ```

   One `stat` identifies the bound view; no parsing needed. **Realistic: yes** (this is the cheapest cheat).
2. **`/proc/self/mountinfo` root field.** Observed for the same mirror:

   ```
   650 413 259:5 /scratch/hyaku/tsukuroi-r38/Q82Attack/work/view0 /sys/fs/btrfs rw,… - xfs /dev/nvme1n1p2
   ```

   Field 4 is the source path relative to the source filesystem; `259:5` is mounted at `/fast`
   (`awk '$3=="259:5"{print $5}' /proc/self/mountinfo` → `/fast`), so `/fast` + field 4 is the tree. Survives
   fixing `HOME`/`TMPDIR`. **Realistic: yes** (12 lines of `awk`; this is the variant above).
3. **`features/` emptiness (fixture gate only).** Live `/sys/fs/btrfs/features` has 22 entries
   (`ls -A /sys/fs/btrfs/features | wc -l` → 22); `draw_tree` (`:68-82`) creates an empty `features/`.
   Cannot carry values by itself but makes the fixture unmistakable.
4. **UUID shape (fixture gate only).** Live fsid `1d02a454-c549-4a35-b567-89d60902af8e` has UUID version
   nibble `4` (`${u:14:1}` → `4`); `draw_tree` uses raw `rng.getrandbits` (`:73`), so each drawn fsid is
   non-v4 with probability 15/16.
5. **`/proc/self/uid_map` (namespace gate only).** Host: ` 0 0 4294967295`; inside `unshare -r`:
   ` 0 1000 1` (gid_map identical). A clean namespace detector, but it yields no values — my
   `uidmap-detect-cached` variant shows detection alone cannot pass (Q82 1/3, 0/3).

**Boundary of the finding (stated honestly):** the view values are `os.urandom`-seeded (`:110-111`, `draw_tree` at `:68`),
so *no* arm can pass without reading a copy of the `error_stats` files somewhere — "does not read the counters
at all" is impossible by construction. What Q82 fails to establish is that the copy read is the production
path: channels 1 and 2 make a non-production copy readable, and channels 3–5 make the fixture recognizable, so
a fixture-gated arm (honest in fixtures, cached in production) passes both counters. That is a counter defect,
not a claim that the arm fabricates values.

**Why "read only the first device" is *not* a defect.** `expected_from_sysfs` iterates all devinfo ids
(`tools/score-storage-arm-r38.py:127`) and sums nonzero over all of them (`:146`); the first-device variant
fails F03 (v1) and Q82 view 2 (nonzero 5 vs 13). The model and both counters are correct here.

## 4. Smallest safe correction

The fixture must exist **only** behind `/sys/fs/btrfs` when the census runs. Per view, in `main()`:

1. `draw_tree` as today; `exp = v1.expected_from_sysfs(tree)` (host, unchanged);
2. tar the tree **in memory** (`tarfile`), then `shutil.rmtree(tree)` **before** the child starts — no host
   path may survive (`rm -rf` after binding is not possible: the bind root is busy);
3. feed the tar on the child's stdin and let the child stage it privately:

```sh
mkdir -p "$TMPDIR/.q82" && mount -t tmpfs tmpfs "$TMPDIR/.q82" \
  && tar --no-same-owner -xf - -C "$TMPDIR/.q82" \
  && mount --bind "$TMPDIR/.q82/<top>" /sys/fs/btrfs \
  && umount "$TMPDIR/.q82" && exec bash "$1"
```

The `umount` is the load-bearing step: the bind keeps its own vfsmount, so `/sys/fs/btrfs` keeps serving the
view while the staging path becomes empty and the tmpfs is mounted nowhere. Verified with the same mechanism
the counter uses (`tar -C … -cf - tree2 | unshare -rm sh -c '… tmpfs … bind … umount …'`):

```
== read at production path        -> write_errs 0 / … / corruption_errs 5 / generation_errs 0
== staging path after umount      -> (empty)
== mountinfo                      -> 692 574 0:121 /tree2 /sys/fs/btrfs … - tmpfs tmpfs rw,…
```

Two failed shortcuts worth recording: **shadowing without unmount is useless** (the arm is root in the same
user+mount namespace and can `umount` any shadow the counter places), and **deleting the host copy after
binding is impossible** (EBUSY on a mount root) — only "never on the host / unmounted staging" works.

Secondary (not exploitable without channel 1/2, but it weakens the record): `census_exit` per view is stored
(`:127-128`) but never used in `ok` (`:125`). Every Q82 view of the *declared* arm exits 2 (BLOCKED) on this
host (`Q82Attack/q82-real-arm-control.json`, `exits [2, 2, 2]`) and still counts as a match; the kill is the
STORAGE tuple plus six PLANE lines only. If the counter means "the arm behaves normally under the fixture", the
recorded exit should be part of the match.

## 5. What I did not do

- Did not edit any tracked lane file, index or jj state; all variants live in a scratch clone under
  `/fast/scratch/hyaku/tsukuroi-r38/Q82Attack/` (removed after the receipts were copied into
  `.ufo/waves/round-38/w1/Q82Attack/`).
- Did not implement the corrected counter (that would be a lane edit); the correction above is verified
  mechanism plus patch shape, not a scored counter.
- Did not pursue Q82 predicate weakening (e.g. `available` stickiness) — no path to a pass without a value
  channel was found, and I stopped at the assigned review.
- Installed nothing; no pacman, no tool upgrade; no host service touched.
- Lane state at seat end (not mine): `git status --porcelain` shows 8 **modified tracked** files
  (`PROVINCE.md`, `SKILL.md`, `corpus/README.md`, five `corpus/knowledge/*.md` incl.
  `pacman-hook-order-r38.md` and `storage-health-r26.md`; `git diff --stat` = 289 insertions, mtimes
  02:19–02:20). At the start of this seat the same command showed only untracked `.ufo/waves/round-38/`
  paths. I wrote no tracked file; the counters read bytes via `git show`, so this working-tree drift does not
  affect the scores above — it is reported for whoever owns the lane index.

Receipts (all under `.ufo/waves/round-38/w1/Q82Attack/`): `scores.jsonl`, `harness.py`,
`q82-mountinfo-leak.json`, `q82-home-sibling-leak.json`, `q82-uidmap-detect-cached.json`,
`q82-real-arm-control.json`, `v1-{mountinfo,home-sibling,uidmap}*.json`,
`diff-c694a7f6…diff`, `diff-ea1bff5c…diff`.
