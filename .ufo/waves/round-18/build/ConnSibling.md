# ConnSibling — R18

Model grok-4.7-fast. Axes: C1 depth, C2 operability, C3 freshness, adjacency. Dead `FxConnSibling` (r17 falsify, 429) asked if r17 tsukuroi host claims contradict sibling r17/r18 reports. Read-only. Route, do not absorb.

## Evidence

[obs] Absent: `.ufo/reports/round-17/{mori,kama}.md`, `round-18/{mori,kama}.md`. Present: r17 kaidoku, kagi, tabi; r18 kaidoku.

[obs] No boot-verdict clash. `round-17/mado.md:159`: 13 runs 07:45–09:39, mkinitcpio 41.1→42.2, "no recorded actor." `round-17/tsukuroi.md:14` already assigns those 13 to account `vgpnk`. `mori-shokunin/PROVINCE.md:112-115` names 09:15:30 `-Syu` and 13:23:08 `-U` zcode; zcode's human actor stays inferred. It omits 09:31 elephant `-U` (`host-capture-r18.txt:71`). Boot verdicts ignore actor.

[obs] Memory staleness is local. `oom-event-plane.md:51,:345` earlyoom absent; `:348` `zswap.enabled=0`. Capture `:16-18` earlyoom active/enabled; `:9-14` `zswap.enabled=1`, Y/25/zstd. Mori `:12-14` refuses unit/boot; `:53` means inactive≠zero, not "earlyoom is down."

[obs] Packages. Kaidoku `PROVINCE.md:40` dates that table 2026-10-13; `:62` lists pacman-contrib absent. Capture `:36` `pacman-contrib-1.13.1-1`; `:83` `/usr/bin/paccache`. `:50` cache 1,350 ≠ installed 1395 (`:25`). Kaidoku r18 `:90` (Go) and kama `PROVINCE.md:55-69` (llama-server) are `~/.local/opt`, outside `-Qm`. Kagi `:10-17` marks `:42` "live" 34113 historical; kama `:19-20` says 8080 and 34113 DEAD. Kagi `:63` leaves 1Password packages here. Tabi `PROVINCE.md` has no boot/memory/package sentence; `tabi.md:130` is only no pacman transaction.

[obs] Mori `:66` cites tsukuroi `PROVINCE.md:21-24`. Those lines are now pacnew/initramfs/snapper. Memory handoff is `:30-33` and ADJ-04 `:49`. Pin drifted; ownership holds.

## Move

Improves C3, harms none. One lane-report pointer, not a record or census arm: C1 fixes must not copy "no actor"; C3 earlyoom/zswap notices quote capture `:9-18`, not mori `:53` or kaidoku `:62`; no `~/.local` arm; do not equate 1,350 with 1395. Rejected: sibling edits, kagi `:42` as current, uninstall here.

## Risks

[unk] pacman-contrib on 2026-10-13. [unk] whether elephant `-U` ran a UKI hook. Pacman not re-run.

## Verification

Re-read cited lines. No systemctl or pacman. Pointer stays out of `PROVINCE.md` and sibling repos.

Scope: executed=python3,wc. No install.
