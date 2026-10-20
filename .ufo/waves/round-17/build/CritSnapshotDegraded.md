# CritSnapshotDegraded — falsifying DEGRADED-PREDICTED (snapshot #2, boot-chain-r17.md:64-65,93-96)

Axis: C1 depth. Capture = l1-capture/boot-chain-capture.txt; fresh = fresh-capture.txt.

**1. Overlay still mounts — refuted [obs].** `init:67,71` mounts `/sysroot`, then runs the late hooks. `btrfs-overlayfs:4,7` runs `findmnt --mountpoint /new_root`. `/new_root` is a bare directory (capture:181), so findmnt exits 1 and the hook returns 0. findmnt(8), man7.org, accessed 2026-10-20: -T: "use the option --mountpoint when checks of path elements are unwanted". EXIT STATUS: "1 … if no filesystem is found". A fallback to the parent mount would find rootfs, not btrfs, so the hook would still return at :8. The packaged `/sysroot` variant (`/usr/lib/limine/overlayfs-setup:4`) is built only into systemd initramfs images (`install/sd-btrfs-overlayfs:8-12`), and these images are busybox (capture:176-178).

**2. The plymouth mismatch makes it fail outright — refuted by outcome [obs].** Boot 0 used the same image (capture:143=220) and is running with 0 failed units (fresh:52-54).

**3. Strongest counter-reading: emergency mode, not a degraded boot [inf].** Snapshot #2 (09:29:19, capture:167) froze the 09:19:40 fstab, which was reinstalled twice after it (capture:84,94,97). `/` has mtime 09:38:14 (capture:102), which hints at a mountpoint created after the snapshot. Without the overlay, systemd cannot create that directory on a read-only root. A mount without `nofail` would then fail and drop to emergency.target. grub-btrfs README, "Warning: booting read-only snapshots can be tricky": "/var/log or even /var must be on a separate subvolume."

**4. It may not be a rollback at all [unk].** Capture:126 cuts each line at 200 columns, so the snapshot `rootflags` on lines 144 and 148 were never seen. The subvol column in the table states them as fact.

**What would settle it:** the full lines 51 and 57 of `/boot/limine.conf`; a diff of `/.snapshots/2/snapshot/etc/fstab` against `/etc/fstab`, checking `nofail` and whether each mountpoint exists in the snapshot; whether `/var/log` is its own subvolume.

**Smallest correction:** set the verdict to DEGRADED-OR-EMERGENCY until those checks are done, and mark the subvol column [inf].

Scope: executed=none
