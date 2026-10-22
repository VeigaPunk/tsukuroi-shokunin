# Draft — `## Gate` sources block for `corpus/lessons/round-25.md`

Seat: `TsukuroiR25.DraftEntry` (scribe). Draft only; the L1 integrates. Lane:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Date 2026-10-22.

This is the sources block of the round-25 lesson Gate. One row per source id, one
located quote per row, each at most 25 words, each copied exactly from a page opened on
2026-10-22, with the line location. The `SOURCES` ids follow the proposal in
`.ufo/waves/round-25/w1/DraftEntry/sources-rows-r25.md`; the L1 renumbers if it assigns
different numbers, and the row `sources` lists in
`corpus/knowledge/memory-pressure-r25.json` follow the same renumbering.

Paste-ready Markdown:

## Sources opened this round

| id | URL | Located quote (at most 25 words) | Opened by |
|---|---|---|---|
| S115 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | lines 45-46: "The "some" line indicates the share of time in which at least some tasks are stalled on a given resource." | DraftEntry |
| S116 | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c | lines 410-411: "group->total[aggregator][s] += div_u64(deltas[s], max(nonidle_total, 1UL));" | DraftEntry |
| S117 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi.h | line 39: "return cgroup_ino(cgrp) == 1 ? &psi_system : cgrp->psi;" | DraftEntry |
| S118 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | lines 1507-1508: "The number of processes belonging to this cgroup killed by any kind of OOM killer." | DraftEntry |
| S119 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | lines 935-936: "count_vm_event(OOM_KILL); memcg_memory_event_mm(mm, MEMCG_OOM_KILL);" | DraftEntry |
| S120 | https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml | line 172: "between 0% and 100%, inclusive. Defaults to 90%." | DraftEntry |
| S121 | https://man.archlinux.org/man/systemd.resource-control.5 | plain-text rendering lines 1319-1320: "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection." | DraftEntry |
| S122 | https://man.archlinux.org/man/systemd-oomd.service.8 | plain-text rendering lines 23-24: "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored." | DraftEntry |

Raw bytes fetched 2026-10-22, sha256 each: psi.rst
`11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`; psi.c
`452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5`; psi.h
`cd80982f753aa56eb3b9e16212056d1ac3e9c905f6fd10ce5be1509c0e93b649`; cgroup-v2.rst
`a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`; oom_kill.c
`452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`; oomd.conf.xml
`36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`;
systemd.resource-control.xml
`d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8`;
systemd-oomd.service.xml
`4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d`. The two Arch man
pages were fetched as plain text at `https://man.archlinux.org/man/systemd.resource-control.5.txt`
(sha256 `7d16b3d5c5ca786e8756679792ae95d64ad1348245ae07687894ef77f8b14422`) and
`https://man.archlinux.org/man/systemd-oomd.service.8.txt` (sha256
`c4e0d11f32f1669dea5a315b54c3cd694a93a010b9618c8f550dc2a8ce4dbb6e`); their page footers
read `systemd 262.1` while the host runs `systemd 262 (262-1-arch)` (round-25 capture
line 9), so the upstream `v262` tag is the version-matched authority and the Arch pages
are the rendering the quote was copied from. In the three systemd XML pages a sentence is
broken by DocBook tags, so the quote is the rendered sentence and the line range locates
it.

## Further located quotes, not part of the Gate table

These carry the same pages and the same access date and are quoted in the entry
`corpus/knowledge/memory-pressure-r25.md`; they are listed here for the reader, and each
is at most 25 words:

- S115, psi.rst lines 48-49: "The "full" line indicates the share of time in which all non-idle tasks are stalled on a given resource simultaneously."
- S115, psi.rst lines 62-63: "The total absolute stall time (in us) is tracked and exported as well"
- S115, psi.rst lines 183-185: "Each subdirectory in the cgroupfs mountpoint contains cpu.pressure, memory.pressure, and io.pressure files; the format is the same as the /proc/pressure/ files."
- S116, psi.c lines 1286-1287: "total = div_u64(group->total[PSI_AVGS][res * 2 + full],"
- S118, cgroup-v2.rst line 1914: "Shows pressure stall information for memory."
- S120, oomd.conf.xml line 167: "the fraction of memory used and the fraction of swap used on the system are both more than"
- S120, oomd.conf.xml line 183: "the fraction of time in a 10 second window in which all tasks in the control group were delayed"
- S120, oomd.conf.xml line 190: "above. Defaults to 60%."
- S120, oomd.conf.xml lines 201-202: "Must be set to 0, or at least 1 second. Defaults to 30 seconds when unset or 0."
- S121, systemd.resource-control.5 plain-text rendering lines 1306-1309: "When set to kill, the unit becomes a candidate for monitoring by systemd-oomd."
- S121, systemd.resource-control.5 plain-text rendering lines 1314-1317: "Setting either of these properties to kill will also result in After= and Wants= dependencies on systemd-oomd.service unless DefaultDependencies=no."
- S121, systemd.resource-control.5 plain-text rendering lines 1325-1328: "Overrides the default memory pressure limit set by oomd.conf(5) for the cgroup of this unit."
- S122, systemd-oomd.service.8 plain-text rendering lines 27-28: "only descendant cgroups are eligible candidates for killing"

## Row-to-Gate-quote map for the C2 entry

| Entry row | Gate quote it uses | Further quotes in the entry |
|---|---|---|
| MP1 | S115 | S115 lines 48-49; S120 oomd.conf.xml line 183 |
| MP2 | S116 | S115 lines 62-63; S120 lines 201-202 |
| MP3 | S117 | S115 lines 183-185; S118 line 1914 |
| MP4 | S121 and S122 | S121 lines 1306-1309 and 1314-1317; S122 lines 27-28 |
| MP5 | S120 | S120 lines 190 and 167; S121 lines 1325-1328 |
| MP6 | S118 and S119 | S118 line 1914 |

## Old-to-new log lines for `corpus/lessons/round-25.md`

The C2 counting rule asks for the log of any registry change made in place. This entry
adds new registry rows only; it changes no existing row, so there is no `old → new`
line to log for `corpus/SOURCES.md`. The two statements this entry supersedes are in a
corpus note, not in the registry, and their supersession is recorded inside the entry and
inside `corpus/knowledge/memory-pressure-r25.json` under `supersedes`.

For the record, the two superseded statements are:

- `corpus/knowledge/oom-event-plane.md:344` — "`ManagedOOMMemoryPressure=auto` +
  `ManagedOOMSwap=auto` **already set** on `user@1000.service` and `user-1000.slice`"
  and "oomd would likely have acted *before* the kernel" → superseded: `auto` is the
  default and means systemd-oomd does not monitor that cgroup, so on this host it would
  have had no monitored cgroup even while running.
- `corpus/knowledge/oom-event-plane.md:301` — "| PSI | `/proc/pressure/memory` | live
  (`some`/`full` with 10/60/300 s averages) | totals only |" → narrowed: the `total`
  field is cumulative stall time in microseconds, so a dated reading needs two reads in
  one boot and their difference.

Scope: read=the fetched source bytes listed above, corpus/lessons/round-24.md Gate format; wrote=.ufo/waves/round-25/w1/DraftEntry/lesson-gate-quotes-r25.md; executed=curl fetches and sha256sum of the eight URLs, contiguity checks of every quote against the fetched bytes
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
