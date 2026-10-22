# DraftEntry — C2 memory-pressure entry and its machine-readable twin

Seat: `TsukuroiR25.DraftEntry` (scribe). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Round 25, wave 1, C2. Date 2026-10-22.

Verdict: the six-row C2 entry is drafted and self-checked — six rows MP1 to MP6, each with a
statement, a verdict, an operator action, one mined SOURCES row opened 2026-10-22, a located
quote of at most 25 words, at least one capture pointer into the frozen capture that is unique
and is neither a header, a command echo nor an exit line, and a named earlier tsukuroi
statement it supersedes — and the two drafts need one L1 decision (the SOURCES id block, where
five sibling seats collided) and no other work from this seat.

## Deliverables (drafts, for the L1)

| Draft | Path | Lands as |
|---|---|---|
| C2 entry, six rows MP1 to MP6 | `.ufo/waves/round-25/w1/DraftEntry/memory-pressure-r25.md` | `corpus/knowledge/memory-pressure-r25.md` |
| Machine-readable twin of the same six rows | `.ufo/waves/round-25/w1/DraftEntry/memory-pressure-r25.json` | `corpus/knowledge/memory-pressure-r25.json` |
| Eight `corpus/SOURCES.md` registry rows, with the id-collision table | `.ufo/waves/round-25/w1/DraftEntry/sources-rows-r25.md` | rows appended to `corpus/SOURCES.md` |
| Lesson `## Gate` sources block, one quote per source, plus the row-to-quote map | `.ufo/waves/round-25/w1/DraftEntry/lesson-gate-quotes-r25.md` | `## Gate` of `corpus/lessons/round-25.md` |

No production lane file was edited. `SKILL.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md`,
`SHONEN.md`, `corpus/` and `tools/` are untouched by this seat. Nothing was committed, no
git or jj write was run in the lane repo, and nothing was pushed anywhere.

## Findings

1. **[obs] The frozen capture is the one the declaration names.** `sha256sum` of
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt`
   returned `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` (exit 0),
   the digest declared in `SCORECARD.md:797`. The file has 155 lines. The capture script
   `.ufo/waves/round-25/capture/capture.sh` is host-read-only: it runs `date`, `uname`,
   `systemctl --version`, `systemctl show`, `systemctl is-active`, `systemctl is-enabled`,
   `systemd-analyze cat-config`, `cat` of `/proc` and `/sys` files, `grep` of `/proc/vmstat`
   and `/proc/meminfo`, and writes only into the output file it is given.

2. **[obs] 45 capture lines are unique, non-header, non-echo, non-exit lines.** The
   uniqueness test over the capture (`grep -vE '^(### |\$ |\[exit )'` then a text count)
   leaves 45 distinct line texts. The counted pointers in the entry are 14 and 15 (MP1), 14
   and 3 (MP2), 34, 38 and 42 (MP3), 73 (MP4), 106, 107 and 108 (MP5), 52 and 50 (MP6). Every
   one of them was checked to occur exactly once in the capture, to be neither a `### `
   header nor a `$ ` echo nor an `[exit ` line, to carry a letter or a digit, and to contain
   its declared token of at least three characters. I ran that check as a script against the
   JSON; it returned no finding for any of the thirteen pointers.

3. **[obs] Several capture lines cannot be counted, and the entry says so instead of
   hiding it.** The second `/proc/pressure/memory` read at lines 21 and 22 is byte-identical
   to the root cgroup's `memory.pressure` at lines 29 and 30, so MP2's second read is cited
   by line number only. The kernel-wide `/proc/vmstat` `oom_kill 0` at line 62 is
   text-identical to the cgroup `memory.events` `oom_kill 0` at line 51, so MP6's counted
   pointers are the cgroup-scope lines 52 and 50. Every `ManagedOOM*` value occurs four times
   (lines 112-118, 121-127, 130-136, 139-145), `disabled` occurs twice (lines 76 and 79), and
   the second timestamp occurs twice (lines 25 and 154). The capture line that is unique and
   carries the oomd state is line 73, the literal `inactive`.

4. **[obs] The uniqueness failure is a kernel property, not a capture error.**
   `include/linux/psi.h:39` at Linux v7.2 reads
   `return cgroup_ino(cgrp) == 1 ? &psi_system : cgrp->psi;`, so the root cgroup is mapped
   onto the system pressure group and its `memory.pressure` prints the same counters as
   `/proc/pressure/memory`. MP3 therefore argues the root identity from kernel source, not
   from the capture, and the sibling lane mori already holds that fact (F9, lines 133-144, at
   `4f05dd5a`).

5. **[obs] `oom-event-plane.md:344` is contradicted on two points by the systemd v262
   manual.** That row says `ManagedOOMMemoryPressure=auto` and `ManagedOOMSwap=auto` are
   "**already set**" on `user@1000.service` and `user-1000.slice`, and infers that "oomd
   would likely have acted *before* the kernel". `systemd.resource-control(5)` at v262 says
   `auto` is the default and that "When set to auto, systemd-oomd will not actively use this
   cgroup's data for monitoring and detection", and `systemd-oomd.service(8)` at v262 says
   "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be
   monitored". Every captured unit is `auto`, including `-.slice`, so the whole ancestor chain
   is `auto` and systemd-oomd would have had no monitored cgroup even while running. The
   entry supersedes `:344` in MP4 and narrows it in MP5, and the supersession is recorded in
   the entry text and in the JSON `supersedes` field.

6. **[obs] The earlier 90 percent rule was read as swap-only; the manual makes it a
   conjunction.** `oomd.conf(5)` at v262: "the fraction of memory used and the fraction of
   swap used on the system are both more than" the limit, and the eligible candidates are the
   descendant control groups "with swap usage greater than 5% of total swap". MP5 records the
   conjunction and the 5 percent floor, and narrows `oom-event-plane.md:344` accordingly. On
   this host at capture time memory used was 24.77 percent and swap used 5.41 percent, so
   neither arm was near its limit.

7. **[obs] `oom-event-plane.md:301` is narrowed, not contradicted.** That row lists PSI as
   live with 10/60/300 s averages and survives as "totals only". The `total` field is
   absolute stall time in microseconds accumulated inside one boot
   (`kernel/sched/psi.c:410-411`), so one read never dates an incident and a dated reading
   needs two reads and their difference. MP2 carries this and supersedes `:301` as a
   statement about how to read the field.

8. **[obs] `oom-event-plane.md:347` stands, and the entry keeps it separate.** That row
   reads `MemoryPressureWatch=skip` on `user@1000.service` with the system default `auto`
   and calls it a cooperating-app lever with no kill semantics. The capture confirms it
   (lines 117, 126, 136, 144 and 150). MP4 names it as *kept separate*, because
   `MemoryPressureWatch=` is the service-side pressure export and is not a systemd-oomd
   property; line 117 is therefore not offered as oomd evidence anywhere in the entry.

9. **[obs] The generic PSI semantics belong to the sibling lane and are cited, not
   absorbed.** Mori's entry at `4f05dd5a` already holds the `some`/`full` meanings (F2,
   lines 69-78), the cgroup scope and root identity (F9, lines 133-144) and the monotonic
   accumulation (F10, lines 146-150). The entry cites those and keeps only the
   systemd-oomd consequence and the OS-triage action, as `PROVINCE.md` row ADJ-04 requires.
   The JSON records the cross-reference in `mori_cross_reference` on every row.

10. **[obs] No row concludes that nothing watches memory before the kernel.** The frozen
    capture never read earlyoom. The supplementary read-only capture
    `.ufo/waves/round-25/capture/capture-earlyoom.txt` (sha256
    `7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309`) shows
    `earlyoom.service` active and enabled, and an empty `OOMRules=` on the four units. It is
    context, not a counting input, and MP4 and MP6 both carry the limit in their action.

11. **[obs] The version trap is handled.** The host runs `systemd 262 (262-1-arch)` (capture
    line 9). The Arch man pages carry page footer `systemd 262.1`, so the upstream `v262` tag
    is the version-matched authority and the Arch pages are recorded as the rendering the
    quote was copied from, with the sha256 of the fetched plain-text rendering for each.
    In the three systemd XML pages a sentence is broken by DocBook tags, so the quote is the
    rendered sentence and the line range locates it; the raw-byte sha256 lets a reader
    re-derive the exact span.

12. **[obs] Every quote was checked against the fetched bytes.** Each of the twenty-three
    quotes in the entry and the JSON was verified as a contiguous substring of the fetched
    file, whitespace-normalized, and each is at most 25 words (longest 20). The sha256 of
    each fetched file is recorded in the entry, in the registry draft and in the Gate draft.

13. **[obs] The five sibling source seats collided on the SOURCES ids, and the L1 must
    renumber.** SrcPsiDoc proposed S115 for psi.rst, S116 for psi.c and S117 for psi.h;
    SrcCgroupV2 proposed S118 for cgroup-v2.rst; SrcOomdConf proposed S116 for oomd.conf;
    SrcOomdService proposed S117 for systemd-oomd.service; SrcKernelOomCounter proposed
    S115 for oom_kill.c; and the SrcResourceControl seat delivered no report at all. My
    draft proposes the contiguous block S115 to S122 with a column naming each sibling's
    competing proposal, so the L1 can renumber in one pass. No fact and no quote changes
    under a renumbering; it is a text edit in the registry, in the entry and in the JSON.

14. **[obs] The JSON schema was agreed with the checker seat and then adjusted to its
    contract.** The checker seat `TsukuroiR25.ExecMemPressureTool` read the schema I
    proposed and asked for two changes: the capture-pointer key renamed from `contains` to
    `token` with the object shape `{path, line, token}`, and a non-empty `statement` on
    every row. Both are applied. The pointer objects now carry exactly `path`, `line` and
    `token`; the schema string is `tsukuroi-memory-pressure-r25-v1`; the row ids are MP1 to
    MP6 exactly once each. I sent the drafted JSON to that seat to be run through the real
    checker before integration, and I report its answer when it arrives.

15. **[obs] The entry's own self-check passes on all six rows.** A script over the drafted
    JSON checked, for each row: the id set, non-empty statement, verdict and action, every
    listed source having a Gate row and a matching quote, every quote being at most 25 words
    and present in its source's Gate cell, and every capture pointer satisfying the count
    rule. Result: no finding on MP1 to MP6.

## What this seat did not do

- It did not edit any production lane file, and it did not commit or push anything. The L1
  integrates all four drafts.
- It did not re-capture the host. The frozen capture is the counting input, and the
  supplementary earlyoom capture is context only.
- It did not run `tools/check-memory-pressure.py` against a real revision. The tool is the
  checker seat's; I sent the drafted JSON to that seat for that run.
- It did not decide the SOURCES ids. That is the L1's, and the collision table is in the
  registry draft.
- It did not attribute pressure to any workload, session or wave. That correlation belongs
  to mori under `PROVINCE.md` row ADJ-04.
- It did not start round 26 and did not create a round-26 task.

## Residual risk for the L1 and for wave 2

- The MP1 statement that systemd-oomd's memory-pressure limit is the `full` line is marked
  in the entry as an inference: `oomd.conf(5)` says "the fraction of time in a 10 second
  window in which all tasks in the control group were delayed" and the kernel says `full` is
  "the share of time in which all non-idle tasks are stalled", and no single document states
  the equivalence in so many words. A wave-2 falsifier should test that identification rather
  than accept it.
- The MP4 verdict is scoped to the four captured units and to their `auto` values. The
  systemd v262 `OOMRules=` channel was not read by the frozen capture; it is closed only by
  the supplementary capture, which is not a counting input. No host-wide statement is made.
- The MP2 verdict rests on the same-boot epoch of the `total` field. The entry's action says
  to record the boot identity with the pair of reads; the capture itself ran no boot-id or
  uptime read, so the epoch of the captured totals is not dated by it.

Scope: read=SCORECARD.md round-25 declaration and its refinements, corpus/SOURCES.md, corpus/lessons/round-24.md Gate format, corpus/knowledge/oom-event-plane.md lines 268-350, PROVINCE.md ADJ-04, SKILL.md verdict and decision-table conventions, the frozen capture and its script, the five sibling source-seat reports and the two critic reports in .ufo/waves/round-25/w1/, mori-shokunin system-pressure-r24.md at 4f05dd5a, and the raw bytes of eight primary pages fetched this session; wrote=.ufo/waves/round-25/w1/DraftEntry.md, .ufo/waves/round-25/w1/DraftEntry/memory-pressure-r25.md, .ufo/waves/round-25/w1/DraftEntry/memory-pressure-r25.json, .ufo/waves/round-25/w1/DraftEntry/sources-rows-r25.md, .ufo/waves/round-25/w1/DraftEntry/lesson-gate-quotes-r25.md; executed=curl fetches of the eight URLs above into /fast/scratch/hyaku/tsukuroi-r25/DraftEntry/src/, sha256sum, read-only git show of the sibling lane file, and local scripts that checked quote contiguity, quote length, capture-pointer uniqueness and the row-to-Gate-quote mapping
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
