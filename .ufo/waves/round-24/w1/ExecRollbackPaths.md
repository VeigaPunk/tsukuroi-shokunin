# ExecRollbackPaths — C2/P5 evidence: package cache, Arch Archive, mirror and Snapper rollback paths

Verdict: The local package cache is empty of package files, so cache rollback is unavailable; the Arch Linux Archive holds the exact installed boot-chain versions (plus pre-upgrade versions), Snapper snapshot 1 is a bootable pre-upgrade rollback, and the omarchy mirror serves only current versions and cannot supply systemd 262-1.

## Evidence

1. Local package cache `/var/cache/pacman/pkg` holds 4 entries, all directories, zero package files.

   - Command `ls -la /var/cache/pacman/pkg` (2026-10-22): 4 entries `download-0jh7Uc`, `download-Lsbwhh`, `download-r5r0Ix`, `download-vcoq00`, each a directory owned by alpm:alpm, mode 0700, all dated 2026-10-20/21.
   - Command `find /var/cache/pacman/pkg -maxdepth 1 -type f | wc -l` → `0`.
   - Command `find /var/cache/pacman/pkg -maxdepth 1 -name "*.pkg.tar*" | wc -l` → `0`.
   - Command `du -sb /var/cache/pacman/pkg/download-*` → `0` for each of the four directories.
   - Command `sudo -n find /var/cache/pacman/pkg -maxdepth 2 -type f -printf ...` → no files.
   - Global search `find /home /var /tmp /opt -xdev -name "*.pkg.tar*" -type f` (120s cap, 2026-10-22) → no package files surfaced.
   - [obs] The capture's `cache-file-count` section (`.ufo/waves/round-24/capture/l1-2/capture.txt:233-236`, `l1-3/capture.txt:226-229`) prints `4` because `ls /var/cache/pacman/pkg | wc -l` counts the four directory entries, not package files.
   - [inf] Premise P5's wording "package cache holds 4 files" is inaccurate: it holds 4 empty alpm download temp directories and 0 package files (per-cause attribution: the count is a directory count).

2. `paccache -d -k1` (dry run only).

   - Command `paccache -d -k1` → `==> no candidate packages found for pruning`, exit 0.
   - Command `sudo -n paccache -d -k1` → same, exit 0.
   - Command `paccache -d -k1 -u` and `paccache -d -k0` → `==> no candidate packages found for pruning`, exit 0.
   - Version: `paccache --version` → `paccache 1.13.1`.
   - [obs] No `/etc/paccache.conf`; the default cachedir `/var/cache/pacman/pkg` is scanned. No package files exist there, so no candidate packages.

3. Arch Linux Archive (archive.archlinux.org): exact installed boot-chain package files and `.sig` files are present (HTTP 200), plus the pre-upgrade versions.

   - mkinitcpio 42.2-1: `https://archive.archlinux.org/packages/m/mkinitcpio/mkinitcpio-42.2-1-any.pkg.tar.zst` → 200, content-length 70844; `.sig` → 200.
   - linux 7.2.11.arch1-1: `https://archive.archlinux.org/packages/l/linux/linux-7.2.11.arch1-1-x86_64.pkg.tar.zst` → 200, content-length 168950404; `.sig` → 200.
   - systemd 262-1: `https://archive.archlinux.org/packages/s/systemd/systemd-262-1-x86_64.pkg.tar.zst` → 200, content-length 11195406; `.sig` → 200.
   - plymouth 26.134.222-3: `https://archive.archlinux.org/packages/p/plymouth/plymouth-26.134.222-3-x86_64.pkg.tar.zst` → 200, content-length 1093925; `.sig` → 200.
   - Pre-upgrade (downgrade) versions also present (HTTP 200): mkinitcpio 41.1-1 and 42.1-1; systemd 261.2-1; linux 7.2.3.arch1-3; plymouth 26.134.222-2.
   - Index pages opened (2026-10-22) with exact located quotes (verbatim substrings of the opened page, whitespace preserved):
     - `https://archive.archlinux.org/packages/m/mkinitcpio/` — `mkinitcpio-42.2-1-any.pkg.tar.zst                  01-Oct-2026 14:16     69K`
     - `https://archive.archlinux.org/packages/l/linux/` — `linux-7.2.11.arch1-1-x86_64.pkg.tar.zst            16-Oct-2026 01:10    161M`
     - `https://archive.archlinux.org/packages/s/systemd/` — `systemd-262-1-x86_64.pkg.tar.zst                   22-Sep-2026 13:17     11M`
     - `https://archive.archlinux.org/packages/p/plymouth/` — `plymouth-26.134.222-3-x86_64.pkg.tar.zst           24-Sep-2026 11:05      1M`
   - [obs] Signature files exist for all four; `archlinux-keyring 20260909-1` is installed and the local pacman keyring contains the Arch master key.

4. Omarchy stable mirror (the host's configured mirror, `https://stable-mirror.omarchy.org/$repo/os/$arch`).

   - Mirror core.db (downloaded 2026-10-22) lists: mkinitcpio-42.2-1, linux-7.2.11.arch1-1, but systemd-262.1-1 (newer than installed 262-1). Mirror extra.db lists plymouth-26.134.222-3.
   - File probes: `mkinitcpio-42.2-1-any.pkg.tar.zst` → 200; `linux-7.2.11.arch1-1-x86_64.pkg.tar.zst` → 200; `plymouth-26.134.222-3-x86_64.pkg.tar.zst` → 200; `systemd-262-1-x86_64.pkg.tar.zst` → 404.
   - Older versions on the mirror → 404: mkinitcpio 41.1-1, systemd 261.2-1, linux 7.2.3.arch1-3, plymouth 26.134.222-2.
   - [inf] The mirror cannot supply the exact installed systemd 262-1 nor any pre-upgrade boot-chain version; it is not a rollback source for the boot chain. It does serve the current mkinitcpio/linux/plymouth files.

5. Snapper.

   - Command `snapper list` (without sudo) → `No permissions.` exit 1 (recorded error; per assignment).
   - Command `sudo -n snapper list` → root config snapshots: 0 current; 1 `pre-nvme-baseline-2026-10-20` (2026-10-20 09:03:02 -03, cleanup=number); 2 `pre-aur-elephant-2.22.1` (2026-10-20 09:29:19 -03, cleanup=number). Both 1 and 2 are readonly btrfs subvolumes (`btrfs subvolume show` shows `Flags: readonly`).
   - Command `sudo -n snapper -c home list` → 44 timeline snapshots (hourly, 2026-10-20 10:00 through 2026-10-22 05:00).
   - Snapshot 1 contains the pre-upgrade boot chain: mkinitcpio 41.1-1, plymouth 26.134.222-2, systemd 261.2-1, linux 7.2.3.arch1-3 (from `/@/.snapshots/1/snapshot/var/lib/pacman/local/`), and its `/usr/lib/initcpio/functions` uses `$root/{new_root,...}` (line 1188) with hooks `usr` realtab=/new_root — i.e. coherent mkinitcpio-41 `/new_root` semantics.
   - Snapshot 2 contains the post-upgrade chain: mkinitcpio 42.2-1, systemd 262-1, plymouth 26.134.222-3, linux 7.2.11.arch1-1.
   - Boot entries exist in `/boot/limine.conf` (read-only): snapshot 1 entry `pre-nvme-baseline-2026-10-20` (kernel 7.2.3-arch1-3, `rootflags=subvol=/@/.snapshots/1/snapshot`) and snapshot 2 entry `pre-aur-elephant-2.22.1`. The snapshot-1 kernel image is preserved at `/boot/432d02b544a5459ebbff9c42ec68334d/limine_history/omarchy_linux.efi_sha256_0f1e3c84...` (290422784 bytes, dated 2026-10-20 09:03:02, i.e. before the 09:16 mkinitcpio 42.2 upgrade) and its sha256 matches `0f1e3c84...`  (verified via `sha256sum`).
   - `linux-lts` 6.18.57-2 also installed with modules present in `/usr/lib/modules/6.18.57-2-lts`; EFI image `/boot/EFI/Linux/omarchy_linux-lts.efi` present (hash 2d49da06).
   - NVIDIA: dkms status shows nvidia/615.78.08 built for 6.18.57-2-lts and 7.2.11-arch1-1; original modules exist for 7.2.3-arch1-3 but are not built in the current modules dir. Snapshot 1 contains nvidia dkms modules for 7.2.3-arch1-3 at `/@/.snapshots/1/snapshot/usr/lib/modules/7.2.3-arch1-3/updates/dkms/` (nvidia.ko.zst, nvidia-uvm.ko.zst, nvidia-modeset.ko.zst, nvidia-drm.ko.zst).

6. `/boot` layout.

   - `/boot` is a separate vfat partition `/dev/nvme0n1p1` (not covered by btrfs snapshots); 2.0G total, 687M free.
   - Present: `/boot/EFI/Linux/omarchy_linux.efi` (7.2.11, hash 2e9c9bdc), `/boot/EFI/Linux/omarchy_linux-lts.efi` (hash 2d49da06), `/boot/EFI/limine/limine_x64.efi` and `limine_x64.bak`, `/boot/EFI/BOOT/BOOTX64.EFI` and `BOOTIA32.EFI`, `/boot/limine.conf` and `limine.conf.old` (identical content, diff empty; both 4919 bytes).
   - limine_history retains both kernel EFI generations (2e9c9bdc for 7.2.11, 0f1e3c84 for 7.2.3).

## Rollback paths remaining

- Local package cache: NOT available (0 package files; paccache dry run finds no candidates).
- Arch Linux Archive: available for the exact installed versions (mkinitcpio 42.2-1, linux 7.2.11.arch1-1, systemd 262-1, plymouth 26.134.222-3) and for the pre-upgrade versions (mkinitcpio 41.1-1, systemd 261.2-1, linux 7.2.3.arch1-3, plymouth 26.134.222-2), each with `.sig`; requires a `pacman -U` transaction (paused host-wide; operator decision).
- Omarchy mirror: serves current mkinitcpio/linux/plymouth, cannot supply systemd 262-1 nor any pre-upgrade boot-chain package; not a boot-chain rollback source.
- Snapper / btrfs: snapshot 1 is a bootable pre-upgrade rollback via the existing limine entry (kernel 7.2.3-arch1-3 + mkinitcpio 41.1-1 userland, NVIDIA dkms modules present); snapshot 2 is the post-upgrade state; `/boot` itself is not in the snapshots but the needed EFI images are preserved in limine_history. `snapper list` requires root.
- Boot-level: current 42.2-based entries and the preserved 7.2.3 entry are both selectable; limine_x64.bak and BOOTX64.EFI fallbacks exist.
- systemd-rollback: not installed (`command -v systemd-rollback` empty). snap-pac: not installed.
- `/etc` pacnew files (3) are unrelated to the boot chain: tpm2-tss P_ECCP384SHA384.json.pacnew, P_RSA3072SHA384.json.pacnew, locale.gen.pacnew.

## Notes for the L1

- P5 premise wording fix: "package cache holds 4 files" should read "4 entry directory listings, 0 package files"; `cache-package-files` would report 0. The updated `capture.sh` adds `cache-package-files`, `cache-entries`, `paccache-runs-since-pause`, `snapper-list` sections (diff in working tree); the committed l1/l1-2/l1-3 captures predate those sections.
- The four ALA index pages were opened this session (2026-10-22) and exact quotes are listed in §3 for SOURCES row drafting.

## Scope and installs

Scope: read=/var/cache/pacman/pkg, /var/log/pacman.log, /var/lib/pacman/sync/*.db, /etc/pacman.conf, /etc/pacman.d/mirrorlist, /boot (limine.conf, limine.conf.old, EFI/Linux, 432d02b.../limine_history, loader), /.snapshots/1/snapshot, /.snapshots/2/snapshot, /usr/lib/initcpio/functions, /usr/lib/initcpio/hooks, /var/lib/dkms, /etc/pacman.d/gnupg, archive.archlinux.org index pages (mkinitcpio, linux, systemd, plymouth), stable-mirror.omarchy.org core/extra db and package probes, pkgs.omarchy.org db, snapper list (root and home configs), journalctl sudo entries, capture files (.ufo/waves/round-24/capture/l1{,-2,-3}/capture.txt), registry draft (.ufo/waves/round-24/w1/ExecRegistryRows/registry-r24.md); wrote=.ufo/waves/round-24/w1/ExecRollbackPaths.md; executed=ls, find, du, stat, paccache -d variants, pacman -Q/-Si, curl -sI/-s, snapper list (and sudo -n variants), btrfs subvolume list/show, sha256sum, grep/sed/awk/tar/gzip/python3 over downloaded db/index scratch files in /tmp.

Installs: none
