# Census closeout receipt — the hardened gate re-run live: **six** plane lines, verdict `DEGRADED` (S10-3, round 10)

source: live read-only probes, host `plazir27`, user `vgpnk` (non-root), window
**2026-10-14 20:50:53Z – 20:52:37Z** (-0300 17:50–17:52). Probes: `bash tools/tsukuroi-census.sh --selftest`
(rc=0), two back-to-back live runs of `bash tools/tsukuroi-census.sh` (rc=1 each, unpiped, stdout and
stderr captured separately), `md5sum`/`sha256sum`/`wc`/`stat` on the census, `git show HEAD:tools/tsukuroi-census.sh`
piped through `md5sum`/`sha256sum`/`wc -lc`, `git status --porcelain`, `ls` on `/var/lib/pacman/db.lck`,
`journalctl --list-boots | wc -l`, `pacman -Qm | wc -l`, `stat -c '%w %n' /var/lib/pacman/sync/*.db`.
No `pacman` transaction, no `-Sy`/`-Syu`, no service action, no root, no network, no external site.
Scratch `/tmp/w10-tsukuroi-s103/` (`selftest.{out,err}`, `live.out`, `live.err`, `live2.{out,err}`).
Zero host mutation: `/var/lib/pacman/db.lck` absent before and after every run; repo tree byte-identical
(0 `git status --porcelain` lines, before the selftest and after the second live run); no stderr on any run.
Dispatch frame: lane **S10-3** — "the 5-plane census receipt: the hardened census re-run live (5 PLANE
lines, verdict) as the round's closeout receipt". Wave plan: `plans/round-10.plan.md` — cited as a plan,
never as landed state.
verified-at: 2026-10-14 20:50:53Z – 20:52:37Z (one window; **every value a capture — re-run, never quote**).
recheck: §7.
Notation: **[obs]** measured in this window · **[inf]** inference, stated as such · **[unk]** not settled,
with the probe that would settle it. Line counts are `wc -l`; the census carries an **unterminated final
line** (`main "$@"`, `tools/tsukuroi-census.sh:2350`), so Read counts one more (2350 vs 2349) — a pin
states its convention.

## 0. Verdict — what the closeout receipt reads [obs]

**The landed round-9 gate executed live emits SIX `PLANE` lines and rolls them up as
`TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED
update-safety=DEGRADED oom=HEALTHY)` with exit code 1** — reproduced twice, 77 s apart, on the same
revision, both with empty stderr.

**Delta against the dispatch premise, recorded not smoothed:** the assignment names "5 PLANE lines".
The realized gate emits **6** — round 9 landed *two* planes on top of round 8's four: S9-1's
`PLANE update-safety` (fifth emitter, `tools/tsukuroi-census.sh:2328`) and S9-2's `PLANE oom`
(sixth emitter, `:2329`; the watch round 8 specified and never landed — `SKILL.md:1363`; the
seat attribution is the landed addendum's own, `SKILL.md:1348`). The
"5-plane" wording still standing in the lane's own round-9 closeout records is stale against the
realized gate [obs]: `LOG.md` last line reads "the 5-plane census landed (update-safety arms — the r7
AUD-X7 gap closed; PLANE oom)", and `SCORECARD.md` row 9 reads "the 5-plane census landed (update-safety
arms — the r7 AUD-X7 gap closed" (the move cell also appears truncated mid-parenthesis before `wave-9
32-lane (2 rerouted alibaba->hyper)`). Neither is repaired here (write scope: this file only); both are
carried as observations for the round's record seats.

The gate arc this receipt closes out, every row a landed pin except the last two (this window) [obs]:

| revision | md5 | `wc -l` | planes | selftest cases | capture |
|---|---|---|---|---|---|
| round-7 revision | `e2c4558a…` | 1472 | 4 | 49 | 19:58:48Z (round-9 plan's capture) |
| round-9 landed revision | `e32aac98…` | 2349 | **6** | **74** | **20:51:09Z / 20:52:26Z (this receipt)** |

## 1. The live run, verbatim [obs]

Canonical capture — second run, 2026-10-14T20:52:26Z, rc=1, stderr empty (start/end stamps
20:52:26Z→20:52:29Z; only capture #1 was timed, wall 2.865 s):

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T20:52:26Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=188 C4_present=2[user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922897 C5_swap_peak_pct=99% C5_pswp=74576965/96424269 C5_sock_throttled=73513; C6_psi_some_avg300=0.00 C6_psi_full_avg300=0.00 C6_psi_full_total_us=72758668 C6_avail_kb=17676964 C6_shmem_kb=8577692; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=798 (coredump=523 kernel=139 other=136); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
PLANE update-safety: DEGRADED (status=UNKNOWN-UPSTREAM; pending=none; qu=rc=1/0; sup=0; join=equal=1171 behind=0 ahead=1 src=sl+expac; expac=agree; chan=dbs=4 fetch=3d stamp=36d; offline.db=present(stamp=85d birth=11d); log=cmd=-S@2026-10-13T16:37:58-0300; refresh=none-in-window(last 300 lines); classes=offline-exile:14,aur-local:2; trap=-Suu:1[omarchy/1password-beta 8.12.42_32.BETA-1]; traps=[-Qu blind to shadowed-newer; '%s' is not a size]; vocab: SKILL.md:358-368)
PLANE oom: HEALTHY (window=boots=13 2026-10-03..2026-10-14; C1_kernel=3 killed_process=1; C2_events=3 C3_events=3 clusters=2[2026-10-13 23:44,2026-10-14 13:10]; base=r8(2) known=2[A, B] new=0 missing=0 out_of_window=0; ledger=vmstat.oom_kill=1; anchors=see drivers.mem; traps=presence-not-count,peak-not-datable,launch-not-live; rule=both-readings-carried; r8 vocab: kill-event-deep-r8.md §1)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=HEALTHY)
```

First run, 2026-10-14T20:51:09Z, rc=1, wall 2.865 s: identical line-for-line **except** the six fields
in §6's drift table — same six plane names, same verdict, same rollup. Both runs unpiped; a piped
invocation was never used, so no pipeline rc can shadow the exit map.

## 2. Identity — the revision under test [obs]

- `md5sum tools/tsukuroi-census.sh` = `e32aac98c6b54f9d7fb8bc4f348cd467`; sha256
  `c396662eeb5f435d841b0c1863903dba807aa9dcbc6a67b2439fdfb13670c650`; 2349 `wc -l` / 123 410 B
  (mtime 2026-10-14 17:17:50 -0300).
- Working tree == committed bytes: `git show HEAD:tools/tsukuroi-census.sh | md5sum` = the same
  `e32aac98…`, sha256 the same, `wc -lc` = `2349 123410`; `git status --porcelain` = 0 lines.
  HEAD = `fac745b` ("probation round 9 (training r8)"), which committed +884/−7 on this file.
- The executed bytes match the round-9 append's superseding identity pin verbatim
  (`SKILL.md` Errata addendum, md5 `e32aac98…` / sha256 `c396662e…` / 2349 / 123 410 B): the commit
  pinned exactly the bytes that ran here. No mismatch to record.
- The tool has **no `--identity` mode** at this pin: `usage()` (`:439-452`) lists `--selftest`,
  `--sample N`, `--help` only; main() (`:2286-2348`) accepts nothing else (unknown argument → usage +
  exit 2). The identity above is therefore derived by the classic three commands, not printed by the
  gate. Round 10's proposed mechanical identity row (one-command re-derivation) is not landed here —
  stated so no later round cites this receipt as that feature's check.
- Version string is still `census-v2` (`VERSION='census-v2'`, `tools/tsukuroi-census.sh:323`; the
  usage/verdict form at `:443-450`): identity is by hash, not by version string. The realized plane
  set is `packages systemd drivers journal update-safety oom` (`:2324-2329`, rollup `:2339-2340`,
  exit map `:2342-2347`).

## 3. Selftest and the counts-move-together check [obs]

`bash tools/tsukuroi-census.sh --selftest` → rc=0 in 11.242 s, terminal line verbatim:
`TSUKUROI_CENSUS_SELFTEST: PASS (74 cases, 74 passed, 0 failed)`; stderr empty. The last two case
labels are both S9-2 oom-watch fail-closed cases ("no boot measured is not a clean window";
"a window scan unreadable fails closed"), both `exit 2, BLOCKED`.

Restatement check against the gate's own documentation: `SKILL.md:1359` and `:1373` state the current
expected line as `PASS (74 cases, 74 passed, 0 failed)` — **executed count == restated count** (74).
History stands as history: 49 cases (round-7 blocks, `SKILL.md:866-868`, `:928`), 63 inside the
round-9 append (`:1314`), 74 in its addendum — a further gate move must move all live restatements
with it. The round-9 append's own stale pins are superseded by its addendum, not by this receipt.

## 4. Plane-set consistency and the exit map [obs]

- Emitted `PLANE` names, mechanically extracted from run 2: `drivers, journal, oom, packages, systemd,
  update-safety` (6). Rollup keys of the same invocation: the same six. **SET-MATCH** — no emitter
  without a rollup term, no rollup term without an emitter.
- Exit map as declared (`usage()`, `:450`): 0 HEALTHY | 1 DEGRADED | 2 BLOCKED, worst plane wins.
  Observed rc=1 with crown DEGRADED and per-plane worst = DEGRADED (packages, drivers, journal,
  update-safety DEGRADED; systemd, oom HEALTHY) — consistent. A BLOCKED plane was not exercised live
  in this window; the fail-closed arms are covered by the selftest's BLOCKED cases, which are the
  authors' evidence, not this receipt's.

## 5. Zero-mutation receipt [obs]

- `git status --porcelain` = 0 lines / md5 `d41d8cd98f00b204e9800998ecf8427e` (the empty stream)
  before the selftest and after the second live run — byte-identical.
- `/var/lib/pacman/db.lck` absent before the first run, and absent after the second; the packages
  plane itself reports `db.lck=absent`.
- No run produced stderr output; no `pacman` lock, no transaction, no service action, no root.
- Selftest scratch: the suite mktemp's `/tmp/tsukuroi-r3-2-selftest.XXXXXX` with an EXIT trap cleanup
  (`tools/tsukuroi-census.sh:1573-1574`), so its writes stay outside the repo and outside the host's
  package state. **[unk]** leftover dirs with *changing names* were observed across this window
  (`…8xGf2C`, then `…Oz399n`/`…znqi7j`, then `…h2DVhk`; shape/timestamps only). None is attributable
  to this seat on the evidence read: this seat's live runs create no temp dirs, and the two dirs whose
  mtimes were read (20:51:50Z, 20:51:57Z) postdate this seat's selftest exit (20:51:04Z). With 32
  lanes in flight, whether they are other seats' runs or interrupted selftests stays **[unk]**; the
  probe that would settle it is a lane-tagged mktemp prefix, which the suite does not carry.

## 6. Drift inside the window — why the receipt quotes captures, not the gate's values [obs]

Same revision, same boot (both captures report `boots=13`), 77 s apart:

| field | run 1 (20:51:09Z) | run 2 (20:52:26Z) | delta |
|---|---|---|---|
| `C6_avail_kb` | 18 329 696 | 17 676 964 | −652 732 kB (≈ −637 MiB) |
| `C6_psi_full_total_us` | 72 681 373 | 72 758 668 | +77 295 µs |
| `C5_pswp` (swap pages) | 74 576 915 / 96 424 269 | 74 576 965 / 96 424 269 | +50 pages |
| `C6_shmem_kb` | 8 573 292 | 8 577 692 | +4 400 kB |
| `journal err` / `coredump` | 798 / 523 | 798 / 523 | 0 / 0 (quiet 77 s) |

And against the round-9 plan's live capture 52 min earlier (same boot, `boots=13`; that run executed
the **round-7 four-plane revision**, `e2c4558a…` 1472 `wc -l`): `err` 742 → 798, `coredump` 467 → 523,
`C5_sock_throttled` 71 447 → 73 513. Every value above is a capture with a stated timestamp; none is a
standing fact about the host, and this receipt is not re-quotable as one.

## 7. Independent cross-probes of live values (not the gate's own reads) [obs]

| # | live value in the receipt | independent probe this window | result |
|---|---|---|---|
| 1 | journal plane `boots=13` | `journalctl --list-boots \| wc -l` | 14 lines = 13 boots + header — agrees |
| 2 | packages plane `foreign=16` | `pacman -Qm \| wc -l` | 16 — agrees |
| 3 | update-safety plane `chan=dbs=4 fetch=3d`; `offline.db=present(stamp=85d birth=11d)` | `stat -c '%w %n' /var/lib/pacman/sync/*.db` | core/extra/multilib/omarchy birth `2026-10-11 12:54:13.542054496 -0300` (4 dbs = `dbs=4`; 3 d 7 h 58 m before this window → floor `3d`); `offline.db` birth `2026-10-03 17:41:33.994891750 -0300` = 11 d 3 h 11 m before 20:52:37Z → floor **11 d**, agrees with `birth=11d`. The `10d` reading in the round-9 append is the same file before the 17:41 day-boundary crossing [inf, arithmetic shown; settles with the same `stat` at any time of day] |

To re-derive this receipt (any seat, no author needed): `md5sum tools/tsukuroi-census.sh` →
`e32aac98c6b54f9d7fb8bc4f348cd467`; `bash tools/tsukuroi-census.sh --selftest` → rc=0 and the
`PASS (74 cases, 74 passed, 0 failed)` line; `bash tools/tsukuroi-census.sh` → six `PLANE` lines whose
names equal the rollup keys, then the rollup line above; `echo $?` → 1; `git status --porcelain` → 0
lines; `ls /var/lib/pacman/db.lck` → absent.

## 8. What this is not, and the unknowns it carries

- **Not a host-health review and not a remediation trigger.** It records one gate revision, executed,
  at one timestamp. `update-safety: DEGRADED` here means the gate's own confluence reading (ahead=1,
  the `omarchy/1password-beta` `-Suu` trap row, 36 d stale sync stamp) — its operator-facing reading
  lives in `corpus/knowledge/update-safety-v3.md`; the oom plane's semantics live in that arm's own
  seats' artifacts (`corpus/knowledge/kill-event-deep-r8.md` §1, cited as its r8 vocabulary at
  `SKILL.md:1363`).
- **Not a non-author verification of the two planes round 9 added** (the D13 rule): this seat re-ran
  the gate and cross-probed three of its live values; the update-safety and oom arms' own contract
  verification is a separate active seat's product and is quoted when it lands, never anticipated here.
- **[unk]** whether the "5-plane" wording in `LOG.md` (last line) and `SCORECARD.md` (row 9, also
  truncated) is repaired by the round-9 record or left as history — adjudication belongs to the
  record/scribe seats; the probe is a later `git log`/read of those files.
- **[unk]** whether other lanes were mid-run on the same gate during this window (the transient
  `/tmp` dirs of §5); my two captures are timestamped and self-consistent, and a lane-tagged scratch
  prefix would settle it.
- **[unk]** `corpus/README.md` (unchanged at 20 `wc -l` since round 3) does not yet index this file or
  the round-9 receipt — the coverage debt it names; owner: the round's note/hygiene seat, not this
  receipt.
- Carried, unchanged, out of this receipt's scope: root `-Qkk` delta, `1password-beta` provenance,
  `walker-restart.hook`, dkms stale row, `snapper` empty, `offline.db` coverage, the "20-min cap"
  item, the AUR-drift watch's own receipt (`aur-drift-receipt-r9.md`), and the coredump-storm class
  (its count here — 523 — is a capture; the class stays with the journal workstream).

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — read-only `tools/tsukuroi-census.sh --selftest`/live runs, package and journal queries, and hash/status checks on host `plazir27`, 2026-10-14; S031 `tools/tsukuroi-census.sh`.
verified-at: 2026-10-14 (the receipt's original capture window recorded in this note).
recheck: on-release; procedure: §7 receipt commands; rerun the selftest and live census after a census release.
supersedes the pointer-only recheck: line above.


## R18-RECHECK — steer-safe procedure

Supersedes this entry's historical pointer-based recheck procedure for a steer forbidding package-manager execution (QUALITY26). Historical command receipts remain historical; do not run their backticked package commands or the live host census merely by following the old section pointer. This is an actual bounded read/compare procedure, not a whole-host clearance or a new host measurement.

- Read the installed-name/version metadata with `ls -1 /var/lib/pacman/local`; for each package whose recorded field is being rechecked, read its exact `/var/lib/pacman/local/<pkg>-<ver>/desc` and compare name, version, install date, reason and validation fields with the dated table. Directory presence does not certify file integrity or current repository reachability.
- Read repository-file inventory and timestamps with `ls -1 /var/lib/pacman/sync` and `stat -c '%y %n' /var/lib/pacman/sync/*.db`. Mtime is an upstream stamp, not local acquisition time; a present database is not proof it is configured.
- Read relevant transaction events using `tail -n 80 /var/log/pacman.log`; distinguish invocation headers from ALPM completion events, preserve capture time and exit status, and never infer a current pending-update count from this history.

- Recheck the repository artifact with `sha256sum tools/tsukuroi-census.sh` and its isolated fixture suite `bash tools/tsukuroi-census.sh --selftest`; these do not refresh a live health verdict. Never substitute the unflagged live invocation under a no-package-command steer.

Record observed values and unresolved questions separately. Uncaptured pending updates, signature validity, exact foreign/orphan classification, private mount views, historical provenance events and recovery feasibility remain unknown until their own authorized evidence is obtained. No installation, restart, rebuild, subvolume action or boot write is authorized.
