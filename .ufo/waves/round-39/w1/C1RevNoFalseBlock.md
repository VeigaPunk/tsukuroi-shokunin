VERDICT: supports
<!-- Seat C1RevNoFalseBlock, item C1-16 — false-BLOCKED risk of the round-39 STORAGE mount-table guard. -->

# C1-16 — Can the new rule produce a false BLOCKED on a healthy host?

**Answer: no false-BLOCKED path found.** "Mounted ⇒ `/sys/fs/btrfs/<fsid>` exists" holds by construction at
linux v7.2 (the runtime kernel line: host runs 7.2.11-arch1-1): the fsid directory is created during
`fill_super`, before the mount is visible in any mount table, and its creation failure aborts the mount;
teardown removes it in `close_ctree`, which runs only after the mount entry has left the table. Every
dispatched scenario resolves to either "cannot happen" or "BLOCKED is honest".

## The rule under review

- Implementation: `tools/tsukuroi-census.sh` `probe_storage_arm()` — worktree file is byte-identical to
  implementation commit 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82
  (`diff -q` of `git show 49cc53c…:tools/tsukuroi-census.sh` vs worktree → no output; receipt `census-49cc53c.sh`).
  Guard: lines 1903-1913 — consulted only when `fsn == 0 && blocked == 0` (line 1903); fsid detection is a
  strict lowercase canonical-UUID regex on directory names (line 1864); the mount-table check compares the
  fstype field only, `if [ "${fst:-}" = btrfs ]` (line 1908); BLOCKED line assembled at 1916-1918.
- The fsid loop (lines 1870-1902) counts a filesystem only for UUID-named dirs, ignoring `features` etc.,
  matching the kernel layout seen live (below).

## Kernel evidence — fs/btrfs, tag v7.2 (raw.githubusercontent.com/torvalds/linux, accessed 2026-10-26; copies in `receipts/src/`)

1. **Creation on the mount path, before visibility; failure aborts the mount.**
   `super.c:1974-1978`: `ret = btrfs_fill_super(sb, fs_devices); if (ret) { deactivate_locked_super(sb); return ret; }`
   → `btrfs_fill_super` (super.c:958) → `open_ctree` (disk-io.c:3354) →
   `disk-io.c:3653-3657`: `ret = btrfs_sysfs_add_fsid(fs_devices);` with error `goto fail_block_groups`
   ("failed to init sysfs fsid interface"). So a btrfs mount that reaches a mount table has already run
   `btrfs_sysfs_add_fsid` successfully. (`btrfs_sysfs_add_mounted` follows at disk-io.c:3660.)
2. **Directory name matches the census regex.**
   `sysfs.c:2253` `btrfs_sysfs_add_fsid`; `sysfs.c:2259-2260`: `kobject_init_and_add(&fs_devs->fsid_kobj, …,
   "%pU", fs_devs->fsid)`; header comment sysfs.c:2248-2252: "Creates: /sys/fs/btrfs/UUID". Live dir name
   `1d02a454-c549-4a35-b567-89d60902af8e` (lowercase dashed canonical) matched the census regex — RUN1 below
   counted `filesystems=1`. `devinfo` is created inside the same function (sysfs.c:2273-2281), so a listed
   fsid dir is the stats-bearing one.
3. **Removal only at superblock teardown, after the table entry is gone.**
   Last unmount: `btrfs_put_super` (super.c:72-78, "last unmount of filesystem %pU") → `close_ctree`
   (disk-io.c:4315) → `disk-io.c:4541-4542`: `btrfs_sysfs_remove_mounted(fs_info); btrfs_sysfs_remove_fsid(fs_info->fs_devices);`.
   The VFS unlinks the mount from the namespace tree before `put_super`/`kill_sb` runs — and empirically
   (probe 4) even `umount -l` removes the entry immediately while the fs is still busy. Order is therefore:
   entry leaves table → then sysfs dirs die. The reverse window (listed, no dir) cannot occur; the harmless
   forward window (dir lingers without entry) reads HEALTHY from sysfs or 0/0/0 — never BLOCKED.
4. **"Kernel built without btrfs sysfs" is not a build configuration.**
   `Makefile:27`: `sysfs.o` is in the unconditional object list (`extent_map.o sysfs.o accessors.o …`);
   `Kconfig` defines no sysfs-related gate (only BTRFS_FS, POSIX_ACL, RUN_SANITY_TESTS, DEBUG, ASSERT,
   EXPERIMENTAL). A kernel able to mount btrfs always carries the fsid-dir code. (Module init creates the
   `/sys/fs/btrfs` kset itself — super.c:2641-2642 `.init_func = btrfs_init_sysfs`.)
5. **Sprout rename keeps the dir fsid-shaped** (edge, not steady state): `btrfs_sysfs_update_sprout_fsid`
   renames the dir between two `%pU` fsid strings ("Sprouting changes fsid of the mounted filesystem, rename
   the fsid directory", sysfs.c:2224-2227) — fsn stays ≥ 1.

## Mount-table semantics probes (all read-only; session log `receipts/evidence.log`)

1. **Live host** (kernel 7.2.11-arch1-1): 4 lines with fstype `btrfs` in `/proc/self/mounts` (one fs, four
   subvolume mounts of `/dev/mapper/root`); `/sys/fs/btrfs` holds exactly `1d02a454-…` + `features`.
   `RUN1` census: `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0` — the normal
   multi-mount/one-fsid layout reads HEALTHY, no false block.
2. **Substring false trigger — none.** Fixture table `…/mnt/btrfs-backup ext4 …` (btrfs only in the path,
   fstype ext4) with absent sysfs root: `RUN2` → `HEALTHY filesystems=0 devices=0 nonzero=0`. The arm
   compares the fstype field (line 1908), not the line text.
3. **Fsid-present shortcut.** Real sysfs (fsid present) with an unreadable `TSUKUROI_PROC_MOUNTS` override:
   `RUN3` → `HEALTHY filesystems=1 devices=1 nonzero=0` — the table is not consulted when fsn>0 (line 1903),
   so a broken/foreign table cannot manufacture a block on a populated sysfs.
4. **Lazy unmount.** tmpfs over a scratch path inside `unshare -rm`, holder keeping it busy:
   1 entry before `umount -l`; `ENTRY GONE from /proc/self/mounts` while still busy; still gone after refs
   drop. MNT_DETACH removes the table entry while the superblock lives — it can never leave "listed in
   mounts" behind. (tmpfs proxies the VFS table behavior; the btrfs sysfs removal timing is quoted above.)
5. **Namespace visibility.** Plain `unshare -rm` (no masking): `ls /sys/fs/btrfs` still lists the fsid dir —
   fsid dirs are not namespace-gated, and `/proc/self/mounts` only ever shows the reading process's own
   namespace. Another namespace's btrfs can therefore only over-report presence, never hide it.

## The three dispatched scenarios

1. **Kernel built without btrfs sysfs** — impossible: same compilation unit, no Kconfig gate (kernel
   evidence 4). Not a false-block source.
2. **A btrfs mount in another namespace visible here** — `/proc/self/mounts` cannot show another
   namespace's mounts; and even a deliberately pointed `TSUKUROI_PROC_MOUNTS` at a foreign table finds the
   global fsid dirs in our own sysfs (probe 5). Only a masked/unreadable sysfs (tmpfs over `/sys/fs/btrfs`
   or `/sys`, chroot/container without sysfs, permission-stripped bind) reaches the BLOCKED branch — and
   there the device error counters genuinely cannot be read, so `BLOCKED detail=mounts:btrfs-without-sysfs`
   is the honest verdict, exactly the round-38 false-all-clear this change removes.
3. **Lazily unmounted fs** — entry leaves the table at detach, dir dies later at `close_ctree`
   (kernel evidence 3 + probe 4): never "listed without dir". No false block; the transient
   dir-without-entry side reads HEALTHY/0-0-0.

**Conclusion:** on a healthy host the guard never fires falsely; it fires only when sysfs is masked or
unreadable, where BLOCKED is correct, or when the table itself is unreadable
(`detail=mounts:unreadable`, selftest `storage-mounts-unreadable`, census lines 2984-2987).

## Residual risks / what I did not do

- Runtime evidence is this host (kernel 7.2.11-arch1-1, one btrfs fs). I did not perform a real btrfs
  mount/unmount cycle (host mutation is forbidden); the ordering argument rests on the quoted v7.2 source
  plus the tmpfs MNT_DETACH proxy.
- A kernel that names fsid dirs outside lowercase dashed canonical UUID would evade the fsn regex and could
  false-block; mainline v7.2 uses `%pU` (sysfs.c:2259-2260) and the live host matches. Vendor-kernel drift
  is out of this round's scope.
- An LSM/secure-level filter hiding fsid dirs while btrfs is mounted would read BLOCKED — correct, since
  the counters are unreadable there.
- I did not read or re-run `tools/score-storage-hidden-r39.py` (counter semantics are the C1 counter item's
  scope; its live leg was scored elsewhere). I did not judge any C2 TO rows — no `TO<n>:` lines apply.
- No tooling was installed or upgraded; all probes used existing host tools and read-only fetches.
- Scratch `/fast/scratch/hyaku/tsukuroi-r39/C1RevNoFalseBlock/` removed after copying receipts.

## Receipts (`receipts/`)

- `evidence.log` — full session log of probes 1-5 with access date `2026-10-26T06:14:52Z`.
- `census-49cc53c.sh` — the implementation-commit census copy used for line citations.
- `src/{sysfs.c,super.c,disk-io.c,volumes.c,Makefile,Kconfig}` — fetched v7.2 sources (HTTP 200).
- `fx2-mounts.fixture`, `evidence.sh` — the RUN2 fixture table and the probe script.
