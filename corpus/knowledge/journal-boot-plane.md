# Journal / boot plane — err/warn census, failed-service history, boot shape, timer drift (TSUKUROI-R3-1)

source: live read-only probes — `journalctl` (list-boots / priority censuses / JSON), `systemctl`
(failed units, timers, show), `systemd-analyze`, `coredumpctl`, `bootctl status`, `pacman -Qo`,
`getfacl` — host `plazir27`, user `vgpnk` (uid 1000, groups `vgpnk docker input wheel`), non-root;
journal read granted by the `/var/log/journal` wheel ACL, not by `systemd-journal` membership (§1.4)
verified-at: 2026-10-14 11:39–11:58 -0300 (every count is quoted with its command and capture
context; journal counts drift live — a coredump storm is running, §2)
recheck: Appendix probe command set. Entry counts are `-o json | wc -l`; never raw lines (§9.1).

**Probe context (all read-only).** Host `plazir27`, kernel `7.2.3-arch1-3`, boot 0 id
`d7f0bc8d938e4249b4a1f250cbfacf58`, kernel boot 2026-10-13 10:57:58 (`uptime -s`), uptime
1 day 0 h 43 m (11:41). Journal persists **13 boots** back to install day 2026-10-03 17:42:07
(`journalctl --list-boots --no-pager` = 14 lines = header + 13 boot rows, 11:39); disk footprint
**181.3 M** (`journalctl --disk-usage`, 11:39). Substrates outside this repo (journal, unit files,
`/boot`, `/etc`) were not modified; no rotate/vacuum/restart verb was run; no `sudo`. Secrets:
journal message text was read only through the census filters below — no credential material
surfaced; `/etc/crypttab` is mode 600 root and its contents were **not** read (shape-only, §7).
Scratch: `/tmp/tsukuroi-r3-1-scratch/` (ephemeral; key outputs embedded below).

Notation: **[observed]** measured · **[inference]** · **[unknown]** · **BLOCKED** = privilege-gated
probe, recorded not escalated. Every count carries its command; negative claims carry their sweep.

## 1. Boot inventory & journal retention

### 1.1 The 13 retained boots

`journalctl --list-boots --no-pager` (11:39) plus per-boot err entry counts
(`journalctl -b <n> -p err -o json --no-pager | wc -l`, loop at 11:40):

| idx | boot id (prefix) | first entry | last entry | err entries |
|---|---|---|---|---|
| −12 | `b2d2184f` | 2026-10-03 17:42:07 | 17:42:11 | 1 |
| −11 | `3b970ff9` | 2026-10-03 17:48:24 | 19:08:35 | 60 |
| −10 | `c5f37237` | 2026-10-03 19:09:41 | 2026-10-04 20:02:24 | 40 |
| −9 | `02f244ce` | 2026-10-04 22:01:14 | 22:05:26 | 39 |
| −8 | `7a203f61` | 2026-10-05 01:08:08 | 2026-10-06 18:20:46 | 40 |
| −7 | `e08954ce` | 2026-10-06 18:26:29 | 18:47:45 | 48 |
| −6 | `7ebbaa31` | 2026-10-06 20:21:24 | 2026-10-09 13:34:03 | 58 |
| −5 | `d5daa438` | 2026-10-09 15:17:42 | 2026-10-10 08:50:32 | 88 |
| −4 | `dfa341ec` | 2026-10-10 11:48:32 | 12:39:11 | 55 |
| −3 | `69e11ec8` | 2026-10-10 12:39:55 | 2026-10-11 04:42:29 | 168 |
| −2 | `2d8f74c5` | 2026-10-11 07:23:31 | 19:00:08 | 80 |
| −1 | `73a8e2fc` | 2026-10-11 19:02:51 | 2026-10-13 10:57:30 | 92 |
| 0 | `d7f0bc8d` | 2026-10-13 11:02:03 | live (last 11:39:39) | **247** (11:40) |

- Err volume per boot is modest (39–92 typical; −3 = 168) until boot 0's **247**, of which **207
  are coredumps** (§2.2): the crash storm is the plane's dominant error source.
- Retention reaches the install day (first record 2026-10-03 17:42:07, the 4-second boot −12);
  anything older is rotated away and cannot be shown → [unknown]. Sweep for the negative claim:
  the list-boots output itself. Rotation policy not proven: `/etc/systemd/journald.conf` ships
  with all directives commented (read 11:39); effective defaults not derived.

### 1.2 Boot 0 — kernel start vs journal start

- `uptime -s` = 2026-10-13 **10:57:58**; first journal record **11:02:03** ⇒ **4 m 05 s** between
  kernel start and the journal's first record (the boot-gap question carried from round 2,
  `SKILL.md:43`).
- First record = kernel banner at monotonic `[ 244.159301]`, then `Command line:` within 11 µs
  (`journalctl -b -o short-monotonic --no-pager | head -3`) — a burst of early records sharing one
  monotonic value; the system-wide pattern is in §5.3.
- `/proc/cmdline` (read): `resume=/dev/mapper/root resume_offset=3795013 quiet splash loglevel=0 …
  cryptdevice=PARTUUID=cf3d875f-…:root root=/dev/mapper/root …`.
- Every retained boot except the −12 live ISO logs `PM: Image not found (code -22)` exactly once
  (sweep: `journalctl --no-pager -g 'PM: Image'` → 12 messages + 12 boot headers = 24 lines).

### 1.3 Journal access — not privilege-blocked

- `id` / `id -nG` → `vgpnk docker input wheel` — **no `systemd-journal` membership**; nevertheless
  `journalctl -b -n 2` rc=0 and all censuses below worked.
- `/var/log/journal` = `drwxr-sr-x root systemd-journal` with ACL marker `+`;
  `getfacl -p /var/log/journal` shows `group:wheel:r-x`, `group:adm:r-x` and the same as default
  ACL ⇒ read access comes from the **wheel ACL**. (Cross-ref: `-Qkk` flagged `/var/log/journal`
  GID 981 `systemd-journal` — `package-state-plane.md:200`.)
- `journalctl --user` also works (uid-1000 slice; same coredump-only err set as §2).

## 2. Error entry census — boot 0

### 2.1 Entries vs lines, again

| measure | value | command (capture 11:40) |
|---|---|---|
| err **entries** (P≤3) | **247** | `journalctl -b -p err -o json --no-pager \| wc -l` |
| err **raw lines** | **63 245** | `journalctl -b -p err --no-pager \| wc -l` |
| ratio | ≈ **256 lines per entry** | coredump dissections are multi-line messages |

Full-boot priority distribution at 11:44 (`journalctl -b -o json --no-pager | jq -r '.PRIORITY' |
sort | uniq -c`): **17 588 entries** = 8952 warn + 8207 info + 211 crit + 137 notice + 41 debug +
40 err; no alert/emerg. The same distribution at 11:42 gave 17 571 — counts grow while the storm
runs; every number in this note is a capture, not a constant.

### 2.2 Class table (P≤3) + coredump cross-count

| class | priority | entries |
|---|---|---|
| `systemd-coredump` | 2 (crit) | 207 |
| `kernel` | 3 (err) | 38 |
| `sddm-helper` | 3 | 1 |
| `limine-snapper-sync` | 3 | 1 |
| **total** | | **247** |

- Coredump cross-count: `coredumpctl list --since "2026-10-13 10:57:58" --json=short --no-pager |
  jq 'length'` at 11:41:52 = **208**; classes (sig/exe via jq): godot 148 (145 present + 3 missing),
  node 47, python3.14 4 (SIGSEGV), grok-bot 3 (SIGBUS), chrome_crashpad 2, typora 2, electron 1,
  bash 1 (SIGSEGV). Journal err coredump entries = 207 at 11:40 vs coredumpctl 208 at 11:41 —
  one crash apart in ~2 min [inference: count drift, not an anomaly]. Round-1 carried 198 — the
  storm continues; root cause out of this plane (report to the owning lane).
- Kernel err classes (38): 20 × `critical target error, dev sr0, sector …` + 15 × `Buffer I/O
  error on dev sr0 …` (boot-only 11:02:03–06; cross-ref `driver-firmware-plane.md:163-165`),
  1 × `virt/tdx: TDX not supported by the host platform`, 1 × OOM kill (Oct 13 23:44:30,
  `python3 … anon-rss:27873696kB … oom_score_adj:200`), 1 × empty MESSAGE (blank printk at err level).

## 3. Warn entry census — boot 0

Capture 11:40 — `journalctl -b -p warning -o json --no-pager > warn.json`:

| measure | value | command |
|---|---|---|
| warn+ entries (P≤4) | **9 172** | `jq -s 'length' warn.json` |
| warn-only entries (P4) | **8 925** | `jq` filter `PRIORITY=="4"` |
| warn+ raw lines | **72 177** | `journalctl -b -p warning --no-pager \| wc -l` (trap again) |

warn-only class split (entries):

| class | entries | anchor |
|---|---|---|
| kernel, total | 8 875 | `._TRANSPORT=="kernel"` |
| ├ `[UFW BLOCK]` | 8 811 | message `startswith("[UFW BLOCK]")`; subclasses 4364 IPv6/UDP, 3409 IPv4/TCP, 1030 IPv4/UDP, 8 misc |
| └ non-UFW kernel | 64 | mostly one OOM splat logged at warn level (header `GpuWatchdog invoked oom-killer`, 23:44) + 2 nvidia load lines + 2 sd cache lines + 1 workqueue truncation + 1 bluetooth + 1 nvme NGUID |
| journal transport | 48 | pipewire 24, wireplumber 6, pipewire-pulse 6, xdg-desktop-portal-gtk 4, xdg-desktop-portal 3, dbus-broker-launch 2, systemd-networkd 1, systemd 1, empty identifier 1 |
| syslog transport | 2 | sddm-helper 1 (`gkr-pam: no password is available for user`), limine-snapper-sync 1 (§3.2) |

- **UFW is the warn floor**: 8 811 of 8 925 warn-only entries (98.7 %) are `[UFW BLOCK]` firewall
  noise that accumulates with live traffic (round-1 measured 8191 such *lines* at 09:54; this
  capture: 8811 *entries* at 11:40). Classification by message prefix is the bounded route.
- Non-kernel warn entries are the usual pipewire/portal chatter at boot + session start
  (same classes as `systemd-user-plane.md:18-23`).

### 3.1 limine-snapper cross-ref (reported, not absorbed)

Boot 0 at 11:02:05 (`journalctl -b -o short-iso -g 'No Snapper config'`) logs, from both
`limine-snapper-watcher[1501]` and `limine-snapper-sync[1519]`:

- P4: `No Snapper config found for '/'. Creating a Snapper config named 'root' and single root snapshot.`
- P3: `No Snapper config found for '/'. Please configure Snapper and set SNAPPER_CONFIG_NAME in /etc/default/limine.`

Today `snapper list-configs` still prints a header-only table, rc=0 (re-measured 11:53).
The tool claims it "creat[es] a Snapper config"; snapper shows none — the rollback-net question
(`update-safety-note.md:286-311`) needs a re-audit. Reported to the update-safety plane / operator.

## 4. Failed-service history — 13 retained boots

- This boot: `systemctl --failed --no-pager` → `0 loaded units listed.` rc=0;
  `systemctl list-units --state=failed --all --no-pager` → same; `is-system-running` → `running`
  (and `--wait` → `running`).
- Sweep across all retained boots (`journalctl --no-pager -p warning -g '<P>' -o json |
  jq -s 'length'`, P = `Failed to (start|load|activate|stop|reload|restart|mount|set up)|entered
  failed state|failed with result|Start request repeated|Dependency failed`, 11:43):

  **36 entries total**; per-boot samples: 0:3, −1:3, −2:3, −5:3, −11:3, −12:0. All 36 are
  `/usr/lib/xdg-desktop-portal[N]: Failed to load RealtimeKit property: … ServiceUnknown` — 3 per
  user session. `journalctl --user … | jq -s 'length'` = 36 (the same set).
  ⇒ **zero unit-activation failures in 13 retained boots**; the only `Failed to` lines are
  user-session portal warnings.
- Stricter pattern (`Failed to start|entered failed state|failed with result|Start request
  repeated`) = 0 matching entries in every sampled boot (0, −1, −5, −12 → `-- No entries --`, rc=1).
- Bounds of the negative claim: the sweep is limited to priority ≤ 4 and to the pattern set — a
  unit dying with other wording would not be caught. Crossing evidence: no `entered failed`
  anywhere, current failed = 0, all five timer services `Result=success` (§6), and the round-1
  user-scope audit (0 failed user units — `systemd-user-plane.md:16`).
- Method trap kept (§10.1): `journalctl -g` with no match prints `-- No entries --` on **stdout**,
  so `| wc -l` reads 1 "match" per boot; the first-pass per-boot count of 1 was this artifact.

## 5. Boot duration shape — and the silent early phase

### 5.1 Current boot (`systemd-analyze`, 11:39)

`18.234s (firmware) + 5.479s (loader) + 4min 3.328s (kernel) + 3.736s (userspace) = 4min 30.778s`;
graphical.target reached after 3.736s in userspace (rc=0). The identical line was logged at
11:02:05 (`journalctl -b -g 'Startup finished'`).

`systemd-analyze blame` top: man-db 3.371s, dev-mapper-root.device 1.157s,
systemd-tmpfiles-setup-dev-early 1.026s, systemd-userdbd 1.015s, plocate-updatedb 830ms,
systemd-tmpfiles-setup 461ms. Critical chain: `graphical.target@3.736s → sddm@3.736s →
plymouth-quit@3.539s → … → systemd-journal-flush@2.849s → var-log.mount@2.845s →
dev-mapper-root.device@803ms+1.157s`.

### 5.2 History across the 13 boots — bimodal kernel phase

Sweep: `journalctl -b <n> -g 'Startup finished'` per boot (11:52). Every retained boot carries
exactly one `systemd[1]: Startup finished …` line (25 `Startup finished` lines in total incl.
user-manager instances; see Appendix for the count command).

| boot | firmware | loader | kernel | userspace | total |
|---|---|---|---|---|---|
| −12 | — | — | — | — | 1.807 s |
| −11 | 19.914 s | 10.488 s | 1 m 53.512 s | 3.582 s | 2 m 27.498 s |
| −10 | 18.567 s | 8.004 s | 35.189 s | 3.145 s | 1 m 4.907 s |
| −9 | 19.192 s | 8.005 s | 25.104 s | 3.175 s | 55.478 s |
| −8 | 19.180 s | 8.005 s | **2 h 57 m 56.876 s** | 3.171 s | 2 h 58 m 27.234 s |
| −7 | 16.897 s | 4.974 s | 14.941 s | 3.171 s | 39.985 s |
| −6 | 48.513 s | 8.006 s | **1 h 28 m 30.454 s** | 3.148 s | 1 h 29 m 30.122 s |
| −5 | 18.454 s | 7.997 s | **1 h 43 m 6.782 s** | 3.194 s | 1 h 43 m 36.429 s |
| −4 | 18.390 s | 7.998 s | **2 h 57 m 27.702 s** | 3.200 s | 2 h 57 m 57.292 s |
| −3 | 18.473 s | 8.011 s | 12.061 s | 3.142 s | 41.688 s |
| −2 | 19.632 s | 7.994 s | **26 m 55.902 s** | 3.228 s | 27 m 26.757 s |
| −1 | 18.929 s | 5.482 s | 20.821 s | 4.732 s | 49.966 s |
| 0 | 18.234 s | 5.479 s | **4 m 3.328 s** | 3.736 s | 4 m 30.778 s |

Shape read: userspace is stable (**3.1–4.7 s, 13/13**), firmware/loader normal-ish (17–48 s /
5–10 s); the kernel phase is **bimodal** — 12–114 s on six boots, **26 m – 2 h 58 m on six**, and
boot 0 = 4 m. "Kernel" here is systemd's own accounting: kernel start → PID1 start.

### 5.3 The kernel phase equals the first-record monotonic (measured rule)

Loop 11:52 — `journalctl -b <n> -o short-monotonic --no-pager | head -1` vs the boot's kernel
phase (§5.2):

| boot | kernel phase s | first-record monotonic s | Δ |
|---|---|---|---|
| −11 | 113.512 | 114.337 | +0.825 |
| −10 | 35.189 | 36.024 | +0.835 |
| −9 | 25.104 | 25.938 | +0.834 |
| −8 | 10676.876 | 10677.705892 | +0.830 |
| −7 | 14.941 | 15.778 | +0.837 |
| −6 | 5310.454 | 5311.270019 | +0.816 |
| −5 | 6186.782 | 6187.620945 | +0.839 |
| −4 | 10647.702 | 10648.538839 | +0.837 |
| −3 | 12.061 | 12.893 | +0.832 |
| −2 | 1615.902 | 1616.716617 | +0.815 |
| −1 | 20.821 | 21.630890 | +0.810 |
| 0 | 243.328 | 244.159301 | +0.831 |

⇒ 12/12: **kernel phase = first-record monotonic − 0.81…0.84 s**. The first journal record marks
PID1/userspace logging start, so systemd-analyze's "kernel" figure is exactly the time from kernel
start to that point — and boot 0 anchors it by wall clock: `uptime -s` 10:57:58 → first record
11:02:03 = 245 s wall vs 244.16 s monotonic. The two clocks agree within 1 s ⇒ for boot 0 the
number is **real elapsed time**, not a clock artifact. Within every boot the clock runs at real
rate (example boot −8: first→last monotonic 10677.7 → 159036.1 = 148 358 s; its wall span
2026-10-05 01:08:08 → 2026-10-06 18:20:46 = 148 358 s).

- [inference] The hour-scale kernel phases are **pre-userspace dwell** (kernel + initramfs), not
  slow compute: the machine sat in early boot before PID1/journald existed. On this host the
  initramfs is busybox-style (`/etc/mkinitcpio.conf:55` → `HOOKS=(base udev autodetect microcode
  modconf kms keyboard keymap consolefont block encrypt filesystems fsck)`) — the `encrypt` hook
  prompts for the LUKS passphrase; the dwell range matches human response (12 s typed quickly …
  2 h 58 m unattended). Candidate mechanism, **not proven**: `/etc/crypttab` is mode 600 root
  (contents not read, BLOCKED), so a configured keyfile cannot be excluded.
- [observed] Each boot's resume attempt concludes with `PM: Image not found (code -22)` — one per
  boot, at the start of the record stream. Its position among initramfs steps is [unknown]
  (kernel-time attempt vs initramfs userspace; sweep for actual hibernation events:
  `hibernation entry`/`hibernation exit` = 0 lines in the whole retained journal).
- Cross-ref `SKILL.md:43`: the boot-gap question stays [inference, unproven]; this note replaces
  the single-boot gap with the 13-boot table + the Δ rule, and shifts the leading hypothesis from
  "journal flush/mount delay" toward "real initramfs dwell" (var-log.mount happens at userspace
  2.845 s — *after* PID1/logging start — so mount delay cannot explain the gap).
- Bounds: prior-boot phases exist only for the 13 retained boots; phases are systemd's accounting.

## 6. Timer plane — last-run vs next-run drift (system scope, 5 timers)

`systemctl list-timers --all --no-pager` (11:41, 8 lines = header + 5 rows + blank + `5 timers
listed.`); exact values via `systemctl show <timer> -p …`; cadence from the unit files:

| timer | cadence (unit file) | LAST (actual) | NEXT | interval last→next | offset / window | Result |
|---|---|---|---|---|---|---|
| `shadow.timer` | daily, AccuracySec=12h, Persistent (`/usr/lib/systemd/system/shadow.timer:5-7`) | Wed 2026-10-14 00:00:13 | Thu 2026-10-15 00:00:00 | 23 h 59 m 47 s | +13 s after nominal 00:00 — inside 12 h accuracy | success |
| `plocate-updatedb.timer` | daily, RandomizedDelaySec=1h, AccuracySec=6h, Persistent (`:5-8`) | Wed 00:34:38 | Thu 00:40:30 | 24 h 5 m 52 s | +34 m 38 s / +40 m 30 s — inside 1 h delay | success |
| `man-db.timer` | daily, RandomizedDelaySec=12h, Persistent, WantedBy=timers.target (`:6-8,11`) | Wed 03:50:48 | Thu 09:50:40 | 29 h 59 m 52 s | +3 h 50 m 48 s / +9 h 50 m 40 s — inside 12 h delay | success |
| `systemd-tmpfiles-clean.timer` | OnBootSec=15min, OnUnitActiveSec=1d (`:16-17`) | Wed 11:13:22 | Thu 11:13:22 | exactly 24 h (monotonic 1 d 15 m 23.980 s → 2 d 15 m 23.981 s, Δ = +0.9 ms) | first run ≈ boot + 24 h 15 m; no randomization | success |
| `archlinux-keyring-wkd-sync.timer` | weekly, Persistent, RandomizedDelaySec=1week (`:5-7`) | Sat 2026-10-10 03:53:00 | Sat 2026-10-17 04:18:20 | 7 d 0 h 25 m 20 s | inside 1-week delay | success |

- Services behind the timers: `systemctl show shadow.service plocate-updatedb.service man-db.service
  systemd-tmpfiles-clean.service archlinux-keyring-wkd-sync.service -p Result -p ExecMainStatus -p
  NRestarts` → all `success` / `0` / `0`.
- **Drift verdict:** every LAST sits inside its unit's declared randomization/accuracy window;
  interval variability (24 h 05 m 52 s / 29 h 59 m 52 s / 7 d 0 h 25 m 20 s) is the documented
  per-occurrence `RandomizedDelaySec` draw [inference from unit text + measured values], not
  lateness; no overdue or missed trigger observed; every last run succeeded.
- `list-timers` quirk: `PASSED` prints `-` when LAST predates the current boot (keyring timer,
  LAST in boot −5).
- Enablement nuance: 4 timers are `static` (no [Install]), and the active set includes
  `man-db.timer` with `UnitFileState=disabled`, preset `disabled` — yet `active (waiting) since
  2026-10-13 11:02:05`. All five are started via **package-shipped vendor symlinks** in
  `/usr/lib/systemd/system/timers.target.wants/` (owners via `pacman -Qo`: `archlinux-keyring`,
  `plocate`, `shadow`, `systemd`, `man-db`). "disabled" does not mean "will not run" for
  vendor-wants units. (Mirror case, user scope: `omarchy-battery-monitor.timer` disabled and
  genuinely not loaded — `systemd-user-plane.md:88-92`.)
- Census counts: `systemctl list-unit-files --type=timer --no-pager` = 21 lines = header + **18
  unit files** + footer (13 disabled, 5 static, 1 static template `mdadm-last-resort@.timer` not
  started); loaded timer set = 5.
- Cross-ref: user-scope timers (`ai-usage.timer` etc.) are covered in `systemd-user-plane.md:80-95`
  — not re-measured here.

## 7. Privilege gates — BLOCKED arms (recorded, not escalated)

| probe | measured | arm |
|---|---|---|
| `dmesg` (raw kernel ring) | rc=1, `dmesg: read kernel buffer failed: Operation not permitted`; `/proc/sys/kernel/dmesg_restrict` = `1` | BLOCKED by design; fallback `journalctl -k` works (cross-ref `driver-firmware-plane.md:9-11`) |
| `ls /boot` | rc=2, `Permission denied` | BLOCKED (operator probe; `SKILL.md:117-119`) |
| `bootctl status` | rc=1; prints the System block (UEFI 2.110, American Megatrends 5.41, Secure Boot disabled, TPM2 no, Measured UKI no) then `Failed to read "/boot/EFI/systemd"` / `Failed to open '/boot/loader/loader.conf'` | PARTIAL / BLOCKED |
| `/etc/crypttab` (keyfile question) | mode `600 root` — contents **not** read | BLOCKED (shape-only) |
| journal itself | readable (§1.3) — wheel ACL; `journalctl`/`coredumpctl`/`systemd-analyze` all answered | not blocked; no `sudo` used |

## 8. Verdict arms — journal/boot plane (fixed vocabulary)

| sub-probe | measured 2026-10-14 | arm |
|---|---|---|
| err entry census (boot 0) | 247 entries (11:40) → 251 (11:44); coredump 207 → 211; godot storm live | DEGRADED (named defect: crash storm) |
| warn census | 8 925 warn-only; 8 811 are `[UFW BLOCK]` floor; OOM splat fragments at warn | DEGRADED (noise floor classed) |
| failed-service history | 0 unit failures in 13 retained boots; only portal warnings | HEALTHY (within retention) |
| boot duration shape | userspace 3.1–4.7 s stable; pre-userspace dwell 12 s → 2 h 58 m; mechanism open | DEGRADED (named unknown) |
| timer drift | 5/5 last runs success; all triggers inside declared windows | HEALTHY |
| privilege arms | dmesg / `ls /boot` / `bootctl` / `/etc/crypttab` BLOCKED; journal readable | recorded; plane still answers |

Composed (strongest fired): **DEGRADED** — consistent with the plane row at `SKILL.md:43`, which
this note now backs with the 13-boot census and the Δ rule.

## 9. Method lessons (measured, reusable)

1. **Entries, not lines**: err 63 245 lines / 247 entries (≈256:1); warn+ 72 177 / 9 172. Count with
   `-o json | wc -l`; classify with jq on `PRIORITY` / `SYSLOG_IDENTIFIER` / `_TRANSPORT`.
2. **`-g` no-match prints `-- No entries --` on stdout** → `| wc -l` = 1. Count matches with
   `-o json | jq -s 'length'` (or check rc=1).
3. **`NextElapseUSecMonotonic` / `LastTriggerUSecMonotonic` are monotonic timestamps** (clock from
   boot), not deltas — verify with LastTrigger + interval (tmpfiles: Δ = 24 h + 0.9 ms). First read
   as "time-to-next" produced an apparent contradiction with `list-timers` (erratum §10.2).
4. **Grep anchors must match the message start**: `startswith("UFW BLOCK")` matched 0;
   the message starts `[UFW BLOCK]`. Use the bracket.
5. **`jq -r` renders MESSAGE with embedded newlines as several lines** (64 non-UFW kernel entries
   printed as 71 rows this session) — count entries, not printed lines.
6. **Pipelines hide rc**: `dmesg | head` reported 0 (head's rc); direct `dmesg` rc=1.
7. **Counts drift live during a crash storm** — re-measure, never cache (err 247→251 in ~4 min;
   coredump 198→208 in a day).
8. `list-timers` `PASSED` = `-` for a LAST trigger that predates the current boot.

## 10. Errata (append-only)

- [2026-10-14 probe] **RETRACTED count**: the first per-boot failed-pattern count of "1 line"
  was the `-- No entries --` notice counted by `wc -l`. Corrected: 0 strict-pattern matches; 36
  broad matches, all portal RealtimeKit warnings. Kept as method evidence (§9.2).
- [2026-10-14 probe] **CORRECTED reading**: `NextElapseUSecMonotonic=2d 15min 23.981234s` was
  first read as a delta ("2 days to next fire") and set against `list-timers`' "23 h" — wrong: it
  is a monotonic timestamp since boot (LastTriggerUSecMonotonic + 1 d). No timer discrepancy.
- [2026-10-14 probe] **CORRECTED filter**: UFW count via `startswith("UFW BLOCK")` = 0; correct
  anchor `[UFW BLOCK]` → 8811.
- [2026-10-14 probe] **CORRECTED rc**: `dmesg` rc read through `| head` as 0; direct rc=1.
- [2026-10-14 probe] **First-pass boot-gap framing superseded**: the round-2 erratum
  (`systemd-user-plane.md:215-221`) treated the gap as a single-boot question; this note measures
  it for all 13 boots (§5.2–5.3) and adds the "kernel phase = first-record monotonic − 0.83 s"
  rule. The mechanism (initramfs dwell vs resume artifact) remains [inference, unproven]; the
  var-log.mount candidate is now weaker (§5.3).

## 11. Unknowns (open)

- Pre-userspace dwell mechanism (§5.3): LUKS prompt response time vs resume-scan vs other;
  `/etc/crypttab` unreadable (keyfile?) — operator probe.
- `PM: Image not found` writer/phase: kernel-time attempt vs initramfs userspace; why present on
  every boot when `resume=` targets a LUKS-mapped device.
- Coredump root cause (godot SIGABRT storm; node/typora/electron; new python3.14 SIGSEGV) —
  process-level, out of this plane; report to the owning lane.
- Whether unit failures exist outside the sweep's pattern set or below priority 4.
- Effective journald retention (`SystemMaxUse`, rotation date of boot −12): shipped config is
  defaults-only; effective value not derived.
- `limine-snapper-sync` "Creating a Snapper config" vs empty `snapper list-configs` (§3.1) —
  update-safety plane re-audit.
- Exact semantics of journald's monotonic stamp for the pre-journald kernel backlog (why the
  banner carries the read-time stamp rather than ~0.8 s) — reasoned here, not proven.

## 12. Sources

- Commands: as embedded, with capture times; full set in the Appendix.
- Files read: the five timer unit files as tabulated; `/etc/mkinitcpio.conf:55`;
  `/etc/systemd/journald.conf` (all directives commented); `/proc/sys/kernel/dmesg_restrict`;
  `/proc/cmdline`; `/var/log/journal` + `getfacl -p`; `pacman -Qo` on the five vendor symlinks;
  `systemctl show` property sets as quoted.
- Cross-refs: `systemd-user-plane.md` (timers / coredumps / boot-gap erratum),
  `driver-firmware-plane.md:9-11,163-165` (kernel ring, sr0), `update-safety-note.md:286-311`
  (rollback net), `SKILL.md:43,117-119,215-220`.
- Scratch (ephemeral, `/tmp/tsukuroi-r3-1-scratch/`): `context.txt`, `failed.txt`, `timers.txt`,
  `timerdetail.txt`, `analyze.txt`, `err.json`, `warn.json`, `bootshape.txt`, `blocked.txt`,
  `blocked2.txt`, `timers2.txt`, `enablement.txt`, `anchors.txt`, `finals.txt`,
  `startup-history.txt`, `crossref.txt`, `bootgap.txt`, `bootgap2.txt`, `lastcheck.txt`,
  `crypt.txt`.

## Appendix — probe command set (reproducible)

```bash
journalctl --list-boots --no-pager; journalctl --disk-usage
journalctl -b -p err -o json --no-pager | wc -l
journalctl -b -p err --no-pager | wc -l
journalctl -b -o json --no-pager | jq -r '.PRIORITY' | sort | uniq -c
journalctl -b -p warning -o json --no-pager > warn.json; jq -s 'length' warn.json
jq -s '[.[]|select(.PRIORITY=="4" and ._TRANSPORT=="kernel")]|length' warn.json
jq -s '[.[]|select(.PRIORITY=="4")|select((.MESSAGE|tostring)|startswith("[UFW BLOCK]"))]|length' warn.json
coredumpctl list --since "2026-10-13 10:57:58" --json=short --no-pager | jq 'length'
systemctl --failed --no-pager; systemctl list-units --state=failed --all --no-pager; systemctl is-system-running
journalctl --no-pager -p warning -g 'Failed to (start|load|activate|stop|reload|restart|mount|set up)|entered failed state|failed with result|Start request repeated|Dependency failed' -o json | jq -s 'length'
systemd-analyze; systemd-analyze blame --no-pager | head -25; systemd-analyze critical-chain --no-pager | head -35
journalctl --no-pager -g 'Startup finished'            # 25 lines incl. user-manager instances
journalctl -b <n> -o short-monotonic --no-pager | head -1   # and tail -1
journalctl --no-pager -g 'PM: Image'
journalctl --no-pager -g 'hibernation entry|hibernation exit'
systemctl list-timers --all --no-pager
systemctl show <timer> -p LastTriggerUSec -p LastTriggerUSecMonotonic -p NextElapseUSecRealtime -p NextElapseUSecMonotonic -p AccuracyUSec -p RandomizedDelayUSec -p Persistent -p Unit -p Result
systemctl show <svc> -p Result -p ExecMainStatus -p NRestarts
systemctl list-unit-files --type=timer --no-pager
pacman -Qo /usr/lib/systemd/system/timers.target.wants/<name>.timer
grep -nE 'OnCalendar|OnBootSec|OnUnitActiveSec|AccuracySec|RandomizedDelaySec|Persistent|WantedBy' /usr/lib/systemd/system/<name>.timer
dmesg >/dev/null 2>&1; echo rc=$?
bootctl status; ls /boot
getfacl -p /var/log/journal
```

## 13. Errata (round 4)

- 2026-10-14 (TSUKUROI-ERR-S sweep) — **missing cross-ref: §4's failed-unit-history claim is
  superseded.** `boot-plane.md` §5 (round 4, TSUKUROI-R4-3) re-measured this note's §4 claim
  ("zero unit-activation failures in 13 retained boots") with case-insensitive patterns and found
  **4 failure records**; the round-3 miss came from the strict lowercase pattern `failed with
  result` vs systemd's `Failed with result` and a broad set that excluded `Failed to enqueue`.
  This note is not edited (append-only), but its §10 errata carried no pointer to that
  supersession — added here. §5 duration table and the Δ rule were re-verified unchanged there.
  [observed: `boot-plane.md` §2.2, §5; live `journalctl` re-reads]
- 2026-10-14 — **index row also stale:** `corpus/README.md:13` still repeats the superseded
  "failed-service history **0 unit failures in 13 retained boots**" line for this note. That file
  is outside this lane's write scope — flagged for the index owner, not edited. [observation]
- 2026-10-14 — **md5-pin consequence:** this append changes this file's md5 and line count, so
  `host-health-report-r3.md` §5's pin for this note (`16d4047e8b03deec69773d2cc0b1b75c`, 411
  lines) is superseded as of this block; post-append values recorded in that report's round-4
  errata. [observation]

## Erratum (2026-10-19, fleet round 1) — D5: Effective HOOKS come from drop-ins
Superseded (`corpus/knowledge/journal-boot-plane.md:244-245`): “`/etc/mkinitcpio.conf:55` → `HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block encrypt filesystems fsck)`”.
Correction: that base-file citation is not the effective host configuration; mkinitcpio reads the host's configuration drop-ins. The host's `omarchy_hooks.conf` defines `HOOKS=...btrfs-overlayfs`, and `omarchy_resume.conf` adds `HOOKS+=(resume)`.
Source: S014 https://wiki.archlinux.org/title/Mkinitcpio § Configuration: “Drop-in configuration files are also supported”.
[obs] Re-opened 2026-10-19: `grep -Hn '^HOOKS' /etc/mkinitcpio.conf.d/*.conf` → `omarchy_hooks.conf:1:HOOKS=(base udev plymouth keyboard autodetect microcode modconf kms keymap consolefont block encrypt filesystems fsck btrfs-overlayfs)` and `omarchy_resume.conf:1:HOOKS+=(resume)`; `grep -n 'drop-in' /var/log/pacman.log` → lines 1991-1993 record use of `nvidia.conf`, `omarchy_hooks.conf`, `omarchy_resume.conf`.

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — read-only `journalctl`, `systemctl`, `systemd-analyze`, `coredumpctl`, `bootctl`, pacman owner and ACL probes on host `plazir27`, 2026-10-14; S014 https://wiki.archlinux.org/title/Mkinitcpio § Configuration re-opened 2026-10-19.
verified-at: 2026-10-14 (the original journal/boot capture window; effective HOOKS drop-ins re-opened 2026-10-19).
recheck: 30d; procedure: Appendix probe command set; use `-o json` entry counts and re-read active mkinitcpio drop-ins.
supersedes the pointer-only recheck: line above.


## R18-FRESHNESS — snapper list-configs premise (journal 147-149)

Dated freshness re-verification, 2026-10-20 16:06 -03, from S060 (fresh R18 read-only capture). The sentence above is a historical 11:53 reading and stays unchanged. Current use is superseded: /etc/snapper/configs lists home and root. Observed now: /etc/snapper/configs lists home and root (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:76-77`; `SNAPPER_CONFIGS="root home"` at `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:80`). The `snapper list-configs` output itself was not re-run in S060, so its current table is unverified. The rollback-net re-audit (`update-safety-note.md:286-311`) remains open. Scope: supersedes current-use only; read-only; no package, service, snapper or reboot action is cleared.

## R18-FRESHNESS — snapper config premise in unknowns (journal 364-365)

Dated freshness re-verification, 2026-10-20 16:06 -03, from S060. The unknown premise "empty `snapper list-configs`" is superseded for current use. Observed now: /etc/snapper/configs lists home and root (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:80`, `SNAPPER_CONFIGS="root home"`). The boot-0 "Creating a Snapper config" lines (§3.1, 11:02:05) stay historical, and the update-safety re-audit stays open. `snapper list-configs` was not re-run in S060. Scope: supersedes current-use only; read-only; historical snapshots preserved; no package, service, snapper or reboot action is cleared.

## R18-FRESHNESS — configured HOOKS versus image hooks (journal 244-245)

Dated freshness re-verification, 2026-10-20 16:06 -03, from S060 and the R17 image extraction (S051). The HOOKS list quoted at :244-245 is a historical read of `/etc/mkinitcpio.conf:55`; it was not re-read in S060 and is superseded for current-image use. Image scope: the default UKI `omarchy_linux.efi` extracts to VERSION 42.2 with HOOKS="udev plymouth keymap consolefont encrypt resume" (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:177`; R17 B:173-178), which differs from the configured list at :244-245. The R18 host runs kernel 7.2.11 (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:6`) with mkinitcpio-42.2-1 installed (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:34`). The v42 init is busybox-based and uses /sysroot (S053, S058). Historical configuration is preserved. Scope: read-only; no image rebuild, package, boot or reboot action is cleared.


## R18-RECHECK — steer-safe procedure

Supersedes this entry's historical pointer-based recheck procedure for a steer forbidding package-manager execution (QUALITY26). Historical command receipts remain historical; do not run their backticked package commands or the live host census merely by following the old section pointer. This is an actual bounded read/compare procedure, not a whole-host clearance or a new host measurement.

- Read the installed-name/version metadata with `ls -1 /var/lib/pacman/local`; for each package whose recorded field is being rechecked, read its exact `/var/lib/pacman/local/<pkg>-<ver>/desc` and compare name, version, install date, reason and validation fields with the dated table. Directory presence does not certify file integrity or current repository reachability.
- Read repository-file inventory and timestamps with `ls -1 /var/lib/pacman/sync` and `stat -c '%y %n' /var/lib/pacman/sync/*.db`. Mtime is an upstream stamp, not local acquisition time; a present database is not proof it is configured.
- Read relevant transaction events using `tail -n 80 /var/log/pacman.log`; distinguish invocation headers from ALPM completion events, preserve capture time and exit status, and never infer a current pending-update count from this history.

- Recheck configuration names with `ls -1 /etc/snapper/configs`; use `systemctl show earlyoom.service -p ActiveState -p UnitFileState --no-pager` only for those named service properties. Config presence, enabled state and active state answer different questions; do not infer snapshot restoration, active timer totals or historical kill attribution.

Record observed values and unresolved questions separately. Uncaptured pending updates, signature validity, exact foreign/orphan classification, private mount views, historical provenance events and recovery feasibility remain unknown until their own authorized evidence is obtained. No installation, restart, rebuild, subvolume action or boot write is authorized.
