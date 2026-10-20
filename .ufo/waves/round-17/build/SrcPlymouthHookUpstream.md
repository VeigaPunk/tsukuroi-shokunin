# SrcPlymouthHookUpstream — does the Arch plymouth hook have a sysroot fix/issue?

**Answer: no fix, no issue, and none currently needed.** [obs]

## Opened (2026-10-20)
- `https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook` — raw `main`, `run_latehook` body:
  `plymouth update-root-fs --new-root-dir=/new_root`
  Unchanged since commit 159d7694 (2026-09-24, tag 26.134.222-3). Host `/usr/lib/initcpio/hooks/plymouth:11` is byte-identical. [obs]
- Project API searches, `state=all`: `issues?search=sysroot` → `[]`; `merge_requests?search=sysroot` → `[]`; `issues?state=opened` → `[]`; only `mkinitcpio` MR is !1 (2024, closed). [obs]
- `https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/repository/commits?path=functions` — commit `00392d94` "Use /sysroot as the root mountpoint" (committed 2026-08-11): "To avoid issues (or to at least try to avoid them), /new_root will be kept as a symlink to /sysroot." [obs]
- mkinitcpio `v42`+`42.2` `functions:1212-1213`: `ln -s "sysroot" "$buildroot/new_root"`; `/usr/lib/initcpio/functions:1212-1213` same. [obs]
- Upstream unit `systemd-units/plymouth-switch-root.service.in` (gitlab.freedesktop.org, main): `update-root-fs --new-root-dir=/sysroot`. [obs]

## Local consistency
L1 capture `boot-chain-capture.txt:181,197` (`dirs: new_root sysroot` for 42.2; `:213` only `new_root` for 41.1). Host uses `udev` path via `/etc/mkinitcpio.conf.d/omarchy_hooks.conf`, so `run_latehook` executes; `/new_root` resolves to `/sysroot` through the shim. [inf]

## Does NOT establish
Plymouthd's reaction if the path ever dangles (daemon handler not inspected; freedesktop API returned 401), shim lifetime beyond 42.x, or `btrfs-overlayfs` semantics. [unk]

Scope: executed=none
