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

## R17-FRESHNESS — dated host re-verification (2026-10-20)

Historical captures stay historical: the 2026-10-19 measurements above remain true as dated observations. The values below are read-only L1 captures of 2026-10-20 under `.ufo/waves/round-17/l1-capture/`; no pacman query was re-run and no package count was re-measured. Nothing here authorizes package, service, or boot action.

- Old: `mkinitcpio 41.1-1` (line 9). [obs] mkinitcpio 42.2-1 is the installed package directory; the 09:15 full upgrade logged `upgraded mkinitcpio (41.1-1 -> 42.2-1)`. Capture: `.ufo/waves/round-17/l1-capture/fresh-capture.txt:16` (also `boot-chain-capture.txt:45`).
- Old: `plymouth 26.134.222-2` (line 9). [obs] plymouth 26.134.222-3 is installed; upgraded at 09:16:45. Capture: `.ufo/waves/round-17/l1-capture/fresh-capture.txt:17` (also `boot-chain-capture.txt:53`).
- Old: `limine-mkinitcpio-hook 1.38.0-1.1` (line 9). [obs] limine-mkinitcpio-hook 1.40.0-2 is installed; upgraded at 09:16:42. Capture: `.ufo/waves/round-17/l1-capture/fresh-capture.txt:18` (also `boot-chain-capture.txt:49`).
- Old: `limine-snapper-sync 1.31.0-1.1` (line 9). [obs] limine-snapper-sync 1.32.1-2 is installed; upgraded at 09:16:42. Capture: `.ufo/waves/round-17/l1-capture/fresh-capture.txt:19` (also `boot-chain-capture.txt:50`).
- Old: `snapper 0.13.1-3` (line 9). [obs] snapper 0.13.2-1 is installed; the captures contain no transaction line for it, so the upgrade path is [unk]. Capture: `.ufo/waves/round-17/l1-capture/fresh-capture.txt:26`.
- Old: "These are future-upgrade compatibility risks, not a claim that the current 41.1 image has failed." (line 14). [obs] VERSION 42.2 in omarchy_linux.efi and omarchy_linux-lts.efi (`boot-chain-capture.txt:174`, `:190`); the only 41.1 image is the snapshot #1 entry (`boot-chain-capture.txt:206`). The future-upgrade framing is stale. Capture: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:174`.
- Old: "After a rebuild that pairs v42 init with the currently configured, unchanged `btrfs-overlayfs` hook, `run_latehook` checks `/new_root`" (line 14). [obs] v42 init paired with the btrfs-overlayfs late hook: init `/sysroot` refs 7 and `/new_root` refs 0 (`boot-chain-capture.txt:175`), with `LATEHOOKS="plymouth btrfs-overlayfs"` (`boot-chain-capture.txt:178`). The silent-no-op prediction is now [unk]: no capture records whether OverlayFS mounted. Capture: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:178`.
- Old: "this is configuration evidence, not an unpack/inspection of the generated image." (line 11). [obs] UKI images were extracted and their HOOKS list has no systemd entry: `HOOKS="udev plymouth keymap consolefont encrypt resume"` (`boot-chain-capture.txt:177`, extraction header `:169-170`). The extraction does not by itself establish the flavour; the [inf] above stands. Capture: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:177`.
- Old: "No image rebuild or test boot was performed in this read-only capture; that is an operator-only discriminator." (line 32). [obs] limine-update ran at 09:26:11 and the current boot started 09:57:09 on 7.2.11 (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:86`, `:5`, `:10`). Whether OverlayFS mounted in that boot is not in either capture: [unk]. Capture: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:86`.
- Old: `pacman -Q mkinitcpio limine-mkinitcpio-hook plymouth` (the `recheck:` header, line 3). Superseded by `## R17-RECHECK — steer-safe procedure` below. [obs] package dirs read as mkinitcpio-42.2-1, plymouth-26.134.222-3 and limine-mkinitcpio-hook-1.40.0-2, with no package-manager query. Capture: `.ufo/waves/round-17/l1-capture/fresh-capture.txt:16`.

## R17-RECHECK — steer-safe procedure

Replaces the pacman query in the `recheck:` header at line 3 for this file. Read-only; no package-manager binary is invoked:

- `ls -d /var/lib/pacman/local/mkinitcpio-[0-9]* /var/lib/pacman/local/plymouth-[0-9]* /var/lib/pacman/local/limine-mkinitcpio-hook-[0-9]* /var/lib/pacman/local/limine-snapper-sync-[0-9]* /var/lib/pacman/local/snapper-[0-9]*`
- The version is the part of each directory name after `<pkg>-`; the last two dash-separated fields are pkgver and pkgrel (for example `limine-mkinitcpio-hook-1.40.0-2` gives `1.40.0-2`).
- Record the substitution (a directory-name read in place of a package query) in the report.


## R17-SYMLINK — silent-no-op prediction withdrawn (2026-10-20, L1)

Appended after the R17 notices above; earlier bytes unchanged. The `## Current host and compatibility surface` inference that, under v42 `init`, `btrfs-overlayfs` "checks `/new_root`" and exits before OverlayFS setup (a "silent no-op") rested on `/new_root` not existing as a mount path. [obs] mkinitcpio 42.x `initialize_buildroot` creates `/new_root` as a relative symlink to `sysroot` (`/usr/lib/initcpio/functions:1212-1213`); every 42.2 image on this host carries `new_root -> sysroot` (`.ufo/waves/round-17/l1-capture/overlay-emulation.txt:5`, `:8`). [obs] An unprivileged namespace emulation with the image's own `findmnt`/`mount` shows `findmnt --mountpoint` resolving through the symlink and the overlay landing on the `sysroot` mount (`overlay-emulation.txt:40-48`). [inf] The hook therefore reaches its btrfs checks and mounts the overlay; the no-op prediction is withdrawn, not confirmed. The Plymouth late hook's `--new-root-dir=/new_root` resolves to the same mount. Current verdicts per boot entry: `corpus/knowledge/boot-chain-r17.md` § Decision table. Nothing here authorizes package, service or boot action.
