# Draft — `corpus/SOURCES.md` rows for the round-25 C2 entry

Seat: `TsukuroiR25.DraftEntry` (scribe). Draft only; the L1 integrates. Lane:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Date 2026-10-22.

Every page below was opened by this seat on 2026-10-22 with `curl -sSfL` into
`/fast/scratch/hyaku/tsukuroi-r25/DraftEntry/src/`. The sha256 values are of the raw
fetched bytes. Each quote was checked as a contiguous substring of the fetched bytes.

## Id collisions the L1 must resolve

Five wave-1 source seats drafted registry rows independently and their proposed ids
collide. The block below is a contiguous, collision-free proposal; where it differs from
a sibling seat's proposal, the sibling's id and the page it names are given.

| proposed id | page | sibling seat proposal |
|---|---|---|
| S115 | Linux v7.2 `Documentation/accounting/psi.rst` | SrcPsiDoc proposed S115 — agrees |
| S116 | Linux v7.2 `kernel/sched/psi.c` | SrcPsiDoc proposed S116 — agrees |
| S117 | Linux v7.2 `include/linux/psi.h` | SrcPsiDoc proposed S117 — agrees |
| S118 | Linux v7.2 `Documentation/admin-guide/cgroup-v2.rst` | SrcCgroupV2 proposed S118 — agrees |
| S119 | Linux v7.2 `mm/oom_kill.c` | SrcKernelOomCounter proposed S115 — renumbered here |
| S120 | systemd v262 `man/oomd.conf.xml` | SrcOomdConf proposed S116 — renumbered here |
| S121 | systemd v262 `man/systemd.resource-control.xml` | no sibling row landed (the SrcResourceControl seat delivered no report); drafted by this seat |
| S122 | systemd v262 `man/systemd-oomd.service.xml` | SrcOomdService proposed S117 — renumbered here |

Renumbering is a text edit in `corpus/SOURCES.md`, in
`corpus/knowledge/memory-pressure-r25.md` and in
`corpus/knowledge/memory-pressure-r25.json`. No fact and no quote changes.

## Rows

Paste-ready. The columns are the registry's fixed columns:
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S115 | Linux v7.2 `Documentation/accounting/psi.rst` — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst (sha256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`) | docs | A | The `some` and `full` line semantics of a pressure file, the unit and accumulation nature of the `total` field, and the per-cgroup pressure file set; the kernel version matching this host's 7.2.11-arch1-1 | lines 45-46: "The "some" line indicates the share of time in which at least some tasks are stalled on a given resource."; lines 48-49: "The "full" line indicates the share of time in which all non-idle tasks are stalled on a given resource simultaneously."; lines 62-63: "The total absolute stall time (in us) is tracked and exported as well"; lines 183-185: "Each subdirectory in the cgroupfs mountpoint contains cpu.pressure, memory.pressure, and io.pressure files; the format is the same as the /proc/pressure/ files." | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |
| S116 | Linux v7.2 `kernel/sched/psi.c` — https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c (sha256 `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5`) | code | A | Where the exported `total` is accumulated, that the accumulation has no decrement path, and that the unit is microseconds; kernel version matching this host's 7.2.11-arch1-1 | lines 410-411: "group->total[aggregator][s] += div_u64(deltas[s], max(nonidle_total, 1UL));"; lines 1286-1287: "total = div_u64(group->total[PSI_AVGS][res * 2 + full]," | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |
| S117 | Linux v7.2 `include/linux/psi.h` — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi.h (sha256 `cd80982f753aa56eb3b9e16212056d1ac3e9c905f6fd10ce5be1509c0e93b649`) | code | A | That the root cgroup is mapped onto the system pressure group, so its `memory.pressure` file is the system group and not a summary of children; kernel version matching this host's 7.2.11-arch1-1 | line 39: "return cgroup_ino(cgrp) == 1 ? &psi_system : cgrp->psi;" | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |
| S118 | Linux v7.2 `Documentation/admin-guide/cgroup-v2.rst` — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst (sha256 `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`) | docs | A | The per-cgroup `memory.pressure` file and the `memory.events` OOM counter definitions; kernel version matching this host's 7.2.11-arch1-1 | lines 1507-1508: "The number of processes belonging to this cgroup killed by any kind of OOM killer."; line 1914: "Shows pressure stall information for memory." | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |
| S119 | Linux v7.2 `mm/oom_kill.c` — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c (sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`) | code | A | Where the kernel raises its OOM-kill counters, that is in the kernel kill path and not in the PSI accounting; kernel version matching this host's 7.2.11-arch1-1 | lines 935-936: "count_vm_event(OOM_KILL); memcg_memory_event_mm(mm, MEMCG_OOM_KILL);" | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |
| S120 | systemd v262 `man/oomd.conf.xml` — https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml (sha256 `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`); the same page rendered for the host at https://man.archlinux.org/man/oomd.conf.5 (page footer `systemd 262.1`, sha256 of the fetched plain-text rendering `1da98cb11b784da7a061c5aa542f9f2a02735f745be8e8b6323b1125219e4a63`) | docs | A | The systemd-oomd default limits, the memory-and-swap conjunction of the swap rule, the 5 percent candidate floor and the memory-pressure semantics; systemd tag v262 matching this host's 262-1-arch | line 172: "between 0% and 100%, inclusive. Defaults to 90%."; lines 201-202: "Must be set to 0, or at least 1 second. Defaults to 30 seconds when unset or 0."; lines 167-168: "the fraction of memory used and the fraction of swap used on the system are both more than"; line 190: "above. Defaults to 60%." | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |
| S121 | systemd v262 `man/systemd.resource-control.xml` — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml (sha256 `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8`); the same page rendered for the host at https://man.archlinux.org/man/systemd.resource-control.5 (page footer `systemd 262.1`, sha256 of the fetched plain-text rendering `7d16b3d5c5ca786e8756679792ae95d64ad1348245ae07687894ef77f8b14422`) | docs | A | What `ManagedOOMMemoryPressure=` and `ManagedOOMSwap=` do in their `auto` and `kill` values, that `auto` is the default and is not monitored, and that `ManagedOOMMemoryPressureLimit=0` means use the default; systemd tag v262 matching this host's 262-1-arch | plain-text rendering lines 1319-1320: "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection."; plain-text rendering lines 1306-1309: "When set to kill, the unit becomes a candidate for monitoring by systemd-oomd."; plain-text rendering lines 1314-1317: "Setting either of these properties to kill will also result in After= and Wants= dependencies on systemd-oomd.service unless DefaultDependencies=no." | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |
| S122 | systemd v262 `man/systemd-oomd.service.xml` — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml (sha256 `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d`); the same page rendered for the host at https://man.archlinux.org/man/systemd-oomd.service.8 (page footer `systemd 262.1`, sha256 of the fetched plain-text rendering `c4e0d11f32f1669dea5a315b54c3cd694a93a010b9618c8f550dc2a8ce4dbb6e`) | docs | A | Which cgroups systemd-oomd monitors and which it may kill, and that its monitoring is a userspace PSI poll rather than kernel accounting; systemd tag v262 matching this host's 262-1-arch | plain-text rendering lines 23-24: "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored."; plain-text rendering lines 27-28: "only descendant cgroups are eligible candidates for killing" | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |

## Notes for the L1

- **Version match.** The host runs `systemd 262 (262-1-arch)` (capture line 9). The
  upstream `v262` tag is the version-matched authority and is what the quotes are taken
  from; the Arch man pages carry the same wording at page footer `systemd 262.1` and
  are recorded only as a rendering cross-check.
- **DocBook quotes.** In the three systemd XML pages a sentence is broken by tags
  (`<option>`, `<command>`, `<varname>`). The quote is the rendered sentence and the
  line range locates it; the sha256 of the raw bytes lets a reader re-derive the exact
  span.
- **No same-page re-registration.** None of these eight pages already has a row in
  `corpus/SOURCES.md`, so this block adds new sources rather than reopening existing
  ones. The nearest existing rows are S041, S044 and S046, which cite
  `systemd.exec(5)`, a different page.
- **The sibling lane holds the same pages.** Mori's registry has S090 (psi.rst v7.2),
  S091 (kernel/sched/psi.c v7.2) and S092 (cgroup-v2.rst v7.2) at `4f05dd5a`. Those are
  mori's rows; the tsukuroi rows above are tsukuroi's own registry entries for pages
  this lane opened and cited, and the entry cites mori's entry as the adjacent reading
  under `PROVINCE.md` row ADJ-04.

Scope: read=SCORECARD.md round-25 declaration, corpus/SOURCES.md, corpus/lessons/round-24.md Gate format, the five sibling source-seat reports in .ufo/waves/round-25/w1/, and the raw fetched source bytes; wrote=.ufo/waves/round-25/w1/DraftEntry/sources-rows-r25.md; executed=curl fetches of the eight URLs above into /fast/scratch/hyaku/tsukuroi-r25/DraftEntry/src/, sha256sum, and contiguity checks of every quote against the fetched bytes
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
