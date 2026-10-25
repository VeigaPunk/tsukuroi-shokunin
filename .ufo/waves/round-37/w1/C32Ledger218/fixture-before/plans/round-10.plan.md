# WWKD plan — tsukuroi round 10 (ufo-round-plan-v1)

Draft lane: PREP-S10 (2026-10-14, drafted during the round-9 wave). Design-time
state read by this lane, not taken from a record: HEAD `72b038da9b2b1da2a37d35e3cce2d1d7650f70be`
(round-8 commit, 2026-10-14 16:55:09 -03 = 19:55:09Z) with `git status --short`
**empty at this draft's freeze 19:57:37Z**; round 8 landed **no gate edit** —
the census at HEAD is byte-identical to round 7's (`e2c4558a…`, 1472 `wc -l`,
73 919 B, re-hashed here against `git show HEAD:`; `SKILL.md:1001-1006`'s
identity block reproduces, sha256 included). Post-freeze shape observation
(20:02:06–20:03:14Z; **shape/hash only, no content relied on**): the tree
gained `?? corpus/knowledge/aur-drift-receipt-r9.md`,
`?? plans/round-9-record-draft.md`, and ` M tools/tsukuroi-census.sh` — the
census was **moving** (`2f746336…`, 1572 `wc -l` at 20:03:07Z against the
freeze revision's 1472) — the round-9 arm seat is landing the fifth plane.
**No pin below is taken from the moving revision**, and no gate run was made
against it. Round-9 scratch dirs live (19:58–20:02Z, shape only):
`/tmp/w9-tsukuroi-s91` (battery outputs), `-s92`, `-s93/live/`, `-s94`
(`census.pin`, `append-draft.md`), `-scr-s9`. `plans/round-9.plan.md` (md5
`3a59d2edd068abf6281d7701d261ea5c`, 270 `wc -l`, unterminated final line) is
cited as a **plan**, never as landed state; every round-9 statement below is a
draft-time reading that Step 0 resolves.

Axis move: **calibration — the lane's first** (rounds 1–8 moved operability,
freshness, depth, adjacency, coverage; calibration is the trend furthest
behind, `LEARNING.md:23-33`). The move is the **ten-round synthesis**: the
lane's own claim-vs-realized ledger for rounds 1–10, and the **standing
discipline of the census** it distills — the rules that keep the realized gate
(5 planes expected after round 9; Step 0 resolves the count) re-derivable by a
non-author instead of remembered by the author. One move, one subject: the
census's standing discipline, with the synthesis as its evidence base. Round
10 is the lane's tenth round (probation 1–3, training r3–r9); the synthesis is
written to stand whether or not any further wave follows [unknown]. Every row
is assembled from re-hashed landed pins at dispatch; no row quotes a plan as
landed state, and no row is quoted from memory.

## Candidate decision (why this one)

Post-round-8 candidates were: (A) the standing discipline + the ten-round
synthesis (calibration); (B) the `PLANE oom` watch round 8 specified and did
not land; (C) the coredump-storm watch (deferred a third time); (D) the
update-safety plane's own non-author verification (owed by round 9's own
measure); (E) the carried operator/boundary ledger.

- (B) is real, measured, and **specified but not landed** in the tree
  (`SKILL.md:1132-1143`; re-checked here at the freeze revision: no `PLANE
  oom` emitter, no `*baseline*`/`*.tsv` file anywhere in the tree). It is not
  this move: it is Step-0 debt (if round 9 landed it, round 10 verifies it,
  never re-lands it), and otherwise a carried row in the synthesis's open
  ledger with its spec intact — which is exactly the calibration point: an
  unlanded claim stops being invisible.
- (C) is deferred a fourth time, not rejected, with the sharpest anchors yet
  measured: census `coredump=467` this boot (19:58:48Z) against 279
  (19:10:40Z, same boot — the round-9 plan's live capture), 269 (round-6
  capture), 224 (round-3 report) — every value a capture. The class still
  needs an app-level vocabulary and a second baseline before a watch can mean
  anything; ownership stays godot/node/LOVE app lanes + the journal
  workstream (boundary `oom-event-plane.md:43-52`).
- (D) is a Step-0 obligation, not a candidate: a non-author verification of
  round 9's plane is part of round 9's own measure; if the landed round-9 set
  lacks it, round 10 finishes it first against round 9's contract — the same
  rule every round has applied to its predecessor.
- (E) is carried into the synthesis's debt ledger with owners, not absorbed:
  root `-Qkk` delta; `1password-beta` provenance (operator);
  `walker-restart.hook` (kagi/operator); dkms stale `7.1.4-arch1-1`;
  `snapper` empty; `offline.db` coverage; the `SCORECARD.md:16` malformed row;
  the "20-min cap" item (integrator); E4–E8 proposed-but-unapplied errata on
  `oom-event-plane.md`.
- (A) is the move: round 10 is the lane's tenth round; the arc's claims and
  mismeasures are all measurable from landed artifacts; and the discipline
  that keeps the gate standing has never been written as **standing rules** —
  it lives scattered across nine rounds of appends, each rule provable, none
  re-derivable in one pass. The synthesis is the one artifact no round has
  produced; `corpus/lessons/` is still **0 files** and `corpus/README.md`
  unchanged since round 3 (both measured below).

## Claim

(a) **The census's standing discipline is distilled into standing rows** —
    one table (target `corpus/knowledge/ten-round-synthesis.md` §4; the
    realized note name and row set are quoted at landing, never this
    proposal), every row citing the landed artifact + round that measured it.
    **No row makes a new host claim.** Rows carried (each already landed; the
    lane-level analogue is `SKILL.md:11-18` "Standing rules"):
    - **D1 fail-closed** — an unreadable probe is `BLOCKED`/`unknown=`, never
      a pass (`SKILL.md:27-31`; the round-2/3 fail-closed cases; round 9's
      channel branch repeats it).
    - **D2 empty-proof** — an empty scan passes only with the scan itself
      measured (journal rc=0 + ≥1 boot; an empty `-Qu` only with the channel
      reading printed — round-7/9 rules).
    - **D3 counts move together** — the gate's restated case count equals the
      executed count; a gate revision moves every restatement with it (the
      live rule at `SKILL.md:925-929`; history at `:519-521`, `:600-602`,
      `:686-688`, `:866-868`, `:1147-1151`).
    - **D4 captures, not quotes** — every count/verdict is a capture; re-run,
      never quote (the coredump drift below is this rule's proof).
    - **D5 pins state their convention** — full md5/sha256, `wc -l` vs
      Read-count, unterminated final line named (`SKILL.md:1001-1006`).
    - **D6 no pin from a moving revision** — concurrent seats; a moving file
      is observed shape-only (round-8/9 practice, reused above).
    - **D7 sample rc never decides** — the bounded `-Qkk` sample's rc is not
      evidence; drift decides (`SKILL.md:235-357`).
    - **D8 zero mutation** — live mode writes nothing; the suite asserts the
      fixture byte-unchanged; `git status` byte-identical before/after; no
      `db.lck` (round-2→9 receipts; `SKILL.md:265,292,866,883`).
    - **D9 one probe per fact** — arm folds read a same-process reading, never
      re-probe; deliberate double-counts are distinct-value only (round-3
      rule, round-7/9 reuse).
    - **D10 printed traps** — each plane line/block names its own traps
      (line-vs-entry, birth-vs-mtime, `-Qu` shadowing, `%s` not a size,
      pipeline rc) — the per-plane blocks of `SKILL.md`.
    - **D11 plane-set consistency (new, mechanical)** — the rollup line names
      exactly the planes that emitted; a plane added or dropped must move both
      in one revision (the freeze revision has no such check: the rollup and
      verdict lines hardcode four keys, `:1456-1464`).
    - **D12 one-command re-derivation (new, mechanical)** — the revision's
      identity (md5/sha256/lines/bytes, declared case count, plane keys, exit
      map) prints as one machine-readable line, so a non-author re-derives the
      pin without the author. Proposal: an `--identity` mode; the realized
      name and fields are adjudicated at landing; a field the landed harness
      cannot support prints `unverifiable`, never a guess.
    - **D13 attested ≠ verified** — an author's suite is author evidence; each
      new arm's verification is a non-author replay (round-5 tameshi sweep,
      round-8 VER-S8; round 9's plane owes its own — Step 0).
(b) **The mechanical rows are executable and fail-closed, with fixtures.**
    New selftest cases (≥4; the realized set is quoted at landing; the
    round-5 lesson applies — no case is claimed that cannot fail):
    - rollup-key set == emitted plane set, asserted on one invocation's stdout
      (falsifiable by dropping a rollup term or an emitter);
    - crown verdict == the worst plane verdict, recomputed on a forced mixed
      fixture (one BLOCKED + one DEGRADED → crown BLOCKED, exit 2);
    - identity fields independently recomputed in the suite (md5/`wc` over
      the same file) must match — a mutated fixture copy must be caught;
    - identity input unreadable, or `$0` not the revision (piped invocation,
      missing copy) → `unverifiable`, **never** `ok`; rc per the fail-closed
      stance;
    - a fifth case (identity `cases=` vs the executed count) only if it can be
      made non-vacuous.
    The mode is a **re-derivation aid, not verification** (D13) — the note and
    the append say so, so no later round can cite the tool as its own
    non-author check.
(c) **The synthesis lands where the lane and the executor read it.**
    - `corpus/knowledge/ten-round-synthesis.md` (proposal; the landed name
      wins): §1 the ten-round ledger — rounds 1–10, one row each: dispatch
      plan (md5/`wc -l`; round 1 has **no plan file**, measured), the claim,
      the realized artifact + re-hashed pin, the mismeasure the round caught
      (counted, cited), debt created/finished; §2 the gate arc — 744 lines
      (743 `wc -l`) / 17 cases / 3 planes (`7a3d3b94…`) → 976 / 26 / 4
      (`41953ee9…`) → 1 032 / 35 (`SKILL.md:687-688`) → 1472 / 49 / 4
      (`e2c4558a…`) → round 9's realized revision — **executed runs only,
      each row citing its landed artifact**; §3 the calibration record —
      every self-correction counted and cited (round-1's four retractions;
      round-4's 755-not-644; round-5's 1/4 survivors; round-8's M01
      prediction miss, method delta, 9 un-exercised clause sites); §4 the
      standing-discipline table (a); §5 the debt ledger (open, with owners);
      §6 the unknowns register (the carried `[unknown]` classes); §7 the
      closing state (probation rounds 1–10; `SHONEN` boxes with evidence;
      `[x]` stays with the non-author review — no self-promotion).
    - `SKILL.md` round-10 append: the standing-discipline block (compact,
      citing the note §), the final count restatements moved together with the
      identity pin at the realized revision, the D13 warning.
    - `corpus/README.md`: the coverage back-rows (rounds 4–9 debt; the gate
      rows for the round-7 and round-9 revisions; the synthesis note) and the
      `## Frontier` section owed since round 1 (`LEARNING.md:57-58`).
    - `SCORECARD.md`: the final move row (calibration; the ten-round axis
      summary) and the `SCORECARD.md:16` malformed row repaired **with its
      original text preserved verbatim** (the unescaped `|` escaped only), the
      repair recorded in the LOG — proposal, adjudicated at landing: a
      repaired historical row must stay readable as history.
    - `corpus/lessons/round-10.md`: the `## Gate` section + the outside spot
      check (≥1 admit, ≥1 reject) per `LEARNING.md:37-43`.
    - LOG closing entry (scribe). **Closing hygiene, owed since round 3**: the
      post-append no-oral-context re-test against the final `SKILL.md`
      revision (`LOG.md:153-154`; `SHONEN.md:32-38`) — an executor seat, the
      tally recorded whatever it is; not a second move.

Step 0 (mechanical, before any edit): round-9 landing check against its own
measure — census revision (md5/`wc -l`/bytes/**selftest count from an executed
run**), whether `PLANE update-safety` landed as a plane line or an extension
(the landed shape governs), the realized arm words/composition/mapping and the
fold, the `SKILL.md` round-9 append, the v2-note errata pointer, README
back-rows, `corpus/lessons/round-9.md`, the round-9 record (a draft file was
appearing at 20:02Z; **the landed name governs**). An unlanded part is named
debt finished first against the plan that specified it, never re-designed.
Then the round-8 carried ledger, item by item: (i) `PLANE oom` — specified,
not landed (`SKILL.md:1132-1143`); (ii) the round-2 note errata pointer —
still owed (note md5 `5cc3067f…`, 478 `wc -l`, unchanged); (iii) README rows —
still owed (md5 `98bd0066…`, 20 `wc -l`, unchanged since round 3); (iv)
`SCORECARD.md:16` — still malformed verbatim (the row reads `| 4 | freshness +
depth | round-3 state | boot plane (299 L | wave-4 32-lane; VER-S1 |`); (v)
E4–E8 errata proposed on `oom-event-plane.md`, not applied (that note's owner
applies them). Then re-measure every pin below; a mismatch is recorded, not
smoothed.

Anti-claim: rows make no new host claim — every row cites a landed artifact
and is re-hashed at dispatch, never quoted from this draft; the identity mode
re-derives, it never verifies (D13 — a self-identity is not a non-author
check); no rule prints `ok` that was not mechanically measured (`attested`
prints as `attested`); the ledger's round-10 row is the only plan row and is
marked as such; the synthesis admits every open debt and every `[unknown]` and
drops none; no promotion is self-issued; no host mutation (`-Qu`,
`-Su* --print*`, `stat`, bounded reads only; `-Sy`/`-Syu` never run; no
transaction, no download, no db write; `db.lck` absent after every probe
here); no external sites, no AUR RPC; secrets shape-only; the
coredump/OOM/hook/GSP classes stay with their owners; no round-8/9 artifact is
re-measured from memory — every citation is re-hashed at dispatch.

Measure: `--selftest` rc=0 with `PASS (N9+M cases, M≥4)` from the executed
run; the identity line prints and its plane list equals the rollup keys of the
same run; the executed count equals the SKILL restatement (grep-checked, moved
together); live run prints the realized plane count with verbatim notes; zero
mutation (fixture byte-unchanged + `git status` byte-identical before/after +
no `db.lck`); the synthesis note landed with md5/line count pinned and **no
row quoting a plan as landed**; ≥3 standing rows and ≥2 ledger rows re-derived
by a **non-author** (each row's probe re-executed, each pin re-hashed); the
no-oral-context re-test run against the final revision; `SKILL.md`/`README.md`/
`SCORECARD.md`/`LOG.md`/`corpus/lessons/round-10.md` landed; the closing
`SHONEN` state recorded with evidence, `[x]` left to the review. Suggested
seats: discipline seat (identity mode + fixtures + table), synthesis seat (the
note), note/hygiene seat (SKILL append + README rows + Frontier + SCORECARD
repair/row + lesson), executor seat (no-oral-context re-test), non-author
verifier (rows + ledger + round-9 plane if Step 0 leaves it open), scribe
(LOG/commit).

Draft-time pins (this lane, 2026-10-14 19:57:37–20:00:17Z, read-only, non-root,
scratch `/tmp/w9-preps10-tsukuroi/`; re-run, never quote). Line counts are
`wc -l`; the census and `SKILL.md` carry an **unterminated final line** (census
ends `main "$@"`), so Read counts one more — a pin states its convention. HEAD
`72b038d`; tree **0 entries at 19:57:37Z** (clean), 3 entries at 20:03:14Z
(named above, shape only). Census (freeze revision = HEAD blob, re-hashed):
md5 `e2c4558a3ae4ddd2eca67e8f4d64281c`, sha256
`bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55`, 1472
`wc -l`, 73 919 B; `--selftest` rc=0 in 5.19 s `PASS (49 cases, 49 passed, 0
failed)`; live rc=1 in 1.25 s (19:58:48Z):

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T19:58:48Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2[user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922897 C5_swap_peak_pct=99% C5_pswp=72403832/95603453 C5_sock_throttled=71447; C6_psi_some_avg300=0.24 C6_psi_full_avg300=0.24 C6_psi_full_total_us=71813007 C6_avail_kb=17542108 C6_shmem_kb=7392592; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=742 (coredump=467 kernel=139 other=136); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

— **four** `PLANE` emitters (no `PLANE update-safety`, no `PLANE oom`); zero
mutation (`git status` 0 lines before/after; no `db.lck`). Update-safety probe
receipts (20:00:17Z, unpiped rcs): `pacman -Qu` rc=1, 0 lines; `pacman -Sup
--print-format '%r/%n %v'` rc=0, 0 lines; `pacman -Suu --print-format` rc=0,
one action `omarchy/1password-beta 8.12.42_32.BETA-1`; sync-db births
core/extra/multilib/omarchy `2026-10-11 12:54:13.542054496 -0300`, `offline.db`
`2026-10-03 17:41:33.994891750 -0300`; mtimes core/extra/multilib `2026-09-08`
(**36 d** before the run), omarchy `2026-10-11`, offline `2026-07-20`;
`/var/log/pacman.log` 2109 lines, last entry `[2026-10-13T16:37:59-0300]`;
`expac` present (`/usr/bin/expac`, version `10-13`); `journalctl --list-boots`
14 lines (13 boots + header); `pacman -Qm` = 16. Census structure anchors on
the freeze revision (a round-9 landing edit moves them — re-derive, never
assume): overrides `:207-241` (`FOREIGN_BASELINE :227`), `R6_FOREIGN_BASELINE
:238-253`, `CLASS_OOM :255`, `CLASS_OOM_SYS :259`, `usage() :269`, helpers
`:286-352`, `probe_packages :354`, `probe_systemd :497`, `probe_drivers :563`,
`probe_mem_arm :685`, `probe_journal :806`, `run_selftest :924` (fixture
dispatcher `:933+`, `EXTRA_ENV` cases `:1075+`), `main() :1415` (probes
`:1444-1449`, the mem fold `DRV_V=$(worse …) :1448`, emitters `:1451-1454`,
rollup `:1456-1460`, verdict `:1462-1463`, exit map `:1465-1469`), 49 `check`
cases, final line `main "$@"` unterminated. Artifact pins (full md5):
`SKILL.md` `e2d058d4a09fbdd50d9c2d4705aac27f` 1169 (round-8 append; `git show
--numstat 72b038d` = +187/−1, net +186), `SCORECARD.md`
`9e3beec5f9a2ca3f2ac7ec42e6bcace3` 20, `LOG.md`
`b24defa5ed2cf65b00f9e68c44fd0f26` 171, `SHONEN.md`
`9cf1d450685ae0ed0d15dee1b54e8fd5` 51, `MINT.md`
`1d75fce9ed65ac6a22be115cc0c84055` 19, `PROVINCE.md`
`f1722b163a5c433b003de362ab93ee11` 19, `corpus/README.md`
`98bd00668e84f18cf6781718c4d09ea0` **20** (unchanged since round 3),
`corpus/QUALITY.md` `e31cef8e56f3666406ab9314d3de3f0e` 8, `corpus/lessons/`
**0 files**; notes `update-safety-note.md` `5cc3067f…` 478,
`update-safety-v2.md` `92803aea…` 353, `update-safety-v3.md` `2ac0c21d…` 387,
`oom-event-plane.md` `7e99d712…` 433, `aur-risk-plane.md` `1a584300…` 341,
`aur-risk-plane-ver-s7.md` `4608743d…` 184, `foreign-provenance-r6.md`
`1b8f47a2…` 307, `kill-event-deep-r8.md` `6685e1da…` 340,
`memory-arm-ver-s8.md` `861d83ad…` 251, `memory-arm-mutants-s8.md`
`a09e5604…` 181; plans `round-2.plan.md` `3563bd41…` 10, `round-3.plan.md`
`160a0272…` 13, `round-4.plan.md` `63c26bb1…` 10, `round-5.plan.md`
`0e9e8640…` 11, `round-6.plan.md` `81a9be07…` 38, `round-7.plan.md`
`bb915954…` 160, `round-8.plan.md` `0bef822d…` 216, `round-9.plan.md`
`3a59d2ed…` 270; records `round-4-record-draft.md` `a44f15db…` 300,
`round-5-record-draft.md` `899db964…` 453, `round-6-record-draft.md`
`4e9708ab…` 424, `round-7-record-draft.md` `c1eed63a…` 425,
`round-8-record-draft.md` `9e7399c3…` 448; **no round-1 plan file exists**
(`git log --all -- plans/round-1.plan.md` empty). The full corpus note set was
re-hashed this window (20 notes; `/tmp/w9-preps10-tsukuroi/pins.txt`).

Deferred candidate (C) anchors for a future slot: live census `coredump=467`
(19:58:48Z; 279 at 19:10:40Z same boot — the round-9 plan's capture; 269
round-6 capture; 224 round-3 report — storm drift, every value a capture);
`/var/lib/systemd/coredump` **443 files / 4.0 G** (20:00:17Z); per-app
attribution exists in notes (systemd-user-plane r1: godot 142 + node 47 in a
198-coredump boot) but not in the gate; the class needs an app-level vocabulary
and a second baseline before a watch can exist; ownership godot/node/LOVE app
lanes + the journal workstream (boundary `oom-event-plane.md:43-52`).

Bounds & unknowns: round-9 landing state at dispatch [unknown — Step 0];
whether `PLANE update-safety` landed as a line or an extension, and whether
round 9 landed its own non-author verification, the README rows, the round-2
errata pointer, the lesson file [unknown — Step 0]; the realized 5-plane
revision's md5/count/case set [unknown — the executed run at dispatch]; the
`--identity` design against the landed harness [design — adjudicated at
landing]; whether a fifth fixture case can be non-vacuous [design]; the
SCORECARD row-16 repair-vs-keep call [adjudicated at landing]; whether the
training ladder extends past round 10 [unknown — the synthesis stands either
way, not contingent]; the promotion review outcome [non-author]; the upstream
Arch/omarchy delta since 2026-09-08 — **the** real update gate — stays
[unknown] read-only (the 36 d stamp is a capture); `pacman.log` rotation window
at dispatch [unknown — the `cmd=unknown` row is built for the miss]; carried:
root `-Qkk` delta, `1password-beta` provenance (operator),
`walker-restart.hook` (kagi/operator), dkms stale `7.1.4-arch1-1`, `snapper`
empty, `offline.db` coverage debt, `omarchy-walker`↔`walker` linkage
(kaidoku/revenger), the "20-min cap" item (integrator), V8 heap-OOM and
coredump-storm boundaries, E4–E8 unapplied errata, H1–H3 and the OOM counter
Q2 as read-only-unmeasurable carries.

Discipline (round 10): host read-only (`PROVINCE.md:16-17`); no external
sites; secrets shape-only; one move; append-only errata; observation /
inference / unknown separated; write scope = the named artifacts only (this
draft wrote only this file).