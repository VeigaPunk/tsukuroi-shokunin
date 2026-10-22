Verdict: all six C2 rows can be true at kernel v7.2 and systemd v262, but MP4 and MP6 have no unique capture line for their central value, MP2 and MP3 can point uniquely only to half of their evidence, and oom-event-plane.md:344 is contradicted by the primary sources.

# CritC2Rows — C2 first falsifier on truth (round 25, wave 1)

Capture checked: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt. Command `sha256sum` printed `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` (exit 0), which matches the declaration. The capture has 155 lines. After excluding `### ` headers, `$ ` command echoes and `[exit ` lines, 90 candidate lines remain, and 45 distinct candidate texts occur exactly once (`grep -vE '^(### |\$ |\[exit )' | sort | uniq -c`, exit 0). Line numbers below are 1-based line numbers in capture.txt.

## Numbered findings

1. [obs] Root cgroup lines duplicate the second system read. Capture lines 29 and 30 (`/sys/fs/cgroup/memory.pressure`) are byte-identical to lines 21 and 22 (second `/proc/pressure/memory` read): `some avg10=0.00 avg60=0.02 avg300=0.06 total=41389485` and `full ... total=40860452` each occur 2 times. So MP2's second read and MP3's root-equality evidence both lack a unique line. [obs] The kernel makes the equality true by construction, not by coincidence. `include/linux/psi.h:39` at v7.2 has `return cgroup_ino(cgrp) == 1 ? &psi_system : cgrp->psi;`, and `kernel/cgroup/cgroup.c:3980-3982` (`cgroup_memory_pressure_show`) calls `psi_show(seq, cgroup_psi(cgrp), PSI_MEM)`. The equality should be argued from that source, not from the capture.

2. [obs] MP4's own values have no unique line. `ManagedOOMSwap=auto`, `ManagedOOMMemoryPressure=auto`, `ManagedOOMMemoryPressureLimit=0`, `ManagedOOMMemoryPressureDurationUSec=[not set]`, `ManagedOOMPreference=none` and `MemoryPressureThresholdUSec=200ms` each occur 4 times (lines 112-118, 121-127, 130-136, 139-145). `MemoryPressureWatch=auto` occurs 3 times and `disabled` occurs 2 times (lines 76 and 79). The only unique lines in the oomd blocks are `inactive` (line 73) and `MemoryPressureWatch=skip` (line 117). [inf] The most likely false pointer is line 117. `MemoryPressureWatch=` is the `$MEMORY_PRESSURE_WATCH` export for cooperating applications, not systemd-oomd (systemd v262 `man/systemd.resource-control.xml:1663-1690`). Citing it as evidence for oomd semantics would be false provenance.

3. [obs] MP6's kernel-wide counter has no unique line. `oom_kill 0` occurs at line 51 (user-1000.slice `memory.events`) and line 62 (`/proc/vmstat`). `high 0` and `max 0` also occur 2 times each. Unique MP6 candidates are `oom 0` (line 50), `oom_group_kill 0` (line 52), `low 0` (line 47), `sock_throttled 13763` (line 53) and `fail 510` (line 58), all cgroup-scope. The `/proc/vmstat` value can be addressed only by line number. [obs] The capture also has no boot anchor: capture.sh runs no uptime or boot_id read. So `oom_kill 0` means zero since a boot the capture does not date.

4. [obs] systemd v262 adds a second way into oomd that the capture never reads: `OOMRules=` (v261). The source says "When set, systemd-oomd.service will monitor this unit's cgroup and evaluate the specified rulesets against it" (`man/systemd.resource-control.xml:1634-1659`), and adds that it "Defaults to an empty list, which means no rulesets are applied." Ruleset keys `MemoryPressureAbove=`, `SwapUsageMax=`, `Action=` and `LastingSec=` are documented at `man/oomd.conf.xml:71-155`. A row that says "no unit is monitored by systemd-oomd on this host" cannot rest on ManagedOOM values alone. [obs] A live read after the capture, `systemctl show -p OOMRules -- <unit>` for user@1000.service, user-1000.slice, user.slice and -.slice, printed `OOMRules=` for all four (exit 0). `stat` of all four `oomd/rules.d/` directories and of `/etc/systemd/oomd.conf.d` returned "No such file or directory". That read is not in the frozen capture, so it cannot be a pointer.

5. [obs] earlyoom is the live userspace OOM guard, and the capture is blind to it. `systemctl is-active earlyoom.service` printed `active` (exit 0), `is-enabled` printed `enabled` (exit 0), `pacman -Q earlyoom` printed `earlyoom 1.9.0-1`, and `ActiveEnterTimestamp=Thu 2026-10-22 04:55:44 -03` is this boot (`/proc/uptime` 8876.91 s at about 10:24Z). This is also recorded at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:1938 (R18-FRESH-SUPPLEMENT-03). C2 reads only this capture and new sources. So MP4 and MP6 MUST NOT say "nothing watches before the kernel"; the claim is true only for systemd-oomd. [inf] An earlyoom kill is a userspace signal and would not raise kernel `oom_kill` counters. That is the same argument as for oomd in finding 6, but I did not open earlyoom source this session [unk].

6. [obs] Prior statement /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:344 is contradicted on two points. It says `ManagedOOMMemoryPressure=auto` + `ManagedOOMSwap=auto` are "**already set**", and it infers that "oomd would likely have acted *before* the kernel" because swap was above the 90 % rule.
   - `auto` is the default and means not monitored: "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection" (`man/systemd.resource-control.xml:1545-1546`).
   - The swap rule needs memory and swap both above the limit. The man page says "If the fraction of memory used and the fraction of swap used on the system are both more than what is defined here" (`man/oomd.conf.xml:166-168`). The code is `oomd_mem_available_below(...) && oomd_swap_free_below(...)` (`src/oom/oomd-manager.c:477-479`).
   - With every captured unit at `auto`, no ancestor at `kill` and no `OOMRules=`, an enabled oomd would have had no monitored cgroup.
   - [obs] Arch ships no oomd default drop-ins. `pacman -Ql systemd | grep -iE 'oomd|user@\.service|\-\.slice'` lists only oomd.conf, the oomd unit, socket and binary, `user-.slice.d/10-defaults.conf` and `user@.service.d/10-login-barrier.conf`.
   - [inf] Other distributions may ship such drop-ins, but I did not open any [unk].
   - Statement :347 is consistent: upstream `units/user@.service.in:36` has `MemoryPressureWatch=skip`, and `systemd-analyze cat-config systemd/system/user@.service` shows it at its line 37 of /usr/lib/systemd/system/user@.service (exit 0).
   - Statement :301 is a single `total` read, which MP2 correctly says is not a dated incident.

7. [obs] Duplicate authority risk with mori. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 4f05dd5a:corpus/knowledge/system-pressure-r24.md` (exit 0) already states the PSI line shape for memory (F2, lines 69-72), that the root cgroup "prints `psi_system`" (line 189), and that the user-slice `memory.pressure` is a different scope "never summed or compared as one number" (lines 190-191). MP1 and MP3 restate those facts for memory. That is fine only if the tsukuroi rows cite mori's F2 and F9 as an adjacent, consistent reading and keep their own verdict on memory-plane diagnosis. [inf] Any sentence that attributes the 92 % of system `some` stall outside user.slice (user.slice is 3150158 of 41389485 µs, or 7.61 %) to a workload or wave belongs to mori under PROVINCE ADJ-04 (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:49). Report it; do not absorb it.

8. [obs] The "unique non-header line" test admits lines with no evidential content. Line 104 is an empty line and is unique. License lines 87 and 89-92, line 10 (the systemd feature string) and line 83 (`1`, the active-line count, which is only the `[OOM]` section header) are also unique. [inf] A checker that tests only uniqueness would accept a pointer that proves nothing. The smallest safe correction for `tools/check-memory-pressure.py` is to also require that the pointed line contains a row-specific token: `some`/`full` for MP1, `total=` for MP2, a cgroup PSI line for MP3, `inactive` for MP4, `Limit=` or `Sec=` for MP5, `oom` for MP6.

9. [obs] Source-version trap. The Arch man pages footer reads `systemd 262.1` (https://man.archlinux.org/man/oomd.conf.5.txt, last line; https://man.archlinux.org/man/systemd.resource-control.5.txt:1624), while the host is `systemd 262 (262-1-arch)` (capture line 9). The wording of every quote used below is the same in both, but the Arch text renders ‰ and ‱ as `<?>` (`a-oomd.conf.5.txt:159`). Prefer the upstream `v262` raw files for exact quotes.

## Per-row prediction

### MP1 — `some` and `full` on system memory pressure
- Predicted verdict: true. [obs] "The \"some\" line indicates the share of time in which at least some tasks are stalled on a given resource." (psi.rst:45-46, 19 words). [obs] "The \"full\" line indicates the share of time in which all non-idle tasks are stalled on a given resource simultaneously." (psi.rst:48-49, 20 words). The averages are percentages: "The ratios (in %) are tracked as recent trends over ten, sixty, and three hundred second windows" (psi.rst:59-60). Memory `full` is defined at system level; only CPU `full` is "undefined at the system level" (psi.rst:57-58).
- Most likely way it is false: reading `avg10=0.02` as 2 % instead of 0.02 %. Another is reading the high lifetime full-to-some ratio (40856373 / 41385384 = 0.987) as thrashing. psi.rst:49-51 ties thrashing to "extended time in this state", but the averages here are at or below 0.06 %. [inf] `full` is per group: `tasks[NR_RUNNING] == tasks[NR_MEMSTALL_RUNNING]` (psi.c:253-257).
- Unique capture lines: 14 `some avg10=0.02 avg60=0.02 avg300=0.06 total=41385384`, 15 `full avg10=0.02 avg60=0.02 avg300=0.06 total=40856373`. Lines 21-22 are not unique.
- Flag: none.

### MP2 — `total` is cumulative; a dated incident needs two reads and a difference
- Predicted verdict: true. [obs] "The total absolute stall time (in us) is tracked and exported as well" (psi.rst:62-63, 13 words), and `psi_show` divides by `NSEC_PER_USEC` (psi.c:1286-1287). The captured differences are 41389485 − 41385384 = 4101 µs (`some`) and 40860452 − 40856373 = 4079 µs (`full`), across a nominal 10 s (`sleep 10`), or 0.041 % of the window.
- Most likely way it is false or unverifiable:
  - The second read (lines 21-22) and the end date (line 25, `2026-10-22T10:06:33Z`, which repeats at line 154) are not unique, so a text-matched pointer to the second half of the difference is ambiguous.
  - The dates bracket more than the read interval: line 3 is taken before `uname`, `systemctl --version` and read 1, and the dates have 1 s resolution.
  - [inf] A reader may call 0.041 % inconsistent with `avg10=0.00` at read 2. It is not: `psi_show` collects totals at read time but folds them into the averages only when the 2 s period has elapsed (psi.c:1266-1270, `if (now >= group->avg_next_update)`), and the averages decay exponentially.
- Unique capture lines: 14, 15 (read 1) and 3 (`2026-10-22T10:06:23Z`). Read 2 can be cited only by line number (21, 22), noting that its text duplicates lines 29-30.
- Flag: partial. The row passes "at least one unique pointer", but its difference uses a non-unique line.

### MP3 — per-cgroup `memory.pressure` and its relation to `/proc/pressure/memory`
- Predicted verdict: true. [obs] "Each subdirectory in the cgroupfs mountpoint contains cpu.pressure, memory.pressure, and io.pressure files; the format is the same as the /proc/pressure/ files." (psi.rst:183-185, 22 words). The root file is the system group (finding 1).
- Answer to "does the root cgroup's memory.pressure equal /proc/pressure/memory": yes, as the same object (psi.h:39), not as a sum of children.
- Most likely way it is false:
  - Claiming "a parent total is at least its child's total" and checking it against this capture. The sequential reads give user.slice 3150158 < user-1000.slice 3158801 < user@1000.service 3161820 (`some`, lines 34, 38, 42), because time passes between reads.
  - [inf] For `full`, a child can legitimately exceed its parent even at the same instant, because each group's `full` state uses that group's own task counts (psi.c:253-257).
  - Proving the root equality from lines 29-30 instead of from source.
  - Noting that `cgroup.pressure` can disable accounting per cgroup, non-hierarchically (cgroup-v2.rst:1066-1080). [obs] `cat /sys/fs/cgroup/user.slice/cgroup.pressure` printed `1`, but that is not in the capture.
- Unique capture lines: 34, 35, 38, 39, 42, 43. Root lines 29-30 are not unique.
- Flag: partial. The cgroup side is pointer-able, but the root equality is not.

### MP4 — `ManagedOOMMemoryPressure=` and `ManagedOOMSwap=` `auto` versus `kill`, and meaning on this host
- Predicted verdict: true if worded as "systemd-oomd monitors nothing here". It is false if worded as "these units are opted in" or "enabling oomd would protect this host".
  - [obs] "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection." (systemd.resource-control.xml:1545-1546, 17 words).
  - [obs] `kill` makes the unit "a candidate for monitoring" and adds `After=` and `Wants=` on systemd-oomd.service (xml:1531-1541).
  - [inf] `disabled` is therefore not a guarantee that oomd never runs: any unit set to `kill`, or with a non-empty `OOMRules=`, pulls it in through `Wants=`.
- Answer to "is `auto` monitored": no. An `auto` unit is only a kill candidate if an ancestor is `kill` (xml:1546-1548), and here `-.slice` is also `auto` (lines 139-140).
- Most likely way it is false:
  - Omitting `OOMRules=` (finding 4).
  - Citing line 117 as oomd evidence (finding 2).
  - Saying "nothing watches before the kernel" while earlyoom is active (finding 5).
  - Repeating oom-event-plane.md:344 (finding 6).
- Unique capture lines: 73 `inactive` only. Every `ManagedOOM*` line and `disabled` is duplicated.
- Flag: **no unique line for the row's ManagedOOM values**. The only admissible pointer is the `inactive` state line. Smallest safe correction: point to line 73, cite ManagedOOM values by line number (112-113 for user@1000.service, 139-140 for -.slice) and label them non-unique, and state the `OOMRules=` gap as [unk] in the entry. A future capture should add `-p OOMRules` and an earlyoom state read.

### MP5 — systemd-oomd defaults for systemd 262
- Predicted verdict: true. The defaults are unchanged in v262.
  - [obs] `man/oomd.conf.xml:172` "Defaults to 90%." (SwapUsedLimit).
  - [obs] `:190` "Defaults to 60%." (DefaultMemoryPressureLimit).
  - [obs] `:202` "Must be set to 0, or at least 1 second. Defaults to 30 seconds when unset or 0."
  - [obs] Compile-time constants: `src/oom/oomd-manager.h:25-27` (`DEFAULT_MEM_PRESSURE_DURATION_USEC (30 * USEC_PER_SEC)`, `DEFAULT_MEM_PRESSURE_LIMIT_PERCENT 60`, `DEFAULT_SWAP_USED_LIMIT_PERCENT 90`).
  - [obs] Upstream `src/oom/oomd.conf:20-22` is byte-for-byte the three commented lines in the capture.
- Most likely way it is false or overstated:
  - Treating the commented lines as proof of the compiled values. They are a static shipped text file, and the host binary was not inspected [unk]. [inf] Arch builds with the upstream defaults.
  - Omitting the AND condition and the 5 % candidate floor. The swap rule acts only on candidates with more than 5 % of total swap (`THRESHOLD_SWAP_USED_PERCENT 5`, oomd-manager.h:30). [obs] On this host, memory used is (31721800 − 23863792) / 31721800 = 24.77 % and swap used is 1717652 / 31722876 = 5.41 % (lines 66-69). Both are far below 90 %.
  - Treating the pressure limit as `some`: it is "the fraction of time in a 10 second window in which all tasks in the control group were delayed" (xml:182-183), that is `full` avg10.
  - Claiming the three keys are all of v262's oomd knobs. v262 also has `PrekillHookTimeoutSec=` (v260, default 0) and the v261 ruleset keys.
- Unique capture lines: 106 `#SwapUsedLimit=90%`, 107 `#DefaultMemoryPressureLimit=60%`, 108 `#DefaultMemoryPressureDurationSec=30s`, 94 `# Entries in this file show the compile time defaults. Local`, 86 `# /etc/systemd/oomd.conf`, 105 `[OOM]`. Line 83 (`1`) is unique but only counts the `[OOM]` header as an "active line".
- Flag: none.

### MP6 — kernel OOM kill counters are separate from pressure stall evidence
- Predicted verdict: true.
  - [obs] `mm/oom_kill.c:934-936` raises `count_vm_event(OOM_KILL)` and `memcg_memory_event_mm(mm, MEMCG_OOM_KILL)` in the kernel kill path only.
  - [obs] systemd-oomd kills by userspace `cg_kill_recursive`/`cg_kill` with `SIGKILL` (`src/oom/oomd-util.c:280,289`) and records its kills in cgroup xattrs `user.oomd_ooms` and `user.oomd_kill` (`:269,306`), not in kernel counters.
  - [obs] "The number of processes belonging to this cgroup killed by any kind of OOM killer." (cgroup-v2.rst:1506-1508, 15 words). Here "any kind" means kernel global or memcg OOM, per the call sites.
  - [obs] `memory.events` is hierarchical (cgroup-v2.rst:1474-1477), and the mount lacks `memory_localevents` (`findmnt -no FSTYPE,OPTIONS /sys/fs/cgroup` printed `cgroup2 rw,nosuid,nodev,noexec,relatime,nsdelegate,memory_recursiveprot,memory_hugetlb_accounting`).
- Most likely way it is false or unverifiable:
  - The non-unique `oom_kill 0` (finding 3).
  - The missing boot anchor.
  - Treating `oom_kill 0` as "no OOM-driven kill of any kind" while earlyoom (finding 5) or oomd could kill without touching it.
  - [unk] Misreading `fail 510` (line 58, with `max 0` at line 57) as swap exhaustion. cgroup-v2.rst:1868-1870 defines `fail` as "running out of swap system-wide or max limit", and 30005224 kB was free. The cause is not established and should stay out of the row.
- Unique capture lines: 50 `oom 0`, 52 `oom_group_kill 0`, 47 `low 0`, 53 `sock_throttled 13763`, 58 `fail 510`. Lines 51 and 62 are not unique.
- Flag: **no unique line for the kernel-wide `/proc/vmstat` `oom_kill` value**. The row is pointer-able only through cgroup-scope lines. Smallest safe correction: point to line 50 or 52, cite line 62 by number as non-unique, and state "since the current boot, which this capture does not date".

## Sources opened this session (2026-10-22), for L1 SOURCES drafting

All were fetched with `curl -sSL` into /fast/scratch/hyaku/tsukuroi-r25/CritC2Rows/, and all returned HTTP 200. The sha256 is of the raw fetched bytes.

| URL | sha256 | used for |
|---|---|---|
| https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692 | MP1, MP2, MP3 |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad | MP3, MP6 |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi.h | cd80982f753aa56eb3b9e16212056d1ac3e9c905f6fd10ce5be1509c0e93b649 | MP3 |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c | 452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5 | MP1, MP2, MP3 |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/cgroup/cgroup.c | 3d4a256adea52d7e3f3b60dbb39622c82aa30dc398c01b5a135d2ccac3379a8c | MP3 |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e | MP6 |
| https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml | 36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617 | MP4, MP5 |
| https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml | d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8 | MP4 |
| https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd.conf | c4aafc5d01251d260a578a4a2bbf345a12aff281902bcfe77413f41e93f6a93c | MP5 |
| https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.h | 577eb8b46eab96395f61c9eeb90d34e4d8d9194826b79af19eb80a93feaa2f4b | MP5 |
| https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.c | 052f19b36d54997b78c4ca93fae17d8c8513ce7240b0b58a47a1efdad0da3a15 | MP5 |
| https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c | 2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a | MP6 |
| https://raw.githubusercontent.com/systemd/systemd/v262/units/user@.service.in | 72c2f40dcfced1d85bcc17583715966fc8a552b68af44404c213de2ea320504c | MP4 (line 117 provenance) |
| https://man.archlinux.org/man/oomd.conf.5.txt | 1da98cb11b784da7a061c5aa542f9f2a02735f745be8e8b6323b1125219e4a63 | version check only (262.1) |
| https://man.archlinux.org/man/systemd.resource-control.5.txt | 7d16b3d5c5ca786e8756679792ae95d64ad1348245ae07687894ef77f8b14422 | version check only (262.1) |

I also fetched `mm/memcontrol.c` and `meson.build` at the same tags, but nothing in them is relied on above.

## Smallest safe corrections (summary)
- MP2: use pointers 14 and 3. Cite read 2 by line number, marked as duplicating 29-30.
- MP3: use pointers 34, 38 and 42. Argue the root equality from psi.h:39 and cgroup.c:3980-3982. Never compare parent and child totals from sequential reads.
- MP4: use pointer 73. Do not use line 117. Name `OOMRules=` as [unk] for the capture. Scope "nothing monitors" to systemd-oomd.
- MP6: use pointer 50 or 52. Cite line 62 by number, with an undated-boot caveat. Do not claim that no userspace kills occurred.
- Entry text: supersede oom-event-plane.md:344 on both points from finding 6.
- Checker: require a row-specific token in the pointed line (finding 8).
- To the L1, not absorbed: the earlyoom capture gap, and the user.slice-share attribution (ADJ-04, mori).

Scope: read=SCORECARD.md round-25 declaration, capture.txt and capture.sh, oom-event-plane.md:268-350, PROVINCE.md ADJ-04, SKILL.md grep, corpus/SOURCES.md S110-S114, mori system-pressure-r24.md at 4f05dd5a, godspeed skill, kernel v7.2 and systemd v262 sources listed above, read-only host state; wrote=.ufo/waves/round-25/w1/CritC2Rows.md, /fast/scratch/hyaku/tsukuroi-r25/CritC2Rows/ (fetched source copies); executed=sha256sum, sort/uniq/awk over capture.txt, curl of the public URLs above, pacman -Q and -Ql, systemctl show/is-active/is-enabled, systemd-analyze cat-config, findmnt, stat, cat of /proc and /sys files, read-only git show/rev-parse/log
Model: Cursor Auto (underlying model not exposed)
Installs: none
