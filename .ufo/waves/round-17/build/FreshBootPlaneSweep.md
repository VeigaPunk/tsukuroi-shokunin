# Fresh boot-plane sweep — stale current-use boot-chain statements (R17)

Axes: A1 statement coverage · A2 per-row path:line grounding · A3 dated-vs-current split · A4 zero edits.
Move order: 4 parallel reads → 3 line-number greps → 1 pin grep → write. No file touched but this report.
Abbrev: **BC** = `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt`; **FC** = `.../fresh-capture.txt`.

## Stale (claim is current-use in the note; host state at 2026-10-20 contradicts it)

| # | path:line | exact quote | capture now shows | verdict |
|---|---|---|---|---|
| S1 | `corpus/knowledge/journal-boot-plane.md:244-245` | "initramfs is busybox-style (`/etc/mkinitcpio.conf:55` → `HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block encrypt filesystems fsck)`)" | effective config is drop-ins (BC:16-18); both live UKIs are `VERSION 42.2`, `EARLYHOOKS="udev"`, `HOOKS="udev plymouth keymap consolefont encrypt resume"`, `LATEHOOKS="plymouth btrfs-overlayfs"` (BC:173-178, 189-194); init mounts `/sysroot` (BC:175, 24-30). None of `base/autodetect/microcode/modconf/kms/keyboard/block/filesystems/fsck` appears in the image hook list | [obs] STALE (citation + flavor). Mechanism at :245-247 survives: `encrypt` is still in image HOOKS (BC:177) |
| S2 | `journal-boot-plane.md:433-436` (2026-10-19 erratum) | "The host's `omarchy_hooks.conf` defines `HOOKS=...btrfs-overlayfs`" | quote still matches BC:17 exactly, but the erratum records config text only: no 42.2 early/late split, no `/sysroot` (BC:174-178) | [obs] INCOMPLETE-CURRENT |
| S3 | `journal-boot-plane.md:147` | "Today `snapper list-configs` still prints a header-only table, rc=0 (re-measured 11:53)." | FC:42-46 → `home /home`, `root /`; `snapper -c root create-config /` ran 2026-10-20T09:03:02 (BC:80); snapshots #1/#2 (BC:166-167) | [obs] STALE outright |
| S4 | `journal-boot-plane.md:148-149` | "snapper shows none — the rollback-net question … needs a re-audit." | same as S3; re-audit still owed, premise wrong | [obs] STALE |
| S5 | `journal-boot-plane.md:364` | "`limine-snapper-sync` … vs empty `snapper list-configs`" | `SNAPPER_CONFIG_NAME="root"` in `/etc/limine-snapper-sync.conf` (FC:71-74); configs exist (FC:42-46) | [obs] STALE premise |
| S6 | `journal-boot-plane.md:300` | "Measured UKI no) then `Failed to read "/boot/EFI/systemd"` / `Failed to open '/boot/loader/loader.conf'`" | `/boot/EFI/Linux/` holds `omarchy_linux.efi` (284439552 B, 09:26:22) and `omarchy_linux-lts.efi` (BC:124-125); `limine.conf` selects UKI paths by sha256 (BC:128-136) | [obs] privilege arm valid; [inf] false as a `/boot`-shape claim |
| S7 | `journal-boot-plane.md:13-15`; `boot-plane.md:19-21` | "Journal persists **13 boots** back to install day 2026-10-03 … **181.3 M**" | boot 0 now `3e7084f4…`, 2026-10-20 09:57:09 (BC:10); full list, oldest boot, disk use [unk] | [unk] STALE-AS-CURRENT; keep as 2026-10-14 measurement |

## Dated measurements — keep as history (do not retag stale)

- `boot-plane.md:6`, `journal-boot-plane.md:11` "kernel `7.2.3-arch1-3`": now `7.2.11-arch1-1` (BC:5; upgrade BC:51). Dated by `:8`/`:7`. 7.2.3 stays correct for the retained 41.1 UKI (BC:205) and the snapshot #1 entry (BC:152).
- `boot-plane.md:213` "kernel-phase dwell 12 s → 2 h 58 m (boot 0: 4 m 3 s)": current boot figure [unk] — neither capture runs `systemd-analyze` or greps `Startup finished` (0 matches).
- `journal-boot-plane.md:62-63` `/proc/cmdline`: BC:12 is a superset (adds `zswap.enabled=1 zswap.max_pool_percent=25 rootflags=subvol=@ rw rootfstype=btrfs`, full `:allow-discards,no-read-workqueue,no-write-workqueue`); not contradicted.
- `journal-boot-plane.md:64-65,249-252` `PM: Image not found`: 2026-10-20 occurrence [unk]; `journal-boot-plane.md:299` `ls /boot` rc=2 still consistent with mode 700 root (BC:101).

## Gaps — capture-backed facts with no statement in either note

No note names the UKI paths (`/boot/EFI/Linux/omarchy_linux{,-lts}.efi`), `/etc/default/limine` (`ENABLE_UKI=yes`, `ESP_PATH="/boot"`, `MAX_SNAPSHOT_ENTRIES=5`, FC:58-70), limine 12.9.3 / limine-mkinitcpio-hook 1.40.0-2 / snapper 0.13.2 (BC:31-39), the second kernel linux-lts 6.18.57-2 (BC:38,82), or ro=true snapshots #1=41.1 / #2=42.2 (BC:160-167).

Not verified: post-09:15 boot duration/failed units and journal retention (absent from captures); busybox presence in 42.2 init (BC extracts `init` checksum only, BC:182).

Scope: executed=none
