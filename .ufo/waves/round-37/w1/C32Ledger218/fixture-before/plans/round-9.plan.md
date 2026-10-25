# WWKD plan — tsukuroi round 9 (ufo-round-plan-v1)

Draft lane: PREP-S9 (2026-10-14, drafted during the round-8 wave). Design-time
state read by this lane, not taken from a record: HEAD `aa136d6` (round-7
commit, 2026-10-14 16:06:31 -03 = 19:06:31Z) with `git status --short` **empty
at this draft's freeze 19:14:32Z** — round 7 is fully committed and round 8 had
landed nothing at the freeze. `plans/round-8.plan.md` (md5
`0bef822da196368c47c56426063990fe`, 216 `wc -l`, unterminated final line) is
cited as a **plan**, never as landed state; every round-8 statement below is a
draft-time reading that Step 0 resolves. Sibling round-8 scratch dirs are live
(shape only, 19:14:32Z): `/tmp/w8-tsukuroi-s81`, `/tmp/w8-s82-tsukuroi`,
`/tmp/w8-s83-tsukuroi`, `/tmp/w8-tsukuroi-s84`, `/tmp/w8-scr-s8-tsukuroi`,
`/tmp/w8-aud-s8-tsukuroi` — the round-8 seats are working; no pin here is taken
from a moving revision.

Axis move: **coverage + operability — the last note family without an
executable presence becomes executable: the update-safety plane joins
`tools/tsukuroi-census.sh` as its next plane line**, carrying the update-safety
arm vocabulary and the two rules the landed corpus already measured — the
channel-freshness rule ("empty proves nothing newer than a 36-day-old snapshot")
and the class fold ("resolvable ≠ maintainable"). One move, one surface: round
7's claim (a) (`plans/round-7.plan.md:53-79`) is **finished from its own
measured model, not re-designed** — it is tagged *not landed* in the landed tree
(`SKILL.md:963-969`: no `PLANE update-safety` emitter, no fifth rollup term,
checked against `e2c4558a…`; `corpus/knowledge/update-safety-v2.md:24-25,33`:
claim (a) is "a sibling lane's deliverable and is **not** carried in this
file"), and it is the one contract item no later round has claimed (round 8
claims the OOM plane as its move; its Step 0 debt list names the v2 note's
landed name and the round-2 errata pointer, not the unlanded fifth plane —
`plans/round-8.plan.md:127-139`, a plan, never landed state).

## Candidate decision (why this one)

Post-round-7 candidates were: (A) the update-safety plane in the gate; (B) the
coredump-storm watch; (C) the memory arm's non-author verification (AUD-X7) +
gate re-sweep; (D) the discernment ledger (`corpus/lessons/`).

- (B) is deferred again, not rejected — and this is its third draft in a row,
  which is itself a signal to schedule it. Measured drift: census
  `coredump=279` this boot (19:10:40Z) against 224 (round 3), 269 (round 6),
  270 (round-8 draft 18:22Z) — every value a capture. Anchors recorded below
  for a future slot; the class still needs an app-level vocabulary and a second
  baseline before a watch can mean anything.
- (C) is a named gap, not a move: round 7's LOG names it verbatim ("S7-2's
  memory arm has no non-author verification (AUD-X7) — queued"), and the landed
  verifier note covers the *foreign* arm only (`aur-risk-plane-ver-s7.md`,
  md5 `4608743d…`, 184 ln, VER-S7 = S7-1 scope). It is Step 0 debt (finished
  first if round 8 did not) and this round's verifier seat — not a second move.
- (D) is real and measured — `corpus/lessons/` holds **0 files** after seven
  rounds (`ls corpus/lessons` empty), `corpus/QUALITY.md` is 8 lines, and the
  LOG has carried "`corpus/lessons/round-1.md` Gate section + non-author
  spot-check" as open debt since round 3 — but it cannot be the move: the
  per-round candidate/reject decisions were never recorded at the time, so a
  retro Gate would have to invent them. The honest forward version of (D) is
  this round's own lesson file (claim (c)); no retro-fabrication.
- (A) is the move: it is the last note family with no executable presence (the
  criterion round 8's own plan uses, applied to the family that actually has
  none — the OOM family already runs as the `mem=` arm, `SKILL.md:904-924`),
  its contract was drafted and never landed (round 7), every probe it needs is
  already exercised read-only (measured below, zero mutation), and the
  measured model for its semantics exists in the landed tree (round-2 block
  `SKILL.md:359-369`; v2 note §4/§7; `aur-risk-plane.md:55-89` rows).

## Claim

(a) **The update-safety plane joins `tools/tsukuroi-census.sh`** (realized
    plane count + 1; 4 today — Step 0 resolves the count after round 8; worst-
    plane rollup unchanged, plane key proposal `update-safety`, adjudicated at
    landing). Probes, all read-only and already exercised (receipts below):
    - **candidates, two ways** — `pacman -Qu` (rc/emptiness, **unpiped**: the
      pipeline-rc trap stays live) and `pacman -Sup --print-format '%r/%n %v'`
      (the one allowed plan verb, `SKILL.md:408-416`); candidates > 0 →
      `REQUIRES-PREP` with count and names; a probe unreadable → `BLOCKED`,
      never a pass; the `expac`-vs-`-Sl` version join (expac present,
      `/usr/bin/expac` 10, measured) is a third reading — its absence must
      print `join=unavailable`, not a silent pass.
    - **channel freshness** — sync-db **births** (`stat -c %w`; the
      birth-vs-mtime trap stays a printed rule: mtimes here are upstream
      stamps), printed as age-in-days at the run's date; the arm's rule: an
      empty `-Qu` is `INERT` **only** with the channel reading present, and the
      staleness is printed with it (36 d today).
    - **offline.db + log tail** — `$PACMAN_DB/sync/offline.db`
      presence/birth; bounded `/var/log/pacman.log` tail for the last
      refresh/upgrade command class (birth is authoritative, the log adds the
      command; a window miss → `cmd=unknown` row, verdict unaffected).
    - **class fold (exposure only)** — read the **same-process** packages-arm
      reading (`foreign=` known-vs-new, already computed by `probe_packages`),
      never re-probe `-Qm`: `classes=offline-exile:14,aur-local:2` from the
      register's rows (`aur-risk-plane.md:55-89`), `unknown-provenance` names
      when the arm reports `new`, `unavailable` when the baseline is
      absent/unreadable → DEGRADED (never HEALTHY off a missing baseline).
      Pins/holds stay in the packages plane — no double-probe.
    - **trap row (verb-level, verdict-neutral unless the mapping says
      otherwise)** — the `-Suu` downgrade trap (`pacman -Suu --print-format`
      prints exactly one action today: `omarchy/1password-beta
      8.12.42_32.BETA-1`); `DO-NOT` stays note content per the round-7
      proposal, adjudicated at landing.

    Arm word carried in the note line: `PASS · INERT · REQUIRES-PREP ·
    BLOCKED · UNKNOWN-UPSTREAM · DO-NOT`; composition `BLOCKED >
    UNKNOWN-UPSTREAM > REQUIRES-PREP > INERT > PASS`
    (`SKILL.md:359-369`, `update-safety-note.md:334-339`). Gate-verdict mapping
    **recorded, not silently applied** (proposal: INERT/PASS→HEALTHY,
    REQUIRES-PREP/UNKNOWN-UPSTREAM→DEGRADED, BLOCKED→BLOCKED; the realized
    mapping is quoted at landing). The realized note string is quoted from an
    executed run at landing, never this proposal; the plane line must name the
    note's own traps (shadowing: `-Qu` never shows a shadowed omarchy copy,
    `SKILL.md:395-397`; `--print-format '%s'` is not a size, `:389-391`).
(b) **Fail-closed, with fixtures.** New selftest cases (≥4, the fixture
    dispatcher `:1075-1093` + `EXTRA_ENV` pattern `:1175` onward; proposed, the
    realized set is quoted at landing):
    - INERT-clean → the N+1-plane rollup, new term present;
    - candidates > 0 (fixture `-Qu`/`-Sup` answer) → REQUIRES-PREP → DEGRADED
      with names printed;
    - `-Qu` unreadable → BLOCKED, **never** INERT;
    - channel unreadable (no `sync/` dir in the fixture db) → BLOCKED, never
      INERT — the "empty ≠ up to date" rule made executable;
    - class fold with an absent baseline → DEGRADED (the round-6/7 rule),
      if the harness shape allows a fifth case.
    New overrides in the `TSUKUROI_*` family, dispatcher-supported: proposal
    `TSUKUROI_PACMAN_LOG` (default `/var/log/pacman.log`), `TSUKUROI_OFFLINE_DB`
    (default `$PACMAN_DB/sync/offline.db`). **Named fixture prerequisite
    [design, adjudicated at landing]:** a fixture file's birth is the fixture
    creation time, so the *stale-channel* reading needs a documented seam (the
    channel stamp must be redirectable, or that case is vacuous and must not be
    claimed — the round-5 lesson: a case that cannot fail is not a case).
(c) **The contract lands where the executor reads it**: the `SKILL.md` round-9
    append (plane semantics, the realized mapping, the channel-freshness rule,
    the fold, count restatements moved together — the rule at `SKILL.md:925-929`
    is live: a gate revision voids the deferrals), the **v2 note's append-only
    errata pointer** ("implemented at <pin>; the realized contract supersedes
    §10 where it differs"), `corpus/README.md` **back-rows for rounds 3-8** (the
    map is the surface the new plane's note must appear on; it is unchanged
    since round 3 — measured below), the SCORECARD move row (before: 4-plane
    gate, update-safety note-only → after: N+1-plane gate) and the LOG entry
    (scribe). Plus the round's own lesson file `corpus/lessons/round-9.md`
    (`LEARNING.md:37-43,61`: the `## Gate` section + the outside spot-check on
    at least one admit and one reject) — the lane's first; the empty
    `corpus/lessons/` is measured, and starting the ledger is hygiene, not a
    second move. **No re-landing**: if round 8 lands any of these, the round
    records the realized one and does not re-do it.

Step 0 (mechanical, before any edit): round-8 landing check against its own
measure — census revision (md5/line count/**selftest count from an executed
run**), whether the OOM plane landed as a `PLANE` line or as a `mem=` extension
(both are within round 8's own plan; the landed shape governs), the baseline
file if any (the round-8 plan's proposal `corpus/knowledge/oom-event-baseline.tsv`;
the landed name wins over any plan name), SKILL append, README/SCORECARD/LOG
rows, the round-8 record. Then the round-7 debt list, item by item: (i)
`PLANE update-safety` absent/present — **if present, this move re-scopes to the
same surface one rung further** (the plane's non-author verification + the fold's
fail-closed branches), never re-landing a landed arm; (ii) the round-2 note
errata pointer — still owed at the freeze (`update-safety-note.md` md5
`5cc3067f…`, 478 ln, unchanged); (iii) `corpus/README.md` rows — still owed
(20 lines, last touched round 3, `git log --oneline -- corpus/README.md` →
`9bcd162`); (iv) AUD-X7 — still open (the landed verifier note covers S7-1
only); (v) `SCORECARD.md:16` (round-4 row) malformed — the unescaped `|` is
still there (measured: the row reads `| 4 | freshness + depth | round-3 state |
boot plane (299 L | wave-4 32-lane; VER-S1 |`). An unlanded part is named debt
finished first against the plan that specified it, not re-designed. Then
re-measure every pin below; a mismatch is recorded, not smoothed.

Anti-claim: the arm runs no mutating verb — `-Qu`, `-Su* --print*` (plan verbs),
`stat`, bounded log reads; `-Sy`/`-Syu` are never run, no transaction, no
download, no db write (`db.lck` absent after every probe here); no external
site, no AUR RPC, upstream state stays [unknown] read-only; empty candidates
are never reported as "up to date" — the channel age is printed with them; an
unreadable probe is BLOCKED, never INERT; the fold names exposure, never
auto-remediates and never touches `IgnorePkg`; a `new` foreign row is printed,
never silently classified; `DO-NOT` never becomes a transaction; the plane
never re-probes pins/holds or `-Qm`; the coredump class (V8 heap-OOM, the
storm) stays with its owners (`oom-event-plane.md:43-52`); root probes stay
BLOCKED and are not escalated; no round-6/7/8 artifact is re-measured from
memory — every citation is re-hashed at dispatch.

Measure: `--selftest` rc=0 with `PASS (N9+M cases, M≥4)` (the four cases in
(b); a fifth if the harness shape allows); live run prints the new plane line
with a verbatim note and the rollup line gains the plane term; zero mutation
(fixture byte-unchanged + `git status` byte-identical before/after + no
`db.lck`); the note's errata pointer + SKILL append + README back-rows +
SCORECARD + LOG + `corpus/lessons/round-9.md` landed; ≥2 plane rows
spot-checked by a **non-author** against live probes (re-executing the row's
probe), plus AUD-X7 closed if round 8 left it open (a verifier note for the
`mem=` arm, same shape as `aur-risk-plane-ver-s7.md`). Suggested seats: plane
seat (census + fixtures + fold), note/hygiene seat (SKILL append + errata
pointer + README back-rows + lesson), non-author verifier (plane rows;
AUD-X7), scribe (SCORECARD/LOG/commit).

Draft-time pins (this lane, 2026-10-14 19:09:58-19:16Z, read-only, non-root,
scratch `/tmp/w8-preps9-tsukuroi/`; re-run, never quote). Line counts are
`wc -l`; three artifacts carry an **unterminated final line** (census ends
`main "$@"`, SKILL.md and round-8.plan.md end `.`), so Read counts one more — a
pin must state its convention. HEAD `aa136d6`, tree clean at 19:14:32Z; census
(HEAD revision) md5 `e2c4558a3ae4ddd2eca67e8f4d64281c`, 1472 `wc -l`, 73 919 B,
selftest rc=0 in 4.48 s `PASS (49 cases, 49 passed, 0 failed)`, live rc=1
(19:10:40Z):

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T19:10:40Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2[user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922849 C5_swap_peak_pct=99% C5_pswp=72122572/94017352 C5_sock_throttled=67558; C6_psi_some_avg300=0.03 C6_psi_full_avg300=0.03 C6_psi_full_total_us=68892127 C6_avail_kb=20403260 C6_shmem_kb=6246944; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=442 (coredump=279 kernel=139 other=24); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

— **four** `PLANE` emitters, no `PLANE update-safety`; zero mutation (`git
status` 0 lines before/after; no `db.lck`). Update-safety probe receipts
(19:14-19:16Z, unpiped rcs): `pacman -Qu` rc=1, 0 lines; `pacman -Sup
--print-format '%r/%n %v'` rc=0, 0 lines; `pacman -Suu --print-format` rc=0,
one action `omarchy/1password-beta 8.12.42_32.BETA-1`; `/var/lib/pacman/db.lck`
absent; sync-db births core/extra/multilib/omarchy all `2026-10-11
12:54:13.542054496 -0300` (offline.db `2026-10-03 17:41:33.994891750 -0300`),
mtimes core/extra/multilib `2026-09-08` (**36 d** before the run), omarchy
`2026-10-11`, offline `2026-07-20`; `/var/log/pacman.log` 2109 lines, last
entry `2026-10-13T16:37:59-0300` (`installed git-filter-repo (2.47.0-3)`);
`pacman -Qm` = 16; `expac` present (`/usr/bin/expac`, `10`); `journalctl
--list-boots` 14 lines (13 boots + header). Gate extension shapes to find on
the landed revision: overrides block :207-241, `R6_FOREIGN_BASELINE` + `CLASS_*`
constants :242-267, `usage()` :269, `probe_packages` :354, `probe_systemd`
:497, `probe_drivers` :563, `probe_mem_arm` :685, `probe_journal` :806,
`run_selftest` :924 (fixture dispatcher :1075-1093, `EXTRA_ENV` cases :1175+
onward, PASS print :1409), `main()` :1415 (probes :1446-1449, emitters
:1451-1454, rollup :1456-1460, verdict :1462-1463, exit map :1465-1470); the
mem arm folds as `DRV_V=$(worse "$DRV_V" "$MEM_V")` (:1449) — the model the new
plane's rollup term copies. Artifact pins (full md5): `SKILL.md`
`b2b0f6a78b9d25e833af6bd54ec83227` 983, `SCORECARD.md`
`021bc898bee4e7af2b73bedde38bf764` 19, `LOG.md`
`e0d92542be357341e1701dfa656a9257` 170, `SHONEN.md`
`9cf1d450685ae0ed0d15dee1b54e8fd5` 51, `corpus/README.md`
`98bd00668e84f18cf6781718c4d09ea0` **20** (unchanged since round 3), `corpus/QUALITY.md`
`e31cef8e56f3666406ab9314d3de3f0e` 8, `corpus/lessons/` **0 files**,
`corpus/knowledge/update-safety-v2.md` `92803aea74ebeb1598fa4f450489e5d2` 353,
`update-safety-note.md` `5cc3067fec33d261d8bff6a5c7e8ac48` 478,
`oom-event-plane.md` `7e99d712ead088727c0980e52a121199` 433 (4th reproduction),
`aur-risk-plane-ver-s7.md` `4608743dfa6230e806985d164f3c00f4` 184,
`aur-risk-plane.md` `1a584300f6b07da78bc8332f04b4fd30` 341,
`foreign-provenance-r6.md` `1b8f47a2a807fc8bd2fc7302f15577c8` 307,
`plans/round-7.plan.md` `bb9159549bfdad7516af381f6f12965d` 160,
`plans/round-8.plan.md` `0bef822da196368c47c56426063990fe` 216.

Deferred candidate (B) anchors for a future slot: live census `coredump=279`
(19:10:40Z; 224 round 3, 269 round 6, 270 round-8 draft — storm drift, every
value a capture); `/var/lib/systemd/coredump` **250 files / 4.0 G** (19:16Z;
4.1 G round 3); `coredumpctl list` 455 lines (capture, header included);
per-app attribution exists in a note (systemd-user-plane r1: 198 this boot =
godot 142 + node 47) but not in the gate; the class needs an app-level
vocabulary and a second baseline before a watch can exist; ownership godot/node/
LOVE app lanes + the journal workstream (boundary `oom-event-plane.md:43-52`).

Bounds & unknowns: round-8 landing state at dispatch [unknown — Step 0];
whether round 8 realizes the OOM plane as `PLANE oom` or as an arm extension,
and whether it lands the README rows / the round-2 errata pointer / AUD-X7
[unknown — Step 0]; whether `PLANE update-safety` is landed by round 8 as
Step-0 debt [unknown — Step 0, with the re-scope rule above]; the realized
plane count N9 and case count N9+M [unknown — from the executed run at
dispatch]; the stale-channel fixture seam [design — adjudicated at landing, or
the case is dropped, never claimed vacuous]; the upstream Arch/omarchy delta
since 2026-09-08 — **the** real update gate — stays [unknown] read-only (the
36 d stamp is a capture); `pacman.log` rotation window at dispatch [unknown —
the `cmd=unknown` row is built for the miss]; carried: root `-Qkk` delta,
`1password-beta` provenance (operator), `walker-restart.hook` (kagi/operator),
dkms stale `7.1.4-arch1-1`, `snapper` empty, `offline.db` coverage debt,
`omarchy-walker`↔`walker` linkage (kaidoku/revenger), the "20-min cap" item
(integrator), V8 heap-OOM and coredump-storm boundaries, B (coredump) and D
(discernment ledger across rounds 1-8) as named schedule candidates.

Discipline (round 9): host read-only (`PROVINCE.md:16-17`); no external sites;
secrets shape-only; one move; append-only errata; observation / inference /
unknown separated; write scope = the named artifacts only (this draft wrote
only this file).