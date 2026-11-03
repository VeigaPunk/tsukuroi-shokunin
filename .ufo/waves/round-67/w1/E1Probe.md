# E1Probe — C1 host applicability probe (read-only)

2026-11-03T21:50:21Z · round 67 / w1 · lane base 5abc31d9 · declaration 071a55c9

## Verdict

`APPLICABILITY: No` — the v7.3 scrub-limit revert reordering cannot change any
scrub on this host. Four independent grounds, each measured:

1. **No v7.3 code is in service.** Installed userspace is `btrfs-progs 7.1-1`
   (`btrfs --version` → `btrfs-progs v7.1`; `pacman -Q` → `7.1-1`; Install Date
   `Sat 03 Oct 2026 05:42:01 PM -03`). Only `/usr/bin/btrfs` exists on PATH; no
   copy in `~/.local/bin`. The v7.1 binary carries the old in-loop revert.
2. **Single device.** `Total devices 1`, `devid 1`, sysfs `devinfo/` contains
   exactly one entry (`1`). The change's distinguishing content is cross-device;
   with one device both orderings emit one identical
   `write_scrub_device_limit(fdmnt, 1, old_limit)`.
3. **No limit to revert.** `scrub_speed_max = 0` for devid 1, and `0` means
   unlimited (`btrfs scrub limit -l … or 0 to reset to unlimited`);
   `throughput_limit` defaults to `0` (`before/src/scrub.c:1275`) and
   `old_limit` is read from the same attribute (`:1413`). Both the pre-scrub
   write and the revert write the same `0`.
4. **Nothing scrubs here.** `btrfs scrub status /` → `no stats available`,
   `Rate: 0.00B/s`; `/var/lib/btrfs` does not exist (no scrub records ever
   written); `btrfs-scrub@-.timer` is `disabled`, absent from
   `timers.target.wants/` and absent from `systemctl list-timers --all`. The
   service is `ExecStart=/usr/bin/btrfs scrub start -B %f`, so when it did run it
   used the installed v7.1 binary.

Residual delta if v7.3 were installed: only whether the sole device's limit is
restored before or after `pthread_join`. With `old_limit = 0` there is no limit
in force for that window to disturb, and no scheduled or recorded scrub to
observe it.

## Code delta confirmed at both ends

| side | file | line | shape |
|---|---|---|---|
| v7.1 | `round-42/frozen/src/scrub.c` | 1596 | revert inside per-device loop, before `skip` check and before `pthread_join(t_devs[i])` |
| v7.3 | `round-67/before/src/scrub.c` | 1641 | single revert loop after every device has finished, before the `do_print` summary |

## Provenance corroborated against upstream (allowed GET hosts only)

- `raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` → HTTP 200,
  sha256 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`,
  byte-identical to the frozen v7.1 copy.
- `…/v7.3/cmds/scrub.c` → HTTP 200, sha256
  `b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528`,
  byte-identical to the pinned v7.3 copy.
- `api.github.com/.../git/refs/tags/v7.3` → tag object
  `b5cb02e0fdd099f44b00a41b225c1a5daf7539ef`; the tag object peels to commit
  `afdc3a65e33f4d42f768ad50dca20c32e5ee1496`, matching the frozen declaration.

## Blocked / caveats

- **BLOCKED (privilege):** `btrfs filesystem show /dev/mapper/root` →
  `ERROR: cannot open /dev/dm-0: Permission denied` / `ERROR: no btrfs on
  /dev/dm-0`, rc=1. Process runs as uid 1000 with `CapEff: 0000000000000000`;
  `/dev/dm-0` is `brw-rw---- root:disk`. This EACCES is why the bare
  `btrfs filesystem show` prints `size 0 used 0 … MISSING` for devid 1 — the
  device is **not** missing: `findmnt` resolves four rw subvols, `df -B1 /`
  reports `998037782528` total, and `scrub status -d /` resolves `id 1` with the
  matching fsid.
- **Unverified assumption:** Arch `7.1-1` is taken to carry upstream v7.1
  ordering. `gitlab.archlinux.org` is outside the GET allowlist, so a backport
  could not be excluded by inspecting the package recipe. Immaterial to the
  verdict given grounds 2–4.
- Non-btrfs mounts `/fast` and `/tmp` are **xfs** (`nvme1n1p2`, `nvme1n1p1`);
  they carry no btrfs scrub surface and were not probed further.

## Environment caveat worth carrying to the L1

The lane's own storage (`/home`, and the fleet root) sits on the single btrfs
device; `/fast` scratch is xfs. Any future C1 experiment that needs a
*multi-device* btrfs filesystem or a *nonzero* `scrub_speed_max` cannot use this
host's real filesystem — it needs a loop-device-backed multi-device fixture.

## Receipts

`probes/e1-g1-identity.txt`, `e1-g2-filesystems.txt`, `e1-g2b-device-access.txt`,
`e1-g3-sysfs-limits.txt`, `e1-g4-records-timers.txt`, `e1-g5-scrub-status.txt`,
`e1-provenance.txt`, `e1-applicability.md`. All read-only; no host writes, no
sudo, no pacman transaction, no service verb.
