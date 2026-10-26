VERDICT: defect-found

Scoped defect: the declaration's fixture count is one too high (4 mount-table fixtures + 1
unlistable-root fixture, not 5 + 1). The mutant non-equivalence itself holds for all nine
mutants as *lines*, but only eight separate on a mount table the kernel can produce: M6
(case-folded fstype) is equivalent on the arm's input domain and is killed solely by a
table (`/dev/fx0 / BTRFS ...`) no kernel can emit. The frozen counter's PASS and the C1
operability property are not affected.

Item C1-6. Lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Seat leaf: no agents,
no lane writes except this report and the receipt dir.

## 0. Surface under test

* Arm under test is the declared-unchanged arm: `probe_storage_arm` body hashes identically at
  base `53b294a` and lane tip `f951f2` — both `71e6007e566e1af32feb495e04e4f291c75fdddb2b521d9822b7363fcdf34d56`
  from `git show <rev>:tools/tsukuroi-census.sh | sed -n '/^probe_storage_arm()/,/^}$/p' | sha256sum`.
  The census text I ran was `git show f951f288483c1af0cef4afd458488b84cf7a2165:tools/tsukuroi-census.sh`
  (3149 lines, sha256 `032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733`).
* Counter on disk and at `a447b67` both sha256 `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159`,
  matching SCORECARD.md:2303.
* My nine mutants are the counter's own frozen strings (`tools/score-selftest-literals-r40.py:69-80`),
  each applied as one exact substring replacement after asserting `text.count(old) == 1` on the
  f951f2 text (all nine: occurrences 1). No mutant text was re-typed by hand.
* Method per run: `bash <scratch copy>.sh` with `cwd=/`, env
  `PATH=/usr/bin:/bin LC_ALL=C HOME=<scratch> TMPDIR=<scratch> TSUKUROI_BTRFS_SYSFS=<fixture root> TSUKUROI_PROC_MOUNTS=<fixture table>`,
  then `grep '^STORAGE '`. That is the contracted override pair (`tools/tsukuroi-census.sh:462-463`);
  the arm reads only those two paths (`:1865-1925`).

Short forms used below, exactly as printed:

```
B   = STORAGE btrfs-device-stats state=BLOCKED  filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
H   = STORAGE btrfs-device-stats state=HEALTHY  filesystems=0 devices=0 nonzero=0
U   = STORAGE btrfs-device-stats state=BLOCKED  filesystems=0 devices=0 nonzero=0 detail=root:unreadable
U2  = STORAGE btrfs-device-stats state=BLOCKED  filesystems=0 devices=0 nonzero=0 detail=root:unreadable,mounts:btrfs-without-sysfs
```

Fixtures (verbatim; receipt `mutant-storage.json` carries the same text):

```
A  (sysfs root absent)
   proc /proc proc rw,nosuid 0 0
   /dev/nvme0n1p3 /home btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=257,subvol=/@home 0 0
   tmpfs /tmp tmpfs rw,nosuid,nodev 0 0

A8 (sysfs root absent)
   proc /proc proc rw,nosuid 0 0
   /dev/disk/by-label/btrfs-old /var/lib/machines btrfs ro,noatime,compress=zstd:3,subvolid=263,subvol=/machines 0 0

B  (sysfs root absent)
   proc /proc proc rw 0 0
   /dev/disk/by-label/btrfs-old /mnt/btrfs-backup ext4 rw,relatime 0 0

C  (sysfs root absent) — the R40 fixture verbatim (census f951f2:3033)
   proc /proc proc rw 0 0
   /dev/fx0 / BTRFS rw,relatime 0 0

D  (sysfs root = scratch dir holding fsid 11111111-1111-1111-1111-111111111111/devinfo/1/error_stats,
    five zero counters, mode 000)
   proc /proc proc rw,nosuid 0 0
   /dev/mapper/root / btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@ 0 0
```

Fixture A's btrfs line is the host's real `/home` line (`/proc/self/mounts`, options and
`subvolid=257,subvol=/@home`) with only the device field changed (a btrfs on an nvme device is
ordinary; on this host all four btrfs mounts use `/dev/mapper/root`, so a device substitution is
the only way to separate M1). A8/B/D are kernel-form lines; C is not (see §3).

## 1. Per-mutant result (base vs mutant on the same fixture)

| mutant (counter line) | fixture / sysfs | base | mutant | differs | direction |
|---|---|---|---|---|---|
| M1-VA-device-literal (`:69`, literal `/dev/mapper/root`) | A / absent | B | H | yes | under-block |
| M2-VB-root-mountpoint (`:70`, literal ` / btrfs `) | A / absent | B | H | yes | under-block |
| M3-VC-substring-btrfs (`:71`, `*btrfs*`) | B / absent | H | B | yes | over-block |
| M4-VG-subvolid-256 (`:72`, literal `subvolid=256`) | A / absent | B | H | yes | under-block |
| M5-a-grep-count (`:73-76`, `grep -c btrfs`) | B / absent | H | B | yes | over-block |
| M6-b-fstype-casefold (`:77`, `${fst,,}`) | C / absent | H | B | yes | over-block, non-producible trigger (§2) |
| M7-e-guard-drops-blocked (`:78`) | D / unreadable root | U | U2 | yes (detail only) | diagnostics |
| M8-subvol-at-literal (`:79`, literal `subvol=/@`) | A8 / absent | B | H | yes | under-block |
| M9-last-line-only (`:80`, `tail -n 1`) | A / absent | B | H | yes | under-block |

All nine differ from the base as a STORAGE line, so none of M1-M9 is textually equivalent;
`differs=True` for all nine in `mutant-storage.json`. The interesting distinctions:

* Under-blocking (dangerous direction, base BLOCKED -> mutant HEALTHY): M1, M2, M4, M8, M9.
  Each separating table is a shape a kernel emits elsewhere: btrfs on a non-`/dev/mapper/root`
  device (M1), btrfs outside `/` (M2), a subvolid other than 256 (M4), a subvolume not under
  `/@` (M8), and a btrfs mount that is not the table's last line (M9).
* Over-blocking with a producible trigger: M3, M5. A kernel line whose *device and mountpoint*
  contain the token `btrfs` (an ext4 mounted from `/dev/disk/by-label/btrfs-old` at
  `/mnt/btrfs-backup`) is enough; the R40 fixture adds `comment=btrfs` on top, which is not
  kernel-emittable (§3), but the kill does not need it.
* Evidence-only: M7. The state stays `BLOCKED`; only `detail=` changes (the mutant appends the
  mount reason to a line already blocked by `root:unreadable`). The R40 selftest anchors `detail=`
  with `$` (census f951f2:3041-3042), so it is killed at the evidence level, not the verdict level.

## 2. M6 does not separate on any kernel-producible table

Chain from kernel source (fetched 2026-10-26) and local tests:

1. `/proc/self/mounts` field 3 is `sb->s_type->name` (plus `.` + subtype): fs/proc_namespace.c:92-94
   `mangle(m, sb->s_type->name);` inside `show_type`, called by `show_vfsmnt` at :101-122 —
   https://raw.githubusercontent.com/torvalds/linux/master/fs/proc_namespace.c.
2. Type lookup is exact and case-sensitive: fs/filesystems.c:79-85
   `if (strncmp(fs->name, name, len) == 0 && !fs->name[len])`, and `get_fs_type` splits only at `.`
   and calls it (:393-399) — https://raw.githubusercontent.com/torvalds/linux/master/fs/filesystems.c.
3. btrfs registers the literal name: fs/btrfs/super.c:2214-2222 `.name = "btrfs"` with
   `FS_REQUIRES_DEV | FS_BINARY_MOUNTDATA | FS_ALLOW_IDMAP | FS_MGTIME` and no `FS_HAS_SUBTYPE`
   — https://raw.githubusercontent.com/torvalds/linux/master/fs/btrfs/super.c.
4. Local kernel probe (this host, 7.2.11-arch1-1), direct syscall, no mount made: inside
   `unshare -rm`, `fsopen("btrfs") -> fd 3`, `fsopen("BTRFS") -> errno 19 (No such device)`,
   `fsopen("BtrFs") -> errno 19`, `fsopen("ext4") -> fd 3`; outside a user namespace all four are
   `EPERM` (the capability gate fires before the lookup). `mount -t BTRFS` in `unshare -rm` says
   `unknown filesystem type 'BTRFS'`; `mount -t btrfs` gets past the lookup and fails
   `permission denied`. Receipt `host-kernel.txt`.
5. Registration-list and live-table checks: of the names in `/proc/filesystems`, only `btrfs`
   case-folds to `btrfs`; of the fstypes in `/proc/self/mounts`, all four btrfs lines are lowercase
   `btrfs` and no fstype begins with a non-lowercase letter. Running base and M6 against the live
   kernel table (with the sysfs root overridden away) prints the identical line `B` for both.

Therefore an `fstype` that case-folds to `btrfs` other than the literal `btrfs` requires a
filesystem type *registered under that casing*, which upstream does not do. The mutant's match set
strictly contains the base's (`${fst,,} = btrfs` is implied by `${fst} = btrfs`), and both only set
`blocked=1`, so M6 can never silence a btrfs mount; on the arm's documented input domain it is
equivalent, differing only where it over-blocks a non-btrfs type whose name happens to case-fold to
`btrfs`. Note the contrast with the excluded guard mutant (`tools/score-selftest-literals-r40.py:23`):
that one is equivalent on *all* inputs (`devn > 0` implies `fsn > 0`, and `fsn > 0` with
`devn == 0` sets `blocked=1` before the guard); M6 is equivalent only on kernel-emitted input.

## 3. Is `/dev/fx0 / BTRFS rw,relatime 0 0` a defensible spec or a contrived input?

Both, in different roles — but as host evidence it is contrived:

* Contrived as host input. No kernel can emit it: `BTRFS` is not a registered type (`fsopen`
  returns `ENODEV`, §2.4) and field 3 is the registered type name, so no `/proc/self/mounts`
  capture from any machine can contain this line. It is the only fixture that kills M6 (my M6
  selftest run fails exactly one case: `FAIL healthy: the fstype match is exact, so BTRFS is not
  btrfs (R40-C1)`, 123/124 pass — `m6-selftest-receipt.txt`), which confirms the kill is
  spec-driven rather than host-driven.
* Defensible as a parser-exactness spec. The arm's contract is "the mount table lists no btrfs
  mount" (census f951f2:365-366), and the kernel's own type registry is case-exact (§2), so a
  parser that compares field 3 exactly mirrors the kernel; a case-folding or substring parser
  deviates. As a unit spec for field-3 equality the case is legitimate, and it is the only way to
  pin exactness against a case-folding regression.

Judgment: contrived input, defensible spec. It should be read as a parser-contract fixture, not as
evidence that a host can reach that STORAGE line. The smallest safe correction is a classification
note (§6), not removal: the fixture is load-bearing for M6 and harmless otherwise.

Minor, same family: the R40 `storage-mounts-btrfs-in-path` fixture (census f951f2:3028) puts
`comment=btrfs` in field 4. `comment` is a mount(8) userspace option (man mount: "The command mount
does not pass the mount options unbindable, runbindable, private, rprivate, slave, rslave, shared,
rshared, auto, noauto, comment, x-*, loop, offset and sizelimit to the mount.<suffix> helpers"), and
locally `mount -t tmpfs -o comment=btrfs tmpfs <dir>` in `unshare -rm` yields a mount line with no
`comment=` (`host-kernel.txt`). So field 4 is not kernel-emittable either. The kill of M3/M5 is
unaffected because fields 1 and 2 already carry the token; the option token is surplus decoration.

## 4. Domain observation: on this host's own table, eight of nine mutants are equal

Running base and M1-M9 against a verbatim copy of `/proc/self/mounts`
(sha256 `0fe57247486e7c0002e09729f65564b83a3b748f01b299e7002129fe06fc49fe`, sysfs root absent):
base `B`; M1,M2,M3,M4,M5,M6,M7,M8 all `B`; only M9 differs (`H`, because the table's last line is
`Grok_Bot_0.70.2.AppImage /tmp/.mount_... fuse.Grok_Bot_0.70.2.AppImage ro,...`, not btrfs).
Receipt `live-table-mutants.json`.

That is not a counter defect — it is the round-39 monoculture restated: the measured host's four
btrfs lines all share device `/dev/mapper/root`, mountpoint-prefix `/@`, `subvolid=256`-adjacent
values and a trailing non-btrfs line, so literal-keyed mutants are indistinguishable *on this
host*. The round-40 fixtures supply the other mount configurations; non-equivalence is therefore
relative to the fixture input domain (other hosts/mounts), which is exactly what the fixtures
assert. It also means "the mutant is non-equivalent" must not be read as "it differs on the
measured host".

## 5. Concrete count defect in the declaration

SCORECARD.md:2303 declares the census "gains five mount-table fixtures that vary device,
mountpoint, options, subvolume, line position and fstype case, plus an unlistable root with btrfs
mounted" (5 + 1 = 6 new cases). Implementation commit `c707e35` adds five `check` labels and no
deletions (`git diff 758a4b0 c707e35 -- tools/tsukuroi-census.sh`: 36 insertions, 5 added
`check '...'`, at census f951f2:3011, 3018, 3026, 3032, 3037). Four are pure mount-table fixtures
(`varied-home`, `varied-multi`, `btrfs-in-path`, `fstype-case`); the fifth is the unlistable-root
fixture (`root-unreadable-mounted`), which also supplies a mount table. So the declaration
overcounts mount-table fixtures by one. This does not touch the counter predicate, which counts
mutants (`mutants_applied == 9`, `survivors == 0`), and the author receipt
`.ufo/waves/round-40/after/c1-after-c707e35.jsonl` shows `baseline 124/124 PASS`, `mutants_applied 9`,
`survivors 0`, `neutral_pass 3`, `selfref 5`, `result PASS`.

## 6. Impacted axes and smallest safe correction

* Impacted axis: C1 operability only (the STORAGE arm and its selftest fixtures). No C2 effect.
  The safety property "a hidden/absent sysfs root must not read as a clean disk" is unchanged:
  every under-blocking mutant is now killed by at least one fixture, and the five new cases
  (census f951f2:3011-3043) kill M1/M2/M4/M8 (two cases each), M9 (two cases), M3/M5 (one),
  M6 (one), M7 (one) — consistent with the per-mutant FAIL counts in the author receipt
  (M1/M2/M4/M8/M9: "2 failed"; M3/M5/M6/M7: "1 failed").
* Smallest safe correction: do not edit the frozen counter (`a447b67`) or the frozen declaration
  (`758a4b0`); record two notes in the round-40 record. Exact text:

  1. Mutant classification note:
     "M6-b-fstype-casefold is a spec-level mutant, not an operability mutant: the kernel
     filesystem registry is case-exact (fsopen(2) resolves btrfs but returns ENODEV for BTRFS and
     BtrFs) and /proc/self/mounts prints sb->s_type->name, so no kernel-emitted mount table can
     carry an fstype that case-folds to btrfs. M6 is therefore equivalent on the arm's input
     domain, differs only by over-blocking, and can never silence a btrfs mount; its separating
     fixture /dev/fx0 / BTRFS ... is a parser-exactness spec, not host-reachable evidence."

  2. Declaration errata:
     "Round-40 C1 added five selftest cases: four mount-table fixtures (varied-home,
     varied-multi, btrfs-in-path, fstype-case) and one unlistable-root-with-btrfs-mounted
     fixture. 'five mount-table fixtures plus an unlistable root' overcounts by one."

* Optional hygiene (same correction class, not required for the claim): drop the non-kernel
  `comment=btrfs` token from the `btrfs-in-path` fixture's field 4, since device and mountpoint
  already carry the token; and consider labeling `storage-mounts-fstype-case` as a spec case in
  its label text. Both are future-round edits, not round-40 changes.

## 7. Receipts and limits

Receipts in `.ufo/waves/round-40/w1/C1CritEquivalence/` (sha256):

* `mutant-storage.json` `116850ab04a65dea0c2844a1782bbdd13e8ba0885602a55818b7c843aec0863b`
  — revision, all five fixture texts, and base/mutant STORAGE lines for M1-M9.
* `live-table-mutants.json` `df7279f355e7e8842c59206156b4747119cba09399097c4a96915ba16a3d0a26`
  — base and M1-M9 against the frozen `/proc/self/mounts` copy (sha256 of copy recorded inside).
* `host-kernel.txt` `265db60630ea704213621000ea40ff62a1c5d082f0f2f6faa9c540d8418ed314`
  — case-fold checks, live btrfs lines, `fsopen(2)` and `mount -t` case tests.
* `m6-selftest-receipt.txt` `7dc3571807a5863eff7de8c4a1d36682398f4d21c108017575a2aff32ac2befa`
  — M6 variant (sha256 `03a64e835e5bc714d92ca384756fe24ae5b0c297f5f734ca906355e2d4899ed9`),
  the single FAIL line, 123 PASS, `FAIL (124 cases, 123 passed, 1 failed)`.

No census copy or counter copy is stored in the seat dir (scratch only). Scratch
`/fast/scratch/hyaku/tsukuroi-r40/C1CritEquivalence/` was removed after the receipts were copied;
the unreadable-root fixture dir was chmod-restored first.

Not done: I did not re-run the full counter at `f951f2` or at base `53b294a` (the author receipt
covers the predicate; my scope was mutant-vs-base on controlled tables), and I did not run any
other seat's counters. No host mutation: mounts were attempted only inside `unshare -rm`; no
package, service, hook, sysfs or `/etc` change; no tool installed. Tooling used: system `bash`,
`python3`, `git` (read-only), `cc` for the `fsopen(2)` probe.
