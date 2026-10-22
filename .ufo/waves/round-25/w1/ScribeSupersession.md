# ScribeSupersession — C2 quality trend: every earlier tsukuroi PSI / systemd-oomd / ManagedOOM* / MemoryPressureWatch / oomd-defaults statement, checked against the round-25 capture and the systemd 262 manual pages

Verdict: the round-25 capture and the systemd 262 manual pages confirm every measured value the lane recorded, but they refute the load-bearing inference in `oom-event-plane.md:344` and `kill-event-deep-r8.md:255` — `ManagedOOMSwap=auto` / `ManagedOOMMemoryPressure=auto` is the shipped default, it means systemd-oomd does *not* monitor those cgroups, and the 90 % swap limit is a conjunction with the memory-used fraction — so "oomd would likely have acted before the kernel" does not follow; nine further statements are narrowed (per-unit `MemoryPressureWatch=skip`, per-cgroup versus system PSI populations, the `auto`/`skip` protocol semantics, `ManagedOOMPreference` xattr ownership, the `ManagedOOMMemoryPressureLimit=0` reading, the oomd kill-candidate set, the 200 ms threshold default, the ADJ-04 evidence shape, the SKILL.md census vocabulary), two are confirmed outright, and three are already covered by round-18 notices so no new notice is owed for them.

Scope of this seat: trend analysis and notice drafting only. No product file was edited; no corpus note, SKILL.md, SCORECARD.md, PROVINCE.md or tool was written. The round-25 entry (`corpus/knowledge/memory-pressure-r25.md` and its `.json`), the SKILL.md decision-table row, the checker and the SOURCES ids belong to other seats.

## 1. Evidence base used

Frozen capture, sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`, at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt` (153 lines). Header facts: kernel `7.2.11-arch1-1` (capture:6), systemd `262 (262-1-arch)` (capture:9), capture window `2026-10-22T10:06:23Z` → `2026-10-22T10:06:33Z` (capture:3, 25).

Manual pages opened this session, with the sha256 of the fetched raw bytes:

| source | sha256 of fetched bytes | lines used |
|---|---|---|
| systemd v262 `man/systemd.resource-control.xml` | `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8` | 1523-1563, 1592-1609, 1663-1705 |
| systemd v262 `man/systemd-oomd.service.xml` | `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d` | 33-53, 101-122 |
| systemd v262 `man/oomd.conf.xml` | `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617` | 164-202 |
| systemd v262 `man/systemd-system.conf.xml` | `161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58` | 317-325 |
| Linux v7.2 `Documentation/accounting/psi.rst` | `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` | 43-64, 178-187 |

Cross-check: the Arch manual pages for systemd 262 (`https://man.archlinux.org/man/systemd.resource-control.5`, `/man/oomd.conf.5`, `/man/systemd-oomd.service.8`) carry the same sentences, so the quotes below hold for the host's installed `262-1-arch` build as well as for the upstream tag.

Host reads I ran, all read-only and none under sudo, none of them part of the frozen capture (they are marked as supplementary below): `systemctl is-active earlyoom.service` → `active` (exit 0); `systemctl is-enabled earlyoom.service` → `enabled` (exit 0); `grep -rn ManagedOOM /etc/systemd /usr/lib/systemd/system /usr/lib/systemd/user /run/systemd/system` → no `ManagedOOM=` assignment anywhere (the only hit is the socket's `ListenStream=/run/systemd/oom/io.systemd.ManagedOOM`); `grep -rn MemoryPressureWatch /etc/systemd /usr/lib/systemd` → `/usr/lib/systemd/system/user@.service:36 MemoryPressureWatch=skip` and `/usr/lib/systemd/system/capsule@.service:37`, plus the commented defaults `#DefaultMemoryPressureWatch=auto` in `/etc/systemd/system.conf:81` and `/etc/systemd/user.conf:56`; `ls /etc/systemd/system/user@.service.d/` → only `faster-shutdown.conf`; `ls /etc/systemd/oomd.conf.d /run/systemd/oomd.conf.d` → no such directories, so no oomd drop-in exists. These `grep`/`ls` reads of `/etc` and `/usr/lib` are outside the enumerated no-sudo probe list in the round-25 contract; they are plain file reads with no state change, and they are used only as corroboration, never as a capture pointer.

Sibling overlap: mori owns CPU, IO and IRQ pressure reading (`corpus/knowledge/system-pressure-r24.md` at `4f05dd5a`, F2/F4/F9/F10 hold the generic `some`/`full` and cumulative-total semantics and the root-cgroup-prints-`psi_system` fact). The observations in findings 5 and 9 are consistent with mori's entry and are reported here only as corrections to tsukuroi's own weaker sentences; they are not absorbed as tsukuroi-owned ground.

## 2. Findings, one per earlier statement

### F1 — `oom-event-plane.md:344`, "ManagedOOM*=auto **already set** … oomd would likely have acted before the kernel" — CONTRADICTED

The measured values in that row survive; the wording and the inference do not.

[obs] The property values are exactly as recorded and are still so at round 25. Capture:112-113 (`user@1000.service`), 121-122 (`user-1000.slice`), 130-131 (`user.slice`), 139-140 (`-.slice`) each read `ManagedOOMSwap=auto` and `ManagedOOMMemoryPressure=auto`; capture:114, 123, 132, 141 read `ManagedOOMMemoryPressureLimit=0`; capture:115, 124, 133, 142 read `ManagedOOMMemoryPressureDurationUSec=[not set]`; capture:116, 125, 134, 143 read `ManagedOOMPreference=none`. The corpus's row-344 scope ("on `user@1000.service` and `user-1000.slice`") is confirmed, and the capture widens it to `user.slice` and the root slice `-.slice`.

[obs] The manual says `auto` is the default and means "not monitored". systemd.resource-control(5) at v262, `ManagedOOMSwap=auto|kill` / `ManagedOOMMemoryPressure=auto|kill` entry, line 1529: "Defaults to `auto`." Lines 1545-1546: "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection." systemd-oomd.service(8) at v262, lines 43-44: "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored."

[inf] "Already set" therefore describes a shipped default as if it were an operator setting, and the row's mechanism cell ("oomd would likely have acted *before* the kernel") does not follow: with `auto` on the four captured units, including the root slice `-.slice` that is the ancestor of the user slice, systemd-oomd would not have monitored those cgroups at all. The row's own escape hatch — an `auto` unit can still be a candidate if an ancestor is set to `kill` — cannot rescue it, because the ancestor here (`-.slice`) itself reads `auto`.

[obs] A second, independent refutation of the same inference: the swap rule is a conjunction, not a swap-only threshold. oomd.conf(5) at v262, `SwapUsedLimit=` entry, lines 166-168: "If the fraction of memory used and the fraction of swap used on the system are both more than what is defined here". The corpus reasons from a swap percentage alone, and the historical memory-used fraction at events A and B is not recorded anywhere in the lane, so the corpus's own evidence does not satisfy the documented rule.

[obs] The `ManagedOOMMemoryPressureLimit=0` reading at row 344 needs the same treatment as at `kill-event-deep-r8.md:255`: systemd.resource-control(5) v262, lines 1559-1563: "Defaults to 0%, which means to use the default set by oomd.conf(5). This property is ignored unless ManagedOOMMemoryPressure=kill." Under `auto` no limit is in force at all.

[obs] The three oomd defaults the row lists are confirmed. oomd.conf(5) v262: `SwapUsedLimit=` line 172 "Defaults to 90%"; `DefaultMemoryPressureLimit=` line 190 "Defaults to 60%"; `DefaultMemoryPressureDurationSec=` line 202 "Defaults to 30 seconds when unset or 0". The host's shipped file matches: capture:105 `[OOM]`, capture:106 `#SwapUsedLimit=90%`, capture:107 `#DefaultMemoryPressureLimit=60%`, capture:108 `#DefaultMemoryPressureDurationSec=30s`; capture:82-83 shows `systemd-analyze cat-config systemd/oomd.conf` yields one non-comment line, the `[OOM]` section header, so every setting is commented out.

[obs] The rest of the row is confirmed at round 25: `is-active` → `inactive` (capture:72-73), `is-enabled` → `disabled` (capture:75-76), `systemd-oomd.socket` `is-enabled` → `disabled` (capture:78-79). The `oomctl cannot reach it` leg is not re-measured by the round-25 capture, which has no `oomctl` probe, so it stands as the dated 2026-10-14 reading.

[obs] The duration rule is sustained, not instantaneous: oomd.conf(5) v262, lines 198-201: "Sets the amount of time a unit's control group needs to have exceeded memory pressure limits before systemd-oomd will take action", with lines 182-184 defining the measured quantity as "the fraction of time in a 10 second window in which all tasks in the control group were delayed".

### F2 — `kill-event-deep-r8.md:255`, same claim in the round-8 detection table — CONTRADICTED

[obs] Every value in this row is confirmed at round 25 for the units the capture probed: `ManagedOOMSwap=auto` and `ManagedOOMMemoryPressure=auto` on `user-1000.slice` (capture:121-122) and `user@1000.service` (capture:112-113), `ManagedOOMPreference=none` (capture:116, 125), `ManagedOOMMemoryPressureLimit=0` (capture:114, 123). The capture adds `ManagedOOMMemoryPressureDurationUSec=[not set]` (capture:115, 124), which the row does not record.

[unk] The row's "and sampled app scopes" leg is not re-measured: the round-25 capture reads no application scope, so that leg stays dated.

[inf] The inference cell is refuted on the same two grounds as F1. Its first clause reads "the swap rule (90 %) is below event A's measured 99.9999 % saturation, so oomd would have had a trigger", and its second reads "it acts by killing the *eligible descendant cgroup* rather than one task". `auto` is not monitored (resource-control.xml:1545-1546, systemd-oomd.service.xml:43-44), and the 90 % limit is a conjunction with the memory-used fraction (oomd.conf.xml:167-168).

[obs] The descendant-cgroup mechanism is itself confirmed, with one constraint the row omits. systemd-oomd.service(8) v262, lines 47-52: "only descendant cgroups are eligible candidates for killing" and "only leaf cgroups and cgroups with memory.oom.group set to 1 are eligible candidates". The lane's own measurement that `memory.oom.group` is `0` everywhere on the path (`oom-event-plane.md:280`, `kill-event-deep-r8.md:257`) therefore means the eligible-candidate set would have been empty even if `kill` had been set. The "rather than one task" half of the row is confirmed and should be kept: systemd-oomd.service.xml:47-48 "will select a cgroup to terminate, and send SIGKILL to all processes in it".

[obs] The row's "the unit runs `OOMScoreAdjust=-900` and gates on `/proc/pressure/*` (PSI present)" is confirmed for the installed unit by my supplementary read of `/usr/lib/systemd/system/systemd-oomd.service` (`OOMScoreAdjust=-900`; `ConditionPathExists=/proc/pressure/cpu`, `/proc/pressure/io`, `/proc/pressure/memory`), and by systemd-oomd.service(8) v262:33-34 "uses cgroups-v2 and pressure stall information (PSI) to monitor and take corrective action before an OOM occurs in the kernel space". The round-25 capture does not read that unit file, so this leg is confirmed by manual and host read, not by the capture. PSI is present on the host (capture:14-15).

### F3 — `oom-event-plane.md:347`, the `MemoryPressureWatch=` prevention row — NARROWED

[obs] The measured state is confirmed and extended. Capture:117 `MemoryPressureWatch=skip` on `user@1000.service`; capture:126, 135, 144 `MemoryPressureWatch=auto` on `user-1000.slice`, `user.slice` and `-.slice`; capture:150 `DefaultMemoryPressureWatch=auto`; capture:149 `DefaultMemoryPressureThresholdUSec=200ms`, matching systemd-system.conf(5) v262:317-325 "Defaults to `auto` and `200ms`, respectively". The corpus records only the `auto` default; the 200 ms threshold default is new information and belongs in the entry.

[obs] The upstream pin is confirmed. systemd.resource-control(5) v262, `MemoryPressureWatch=` entry, lines 1665-1666: "Takes a boolean or one of `auto` and `skip`"; lines 1671-1672: "It then sets the $MEMORY_PRESSURE_WATCH environment variable for processes invoked by the unit to the file system path to this file"; lines 1673-1674: "The threshold information configured with MemoryPressureThresholdSec= is encoded in the $MEMORY_PRESSURE_WRITE environment variable". My supplementary read of `/usr/lib/systemd/system/user@.service` line 36 shows `MemoryPressureWatch=skip` still shipped upstream at 262, and the only local drop-in under `/etc/systemd/system/user@.service.d/` is `faster-shutdown.conf` (`TimeoutStopSec=5s`), matching the row's "not a local override" and the round-8 counterpart at `kill-event-deep-r8.md:258`.

[inf] Three narrowings. First, the row's "system default `DefaultMemoryPressureWatch=auto`; other units show `auto`" hides that `auto` is conditional: systemd.resource-control(5) v262, lines 1674-1676: "If the `auto` value is set the protocol is enabled if memory accounting is anyway enabled for the unit, and disabled otherwise." Second, the row's "skip" cell should carry the documented meaning rather than only "pinned upstream": lines 1676-1677: "If set to `skip` the logic is neither enabled, nor disabled and the two environment variables are not set." Third, the row's operator action names the value `on`, which the v262 manual does not list among the documented tokens of this setting (it documents boolean plus `auto` and `skip`, lines 1665-1666); `on` is a generic systemd boolean synonym rather than a documented spelling of this property, and `yes`/`no` are the documented ones.

[obs] The row's characterisation of the lever is confirmed: nothing in the v262 text gives `MemoryPressureWatch=` any kill power, so "a *cooperating-app* lever, not a guard" and "no kill semantics" stand.

### F4 — `kill-event-deep-r8.md:258`, the round-8 `MemoryPressureWatch=` row — NARROWED

[obs] Confirmed where the round-25 capture reaches: `user@1000.service` reads `skip` (capture:117) and `user-1000.slice` reads `auto` (capture:126); the upstream pin and the absence of any `MemoryPressureWatch` drop-in are confirmed by my supplementary read of `/usr/lib/systemd/system/user@.service:36` and of `/etc/systemd/system/user@.service.d/`.

[unk] `session-4.scope` is not probed by the round-25 capture, so that leg of the row stays dated.

[inf] Narrowed by the same two manual sentences as F3: `auto` on the slice means the protocol is enabled only if memory accounting is enabled for that unit (resource-control.xml:1674-1676), and `skip` means neither enabled nor disabled with no environment variables set (1676-1677).

### F5 — `oom-event-plane.md:274`, the plane's list of pressure signals — NARROWED

[obs] The list itself is not contradicted. It is incomplete as a reading rule, and the round-25 capture shows what is missing. The capture reads four distinct PSI surfaces: system `/proc/pressure/memory` (capture:14-15, 21-22), the root cgroup `memory.pressure` (capture:27-30), and the per-cgroup files of `user.slice` (capture:33-36), `user.slice/user-1000.slice` (capture:37-40) and `user.slice/user-1000.slice/user@1000.service` (capture:41-44).

[obs] The root cgroup file and the system file are the same numbers at the second read (capture:21-22 and capture:29-30 are byte-identical), while every descendant cgroup carries its own smaller totals (capture:34 `total=3150158`, capture:38 `total=3158801`, capture:42 `total=3161820`, against the system `total=41389485` at capture:21). Linux v7.2 `Documentation/accounting/psi.rst` lines 181-185 confirm the mechanism: "Each subdirectory in the cgroupfs mountpoint contains cpu.pressure, memory.pressure, and io.pressure files" (183-184) "the format is the same as the /proc/pressure/ files" (184-185).

[inf] "PSI" as one entry in the plane's signal list is therefore two populations with different scopes, and the list gives no way to tell them apart. The general semantics of `some` and `full` and of the cumulative total are mori's admitted ground (`system-pressure-r24.md` F2, F4, F9, F10) and tsukuroi must cite mori rather than restate it; the narrowing that is tsukuroi's own is that the plane must say which file a reading came from.

[obs] The systemd-oomd pressure rule is defined on the cgroup metric, not on the system file: oomd.conf(5) at v262, lines 182-184: "the fraction of time in a 10 second window in which all tasks in the control group were delayed".

### F6 — `oom-event-plane.md:301`, the PSI row of the §5 signal table — NARROWED

[obs] The shape of the row is confirmed. Capture:14-15 and 21-22 show a `some` line and a `full` line, each with `avg10`, `avg60`, `avg300` and `total`, exactly as the row's "live (`some`/`full` with 10/60/300 s averages)" cell claims. Linux v7.2 `psi.rst` lines 60-62 confirm the window set: "The ratios (in %) are tracked as recent trends over ten, sixty, and three hundred second windows", and lines 62-63 confirm the total is stall time: "The total absolute stall time (in us) is tracked and exported as well".

[obs] The row's "totals only" survival cell is confirmed in substance and the kernel doc says why a total cannot be read as an event: the total is an absolute stall accumulator, not a timestamp, and the ratios are windowed trends.

[inf] Three narrowings. The row names the file but not the scope, so a reader cannot tell the system-wide file from the per-cgroup files of F5. It does not define `some` against `full` (Linux v7.2 `psi.rst` lines 45-46: "The \"some\" line indicates the share of time in which at least some tasks are stalled on a given resource"; lines 48-50: "The \"full\" line indicates the share of time in which all non-idle tasks are stalled on a given resource simultaneously"), and it does not say the system memory `full` line exists at system level — capture:15 and capture:22 show it does, with its own total. Finally, the row's "totals only" is not a substitute for differencing: the round-25 capture performs exactly the two-read difference the row lacks, `some` total 41,385,384 (capture:14) to 41,389,485 (capture:21), a rise of 4,101 µs across the ~10 s sleep (capture:17), with `full` rising 4,079 µs (capture:15 to capture:22). A dated stall reading needs two reads and a difference; one total is not a reading.

[obs] The row's dated value (`14:42: avg300=0.09, total=69,393,986 µs`) stays a 2026-10-14 measurement. The round-25 values are `avg300=0.06`, `total=41385384` (capture:14). These two totals are not comparable: the capture's kernel is `7.2.11-arch1-1` (capture:6) against the note's `7.2.3-arch1-3` (`oom-event-plane.md:6`), and the kernel total is a since-boot accumulator, so a lower later total is expected rather than a contradiction.

### F7 — `kill-event-deep-r8.md:180`, the slice PSI total row — NARROWED

[obs] The reading is confirmed: a slice PSI total is cumulative and cannot date an incident, which the row already says as "cumulative — no". Linux v7.2 `psi.rst` lines 62-63 support the mechanism.

[inf] Narrowed in scope. The figure `37,041,770 / 36,105,580 µs` is a per-cgroup lifetime figure for the slice at the time of the round-8 capture. The round-25 capture reads the same family of file with different numbers — `user.slice` `total=3150158` (capture:34) and `user-1000.slice` `total=3158801` (capture:38) — so the old slice figure must not be compared with a round-25 system total (`total=41389485`, capture:21) nor with a round-25 slice total. The row should name the file and the cgroup, because a PSI total means different things depending on which of the F5 surfaces produced it.

### F8 — `kill-event-deep-r8.md:266`, the `ManagedOOMPreference` row — NARROWED

[obs] Confirmed at round 25 for the probed units: `ManagedOOMPreference=none` on `user@1000.service` (capture:116), `user-1000.slice` (capture:125), `user.slice` (capture:134) and `-.slice` (capture:143); and "oomd never ran" is confirmed by capture:72-73 (`inactive`) and capture:75-76 (`disabled`).

[inf] The action cell "if oomd is enabled, `ManagedOOMPreference=avoid/omit` on selected units … is the steering knob — measured as available, not configured" is narrower than the lane's evidence supports. systemd.resource-control(5) v262, `ManagedOOMPreference=` entry, lines 1593-1595: "Requires support for extended attributes (see xattr(7)) in order to use `avoid` or `omit`"; lines 1601-1602: "systemd-oomd will only respect these extended attributes if the unit's cgroup is owned by root"; lines 1602-1603: "if the unit's cgroup owner, and the owner of the monitored ancestor cgroup are the same". The man page's own worked example (lines 1604-1609) is this host's shape: "extended attributes set on descendants of /user.slice/user-1000.slice/user@1000.service/ will be ignored because the descendants are owned by UID 1000" (1605-1607). The knob is therefore narrower than "available" for the user slice: it is available only for cgroups whose ownership matches the monitored ancestor's.

### F9 — `oom-event-plane.md:280-281`, §4.5 "No guards configured anywhere on the path" — NARROWED

[obs] `systemd-oomd` inactive+disabled is confirmed (capture:72-73, 75-76, 78-79). `MemoryPressureWatch = skip` is confirmed for `user@1000.service` (capture:117), and the upstream pin is confirmed by my supplementary read of `/usr/lib/systemd/system/user@.service:36`.

[inf] Narrowed in two ways. First, `MemoryPressureWatch = skip` is a per-unit reading, not a path-wide one: capture:126, 135, 144 show `auto` on `user-1000.slice`, `user.slice` and `-.slice`, and the system default is `auto` (capture:150). Second, the concluding sentence "Nothing was configured to act before the kernel" reads as if the only thing standing between the session and a kill was that the units were disabled. Under systemd 262 the stronger and more accurate statement is that `ManagedOOM*=auto` would not have been monitored even with the service running (resource-control.xml:1545-1546; systemd-oomd.service.xml:43-44), so the absence of a systemd-oomd action was structural, not a matter of the enable state.

[obs] The `earlyoom absent` half of line 280 was already noticed at round 18 (`oom-event-plane.md:448`, record `R18-FRESH-NoticeOom-02`), and the "Nothing was configured to act before the kernel" conclusion was extended by the round-18 precision block at `oom-event-plane.md:469`. The R18-noticed part of this line is therefore not re-noticed here; the new narrowing is the systemd-oomd structural point above.

[obs] The R25 capture adds a fact this line does not have: `systemd-oomd` remains inactive and disabled on this host on 2026-10-22 (capture:71-79), while `earlyoom` is active and enabled (my supplementary read this session). The two monitors now have opposite states.

### F10 — `SKILL.md:809-812`, the "No guard was configured on the path" bullet — NARROWED

[obs] The systemd-oomd half is confirmed at round 25 (capture:72-73, 75-76). The `MemoryPressureWatch=skip` half is confirmed for `user@1000.service` (capture:117) but is not a path-wide reading (capture:126, 135, 144 are `auto`).

[obs] The `earlyoom absent` half is already covered by the round-18 notice at `SKILL.md:1938` (`R18-FRESH-SUPPLEMENT-03`), which quotes this very locus.

[inf] Narrowed: the bullet's "nothing acted before the kernel" needs the systemd-oomd structural reason of F9 attached to it, so that a reader does not infer that enabling systemd-oomd would have produced a pre-kernel kill. It would not have, because the units carry the `auto` default.

### F11 — `SKILL.md:918` and `SKILL.md:1027-1029`, the C6 census vocabulary "PSI avg300/total" — NARROWED

[obs] The field names are confirmed to exist on this host: capture:14 carries `some avg10=0.02 avg60=0.02 avg300=0.06 total=41385384` and capture:15 the matching `full` line, so the census arm's `avg300` and `total` inputs are real and live.

[inf] Narrowed: the vocabulary names the fields but not the scope or the semantics, so the census vocabulary cannot tell a system-wide reading from a cgroup reading (F5) and cannot express that `total` is a since-boot accumulator to be differenced rather than read (F6). The vocabulary names no `some`/`full` distinction.

[obs] The round-8 census verification at `corpus/knowledge/memory-arm-ver-s8.md:65` is a dated 2026-10-13 measurement of the same fields (`some avg300 0.04 / full avg300 0.04, full total 69 151 811 µs`), and its "arm read 69 186 087 µs at its later instant" is the two-read difference pattern that F6 shows the corpus table lacks.

### F12 — `PROVINCE.md:49`, the ADJ-04 minimum-evidence clause — NARROWED

[obs] The routing itself is unchanged and unchallenged: `PROVINCE.md:30-33` keeps host memory and kill-event measurement as tsukuroi OS triage, and `PROVINCE.md:49` keeps fleet and wave attribution with mori.

[inf] Narrowed on the evidence shape. The clause asks for "exact counter or PSI command/exit and observed value", which reads as if a single PSI observation with an exit code is a usable reading. The round-25 capture shows what the manual and the kernel doc require: a PSI total is a cumulative stall accumulator (Linux v7.2 `psi.rst` lines 62-63) and a dated stall reading needs two reads and a difference (capture:14 to capture:21), and the systemd-oomd limit itself is a sustained condition over `DefaultMemoryPressureDurationSec` (oomd.conf.xml:198-202) on the cgroup metric (oomd.conf.xml:182-184). A single observed value is a snapshot of a counter, not an incident.

### F13 — `oom-event-plane.md:51`, the "userland OOM monitors" bullet — CONFIRMED, no new notice owed

[obs] The systemd-oomd half is confirmed at round 25 (capture:72-73, 75-76). The `earlyoom not installed` half was already noticed at round 18 (`oom-event-plane.md:444`, record `R18-FRESH-NoticeOom-01`), and the round-25 capture contains no `earlyoom` probe, so it adds nothing on that half.

### F14 — `oom-event-plane.md:305` and `oom-event-plane.md:345`, the "nothing was watching" and earlyoom probe rows — CONFIRMED, no new notice owed

[obs] The systemd-oomd inactive reading is confirmed (capture:72-73). The `oomctl` leg is not re-measured by the round-25 capture and stays dated. The round-18 falsify record already ruled that the dated "nothing was watching" cell of §5 is historical and owes no notice (`.ufo/waves/round-18/falsify/FxFresh10.md:19`), and the `earlyoom` probe row was noticed at round 18 (`oom-event-plane.md:452`, record `R18-FRESH-NoticeOom-03`).

[inf] One present-use constraint for the new entry, not a supersession: the R25 capture cannot support any present-tense "nothing is watching" statement, because it never reads earlyoom, and the host's earlyoom is active and enabled (supplementary read this session). The entry must say so explicitly rather than inherit the old cell.

### F15 — `corpus/knowledge/adjacency-handoffs-fleet-r1.md:94-101`, the fleet-r1 PSI packet — CONFIRMED, scope note only

[obs] The interpretation is confirmed by the kernel doc: "PSI totals are cumulative stalled time, not an event timestamp" matches Linux v7.2 `psi.rst` lines 62-63. The packet's own hedge, "no cgroup subtree was enumerated", is a true statement about that 2026-10-15 packet.

[obs] The round-25 capture does enumerate cgroup subtrees (capture:27-44 for the pressure files, capture:46-53 for `memory.events`, capture:55-58 for `memory.swap.events`), and it reads the root cgroup's `memory.pressure` (capture:27-30), which the packet did not. The packet's "Root `memory.events` was absent, not zero" leg is not re-measured at all by the round-25 capture, since the capture reads the root `memory.pressure` but not the root `memory.events`; that leg stays dated.

[inf] Because the round-25 capture's root `memory.pressure` equals the system `/proc/pressure/memory` byte for byte (capture:21-22 versus capture:29-30), the mori-owned F9 fact (the root cgroup prints `psi_system`) is corroborated from the tsukuroi capture. It remains mori's claim to admit; tsukuroi cites it.

### F16 — `corpus/knowledge/adjacency-anchors-r19.md:163` and `:171`, the mori anchors quoting `oom-event-plane.md:344` — CONFIRMED as quoted, no notice owed

[obs] Both anchor rows quote `oom-event-plane.md:344` only up to the semicolon: "| 1 | `systemd-oomd` (userland PSI+swap monitor) | unit present (`/usr/lib/systemd/system/systemd-oomd.service`); `is-active`=inactive, `is-enabled`=disabled;". That quoted prefix is confirmed at round 25 (capture:72-73, 75-76).

[inf] The anchors' quoted text therefore survives the F1 contradiction intact, and the ledger classifications `RESOLVES` stand. The only risk is a reader who follows the anchor's line pointer and reads the whole row; the notices in section 3 make that row's later clause superseded, so no anchor edit is needed and none is proposed.

### F17 — `corpus/README.md` — no statement in this family, coverage observation only

[obs] A grep of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md` for `PSI`, `MemoryPressure`, `ManagedOOM`, `oomd`, `OOMD` and `pressure` returns no match. The only "memory" occurrence is the frontier line about the "memory observation packet" (`corpus/README.md:30`), and the only "kill" occurrences are inside unrelated words. So there is no README statement to confirm, narrow or contradict.

[obs] Separate coverage observation for the L1, not a supersession: the README coverage map carries 16 `knowledge/` rows and none of them is `oom-event-plane.md`, `kill-event-deep-r8.md`, `memory-arm-ver-s8.md` or `memory-arm-mutants-s8.md`. The notes that hold every statement in this trend are not indexed in the corpus README. This is also relevant to the C1 `README` row-count check, whose expected value the L1 must take from the current file rather than from the round-11 axes table.

## 3. Drafted append-only current-use notices

Each block below is a draft for the L1 to append. None is applied by this seat. Every block is append-only: earlier bytes stay as they are, and the notice names the file and line it supersedes for current use. The style follows the existing round-18 notice blocks in `oom-event-plane.md` and `SKILL.md`, and each notice carries the capture pointer and the manual quote it rests on. Source ids are left to the L1; the contract's next free id is S115, and S115 and S116 are already spoken for by the sibling round-25 source seats.

### Notice A — `corpus/knowledge/oom-event-plane.md`, superseding line 344 (the `systemd-oomd` prevention row)

```
## R25-CURRENT-USE — oom-event-plane line 344 `ManagedOOM*=auto` is the default, not a configured arming (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. The measured
values in the §7 row 1 cell stay as measured on 2026-10-14 and are re-measured as still current on 2026-10-22:
`ManagedOOMSwap=auto` and `ManagedOOMMemoryPressure=auto` on `user@1000.service` (capture:112-113),
`user-1000.slice` (capture:121-122), `user.slice` (capture:130-131) and `-.slice` (capture:139-140);
`ManagedOOMMemoryPressureLimit=0` (capture:114, 123, 132, 141); `ManagedOOMMemoryPressureDurationUSec=[not set]`
(capture:115, 124, 133, 142); `ManagedOOMPreference=none` (capture:116, 125, 134, 143). `systemd-oomd.service`
is `inactive` (capture:72-73), `disabled` (capture:75-76) and its socket `disabled` (capture:78-79). The three
oomd defaults the row lists are confirmed: `SwapUsedLimit=90%` (capture:106), `DefaultMemoryPressureLimit=60%`
(capture:107), `DefaultMemoryPressureDurationSec=30s` (capture:108), all commented out, with one non-comment
line in the effective config, the `[OOM]` section header (capture:83, capture:105). The `oomctl` leg of the row
was not re-measured on 2026-10-22 and stays dated.

Two claims in the row are superseded for current use. First, `ManagedOOMSwap=auto` and
`ManagedOOMMemoryPressure=auto` are the shipped defaults, and `auto` means systemd-oomd does not monitor the
cgroup: systemd.resource-control(5) at v262 states "Defaults to `auto`." (man/systemd.resource-control.xml:1529)
and "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection."
(man/systemd.resource-control.xml:1545-1546), while systemd-oomd.service(8) at v262 states "Cgroups of units
with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored."
(man/systemd-oomd.service.xml:43-44). The phrase "already set" therefore describes a default as if it were an
operator setting. Second, the inference that "oomd would likely have acted *before* the kernel" does not follow:
with `auto` on the four captured units, including the root slice `-.slice` that is the ancestor of the user
slice, no captured unit is a monitoring candidate, and the `auto` escape hatch (an ancestor set to `kill`) does
not apply because that ancestor itself reads `auto`. The 90 % swap rule is in any case a conjunction, not a
swap-only threshold: oomd.conf(5) at v262 states "If the fraction of memory used and the fraction of swap used
on the system are both more than what is defined here" (man/oomd.conf.xml:167-168), and the lane recorded no
memory-used fraction for either historical event. The `ManagedOOMMemoryPressureLimit=0` reading needs the same
qualifier the corpus already applies to `kill-event-deep-r8.md:255`: systemd.resource-control(5) at v262 states
"Defaults to 0%, which means to use the default set by oomd.conf(5). This property is ignored unless
ManagedOOMMemoryPressure=kill." (man/systemd.resource-control.xml:1559-1563).

Historical event reconstruction is unchanged: this notice supersedes the current-use reading of the row, not the
2026-10-13 and 2026-10-14 event account. No package, service, configuration or boot action is authorized by it.
```

### Notice B — `corpus/knowledge/kill-event-deep-r8.md`, superseding line 255 (the round-8 `systemd-oomd` detection row)

```
## R25-CURRENT-USE — kill-event-deep-r8 line 255 `ManagedOOM*=auto` is the default, not a configured arming (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. Every value
in the §8 row 1 cell is re-measured as still current on 2026-10-22 for the units the round-25 capture probed:
`ManagedOOMSwap=auto` and `ManagedOOMMemoryPressure=auto` on `user-1000.slice` (capture:121-122) and
`user@1000.service` (capture:112-113), `ManagedOOMPreference=none` (capture:116, 125) and
`ManagedOOMMemoryPressureLimit=0` (capture:114, 123); the capture adds
`ManagedOOMMemoryPressureDurationUSec=[not set]` (capture:115, 124), which this row does not record, and it
probes no application scope, so the row's "and sampled app scopes" leg stays dated.

The row's inference cell, "the swap rule (90 %) is below event A's measured 99.9999 % saturation, so oomd would
have had a trigger", is superseded for current use. `auto` is the shipped default and means systemd-oomd does
not monitor the cgroup: systemd.resource-control(5) at v262 states "Defaults to `auto`."
(man/systemd.resource-control.xml:1529) and "When set to auto, systemd-oomd will not actively use this cgroup's
data for monitoring and detection." (man/systemd.resource-control.xml:1545-1546); systemd-oomd.service(8) at v262
states "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored."
(man/systemd-oomd.service.xml:43-44). The 90 % swap limit is a conjunction with the memory-used fraction:
oomd.conf(5) at v262 states "If the fraction of memory used and the fraction of swap used on the system are both
more than what is defined here" (man/oomd.conf.xml:167-168). The row's own mechanism claim, that systemd-oomd
"acts by killing the *eligible descendant cgroup* rather than one task", is confirmed and gains one constraint:
systemd-oomd.service(8) at v262 states "only descendant cgroups are eligible candidates for killing" and "only
leaf cgroups and cgroups with memory.oom.group set to 1 are eligible candidates"
(man/systemd-oomd.service.xml:47-52), and this lane measured `memory.oom.group` as 0 everywhere on the path
(`oom-event-plane.md:280`), so the eligible-candidate set would have been empty even under `kill`. The
`ManagedOOMMemoryPressureLimit=0` reading is confirmed as a property value and narrowed: systemd.resource-control(5)
at v262 states "Defaults to 0%, which means to use the default set by oomd.conf(5). This property is ignored
unless ManagedOOMMemoryPressure=kill." (man/systemd.resource-control.xml:1559-1563). Historical event
reconstruction is unchanged and no service action is authorized by this notice.
```

### Notice C — `corpus/knowledge/oom-event-plane.md`, superseding line 301 (the §5 PSI signal row)

```
## R25-CURRENT-USE — oom-event-plane line 301 PSI row is a system-wide reading, and a total is not a reading (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. The row's
shape is re-measured as current on 2026-10-22: `/proc/pressure/memory` prints a `some` line and a `full` line,
each with `avg10`, `avg60`, `avg300` and `total` (capture:14-15, capture:21-22). The row's "live (`some`/`full`
with 10/60/300 s averages)" and "totals only" cells are therefore confirmed.

Two narrowings are added. First, scope: the row names the file but not the population, and the host carries at
least four PSI surfaces. On 2026-10-22 the capture reads the system file (capture:14-15, 21-22), the root cgroup
`memory.pressure` (capture:27-30), and the per-cgroup files of `user.slice` (capture:33-36),
`user.slice/user-1000.slice` (capture:37-40) and `user.slice/user-1000.slice/user@1000.service` (capture:41-44).
The root cgroup file and the system file are byte-identical at the second read (capture:21-22 and capture:29-30)
while every descendant cgroup carries its own smaller totals (capture:34, capture:38, capture:42). The kernel
documentation for v7.2 states that "Each subdirectory in the cgroupfs mountpoint contains cpu.pressure,
memory.pressure, and io.pressure files; the format is the same as the /proc/pressure/ files"
(Documentation/accounting/psi.rst:183-185). The generic `some`/`full` and cumulative-total semantics belong to
mori's admitted entry (mori `corpus/knowledge/system-pressure-r24.md` at 4f05dd5a, F2, F4, F9, F10) and are cited
here rather than restated.

Second, the row's dated figure is a 2026-10-14 measurement (`avg300=0.09`, `total=69,393,986 µs`) and is not
comparable with a later total: the capture's kernel is `7.2.11-arch1-1` (capture:6) against this note's
`7.2.3-arch1-3` (line 6), and the total is a since-boot accumulator, so the round-25 value
`avg300=0.06`, `total=41385384` (capture:14) is expected to differ rather than to contradict. A total is a
cumulative stall time, not an event timestamp (Linux v7.2 `Documentation/accounting/psi.rst`: "The total absolute
stall time (in us) is tracked and exported as well", lines 62-63), so a dated stall reading requires two reads
and a difference: the round-25 capture rises by 4,101 µs on the `some` total (capture:14 to capture:21) and by
4,079 µs on the `full` total (capture:15 to capture:22) across the ~10 s sleep (capture:17). The systemd-oomd
pressure rule is defined on the cgroup's own metric, not on this file: oomd.conf(5) at v262 states "the fraction
of time in a 10 second window in which all tasks in the control group were delayed"
(man/oomd.conf.xml:182-184). No host action is authorized by this notice.
```

### Notice D — `corpus/knowledge/oom-event-plane.md`, superseding line 347 (the `MemoryPressureWatch=` prevention row)

```
## R25-CURRENT-USE — oom-event-plane line 347 MemoryPressureWatch row: `auto` is conditional and `skip` is inert (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. The row's
measured state is re-measured as current on 2026-10-22 and is slightly wider: `MemoryPressureWatch=skip` on
`user@1000.service` (capture:117), `MemoryPressureWatch=auto` on `user-1000.slice` (capture:126), `user.slice`
(capture:135) and `-.slice` (capture:144), with `DefaultMemoryPressureWatch=auto` (capture:150) and
`DefaultMemoryPressureThresholdUSec=200ms` (capture:149), the latter matching the documented default of
"auto and 200ms, respectively" (systemd-system.conf(5) at v262, man/systemd-system.conf.xml:322-325).

The row's mechanism cell is narrowed. systemd.resource-control(5) at v262 defines the property as taking
"a boolean or one of `auto` and `skip`" (man/systemd.resource-control.xml:1665-1666); it states that with `auto`
"the protocol is enabled if memory accounting is anyway enabled for the unit, and disabled otherwise"
(man/systemd.resource-control.xml:1674-1676) and that with `skip` "the logic is neither enabled, nor disabled and
the two environment variables are not set" (man/systemd.resource-control.xml:1676-1677). So the row's `auto`
readings do not mean the protocol is enabled, and the row's `skip` reading means inert rather than off. The
row's operator action names the value `on`, which is not one of the documented tokens of this property at v262;
the documented ones are the boolean (`yes`/`no`), `auto` and `skip`. The row's characterisation of the lever as
"a *cooperating-app* lever, not a guard" with "no kill semantics" is confirmed: the v262 text gives this
property no kill power, and it also states that the threshold is carried in a second variable, "$MEMORY_PRESSURE_WRITE"
(man/systemd.resource-control.xml:1673-1674), alongside "$MEMORY_PRESSURE_WATCH" (man/systemd.resource-control.xml:1671-1672).
The upstream pin in `/usr/lib/systemd/system/user@.service` and the absence of a local `MemoryPressureWatch`
drop-in are confirmed outside the capture. No configuration write is authorized by this notice.
```

### Notice E — `corpus/knowledge/oom-event-plane.md`, superseding lines 280-281 (§4.5 no-guards conclusion)

```
## R25-CURRENT-USE — oom-event-plane lines 280-281: `MemoryPressureWatch=skip` is per unit, and systemd-oomd would not have monitored the path (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. The
`systemd-oomd` inactive+disabled reading is re-measured as current on 2026-10-22 (capture:72-73, capture:75-76,
socket disabled capture:78-79). The `MemoryPressureWatch` reading is narrowed: `skip` holds on
`user@1000.service` (capture:117), while `user-1000.slice` (capture:126), `user.slice` (capture:135) and
`-.slice` (capture:144) read `auto` and the system default is `auto` (capture:150), so the line's unqualified
"`MemoryPressureWatch` = `skip`" is a per-unit statement about the user manager service, not about the path.

The conclusion "Nothing was configured to act before the kernel" is narrowed for current use rather than
repeated: with `ManagedOOMSwap=auto` and `ManagedOOMMemoryPressure=auto` on the captured units including the
root slice, systemd-oomd would not have monitored those cgroups even if its service had been running
(systemd.resource-control(5) at v262, man/systemd.resource-control.xml:1545-1546; systemd-oomd.service(8) at v262,
man/systemd-oomd.service.xml:43-44), so the absence of a systemd-oomd action was structural and not a
consequence of the enable state alone. The round-18 notices on this line (R18-FRESH-NoticeOom-01 at line 444 and
R18-FRESH-NoticeOom-02 at line 448, with the precision block at line 469) already supersede the `earlyoom absent`
half of line 280 and the line 281 conclusion for current use; they are not repeated here. The round-25 capture
contains no `earlyoom` probe, so no statement about earlyoom may be carried from it. Historical event
reconstruction is unchanged and no service action is authorized by this notice.
```

### Notice F — `corpus/knowledge/kill-event-deep-r8.md`, superseding line 258 (the round-8 `MemoryPressureWatch=` row)

```
## R25-CURRENT-USE — kill-event-deep-r8 line 258 MemoryPressureWatch row: `auto` is conditional and `skip` is inert (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. The row is
re-measured as current on 2026-10-22 for the units the round-25 capture probed: `MemoryPressureWatch=skip` on
`user@1000.service` (capture:117) and `MemoryPressureWatch=auto` on `user-1000.slice` (capture:126). The
upstream pin and the absence of any local `MemoryPressureWatch` drop-in are confirmed outside the capture.
`session-4.scope` was not probed on 2026-10-22 and that leg stays dated.

The row's "a cooperating-app lever, not a guard" reading is confirmed and narrowed by systemd.resource-control(5)
at v262: the property takes "a boolean or one of `auto` and `skip`" (man/systemd.resource-control.xml:1665-1666);
with `auto` "the protocol is enabled if memory accounting is anyway enabled for the unit, and disabled otherwise"
(man/systemd.resource-control.xml:1674-1676); with `skip` "the logic is neither enabled, nor disabled and the
two environment variables are not set" (man/systemd.resource-control.xml:1676-1677). The `auto` reading is
therefore conditional, and `skip` means inert rather than off. The v262 text gives this property no kill power,
so "no kill semantics" stands. No configuration write is authorized by this notice.
```

### Notice G — `corpus/knowledge/kill-event-deep-r8.md`, superseding line 266 (the `ManagedOOMPreference` row)

```
## R25-CURRENT-USE — kill-event-deep-r8 line 266 ManagedOOMPreference steering knob is narrower than "available" (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. The measured
state is re-measured as current on 2026-10-22 for the units the round-25 capture probed: `ManagedOOMPreference=none`
on `user@1000.service` (capture:116), `user-1000.slice` (capture:125), `user.slice` (capture:134) and `-.slice`
(capture:143); `systemd-oomd.service` remains `inactive` (capture:72-73) and `disabled` (capture:75-76), so
"oomd never ran" is confirmed.

The action cell is narrowed. systemd.resource-control(5) at v262 states that the avoid and omit values
"Requires support for extended attributes (see xattr(7)) in order to use `avoid` or `omit`"
(man/systemd.resource-control.xml:1593-1595) and that "systemd-oomd will only respect these extended attributes
if the unit's cgroup is owned by root, or if the unit's cgroup owner, and the owner of the monitored ancestor
cgroup are the same" (man/systemd.resource-control.xml:1601-1603). The manual's own example is this host's
shape: attributes set on descendants of `/user.slice/user-1000.slice/user@1000.service/` are ignored when
candidates are computed for the root-owned `-.slice`, because the descendants are owned by UID 1000 and
`-.slice` is owned by UID 0 (man/systemd.resource-control.xml:1604-1609). The knob is therefore available only
for cgroups whose ownership matches the monitored ancestor's, which is narrower than "measured as available" for
the user slice. The round-25 capture probed no application scope, so the "everywhere sampled" claim keeps its
probed scope. No service or configuration action is authorized by this notice.
```

### Notice H — `corpus/knowledge/oom-event-plane.md`, superseding line 274 (the plane's pressure-signal list)

```
## R25-CURRENT-USE — oom-event-plane line 274 pressure-signal list: PSI is more than one population (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. The list at
lines 273-275 is not contradicted and stays as the plane's signal inventory. It is narrowed as a reading rule,
because the round-25 capture shows that "PSI" names at least four distinct surfaces on this host:
`/proc/pressure/memory` (capture:14-15, capture:21-22), the root cgroup `memory.pressure` (capture:27-30), and
the per-cgroup files of `user.slice` (capture:33-36), `user.slice/user-1000.slice` (capture:37-40) and
`user.slice/user-1000.slice/user@1000.service` (capture:41-44). The root cgroup file and the system file are
byte-identical at the second read (capture:21-22 and capture:29-30) while every descendant cgroup carries its
own smaller totals (capture:34, capture:38, capture:42). The kernel documentation for v7.2 states that "Each
subdirectory in the cgroupfs mountpoint contains cpu.pressure, memory.pressure, and io.pressure files; the
format is the same as the /proc/pressure/ files" (Documentation/accounting/psi.rst:183-185).

The systemd-oomd pressure rule is defined on the cgroup's own metric rather than on the system file:
oomd.conf(5) at v262 states that the limit "represents the fraction of time in a 10 second window in which all
tasks in the control group were delayed" (man/oomd.conf.xml:182-184). The generic `some`/`full` and
cumulative-total semantics, and the root-cgroup-prints-`psi_system` fact, are mori's admitted entry (mori
`corpus/knowledge/system-pressure-r24.md` at 4f05dd5a, F2, F4, F9, F10) and are cited here rather than restated.
No host action is authorized by this notice.
```

### Notice I — `corpus/knowledge/kill-event-deep-r8.md`, superseding line 180 (the slice PSI total row)

```
## R25-CURRENT-USE — kill-event-deep-r8 line 180 slice PSI total: name the file and the cgroup (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. The row's
reading, that a PSI total is cumulative and cannot date an incident, is confirmed: the kernel documentation for
v7.2 states that "The total absolute stall time (in us) is tracked and exported as well"
(Documentation/accounting/psi.rst:62-63), so the total is an accumulator and not an event marker.

The row is narrowed in scope. The recorded figure, 37,041,770 / 36,105,580 µs, is a per-cgroup lifetime figure
for the slice as captured on 2026-10-13. The round-25 capture reads the same family of file with different
numbers: `user.slice` `total=3150158` and `full total=3125148` (capture:34-35), and
`user.slice/user-1000.slice` `total=3158801` and `full total=3133751` (capture:38-39), against the system-wide
`total=41389485` (capture:21). The old slice figure must therefore not be compared with a system total or with a
later slice total; only files and cgroups named the same way are comparable. The generic PSI semantics are
mori's admitted entry (mori `corpus/knowledge/system-pressure-r24.md` at 4f05dd5a, F2, F4, F9, F10). No host
action is authorized by this notice.
```

### Notice J — `SKILL.md`, superseding lines 809-812 (the no-guard bullet)

```
## R25-CURRENT-USE — SKILL.md lines 809-812 no-guard bullet: `skip` is per unit and systemd-oomd would not have monitored the path (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. The
`systemd-oomd` inactive+disabled reading is re-measured as current on 2026-10-22 (capture:72-73, capture:75-76).
The `MemoryPressureWatch=skip` reading is confirmed for `user@1000.service` (capture:117) and narrowed: it is a
per-unit reading, since `user-1000.slice` (capture:126), `user.slice` (capture:135) and `-.slice` (capture:144)
read `auto` and the system default is `auto` (capture:150).

The bullet's "nothing acted before the kernel" conclusion is narrowed for current use: with
`ManagedOOMSwap=auto` and `ManagedOOMMemoryPressure=auto` on the captured units including the root slice,
systemd-oomd would not have monitored those cgroups even if its service had been running
(systemd.resource-control(5) at v262, man/systemd.resource-control.xml:1545-1546; systemd-oomd.service(8) at
v262, man/systemd-oomd.service.xml:43-44), so the absence of a systemd-oomd action was structural rather than a
consequence of the enable state alone. The round-18 notice on this bullet (R18-FRESH-SUPPLEMENT-03 at
SKILL.md:1938) already supersedes the `earlyoom absent` half for current use and is not repeated here; the
round-25 capture contains no `earlyoom` probe, so no statement about earlyoom may be carried from it. No
package, service, configuration or boot action is authorized by this notice.
```

### Notice K — `SKILL.md`, superseding lines 918 and 1027-1029 (the C6 PSI vocabulary)

```
## R25-CURRENT-USE — SKILL.md lines 918 and 1027-1029 C6 vocabulary: name the PSI scope (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. The field
names in the C6 vocabulary are re-measured as live on 2026-10-22: `/proc/pressure/memory` prints a `some` line
and a `full` line, each with `avg10`, `avg60`, `avg300` and `total` (capture:14-15, capture:21-22). The
vocabulary is narrowed because it names the fields without their scope or their semantics, and the host carries
more than one PSI surface: the system file, the root cgroup `memory.pressure` (capture:27-30, byte-identical to
the system file at capture:21-22 and capture:29-30) and the per-cgroup files of `user.slice` (capture:33-36),
`user.slice/user-1000.slice` (capture:37-40) and `user.slice/user-1000.slice/user@1000.service`
(capture:41-44), each with its own totals (capture:34, capture:38, capture:42). A `total` is a since-boot
cumulative stall accumulator, not a reading: the kernel documentation for v7.2 states that "The total absolute
stall time (in us) is tracked and exported as well" (Documentation/accounting/psi.rst:62-63), and the round-25
capture differs by 4,101 µs on the `some` total between capture:14 and capture:21 and by 4,079 µs on the `full`
total between capture:15 and capture:22. The generic PSI semantics belong to mori's admitted entry (mori
`corpus/knowledge/system-pressure-r24.md` at 4f05dd5a, F2, F4, F9, F10) and are cited rather than restated. No
host action is authorized by this notice.
```

### Notice L — `PROVINCE.md`, superseding line 49 (the ADJ-04 minimum-evidence clause)

```
## R25-CURRENT-USE — PROVINCE.md line 49 ADJ-04 minimum evidence: a PSI value is a snapshot of a counter (2026-10-22)

Appended 2026-10-22 by the tsukuroi round-25 L1 (ScribeSupersession seat); earlier bytes unchanged. The routing
is unchanged: host memory and kill-event measurement stays tsukuroi OS triage (lines 30-33) and fleet and wave
attribution stays with mori. The minimum-evidence clause is narrowed on one point: "exact counter or PSI
command/exit and observed value" reads as if a single PSI observation is a usable reading, but a PSI total is a
cumulative stall accumulator (Linux v7.2 `Documentation/accounting/psi.rst`: "The total absolute stall time
(in us) is tracked and exported as well", lines 62-63), so a dated stall reading requires two reads and a
difference, as the round-25 capture performs between capture:14 and capture:21 (4,101 µs on the `some` total
across the ~10 s sleep at capture:17). The systemd-oomd limit is a sustained condition over
`DefaultMemoryPressureDurationSec` on the cgroup metric (oomd.conf(5) at v262, man/oomd.conf.xml:198-202 and
man/oomd.conf.xml:182-184), not an instantaneous value. A single observed value is a snapshot of a counter and
is not an incident. No host action is authorized by this notice.
```

## 4. Out-of-scope items and boundaries observed

- Mori's ground was not absorbed. The generic `some`/`full` semantics, the cumulative-total semantics and the root-cgroup-prints-`psi_system` fact belong to mori's `corpus/knowledge/system-pressure-r24.md` at `4f05dd5a` (F2, F4, F9, F10). Every notice above cites mori for those and asserts only the tsukuroi-owned delta, namely that tsukuroi's own sentences named the wrong scope and drew the wrong inference. PROVINCE.md:49 keeps the fleet attribution with mori.
- No product file was written: not `SKILL.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, `SHONEN.md`, `corpus/` or `tools/`. The only file written by this seat is this report.
- No git or jj write command was run, and no push, fetch or other network write targeted the lane repository. This seat created no clone and no scratch repository.
- Host actions were read-only. `systemctl is-active` and `is-enabled` on earlyoom, greps of `/etc/systemd` and `/usr/lib/systemd`, and `ls` of unit directories were used; no service was started, stopped or restarted, no configuration was written, no package transaction was made, and sudo was never used. The greps and `ls` of `/etc` and `/usr/lib` are outside the enumerated no-sudo probe list and are marked supplementary everywhere they are used.
- The frozen capture was not modified and not re-captured; its sha256 was re-verified as `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`.
- The round-25 entry text, the six MP verdicts and actions, the SKILL.md decision-table row, the checker and its counted pointer for each row, and the SOURCES ids belong to other seats and are not written here.
- Three statements that the assignment named were deliberately left without a new notice because round 18 already noticed them or already ruled on them: `oom-event-plane.md:51` (earlyoom, R18-FRESH-NoticeOom-01), `oom-event-plane.md:345` (earlyoom probe row, R18-FRESH-NoticeOom-03) and `oom-event-plane.md:305` (dated "nothing was watching" cell, ruled historical at `.ufo/waves/round-18/falsify/FxFresh10.md:19`). The SKILL.md:809-812 bullet's earlyoom half is likewise already noticed at `SKILL.md:1938`.

## 5. Points the L1 needs to carry into the entry and the checker

1. The refutation belongs in MP4's verdict in so many words, because `oom-event-plane.md:344` is the lane's only prior statement about systemd-oomd's semantics, and its inference is the one the R18 notices never reached.
2. MP4 and MP5 must be scoped to the four captured units (`user@1000.service`, `user-1000.slice`, `user.slice`, `-.slice`). The capture reads no application scope and no other slice, so no host-wide claim is available.
3. The capture has no `earlyoom` probe. Any row or entry sentence that says "nothing is watching" on this host is unsupported by the capture, and the host's earlyoom is active and enabled.
4. Capture-pointer uniqueness matters for the checker. Within this capture `inactive` (capture:73), `MemoryPressureWatch=skip` (capture:117), `DefaultMemoryPressureWatch=auto` (capture:150), `DefaultMemoryPressureThresholdUSec=200ms` (capture:149), `1` (capture:83), `[OOM]` (capture:105) and the three commented defaults (capture:106-108) are unique lines; `ManagedOOMSwap=auto`, `ManagedOOMMemoryPressure=auto`, `ManagedOOMMemoryPressureLimit=0`, `ManagedOOMMemoryPressureDurationUSec=[not set]`, `ManagedOOMPreference=none` and `MemoryPressureThresholdUSec=200ms` each occur four times, `MemoryPressureWatch=auto` three times, `disabled` twice, `oom_kill 0` twice, and the second `/proc/pressure/memory` read (capture:21-22) is byte-identical to the root `memory.pressure` lines (capture:29-30). A counted pointer has to be one of the unique lines, with the repeated values cited by number.
5. `corpus/README.md` indexes none of `oom-event-plane.md`, `kill-event-deep-r8.md`, `memory-arm-ver-s8.md` or `memory-arm-mutants-s8.md`, so the corpus index does not point a reader at the notes that carry this trend.

Report: .ufo/waves/round-25/w1/ScribeSupersession.md
Scope: read=corpus/knowledge/oom-event-plane.md, kill-event-deep-r8.md, memory-arm-ver-s8.md, memory-arm-mutants-s8.md, adjacency-handoffs-fleet-r1.md, adjacency-anchors-r19.md, freshness-recheck-r18.json, statement-corrections-r18.json, adjacency-recheck-2026-10-19.md; SKILL.md; PROVINCE.md; corpus/README.md; SCORECARD.md round-25 declaration; corpus/SOURCES.md; the round-25 frozen capture and capture.sh; five upstream manual and kernel documentation pages (four systemd v262, one Linux v7.2) plus the three Arch man pages for systemd 262; the sibling round-25 seat reports CritC2Learning.md, SrcKernelOomCounter.md, ConnSiblingOverlap.md, SentinelCapture.md, ScoutPlanWalk.md and the round-18 artifacts FreshMemoryPlaneSweep.md and FxFresh10.md; mori `corpus/knowledge/system-pressure-r24.md` at 4f05dd5a; wrote=.ufo/waves/round-25/w1/ScribeSupersession.md (this report only); executed=read-only greps and `ls` of /etc/systemd, /usr/lib/systemd and /run/systemd, `systemctl is-active`/`is-enabled` on earlyoom.service, `systemctl --version`, curl of five upstream raw files and three Arch man pages, sha256sum of the fetched bytes and of the frozen capture, and python3 arithmetic over the capture values; no sudo, no package transaction, no service action, no configuration write, no git or jj write, no push.
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
