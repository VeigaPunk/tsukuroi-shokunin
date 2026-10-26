VERDICT: defect-found

# C1-15 — "an absent btrfs sysfs root reads HEALTHY 0/0/0" is a false universal

Item: attack the frozen rule at `tools/tsukuroi-census.sh:363` — "An absent TSUKUROI_BTRFS_SYSFS means
no btrfs filesystem is mounted: HEALTHY 0/0/0" — fixture F06 of the C1 counter
(`tools/score-storage-arm-r38.py:82`, `:98`).

Finding in one sentence: **the rule holds only while the reader can see sysfs.** A mounted btrfs
implies the btrfs sysfs kset exists (kernel init order, below), so an absent root under an otherwise
btrfs-capable kernel is an *observability* failure; the arm renders it as a HEALTHY all-clear on the
one plane whose purpose is detecting silent corruption. The frozen *predicate* is not broken — F06 is
satisfiable and stable, v1's live arm is blind by construction — so this is a defect of the claim's
meaning and of the coverage claim built on it, not of the scoring object.

Receipts (kept): `.ufo/waves/round-38/w1/C1CritAbsentRoot/{matrix.txt,env.txt,mutant.diff,sources.txt}`.
Scratch `/fast/scratch/hyaku/tsukuroi-r38/C1CritAbsentRoot/` removed after copying; no `/tmp` evidence.

## 1. The counterexample, executed twice against the frozen census bytes

Census bytes measured: `git show 52ffd65f868431f021b8615ab281efd87195eac6:tools/tsukuroi-census.sh`,
sha256 `8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c`, byte-identical to HEAD
(`5edb6c2`) — `env.txt:7-9`. Host: `7.2.11-arch1-1`, root `/dev/mapper/root[/@]` fstype btrfs,
`/sys/fs/btrfs` present with `1d02a454-… features` (`env.txt:2-6`).

L2 — a mount over the path (also the technique the QUALITY-82 counter itself uses):

```
unshare -rm --propagation private → mount --bind <empty dir> /sys/fs/btrfs
sysfs root present, entries=0
btrfs mounts here=4
findmnt -n -o TARGET -t btrfs → / ├─/home ├─/var/cache/pacman/pkg └─/var/log
STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0
```

L3 — sysfs not visible at all (plain `chroot`, `TemporaryFileSystem=/sys`, container without `/sys`):

```
mount --bind <empty dir> /sys     →  sysfs root ABSENT
proc/filesystems has btrfs=1       btrfs mounts here=4
STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0
TSUKUROI_BTRFS_SYSFS=<typo path>   →  same line
```

(`matrix.txt:1-20`.) In both cases the census asserts "no btrfs filesystem is mounted" **in the very
mount namespace it reads**, while `findmnt` and `awk '$3=="btrfs"' /proc/self/mounts` count four. The
third run is the operator footgun: `TSUKUROI_BTRFS_SYSFS` is a documented live knob
(`tools/tsukuroi-census.sh:392`), so a typo buys an all-clear.

The same line also collapses two different world states: F06 (root absent) and a *legitimate*
"btrfs loaded, nothing mounted" host (root present with only `features/`) both print
`state=HEALTHY filesystems=0 devices=0 nonzero=0` — L2 already shows the frozen census printing that
exact line for an existing empty root. And no fixture pins the legitimate branch: `FIXTURES` has
F06 = absent root, F07 = `U1/features` (1 fs, BLOCKED), F08 = `features/` + `not-a-uuid` + `U1`
(1 fs, HEALTHY) — `tools/score-storage-arm-r38.py:80-90`. So `filesystems=0` is one string for
"nothing mounted", "cannot see", and "wrong path".

## 2. Why absence cannot mean "nothing mounted" — kernel init order (pinned sources, read 2026-10-26)

- `fs/btrfs/sysfs.c:2657-2661` (v7.2, raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c,
  sha256 `ce146120…` — the same digest `corpus/SOURCES.md` S133 pins, so these are the lane's bytes):
  `int __init btrfs_init_sysfs(void)` / `btrfs_kset = kset_create_and_add("btrfs", NULL, fs_kobj);`
  and `:2666` `sysfs_create_group(&btrfs_kset->kobj, &btrfs_feature_attr_group);` — the kset and
  `features/` are created at btrfs init, independent of any mount.
- `fs/btrfs/super.c:2641` `{ .init_func = btrfs_init_sysfs, .exit_func = btrfs_exit_sysfs, }` inside
  `mod_init_seq`, and `:2732-2740` `init_btrfs_fs()` runs each entry and aborts on failure. A btrfs
  mount is therefore impossible before the kset exists ⇒ **btrfs mounted ⟹ the kobject exists**.

So every "absent while mounted" case is reader-side or build-side:

1. sysfs not mounted in the reader's namespace/chroot (L3). `sysfs(5)` (Linux man-pages 6.19, page
   date 2026-02-08): "The sysfs filesystem is commonly mounted at `/sys`. Typically, it is mounted
   automatically by the system, but it can also be mounted manually".
2. sysfs mounted at a path other than `/sys` (same sentence; the default path is then empty).
3. a mount over `/sys` or `/sys/fs/btrfs` (L2) — including `tools/score-storage-arm-r38-q82.py:9-10`
   and `:119-120`, which bind a fabricated tree over the production path by design.
4. `TSUKUROI_BTRFS_SYSFS` set to a nonexistent path (L3, second run).
5. unusual kernel with `CONFIG_SYSFS=n`: `fs/btrfs/Kconfig:3-19` lists the whole depends/select set
   (`PAGE_SIZE_LESS_THAN_256KB`, CRC32, ZSTD, …) with **no SYSFS dependency**, and
   `include/linux/sysfs.h:397/503` stub the `sysfs_*` calls in that build — btrfs mounts, no sysfs
   tree exists at all, F06-shaped output for a mounted filesystem.

## 3. Scope asymmetry — why the cross-check must be one-sided (not a count equality)

- sysfs is a global kobject view: `sysfs(5)` — "(More precisely, the files and directories in sysfs
  provide a view of the kobject structures defined internally within the kernel.)"
- `/proc/self/mounts` is namespace-scoped: `proc_pid_mounts(5)` (same release) — "This file lists all
  the filesystems currently mounted in the process's mount namespace".
⇒ `filesystems=N` from sysfs is *not* evidence of N mounts *here* (a container with a private mount
namespace sees the host's fsid dirs and no btrfs mount — [INFERENCE], not executed). The sound,
cheap check is existential only in the hidden direction: `filesystems == 0` while this namespace has
btrfs mounts ⇒ BLOCKED. A count-equality check would be wrong *and* would break the q82 arm, whose
`draw_tree` always fabricates 1-3 filesystems (`tools/score-storage-arm-r38-q82.py:68`). Measured:
the one-sided rule leaves a q82-shaped forged tree at `DEGRADED filesystems=1` (`matrix.txt`, M9).

## 4. What is *not* broken (so the fix is scoped)

- F06 is internally consistent with the arm and satisfiable; nothing here falsifies
  `fixtures_matched == 10 and live_match == 1 and six_planes_all == 1`.
- v1's live arm cannot catch this: `tools/score-storage-arm-r38.py:223-227` compares the census's
  STORAGE line with `expected_from_sysfs(LIVE_SYSFS)` — both sides read the same sysfs, so both go
  blind together.
- q82 proves only that the arm reads the tree it is handed; it inherits the same blindness by
  construction (it *is* a deliberate hide).
- Provenance nit (same item's family): the counter docstring attributes the absence rule to
  "SH1/SH2 of corpus/knowledge/storage-health-r26.md, S128/S133" (`tools/score-storage-arm-r38.py:18-20`).
  Those rows do not carry it: S128 = device-stats counters, S133 = `error_stats` content
  (`corpus/SOURCES.md:134,139` teach cells), and `corpus/knowledge/storage-health-r26.md` has no
  absence statement (its only "absent" is line 59, `/var/lib/btrfs`). The rule is the arm author's
  inference from sysfs semantics and should be labelled so.

## 5. Smallest safe correction (tiered)

**T1 — this round, identity-preserving (recommended).** Do **not** edit `tools/tsukuroi-census.sh`:
its sha256 `8e0084f6…` is the object `c1-after-52ffd65.json` is bound to, so even a comment changes the
measured identity mid-wave. Record the limit instead, as a new post-seat section (precedent: commit
`9c9bb6477951b3a52ac49ed83db4395765dfcf1a`, "Round 38 — pre-seat amendment"), exact text:

> **Round 38 — post-seat recorded limits, C1 (C1CritAbsentRoot).** The frozen rule "an absent
> `TSUKUROI_BTRFS_SYSFS` means no btrfs filesystem is mounted: HEALTHY 0/0/0"
> (`tools/tsukuroi-census.sh:363`) holds only while the reader can see sysfs. Measured: with an empty
> tree bound over `/sys/fs/btrfs`, or over `/sys`, the frozen census prints
> `STORAGE … state=HEALTHY filesystems=0 devices=0 nonzero=0` while `findmnt -n -o TARGET -t btrfs`
> lists four btrfs mounts in the same namespace (`.ufo/waves/round-38/w1/C1CritAbsentRoot/matrix.txt`).
> `btrfs_init_sysfs()` creates the kset before any mount can exist (`fs/btrfs/sysfs.c:2657-2666`,
> `fs/btrfs/super.c:2641`), so an absent root under a `/proc/filesystems` that names btrfs is an
> observability failure, not an empty host. Until a v3 counter adds the cross-check
> (`w1/C1CritAbsentRoot/mutant.diff`), read the STORAGE line only together with
> `grep -w btrfs /proc/filesystems` and `findmnt -n -t btrfs`; an all-clear taken from a chroot or a
> masked `/sys` is not evidence. F06 remains the frozen fixture: "no btrfs anywhere".
> Provenance: the counter docstring's SH1/SH2/S128/S133 attribution of this rule is withdrawn — those
> rows cover the counters and `error_stats`, not kobject presence.

**T2 — next declaration (needs a re-freeze, cannot land now).** The 20-line patch in `mutant.diff`,
measured on the frozen census plus two seams:

```sh
BTRFS_FILESYSTEMS=${TSUKUROI_BTRFS_FILESYSTEMS:-/proc/filesystems}
PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}
btrfs_kernel_state() { # 0 has btrfs, 1 readable without btrfs, 2 unreadable
  if [ ! -r "$BTRFS_FILESYSTEMS" ]; then printf 2
  elif grep -qw btrfs "$BTRFS_FILESYSTEMS"; then printf 0
  else printf 1; fi
}
btrfs_mounts_n() { [ -r "$PROC_MOUNTS" ] || { printf -- -1; return 0; }; awk '$3 == "btrfs"' "$PROC_MOUNTS" | wc -l; }
# in probe_storage_arm, after the scan:
  elif cases=$(btrfs_kernel_state); [ "$cases" != 1 ]; then blocked=1; detail+='sysfs-unseen,'
  fi
  local nmounts; nmounts=$(btrfs_mounts_n)
  if [ "$fsn" -eq 0 ] && [ "$nmounts" -gt 0 ]; then blocked=1; detail+="mounts-not-in-sysfs=$nmounts,"
  fi
```

Measured behaviour (`matrix.txt:22-40`): live host unchanged (`HEALTHY filesystems=1`); L2 →
`BLOCKED … detail=mounts-not-in-sysfs=4`; L3 → `BLOCKED … detail=sysfs-unseen,mounts-not-in-sysfs=4`;
F06 semantics preserved when both seams point at btrfs-free fixtures (`HEALTHY 0/0/0`); new fixture
shape (absent root, kernel has btrfs) → `BLOCKED … detail=sysfs-unseen`; q82-shaped forged tree →
unchanged `DEGRADED filesystems=1`.

Cost, measured: 20 added shell lines (one file), 2 env seams (required — the census header's own
hermetic rule, `tools/tsukuroi-census.sh:373-400`, demands an override for every host path read in
live mode), 2 new fixtures (F06b absent-root-with-btrfs → BLOCKED; F11 root with `features/` only →
HEALTHY 0/0/0), and the one existing selftest case `storage-absent`
(`tools/tsukuroi-census.sh:2890-2891`) must set both seams. **Blocking constraint measured:** with the
patch applied but the seams unset, F06 reads `BLOCKED` on this btrfs host (`matrix.txt`, M4), so
`fixtures_matched` drops to 9 and the frozen v1 predicate fails — the v1 and q82 counters must both
add the two seams to `CHILD_ENV` in the same re-freeze, and the header's `detail=` grammar
(`tools/tsukuroi-census.sh:353-354`, per-device only) needs one clause for a root-level reason.

**Residual limit, stated so it is not overclaimed:** a reader that hides both `/sys/fs/btrfs` and the
mount table still reads `HEALTHY 0/0/0` (`matrix.txt`, M10). No in-process check closes that; only an
external authority (operator command, or a second reader in the init namespace) does.

## 6. Impacted axes

- **Coverage (C1)** — "storage integrity moves Frontier→Core" rests on this arm; as frozen, the arm
  reports an all-clear when it cannot see the surface, which is the one failure mode the coverage move
  was meant to remove.
- **Claim semantics / provenance** — `tools/tsukuroi-census.sh:363` and
  `tools/score-storage-arm-r38.py:18-20` state a universal the kernel does not support and cite rows
  that do not carry it.
- **Not impacted** — the frozen predicates themselves, the STORAGE grammar, six-plane neutrality, the
  q82 arm (given the one-sided form), and the q82/v1 scoring records.

## 7. What I did not do

- No lane file edited, created or deleted; no `git`/`jj` mutation in the lane; no index or jj state
  touched; no package, service, sysfs, hook, counter-reset or `/etc` change; no `sudo`; no subagents
  (leaf); no `agent://all`.
- I did not run the frozen counters (`score-storage-arm-r38.py`, `-q82.py`) — sibling scope. My census
  runs are the script extracted with `git show 52ffd65…` and executed as `bash <file>`; scratch only.
- Not executed, therefore marked as inference: an actual container (podman/docker) with a private
  mount namespace (the sysfs-over-report direction, §3), and a `CONFIG_SYSFS=n` kernel (§2.5 — argued
  from `fs/btrfs/Kconfig:3-19` and `include/linux/sysfs.h:397/503`, not from a running kernel).
- No tool installed or upgraded (nothing needed); no tooling channel exercised.
