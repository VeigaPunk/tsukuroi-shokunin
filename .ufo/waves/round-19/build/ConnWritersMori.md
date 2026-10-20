# ConnWritersMori

Model: Grok 4.7 (cursor/grok-4.7-fast). Axes: C2 writer-class depth; C1 pointer stability. C3 untouched.

[obs] No contested claim. Pin `tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md:12-14` refuses “boot state (→ tsukuroi)”. `:111-116` is detection only: 09:15:30 `pacman -Syu`, 13:23:08 `pacman -U …zcode…`, and “boot-chain interpretation/recovery remain tsukuroi/operator-owned.” Live `mori-shokunin/PROVINCE.md` matches those lines. `mori-shokunin/SKILL.md:143-145` refuses pacman/systemd/boot ownership. Neither file contains `limine`, `snapper`, or `/boot`.

[obs] `limine|snapper|/boot` is absent from all eight pinned sibling snapshots and from live PROVINCE.md in mado, tameshi, souji, kaidoku, kama, lore, kumitate, kengaku, kasegi, kake, kagi, kotoba, tabi, kotodama, audio, game-dev-2d, game-dev-3d, revenger, and chousa. Sole hit: `tsukuroi-shokunin/PROVINCE.md:11,22-23`.

[obs] Actor is not a writer class. `mori-shokunin/.ufo/waves/round-17/build/PacmanActorTrace.md:12-17` names one OMP session for the `-Syu` and yay for zcode (human actor inferred). The two C2 scriptlet writes sit inside that `-Syu`: `host-capture-r19.txt:576-598` (`Updated: /boot/limine.conf` at 09:18:18 and 09:18:24). The following name `99-limine.hook` (`:598`) has an Exec that only copies `BOOT*.EFI` (`:399-403`). [inf] That hook name is not the limine.conf writer. [obs] 13:23 is `10-limine-snapper-lock.hook` (`:605`), not an `Updated:` line. Existing mori outbound pointers (`tsukuroi-shokunin/PROVINCE.md:33,49-50`) cite `:6-16`, `:3-16`, and `:12-16` (fleet/OOM), not `:111`.

Move: one retention note, recipient none. Do not absorb. Keep the OMP/yay actor trace out of `attributed_events`. Treat 09:15 only as the envelope of pacman.log lines 3015 and 3047. Exclude 13:23 and `99-limine.hook` from the 12. Do not retarget the three mori pointers at `:111-117`. Any new anchor is an eleventh quote from pin `:111-116`.

Risk: recipient=mori reverses ADJ-04 and hands writers away. An OMP-session writer class fails the unit/hook/plugin shape.

Verify: `attributed_events` is 12; no class is mori, OMP, or yay; 13:23 is absent; the original ten pointer ranges stay put.

Scope: executed=none
