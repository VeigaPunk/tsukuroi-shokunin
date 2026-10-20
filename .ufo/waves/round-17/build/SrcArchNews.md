# SrcArchNews — Arch news vs. boot-chain packages

Opened `https://archlinux.org/news/` (access 2026-10-20), heading `Arch Linux News Archives`; freshness cross-checked against `https://archlinux.org/feeds/news/`.

**[obs] Window 2026-10-01..2026-10-20 contains ZERO news items.** Newest index row: `2026-09-22 | Mkinitcpio >=42 requires manual intervention for TPM2-based unlocking of LUKS devices | David Runge`. The feed's newest entry is the same item (`Tue, 22 Sep 2026 09:09:27 +0000`).

**[obs] No item anywhere in the index mentions systemd 262, plymouth, linux 7.2, or nvidia 615.** The nvidia item is 2025-12-20 and covers 590/open-module, not 615.

Opened the 42.x article: `https://archlinux.org/news/mkinitcpio-42-requires-manual-intervention-for-tpm2-based-unlocking-of-luks-devices/`, fragment "Starting with package version": "Starting with package version `42-1`, the mkinitcpio systemd hook now includes `systemd-pcrosseparator.service`". Also: "If you configured the systemd hook ... you need to re-enroll the TPM2 in use."

**[inf] Inapplicable to this host**: effective UKI HOOKS are `"udev plymouth keymap consolefont encrypt resume"`, no `systemd`/`sd-encrypt` (`l1-capture/boot-chain-capture.txt:177`, cmdline `cryptdevice=` at `:12`). PCR-re-enrollment is scoped by the article's own precondition.

**Does NOT establish**: any announcement of mkinitcpio 42's `/new_root`→`/sysroot` init move — no news item covers it, so news cannot corroborate or clear the `btrfs-overlayfs:4` / `plymouth:11` hazard (`boot-chain-capture.txt:179-180`). Nothing on plymouth 26 or limine.

**[unk]** `/etc/crypttab` unreadable (EACCES, 0600 root); TPM2 keyscript presence unverified.

Scope: executed=ls, grep, wc, tail, pacman -Qo
