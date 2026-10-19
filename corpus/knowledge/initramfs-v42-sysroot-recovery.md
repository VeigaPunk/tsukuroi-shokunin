source: S014 https://wiki.archlinux.org/title/Mkinitcpio § implementation choice, Runtime hooks, Runtime customization; S015 https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42 § Changes in mkinitcpio and https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v40 § Changes in hooks; S016 https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42/init § init:66-67,110 and https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v41/init § init:66-67,110; S021 https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs § run_latehook; S022 https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook § run_latehook; S025 https://man.archlinux.org/man/systemd-debug-generator.8 § KERNEL COMMAND LINE; S026 https://wiki.archlinux.org/title/General_troubleshooting § Boot problems and Recovery shells; S017 https://wiki.archlinux.org/title/Unified_kernel_image § Preparing a unified kernel image; S002 https://archlinux.org/news/mkinitcpio-42-requires-manual-intervention-for-tpm2-based-unlocking-of-luks-devices/ § applicability; S032 /var/log/pacman.log § 1991-1994 (own-work).
verified-at: 2026-10-19 (re-opened S014-S017, S021-S022, S002; re-ran read-only host configuration, package, hook and log probes).
recheck: on-release; procedure: `grep -Hn '^HOOKS' /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d/*.conf; grep -n '/new_root' /usr/lib/initcpio/hooks/*; curl -fsSL 'https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42/init' | grep -o '/new_root' | wc -l; pacman -Q mkinitcpio limine-mkinitcpio-hook plymouth`.

# mkinitcpio v42 `/sysroot` transition and recovery points

## Current host and compatibility surface

- [obs] `pacman -Q mkinitcpio plymouth limine-mkinitcpio-hook limine-snapper-sync snapper` returned `mkinitcpio 41.1-1`, `plymouth 26.134.222-2`, `limine-mkinitcpio-hook 1.38.0-1.1`, `limine-snapper-sync 1.31.0-1.1`, and `snapper 0.13.1-3` — `pacman -Q mkinitcpio plymouth limine-mkinitcpio-hook limine-snapper-sync snapper` 2026-10-19.
- [obs] The `HOOKS` declarations in `/etc/mkinitcpio.conf` and `/etc/mkinitcpio.conf.d/omarchy_hooks.conf` omit `systemd`; the drop-in includes `plymouth`, `encrypt`, and `btrfs-overlayfs`, and `omarchy_resume.conf` appends `resume` — `grep -Hn '^HOOKS' /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d/*.conf` 2026-10-19. Pacman log lines 1991-1994 show these drop-ins loaded in the Oct 11 image build — `grep -n 'drop-in' /var/log/pacman.log` 2026-10-19.
- [inf] ArchWiki says the presence or absence of the `systemd` hook selects the initramfs implementation, and runtime hooks are for busybox init (S014). The observed configuration therefore selects a busybox-style initramfs; this is configuration evidence, not an unpack/inspection of the generated image.
- [obs] The hook sweep printed `btrfs-overlayfs:4`, `plymouth:11`, and two `/usr/lib/initcpio/hooks/usr` lines — `grep -n '/new_root' /usr/lib/initcpio/hooks/*` 2026-10-19. The current `HOOKS` drop-in names `btrfs-overlayfs` and `plymouth`, but not `usr`: **2 configured runtime hooks** hardcode `/new_root` — `grep -Hn '^HOOKS' /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d/*.conf` plus `grep -n '/new_root' /usr/lib/initcpio/hooks/*` 2026-10-19. The extra `usr` hook is not included in this count.
- [obs] The reopened v42 `init` contains **0** `/new_root` references — `curl -fsSL 'https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42/init' | grep -o '/new_root' | wc -l` 2026-10-19. The reopened v41 `init` contains **7** — `curl -fsSL 'https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v41/init' | grep -o '/new_root' | wc -l` 2026-10-19. The v42 source mounts root on `/sysroot` (init:66-67) and switches root there (init:110); v41 uses `/new_root` at the corresponding points (S016). The v42 release notes state that busybox init now uses `/sysroot` (S015).
- [inf] After a rebuild that pairs v42 init with the currently configured, unchanged `btrfs-overlayfs` hook, `run_latehook` checks `/new_root`; `findmnt --mountpoint "$root_mnt" ... || return 0` means the missing mountpoint exits successfully before OverlayFS setup. This predicts a silent no-op. The configured Plymouth late hook also passes `--new-root-dir=/new_root`; its behavior after the path change is [unk]. These are future-upgrade compatibility risks, not a claim that the current 41.1 image has failed.

## Recovery entry points by stage

| stage | entry point | boundary |
|---|---|---|
| Current busybox initramfs, before root mount | `break=premount` (also legacy `break` / `break=y`) | S014: pauses after hooks load and before root mount; exit the shell to continue. |
| Current busybox initramfs, after root mount | `break=postmount` | S014: launches a troubleshooting shell after root has mounted; exit to continue. |
| Installed host under systemd | `systemd.break=pre-udev` or `systemd.break=pre-basic`; `systemd.debug_shell` (default tty9) | Unprefixed `systemd.*` parameters apply on the host. `systemd.break=pre-mount` and `pre-switch-root` are initrd-only breakpoints (S025). |
| Installed host recovery shell | `rescue`, `emergency`, or last-resort `init=/bin/sh` | S026: `rescue` is after root remounts read/write; `emergency` is earlier; `init=/bin/sh` replaces init. |
| A systemd-based initrd only — **not this host's configured flavor** | `rd.systemd.break=...`, `rd.systemd.debug_shell` | `rd.`-prefixed options are honored only in the initrd (S025); busybox init does not use systemd's initrd generator. |

## Rejected readings

- **R5 — “The mkinitcpio ≥42 TPM2 manual-intervention news applies to this configuration.”** [obs] The measured HOOKS omit `systemd` and use busybox `encrypt` — `grep -Hn '^HOOKS' /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d/*.conf` 2026-10-19. S002's intervention condition is systemd-hook TPM2-bound LUKS unlocking. The news is therefore N/A to the observed initramfs path; this does not establish whether TPM hardware exists.

## Falsifier

[inf] The silent-no-op prediction is falsified if a boot using v42 `init` with the same hook shows the hook mounting OverlayFS on the root after switch-root preparation, despite the hook's `/new_root` lookup. No image rebuild or test boot was performed in this read-only capture; that is an operator-only discriminator.

## QUALITY check

1. Falsifiable: source counts, installed HOOKS and hook names are re-runnable; the compatibility inference has a specific falsifier above.
2. Claims cite the opened docs/code, revision/tag or current host command and location below.
3. `[obs]`, `[inf]`, and `[unk]` separate measurements, compatibility inference, and untested behavior.
4. This is a new entry; any later correction to existing notes belongs in an appended dated erratum, not an overwrite.
5. R5 is retained under `## Rejected readings`.
6. No pacman transaction is advised; in particular this entry never advises bare `pacman -Sy`.
7. External claims cite S-rows with scoped tiers below; tier C is not used.
8. The mechanism claim is `[inf]` and carries the falsifier above.
9. The negative `/new_root` result carries its source sweep; the host hook and flavor findings carry their explicit config/file sweeps.

## Sources

- **S014, tier A** — https://wiki.archlinux.org/title/Mkinitcpio § implementation choice, `HOOKS`, Runtime hooks, Runtime customization. Quotes: “The concrete variant is determined by the presence or absence of the `systemd` hook”; “Runtime hooks are only used by a busybox initramfs”; Runtime customization says `break=premount` pauses before mounting root and `break=postmount` after it is mounted.
- **S015, tier A** — registry URL https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/releases/v42, fetched via https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42 § Changes in mkinitcpio: “Busybox-based init now uses /sysroot as the root mountpoint”. Also reopened v40 at https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v40 § Changes in hooks: “install/systemd now supports systemd v258 and onwards.”
- **S016, tier A** — https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42/init § init:66-67,110: “Mount root at /sysroot”; `/usr/bin/switch_root /sysroot`. Comparison https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v41/init § init:66-67,110: “Mount root at /new_root”; `/usr/bin/switch_root /new_root`.
- **S021, tier A** — https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs § `run_latehook`, lines 4, 7: `root_mnt="/new_root"`; `findmnt ... || return 0`.
- **S022, tier A** — https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook § `run_latehook`: `plymouth update-root-fs --new-root-dir=/new_root`.
- **S025, tier A** — https://man.archlinux.org/man/systemd-debug-generator.8 § KERNEL COMMAND LINE (`systemd.break`, `systemd.debug_shell`): “The option prefixed with `rd.` is honored only in the initrd, while the one without prefix is only honored on the host.”
- **S026, tier A** — https://wiki.archlinux.org/title/General_troubleshooting § Boot problems / Recovery shells: “rescue launches a shell shortly after the root file system is remounted read/write.”
- **S017, tier A** — https://wiki.archlinux.org/title/Unified_kernel_image § Preparing a unified kernel image: “mkinitcpio will assemble the UKI itself unless systemd-ukify is installed.” This entry makes no host-specific claim about which UKI route is currently selected.
- **S002, tier A** — https://archlinux.org/news/mkinitcpio-42-requires-manual-intervention-for-tpm2-based-unlocking-of-luks-devices/ § article body: “If you configured the systemd hook and unlock LUKS partitions” using affected PCR values, re-enrollment is required.
- **S032, own-work** — `/var/log/pacman.log` § lines 1991-1994, capture queried with `grep -n 'drop-in' /var/log/pacman.log` 2026-10-19; Oct 11 lines record the two mkinitcpio drop-ins loaded.
