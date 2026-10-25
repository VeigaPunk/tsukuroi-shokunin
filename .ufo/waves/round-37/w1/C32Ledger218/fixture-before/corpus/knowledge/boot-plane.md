# Boot plane — duration shape, failed-unit history, boot-critical chains (TSUKUROI-R4-3)

source: live read-only probes — `systemd-analyze` (`time`/`blame`/`critical-chain`, default and
`--fuzz=0`), `journalctl` (`--list-boots`, per-boot `-o json` censuses, `-k`), `systemctl`
(`show` / `is-system-running` / `--failed` both scopes), `getfacl`, `/proc/meminfo`,
`/sys/fs/cgroup` counter reads — host `plazir27`, kernel `7.2.3-arch1-3`, user `vgpnk`
(uid 1000, groups `vgpnk docker input wheel`), non-root, **no sudo**;
verified-at: 2026-10-14 13:19–13:31 -0300; every count is a capture (host is live — a coredump
storm and a user-session restart ran during this probe).
recheck: Appendix command set. Entry counts are `-o json | jq` counts, never raw lines.

Notation: **[observed]** measured · **[inference]** · **[unknown]** · **BLOCKED** = privilege-gated
probe (none fired this round — every probe answered; `dmesg`/`/boot` BLOCKED arms are round-3's,
not re-run). Scope: this note is the round-4 boot-plane deep-dive; it re-verifies the duration
rule and **supersedes only the failed-unit-history claim** of `journal-boot-plane.md` §4 (§5 errata).

## 0. Probe context (all read-only)

- Boot 0 id `d7f0bc8d938e4249b4a1f250cbfacf58`; kernel boot 2026-10-13 10:57:58 (`uptime -s`);
  uptime 1 day 2 h 21 m at 13:19; retention unchanged from round 3: **13 boots**
  (`journalctl --list-boots --no-pager` = header + 13 rows, first 2026-10-03 17:42:07), 181.3 M
  on disk. Journal readable non-root via the `group:wheel:r-x` ACL on `/var/log/journal`
  (`getfacl` re-checked 13:26).
- No system mutation verb was run: no `pacman` install/upgrade/remove, no `systemctl start|stop|
  restart|reload|kill`, no `journalctl --rotate|--vacuum*`, no `sudo`. Scratch `/tmp/w4-s4-3-scratch/`.
- Environment is live and shared: the journal shows a concurrent lane's probe at 13:19:54
  (`sudo[1213816] … PWD=/tmp/w4-s41 … COMMAND=/usr/bin/true`) — not this lane's; counts drift.

## 1. Boot duration shape

### 1.1 Current boot (`systemd-analyze`, 13:19)

`18.234s (firmware) + 5.479s (loader) + 4min 3.328s (kernel) + 3.736s (userspace) = 4min 30.778s`;
`graphical.target reached after 3.736s in userspace.` (rc=0). This is the same boot round 3
captured ~1 h 40 m earlier; the figures are byte-identical — boot-time facts, not live state.

### 1.2 The 13 retained boots

Per boot: `Startup finished` line (systemd[1]), journal first-record monotonic, and wall session
span (`--list-boots` first→last; session ≈ uptime minus the pre-journald head). Δ = first-record
monotonic − kernel phase (§1.3).

| idx | boot id | session span (first→last, −03) | session dur | userspace | kernel phase | first rec mono | Δ s |
|---|---|---|---|---|---|---|---|
| −12 | `b2d2184f` | 2026-10-03 17:42:07 → 17:42:11 | 4.0 s | 1.807 s total (no breakdown) | n/a | 165.068 | n/a |
| −11 | `3b970ff9` | 2026-10-03 17:48:24 → 19:08:35 | 1 h 20 m 11 s | 3.582 s | 113.512 s | 114.337 | +0.825 |
| −10 | `c5f37237` | 2026-10-03 19:09:41 → 2026-10-04 20:02:24 | 24 h 52 m 43 s | 3.145 s | 35.189 s | 36.024 | +0.835 |
| −9 | `02f244ce` | 2026-10-04 22:01:14 → 22:05:26 | 4 m 12 s | 3.175 s | 25.104 s | 25.938 | +0.834 |
| −8 | `7a203f61` | 2026-10-05 01:08:08 → 2026-10-06 18:20:46 | 41 h 12 m 38 s | 3.171 s | **2 h 57 m 56.876 s** | 10677.706 | +0.830 |
| −7 | `e08954ce` | 2026-10-06 18:26:29 → 18:47:45 | 21 m 16 s | 3.171 s | 14.941 s | 15.778 | +0.837 |
| −6 | `7ebbaa31` | 2026-10-06 20:21:24 → 2026-10-09 13:34:03 | 65 h 12 m 39 s | 3.148 s | **1 h 28 m 30.454 s** | 5311.270 | +0.816 |
| −5 | `d5daa438` | 2026-10-09 15:17:42 → 2026-10-10 08:50:32 | 17 h 32 m 50 s | 3.194 s | **1 h 43 m 6.782 s** | 6187.621 | +0.839 |
| −4 | `dfa341ec` | 2026-10-10 11:48:32 → 12:39:11 | 50 m 39 s | 3.200 s | **2 h 57 m 27.702 s** | 10648.539 | +0.837 |
| −3 | `69e11ec8` | 2026-10-10 12:39:55 → 2026-10-11 04:42:29 | 16 h 2 m 34 s | 3.142 s | 12.061 s | 12.893 | +0.832 |
| −2 | `2d8f74c5` | 2026-10-11 07:23:31 → 19:00:08 | 11 h 36 m 37 s | 3.228 s | **26 m 55.902 s** | 1616.717 | +0.815 |
| −1 | `73a8e2fc` | 2026-10-11 19:02:51 → 2026-10-13 10:57:30 | 39 h 54 m 39 s | 4.732 s | 20.821 s | 21.631 | +0.810 |
| 0 | `d7f0bc8d` | 2026-10-13 11:02:03 → 2026-10-14 13:19:04 (live) | 26 h 17 m 1 s | 3.736 s | **4 m 3.328 s** | 244.159 | +0.831 |

- **Kernel phase is bimodal** [observed]: 12.061 s … 113.512 s on six boots, 26 m – 2 h 58 m on
  five, boot 0 = 4 m. Userspace is stable (3.142–4.732 s, 12/12 with a breakdown); firmware
  16.897–48.513 s; loader 4.974–10.488 s.
- Session-life shape [observed]: 4 s (installer-media boot −12) up to **65 h 12 m** (−6); nothing
  in between is constrained.
- −12 is atypical: only ~3.3 s of monotonic records retained and no phase breakdown — installer
  media; its row is not used for shape.

### 1.3 Independent rules (re-measured this round)

- **Kernel phase = first-record monotonic − 0.810…0.839 s** (12/12 boots with a breakdown) —
  reproduces round-3's rule from independent reads. Method note: parse the `(kernel)` segment
  explicitly — the total segment (`= 1min 4.907s` on boot −10) collides with a naive `min` regex.
- boot 0 wall-clock anchor: `uptime -s` 10:57:58 → first record 11:02:03 = 245 s wall vs
  244.159 s monotonic ⇒ the two clocks agree within 1 s; the kernel phase is real elapsed time.

### 1.4 Bounds

- firmware/loader phases exist only inside each boot's recorded `Startup finished` line;
  `systemd-analyze` answers for the running boot only ⇒ history here = Startup lines + first/last
  record bounds. Retention wall: nothing older than boot −12; effective journald retention not
  derived (round-3 open item).

## 2. Failed-unit history across the 13 boots

### 2.1 Method (and the case trap)

Two sweeps: (1) per-boot JSON at P≤4, pattern `(?i)failed to start|entered failed state|failed
with result|start request repeated|dependency failed`; (2) whole-retention, **all priorities**:
`journalctl -g '[Ff]ailed with result|entered failed state|Start request repeated|[Ff]ailed to
start' -o json` → **exactly 4 records** (§2.2). Round-3's "zero" came from a lowercase
`failed with result` pattern — systemd capitalizes `Failed with result` — and `Failed to enqueue`
was outside its set (§5 errata). Third stream: PID1-only census (`_PID=1`, all priorities,
`(?i)failed|killed|killing`, rfkill keyword false positives excluded) → per boot: −12:1, −11:5,
−10…−7:0, −6:5, −5:5, −4:5, −3…−2:0, −1:4, 0:4. Classes: §2.3–2.4.

### 2.2 The four unit-failure records (complete within the sweeps)

| when (local −03) | boot | unit | record | scope |
|---|---|---|---|---|
| 2026-10-11 16:14:34 | −2 | `elephant.service` | `Failed with result 'exit-code'` (logged by user manager pid 1582) | user |
| 2026-10-13 10:57:28 | −1 | `app-com.onepassword.OnePassword@autostart.service` | `Failed with result 'core-dump'` (pid 1585) | user |
| 2026-10-13 23:44:31 | 0 | `app-Hyprland-xdg-terminal-exec-…scope` | `Failed with result 'oom-kill'` (pid 1573) | user |
| 2026-10-14 13:10:59 | 0 | **`user@1000.service`** | `Failed with result 'signal'` (logged by PID 1) | **system** |

- The −1 record sits **2 s before that boot's last journal entry** (10:57:30) — teardown-time app
  crash, not a boot failure. The scope record is the cgroup of the 23:44:30 python3 OOM kill (§2.4).
- No `Failed to start` / `entered failed state` / `Start request repeated` record exists anywhere in
  the retention (sweep 2) ⇒ **zero boot-path start failures**; the failure history is session-side
  plus one system-scope service (`user@1000.service`).

### 2.3 Shutdown-race class (failure-worded, not unit failures)

- 24 × PID1 `Failed to enqueue SYSTEMD_WANTS job, ignoring: … destructive` in the last 1–2 s of
  boots −11 (19:08:34), −6 (13:34:02), −5 (08:50:30), −4 (12:39:10) and −1 (10:57:28). [inference]
  shutdown/udev race, deliberately ignored jobs — benign; [unknown] why only these boots.
- 1 × boot −12 `Failed unmounting /var/log.` (installer-media shutdown).
- Boots −10, −9, −8, −7, −3, −2 have zero PID1 failure-word lines (quiet shutdowns).

### 2.4 The 2026-10-14 13:10:59 event (boot 0) — session churn + OOM-notice lag

Sequence (`journalctl -b 0 --since 13:10:40 --until 13:11:15`), all at 13:10:59:
1. session 1 closes (sddm-helper PAM close; `session-1.scope: Deactivated successfully`), sddm
   restarts its greeter — uid 964 (`sddm`) gets its own user manager;
2. `user@1000.service: Main process exited, code=killed, status=9/KILL` → `Failed with result
   'signal'` → consumed `1d 11h 3min 1.574s CPU over 1d 2h 8min 53.364s wall clock time, 28.5G
   memory peak, 34.2G memory swap peak`;
3. PID1 P5: `user-1000.slice: The kernel OOM killer killed some processes in this unit.`;
4. 13:11:07 new manager starts (logind sessions 4 user + 5 manager; `Startup finished in 67ms`).

OOM attribution evidence:

- The whole journal contains **1** kernel OOM kill: python3 at 2026-10-13 23:44:30
  (`task_memcg=…/app-Hyprland-…scope`, `anon-rss:27873696kB`); boot 0 kernel `oom|killed` sweep =
  5 lines, all that second. Nothing at 13:10:59.
- `/sys/fs/cgroup/user.slice/user-1000.slice/memory.events` (read 13:26): `oom_kill 1`; the slice
  existed continuously across both timestamps (manager wall clock 1d 2 h 8 m) ⇒ the single
  increment is the 23:44:30 kill ⇒ **[inference]** the 13:10:59 slice notice is a *late report* of
  that kill (PID1 surfaces the slice counter at unit stop), not a new OOM kill.
- [unknown] the SIGKILL source: no `Stopping User Manager…` line (no controlled stop), no kernel
  kill log, and the cgroup counter rules out a kernel OOM kill (unit ships `TimeoutStopSec=120s`,
  `KillMode=mixed` — a stop-path escalation would not land in the same second either). Recorded
  for operator audit; not absorbed.
- Side artifact [inference]: 8 × `systemd-xdg-autostart-generator: Failed to create unit file …:
  File exists` at 13:11:07.32 (≤300 ms after manager start) — regeneration race on restart, not
  unit failures.

### 2.5 Current-state arms

`systemctl --failed` (system and user) → `0 loaded units listed`; `is-system-running` → `running`
(also `--wait`); `user@1000.service` active, `Result=success`, `NRestarts=0`, `Restart=no` ⇒ the
failure is historical only. **"0 loaded units listed" ≠ "no failure history"** — the history holds
4 records + the shutdown class above.

### 2.6 Bounds of the negative claims

- Sweep 2 is wording-bounded (standard systemd failure phrasings); a unit dying with other wording
  would not be caught. Crossing evidence: PID1 census classes (all accounted), cgroup OOM counter,
  kernel OOM line count.
- Per-boot JSON sweep capped at P≤4; sweep 2 lifts the priority cap for the decisive phrasings only.

## 3. Boot-critical chain shapes

### 3.1 The chain (current boot, 13:19)

```
graphical.target @3.736s
└─sddm.service @3.736s
  └─plymouth-quit.service @3.539s +195ms
    └─systemd-user-sessions.service @3.519s +19ms
      └─network.target @3.518s
        └─iwd.service @3.474s +43ms
          └─basic.target @3.471s
            └─dbus-broker.service @3.464s +6ms
              └─dbus.socket @3.461s +6us
                └─sysinit.target @3.461s
                  └─systemd-update-done.service @3.442s +18ms
                    └─ldconfig.service @3.335s +107ms
                      └─systemd-tmpfiles-setup.service @2.872s +461ms
                        └─systemd-journal-flush.service @2.849s +21ms
                          └─var-log.mount @2.845s +3ms
                            └─dev-mapper-root.device @803ms +1.157s
```

16 units; `--fuzz=0` produced a **byte-identical** output (diff empty) ⇒ no sub-fuzz link is
hidden; this is the complete chain. Shape: the only >1 s element is the LUKS-mapped root device
(1.157 s); the tmpfiles→ldconfig tail adds 0.57 s; all 16 chain units are `active` with
`Result=success`, `NRestarts=0` (`systemctl show` on the chain).

### 3.2 `systemd-analyze blame` — top is not the boot path

111 units listed. Top: `man-db.service` 3.371 s — timer-triggered, ran 2026-10-14 03:50:48–52
inside boot 0 (`Starting Daily man-db regeneration…`, consumed 3.371 s wall), currently inactive;
`TriggeredBy=man-db.timer` ⇒ blame mixes boot-time and post-boot units — intersect with
`critical-chain` before calling anything a boot cost. Chain-relevant blame: root device 1.157 s,
tmpfiles-setup 461 ms, ldconfig 107 ms; non-chain boot activity: tmpfiles-setup-dev-early 1.026 s,
systemd-userdbd 1.015 s, plocate-updatedb 830 ms (timer).

### 3.3 Reachability across boots

`Reached target Graphical Interface` = exactly 1 line in every retained boot (13/13, sweep);
every boot has its `systemd[1]: Startup finished` line (13/13). Message census: **27**
`Startup finished` lines = 13 system + 14 user managers (11 boots with 1 manager, boot −12 with
0, boot 0 with 3 because of the 13:10:59 churn). User-manager startup is 57–81 ms (observed range).

### 3.4 Bounds

No historical `critical-chain` (systemd-analyze answers for the running boot only); cross-boot
chain evidence = Startup lines + reach counts + failure history (§2).

## 4. Triage rows (round-4 axis: mechanism → blast radius → action)

| finding | mechanism (measured / blocked) | blast radius | action |
|---|---|---|---|
| kernel-phase dwell 12 s → 2 h 58 m (boot 0: 4 m 3 s) | [inference] pre-userspace dwell (initramfs/LUKS prompt); `/etc/crypttab` BLOCKED shape-only (round-3) | every boot's wall duration; unbounded wait if unattended | operator probe: crypttab/keyfile audit (mechanism blocked read-only) |
| `user@1000` SIGKILL 13:10:59 | [unknown] out-of-band SIGKILL; kernel OOM ruled out (counter), controlled stop ruled out (no `Stopping` line) | whole user session (all session units); 1 observed teardown, 8 s session gap, no persistent damage | operator: audit shell history/auditd around 13:10:59 on 2026-10-14 |
| OOM history (python3 27.8 G at 23:44:30; slice peak 28.5 G / swap peak 34.2 G) | kernel OOM kill measured; cgroup `oom_kill 1` | memory-pressure class; user manager near-limit | owning lane (crash/OOM root cause); this plane reports state only |

## 5. Errata (append-only)

- [2026-10-14 S4-3] **Cross-note correction, `journal-boot-plane.md` §4** ("zero unit-activation
  failures in 13 retained boots"): re-measurement with case-insensitive patterns finds 4 failure
  records (§2.2). Root cause of the round-3 miss: its strict pattern `failed with result` is
  lowercase while systemd logs `Failed with result`; its broad set also excluded `Failed to
  enqueue`. That note is not edited (append-only discipline) — this note supersedes the claim.
  Its §5 duration table and Δ rule re-verified here unchanged.
- [2026-10-14 S4-3] **Own first-pass method error**: `jq '.[]…'` on `journalctl -o json` output
  without `-s` treats json-lines as a stream of strings — every line errored `Cannot index string
  with string`; use `jq -s`. Kept as method evidence.
- [2026-10-14 S4-3] **OOM notices are P5 (notice)** and a slice-level notice can lag its kill by
  hours (23:44:30 kill → slice notice 13:10:59, §2.4) — count OOM events from the kernel log /
  `memory.events`, never from PID1 notices (3 notices, 1 kill).
- [2026-10-14 S4-3] PID1 keyword censuses need an rfkill exclusion — `Load/Save RF Kill Switch
  Status` matches `kill`.

## 6. Unknowns (open)

- SIGKILL source at 2026-10-14 13:10:59 (not resolvable from the journal; operator audit needed).
- systemd's exact trigger/lag semantics for slice-level OOM notices (observed behavior only).
- Why the enqueue-destructive shutdown race fires only on 5 of the reboot boots.
- Pre-userspace dwell mechanism (unchanged from round-3; leading hypothesis initramfs/LUKS).
- Effective journald retention beyond the 13 retained boots.
- Whether failures exist outside the measured wording set (§2.6).

## 7. Sources

- Commands as embedded, with capture times; full set in the Appendix.
- Files read: `/etc/systemd/logind.conf` (only `HandlePowerKey=ignore` uncommented);
  `/usr/lib/systemd/system/user@.service` (TimeoutStopSec=120s, KillMode=mixed,
  OOMScoreAdjust=100, `WantedBy=session-4.scope`); `/sys/fs/cgroup/user.slice/user-1000.slice/`
  `{memory.events,memory.peak,memory.current,memory.swap.current}`; `/proc/meminfo`;
  `getfacl -p /var/log/journal`; `systemctl show` property sets as quoted.
- Cross-refs: `journal-boot-plane.md` (boot-gap rule §5.3, timers, BLOCKED arms),
  `systemd-user-plane.md` (user units / coredumps), `driver-firmware-plane.md` (kernel ring
  classes), `update-safety-note.md`.
- Scratch (ephemeral, `/tmp/w4-s4-3-scratch/`): `context.txt`, `analyze.txt`, `chain.txt`,
  `c_default.txt`, `c_zero.txt`, `perboot.tsv`, `b*.warnp.json`, `b*.bounds.json`,
  `strict_matches2.txt`, `pid1_fail.txt`, `broad_classes.txt`, `window.txt`, `startup_lines.txt`,
  `user1000.txt`, `mem.txt`.

## Appendix — probe command set (reproducible)

```bash
date '+%F %T %z'; date -u '+%F %T UTC'; hostname; uname -r; id; uptime -s; uptime -p
journalctl --list-boots --no-pager; journalctl --disk-usage
systemctl is-system-running; systemctl is-system-running --wait
systemctl --failed --no-pager; systemctl --user --failed --no-pager
systemd-analyze; systemd-analyze blame --no-pager
systemd-analyze critical-chain --no-pager; systemd-analyze critical-chain --fuzz=0 --no-pager
# per-boot sweep (n = -12..0):
journalctl -b $n -p warning -o json --output-fields=PRIORITY,MESSAGE,_PID,SYSLOG_IDENTIFIER,__REALTIME_TIMESTAMP --no-pager > b$n.warnp.json
jq -s '[.[]|select((.MESSAGE|tostring)|test("(?i)failed to start|entered failed state|failed with result|start request repeated|dependency failed"))]|length' b$n.warnp.json
journalctl -b $n _PID=1 -o json --output-fields=PRIORITY,MESSAGE --no-pager | jq -s '[.[]|select((.MESSAGE|tostring)|test("(?i)failed|killed|killing"))|select((.MESSAGE|tostring)|test("RF Kill";"i")|not)]|length'
journalctl -b $n -o json --output-fields=__MONOTONIC_TIMESTAMP,__REALTIME_TIMESTAMP --no-pager | sed -n '1p;$p'
journalctl -b $n -g 'Startup finished' -o short-monotonic --no-pager
journalctl -b $n -g 'Reached target Graphical Interface' -o cat --no-pager | wc -l
# all-priority decisive sweep + OOM census:
journalctl --no-pager -g '[Ff]ailed with result|entered failed state|Start request repeated|[Ff]ailed to start' -o json --output-fields=PRIORITY,MESSAGE,_PID,__REALTIME_TIMESTAMP,SYSLOG_IDENTIFIER
journalctl -k --no-pager -g 'Out of memory: Killed process' -o json | jq -s 'length'
journalctl --no-pager -g 'OOM killer killed some processes' -o json --output-fields=PRIORITY,MESSAGE,_BOOT_ID,__REALTIME_TIMESTAMP
cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.events
systemctl show user@1000.service -p Result -p NRestarts -p Restart -p TimeoutStopUSec -p KillMode -p ActiveEnterTimestamp -p InactiveEnterTimestamp
systemctl cat user@.service; loginctl list-sessions --no-pager; loginctl list-users --no-pager
getfacl -p /var/log/journal
```

## Recheck receipt — bounded probes (2026-10-14 13:34–13:36 -0300)

No probe in this note hung; re-verified under explicit `timeout 30` wrappers, all rc=0 (no 124):

| probe | bounded result | wall |
|---|---|---|
| `timeout 30 journalctl --list-boots --no-pager \| wc -l` | 13 boot rows | 0.004 s |
| `timeout 30 journalctl -b -8 -o json --output-fields=__MONOTONIC_TIMESTAMP,__REALTIME_TIMESTAMP` | 10677.705892 → 159036.059279 s (longest session) | 0.108 s |
| `timeout 30 journalctl -b 0 -p warning -o json \| wc -l` (biggest boot) | 10 344 entries (10 149 at 13:22 — live drift, §0) | 0.104 s |
| `timeout 30 journalctl -g '<decisive pattern>' -o json \| wc -l` | 4 — matches §2.2 | 0.210 s |
| `timeout 30 systemd-analyze critical-chain --fuzz=0 --no-pager` | chain tail `var-log.mount → dev-mapper-root.device` | 0.138 s |
| `timeout 30 systemctl show user@1000.service -p Result -p NRestarts -p ActiveState` | `active` / `success` / `0` | 0.002 s |

Journal reads on this host are sub-second even for the largest retained boot and the longest
session; nothing was privilege-blocked. The warn-count drift (10 149 → 10 344 in ~12 min)
re-confirms the capture-not-constant rule (§0).

## 8. Errata (round 4)

- 2026-10-14 (TSUKUROI-ERR-S sweep) — **drifted anchor in the §5 recheck table.** The row
  `timeout 30 journalctl --list-boots --no-pager | wc -l` reports "13 boot rows"; the command
  counts **lines**, and live re-measure gives **14** (header + 13 boot rows). This note's own §0
  states the 14-line shape correctly — the recheck table conflated the row count with the `wc -l`
  output. Corrected reading: `wc -l` → 14 lines = 13 boot rows. [observed: `journalctl
  --list-boots --no-pager | wc -l` → 14, round-4]
- 2026-10-14 — **round-4 note not yet in the corpus index:** `corpus/README.md`'s coverage map has
  no row for this note (nor for `degraded-triage-r4.md`). Out of this lane's write scope — flagged
  for the index owner. [observation]

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — `systemd-analyze`, `journalctl`, `systemctl`, `getfacl`, `/proc/meminfo` and cgroup counter probes on host `plazir27`, 2026-10-14.
verified-at: 2026-10-14 (the original boot-plane capture window recorded in this note).
recheck: 30d; procedure: Appendix command set; preserve the `-o json | jq` entry-count convention.
supersedes the pointer-only recheck: line above.
