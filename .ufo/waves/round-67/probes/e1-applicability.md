2026-11-03T21:50:21Z

# C1 host applicability probe (E1Probe, round 67 / w1)

Read-only host probes for C1 (btrfs-progs v7.3 scrub-limit revert reordering).
No privilege escalation was attempted; no host state was modified. Per-group
stdout+stderr+rc captures live beside this file as `e1-g*.txt`; provenance is
`e1-provenance.txt`.

## Probe table

| probe | command | observed | rc |
|---|---|---|---|
| G1 kernel | `uname -r` | `7.2.11-arch1-1` | 0 |
| G1 userspace version | `btrfs --version` | `btrfs-progs v7.1` / `-EXPERIMENTAL -INJECT -STATIC +LZO +ZSTD +UDEV +FSVERITY +ZONED CRYPTO=libgcrypt` | 0 |
| G1 package | `pacman -Q btrfs-progs` | `btrfs-progs 7.1-1` | 0 |
| G1 package detail | `pacman -Qi btrfs-progs \| grep -E '^(Version\|Install Date)'` | `Version         : 7.1-1` / `Install Date    : Sat 03 Oct 2026 05:42:01 PM -03` | 0 |
| G1 binary resolution | `type -a btrfs` | `btrfs is /usr/bin/btrfs` (no shadowing copy in `~/.local/bin`) | 0 |
| G2 btrfs mounts | `findmnt -t btrfs -o TARGET,SOURCE,FSTYPE,OPTIONS` | one fs: `/dev/mapper/root`, subvols `/@` `/@home` `/@pkg` `/@log`, `compress=zstd:3,ssd,discard=async,space_cache=v2` | 0 |
| G2 filesystem show | `btrfs filesystem show` | `uuid: 1d02a454-c549-4a35-b567-89d60902af8e`, `Total devices 1`, `devid    1 size 0 used 0 path /dev/mapper/root MISSING` | 0 |
| G2 block layout | `lsblk -o NAME,FSTYPE,MOUNTPOINT` | `nvme0n1p2 crypto_LUKS` → `root btrfs`; `/fast` and `/tmp` are **xfs**, not btrfs | 0 |
| G2 direct device scan | `btrfs filesystem show /dev/mapper/root` | **BLOCKED** `ERROR: cannot open /dev/dm-0: Permission denied` / `ERROR: no btrfs on /dev/dm-0` | 1 |
| G2 capability context | `cat /proc/self/status \| grep -E "^CapEff"` | `CapEff:	0000000000000000` (uid 1000, zero effective caps) | 0 |
| G3 sysfs fsids | `ls -1 /sys/fs/btrfs/` | `1d02a454-c549-4a35-b567-89d60902af8e`, `features` | 0 |
| G3 devinfo enumeration | `ls -1 <fsid>/devinfo` | `1` (single devid) | 0 |
| G3 scrub limit | `cat <fsid>/devinfo/1/scrub_speed_max` | `0` (`-rw-r--r--`, writable attribute present) | 0 |
| G4 scrub records | `ls -la /var/lib/btrfs` | **`ls: cannot access '/var/lib/btrfs': No such file or directory`** | 2 |
| G4 timer wants | `ls -1 /etc/systemd/system/timers.target.wants/ \| grep -i scrub` | no match (empty) | 1 |
| G4 timer enablement | `systemctl is-enabled 'btrfs-scrub@-.timer'` | `disabled` | 1 |
| G4 scheduled timers | `systemctl list-timers --all \| grep -i scrub` | no match (empty) | 1 |
| G5 scrub status | `btrfs scrub status /` | `UUID: 1d02a454-…`, `no stats available`, `Total to scrub: 213.01GiB`, `Rate: 0.00B/s`, `Error summary: no errors found` | 0 |
| G5 per-device status | `btrfs scrub status -d /` | `Scrub device /dev/mapper/root (id 1)`, `no stats available` | 0 |
| G5 raw counters | `btrfs scrub status -R /` | all counters `0` (`data_extents_scrubbed: 0` … `last_physical: 0`) | 0 |

## Notes

**The `MISSING` token in `btrfs filesystem show` is an artefact of my own
privilege, not a degraded filesystem.** `btrfs filesystem show` follows
`/dev/mapper/root` → `/dev/dm-0`, which is `brw-rw---- root:disk`; with
`CapEff: 0000000000000000` the open fails with `EACCES`, so the tool prints
`size 0 used 0 … MISSING`. Independent evidence that the device is present and
healthy: `findmnt` resolves all four subvols, `/proc/mounts` lists them `rw`,
`df -B1 /` reports `998037782528` bytes total, and the scrub ioctl path
(`btrfs scrub status -d /`) resolves `id 1` with the matching fsid. This is
recorded as a BLOCKED probe, not as a missing device.

**`scrub_speed_max = 0` means unlimited, so there is no limit to revert.**
`cmd_scrub_limit` help: `-l, --limit SIZE … or 0 to reset to unlimited`.
`throughput_limit` defaults to `0` (`cmds/scrub.c:1275`), and
`sp[i].old_limit` is read from the same attribute (`:1413`), so on this host both
the pre-scrub write and the revert write the value `0`.

**Version delta is real and the pinned copies are genuine.** Upstream
`kdave/btrfs-progs` tag `v7.1` `cmds/scrub.c` hashes to
`48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`, byte-identical
to the frozen v7.1 copy; tag `v7.3` `cmds/scrub.c` hashes to
`b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528`,
byte-identical to the pinned v7.3 copy. Tag object
`b5cb02e0fdd099f44b00a41b225c1a5daf7539ef` peels to commit
`afdc3a65e33f4d42f768ad50dca20c32e5ee1496`, matching the frozen declaration.
The reordering itself: v7.1 reverts inside the per-device loop at
`frozen/src/scrub.c:1596` (before the `skip` check and before
`pthread_join(t_devs[i])`); v7.3 does one revert loop after every device has
finished at `before/src/scrub.c:1641`.

**Unverified assumption.** Arch's `btrfs-progs 7.1-1` is taken to carry upstream
v7.1 ordering. The Arch package recipe (`gitlab.archlinux.org`) is not reachable
from the hosts this seat may GET, so a backport cannot be excluded by direct
inspection; the version string is `v7.1` and pkgrel is `1`.

**Multi-device dimension collapses here.** The distinguishing content of the
v7.3 change is cross-device (one revert pass after all devices, lowest-limit
aggregation). With `Total devices 1` both the in-loop and post-loop forms emit
exactly one `write_scrub_device_limit(fdmnt, 1, 0)`.

**Conditional.** Even with v7.3 installed, the residual single-device delta would
be only the window in which the limit is restored (before vs after
`pthread_join` of the sole device). With `old_limit = 0` (unlimited) there is no
throughput limit in force for that window to disturb, and nothing scheduled or
recorded can observe it.

APPLICABILITY: No — v7.3's revert-after-all-devices ordering cannot change any scrub on this host, because the only btrfs filesystem has a single device (devid 1, so both orderings emit one identical `scrub_speed_max` write of `0` and no cross-device interaction exists), that attribute is `0` meaning unlimited so the revert is a no-op, no scrub is running or recorded and the monthly `btrfs-scrub@-.timer` is disabled, and the installed btrfs-progs is `7.1-1` which still ships the old in-loop ordering.
