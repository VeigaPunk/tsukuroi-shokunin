# RevNewRootDir

[obs] 42.2's `initialize_buildroot` creates `/new_root` as a **symlink**, not a directory: `/usr/lib/initcpio/functions:1212-1213` — `install -dm755 "$buildroot/sysroot"`; `ln -s "sysroot" "$buildroot/new_root"`; the same function's brace list (`:1198`) no longer lists `new_root`. [inf] The 42.2 UKIs carry that link: the builder passes no `--generatedir`, so `buildroot` is a fresh mktemp (`/usr/share/libalpm/scripts/limine-mkinitcpio-install:180`).

[obs] 41.1 created a real dir: `/var/cache/pacman/pkg/mkinitcpio-41.1-1-any.pkg.tar.zst:usr/lib/initcpio/functions:1189` — `install -dm755 "$root"/{new_root,proc,sys,...}` for buildroot and earlyroot, no `sysroot` (matches capture's `dirs: new_root`).

[obs] Whole-tree sweep of `/usr/lib/initcpio` for `new_root|sysroot` yields only `functions:1212-1213`, runtime hooks (`btrfs-overlayfs:4`, `plymouth:11`, `usr:5,18`) and `init:66-110`. `install/base` adds busybox/kmod/blkid/mount/umount/switch_root/init only; `install/{btrfs-overlayfs,plymouth}` add no dirs. Runtime creates neither: `init_functions:534-539` (`mount_setup`) and `:430-432` (`default_mount_handler`) mount onto `$1`=`/sysroot` with no mkdir. Early cpio gets neither (`1212-1213` touches `$buildroot` only).

[inf] The relative link makes `/new_root` resolve to the mounted root; findmnt canonicalizes by default (`-C,--nocanonicalize` "Do not canonicalize paths at all. This option affects the comparing of paths." man7 findmnt.8, 2026-10-20), so `btrfs-overlayfs:7` matches `/sysroot` and `mount --move` resolves. Round-12's "silently no-ops" premise is probably wrong.

[unk] Capture's `dirs:` carries no types; re-extraction needs objcopy (execution, not authorized). L1 check: `objcopy -O binary --only-section=.initrd /boot/EFI/Linux/omarchy_linux.efi /tmp/i && lsinitcpio -x /tmp/x /tmp/i && ls -l /tmp/x/new_root` → `new_root -> sysroot`.

Installs: none.

Scope: executed=ls -l /var/cache/pacman/pkg/mkinitcpio-*, ls /usr/lib/initcpio/
