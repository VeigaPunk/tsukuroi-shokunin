source: S090 (Linux v7.2 Documentation/accounting/psi.rst), S091 (Linux v7.2 kernel/sched/psi.c), S092 (Linux v7.2 cgroup-v2.rst pressure files), S093 (Linux v7.2 init/Kconfig PSI options), S094 (Linux v7.2 psi= boot parameter), S095 (Linux v7.2 include/linux/psi_types.h), S096 (upstream commit 52b1364ba0b1 adding PSI_IRQ, first released in Linux 6.1). Rejected candidate: S097 (proc_pressure(5) does not exist; HTTP 404). Supporting reads without registry rows: Linux v7.2 kernel/cgroup/cgroup.c and kernel/time/sched_clock.c (opened by wave-1 seat DraftKnowledgeEntry, round 24).
verified-at: 2026-10-22 — sources opened as raw text by round-24 wave-1 seats (digests in corpus/lessons/round-24.md Gate). Host observation (ScoutHostKernelConfig, LivePressureCapture; read-only): kernel 7.2.11-arch1-1 with CONFIG_PSI=y, CONFIG_PSI_DEFAULT_DISABLED not set, CONFIG_IRQ_TIME_ACCOUNTING=y, no psi= on the command line; all four /proc/pressure files present; irq carries one full line; system cpu full total 0.
recheck: `python3 -I tools/mori-pressure.py --selftest` (frozen cases) and one live run of `python3 -I tools/mori-pressure.py`; on a kernel release, re-open S090 and S091.
author: MoriR24 (L1) from the wave-1 scribe draft `.ufo/waves/round-24/w1/DraftKnowledgeEntry.md`; mapping to S-ids, U1 resolution and the EOPNOTSUPP wording were changed by the L1 per contract amendment A2.

# System pressure (PSI) for CPU, IO and IRQ — one-shot read, and what each file state does not prove

## Corrections after wave-2 falsification (round 24, before closure)

Wave-2 seat CriticKnowledgeOverclaim (`.ufo/waves/round-24/w2/CriticKnowledgeOverclaim.md`) contradicted or narrowed
several statements below. Where this section and a later line disagree, this section wins.

- **Version scope (K3).** The decision-table rules "a nonzero system CPU `full` value means the file is not the
  kernel's" and "`malformed` means this is not a kernel PSI file" hold **on v7.2 only**: the zeroing of system CPU
  `full` arrived in 5.19 (commit `890d550d7dba`), and kernels before 5.13 print no CPU `full` line at all, so a
  genuine pre-5.13 cpu file reads `malformed` under the tool's required-kinds rule.
- **Averages (K5).** Each read collects the totals; the averages are recomputed on a read only when the next
  2-second update is due (`psi.c:1268-1270`), not on every read.
- **Trigger window (K6).** psi.rst states 500 ms to 10 s; the v7.2 code enforces only 0 < window ≤ 10 s
  (`psi.c:1372-1373`) and, for unprivileged writers, a multiple of 2 s (`psi.c:1379-1380`). The documentation's
  lower bound is stale at v7.2.
- **Boot disable and EOPNOTSUPP (P2).** The `[INFERENCE]` label in F7 and U4 is withdrawn: `psi_proc_init` tests
  `psi_enable` directly (`psi.c:1712`), and `psi=` is parsed before `psi_init()` and the initcalls
  (`init/main.c:1011,1047,1445`, no registry row). So at v7.2 the `psi_disabled` EOPNOTSUPP branch cannot be
  reached through a `/proc/pressure` read; the only reachable `/proc` EOPNOTSUPP is `irq` with IRQ time
  accounting off. A boot-disabled host **must** show cpu, memory and io `absent`.
- **IRQ `some` (P3).** `some: null` for irq means "not tracked by the kernel" (S095; S096 rationale), not
  "undefined"; that word is psi.rst's for system CPU `full`. [UNKNOWN] No upstream document defines what IRQ
  `full` measures; the code charges IRQ time only to a non-idle current task (`psi.c:1017`).
- **Decreasing total and missing files (P4).** The v7.2 code has no decrement path, so a decrease means the two
  samples are not comparable [INFERENCE]; it does not prove the absence of a kernel defect. A missing file is
  consistent with, among others: PSI boot-disabled, no IRQ time accounting (irq only), a kernel without
  `CONFIG_PSI`, a kernel older than 6.1 (irq only), or a `--root` that points elsewhere.
- **Provenance (wave-2 ReviewSourcesShape H1).** Statements resting only on `kernel/cgroup/cgroup.c`,
  `kernel/time/sched_clock.c`, `kernel/sched/sched.h`, `include/linux/sched/clock.h`, `include/linux/psi.h`,
  `init/main.c`, `arch/x86/kernel/tsc.c` or `kernel/sched/clock.c` are pointers for the next round, not admitted
  facts: those files have no registry row this round. That covers F12, the cgroup-code half of F9, U1's branch
  location and the mechanism half of U7. The admitted facts rest on S090–S096.
- **Citations (minor).** F3's readers are `psi.c:1540,1545,1550` plus the irq reader at `psi.c:1686`; in F9 the
  cgroup files sit in separate sections of cgroup-v2.rst (1083, 1215, 1911, 2171); F11's "no threshold rule" is
  scoped to `psi.c` and `psi.rst`, the files read.

## Scope

System pressure stall information is exported by the kernel as text files under `/proc/pressure/`. This note
records what those files are, exactly which shapes the kernel emits, which error codes the kernel returns,
and how each observable file state maps onto the round-24 C2 tool state
(`tools/mori-pressure.py`, contract `.ufo/waves/round-24/contract.md` C2).

It is a **reading** note. It describes one-shot, system-scope reads. It does not register a PSI trigger,
does not poll, does not read cgroup-scoped pressure, and does not set any threshold the kernel or a vendor
defines. The tool's vocabulary (`ok`, `absent`, `unsupported`, `unreadable`, `malformed`,
`counter_regressed`), its verdicts (`PRESSURE_OK | PRESSURE_HIGH | PRESSURE_PARTIAL | PRESSURE_UNAVAILABLE`)
and its exit codes are the tool's own contract, not kernel vocabulary.

## Facts

Every fact below carries its upstream pointer. URL to row: `psi.rst` → S090, `kernel/sched/psi.c` → S091, `cgroup-v2.rst` → S092, `init/Kconfig` → S093, `kernel-parameters.txt` → S094, `psi_types.h` → S095, commit `52b1364ba0b1` → S096.

**F1 — the file set.** System PSI is exported through one file per resource under `/proc/pressure/`. The
upstream documentation names exactly three of them: "Pressure information for each resource is exported
through the respective file in /proc/pressure/ -- cpu, memory, and io."
([psi.rst:36-38](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).
The kernel creates a fourth: `proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops)` under
`#ifdef CONFIG_IRQ_TIME_ACCOUNTING` ([psi.c:1710-1721](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
So on v7.2 the kernel can expose an IRQ file the documentation does not mention; the documentation is not an
inventory of the file set. The build option's help text likewise names only cpu, memory and io (S093, `init/Kconfig:730-731`).

**F2 — the file shape.** Each documented file (cpu, memory, io) holds two lines of the form
`some avg10=0.00 avg60=0.00 avg300=0.00 total=0` and
`full avg10=0.00 avg60=0.00 avg300=0.00 total=0`
([psi.rst:40-43](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).
The kernel's emitter is one `seq_printf`:
`"%s avg10=%lu.%02lu avg60=%lu.%02lu avg300=%lu.%02lu total=%llu\n"`, i.e. always two fraction digits and an
integer total, one line per kind, in the order `some` then `full` ([psi.c:1290-1296](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
The `some` line is "the share of time in which at least some tasks are stalled on a given resource"; the
`full` line is "the share of time in which all non-idle tasks are stalled on a given resource simultaneously"
([psi.rst:45-56](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).

**F3 — system CPU `full` is undefined, and the kernel writes zeros there.** "CPU full is undefined at the
system level, but has been reported since 5.13, so it is set to zero for backward compatibility."
([psi.rst:57-59](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)). The
kernel implements it by skipping the read: `if (!(group == &psi_system && res == PSI_CPU && full))` leaves
both the averages and the total at zero for that one line ([psi.c:1282-1288](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
All four `/proc/pressure/*` readers pass the system group (`psi_show(m, &psi_system, …)`,
([psi.c:1538-1550](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)), so the system CPU
`full` line is always zeros at v7.2.

**F4 — units and windows.** The three averages are "ratios (in %) … tracked as recent trends over ten,
sixty, and three hundred second windows"; "The total absolute stall time (in us) is tracked and exported as
well" ([psi.rst:60-65](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).
The kernel converts the accumulated nanoseconds to microseconds when it prints the total:
`total = div_u64(group->total[PSI_AVGS][…], NSEC_PER_USEC)` ([psi.c:1284-1288](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
The averages are exponentially decayed, sampled at `PSI_FREQ = (2*HZ+1)` ("2 sec intervals"), and refreshed
on each read ([psi.c:160-164](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c),
[psi.c:1265-1272](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).

**F5 — IRQ pressure has only a `full` line.** `only_full = res == PSI_IRQ;` and the print loop runs
`for (full = 0; full < 2 - only_full; full++)`, and the label is `"full"` when `only_full` is set
([psi.c:1273-1296](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)). The IRQ accounting
path adds only to `PSI_IRQ_FULL` ([psi.c:1032-1042](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)),
and a trigger request naming `some` for IRQ is refused with `-EINVAL`
([psi.c:1364-1367](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
An IRQ file therefore carries one `full` line; a missing `some` line for IRQ is the kernel's shape, not a defect. The kernel's state enum has `PSI_IRQ_FULL` and no IRQ `some` state, both under `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` (S095, `psi_types.h:41-49,57-70`); the full-only rule arrived with commit `52b1364ba0b1`, whose message says "we only use PSI_IRQ_FULL" and which first shipped in Linux 6.1 (S096).

**F6 — the IRQ file is conditional, and a read of it can fail.** `pressure/irq` is created only under
`CONFIG_IRQ_TIME_ACCOUNTING` ([psi.c:1717-1719](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)),
and `psi_show` returns `-EOPNOTSUPP` for IRQ when IRQ time accounting is not enabled:
`if (!irqtime_enabled() && res == PSI_IRQ) return -EOPNOTSUPP;`
([psi.c:1260-1263](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).

**F7 — PSI can be disabled, and the errors surface on read.** The `psi_disabled` static key makes every read
fail: `if (static_branch_likely(&psi_disabled)) return -EOPNOTSUPP;`
([psi.c:1257-1258](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)). The key is enabled at
init when `psi_enable` is false ([psi.c:228-240](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c));
`psi_enable` is false either by `CONFIG_PSI_DEFAULT_DISABLED` or by the `psi=` boot parameter
([psi.c:149-158](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)). The open handlers are
plain `single_open` ([psi.c:1553-1566](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)),
so the failure appears on **read**, not on open. Separately, the proc files themselves are created only when
`psi_enable` is true ([psi.c:1711-1719](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)),
The boot parameter is documented as `psi=` "Enable or disable pressure stall information tracking", format `<bool>` (S094, `kernel-parameters.txt:5505-5507`), and `CONFIG_PSI_DEFAULT_DISABLED` makes `psi=1` the opt-in (S093, `init/Kconfig:743-760`); so on v7.2 the boot-parameter path removes the files rather than leaving them to fail with `EOPNOTSUPP`
(a direct code reading: `psi=` is parsed before `psi_init()` and before the initcall that runs `psi_proc_init()`, `init/main.c:1011,1047,1445`, no registry row; so at v7.2 the `psi_disabled` EOPNOTSUPP branch is not reachable through a `/proc/pressure` read).

**F8 — the event-driven interface exists and is not used here.** A user registers a trigger by writing
`"<some|full> <stall amount in us> <time window in us>"` into the file and polling the same descriptor
([psi.rst:67-88](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)); the
documentation states windows "ranging from 500ms to 10s" (the v7.2 code enforces only 0 < window ≤ 10 s, `psi.c:1372-1373`) ([psi.rst:102-104](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst),
`WINDOW_MAX_US 10000000` at [psi.c:167](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c));
a second trigger on the same descriptor fails with `EBUSY`
([psi.c:1596-1598](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)). This note and the
C2 tool use none of it: the tool reads and never writes.

**F9 — cgroup scope is a different surface.** "In a system with a CONFIG_CGROUPS=y kernel and the cgroup2
filesystem mounted, pressure stall information is also tracked for tasks grouped into cgroups. Each
subdirectory in the cgroupfs mountpoint contains cpu.pressure, memory.pressure, and io.pressure files; the
format is the same as the /proc/pressure/ files." ([psi.rst:178-187](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).
The cgroup v2 documentation lists `irq.pressure` beside `cpu`, `io` and `memory.pressure` and documents `cgroup.pressure` as a per-cgroup, non-hierarchical switch (S092, `cgroup-v2.rst:1066-1087`). The v7.2 kernel's cgroup file set also carries IRQ: `cgroup_irq_pressure_show`/`_write`
([cgroup.c:4077-4091](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/cgroup/cgroup.c)) and the
comment "show or hide {cpu,memory,io,irq}.pressure files"
([cgroup.c:4127](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/cgroup/cgroup.c)). The system readers
and the non-root cgroup readers are different groups: the former pass `&psi_system`
([psi.c:1538-1550](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)), the latter pass
`cgroup_psi(cgrp)` ([cgroup.c:3970-4091](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/cgroup/cgroup.c)).
A system-scope read says nothing about any **non-root** cgroup's pressure, and vice versa; the root cgroup's pressure files print the same `psi_system` group as `/proc/pressure` (`include/linux/psi.h:39`, no registry row; on this host the two were byte-identical in one read pass).

**F10 — the kernel accumulates the total monotonically.** The running total is
`group->total[aggregator][s] += div_u64(deltas[s], max(nonidle_total, 1UL));`
([psi.c:408-410](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)). A `total` that
*decreases* between two reads of the same file is therefore not a stall event; the v7.2 code has no decrement path, so [INFERENCE] the two
samples are not comparable readings of the same counter.

**F11 — no upstream threshold exists.** The kernel source defines no "warn at N %" rule. The only thresholds
in the documentation are the user's own trigger values, given as examples ("100ms of total stall time within
any 500ms window", "some 150000 1000000") ([psi.rst:70-88](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).
A tool threshold is therefore the tool's own, and must be labeled as local.

**F12 — on generic-sched-clock architectures (not x86) the IRQ clock is a boot parameter.** `static int irqtime = -1; core_param(irqtime, irqtime,
int, 0400);` and `if (irqtime > 0 || (irqtime == -1 && rate >= 1000000)) enable_sched_clock_irqtime();`
([sched_clock.c:48-50, 242-243](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/time/sched_clock.c));
the declarations live in `include/linux/sched/clock.h:112-116`. This applies only on architectures built with `CONFIG_GENERIC_SCHED_CLOCK` (`kernel/time/Makefile:23`); x86, this host, has no `irqtime=` parameter. On x86 the TSC code enables IRQ time accounting unless `tsc=noirqtime` (`arch/x86/kernel/tsc.c:327-328,1544-1545`), and `kernel/sched/clock.c:176,243` can disable it after boot when the clock is found unstable (wave-2 seat CriticKnowledgeOverclaim; these files have no registry row).

## Decision table

Observable state of one resource file → the state the C2 tool reports → what that state does **not** prove.
Tool states and verdicts are the contract's vocabulary (contract C2); the "not proved" column is what the
sources above forbid.

| Observable file state | Tool state (C2) | Verdict / exit | What it does NOT prove |
|---|---|---|---|
| All four files present, kernel shape (F2), low values | each resource `ok` | `PRESSURE_OK`, exit 0 | That there was no stall: `avg10` is a decayed 10-second trend resampled every ~2 s (F4), so a shorter spike between two reads can be invisible. That the host is healthy. That the reading covers per-cgroup pressure (F9). That the local threshold was meaningful (F11). That accounting was running: a root `cgroup.pressure` of 0 freezes the totals and decays the averages, so `PRESSURE_OK` can stand under real pressure (U7). |
| IRQ file carries only a `full` line (F5) | `irq` = `ok`, `some: null` | unchanged by the resource itself | That IRQ "some" pressure is zero — the kernel never emits an IRQ `some` line (F5); `null` means *undefined*, not *zero*. That IRQ pressure is low. That the IRQ file is complete for the host: it is created only under `CONFIG_IRQ_TIME_ACCOUNTING` (F6). |
| System CPU `full` line present | `cpu` = `ok`, `full_system_undefined: true`; the `full` values are reported but never thresholded (contract C2) | unchanged by the resource itself | That the system had no full CPU stall: CPU `full` is undefined at the system level (F3) and must never be read as evidence of no stall. That a nonzero system CPU `full` value reports a stall — at v7.2 the kernel writes zeros there (F3), so a nonzero value means the file is not the kernel's system CPU pressure file, not that the system stalled. |
| File missing (ENOENT) | `absent` — unavailable, never zero | `PRESSURE_PARTIAL`, exit 0 (if no other resource crosses the threshold; a threshold finding anywhere gives `PRESSURE_HIGH`, exit 1); `PRESSURE_UNAVAILABLE`, exit 2 if every resource is absent | That the resource was not under pressure. Which cause applies: on v7.2 a boot-disabled PSI removes every file (F7) and a kernel without IRQ time accounting has no irq file (F6), so a missing file is consistent with either; the tool records no cause. That any other resource is fine. |
| Read fails `EOPNOTSUPP` | `unsupported` — unavailable, never zero | as above | That there was no pressure. That the threshold was met or missed. At v7.2 it is reachable through `/proc/pressure` only on `irq`, when IRQ time accounting is off (F6; on x86 `tsc=noirqtime` or a clock found unstable); the `psi_disabled` branch is not reachable while the files exist (corrections section). The tool records no cause; kernel and boot diagnosis belongs to tsukuroi. |
| Read fails `EACCES`/`EPERM` | `unreadable` — unavailable, never zero | as above | That the resource was idle or unpressured. That access is the *only* reason for the failure — `unreadable` records that this seat could not read, nothing about the resource's state. |
| Line shape does not match, duplicate kind, or a required kind missing (`cpu`/`memory`/`io` need `some` **and** `full`) | `malformed` | `PRESSURE_PARTIAL`, exit 0 (if no other resource crosses the threshold; a threshold finding anywhere gives `PRESSURE_HIGH`, exit 1) | That the kernel misbehaved: the kernel's own emitter produces exactly the documented shape (F2), so `malformed` means *this file is not a kernel PSI file of this resource*, or that the two samples were inconsistent — it is a refusal, not a fault finding. That the missing kind is zero. That the pressure was low. |
| Interval mode: second `total` < first `total` | `counter_regressed` | `PRESSURE_PARTIAL`, exit 0 | That pressure dropped, that counts were lost, or that the counter is broken: the kernel accumulates totals monotonically (F10), so a decrease means the two samples are not comparable readings of the same counter. The tool still prints the negative `total_delta_us` and `stall_ratio`; they are not a rate of anything. |
| `avg10` ≥ the tool's `--warn-avg10` on `some` of `cpu`/`io`/`memory` or `full` of `memory`/`io`/`irq` | finding `PRESSURE_HIGH` on that resource | `PRESSURE_HIGH`, exit 1 | That the threshold is calibrated: 10.0 is a labeled-local placeholder with no upstream basis (F11). That any specific workload was harmed. That CPU `full` (excluded by contract) or IRQ `some` (does not exist, F5) had no pressure. |
| Any resource `absent`/`unsupported`/`unreadable`/`malformed` while the others are `ok` | as above | `PRESSURE_PARTIAL`, exit 0 | That the observed resources are the whole system, or that the missing resource was fine. That exit 0 means "no pressure anywhere". |
| Every resource unavailable | all unavailable | `PRESSURE_UNAVAILABLE`, exit 2 | That the system is unpressured. That the tool is broken: exit 2 is also the usage-error code. |

## Limits

- **One-shot only.** The tool reads each file once (twice with `--interval`) and stops. It registers no trigger and does not poll, although the
  kernel supports exactly that ([F8]: write a threshold, poll the descriptor). An event that starts and ends
  between two reads is still counted in `total` and decayed into the averages (F4), but it may leave `avg10` under
  the threshold, and a single read cannot say when it happened.
- **No cgroup scope.** Only `/proc/pressure` is read, i.e. the system group (F9). Per-cgroup `cpu.pressure`,
  `memory.pressure`, `io.pressure` and (at v7.2) `irq.pressure` exist and, except for the root cgroup (which prints `psi_system`), are a different population (F9).
  The census's user-slice `memory.pressure` is likewise a different scope; the two are never summed or
  compared as one number.
- **Threshold local.** `--warn-avg10` (default 10.0) is a local placeholder. The kernel defines no such
  threshold (F11), and the documentation's trigger numbers are examples (F8). The threshold may be tuned to
  suit a host; it must always be reported as labeled-local, and the value must never be presented as a
  vendor or kernel constant.
- **The kernel's CPU `full` is excluded from the threshold** by contract, and reported with
  `full_system_undefined: true`. It is not evidence of no stall in either direction (F3).
- **The tool's grammar is looser than the kernel's emitter.** The kernel always prints two fraction digits
  and an integer total (F2); the tool's grammar accepts any decimal. That looseness is the tool's rule, not
  the kernel's, and a file the kernel did not produce can still pass it.
- **Interval mode is a two-point slope.** `total_delta_us` and `stall_ratio` are derived from two reads of a
  cumulative, microsecond-denominated counter (F4, F10) — not a window average, and not comparable across
  hosts or across intervals.
- **Detection and report only.** No host write, no PSI trigger registration, no cgroup write, no service or
  package change (round-24 bounds).
- **The verdict vocabulary and exit codes are the tool's own** (contract C2). The kernel's vocabulary is
  `EOPNOTSUPP`, `EBUSY`, `EINVAL` and file shapes; the kernel never emits `PRESSURE_OK`.

## [UNKNOWN]

- **U1 — `irqtime_enabled()` (resolved by seat SrcPsiC).** Defined as a run-time static branch in `kernel/sched/sched.h:3492-3495` at v7.2, constant false when `CONFIG_IRQ_TIME_ACCOUNTING` is absent (`sched.h:3518-3521`); where the branch is switched on at run time was not located (F12 names the `irqtime=` parameter and `enable_sched_clock_irqtime()`). Who may read `/proc/pressure/irq` is not claimed beyond the created mode `0666`.
- **U2 — host configuration (resolved for this host only).** Seat ScoutHostKernelConfig read `/proc/config.gz`: CONFIG_PSI=y, CONFIG_PSI_DEFAULT_DISABLED not set, CONFIG_IRQ_TIME_ACCOUNTING=y; `/proc/cmdline` carries no `psi=`. This is one host on 2026-10-22, not a fleet fact.
- **U3 — live reachability of `EOPNOTSUPP`.** Resolved by code reading (corrections section): cpu, memory and io
  show `absent` on a boot-disabled v7.2 host; EOPNOTSUPP is reachable only on `irq`. Neither was observed live.
- **U4 — boot ordering.** Resolved (corrections section); the `[INFERENCE]` label is withdrawn.
- **U5 — version bounds.** Every kernel pointer here is the `v7.2` tag. Whether `pressure/irq` and cgroup
  `irq.pressure` exist in earlier or later kernels was not checked.
- **U6 — the man page.** No `proc_pressure(5)` page exists (S097, rejected: HTTP 404; man-pages 6.20 has no such page). The kernel documentation (S090) is the format authority.
- **U7 — root `cgroup.pressure` switch.** Writing 0 to the root cgroup's `cgroup.pressure` stops `psi_system` accounting: `psi_group_change` stops recording (S091 `psi.c:845-857`), so totals freeze and the averages decay toward zero over the following reads (`psi.c:551,1269-1270`); a one-shot read can then report `PRESSURE_OK` under real pressure, and for a few periods right after the switch it can still report the earlier high values. The flag is directly readable at `/sys/fs/cgroup/cgroup.pressure` (this host: `1`); `mori-pressure.py` does not read it. Only the root-to-system mapping (`include/linux/psi.h:39`) and the root file's presence (`kernel/cgroup/cgroup.c:5585-5589`) lack registry rows. Sources: wave-1 CriticC2Semantics, wave-2 CriticKnowledgeOverclaim.

## Not claimed

- No trigger, no watcher, no poll loop, no daemon, no cgroup read, no write of any kind.
- No health claim: `PRESSURE_OK` is the absence of a threshold crossing in a local threshold, on a system
  scope, at one instant.
- No calibration of `--warn-avg10`, no comparison of these values across hosts, and no aggregation of system
  and cgroup scopes.
- No claim that CPU `full` is zero because the system was idle; it is undefined at the system level (F3).
- No claim that a missing or unreadable resource was unpressured; it was not observed.
