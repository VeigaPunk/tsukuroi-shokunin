# ConnSiblingOverlapB — mado / mori / tameshi

Model: cursor/grok-4.7-500k-fast. Author-side route note only. Axes kept: ownership separation, C2 writer attribution, ADJ route fidelity. No install.

## Shared surfaces (acknowledge, do not absorb)

- **OOM/kill (ADJ-04).** Tsukuroi keeps OS memory, journal, and boot diagnosis; cumulative counters are not dated incidents (`PROVINCE.md:30-33,49`). Mori snapshot `91940fa` and live `mori-shokunin/PROVINCE.md:6-16,24` own catalog-ID kill/OOM records, signal-11 coredumps, cgroup `memory.events`, and fleet correlation; they refuse OS/package/unit/boot state and route non-fleet `UNIT_FAILURE_OUT_OF_SCOPE` back here. Mori Adjacent names tsukuroi the only R12 hit for `systemd-oomd`/`earlyoom`/`memory.events`/`MESSAGE_ID` and calls that adjacent host diagnosis, not contested fleet ownership (`mori PROVINCE.md:66`). Packet `TSUKUROI-F1-MEM-01` stays `prepared`; mori places fleet activity at 04:53:46Z and records zero bounded notices — not cause (`:82-90`). [obs]
- **pacman.log detection.** Live mori only, heading `## Round-17 appended scope and closure notes (2026-10-20)`, line 111: `Adjacent tsukuroi handoff, detection only`. It records 09:15:30 `pacman -Syu` and 13:23:08 `pacman -U …zcode…`, evidence in mori `.ufo/waves/round-17/build/PacmanTxnToday.md` / `PacmanActorTrace.md`, and says package and boot-chain interpretation stay tsukuroi/operator-owned (`mori PROVINCE.md:111-117`). The pinned snapshot ends at line 95 and does not contain this paragraph. [obs] [unk] whether that live append is committed past `91940fa`.
- **Boot/limine is C2, not mori's.** Captures attribute `/boot/limine.conf` writes to tsukuroi mechanisms: drop-in `ExecStopPost=limine-snapper-sync` (`host-capture-r19.txt:256-260`); timer `OnBootSec=10m`/`OnUnitActiveSec=1h` (`:227-228`); 8 events in `snapper-cleanup.service` and 2 in transient `limine-snapper-add-1-5846` / `limine-snapper-add-2-260668` (`host-capture-r19c.txt:11-20`); ALPM-SCRIPTLET updates at pacman.log 3015/3047 (`host-capture-r19.txt:576-598`) via `/etc/pacman.d/hooks/90-mkinitcpio-install.hook` Exec `/usr/share/libalpm/scripts/limine-mkinitcpio-install` (`:396-398`). Mori's log note is detection of transactions, not writer-class ownership. Do not fold the handoff into C2 attribution or treat mori as a `/boot` writer. [obs]
- **Mado (ADJ-03).** Snapshot `a4046a` and live `mado-shokunin/PROVINCE.md:1-20` are byte-identical: Hyprland/waybar/walker/terminal/idle config, read-only; round-19 theme plane `~/.config/omarchy/**` is mado's, with program update, theme write, and consumer reload refused. Tsukuroi `PROVINCE.md` has no omarchy/theme row. IN-023 relies on `SKILL.md` walker package/hook lines (package/hook repair here; UI config there). [obs]
- **Tameshi (ADJ-07).** Snapshot `01d586` and live `tameshi-shokunin/PROVINCE.md:1-83` are byte-identical. Tameshi reads `tools/tsukuroi-census.sh` as a mutation-leg surface and refuses product domains and sibling gate edits (`:14-17,32-35`). Census bug, contract, and repair stay here; method advice only. Eight-leg append does not transfer `check-boot-writers.py` or registry gates. [obs]

## Census (route, do not reclassify here)

Inbound at pinned tips: mado 26 (IN-023..IN-047), mori 32 (IN-048..IN-079), tameshi 22 (IN-094..IN-115). [obs] Classification remains the inbound seats.

## Route

Acknowledge mori's pacman.log detection as an owner handoff already received; answer it on the package/boot-chain surface without adopting actor authentication or fleet correlation. Keep C2's 12 `/boot/limine.conf` events inside tsukuroi writer classes. Keep OOM fleet cause on ADJ-04. Keep mado theme/UI and tameshi method off this lane's gates.

Scope: executed=none
