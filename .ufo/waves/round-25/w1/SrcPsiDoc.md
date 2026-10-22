# SrcPsiDoc — C2 source for MP1 and MP2 (round 25, wave 1)

Verdict: the Linux v7.2 pressure stall information documentation supplies every MP1 and MP2 fact the
declaration asks for, and the frozen capture supplies matching host evidence, but one wording detail
must travel with the entry: the documentation never uses the word "cumulative" about the `total` field,
so the "cumulative" wording of MP2 needs the kernel accounting source as a second anchor.

## 1. Source opened and pinned

1. [obs] The primary source is the kernel pressure stall information documentation at the tag `v7.2`,
   fetched from `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst`.
   The sha256 of the fetched raw bytes is `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`
   (6792 bytes). The same bytes were fetched a second time from an independent host, the kernel.org
   plain view of the stable tree at the same tag,
   `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/accounting/psi.rst?h=v7.2`,
   and the two files are byte identical (`diff` reports no difference; the sha256 values match).
2. [obs] The tag was resolved with `git ls-remote --tags https://github.com/torvalds/linux.git v7.2`:
   the tag object is `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63` and it peels to commit
   `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`. The git blob id of the fetched documentation is
   `d455db3e58083869fa50bf8b29591b491292db50`.
3. [obs] The host kernel is `7.2.11-arch1-1` (capture line 6), so the `v7.2` documentation is the
   version family that matches this host.
4. [obs] The supporting kernel accounting source `kernel/sched/psi.c` was fetched from the same tag,
   `https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c`, with sha256
   `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5` (48859 bytes, git blob id
   `e2e825dcd088fcc4563be45fc5ba4bca8e73e4a0`). The kernel.org plain view at the same tag returns the
   identical file.
5. [obs] The frozen capture at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt` has
   sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`, which is the value the
   declaration fixes.

## 2. MP1 — the meaning of the `some` and `full` lines of system memory pressure

6. [obs] The documentation defines the two lines of every pressure file. Quote A, documentation lines
   45 and 46, twenty words:
   `The "some" line indicates the share of time in which at least some`
   `tasks are stalled on a given resource.`
7. [obs] Quote B, documentation lines 48 and 49, twenty words:
   `The "full" line indicates the share of time in which all non-idle`
   `tasks are stalled on a given resource simultaneously.`
8. [obs] Quote C, documentation lines 50 and 51, twenty-two words, gives the consequence of the `full`
   state:
   `actual CPU cycles are going to waste, and a workload that spends`
   `extended time in this state is considered to be thrashing.`
9. [obs] Quote D, documentation lines 37 and 38, eighteen words, places the file:
   `Pressure information for each resource is exported through the`
   `respective file in /proc/pressure/ -- cpu, memory, and io.`
10. [obs] Quote E, documentation lines 42 and 43, shows the field order of a pressure file, five words
   each: `some avg10=0.00 avg60=0.00 avg300=0.00 total=0` and
   `full avg10=0.00 avg60=0.00 avg300=0.00 total=0`.
11. [obs] Quote F, documentation lines 57 and 58, twenty-three words, is the only sentence in the
   document about a system-level `full` line, and it names CPU as the exception:
   `CPU full is undefined at the system level, but has been reported`
   `since 5.13, so it is set to zero for backward compatibility.`
12. [inf] MP1 needs the statement that memory has a system-level `full` line. The documentation states
   the file layout for every resource (quote D and quote E) and states the CPU system-level exception
   (quote F). Because CPU is named as the only resource whose `full` line is undefined at the system
   level, the memory `full` line is defined there. That step is a reading of the document, not a sentence
   in it, and the kernel accounting source makes it explicit.
13. [obs] The kernel accounting source confirms both halves. Quote G, source lines 42 to 44, eleven
    words: `For memory, productive means a running task that isn't a reclaimer.` Quote H, source lines
    1282 and 1283, twenty-one words: `/* CPU FULL is undefined at the system level */` followed by
    `if (!(group == &psi_system && res == PSI_CPU && full)) {`. The guard exempts CPU only, so the
    memory `full` line is exported at the system level. Quote I, source lines 864 to 869, seventeen
    words, gives the memory specific rule: `Since we care about lost potential, a memstall is FULL`
    `when there are no other working tasks`.
14. [obs] Host evidence for MP1 in the capture. The system-level memory read is capture lines 13 to 16.
    Line 14 reads `some avg10=0.02 avg60=0.02 avg300=0.06 total=41385384` and line 15 reads
    `full avg10=0.02 avg60=0.02 avg300=0.06 total=40856373`. Both lines are non-zero, so on this host
    the memory `full` line exists at the system level and carries real stall time. Line 14 and line 15
    each appear exactly once in the capture, and neither is a section header, a command echo or an exit
    line, so both are admissible pointers.

## 3. MP2 — `total` is stall time, so a dated incident needs two reads and a difference

15. [obs] Quote J, documentation lines 62 and 63, thirteen words, states the meaning and the unit of
    the field: `The total absolute stall time` followed by `(in us) is tracked and exported as well`.
16. [obs] Quote K, documentation lines 60 and 61, seventeen words, states the averaging windows:
    `The ratios (in %) are tracked as recent trends over ten, sixty, and`
    `three hundred second windows`
17. [obs] Quote L, documentation lines 63 to 65, states why the total exists next to the averages:
    `to allow detection of latency spikes which wouldn't necessarily make a dent in the time averages`
    followed by `or to average trends over custom time frames.`
18. [unk] The word "cumulative" does not appear in the documentation in connection with the `total`
    field of a pressure file. It appears at lines 73 and 74 in the trigger description, where it
    describes a trigger threshold, not the exported field: `A trigger describes the maximum cumulative
    stall time over a specific` and `time window, e.g. 100ms of total stall time within any 500ms
    window to`. The MP2 statement as written in the declaration says the `total` field is cumulative
    stall time, so the entry must either keep quote L plus the kernel accounting source, or soften the
    wording to "absolute stall time tracked and exported". This is a decision for the L1 and the critic.
19. [obs] The kernel accounting source settles the question directly. Quote M, source lines 408 to 411,
    five words: `group->total[aggregator][s] +=` followed by `div_u64(deltas[s], max(nonidle_total,
    1UL));`. The counter is accumulated, so the exported value is a running total. Quote N, source lines
    1286 and 1287, eight words, fixes the unit: `total = div_u64(group->total[PSI_AVGS][res * 2 +
    full],` followed by `NSEC_PER_USEC);`. The exported total is the accumulated nanosecond counter
    divided by `NSEC_PER_USEC`, so it is microseconds, which agrees with the `(in us)` of quote J.
20. [obs] Host evidence for MP2 in the capture, and this is the two-read demonstration the row needs.
    The first system read is capture lines 13 to 16 with the timestamp at capture line 3
    (`2026-10-22T10:06:23Z`, unique in the capture). The capture sleeps ten seconds at line 17 and
    takes the second system read at capture lines 20 to 23 with the timestamp at capture line 25
    (`2026-10-22T10:06:33Z`). The `some` total moved from `41385384` (line 14) to `41389485` (line 21),
    a difference of 4101 microseconds, and the `full` total moved from `40856373` (line 15) to
    `40860452` (line 22), a difference of 4079 microseconds.
21. [obs] That difference is the point of the row, and the documentation supports it. The averages fell
    between the two reads while the totals rose: `avg10` for `some` moved from `0.02` to `0.00`. The
    documentation states the purpose of exporting the total in exactly this way, quote L at lines 63 to
    65, and the trigger description at lines 73 and 74 also speaks of "cumulative stall time". A dated
    incident therefore cannot be read from a single snapshot of the averages; it needs the total read
    twice and the difference taken.
22. [obs] Capture pointer suitability for MP2, checked line by line. Capture line 3 and capture line 14
    and capture line 15 each appear exactly once in the capture, so they satisfy the uniqueness rule in
    the declaration. Capture line 21 and capture line 22 each appear twice in the capture: the same
    text is repeated at capture line 29 and capture line 30, which are the root cgroup memory pressure
    read at the same instant. The repeated text is itself meaningful, because the root cgroup
    `memory.pressure` totals equal the system totals at that moment. The entry should still cite
    capture line 21 and capture line 22 as the second read, and the L1 should tell the tool author that
    a pointer to a duplicated line is acceptable for the second read, because at least one pointer of
    the row is on a unique line.

## 4. Supersession of the weaker prior statements

23. [obs] The prior lane note `corpus/knowledge/oom-event-plane.md` line 301 records the pressure
    source as `| PSI | /proc/pressure/memory | live (some/full with 10/60/300 s averages) | totals only
    | 14:42: avg300=0.09, total=69,393,986 us |`. That line names the file and the field names but
    does not define `some` against `full`, does not say that the memory `full` line exists at the
    system level, and does not say that the total must be differenced across two reads. The MP1 and MP2
    rows supersede that line and should carry it in the supersedes field.
24. [obs] Line 274 of the same note lists PSI among the pressure signals without semantics. Line 344
    and line 347 of the same note concern the systemd-oomd unit and the pressure watch export; they are
    the weaker prior statements behind MP4 and MP5, not behind MP1 and MP2. MP1 and MP2 do not need to
    absorb them.

## 5. Drafted SOURCES rows for the L1

25. [obs] The next free source id in `corpus/SOURCES.md` is S115. The L1 assigns the final numbers, so
    the ids below are proposals. The row format follows the existing registry table exactly:
    `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.
26. [obs] Proposed primary row, for the pressure stall information documentation, which carries the
    MP1 and MP2 anchors:

| S115 | Linux kernel PSI documentation at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | docs | A | The `some` and `full` semantics of a pressure file, the system-level scope of the memory `full` line, the `total` stall time field and its averaging windows | L37-38 "Pressure information for each resource is exported through the respective file in /proc/pressure/ -- cpu, memory, and io."; L42-43 "some avg10=0.00 avg60=0.00 avg300=0.00 total=0" and "full avg10=0.00 avg60=0.00 avg300=0.00 total=0"; L45-46 "The \"some\" line indicates the share of time in which at least some tasks are stalled on a given resource."; L48-49 "The \"full\" line indicates the share of time in which all non-idle tasks are stalled on a given resource simultaneously."; L50-51 "actual CPU cycles are going to waste, and a workload that spends extended time in this state is considered to be thrashing."; L57-58 "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to zero for backward compatibility."; L60-61 "The ratios (in %) are tracked as recent trends over ten, sixty, and three hundred second windows"; L62-63 "The total absolute stall time (in us) is tracked and exported as well"; L63-65 "to allow detection of latency spikes which wouldn't necessarily make a dent in the time averages"; L64-65 "or to average trends over custom time frames."; raw bytes sha256 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692, identical to the kernel.org plain view of tag v7.2, peeled commit 8d3ae59288f1e7d58d76558a6ee96d533bc5019f | A pressure file reports two lines, `some` for a share of time in which at least some tasks are stalled and `full` for a share of time in which all non-idle tasks are stalled; only CPU `full` is undefined at the system level, so the memory `full` line is defined there; `total` is the absolute stall time in microseconds, and the ratios are ten, sixty and three hundred second averages | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |

27. [obs] Proposed optional second row, for the kernel accounting source, which is what makes the
    "cumulative" wording of MP2 and the memory-specific `full` rule explicit. This row is optional and
    may overlap with a sibling kernel-source seat, so the L1 decides whether to keep it:

| S116 | Linux kernel PSI accounting source at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c | code | A | The memory specific meaning of the `full` line, the system-level export of the memory `full` line, and the accumulation and unit of the exported `total` | L42-44 "For memory, productive means a running task that isn't a reclaimer."; L408-411 "group->total[aggregator][s] += div_u64(deltas[s], max(nonidle_total, 1UL));"; L864-869 "Since we care about lost potential, a memstall is FULL when there are no other working tasks"; L1282-1283 "/* CPU FULL is undefined at the system level */ if (!(group == &psi_system && res == PSI_CPU && full)) {"; L1286-1287 "total = div_u64(group->total[PSI_AVGS][res * 2 + full], NSEC_PER_USEC);"; raw bytes sha256 452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5, identical to the kernel.org plain view of tag v7.2 | The exported total is an accumulated counter divided by NSEC_PER_USEC, so it is microseconds of cumulative stall time and must be differenced across two reads; the system-level export guard exempts CPU only, so the memory `full` line is populated at the system level, and for memory a reclaiming task is not productive | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |

28. [obs] Proposed third row, for the kernel headers, which carry the two structural facts that the
    source files alone only imply: the root cgroup is mapped onto the system group, and the accumulator
    is a plain unsigned 64-bit array with no initialiser. This row is optional and serves MP3 as much
    as MP2, so the L1 may fold it into the second row or drop it:

| S117 | Linux kernel pressure stall headers at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi.h ; https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi_types.h | code | A | The identity of the root cgroup pressure group and the type and initialisation of the stall-time accumulator | psi.h L37-40 "return cgroup_ino(cgrp) == 1 ? &psi_system : cgrp->psi;"; psi_types.h L183 "u64 total[NR_PSI_AGGREGATORS][NR_PSI_STATES - 1];"; raw bytes sha256 cd80982f753aa56eb3b9e16212056d1ac3e9c905f6fd10ce5be1509c0e93b649 for psi.h and 483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc for psi_types.h, each identical to the kernel.org plain view at tag v7.2 | The root cgroup reads the system pressure group, so its pressure files print the same counters as `/proc/pressure`; the stall-time accumulator is an unsigned 64-bit array with no initialiser, so it starts at zero when its group is created | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json |

29. [obs] Every quote in the three proposed rows was checked against the fetched bytes. Each quote is at
    most twenty-five words, the longest being twenty-three words at documentation lines 57 and 58. Each
    quote is a contiguous substring of the source once the wrapped lines are joined by a single space, and
    the line numbers were taken from the fetched copy, not from memory. Every proposed row carries
    status `mined`, opened `2026-10-22`, and a used-by that names both
    `corpus/knowledge/memory-pressure-r25.md` and `corpus/knowledge/memory-pressure-r25.json`, which is
    what the C2 counting rule requires.

## 6. Row to source mapping requested by the seat task

| Fact | MP row | Documentation lines | Capture lines | Notes |
|---|---|---|---|---|
| `some` line definition | MP1 | 45-46 | 14 | capture line 14 is unique in the capture |
| `full` line definition | MP1 | 48-49 | 15 | capture line 15 is unique in the capture |
| `full` means thrashing | MP1 | 50-51 | 15 | capture line 15 is unique in the capture |
| memory file location | MP1 | 37-38 | 13 | capture line 13 is the command echo, not a pointer |
| field order of a pressure file | MP1 and MP2 | 42-43 | 14 | matches the capture field order exactly |
| system-level `full` line, CPU exception | MP1 | 57-58 | 15 | memory is defined there; see finding 12 |
| memory-specific `full` rule | MP1 | kernel source 42-44 and 864-869 | 15 | see proposed row S116 |
| `total` meaning and unit | MP2 | 62-63 | 14 and 21 | microseconds, absolute stall time |
| averaging windows | MP2 | 60-61 | 14 and 21 | ten, sixty and three hundred second windows |
| why the total exists beside the averages | MP2 | 63-65 | 14 and 21 | latency spikes and custom time frames |
| two reads and a difference | MP2 | 73-74 for the cumulative wording, plus kernel source 408-411 | 3, 14, 15, 21, 22 | difference 4101 and 4079 microseconds |
| `total` is a boot-relative accumulator | MP2 | kernel source 173-177, 240, 408-411 and psi_types.h 183 | 14 and 21 | see section 8, findings 34 to 39 |
| the total restarts at boot | MP2 | kernel source 173-177 and 240 | 14 and 21 | the lane's own older readings at SKILL.md 883 and 1213 confirm it |
| root cgroup prints the system group | MP3 subject | psi.h 37-40 | 29 and 30 | explains why capture lines 29 and 30 repeat lines 21 and 22 |

## 7. Findings for the L1, the critic and the tool author

30. [unk] The declaration wording of MP2 uses "cumulative stall time" for the `total` field. The
    pressure stall information documentation does not use that word for the field; it uses it only for
    trigger thresholds at lines 73 and 74. The kernel accounting source at lines 408 to 411 shows the
    accumulation that makes "cumulative" true. The entry should either carry the kernel source as a
    second anchor, or the row wording should be softened. The L1 and the critic own that choice.
31. [obs] The tool author needs to know that capture line 21 and capture line 22 are duplicated in the
    capture by capture line 29 and capture line 30, the root cgroup memory pressure read at the same
    instant. The declaration requires at least one pointer per row on a line whose text is unique, and
    capture line 3, capture line 14 and capture line 15 are unique, so the requirement is met either
    way. If the tool rejects every duplicated pointer, the second read of MP2 would have to be cited
    through the unique timestamps at capture line 3 and capture line 25 instead of the duplicated totals.
32. [obs] The root cgroup totals at capture lines 29 and 30 equal the system totals at capture lines
    21 and 22. This is host evidence for the relationship between the system file and the per-cgroup
    file, which is the MP3 subject. It is reported here for the MP3 owner and is not claimed by MP1 or
    MP2.
33. [obs] The averaging windows named in the documentation, ten, sixty and three hundred seconds, match
    the field names `avg10`, `avg60` and `avg300` that the capture prints at capture lines 14, 15, 21,
    22, 29, 30, 34, 35, 38, 39, 42 and 43. The documentation and the host output agree on the field
    semantics.

## 8. The total is a boot-relative accumulator, verified from the source

34. [obs] The printed `total` is not a lifetime counter. The system-level pressure group is a static
    object. Quote P, source lines 173 to 177, five words plus the declaration:
    `/* System-level pressure and stall tracking */` followed by `struct psi_group psi_system = {`.
    A static object is zero-initialised at boot, and the accumulator array is declared at
    `include/linux/psi_types.h` line 183 as `u64 total[NR_PSI_AGGREGATORS][NR_PSI_STATES - 1];`,
    four words, with no initialiser.
35. [obs] The only write to that array is the accumulation. Quote Q, source lines 408 to 411:
    `/* total= */` followed by `group->total[aggregator][s] +=` and
    `div_u64(deltas[s], max(nonidle_total, 1UL));`. A bounded search of the whole file for writes to
    `group->total[` returns only this statement; the other seven occurrences are reads, a local
    pointer at line 467, a subtraction into the averaging path at line 551, and copies of the separate
    polling aggregator at lines 619, 620, 724 and 1395. The scope of that search is the accounting
    source and its type header at tag v7.2, not the whole kernel tree, so it shows that the printed
    counter has no decrement path in the code that produces it. It does not exclude every other
    kernel path, and a reboot is a sufficient ordinary explanation for a decrease rather than the only
    possible one.
36. [obs] The initialisation path does not reset it. Quote R, source lines 240: `group_init(&psi_system);`,
    one word, and the body of `group_init` at source lines 205 to 226 contains zero occurrences of
    the word `total`. The per-cgroup path is the same shape: `cgroup->psi = kzalloc_obj(struct
    psi_group);` at source line 1117 gives a zeroed group, and `psi_cgroup_restart` at source lines
    1216 to 1248 only restarts the per-cpu state masks and never touches the accumulator.
37. [inf] The consequence, stated so it can be checked: within one boot the printed `total` only
    grows, and it restarts at zero on the next boot. The `/proc/pressure/memory` file is served by the
    system group. Quote S, source lines 1543 to 1546: `return psi_show(m, &psi_system, PSI_MEM);`,
    four words, inside `psi_memory_show`. A difference between two reads is therefore meaningful only
    when both reads come from the same boot. A decrease between two reads has an ordinary
    explanation, a reboot or a cgroup recreation between them, and this does not by itself establish
    the absence of a kernel defect. This conclusion rests on the newly opened kernel sources alone,
    which the declaration at `SCORECARD.md` line 788 admits, so it can carry a counted MP2 verdict;
    the host confirmation in findings 38 and 39 comes from outside the frozen capture and cannot.
38. [obs] The host bears this out on this very capture, but by evidence outside the frozen capture.
    The current boot time from `/proc/stat` is `btime` 1792655724, which is 2026-10-22T07:55:24Z, and
    `/proc/uptime` read at 2026-10-22T10:37:10Z was 9706.61 seconds. The capture was taken at
    2026-10-22T10:06:23Z, 7859 seconds after that boot, so the capture total of 41385384 microseconds
    is 41.39 seconds of memory stall since that boot, about 0.53 percent of the elapsed uptime. The
    capture script at `.ufo/waves/round-25/capture/capture.sh` records no boot id, no boot time and no
    uptime, and the capture text contains no such line. Under the declaration at `SCORECARD.md` line
    788, C2 reads only this round's host capture, newly opened sources and its own entry, so these
    host figures cannot back a counted MP2 verdict. They can carry a limit line or a round-26 capture
    item, and the boot id belongs in the round-26 capture rather than widening C2. Inside the frozen
    capture the same-boot property is an inference from one script run, a ten second sleep between the
    two reads, and totals that only increased.
39. [obs] The lane's own older readings confirm the reset, and they carry the same boundary. `SKILL.md`
    line 883 records `C6_psi_full_total_us=68625258` in the census run stamped 2026-10-14T18:39:42Z,
    and `SKILL.md` line 1213 records `C6_psi_full_total_us=72403325` in the run stamped
    2026-10-14T20:10:48Z. Those two grew within the 2026-10-14 boot. The round-25 capture on
    2026-10-22 reads 40856373 microseconds, smaller despite being eight days later, which is what a
    boot reset produces. The census script reads that field from the `full` line at
    `tools/tsukuroi-census.sh` lines 1105 to 1112, so the comparison is like for like. These readings
    are lane files and not part of the frozen capture, so like the host reads above they support a
    limit line and a round-26 capture item, not a counted MP2 verdict.
40. [inf] The per-cgroup files carry the same property with a different epoch. Each cgroup gets a
    zeroed group at creation and the group is freed at cgroup teardown, `kfree(cgroup->psi);` at
    source line 1146. A per-cgroup `total` therefore counts from that cgroup's creation, not from
    boot, and it restarts if the cgroup is removed and recreated. The lifetime of the group is the
    lifetime of the cgroup. On this host the cgroup lifetime of `user@1000.service` is the user
    manager's lifetime rather than a session's, because the account lingers. `loginctl show-user 1000`
    reports `Linger=yes`, `Sessions=2 1` and `State=active`, and `systemctl show` puts the
    `ActiveEnterTimestamp` of `user@1000.service` and of `user-1000.slice` at Thu 2026-10-22
    04:55:44 -03, and of `user.slice` at Thu 2026-10-22 04:55:41 -03, all within seconds of the boot
    at 07:55:24Z. The systemd v262 login manager starts lingering users at startup, `HASHMAP_FOREACH(user,
    m->users) (void) user_start(user);` at `src/login/logind.c` lines 1301 to 1302, and it refuses to
    garbage collect a lingering user whose unit is still active, `if (user_check_linger_file(u) > 0 &&
    (!drop_not_started || user_unit_active(u)))` at `src/login/logind-user.c` line 828. So the service
    cgroup is created at boot and torn down only when the user manager itself is stopped or killed,
    as in event B. The rule for MP3 is therefore: a per-cgroup total counts from that cgroup's
    creation, and a comparison across a user manager restart must use `user-1000.slice` or
    `user.slice`, not `user@1000.service`. The linger state is outside the frozen capture and belongs
    with the boot id as a round-26 capture item rather than as a counted verdict. This belongs to the
    MP3 row and is reported here for its owner rather than claimed by MP1 or MP2.
41. [obs] The root cgroup is the exception and it explains the duplicated capture lines. Quote T,
    `include/linux/psi.h` lines 37 to 40: `return cgroup_ino(cgrp) == 1 ? &psi_system : cgrp->psi;`,
    eight words. The root cgroup is mapped onto the system group itself, so the root cgroup
    `memory.pressure` file and `/proc/pressure/memory` print the same counters. That is why capture
    lines 29 and 30 carry exactly the text of capture lines 21 and 22. It is a property of the
    kernel, not a repeated line in the capture, and it belongs to the MP3 row.

## 9. Round-26 capture item proposed from this seat

42. [obs] The frozen capture cannot answer the boot question, because
    `.ufo/waves/round-25/capture/capture.sh` records no boot identity. The script runs a date, the
    kernel release, the systemd version, the two pressure reads, the cgroup pressure files, the
    cgroup memory and swap event files, the kernel OOM counter, the memory and swap figures, the
    oomd unit state, the oomd configuration, the managed OOM properties and the manager defaults. No
    line of it identifies the boot. A round-26 capture should add one read-only line carrying the boot
    id, for example `cat /proc/sys/kernel/random/boot_id`, which on this host is
    `6a7f4fdf-ac62-4e2e-a6c1-b3c55d6f94f4` and matches the current journal boot identifier, so that a
    total can be tied to the boot that produced it. That is a capture item for the next round and not
    a widening of C2.
43. [obs] A second capture item follows from the same limit: when two reads of the same pressure file
    are taken for an interval measurement, the capture should record the boot id alongside them, so the
    difference is verifiable as a same-boot interval rather than inferred from the totals alone.
44. [obs] A third capture item follows from the per-cgroup epoch in finding 40. The capture records no
    unit start time and no linger state, so the epoch of a per-cgroup total cannot be established from
    it. The proposed lines are `systemctl show -p ActiveEnterTimestamp -- user@1000.service` and
    `loginctl show-user 1000`, the latter carrying `Linger` and `Sessions`. On this host those give
    `Linger=yes`, `Sessions=2 1` and an `ActiveEnterTimestamp` of Thu 2026-10-22 04:55:44 -03, so the
    user manager cgroup dates from the boot rather than from any session.

## 10. Sibling lane overlap with mori, reported not absorbed

45. [obs] The sibling lane mori already holds registry rows for the same two upstream pages. At commit
    `4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e` of `/home/vgpnk/Projects/shokunin/mori-shokunin`, its
    `corpus/SOURCES.md` carries row S090 for the v7.2 pressure stall information documentation and
    row S091 for the v7.2 `kernel/sched/psi.c`, and its note
    `corpus/knowledge/system-pressure-r24.md` states the units and windows at its lines 89 to 93 under
    the heading "F4 — units and windows", the monotonic accumulation at its lines 146 to 150 under the
    heading "F10 — the kernel accumulates the total monotonically", and at its line 144 that the root
    cgroup pressure files print the same `psi_system` group as `/proc/pressure`.
46. [obs] Those mori rows sit in mori's own registry and cannot be cited by the tsukuroi entry, because
    the C2 counting rule requires a `mined` row in `corpus/SOURCES.md` of this lane whose used-by names
    `corpus/knowledge/memory-pressure-r25.md`. The tsukuroi registry therefore needs its own rows for
    the same two pages, which is what the proposed rows in section 5 are for. The next free id in
    this lane's registry is S115; mori's S090 and S091 are a different lane's numbering and carry no
    meaning here.
47. [obs] The scope boundary holds. Mori owns the CPU, IO and IRQ pressure reading; tsukuroi's PROVINCE
    core is the OOM and memory plane, so the memory `some` and `full` reading and the `total` field
    are tsukuroi's own subject and are sourced here from the primary pages. Nothing in section 7 asks
    for fleet or wave attribution of a pressure event, which is the part ADJ-04 routes to mori.
48. [obs] The observation at finding 32 about the root cgroup totals equalling the system totals in the
    same capture pass agrees with mori's line 144 statement that the root cgroup pressure files print
    the same `psi_system` group. It is reported here for the MP3 owner and is not claimed by MP1 or
    MP2, and it is not re-derived from mori's note.

Scope: read=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst, https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c, https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi.h, https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi_types.h and https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/cgroup/cgroup.c, each of the five also fetched from git.kernel.org at tag v7.2, https://raw.githubusercontent.com/systemd/systemd/v262/src/login/logind.c and https://raw.githubusercontent.com/systemd/systemd/v262/src/login/logind-user.c, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt and capture.sh, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md round 25 declaration, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md including its census lines 883, 1041 and 1213, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh lines 1100 to 1115, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md ADJ-04 and OUT-005, the live host files /proc/uptime, /proc/stat and /proc/sys/kernel/random/boot_id, and the sibling lane files corpus/SOURCES.md and corpus/knowledge/system-pressure-r24.md read at commit 4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e of /home/vgpnk/Projects/shokunin/mori-shokunin with git show; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/SrcPsiDoc.md and scratch copies under /fast/scratch/hyaku/tsukuroi-r25/SrcPsiDoc/; executed=curl fetch of the five kernel files from raw.githubusercontent.com and from git.kernel.org plus the two systemd v262 login manager files, git ls-remote --tags for tag v7.2, sha256sum and diff for byte identity, python3 quote and word-count verification against the fetched bytes, grep and read for the capture, the capture script, the scorecard, the prior note, the census script, the province table and the sibling lane files, and the read-only host reads cat /proc/uptime, cat /proc/sys/kernel/random/boot_id, awk over /proc/stat for btime, journalctl --list-boots, loginctl show-user 1000, systemctl show for the three user units, and cat of /proc/pressure/memory and the two cgroup pressure files. No host command that changes state was run.
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
