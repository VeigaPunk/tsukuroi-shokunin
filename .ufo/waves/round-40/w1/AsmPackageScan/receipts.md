# AsmPackageScan receipts (2026-10-26T07:16Z, read-only)
Lane tip read: working tree at dispatch; staged dir: /home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/ (70 files).

## Cmd 1 — gate adjudication hits per staged filename (lessons round-3*.md)
for f in staged: grep -l -F "${f%.md}" corpus/lessons/round-3*.md
Non-zero: alpm-package-anatomy-r26 (2: round-38.md:49,120), errno-contract-variance-r37 (3), errno-name-discrimination-r25 (2: round-37.md:22,74; spotcheck:96),
mount-errno-contract-r26 (3), pacman-hook-timing-r25 (4: round-38.md:48; round-39.md:45-64; spotchecks). All other 65 staged names: 0 hits in lessons/round-3*.md.
Cross-ref only (no decision): initramfs-hook-api-r25 is named at .ufo/waves/round-38/w1/AsmRevTiming.md:228 ("does not exist in the lane") and round-39/w1/C2RevenStaged.md:33;
upstream-release-watch-r25 and snapper-rollback-bilingual-r25 at round-39/w1/ScoutQuarantine.md:18 ("neither exists in the lane", not adopted).

## Cmd 2 — host checks (read-only)
pacman -Q mkinitcpio pacman plymouth -> mkinitcpio 42.2-1; pacman 7.1.0.r9.g54d9411-3; plymouth 26.134.222-3
man -P cat mkinitcpio | grep: lines 239-256 list run_earlyhook, run_hook, run_latehook, run_cleanuphook, run_emergencyhook with the staged wording
/usr/lib/initcpio/hooks/*: btrfs run_hook; btrfs-overlayfs run_latehook; consolefont/encrypt/keymap/memdisk/resume/sleep run_hook; plymouth run_hook run_latehook run_emergencyhook;
  shutdown run_cleanuphook; udev run_earlyhook run_hook run_cleanuphook; usr run_latehook
/etc/mkinitcpio.conf.d: HOOKS=(base udev plymouth keyboard autodetect microcode modconf kms keymap consolefont block encrypt filesystems fsck btrfs-overlayfs) [+ resume]
curl https://archlinux.org/news/mkinitcpio-hook-migration-and-early-microcode/ (2026-10-26T07:16Z) -> 200; "2024-03-04 - Morten Linderud"; "moved to the mkinitcpio upstream project. The hooks are: systemd, udev, encrypt,"; "conflicts have been introduced into the respective packages to prevent installing packages"
man -P cat PKGBUILD | grep: line 279 "Note that during an upgrade operation, none of the install or remove functions will be called."; package() text says "run inside" $srcdir (lines 228, 237-244)
Registry: corpus/SOURCES.md last id S225 (grep -o '^| S[0-9]* ' | tail -1); lane S200-S225 all taken, staged S200-S225 collide with different documents.
