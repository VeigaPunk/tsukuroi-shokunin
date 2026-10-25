# timer-drift plane — enabled user timers, plazir27 (probe 2026-10-14)

source: live read-only probes, host `plazir27`, user `vgpnk` uid 1000, non-root —
`systemctl --user` (`list-unit-files` / `list-timers` / `list-units` / `show` / `is-active`),
`journalctl --user` (`-u`, `-o json`, `--list-boots`), `date`, `python3 clock_gettime`
(CLOCK_MONOTONIC + CLOCK_BOOTTIME), `/proc/uptime`, `systemd-analyze --user unit-paths`,
read-only greps of `/var/log/pacman.log`. Companion corpus: `systemd-user-plane.md:80-95`
(round-1 snapshot of the same surface), `journal-boot-plane.md:259-303` (system-scope timer
table — not re-measured here), `tools/tsukuroi-census.sh:94-97` (the armed-state arm).
Nothing outside this repo was modified; no unit was started, stopped, reloaded or edited.
Scratch: `/tmp/w5-tsukuroi-s5-2-timer-drift/` (sample.log, all_starts3.tsv).

verified-at: 2026-10-14 13:59–14:08 -03 (live snapshot + a ≈20–40 s sampler spanning one full
fire cycle); interval history from the retained user journal, 2026-10-06 16:21 → 2026-10-14 14:07.

recheck: §10 command set. The interval classification is reproducible from one `jq` extraction
plus the §4.2 one-liner; the snapshot rows in §2 are live values and will have moved.

Notation: **[obs]** measured · **[inf]** inference · **[unk]** unknown. Counts carry their command.

## 0. Scope and the three clocks

**Scope.** "Enabled user timers" = timer units inside the `systemctl --user` scope with
`UnitFileState=enabled` (tsukuroi `PROVINCE.md:8-9`). Measured size of that set on this host:
**1** (§2). System-scope timers are a different plane — 5 of them, already measured in
`journal-boot-plane.md:259-303`; §6 records only the one boundary fact that touches this plane.

**The three clocks** (one call, 2026-10-14 14:01:41 -03):

| clock | value | how read |
|---|---|---|
| wall | `1791997301.359` | `date +%s.%N` |
| CLOCK_MONOTONIC | `97422.477` | `python3 -c 'time.clock_gettime(time.CLOCK_MONOTONIC)'` |
| CLOCK_BOOTTIME | `97422.477` | same call, `time.CLOCK_BOOTTIME`; equals `/proc/uptime` field 1 (`97422.47`) |

- **[obs]** `CLOCK_MONOTONIC == CLOCK_BOOTTIME` to the millisecond ⇒ **no suspend since boot**.
  Independent sweep: `journalctl --no-pager | grep -E 'PM: suspend (entry|exit)|Suspending system|
  Reached target Sleep'` → **0 matches** across the whole retained journal. The wall-vs-monotonic
  divergence row in §5 is therefore a counterfactual on this host, marked as such.
- **[obs]** monotonic→wall conversion measured in the same call:
  `offset = wall − monotonic = 1791899878.882 s`. Cross-check: `LastTriggerUSecMonotonic`
  `1d 2h 59min 9.819010s` (= 97149.819010 s) → wall `13:57:08.701` = the `list-timers` LAST cell. ✓
- **[inf]** every timer on this host is monotonic (no `OnCalendar` anywhere in the enabled set,
  §3), so timers are anchored to CLOCK_MONOTONIC and "on time" can only be defined as an
  *interval since the target's last activation*, never as a wall-clock instant.

## 1. Unit-path sweep (the inventory is closed)

- **[obs]** `systemd-analyze --user unit-paths | wc -l` → **18** roots (last line
  `/run/user/1000/systemd/generator.late`). Sweeping every root
  (`for r in $(systemd-analyze --user unit-paths); do find "$r" -maxdepth 2 -name '*.timer'; done
  | sort -u`) → exactly **4** paths, no more:

```
/home/vgpnk/.config/systemd/user/ai-usage.timer                    (unit)
/home/vgpnk/.config/systemd/user/omarchy-battery-monitor.timer     (unit)
/home/vgpnk/.config/systemd/user/timers.target.wants/ai-usage.timer (enablement symlink)
/usr/lib/systemd/user/systemd-tmpfiles-clean.timer                 (unit, system-shipped)
```

- **[obs]** `~/.local/share/systemd/user/` does not exist; no transient/generated timers
  (`/run/user/1000/systemd/transient` empty of `*.timer`).
- **[obs]** `systemctl --user list-unit-files --type=timer --all --no-pager` → 3 rows
  (`ai-usage.timer` enabled/enabled, `omarchy-battery-monitor.timer` disabled/enabled,
  `systemd-tmpfiles-clean.timer` disabled/enabled); `list-units --type=timer --all` → **1**;
  `list-timers --all` → `1 timers listed.`
  (Column semantics: `STATE` = `UnitFileState`, `PRESET` = the preset policy, which is *not*
  the runtime state — the round-3 note's vendor-wants nuance, `journal-boot-plane.md:297-301`.)

## 2. The enabled set at probe time (N=1)

`systemctl --user show <unit> -p LoadState -p ActiveState -p SubState -p UnitFileState
-p LastTriggerUSec -p NextElapseUSecMonotonic -p NextElapseUSecRealtime -p Triggers`

| unit | UnitFileState | LoadState | ActiveState (SubState) | want symlink | LastTrigger | NextElapse (monotonic) | target |
|---|---|---|---|---|---|---|---|
| `ai-usage.timer` | enabled | loaded | active (waiting) | yes | 2026-10-14 14:07:18 | 1 d 3 h 14 min 19.82 s | `ai-usage.service` |
| `omarchy-battery-monitor.timer` | disabled | loaded | inactive (dead) | **no** | *(empty)* | `infinity` | `omarchy-battery-monitor.service` |
| `systemd-tmpfiles-clean.timer` | disabled | loaded | inactive (dead) | **no** | *(empty)* | `infinity` | `systemd-tmpfiles-clean.service` |

- **[obs]** `timers.target.wants/` holds exactly one link (`ai-usage.timer → ~/.config/systemd/user/
  ai-usage.timer`, created 2026-10-06 16:21); the other two have no symlink, so they are not pulled
  into `timers.target` — that, not the `PRESET` column, is why they never run.
- **[obs]** live `list-timers --all` row at 14:07:51:
  `NEXT Wed 2026-10-14 14:12:18 -03 | LEFT 4min 27s | LAST Wed 2026-10-14 14:07:18 -03 | PASSED 32s ago`.

## 3. The contract, read off the one enabled unit

`~/.config/systemd/user/ai-usage.timer` (mtime 2026-10-06 16:21:10.097, 202 B):

| line | directive | consequence measured below |
|---|---|---|
| `:5` | `OnBootSec=30` | first-fire window only (fires at manager start in practice, §5.2 #1/#2/#5) |
| `:6` | `OnActiveSec=15` | first-fire window after every manager start |
| `:7` | `OnUnitActiveSec=300` | **P = 300 s**, the recurring cadence |
| `:8` | `Persistent=true` | no-op here: no `OnCalendar` ⇒ no catch-up for missed wall-clock windows (§4.3) |
| `:9` | `AccuracySec=10` | **A = 10 s**, the fire window `[P, P+A]` |
| `:10`,`:13` | `Unit=ai-usage.service`, `WantedBy=timers.target` | target exists; enabled via the wants link |

`systemctl --user show ai-usage.timer` → `RandomizedDelayUSec=0` `WakeSystem=no`
`OnClockChange=no` `OnTimezoneChange=no` `RemainAfterElapse=yes` `TimersCalendar=` *(none)*
`TimersMonotonic={OnUnitActiveUSec=5min;…}{OnActiveUSec=15s;…}{OnBootUSec=30s; next_elapse=30s}`.

Target `ai-usage.service` (mtime 2026-10-06 16:21): `Type=oneshot` `:5`, `TimeoutStartSec=180` `:6`,
`Nice=10` `:7`, optional `EnvironmentFile` `:9` (contents not read — secrets discipline),
`ExecStart=%h/.local/bin/ai-usage refresh` `:10`.

- **[obs]** no `OnCalendar` in the unit and `TimersCalendar=` empty ⇒ **the timer promises an
  interval, not a wall-clock instant.** Any drift table that compares it to a grid is measuring
  the wrong thing.
- **[obs]** trigger→activation latency, three consecutive cycles
  (`LastTriggerUSecMonotonic` vs `ExecMainStartTimestampMonotonic`, µs):
  `+0.740 ms` (13:57:08), `+0.620 ms` (14:02:11), `+0.646 ms` (14:07:18). Sub-millisecond ⇒ this
  delta is a *fault* discriminator (ms → s would mean a queued/blocked job), not a drift measure.

## 4. Measured interval history — 2,100 intervals, 9 boots, 0 late

### 4.1 Method

Every `Starting Probe AI CLI usage limits into cache...` record in the retained user journal
(`journalctl --user -u ai-usage.service -o json`; jq over `.MESSAGE`, `.__REALTIME_TIMESTAMP`,
`._BOOT_ID`), **paired inside each `_BOOT_ID`** — never across (§7.3).

- **[obs]** extraction size: `wc -l` → **2,109** records (cut: records ≤ the third sampled fire,
  2026-10-14 14:07:18.701); containing boots: **9** (the two earliest retained boots predate the
  unit, whose file mtime is 2026-10-06 16:21:10).
- **[obs]** pairing → **2,100** within-boot intervals + **8** boot-boundary gaps.

### 4.2 Classification (within-boot intervals only)

| class | rule | count | min | max |
|---|---|---|---|---|
| **on-schedule** | `P ≤ Δ ≤ P+A` (+50 ms tolerance) | **2,095** | 300.0035 s | 310.0093 s |
| **early / re-arm** | `Δ < P` | **5** | 9.991 s | 277.575 s |
| **late** | `Δ > P+A+0.05 s` | **0** | — | — |
| *boot-boundary gap* (not a class) | spans two `_BOOT_ID`s | *8* | *302.6 s* | *10 939.0 s* |

Shape inside the window (n = 2,095): median `310.0000`; **1,847 (88.2 %)** inside the
window-end band `[309.98, 310.02]`; **248 (11.8 %)** lower in `[300, 309.98)`; exactly
`310.000000` for only **6** — i.e. the mode is *the window's upper edge ± ≤12 ms*, and a drift
reading keyed on the mean (307.6 s in boot 0) or on float equality both misdescribe it.

- **[obs]** the lower draws are **bursty, not random**: 91 maximal runs of sub-band draws
  (median run 2, longest 12) covering 253 draws = the 248 lower-band draws + the 5 early fires.
  Typical runs: `… 12:16:08 304.871, 12:21:13 305.129, 12:26:18 303.871, 12:31:22 301.584,
  12:36:24 301.618, 12:41:25 300.432, 12:46:26 302.494` then back to a 310.000 stretch.
- **[obs]** current boot only: 318 starts / 317 intervals → 196 window-end band, 120 lower-band,
  1 early, 0 late.
- **[unk]** the mechanism that decides the draw inside `[P, P+A]` is not established (§9 U1).

### 4.3 The three measured facts that make "drift" meaningful

1. **`NextElapseUSecMonotonic` is the window's lower bound, not the fire time.** Measured over
   three consecutive cycles, `NextElapse − LastTrigger = 300.000947 / 300.000784 / 300.000850 s`
   (≡ P). Actual fires after that projection: `+2.55 s` (14:02:11.256 vs 14:02:08.70),
   `+7.44 s` (14:07:18.703 vs 14:07:11.26), and the modal `+10.000 s`. ⇒ `list-timers` NEXT and
   `LEFT` understate the fire time by up to `AccuracySec`; a NEXT-vs-wall gap ≤ 10 s is **not** drift.
2. **The cadence ignores run time.** `OnUnitActiveSec` is measured from the target's *activation*.
   317 runs with runtimes `min 1.494 / p50 4.547 / p90 6.585 / max 22.520 s` (Start↔Finish pairing
   in the same boot) and intervals do not stretch. ⇒ "period + runtime" is the wrong mental model;
   runtime only matters against `TimeoutStartSec=180` (§5 row 8).
3. **`Persistent=true` buys nothing without `OnCalendar`.** The 10-13 10:53:58.73 → 11:02:28.70
   gap (509.97 s across the 10:57–11:02 reboot) shows the missed fires were *not* caught up.

**Interim caveat on the "next-run" column.** While the target is running between fires, the timer
briefly reports `NextElapseUSecMonotonic=infinity`: sampler rows at 14:07:23 (4.3 s after the
14:07:18.703 fire, target still active, run p50 4.5 s) and 14:07:43 (`LastTrigger+300` restored,
`14:12:18.70`). A one-shot probe that lands in that window would misread a healthy timer as dead —
see §5 row 7.

## 5. Drift classes and the decision table

**Ladder (all thresholds anchored on the unit, not invented).** `P = OnUnitActiveSec = 300 s`,
`A = AccuracySec = 10 s`, tolerance band `t = 0.05 s` (largest measured window-end overshoot:
+9.3 ms).

| # | signature (read-only fields) | class | what it means / evidence grade | verify (read-only) | operator action |
|---|---|---|---|---|---|
| 1 | `P ≤ Δ ≤ P+A`; `LastTriggerUSec` advancing; `NextElapse = LastTrigger + P` | **on-schedule** | 2,095/2,100 intervals; mode = window end [obs] | `list-timers --all`; `show -p LastTriggerUSec -p NextElapseUSecMonotonic` | none |
| 2 | `NextElapse − now < 0` but `< A` behind the *expected fire* | **not drift** | NEXT is a lower bound; fires land up to `+A` later [obs] | compare against `LastTrigger + P + A`, not `LastTrigger + P` | none — do not "fix" |
| 3 | `Δ < P`, with a manager start inside the window (`Queued start job for default target Main User Target`, or a changed `systemd[PID]`) | **early — re-arm (by design)** | timer re-based at manager start; first fire lands in `[OnActiveSec, +A]`: measured `+0.29/+16.74 s` (10-06), `+12.8/+22.8 s` (10-06), `+16.65 s` (10-14) [obs] | `journalctl --user \| grep 'Queued start job'`; `show -p ActiveEnterTimestamp <timer>` | none; the phase shift is inherent |
| 4 | `Δ < P`, **no** manager start, but a package transaction / unit-path change inside the window | **early — environmental re-arm** | 10-11 `258.724 + 161.276 = 420.000 s` with the pre-anomaly phase restored afterwards; `pacman -Syu` started 16:13:19, transaction 16:14:18 (glibc, systemd-libs 261.1→261.2), dbus-broker reloads 16:14:23, short fire 16:14:39.436 [inf — cause measured, link unproven] | `grep -E '^\[<date>' /var/log/pacman.log`; `systemd-delta --user`; `/usr/lib/systemd/user/*.timer` mtimes | none; if the phase matters, expect one off-grid cycle after every upgrade |
| 5 | `Δ < P`, neither of the above | **early — external activation (or unknown)** | any non-timer start of the target re-bases `OnUnitActiveSec`; indistinguishable from an early timer fire at default log level [unk] | `journalctl --user -u <service>` around the fire; `show -p InvocationID <service>` | report; discriminator needs `systemd.log_level=debug` on the timer (a mutation — §9 U2) |
| 6 | `Δ > P+A+t`, timer still `active (waiting)` | **late** | 0 occurrences in 2,100 within-boot intervals — class defined, **unobserved** on this host | same sweep as §4.2; `systemctl --user status <timer>`; `journalctl --user -u <service>` for `Failed`/timeout | P2 candidate: report with the offending interval; do not restart anything |
| 7 | `NextElapseUSecMonotonic=infinity` **and** `LastTriggerUSec` empty **and** `ActiveState=inactive` | **dead (unarmed)** | the shape the two disabled timers show (§6); already the census gate's arm 5 (`tools/tsukuroi-census.sh:94-97`) | `is-enabled`; `ls -l ~/.config/systemd/user/timers.target.wants/`; `show -p UnitFileState -p ActiveState -p LastTriggerUSec` | operator: `systemctl --user start <timer>` (this lane never starts units) |
| 7b | `NextElapseUSecMonotonic=infinity` **and** `LastTriggerUSec` set **and** `ActiveState=active` | **transient, not dead** | measured mid-cycle at 14:07:23; re-armed by 14:07:43 [obs] | re-read 30 s later; or compare `LastTriggerUSec` age vs `P` | none — never classify on `infinity` alone |
| 8 | `LastTriggerUSec` advances but the target's `ExecMainStartTimestamp` does not (or `Result != success`) | **fires into a failing/missing target** | target-side faults are invisible in timer fields; `Result=success`, `ExecMainStatus=0`, `NRestarts=0`, latency `+0.62…0.74 ms` on this host [obs]; failing case unobserved [inf] | `show -p Result -p ExecMainStatus -p NRestarts <service>`; `journalctl --user -u <service>` | report with `Result`/exit code; operator remediates the target |
| 9 | wall-clock gap spanning two `_BOOT_ID`s (302.6 s … 3.04 h, 8×) | **downtime, not drift** | monotonic-only timers have no catch-up (`Persistent` inert, §4.3.3) [obs] | `journalctl --list-boots`; pair records per `_BOOT_ID` | none; catch-up would be a unit-design change (add `OnCalendar`), operator's call |
| 10 | wall-clock late by ≈ the suspend duration, monotonic schedule intact | **suspend, not drift** | `WakeSystem=no`, monotonic clocks; **no suspend event exists in the retained journal** ⇒ counterfactual here [unk] | `grep -E 'PM: suspend (entry\|exit)' <journal>`; `python3 -c 'time.CLOCK_BOOTTIME - time.CLOCK_MONOTONIC'` (0 s now) | none on this host |

Row 1–3 and 8–9 are the observed regime; rows 4–7b are the detection surface this plane adds
around them.

### 5.2 Every non-window interval in the retained history (5 of 2,100), with cause

| when (start) | Δ | cause evidence | grade |
|---|---|---|---|
| 10-06 16:21:10.293 | 16.744 s | first-ever activation of the timer (unit mtime 16:21:10.097; `Started Refresh AI usage cache` 16:21:10): two first-window fires (immediate `OnBootSec` draw + `OnActiveSec=15` + 1.74 s), then the grid | [obs] |
| 10-06 18:26:43.784 | 9.991 s | same shape after a manager start (`systemd[1540]` `Queued start job` 18:26:31; timer `Started` 18:26:31) | [obs] |
| 10-11 16:10:20.712 | 258.724 s | no manager restart in 3.5 h (`systemd[1582]` queued 07:23:34); next fire also short (161.276 s), sum exactly 420.000 s, then the old phase (…:20.712) resumes; `pacman -Syu` in flight (16:13:19 start, ALPM transaction 16:14:18, dbus-broker reload 16:14:23) | [inf] |
| 10-11 16:14:39.436 | 161.276 s | same event, second fire | [inf] |
| 10-14 13:06:46.071 → fire 13:11:23.646 | 277.575 s | user manager replaced mid-interval: last record of `systemd[1573]` 13:10:34, `systemd[1203171]` logs `Queued start job` + `Started Refresh AI usage cache` at 13:11:07, `ActiveEnterTimestamp` resets to 13:11:07, first fire `+16.65 s` (inside `[15, 25]`) | [obs] |

## 6. Boundary — the disabled timers, and the system scope

- **[obs]** `omarchy-battery-monitor.timer` (`:6-7` `OnBootSec=1min`, `OnUnitActiveSec=30sec`,
  `AccuracySec=10sec`; `:11` `WantedBy=timers.target`; `Requires=` a `static` service at `:3`):
  disabled, no wants symlink, `PRESET=enabled` ⇒ *latent*: preset-arming would start it, and its
  target is present (`~/.local/share/omarchy/bin/omarchy-battery-monitor`, 834 B, mode 755).
  Intent [unk]; duplication of round-1 text (`systemd-user-plane.md:80-95`) is deliberate — this
  plane needs it as the **dead-class signature exemplar** (`NextElapse=infinity`, `LastTrigger`
  empty, `ActiveState=inactive`).
- **[obs]** `systemd-tmpfiles-clean.timer` (`/usr/lib/systemd/user/…:16-17` `OnStartupSec=5min`,
  `OnUnitActiveSec=1d`) is disabled in the **user** scope while the **system** instance runs
  (system-scope row: LAST 2026-10-14 11:13:22 → NEXT 2026-10-15 11:13:22, exactly +24 h).
  ⇒ "user tmpfiles never cleaned" would be a wrong reading of this row.
- **[obs]** system scope holds 5 timers (`systemctl list-timers --all`); their drift table already
  exists (`journal-boot-plane.md:259-303`) and is not duplicated here.

## 7. Method lessons (each from a measurement that produced it)

1. **Compare against `P + A`, not `P`.** The mode is the window's upper edge; a table keyed on
   `P` reports a false `+10 s` on ~88 % of runs.
2. **`NextElapseUSecMonotonic` is a lower bound** (`LastTrigger + P`, measured to 1 ms over three
   cycles); the fire lands up to `A` later (`+2.56 s`, `+7.44 s`, modal `+10.000 s`).
3. **Pair starts inside `_BOOT_ID`.** Pooling the sorted global stream fabricates 8 gaps of
   5 min–3.04 h that are just powered-off windows; one of them (302.6 s) even falls inside
   `[P, P+A]`, so gap *length* alone cannot separate a reboot from a normal interval.
4. **Float equality fails on this data.** `Δ == 310.0` matched 6 of 2,100 intervals; the mode is
   `309.9999…310.0093`. Use a tolerance band, never `==`.
5. **`journalctl -u <timer>` logs the timer unit's start/stop, not its triggers.** Trigger times
   come from the target's journal (`Starting …`), and trigger *provenance* is not logged at
   default level — which is why §5 rows 4/5 stay [inf]/[unk].
6. **jq field traps:** `_SOURCE_MONOTONIC_TIMESTAMP` is `null` for userspace records (it errors
   out as "null cannot be parsed as a number"); `__MONOTONIC_TIMESTAMP` is the field that carries
   boot-relative time. A spaced field access (`._BOOT_ID` typed as `. _BOOT_ID`) silently yields
   0 rows under `2>/dev/null` — check line counts, not exit codes.
7. **Latency is a fault channel, not a drift channel:** trigger→activation `+0.62…0.74 ms`;
   anything in seconds means a queued job.
8. **Run time does not stretch the interval** (317 runs, 1.494–22.520 s, cadence unchanged);
   runtime matters only against `TimeoutStartSec=180` — and a timeout shows up as a *target*
   fault (row 8), never as interval drift.

## 8. Census hooks (observed, and one proposal — not applied)

- **[obs]** `tools/tsukuroi-census.sh` (1032 lines, md5 `e9327046b05b5c71e07fe511ad7e82dd`, pin
  taken 2026-10-14 14:07 -03; the file's mtime moved at 14:06 that day under a concurrent lane, so
  re-pin before trusting the `:94-97` line numbers) arm 5
  ("timer drift", `:94-97`) scans enabled user timers with `show <t> -p ActiveState` and counts a
  timer that is not `active` — i.e. **class "dead" (row 7) only.** The last observed live line
  (`degraded-triage-r4.md:45`) reads `timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0`.
- **[proposal, not applied]** rows 1–6 and 8 need three more read-only fields per scanned timer —
  `LastTriggerUSec`, `AccuracyUSec`, `NextElapseUSecMonotonic` — and the two-clock comparison of
  §4.2. Same scan loop, same `TIMER_SCAN_MAX` bound, no write. Left unapplied because this lane's
  write scope is this file; the gate is `TSUKUROI-R?` territory.

## 9. Unknowns

- **U1 — the draw inside `[P, P+A]`.** 248 of 2,095 in-window intervals sit below the window-end
  band, in bursts (88 runs). Mechanism [unk]. Falsifier: a scratch timer with identical parameters
  plus `systemd.log_level=debug` — both are mutations, outside this lane's contract.
- **U2 — trigger provenance for the 10-11 early fires** (timer re-arm after the upgrade vs an
  external `systemctl --user start ai-usage.service`). Same falsifier as U1.
- **U3 — intent** behind `omarchy-battery-monitor.timer` being disabled while preset-enabled
  (latent by choice, or forgotten). Lives outside the machine.
- **U4 — suspend/clock-step behaviour** of these timers is unmeasured: 0 suspend events in the
  retained journal. Note `WakeSystem=no`, so a suspended host would not be woken to fire.
- **U5 — retention horizon.** The retained journal's earliest timer start is 2026-10-06 16:21;
  drift classes before that are unknowable from this host.
- **U6 — other user managers.** `loginctl list-users` = 1 (uid 1000), `list-sessions` = 2
  (tty2 `user`, `manager`); no other user-scope timer set exists here. Untested on multi-user hosts.

## 10. Appendix — probe command set (reproducible, read-only)

```bash
# inventory (closed set) -------------------------------------------------
systemctl --user list-unit-files --type=timer --all --no-pager
systemctl --user list-units --type=timer --all --no-pager
for r in $(systemd-analyze --user unit-paths); do find "$r" -maxdepth 2 -name '*.timer'; done | sort -u

# per-timer state + the three clocks ------------------------------------
systemctl --user show <timer> -p LoadState -p ActiveState -p SubState -p UnitFileState \
  -p LastTriggerUSec -p LastTriggerUSecMonotonic -p NextElapseUSecMonotonic \
  -p NextElapseUSecRealtime -p TimersMonotonic -p TimersCalendar -p AccuracyUSec \
  -p RandomizedDelayUSec -p Persistent -p WakeSystem -p Unit -p Triggers
date -Is; python3 -c 'import time;print(time.clock_gettime(time.CLOCK_MONOTONIC), time.time())'; cat /proc/uptime

# interval history (per boot!) -----------------------------------------
journalctl --user -u ai-usage.service -o json --no-pager \
 | jq -r 'select(.MESSAGE=="Starting Probe AI CLI usage limits into cache...")
          | [._BOOT_ID, ((.__REALTIME_TIMESTAMP|tonumber)/1000000)] | @tsv'
python3 - <<'EOF'
import collections, statistics
per=collections.defaultdict(list)
for ln in open('all_starts.tsv'):
    b,rt=ln.split()[:2]; per[b].append(float(rt))
d=[c-a for v in per.values() for a,c in zip(sorted(v),sorted(v)[1:])]
win=[x for x in d if 300<=x<=310.05]; early=[x for x in d if x<300]; late=[x for x in d if x>310.05]
print(len(d), len(win), len(early), len(late), statistics.median(win))
EOF

# re-arm evidence --------------------------------------------------------
journalctl --user --no-pager -o short-iso | grep -E 'Queued start job for default target Main User Target'
journalctl --user -u ai-usage.timer --no-pager -o short-iso | grep -E 'Started|Stopped'

# not-drift exclusions ---------------------------------------------------
journalctl --list-boots --no-pager
journalctl --no-pager | grep -E 'PM: suspend (entry|exit)|Suspending system|Reached target Sleep'
```

## 11. Errata (append-only)

- 2026-10-14 (mid-probe, first pass superseded) — the first classification keyed on **300 s** and
  tested **`Δ == 310.0`**, producing "1,196 intervals in [300,310)" as if 300 were the target and
  a 6/2,099 equality hit as if 310 were rare. Both readings are wrong (§4.2, §7.1/§7.4): the
  contract window is `[P, P+A]` and the mode is its upper edge. The pass also pooled records
  globally and fabricated 8 multi-hour "gaps" (§7.3). Numbers here supersede it; the mistake is
  kept as the reason §7 exists.
- 2026-10-14 — first count of the current boot (`316` starts, from an extraction without
  `_BOOT_ID`) was taken before the 14:02:11 fire; the §4 figures use the later run (`2,108`
  records total, `317` in boot 0). Live values in §2 keep moving by design.
- 2026-10-14 (pre-handoff, supersedes the bullet above) — the extraction cut moved once more, to
  the third sampled fire `2026-10-14 14:07:18.701`: `2,109` records → **2,100** within-boot
  intervals → window **2,095** (band 1,847 = 88.2 %, lower 248 = 11.8 %), early **5**, late **0**,
  boot 0 = 318 starts / 317 intervals. Applying the cut exposed a transcription slip: two fire
  instants had been written as *monotonic* seconds (`14:02:11.258`, `14:07:18.819`) instead of
  wall times; the wall instants are `14:02:11.256` and `14:07:18.703`, so the offsets stay
  `+2.55 s` / `+7.44 s` after the projected `NextElapse`. Both corrections are counted, not
  silently applied — the classifier itself reproduced class-for-class on re-extraction
  (`/tmp/w5-tsukuroi-s5-2-timer-drift/recheck.tsv`).
- 2026-10-14 — write-scope note: `AGENTS.md` asks every change to append a `LOG.md` entry; this
  round's assignment (S5-2) names exactly one output file, so the LOG entry is left to the
  integrator rather than written from this lane.

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — `systemctl --user`, `journalctl --user`, wall/monotonic/boottime clocks, `/proc/uptime`, and pacman-log reads on host `plazir27`, 2026-10-14; S032 `/var/log/pacman.log`.
verified-at: 2026-10-14 (the timer snapshot/sampler window recorded in this note).
recheck: 30d; procedure: §10 command set; re-run a full timer fire-cycle sample and the journal interval classification.
supersedes the pointer-only recheck: line above.


## R18-FRESHNESS — sibling current-use restatements (2026-10-20)

Sources S060, S051 and S052. This appended correction supersedes the current-use readings listed below and every repeated current-use restatement of the same premise in this file. Historical measurements remain intact. No package, service, rebuild, boot or rollback action is authorized.

- R18-FRESH-SUPPLEMENT-31: prior locus `**1** (§2). System-scope timers are a different plane — 5 of them, already measured in`. Now: the five-system-timer boundary count is historical only. R17 records enabled snapper timeline/cleanup timers; neither that enabled listing nor R18 establishes a current active/all timer count [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:75-81, .ufo/waves/round-17/l1-capture/fresh-capture.txt:47-51]. Capture: .ufo/waves/round-17/l1-capture/fresh-capture.txt:47.
