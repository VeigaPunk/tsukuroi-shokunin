
source: S200 — https://man7.org/linux/man-pages/man2/mount.2.html — `ERRORS`, man-pages 6.19 (opened 2026-10-25)
source: S201 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c — `create_snapshot`, kernel tag v7.2 (opened 2026-10-25)
verified-at: 2026-10-25
recheck: on-release — re-read mount(2) ERRORS and fs/btrfs/ioctl.c at the host's kernel tag

ground: the untested btrfs-overlayfs snapshot-boot path in `corpus/README.md:151-153` and the errno:13 classification frontier in `corpus/README.md:38-42`

# Mount and Btrfs snapshot errno classes for the snapshot-boot path

The errno on a mount or Btrfs snapshot failure identifies an operation-specific error class; it is not by itself a cause diagnosis. The syscall contract and the filesystem's own ioctl path must be read separately.

## Mount syscall

`mount(2)` requires `CAP_SYS_ADMIN`; missing privilege returns `EPERM`. Its `ERRORS` section distinguishes path search (`EACCES`), mounting a read-only filesystem without `MS_RDONLY` (`EACCES`), and filesystems that instead return `EROFS` for that read-only condition. It also documents `EBUSY` when stacking a new mount with the same source and target, and `ENODEV` when the filesystem type is not configured in the running kernel. The exact error depends on operation and filesystem; `EACCES` and `EROFS` are not interchangeable observations.

## Btrfs snapshot ioctl

At kernel tag v7.2, `create_snapshot()` in `fs/btrfs/ioctl.c` tests the source filesystem and source ownership separately: a cross-filesystem snapshot source returns `-EXDEV`; a source the caller does not own returns `-EPERM`. The latter branch's comment says snapshotting is limited to subvolumes the caller owns. These are distinct from path-component search failures. This is source-code behavior at the pinned tag, not a statement that the host's earlier `errno:13` event came from a Btrfs snapshot ioctl.

| Observed operation | Error class | Read this as | Recheck |
|---|---|---|---|
| Mount needs privilege; caller lacks it | `EPERM` | privilege/capability denial for this mount operation | `mount(2)` ERRORS |
| Read-only mount attempted without `MS_RDONLY` | `EACCES` or `EROFS` | filesystem-specific read-only condition; do not collapse the two spellings | `mount(2)` ERRORS |
| Same source and target mount is stacked | `EBUSY` | existing-mount conflict in the same namespace | `mount(2)` ERRORS |
| Snapshot source belongs to another filesystem | `EXDEV` | cross-filesystem snapshot attempt | `fs/btrfs/ioctl.c` `create_snapshot()` |
| Snapshot source is not owned by caller | `EPERM` | Btrfs source-ownership check | `fs/btrfs/ioctl.c` `create_snapshot()` |

## Boundaries

- These are documented operation/error associations, not proof of a cause for a historical errno log line.
- `EPERM` is not synonymous with `EACCES`; a capability check, a Btrfs ownership check, and a path DAC check are different questions.
- No mount, snapshot, filesystem repair, package operation or host mutation is authorized by this entry.
- The target is the existing snapshot-boot frontier; this entry adds detail there and does not claim a new coverage surface.

## QUALITY check

- QUALITY 1-3: pass — each table row names a falsifiable operation/error association, cites the pinned primary source rows, and keeps source behavior separate from host inference/unknowns.
- QUALITY 7: pass — external claims cite the exact mined S200/S201 rows, tiers and section/code anchors.
- QUALITY 14: pass — the sources are re-opened this round and the source-specific propositions above resolve against their located sections/branch.
- Coverage-map check: pass for depth on existing frontier ground only; not claimed as new coverage or a host repair.
