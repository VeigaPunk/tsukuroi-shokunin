source: S051 .ufo/waves/round-17/l1-capture/boot-chain-capture.txt; S052 .ufo/waves/round-17/l1-capture/fresh-capture.txt; S055 .ufo/waves/round-17/l1-capture/overlay-emulation.txt; S056 .ufo/waves/round-17/l1-capture/supplement-capture.txt (own-work, L1 read-only captures 2026-10-20); S054 https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init § init:66-67,110; S053 https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases § CHANGES WITH v42, v42.1, v42.2; S057 https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/merge_requests/482 § description; S021 https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs § run_latehook; S022 https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook § run_latehook; S015/S016 (v42 notes and init).
verified-at: 2026-10-20 (L1 extracted every limine UKI's initramfs read-only, read the firmware loader variables, and emulated the overlay hook's path handling in an unprivileged namespace; S021, S022, S053, S054, S057 opened the same day).
recheck: on-release; procedure: `bash tools/boot-chain-audit.sh --live` (read-only: `sudo -n` is used only to read /boot files and snapshot properties, all extraction runs in a private mktemp directory; it never writes /boot); re-run after any mkinitcpio, kernel, plymouth, limine-mkinitcpio-hook or limine-snapper-sync change and before relying on a snapshot entry. No pacman invocation.

# Boot chain after the 2026-10-20 mkinitcpio 42.2 upgrade — next-boot verdict per limine entry

Machine-readable twin: `corpus/knowledge/boot-chain-r17.json` (schema `tsukuroi-boot-chain-v2`).
Line references: `B:` boot-chain-capture.txt, `F:` fresh-capture.txt, `E:` overlay-emulation.txt,
`S:` supplement-capture.txt (all under `.ufo/waves/round-17/l1-capture/`).
Authority: observation, namespace emulation and source-grounded inference only. Nothing here
authorizes a package, service, initramfs, bootloader or `/boot` change.

## What ran

- [obs] The sudo journal attributes every pacman run 07:45–09:39 to account `vgpnk` (B:76–96);
  4 of the 13 ran from `/home/vgpnk/tmp`, the rest from `~/Documents/nvhelpme` or `/home/vgpnk` (B:76–97). Operator attribution is [inf].
- [obs] 09:03:02 root snapper config and snapshot #1 `pre-nvme-baseline-2026-10-20` were
  created (B:80–81, B:166).
- [obs] 09:15:30 `pacman -Syu --needed --noconfirm` plus 13 named packages (B:59, B:82): 448
  `[ALPM] upgraded|installed` records in that transaction's log lines 2462–3063 (S:124–125);
  mkinitcpio 41.1-1→42.2-1, linux 7.2.3→7.2.11, systemd 261.2→262, plymouth
  26.134.222-2→-3, limine-mkinitcpio-hook 1.38.0-1.1→1.40.0-2, limine-snapper-sync
  1.31.0-1.1→1.32.1-2, nvidia-open-dkms 610.57.04→615.78.08, linux-lts 6.18.57-2 installed
  (B:44–53).
- [obs] 09:18 the pacman hook built both UKIs (B:69–74). 09:26:11 account `vgpnk` ran
  `limine-update` via sudo (B:86; operator attribution [inf]). [inf] It rebuilt both UKIs outside any pacman transaction: `/boot/EFI/Linux`
  mtimes 09:26:16 / 09:26:22 (B:124–125); the last UKI build lines in pacman.log are the 09:18
  ones (B:68–74).
- [obs] 09:29:19 snapshot #2 `pre-aur-elephant-2.22.1` (B:88, B:167); `limine_history` holds
  copies of the then-current UKIs dated 09:29:18 (B:115–116). [inf] limine-snapper-sync made the
  copies at snapshot time (RevLimineSnapperSync seat report, source 1.32.1).
- [obs] `/etc/fstab` was installed three times (09:19:40, 09:38:14, 09:48:47; B:85, 94, 97).
  Boot −1 ended 09:56:15; boot 0 started 09:57:09 on 7.2.11 (B:5–10).
- [obs] 12:07:07 `snapper-cleanup` ran and limine-snapper-sync logged
  `Updated: /boot/limine.conf` (S:118–122). [inf] That write explains the file's 12:07:06 mtime
  (B:106; FAT 2-second timestamps).

## Image facts

- [obs] Both current UKIs are mkinitcpio `VERSION 42.2`; their `init` has 7 `/sysroot` and 0
  `/new_root` references (B:174–175, 190–191) and equals the installed `/usr/lib/initcpio/init`
  (B:182, 251).
- [obs] Their `LATEHOOKS="plymouth btrfs-overlayfs"` (B:178, 194); the hooks still say
  `root_mnt="/new_root"` (btrfs-overlayfs:4) and `--new-root-dir=/new_root` (plymouth:11)
  (B:179–180), byte-identical to the installed hooks (B:183–184, 252–253). The upstream files
  re-opened today contain the same two strings (S021, S022).
- [obs] In all four extracted 42.2 images `/new_root` is a relative symlink `new_root -> sysroot`;
  the 41.1 image has a real `new_root` directory (E:51–66; E:8 `lsinitcpio -v`). [inf] Every
  42.x build does the same: `initialize_buildroot` creates it (`/usr/lib/initcpio/functions:1212-1213`,
  E:9–10), and the maintainer merge request for v42 says “/new_root will be kept as a symlink to
  /sysroot” (S057).
- [obs] The image's `findmnt` and `mount` are byte-identical to the host's util-linux 2.42.4
  binaries (E:11–15).
- [obs] Emulation in an unprivileged user+mount namespace (tmpfs standing in for btrfs) of the
  hook's path steps: `findmnt --mountpoint <R>/new_root` returns the `<R>/sysroot` mount (rc 0;
  E:40–42); `mount --move <R>/new_root` succeeds; the overlay mounted on `<R>/new_root` appears
  on `<R>/sysroot`, and a write after it lands in the overlay's upper layer (E:43–48). The
  emulated root was a writable tmpfs, so it shows the path handling, not a read-only root made
  writable; the hook's `ro=true` branch was not emulated.
- [inf] Therefore, under a 42.2 image, the btrfs-overlayfs hook reaches its btrfs checks and,
  for a read-only snapshot root, mounts the overlay where v42 `init` will `switch_root`. The
  btrfs-specific steps (`FSTYPE` btrfs, `/snapshot` source path, `btrfs property get … ro`)
  were not emulated; they follow the same kernel path resolution.

## Decision table

| entry | image sha256 | VERSION | init root | image `/new_root` | root | verdict | evidence |
|---|---|---|---|---|---|---|---|
| `linux` (`//linux`, default) | `2e9c9bdc…` | 42.2 | /sysroot | symlink → sysroot | `subvol=@` | **BOOTED-OBSERVED** | B:5–14, 124, 171–180, 256–258; S:34–35, 113–115; E:59–61 |
| `linux-lts` | `2d49da06…` | 42.2 | /sysroot | symlink → sysroot | `subvol=@` | **UNTESTED** | B:125, 187–200; S:42–43; F:36; E:53–55 |
| `snapshot-2/linux` | `2e9c9bdc…` | 42.2 | /sysroot | symlink → sysroot | `/@/.snapshots/2/snapshot`, ro=true | **PATH-ALIASED-EMULATED** | B:115, 161, 219–229; S:54–55; E:40–48, 64–66 |
| `snapshot-2/linux-lts` | `2d49da06…` | 42.2 | /sysroot | symlink → sysroot | `/@/.snapshots/2/snapshot`, ro=true | **PATH-ALIASED-EMULATED** | B:116, 161, 235–245; S:60–61; E:40–48, 56–58 |
| `snapshot-1/linux` | `0f1e3c84…` | 41.1 | /new_root | directory | `/@/.snapshots/1/snapshot`, ro=true | **CONSISTENT-PRE42** | B:114, 160, 203–213; S:68–69; E:62–63 |
| `efi-fallback` | `94308b4e…` (= limine_x64.efi) | — | — | — | — | NOT-A-KERNEL-ENTRY | S:71–76, 93–95 |

Rules, first match (identical in the JSON): no initramfs → NOT-A-KERNEL-ENTRY; firmware
`LoaderEntrySelected` names the entry, the image equals the file that booted and none of the
nine boot-input paths swept at B:256 is newer than the boot → BOOTED-OBSERVED; a non-snapshot entry that has not
booted → UNTESTED; `/sysroot` init + `/new_root` symlink to sysroot + `/new_root` hooks →
PATH-ALIASED-EMULATED; `/new_root` init + `/new_root` directory + `/new_root` hooks →
CONSISTENT-PRE42; otherwise UNTESTED. Each `path:` `#` hash equals the image's b2sum
(S:34/B:172, S:42/B:188, S:54/B:220, S:60/B:236, S:68/B:204).

## Next-boot verdict

- [obs] **Default entry — booted this image.** Firmware variables written by Limine 12.9.3 name
  the booted entry `Omarchy.linux` / `Omarchy/linux` (S:113–115); `/proc/cmdline` and the root
  mount show `rootflags=subvol=@` (B:12, 14). The image file (mtime 09:26:22) is byte-identical to
  the 09:29:18 history copy (B:115, 171, 219). Of the nine boot-input paths swept at B:256
  (`/etc/fstab`, `/etc/crypttab`, `/etc/mkinitcpio.conf`, `/etc/mkinitcpio.conf.d`,
  `/etc/default/limine`, `/etc/limine-snapper-sync.conf`, `/usr/lib/initcpio`, and the 7.2.11 and
  6.18.57-lts module trees), none holds a file newer than the boot (B:257: count 0; B:258: 58674
  files under the last three). `/boot` was not in that sweep: `/boot/limine.conf` changed at 12:07
  (S:121), and its `//linux` hash still matches this image's b2sum (S:34, B:172).
  [inf] The next default boot repeats this boot unless one of those inputs changes first.
- [inf] **linux-lts — untested.** [obs] It has never booted: it was installed at 09:16:29 (B:46);
  boot −1 started 08:57:58, before that install, and boot 0 runs 7.2.11 (B:5, B:8–10). Same `init` and hook bytes as the booted image (B:198–200 =
  182–184) with a different kernel and its own nvidia 615.78.08 DKMS build (F:36). It is a
  fallback for a 7.2.11 kernel or driver regression, not for an initramfs problem.
- [inf] **Snapshot #2 entries — overlay expected.** They boot the same 42.2 bytes into a
  read-only subvolume; the hooks' `/new_root` resolves through the symlink, so the overlay
  should mount (E:40–48). The snapshot's own `/etc/fstab` predates the 09:38/09:48 edits and
  lacks only the `/tmp` and `/fast` XFS lines (both `nofail`) and the `/dev/shm` cap (S:127–137).
  Not boot-tested.
- [inf] **Snapshot #1 entry — consistent pre-42 rollback.** 41.1 `init` and a real `/new_root`
  directory match both hooks (B:206–213, E:7); its cmdline is the pre-09:19 one with
  `zswap.enabled=0` (S:69). Not boot-tested. It is the only pre-upgrade rollback and has
  cleanup algorithm `number` (B:166).
- [inf] **EFI fallback is not independent.** [obs] `BOOTX64.EFI` is byte-identical to
  `limine_x64.efi` (S:94–95). [inf] It reopens the same Limine menu.

## Operator checks before the next reboot

Checks (read-only) and operator-only actions; tsukuroi takes none of these actions:

1. Check, just before rebooting: re-run the recheck procedure; the `//linux` block of
   `/boot/limine.conf` and the sha256 of `/boot/EFI/Linux/omarchy_linux.efi` are unchanged, and
   no one-shot or firmware next-boot request is pending (`LoaderEntryOneShot` absent from
   `/sys/firmware/efi/efivars`, `efibootmgr` shows no `BootNext`; fwupd was installed at 09:27,
   B:60). Any change voids BOOTED-OBSERVED for the next boot. [inf] `default_entry: 2`
   selects `//linux` because Limine numbers the expanded `/+Omarchy` directory row 1 and no
   `remember_last_entry` is set (S:5–24; wave-2 FxScoutLimineDocs).
2. Operator action, optional: keep snapshot #1 (the only pre-upgrade image) — snapper number
   cleanup can delete the snapshot, and limine-snapper-sync prunes menu entries by
   `MAX_SNAPSHOT_ENTRIES=5` and `LIMIT_USAGE_PERCENT=85` (F:68, F:72); how pruning treats a
   pinned snapshot was not checked.
3. Operator action, optional: [unk] the sudo journal records a LUKS header backup at 09:03
   under `/var/backups/` (not in a capture file). A header backup plus any passphrase valid at
   backup time decrypts the disk even after the passphrase changes (cryptsetup-luksHeaderBackup(8)):
   keep any copy encrypted and offline, and destroy it after a passphrase change.
4. Operator action: keep external boot media available; the EFI fallback entry is Limine itself.

## Falsifier

- BOOTED-OBSERVED for `linux` is falsified by a loader variable naming another entry or a
  booted image whose sha256 differs from `2e9c9bdc…`.
- PATH-ALIASED-EMULATED is falsified by a snapshot-#2 boot whose root is not an `overlay`
  mount (`findmnt -no FSTYPE /` ≠ `overlay`), or by a 42.x image whose `/new_root` is not a
  symlink to `sysroot`.
- CONSISTENT-PRE42 is falsified by a snapshot-#1 boot whose root is not an overlay.

## Rejected readings

- **“42.2 images carry an empty `/new_root` directory, so the overlay hook silently no-ops and
  snapshot boots are degraded.”** Rejected: this was the first L1 draft and the first L0 line
  of this round; `/new_root` is a symlink to `sysroot` (E:51–66) and the emulated hook path
  works (E:40–48). The `dirs:` label at B:181/197 lists names only; the L1 produced it with a
  name-only listing (`ls -d`, command not recorded in the capture). Correction filed as an L0 line the same day.
- **“linux-lts protects against an initramfs hook problem.”** Rejected: identical `init`/hook
  bytes (B:198–200 vs 182–184).
- **“The successful 09:57 boot proves snapshot rollback works.”** Rejected: the default root is
  a writable subvolume; the overlay path was not exercised by that boot.
- **“No pacman.log rebuild after 09:18 means the booted UKI is the 09:18 build.”** Rejected:
  [inf] `limine-update` at 09:26:11 rebuilt it outside pacman (B:86, 124–125).
- **“The `/EFI fallback` entry is a separate rescue path.”** Rejected: same Limine binary (S:94–95).

## QUALITY check

1. Falsifiable: hashes, loader variables, the emulation and the Falsifier are re-runnable.
2. Each claim cites a capture line, S-row, file or seat report; the LUKS backup location (operator check 3) comes from the sudo journal and is marked as such.
3. `[obs]`/`[inf]` separate measurement from inference; btrfs-specific hook steps stay [inf].
4. New entry; older entries receive appended dated notices only.
5. The withdrawn degraded reading is kept under `## Rejected readings`.
6. No pacman action is advised; the recheck invokes no pacman.
7. External claims cite S015, S016, S021, S022, S053, S054, S057 (tier A, scoped rows).
8. `source:`, `verified-at:`, `recheck:` present; the recheck tool is `tools/boot-chain-audit.sh`.
9. Negative claims carry their sweep: “no newer input” (B:256–258, nine named paths); “no
   `/new_root` note in v42.1/v42.2” (S053, the three release descriptions read in full).
10. Superseded current-use mentions in six older entries carry R17 freshness notices (`corpus/knowledge/freshness-recheck-r17.json`).
11. The landing commit carries the round-17 LOG entry.
12. No mechanism is marked unknown because a tool was absent.
13, 15–18, 20. Not applicable (no EACCES, root-metadata, unit-permission, bot-attribution or comment-ID claims).
14. This section evaluates criteria 1–27.
19/21/22/23. Sources carry heading/fragment, quote and access date in `corpus/lessons/round-17.md` `## Gate`; no absence is asserted beyond the named sweeps.
24/26. Seats ran no host probes for this entry; the L1 captured, with its own `pacman -Q` breach recorded as R17-STEER-SCOPE.
25. Verdicts come from typed image facts bound to the booted entry (S:113–115) and image hash.
27. Gate measurements name landed hex revisions only.

## Sources

- **S051, own-work, A** — boot-chain capture (B:).
- **S052, own-work, A** — freshness capture (F:).
- **S055, own-work, A** — symlink listing and namespace emulation (E:).
- **S056, own-work, A** — supplement capture: full limine.conf, loader variables, fallback hash, snapshot fstab diff, count recheck (S:).
- **S054, code, A** — v42.2 `init`: “Mount root at /sysroot” (init:66); `/usr/bin/switch_root /sysroot` (init:110).
- **S053, docs, A** — v42: “Busybox-based init now uses /sysroot as the root mountpoint”; v42.1/v42.2 change ESP directory creation and systemd-hook units only.
- **S057, code, A** — mkinitcpio MR !482: “/new_root will be kept as a symlink to /sysroot”.
- **S021, code, A** — `root_mnt="/new_root"`; `findmnt --mountpoint "$root_mnt" -no FSTYPE … || return 0`.
- **S022, code, A** — `plymouth update-root-fs --new-root-dir=/new_root`.


## R18-CORRECTION — :19 transaction names 12 packages, not 13

- [obs] Correction R18 (C1), source S051 (`corpus/SOURCES.md:57`, own-work, tier A). Corrected reference: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:59`.
- Superseded text, kept in the historical bytes: "plus 13 named packages (B:59, B:82)".
- Corrected: plus 12 named packages (B:59). B:59 lists nvme-cli, smartmontools, fio, xfsprogs, pacman-contrib, earlyoom, iotop-c, sysstat, stress-ng, btrbk, linux-lts and linux-lts-headers. B:82 is a truncated history display, not the complete counted argv.
- Reason: B:59 names 12 packages, not 13 (count slip, closure defect 3).
- Now: plus 12 named packages (B:59)
- Scope: historical snapshot preserved; this notice supersedes the current-use reading only. Read-only record; it clears no package, reboot, or boot-chain action.

## R18-CORRECTION — :40-42 init equality also cites linux-lts image (B:198)

- [obs] Correction R18 (C1), source S051 (`corpus/SOURCES.md:57`, own-work, tier A). Corrected reference: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:198`.
- Superseded citation, kept in the historical bytes: "(B:182, 251)." for both UKIs.
- Corrected: "and equals the installed `/usr/lib/initcpio/init` (B:182, 198, 251)". B:182 is the linux image init, B:198 the linux-lts image init (same sha256 `62fcc3a9…`), B:251 the installed file.
- Reason: Both-UKI init equality cited only the linux image (B:182, 251); the linux-lts image init is B:198 (closure defect 3).
- Now: and equals the installed `/usr/lib/initcpio/init` (B:182, 198, 251)
- Scope: historical snapshot preserved; this notice supersedes the current-use reading only. Read-only record; it clears no package, reboot, or boot-chain action.

## R18-CORRECTION — :43-46 hook identity also cites linux-lts image (B:199–200)

- [obs] Correction R18 (C1), source S051 (`corpus/SOURCES.md:57`, own-work, tier A). Corrected reference: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:199` and `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:200`.
- Superseded citation, kept in the historical bytes: "byte-identical to the installed hooks (B:183–184, 252–253)".
- Corrected: "byte-identical to the installed hooks (B:183–184, 199–200, 252–253)". B:199 (btrfs-overlayfs, `eeac1ed3…`) and B:200 (plymouth, `de852646…`) are the linux-lts image hooks, equal to B:252–253.
- Reason: Both-UKI hook identity cited only the linux image hooks (B:183–184); the linux-lts hook hashes are B:199–200 (closure defect 3).
- Now: byte-identical to the installed hooks (B:183–184, 199–200, 252–253)
- Scope: historical snapshot preserved; this notice supersedes the current-use reading only. Read-only record; it clears no package, reboot, or boot-chain action.

## R18-CORRECTION — :88 image mtime 09:26:22 cites B:124, not B:115

- [obs] Correction R18 (C1), source S051 (`corpus/SOURCES.md:57`, own-work, tier A). Corrected reference: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:124`.
- Superseded citation, kept in the historical bytes: "the 09:29:18 history copy (B:115, 171, 219)" for the image mtime.
- Corrected: the image mtime 09:26:22 is B:124. B:115 remains the citation for the 09:29:18 history copy, which is the object it lists.
- Reason: The mtime 09:26:22 belongs to /boot/EFI/Linux/omarchy_linux.efi at B:124; B:115 is the 09:29:18 history copy (closure defect 3).
- Now: The image file (mtime 09:26:22, B:124) is byte-identical to the 09:29:18 history copy (B:115, 171, 219).
- Scope: historical snapshot preserved; this notice supersedes the current-use reading only. Read-only record; it clears no package, reboot, or boot-chain action.

## R18-SOURCE-SCOPE — tagged init versus host-byte equality

S058 supersedes the historical S054 teaching for the tagged v42.2 init: its `# Mount root at /sysroot` statement and `switch_root /sysroot` are source facts. Equality with these two host UKIs is separately established by S051, capture B:182/198/251; hooks by B:183–184/199–200/252–253. Earlier S054 citations above are historical locators, not the active broader teaching. Existing next-boot verdicts and their emulation/boot limits remain unchanged. W04 duplicate rows are retained, never merged. Source: S058, S051; opened2026-10-20.
