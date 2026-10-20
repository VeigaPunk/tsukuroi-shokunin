# Sweep08 — arch-news-gate-2026.md C3 (R18)

Baseline `842a5312`; working tree identical (`git diff` empty). Read-only.

## Stale current-use (1)

[obs] NVIDIA “Fresh host check” (baseline:28): `` `nvidia-open-dkms 610.57.04-1` ``. Now `/var/lib/pacman/local/nvidia-open-dkms-615.78.08-1` (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:35`). S051 dates 610.57.04-1→615.78.08-1 at 2026-10-20T09:16:44 (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:52`); S052 lists “NVIDIA 610.57.04” as no longer holding. The 2026-10-19 value was true then; only current use is superseded. Gate reading survives: 615.78.08 > announced 590; GPU generation unprobed.

Record `R18-FRESH-SWEEP08-01` (`path` `corpus/knowledge/arch-news-gate-2026.md`): `baseline_quote` `` `nvidia-open-dkms 610.57.04-1` ``; `capture_quote` `/var/lib/pacman/local/nvidia-open-dkms-615.78.08-1`; `capture_ref` `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:35`; `now` `2026-10-20`; `notice_heading` `## R18-FRESHNESS — NVIDIA open-module host check superseded (2026-10-20)` (absent baseline).

```markdown
## R18-FRESHNESS — NVIDIA open-module host check superseded (2026-10-20)

Appended 2026-10-20 by the tsukuroi round-18 L1; earlier bytes unchanged. Historical captures stay true at their date; this supersedes current use only. Read-only: no package, service or boot action authorized.

- Old (2025-12-20 “Fresh host check”): `nvidia-open-dkms 610.57.04-1`. [obs] Installed now: `/var/lib/pacman/local/nvidia-open-dkms-615.78.08-1` (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:35`); S051 dates the upgrade 2026-10-20T09:16:44 (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:52`); S052 records 610.57.04 as no longer current. [inf] Gate reading stands: 615.78.08 is beyond the announced 590 transition; GPU generation unprobed, so Pascal-or-older is the live check. Capture: `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:35`.
```

## Already superseded

[obs] `mkinitcpio 41.1-1` and its below-threshold reading are superseded by baseline `## R17-FRESHNESS` (:89); R18:34 reconfirms 42.2-1. No second notice.

## Bounded no-evidence

[unk] 14 package rows and the AUR `pacman -Qm` **16** count have no probe; R18:72-73 yay `-U` upgrades neither confirm nor contradict the count. Within 7d recheck (2026-10-19). Five-name repo list corroborated (R18:42-46, :49-53). No other stale guidance.

[obs] S060 row uncommitted (worktree `corpus/SOURCES.md:66`, absent HEAD); land with notice.

Scope: executed=read-only git show/diff/status, grep, nl, sed, python3; no host probes or gates; only this report written.
