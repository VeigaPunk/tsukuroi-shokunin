# SrcOomdService — C2 source for MP4 (systemd-oomd.service(8), systemd 262)

Verdict: the Arch man page for systemd-oomd.service(8) at systemd 262.1 carries located quotes for all four MP4 source points — what systemd-oomd monitors (PSI and cgroups-v2), which units it acts on (only cgroups whose unit sets `ManagedOOMSwap=`/`ManagedOOMMemoryPressure=` to `kill`), its requirements (PSI in the kernel, swap enabled, a full unified cgroup hierarchy with memory accounting), and the fact that all of its monitoring and killing is performed by the running service itself, so with the unit inactive and disabled nothing is polled and nothing is killed; the frozen capture pins that host state at `capture.txt:73` (`inactive`, unique in the file).

## 1. The source opened and its version match

1. [obs] The page opened is `https://man.archlinux.org/man/systemd-oomd.service.8`. `curl -sS -L` returned HTTP 200 and 12541 bytes; the sha256 of the fetched raw bytes is `0878146ba32b46fefce0085a3e996372efc1b83043c613ff846fff5dacbf2cc4`. The page footer reads `systemd 262.1`, package `core/systemd`, version `262.1-1`.

2. [obs] Two sibling renderings of the same page were also fetched and hashed, because the line numbers quoted below are taken from the plain-text rendering: `https://man.archlinux.org/man/systemd-oomd.service.8.txt` returned HTTP 200, 5230 bytes, sha256 `c4e0d11f32f1669dea5a315b54c3cd694a93a010b9618c8f550dc2a8ce4dbb6e`; `https://man.archlinux.org/man/systemd-oomd.service.8.en` returned HTTP 200, 12547 bytes, sha256 `b5a3eb5a581949ccb8f18aff4f548f263024a75988a174f7c2bd6b9c327eae0c`. The `.en` hash equals the hash the reviewer seat `RevMp4Semantics` recorded for the same URL, so the two seats read byte-identical pages.

3. [obs] The upstream source of the same page at the tag matching the host was fetched as a version anchor: `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml` returned HTTP 200, 8348 bytes, sha256 `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d`. The upstream file contains the same sentences, except that `systemd(1)` is written as `<command>systemd</command>(1)` in the XML; every other quoted sentence below appears character-for-character in it.

4. [obs] The host runs `systemd 262 (262-1-arch)` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt:8-9`), and `pacman -Q systemd` prints `262-1`. The man page the host itself carries is `/usr/share/man/man8/systemd-oomd.service.8.gz`, sha256 `e53db8390f88bd800c5324da425a1952743553cc41ccf3c9f05b48ff3764486f`, owned by systemd 262-1 (`pacman -Qo`), with the roff header `.TH "SYSTEMD\-OOMD\&.SERVICE" "8" "" "systemd 262"`. [obs] De-rendering that local file and diffing it word by word against the Arch plain-text rendering yields no difference in any sentence: the only differences are the rendering artifacts of the two formats (section-heading lines, the `you\*(Aqre` roff escape for "you're", the `\%` URL escape and the `systemd 262.1` versus `systemd 262` footer). The quotes below therefore hold for the host's installed 262 manual as well as for the online 262.1 page.

## 2. Located quotes, each of at most 25 words, copied exactly from the opened page

Line numbers refer to the plain-text rendering `systemd-oomd.service.8.txt` (sha256 `c4e0d11f…`), whose headings are `NAME` (line 3), `SYNOPSIS` (7), `DESCRIPTION` (12), `SYSTEM REQUIREMENTS AND CONFIGURATION` (43), `USAGE RECOMMENDATIONS` (73), `OPTIONS` (86), `SIGNALS` (100), `SEE ALSO` (107), `NOTES` (111). Every quote below was checked to be present in three independent renderings of the same document — the `.txt` rendering, the `.en` HTML rendering, and the host's installed `.gz` — and is reproduced here exactly.

### What systemd-oomd monitors

- **Q-MON-1** — § DESCRIPTION, lines 13-15, 19 words:
  > "systemd-oomd is a system service that uses cgroups-v2 and pressure stall information (PSI) to monitor and take corrective action before an OOM occurs"

  (the sentence continues on line 15 with "in the kernel space."; the 19-word form above is the truncated variant, the 21-word form "uses cgroups-v2 and pressure stall information (PSI) to monitor and take corrective action before an OOM occurs in the kernel space." is the complete final clause and is also exact. Both are within the 25-word budget.)

- **Q-MON-2** — § DESCRIPTION, lines 24-26, 17 words:
  > "systemd-oomd periodically polls PSI statistics for the system and those cgroups to decide when to take action."

### Which units it acts on

- **Q-UNIT-1** — § DESCRIPTION, lines 23-24, 13 words:
  > "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored."

- **Q-UNIT-2** — § DESCRIPTION, lines 26-27, 21 words:
  > "If the configured limits are exceeded, systemd-oomd will select a cgroup to terminate, and send SIGKILL to all processes in it."

- **Q-UNIT-3** — § DESCRIPTION, lines 30-32, 14 words:
  > "Also only leaf cgroups and cgroups with memory.oom.group set to 1 are eligible candidates"

  (the entry continues on line 32 with "; see OOMPolicy= in systemd.service(5)."; the preceding clause on lines 28-30 reads "Note that only descendant cgroups are eligible candidates for killing; the unit with its property set to kill is not a candidate (unless one of its ancestors set their property to kill).", which is 34 words and therefore exceeds the 25-word budget — it is recorded here as a located fact, not as a quote.)

- **Q-UNIT-4** — § DESCRIPTION, lines 19-21, 16 words:
  > "systemd-oomd retrieves information about such units from systemd(1) when it starts and watches for subsequent changes."

- **Q-UNIT-5** — § DESCRIPTION, lines 34-35, 11 words:
  > "oomctl(1) can be used to list monitored cgroups and pressure information."

### Its requirements

- **Q-REQ-1** — § SYSTEM REQUIREMENTS AND CONFIGURATION, lines 44-45, 17 words:
  > "The system must be running systemd with a full unified cgroup hierarchy for the expected cgroups-v2 features."

- **Q-REQ-2** — § SYSTEM REQUIREMENTS AND CONFIGURATION, lines 45-46, 13 words:
  > "Furthermore, memory accounting must be turned on for all units monitored by systemd-oomd."

- **Q-REQ-3** — § SYSTEM REQUIREMENTS AND CONFIGURATION, lines 50-51, 16 words:
  > "The kernel must be compiled with PSI support. This is available in Linux 4.20 and above."

- **Q-REQ-4** — § SYSTEM REQUIREMENTS AND CONFIGURATION, lines 53-54, 16 words:
  > "It is highly recommended for the system to have swap enabled for systemd-oomd to function optimally."

- **Q-REQ-5** — § SYSTEM REQUIREMENTS AND CONFIGURATION, line 59, 10 words:
  > "Any swap-based actions on systems without swap will be ignored."

- **Q-REQ-6** — § SYSTEM REQUIREMENTS AND CONFIGURATION, lines 74-76, 7 words:
  > "ManagedOOMSwap= works with the system-wide swap values"

  (the sentence continues on lines 74-76: "…so setting it on the root slice -.slice, and allowing all descendant cgroups to be eligible candidates may make the most sense.", which is 29 words as a whole and therefore exceeds the budget.)

### What happens when it is not running

- **Q-RUN-1** — § DESCRIPTION, lines 17-21, 21 words:
  > "You can enable monitoring and actions on units by setting ManagedOOMSwap= and ManagedOOMMemoryPressure= in the unit configuration"

  (the sentence continues "see systemd.resource-control(5). systemd-oomd retrieves information about such units from systemd(1) when it starts and watches for subsequent changes.")

- **Q-RUN-2** — § OPTIONS, lines 87-90, 21 words:
  > "Do a dry run of systemd-oomd: when a kill is triggered, print it to the log instead of killing the cgroup."

- **Q-RUN-3** — § OPTIONS, lines 89-90, 9 words:
  > "The short option -n was added in version 262."

  [obs] The host runs systemd 262, so the dry-run option that the page documents as new in this very version is available to the operator here.

## 3. Mapping to the capture lines for `systemctl is-active systemd-oomd.service`

The frozen capture is `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt`, sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`, re-verified locally with `sha256sum`; it is 155 lines and its timestamp is 2026-10-22T10:06:23Z (lines 2-3).

1. [obs] The capture's `### oomd-unit` block is lines 71-80:
   - line 71: `### oomd-unit` (section header)
   - line 72: `$ systemctl is-active systemd-oomd.service` (command echo)
   - line 73: `inactive` (the result)
   - line 74: `[exit 3]` (exit line; `is-active` exits 3 for an inactive unit)
   - line 75: `$ systemctl is-enabled systemd-oomd.service`
   - line 76: `disabled`
   - line 77: `[exit 1]`
   - line 78: `$ systemctl is-enabled systemd-oomd.socket`
   - line 79: `disabled`
   - line 80: `[exit 1]`

2. [obs] The C2 rule requires a pointer to a capture line whose text is unique in the capture and which is not a section header, command echo or exit line. Line 73 (`inactive`) satisfies it: `grep -cx 'inactive' capture.txt` returns 1. Line 76 (`disabled`) does not, because `grep -cx 'disabled' capture.txt` returns 2 — the same word appears at line 79 for the socket. So the row's capture pointer must be `capture.txt:73`, and line 73 must not be quoted together with the word "disabled" as if it were unique.

3. [inf] MP4 as a sourced row is therefore: on this host systemd-oomd is not running and is disabled, so by Q-MON-1 and Q-MON-2 the PSI polling and the corrective SIGKILL described in the page do not happen at all; the only OOM actor on this host is the kernel's own OOM killer. By Q-UNIT-1, even a running systemd-oomd would monitor no cgroup on this host, because every unit the capture sampled carries `ManagedOOMSwap=auto` and `ManagedOOMMemoryPressure=auto` (`capture.txt:112-113`, `121-122`, `130-131`, `139-140`) and the page's rule for which cgroups are monitored is `kill`. The word "auto" itself is defined on the systemd.resource-control(5) page, not on this page; that page belongs to the `SrcResourceControl` seat (see section 6).

4. [obs] The requirement statements also hold or fail on this host, each read read-only outside the capture:
   - Q-REQ-1, unified cgroup hierarchy: `stat -fc %T /sys/fs/cgroup` prints `cgroup2fs`, and `/sys/fs/cgroup/cgroup.controllers` lists `memory`. The requirement is met.
   - Q-REQ-3, PSI in the kernel: `/proc/pressure/cpu`, `/proc/pressure/io` and `/proc/pressure/memory` all exist on this host. The requirement is met.
   - Q-REQ-4 and Q-REQ-5, swap: the capture itself reads `SwapTotal: 31722876 kB` at `capture.txt:68`. Swap is present and large, so swap-based actions would not be ignored for want of swap.
   - Q-REQ-2, memory accounting: `systemd-analyze cat-config systemd/systemd-system.conf` prints "Main configuration file systemd/systemd-system.conf not found", so no local file sets `DefaultMemoryAccounting=`; whether the shipped default is `true` is not established by this page or by any source this seat opened. [unk]

## 4. A host fact that must not be misread: `ConditionResult=no` on systemd-oomd.service

1. [obs] `systemctl show -p ConditionResult -p Result -p UnitFileState -p ActiveState -p SubState -- systemd-oomd.service` prints `ConditionResult=no`, `Result=success`, `UnitFileState=disabled`, `ActiveState=inactive`, `SubState=dead`. The socket prints `ConditionResult=no`, `UnitFileState=disabled`, `ActiveState=inactive`.

2. [obs] That `no` does not mean a condition failed on this host. In the upstream v262 source, `condition_result` is a plain `bool` field of `Unit` (`src/core/unit.h:434`), the `Unit` struct is allocated with `u = malloc0(size);` (`src/core/unit.c:103`), so the field starts false, and the only two writes to it are inside `unit_test_condition()` (`src/core/unit.c:1815` and `1817`). The only call site of `unit_test_condition()` in that file is inside the unit start path (`src/core/unit.c:1977-1978`, inside `if (state != UNIT_ACTIVATING && !unit_test_condition(u))`). The D-Bus property exposes the stored field read-only (`src/core/dbus-unit.c:1001`, `SD_BUS_PROPERTY("ConditionResult", "b", bus_property_get_bool, offsetof(Unit, condition_result), …)`). [obs] Fetched hashes: `src/core/unit.c` sha256 `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7`, `src/core/unit.h` sha256 `563a8180f79038ddc28d267cd971c902bd6c1df438ac92cee6e0a6612b8e1eca`, `src/core/dbus-unit.c` sha256 `47f461aeb70722ae7fb02f9b89ffd12db1639b7750a02e218dc27747f4cd9d0d`.

3. [obs] The host corroborates that reading. `systemd-hostnamed.service` was started and stopped during this boot (`journalctl --no-pager -b -u systemd-hostnamed.service` shows "Starting Hostname Service…" and "Deactivated successfully." at 06:01:45 and 06:02:15) and it reports `ConditionResult=yes`. `systemd-backlight.service` and `systemd-networkd-wait-online.service` were never started in this boot (`journalctl --no-pager -b -u …` prints "-- No entries --" for both) and both report `ConditionResult=no`. systemd-oomd.service has never started in this boot either: `journalctl --no-pager -b -u systemd-oomd.service` and the same query for `systemd-oomd.socket` both print "-- No entries --", and `journalctl --no-pager -u systemd-oomd.service --since "-30 days"` contains no entry.

4. [inf] The correct reading is therefore: `ConditionResult=no` on systemd-oomd.service reflects that the unit was never started, so its conditions were never evaluated, not that the host fails them. The conditions themselves are satisfiable here — the installed unit file `/usr/lib/systemd/system/systemd-oomd.service` carries `ConditionControlGroupController=memory`, `ConditionPathExists=/proc/pressure/cpu`, `ConditionPathExists=/proc/pressure/io` and `ConditionPathExists=/proc/pressure/memory` (lines 18-21), and all four hold on this host: the `memory` controller is in `cgroup.controllers` and the three PSI files exist. The upstream v262 unit file `https://raw.githubusercontent.com/systemd/systemd/v262/units/systemd-oomd.service.in` (HTTP 200, 1783 bytes, sha256 `2f4c2862b5826e85d63d5c7993f8610556f2f201facc0b20af04c1b972f288d3`) carries the same conditions; diffing it against the installed file after substituting the build-time placeholders shows they are identical apart from `ExecStart=/usr/lib/systemd/systemd-oomd` and the rendered `WatchdogSec=3min`. [unk] Whether the kernel OOM killer or a userspace guard would actually have fired in either of the two historical OOM events is outside this seat's scope and was not measured here.

## 5. Draft SOURCES row (one row; the L1 assigns the final id)

Column order per `corpus/SOURCES.md:5`: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.

```
| S117 | systemd-oomd.service(8) — https://man.archlinux.org/man/systemd-oomd.service.8 | docs | A | What systemd-oomd monitors, which units it acts on, its documented requirements (PSI in the kernel, swap, unified cgroup hierarchy, memory accounting) and the fact that the running service itself performs all monitoring and killing; the systemd 262 service manual, not host state and not a claim that the service runs on this host | § DESCRIPTION lines 13-15 "systemd-oomd is a system service that uses cgroups-v2 and pressure stall information (PSI) to monitor and take corrective action before an OOM occurs"; § DESCRIPTION lines 23-24 "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored."; § DESCRIPTION lines 26-27 "If the configured limits are exceeded, systemd-oomd will select a cgroup to terminate, and send SIGKILL to all processes in it."; § SYSTEM REQUIREMENTS AND CONFIGURATION lines 44-45 "The system must be running systemd with a full unified cgroup hierarchy for the expected cgroups-v2 features."; lines 45-46 "Furthermore, memory accounting must be turned on for all units monitored by systemd-oomd."; lines 50-51 "The kernel must be compiled with PSI support. This is available in Linux 4.20 and above."; lines 53-54 "It is highly recommended for the system to have swap enabled for systemd-oomd to function optimally."; line 59 "Any swap-based actions on systems without swap will be ignored."; § OPTIONS lines 87-90 "Do a dry run of systemd-oomd: when a kill is triggered, print it to the log instead of killing the cgroup." and lines 89-90 "The short option -n was added in version 262."; plain-text rendering https://man.archlinux.org/man/systemd-oomd.service.8.txt sha256 c4e0d11f32f1669dea5a315b54c3cd694a93a010b9618c8f550dc2a8ce4dbb6e, HTML sha256 0878146ba32b46fefce0085a3e996372efc1b83043c613ff846fff5dacbf2cc4, page footer systemd 262.1 / core/systemd 262.1-1, opened 2026-10-22 | The page states that systemd-oomd uses cgroups-v2 and PSI to monitor and to take corrective action before a kernel OOM, polling PSI periodically and sending SIGKILL to a selected cgroup when configured limits are exceeded; it monitors only cgroups of units whose ManagedOOMSwap= or ManagedOOMMemoryPressure= is set to kill, with only leaf cgroups or cgroups with memory.oom.group set to 1 eligible; it requires a full unified cgroup hierarchy, memory accounting on the monitored units, a kernel with PSI support and, for swap-based actions, swap present; and because the running service itself performs the polling and the killing, an inactive and disabled systemd-oomd polls nothing and kills nothing | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md |
```

Notes for the L1 on this row.

- The id is a proposal. `corpus/SOURCES.md` carries S001 through S114 with no gaps, so S115 is the next free id in the registry as it stands (confirmed independently by the `RevCensusBefore` seat). Two other round-25 source seats have already claimed S115 in their own drafts — `SrcCgroupV2` for the Linux v7.2 cgroup-v2 page and `SrcKernelOomCounter` for `mm/oom_kill.c` — and `SrcOomdConf` has claimed S116 for oomd.conf(5). To keep the four rows distinguishable in the drafts I have numbered mine S117. The L1 must renumber all of them at integration.
- `kind` is `docs` and `tier` is `A`, matching the existing man-page rows in the registry (for example the `systemd.exec(5)` rows). `status` is `mined`, the registry's vocabulary for a row whose page has been opened and read. `recheck` is `on-release` because the row is pinned to the systemd 262 series; the upstream tag `v262` was opened as a version anchor and carries the same sentences.
- `used-by` names the entry `corpus/knowledge/memory-pressure-r25.md`, the round-25 C2 entry that carries the MP4 row. The entry's `.json` sibling is not listed separately in the registry's `used-by` convention; the existing rows name the `.md` path only.
- The row's `anchor` quotes each have at most 25 words. Two sentences of the page are longer than that budget and are therefore recorded in section 2 as located facts rather than as quotes: the "only descendant cgroups are eligible candidates for killing" clause (34 words) and the "ManagedOOMSwap= works with the system-wide swap values, so setting it on the root slice -.slice…" sentence (29 words). The entry may use either of them if it prefers a different truncation, but it must not present them as sub-25-word quotes.

## 6. Supporting sources opened in this session, not drafted as rows by this seat

These were fetched and read, so the L1 may attribute them to the seats that own them; this seat drafted only the one row in section 5.

| source | URL | sha256 | key located content |
|---|---|---|---|
| systemd.resource-control(5) plain-text rendering | https://man.archlinux.org/man/systemd.resource-control.5.txt | `7d16b3d5c5ca786e8756679792ae95d64ad1348245ae07687894ef77f8b14422` | § Memory Pressure Control, lines 1303-1324: `ManagedOOMSwap=auto\|kill, ManagedOOMMemoryPressure=auto\|kill`; "Specifies how systemd-oomd.service(8) will act on this unit's cgroups. Defaults to auto."; "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection." (16 words); "Setting either of these properties to kill will also result in After= and Wants= dependencies on systemd-oomd.service unless DefaultDependencies=no." (19 words). This is the page that defines `auto` and `kill` for MP4 and that shows a `kill` unit would pull systemd-oomd in, so it belongs to the `SrcResourceControl` seat's row, not to this one. |
| upstream v262 unit file | https://raw.githubusercontent.com/systemd/systemd/v262/units/systemd-oomd.service.in | `2f4c2862b5826e85d63d5c7993f8610556f2f201facc0b20af04c1b972f288d3` | Conditions `ConditionControlGroupController=memory`, `ConditionPathExists=/proc/pressure/{cpu,io,memory}`, `Requires=systemd-oomd.socket`, `After=swap.target`, `User=systemd-oom`, `OOMScoreAdjust=-900`. |
| upstream v262 `src/core/unit.c` | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c | `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7` | Lines 103, 1804-1825, 1977-1978: the `condition_result` lifecycle used in section 4. |
| upstream v262 `src/core/unit.h` | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.h | `563a8180f79038ddc28d267cd971c902bd6c1df438ac92cee6e0a6612b8e1eca` | Line 434: `bool condition_result;` |
| upstream v262 `src/core/dbus-unit.c` | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/dbus-unit.c | `47f461aeb70722ae7fb02f9b89ffd12db1639b7750a02e218dc27747f4cd9d0d` | Line 1001: the read-only `ConditionResult` D-Bus property. |
| upstream v262 `man/systemd-oomd.service.xml` | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml | `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d` | Same sentences as the man page; the version anchor for the page. |

## 7. Limits and out-of-scope items

- [unk] The `auto` and `kill` value semantics that MP4 turns on are defined on systemd.resource-control(5), not on systemd-oomd.service(8). This seat did not draft a row for that page, because the `SrcResourceControl` seat exists for it; the located quotes are supplied in section 6 so the L1 can attach them to whichever row owns the page.
- [unk] The page does not state a sentence of the form "when the service is not running, X happens". The not-running reading in section 3 is an inference from Q-MON-1, Q-MON-2 and Q-UNIT-1 together with the capture, and it is marked as such.
- [unk] Whether the shipped default of `DefaultMemoryAccounting=` is `true` was not established by any source this seat opened, so the memory-accounting half of Q-REQ-2 is not closed here.
- [unk] No live systemd-oomd was observed. Starting or stopping a service is forbidden on this host, so the dry-run path described by Q-RUN-2 was read but not exercised. The host corroboration available instead is that `oomctl` cannot reach the daemon: running `oomctl` prints "Failed to dump context: Could not activate remote peer 'org.freedesktop.oom1': activation request failed: unknown unit" and exits 1, because the D-Bus activation file `/usr/share/dbus-1/system-services/org.freedesktop.oom1.service` points at `SystemdService=dbus-org.freedesktop.oom1.service`, and `systemctl is-enabled dbus-org.freedesktop.oom1.service` returns "not-found" (exit 4) while `/run/systemd/oom` does not exist.
- [obs] The weaker prior statements that MP4 sharpens live in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md`: line 344 calls systemd-oomd the "userland PSI+swap monitor" and records that it is inactive and disabled, but does not tie the inactive state to the page's own rule that only `kill` cgroups are monitored, nor to the requirement statements; line 347 treats `MemoryPressureWatch=` as a cooperating-app lever. This seat did not edit that note.
- [obs] No file under `SKILL.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, `SHONEN.md`, `corpus/` or `tools/` was read for modification or written. Only this report and scratch copies of the fetched pages were produced, under `/fast/scratch/hyaku/tsukuroi-r25/SrcOomdService/`. No git or jj write command was run, no service was started, stopped or restarted, no configuration was written, and no package transaction was attempted.

Scope: read=https://man.archlinux.org/man/systemd-oomd.service.8 (plus its .txt and .en renderings), https://man.archlinux.org/man/systemd.resource-control.5.txt, https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml, https://raw.githubusercontent.com/systemd/systemd/v262/units/systemd-oomd.service.in, https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c, https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.h, https://raw.githubusercontent.com/systemd/systemd/v262/src/core/dbus-unit.c, /usr/share/man/man8/systemd-oomd.service.8.gz, /usr/lib/systemd/system/systemd-oomd.service, /usr/lib/systemd/system/systemd-oomd.socket, /usr/share/dbus-1/system-services/org.freedesktop.oom1.service, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md (round 25 declaration), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md (registry and column format), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md (lines 270-352); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/SrcOomdService.md; executed=curl of the eight URLs above (all HTTP 200; the .en fetch needed one retry after a TLS EOF), sha256sum over every fetched file and over the frozen capture, grep/awk/diff over the fetched renderings and over the capture, systemctl show/status/is-active/is-enabled (read-only), systemd-analyze cat-config (read-only), journalctl (user-readable), pacman -Q and -Qo (read-only), stat and ls on /proc/pressure, /sys/fs/cgroup and /usr/lib/systemd/system, and one `oomctl` query that failed to reach the daemon and changed no host state
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
