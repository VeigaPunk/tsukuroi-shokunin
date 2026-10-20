# CritNextBootChecklist — critique of L0 line `tsukuroi | round-17` (l0-questions.md:60)

Confirmed: [obs] the overlay no-op holds. `findmnt --mountpoint /new_root` fails, so the hook returns 0 (btrfs-overlayfs:4,7), and root is mounted at `/sysroot` (init:67).

Unsafe or missing:
1. [obs/inf] The LUKS header backup sits in `/var/backups/…` on the same encrypted root it is meant to recover, so it is useless if the header is damaged. The L0 line states its contents as fact; boot-chain-r17.md:19-21 lists them as "unverified". Fix: copy it off-disk and verify it.
2. [inf] There is no independent fallback entry. `/EFI fallback` chainloads BOOTX64.EFI (capture:155-156), which `ENABLE_LIMINE_FALLBACK=yes` (fresh:65) makes a copy of Limine (limine-install:533-548), so it loops back to the same menu. There are only 2 UKIs (capture:124-125), and lts shares the init and hooks. Fix: have a live USB ready.
3. [obs] Option (c) leaves out retention. Snapshot #1 has `cleanup=number` (capture:166), and `MAX_SNAPSHOT_ENTRIES=5` and `LIMIT_USAGE_PERCENT=85` apply (fresh:68,72). Its 41.1 image is the only copy (capture:114). Fix: operator pins #1 (`snapper modify -c "" 1`).
4. [obs] Overclaims "dkms built for 7.2.3". dkms reports the built modules missing (fresh:38), and `/usr/lib/modules` has no 7.2.3 (fresh:39-41). lts dkms shows `installed` (fresh:36), but the lts entry has never booted.
5. [obs] "No boot-chain input changed after boot" leaves out `/boot/limine.conf`. Its mtime is 12:07:06, after the boot (capture:106); who wrote it is [unk], and the sweep at capture:256 skips `/boot`. Fix: re-hash `limine.conf` and the UKI just before the reboot.
6. [unk] Unchecked BIOS/NVMe and power risks. fwupd and fwupd-efi were installed at 09:27 (pacman.log:3064-3073), and whether a capsule is staged is unknown. `/etc/fstab` was rewritten 3× (capture:85,94,97); without `nofail`, missing or reordered NVMe drives can drop the boot into emergency mode. The images include the `resume` hook (capture:177), so power off fully rather than hibernate. A dd clone would duplicate the PARTUUID used by `cryptdevice` (fresh:61).

Scope: executed=wc -l
