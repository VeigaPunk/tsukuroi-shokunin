# ConnFreshCoverage — defect5 × eight scribes

Axes: C3 freshness (defect5 only), calibration, depth.

## Join [obs]

Eight freshness scribes match defect5 (`round-17-verifier-spotcheck.md:207-213`) and `SCORECARD.md:526`. NoticeBootCorrections is C1. Matched lines: SKILL 118, 129-133, 135, 1833; health 301-306, 591-594; journal 147-149, 364-365; package 44, 75, 82, 90, 112, 143, 277-279, 310; aur 47, 48, 98, 103, 197; foreign 29-37, 47, 55, 194; oom 51, 280; kill 256, 259, 265. Package `now` is `host-capture-r18.txt:25` `1395`, not R17 `fresh-capture.txt:31` `1394`.

## Uncovered [obs]

- `oom-event-plane.md:345` is earlyoom not-found; `:346` is MemoryHigh. `:348` is `zswap.enabled=0`; `:349` is oom_score_adj. `:384` matches. Prompt 346/349 miss defect5.
- `host-health-report-r3.md:283-289` still says configure Snapper. Not in NoticeHealth. `host-capture-r18.txt:76-77` lists `home` and `root`.
- `SKILL.md:120-121` says a 7.1.4 dkms row is present. `host-capture-r18.txt:93-95` lists 6.18.57, 7.2.11, and 7.2.3 only.
- `package-state-plane.md:86` repeats 1188; `:48-57` still lists elephant 2.21.0-1. A `:44`-only quote misses them. `host-capture-r18.txt:30` is `elephant-2.22.1-1`.

## Cleared [obs]/[unk]

Keep historical or unmeasured: Oct 13 kill story; oom `:305`; kill 255, 257-258, 260-264, 266; foreign `:194` (`-U` at `host-capture-r18.txt:72-73`, not `-Syu`); pending counts (no `-Qu`, never 0); keyring “≈ Oct 11” (`:28` `20260909-1`, `:90` mtime 2026-09-09); journal `:13-14`; `boot-plane.md`. Journal `:244-245` cfg is already corrected at `:432-436`; image hooks are `boot-chain-capture.txt:176-178`. update-safety `:513` / v2 `:383` / v3 `:410` repeat 41.1/413 outside the eight (`v3:437` leaves the banner). Sweep05–07. Not in the C3 denominator.

## Move

Oom quotes only from `:345` and `:348`, plus `:51`, `:280`, `:384`. One health record for `:283-289`. Fold SKILL `:120` and the census versions into existing `now`. Reject `-Syu`-updated-elephant and keyring-updated-Oct-20.

Risk: wrong oom lines harm calibration. Skipping J4 leaves a live unblock. A HOOKS rewrite of conf bytes or boot verdicts harms depth.

Check: `baseline_quote` on that line; `capture_quote` a substring of the capture line. Count only with `check-appended-notices.py`.

model: grok-4.7-fast.

Scope: executed=none
