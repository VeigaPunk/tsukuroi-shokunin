# SrcLimineSnapperSync — limine-snapper-sync upstream README

**Opened** [obs]: `https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/README.md` (text/plain, default branch `master`), accessed 2026-10-20. `/-/raw/main/README.md` → HTTP 404; repo root returned only an HTML shell, so the raw master README is the actual source.

## Q1 — snapshot entry → UKI

[obs] Zero occurrences of `limine_history` in this README, its CHANGELOG, and the linked limine-entry-tool README (greps). Boot Configuration shows only `protocol: linux` examples, no UKI/`protocol: efi` entry (`README:283-316`). Closest statements:

- "When a Snapper snapshot is created, a snapshot boot entry with its matching kernel versions is added to Limine." (Description, `README:29`)
- "Bootable files (kernel, initramfs/initrd, or UKI) are stored outside a fully encrypted partition" (Why it was created, `README:55`)
- "Deduplicate kernel files to avoid copies by re-using existing files on the boot partition" (Core sync system, `README:840`)

[inf] Snapshot UKIs are boot-partition copies referenced by the generated entry; the copy trigger/naming and any `limine_history` role are [unk] — not documented.

## Q2 — retention

[obs] "Limits how many snapshot entries appear in the \"Snapshots\" boot menu." (Tool Configuration, `README:370`); auto mode "automatically removes older snapshot boot entries based on LIMIT_USAGE_PERCENT without warning" (`README:377`); default `auto` (`README:385`); fewer-than-Snapper troubleshooting (`README:717`). Pinned snapshots are **planned only** (`README:928`).

## Q3 — btrfs-overlayfs dependency

[obs] Installation: "Manually add `btrfs-overlayfs` after `filesystems` in `HOOKS=(...)`" plus "for systemd hooks, use `sd-btrfs-overlayfs`" (`README:163-164`). Troubleshooting "Some display managers fail to boot into read-only snapshots" (`README:726-754`) recommends "Use OverlayFS to simulate a writable layer", mkinitcpio hook at `README:751-752`. [obs] Never stated as a universal read-only-boot prerequisite; `SNAPSHOT_WRITABLE=yes` is the documented alternative (`README:427-437`).

## Not established

[unk] No `limine_history`, no UKI selection/copy timing, no statement retention deletes UKI copies versus entries; nothing on mkinitcpio 42 `/sysroot` vs `/new_root`. Arch Wiki "Snapper snapshot integration for Btrfs" (accessed 2026-10-20) corroborates both hooks, also never mentions `limine_history`.

Scope: executed=none
