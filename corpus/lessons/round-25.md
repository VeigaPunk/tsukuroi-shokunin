# Round 25 — lesson (tsukuroi, attempt 1, 2026-10-22)

author: TsukuroiR25 (L1). Claim base `b9046016831237cd04d38da11ba76e50d5380c53`; declaration `6c580b155840c8750a7bb5f14dcb8e48913d0073`; refinements `0cd9b28bee5fd5a50d991e6dee0c0d0f48b15935`.

## Gate

Candidates considered: the primary pages for memory pressure stall reading (Linux v7.2) and for systemd-oomd policy (systemd v262, the installed 262-1), opened by wave-1 seats SrcPsiDoc, SrcCgroupV2, SrcKernelOomCounter, SrcOomdConf, SrcResourceControl, SrcOomdService, SrcSystemdCode, DraftEntry, RevMp4Semantics and RevMpThresholds, plus the sibling entry `mori-shokunin/corpus/knowledge/system-pressure-r24.md` at `4f05dd5a` (SrcMoriSibling, ConnSiblingOverlap). The L1 re-checked every quote below as a whitespace-normalised substring of the fetched raw bytes (sha256 values are in the SOURCES anchors).

Admitted rows (all `mined`, opened 2026-10-22, recheck `on-release`, used-by the new entry): S115 to S124 (primary, tier A) and S125 (sibling entry, tier B, boundary only). No existing row changed `status`, `recheck` or `used-by` this round, so the old → new registry log is empty.

| Source | URL | Opened | Located quote (at most 25 words) | Location |
|---|---|---|---|---|
| S115 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | 2026-10-22 | "line indicates the share of time in which at least some tasks are stalled on a given resource." | lines 45-46, tag v7.2 |
| S115 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | 2026-10-22 | "line indicates the share of time in which all non-idle tasks are stalled on a given resource simultaneously." | lines 48-49, tag v7.2 |
| S115 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | 2026-10-22 | "The total absolute stall time (in us) is tracked and exported as well" | lines 62-63, tag v7.2 |
| S116 | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c | 2026-10-22 | "group->total[aggregator][s] += div_u64(deltas[s], max(nonidle_total, 1UL));" | lines 410-411, tag v7.2 |
| S117 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi.h | 2026-10-22 | "return cgroup_ino(cgrp) == 1 ? &psi_system : cgrp->psi;" | line 39, tag v7.2 |
| S118 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | 2026-10-22 | "Shows pressure stall information for memory." | line 1914, tag v7.2 |
| S121 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml | 2026-10-22 | "will not actively use this cgroup's data for monitoring and detection." | lines 1545-1546, tag v262 |
| S121 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml | 2026-10-22 | "the unit becomes a candidate for monitoring by" | line 1531, tag v262 |
| S122 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml | 2026-10-22 | "periodically polls PSI statistics for the system and those cgroups to decide when to take action." | lines 45-46, tag v262 |
| S123 | https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.c | 2026-10-22 | "if (message.mode == MANAGED_OOM_AUTO) {" | line 124, tag v262 |
| S120 | https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml | 2026-10-22 | "Defaults to 60%." | line 190, tag v262 |
| S120 | https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml | 2026-10-22 | "Defaults to 30 seconds when unset or 0." | line 202, tag v262 |
| S120 | https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml | 2026-10-22 | "Defaults to 90%." | line 172, tag v262 |
| S124 | https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.h | 2026-10-22 | "#define DEFAULT_MEM_PRESSURE_LIMIT_PERCENT 60" | line 26, tag v262 |
| S124 | https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.h | 2026-10-22 | "#define DEFAULT_SWAP_USED_LIMIT_PERCENT 90" | line 27, tag v262 |
| S119 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | 2026-10-22 | "count_vm_event(OOM_KILL);" | line 935, tag v7.2 |
| S118 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | 2026-10-22 | "The number of processes belonging to this cgroup killed by any kind of OOM killer." | lines 1507-1508, tag v7.2 |
| S125 | mori-shokunin/corpus/knowledge/system-pressure-r24.md at 4f05dd5a | 2026-10-22 | "This note records what those files are, exactly which shapes the kernel emits" | section Scope |

Rejected or not registered:

- The Arch rendered man pages (`https://man.archlinux.org/man/oomd.conf.5`, `systemd.resource-control.5`, `systemd-oomd.service.8`) were opened but not registered: they render systemd 262.1, while the host runs 262-1. The upstream v262 XML is the version-matched authority; seats confirmed the wording is the same. Flip: register them if the host moves to 262.1.
- `src/login/logind.c` and `src/login/logind-user.c` (systemd v262, linger and user-manager lifetime) were opened by SrcPsiDoc but not registered: no counted row uses them. Flip: a later capture that records linger state and unit start times.
- `kernel/cgroup/cgroup.c`, `include/linux/psi_types.h`, `mm/memcontrol.c`, `mm/vmstat.c`: opened as supporting reads, not registered; no admitted statement rests on them alone.

Registry recheck log (old -> new): none.

Spot-check result: owed to the non-author closure; not self-granted.

## Routed defects from the round-24 spot-check

| Defect (spot-check line) | Disposition this round |
|---|---|
| 1 Claim sizing and lowest axis (98) | C1 counts mismatches between SCORECARD/SHONEN and repository state (23 fixed checks); C2 sits on depth, tied lowest at 8 with adjacency. QUALITY 57. |
| 2 Privileged-probe boundary (99) | Both wave contexts carry a written read-only sudo allow-list; no item needed sudo. QUALITY 58. |
| 3 Sequencing (100) | Partly repaired. Wave 2 was dispatched only after every wave-1 seat returned, and code-writing executors had separate clones. Not repaired: the canonical `kimi-shokunin` protocol copies were read after wave 1 was dispatched (the fleet-root copies were read before; the differences are wording, checked with `diff`), and one seat pushed scratch commits into the lane through its clone (Mistakes R25-SEAT-PUSH). |
| 4 Provenance (101) | The wave context carries the verbatim bytes of `~/.agents/skills/godspeed/directive.md`; every seat report ends with a `Model:` line (exposed for most seats, `not exposed` for some). |
| 5 Registry inflation (102) | The C2 checker accepts a row opened this round or a logged in-place `recheck` update, so a re-read never forces a new row. One row per URL: the W04 count is unchanged at 21 (wave-1 ExecCensusW04 classified the 21 existing pairs: 17 same-page different-scope, 4 different anchors). |
| 6 Label drift (103) | Appended correction after QUALITY 56: the lesson IDs `R24-KEY-RECOLLECTION` and `R24-STALE-PREMISE` win (RevQualityLabels). |
| 7 P3 snapshot boot (104) | Not claimed; needs an operator-authorized boot. No L0 line was added because the round-24 question stands. |
| 8 Private identifier in history (105) | Operator-owned; unchanged. |

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R25-STALE-AXES-TABLE | stale-premise | The only axes table before this round, `SCORECARD.md:45-52` (round 11), said 24 notes, `SKILL.md` 1631 lines, 55 table lines, 0 lesson files, `corpus/README.md` 20 lines, 80 census cases, coverage 8, freshness 8, adjacency 7, and that the PROVINCE sections and an overlap table did not exist. At `b9046016` the repository holds 46 notes, 2301 lines, 259 table lines, 25 lesson files, 231 README lines, 97 census cases, ordinals 9, 9 and 8, and both PROVINCE structures. Round 24 read freshness 8 from this table (spot-check line 98). | none | `tools/check-self-assessment.py` over the fixed checks K01 to K23; at `b9046016` it exits 1 with the mismatches listed in `SCORECARD.md` Round 25 measured outcome, and its selftest has a stale-ordinal and a stale-count case that fail. The new appended axes table is the fix; QUALITY 57. |
| R25-SEAT-PUSH | landing | Wave-1 seat DraftSkillTable cloned the lane into scratch and ran `git push`; the clone's origin was the lane, so four scratch commits (authors `t <t@x>` and `r20 <r20@example.invalid>`, tip `d5e64812`) landed on the lane's local `master` at 07:30-07:32 -03. The remote was never touched. The L1 found it with `jj-lane.sh state` (`ahead=4`) and reset the ref with a compare-and-swap `git update-ref refs/heads/master 0cd9b28b… d5e64812…` before any jj import, so no helper commit carried them. | none (the wave context forbade git writes "in the lane repo" but not pushes from a clone whose origin is the lane) | Every executor clone now has push URL `/nonexistent/no-push-to-lane`, and all running seats were told that a clone push into the lane is forbidden. The wave-2 context names that bound. QUALITY 59. Shown able to fail: `jj-lane.sh state` printed `ahead=4` before the repair and `ahead=0` after. |

## Process notes

- Inherited leftovers from round-24 seats that kept writing after round 24 ended (writers ExecPauseGateChecker-2, ScribeGateEntry-2 and RevGateSchema-2, last write 07:00:17 -03): three tracked files restored from `master` (`.ufo/waves/round-24/w1/ExecPauseGateChecker/check-pause-gate.py`, `.ufo/waves/round-24/w1/RevGateSchema.md`, `.ufo/waves/round-24/w1/ScribeGateEntry/pause-lift-gate-r24.json`; the discarded diff had sha256 `0a215d8083cd3f6cc6c64e7d7fbe26960c2606ccc86df0bcdfbef621a47f3559`, 593 insertions and 364 deletions) and two untracked files deleted (`.ufo/waves/round-24/w1/ScribeGateEntry/p2-measured-probe.txt`, sha256 `2eb7ab535d72a9fb89aea2bbdd06d289aec14d072779244f10f6c4bdccfe3f9c`, 15 lines; `.ufo/waves/round-24/w1/ScribeGateEntry/zero-probes-measured.txt`, sha256 `5266b65467dacaa34eca96641ff047075117c5ddafdf31384048a9a25972e4d4`, 19 lines). RevLeftoverIncident confirmed the restore and found no later round-24 writes.
- The frozen capture never read earlyoom, which is active and enabled; the supplementary read-only capture `capture-earlyoom.txt` records it and empty `OOMRules=`. It is context, not a counting input.
- Sentinel finding: `capture.sh` prints an "active lines" count of 1 for oomd.conf; that line is the `[OOM]` section header, so the active settings count is 0.
- Round-26 capture items proposed by SrcPsiDoc: the boot id (`/proc/sys/kernel/random/boot_id`) beside any pair of interval reads, and unit start time plus linger state for per-cgroup totals.
- Installs: none.

## Gate errata after wave 2 (appended 2026-10-22, before closure)

- S120 anchor: the sha256 in `corpus/SOURCES.md` row S120 has a transposition (`…5632d4a6…`); the fetched bytes of `https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml` hash to `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617` (CritC2Supersession). The registry row is append-only outside its status, re-check date and used-by cells, so this erratum (and the superseding row S126) carries the correction; the three copies in this round's SKILL.md section were corrected in place.
- S125 anchor: the entry cites mori facts F2, F9 and F10, not F1 to F4 and F10 as the row says; the row also carries no blob digest. Mori's note at `4f05dd5a` lists `include/linux/psi.h` facts as pointers for a later round, so MP3's root-identity fact rests on this lane's S117, not on mori (CritC2Adjacency).
- R25-STALE-AXES-TABLE captured-by: QUALITY 55 (stale host-state premise) partly covered the same failing example; it did not cover the lane's self-assessment table, which QUALITY 57 now does (CritTrendVerdicts).

## Wave-2 findings recorded, not repaired this round

- The C2 checker counts complete evidence links, not true verdicts. MutC2Rules killed 8 of 17 mutants against the real entry; the 9 survivors are in the quote rule (a Gate or entry quote mismatch is a non-blocking finding), the SKILL row rule (any table line naming the id) and the row count (a duplicated row still counts 6). CritC2Adjacency showed the sibling row S125 can stand as a row's only source. The instrument is not changed after measurement; tightening it (blocking quote mismatch, SKILL id in the first cell of the round-25 table, distinct ids, at least one tier-A source per row) is a round-26 item.
- Four of the six C2 rows (MP1, MP2, MP3, MP6) restate generic kernel facts the sibling lane mori already holds; the new knowledge is MP4 (auto is not monitored) and part of MP5 (the memory-and-swap condition and the 5 percent floor). Nothing was reported back to mori this round.
- S121 and S122 teaches cells say "only kill" makes a cgroup a candidate or is monitored; systemd v262 also monitors units with `OOMRules=` (S121 lines 1633-1644). S122's "when it is not running it acts on nothing" is an inference, not a quote. S118's teaches cell omits that `memory.events` is hierarchical. These rows are not rewritten; the entry carries the corrections (RevSourcesSystemd, RevSourcesKernel).

## Record of the one in-place edit (appended after wave 2)

`SHONEN.md` box 2 (line 8) changed `observation/request` to `observation and request`. Reason: the declared C1 path grammar (`SCORECARD.md` refinements, a token with a slash is a path) reads the slash token as a missing path, so K21 mismatched at the base. The packet in `corpus/knowledge/adjacency-handoffs-fleet-r1.md` section 3 is an observation plus a request, so the meaning is unchanged. One of the 13 base mismatches is therefore a grammar artifact repaired by rewording, not a stale fact; 12 are stale self-assessment facts (CritC1Construction, RevShonen). RevShonen also found that SHONEN boxes 3 and 4 cite superseded notes; they stay `[~]` and are routed to the next round.

## Mistakes added after wave 2

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R25-LATE-CANONICAL-LOAD | landing | The canonical `kimi-shokunin/skills/shokunin/protocol/` files were read after wave 1 was dispatched; before dispatch the L1 read the fleet-root copies, which differ in wording only (`diff` line counts: PROTOCOL 71, MISSION 42, CORPUS 63, LEARNING 12, AXES 0). Third recurrence (rounds 21, 24, 25; CritRoutedPlan, CritRoutedClosure). | round-24 routed defect 3 (prose only) | Not fixed this round. Round 26 must read the canonical files and record their sha256 in the declaration commit before any wave is validated; a declaration without those digests is the failing state. |
| R25-SEAT-WAKE-WRITES | landing | Wave-1 seats that had returned were woken by messages from other seats and kept editing their reports and copies after the L1 committed `5e7c04ec` (15 tracked files changed between 11:37Z and 11:59Z, including `w1/ExecMemPressureTool/check-memory-pressure.py`, which is not the measured `tools/` copy). The L1 sent a stop at 11:59Z and every seat acknowledged. | none (the wave context forbade messaging other seats only in wave 2) | The final wave-1 bytes are committed as evidence after the stop; the measured tools are the `tools/` copies at the measured revision. Round 26 contexts must forbid seat-to-seat messages in every wave. |
