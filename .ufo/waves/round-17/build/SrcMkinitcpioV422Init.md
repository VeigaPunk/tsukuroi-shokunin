# SrcMkinitcpioV422Init — v42.2 init counts and the `/new_root` creator (access 2026-10-20)

[obs] Opened: `https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init`, `.../-/raw/v42.2/install/base`, `.../-/raw/v42.2/functions`; API `repository/tags/v42.2` (target `3cee3fa9`), commit diff `00392d94`.

**`init`** (fragment `# Mount root at /sysroot`): 7 × `/sysroot`, 0 × `/new_root` — lines 66, 67, 77, 78, 87, 88, 110. Quotes: `"$mount_handler" /sysroot`; `/usr/bin/switch_root /sysroot "$init" "$@"`.
**`install/base`** (`build()`, whole file): no root-mountpoint path; only busybox, kmod, blkid, mount/umount, switch_root, `init`, `init_functions`.

**Creator** — `functions` `initialize_buildroot()` (called `mkinitcpio:1121`): `install -dm755 "$buildroot/sysroot"` then `ln -s "sysroot" "$buildroot/new_root"` (functions:1218-1219).

`/new_root` is thus a *relative symlink* to `sysroot`, not an empty directory. Commit `00392d94` "Use /sysroot as the root mountpoint" (2026-08-11) removed `new_root` from the shared `install -dm755 "$root"/{new_root,...}` loop and added these lines; message: "/new_root will be kept as a symlink to /sysroot". Both names are buildroot-only, absent from `$earlyroot`. `add_dir /new_root` no-ops via `[[ -d ${BUILDROOT}${1} ]]` (functions:808-826). (`SrcMkinitcpioV42x.md` aliasing gap filled.)

[inf] A 42.2 image should hold `/new_root -> sysroot` (cpio mode 120777); a directory in a capture means dereferenced link or hook replacement.

**Does not establish:** that plymouth/btrfs-overlayfs work through the symlink (peer: btrfs-overlayfs keeps `root_mnt=/new_root` literally, so the link is load-bearing); that the captured UKI stores a symlink (needs `cpio -tv` mode); runtime boot outcome.

Scope: executed=none
