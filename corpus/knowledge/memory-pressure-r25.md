source: Round-25 frozen capture `.ufo/waves/round-25/capture/capture.txt` (sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`, produced by `.ufo/waves/round-25/capture/capture.sh`); eight SOURCES rows for the primary pages below, all opened 2026-10-22, status `mined`, used-by `corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json`; machine-readable twin `memory-pressure-r25.json`; sibling reading cited and not absorbed: `mori-shokunin/corpus/knowledge/system-pressure-r24.md` at `4f05dd5a` (PROVINCE row ADJ-04); supplementary read-only capture `.ufo/waves/round-25/capture/capture-earlyoom.txt` (sha256 `7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309`), context only and not a counting input.
verified-at: 2026-10-22 (capture header line 3 reads `2026-10-22T10:06:23Z`; capture end line 154 reads `2026-10-22T10:06:33Z`; host kernel `7.2.11-arch1-1` at capture line 6; host systemd `systemd 262 (262-1-arch)` at capture line 9).
recheck: after any kernel, systemd or systemd-oomd configuration change, and after any memory incident. Procedure: run `bash .ufo/waves/round-25/capture/capture.sh <new-output-file>` (host-read-only; it writes only the named output file), update the capture pointers and the JSON, then `python3 tools/check-memory-pressure.py --revision <commit>`. A live re-capture needs an explicit read-only authorization; a committed gate count does not grant it.

# Memory pressure and systemd-oomd — round 25 entry

Six reading rules for the memory plane of this host, each one stated against the frozen
round-25 capture, each one sourced, and each one carrying a verdict and an operator
action. The rules are about **reading** memory pressure and about **what the installed
systemd-oomd would do if it were running**. They are not a kill policy and they are not a
repair plan; every change named below is operator-owned.

## How to read this entry

- **Verdict words.** `verified` means the statement holds on this host on the counted
  evidence. `scoped` means it holds inside a stated limit that the evidence does not
  cross. These are premise verdicts for six reading rules; the plane-level vocabulary
  `HEALTHY | DEGRADED | BLOCKED` in `SKILL.md` §Verdict vocabulary is unchanged and
  applies to planes, not to these rules.
- **Capture pointers.** A pointer is a line number plus a token of at least three
  characters. A pointer counts only when the pointed line's text occurs exactly once in
  the capture, is not a `### ` section header, is not a `$ ` command echo and is not an
  `[exit ` line. Lines that fail that test are still cited below by line number, and are
  listed as *supporting*, never as the counted pointer.
- **Quotes.** A quote is copied from the opened page. Where a sentence crosses a line
  break in the source, the quote is written with single spaces and the line range is
  given; where the source is DocBook XML, the quote is the rendered sentence and the raw
  bytes of the tag-free sentence are marked by the line range. The sha256 of the raw
  bytes fetched is recorded for every page, so quote fidelity can be re-derived.
- **SOURCES ids.** The ids below are the L1's to assign. The proposed block and the
  sibling seats' competing proposals are in `.ufo/waves/round-25/w1/DraftEntry/sources-rows-r25.md`.
  Renumbering is a text edit in this file, in `memory-pressure-r25.json` and in
  `corpus/SOURCES.md`; no fact changes.
- **Sibling lane.** The generic PSI file semantics are already held by the sibling lane
  mori (`mori-shokunin@4f05dd5a:corpus/knowledge/system-pressure-r24.md`, F2 at lines
  69-78, F9 at lines 133-144, F10 at lines 146-150). Those facts are cited here, not
  absorbed. What is tsukuroi's own in this entry is the systemd-oomd consequence and the
  OS-triage action on this host. Fleet or wave attribution of pressure belongs to mori
  under `PROVINCE.md` row ADJ-04.
- **Userspace killers.** The frozen capture never read earlyoom. The supplementary
  read-only capture shows `earlyoom.service` active and enabled on this host. No row
  below concludes that nothing watches memory before the kernel.

---

## MP1 — the `some` and `full` lines of system memory pressure

**Statement.** The `some` line of a memory pressure file is the share of time in which at
least some tasks are stalled on that resource; the `full` line is the share of time in
which all non-idle tasks are stalled simultaneously. systemd-oomd's memory-pressure limit
is documented as the share of time in a 10 second window in which all tasks of the
control group were delayed, which is the `full` line of that cgroup's memory pressure
file [inference from `oomd.conf(5)` and the kernel's definition of `full`; the two
documents do not state the equivalence in so many words]. A rising `some` value with a
much lower `full` value is therefore partial stall and never by itself an oomd
condition.

**Verdict.** `verified` — the file on this host carries both lines, and the `full` line
is the one the oomd rule reads.

**Action.** Read `full` and `some` together before quoting either, and quote the `full`
share when the question is whether systemd-oomd would have acted. Do not read a high lifetime
`full`/`some` ratio as thrashing on its own: the ratio here is 40856373 / 41385384 =
0.987 lifetime, while the current averages are at or below 0.06 percent.

**Counted capture pointers.**

| line | token | text | why |
|---|---|---|---|
| 14 | `total=41385384` | `some avg10=0.02 avg60=0.02 avg300=0.06 total=41385384` | the `some` line of the first read |
| 15 | `total=40856373` | `full avg10=0.02 avg60=0.02 avg300=0.06 total=40856373` | the `full` line of the same read |

Both texts occur exactly once in the capture; neither is a header, a command echo or an
exit line.

**Sources.**

- S115, Linux v7.2 `Documentation/accounting/psi.rst`
  (https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst,
  sha256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`), lines 45-46:
  "The "some" line indicates the share of time in which at least some tasks are stalled on a given resource."
- S115, same page, lines 48-49: "The "full" line indicates the share of time in which all non-idle tasks are stalled on a given resource simultaneously."
- S120, systemd v262 `man/oomd.conf.xml`
  (https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml, sha256
  `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`), lines 182-183:
  "the fraction of time in a 10 second window in which all tasks in the control group were delayed"

**Supersedes / narrows.** `corpus/knowledge/oom-event-plane.md:301` — that row named the
PSI file and its averages but did not state what the two lines mean, and it did not say
which of them the oomd rule consumes. The meaning of `some` and `full` is mori's held
ground (F2); the oomd consequence is new here.

---

## MP2 — the `total` field is cumulative stall time, so a dated incident needs two reads and a difference

**Statement.** The `total` field of a memory pressure line is absolute stall time in
microseconds, accumulated monotonically inside one boot. A single read therefore never
dates an incident: a dated reading needs two reads of the same file in the same boot and
the difference between them. systemd-oomd's own rule is not a difference of totals; it is
a sustained-limit rule, so a stall that ends inside the 30 second default duration never
reaches the oomd action even though a difference of totals would show it.

**Verdict.** `verified` — the two reads in the capture differ, and the difference is
what the two-read rule consumes.

**Action.** Take two reads with a known gap and subtract, and record the boot identity
with the pair. In this capture the gap was the `sleep 10` of capture line 17: `some`
41389485 − 41385384 = 4101 µs and `full` 40860452 − 40856373 = 4079 µs, that is 0.041
percent of the interval. A zero difference is not proof of no stall.

**Counted capture pointers.**

| line | token | text | why |
|---|---|---|---|
| 14 | `total=41385384` | `some avg10=0.02 avg60=0.02 avg300=0.06 total=41385384` | the first read's `some` total |
| 3 | `2026-10-22T10:06:23Z` | `2026-10-22T10:06:23Z` | the timestamp of the first read |

**Supporting lines, cited by number only** (their text occurs more than once in the
capture, so they are not counted pointers): the second read is capture lines 21 and 22,
whose text is identical to capture lines 29 and 30, the root cgroup's `memory.pressure`;
the second timestamp is capture line 25, whose text repeats at capture line 154.

**Sources.**

- S115, Linux v7.2 `Documentation/accounting/psi.rst` (sha256 as above), lines 62-63:
  "The total absolute stall time (in us) is tracked and exported as well"
- S116, Linux v7.2 `kernel/sched/psi.c`
  (https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c, sha256
  `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5`), lines 410-411:
  "group->total[aggregator][s] += div_u64(deltas[s], max(nonidle_total, 1UL));"
- S120, systemd v262 `man/oomd.conf.xml`, lines 196-202: "Must be set to 0, or at least 1 second. Defaults to 30 seconds when unset or 0."

**Supersedes / narrows.** `corpus/knowledge/oom-event-plane.md:274` — that reading rule
listed PSI among the plane's pressure signals without saying that the PSI figure is a
cumulative counter that cannot date an incident; and
`corpus/knowledge/oom-event-plane.md:301` — that row's "totals only" survival note did
not say that a difference of two totals, in one boot, is what a dated reading requires.
The accumulation fact is mori's held ground (F10); the two-read rule and the sustained
duration contrast are new here.

---

## MP3 — per-cgroup `memory.pressure` files and how they relate to `/proc/pressure/memory`

**Statement.** Every cgroup directory exposes `memory.pressure` in the same format as
`/proc/pressure/`. The root cgroup's file is not a summary of its children: the kernel
maps the root cgroup onto the system pressure group, so the root file prints the system
group's counters and equals `/proc/pressure/memory` by identity. A system-scope read
therefore says nothing about any non-root cgroup, and a parent total is not the sum of
its children. systemd-oomd watches the `memory.pressure` file of the cgroups it
monitors, not `/proc/pressure/memory`.

**Verdict.** `verified` — the per-cgroup files read on this host, and they are distinct
from the system file.

**Action.** Name the cgroup whose pressure is being read before quoting it, and never
compare a parent total with a child total taken from sequential reads: time passes
between the reads, and a child can legitimately exceed its parent. In this capture the
sequential reads give `user.slice` 3150158 µs, `user-1000.slice` 3158801 µs and
`user@1000.service` 3161820 µs of `some` total, which is a time artifact, not a
hierarchy.

**Counted capture pointers.**

| line | token | text | why |
|---|---|---|---|
| 34 | `3150158` | `some avg10=0.00 avg60=0.00 avg300=0.00 total=3150158` | `user.slice` `some` |
| 38 | `3158801` | `some avg10=0.00 avg60=0.00 avg300=0.00 total=3158801` | `user-1000.slice` `some` |
| 42 | `3161820` | `some avg10=0.00 avg60=0.00 avg300=0.00 total=3161820` | `user@1000.service` `some` |

**Supporting lines, cited by number only** (text duplicated): capture lines 29 and 30,
the root cgroup's `memory.pressure`, whose text is identical to the second system read at
capture lines 21 and 22. The root identity is argued from kernel source below, not from
the capture.

**Sources.**

- S115, Linux v7.2 `Documentation/accounting/psi.rst`, lines 183-185: "Each subdirectory in the cgroupfs mountpoint contains cpu.pressure, memory.pressure, and io.pressure files; the format is the same as the /proc/pressure/ files."
- S117, Linux v7.2 `include/linux/psi.h`
  (https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi.h, sha256
  `cd80982f753aa56eb3b9e16212056d1ac3e9c905f6fd10ce5be1509c0e93b649`), line 39:
  "return cgroup_ino(cgrp) == 1 ? &psi_system : cgrp->psi;"
- S118, Linux v7.2 `Documentation/admin-guide/cgroup-v2.rst`
  (https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst,
  sha256 `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`), line 1914:
  "Shows pressure stall information for memory."

**Supersedes / narrows.** `corpus/knowledge/oom-event-plane.md:274` — that reading rule
named PSI as a single plane signal; the per-cgroup files are a second scope with their
own identity rule, and the root file is the system group rather than a child summary.
The scope fact is mori's held ground (F9); the oomd consequence is new here.

---

## MP4 — what `ManagedOOMMemoryPressure=` and `ManagedOOMSwap=` mean, and what `auto` means on this host

**Statement.** `ManagedOOMMemoryPressure=` and `ManagedOOMSwap=` decide whether
systemd-oomd may act on a unit's cgroup. `kill` makes the unit a candidate for
monitoring and adds `After=` and `Wants=` dependencies on systemd-oomd.service. `auto`
is the default and means systemd-oomd will not actively use that cgroup's data for
monitoring and detection; an `auto` unit becomes a kill candidate only when an ancestor
cgroup is set to `kill`. systemd-oomd monitors only cgroups whose units carry `kill`.
On this host systemd-oomd is inactive and disabled, and every one of the four captured
units — `user@1000.service`, `user-1000.slice`, `user.slice` and `-.slice` — carries
`auto` on both properties, so the whole ancestor chain up to the root slice is `auto`
and nothing in it is monitored.

**Verdict.** `scoped` — the four captured units and their ancestor chain are `auto` and
systemd-oomd is inactive; a unit outside those four was not read by the capture, so no
host-wide statement is made.

**Action.** Read the two properties on a unit before assuming any protection from
systemd-oomd. Enabling the unit would still monitor nothing while every unit stays
`auto`; setting `kill` on a unit, or enabling systemd-oomd, is an operator action
outside this lane, and the operator must check for the running userspace killer
(earlyoom is active and enabled on this host) before deciding what a second killer
would do. Do not read `MemoryPressureWatch=` as an oomd property: it is the service-side
pressure export with no kill semantics.

**Counted capture pointer.**

| line | token | text | why |
|---|---|---|---|
| 73 | `inactive` | `inactive` | the systemd-oomd.service state read |

**Supporting lines, cited by number only** (each text occurs four times, so they are not
counted pointers): `ManagedOOMSwap=auto` and `ManagedOOMMemoryPressure=auto` at capture
lines 112 and 113, 121 and 122, 130 and 131 and 139 and 140; `is-enabled` reads
`disabled` at capture lines 76 and 79, whose text occurs twice.

**Sources.**

- S121, systemd v262 `man/systemd.resource-control.xml`
  (https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml,
  sha256 `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8`; the same
  page rendered for the host at https://man.archlinux.org/man/systemd.resource-control.5,
  plain-text rendering sha256
  `7d16b3d5c5ca786e8756679792ae95d64ad1348245ae07687894ef77f8b14422`), plain-text
  rendering lines 1319-1320: "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection."
- S121, same page, plain-text rendering lines 1306-1309: "When set to kill, the unit becomes a candidate for monitoring by systemd-oomd."
- S121, same page, plain-text rendering lines 1314-1317: "Setting either of these properties to kill will also result in After= and Wants= dependencies on systemd-oomd.service unless DefaultDependencies=no."
- S122, systemd v262 `man/systemd-oomd.service.xml`
  (https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml,
  sha256 `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d`; the same page
  rendered for the host at https://man.archlinux.org/man/systemd-oomd.service.8, plain-text
  rendering sha256 `c4e0d11f32f1669dea5a315b54c3cd694a93a010b9618c8f550dc2a8ce4dbb6e`),
  plain-text rendering lines 23-24: "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored."

**Supersedes / narrows.** `corpus/knowledge/oom-event-plane.md:344` — that prevention
row said the two properties were "**already set**" on `user@1000.service` and
`user-1000.slice`, and then inferred that "oomd would likely have acted *before* the kernel".
`auto` is the default and means not monitored, so on this host systemd-oomd would have
had no monitored cgroup even if it had been running. The row also carried the pressure
watch property at `corpus/knowledge/oom-event-plane.md:347`; that statement stands as
written — `MemoryPressureWatch=skip` on `user@1000.service` and `auto` elsewhere, as the
capture shows at lines 117, 126, 136, 144 and 150 — and MP4 keeps it separate from the
systemd-oomd properties, because it is the service-side export and has no kill
semantics.

---

## MP5 — the systemd-oomd default limits for the installed systemd 262

**Statement.** For the installed systemd 262 the systemd-oomd defaults are a
memory-pressure limit of 60 percent, a memory-pressure duration of 30 seconds and a
swap-use limit of 90 percent. The swap rule fires only when the fraction of memory used
and the fraction of swap used are **both** above the limit, and only on descendant
cgroups holding more than 5 percent of total swap. A unit's
`ManagedOOMMemoryPressureLimit=0` means "use the default", and it is ignored unless that
unit is `kill`. This host's `/etc/systemd/oomd.conf` sets no local key, so the shipped
defaults are the effective ones.

**Verdict.** `verified` — the shipped file carries the three commented defaults and no
active key, and the systemd 262 manual states the same three values.

**Action.** Read the three commented keys as the effective defaults for this host. Never
read the 90 percent rule as a swap-only rule, and never read
`ManagedOOMMemoryPressureLimit=0` as a zero-percent limit. On this host at capture time
memory used was 24.77 percent and swap used 5.41 percent, so neither arm of the swap
conjunction was near its limit.

**Counted capture pointers.**

| line | token | text | why |
|---|---|---|---|
| 106 | `SwapUsedLimit=90%` | `#SwapUsedLimit=90%` | the shipped swap limit |
| 107 | `DefaultMemoryPressureLimit=60%` | `#DefaultMemoryPressureLimit=60%` | the shipped pressure limit |
| 108 | `DefaultMemoryPressureDurationSec=30s` | `#DefaultMemoryPressureDurationSec=30s` | the shipped duration |

**Supporting line, cited by number only** (the text occurs twice): capture line 83, the
count of active lines in `systemd-analyze cat-config systemd/oomd.conf`, is 1, and that
single active line is the `[OOM]` section header at capture line 105, so no local key
is set.

**Sources.**

- S120, systemd v262 `man/oomd.conf.xml` (sha256 as above), line 172: "between 0% and 100%, inclusive. Defaults to 90%."
- S120, same page, line 190: "above. Defaults to 60%."
- S120, same page, lines 201-202: "Must be set to 0, or at least 1 second. Defaults to 30 seconds when unset or 0."
- S120, same page, line 167: "the fraction of memory used and the fraction of swap used on the system are both more than"
- S121, systemd v262 `man/systemd.resource-control.xml` (sha256 as above), plain-text
  rendering lines 1325-1328: "Overrides the default memory pressure limit set by oomd.conf(5) for the cgroup of this unit."

**Supersedes / narrows.** `corpus/knowledge/oom-event-plane.md:344` — that row quoted the
same three default values out of the commented host file and read the 90 percent rule
as a swap-only rule; the v262 manual shows the rule is a conjunction of memory and
swap, and the candidate floor is 5 percent of total swap.

---

## MP6 — kernel OOM-kill evidence and pressure-stall evidence are separate readings

**Statement.** The kernel raises its OOM-kill counters in the kill path, in a different
file from the one where stall time is accumulated. A cgroup's `memory.events` `oom_kill`
field counts the processes of that cgroup killed by any kind of OOM killer, while the
PSI `total` counts stall time. A userspace killer's SIGKILL moves neither counter, so
the kernel counter reads zero even when a userspace killer has killed something.

**Verdict.** `scoped` — the cgroup counters on this host are zero, and the kernel-wide
counter is a since-boot value that this capture does not date.

**Action.** Read the kernel counter and the stall counter separately, and never read one
as the other. This capture never read earlyoom, so no claim is made that nothing watches
memory before the kernel: the supplementary read-only capture shows `earlyoom.service`
active and enabled on this host, and an earlyoom kill would not move the kernel
counters. A zero `oom_kill` is a statement about one counter in one scope since one
boot, never about the absence of memory-related kills.

**Counted capture pointers.**

| line | token | text | why |
|---|---|---|---|
| 52 | `oom_group_kill` | `oom_group_kill 0` | the cgroup `memory.events` OOM-kill group counter |
| 50 | `oom 0` | `oom 0` | the cgroup `memory.events` OOM counter, the class the kernel kill path feeds |

**Supporting lines, cited by number only** (their text occurs more than once, so they
are not counted pointers): the kernel-wide `/proc/vmstat` `oom_kill 0` is capture line
62, whose text is identical to capture line 51, the cgroup `memory.events` `oom_kill`
field; the cgroup `oom` field is capture line 50. The capture ran no uptime or boot-id
read, so the kernel counter's epoch is not dated by it.

**Sources.**

- S119, Linux v7.2 `mm/oom_kill.c`
  (https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c, sha256
  `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`), lines 935-936:
  "count_vm_event(OOM_KILL); memcg_memory_event_mm(mm, MEMCG_OOM_KILL);"
- S118, Linux v7.2 `Documentation/admin-guide/cgroup-v2.rst` (sha256 as above), lines
  1507-1508: "The number of processes belonging to this cgroup killed by any kind of OOM killer."

**Supersedes / narrows.** `corpus/knowledge/oom-event-plane.md:274` — that reading rule
listed "PSI, and the kernel/systemd records" in one row of pressure signals; the kernel
kill counters and the stall counters are different readings of different files, and a
kill counter that reads zero does not close the memory question. Also
`corpus/knowledge/oom-event-plane.md:344` — the inference that systemd-oomd "would
likely have acted *before* the kernel" conflated a userspace killer's SIGKILL with
kernel OOM-kill accounting; the two are counted separately.

---

## What this entry does not claim

- It does not claim that nothing watches memory before the kernel. earlyoom is active and
  enabled on this host (supplementary read-only capture, context only).
- It does not claim a host-wide systemd-oomd state: the capture read four units. The
  `OOMRules=` channel of systemd v262 was not read by the capture.
- It does not attribute pressure to any workload, session or fleet wave. That is mori's
  correlation under `PROVINCE.md` row ADJ-04.
- It does not change the host. Every action above is a read-only diagnosis or an
  operator-owned change.

## Gate

The located quotes for this entry are listed in
`.ufo/waves/round-25/w1/DraftEntry/lesson-gate-quotes-r25.md`, ready for the L1 to place
in the `## Gate` section of `corpus/lessons/round-25.md`. The registry rows are in
`.ufo/waves/round-25/w1/DraftEntry/sources-rows-r25.md`.

## Corrections after wave-2 review (2026-10-22, before closure)

- MP6: capture line 50 (`oom 0`) is the memcg OOM event raised in `mem_cgroup_oom`, not the kill path. The kill counter `oom_kill 0` sits on capture lines 51 and 62, which repeat each other, so they are cited by number only. A userspace killer moves neither kernel counter unless it asks the kernel to kill: earlyoom with `--kernel-oom` does (held by the sibling lane mori in `corpus/knowledge/oom-kill-counter-kernel-only-r12.md`). The captures did not read earlyoom's arguments. MP6 no longer lists `oom-event-plane.md:344` as superseded; MP4 carries that.
- MP4: its supersession reason is scoped to the four units the capture read. The same refuted premise in `kill-event-deep-r8.md:255` now carries its own R25 notice.
- MP3: the root-cgroup identity rests on this lane's S117 (`include/linux/psi.h`); mori's note lists that file as a pointer for a later round, not an admitted fact, so it is not attributed to mori.
- The checker counts rows with complete evidence links (statement, verdict, action, sources, Gate quote, unique capture line, SKILL row). It does not test that a verdict is true; wave-2 reviewers RevMP1 to RevMP6 re-opened the sources row by row (`.ufo/waves/round-25/w2/`).
- MP1: the bracketed "[inference]" about systemd-oomd reading the `full` line is withdrawn. S120 itself states it: systemd v262 `oomd.conf.xml` lines 95-96 say "(PSI full avg10)". The oomd limit reads the `full avg10` share of a monitored cgroup's `memory.pressure`, not the lifetime `total` (RevMP1).
- MP4: "systemd-oomd monitors only cgroups whose units carry kill" is too strong for systemd v262. Units with `OOMRules=` are also monitored (S121 lines 1633-1644; S123 lines 115-116). On this host `OOMRules=` is empty on the four read units (supplementary `capture-earlyoom.txt`, context only), so the host conclusion stands. A monitored `kill` unit's leaf cgroups, not the unit itself, are the kill candidates (S122 lines 47-51) (RevSourcesSystemd).
- MP2 and MP3: "only grows within one boot" holds for the system group (`/proc/pressure/memory` and the root cgroup). A per-cgroup total starts at zero when its cgroup is created, so a recreated cgroup restarts within one boot (psi.c lines 1117-1146) (RevSourcesKernel). The `memory.events` `oom_kill` field is hierarchical; the cgroup-local count is in `memory.events.local` (cgroup-v2.rst lines 1474 and 1517-1518).
- MP5: the swap rule named here is the `[OOM]` `SwapUsedLimit=` rule; v262 rulesets (`SwapUsageMax=`) act alone. The memory-pressure path also needs reclaim activity in the last 30 s before it acts (`oomd-manager.c` line 596, `oomd-manager.h` line 32), and the selected cgroup is killed with all its descendants (`oomd-util.c` line 366). The 5 percent swap floor (`oomd.conf.xml` lines 168-169) and the "0 means the default" rule (`systemd.resource-control.xml` lines 1560-1563) are located here but were not in the counted Gate quotes (RevMP5).
- MP4 action: `systemd-oomd.socket` (inactive and disabled) listens with mode 0666 when active, so a running daemon could also take cgroup reports from local accounts for cgroups they own (`oomd-manager.c` lines 96-111 and 1277-1288); "monitors nothing while every unit stays auto" holds only while no such report arrives. Starting it remains operator-owned (RevMP4).
- MP3: "a parent total is not the sum of its children" is withdrawn as a statement about values. The v7.2 code never computes a parent total by adding child totals (the only write is `psi.c` lines 409-411, from the group's own per-CPU state), but a parent total weights stall time across CPUs, so at one instant it can be below, equal to or above the children's sum (RevMP3). The supported rule is: compare totals of one cgroup only, and never infer a child's stall from a parent's.
- Registry corrections: S126 supersedes S120 (digest typo) and S127 supersedes S125 (mori facts F2, F9 system half, F10; blob `d4ccce42`). The source set cited by this entry is S115 to S124 primary and S127 sibling.

## R26 source-row note (2026-10-22)

Append-only; nothing above is rewritten. Round-25 routed defect 8 found that three registry rows overstate or omit: S121's teaches cell says only `kill` makes a cgroup a systemd-oomd candidate, but systemd v262 also monitors units with `OOMRules=` ("systemd-oomd.service will monitor this unit's cgroup and evaluate the specified rulesets against it.", systemd.resource-control.xml lines 1643-1644); S122's "when it is not running it acts on nothing" is an inference the page does not state; S118's omits that every `memory.events` field is hierarchical (cgroup-v2.rst lines 1474-1476). The superseding rows are S136 (supersedes S121), S137 (supersedes S122) and S138 (supersedes S118) in `corpus/SOURCES.md`, re-opened 2026-10-22 with the same bytes as the rows they supersede. This entry's MP3, MP4 and MP6 corrections above already carry the right meaning; read S136 to S138 for the source teaching.

R26 note, continued (wave-2 CritTrendVerdicts): the JSON companion `memory-pressure-r25.json` still carries the pre-correction statement text of row MP4 ("monitors only cgroups whose units carry kill") and of row MP6 (without the hierarchy), and cites S121, S122 and S118. Those JSON statement fields are superseded by the MP4 and MP6 corrections in this Markdown entry and by S136 and S138; the JSON is not rewritten in place.

R26 note, Gate-quote erratum (wave-2 RevS136): the S136 quote in the R26 source-row note above begins with a man-page cross-reference whose tag-free form is "systemd-oomd.service8 will monitor ..."; the exact text on line 1644 is "will monitor this unit's cgroup and evaluate the specified rulesets against it." The meaning is unchanged. S136's teaches cell also widens the ancestor case: for an ancestor set to `kill`, an `auto` unit is a candidate "for systemd-oomd to terminate" (lines 1546-1548), not a monitoring candidate.

R27 current-use notice (appended 2026-10-22, register row OV5 in `corpus/knowledge/adjacency-mori-oom-r27.json`): the MP6 correction above relies on earlyoom's `--kernel-oom` option as the exception to "a userspace killer moves neither kernel counter". Mori's admitted entry `userspace-oom-killers-r26.md` (mori commit `ef9dbee1`, section Facts, F7) says that delegation does not exist in the installed earlyoom 1.9.0. earlyoom behaviour is mori's ground: read the exception as withdrawn for this host and follow mori's F7; this lane does not restate it.
