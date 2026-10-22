# SrcKernelOomCounter — MP6 code source for the round-25 memory-pressure entry

Verdict: the kernel v7.2 source opened in this session proves that an OOM kill is counted by two
independent counters (`count_vm_event(OOM_KILL)` for `/proc/vmstat` and
`memcg_memory_event_mm(mm, MEMCG_OOM_KILL)` for `memory.events`), both incremented in
`mm/oom_kill.c` at the moment of the kill, in a source file disjoint from the PSI stall accounting
in `kernel/sched/psi.c`; the draft SOURCES row below is grounded in that source and is offered to
the L1 for the MP6 row of `corpus/knowledge/memory-pressure-r25.md`.

Scope of this seat: code source for MP6 only. No product file, judge, corpus note, tool or
configuration was written, and no host state was changed. The row and the file are drafts for the
L1 integrator.

## 1. Delivered SOURCES row draft (one row, id S115)

Column order is the frozen contract order: `id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S115 | Linux kernel v7.2 `mm/oom_kill.c` — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | code | A | Where the kernel increments its OOM-kill counters, i.e. the accounting behind `/proc/vmstat` `oom_kill` and the per-cgroup `memory.events` `oom_kill` line | `mm/oom_kill.c:934-936`, function `__oom_kill_process`; tag `v7.2`, raw bytes fetched 2026-10-22, sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` (1257 lines) | The OOM kill path raises its event counters at the moment of the kill, before `SIGKILL` is sent: `count_vm_event(OOM_KILL);` and `memcg_memory_event_mm(mm, MEMCG_OOM_KILL);` (quoted verbatim from `mm/oom_kill.c:935-936`, comment on line 934 reads "Raise event before sending signal: task reaper must see this"), so an OOM kill is counted by its own counters and is not derived from pressure stall accounting | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md (MP6) |

Quote budget check: the located quote above is `count_vm_event(OOM_KILL);` plus
`memcg_memory_event_mm(mm, MEMCG_OOM_KILL);` — eight whitespace-separated tokens, at most 25 words,
copied character for character from the fetched bytes of `mm/oom_kill.c` lines 935 and 936
(leading tab indentation preserved in the file, omitted inside the table cell).

S115 is the next free id: the lane registry `corpus/SOURCES.md` carries rows S001 through S114
(read 2026-10-22; no row in that file mentions `torvalds/linux`, `vmstat` or `oom_kill`, so this
source is new to the registry). The id is a draft for the L1 to renumber: at draft time the
parallel round-25 source seat for the oomd.conf(5) row (MP5) was told S116 for the same reason,
so the two round-25 source rows do not collide at integration.

## 2. Findings, with evidence

1. [obs] The OOM kill counters are raised in one place, inside `__oom_kill_process()`, in
   `mm/oom_kill.c` of the `v7.2` tag. Fetched raw bytes:
   `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c`, HTTP 200, sha256
   `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`, 1257 lines.
   `mm/oom_kill.c:934-936` read as:
   ```
   	/* Raise event before sending signal: task reaper must see this */
   	count_vm_event(OOM_KILL);
   	memcg_memory_event_mm(mm, MEMCG_OOM_KILL);
   ```
   The counters are raised before `do_send_sig_info(SIGKILL, ...)` at `mm/oom_kill.c:942`, so the
   counter is not conditional on the victim dying or on any later accounting.

2. [obs] The vmstat counter the capture reads is the same `OOM_KILL` event, and its printed name
   is `oom_kill`. `mm/vmstat.c:1355` (fetched HTTP 200, sha256
   `42f358d199a615e62d8c66bda9321d629311303d7082bd6dd7ed0b1ca4263329`) reads
   `[I(OOM_KILL)]				= "oom_kill",`; the enum member `OOM_KILL` is defined at
   `include/linux/vm_event_item.h:51` (HTTP 200, sha256
   `0b5e7bf8e70e387cc1261fcf00118806b2c8b2fff4391a6719360db3a3bab40f`). The `/proc/vmstat` name
   is produced from that table through `vm_event_name()` at `include/linux/vmstat.h:507-513`
   (HTTP 200, sha256 `a71d9cbd4b2257167f30d7d1adff7fca15d9e3cce74bd00398f6e33ac6c4aa78`; the first
   attempt to fetch this file returned HTTP 429 and was retried successfully).

3. [obs] The per-cgroup `oom_kill` line in `memory.events` is the memcg event incremented at the
   same place. `mm/memcontrol.c:4881-4882` (fetched HTTP 200, sha256
   `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e`) reads
   ```
   	seq_printf(m, "oom_kill %lu\n",
   		   atomic_long_read(&events[MEMCG_OOM_KILL]));
   ```
   inside `__memory_events_show()`, which is the emitter behind
   `/sys/fs/cgroup/<path>/memory.events`. The enum member `MEMCG_OOM_KILL` is at
   `include/linux/memcontrol.h:51` (HTTP 200, sha256
   `b067e1db2e0a2eb46faeb5bc7041efa4641bf4cea9aff3602d56e3023f7e4cf0`), and
   `memcg_memory_event_mm()` at `include/linux/memcontrol.h:1005-1018` charges the event to the
   memory cgroup that owns the victim's `mm`. The neighbouring line at `mm/memcontrol.c:4880` is
   the distinct `oom` event (`MEMCG_OOM`), so `oom` and `oom_kill` are separate counters and must
   not be read as one another.

4. [obs] The pressure-stall accounting is a different subsystem in a different file, so the
   counters are independent of it. Memory stall time is accounted by `psi_memstall_enter()` and
   `psi_memstall_leave()` in `kernel/sched/psi.c:1056` and `kernel/sched/psi.c:1087` (fetched HTTP
   200, sha256 `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5`), and the
   `/proc/pressure/memory` file is created in the same file at `kernel/sched/psi.c:1715`. The OOM
   kill counters are incremented in `mm/oom_kill.c` and never in `kernel/sched/psi.c`; the string
   `oom_kill` does not occur in the fetched `psi.c` bytes. A kill therefore raises its own
   counters whether or not any stall time was accumulated, and a stall with no kill leaves the
   kill counters unchanged. [inf] This is the code-level reason MP6 can assert that OOM-kill
   evidence and pressure-stall evidence are two separate readings; it is not a claim that the two
   phenomena are unrelated in practice (a kill usually follows stalls).

5. [obs] Host-side readings this source maps to, all from the frozen capture
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt`
   (sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` as stated in the
   dispatch):
   - `capture.txt:61-62` — `$ grep -E ^oom_kill /proc/vmstat` → `oom_kill 0`. This is the
     system-wide vmstat counter of finding 1 and 2.
   - `capture.txt:46-51` — `$ cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.events` →
     `oom 0`, `oom_kill 0`, `oom_group_kill 0`. The `oom_kill 0` at `capture.txt:51` is the memcg
     event of finding 3 for the `user-1000.slice` cgroup.
   - `capture.txt:12-19` and `capture.txt:27-30` — the PSI memory readings
     (`/proc/pressure/memory`, root cgroup `memory.pressure`) whose `total` fields are stall
     accumulations, i.e. the accounting of finding 4, distinct from both kill counters.
   - `capture.txt:71-79` — `systemd-oomd.service` `inactive` and `disabled`; the userland monitor
     that reads PSI never ran on this host, so the PSI side of the capture has no oomd-driven kill
     to attribute.
   [obs] Both kill counters read `0` at capture time, and the memcg `memory.events` block also
   shows `sock_throttled 13763` — non-zero swap-throttling activity with zero OOM kills in that
   cgroup.
   [inf] `/proc/vmstat` counters are reset at boot, so `oom_kill 0` at `capture.txt:62` indicates no
   kernel OOM kill since boot; the per-cgroup `memory.events` counters belong to the cgroup's own
   lifetime and reset when the cgroup is removed. The entry should source these two lifetime
   statements separately if it wants to assert them; this seat did not open a source for them.

6. [obs] The weaker prior statements that MP6 sharpens live in
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md`:
   line 274 lists the plane's signals as `memory.swap.peak`, `memory.swap.events.fail`,
   `pswpin/pswpout`, PSI and the kernel/systemd records; line 301 lists PSI as a live signal with
   `totals only`; line 344 treats `systemd-oomd` as the userland PSI+swap monitor and notes it is
   inactive and disabled; line 347 treats `MemoryPressureWatch=` as a cooperating-app lever with
   "no kill semantics". None of those lines anchors the OOM-kill counters in kernel code, so the
   entry cannot say from them that an OOM kill is counted independently of stall accounting. The
   S115 row supplies exactly that missing code anchor. (No edit to that note was made by this
   seat.)

## 3. Supporting sources opened in this session (no registry row drafted by this seat)

These were fetched and read, so they are available to the L1 if it wants to add further rows; this
seat drafted only S115 as assigned.

| file | URL | sha256 | key located line |
|---|---|---|---|
| `mm/memcontrol.c` | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c | `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e` | 4881-4882 (`oom_kill` in `memory.events`) |
| `mm/vmstat.c` | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/vmstat.c | `42f358d199a615e62d8c66bda9321d629311303d7082bd6dd7ed0b1ca4263329` | 1355 (`[I(OOM_KILL)] = "oom_kill"`) |
| `include/linux/vm_event_item.h` | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/vm_event_item.h | `0b5e7bf8e70e387cc1261fcf00118806b2c8b2fff4391a6719360db3a3bab40f` | 51 (`OOM_KILL`) |
| `include/linux/vmstat.h` | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/vmstat.h | `a71d9cbd4b2257167f30d7d1adff7fca15d9e3cce74bd00398f6e33ac6c4aa78` | 507-513 (`vm_event_name()`) |
| `include/linux/memcontrol.h` | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/memcontrol.h | `b067e1db2e0a2eb46faeb5bc7041efa4641bf4cea9aff3602d56e3023f7e4cf0` | 51 (`MEMCG_OOM_KILL`), 1005-1018 (`memcg_memory_event_mm()`) |
| `kernel/sched/psi.c` | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c | `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5` | 1056, 1087, 1715 (stall accounting, `/proc/pressure/memory`) |

Version note: the host kernel is `7.2.11-arch1-1` (`capture.txt:3-4`), so the `v7.2` upstream tag
is the matching major version; the tag is upstream Linux, not the Arch package build, and the
Arch build may carry patches.

## 4. Out of scope for this seat

- No file under `corpus/`, `tools/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md` or
  `SHONEN.md` was created or modified.
- The `corpus/knowledge/memory-pressure-r25.md` entry and its `.json`, the MP6 row text with its
  verdict and action, the `SKILL.md` decision-table row and the checker `verified_rows` count are
  other seats' work; this seat supplies the source row and the capture mapping only.
- No host command was run against the live host beyond reading the frozen capture; no service was
  started, stopped or restarted, no configuration was written, no package transaction was made.
- Sibling lane overlap (CPU, IO and IRQ pressure reading owned by mori) was not touched; this row
  concerns only the memory OOM-kill counters.

## 5. Open items for the L1

- The MP6 entry must carry a verdict and an action alongside this source; this seat supplies
  neither, and does not claim a verdict for the memory plane.
- If the entry asserts that `/proc/vmstat` counters are since-boot and that `memory.events`
  counters reset with the cgroup, those two lifetime claims need their own opened source; they are
  marked [inf] above and are not carried by S115.
- The row id S115 assumes the registry still ends at S114 at integration time; the L1 assigns the
  final number.

Report: .ufo/waves/round-25/w1/SrcKernelOomCounter.md
Scope: read=frozen capture `capture.txt` (sha256 `e60f1bbc…`), `SCORECARD.md` round-25 declaration (lines 784-801), `corpus/SOURCES.md` registry head and tail, `corpus/knowledge/oom-event-plane.md` lines 270-352, and upstream Linux v7.2 sources `mm/oom_kill.c`, `mm/memcontrol.c`, `mm/vmstat.c`, `include/linux/vm_event_item.h`, `include/linux/vmstat.h`, `include/linux/memcontrol.h`, `kernel/sched/psi.c`; wrote=.ufo/waves/round-25/w1/SrcKernelOomCounter.md (this report only); executed=curl of seven raw.githubusercontent.com v7.2 files (HTTP 200 each; one HTTP 429 on `include/linux/vmstat.h` retried successfully), sha256sum and grep/sed over the fetched bytes, grep/sed over the lane's frozen capture and corpus notes; no host command, no package transaction, no service action, no sudo.
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
