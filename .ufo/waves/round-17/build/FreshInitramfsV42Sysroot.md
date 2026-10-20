# FreshInitramfsV42Sysroot — report

## Behavior
- Appended to `corpus/knowledge/initramfs-v42-sysroot-recovery.md`: `## R17-FRESHNESS — dated host re-verification (2026-10-20)` (10 bullets) and `## R17-RECHECK — steer-safe procedure` (`ls -d` directory-name reads, no package-manager binary).
- Baseline bytes preserved: the file's first 10358 bytes equal `6923fe0bd3add04fc90f3bc3522895b27cf44bbe:corpus/knowledge/initramfs-v42-sysroot-recovery.md` [obs].
- Fragment: `.ufo/waves/round-17/build/fresh/initramfs-v42-sysroot-recovery.json`, 10 records `R17-FRESH-INITRAMFS-01..10` [obs]. Read-only check: every `baseline_quote` is in the baseline, every `capture_quote` is in its cited capture line, and every `observed_now` and `capture_ref` appears in the notice [obs].

## Stale statements flagged
- Line 9: mkinitcpio 41.1-1, plymouth 26.134.222-2, limine-mkinitcpio-hook 1.38.0-1.1, limine-snapper-sync 1.31.0-1.1, snapper 0.13.1-3 now 42.2-1, -3, 1.40.0-2, 1.32.1-2, 0.13.2-1 [obs] (`fresh-capture.txt:16-19,26`).
- Line 14: "current 41.1 image" is VERSION 42.2 [obs] (`boot-chain-capture.txt:174,190`); the v42 plus btrfs-overlayfs pairing exists (`:175,:178`).
- Line 11: UKIs were extracted; HOOKS has no systemd entry [obs] (`:170,:177`).
- Line 32: limine-update ran 09:26:11 (`:86`); boot started 09:57:09 (`:10`).
- Line 3: `pacman -Q` recheck superseded by the R17-RECHECK procedure.

## Not flagged
Line 2 verified-at, lines 10 and 12 (HOOKS and hook sweep match `:16-23`), line 13 and 28 source and R5 claims, recovery table: still true or dated.

## Unverified [unk]
- Whether OverlayFS mounted in the 09:57 boot (no capture).
- Package count: not re-measured; pacman was forbidden.
- snapper 0.13.2-1 transaction: no capture line.

## Tooling
No installs or updates. No package, service, or boot action; nothing written outside the two owned paths except this report.

Scope: executed=git show,cmp,grep,rm,python3
