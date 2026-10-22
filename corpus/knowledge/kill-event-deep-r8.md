# Kill-event plane deepened — the 13:10:59 SIGKILL's causal picture readable non-root (TSUKUROI-R8-S8-2)

source: live read-only probes on host `plazir27` — `journalctl` (boot list, text windows, `-o json`
field-level extraction), `/proc` (`vmstat`, `meminfo`, `pressure/memory`, per-PID `stat`/`oom_score_adj`/
`cgroup`), cgroupfs under `/sys/fs/cgroup`, `systemctl show/cat`, local unit files and man pages; user `vgpnk`
(uid 1000), non-root, no `sudo`. Kernel `7.2.3-arch1-3`; systemd `261.2-1-arch`; boot 0 id
`d7f0bc8d938e4249b4a1f250cbfacf58` (journal boot start 2026-10-13 11:02:03 -03; `uptime -s` reads 10:57:58 —
the ~4 min difference is a suspend-accounting detail, §11.1).
verified-at: **2026-10-14 16:11:54–16:25 -03** (UTC−3). Every count carries its command; the host is live and
counters drift — §5 values are capture-time.
recheck: §11 probe ledger; every negative claim carries its sweep.
Substrate contract: nothing written to the host — journal, cgroup, `/proc`, unit files read-only; the only
writability check is `test -w` (no write); no install/upgrade/remove; no service started, stopped or
restarted; `sudo` never used; `dmesg` stays **BLOCKED** (`dmesg_restrict`=1, not escalated). Scratch
`/tmp/w8-s82-tsukuroi/` (ephemeral).
Deepens: `corpus/knowledge/oom-event-plane.md` (round 6, md5 `7e99d712ead088727c0980e52a121199`, 433 `wc -l`) —
its event B (§3), counter anomaly (§4.2), memory picture (§5), victim list (§6.2), prevention table (§7),
detection contract (§8), H1–H3 (§3.5), Q2/Q3. **Errata against that file are proposed rows here (§9), never
applied to it**; this lane writes only this file.
Notation: **[observed]** · **[inference]** · **[unknown]** · **BLOCKED**. Event A = 2026-10-13 23:44:30 kernel
OOM (victim `python3`); **event B** = 2026-10-14 13:10:59 SIGKILL class. All times host-local (-03). "Message
#n" = the n-th `kernel OOM killer killed some processes` record in the boot (#1, #2 at event A; #3 at event
B). Text renderings are `_SOURCE_REALTIME_TIMESTAMP`; JSON figures are `__REALTIME_TIMESTAMP` — at event B
they agree to within 2 µs, at event A they differ by 39–58 ms (journald receipt delay under the dump; §11.3).

## 1. What this capture settles (headline)

| F | finding | evidence |
|---|---|---|
| F1 | **No kernel OOM kill happened at event B.** Since boot `/proc/vmstat` reads `oom_kill 1`; event A is the only kernel kill in the retained journal (exactly 1 `Out of memory: Killed process` line; **0** `Memory cgroup out of memory` lines in 13 boots). The 13:10:59 second contains no kernel record of any OOM/kill class. | §2, §3.4, §7 |
| F2 | **Message #3 is teardown-coincident, not kill-coincident**: it follows `user@1000.service: Consumed …` by **0.45 ms** (`.400149` → `.400593`, JSON µs) and repeats a counter value event A set. | §2.2, §3.3 |
| F3 | **Counter map**: kernel `memory.events` non-zero only at `user.slice` and `user-1000.slice` (each `oom_kill 1`; `.local` **0** at both); systemd's own `OOMKills=` property: `user-1000.slice` 1, `user.slice` 0, current `user@1000.service` 0. No counter anywhere reads 2, and no live descendant carries the slice's 1. | §3.4 |
| F4 | **Complete uid-1000 population turnover**: zero vgpnk processes survive from before 13:10:59; earliest live start is 13:11:07 (157 procs at capture). The session-command chain exited *before* the manager died; the app purge follows mechanically from `KillMode=mixed` unit teardown. | §6.2 |
| F5 | **Event B's pre-kill memory picture is not retained**: every surviving memory signal is a lifetime maximum or a cumulative counter; the 34.2 GiB swap peak cannot be dated to 13:10:59 and is consistent with event A's documented saturation. | §5 |
| F6 | **Launch-count trap (measured)**: app scopes here leave **no deactivation record** — 0 `app-*.scope: Deactivated` lines in boot 0, in boot −1, and 0 against 98 starts in the current session. "Started app-…scope" counts launches, never live units. | §6.3 |
| F7 | **The OOM-score class argues against a kernel kill**: the session ran at +200/+300, the manager at +100; what died was the +100 manager, not a +200 big-RSS app. | §4 |
| F8 | Prevention table refined with this picture; new rows for the capture gap and the kernel-kill ledger. | §8 |

## 2. The 13:10:59 sequence, re-measured

### 2.1 The window (13:10:35–13:11:20; 1136 journal lines, 128 of them kernel)

| time (-03) | writer | event |
|---|---|---|
| 13:10:42.2008 | kernel | 3 `[UFW BLOCK]` records (LAN discovery chatter — ambient) |
| 13:10:49.257175 | systemd-coredump | LOVE `SIGABRT` (process 1201250, `liblove-11.5.so` backtrace), core processed by .318715 |
| 13:10:59.345266 | xdg-desktop-portal-hyprland[1920] | last journal record ever emitted from inside the old session (`Got interface: ext_foreign_toplevel_image_capture`) |
| 13:10:59.346180 | sddm-helper[1567] | `[PAM] Closing session` — an *orderly* close path, not a mid-flight death |
| 13:10:59.347555 | sddm-helper[1567] | `pam_unix(sddm-autologin:session): session closed for user vgpnk` |
| 13:10:59.352586 | sddm-helper[1567] | `[PAM] Ended.` |
| 13:10:59.360829 | systemd[1] | `session-1.scope: Deactivated successfully.` (the session scope is empty before the manager dies) |
| 13:10:59.361095 | sddm[1562] | `Auth: sddm-helper exited with 9` (see §6.1 on the semantics of "9") |
| 13:10:59.361672/.361935 | systemd-logind | `Session 1 logged out…` / `Removed session 1.` |
| 13:10:59.3636–.3657 | sddm[1562] | display removed, new display added, `Greeter starting...` |
| 13:10:59.3743–.3790 | sddm-helper[1203049], logind | greeter PAM session (user `sddm`, uid 964) opened; `New session 'c1'` (class greeter) |
| 13:10:59.380873 | systemd[1] | `user@1000.service: Main process exited, code=killed, status=9/KILL` |
| 13:10:59.381136 | systemd-logind | `Removed session 2.` (vgpnk's manager-early session) |
| 13:10:59.381949 | systemd[1] | `user@1000.service: Failed with result 'signal'.` |
| 13:10:59.400143 | systemd[1] | `Consumed 1d 11h 3min 1.574s CPU time … 28.5G memory peak, 34.2G memory swap peak.` |
| 13:10:59.400591 | systemd[1] | `user-1000.slice: The kernel OOM killer killed some processes in this unit.` (message #3) |
| 13:10:59.4035/.4041 | systemd[1] | `/run/user/964` runtime dir; `Starting User Manager for UID 964...` |
| 13:11:00–.4847 | sddm stack | greeter compositor boots (`start-hyprland`, `/usr/share/sddm/hyprland.conf`); `Greeter session started successfully` |
| 13:11:07.283287 | sddm-greeter[1203129] | `Message received from greeter: Login` — session `omarchy.desktop`, command `uwsm start -g -1 -e -D Hyprland hyprland.desktop`, **PAM service `sddm`** (a greeter-driven login; the old session's PAM line was `sddm-autologin`) |
| 13:11:07.301682/.302198 | logind / systemd[1] | `New session '4' of user 'vgpnk'`; `Starting User Manager for UID 1000...` (fresh instance) |
| 13:11:07.325957 | generator | 8 × `File exists` for generator units — the surviving `/run/user/1000` still held the old session's generator output |
| 13:11:07.408647 | kernel | `Hyprland[1203102]: segfault … in libaquamarine.so.0.15.0` — the **greeter's** compositor, adjacent noise |
| 13:11:07.746767–.747021 | logind | `Session c1 logged out` / `Removed session c1.` |
| 13:11:17.998029 | logind | `Removed session 3.`; `Stopping/Stopped User Manager for UID 964` (13:11:17) |

**Kernel classification of the window** [observed]: 115 records carry the `sr0` optical-drive identifiers
(the round-4 E3 burst class, third occurrence), 7 are `[UFW BLOCK]`, and 6 others are 4 `scsi_io_completion_action
/ blk_print_req_error … callbacks suppressed` notices and the greeter-Hyprland segfault pair. The **only**
OOM/kill-family string in the whole window is message #3 itself (`grep -icE 'oom|out of memory'` = 1).

### 2.2 Last record per writer, 13:10:00–13:11:00 [observed]

15 distinct writers; the session-side writers stop in this order: `systemd[1573]` (the old manager) last
wrote at 13:10:34.599853; `xdg-desktop-portal-hyprland[1920]` at 13:10:59.345266; `sddm-helper[1567]` at
13:10:59.352592; then only system-side writers (sddm, logind, PID 1, the greeter chain). No session process
emits anything after 13:10:59.345. The old manager's own last words are `Started
app-org.chromium.Chromium-1198710.scope.` — no error, no warning, no stop request.

## 3. Which cgroup — measured answers

### 3.1 The message's own fields (JSON, all three records)

| # | source time | `_PID` / comm | `_SYSTEMD_CGROUP` (writer) | `UNIT` (subject) | `_SYSTEMD_UNIT` (writer's own unit) |
|---|---|---|---|---|---|
| 1 | 23:44:30.574948 | 1573 `systemd --user` | `/user.slice/user-1000.slice/user@1000.service/init.scope` | **(field absent)** — subject is the scope, named in the message text | `user@1000.service` |
| 2 | 23:44:30.576028 | 1 `systemd` | `/init.scope` | `user@1000.service` | `init.scope` |
| 3 | **13:10:59.400591** | 1 `systemd` | `/init.scope` | **`user-1000.slice`** | `init.scope` |

The `UNIT` field is set only on PID 1's records; the user manager's own message (#1) carries its subject
only in the text (`app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope: …`) and shows its *sender's* unit as
`_SYSTEMD_UNIT` — the two fields answer different questions and are read apart here. [observed]

All three carry `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`; the local catalog (`/usr/lib/systemd/catalog/
systemd.catalog`) renders it: *"A process of @UNIT@ unit has been killed by the OOM killer."* — i.e. a report
*about the named unit*, not itself evidence of when a kill happened. [observed]

### 3.2 The cgroup paths the killed processes actually lived in [observed]

- the old user manager (PID 1573): `/user.slice/user-1000.slice/user@1000.service/init.scope` — its own
  `_SYSTEMD_CGROUP` field; the unit file sets `Delegate=pids memory cpu` and `DelegateSubgroup=init.scope`,
  and today's instance (`MainPID` 1203171) sits in the same path.
- `sddm-helper[1567]`: `/user.slice/user-1000.slice/session-1.scope` (a **direct child of the slice**, not of
  `user@1000.service`); sessions are siblings of the service, `app-*` scopes are not.
- the event-A victim (`python3`, pid 1732581): `task_memcg=/user.slice/user-1000.slice/user@1000.service/
  app.slice/app-graphical.slice/app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope` (kernel line, global OOM).

### 3.3 What "this unit" meant at event B [observed + inference]

The slice was named, not the service. The old service cgroup (and its whole subtree) ceased to exist at
13:10:59 and was re-created at 13:11:07; today `user-1000.slice/` contains only `session-4.scope` and the new
`user@1000.service/` (`app.slice`, `background.slice`, …), and no old scope name survives in cgroupfs.
[inference] the kill happened inside the old `user@1000.service` subtree, and message #3 named the *slice*
because that is the unit systemd read the counter from — 0.45 ms after the service's resource line, i.e.
during teardown, ~19.7 ms after the manager's death.

### 3.4 The counter map (this capture; 96 `memory.events` files swept) [observed]

| object | kernel `memory.events` | kernel `.local` | systemd `OOMKills=` | reads |
|---|---|---|---|---|
| `user.slice` | `oom_kill 1`, `oom_group_kill 0`, `sock_throttled 67558` | all 0 | **0** | one charge, highest ancestor |
| `user-1000.slice` | `oom_kill 1`, `sock_throttled 67558` | all 0 | **1** | the charge survives here |
| `user@1000.service` (new) | `oom_kill 0`, `sock_throttled 3320` | — | 0 | fresh cgroup, counts from zero |
| `session-4.scope`, sampled `app-*` scopes | 0 | 0 | 0 | nothing |
| `/proc/vmstat` | `oom_kill 1` (whole boot) | — | — | the kernel's own ledger |

No second charge exists anywhere, and no *live* descendant of the slice is non-zero — yet the slice's
hierarchical file reads 1 while `.local` reads 0. [inference] the file behaves as **stored state**: the
event-A charge was propagated up at event time and survived the later removal of the subtree that produced
it (a read-time live-descendant aggregate would read 0). This narrows round 6's Q2 (§4.2 there) without
closing the kernel-internals question.

## 4. The OOM score class (measured on the live host)

| band | who carries it (measured) |
|---|---|
| **+300** | 7 × `chromium` in `app-Hyprland-chromium-44e683fd.scope` |
| **+200** | 143 uid-1000 processes: every sampled session-side process — `Hyprland[1203316]`, `uwsm-app` (defunct), `uwsm aux app-daemon[1203477]`, scope members (`waybar`, `swaybg`, …) |
| **+100** | exactly 2: the user manager `systemd[1203171]` and its `(sd-pam)[1203173]` — `user@.service` sets `OOMScoreAdjust=100`; `man systemd.exec` documents the default as "the OOM score adjustment level of the service manager itself" |
| **0** | 502 root processes incl. PID 1; `sh`/`systemctl` in `session-4.scope`; `sddm-helper` (0) |
| **−250 / −900 / −1000** | `systemd-journald` / `dbus-broker` ×2 / `systemd-udevd` — exactly the extremes event A's dump listed (round 6 §2.3: −1000×1, −900×2, −250×1), i.e. those are system defaults, not event artifacts |

[observed] the killed process was the **+100 user manager**, in a session whose apps all sat at +200/+300.
[inference] under a kernel OOM the scan prefers the higher-scored, larger-RSS tasks first; a kernel pick of
the manager while +200 Chromium clients existed contradicts the class picture — one more argument against
H1. The **origin of the +200 band is [unknown]**: `grep -rn "OOMScore|oom_score"` over `/usr/bin/uwsm`,
`/usr/lib/uwsm/`, `/usr/share/uwsm/` and the generated units under `/run/user/1000/systemd/user/` found
nothing, and a sampled scope exposes no `OOMScoreAdjust` property; the measured shape is inheritance down
the session chain (the session command's children all carry +200).

## 5. The memory picture *before* event B — what exists and what does not

### 5.1 The dating problem (the key refinement) [observed + inference]

`memory.peak` / `memory.swap.peak` are **lifetime maxima** of the cgroup, not pressure snapshots — round 6
flagged the *space* dimension of this (§4.4: peaks include page cache) but not the *time* dimension:

- `user-1000.slice` exists since 2026-10-13 11:02:05, so its numbers span event A *and* event B.
- The old service's death line ("28.5G memory peak, 34.2G memory swap peak") covers the *whole old session*
  (26 h), event A included. Event A's own dump shows the swap plane at **99.9999 %** full
  (`Free swap` 44 kB of 35,917,176 kB); the slice's swap peak reads 36,744,949,760 B = 99.907 % of
  `SwapTotal`. The peak is therefore *consistent with event A's documented moment* and **cannot be assigned
  to 13:10:59** [unknown].
- The discriminator: the *new* service (3.2 h old) has `memory.swap.peak` = **3,171,446,784 B** and
  `memory.swap.events fail` = **4** — the current session never approaches the old profile, and the slice's
  `fail` counter sits at 5,922,849, **identical to round 6's 14:42 reading** (no growth in ~1.6 h).
  [inference] the extreme swap counters are old-epoch; nothing dates them to the kill.

### 5.2 What a non-root seat can read about "before the kill" (capture-time values)

| signal | value now | dated to the kill? |
|---|---|---|
| slice `memory.peak` | 30,699,745,280 B | lifetime max — **no** |
| slice `memory.swap.peak` | 36,744,949,760 B (99.907 % of swap) | lifetime max — **no** |
| slice `memory.swap.events fail` | 5,922,849 (unchanged since 14:42) | cumulative — no |
| slice `sock_throttled` | 67,558 (unchanged since 14:42) | cumulative — no |
| slice PSI `some/full` total | 37,041,770 / 36,105,580 µs (since Oct-13 11:02) | cumulative — no |
| `/proc/vmstat` pswpin/pswpout | 72,335,126 / 94,080,361 pages (Δ +233,373 / +307,784 ≈ +912 MiB / +1.20 GiB vs round 6's 14:42 capture) | cumulative — no |
| `/proc/meminfo` | MemTotal 31,721,780 kB; MemAvailable 19,860,508; Shmem 6,935,596; SwapFree 34,818,408 | live only — no |
| slice `memory.stat` | anon 2,699,935,744 · file 22,687,072,256 · slab 1,181,659,992 (page-cache-dominated, as round 6 §4.4) | live only — no |
| tmpfs | `/tmp` 16 G, 6.8 G used (45 %); `/dev/shm` 65 M | live only — no |
| the things *at* the kill second | the 6 Chromium scope launches (13:08:45.18 → 13:10:34.60, PIDs 1161990/1190456/1192514/1194175/1198002/1198710), the LOVE `SIGABRT` (13:10:49), the sr0 burst (13:10:59.4046) | **yes** — but none of them is a memory measurement |

An oddity recorded rather than interpreted: slice `inactive_anon` (7,328,153,600 B) exceeds slice `anon`
(2,699,935,744 B) — internally odd for a live session; a candidate explanation is charge reparenting from
the destroyed old hierarchy (kernel-internals; [unknown]).

[observed] probe inventory for a *pre-kill* picture: `sar`/`atop`/`dool`/`dstat` absent, `/var/log/sa`
absent, `systemd-cgtop` present but live-only, PSI files live-only, `dmesg` **BLOCKED**. **There is no
non-root-readable instantaneous memory snapshot of the seconds before event B, and none can be backfilled.**

## 6. Victim list, deepened

### 6.1 Provable deaths [observed]

- `user@1000.service` main process = the old user manager (PID 1573, the writer of messages #1) —
  `code=killed, status=9/KILL`; this is the boot's **only** `status=9/KILL|code=killed|status=137` line
  (sweep count 1; round 6's ledger §11.6 reported 2 — recorded as a discrepancy, not smoothed).
- `sddm-helper[1567]` — sddm logged `Auth: sddm-helper exited with 9`. **[unknown]** whether the printed 9
  is a signal number or an exit code: the normal form is `Auth: sddm-helper exited successfully` /
  `Greeter stopped. SDDM::Auth::HELPER_SUCCESS` (measured at 13:11:07), so "with 9" is the abnormal branch,
  but the log text alone does not settle it, and the helper had just executed an orderly `[PAM] Closing
  session` → `[PAM] Ended.` sequence. Round 6's §6.2 read it as SIGKILL; this note downgrades that to
  [inference, not settled] and rests nothing on it.
- sessions: 1 (removed .361935), 2 (manager-early, .381136), 3 (manager-early of sddm, 13:11:17.998),
  c1 (greeter, 13:11:07.747); sessions 4/5 (vgpnk user + manager) created 13:11:07.30x. `session-1.scope`
  deactivated at .360829 — i.e. the graphical session scope was **empty before** the manager was killed.

### 6.2 The purge, measured [observed]

Zero uid-1000 processes survive from before 13:10:59: the earliest live uid-1000 process start is
**13:11:07** (pid 1203171, the new manager; 157 uid-1000 processes at capture). Method: `/proc/<pid>/stat`
`starttime` ticks + `/proc/uptime` base; the method self-validates to the second against the journal's own
`Starting User Manager for UID 1000... 13:11:07.302198`. The old cgroup subtrees are absent from cgroupfs.

[inference] the mechanism is two-staged: the session-command chain (`uwsm start … hyprland.desktop` under
sddm's helper) exited first and the session scope emptied at .360829; the manager died at ~.3808; then
systemd's `KillMode=mixed` unit teardown SIGKILLs the remaining cgroup members — which purges every app
scope. An external "kill the whole cgroup" would also fit the survivor data; the helper's *orderly* PAM
path argues against "every process of the user was signalled at once".

### 6.3 The launch-vs-live trap (new, and it changes what the journal can say) [observed]

The old manager started **69 distinct `app-*.scope` units** (50 chromium, 5 typora, 4 grok-bot, 3 obsidian,
2 zcode, 2 r5-electron, 1 kaidoku-r4-electron, 1 kaidoku-probe, 1 onepassword) and logged **zero**
deactivations — but that is not an inventory of survivors: the current session reproduces the pattern
exactly (98 distinct app scopes started since 13:11:07, **0** `app-*.scope: Deactivated successfully`), and
boot −1 shows 0 as well. Sampled scopes carry `CollectMode=inactive-or-failed` [inference: the likely reason
the record is absent]. **Consequence:** the journal cannot say which units (let alone processes) were alive
at 13:10:59; the per-process victim list stays structurally unrecoverable (round 6's Q3), now with the
*measured* reason: no deactivation records, cgroups destroyed, SIGKILL leaves no coredump.

Corollary on cadence: the pre-kill "6 Chromium scopes in 110 s" is not anomalous — the fleet's *current*
launch rate is of the same order (98 distinct scopes at 16:20 → 106 at 16:24, ≈2/min). The rate is a load
fact, not a symptom of the kill.

## 7. H1–H3, updated

| H | round 6 status | what this capture adds |
|---|---|---|
| **H1** kernel OOM path ran, print lost | no read-only discriminator | [strongly disfavoured] the kernel-kill ledger reads 1 (event A) and never moved; there is **no** kernel OOM-family print in the boot beyond event A; 0 `Memory cgroup out of memory` prints in 13 boots; and with `memory.max`/`memory.high`/`memory.swap.max`/`memory.zswap.max` all `max` and `oom.group` 0 on the path, the memcg *limit* trigger is closed — the only kernel path reachable is global exhaustion, which prints a dump and counts (event A did both). The residual H1 needs print **and** counter **and** dump lost at once, with no positive evidence. |
| **H2** non-kernel SIGKILL; systemd's line from its own bookkeeping | supported | counters agree: nothing was charged at 13:10:59; the message's timing is teardown-coincident (F2). The *sender* is still [unknown] — candidates with measured provenance: an external user/session kill (no orderly stop anywhere in the journal), PID 1's stop path (**no** `Stopping User Manager for UID 1000` line exists — the boot's only two such lines are UID 964 at 13:11:17 — and no `user-runtime-dir@1000` stop; `KillMode=mixed` would have sent SIGTERM to the main process first), or a session component (`/usr/lib/uwsm/signal-handler.sh` stops the *envelope unit* via `systemctl --user stop` — orderly, not a manager SIGKILL). |
| **H3** message #3 is a deferred/aggregated report of the Oct-13 wave | counter value 1 vs 2 | **strengthened**: the surviving slice charge is exactly event A's (F3), no live descendant carries it, and #3 fires 0.45 ms after the old service's resource line — a stored counter read at teardown, not a new kill. *Why* systemd read the slice then (its watch/re-read model) remains [unknown]. |

## 8. Prevention options — refined with the measured picture

Rows 1–10 are round 6's table restated against this capture (operator-owned; nothing here was changed);
rows 11–12 are new.

| # | lever | measured current state (this capture) | mechanism vs event B / A | tsukuroi detection |
|---|---|---|---|---|
| 1 | `systemd-oomd` | unit + socket present, `is-active` inactive, `is-enabled` **disabled**; binary `/usr/lib/systemd/systemd-oomd` (same 261.2-1-arch build); `/etc/systemd/oomd.conf` contains only `[OOM]` (all defaults: `SwapUsedLimit=` 90 %, `DefaultMemoryPressureLimit=` 60 %, `DefaultMemoryPressureDurationSec=` 30 s — local `oomd.conf(5)`); `oomctl` fails (`Could not activate remote peer 'org.freedesktop.oom1'`); the unit runs `OOMScoreAdjust=-900` and gates on `/proc/pressure/*` (PSI present); `ManagedOOMSwap=auto` **and** `ManagedOOMMemoryPressure=auto` are already set on `user-1000.slice`, `user@1000.service` and sampled app scopes; `ManagedOOMPreference=none`, `ManagedOOMMemoryPressureLimit=0` (=default) | [inference] the swap rule (90 %) is below event A's measured 99.9999 % saturation, so oomd would have had a trigger; it acts by killing the *eligible descendant cgroup* rather than one task — policy kills before the kernel needs to act | presence/`is-enabled`; `ManagedOOM*` property read |
| 2 | `earlyoom` | `command -v earlyoom` → absent | alternative monitor | command check |
| 3 | per-unit guards | `memory.max`/`memory.high` = `max`, `memory.swap.max` = `max`, `memory.oom.group` 0, `memory.zswap.max` = `max` at every level of the live path — **no guard anywhere**. Writability (`test -w`, nothing written): `app.slice/memory.max` **writable by uid 1000**, `user@1000.service/memory.max` and slice root-only | [inference] a non-root guard can only bound *app scopes* (per-app), never the session as a whole — relevant because event B killed the session, not one app. `OOMPolicy`: service `continue`, app scopes `stop` (a kill inside an app scope stops that scope; inside the service it does not fail the unit) | read `memory.max/high` per unit; report `max` as "no guard" |
| 4 | `MemoryPressureWatch=` | `user@.service` pinned **skip** (unit file); slice and `session-4.scope` read `auto`; only local drop-in on the service is `faster-shutdown.conf` (`TimeoutStopSec=5s`) | a cooperating-app lever, not a guard | property read |
| 5 | swap capacity | `/swap/swapfile` 32,484,229,120 B (30.25 GiB) prio 0, used 30 MiB; `/dev/zram0` 4 GiB prio 100, used ~1.0 GiB; `zswap.enabled=0` (sysfs `N` + cmdline); `swappiness` 60; zram `mm_stat`: orig 1,041,842,176 B, `mem_used_max` 1,518,989,312 B | both kill waves end at the swap plane (A: 99.9999 % measured; B: [unknown — undatable, §5.1]) | `swapon --show`, `memory.swap.peak`, `swap.events.fail` |
| 6 | `oom_score_adj` steering | session at +200, Chromium children +300, manager +100, system defenders −250/−900/−1000 (§4). Scope units expose no `OOMScoreAdjust` property, so per-scope steering must come from the launcher; the +200 origin is [unknown] | the +200 band is scanned first; a known-huge batch job placed differently changes who dies — but this event killed the *manager*, which no +200 client shared a band with | kernel dump's adj column; live `/proc/*/oom_score_adj` |
| 7 | tmpfs discipline | `/tmp` 16 G, 6.8 G used (45 %); `/dev/shm` 65 M; `Shmem` 6,935,596 kB | `/tmp` content is memory that competes with anon | `df -h /tmp`, `meminfo Shmem` |
| 8 | kernel diagnostics | `oom_dump_tasks`=1, `panic_on_oom`=0, `overcommit_memory`=0, `swappiness`=60, `dmesg_restrict`=1 (**dmesg BLOCKED** — the journal is the only non-root kernel window) | dumps enabled → §7's H1 argument; `panic_on_oom=1` would be catastrophic here (event A was a global OOM) | `/proc/sys/vm/*` |
| 9 | stop-time behaviour | `KillMode=mixed` (unit) + `TimeoutStopSec=5s` drop-in | explains the *purge* shape of event B (remaining cgroup members SIGKILLed at teardown), not its trigger | unit/drop-in read |
| 10 | detection design | counters are presence flags, never event counts; the journal messages are the event list | **new anchors**: `/proc/vmstat` `oom_kill` as the kernel-kill ledger (1 at capture, non-root), systemd's `OOMKills=` property, and the launch-vs-live trap for scope counting (§6.3) | §8 rows above |
| 11 | **pre-kill capture (new)** | no `sar`/`atop`/`dool`/`dstat`, no `/var/log/sa`; `systemd-cgtop` exists but live-only; PSI live-only | event B's "before" picture exists nowhere; without an operator-installed capture (cgtop/PSI logging or a full monitor) no future event's pre-kill picture will exist either, and the victim list stays unrecoverable | detection-of-the-gap itself: report the missing capture capability as a standing row |
| 12 | **oomd kill selection (new)** | `ManagedOOMPreference=none` everywhere sampled; oomd never ran | if oomd is enabled, `ManagedOOMPreference=avoid/omit` on selected units (e.g. the user session vs batch agents) is the steering knob — measured as available, not configured | property read |

## 9. Proposed errata for `oom-event-plane.md` (append-only; owner applies)

- **E4 (round 6 §3.2/§5).** The "swap footprint had reached ≈99.9 %" reading uses lifetime maxima; they
  cannot be dated to 13:10:59 and are consistent with event A. Rewrite as "at some point in the slice's
  life swap reached 99.907 %; the most extreme *dated* swap moment in retention is event A's dump
  (99.9999 %)".
- **E5 (round 6 §4.2).** The surviving `oom_kill 1` at `user.slice`/`user-1000.slice` is event A's charge:
  counters behave as *stored* state (propagated at event time, surviving subtree removal); `.local` stays 0
  at ancestors; no live descendant is non-zero; systemd's `OOMKills=` mirrors it at `user-1000.slice` (1)
  but not at `user.slice` (0). Q2 is narrowed, not closed.
- **E6 (round 6 §3.5).** H1 loses its last support: `/proc/vmstat oom_kill` = 1 (event A), 0 memcg-OOM
  prints in 13 boots, no limits on the path. H2/H3 carried; the *sender* of the SIGKILL remains unknown.
- **E7 (round 6 §1/§6.2).** `Auth: sddm-helper exited with 9`: signal-vs-exit-code unproven; only the
  manager's `status=9/KILL` is explicit. Also: round 6's ledger §11.6 reports a 2-line `status=9` sweep;
  this capture's exact pattern yields **1**.
- **E8 (round 6 §1/§3.4).** `Started app-…scope` counts are launches, never live units — no app scope in
  boot 0 (or boot −1) has a deactivation record, and the 6-launch pre-kill burst is the fleet's normal
  cadence order, not an anomaly.

## 10. Open questions

| Q | question | what would settle it |
|---|---|---|
| Q8 | `/proc/vmstat` `oom_kill` semantics: per task or per event, and does it cover memcg-limit OOM kills? | kernel source/docs; no local doc exists (man-pages carry no vmstat field text; the linux package ships no Documentation) |
| Q9 | Who sent the SIGKILL to PID 1573 (and the helper's "9")? | root/audit (`auditd` state not measured) or a controlled test — out of province |
| Q10 | systemd's message trigger: why was the *slice* messaged at 13:10:59 and not at 23:44:30? | systemd source/cgroup-watch internals |
| Q11 | Scope-launch cadence: 69 launches/26 h in the old session vs ≈2/min at capture — cause? | workload attribution (fleet lanes vs chromium automation); launcher identity still unproven (round 6's Q6) |
| Q12 | Origin of the session-wide +200 `oom_score_adj` (not in uwsm text files) | launcher/session source or a controlled launch trace |
| — | carried unchanged: round 6's Q1–Q7, incl. the sr0 burst (3rd occurrence, 13:10:59.4046 / 13:11:07.4356) and the greeter's `libaquamarine` segfault (boot 0 has 13 segfaults, 1 libaquamarine) | as round 6 lists them |

## 11. Probe ledger (spot-check anchors)

All read-only, non-root; host-local times, 2026-10-14; scratch `/tmp/w8-s82-tsukuroi/`.

1. 16:11:54 `date -Is`; `uptime -s` (10:57:58); `/proc/sys/kernel/random/boot_id` (d7f0bc8d…);
   `journalctl --list-boots` (13 boots; boot 0 2026-10-13 11:02:03); `git rev-parse HEAD` `aa136d69…`,
   `git status --short` 0 lines. **Convention note:** `uptime -s` and the journal's boot start differ by
   ~4 min (suspend accounting); `/proc/<pid>/stat` `starttime` ticks were converted against the `uptime`
   base and validated against the journal (manager start 13:11:07.302198) to the second.
2. 16:12 `grep oom`/page fields `/proc/vmstat` (`oom_kill 1`; pswpin 72,335,126; pswpout 94,080,361;
   pgmajfault 26,277,375); `meminfo`; `/proc/pressure/memory` (some total 70,921,611 µs);
   `/proc/swaps`, `swapon --show`, zram `mm_stat`, `/sys/module/zswap/parameters/enabled` (N), `/proc/cmdline`.
3. 16:13–16:16 artifact pins (md5 + `wc -l`): `oom-event-plane.md` `7e99d712…` 433;
   `round-8.plan.md` `0bef822d…` 216 (Read shows 217 — unterminated final line); `SKILL.md` `b2b0f6a7…` 983;
   `tools/tsukuroi-census.sh` `e2c4558a…` 1472; `update-safety-v2.md` `92803aea…` 353.
4. 16:14 cgroup tree `ls -la` for `user.slice/user-1000.slice[/user@1000.service[/app.slice]]`; 96-file
   `memory.events` sweep (non-zero only the two slices); full reads of slice/user.slice `memory.events`
   and slice `.local`; root `memory.events` absent (`No such file`).
5. 16:14 JSON extraction of the 3 OOM attribution messages with `UNIT`, `_SYSTEMD_CGROUP`, `_PID`, `_COMM`,
   `MESSAGE_ID`, and both timestamp fields (`_SOURCE_REALTIME_TIMESTAMP` vs `__REALTIME_TIMESTAMP`); catalog
   lookup of `fe6faa94e7774663a0da52717891d8ef`; `journalctl --catalog` render.
6. 16:15 window dump 13:10:35–13:11:20 (1136 lines) and its classification (128 kernel: 115 sr0, 7 UFW,
   6 other; 1 'oom' string = message #3); writer table (15 writers; last records §2.2).
7. 16:16 `_PID=1573` inventory: 1177 journal lines; last line 13:10:34.599853; 69 distinct `Started
   app-*.scope`, 0 deactivations, 0 stop/close of any scope; scope-type histogram; boot −1 control.
8. 16:17–16:23 live-state reads: uid-1000 `oom_score_adj` histogram (200×143, 300×7, 100×2, 0×2) and the
   −1000/−900/−250 identities; `systemctl show` batches (`OOMScoreAdjust`, `KillMode`, `ManagedOOM*`,
   `Memory*`, `OOMPolicy`, `OOMKills`, `MemorySwapPeak`) for `user@1000.service`, `user-1000.slice`,
   `user.slice`, `session-4.scope`, sampled app scopes; `user@.service` unit file + `faster-shutdown.conf`;
   `/etc/systemd/oomd.conf`, `oomd.conf(5)`, `systemd-oomd.service`, `oomctl`, `command -v` for
   earlyoom/sar/atop/dool/dstat; `test -w` ×3; `/proc/sys/vm/*`; `df -h /tmp /dev/shm`; PSI files.
9. 16:18 survivor probe: `starttime` conversion over all uid-1000 `/proc/*/stat` → 0 processes before
   13:10:59; earliest 13:11:07 (pid 1203171); 157 processes; cgroup older subtrees absent.
10. 16:20–16:25 counters re-read: `vmstat oom_kill 1`; slice `memory.swap.events fail 5,922,849`;
    `sock_throttled 67,558`; service `swap.peak` 3,171,446,784 B, `fail 4`; `/proc/vmstat` deltas vs round 6.
11. 16:22 sweeps: kernel `-k` all-boots (`oom` 5 lines, all event A; `Killed process` 1; `Memory cgroup out
    of memory` **0**); journal-wide oom-ish 8; `status=9/KILL|code=killed|status=137` **1**;
    `Started/Deactivated` scope counts old vs current session.
12. 16:23 correction pass: `status=9/KILL` sweep, `vmstat` re-read, `git status` still 0 lines (nothing
    written to the host or to the repo tree by this lane).

## 12. Errata (append-only, this file)

- (none yet — first capture)

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — read-only `journalctl`, `/proc`, cgroupfs, and `systemctl show/cat` probes on host `plazir27`, 2026-10-14.
verified-at: 2026-10-14 (the live event-capture window recorded in this note).
recheck: 30d; procedure: §11 probe ledger; carry each negative claim's sweep.
supersedes the pointer-only recheck: line above.


## R18-FRESHNESS — earlyoom state (2026-10-20)

Historical snapshots preserved: row 2 of §8 above (`command -v earlyoom` → absent, measured 2026-10-14) keeps its original meaning and bytes. This notice supersedes that row for current use only. Read-only scope: nothing here clears a package, reboot, service or boot action.

- Now (2026-10-20 read-only L1 capture): earlyoom is installed (local database `earlyoom-1.9.0-1`), its unit is active and enabled [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:16-23, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39], and `/usr/bin/earlyoom` resolves. Capture: `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:29` (local database entry); also `:17-18` (`active`, `enabled`), `:21-22` (`ActiveEnterTimestamp=Tue 2026-10-20 09:57:11 -03`, `ExecMainPID=1379`), `:85` (`/usr/bin/earlyoom`). Source S060.
- This notice does not date or explain any historical kill event (2026-10-13 or 2026-10-14).

## R18-FRESHNESS — zswap state (2026-10-20)

Historical snapshots preserved: row 5 of §8 above (`zswap.enabled=0` with sysfs `N`, measured 2026-10-14) keeps its original meaning and bytes; the zswap readings of that date describe that capture only. This notice supersedes that clause for current use only. Read-only scope: nothing here clears a package, reboot, service or boot action.

- Now (2026-10-20 read-only L1 capture, kernel `7.2.11-arch1-1`): zswap is enabled (sysfs `Y`, `max_pool_percent` `25`, compressor `zstd`) and the running kernel command line carries `zswap.enabled=1 zswap.max_pool_percent=25` [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:8-15]. Capture: `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:9` (command line), `:12-14` (sysfs values), `:6` (kernel release). Source S060.
- This notice does not date or explain any historical kill event (2026-10-13 or 2026-10-14).

## R18-FRESHNESS — sar and sa-log state (2026-10-20)

Historical snapshots preserved: row 11 of §8 above (no `sar` and no `/var/log/sa`, measured 2026-10-14) keeps its original meaning and bytes. This notice supersedes that row for current use only. Read-only scope: nothing here clears a package, reboot, service or boot action.

- Now (2026-10-20 read-only L1 capture): sar is present at `/usr/bin/sar` (sysstat-12.8.0-1), `/var/log/sa` exists and lists no entries, so no retained sar data is present there; atop, dool and dstat were not found. Capture: `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:84` (`/usr/bin/sar`), `:87-88` (`ls -1 /var/log/sa`, empty listing, `rc=0`), `:38` (`sysstat-12.8.0-1`), `:82-86` (command probe). Source S060.
- This notice does not date, explain or attribute any historical kill event (2026-10-13 or 2026-10-14). An empty `/var/log/sa` listing does not show whether sar collected data before those events, and the capture does not read sysstat timers or configuration.


## R18-FRESHNESS — sibling current-use restatements (2026-10-20)

Sources S060, S051 and S052. This appended correction supersedes the current-use readings listed below and every repeated current-use restatement of the same premise in this file. Historical measurements remain intact. No package, service, rebuild, boot or rollback action is authorized.

- R18-FRESH-SUPPLEMENT-11: prior locus `[observed] probe inventory for a *pre-kill* picture: `sar`/`atop`/`dool`/`dstat` absent, `/var/log/sa``. Now: sar now resolves to/usr/bin/sar; the captured /var/log/sa listing is empty. This does not backfill a pre-kill historical measurement; other tools in the old list were not re-audited for integrity. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:84.


## R25 current-use notice (2026-10-22)

Append-only; the table above stays as written. Row 1 at line 255 says `ManagedOOMMemoryPressure=` and `ManagedOOMSwap=` are already set and that systemd-oomd would have had a trigger. That conclusion is contradicted by `corpus/knowledge/memory-pressure-r25.md` row MP4 (sources S121, S122, S123): `auto` is the systemd default, and systemd-oomd "will not actively use this cgroup's data for monitoring and detection" (systemd v262 `systemd.resource-control(5)`); only `kill` on the unit or an ancestor makes a cgroup a candidate. On the round-25 capture the four read units, up to `-.slice`, are all `auto`. The three default values in the same cell stand (row MP5 confirms them), but the 90 percent swap rule needs memory use and swap use both above the limit. Row 12 at line 266 (`ManagedOOMPreference=` as the steering knob) is narrowed the same way: preference only matters for cgroups systemd-oomd monitors, which needs `kill`. Row 2 (earlyoom absent) was already superseded in round 18; earlyoom 1.9.0-1 is active and enabled on 2026-10-22 (`.ufo/waves/round-25/capture/capture-earlyoom.txt`).
