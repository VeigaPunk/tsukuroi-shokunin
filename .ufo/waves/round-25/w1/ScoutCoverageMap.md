# C2 trend placement — the OOM and memory plane on tsukuroi's map

**Verdict:** no row of the coverage map in `corpus/README.md` holds the OOM and memory plane, and neither
memory-pressure reading nor systemd-oomd policy appears there as a decided surface; the plane is held only
by the census and by round-6 to round-9 `SKILL.md` appends. On the trend set by rounds 12 to 24, a
`memory-pressure-r25` entry is a **stronger, decision-bearing entry on held ground (depth)**, not uncovered
ground (coverage).

Read at claim base `b9046016831237cd04d38da11ba76e50d5380c53` (46 `corpus/knowledge/*.md` notes, 231 lines
in `corpus/README.md`; both re-derived with `git ls-tree` and `git cat-file` against that revision) and in the
working tree, which shows only round-25 wave artefacts as untracked (`git status --porcelain`: four `.ufo/waves/round-25/*`
entries, no production file modified).

## 1. The map has 15 rows, and none of them owns the memory plane [obs]

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md:3-21`. The table header is at `:5-6`
(``| Note | Holds | Sources |``) and the rows run `:7` to `:21`: package state, systemd user plane, driver
firmware, update safety, census v1, census v2, journal/boot, host health, executor sufficiency, adjacency
handoffs, Arch news, pacnew, initramfs v42, snapper, adjacency recheck. Fourteen are knowledge notes plus
two census rows; none is an OOM, memory, pressure or kill-event row.

The only literal `oom` inside the map is a class counter inside the round-2 census row:

> `corpus/README.md:11` — "kernel-ring error classes at entry count (`oom/io/gpu/other`)"

and the superseding row drops even that word from its journal arm:

> `corpus/README.md:12` — "boot err **entries** at `-o json` count with disjoint classes (coredump > kernel > other)"

The journal/boot row `corpus/README.md:13` carries the third and last adjacency: "13-boot retained-journal
census (per-boot err entries 1–168 …)". So the map represents OOM only as a filter class inside two other
planes, never as the memory/OOM plane itself.

## 2. The OOM plane's notes exist and are unmapped [obs]

At the base revision, `corpus/knowledge/` holds `oom-event-plane.md`, `kill-event-deep-r8.md`,
`memory-arm-ver-s8.md` and `memory-arm-mutants-s8.md`; grepping each basename in `corpus/README.md` returns
zero hits, alongside 14 further unmapped notes (18 of 46 unmapped in total). The lane's own coverage row
already admits the map's horizon:

> `SCORECARD.md:48` — "Ceiling: `PROVINCE.md` Core/Frontier/Adjacent not landed; `corpus/README.md` rows stop at r3"

The OOM note is registered outside the map, in the round-6 append:

> `SKILL.md:722` — "the OOM-event plane `corpus/knowledge/oom-event-plane.md` (S6-3; md5 `7e99d712…`, 433 lines — re-cut mid-append)"

## 3. Memory-pressure (PSI) reading is already held, but not mapped [obs]

Reading is implemented in the lane's gate, not described by any map row.
`tools/tsukuroi-census.sh:376` sets `PRESSURE_FILE=${TSUKUROI_PRESSURE_FILE:-/proc/pressure/memory}`;
`:1006` heads the arm "arm: memory pressure (rides the drivers plane's line and verdict)"; `:1100-1114` is the
C6 live read of PSI with an unreadable file reported as a named unknown (`C6-psi`), exercised by the fixture
case at `:2273-2276`. The arm is printed inside the drivers line (`:2656`, `mem=%s`) and the sixth plane is
printed at `:2659` (`PLANE oom:`). The prior note records the same live read:

> `corpus/knowledge/oom-event-plane.md:301` — "| PSI | `/proc/pressure/memory` | live (`some`/`full` with 10/60/300 s averages) | totals only | 14:42: `avg300=0.09`, `total=69,393,986 µs` |"

Round 7 already counted this landfall as coverage, which is why it cannot be coverage again:

> `SCORECARD.md:33` — "coverage + operability | round-6 state | AUR watch arm + OOM/memory-pressure arm landed in the census (49 selftest cases)"

## 4. systemd-oomd state is recorded; a decision is not [obs]

The measured state is in the OOM note at three places, and each is a state cell rather than a decision:

> `corpus/knowledge/oom-event-plane.md:280` — "`memory.oom.group` = 0; `systemd-oomd` inactive+disabled; `earlyoom` absent; `MemoryPressureWatch` = `skip`"
> `corpus/knowledge/oom-event-plane.md:344` — "| 1 | `systemd-oomd` (userland PSI+swap monitor) | unit present … `is-active`=inactive, `is-enabled`=disabled; socket disabled; `oomctl` cannot reach it; `oomd.conf` all-commented (defaults `SwapUsedLimit…"
> `corpus/knowledge/oom-event-plane.md:347` — "| 4 | pressure-watch export (`MemoryPressureWatch=`) | `skip` on `user@1000.service` (pinned in `/usr/lib/systemd/system/user@.service`, not a local override); system default `DefaultMemoryPressureWatch=auto` …"

The only table shaped like a decision on this subject is the operator-owned prevention list
(`oom-event-plane.md:337-353`), whose column heading is "operator action (not taken here)". The lane's
per-plane health-verdict decision table has five rows and no memory or OOM row:

> `SKILL.md:44-50` — "| Plane | Probe (verbatim, all read-only) | `HEALTHY` when | `DEGRADED` when | `BLOCKED` when | …" with rows "Package state (pacman)" `:46`, "systemd user units & timers" `:47`, "Journal & boot triage" `:48`, "Driver & firmware plane" `:49`, "Update-safety" `:50`

So the C2 "SKILL.md decision-table row" would be a **sixth row in an existing table**, or a new memory row
beside it — an extension of held ground either way, not a new table on new ground.

## 5. The declaration already books C2 against depth, not coverage [obs]

> `SCORECARD.md:793` — "| C2 memory-pressure reading and oomd decision entry (learning claim; sourced; PROVINCE core: OOM and memory plane) | depth 8 → 8 (tied lowest) | 0 verified rows (entry and checker absent) | 6 verified rows, MP1 to MP6, exit 0 |"

The claim fence also keeps the entry away from the map:

> `SCORECARD.md:788` — "C2 reads only this round's host capture, newly opened sources and its own entry."

Neither the claim row (`:793`) nor the fixed row list (`:797`) names a coverage-map edit, so a map row is a
choice the L1 must make explicitly, not a deliverable C2 carries.

## 6. PROVINCE names five surfaces and treats memory as triage support [obs] / [inf]

> `PROVINCE.md:8-12` — "**Owns (surfaces, all read-only probes):** pacman state … systemd user units & timers … journal/boot triage … driver/firmware plane … Update-safety questions"
> `PROVINCE.md:30-33` — "Host memory and kill-event measurements support OS triage; they do not establish which fleet wave caused pressure or whether an endpoint works. The existing census reports those signals; fleet correlation belongs to mori"
> `PROVINCE.md:49` — "| ADJ-04 | Host pressure or a kill signal needs fleet/wave attribution … | OS memory, journal and boot diagnosis; cumulative counters are not dated incidents | mori | …"

[inf] The declaration's parenthetical "PROVINCE core: OOM and memory plane" is a fair reading of
`PROVINCE.md:30-33` plus the census's sixth plane, but Core does not literally list memory as a named
surface. The entry should therefore lean on `PROVINCE.md:30-33` and the census, and should not assert that
Core enumerates an OOM surface.

## 7. No frontier item covers pressure or oomd, so nothing is promoted [obs]

> `corpus/README.md:30-33` — "Recipient-side replay, acknowledgement/acceptance and closure of the memory observation packet are unverified; author-side advisory seats are not outside promotion or admit/reject spot-checks."

That is the only memory-adjacent frontier bullet under `## Frontier` (`corpus/README.md:28`); the rest of the
section at `:34-42` covers RE ownership, index backfill and the mkinitcpio watch. `PROVINCE.md` Frontier
(`:75-107`) holds recipient acknowledgement, RE arbitration and round-12 to round-14 refinements. There is no
PSI or oomd frontier item to retire.

## 8. The trend precedent says "held ground", never "new surface" [obs]

Every round from 12 onward states its own placement in the map's prose:

> `corpus/README.md:59` (round 12) — "This deepens the existing rollback-net surface; it is not uncovered coverage"
> `corpus/README.md:160` (round 18) — "Held surfaces, not new coverage"
> `corpus/README.md:184` (round 20) — "deepens held adjacency/boot/tooling ground, not new coverage"
> `corpus/README.md:192` (round 21) — "deepen the existing revision-bound evidence-tooling surface"
> `corpus/README.md:196` (round 21) — "This is held-ground quality/depth, not uncovered coverage or a frontier graduation."
> `corpus/README.md:206` (round 22) — "deepen held source/evidence-operability ground"
> `corpus/README.md:231` (round 24) — "This is stronger evidence on an existing Core surface, not new coverage or a frontier promotion."

Rounds 19 to 21 also show the permitted map gesture: "extends the coverage-map row `knowledge/adjacency-recheck-2026-10-19.md`"
(`:176`) and "extends the coverage-map row `knowledge/initramfs-v42-sysroot-recovery.md` through `knowledge/boot-chain-r17.md`"
(`:178`). Extending a row is not a coverage promotion in this lane's own vocabulary.

## 9. Sibling boundary: mori owns the fleet-side reading, and already teaches MP1/MP2 [obs]

At the pinned sibling commit `4f05dd5a`, `corpus/knowledge/system-pressure-r24.md` covers system-scope PSI
file semantics, including memory: F1 names the file set ("cpu, memory, and io", `:60-63`), F2 quotes the
`some` and `full` definitions (`:76-78`), and F4 the cumulative microsecond total (`:90-91`). Its boundary is
explicit:

> `system-pressure-r24.md:50` — "It is a **reading** note. It describes one-shot, system-scope reads. It does not register a PSI trigger,"
> `system-pressure-r24.md:188-190` — "**No cgroup scope.** Only `/proc/pressure` is read … The census's user-slice `memory.pressure` is likewise a different scope; the two are never summed or compared as one number."

[inf] MP1 (meaning of `some`/`full`) and MP2 (`total` cumulative, needs two reads) are therefore already
taught and sourced by the sibling lane and are not tsukuroi's to re-derive. The tsukuroi-specific content is
the host decision layer (MP3 to MP6: cgroup files versus `/proc/pressure/memory`, the meaning of
`ManagedOOMMemoryPressure=`/`ManagedOOMSwap=` values on this host, the systemd 262 defaults, and the
separation of pressure stall evidence from `oom_kill` counters). [unk] Whether C2 may cite the sibling note
at all is unsettled: the fence at `SCORECARD.md:788` admits "this round's host capture, newly opened sources
and its own entry", so a sibling-note citation is a fourth input class the declaration does not list. The
safe placement is to open the kernel and systemd sources fresh and mention mori's note only as a boundary
locator, leaving fleet attribution to ADJ-04.

## 10. Freshness hazard: "earlyoom absent" is superseded, and the capture cannot carry that row [obs]

The round-6 current-use reading at `oom-event-plane.md:280` ("`earlyoom` absent") and `:305` ("nothing was
watching") is already superseded in this lane's own record:

> `SKILL.md:1938` — "R18-FRESH-SUPPLEMENT-03: … Now: earlyoom is installed1.9.0-1 and active/enabled atR18; this later state cannot explain the historical OOM or certify other memory guards"

A live read-only probe on 2026-10-22 agrees: `pacman -Q earlyoom` prints `earlyoom 1.9.0-1` (exit 0),
`systemctl is-active earlyoom` prints `active` (exit 0), `systemctl is-enabled earlyoom` prints `enabled`
(exit 0), while `systemctl is-active systemd-oomd` prints `inactive` and `systemctl is-enabled systemd-oomd`
prints `disabled`. The round-25 capture does not mention earlyoom at all: its memory material is PSI at
`capture.txt:13-25` (two reads ten seconds apart, `total` 41385384 → 41389485 on `some` and 40856373 →
40860452 on `full`), the oomd unit at `:71-79`, `oomd.conf` at `:82-108`, and the `ManagedOOM*`/`MemoryPressure*`
properties at `:111-150`. [inf] MP4 and MP5 must therefore not conclude "no userland monitor" from the
capture; the action cell must name earlyoom as the live monitor (or name its state as a separate probe).

## 11. Map presence: the entry ships invisible unless the map is extended [inf]

As declared, C2 produces `corpus/knowledge/memory-pressure-r25.md` and `.json`, a SOURCES row and a
`SKILL.md` row, and neither file exists at the base (`ls` returns "No such file or directory" for both
`tools/check-memory-pressure.py` and `corpus/knowledge/memory-pressure-r25.md`). Without a map edit the round
would add a nineteenth unmapped note to a map already described as stopping at round 3 (`SCORECARD.md:48`).
Two map gestures are consistent with precedent: extend an existing row's Holds text (the census rows at
`:11-12`, or the journal/boot row at `:13`) to name the `mem=` arm, the sixth `PLANE oom` and the new
decision entry, as rounds 19 to 21 extended rows (`:176`, `:178`); or add one map row for the OOM and memory
plane, which repairs a mapping gap open since round 6 and is a map-completeness repair rather than a coverage
promotion. Either is an L1 edit. Recommendation: extend, and label the round "deepens held memory/OOM ground",
matching every round since 12.

## 12. Remaining unknowns [unk]

- Whether the L1 wants a coverage-map row at all; the declaration fixes the entry, the JSON, the SOURCES row
  and the `SKILL.md` row only (`SCORECARD.md:793-797`).
- Whether citing mori's `system-pressure-r24.md` fits the C2 input fence (`SCORECARD.md:788`).
- Whether C1's depth count (K07) is expected to move when the new note lands; that check set is C1's, not
  this scout's, and the map's neighbour table is already known stale (its depth row at `SCORECARD.md:47`
  says "24 notes" against 46 at the base).

## Supporting check on the capture

`sha256sum capture.txt` prints
`e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`, matching the assignment; the file is 155
lines and 5607 bytes. Unique non-header lines exist for the C2 pointer requirement (for example
`capture.txt:107` `#DefaultMemoryPressureLimit=60%`, `capture.txt:117` `MemoryPressureWatch=skip`, and
`capture.txt:14` `some avg10=0.02 avg60=0.02 avg300=0.06 total=41385384`).

Scope: read=corpus/README.md (map rows, Frontier, round prose), PROVINCE.md (Core, Frontier, ADJ-04), SCORECARD.md (axes table, round-7 move row, round-25 declaration), SKILL.md (per-plane table, round-6 registration, memory-arm description, R18 supplement), oom-event-plane.md (sections 4 to 7), tools/tsukuroi-census.sh (pressure arm and emitters), mori-shokunin corpus/knowledge/system-pressure-r24.md at 4f05dd5a, .ufo/waves/round-25/capture/capture.txt; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ScoutCoverageMap.md; executed=wc, grep by pattern, sed line ranges for citations, git ls-tree/git cat-file/git status (read-only), git -C mori-shokunin show 4f05dd5a:…, sha256sum, pacman -Q earlyoom systemd, systemctl is-active/is-enabled earlyoom and systemd-oomd
Model: opencode-go/deepseek-v4.1-flash
Installs: none
