# SrcOverlayHookUpstream (R17) — /sysroot upstream status

**Answer: no upstream fix; no open issue or MR mentions /sysroot or new_root.** [obs] Opened 2026-10-20 with the read tool only:

- `https://gitlab.com/Zesko/limine-entry-tool` (`README.md · master`); `/-/issues?search=sysroot` redirected to a `work_items.atom` feed, empty.
- API `projects/60144633`: `issues?search=sysroot`, `?search=new_root`, `?state=opened` → `[]` each; `merge_requests?search=sysroot|new_root|mkinitcpio 42`, `?state=opened` → `[]` each.
- API `issues?search=mkinitcpio 42` → #26, #27 only; both closed, on kernel discovery and `pacman -Ql` cost; "mkinitcpio 42-1" appears only in Environment. Latest commit b9117873, 2026-10-10.
- raw `…/initcpio/hooks/btrfs-overlayfs`, `run_latehook()`: `root_mnt="/new_root"` — no /sysroot branch; last change 3c011dc2, 2026-01-11.
- raw `…/usr/lib/limine/overlayfs-setup`, `mount_snapshot_overlay()`: `local root_mnt="/sysroot"`.
- raw `…/systemd/system/overlayfs-setup.service`, `[Unit]`: `After=initrd-fs.target` / `Before=initrd.target`.
- raw `…/initcpio/install/sd-btrfs-overlayfs`, `build()`: `sd-btrfs-overlayfs requires systemd hook, not busybox hooks.`
- `CHANGELOG.md` @1.40.0: Fixed names pkgbase, no-kernel warning, `pacman -Ql`, enroll-config only; tag `1.40.0` matches master.

Cross-seat `build/SrcMkinitcpioV422Init.md`: mkinitcpio 42.2 creates `/new_root → sysroot` as a relative symlink (`functions:1218-1219`, 00392d94), so the hook's literal path is load-bearing on that link; upstream neither documents nor tests it.

Not established: [unk] upstream stance on the hook under 42; [unk] symlink semantics per call — `mount(8)` canonicalizes its target, so `--move` likely follows [inf], `findmnt -T` reports the resolved mount, but nothing was executed; [unk] whether `overlayfs-setup` works (`lowerdir=${root_mnt}`, no `mount --move`); [unk] blob search, HTTP 401; [inf] /sysroot script predates 42.

Scope: executed=none
