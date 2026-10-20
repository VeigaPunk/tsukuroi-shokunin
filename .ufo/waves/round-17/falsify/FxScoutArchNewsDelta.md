# FxScoutArchNewsDelta — attack on the arch-news-gate-2026.md R17 notice

**Verdict: SURVIVES.**

[obs] Claim (corpus/knowledge/arch-news-gate-2026.md:89): "the article's precondition is still unmet on this host" — UKIs use busybox `encrypt`, no `systemd` hook. Confirmed: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:177,193,209,225,241` show all five extracted UKIs with `HOOKS="udev plymouth keymap consolefont encrypt resume"`; no `systemd` hook anywhere in the capture. Host config agrees: `/etc/mkinitcpio.conf.d/omarchy_hooks.conf:1` `HOOKS=(base udev plymouth keyboard autodetect microcode modconf kms keymap consolefont block encrypt filesystems fsck btrfs-overlayfs)`.

[obs] Article https://archlinux.org/news/mkinitcpio-42-requires-manual-intervention-for-tpm2-based-unlocking-of-luks-devices/ § article, accessed 2026-10-20: "If you configured the systemd hook and unlock LUKS partitions, that depend on these values, you need to re-enroll". Condition absent; mkinitcpio 42.2-1 itself (`boot-chain-capture.txt:32`) is not the trigger.

[obs] No delta: https://archlinux.org/news/ § Arch Linux News Archives, newest row 2026-09-22; https://archlinux.org/feeds/news/ newest item "Tue, 22 Sep 2026"; in-range census unchanged (7×2026 + 13×2025 = 20). Nothing after 2026-09-22, hence nothing since 2026-10-20 morning.

[unk] `/etc/crypttab` unreadable (EACCES); a tpm2-device entry is not excluded, but without a `systemd` hook it cannot gate boot unlocking.

[unk] Notice's "09:15 transaction" vs capture upgrades at 09:16:28–29 (`boot-chain-capture.txt:44-45`); non-flipping.

[obs] Read-only inspection (file reads, grep, git log/status); no probes, builds, or writes.

Scope: executed=none
