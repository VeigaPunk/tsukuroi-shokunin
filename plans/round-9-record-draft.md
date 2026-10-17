# Round-9 record — DRAFT (scribe prep, seat SCR-S9)

Status: **draft, pre-landing.** This file is the scribe's working skeleton for the
round-9 `LOG.md` entry and for the round's artifact families (the **update-safety
plane joining `tools/tsukuroi-census.sh` as its 5th plane line**). It is not the
record; the record is the append-only `LOG.md` entry written after every round-9
artifact has landed (`AGENTS.md:3`). Every number below is a draft-time capture
with its command and time; the host is live — re-run, never quote.
**The round's headline is the 5-plane census** (§4a): if the round's move lands,
the gate emits five `PLANE` lines and the rollup gains the plane term — the
update-safety family stops being note-only. The record leads with it; §5's entry
skeleton does too. The second measured thread is Step 0's verdict that round 8
**changed no gate bytes** (§2): the round-8 `PLANE oom` watch is unlanded, so the
5th plane is the update-safety one, not the OOM one.

Draft seat: SCR-S9. Draft window: 2026-10-14 19:57–19:59Z (16:57–16:59 -03), host
`plazir27`, user `vgpnk` (non-root). Write scope: **this file only**. Scratch:
`/tmp/w9-tsukuroi-scr-s9/` (`pins.txt`, `status-before.txt`, `status-after.txt`,
`selftest.out`, `live.out`, `updsafety.out`, `sup.out`, `suu.out`,
`qm.out`; ephemeral). All probes read-only; no install/upgrade/remove/restart verb
(`PROVINCE.md:16-17`); no external site; no AUR RPC.

Tags used throughout: [observed] = measured now, command named; [inference] = join
from measurements; [unknown] = named gap with owner.

Round state at draft time [observed]: HEAD
`72b038da9b2b1da2a37d35e3cce2d1d7650f70be` ("probation round 8 (training r7): see
LOG", committed 2026-10-14 16:55:09 -0300 / 19:55:09Z); `git status --short` empty
at 19:58:09Z, byte-identical after the gate runs at 19:58:14Z, and still empty at
the freeze. **Round 8 is fully committed** — the commit carries 9 files (census
excluded; LOG, SCORECARD, SKILL, four `corpus/knowledge/` notes, the round-8
record draft, and `plans/round-9.plan.md`). The commit is ~3 minutes old at this
freeze: **round 9 has landed nothing yet** — census unchanged (`e2c4558a…`, 1472
`wc -l`), no `*baseline*` / `*.tsv` file anywhere in the tree (`find` excluding
`.git`, empty), no round-9 artifact. Sibling round-9 scratch dirs observed
shape-only (names/timestamps, no content relied on; 19:58Z): `/tmp/w9-tsukuroi-s91/`
(empty), `/tmp/w9-tsukuroi-s93/live/`, `/tmp/w9-tsukuroi-s94/` (census.pin,
gitstatus.before/after, live.before.out, poll.log), `/tmp/w9-ver-m9/`
(baseline-live.log), `/tmp/w9-scrb9/`, `/tmp/w9-scr-m9/`, `/tmp/w9-preps10-tsukuroi/`,
`/tmp/w9-tameshi-*` — the round-9 seats are working; no pin here is taken from a
moving revision. The draft's job is to have the fills ready when the artifacts land.

## 1. Plan anchor and the round's measure

`plans/round-9.plan.md` (md5 `3a59d2edd068abf6281d7701d261ea5c`, 19 509 B, 270
`wc -l` / 271 as read — **unterminated final line**, mtime 2026-10-14 16:15:52 -03;
committed inside `72b038d`; drafted by PREP-S9 during the round-8 wave, so every
round-8 artifact it names is a plan-side reading, never landed state):

> Axis move: **coverage + operability — the last note family without an executable
> presence becomes executable: the update-safety plane joins `tools/tsukuroi-census.sh`
> as its next plane line**, carrying the update-safety arm vocabulary and the two
> rules the landed corpus already measured — the channel-freshness rule ("empty
> proves nothing newer than a 36-day-old snapshot") and the class fold
> ("resolvable ≠ maintainable"). One move, one surface: round 7's claim (a)
> (`plans/round-7.plan.md:53-79`) is **finished from its own measured model, not
> re-designed** — it is tagged *not landed* in the landed tree (`SKILL.md:963-969`:
> no `PLANE update-safety` emitter, no fifth rollup term, checked against
> `e2c4558a…`; `corpus/knowledge/update-safety-v2.md:24-25,33`: claim (a) is "a
> sibling lane's deliverable and is **not** carried in this file"), and it is the
> one contract item no later round has claimed. (`plans/round-9.plan.md:16-30`)

Claims as the plan states them (`:64-141`):

- (a) **The update-safety plane joins the gate** (realized plane count + 1;
  worst-plane rollup unchanged; plane key proposal `update-safety`, adjudicated at
  landing). Probes, all read-only and already exercised: candidates two ways
  (`pacman -Qu` **unpiped** rc/emptiness + `pacman -Sup --print-format '%r/%n %v'`),
  the `expac`-vs-`-Sl` version join (absence must print `join=unavailable`), channel
  freshness (sync-db **births** via `stat -c %w`; mtime is an upstream stamp; age in
  days printed with an empty `-Qu`), `offline.db` + bounded `pacman.log` tail
  (`cmd=unknown` on a window miss, verdict unaffected), class fold exposure-only
  from the **same-process** `foreign=` reading (never a re-probe of `-Qm`),
  and the `-Suu` downgrade trap as a verdict-neutral trap row (`DO-NOT` stays note
  content per the round-7 proposal). Arm word carried in the note line: `PASS ·
  INERT · REQUIRES-PREP · BLOCKED · UNKNOWN-UPSTREAM · DO-NOT`; composition
  `BLOCKED > UNKNOWN-UPSTREAM > REQUIRES-PREP > INERT > PASS` (`SKILL.md:359-369`,
  `update-safety-note.md:334-339`). Gate-verdict mapping **recorded, not silently
  applied** (proposal: INERT/PASS→HEALTHY, REQUIRES-PREP/UNKNOWN-UPSTREAM→DEGRADED,
  BLOCKED→BLOCKED). Note-line traps named: shadowing (`-Qu` never shows a shadowed
  omarchy copy, `SKILL.md:395-397`) and `--print-format '%s'` is not a size
  (`:389-391`).
- (b) **Fail-closed, with fixtures** (≥4 new selftest cases; the realized set is
  quoted at landing): INERT-clean rollup; candidates>0 → REQUIRES-PREP → DEGRADED
  with names; `-Qu` unreadable → BLOCKED (never INERT); channel unreadable → BLOCKED
  (never INERT); class fold with absent baseline → DEGRADED if the harness allows a
  fifth. Proposed overrides `TSUKUROI_PACMAN_LOG`, `TSUKUROI_OFFLINE_DB`. **Named
  fixture prerequisite** [design]: a fixture file's birth is its creation time, so
  the *stale-channel* reading needs a documented seam or that case is vacuous and
  must not be claimed (the round-5 lesson).
- (c) **The contract lands where the executor reads it**: SKILL round-9 append
  (plane semantics, realized mapping, the channel-freshness rule, the fold, count
  restatements moved together — the rule at `SKILL.md:925-929` is live), the v2
  note's append-only errata pointer, `corpus/README.md` **back-rows for rounds 3-8**,
  the SCORECARD move row (before: 4-plane gate, update-safety note-only → after:
  N+1-plane gate), the LOG entry (scribe), plus the round's own lesson file
  `corpus/lessons/round-9.md` (`LEARNING.md:37-43,61`: `## Gate` section +
  outside spot-check on at least one admit and one reject). **No re-landing:** if
  round 8 landed any of these, the round records the realized one and does not re-do
  it.

**Measure as the plan states it** (`plans/round-9.plan.md:178-187`): `--selftest`
rc=0 with `PASS (N9+M cases, M≥4)`; the live run prints the new plane line with a
verbatim note and the rollup line gains the plane term; zero mutation (fixture
byte-unchanged + `git status` byte-identical before/after + no `db.lck`); the
errata pointer + SKILL append + README back-rows + SCORECARD + LOG +
`corpus/lessons/round-9.md` landed; **≥2 plane rows spot-checked by a non-author**
against live probes (re-executing the row's probe), plus AUD-X7 closed if round 8
left it open — a draft-time condition the landed round 8 **already resolved**
(closed, §2; the record states the closure and re-verifies only round-9 rows).
Suggested seats: plane seat, note/hygiene seat, non-author verifier, scribe.

**Plan-premise deltas measured now** (record, don't smooth) [observed]:

1. **Plane count resolved.** The plan says "realized plane count + 1; 4 today —
   Step 0 resolves the count after round 8" (`:66-67`). Step 0 result: **round 8
   landed no census revision** (§2) — the realized count is still **4**, so the
   move is **4→5** and the headline's "5-plane census" holds exactly as the
   assignment states. No re-scope of the plan's own Step 0 rule (i) is triggered.
2. **The OOM-plane item is resolved by non-landing, not by landing.** The plan's
   Step 0 asks "whether the OOM plane landed as a `PLANE` line or as a `mem=`
   extension (both within round 8's own plan)". Neither happened: the census is
   byte-identical and the round-8 SKILL append tags the watch "specified, not
   landed" (`SKILL.md:1132-1143`). The round-8 half of the round-8 plan's measure
   (new `PLANE oom` + ≥2 baseline rows re-executed non-author) is therefore
   unverifiable-by-construction and is carried, never re-opened here.
3. **Plan pins of round-7-era files moved with the round-8 landing.** The plan's
   Step 0 list quotes `SKILL.md:963-969`, md5 `b2b0f6a7…`, 983 ln (the round-7
   revision); the landed file is `e2d058d4…`, 1169 `wc -l` (1170 as read). The
   cited content still resolves — the round-7 errata block is now `:963-984` and
   the "no `PLANE update-safety` emitter" statement still reads true at `:963-970`.
   Same for `SCORECARD.md` (19→20 lines) and `LOG.md` (170→171). The record quotes
   landed pins, never the plan's draft pins.
4. **The plan's Step 0 item (iv) (AUD-X7 "still open") is refuted by the landed
   round 8**: AUD-X7 is **closed** (VER-S8 `CONFIRMED`, §2). The plan wrote it as a
   draft-time reading; the record states the closure and does not re-verify a closed
   gap.
5. **The deviation candidate (B) anchor has already drifted in-window**: the plan
   recorded the live census `coredump=279` at 19:10:40Z; the 19:58:14Z run reads
   `coredump=467` (same boot) — a capture, not a trend line (§3.1). Both are kept
   as captures for the deferred schedule item.

## 2. Step 0 — round-8 landing check against its own measure [observed]

Round-8's measure: its plan's contract (`plans/round-8.plan.md`, md5
`0bef822da196368c47c56426063990fe`, 216 `wc -l` / 217 as read) plus the round-9
plan's Step 0 restatement (`:143-161`). Verdict: **round 8 landed its notes and its
verification; it landed no gate change.**

| round-8 member | landed? | pin at draft time |
|---|---|---|
| census revision (`PLANE oom` watch + baseline) | **no — the move never landed** | `tools/tsukuroi-census.sh` still `e2c4558a3ae4ddd2eca67e8f4d64281c`, 1472 `wc -l` / 73 919 B; 4 `PLANE` emitters; no `PLANE oom`; no `*baseline*`/`*.tsv` file in the tree; tagged in `SKILL.md:1132-1143` |
| standalone baseline file (`oom-event-baseline.tsv` proposal) | **no** | (`find` empty, 19:58Z) |
| VER-S8 closure (non-author verification) | **yes** | `corpus/knowledge/memory-arm-ver-s8.md` md5 `861d83ad5a120487507b167236ee3cd0`, 251 `wc -l` / 252 as read; verdict `CONFIRMED` — `AUD-X7` closed for the S7-2 memory arm; 0 live claims refuted; 9 clause sites named as suite-coverage debt (`SKILL.md:1042-1071`) |
| S8-1 mutant set | **yes** | `corpus/knowledge/memory-arm-mutants-s8.md` md5 `a09e5604a9a818f38096569365d48823`, 181 `wc -l` |
| S8-2 kill-event deep capture | **yes** | `corpus/knowledge/kill-event-deep-r8.md` md5 `6685e1da443f5d368cd41584d2b9943e`, 340 `wc -l` |
| S8-3 update-safety v3 | **yes** (the round's update-safety artifact) | `corpus/knowledge/update-safety-v3.md` md5 `2ac0c21db678c1c806d6de9e546daf2e`, 387 `wc -l`; its §9 names the still-owed items (the census 5th plane, the r2 errata pointer, `README` rows) |
| SKILL round-8 append | **yes** | `SKILL.md` md5 `e2d058d4a09fbdd50d9c2d4705aac27f`, 1169 `wc -l` / 1170 as read; round-8 append `:986-1170` |
| SCORECARD round-8 row | **yes** | `SCORECARD.md:20` ("operability … the VER-S8 GAP CLOSED …"); the round-4 row `:16` is **still malformed** — the unescaped `|` truncates the After cell to `boot plane (299 L` |
| LOG round-8 entry | **yes** | `LOG.md:171` (one line; names VER-S8 as the closure) |
| `corpus/README.md` coverage rows | **no** | unchanged since round 3 (`98bd00668e84f18cf6781718c4d09ea0`, 20 `wc -l`, mtime 12:58 -03) — rounds 4-8 rows collapsed |
| round-8 record draft | **yes** | `plans/round-8-record-draft.md` md5 `9e7399c32838dea3d3e67e988d5ad35d`, 448 `wc -l` |

**The round-9 plan's Step 0 debt list, resolved** (`plans/round-9.plan.md:143-161`)
[observed]:

(i) `PLANE update-safety` absent/present — **absent**; the move stands as specified,
    no re-scope to "one rung further" (4 `PLANE` emitters `:1451-1454`; 4-term rollup
    `:1456-1460`; all re-measured by this seat).
(ii) round-2 note errata pointer — **still owed**; `update-safety-note.md` unchanged
    at md5 `5cc3067fec33d261d8bff6a5c7e8ac48`, 478 `wc -l`.
(iii) `corpus/README.md` rows — **still owed** (now rounds 4-8; last touched round 3,
    `git log --oneline -- corpus/README.md` → `9bcd162`).
(iv) AUD-X7 — **closed by round 8** (VER-S8; `SKILL.md:1042-1071`; `LOG.md:171`);
    the plan's "still open" was a draft-time reading. Do not re-open.
(v) `SCORECARD.md:16` malformed row — **still there**, measured verbatim:
    `| 4 | freshness + depth | round-3 state | boot plane (299 L | wave-4 32-lane; VER-S1 |`.

Plus one item the round-8 append names and no round-9 seat should absorb: the
round-8 `PLANE oom` arm's own non-author verification is separate from AUD-X7
(`SKILL.md:1152-1155`) — but since that arm never landed, there is nothing to
verify; the record states it as **superseded by non-landing**, not silently dropped.

**Consequence for round 9's order of work [inference].** The plan's three claims are
all live work (none was pre-empted by round 8), and two carried hygiene items ride
alongside: the r2 errata pointer and the README back-rows. The round's lesson-file
obligation (`corpus/lessons/round-9.md`) starts a ledger that holds **0 files after
eight rounds** (`ls corpus/lessons` empty, measured) — and per the plan's own
candidate-(D) reasoning, a retro Gate for earlier rounds would invent decisions that
were never recorded; only round 9's own gate decisions are recordable. This draft
invents none.

## 3. Draft-time baseline receipts (this seat, read-only)

### 3.1 Gate, re-run 2026-10-14 19:58:14Z

Raw captures `/tmp/w9-tsukuroi-scr-s9/{selftest,live}.out`:

```bash
bash tools/tsukuroi-census.sh --selftest   # 19:58:14Z, rc=0
bash tools/tsukuroi-census.sh              # 19:58:14Z, rc=1
```

Selftest last line verbatim: `TSUKUROI_CENSUS_SELFTEST: PASS (49 cases, 49 passed,
0 failed)`. Live run verbatim:

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T19:58:14Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2[user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922897 C5_swap_peak_pct=99% C5_pswp=72354780/95577924 C5_sock_throttled=71107; C6_psi_some_avg300=0.26 C6_psi_full_avg300=0.26 C6_psi_full_total_us=71777605 C6_avail_kb=19912492 C6_shmem_kb=5249040; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=742 (coredump=467 kernel=139 other=136); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

— **four** `PLANE` emitters, no `PLANE update-safety`; the emitters are
`:1451-1454` and the 4-term rollup `:1456-1460` in the landed revision (re-read by
this seat). Zero-mutation receipt: `git status --short` 0 lines before / 0 lines
after, byte-identical (`status-before.txt` / `status-after.txt`); `/var/lib/pacman/db.lck`
absent. At landing the record quotes the **post-round-9** run (5-plane line incl.
`PLANE update-safety:`), never this one.

Drift note [observed]: this run's journal line reads `err=742 (coredump=467
kernel=139 other=136)` against the round-9 plan's 19:10:40Z capture of `442
(coredump=279 kernel=139 other=24)` — same boot (`boots=13 current=yes`). The
coredump storm and the `other` class both moved in 48 minutes; every value is a
capture. C5/C6 moved likewise (`C5_pswp` 72122570/93982664 → 72354780/95577924;
`C6_psi_some_avg300` 0.03 → 0.26). Same-value readings elsewhere (e.g. `kerr=139`,
`foreign=16`) are captures too, never confirmations.

### 3.2 Update-safety probe receipts, 19:58:25Z (the fill material for §4a)

All read-only, all raw in `/tmp/w9-tsukuroi-scr-s9/updsafety.out` [observed]:

- `pacman -Qu` — **rc=1, 0 lines** (unpiped, so the rc is the command's, never a
  pipeline's). rc=1 with empty output is "no candidates", not "unreadable".
- `pacman -Sup --print-format '%r/%n %v'` — **rc=0, 0 lines** (plan verb; no
  transaction, no download, no db write).
- `pacman -Suu --print-format '%r/%n %v'` — **rc=0, 1 line**: `omarchy/1password-beta
  8.12.42_32.BETA-1` — the downgrade trap, reproduced byte-for-byte from the
  round-2/7/8 readings.
- `/var/lib/pacman/db.lck` — **absent**.
- Sync-db **births**: core/extra/multilib/omarchy all `2026-10-11
  12:54:13.542054496 -0300`; `offline.db` `2026-10-03 17:41:33.994891750 -0300`.
- Sync-db **mtimes** (upstream stamps): core `2026-09-08 15:23:46`, extra
  `:47`, multilib `:45` — **36 d** before this run; omarchy `2026-10-11 10:16:17`;
  offline `2026-07-20 21:11:36`.
- `offline.db` — 304 318 B, root:root.
- `/var/log/pacman.log` — **2109 lines**; last timestamped entry
  `2026-10-13T16:37:59-0300` (`transaction completed` + `35-systemd-update.hook`).
- `pacman -Qm` — **16 rows** (rc=0).
- `expac` — present (`/usr/bin/expac`, `10-13`).

These reproduce the round-9 plan's own probe receipts (its `:209-217`) exactly,
which is expected, not independent confirmation: no pacman activity has occurred
since 2026-10-13 16:37 unless the log's own tail says otherwise at landing.

### 3.3 Artifact pins, hashed 2026-10-14 19:58:37Z (clean tree — every hash is of committed bytes)

| artifact | md5 | lines |
|---|---|---|
| `tools/tsukuroi-census.sh` (round-7 revision, unchanged in round 8) | `e2c4558a3ae4ddd2eca67e8f4d64281c` | 1472 (1473 read) |
| `SKILL.md` (round-8 append landed) | `e2d058d4a09fbdd50d9c2d4705aac27f` | 1169 (1170 read) |
| `LOG.md` / `SCORECARD.md` / `SHONEN.md` | `b24defa5ed2cf65b00f9e68c44fd0f26` / `9e3beec5f9a2ca3f2ac7ec42e6bcace3` / `9cf1d450685ae0ed0d15dee1b54e8fd5` | 171 / 20 / 51 |
| `corpus/README.md` | `98bd00668e84f18cf6781718c4d09ea0` | 20 |
| `corpus/QUALITY.md` | `e31cef8e56f3666406ab9314d3de3f0e` | 8 |
| `plans/round-8.plan.md` / `plans/round-8-record-draft.md` | `0bef822da196368c47c56426063990fe` / `9e7399c32838dea3d3e67e988d5ad35d` | 216 (217 read) / 448 (449 read) |
| `plans/round-9.plan.md` | `3a59d2edd068abf6281d7701d261ea5c` | 270 (271 read) |
| `corpus/knowledge/update-safety-v3.md` / `update-safety-v2.md` / `update-safety-note.md` | `2ac0c21db678c1c806d6de9e546daf2e` / `92803aea74ebeb1598fa4f450489e5d2` / `5cc3067fec33d261d8bff6a5c7e8ac48` | 387 / 353 / 478 |
| `corpus/knowledge/memory-arm-ver-s8.md` / `memory-arm-mutants-s8.md` / `kill-event-deep-r8.md` | `861d83ad5a120487507b167236ee3cd0` / `a09e5604a9a818f38096569365d48823` / `6685e1da443f5d368cd41584d2b9943e` | 251 / 181 / 340 |
| `corpus/knowledge/oom-event-plane.md` / `aur-risk-plane.md` / `aur-risk-plane-ver-s7.md` | `7e99d712ead088727c0980e52a121199` / `1a584300f6b07da78bc8332f04b4fd30` / `4608743dfa6230e806985d164f3c00f4` | 433 / 341 / 184 |
| `corpus/knowledge/aur-risk-plane-ver-s6.md` / `foreign-provenance-r6.md` | `b0de352dec653891d5d36dd742536198` / `1b8f47a2a807fc8bd2fc7302f15577c8` | 133 / 307 |
| `corpus/knowledge/journal-boot-plane.md` / `boot-plane.md` / `timer-drift-plane.md` | `e5ca40dafc4d1d2a2158fded39067df6` / `e722b7a931858aa5ff1a89ce91cccca9` / `fc0760c8070c9387ff5334f0f8c645cc` | 430 / 312 / 332 |
| `corpus/knowledge/degraded-triage-r4.md` / `host-health-report-r3.md` / `executor-test-sufficiency.md` | `d57ae2d48e01777e1ef3c8c0ffb642c9` / `98a0f263f801245f6069e57a9f72d4af` / `4b2c1d3612db7db1477da92aaec39862` | 607 / 563 / 219 |
| `corpus/knowledge/package-state-plane.md` / `systemd-user-plane.md` / `driver-firmware-plane.md` | `ef93f1b78b6a9e17e8c9d096e7852a02` / `af07a829cfd0307fbe970a2cdc054e18` / `518eda8f0f39f25ee95c715571a9cf95` | 323 / 265 / 256 |
| `corpus/lessons/` | — | **0 files** |

Every round-7/8-era pin reproduces exactly at the draft freeze. **Convention
note:** an **unterminated final line** is common in this repo — measured by
last-byte check at 19:59Z: it holds for the census, `SKILL.md`, both checked plans
(`plans/round-8.plan.md`, `plans/round-9.plan.md`), the round-8 record draft, and
for 12 of the 20 `corpus/knowledge/` files (v2 and v3 among them — full list:
`aur-risk-plane.md`, `aur-risk-plane-ver-s6.md`, `aur-risk-plane-ver-s7.md`,
`degraded-triage-r4.md`, `executor-test-sufficiency.md`, `foreign-provenance-r6.md`,
`kill-event-deep-r8.md`, `memory-arm-mutants-s8.md`, `memory-arm-ver-s8.md`,
`timer-drift-plane.md`, `update-safety-v2.md`, `update-safety-v3.md`). `LOG.md`,
`SCORECARD.md`, `SHONEN.md`, `README.md`, `QUALITY.md` are newline-terminated. The
earlier plans and record drafts were not re-checked at this freeze [unknown]. **A
pin must state its convention** (`wc -l` vs a Read).

### 3.4 Census shape anchors re-resolved (the fills' line references)

Re-read at 19:58Z against the landed revision (the round-9 plan's `:218-227` shape
list re-resolved; the deltas below are recorded, not smoothed) [observed]:

- overrides block `:206-227` (header comment `:206`; `PACMAN` `:207` … `PACMAN_DB`
  `:210` … `FOREIGN_BASELINE` `:227`); the accepted baseline's comment `:229-237`;
  `R6_FOREIGN_BASELINE` `:238-253`; `CLASS_*` constants `:255-260`; `usage()` `:269`.
  (The plan's shape list writes "overrides block `:207-241`, `R6_FOREIGN_BASELINE`
  + `CLASS_*` constants `:242-267`" — the realized spans are `:207-227` and
  `:238-260`; measured by `grep -n`, recorded as a plan-vs-landed pin delta.)
- probes: `probe_packages` `:354`, `probe_systemd` `:497`, `probe_drivers` `:563`,
  `probe_mem_arm` `:685`, `probe_journal` `:806`.
- selftest: `run_selftest` `:924`; fixture dispatcher `:933-983`; `run_case` env
  block `:1075-1094` (the plan's `:1075-1093` — the array expansion line is `:1094`);
  `EXTRA_ENV` cases from `:1175` onward; PASS print `:1409-1411`.
- `main()` `:1415`; call list `:1444-1449` (the plan's `:1446-1449`); **the mem fold
  is `DRV_V=$(worse "$DRV_V" "$MEM_V")` at `:1448`** (the plan writes `:1449` — one
  line off, recorded); emitters `:1451-1454`; rollup `:1456-1460`; verdict printf
  `:1462`; exit map `:1464-1470`; `main "$@"` last line `:1473` (1472 `wc -l`).

The new plane's rollup term copies the mem arm's fold model (`:1448`) — the plan
says so (`:224-226`), and the shape confirms it.

## 4. Fill rules — what the record must state on landing

**(a) The realized census revision and the fifth plane — the headline.** Ink the
post-commit bytes: new md5 + line count + size of `tools/tsukuroi-census.sh` (before:
`e2c4558a…`, 1472 `wc -l`); the executed selftest line `PASS (49+M cases, …)` with
case attribution (**49 legacy = 35 base + 6 foreign-baseline + 8 S7-2 memory**;
M new — the plan's four named cases plus the class-fold case if the harness shape
allows; attribute, never conflate); the verbatim `PLANE update-safety:` note from an
executed live run (realized spelling, never this draft's); the rollup line with the
new plane term; the realized plane count (**4→5** — Step 0 resolved, §1 delta 1).
The realized note must carry, per the plan: the candidates reading with the
**unpiped** rc rule (`-Qu` rc=1 + empty = 0 candidates; any other non-zero rc =
unreadable → `BLOCKED`); the channel-freshness print (sync-db **birth** age in days
at the run's date; today 36 d on the core/extra/multilib mtimes — a capture); the
`offline.db` + bounded `pacman.log` tail row (birth authoritative, log adds the
command, a window miss → `cmd=unknown`, verdict unaffected); the class fold
(`classes=` exposure-only, from the **same-process** `foreign=` reading the packages
plane already computes — never a second `-Qm` probe; absent/unreadable baseline →
DEGRADED) and the two note-line traps (shadowing `SKILL.md:395-397`;
`--print-format '%s'` is not a size `:389-391`). Arm words and gate mapping
**recorded, not silently applied** (proposal: INERT/PASS→HEALTHY,
REQUIRES-PREP/UNKNOWN-UPSTREAM→DEGRADED, BLOCKED→BLOCKED; `DO-NOT` note content —
adjudicated against the realized round-7 mechanism). Fail-closed receipts: fixture
byte-unchanged assertion, `git status --short` byte-identical before/after, no
`db.lck`. The packages plane's `pins=none holds=pacman glibc` row **stays** — no
double-probe (the plan's anti-claim; if the diff shows a duplicate `-Qm` or a
pins re-probe, that is a defect to record, not to smooth).

**(b) Fail-closed fixtures.** New selftest cases ≥4, realized set quoted: INERT-clean
rollup with the new term; candidates>0 → REQUIRES-PREP → DEGRADED (names printed);
`-Qu` unreadable → BLOCKED, never INERT; channel unreadable (no `sync/` in the
fixture db) → BLOCKED, never INERT; class fold with absent baseline → DEGRADED if a
fifth case fits. New overrides in the `TSUKUROI_*` family, realized names quoted
(proposal `TSUKUROI_PACMAN_LOG`, `TSUKUROI_OFFLINE_DB`). **The stale-channel fixture
seam is the named prerequisite**: a fixture file's birth is the fixture's creation
time, so the stale-channel case needs a documentable redirect for the channel stamp
— if the seam cannot be built, the case is **dropped and reported as dropped**,
never claimed vacuous (the round-5 lesson: a case that cannot fail is not a case).
The record also states whether the `expac`-absent path is exercised (it must print
`join=unavailable`, not a silent pass).

**(c) The contract artifacts.** The `SKILL.md` round-9 append (plane semantics, the
realized mapping, the channel-freshness rule, the fold, and the count restatements
moved together: the current expected line is `PASS (49 cases…)` at the identity pin
above; a round-9 gate revision makes the round-3/5/7/8 restatements history and must
move them with it — the rule at `SKILL.md:925-929,1147-1151` is live). The
`corpus/knowledge/update-safety-v2.md` **append-only errata pointer** ("implemented
at <pin>; the realized contract supersedes §10 where it differs") — v2's §10 item is
the literal owed row; the r2 note (`update-safety-note.md`) stays the arm-word owner
and its pointer debt is separate (`SKILL.md:971-972`). `corpus/README.md` **back-rows
for rounds 3-8** (the map is the surface the new plane's note must appear on) — or
the debt stated open, never silently skipped. SCORECARD round-9 move row (axis:
coverage + operability; Before: 4-plane gate, update-safety note-only (arm words in
the r2 note, classes in v2, live join in v3) → After: 5-plane gate with
`PLANE update-safety`, N+1-plane rollup). LOG entry (scribe). And the round's own
`corpus/lessons/round-9.md` — the lane's **first** lesson file: `## Gate` section
(candidates considered/admitted/rejected with reasons — recordable only for round 9
itself; no retro-fabrication) plus the outside spot-check on at least one admit and
one reject (`LEARNING.md:37-43,61`). **No re-landing**: if a sibling lane lands any
of these before the record, the record quotes the realized one and does not re-do it.

**(d) Headline placement.** The LOG entry's first line carries the 5-plane census
(§5), not the notes. The record also states the second measured thread: round 8
changed no gate bytes, so this round's move is the realized N+1 (4→5), and the
round-8 `PLANE oom` watch remains "specified, not landed" (`SKILL.md:1132-1143`).

## 5. Record skeleton (what the `LOG.md` entry must carry on landing)

Round 8 used a one-line entry; the round-9 headline (the 5-plane census) must stay
on the first line. Candidate (fill at landing):

```
- 2026-10-14 — round 9 (training r8): the update-safety plane joins the gate as its
  ⟨5th⟩ plane line — the ⟨4→5⟩-plane census (selftest 49→⟨49+M⟩; M≥⟨4⟩: ⟨case names⟩)
  prints ⟨verbatim PLANE update-safety note⟩ with the channel-freshness rule (empty
  -Qu = ⟨age⟩-d snapshot) and the ⟨classes=…⟩ fold; contract: SKILL round-9 append +
  ⟨v2 errata pointer | owed⟩ + ⟨README back-rows rounds 3-8 | owed⟩ +
  ⟨corpus/lessons/round-9.md (first) | owed⟩. Axis: coverage + operability.
  Verifiers: VER-S9 ⟨scope/verdict⟩ | ⟨…⟩.
```

- **Work (observed in tree):** ⟨artifact list: path, seat/ID, md5, lines, mtime⟩ —
  expected members: the census revision (new md5 + case count), the SKILL round-9
  append, the v2 errata pointer, the round-9 lesson file, plus scribe-owned
  README/SCORECARD/LOG. Each member's write scope is named, not absorbed.
- **Scribe re-verification:** §6 command set; quote the selftest line, the live
  5-plane rollup, one verbatim `PLANE update-safety:` note, and the re-executed row
  probes (non-author's rows named separately).
- **Ancillary scribe writes (owed at record time):**
  - `SCORECARD.md` round-9 move-log row (axis vocabulary per `AXES.md:9-16`;
    before/after as in §4c); **form defect carried: `SCORECARD.md:16` (round-4 row)
    still malformed** [observed 19:58Z].
  - `corpus/README.md` coverage rows — debt now rounds 4-8 + round 9; land or state
    open, never silently skip.
  - `SKILL.md` count restatements move together with any gate revision (§4c).
- **SHONEN boxes:** stay `[~]` (asserted with verifier names); the round-9 record may
  refresh evidence pointers but must not upgrade to `[x]` — that stays with the
  non-author promotion review. `SHONEN.md` unchanged since round 3
  (`9cf1d450…`, 51 `wc -l`) [observed].
- **State at entry:** the round commit hash landed, or "round work uncommitted in
  tree" + exact `git status --short`; the scribe writes only its named files; the
  commit carries the lane identity (`AGENTS.md:5`); commit-message pattern
  `probation round 9 (training r8): see LOG`.

## 6. Scribe re-run set (receipts owed by the record)

```bash
cd ~/Projects/shokunin/tsukuroi-shokunin
bash tools/tsukuroi-census.sh --selftest            # expect rc=0, 49+M/49+M PASS
bash tools/tsukuroi-census.sh                       # expect rc=1(frame), 5-plane rollup + PLANE update-safety:
md5sum tools/tsukuroi-census.sh; wc -l tools/tsukuroi-census.sh   # landed revision vs e2c4558a…
grep -n '^PLANE' <live-run-file>                    # count the emitters: 5 expected; the rollup gains the term
pacman -Qu; echo "rc=$?"                            # UNPIPED: rc=1 + empty = 0 candidates; other rc = unreadable
pacman -Sup --print-format '%r/%n %v'; echo "rc=$?" # plan verb; 0 lines today
pacman -Suu --print-format '%r/%n %v'; echo "rc=$?" # the downgrade trap row (1 line today)
test -e /var/lib/pacman/db.lck && echo present || echo absent
stat -c '%w | %y | %n' /var/lib/pacman/sync/*.db    # births (authoritative) + mtimes (upstream stamps)
wc -l < /var/log/pacman.log; tail -2 /var/log/pacman.log
pacman -Qm | wc -l                                  # (rc is the pipeline's — do not cite it as a measurement)
command -v expac && expac -Q '%v' expac
find . -path ./.git -prune -o \( -name '*.tsv' -o -name '*baseline*' \) -print  # baseline files, if any
ls corpus/lessons/                                  # round-9.md exists?
sed -n '16p;20p' SCORECARD.md                       # :16 defect + round-8 row
git log --oneline -- corpus/README.md               # README row debt (last 9bcd162, round 3)
git status --short                                  # zero-mutation receipt (before/after)
# + the landed census md5/lines; + the round-9 selftest fixtures read from the executed run
```

Rules restated: never carry a piped rc as a measurement (`| head`, `| wc -l`); a
probe's rc is the command's own only when unpiped; empty `-Qu` is only a pass with
the channel reading present and its age printed; an unreadable probe is `BLOCKED`,
never `INERT`.

## 7. Unknowns register (draft-time; owners)

1. Realized plane shape: plane key (`update-safety` = proposal), emitter position,
   note string, arm words, composition, gate mapping (owner: plane seat; the record
   quotes realized values, never this draft's).
2. M and the realized case set: the plan's four + possibly the fold case; the
   stale-channel fixture seam decides one — if the seam is not buildable that case
   is dropped, never claimed vacuous (owner: plane seat; [design] → adjudicated at
   landing).
3. New override names (proposal `TSUKUROI_PACMAN_LOG`, `TSUKUROI_OFFLINE_DB`)
   and whether the `expac`-absent path is exercised (owner: plane seat).
4. Which hygiene items land in this round vs stay owed: the v2 errata pointer, the
   `corpus/README.md` back-rows (rounds 3-8), `corpus/lessons/round-9.md` (owner:
   note/hygiene lane + scribe; the record states realized, never assumes).
5. Non-author verification: the plan's measure requires ≥2 plane rows spot-checked
   by a non-author; whether a VER-S9 artifact lands at all, and its scope (owner:
   verifier seat). `AUD-X7` is closed (§2); do not re-open it.
6. Upstream Arch/omarchy delta since 2026-09-08 — **the real update gate** — stays
   [unknown] read-only; the 36 d stamp is a capture (owner: the operator's next
   `-Sy`; the plane may only print the age).
7. `pacman.log` rotation window at landing — the `cmd=unknown` row is built for the
   miss (owner: host; retention out of scope).
8. `offline.db` coverage debt: 304 318 B, birth 2026-10-03, mtime 2026-07-20 —
   whether the plane line surfaces it beyond the fold's `offline-exile` class
   (owner: plane seat; fold is exposure-only by the plan's anti-claim).
9. The round-8 `PLANE oom` non-author-verification item (`SKILL.md:1152-1155`):
   superseded by non-landing, or carried as an arm-tagged item? (owner: record
   scribe at landing — the arm did not land, so there is nothing to verify).
10. Coredump-storm watch (candidate B) anchors carried for a future draft:
    live census `coredump=279` (19:10:40Z) → `coredump=467` (19:58:14Z, same boot;
    269 round 6, 224 round 3 — every value a capture); ownership godot/node/LOVE +
    the journal workstream; needs an app-level vocabulary and a second baseline.
11. Carried rounds 1-8, unchanged: root `-Qkk` delta; the 18/19 sweep-summary
    split; `1password-beta` provenance (operator); `walker-restart.hook`
    (kagi/operator); dkms stale `7.1.4-arch1-1`; `snapper` empty;
    `omarchy-walker`↔`walker` linkage (kaidoku/revenger); the "20-min cap" item
    (integrator); round-6 H1-H3 / Q1-Q7; the `SCORECARD.md:16` malformed row; the
    round-2 wave-1 errata merge.

## 8. Errata / pending (append-only)

- 2026-10-14 — this draft file created by SCR-S9; it is prep, not a record. The
  `LOG.md` round-9 entry remains owed (`AGENTS.md:3`); measures are judged against
  the landed census revision + the contract artifacts, not this skeleton.
- 2026-10-14 — all counts in §3 are captures on a live host (coredump storm live;
  C5/C6 counters move between runs; `boots=13 current=yes` is the same boot as the
  round-9 plan's 19:10Z capture); re-run, never quote.
- 2026-10-14 — Step 0 result recorded above: round 8 landed **no gate change**
  (census byte-identical; no baseline file; the `PLANE oom` watch stays "specified,
  not landed"); it landed VER-S8 (`AUD-X7` closed), the mutant note, the kill-event
  capture, and update-safety v3. Carried into round 9: `PLANE update-safety` (the
  move), the r2 errata pointer, the `corpus/README.md` rows, and the
  `SCORECARD.md:16` defect. This draft re-designs nothing; it names the debts for
  the record scribe.
- 2026-10-14 — plan-vs-landed deltas measured (§1): plane count resolved 4→5 (not
  a re-scope); the OOM-plane Step-0 question resolved by non-landing; the plan's
  SKILL/SCORECARD/LOG pins are round-7-era and moved with round 8's landing (the
  cited SKILL content still resolves at `:963-984`); the plan's "AUD-X7 still open"
  is refuted by the landed VER-S8; the census shape pins shift — two by one line
  (run_case env block, the mem fold) and two block spans restated (§3.4). The
  record quotes realized values.
- 2026-10-14 — the round is concurrent: no round-9 artifact had landed at 19:58Z;
  sibling scratch dirs observed shape-only (names/timestamps; s91/s93/s94, ver-m9,
  scrb9, preps10, tameshi lanes). The record scribe fills every generic slot with
  actual filenames, md5s and executed lines at entry.
- 2026-10-14 — **the lesson-ledger boundary, stated so it cannot be read as
  retro-fabrication**: `corpus/lessons/` holds 0 files after eight rounds; per the
  round-9 plan's own candidate-(D) reasoning, the per-round candidate/reject
  decisions were never recorded at the time, so a retro Gate for rounds 1-8 would
  invent them. `corpus/lessons/round-9.md`, if it lands, records **round 9's own**
  gate decisions and the outside spot-check, nothing earlier.
- 2026-10-14 — final-file spot-check and this file's own line count/md5 are
  reported in the seat's handoff, not in-file (a further edit would invalidate
  them). All fix-ups stay append-only above this line.
- 2026-10-14 20:01–20:02Z — **post-freeze tree movement (append-only, shape only)**:
  the tree gained `?? corpus/knowledge/aur-drift-receipt-r9.md` (untracked, mtime
  17:01 -03) alongside this file (`?? plans/round-9-record-draft.md`) — a sibling
  round-9 lane's artifact, **not** a write by this seat; its content was not read
  and no pin is taken from it (it may still be moving). The census was still
  byte-identical at `e2c4558a…` (1472 `wc -l`) at 20:02Z; no `*baseline*` / `*.tsv`
  file exists. The readings above are kept as the freeze-time (19:57–19:59Z) state;
  nothing was re-measured against any later revision.
- 2026-10-14 20:02:42–20:02:48Z — **the census has moved (append-only, shape only)**:
  `git status --short` now shows `M tools/tsukuroi-census.sh`; the working revision
  captures at md5 `5b76f21b4687dfa51cb0bc34de6e913d`, 1535 `wc -l`, 79 432 B
  (mtime 17:02:42 -03), `git diff --stat` = **+63 insertions, 0 deletions**, and
  **four** `PLANE` emitters still (`:1514-1517`) — the fifth plane is not in the
  working revision at this capture. **Not a pin** — the file is the plane seat's
  in-flight work (it was still committed-clean at 20:02:21Z). The record scribe
  re-hashes at entry; §3.1–3.4 above remain the freeze-time (19:58Z) state.
