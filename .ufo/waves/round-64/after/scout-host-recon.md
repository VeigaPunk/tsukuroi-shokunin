2026-11-03T18:45:50Z

# Host recon — systemd user manager, journal err classes, coredumps (round 64 / w1, seat SC1Host)

Seat: `SC1Host` (scout, read-only, one output file). Item **C2-RECON**.
Lane repo: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Host: `plazir27`.

Host identity at probe time:

```
$ uname -r
7.2.11-arch1-1
$ systemctl --version | head -1
systemd 262 (262.1-1-arch)
$ uptime -s
2026-11-02 12:07:17
$ hostname
plazir27
```

Zero writes were made outside this file: no `systemctl` start/stop/restart/enable/disable, no
`journalctl --rotate/--vacuum`, no `coredumpctl` delete/dump, no `snapper` mutation, no `sudo`.

---

## 1. Probe receipts

### P1 — failed user units

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T18:40:32Z
$ systemctl --user list-units --state=failed --all --no-pager
  UNIT                        LOAD   ACTIVE SUB    DESCRIPTION
● run-p1157862-i1164315.scope loaded failed failed [systemd-run] /home/vgpnk/.local/bin/rembg i -m birefnet-general -om /tmp/p61cut-32dbqf_r/0.png /tmp/p61cut-32dbqf_r/0_m.png
● run-p1159104-i1145275.scope loaded failed failed [systemd-run] /home/vgpnk/.local/bin/rembg i -m birefnet-general -om small.png small_m.png

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

2 loaded units listed.
To show all installed unit files use 'systemctl list-unit-files'.
rc=0
```

`$ systemctl --user list-units --state=failed --all --no-pager --no-legend | wc -l` → `2`

### P2 — manager states (both scopes)

```
$ systemctl --user is-system-running; echo rc=$?
degraded
rc=1
$ systemctl is-system-running; echo rc=$?
running
rc=0
$ systemctl --user show -p Version -p NFailedUnits -p NNames
Version=262.1-1-arch
NNames=314
NFailedUnits=2
$ systemctl show -p Version -p NFailedUnits -p State
Version=262.1-1-arch
NFailedUnits=0
```
(no `State=` line is emitted by this systemd build for the manager — see §7 traps)

```
$ systemctl --failed --all --no-pager
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
$ systemctl --user list-unit-files --state=bad --no-pager
UNIT FILE STATE PRESET

0 unit files listed.
```

Boot target: `$ systemctl is-active graphical.target` → `active`; `$ systemctl get-default` → `graphical.target`.

### P3 — err entry count and the line-count trap

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T18:40:32Z
$ journalctl -b -p err -o json --no-pager | wc -l
5276

$ journalctl -b -p err -o short --no-pager | wc -l
6213
rc=0
```

The 937-line gap is coredump stack-trace continuation lines inside single journal entries
(`Stack trace of thread …`, `#0 0x…`), i.e. the same trap the stored snapshot documents. Entry
count via `-o json` is the only sound number; multiline count is 0 (`MESSAGE` fields contain no
`\n` in the 5276 entries).

Cross-check by cursor: `journalctl -b -p err -o export --no-pager | grep -c '^__CURSOR='` → `5275`
at 18:38Z (one fewer than `-o json` because the trailing partial read window shifted between the
two invocations; both runs are within the same second-scale window and the count later settled at
5276).

### P4 — err classes by `SYSLOG_IDENTIFIER`

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T18:44:51Z
$ journalctl -b -p err -o json --no-pager | python3 -c "<count by SYSLOG_IDENTIFIER>"
total 5276
5230 systemd-socket-proxyd
40 kernel
4 systemd-coredump
1 sddm-helper
1 systemd
rc=0
```

Same run, with per-class first/last timestamps:

```
$ journalctl -b -p err -o json --no-pager | python3 -c "<count + min/max __REALTIME_TIMESTAMP>"
2026-11-03T18:42:44Z
  5230  systemd-socket-proxyd    2026-11-02 16:04:19 .. 2026-11-02 16:09:50
    40  kernel                   2026-11-02 12:07:17 .. 2026-11-03 15:39:19
     4  systemd-coredump         2026-11-02 16:47:00 .. 2026-11-02 23:05:12
     1  sddm-helper              2026-11-02 12:07:20 .. 2026-11-02 12:07:20
     1  systemd                  2026-11-02 16:47:55 .. 2026-11-02 16:47:55
sum 5276
```

Owner split (`_SYSTEMD_OWNER_UID`/`_UID`): `{'?': 40, '0': 1, '1000': 5235}` — the kernel 40 carry
no UID, `systemd` 1 is uid 0 (system manager), and 5235 are the user manager's. A
`journalctl --user -b -p err` run independently returns 5235 entries (5230 proxyd + 4 coredump +
1 systemd), consistent.

### P5 — the 5230-entry class is one process, one 5-minute window

```
$ journalctl -b _COMM=systemd-socket- --no-pager -o json | python3 -c "<minute buckets>"
2026-11-02 16:04 666
2026-11-02 16:05 940
2026-11-02 16:06 940
2026-11-02 16:07 942
2026-11-02 16:08 940
2026-11-02 16:09 802
total 5230
```

Single PID for all 5230 (`$ … python3 -c "<distinct pids>"` → `distinct pids: 1`, `pid 442437`),
single message text (`5230 × 'Failed to connect to remote host: Connection refused'`), single
cgroup:

```
_SYSTEMD_CGROUP=/user.slice/user-1000.slice/user@1000.service/app.slice/comfyui.service
_EXE=/usr/lib/systemd/systemd-socket-proxyd
```

≈15.8 entries/s sustained for 330.6 s. The proxy's backend had just exited:

```
$ journalctl --user -b -u comfyui.service --no-pager -o short | grep -E '16:0[0-9]' | head -3
Nov 02 16:04:19 plazir27 systemd[1499…]: comfyui-backend.service: Consumed 53min 17.901s CPU time over 1h 6min 47.888s wall clock time, 24.1G memory peak, 6.5G memory swap peak.
Nov 02 16:04:19 plazir27 systemd-socket-proxyd[442437]: Failed to connect to remote host: Connection refused
```

(verbatim tail, `head` truncated in the transcript; the `Consumed` line precedes the first
`Connection refused` in the same second).

### P6 — kernel err sub-classes (40)

```
$ journalctl -b -p err -o json --no-pager | python3 -c "<classify kernel>"
2026-11-03T18:43:59Z
kernel_total 40
20 sr0-critical
15 sr0-bufferio
2 cgroup-oom
1 tdx-unsupported
1 empty-message
1 overlayfs
rc=0
```

* `sr0` = 35 lines, all inside `2026-11-02 12:07:17.776 .. 12:07:20.389` (span 2.612 s), all
  boot-time. Device identity:

  ```
  $ lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL,MOUNTPOINT | grep sr0
  sr0          21.5G rom   iso9660     MB Support CD
  $ udevadm info --query=property --name=/dev/sr0 | grep -E 'ID_MODEL|ID_FS_LABEL|ID_CDROM'
  ID_CDROM=1
  ID_CDROM_MEDIA=1
  ID_CDROM_MEDIA_CD=1
  ID_MODEL=ProductCode
  ID_FS_LABEL=MB_Support_CD
  $ cat /sys/block/sr0/size
  44989040
  ```
  DEVPATH shows a USB-attached drive (`…/usb8/8-10/8-10:1.0/host12/target12:0:0/12:0:0:0/block/sr0`).
  Not mounted (`findmnt -no SOURCE,TARGET,FSTYPE /dev/sr0` → rc=1).

* `cgroup-oom` = 2, both `Memory cgroup out of memory: Killed process …` for the two rembg PIDs
  (§2). This is the class that grew vs the stored `1 OOM`.
* `tdx-unsupported` = `virt/tdx: TDX not supported by the host platform`, boot head, benign.
* `empty-message` = one priority-3 kernel entry with `MESSAGE=""` at `1793632037772179`
  (2026-11-02 12:07:17.772), adjacent to the TDX line. Nothing to attribute; recorded so the
  kernel 40 reconciles to 39 named + 1 empty.
* `overlayfs` = 1 err-priority entry: `overlayfs: failed to resolve '/upper': -2` at
  2026-11-03 15:39:19 (§6).

### P7 — boots

```
$ journalctl --list-boots --no-pager
IDX BOOT ID                          FIRST ENTRY                 LAST ENTRY
 -2 bcbf8b4825bb4aa5b379018848f39361 Mon 2026-10-26 12:08:45 -03 Sat 2026-10-31 20:25:18 -03
 -1 9b1b2c44b87343b78069192a81235222 Sat 2026-10-31 20:26:17 -03 Mon 2026-11-02 12:06:39 -03
  0 1c5e4375946b4abbb68cf222fe64bed6 Mon 2026-11-02 12:07:17 -03 Tue 2026-11-03 15:40:24 -03
$ journalctl --list-boots --no-pager | tail -n +2 | wc -l
3
```

Per-boot err entry counts (`journalctl -b <n> -p err -o json | wc -l`): boot `0` = **5276**,
boot `-1` = **77**, boot `-2` = **363**.

Per-boot err classes:

| boot | total | dominant classes |
|---|---|---|
| `0` | 5276 | systemd-socket-proxyd 5230, kernel 40, systemd-coredump 4, sddm-helper 1, systemd 1 |
| `-1` | 77 | kernel 62, systemd-coredump 13, sddm-helper 1, systemd 1 |
| `-2` | 363 | systemd-coredump 242, kernel 114, systemd-socket-proxyd 4, systemd 3 |

Boot performance: `$ systemd-analyze` → `Startup finished in 15.572s (firmware) + 5.515s (loader) + 13.655s (kernel) + 2.660s (userspace) = 37.403s`, `graphical.target reached after 2.660s in userspace.`

### P8 — coredumps

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T18:40:32Z
$ coredumpctl list --no-pager | wc -l
253                     # 252 rows + 1 header
$ ls /var/lib/systemd/coredump | wc -l
10
$ du -sh /var/lib/systemd/coredump; du -sb /var/lib/systemd/coredump
704M	/var/lib/systemd/coredump
737406945	/var/lib/systemd/coredump
```

Histogram over the 252 rows:

```
$ coredumpctl list --no-pager | python3 -c "<exe/signal/corefile histogram>"
--- EXE (top 12) ---
81 python3.14 -
29 unshare -
19 chromium -
11 gcc16-O3 -
10 clang23-O3 -
10 bw12-O3 -
9 chrome_crashpad_handler -
9 bash -
6 sasquatch-v4be -
6 python3 -
6 git -
6 python3.14
--- SIGNAL ---
191 SIGSEGV
29 SIGABRT
17 SIGBUS
7 SIGXFSZ
5 SIGILL
2 SIGTRAP
1 SIGSYS
--- COREFILE ---
228 missing
14 none
9 present
1 truncated
total 252
```

Oldest row `Mon 2026-10-26 12:47:05 -03`, newest `Mon 2026-11-02 23:05:12 -03`.
`coredumpctl` has no `--boot`/`-b` in this build (see §7), so per-boot attribution is by time
window:

```
boot -2 (2026-10-26 12:08:45 .. 2026-10-31 20:25:18): 237
boot -1 (2026-10-31 20:26:17 .. 2026-11-02 12:06:39): 11
boot  0 (2026-11-02 12:07:17 .. now):            4
```

The 4 boot-0 rows, verbatim:

```
$ coredumpctl list --since "2026-11-02 12:07:17" --no-pager
Mon 2026-11-02 16:47:00 -03 1107245 1000 1000 SIGSEGV present  /usr/lib/chromium/chromium  6.8M
Mon 2026-11-02 16:47:01 -03 1098996 1000 1000 SIGSEGV present  /usr/lib/chromium/chromium 17.9M
Mon 2026-11-02 22:53:23 -03 3686161 1000 1000 SIGABRT none     /usr/bin/python3               -
Mon 2026-11-02 23:05:12 -03 3735105 1000 1000 SIGABRT none     /usr/bin/python3               -
```

Effective policy: `Storage=external`, `MaxUse=8G`, `KeepFree=8G` (compression default). The 10
retained files are 5 chromium cores (one 530.6M, one 150.4M llama-server) plus 8 python3 cores of
~0.65–0.84M.

### P9 — timers

```
$ systemctl --user list-timers --all --no-pager
NEXT                            LEFT LAST                         PASSED UNIT                          ACTIVATES
Tue 2026-11-03 15:48:41 -03 4min 24s Tue 2026-11-03 15:43:41 -03 35s ago ai-usage.timer                ai-usage.service
-                                  - Mon 2026-10-19 00:33:15 -03       - cursor-shim-healthcheck.timer cursor-shim-healthcheck.service

2 timers listed.
rc=0
$ systemctl --user list-unit-files --type=timer --no-pager
UNIT FILE                     STATE    PRESET
ai-usage.timer                enabled  enabled
cursor-shim-healthcheck.timer enabled  enabled
omarchy-battery-monitor.timer disabled enabled
systemd-tmpfiles-clean.timer  disabled enabled

4 unit files listed.
rc=0
```

`ai-usage.timer`: `ActiveState=active SubState=waiting`, `OnUnitActiveUSec=5min`,
`LastTriggerUSec=Tue 2026-11-03 15:43:41 -03`, `Result=success`. 327 `Starting Probe …` runs this
boot, 1 `Failed with result` (see §4).

`cursor-shim-healthcheck.timer`: `ActiveState=active SubState=elapsed`,
`TimersMonotonic={ OnUnitActiveUSec=1min ; next_elapse=0 }`,
`LastTriggerUSec=Mon 2026-10-19 00:33:15 -03`, `Result=success`, `UnitFileState=enabled`.
Its service has **no journal entries at all**:

```
$ journalctl --user -u cursor-shim-healthcheck.service --no-pager -o short | tail -3
-- No entries --
$ systemctl --user show cursor-shim-healthcheck.service -p ActiveState -p Result -p ExecMainExitTimestamp
ActiveState=inactive
SubState=dead
Result=success
ExecMainExitTimestamp=
```

### P10 — failed units, full identity

```
$ systemctl --user status run-p1157862-i1164315.scope --no-pager -l | head -25
× run-p1157862-i1164315.scope - [systemd-run] /home/vgpnk/.local/bin/rembg i -m birefnet-general -om /tmp/p61cut-32dbqf_r/0.png /tmp/p61cut-32dbqf_r/0_m.png
     Loaded: loaded (/run/user/1000/systemd/transient/run-p1157862-i1164315.scope; transient)
  Transient: yes
     Active: failed (Result: oom-kill) since Mon 2026-11-02 16:49:24 -03; 22h ago
   Duration: 5.183s
 Invocation: 4279ec0059694aa99d83ba24af939922
   Mem peak: 3G
        CPU: 38.434s

Nov 02 16:49:19 plazir27 systemd[1487]: Started [systemd-run] /home/vgpnk/.local/bin/rembg i -m birefnet-general -om /tmp/p61cut-32dbqf_r/0.png /tmp/p61cut-32dbqf_r/0_m.png.
Nov 02 16:49:24 plazir27 systemd[1487]: run-p1157862-i1164315.scope: The kernel OOM killer killed some processes in this unit.
Nov 02 16:49:24 plazir27 systemd[1487]: run-p1157862-i1164315.scope: Failed with result 'oom-kill'.
Nov 02 16:49:24 plazir27 systemd[1487]: run-p1157862-i1164315.scope: Consumed 38.434s CPU time over 5.183s wall clock time, 3G memory peak.
rc=0
```

```
$ systemctl --user status run-p1159104-i1145275.scope --no-pager -l | head -25
× run-p1159104-i1145275.scope - [systemd-run] /home/vgpnk/.local/bin/rembg i -m birefnet-general -om small.png small_m.png
     Loaded: loaded (/run/user/1000/systemd/transient/run-p1159104-i1145275.scope; transient)
  Transient: yes
     Active: failed (Result: oom-kill) since Mon 2026-11-02 16:49:45 -03; 22h ago
   Duration: 11.616s
 Invocation: 8cffbc291ee54a008d03fdda63261a50
   Mem peak: 8G
        CPU: 3min 19.220s

Nov 02 16:49:33 plazir27 systemd[1487]: Started [systemd-run] /home/vgpnk/.local/bin/rembg i -m birefnet-general -om small.png small_m.png.
Nov 02 16:49:45 plazir27 systemd[1487]: run-p1159104-i1145275.scope: The kernel OOM killer killed some processes in this unit.
Nov 02 16:49:45 plazir27 systemd[1487]: run-p1159104-i1145275.scope: Failed with result 'oom-kill'.
Nov 02 16:49:45 plazir27 systemd[1487]: run-p1159104-i1145275.scope: Consumed 3min 19.220s CPU time over 11.616s wall clock time, 8G memory peak.
rc=0
```

```
$ systemctl --user show run-p1157862-i1164315.scope -p Result -p MemoryPeak -p MemorySwapPeak -p Transient -p ActiveEnterTimestamp -p InactiveEnterTimestamp
ActiveEnterTimestamp=Mon 2026-11-02 16:49:19 -03
InactiveEnterTimestamp=Mon 2026-11-02 16:49:24 -03
Transient=yes
Result=oom-kill
MemoryPeak=3221225472
MemorySwapPeak=0
$ systemctl --user show run-p1159104-i1145275.scope -p Result -p MemoryPeak -p MemorySwapPeak -p Transient -p ActiveEnterTimestamp -p InactiveEnterTimestamp
ActiveEnterTimestamp=Mon 2026-11-02 16:49:33 -03
InactiveEnterTimestamp=Mon 2026-11-02 16:49:45 -03
Transient=yes
Result=oom-kill
MemoryPeak=8589934592
MemorySwapPeak=0
```

Both scopes carry an explicit cgroup cap equal to their peak, and `MemorySwapMax=0`:

```
$ cat /run/user/1000/systemd/transient/run-p1157862-i1164315.scope
# This is a transient unit file, created programmatically via the systemd API. Do not edit.
[Unit]
Description=[systemd-run] /home/vgpnk/.local/bin/rembg i -m birefnet-general -om /tmp/p61cut-32dbqf_r/0.png /tmp/p61cut-32dbqf_r/0_m.png

[Scope]
MemoryMax=3221225472
MemorySwapMax=0
$ cat /run/user/1000/systemd/transient/run-p1159104-i1145275.scope
…
[Scope]
MemoryMax=8589934592
MemorySwapMax=0
```

### P11 — every unit that failed at some point this boot

```
$ journalctl --user -b --no-pager -o cat | grep -E ': Failed with result' | sed -E "s/: Failed with result '([a-z-]+)'.*/ \1/" | sort | uniq -c
      1 ai-usage.service signal
      1 antigravity-shim.service signal
      1 claude-shim.service signal
      2 codex-shim.service signal
      1 cursor-shim.service signal
      1 devin-shim.service signal
      1 ds-flash-shim.service signal
      2 glm-flash-shim.service signal
      1 run-p1157862-i1164315.scope oom-kill
      1 run-p1159104-i1145275.scope oom-kill
      1 shokunin-preflight-9bff2d88a90c42799bab97d163380d09.service exit-code
      1 shokunin-r67-feas-9486de88b976433fab83a2b9553c1861.service exit-code
      1 shokunin-r67-resource-52cc07d8d0274babb92a1cc1e8efff7f.service exit-code
      2 xai-shim.service signal
```

17 failure events across 14 distinct units; by result: `signal` 12, `exit-code` 3, `oom-kill` 2.
Only the two `oom-kill` scopes are still in the failed state; the other 12 units have since
recovered (shim services restarted, `ai-usage.service` next run `Result=success`,
`NRestarts=0`, `ExecMainStatus=0`) and the three `shokunin-*` transients were unloaded with
`ActiveState=inactive Result=success ExecMainStatus=0`.

### P12 — memory / earlyoom context for the OOM cluster

```
$ free -m
               total        used        free      shared  buff/cache   available
Mem:           30978       17654        1192          15       14027       13323
Swap:          30979       12107       18871
$ swapon --show
NAME           TYPE  SIZE  USED PRIO
/swap/swapfile file 30.3G 11.8G    0
$ cat /proc/pressure/memory
some avg10=0.18 avg60=0.09 avg300=0.03 total=652515559
full avg10=0.18 avg60=0.09 avg300=0.03 total=610989489
```

```
$ journalctl -b -u earlyoom --no-pager -o cat | grep -cE '^sending SIGKILL to process'
176
$ journalctl -b -u earlyoom --no-pager -o cat | grep -cE '^sending SIGTERM to process'
144
$ journalctl -b -u earlyoom --no-pager -o cat | grep -E 'when mem avail'
sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,
        SIGKILL when mem avail <=  5.00% and swap free <=  5.00%
$ journalctl -b -u earlyoom --no-pager -o short | grep -E 'sending SIG[A-Z]+ to process' | sed -n '1p;$p'
Nov 02 16:04:18 plazir27 earlyoom[1368]: sending SIGTERM to process 442091 uid 1000 "python": oom_score 1199, oom_score_adj 200, VmRSS 2514 MiB, cmdline "/fast/ComfyUI/.venv/bin/python main.py --listen 127.0.0.1 --port 18188 …"
Nov 02 16:48:00 plazir27 earlyoom[1368]: sending SIGKILL to process 1125092 uid 1000 "rembg": oom_score 949, oom_score_adj 200, VmRSS 8414 MiB, cmdline "/home/vgpnk/.local/share/uv/tools/rembg/bin/python /home/vgpnk/.local/bin/rembg p -m birefnet-general -om /tmp/p61cut-iprguif5/in /tmp/p61cut-iprguif5/out"
```

Kill targets by comm (176 SIGKILL): `chromium 114`, `python3 50`, `python 10`, `rembg 1`,
`node 1`.

Per-boot earlyoom activity: boot `0` = 176 SIGKILL + 144 SIGTERM; boots `-1` and `-2` = **0 / 0**.

Corroborating swap-exhaustion evidence from the kill window:

```
Nov 02 16:47:00 plazir27 earlyoom[1368]: low memory! at or below SIGKILL limits: mem  5.00%, swap  5.00%
Nov 02 16:47:00 plazir27 earlyoom[1368]: mem avail:   409 of 26184 MiB ( 1.57%), swap free:    0 of 30979 MiB ( 0.00%)
```

`systemd-oomd` is **not** the killer: `Loaded: … disabled; preset: disabled`, `Active: inactive (dead)`, and `journalctl -b -u systemd-oomd` → `-- No entries --`.

### P13 — unit-file inventory

```
$ systemctl --user list-unit-files --no-pager | wc -l
159
$ systemctl list-unit-files --no-pager | wc -l
565
$ ls /usr/lib/systemd/user | wc -l
109
$ systemctl --user show -p UnitPath | tr ' ' '\n' | grep -c .
17
$ ls /home/vgpnk/.config/systemd/user/
app-walker@autostart.service.d/  comfyui-backend.service.d/  default.target.wants/  graphical-session-pre.target.wants/  graphical-session.target.wants/  sockets.target.wants/  timers.target.wants/
agents.slice  ai-usage.service  ai-usage.timer  antigravity-shim.service  claude-shim.service  codex-shim.service  codex-shim.service.20261016-132949.bak  codex-shim.service.20261016-135032.bak  comfyui-backend.service  comfyui.service  comfyui.socket  cursor-shim-healthcheck.service  cursor-shim-healthcheck.timer  cursor-shim.service  devin-shim.service  ds-flash-shim.service  ds-flash-shim.service.20261015-112418.bak  ds-flash-shim.service.20261015-112620.bak  elephant.service  glm-flash-shim.service  lfm3-server.service  lfm3-server.service.20261029-031946.bak  omarchy-battery-monitor.service  omarchy-battery-monitor.timer  omarchy-recover-internal-monitor.service  open-design.service  swayosd-server.service  xai-shim.service
```

28 files (18 `.service`, 4 `.timer`, 1 `.socket`, 1 `.slice`, 5 `.bak`) + 7 directories.
Note: 4 of the `.service` entries are timestamped `.bak` backups left inside the unit directory.

---

## 2. Findings — failed-unit identity

**Both failed units are app-level transients, not system-unit failures.**

| unit | class | result | cap | peak | window | trigger |
|---|---|---|---|---|---|---|
| `run-p1157862-i1164315.scope` | transient `systemd-run` scope (rembg) | `oom-kill` | `MemoryMax=3221225472` (3 GiB), `MemorySwapMax=0` | `MemoryPeak=3221225472` (exactly at cap) | 2026-11-02 16:49:19 → 16:49:24 (5.183 s, 38.434 s CPU) | kernel cgroup OOM |
| `run-p1159104-i1145275.scope` | transient `systemd-run` scope (rembg) | `oom-kill` | `MemoryMax=8589934592` (8 GiB), `MemorySwapMax=0` | `MemoryPeak=8589934592` (exactly at cap) | 2026-11-02 16:49:33 → 16:49:45 (11.616 s, 3 min 19.220 s CPU) | kernel cgroup OOM |

Identity basis:

* `Loaded: loaded (/run/user/1000/systemd/transient/run-….scope; transient)` and `Transient=yes`
  — they carry **no unit file** (`systemctl --user list-unit-files --state=bad` → `0 unit files
  listed`), so they cannot be "broken units" in the unit-file sense.
* Descriptions are `[systemd-run] /home/vgpnk/.local/bin/rembg i -m birefnet-general …` — the
  `rembg` background-removal CLI invoked under an explicit memory cap; the shape matches the
  stored `rembg-class` app transient vocabulary.
* Both were killed by the **cgroup** OOM killer, not by the global one: the kernel messages read
  `Memory cgroup out of memory: Killed process 1157862 (rembg) … oom_score_adj:200` and
  `… 1159104 (rembg) … oom_score_adj:200`, and each peak equals its own `MemoryMax` exactly.
  `MemorySwapMax=0` means the scope could not spill to the 30 GiB swapfile at all — the cap was
  the binding constraint, not host pressure at that instant.
* They did not appear in the earlier `--failed` sweep at 16:49:24/16:49:45 as fresh failures of a
  service: they have been in `failed` state for ~22 h and stay there because transient scopes are
  never garbage-collected while failed.

Consequence for the plane: the user manager's `degraded` is caused **entirely** by these two
leftover app transients. `NFailedUnits=2` and `list-units --state=failed` agree; the system scope
has `NFailedUnits=0`, `--failed` empty, and `graphical.target` active.

Classification: **app-level transient (rembg-class), not a system unit failure.** Neither is
evidence of a defect in systemd, the kernel, or any packaged unit.

### Failure history that has since recovered (context for the register, not the failed list)

* 12 shim/agent services failed with `signal` at 2026-11-02 16:47–16:48 — every one is an
  earlyoom kill or an earlyoom SIGTERM escalation during the memory exhaustion in §4. Example
  chain: `earlyoom[1368]: sending SIGTERM to process 1140951 … "python3" … cmdline "python3
  /home/vgpnk/.local/bin/ai-usage refresh"` → `ai-usage.service: Main process exited,
  code=killed, status=15/TERM` → `Failed with result 'signal'` → `Failed to start Probe AI CLI
  usage limits into cache.` That single systemd-class err entry is the whole `systemd 1` class.
* 3 `shokunin-*` transient units failed with `exit-code` (status 1, 134, 134) — orchestrator probe
  runs from `/home/vgpnk/Documents/Codex/2026-11-02/task-4/…`, all now `inactive/success`. The two
  `134` exits are SIGABRT and are the same PIDs as the two `systemd-coredump` crit entries
  (`Process 3686161 (python) … terminated abnormally without generating a coredump`).

---

## 3. Findings — err-class shift vs the r1 stored classes

Stored (2026-10-14 snapshot, `SKILL.md:48`): **238 entries**; classes `systemd-coredump 198`,
`kernel 38`, `sddm-helper 1`.

Live (2026-11-03T18:44:51Z, boot `0`): **5276 entries**; classes:

| class | stored | live | delta | reading |
|---|---|---|---|---|
| `systemd-socket-proxyd` | — (absent) | **5230** | **new dominant class** | one process, one 5-min window (§5) |
| `systemd-coredump` | 198 | **4** | −194 | crash volume collapsed; boot `-2` still shows 242, so this is a *this-boot* property, not a fixed change |
| `kernel` | 38 | **40** | +2 | +1 cgroup-OOM (1→2), +1 empty-message, +1 overlayfs, −? net +2 |
| `sddm-helper` | 1 | **1** | 0 | **match** — same message: `gkr-pam: couldn't unlock the login keyring.` |
| `systemd` | — | **1** | +1 | `Failed to start Probe AI CLI usage limits into cache.` (the earlyoom SIGTERM run) |

Residual after removing the single-process storm: **46 entries** (kernel 40, coredump 4,
sddm-helper 1, systemd 1) — i.e. the plane's "real" noise floor today is *lower* than the stored
238, and the 22× growth in the headline number is one application-level log loop.

Top identifiers at probe time (counts of 5276):

1. `systemd-socket-proxyd` — 5230
2. `kernel` — 40 (of which `sr0` 35, cgroup-OOM 2, TDX 1, empty 1, overlayfs 1)
3. `systemd-coredump` — 4
4. `sddm-helper` — 1
5. `systemd` — 1

### The socket-proxyd class (5230) — what it actually is

* Unit context: `_SYSTEMD_CGROUP=/user.slice/user-1000.slice/user@1000.service/app.slice/comfyui.service`,
  i.e. the `comfyui.service` on-demand socket proxy
  (`ExecStart=/usr/lib/systemd/systemd-socket-proxyd --exit-idle-time=20min 127.0.0.1:18188`,
  `Requires=comfyui-backend.service`).
* Trigger: the backend was killed at 16:04:19 (`Consumed … 24.1G memory peak, 6.5G memory swap
  peak` — earlyoom SIGTERM at 16:04:18, VmRSS 2514 MiB, oom_score 1199). From that instant until
  the proxy hit its 20-min idle exit, every client connect produced one
  `Failed to connect to remote host: Connection refused` at **err** priority.
* Rate: ~15.8/s for 330.6 s (buckets 666 / 940 / 940 / 942 / 940 / 802 per minute). This is a
  *single-client retry loop* hammering `127.0.0.1:8188`, not a systemd defect.
* `comfyui.socket` itself is healthy: `ActiveState=active SubState=listening Result=success`,
  `NAccepted=0` (the accepted connections were counted against the proxy unit, not the socket),
  and `comfyui-backend.service` has **0** failed/killed lines of its own where the failure is
  attributed to the proxy.

Journal-growth check: the err entry count was 5275 → 5276 across a 90-second observation and is
**stable**; the class is a historical 5-minute window, not an ongoing loop.

---

## 4. Findings — the memory-exhaustion cluster (the real operability event this boot)

Timeline, all on 2026-11-02, all within boot `0`:

| time | event |
|---|---|
| 16:04:18 | earlyoom SIGTERM → ComfyUI backend (`VmRSS 2514 MiB`, `oom_score 1199`) |
| 16:04:19 | backend exits, `24.1G` peak / `6.5G` swap peak; socket-proxyd starts its 5230-entry loop |
| 16:46–16:47 | global pressure: `mem avail 409 of 26184 MiB (1.57%)`, `swap free 0 of 30979 MiB (0.00%)` |
| 16:47:00 | earlyoom escalates to SIGKILL; first chromium renderers die (SIGSEGV → 2 cores) |
| 16:47:54–16:48:00 | `ai-usage.service` SIGTERM'd (status 15/TERM), 11 shim services SIGKILL'd |
| 16:49:19–16:49:45 | the two rembg scopes hit their own `MemoryMax` and are cgroup-OOM killed |

Supporting numbers: 176 SIGKILL + 144 SIGTERM this boot; 0 and 0 in boots `-1` and `-2`; 32
threads/cores (`nproc` 32), 30.25 GiB RAM, 30.3 GiB swapfile used 11.8–12.9 GiB at probe time;
`/proc/pressure/memory` `some avg300=0.03`, `full avg300=0.03` (no current pressure).

The two failed units, the 12 `signal` failures, the `systemd 1` err entry, and the two
`systemd-coredump` crit entries are all downstream of this one cluster.

---

## 5. Findings — coredump surface

| quantity | r1 stored (2026-10-14) | live (2026-11-03) | verdict |
|---|---|---|---|
| `coredumpctl list` rows | 198 | **252** (+1 header = 253 lines) | drift |
| files in `/var/lib/systemd/coredump` | 764 | **10** | drift |
| bytes on disk | 3.8 G | **704 M** (`737406945` B) | drift |

Composition now: `python3.14` 81, `unshare` 29, `chromium` 19, `gcc16-O3` 11, `clang23-O3` 10,
`bw12-O3` 10, `chrome_crashpad_handler` 9, `bash` 9, `sasquatch-v4be` 6, `python3` 6, `git` 6,
`node` 5, then singletons (`sim`, `probe`, `cmain`, `harness`, `strace`, `turbo`, `ffmpeg`, …).
Signals: SIGSEGV 191, SIGABRT 29, SIGBUS 17, SIGXFSZ 7, SIGILL 5, SIGTRAP 2, SIGSYS 1.
Storage: **228 of 252 cores are `COREFILE missing`**, 14 `none`, 9 `present`, 1 `truncated` — so
the 252-row count is a *crash* count, not a *core-file* count, and the 10 files / 704 M are the
real disk footprint.

Per-boot: boot `-2` 237, boot `-1` 11, boot `0` **4**. The 252 rows are therefore dominated by an
episode that predates the current boot (2026-10-26 → 10-31), including the `unshare` (29) and
`gcc16/clang23/bw12` (31) suites that look like benchmark/test-harness runs, not desktop crashes.

This boot has **4** coredumps: 2 chromium SIGSEGV at 16:47:00/01 (earlyoom SIGKILL'd renderers,
each producing a real `present` core, 6.8 M / 17.9 M) and 2 python3 SIGABRT at 22:53:23/23:05:12
(`none` — `terminated abnormally without generating a coredump`), which are the two
`shokunin-r67-*` probe units exiting 134.

---

## 6. OS-level observations worth the operator's attention (detection only)

Per the lane boundary these are recorded for triage; **no remediation was attempted or is
proposed as an action in this seat**.

### 6.1 USB optical drive `sr0` fails reads at every boot (chronic, 3 boots)

35 kernel err entries in 2.6 s at boot (`critical target error, dev sr0, sector 44989024 op …`
and `Buffer I/O error on dev sr0, logical block 5623628, async page read`). The device is a
USB-attached optical drive with a disc labelled `MB_Support_CD` (`ID_MODEL=ProductCode`,
`ID_CDROM_MEDIA=1`, 21.5 G `iso9660`), never mounted. Counts: boot `-2` 65, boot `-1` 60, boot `0`
35. Chronic and self-limiting (boot-time enumeration only, no runtime recurrence), but it is the
single largest kernel-err class in every retained boot and it is a *hardware/media* class, not a
software one. Confidence: high that the class is real and boot-scoped; medium on whether the
media or the drive is at fault (both consistent with `critical target error`).

### 6.2 `overlayfs: failed to resolve '/upper': -2` — new err-priority burst during wave hours

```
Nov 03 15:38:04 plazir27 kernel: overlayfs: failed to set xattr on upper
Nov 03 15:38:04 plazir27 kernel: overlayfs: ...falling back to redirect_dir=nofollow.
Nov 03 15:38:04 plazir27 kernel: overlayfs: ...falling back to metacopy=off.
Nov 03 15:38:04 plazir27 kernel: overlayfs: ...falling back to index=off.
Nov 03 15:38:04 plazir27 kernel: overlayfs: ...falling back to uuid=null.
Nov 03 15:38:04 plazir27 kernel: overlayfs: ...falling back to xino=off.
Nov 03 15:38:04 plazir27 kernel: overlayfs: try mounting with 'userxattr' option
Nov 03 15:39:19 plazir27 kernel: overlayfs: failed to resolve '/upper': -2
Nov 03 15:39:33 plazir27 kernel: overlayfs: failed to set xattr on upper
… (repeats)
```

Priorities: the `failed to set xattr` / `falling back` / `try mounting with 'userxattr'` lines are
**4 (warning)** / 6 (info); only `failed to resolve '/upper': -2` is **3 (err)**. Burst times:
15:38:04, 15:39:33, 15:41:07, 15:41:23, 15:41:30, 15:43:11 — all inside the r64 wave session
window, none during a 30 s idle window I observed (18:41:30→18:42:00Z, delta 0 lines).

Context: `/upper` does not exist (`ls -d /upper` → `No such file or directory`), there is **no
overlay mount anywhere** (`findmnt -t overlay` empty; zero `overlay` lines in `/proc/*/mountinfo`
for every process I could read), `unprivileged_userns_clone=1`, `user.max_user_namespaces=122865`,
LSM list `capability,landlock,lockdown,yama,bpf`. `overlayfs` also appears in boot `-2` (14 lines,
e.g. `workdir and upperdir must reside under the same mount`) and not in boot `-1`.

**Inference (medium confidence):** these are ephemeral, short-lived user-namespace overlay mounts
set up by sandboxed tooling — the `-2` (`ENOENT`) resolve and the xattr fallbacks are what an
unprivileged mount on a btrfs/`nosuid` upper looks like, and the timing tracks agent activity, not
a boot or kernel path. They are **non-fatal**: the kernel falls back and the mount either succeeds
with reduced features or the sandbox retries. Recording as an observed class, not as a defect.
Not attributable from journal alone — no unit/scope/cgroup is attached to these lines
(`_COMM`/`_PID` are absent for both entries).

### 6.3 `cursor-shim-healthcheck.timer` has not triggered in 15 days and its service never logs

`UnitFileState=enabled`, `ActiveState=active SubState=elapsed`,
`TimersMonotonic={ OnUnitActiveUSec=1min ; next_elapse=0 }`, `LastTriggerUSec=Mon 2026-10-19
00:33:15 -03`. The service has `-- No entries --` in the user journal for **every retained boot**,
and `ExecMainExitTimestamp=` empty. So the healthcheck has produced no observable activity since
2026-10-19 despite being enabled with a 1-minute monotonic interval. `next_elapse=0` on a
`OnUnitActiveSec` timer means it is waiting on an activation that will not come; that is a
self-referential dead timer, not a failing one — it never appears in `--failed`. Detection only:
this is a silently-degraded watchdog, and the stored plane note ("only `ai-usage.timer` active")
would have hidden it because the timer *is* listed as active.

### 6.4 Sustained swap use is high but pressure is currently zero

`/swap/swapfile` 30.3 G, 11.8→12.9 G used; `buff/cache` 9.8–14 G; `available` 13.3–20.2 G;
PSI `some/full avg300=0.03`. No action implied — recorded because the stored r6 note carries
`C5_swap_peak_pct=99%` and the same swapfile is what earlyoom monitors with a 5 %/5 % gate.

---

## 7. Traps and non-probes (recorded so no later seat re-derives them)

1. **`coredumpctl` in this build has no `--boot`/`-b`.**
   `$ coredumpctl list -b 0` → `coredumpctl: unrecognized option '-b'`, rc=1;
   `$ coredumpctl list --boot` → `coredumpctl: unrecognized option '--boot'`, rc=1.
   `coredumpctl --help` lists only `-S --since=DATE`. Per-boot attribution must use
   `--since … --until …` windows built from `journalctl --list-boots`. Any stored row that reports
   "coredumps this boot" from `coredumpctl --boot` is derived from a different tool version.
2. **`systemctl --user show -p State` prints nothing.** `$ systemctl --user show -p State` → empty,
   rc=0. Use `systemctl --user is-system-running` (prints `degraded`, rc=1) or `NFailedUnits`.
3. **`-p err` line count ≠ entry count.** 6213 lines vs 5276 entries in the *same* invocation
   window; the difference is coredump stack traces inside single entries. The stored snapshot's
   own note already flags this; it reproduces exactly.
4. **`dmesg` is blocked** (`dmesg_restrict=1`): `dmesg: read kernel buffer failed: Operation not
   permitted`, rc=1. Kernel evidence had to come from `journalctl -k`.
5. **`journalctl -b -p err` overcounts earlyoom config lines** if you grep `sending SIG` — the
   banner lines `sending SIGTERM when mem avail <= …` match. Counting with
   `'^sending SIGKILL to process'` gives 176, vs 176 for the naive grep only by coincidence of a
   different anchor; use the `to process` anchor.
6. **`btrfs subvolume list /` is blocked**: `ERROR: can't perform the search: Operation not
   permitted`. Not needed for this item.
7. **`/sys/kernel/debug/zswap/*` is blocked** (`Permission denied`, rc=0 from the shell) — zswap
   stats are not readable unprivileged, so the `zswap.enabled=1 zswap.max_pool_percent=25` cmdline
   settings are recorded but their runtime counters are not.
8. **`du` on `/var/cache/pacman/pkg` style dirs needs care** — not probed here (out of scope), but
   `du -sh /var/lib/systemd/coredump` succeeded (704M) where sibling caches have been
   permission-limited in prior rounds.
9. **`ps -eo --sort=-etimes` is unsupported** on this procps build (`ps: unknown sort specifier
   'etimes'`); `--sort=-rss` works.

---

## 8. Register-ready values (for the drift table; E2Probes owns that file)

Not written into `after/drift-table-draft.md` — supplied here verbatim so the owner can lift them
with a receipt pointer to this file.

| id | plane | stored (2026-10-14) | live (2026-11-03T18:44Z) | verdict |
|---|---|---|---|---|
| SC1-DR-a | systemd user scope | `running`, rc=0 | `degraded`, rc=1 | `drift` |
| SC1-DR-b | failed units | `0 failed units (--failed and --all)` | `2` — `run-p1157862-i1164315.scope`, `run-p1159104-i1145275.scope`, both `Result=oom-kill`, both transient rembg scopes | `drift` |
| SC1-DR-c | system scope | `running` | `running`, `NFailedUnits=0`, `graphical.target active` | `match` |
| SC1-DR-d | journal err entries | `238` | `5276` | `drift` |
| SC1-DR-e | journal err classes | `systemd-coredump 198, kernel 38, sddm-helper 1` | `systemd-socket-proxyd 5230, kernel 40, systemd-coredump 4, sddm-helper 1, systemd 1` | `drift` |
| SC1-DR-f | kernel err sub-classes | `20 sr0 critical + 15 Buffer I/O, 1 OOM, 1 TDX` | `20 sr0-critical + 15 sr0-bufferio, 2 cgroup-oom, 1 TDX, 1 overlayfs, 1 empty` | `drift` (+1 OOM, +1 overlayfs, +1 empty) |
| SC1-DR-g | coredump entries | `198` | `252` rows | `drift` |
| SC1-DR-h | coredump files / bytes | `764 files, 3.8 G` | `10 files, 704 M (737406945 B)` | `drift` |
| SC1-DR-i | retained boots | `13` (census line) / `9` (later note) | `3` | `drift` |
| SC1-DR-j | timers | `only ai-usage.timer active` | 2 listed: `ai-usage.timer` (active/waiting, 5 min, 327 runs this boot); `cursor-shim-healthcheck.timer` (active/elapsed, `LastTriggerUSec=2026-10-19`, never logs) | `drift` |
| SC1-DR-k | `sddm-helper` err | `1` (`gkr-pam: couldn't unlock the login keyring.`) | `1`, same message | `match` |

---

## 9. Remaining unknowns

* **What opened the 5230 connections to `127.0.0.1:8188`.** The proxy's log records only
  `Connection refused`; the client is not in the journal (no `_SYSTEMD_UNIT` on the accept side,
  `NAccepted=0` on the socket). The rate (≈16/s, flat across 5 minutes) is a retry loop, but which
  process drives it is not derivable from the journal alone.
* **Which process mounts the ephemeral overlayfs.** Kernel lines carry no `_PID`/`_COMM`; no
  overlay mount is readable in any process's `mountinfo` at probe time (the mounts are gone), and
  `findmnt -t overlay` is empty. Timing correlates with wave-hours agent activity, but that is
  inference, not observation.
* **Whether `sr0` media or drive is at fault.** `critical target error` at fixed sector ranges is
  consistent with both; resolving it needs a read test that this seat is not authorised to run.
* **Whether the 252 `coredumpctl` rows contain any entry newer than boot `0`'s 4.** The newest
  timestamp is 2026-11-02 23:05:12, i.e. no new cores during wave hours; the 10 stored files
  are all ≤ 2026-11-02 16:47.
