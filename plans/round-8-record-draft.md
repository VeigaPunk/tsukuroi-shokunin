# Round-8 record — DRAFT (scribe prep, seat SCR-S8)

Status: **draft, pre-landing.** This file is the scribe's working skeleton for the
round-8 `LOG.md` entry and for the round's artifact families (the OOM/kill-event
plane joining `tools/tsukuroi-census.sh` as a new-vs-baseline watch). It is not
the record; the record is the append-only `LOG.md` entry written after every
round-8 artifact has landed (`AGENTS.md:3`). Every number below is a draft-time
capture with its command and time; the host is live — re-run, never quote.
**The round's headline is the VER-S8 closure** (§4d): the non-author
verification that round 7 queued as `AUD-X7` (`LOG.md:170`) plus the round-8
arm's own verification. The record leads with it; §5's entry skeleton does too.

Draft seat: SCR-S8. Draft window: 2026-10-14 19:09:51–19:13Z (16:09–16:13 -03),
host `plazir27`, user `vgpnk` (non-root). Write scope: this file only. Scratch:
`/tmp/w8-scr-s8-tsukuroi/` (`state.txt`, `pins.txt`, `pins-all.txt`,
`gate-run.out`, `oom-anchors.out`, `fixtures-ends.txt`; ephemeral). All probes
read-only; no install/upgrade/remove/restart verb (`PROVINCE.md:16-17`); no
external site; no AUR RPC.

Tags used throughout: [observed] = measured now, command named; [inference] =
join from measurements; [unknown] = named gap with owner.

Round state at draft time [observed]: HEAD
`aa136d69e0e4666b86782152cd1d1fa00f90a0b3` ("probation round 7 (training r6):
see LOG", committed 2026-10-14 16:06:31 -0300 / 19:06:31Z); `git status --short`
empty at 19:10:17Z and again at 19:12:59Z (clean tree). **Round 7 is fully
committed** — the commit carries 8 files (census, SKILL, LOG, SCORECARD,
`update-safety-v2.md`, `aur-risk-plane-ver-s7.md`, `plans/round-7-record-draft.md`,
`plans/round-8.plan.md`). The commit is ~3 minutes old at this freeze: **round 8
has landed nothing yet** — no `*baseline*` / `*.tsv` file anywhere in the tree
(`find` excluding `.git`, empty), the census unchanged (`e2c4558a…`, 1472 lines),
no VER-S8 artifact. Sibling round-8 scratch observed shape-only (19:10–19:13Z,
names only, no content relied on): `/tmp/w8-scrb8/` (poll.sh, poll.log,
spot-archive.txt), `/tmp/w8-arch-tranche/` (hash-manifest lane: arch-hashes.txt
54 275 B + scripts), `/tmp/w8-tameshi-t81/`, `/tmp/w8-prep-m9-nolive.k6Nj/`,
`/tmp/w8-frozen-files.txt`, `/tmp/w8-tracked-files.txt`. The draft's job is to
have the fills ready when the artifacts land.

## 1. Plan anchor and the round's measure

`plans/round-8.plan.md` (md5 `0bef822da196368c47c56426063990fe`, 14 592 B, 216
`wc -l` / 217 as read — **unterminated final line**, mtime 2026-10-14 15:28:21
-03; committed in `aa136d6`; drafted by PREP-S8 during the round-7 wave, so every
round-7 artifact it names is a plan-side reading, never landed state):

> Axis move: operability — the OOM/kill-event plane (round 6's note, 433 ln; its
> kernel arm a bare class count inside the drivers plane) becomes **executable
> as a watch**: the OOM plane joins the census as its next plane line, and its
> content is **new-vs-baseline, fail-closed**.
> Claim (a): the OOM/kill-event watch joins `tools/tsukuroi-census.sh` (round-7's
> realized plane count + 1; expected 5→6, worst-plane rollup unchanged, plane key
> proposal `oom`, adjudicated at landing) — kernel arm C1 retained-window scan
> (`journalctl -k -g … -o short-precise`, boot-separator lines counted out),
> attribution arm C2, kill9/teardown arm C3, presence flags C4 (never counts),
> pressure anchors C5 (rows, verdict-neutral), guards row; new overrides
> `TSUKUROI_CGROUP_DIR`, `TSUKUROI_MEMINFO_FILE`, `TSUKUROI_OOM_BASELINE`.
> Claim (b): new-vs-baseline, fail-closed — `corpus/knowledge/oom-event-baseline.tsv`
> (name adjudicated at landing), one row per declared wave (cluster id, class,
> first/last seen absolute **and boot id**, evidence pointer, note); observed
> cluster matching a row → `known`; not in the baseline → `new` → DEGRADED;
> declared wave absent inside the retained window → `missing` → DEGRADED; absent
> outside → `out_of_window=N`, verdict unchanged; baseline absent/unreadable →
> DEGRADED, never HEALTHY; window unreadable → BLOCKED.
> Claim (c): the contract lands where the executor reads it — SKILL round-8
> append, baseline file, append-only errata pointer in `oom-event-plane.md`,
> `corpus/README.md` row, SCORECARD move row, LOG entry (scribe). The drivers
> plane's `oom=` class count **stays** (distinct value).
> Measure: `--selftest` rc=0 `PASS (N7+M cases, M≥4)` — four new cases:
> known-clean rollup, new-wave→DEGRADED, declared-missing-in-window→DEGRADED,
> window-unreadable→BLOCKED (a fifth, baseline-absent→DEGRADED, if the harness
> shape allows); live run prints the new plane line with a verbatim note and the
> rollup line gains the plane key; zero mutation (fixture byte-unchanged +
> `git status` byte-identical before/after); baseline file landed with md5/line
> count pinned; SKILL/README/SCORECARD/LOG landed; ≥2 baseline rows spot-checked
> by a **non-author** against live probes (re-executing the row's probe).

**Plan anchors re-resolved at draft time [observed]** against the settled
`aa136d6` tree (landed census `e2c4558a…`, 1472 `wc -l`; every anchor below
supersedes the plan's `:174-187` shape list, which described the 1032-line
round-5 revision):

- overrides (every host path is override-able): `:205-227` — `CGROUP_ROOT`
  `:223`, `MEM_SLICE` `:224`, `PRESSURE_FILE` `:225`, `MEMINFO_FILE` `:226`,
  `FOREIGN_BASELINE` `:227`.
- class vocabulary: `CLASS_OOM` `:255` (`Out of memory|oom-kill|oom_reaper`),
  `CLASS_OOM_SYS` `:259`, `CLASS_SIGKILL` `:260`
  (`status=9/KILL|Failed with result '(signal|oom-kill)'`). The C3 class is
  **journal-wide**, not kernel-scope (§3, probe-scope trap).
- foreign watch (round-6 debt, realized): `probe_packages` `:354`, watch block
  `:414-484`, embedded snapshot `R6_FOREIGN_BASELINE` `:238-253`.
- memory-pressure arm (S7-2, realized): `probe_mem_arm` `:685-803` — C1–C3
  probes `:698-719`, C4 sweep `:721-739`, C5 `:741-767`, C6 `:769-784`, verdict
  `:786-799`, `MEM_NOTE` `:801`.
- other probes: `probe_systemd` `:497`, `probe_drivers` `:563` (note `:665`),
  `probe_journal` `:806`.
- selftest: dispatcher `:933-983`, `ok()`/`bad()` `:992-993`, `check()` `:1068`,
  PASS print `:1409`; foreign fixtures `:1170-1205`; S7-2 fixtures `:1355-1407`.
- main: `:1415`; call order `:1444-1449` (`probe_packages; probe_systemd;
  probe_drivers; probe_mem_arm; DRV_V=$(worse "$DRV_V" "$MEM_V"); probe_journal`);
  emitters `:1451-1454`; rollup `:1456-1460`; verdict printf `:1462`; exit map
  `:1465-1469`; `main "$@"` last line (1473 as read / 1472 `wc -l`).

**Plan-premise deltas measured now** (record, don't smooth) [observed]:

1. **Plane count.** The plan says "round-7's realized plane count + 1; expected
   5→6" (`plans/round-8.plan.md:58-59`) — but round 7's realized gate has **4**
   planes: no `PLANE update-safety` landed (§2). The realized move, if the arm
   lands as proposed, is **4→5** with the rollup line gaining one key. The
   plan's "5" was its draft-time expectation of round 7, refuted by the landed
   revision; the record quotes the realized count.
2. **Overrides.** The plan proposes new overrides `TSUKUROI_CGROUP_DIR`,
   `TSUKUROI_MEMINFO_FILE`, `TSUKUROI_OOM_BASELINE` with dispatcher support
   (`:86-87`). Measured: `TSUKUROI_MEMINFO_FILE` (`:226`, in the fixture env
   `:1093`) and a cgroup-root override already exist — the cgroup one under the
   landed name `TSUKUROI_CGROUP_ROOT` (`:223`), **not** the plan's
   `TSUKUROI_CGROUP_DIR`; only `TSUKUROI_OOM_BASELINE` is genuinely new. The
   record quotes the realized names.
3. **Baseline source precedent.** Round 6's proposed `aur-risk-plane.tsv` and
   round 7's plan-side `update-safety-plane.md` both stayed proposals; round 7
   realized its baseline as an **embedded constant** (`base=r6(16)`). §4b's fill
   reads the realized source, never the plan's `oom-event-baseline.tsv` name.

## 2. Step 0 — round-7 landing check against its own measure [observed]

Round-7's measure (its plan's own contract `plans/round-7.plan.md:93-109` plus
the round-8 plan's Step 0 restatement `plans/round-8.plan.md:128-139`): census
revision landed with executed selftest count; round-6 foreign-baseline debt
landed in it (`foreign=` known-vs-new + ≥3 fixtures); v2 note with the name as
landed; round-2 note errata pointer; README/SKILL/SCORECARD/LOG rows; the
round-7 record.

| round-7 member | landed? | pin at draft time |
|---|---|---|
| census revision (S7-1 + S7-2 arms) | **yes** | `tools/tsukuroi-census.sh` md5 `e2c4558a3ae4ddd2eca67e8f4d64281c`, 1472 `wc -l` (1473 as read), 73 919 B; selftest executed by this seat: rc=0, `PASS (49 cases, 49 passed, 0 failed)`; live rc=1, 4-plane rollup (§3) |
| round-6 foreign-baseline debt (known-vs-new + ≥3 fixtures) | **yes** | live note `foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16)`; embedded snapshot `:238-253`; 6 fixtures — hit `:1170` / embedded-default `:1176` / new `:1182` / drift `:1188` / gone `:1194` / absent `:1200` |
| the standalone baseline file | **no — stayed a proposal** | no `*baseline*` / `*.tsv` file in the tree; the realized source is the embedded snapshot |
| v2 decision note | **yes** (landed name ≠ plan draft `update-safety-plane.md`) | `corpus/knowledge/update-safety-v2.md` md5 `92803aea74ebeb1598fa4f450489e5d2`, 353 `wc -l` |
| round-2 note errata pointer (claim (b)) | **no** | `corpus/knowledge/update-safety-note.md` unchanged at `5cc3067fec33d261d8bff6a5c7e8ac48`, 478 `wc -l`; SKILL round-7 errata says still owed (`SKILL.md:971-972`) |
| fifth plane `PLANE update-safety` (claim (a)) | **no** | 4 emitters (`:1451-1454`), 4-term rollup (`:1462`); carried with the tag in `SKILL.md:963-970` |
| verifier note (non-author) | **yes — S7-1 scope only** | `corpus/knowledge/aur-risk-plane-ver-s7.md` md5 `4608743dfa6230e806985d164f3c00f4`, 184 `wc -l`; the S7-2 memory arm has **no** non-author verification — `AUD-X7` queued (`LOG.md:170`) |
| SKILL round-7 append | **yes** | `SKILL.md` md5 `b2b0f6a78b9d25e833af6bd54ec83227`, 983 `wc -l` (984 as read) |
| SCORECARD round-7 row | **yes** | `SCORECARD.md:19` (row 5/6/7 one-liners); the round-4 row `:16` is still malformed — an unescaped `|` truncates the After cell to `boot plane (299 L` |
| LOG round-7 entry | **yes** | `LOG.md:170` (one line; names the AUD-X7 gap) |
| round-7 record draft | **yes** | `plans/round-7-record-draft.md` md5 `c1eed63afdd5ca420ce8b5570fa9b32f`, 425 `wc -l` |
| `corpus/README.md` coverage rows | **no** | unchanged since round 3 (`98bd00668e84f18cf6781718c4d09ea0`, 20 `wc -l`, mtime 12:58 -03) — rounds 4–7 rows collapsed; SKILL round-7 errata names them owed (`SKILL.md:976-979`) |

**Consequence for round 8's order of work [inference].** Three carried items
ride into round 8, and the record must state, per item, finished-or-re-carried:
(i) the fifth plane (update-safety) — carried with tag, no silent assumption;
(ii) the round-2 note errata pointer — a one-line append-only edit owed since
round 7; (iii) `corpus/README.md` rows — debt now rounds 4–8. Round 8's own move
(the OOM plane + baseline) is orthogonal to all three; the plan's Step 0 line
(`:128-139`) says an unlanded part is named debt finished first, so this table
gets re-filled at entry, from the landed tree, never from this draft.

## 3. Draft-time baseline receipts (this seat, read-only)

Gate, re-run 2026-10-14 19:10:28Z (raw captures
`/tmp/w8-scr-s8-tsukuroi/gate-run.out`):

```bash
bash tools/tsukuroi-census.sh --selftest   # 19:10:28Z, rc=0
bash tools/tsukuroi-census.sh              # 19:10:28Z, rc=1
```

Selftest last line verbatim: `TSUKUROI_CENSUS_SELFTEST: PASS (49 cases, 49
passed, 0 failed)`. Live run verbatim:

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T19:10:28Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2[user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922849 C5_swap_peak_pct=99% C5_pswp=72122570/93982664 C5_sock_throttled=67558; C6_psi_some_avg300=0.03 C6_psi_full_avg300=0.03 C6_psi_full_total_us=68862753 C6_avail_kb=20260828 C6_shmem_kb=6367700; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=442 (coredump=279 kernel=139 other=24); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

At landing the record quotes the **post-round-8** run (5-plane line incl.
`PLANE oom:`), never this one. Zero-mutation receipt: `git status --short` empty
before and after the runs; live mode writes nothing (the round-2 guarantee
still holds).

Artifact pins, hashed 2026-10-14 19:10:17Z (clean tree — every hash is of
committed bytes):

| artifact | md5 | lines |
|---|---|---|
| `tools/tsukuroi-census.sh` (round-7 revision) | `e2c4558a3ae4ddd2eca67e8f4d64281c` | 1472 (1473 read) |
| `SKILL.md` (round-7 append landed) | `b2b0f6a78b9d25e833af6bd54ec83227` | 983 (984 read) |
| `LOG.md` / `SCORECARD.md` / `SHONEN.md` | `e0d92542be357341e1701dfa656a9257` / `021bc898bee4e7af2b73bedde38bf764` / `9cf1d450685ae0ed0d15dee1b54e8fd5` | 170 / 19 / 51 |
| `corpus/README.md` | `98bd00668e84f18cf6781718c4d09ea0` | 20 |
| `plans/round-8.plan.md` | `0bef822da196368c47c56426063990fe` | 216 (217 read) |
| `plans/round-7.plan.md` / `plans/round-7-record-draft.md` | `bb9159549bfdad7516af381f6f12965d` / `c1eed63afdd5ca420ce8b5570fa9b32f` | 160 / 425 |
| `corpus/knowledge/update-safety-v2.md` | `92803aea74ebeb1598fa4f450489e5d2` | 353 |
| `corpus/knowledge/aur-risk-plane-ver-s7.md` | `4608743dfa6230e806985d164f3c00f4` | 184 |
| `corpus/knowledge/oom-event-plane.md` | `7e99d712ead088727c0980e52a121199` | 433 |
| `corpus/knowledge/update-safety-note.md` | `5cc3067fec33d261d8bff6a5c7e8ac48` | 478 |
| `corpus/knowledge/aur-risk-plane.md` / `aur-risk-plane-ver-s6.md` | `1a584300f6b07da78bc8332f04b4fd30` / `b0de352dec653891d5d36dd742536198` | 341 / 133 |
| `corpus/knowledge/journal-boot-plane.md` / `boot-plane.md` | `e5ca40dafc4d1d2a2158fded39067df6` / `e722b7a931858aa5ff1a89ce91cccca9` | 430 / 312 |
| `corpus/knowledge/timer-drift-plane.md` / `degraded-triage-r4.md` | `fc0760c8070c9387ff5334f0f8c645cc` / `d57ae2d48e01777e1ef3c8c0ffb642c9` | 332 / 607 |
| `corpus/knowledge/host-health-report-r3.md` / `executor-test-sufficiency.md` | `98a0f263f801245f6069e57a9f72d4af` / `4b2c1d3612db7db1477da92aaec39862` | 563 / 219 |
| `corpus/knowledge/package-state-plane.md` / `systemd-user-plane.md` / `driver-firmware-plane.md` | `ef93f1b78b6a9e17e8c9d096e7852a02` / `af07a829cfd0307fbe970a2cdc054e18` / `518eda8f0f39f25ee95c715571a9cf95` | 323 / 265 / 256 |
| `corpus/knowledge/foreign-provenance-r6.md` | `1b8f47a2a807fc8bd2fc7302f15577c8` | 307 |

Every round-6/7-era pin reproduces exactly at the draft freeze. **Convention
note:** three artifacts carry an **unterminated final line** — the census ends
`main "$@"`, `SKILL.md` and `plans/round-8.plan.md` end `.` — so `wc -l` counts
one fewer than a Read; a pin must state its convention (census 1472/1473, SKILL
983/984, round-8 plan 216/217). `LOG.md`/`SCORECARD.md`/`SHONEN.md`/`README.md`
are newline-terminated.

**OOM-plane anchors re-measured 19:10:45–19:11:30Z** (the fill material for
§4a/§4b; every row re-runnable, none quoted) [observed]:

- boot 0 still `d7f0bc8d938e4249b4a1f250cbfacf58`; `journalctl --list-boots
  --no-pager` = **14 lines = header + 13 boots** (index −12…0; the census's
  `boots=13` counts only `^-?[0-9]+` rows — `probe_journal` `:806-830`).
- **C2 attribution** (`journalctl -g 'kernel OOM killer killed some processes'
  -o short-precise --no-pager`, rc=0) = **3 messages**, verbatim: `Oct 13
  23:44:30.574948 … app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope: The
  kernel OOM killer killed some processes in this unit.` + `Oct 13 23:44:30.576028
  … user@1000.service: …` (event A, two messages) + `Oct 14 13:10:59.400591 …
  user-1000.slice: …` (event B). Both waves still retained at the freeze.
- **C1 kernel family over the whole window** (`journalctl -k -g 'Out of
  memory|oom-kill|oom_reaper' -o short-precise --no-pager`, rc=0) = **3 lines**,
  all `23:44:30`: `.570564 GpuWatchdog invoked oom-killer … oom_score_adj=200`;
  `.638184 oom-kill:constraint=CONSTRAINT_NONE … task=python3,pid=1732581`;
  `.638238 Out of memory: Killed process 1732581 (python3) … anon-rss:27873696kB
  …`. Boot-separator lines (`-- Boot <id> --`) appear in server-side `-g` output
  and are **not messages** — the counting trap the plan flags (`:64-66`); count
  them out.
- **Probe-scope trap (measured):** `journalctl -k -g 'status=9'` → `-- No
  entries --`; the C3 class is **journal-wide** (`CLASS_SIGKILL` `:260`; note
  C3 `oom-event-plane.md:361-362`: event B ⇒ 3 lines). The landed arm reads
  `C3_sigkill=3` because it probes the journal, `-b`; the record's re-run set
  must name the scope (kernel vs all, boot-0 vs retained window) or two honest
  readers will disagree.
- Landed arm state this run (from the census line above): `mem=[DEGRADED]
  C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2; …
  C5_swap_fail=5922849 C5_swap_peak_pct=99%; guards=max/max oom.group=0` — the
  round-8 plane's declared rows must agree with these probes (or the mover is
  recorded).
- Captures drift: vs the round-7 append's 18:39Z run (`SKILL.md:878`), `err=442
  (coredump=279 kernel=139 other=24)` reads identical at 19:10Z while
  `C5_pswp` (72 118 991/93 920 636 → 72 122 570/93 982 664) and the C6 PSI/
  avail fields moved — same-value is a capture, not confirmation.

## 4. Fill rules — what the record must state on landing

**(a) The realized census revision and the new plane.** Ink the post-commit
bytes: new md5 + line count of `tools/tsukuroi-census.sh`; the executed selftest
line `PASS (49+M cases, …)` with case attribution (**49 legacy = 35 base + 6
foreign-baseline `:1170-1205` + 8 S7-2 `:1355-1407`**; M new — the plan's four
named cases plus baseline-absent if the harness shape allows; attribute, never
conflate); the verbatim `PLANE oom:` note from an executed live run (realized
spelling quoted, never this draft's); the rollup line with the new plane key;
the realized plane count (**4→5** — §1 delta 1, not the plan's 5→6). Arm words
and gate mapping **recorded, not silently applied** (plan proposal: CLEAN →
HEALTHY; NEW / DECLARED-MISSING / NO-BASELINE → DEGRADED; BLOCKED → BLOCKED;
composition BLOCKED > {NEW, DECLARED-MISSING, NO-BASELINE} > CLEAN — adjudicated
at landing against the realized round-7 mapping mechanism). Fail-closed
receipts: fixture byte-unchanged assertion, `git status --short` byte-identical
before/after, no mutation. The drivers plane's `oom=` class count **stays**
(double-count precedent, round 3; distinct value = attribution + kill9 +
presence + swap rows, invisible to the kernel arm by construction) — check the
diff carries no duplicated probe. The declared rows at draft time: **event A**
kernel OOM 2026-10-13 23:44:30 (boot `d7f0bc8d…`, victim `python3` 1732581) and
**event B** SIGKILL 2026-10-14 13:10:59 (same boot, `user-1000.slice`).

**(b) The OOM baseline.** Name as landed (`corpus/knowledge/oom-event-baseline.tsv`
is the plan's proposal — read the realized source: file vs embedded constant,
the realized `base=`-style spelling, row count). If a file lands: md5 + `wc -l`
pinned; one row per declared wave (cluster id, class, first/last seen absolute
**and boot id — boot index is not identity**, evidence pointer, note); env
override realized name (proposal `TSUKUROI_OOM_BASELINE`). Rules, each to be
stated with its selftest fixture: observed cluster matching a row → `known`;
cluster not in the baseline → `new` → DEGRADED, cluster printed; declared wave
absent **inside** the retained window → `missing` → DEGRADED (never silently
dropped); absent **outside** → `out_of_window=N`, verdict unchanged (retention
loss is a coverage fact, not a health fact); baseline absent/unreadable →
DEGRADED, never HEALTHY off a missing baseline; window unreadable → BLOCKED (an
empty scan is only a pass if the window itself is measured, rc=0, ≥1 boot). The
**both-readings rule** is printed, never adjudicated: event B's 13:10:59 slice
notice is a late report of the 23:44:30 kill (`boot-plane.md:228-229`) **and** a
session-SIGKILL attribution under `oom-event-plane.md:215-224` (H1–H3) — both
rows verbatim; no round resolves them.

**(c) The contract artifacts.** The `SKILL.md` round-8 append (arm semantics,
the recorded mapping, the counter rule — cgroup `memory.events` oom_kill is a
**presence flag, never a meter** (`oom-event-plane.md:245-257`) — the
both-readings rule, count restatements moved together: the current expected
line is `PASS (49 cases…)` at the identity pin above; a round-8 gate revision
makes it history and must move the round-3/5 restatements with it). The
`corpus/knowledge/oom-event-plane.md` append-only errata pointer ("implemented
at <pin>; the realized contract supersedes §8 where it differs"). `corpus/README.md`
row (or the rounds 4–8 debt stated open). SCORECARD round-8 move row (axis:
operability; Before: 4-plane gate, OOM note-only + `mem=` continuation inside
drivers; After: 5-plane gate, `PLANE oom` watch, baseline known-vs-new). The
`LOG.md` entry (scribe).

**(d) Headline — the VER-S8 closure.** The record's first line carries the
verification, not the landing:

- **AUD-X7** — the queued gap (`LOG.md:170`: "S7-2's memory arm has no non-author
  verification (AUD-X7) — queued") is closed **only if** the landed verifier
  artifact re-measures the S7-2 memory arm with the verifier's own probes (the
  round-7 precedent shape: `aur-risk-plane-ver-s7.md` header + verdict line +
  own commands). Quote the landed name (never assume — the round-7 artifact
  landed as `aur-risk-plane-ver-s7.md`), the verdict verbatim (precedent:
  `CONFIRMED`), and the rows re-executed. If VER-S8 verifies only the round-8
  arm, **AUD-X7 stays open and is named again** — never silently closed.
- **The round-8 arm + baseline rows** — the plan's measure requires ≥2 baseline
  rows spot-checked by a non-author re-executing the row's probe
  (`plans/round-8.plan.md:158-159`); the record quotes the verifier's own
  commands and results (not the author's selftest) and states which fail-closed
  branches fired.
- **A refutation or partial closure is recorded verbatim, not smoothed**
  (round-4 precedent: "VER-S1: P1/D2/U6 CONFIRMED, 755-not-644 correction").
  The author's selftest (`PASS (49+M…)`) is **not** verification; only the
  non-author run closes a named gap.

## 5. Record skeleton (what the `LOG.md` entry must carry on landing)

Round 7 used a one-line entry; the round-8 headline (VER-S8 closure) must stay
on the first line. Candidate (fill at landing):

```
- 2026-10-14 — round 8 (training r7): the OOM/kill-event plane joins the gate as its
  ⟨5th⟩ plane line (⟨4→5⟩-plane census; selftest 49→⟨49+M⟩; M≥⟨4⟩: ⟨case names⟩) + OOM
  baseline ⟨source⟩(⟨md5⟩/⟨lines⟩; known-vs-new, fail-closed) + ⟨OOM note⟩ errata pointer;
  VER-S8 ⟨CONFIRMED/…⟩ — AUD-X7 ⟨closed: S7-2 memory arm verified | still open⟩, ⟨≥2⟩
  baseline rows spot-checked by the non-author. Axis: operability. Verifiers: VER-S8⟨ | …⟩.
```

- **Work (observed in tree):** ⟨artifact list: path, seat/ID, md5, lines, mtime⟩
  — expected members: the census revision (new md5 + case count), the OOM
  baseline (as realized), the SKILL round-8 append, the `oom-event-plane.md`
  errata pointer, the VER-S8 note, plus scribe-owned README/SCORECARD/LOG.
- **Scribe re-verification:** §6 command set; quote the selftest line, the live
  5-plane rollup, one verbatim `PLANE oom:` note, and the re-executed row
  probes (non-author's rows named separately).
- **Ancillary scribe writes (owed at record time):**
  - `SCORECARD.md` round-8 move-log row (axis vocabulary per `AXES.md:9-16`;
    before/after as in §4c); **form defect carried: `SCORECARD.md:16` (round-4
    row) is still malformed** — unescaped `|` truncates the After cell to
    `boot plane (299 L` [observed 19:12Z].
  - `corpus/README.md` coverage rows — debt now rounds 4–7 + round 8; land the
    rows or state the debt stays open, never silently skip.
  - `SKILL.md` count restatements move together with any gate revision (§4c).
- **SHONEN boxes:** stay `[~]` (asserted with verifier names); the round-8
  record may refresh evidence pointers but must not upgrade to `[x]` — that
  stays with the non-author promotion review. `SHONEN.md` unchanged since round
  3 (`9cf1d450…`, 51 `wc -l`) [observed].
- **State at entry:** the round commit hash landed, or "round work uncommitted
  in tree" + exact `git status --short`; the scribe writes only its named
  files; the commit carries the lane identity (`AGENTS.md:5`); commit-message
  pattern `probation round 8 (training r7): see LOG`.

## 6. Scribe re-run set (receipts owed by the record)

```bash
cd ~/Projects/shokunin/tsukuroi-shokunin
bash tools/tsukuroi-census.sh --selftest            # expect rc=0, 49+M/49+M PASS
bash tools/tsukuroi-census.sh                       # expect rc=1(frame), 5-plane rollup + PLANE oom:
md5sum tools/tsukuroi-census.sh; wc -l tools/tsukuroi-census.sh   # landed revision vs e2c4558a…
journalctl --list-boots --no-pager                  # 14 lines = header + 13 boots; index-0 must exist
cat /proc/sys/kernel/random/boot_id                 # boot identity, not boot index
journalctl -k -g 'Out of memory|oom-kill|oom_reaper' -o short-precise --no-pager   # C1 window scan (boot separators counted out)
journalctl -g 'kernel OOM killer killed some processes' -o short-precise --no-pager # C2 attribution
journalctl -b -o json --no-pager --grep 'status=9/KILL'                            # C3, boot-0 journal scope (as the arm runs it)
find /sys/fs/cgroup -xdev \( -name memory.events -o -name memory.events.local \) -print | wc -l   # C4 sweep size
cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.swap.events                   # C5 fail count
grep -E 'SwapTotal|MemAvailable|Shmem' /proc/meminfo; cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.swap.peak
# per baseline row: re-execute the row's own probe (non-author rows named separately)
git status --short                                  # zero-mutation receipt (before/after)
# + landed baseline md5/lines; + the round-8 selftest fixtures read from the executed run
```

Pipeline-rc rule restated: never carry a piped rc as a measurement (`| head`,
`| wc -l`); `journalctl --grep` rc=1 means "0 entries", any other non-zero rc
means "unreadable" (landed rule `:696-698`); boot-separator lines are not
messages.

## 7. Unknowns register (draft-time; owners)

1. Realized round-8 arm shape: plane key (`oom` = proposal), note string, arm
   words, gate mapping, kernel arm scope boot-0 vs retained-window (owner: arm
   seat; the record quotes realized values).
2. Baseline realization: file vs embedded; path; row count; env override name
   (owner: arm seat; plan proposes `corpus/knowledge/oom-event-baseline.tsv` +
   `TSUKUROI_OOM_BASELINE`).
3. VER-S8: landed artifact name; verdict; scope — does it close AUD-X7 (S7-2
   memory arm), verify the round-8 arm, or both? (owner: verifier seat; the
   record states the landed verdict — closure or carried).
4. Retention at landing: waves A/B still in the window? Measured holding at
   19:11Z; the `missing` / `out_of_window` rows are built for loss (owner:
   host/journal; retention policy out of scope).
5. Which carried items round 8 finishes vs re-carries: fifth plane
   (update-safety); round-2 note errata pointer; `README.md` rounds 4–8 (owner:
   note/scribe lanes; §2 re-filled at entry).
6. Whether M is exactly the plan's four cases or five (baseline-absent
   included); only the executed count line decides (owner: arm seat).
7. Both-readings rule of event B — H1–H3 [unknown, read-only unmeasurable] —
   carried, never resolved by a round.
8. Counter-lifecycle model Q2 [unknown] — the presence-flag rule is the
   response; carried.
9. Coredump-storm watch (candidate C) anchors carried for a future draft: live
   census `coredump=279` (19:10Z; 270 at 18:22Z, 269 round 6, 224 round 3 —
   storm drift, every value a capture); coredump dir 4.1 G (round 3); ownership
   godot/node/LOVE + journal workstream; needs an app-level vocabulary and a
   second baseline.
10. Carried rounds 1–7, unchanged: root `-Qkk` delta; `1password-beta`
    provenance (operator); `walker-restart.hook` (kagi/operator); `offline.db`
    coverage debt; the `SCORECARD.md:16` malformed row; the "20-min cap" item
    (owner: integrator); round-2 wave-1 errata merge.

## 8. Errata / pending (append-only)

- 2026-10-14 — this draft file created by SCR-S8; it is prep, not a record. The
  `LOG.md` round-8 entry remains owed (`AGENTS.md:3`); measures are judged
  against the landed census revision + baseline + VER-S8 note, not this
  skeleton.
- 2026-10-14 — all counts in §3 are captures on a live host (coredump storm
  live; C5/C6 counters move between runs); re-run, never quote.
- 2026-10-14 — Step 0 result recorded above: round 7 finished its foreign
  baseline debt and its v2 note; carried are the fifth plane, the round-2 errata
  pointer, and the README rows; `AUD-X7` stays queued until a non-author
  re-measures the S7-2 memory arm. This draft re-designs nothing; it names the
  debts for the record scribe.
- 2026-10-14 — plan-vs-landed deltas measured (§1): plane-count expectation
  5→6 vs realized 4; `TSUKUROI_CGROUP_DIR` proposal vs landed
  `TSUKUROI_CGROUP_ROOT`; `TSUKUROI_MEMINFO_FILE` already landed; the
  `oom-event-baseline.tsv` name is a proposal. The record quotes realized
  values.
- 2026-10-14 — the round is concurrent: no round-8 artifact had landed at
  19:10Z; sibling scratch dirs observed shape-only (names/timestamps). The
  record scribe fills every generic slot with actual filenames, md5s and
  executed lines at entry.
- 2026-10-14 19:15:52Z — **post-freeze tree movement (append-only, shape
  only)**: the tree gained `?? plans/round-9.plan.md` (a sibling lane's
  next-round draft; **not** a write by this seat) alongside this file
  (`?? plans/round-8-record-draft.md`). The census was still byte-identical at
  `e2c4558a…` (1472 `wc -l`) and no `*baseline*` / `*.tsv` file existed at that
  observation — no round-8 arm artifact had landed. The draft-time readings
  above are kept as the freeze-time (19:09:51–19:13Z) state; nothing was
  re-measured against any later revision.
- 2026-10-14 — final-file spot-check and this file's own line count/md5 are
  reported in the seat's handoff, not in-file (a further edit would invalidate
  them).