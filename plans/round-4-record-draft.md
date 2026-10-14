# Round-4 record — DRAFT (scribe prep, seat SCR-S)

Status: **draft, pre-landing.** This file is the scribe's working skeleton for the
round-4 `LOG.md` entry and for the round's triage artifact review. It is not the
record; the record is the append-only `LOG.md` entry the round's scribe writes
after every round-4 artifact has landed (`AGENTS.md:3`). Every number below is a
draft-time capture with its command and time; the armed state of the round keeps
moving (a coredump storm and a live session restart — §3), so re-run, never
quote.

Draft seat: SCR-S. Draft window: 2026-10-14 16:19:57–16:22:32Z (13:19–13:22
-03), host `plazir27`, user `vgpnk` (non-root). Write scope: this file only.
Scratch: `/tmp/w4-scr-s-work/` (ephemeral). All probes read-only; no
install/upgrade/remove/restart verb was run (`PROVINCE.md:16-17`).

## 1. Plan anchor and the round's measure

`plans/round-4.plan.md` (md5 `63c26bb14d59126cd24de8255dda2fc4`, 10 lines):

> Axis move: depth (triage of the lane's own DEGRADED findings). Claim: every
> DEGRADED finding from the round-3 health report gets a triage note: the
> failure mechanism (measured deeper — what exactly is failing and why, one
> level down), the blast radius (what depends on it), and the priority-ordered
> unblock action. Grouped into triage classes (package / service /
> driver-firmware / config) with the census gate re-run as receipt.
> Anti-claim: a finding whose mechanism can't be read without elevated perms
> gets an honest 'mechanism blocked' row with the exact elevation needed.
> Measure: finding->class->mechanism->action rows = the round-3 DEGRADED count.

Interpretation to check when the triage artifact lands: "the round-3 DEGRADED
count" reads as the report's **20 finding→action pairs**
(`host-health-report-r3.md` §0.1, "Finding → action index (20 pairs)":
P1–P5, D1–D3, J1–J4, U1–U8 = 5+3+4+8 = 20). If the landed artifact counts a
different unit (e.g. 4 DEGRADED planes, or includes the round-4 new classes),
the record states the actual row count and the unit — no laundering toward 20.

## 2. Draft-time baseline receipts (measured by this seat)

Gate, re-run 2026-10-14 (raw captures in `/tmp/w4-scr-s-work/`):

```bash
bash tools/tsukuroi-census.sh --selftest   # 16:19:57Z, rc=0
bash tools/tsukuroi-census.sh              # 16:20:04Z, rc=1
```

Selftest last line verbatim: `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26
passed, 0 failed)`. Gate file md5 unchanged from the round-3 pin:
`41953ee9f2099281c91759249fe8708f`, 976 lines → all deltas below are host
state, not gate drift.

Live run verbatim (16:20:04Z, `census-live.out`):

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T16:20:04Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16; pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=137 (oom=1 io=70 gpu=0 other=66) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=405 (coredump=244 kernel=137 other=24); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

Delta table vs the two earlier captures in the tree (same gate, same boot
d7f0bc8d938e4249b4a1f250cbfacf58 — boots=13, boot 0 still current):

| capture | err | coredump | kernel | kerr (io/other) | failedhist |
|---|---|---|---|---|---|
| round-3 report §1, 14:57:13Z | 251 | 211 | 38 | 38 (35/2) | 0 |
| R4-2 erratum, 16:06:19Z | 344 | 228 | 102 | 102 (35/66) | 0 |
| **this draft, 16:20:04Z** | **405** | **244** | **137** | **137 (70/66)** | **8** |

Arithmetic checks [observed]: 344→405 = +61 (coredump +16, kernel +35, other
+10); kernel 137 = oom 1 + io 70 + other 66; io 35→70 = a second 35-line sr0
burst (§3, E3).

Artifact md5s re-hashed at draft time (16:20Z, `md5-drafttime.out`) — all
round-3 pins reproduce; the two round-4 artifacts are new:

| artifact | md5 | lines |
|---|---|---|
| `tools/tsukuroi-census.sh` | `41953ee9f2099281c91759249fe8708f` | 976 |
| `corpus/knowledge/host-health-report-r3.md` (now carries the R4-2 erratum) | `cb7c26b033c31fe070c03a45252a5916` | 519 |
| `corpus/knowledge/journal-boot-plane.md` | `16d4047e8b03deec69773d2cc0b1b75c` | 411 |
| `corpus/knowledge/package-state-plane.md` | `24eafc4067f6ca7bf3608dfff5ff63d6` | 303 |
| `corpus/knowledge/systemd-user-plane.md` | `26dca9cf12b322926babfef49e257f07` | 247 |
| `corpus/knowledge/driver-firmware-plane.md` | `a44e9c07d5b139fe65d5284674398b3a` | 242 |
| `corpus/knowledge/update-safety-note.md` | `5cc3067fec33d261d8bff6a5c7e8ac48` | 478 |
| `corpus/knowledge/executor-test-sufficiency.md` | `4b2c1d3612db7db1477da92aaec39862` | 219 |
| `SKILL.md` | `63b0900e8f3a5d850a035cef94c03ce0` | 543 |
| `plans/round-4.plan.md` | `63c26bb14d59126cd24de8255dda2fc4` | 10 |

Repo state at draft entry: HEAD `9bcd162` (probation round 3);
`git status --short` = ` M corpus/knowledge/host-health-report-r3.md`,
`?? plans/round-4.plan.md` (both round-4 artifacts, not this seat's writes).

## 3. Round-4 event docket (the delta the triage must explain)

These are host events measured inside the round-4 window (after the round-3
report's 14:57:13Z capture), not lane-caused. Each row: class → measured
mechanism → blast radius → action/status. Numbers are captures; §2 pins the
commands.

**E1 — session teardown + OOM kill, 13:10:59 -03 (16:10:59Z); new session
13:11:07 -03 (16:11:07Z).** class: service (+ resource).
[observed] `systemd[1]`: `user@1000.service: Main process exited, code=killed,
status=9/KILL` → `Failed with result 'signal'`; `Consumed 1d 11h 3min 1.574s
CPU time … 28.5G memory peak, 34.2G memory swap peak`; `user-1000.slice: The
kernel OOM killer killed some processes in this unit`. sddm-helper: `[PAM]
Closing session` / `session closed for user vgpnk`; `Session 1 logged out`;
`Removed session 1`, `Removed session 2`. At 13:11:07: new `user@1000.service`
MainPID `1203171`, `NRestarts=0`, active/running; `loginctl list-sessions`
(16:21:12Z) = session 4 (user, tty2, leader 1203167) + session 5 (manager,
leader 1203171). Cgroup files (16:21:52Z): `memory.events` → `oom_kill 1`;
`memory.peak` = `30699745280` (~28.6 GiB); `memory.current` =
`27054899200` (~25.2 GiB); `memory.max` = `max`. `systemd-oomd` = inactive
(dead, disabled) → not the killer. Memory at 16:21:52Z: `free -h` = 30Gi
total, 9.4Gi used, 689Mi free, 34Gi swap (1.1Gi used);
`/proc/pressure/memory` some avg10=0.22.
[inference] the OOM killer took the old session down (same-second slice
message + SIGKILL + session logout); the new session is a fresh login into the
same boot.
[unknown] the kernel-side OOM detail for this kill is absent from the ring:
`journalctl -k -b` 13:10:55–13:11:05 holds only sr0 lines + `10 callbacks
suppressed` pairs, and the boot's only `Out of memory: Killed process` line is
the Oct-13 23:44:30 python3 one (`oom=1` in the census, regex
`Out of memory|oom-kill|oom_reaper` at `tools/tsukuroi-census.sh:163`) — why
this kill left no kernel line, and which processes were killed, are open.
Blast radius: the whole graphical session (compositor, agents, in-flight lane
work) died and restarted; any lane that held state only in memory lost it.
Action: report to fleet/operator; a memory-pressure guard is an operator
decision, out of province to fix.

**E2 — `failedhist` 0 → 8, all one generator collision event.** class:
service. [observed] all 8 lines (verbatim, 16:20:15Z) are
`systemd-xdg-autostart-generator[1203177]: Failed to create unit file
'/run/user/1000/systemd/generator.late/app-…@autostart.service': File exists`
at 13:11:07 -03 (one per leftover file). The leftover files are dated
Oct 13 11:02 (old manager's run; `stat` on
`app-walker@autostart.service` → `2026-10-13 11:02:06.192794577 -0300`);
`/run/user/1000` survived the manager restart, the new manager's generator
refused to overwrite. [observed] no unit is actually failed:
`systemctl --user list-units --state=failed` = `0 loaded units listed`
(16:20:15Z). Mechanism: pattern collision — the census's failedhist arm
(`CLASS_FAILED='Failed to |entered failed state|Failed with result'`,
`tools/tsukuroi-census.sh:166`) counts "Failed to create unit file" as
failed-service history. Blast radius: none observed beyond the DEGRADED
verdict contribution; [inference] if a unit file's generator output changed
between manager starts, the collision could mask a change — unverified.
Action: record as session-restart residue; re-check `failedhist` next boot.

**E3 — sr0 read burst recurrence (D1's conditional now live).** class:
driver-firmware. [observed] `journalctl -k -b -p err` holds 70 sr0 lines, in
two 35-line bursts: `2026-10-13T11:02:03` (boot) and `2026-10-14T13:10:59`
(session teardown second, with `scsi_io_completion_action: 10 callbacks
suppressed` / `blk_print_req_error: 10 callbacks suppressed`). Content:
`critical target error, dev sr0, sector 44986976/44987936/44988448/44989016–24`
+ `Buffer I/O error on dev sr0, logical block 5623…, async page read`;
`sr 12:0:0:0` `Sense Key : Illegal Request` / `Logical block address out of
range`. [unknown] what reads the optical device at teardown second (the
coincidence with E1 is exact to the second; no mount/udisks line found).
Blast radius: boot-ring noise floor only — no filesystem on sr0. Action: D1's
"only if it recurs" condition is met → media/drive check is now operator-
justified; otherwise accept as recurring noise.

**E4 — coredump storm continues, live.** class: service (cross-domain
victims). [observed] err entries 405 (coredump=244) at 16:20:04Z, 407 at
16:22:14Z; `coredumpctl … | jq length` = 244; identifier histogram (16:22Z):
244 systemd-coredump, 139 kernel, 10 pipewire, 8 generator, 3 pipewire-pulse,
2 sddm-helper, 1 limine-snapper-sync. New entrants per the R4-2 erratum
(`host-health-report-r3.md:441-462`): blender 7 SIGSEGV, love 2 SIGABRT. The
old manager's last journal lines (13:10:45–13:10:59) show a LOVE
(`liblove-11.5.so` / SDL3 / libusb) coredump backtrace — the storm and E1 are
temporally adjacent [observed]; causal link [unknown]. Blast radius: disk
(J2), memory pressure (E1 candidate contributor), lane hygiene. Action:
already handed to owning workstreams (report, not absorb).

**E5 — USB-audio + pipewire error cluster (cited from the R4-2 erratum, not
re-measured by this seat).** class: service/config. [observed, R4-2] 64 ×
kernel `usb 8-12: Incompatible EP setup for 0x8` (device `0db0:cd0e` USB
Audio, still enumerated), 15:30:08–16:03:04Z; 9 × pipewire + 3 ×
pipewire-pulse err entries 15:29:03–15:30:39Z (`can't find protocol
'PipeWire:Protocol:Native'`, fallback-sink module failure, `org.pulseaudio.
Server already taken`), one-shot clients, daemons not flipped. [unknown]
launcher/mechanism; current audio-path health unprobed. Action: triage deepens
this; E1's session restart is 100 min later — no measured link.

**E6 — aggregate deltas** (§2 table): err 251→344→405; coredump 211→228→244;
kerr 38→102→137; io 35→70; failedhist 0→0→8. Every value a capture with time;
the storm drifts in seconds (`coredumpctl` 244→230→235 within one minute in
the R4-2 erratum).

## 4. Triage skeleton — the 20 round-3 DEGRADED findings + round-4 entrants

Fill rule: the round-4 triage artifact deepens the **mechanism** column one
level down, adds **blast radius**, and keeps/refines the **action**;
`[R4: …]` marks what the triage owes. Class vocabulary: package / service /
driver-firmware / config. Pre-filled values are the round-3 report's own
(pointer in the last column); they are starting points, not replacements.

| ID | Class | Mechanism (measured so far) | Blast radius / status | Action (priority) | Source |
|---|---|---|---|---|---|
| P1 | package | setgid helpers, vendor dynamic groups; GID+mode delta only | census DEGRADED arm | root-verify or reinstall (P2-adjacent) | r3 §2.1 |
| P2 | package | 36 non-root artifacts (32 failed-calc SHA + 4 perm-denied) | sweep completeness | root `-Qkk` re-run | r3 §2.1 |
| P3 | package | one true content signal (mtime+size+SHA) in sweep | omarchy patch vs drift [unknown] | decide patch vs reinstall | r3 §2.1 |
| P4 | package | 16 foreign; elephant family in no synced repo | silent soname break risk | record baseline or remove | r3 §2.1 |
| P5 | package | cache 8.6 G + 3 root-only alpm temp dirs | hygiene, 849 G free | optional prune; **mechanism blocked: root** (`sudo ls` the 3 dirs) | r3 §2.1 |
| D1 | driver-firmware | sr0 LBA-out-of-range reads; OOM 1; TDX info | **live: second burst E3** | media check now justified; else noise floor | r3 §2.2 + §3 E3 |
| D2 | driver-firmware | stale dkms 7.1.4 row vs only 7.2.3 tree | rebuild already failed once (U3) | `sudo dkms remove nvidia/610.57.04 -k 7.1.4-arch1-1`; **mechanism blocked: root** | r3 §2.3 |
| D3 | driver-firmware | DKMS build output unowned by pacman (expected) | none | verify via `modinfo`/`nvidia-smi`; no repair | r3 §2.3 |
| J1 | service | coredump storm — **live, E4**; class composition measured; root cause cross-domain | disk + memory pressure | hand to owning workstreams | r3 §2.4 + E4 |
| J2 | service | 3.9→4.1 G coredump dir; no `coredumpctl` vacuum in build | disk hygiene | operator prune after owners served | r3 §2.4 |
| J3 | driver-firmware | boot dwell bimodal; crypttab mode 600 — **mechanism blocked: root** (`sudo` read of `/etc/crypttab` + resume config) | boot latency only | operator probe if dwell matters | r3 §2.4 |
| J4 | service/config | limine-snapper claims a config; `snapper list-configs` header-only | rollback net (U1) | configure or accept in writing | r3 §2.4 |
| U1 | config | no rollback net (same evidence as J4) | any `-Syu` wave | written decision before any wave | r3 §2.5 |
| U2 | config | upstream delta unmeasurable read-only; dbs 2026-09-08 content | update decisions blind | operator `-Sy`/`checkupdates` | r3 §2.5 |
| U3 | config | kernel/DKMS rebuild coupling (D2 as evidence) | reboot-before-verify risk | verify `dkms status` post-wave | r3 §2.5 |
| U4 | config | `[omarchy]` TrustAll + LocalFileSigLevel Optional | trust channel | written accept/re-scope | r3 §2.5 |
| U5 | package | `1password-beta` 1 ahead of channel; `-Suu` downgrades | 579 MiB rewrite trap | plain `-Syu` only | r3 §2.5 |
| U6 | config | `/boot` unreadable non-root — **mechanism blocked: root** (`sudo ls /boot` + `sudo bootctl status`) | kernel/firmware waves | root pre-verify | r3 §2.5 |
| U7 | config | `walker-restart.hook` execs user-owned script as root | root-exec surface | kagi/operator review (reported) | r3 §2.5 |
| U8 | service | live workload contention (75× ffmpeg r2; fleet lanes now) | wave timing + **E1 memory pressure** | schedule quiet window | r3 §2.5 + E1 |
| R4-A | service | OOM kill + session restart (**E1**) — kernel detail absent [unknown] | whole session | report; operator memory guard | §3 E1 |
| R4-B | service | generator collision on manager restart (**E2**) | verdict noise; masking [inference] | re-check next boot | §3 E2 |
| R4-C | service/config | USB EP-setup + pipewire cluster (**E5**) | audio path unprobed | triage deepen; cross-domain | §3 E5 |

Anti-claim compliance (plan): the "mechanism blocked" rows carry the exact
elevation — P5 (root `ls` of alpm temp dirs), D2 (`sudo dkms remove` is an
action, the *mechanism* read is `sudo dkms status`-as-root), J3 (root
`/etc/crypttab` + resume config read), U6 (`sudo ls /boot`, `sudo bootctl
status`). No row may claim a mechanism its privilege gate forbids.

## 5. Record skeleton (what the LOG.md entry must carry on landing)

Fill on landing; keep the round-3 scribe shape (`LOG.md:83-166`).

**Work (observed in tree).** `⟨artifact list: path, seat/ID, md5, lines, mtime⟩`
— expected: the round-4 triage artifact + the R4-2 erratum already in
`host-health-report-r3.md:422-478` + any SKILL/coverage/move-log updates. Hash
every artifact at entry; do not quote stale md5s (the report changed under us
once already — that is the recorded-not-laundered precedent,
`host-health-report-r3.md:408-412`).

**Scribe re-verification (re-executed, read-only).** §6 command set; quote the
selftest line, the live line, and the drift caveat.

**SHONEN boxes.** At draft time all four are `[~]` asserted with evidence
pointers and verifier names (`SHONEN.md`); the promotion review (non-author)
is the owed `[x]` step. The round-4 record must not upgrade boxes itself.

**State at entry.** Commit landed for the round (hash), or "round work
uncommitted in tree" with the exact `git status --short`; the record is written
by the scribe seat, which writes only its named files; commit carries the lane
identity.

**Open (carried + new).** Carried from rounds 1–3: root `-Qkk` delta;
`offline.db` coverage; round-2 wave-1 errata merge into SKILL round-1 blocks;
v1 census md5-prefix transcription candidate; literal
`source:`/`verified-at:`/`recheck:` keys; `corpus/lessons/round-1.md`. New,
from this draft: E1 kernel-detail gap; E2 masking question; E3 media check;
post-append no-oral-context re-test (round-3 box 3); "20-min cap" resolution
(executor record §7 U1 — still undefined in the lane; owner: integrator).

## 6. Scribe re-run set (receipts owed by the record)

```bash
cd ~/Projects/shokunin/tsukuroi-shokunin
bash tools/tsukuroi-census.sh --selftest           # expect rc=0, 26/26 PASS
bash tools/tsukuroi-census.sh                      # expect rc=1, DEGRADED rollup
md5sum tools/tsukuroi-census.sh                    # 41953ee9… (if unchanged, deltas are host state)
journalctl -b -p err -o json --no-pager | wc -l    # entry count, drifts — capture time it
journalctl -b -p err -o json --no-pager | jq -r '[.SYSLOG_IDENTIFIER]|@tsv' | sort | uniq -c | sort -rn
journalctl -k -b -p err -o json --no-pager | wc -l # kerr class line
journalctl -b --no-pager -o short-iso | grep -E "killed some processes|Out of memory" # E1/E2 evidence
systemctl --user list-units --state=failed --no-pager   # E2: expect 0
cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.events   # E1: oom_kill N
git status --short                                 # zero mutation receipt
```

## 7. Unknowns register (draft-time; owners)

1. E1: why the 13:10:59 OOM kill has no kernel `Out of memory:` line while
   the Oct-13 one does; which processes died (owner: triage lane / operator).
2. E1: whether the session restart was OOM-caused end-to-end or partly
   coincident (SDDM logout path) (owner: triage lane).
3. E2: whether generator collisions can mask changed unit definitions across
   a manager restart (owner: triage lane; upstream systemd check).
4. E3: what reads sr0 at 13:10:59 (owner: triage lane; `lsof`/udev history
   would need a live trigger).
5. E5: launcher/mechanism of the USB-audio + pipewire cluster; current audio
   path health unprobed (owner: triage lane, per R4-2).
6. Round-3 register items still open (root `-Qkk`, crypttab, `/boot`,
   elephant provenance, upstream delta, dwell mechanism) — unchanged.

## 8. Errata / pending (append-only)

- 2026-10-14 — this draft file created by SCR-S; it is prep, not a record.
  The `LOG.md` round-4 entry remains owed (`AGENTS.md:3`); the record's measure
  (finding→class→mechanism→action rows) is judged against the landed triage
  artifact, not against this skeleton.
- 2026-10-14 — counts in §2/§3 are captures in a live storm and a post-restart
  session; the record must re-capture, never quote (drift precedent:
  `host-health-report-r3.md:441-462`).