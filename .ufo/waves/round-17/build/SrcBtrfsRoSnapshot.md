# SrcBtrfsRoSnapshot — ro=true subvolume mounted with rw

[obs] Opened 2026-10-20 (read tool):
- https://btrfs.readthedocs.io/en/latest/Subvolumes.html — § "Subvolume flags": "The subvolume flag currently implemented is the _ro_ property (read-only status)." (l.76-77) and "Read-write subvolumes have that set to _false_, snapshots as _true_." (l.77).
- https://btrfs.readthedocs.io/en/latest/ch-mount-options.html — § "BTRFS SPECIFIC MOUNT OPTIONS": "Mount options are processed in order, only the last occurrence of an option takes effect" (l.17). § "NOTES ON GENERIC MOUNT OPTIONS" has no ro/rw entry.
- Subvolumes.html § "Mount options" (l.138-142) lists generic "`ro`, `rw`" as VFS-handled, and l.158 states: "Mounting a read-write snapshot as read-only is possible and will not change the _ro_ property and flag of the subvolume."

Answer: neither assigned page states whether a ro=true subvolume mounted `rw` has a writable root. Only the converse direction is documented. [inf] So `_ro_` is a persistent per-subvolume flag independent of mount `ro`/`rw`; `rw` cannot be assumed to clear or bypass it.

[obs] Supplementary kernel source (not the assigned pages): `fs/btrfs/inode.c` `btrfs_permission` returns `-EROFS` for MAY_WRITE when `btrfs_root_readonly()` (l.9392-9402); `btrfs_setattr` (l.5507) and `btrfs_update_time` (l.6492) likewise; `ctree.h:321-325` reads `BTRFS_ROOT_SUBVOL_RDONLY`. Mount succeeds rw; open-for-write, create, chmod and utimes fail EROFS.

Not established: mount(8) success/failure text, errno for already-open fds, nested subvolumes, whether boot degrades — [unk], no execution.

Scope: executed=none
