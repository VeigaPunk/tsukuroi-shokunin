# OOM-event plane — the 13:10 SIGKILL class, kernel OOM dumps, cgroup accounting, victims (TSUKUROI-R6-S6-3)

source: live read-only probes on host `plazir27` — `journalctl` (boot list, kernel ring, JSON, unit-filtered
windows), `systemctl show`/`cat`/`is-enabled`, cgroupfs reads under `/sys/fs/cgroup`, `/proc/{meminfo,pressure,
swaps,sys}`, `ps`, `free`, `swapon`, `df`, `oomctl`; user `vgpnk` (uid 1000, groups `vgpnk docker input wheel`),
non-root, no `sudo`. Kernel `7.2.3-arch1-3`; boot 0 id `d7f0bc8d938e4249b4a1f250cbfacf58`, started
2026-10-13 11:02:03 -03.
verified-at: **2026-10-14 14:38:25–14:46:20 -03** (UTC−3). Every count carries its command; the host is live and
memory counters drift — §4.6 records one drift observed during this capture.
recheck: §11 probe ledger; negative claims carry their sweep.
Substrate contract: nothing was written to the host — journal read-only, cgroup files read-only (the one
writability check is `test -w`; no write), no install/upgrade/remove, no service restarted, `sudo` never used.
`dmesg` itself is root-only here (`/proc/sys/kernel/dmesg_restrict`=1; `dmesg` → `read kernel buffer failed:
Operation not permitted`), so the kernel stream is read through `journalctl -k`. Scratch `/tmp/w6-tsukuroi-s63/`
(ephemeral; `oom-table-raw.txt` = the event-A task table as extracted).

Notation: **[observed]** measured · **[inference]** · **[unknown]** · **BLOCKED** = privilege-gated probe, recorded
not escalated. Names: **event A** = the 2026-10-13 23:44:30 kernel OOM; **event B** = the 2026-10-14 13:10:59
SIGKILL class (round-4 E1). All timestamps are host-local (-03).

## 1. Event inventory

The retained journal (13 boots, `journalctl --list-boots --no-pager`, 14:38) holds **one** kernel OOM dump and
**three** systemd OOM attribution messages, in **two** kill waves:

| # | when (-03) | class | what exists for it |
|---|---|---|---|
| A | 2026-10-13 23:44:30.57–31.60 | kernel OOM kill (global OOM), victim `python3` | full kernel dump (`journalctl -k`, text lines 6350–6581); 2 systemd messages (user scope + service); scope result `oom-kill` + unit accounting |
| B | 2026-10-14 13:10:59.35–59.40 | SIGKILL of the whole graphical session (user manager + helper) | systemd[1] sequence incl. one systemd OOM attribution message; service accounting (28.5G/34.2G); **no kernel record anywhere** (§3.3) |

The three systemd messages (`journalctl -o json`, filtered on the message text, 14:39):

| # | timestamp | emitted by | message |
|---|---|---|---|
| 1 | 2026-10-13 23:44:30.574948 | `systemd[1573]` (the old **user** manager) | `app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope: The kernel OOM killer killed some processes in this unit.` |
| 2 | 2026-10-13 23:44:30.576028 | `systemd[1]` (init.scope) | `user@1000.service: The kernel OOM killer killed some processes in this unit.` |
| 3 | 2026-10-14 13:10:59.400591 | `systemd[1]` (init.scope) | `user-1000.slice: The kernel OOM killer killed some processes in this unit.` |

`journalctl --no-pager | grep -c "kernel OOM killer killed some processes"` = **3** — i.e. round 4's single
message for event A was one of two; event A produced a scope-level message (from the user manager) *and* a
service-level message (from PID 1).

Boundary — classes in the same vocabulary that are **not** this plane and were not absorbed here:
- **process-level heap OOM** (Node/V8 `FatalProcessOutOfMemory` coredumps): 15 distinct coredumps in boot 0
  carry that backtrace (streamed pairing of `systemd-coredump … terminated abnormally` with
  `FatalProcessOutOfMemory` lines; first occurrence Oct-13 12:43, most at 13:59–14:01, e.g.
  `Process 190918 (MainThread) … signal 5/TRAP`). These are application failures, not kernel kills; handed to
  the journal/coredump workstreams, not absorbed.
- **coredump storm** (round-4 count 244, not re-measured here) and the LOVE `SIGABRT` immediately before
  event B (§3.4) — adjacent, separate owners.
- **userland OOM monitors**: `systemd-oomd` inactive+disabled, `earlyoom` not installed (§7 rows 1–2) — so
  neither produced any kill.

## 2. Event A — the only kernel OOM dump in retention (2026-10-13 23:44:30)

### 2.1 Trigger and victim

All 3 lines below are `journalctl -k -b --no-pager -o short-precise` (captured 14:38):

- Trigger [observed]: `GpuWatchdog invoked oom-killer: gfp_mask=0x140cca(GFP_HIGHUSER_MOVABLE|__GFP_COMP),
  order=0, oom_score_adj=200` at 23:44:30.570564, initiator `CPU: 20 UID: 1000 PID: 331582 Comm: GpuWatchdog`
  (a Chromium GPU-watchdog thread), fault path `filemap_fault`/`exc_page_fault` [from the Call Trace].
- Selection [observed]: `oom-kill:constraint=CONSTRAINT_NONE,nodemask=(null),cpuset=user.slice,mems_allowed=0,
  global_oom,task_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/app-graphical.slice/
  app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope,task=python3,pid=1732581,uid=1000` — a *global* OOM
  (constraint NONE), kill inside the user slice.
- Victim [observed]: `Out of memory: Killed process 1732581 (python3) total-vm:56727648kB,
  anon-rss:27873696kB, file-rss:16kB, shmem-rss:0kB, UID:1000 pgtables:110928kB oom_score_adj:200`
  (≈26.6 GiB anon RSS at kill time).
- The victim lived in a transient XDG-terminal scope started the day before:
  `Oct 13 11:14:28.086296 … '--unit=app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope' … xdg-terminal-exec
  --dir=/home/vgpnk` (`uwsm_app-daemon[1817]`).

### 2.2 The pre-OOM memory picture, straight from the dump

From the same dump (Mem-Info block, 23:44:30.635–636): **[observed]**

| signal | dump value | reading |
|---|---|---|
| `free:` | `54844` pages ≈ 214 MiB | free memory at trigger |
| Node 0 Normal | `free:88276kB min:113068kB low:142808kB high:172548kB` | free **below the min watermark** |
| `Free swap` / `Total swap` | `44kB` / `35917176kB` | swap effectively **full** (35.9 GB of 35.9 GB) |
| `all_unreclaimable?` | `yes` | reclaim had given up |
| anon pages | `active_anon:4014530 inactive_anon:3133887` (pages) ≈ 27.3 GiB | the pressure was anonymous memory |
| `zspages` | `20544kB` + `1122508kB` ≈ 1.14 GiB | zswap/zsmalloc-class pages — see Q4 (zswap is *off*) |

The swap figure matches the persistent slice accounting (§4.3): the old session's `memory.swap.peak` is
**34.2 GiB** against **34.25 GiB** total swap — the swap plane was saturated well before this kill.

### 2.3 The task table survey (164 rows)

The dump lists every task in the OOM domain: **164 rows** (`[ pid ] uid tgid total_vm rss rss_anon rss_file
rss_shmem pgtables_bytes swapents oom_score_adj name`). Aggregates and top consumers (extracted 14:39;
raw copy `/tmp/w6-tsukuroi-s63/oom-table-raw.txt`):

| metric | value |
|---|---|
| rows | 164 (uid 1000: 139 · uid 0: 17 · uid 81: 2 · uid 969: 2 · 102/973/974/977: 1 each) |
| Σ `rss_anon` | 7,140,787 pages = 27.24 GiB |
| Σ `swapents` | 8,228,965 pages = 31.39 GiB |

Top consumers at the moment of the kill [observed]:

| pid | oom_score_adj | rss_anon (pages → GiB) | swapents (pages → GiB) | name |
|---|---|---|---|---|
| 1732581 | 200 | 6,968,424 → 26.58 | 7,110,160 → 27.12 | **python3 (the victim)** |
| 295525 | 200 | 30,388 → 0.12 | 88,646 → 0.34 | kimi |
| 336192 | 200 | 30,004 → 0.11 | 114,532 → 0.44 | devin |
| 1758897 | 200 | 10,872 → 0.04 | 73 | godot |
| 1758861 | 200 | 9,318 → 0.04 | 11 | godot |
| 333587 | 300 | 8,845 → 0.03 | 9,503 → 0.04 | chromium |
| 336136 | 200 | 8,839 → 0.03 | 8,377 → 0.03 | devin |
| 1811 | 200 | 6,805 → 0.03 | 7,523 → 0.03 | elephant |

`oom_score_adj` distribution: `-1000`×1, `-900`×2, `-250`×1, `0`×23, `100`×2, `200`×120, `300`×15 — i.e. the
user workload ran at +200 (and Chromium helpers at +300), which is exactly the band the kernel scans first.
**[inference]** the victim was the dominant anonymous-memory holder (26.6 GiB anon + 27.1 GiB swapped of the
27.2 GiB anon total), so its death returned the budget that re-armed the system; the trigger being a Chromium
GPU-watchdog page fault is the *symptom of exhaustion*, not the memory holder.

### 2.4 Aftermath of event A

[observed] one second later the scope was finished by the user manager:

- `23:44:31.603001 systemd[1573]: app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope: Failed with result 'oom-kill'.`
- `23:44:31.603718 … Consumed 19h 12min 17.770s CPU time over 12h 30min 3.509s wall clock time, 27.4G memory
  peak, 30.7G memory swap peak.`

Because the scope was transient and `--collect`ed, its cgroup (and its counters) are gone — nothing of event A
survives in the cgroup files; it survives in the journal (§2.1–2.2). The boot continued; the session itself was
not torn down (the user manager `systemd[1573]` stayed alive until event B).

## 3. Event B — the 13:10:59 SIGKILL class

### 3.1 The sequence (all `journalctl -b -o short-precise`, window 13:10:40–13:11:20)

| # | time | writer | event |
|---|---|---|---|
| 0 | 13:10:49.320394 | systemd-coredump | LOVE `SIGABRT` core processed (`Process 1201250 (love) … signal 6/ABRT`, `liblove-11.5.so` backtrace) |
| 1 | 13:10:59.346180 | sddm-helper[1567] | `[PAM] Closing session` |
| 2 | 13:10:59.347555 | sddm-helper[1567] | `session closed for user vgpnk` |
| 3 | 13:10:59.360829 | systemd[1] | `session-1.scope: Deactivated successfully.` |
| 4 | 13:10:59.361095 | sddm[1562] | `Auth: sddm-helper exited with 9` |
| 5 | 13:10:59.361672 | systemd-logind | `Session 1 logged out. Waiting for processes to exit.` |
| 6 | 13:10:59.361935 | systemd-logind | `Removed session 1.` |
| 7 | 13:10:59.380873 | systemd[1] | `user@1000.service: Main process exited, code=killed, status=9/KILL` |
| 8 | 13:10:59.381136 | systemd-logind | `Removed session 2.` |
| 9 | 13:10:59.381949 | systemd[1] | `user@1000.service: Failed with result 'signal'.` |
| 10 | 13:10:59.400143 | systemd[1] | `user@1000.service: Consumed 1d 11h 3min 1.574s CPU time over 1d 2h 8min 53.364s wall clock time, 28.5G memory peak, 34.2G memory swap peak.` |
| 11 | 13:10:59.400591 | systemd[1] | `user-1000.slice: The kernel OOM killer killed some processes in this unit.` |
| 12 | 13:11:07.283287 | sddm | greeter Login → a **new** graphical session (leader `uwsm … Hyprland`, MainPID 1203171) starts |

[observed] nothing between #6 and #7 requests the stop: **no `Stopping User Manager for UID 1000…` line exists**
in the boot (`journalctl -b | grep "Stopping User Manager"` → none in the window; the ledger §11 has the sweep).
PID 1 did not initiate the teardown; the user manager died of an external SIGKILL.

Structural context [observed]: `user-1000.slice` **never stopped** across this event —
`systemctl show user-1000.slice -p ActiveEnterTimestamp -p InvocationID` = `Tue 2026-10-13 11:02:05 -03`,
`cc612e6f66fa4bbcad7fa0b7dd02df19`, SubState `active` at 14:44. Only `user@1000.service` was destroyed and
recreated (new `InvocationID=e288c87781a242ab87ebf3f236a96226`, `NRestarts=0`, active since 13:11:07). This is the
reason the *slice-level* accounting survives (§4.3).

### 3.2 What systemd accounted

[observed] `user@1000.service`'s final line (#10) reports **28.5G memory peak / 34.2G memory swap peak** —
byte-identical, at the slice level, to what the cgroup files still show (`memory.peak` 30,699,745,280 B =
28.59 GiB; `memory.swap.peak` 36,744,949,760 B = 34.22 GiB, §4.3). [inference] the peaks are the **old
session's** values (the new session's own service cgroup, created 13:11:07, reads its own peak 26.86 GB, a
different object), so the kill met a session whose swap footprint had reached ≈99.9 % of the 34.25 GiB swap and
whose total footprint peaked at 28.6 GiB — the same saturation profile as event A.

sddm-helper `exited with 9` (#4) means the PAM session helper was killed by signal 9 too, 19 ms before the user
manager. Two sessions were removed (#3/#8: sessions 1 and 2 — the user's graphical session and its
manager-early session).

### 3.3 The decisive negative — why "no kernel record" is a measurement, not a privilege artifact

[observed] there is **no OOM-family kernel record anywhere** for event B:

1. `journalctl -k -b --since "2026-10-14 13:10:55" --until "2026-10-14 13:11:12"` = 121 records; classified,
   they are sr0 optical noise + `UFW BLOCK` + one `Hyprland[1203102]: segfault … libaquamarine.so.0.15.0`
   (the *greeter's* Hyprland, uid 964, at 13:11:07.408). Nothing else. The 13:10:59 second itself carries sr0
   records from `.404645` onward — **kernel records from that same second were captured**.
2. The journal's kernel stream is continuous from the boot banner (`journalctl -k -b | head -1` =
   `Oct 13 11:02:03.040941 Linux version 7.2.3-arch1-3`), and it still retains the Oct-13 23:44 dump
   (7 h earlier) — so the ring/journal did not wrap past the event.
3. Dumps were *enabled*: `oom_dump_tasks`=1, `panic_on_oom`=0 (`/proc/sys/vm/*`, 14:41). `printk` = `0 4 1 4`
   (console loglevel 0 from the `quiet splash loglevel=0` cmdline) affects the console only, not the ring.
4. journald drop is not supported by any trace: `/etc/systemd/journald.conf` is all-commented (defaults,
   no drop-in dir), and boot 0 has **no** journald `Suppressed N messages` entry — the 4 grep hits for
   "suppressed" are kernel `scsi_io_completion_action: 10 callbacks suppressed` /
   `blk_print_req_error: 10 callbacks suppressed` notices.
5. The census's OOM arm is blind to it by construction: with its exact command
   (`journalctl -k -b -p err -o json`, `tools/tsukuroi-census.sh:399-425`), boot 0 yields 139 entries and the
   class regex `CLASS_OOM='Out of memory|oom-kill|oom_reaper'` (`tools/tsukuroi-census.sh:163`) matches exactly
   **1** entry — the event-A kill line. (Unfiltered, the same regex also matches event A's
   `invoked oom-killer` and `oom-kill:constraint=…` lines = 3 hits; `-p err` leaves only the kill line.)

So event B is visible **only** through systemd's interpretation (#11) and the service accounting (#7/#10).

### 3.4 The 110 seconds before (adjacent, causal link [unknown])

[observed] in the old session's last 2 minutes:

- **6 Chromium scopes started** (`systemd[1573]: Started app-org.chromium.Chromium-…`) at 13:08:45.18,
  13:09:58.95, 13:10:06.87, 13:10:13.02, 13:10:32.26, 13:10:34.60 (PIDs 1161990/1190456/1192514/1194175/
  1198002/1198710). Who drives this launch cadence is not visible read-only (Q6).
- **LOVE `SIGABRT` coredump 9.7 s earlier** (#0), backtrace in `liblove-11.5.so` — the same process family
  round 4 flagged next to E1.
- **The sr0 read burst in the kill's own second** (30+ `Logical block address out of range` records starting
  13:10:59.4046), recurring at 13:11:07 — the round-4 E3 unknown (Q5) now has a *third* occurrence.

No measurement here links any of these to the SIGKILL; each stays its own question.

### 3.5 Candidate mechanisms for the missing kernel record (hypotheses, not conclusions)

| H | statement | supporting | against | discriminator |
|---|---|---|---|---|
| H1 | Kernel OOM path ran but its print is absent from the journal | systemd attribution (#11) + SIGKILL timing | §3.3(1,2,3,4): same-second kernel capture, no wrap, dumps enabled, no journald suppression — no positive evidence of loss | none read-only now: raw ring is BLOCKED (`dmesg_restrict=1`); would need root `dmesg` *before* it wraps |
| H2 | SIGKILL came from a non-kernel path; systemd's message came from its own counter bookkeeping | no `Stopping` request (#7); helper also exit 9; counter anomaly (§4.2) proves systemd does read these counters | systemd's message names the kernel explicitly | controlled cgroup-kill experiment to see what systemd logs — **out of province** (mutating test) |
| H3 | #11 is a *deferred/aggregated* report of the Oct-13 wave read during teardown | counter for the old hierarchy is 1, not 2 (§4.2) | event A already produced its own two messages on Oct 13 (table §1); systemd emitted none for this counter then | counter-lifecycle semantics (Q2) |

Per the lane's anti-claim, this is a **kernel/attribution-internals question**: reported here with the exact
probes, never absorbed. Owner suggestion in Q1.

## 4. cgroup accounting, readable non-root

All files under `/sys/fs/cgroup` are world-readable here; 95 `memory.events` files were scanned (14:39) and the
only ones with `oom_kill ≠ 0` are the two in the table below.

### 4.1 Live snapshot (captured 14:38–14:46)

| path | `memory.events` oom_kill / oom / sock_throttled | `memory.events.local` oom_kill | other |
|---|---|---|---|
| `user.slice` | **1** / 0 / 67558 | **0** | `memory.swap.events` `fail 5,922,849` (same as below — shared descendant account) |
| `user.slice/user-1000.slice` | **1** / 0 / 67558 | **0** | `memory.current` 26.0 GB; `memory.peak` 30.70 GB (28.59 GiB); `memory.swap.current` 2.34 GB; `memory.swap.peak` 36.74 GB (34.22 GiB); `memory.max`/`memory.high` = `max`; `memory.swap.max` = `max`; `oom.group` 0 |
| `…/user@1000.service` (current, since 13:11:07) | 0 / 0 / 3320 | 0 | `systemctl show`: `MemoryCurrent` 26.49 GB, `MemoryPeak` 26.86 GB, `MemoryHigh/Max/SwapMax` = infinity, `MemoryAvailable` 21.1 GB, `ManagedOOMMemoryPressure=auto` |
| `…/session-4.scope` | 0 / 0 / 0 | — | — |
| `…/user@1000.service/app.slice` | 0 / 0 / 3320 | — | — |

Memory-controller delegation [observed]: `cgroup.subtree_control` = `cpu memory pids` at user.slice,
user-1000.slice and the user manager; `app.slice/memory.max` is **writable by uid 1000**, while
`user@1000.service/memory.max` is root-owned `-rw-r--r--` (writability checked with `test -w`; nothing written).

### 4.2 The counter anomaly — two documented waves, surviving counter = 1

[observed] Two kill waves are documented inside `user.slice` (§1), yet after both, `user.slice` and
`user-1000.slice` each read `oom_kill 1` (`memory.events.local` at the slice = 0), and no live descendant has a
non-zero value (95-file sweep). The old hierarchy that contained event B (`user@1000.service` and below) was
destroyed and replaced; the new service cgroup counts from zero.

[unknown] which wave the surviving "1" represents, and how `memory.events` counters behave when the subtree that
generated them is destroyed — the two models agree with different parts of the data (a static accumulate-at-event
model predicts 2 at both surviving ancestors; a sum-over-live-descendants model predicts 0, since no live
descendant is non-zero). Not resolvable by the retained files; a controlled test (create/kill a cgroup) is out of
province. Q2. **Consequence for detection:** treat `memory.events oom_kill` as a *presence flag*, not as a
per-event meter, and use the journal messages (§8 C2) as the event list.

### 4.3 Accounting that survives a session restart

| signal (path) | value at capture | why it matters |
|---|---|---|
| `user-1000.slice/memory.peak` | 30,699,745,280 B = 28.59 GiB | matches systemd's `28.5G memory peak` for the dead session (§3.2) |
| `user-1000.slice/memory.swap.peak` | 36,744,949,760 B = 34.22 GiB | vs `SwapTotal` 35,917,176 kB = 34.25 GiB → swap was ~99.9 % used at some point |
| `user-1000.slice/memory.swap.events` | `high 0 max 0 fail 5,922,849` | **5.9 M swap-slot allocation failures**, cumulative; the new session's own service cgroup shows `fail 4` — i.e. this number is dominated by the old session |
| `user-1000.slice/memory.stat` (14:42) | `pswpin 72,101,753` / `pswpout 93,772,577` pages (275 / 358 GiB); `pgscan_direct 132,223,585`; `pgmajfault 26,222,568`; `workingset_refault_anon 70,470,418` | cumulative thrash evidence, survives the restart |
| `user-1000.slice/memory.events` | `sock_throttled 67,558` | socket-memory throttling inside the slice — a second pressure class |

### 4.4 Reading rule: `memory.current`/`peak` include page cache

[observed] at 14:42 the slice read `memory.current` 26.0 GB while `memory.stat` showed `anon` 2.59 GB, `file`
21.31 GB, `slab` 1.02 GB — ~21 GB of reclaimable file cache inside a 31.7 GB machine whose `free` showed
11.6 GB used / 19.4 GB available. **A cgroup "peak" is therefore not a pressure reading**; the pressure
signals in this plane are `memory.swap.peak`, `memory.swap.events.fail`, `pswpin/pswpout`, PSI, and the
kernel/systemd records. (This also softens §3.2's 28.5 G peak: the *swap* peak is the hard number.)

### 4.5 No guards configured anywhere on the path

[observed] `memory.high`/`memory.max` = `max` (slice) and `MemoryHigh/Max/SwapMax` = `infinity` (service);
`memory.oom.group` = 0; `systemd-oomd` inactive+disabled; `earlyoom` absent; `MemoryPressureWatch` = `skip`
(pinned upstream in `/usr/lib/systemd/system/user@.service`). Nothing was configured to act before the kernel.

### 4.6 Freshness — a drift observed during this capture

[observed] zram0 readings minutes apart: swapon `USED 2.2G` (mm_stat `orig_data_size` 2,453,393,408 B,
`mem_used_total` 1,060,499,456 B) at ~14:41:33 → swapon `770.6M` / `/proc/swaps` 789,124 KiB and mm_stat
`orig` 751,521,792 B / `mem_used` 176,365,568 B at 14:43:49. Same-second cross-checks then agree
(`free` 14:42:58: swap used 800 Mi; `free` 14:43:49: 798 Mi). This was real churn, not a tool conflict —
recorded so no later reader treats the discrepancy as a bug.

## 5. The pre-OOM memory picture that IS readable non-root

What a non-root seat can and cannot see, per signal, with what was actually available for each event:

| signal | command | pre-event? | post-event survival | used for |
|---|---|---|---|---|
| kernel OOM dump | `journalctl -k` (dmesg BLOCKED, `dmesg_restrict=1`) | only if the kernel OOM path prints | permanent in the journal | event A fully (§2.2); event B not at all |
| systemd unit accounting | `journalctl -b \| grep "Consumed .*memory peak"` | no — emitted at unit death | permanent | event A scope 27.4G/30.7G; event B service 28.5G/34.2G |
| systemd OOM attribution | `journalctl -b \| grep "kernel OOM killer killed"` | no | permanent | the *only* process attribution for event B |
| cgroup events/peaks | `/sys/fs/cgroup/…/memory.{events,peak,swap.peak,swap.events,stat}` | live only (no history) | while the cgroup exists; slice survives session restarts | §4.3 — the swap evidence of event B |
| PSI | `/proc/pressure/memory` | live (`some`/`full` with 10/60/300 s averages) | totals only | 14:42: `avg300=0.09`, `total=69,393,986 µs` |
| free memory | `free -h`; `/proc/meminfo` | live only | none | 14:42:58: 30.98 G total, 11.63 used, 3.51 free, 19.35 available, swap 800 Mi used |
| tmpfs pressure | `df -h /tmp` | live | none | `/tmp` = 16 G tmpfs, **6.5 G used (43 %)** — `Shmem` 6.4 GiB of `free` |
| top consumers | `ps -eo pid,user,rss,pmem,comm --sort=-rss` | live | none | 14:42: kimi 706 MB, chromium ×6 260–344 MB, devin, Hyprland … |
| userland monitor | `systemctl is-active systemd-oomd`; `oomctl` | absent (inactive; `oomctl` → `Could not activate remote peer`) | — | nothing was watching |
| journald/kernel continuity | `journalctl -k -b \| head -1` | — | — | validates negatives (§3.3) |

**Reconstruction of event B's pre-OOM picture** [inference, from §4.3]: a session that had at some point swapped
34.2 of 34.25 GiB, accumulated 5.9 M swap-slot allocation failures, and was peaking at 28.6 GiB — with no
userland monitor and no cgroup guards (§4.5). Nothing in the journal *before* the kill announces it; the
readable pre-OOM picture exists only in the cumulative cgroup counters, and only because the *slice* cgroup
outlived the session.

## 6. Victim list

### 6.1 Event A — directly enumerable

| victim | evidence |
|---|---|
| `python3` PID 1732581 (uid 1000), 26.6 GiB anon RSS, in the XDG-terminal scope | kernel `Out of memory: Killed process …` line (§2.1) |
| the rest of that scope | scope `Failed with result 'oom-kill'`, collected (§2.4) — remaining members were torn down by the user manager; individual processes not listed (SIGKILL produces no coredump: `coredumpctl` holds none for that second) |

The other 163 tasks in the dump (§2.3) were *not* killed by the kernel in this event.

### 6.2 Event B — partially provable, not enumerable

| provable death | evidence |
|---|---|
| `user@1000.service` main process = the old systemd user manager (PID 1573, the writer of the Oct-13 messages) | `Main process exited, code=killed, status=9/KILL` + `Failed with result 'signal'` |
| `sddm-helper[1567]` | `Auth: sddm-helper exited with 9` |
| sessions 1 and 2 (user graphical + manager-early) | `Removed session 1` / `Removed session 2`, `session-1.scope: Deactivated successfully` |
| **everything inside the old session's cgroup tree** (Hyprland session processes, the 6 just-started Chromium scopes, terminal/agent processes) | [inference] as members of the killed service's cgroup; **no per-process record exists** — the user manager died by SIGKILL, its journal ends at 13:10:34.599 (`systemd[1573]` last line), and its units' stop messages were never emitted |

[unknown] the exact process list of event B — the reason is structural (the writer was the victim), not a probe
gap; Q3 records it as unrecoverable from retained state.

## 7. Prevention options — operator-owned; detection-only here

Nothing in this table was changed by this lane; every "current state" cell is a measurement. "Would it have
helped" is [inference] unless marked otherwise.

| # | lever | measured current state | mechanism vs these events | operator action (not taken here) | tsukuroi detection |
|---|---|---|---|---|---|
| 1 | `systemd-oomd` (userland PSI+swap monitor) | unit present (`/usr/lib/systemd/system/systemd-oomd.service`); `is-active`=inactive, `is-enabled`=disabled; socket disabled; `oomctl` cannot reach it; `oomd.conf` all-commented (defaults `SwapUsedLimit=90%`, `DefaultMemoryPressureLimit=60%`, `DefaultMemoryPressureDurationSec=30s`); `ManagedOOMMemoryPressure=auto` + `ManagedOOMSwap=auto` **already set** on `user@1000.service` and `user-1000.slice` | [inference] event B met a swap plane at ≈99.9 % and event A at 100 % — above oomd's 90 % swap rule; oomd would likely have acted *before* the kernel, at the cost of policy-driven kills (it kills the pressured cgroup's processes) | `systemctl enable --now systemd-oomd` (a service action — outside this lane) | `is-active`/`is-enabled`; presence of `sock_throttled`, `swap.peak`, `swap.events.fail` |
| 2 | `earlyoom` | `command -v earlyoom` → not-found; no unit | alternative userland monitor (no PSI threshold semantics) | install (outside this lane) | `command -v`/unit check |
| 3 | per-unit memory guards (`MemoryHigh`/`MemoryMax`) | `max`/`infinity` everywhere on the path (§4.5); **controller delegated**: `memory` in `subtree_control` down to the user manager, `app.slice/memory.max` writable by uid 1000, `user@1000.service/memory.max` root-only | a `MemoryHigh` on the big app scope throttles reclaim instead of letting the kernel choose a victim; a `MemoryMax` confines a kill to one unit | set `MemoryHigh=`/`MemoryMax=` (user for own app scopes; root for the service) | read `memory.max`/`memory.high` per unit; report `infinity` as "no guard" |
| 4 | pressure-watch export (`MemoryPressureWatch=`) | `skip` on `user@1000.service` (pinned in `/usr/lib/systemd/system/user@.service`, not a local override); system default `DefaultMemoryPressureWatch=auto`; other units show `auto` | `on` exports `$MEMORY_PRESSURE_WATCH` to a unit's processes so apps can react themselves (per `systemd.resource-control(5)`) — a *cooperating-app* lever, not a guard | drop-in `MemoryPressureWatch=on` where useful | property read; no kill semantics |
| 5 | swap plane capacity | `/swap/swapfile` 30.3 G (prio 0; 30.1 M used @14:43:49) + `/dev/zram0` 4 G (prio 100; orig data 0.72–2.28 GiB across captures, `mem_used_max` 1.41 GiB); `zswap.enabled=0` (sysfs and cmdline) | both kill events end at 100 %/99.9 % swap — capacity itself participates | grow swapfile / zram size; or enable zswap (needs planning; `zswap.enabled=0` is a deliberate cmdline choice here) | `swapon --show`, `memory.swap.peak`, `swap.events.fail` |
| 6 | `oom_score_adj` steering | user workload at +200 (120 tasks), Chromium helpers +300, victim +200, system/elephant at −900/0 (§2.3) | the +200 band is chosen first; marking a known-huge batch job differently changes who dies | `OOMScoreAdjust=` in units (user-scope units are the user's) | kernel dump's adj column; live `/proc/*/oom_score_adj` |
| 7 | tmpfs discipline | `/tmp` 16 G, **6.5 G used** (43 %) at 14:42:58; `/dev/shm` 72 M | `/tmp` content is `Shmem` — memory that competes with anon | cap tmpfs size / clean scratch before heavy rounds | `df -h /tmp`, `meminfo Shmem` |
| 8 | kernel OOM diagnostics | `oom_dump_tasks=1`, `panic_on_oom=0`, `overcommit_memory=0`, `swappiness=60` | dumps are enabled — §3.3 uses this to argue the missing event-B record is *not* a dump-setting artifact; `panic_on_oom=1` would be catastrophic here (global OOM occurred) | leave as-is; revisit only with cause | `/proc/sys/vm/*` |
| 9 | stop-time behaviour | `/etc/systemd/system/user@.service.d/faster-shutdown.conf` → `TimeoutStopSec=5s` | shortens the kill window on any user-manager stop (and makes the teardown observed in event B final within seconds) | operator choice; not a prevention lever | unit drop-in read |
| 10 | detection design | — | **do not use cgroup counters as an event count** (§4.2); use the journal message (C2) | — | see §8 |

## 8. Detection contract for this plane (read-only, per round)

Commands (all non-root; each maps to a section):

- **C1** kernel OOM dumps: `journalctl -k -b -p err -o json --no-pager` + regex
  `Out of memory|oom-kill|oom_reaper` (the census arm; event A ⇒ 1 entry, **event B ⇒ 0** — blind spot §3.3.5).
- **C2** systemd OOM attribution: `journalctl -b --no-pager | grep -c "kernel OOM killer killed some processes"`
  (event A ⇒ 2, event B ⇒ 1).
- **C3** SIGKILL/teardown class: `journalctl -b --no-pager | grep -E "status=9/KILL|Failed with result
  '(signal|oom-kill)'"` (event B ⇒ 3 lines).
- **C4** cgroup presence flag: read `memory.events` at `user.slice` + `user-1000.slice` + current
  `user@1000.service` (+ `.local`); report as "an oom_kill has been accounted since this cgroup was created",
  never as a count.
- **C5** swap-pressure anchors: `memory.swap.peak` vs `SwapTotal`, `memory.swap.events.fail`,
  `memory.stat` `pswpin/pswpout`, `memory.events` `sock_throttled`.
- **C6** live picture: `free -h`, `/proc/pressure/memory`, `df -h /tmp`, `ps … --sort=-rss`.

Reading rules: entry counts, not raw lines; `-p err` semantics (above); kernel facts from `journalctl -k`,
attribution facts from `journalctl`; every negative claim carries its sweep (boot list / ring head / message
count). A round that reports `kerr oom=1` while saying nothing about event B is telling the truth about the
kernel arm and nothing about this class — the two must be reported together.

## 9. Open questions (register)

| Q | question | what would settle it | owner suggestion |
|---|---|---|---|
| Q1 | Event B: why no kernel record, and what killed the session (H1/H2/H3, §3.5) — kernel/attribution internals | root `dmesg` (BLOCKED now) *before* ring wrap; systemd/kernel source for the message trigger; controlled test | fleet/operator; per anti-claim, not absorbed here |
| Q2 | `memory.events` counter lifecycle across subtree destruction: two waves, surviving `oom_kill=1` (§4.2) | controlled cgroup experiment (mutating — out of province) or kernel documentation | operator/kaidoku |
| Q3 | Event B victim list beyond §6.2 | nothing retained can answer; needs a pre-death snapshot mechanism (e.g. `systemd-cgtop` logging) | fleet (monitoring gap) |
| Q4 | `zspages` ≈1.14 GiB in the event-A dump while `zswap.enabled=0` (sysfs `N` + cmdline) | kernel/zram accounting documentation; root `dmesg` | operator |
| Q5 | sr0 burst coincident with both kill seconds *and* 13:11:07 (round-4 E3) | udev/media check; `lsof`-class probe must run in the moment | driver workstream |
| Q6 | Who starts 6 Chromium scopes in the 110 s before event B | process audit at the next occurrence (parent chain of the scope leader) | fleet/operator |
| Q7 | zram accounting semantics (`swapon USED` vs `mm_stat orig`/`mem_used`) — device internals | kernel/zram docs; not chased here | operator |

## 10. Errata (append-only)

- **E1 (round-4 E1 confirmed and extended).** Round 4 recorded event B as "[unknown]: the kernel-side OOM detail
  for this kill is absent from the ring". Re-measured 2026-10-14 14:38–14:45 with three strengthenings: (a) the
  same second carries journaled kernel records (sr0) → the absence is not a capture gap; (b) journal `-k`
  continuity from the boot banner and no wrap past the event; (c) `oom_dump_tasks=1` → dumps enabled.
  New: the journal-wide count of `kernel OOM killer killed some processes` messages is **3**, not 1 —
  event A produced a scope-level (user manager) *and* a service-level (PID 1) message; only event B's is the
  slice-level one.
- **E2 (round-4 count confirmed).** The boot's only `Out of memory: Killed process` line remains the Oct-13
  23:44:30 `python3` one — re-checked across all 13 retained boots at 14:39 (`journalctl -k --no-pager | grep -c`
  = 1 for both `invoked oom-killer` and `Out of memory: Killed process`).
- **E3 (self-erratum, freshness).** The first swapon capture (~14:40) read zram `USED 2.2G`; two minutes later
  the same command read `770.6M` (§4.6). Live churn, not a tool conflict — recorded so the number is not
  quoted as if stable.

## 11. Probe ledger (spot-check anchors)

Ordered by capture; all read-only. Host-local times, 2026-10-14.

1. 14:38:25 `date -Is`; `uptime -s`; `journalctl --list-boots --no-pager` (13 boots; boot 0 `d7f0bc8d…`).
2. 14:38 `journalctl -k --no-pager | grep -nE "invoked oom-killer|Out of memory|oom_reaper|oom-kill:"`
   (3 hits, all Oct-13 23:44:30; text lines 6350/6580/6581).
3. 14:38 `journalctl -k -b --no-pager -o short-precise | sed -n '6350,6581p'` → event A dump; task table
   copied to `/tmp/w6-tsukuroi-s63/oom-table-raw.txt` (165 lines incl. header).
4. 14:39 `journalctl -o json` scan → the 3 `kernel OOM killer killed some processes` messages (§1 table).
5. 14:39–14:40 `journalctl -b -o short-precise --since "2026-10-14 13:10:40" --until "2026-10-14 13:11:20"`
   → event B sequence (§3.1); `journalctl -k … 13:10:55–13:11:12` → 121 records, classification sweep §3.3(1).
6. 14:39–14:44 `journalctl -b --no-pager | grep -c "kernel OOM killer killed some processes"` = 3; boot-0
   `status=9/KILL|code=killed|status=137` sweep = 2 lines (the user manager + the kernel kill line).
7. 14:38–14:46 cgroup reads: `memory.events[.local]`, `memory.peak/current/max/high`, `memory.swap.*`,
   `memory.stat`, `memory.swap.events`, `memory.oom.group`, `memory.zswap.*` at `user.slice`, `user-1000.slice`,
   `user@1000.service`, `session-4.scope`, `app.slice`; 95-file `memory.events` sweep for non-zero `oom_kill`.
8. 14:40 `systemctl show user@1000.service|user-1000.slice -p Memory*|ManagedOOM*|MemoryPressureWatch`;
   `user-1000.slice -p ActiveEnterTimestamp -p InvocationID`.
9. 14:40–14:41 `systemctl is-active/is-enabled systemd-oomd`; `oomctl`; `systemctl cat systemd-oomd`;
   `command -v earlyoom`; `/proc/sys/vm/*`; `/proc/sys/kernel/printk`; `swapon --show`; `zram0/mm_stat`.
10. 14:42:22–14:43:49 `free -h`/`-m`; `/proc/meminfo`; `/proc/pressure/*`; `df -h /tmp /dev/shm /run`;
    `ps -eo pid,user,rss,pmem,comm --sort=-rss`.
11. 14:44 `journalctl -k -b -p err -o json --no-pager | wc -l` = 139; regex replay = 1 event-A entry (§8 C1).
12. 14:44–14:45 `dmesg` (denied); `journalctl -k -b | head -1` (boot banner); `grep -c suppressed`;
    `test -w` on `app.slice/memory.max` (writable) and `user@1000.service/memory.max` (not);
    `grep -i pressure /usr/lib/systemd/system/user@.service` (`MemoryPressureWatch=skip`).
13. 14:39 V8-OOM boundary count: streamed `journalctl -b -o json` pairing → 15 distinct coredumps with
    `FatalProcessOutOfMemory` backtraces (boot 0).

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — read-only `journalctl`, `systemctl`, cgroupfs, `/proc`, `ps`, memory and disk probes on host `plazir27`, 2026-10-14.
verified-at: 2026-10-14 (the original live OOM/event capture window recorded in this note).
recheck: 30d; procedure: §11 probe ledger; keep event-window and cumulative-counter claims distinct.
supersedes the pointer-only recheck: line above.


## R18-FRESHNESS — oom-event-plane line 51 earlyoom (2026-10-20)

Appended 2026-10-20 by the tsukuroi round-18 L1 (NoticeOom seat); earlier bytes unchanged. Historical measurements stay historical: the 2026-10-14 statement at line 51 that `earlyoom` was not installed keeps its dated meaning and is superseded as a current-use fact only. Now: earlyoom 1.9.0-1 installed [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:16-23, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39] (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:29`; active and enabled at lines 17-18; source S060, fresh R18 read-only capture). Read-only scope: this grants no package, reboot, or service clearance and draws no host pressure conclusion.

## R18-FRESHNESS — oom-event-plane line 280 earlyoom (2026-10-20)

Appended 2026-10-20 by the tsukuroi round-18 L1 (NoticeOom seat); earlier bytes unchanged. Historical captures stay historical: the 2026-10-14 `earlyoom` absence at line 280 keeps its dated meaning and is superseded as a current-use fact only. Now: earlyoom active (since 2026-10-20 09:57:11 -03) and enabled [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:16-23, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39] (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:21`; source S060). Read-only scope: no package, reboot, or service clearance follows, and no host pressure conclusion is drawn.

## R18-FRESHNESS — oom-event-plane line 345 earlyoom probe row (2026-10-20)

Appended 2026-10-20 by the tsukuroi round-18 L1 (NoticeOom seat); earlier bytes unchanged. The §7 row 2 measured-state cell at line 345 is a dated 2026-10-14 probe and stays as measured. Its install action is superseded as current-use guidance only. Now: command -v earlyoom resolves to /usr/bin/earlyoom [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:16-23, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39] (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:85`; source S060). Read-only scope: no package, reboot, or service clearance follows, and no host pressure conclusion is drawn.

## R18-FRESHNESS — oom-event-plane line 85 zswap-off premise (2026-10-20)

Appended 2026-10-20 by the tsukuroi round-18 L1 (NoticeOom seat); earlier bytes unchanged. The parenthetical "zswap is off" in the `zspages` row at line 85 describes the 2026-10-14 event-A dump and stays dated; it is superseded as a current-use fact only. Now: zswap enabled Y, max_pool_percent 25, compressor zstd [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:8-15] (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:12`; max_pool_percent and compressor at lines 13-14; source S060). Read-only scope: no package, reboot, or service clearance follows, and no host pressure conclusion is drawn.

## R18-FRESHNESS — oom-event-plane line 348 zswap row (2026-10-20)

Appended 2026-10-20 by the tsukuroi round-18 L1 (NoticeOom seat); earlier bytes unchanged. The swap-plane row's statement `zswap.enabled=0` (sysfs and cmdline) describes 2026-10-14 and stays dated. Its "enable zswap" action is superseded as current-use guidance only, because zswap is already enabled on 2026-10-20. Now: zswap.enabled=1 zswap.max_pool_percent=25 on the kernel cmdline [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:8-15] (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:9`; sysfs Y/25/zstd at lines 12-14; source S060). Read-only scope: no package, reboot, or service clearance follows, and no host pressure conclusion is drawn.

## R18-FRESHNESS — oom-event-plane line 384 zswap Q4 premise (2026-10-20)

Appended 2026-10-20 by the tsukuroi round-18 L1 (NoticeOom seat); earlier bytes unchanged. The Q4 premise that zswap is off (sysfs `N` and cmdline) is dated to 2026-10-14 and is superseded as a current-use fact only; the zspages figure is not re-measured here. Now: zswap.enabled=1 on the kernel cmdline [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:8-15] (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:9`; source S060). Read-only scope: no package, reboot, or service clearance follows, and no host pressure conclusion is drawn.


## R18-PRECISION — guard conclusion scope

The NoticeOom-02 supersession includes the current-use reading of the adjacent line281 ('Nothing was configured to act before the kernel'), not only its quoted line280. At S060 observation earlyoom was active since09:57:11 and currently enabled; the date of enablement itself was not captured. This later configured guard does not establish whether it was present before either historical kill, whether it acted, or current systemd-oomd state. Historical event reconstruction remains historical.

## R25 current-use notice (2026-10-22)

Append-only; the lines above stay as written. Line 344 is contradicted on two points by `corpus/knowledge/memory-pressure-r25.md` (rows MP4 and MP5; sources S121 to S124). First, `ManagedOOMMemoryPressure=auto` and `ManagedOOMSwap=auto` are the systemd defaults, not a setting someone made, and `auto` means systemd-oomd "will not actively use this cgroup's data for monitoring and detection" (systemd v262 `systemd.resource-control(5)`); on the round-25 capture every unit up to `-.slice` is `auto`, so an enabled systemd-oomd would have monitored none of them, and the inference that it "would likely have acted before the kernel" does not follow. Second, the 90 percent swap rule needs memory use and swap use both above the limit (`oomd.conf(5)`), not swap alone. Line 301 is narrowed by row MP2: the PSI `total` is stall time in microseconds that only grows within one boot, so a dated reading needs two reads in the same boot. Line 347 (`MemoryPressureWatch=`) stands; it has no kill semantics. The earlyoom statements were already superseded in round 18; earlyoom 1.9.0-1 is active and enabled on 2026-10-22 (`.ufo/waves/round-25/capture/capture-earlyoom.txt`).

R25 precision after wave-2 review (CritC2Supersession, CritC2Learning): the swap point above narrows line 344's wording rather than contradicting it, because event A was a global OOM where memory use was very likely above the limit as well; only the `auto` point refutes the line's conclusion. Line 344's suggested action `systemctl enable --now systemd-oomd` would by itself monitor nothing on these units, because they are `auto`; any change stays operator-owned. Line 274 is narrowed by rows MP2, MP3 and MP6 (stall counters and kill counters are separate readings), and line 301 is deepened by rows MP1 and MP2, not refuted. The same superseded claim in `kill-event-deep-r8.md` line 255 carries its own R25 notice.

## Correction (round 29) — kernel OOM victim selection

[obs] Linux v7.2 `mm/oom_kill.c` has no ordered band walk. `oom_badness()` returns rss plus
`MM_SWAPENTS` plus page-table pages plus `oom_score_adj * (totalpages / 1000)` (lines 228-233),
with `totalpages = totalram_pages() + total_swap_pages` for a global OOM (line 263), and
`oom_evaluate_task()` keeps the single largest value over every eligible task (line 340);
`select_bad_process()` is a plain walk of that test (lines 359-377). `proc.rst` 3.1 states the
adjustment is added to the badness score before the kill decision (line 1777). The argmax has
three bypasses: `oom_task_origin()` forces `LONG_MAX` (lines 334-337), `task_will_free_mem(current)`
selects the allocating task before the walk (line 1122), and `oom_kill_allocating_task` kills
current instead of scanning (lines 1145-1151). [obs] Totals: live `/proc/meminfo` reads MemTotal
31,721,800 kB and SwapTotal 31,722,876 kB = 60.5 GiB, while event A's dump records SwapTotal
35,917,176 kB (swapfile plus 4 GiB zram) = 64.5 GiB. The integer term `totalpages / 1000` is
15,861 live and 16,909 at event A, so +200 is worth 3,172,200 points (12.1 GiB) now and 3,381,800
(12.9 GiB) then; +300 is 18.15 GiB now. [obs] Event A's victim held 6,968,424 rss + 7,110,160
swapents = 14,078,584 pages (53.7 GiB) = 888 points before any adjustment (833 on event A's
totalpages), against 301 for the best +300 helper: the +200 credit was roughly a quarter of its
raw points and did not decide the kill. [inf] §2.3's conclusion — the dominant anonymous-memory
holder died, returning the budget — survives unchanged; only the band wording above is wrong.

[R29-OWED-O01] verdict: corrected | original: "exactly the band the kernel scans first" | now: No band is scanned: oom_badness scores every eligible task as resident pages plus swap entries plus page-table pages plus oom_score_adj times totalpages over 1000, and select_bad_process keeps the single highest value; +200 adds 3,381,800 points, about 12.9 GiB, at event A's 64.5 GiB RAM plus swap, or 3,172,200 points, 12.1 GiB, at the live 60.5 GiB, and the 53.7 GiB victim wins either way. | basis: S149 (mm/oom_kill.c lines 228-233, 263, 340, 359-377) and S148 (/proc/<pid>/oom_score_adj, lines 1777-1789)

[R29-OWED-O02] verdict: corrected | original: "the +200 band is chosen first" | now: The killer walks each task once and retains the maximum points, so no adjustment band is ordered at all; the +200 credit is 3.17 million points live, about 12.1 GiB, against the victim's own 14.08 million points from 53.7 GiB of footprint, so the adjustment was roughly a quarter of the evidence and not the reason for the pick. | basis: S149 (mm/oom_kill.c lines 228-233, 340, 359-377) and S148 (/proc/<pid>/oom_score_adj, lines 1777-1789)
