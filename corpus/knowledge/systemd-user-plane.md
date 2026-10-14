# systemd user plane — plazir27 (probe 2026-10-14)

**Probe context (all read-only).** Host `plazir27`, user `vgpnk` UID 1000, `systemd 261 (261.2-1-arch)`
(`systemctl --user --version`). Boot 0 id `d7f0bc8d938e4249b4a1f250cbfacf58`, kernel boot
2026-10-13 10:57:58 (`uptime -s`), first journal record 2026-10-13 11:02:03
(`journalctl --list-boots --no-pager`, last line). Probe window 2026-10-14 ~09:50–10:00 -03.
Substrates outside this repo (systemd, journal, unit files, `~/.config`, `/etc`, `/usr`) were not modified.

Notation: **[obs]** measured, **[inf]** inference, **[unk]** unknown. Every bullet carries its anchor.
Unit paths below `~/.config/systemd/user/` are abbreviated after first mention.

## 1. Manager state

- **[obs]** `systemctl --user is-system-running` → `running`.
- **[obs]** `systemctl --user get-default` → `default.target`.
- **[obs]** `systemctl --user --failed --no-pager` → `0 loaded units listed.`
- **[obs]** `systemctl --user list-timers --all --no-pager` → `1 timers listed.` (only `ai-usage.timer`).
- **[obs]** Bounded user-journal failure grep (`journalctl --user -b --no-pager | grep -E 'Failed to|failed with result|entered failed'`, head-limited) returned only application-level
  warnings: `uwsm_hyprland.desktop[1671]: WARN ... Failed to change process scheduling strategy`;
  `xdg-desktop-portal[1850]: Failed to load RealtimeKit property ... ServiceUnknown` (×3);
  `1password[1800]: ERROR ... Failed to retrieve initial metering setting`;
  `xdg-desktop-portal-gtk[1881]: Failed to associate portal window with parent window` (×2).
  No unit-level `Failed to start` / `entered failed` lines in the scanned range. **[inf]** No user unit
  entered failed state this boot. Caveat: the grep was head-bounded — absence is proven only for the
  scanned lines, not the whole journal.

## 2. Unit inventory — `~/.config/systemd/user/`

Measured set (`find ~/.config/systemd/user/ -type f -o -type l`): **7 unit files + 1 drop-in + 5
enablement symlinks**.

### 2.1 Files and operative lines

| path:line | directive |
|---|---|
| `ai-usage.service:9` | `EnvironmentFile=-%h/.config/ai-usage/env` (leading `-` = optional; file exists per `test -f`; contents NOT read — secrets discipline, shape only) |
| `ai-usage.service:10` | `ExecStart=%h/.local/bin/ai-usage refresh` (Type=oneshot, TimeoutStartSec=180, Nice=10) |
| `ai-usage.timer:5,7,9,10,13` | `OnBootSec=30` / `OnUnitActiveSec=300` / `AccuracySec=10` / `Unit=ai-usage.service` / `WantedBy=timers.target` |
| `omarchy-battery-monitor.service:7` | `ExecStart=%h/.local/share/omarchy/bin/omarchy-battery-monitor`; no `[Install]` → `is-enabled` = `static` |
| `omarchy-battery-monitor.timer:3,6,7,8,11` | `Requires=omarchy-battery-monitor.service` / `OnBootSec=1min` / `OnUnitActiveSec=30sec` / `AccuracySec=10sec` / `WantedBy=timers.target` |
| `omarchy-recover-internal-monitor.service:4,8,11` | `ConditionPathExists=%h/.local/state/omarchy/toggles/hypr/internal-monitor-disable.conf` / `ExecStart=%h/.local/share/omarchy/bin/omarchy-hw-recover-internal-monitor` / `WantedBy=graphical-session-pre.target` |
| `elephant.service:8,9,12` | `ExecStart=elephant` / `Restart=on-failure` / `WantedBy=graphical-session.target` |
| `swayosd-server.service:8,9,10,13` | `ExecStart=/usr/bin/swayosd-server` / `Restart=always` / `RestartSec=2` / `WantedBy=graphical-session.target` |
| `app-walker@autostart.service.d/restart.conf:2,3` | `Restart=always` / `RestartSec=2` — drop-in hardening a *generated* xdg-autostart unit (`app-walker@autostart.service` STATE=`generated`) |

### 2.2 Enablement / run state (probe-time)

| unit | `is-enabled` | runtime state |
|---|---|---|
| `ai-usage.timer` | `enabled` | `active (waiting)` |
| `ai-usage.service` | `static` | `inactive dead` (oneshot; last run `Result=success`, `ExecMainStatus=0`, `NRestarts=0`, start 2026-10-14 09:52:56 -03) |
| `omarchy-battery-monitor.timer` | `disabled` | `inactive (dead)`, `Trigger: n/a` |
| `omarchy-battery-monitor.service` | `static` | `inactive dead` |
| `omarchy-recover-internal-monitor.service` | `enabled` | `inactive dead` — condition-skipped, see §4 |
| `elephant.service` | `enabled` | `active running` |
| `swayosd-server.service` | `enabled` | `active running` |
| `ssh-agent.socket` | `enabled` | `active listening`; `ssh-agent.service` is `inactive dead` (socket-activated; list-unit-files STATE=`indirect`) |

Symlink targets (`ls -la` on `*.wants/`): `graphical-session.target.wants/elephant.service`,
`graphical-session.target.wants/swayosd-server.service`,
`graphical-session-pre.target.wants/omarchy-recover-internal-monitor.service`,
`timers.target.wants/ai-usage.timer` — all point back to their own unit files in `~/.config`;
`sockets.target.wants/ssh-agent.socket → /usr/lib/systemd/user/ssh-agent.socket` (system-shipped
unit enabled by user symlink).

### 2.3 Other roots (system-level, root-owned)

- **[obs]** `/etc/systemd/user/` enables system-shipped units via symlinks:
  `graphical-session-pre.target.wants/xdg-user-dirs.service`,
  `pipewire.service.wants/wireplumber.service`,
  `sockets.target.wants/{gnome-keyring-daemon,p11-kit-server,pipewire-pulse,pipewire}.socket`
  (all → `/usr/lib/systemd/user/`); alias `pipewire-session-manager.service → …/wireplumber.service`.
- **[obs]** `/usr/lib/systemd/user/` ships 109 unit files (`ls | wc -l`).
- **[obs]** `systemd-analyze --user unit-paths` lists 17 roots; user-writable roots in use:
  `~/.config/systemd/user`, `~/.local/share/systemd/user` (latter empty as measured).
- **[obs]** `list-units --type=service --all` shows `not-found` (dead): `pipewire-media-session.service`,
  `pulseaudio.service`, `systemd-remount-fs.service` — absent units referenced by aliases.
  **[inf]** expected on a pipewire-based Arch/Omarchy session; not failures.

## 3. Timer plane

- **[obs]** `ai-usage.timer` — only active timer: `Active: active (waiting) since Tue 2026-10-13 11:02:06 -03`,
  `Trigger: Wed 2026-10-14 09:57:56 -03`; cadence from unit (`OnBootSec=30` + `OnUnitActiveSec=300`,
  `ai-usage.timer:5,7`) = first run 30 s after boot, then every ~5 min. Recent run trace
  (`journalctl --user -u ai-usage.service -n 10`): `Finished Probe AI CLI usage limits into cache.`,
  `Consumed 1.975s CPU time over 3.671s wall clock time, 148.8M memory peak`; log lines are per-provider
  usage metadata (percentages); no credential material surfaced in the log sample.
- **[obs]** `omarchy-battery-monitor.timer` is `disabled` → not loaded into the timer set
  (`list-timers --all` shows 1 timer). It declares `[Install] WantedBy=timers.target`
  (`omarchy-battery-monitor.timer:11`) but no `timers.target.wants/` symlink exists.
  **[inf]** latent unit — never runs as measured; preset is `enabled`, so
  `systemctl --user preset omarchy-battery-monitor.timer` would arm it. Intent **[unk]**.
- **[obs]** `systemd-tmpfiles-clean.timer`: `disabled` / preset `enabled` (list-unit-files).
- **[obs]** `list-timers --all` shows `NEXT/LEFT/LAST/PASSED` for the active timer only;
  no failed timer units exist (0 failed units overall, §1).

## 4. Condition-gated units

- **[obs]** `omarchy-recover-internal-monitor.service`: `is-enabled`=`enabled`, runtime `inactive dead`.
  Gate: `ConditionPathExists=%h/.local/state/omarchy/toggles/hypr/internal-monitor-disable.conf` (`:4`);
  probe of the path (`test -e …`) → `ABSENT`.
  **[inf]** Unit was skipped by condition, not failed; it will run only when that toggle file exists.

## 5. Last-boot error classes — `journalctl -b -p err --no-pager` (bounded)

**[obs]** Raw output = **60,941 lines**; JSON entry count = **238**
(`journalctl -b -p err -o json --no-pager | wc -l`). Line count ≫ entry count because coredump
messages embed full multi-thread stack traces (see §8.1). Entry-level classes
(`jq -r '[.SYSLOG_IDENTIFIER] …' | sort | uniq -c`):

| class | entries | detail |
|---|---|---|
| `systemd-coredump` | 198 | all `_UID=1000`; `_COMM` truncated to `systemd-coredum` (15-char comm limit) |
| `kernel` | 38 | 20× `critical target error, dev sr0, sector …` + 15× `Buffer I/O error on dev sr0, …` (35 sr0 lines, window 11:02:03–11:02:06; last: `Oct 13 11:02:06 … Buffer I/O error on dev sr0`); 1× `virt/tdx: TDX not supported by the host platform`; 1× `Out of memory: Killed process 1732581 (python3) total-vm:56727648kB, anon-rss:27873696kB … oom_score_adj:200` (PRIORITY=3, _TRANSPORT=kernel, Oct 13 23:44:30) |
| `sddm-helper` | 1 | `gkr-pam: couldn't unlock the login keyring.` (Oct 13 11:02:06) |
| `limine-snapper-sync` | 1 | `No Snapper config found for '/'. Please configure Snapper and set SNAPPER_CONFIG_NAME in /etc/default/limine.` (Oct 13 11:02:05) |

Error window: first 11:02:03 (sr0) → last **2026-10-14 09:42:10 -03** (godot coredump entry,
epoch µs 1791981730606818; `date -d @1791981730`).
**[inf]** The `sr0` cluster is one boot-window incident on the optical device (`dev-cdrom.device`
"ProductCode MB_Support_CD" and OMARCHY/ARCHISO USB entries are present in `list-units --all`);
it stopped after 11:02:06 with no recurrence in the error journal.
**[unk]** Whether the limine-snapper-sync message is a defect or expected "not configured" notice;
whether the sddm-helper keyring line relates to the 1Password autostart.

## 6. Coredump census — `coredumpctl list --since "2026-10-13 10:57:58" --json=short`

**[obs]** 198 coredumps this boot (`jq 'length'` = 198; matches §5 coredump entry count).
By signal + executable (`.[] | [.sig,.exe,.corefile]`):

| sig | exe | count (corefile) |
|---|---|---|
| 6 SIGABRT | `/usr/bin/godot` | 142 (139 present, 3 missing) |
| 6 SIGABRT | `…/fnm/node-versions/v24.21.0/installation/bin/node` | 25 (14 missing, 11 present) |
| 5 SIGTRAP | `…/fnm/node-versions/v24.21.0/installation/bin/node` | 22 (15 present, 7 none) |
| 7 SIGBUS | `/grok-bot` | 3 (present) |
| 5 SIGTRAP | `/usr/share/typora/Typora` | 2 (missing) |
| 7 SIGBUS | `/chrome_crashpad_handler` | 2 (present) |
| 5 SIGTRAP | `/usr/lib/electron43/electron` | 1 (present) |
| 11 SIGSEGV | `/usr/bin/bash` | 1 (present) |

Corefile status overall: **172 present / 19 missing / 7 none**. Crashes continue through the probe
window: latest entries 2026-10-14 09:40:41, 09:40:48, 09:42:10 — all `godot`, SIGABRT, 4.8M core.
**[inf]** `/grok-bot` and `/chrome_crashpad_handler` are verbatim coredumpctl JSON paths that look
like mount-namespace paths of sandboxed processes; origin not verified.
**[unk]** Root cause of the godot SIGABRT storm (dev workload vs. defect — outside this probe's scope
to attribute).

## 7. User journal view — `journalctl --user -b -p err`

**[obs]** 198 entries, all `SYSLOG_IDENTIFIER=systemd-coredump`, all `_UID=1000`,
`_TRANSPORT=journal`; zero kernel lines. This is the same 198 coredump entries as the system view.
**[unk]** Mechanism (journald routing): on this system the `--user` view presents the UID-1000 slice
of the boot journal rather than only user-unit messages; not verified from first principles.
**Practical rule:** before counting user-plane errors, dedupe against system `-p err` by
`_UID=1000` + `systemd-coredump`; the views overlap.

## 8. Method lessons (measured, reusable)

1. **[obs]** Never classify `journalctl -p err` by output lines / awk columns: 60,941 lines vs 238
   entries; stack-trace continuation lines fake classes (`AMD` came from
   `ELF object binary architecture: AMD x86-64`; `+` from `+ 0x…` frames). Count entries with
   `-o json | wc -l`; classify with jq on `SYSLOG_IDENTIFIER`/`_COMM`. (See §10.)
2. **[obs]** jq `sub()` has no `\1` backreference — an intermediate query emitted a literal class
   `\1 ...`. Use named captures or `split()`.
3. **[obs]** Coredump `MESSAGE` in `-o json` is a byte array (non-UTF8 payload) — string pipelines
   yield `<binary-message>`; use short output, `_COMM`, or `coredumpctl --json=short` fields.
4. **[obs]** `coredumpctl list` table parsing misleads: the TIME column spans 4 fields, and
   `-F exe` returned empty output on this systemd 261 while `--json=short` + jq worked. JSON is canonical.
5. **[obs]** `uptime -s` = 2026-10-13 10:57:58 vs first journal record = 11:02:03 (boot 0). Cite the
   exact anchor measured; do not equate kernel boot time with journal start.
6. **[obs]** `systemctl --user list-units --all` is dominated by `.device` units before services
   appear; filter `--type=service` / `--state=failed` for triage legibility.

## 9. Unknowns (open)

- Intent behind `omarchy-battery-monitor.timer` being `disabled` (preset would enable it).
- `ai-usage.service` env-file contents — deliberately not read (secrets shape-only); whether the probe
  requires credentials there is unknown.
- Journald mechanism behind the UID-slice `--user` view (§7).
- Relationship (if any) between the Oct 13 23:44 OOM kill, the node/typora/godot coredump storms, and
  the ongoing godot crashes — no causal tracing attempted (out of scope).
- Whether `sr0` errors mean bad/missing optical media vs. drive fault (single incident, no record).
- The ~5-min gap between kernel boot (10:57:58) and first journal record (11:02:03): journal flush
  delay or separate `/var/log` mount (`var-log.mount` is present) — plausible, unverified.
- Failure history of prior boots not measured (scope = last boot).

## 10. Errata (append-only)

- **[2026-10-14 probe] RETRACTED**: intermediate line-level awk classification reported classes
  `AMD` (191), `+` (49,766), blank (5,373) as boot errors. Artifacts of parsing multi-line coredump
  stack traces as individual messages. Entry-level JSON recount: 238 entries, classes per §5. Kept as
  evidence of method risk (lesson §8.1).
- **[2026-10-14 probe] CORRECTED**: first coredump per-exe parse used `awk '$5,$7'` (table columns) and
  printed PIDs/GIDs because the TIME column spans four fields. Re-derived from `--json=short`
  (canonical) per §6; table numbers match after field shift.

### Wave-1 errata applied (2026-10-14 10:48–10:51 -0300, re-measured; append-only)

Wave-1 record sources: `SKILL.md:217-227` (journal / unit-file / rollback
corrections), `SKILL.md:43` (boot-gap inference), `LOG.md:33-38`,
`CORPUS.md:17`. Scratch `/tmp/tsukuroi-r2-3-work/`. Numbers below are today's.

- 2026-10-14 — **unit-file count corrected: 136 → 133** (`SKILL.md:221-223`):
  `systemctl --user list-unit-files --no-pager | wc -l` = **136 raw lines**,
  decomposing as 1 header + **133 unit rows** + 1 blank + 1 footer
  (`133 unit files listed.`); awk on `\.(service|timer|socket|…)$` = 133. The
  first-pass 136 was a raw line count, never a unit count. [observation]
- 2026-10-14 — **journal-err recount (drifts; re-quote, never cache)**:
  `journalctl -b -p err --no-pager | wc -l` = **61 343 lines** vs
  `-o json | wc -l` = **239 entries** (note: 60 941 / 238); `--user` view 199
  entries; coredump census 199 (was 198; latest entries still godot SIGABRT).
  The ~257:1 line:entry ratio keeps the line-count trap (§8.1) live.
  [observation]
- 2026-10-14 — **boot-gap judgment recorded as erratum, not promoted to fact**
  (`SKILL.md:43`): re-measured anchors are consistent with the resume
  hypothesis — `/proc/cmdline` carries
  `resume=/dev/mapper/root resume_offset=3795013`; first journal record at
  monotonic `[ 244.159301]`; `systemd-analyze` kernel phase 4 min 3.328 s. The
  §9 gap question stays [inference, unproven]: resume explains it, but the
  journal-flush/mount-delay hypothesis is not excluded by the same evidence.
- 2026-10-14 — manager state re-measured unchanged: `is-system-running` =
  `running`, 0 failed units, 1 timer (`ai-usage.timer`, last run 10:49:38).
  [observation]
- 2026-10-14 — **field-contract erratum**: the header carries measured-date
  prose, not the contracted literal keys (`CORPUS.md:17`). Appended values:
  `source:` systemctl / journalctl / coredumpctl probes, host `plazir27`;
  `verified-at:` 2026-10-14 (wave-1 audits + this re-measure); `recheck:` the
  Appendix command set below. [observation]

## Appendix — probe command set (reproducible)

```
systemctl --user is-system-running; systemctl --user get-default
systemctl --user --failed --no-pager
systemctl --user list-units --all --no-pager
systemctl --user list-unit-files --no-pager
systemctl --user list-timers --all --no-pager
systemctl --user is-enabled <unit>; systemctl --user status <unit> --no-pager
find ~/.config/systemd/user/ -type f -o -type l; ls -la ~/.config/systemd/user/*.wants/
find /etc/systemd/user/ -type f -o -type l
systemd-analyze --user unit-paths
journalctl -b -p err --no-pager | wc -l
journalctl -b -p err -o json --no-pager | jq -r '[.SYSLOG_IDENTIFIER, (._UID|tostring)] | @tsv' | sort | uniq -c
journalctl --user -b -p err -o json --no-pager | wc -l
coredumpctl list --since "2026-10-13 10:57:58" --json=short --no-pager | jq -r '.[] | [.sig,.exe,.corefile] | @tsv' | sort | uniq -c
journalctl --list-boots --no-pager | tail -4
```

## 11. Errata (round 4)

- 2026-10-14 (TSUKUROI-ERR-S sweep) — **header pin re-verified, holds.** `systemctl --user
  --version` → `systemd 261 (261.2-1-arch)`, identical to the header pin (`:3`). No stale pin
  on this note. [observed]
- 2026-10-14 — **field-contract erratum** (same class as `driver-firmware-plane.md:239`): the
  header carries probe-context prose, not the contracted literal keys (`CORPUS.md:17`) — a
  contract this note itself cites at `:202` and `:226` without satisfying. Appended values:
  `source:` live read-only probes — `systemctl --user` / `journalctl` / `coredumpctl` /
  `systemd-analyze` / `find` on host `plazir27`, uid 1000, non-root; `verified-at:` 2026-10-14
  (round-4 re-check of the header pin only; body captures keep their own stamps); `recheck:`
  `systemctl --user --version` for the header pin + the §10 probe set. [observation]
- 2026-10-14 — **md5-pin consequence:** this append changes this file's md5 and line count, so
  `host-health-report-r3.md` §5's pin for this note (`26dca9cf12b322926babfef49e257f07`, 247
  lines) is superseded as of this block; post-append values recorded in that report's round-4
  errata. [observation]
