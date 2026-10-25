# Round-10 record — DRAFT (scribe prep, seat SCR-S10)

Status: **draft, pre-landing.** This file is the scribe's working skeleton for the
round-10 `LOG.md` entry and for the round's artifact families. It is not the record;
the record is the append-only `LOG.md` entry written after every round-10 artifact
has landed (`AGENTS.md:3`). Every number below is a draft-time capture with its
command and time; the host is live — re-run, never quote.
**The round's headline is the self-sweep (§4a):** if the round's move lands, the
lane's own ten-round claim-vs-realized ledger (rounds 1–10) and the census's standing
discipline (D1–D13) stop living scattered across nine rounds of appends and become one
artifact a non-author can re-derive — the **calibration** move, the lane's first
(rounds 1–8 moved operability, freshness, depth, adjacency, coverage;
`plans/round-10.plan.md:23-34`, `AXES.md:15`). The record leads with it; §5's entry
skeleton does too. The second measured thread is Step 0's verdict (§2): **round 9
landed a six-plane census** (update-safety **and** oom), selftest 74, and left named
contract debts (the v2 errata pointer, the `corpus/README.md` back-rows,
`corpus/lessons/round-9.md`, the plane's non-author verification) — the synthesis's
debt ledger must carry them.

Draft seat: SCR-S10. Draft window: 2026-10-14 20:51–20:55Z (17:51–17:55 -03), host
`plazir27`, user `vgpnk` (non-root). Write scope: **this file only**. Scratch:
`/tmp/w10-tsukuroi-scr-s10/` (`status-before.txt`, `status-after.txt`, `selftest.out`,
`live.out`, `qu.out`, `sup.out`, `suu.out`; ephemeral). All probes read-only; no
install/upgrade/remove/restart verb (`PROVINCE.md:16-17`); no external site; no AUR
RPC; no `-Sy`/`-Syu`.

Tags used throughout: [observed] = measured now, command named; [inference] = join
from measurements; [unknown] = named gap with owner.

Round state at draft time [observed]: HEAD
`fac745b2813980014125390ff63defe0420b16d7` ("probation round 9 (training r8): see
LOG", committed 2026-10-14 17:47:30 -03 = 20:47:30Z); `git status --short` empty at
20:51:04Z and byte-identical after the gate runs at 20:51:29Z. **Round 9 is fully
committed** — the commit carries 7 files (`git show --numstat fac745b`): `LOG.md`
(+1), `SCORECARD.md` (+1), `SKILL.md` (+206/−1), `corpus/knowledge/aur-drift-receipt-r9.md`
(+249), `plans/round-10.plan.md` (+322), `plans/round-9-record-draft.md` (+537), and
`tools/tsukuroi-census.sh` (+884/−7). Round 10 has landed nothing in-tree at this
freeze; a sibling round-10 lane's artifact was **appearing and still moving** during
this window (`?? corpus/knowledge/census-closeout-receipt-r10.md`: 15 176 B /
179 `wc -l` at 20:53:44Z → 15 313 B at 20:54:38Z — **shape only, no content read, no
pin taken**). Sibling scratch dirs observed shape-only (names/timestamps, 20:54Z):
`/tmp/w10-tsukuroi-s101-scratch/`, `-s102/`, `-s103/`, `-s104/`, this seat's
`-scr-s10/`; `/tmp/w10-scrb10/`, `/tmp/w10-scr-m10/`, `/tmp/w10-ver-m10/`,
`/tmp/w10-aud-*`, `/tmp/w10-audx10-*`, `/tmp/w10-b101-arc/`, `/tmp/w10-t10-*`,
`/tmp/w10-tameshi-*`, `/tmp/w10-mado-*`, `/tmp/w10-tabi-*`,
`/tmp/w10-preps11-tsukuroi/`, `/tmp/w10-prept11-*`, `/tmp/w10-prep-m11/` — the
round-10 seats are working; no pin here is taken from a moving revision.

## 1. Plan anchor and the round's measure

`plans/round-10.plan.md` (md5 `c905a263e7a343d2c84afb21262ec465`, sha256
`33c8f9fe485fa8cf5c6de25e0b079a76aa7e3d307449c65dbf888008678cf9e1`, 22 879 B, 321
`wc -l` / 322 as read — **unterminated final line**; committed inside `fac745b`;
drafted by PREP-S10 during the round-9 wave, so every round-9 artifact it names is a
plan-side reading, never landed state):

> Axis move: **calibration — the lane's first**. The move is the **ten-round
> synthesis**: the lane's own claim-vs-realized ledger for rounds 1–10, and the
> **standing discipline of the census** it distills — the rules that keep the realized
> gate re-derivable by a non-author instead of remembered by the author.
> (`plans/round-10.plan.md:23-34`)

Claims as the plan states them (`:78-174`):

- (a) **The census's standing discipline is distilled into standing rows** — one
  table (target `corpus/knowledge/ten-round-synthesis.md` §4; the realized note name
  and row set are quoted at landing, never this proposal), every row citing the landed
  artifact + round that measured it. **No row makes a new host claim.** Rows carried
  (`plans/round-10.plan.md:84-123`): D1 fail-closed · D2 empty-proof · D3 counts move
  together · D4 captures, not quotes · D5 pins state their convention · D6 no pin from
  a moving revision · D7 sample rc never decides · D8 zero mutation · D9 one probe per
  fact · D10 printed traps · **D11 plane-set consistency (new, mechanical)** ·
  **D12 one-command re-derivation (new, mechanical; proposal: an `--identity` mode)** ·
  **D13 attested ≠ verified**.
- (b) **The mechanical rows are executable and fail-closed, with fixtures** — new
  selftest cases ≥4 (realized set quoted at landing; the round-5 lesson: no case is
  claimed that cannot fail): rollup-key set == emitted plane set on one invocation's
  stdout (falsifiable by dropping a rollup term or an emitter); crown verdict == the
  worst plane verdict on a forced mixed fixture (one BLOCKED + one DEGRADED → crown
  BLOCKED, exit 2); identity fields independently recomputed in the suite (md5/`wc`
  over the same file) with a mutated fixture copy caught; identity input unreadable, or
  `$0` not the revision (piped invocation, missing copy) → `unverifiable`, **never**
  `ok`; a fifth case (identity `cases=` vs the executed count) only if it can be made
  non-vacuous. The mode is a **re-derivation aid, not verification** (D13) — the note
  and the append must say so.
- (c) **The synthesis lands where the lane and the executor read it**:
  `corpus/knowledge/ten-round-synthesis.md` (proposal; the landed name wins) §1 the
  ten-round ledger (rounds 1–10; round 1 has **no plan file**, measured), §2 the gate
  arc, §3 the calibration record, §4 the standing-discipline table, §5 the debt ledger
  (open, with owners), §6 the unknowns register, §7 the closing state. Then the
  `SKILL.md` round-10 append (standing-discipline block, count restatements moved
  together with the identity pin, the D13 warning); `corpus/README.md` back-rows +
  the `## Frontier` section owed since round 1 (`LEARNING.md:57-58`); `SCORECARD.md`
  the final move row + the `SCORECARD.md:16` malformed row repaired **with its
  original text preserved verbatim** (the unescaped `|` escaped only; the repair
  recorded in the LOG; adjudicated at landing); `corpus/lessons/round-10.md`
  (`## Gate` + the outside spot-check ≥1 admit, ≥1 reject; `LEARNING.md:37-43,61-62`);
  the LOG closing entry (scribe). **Closing hygiene, owed since round 3**: the
  post-append no-oral-context re-test against the final `SKILL.md` revision
  (`LOG.md:153-154`; `SHONEN.md:32-38`) — an executor seat; the tally recorded
  whatever it is.

**Measure as the plan states it** (`:207-222`): `--selftest` rc=0 with
`PASS (N9+M cases, M≥4)` from the executed run; the identity line prints and its plane
list equals the rollup keys of the same run; the executed count equals the SKILL
restatement (grep-checked, moved together); the live run prints the realized plane
count with verbatim notes; zero mutation (fixture byte-unchanged + `git status`
byte-identical before/after + no `db.lck`); the synthesis note landed with md5/line
count pinned and **no row quoting a plan as landed**; ≥3 standing rows and ≥2 ledger
rows re-derived by a **non-author** (each row's probe re-executed, each pin re-hashed);
the no-oral-context re-test run against the final revision;
`SKILL.md`/`README.md`/`SCORECARD.md`/`LOG.md`/`corpus/lessons/round-10.md` landed; the
closing `SHONEN` state recorded with evidence, `[x]` left to the review. Suggested
seats: discipline seat (identity mode + fixtures + table), synthesis seat (the note),
note/hygiene seat (SKILL append + README rows + Frontier + SCORECARD repair/row +
lesson), executor seat (no-oral-context re-test), non-author verifier (rows + ledger +
round-9 plane), scribe (LOG/commit).

**Plan-premise deltas measured now** (record, don't smooth) [observed]:

1. **Plane count resolved — and it is six, not five.** The plan expects "5 planes
   expected after round 9; Step 0 resolves the count" (`:29-30`). Step 0 result:
   round 9 landed **both** the update-safety plane (S9-1, the fifth) **and** the oom
   plane (S9-2, the sixth) — six `PLANE` emitters
   (`tools/tsukuroi-census.sh:2324-2329`), six rollup terms (`:2339`), live rollup
   `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED
   journal=DEGRADED update-safety=DEGRADED oom=HEALTHY)`. The plan's Step-0 item (i)
   ("`PLANE oom` — specified, not landed", `:190-191`) is **resolved by landing**:
   round 10 verifies it, never re-lands it.
2. **Plan pins are round-8-era and moved with round 9's landing.** The plan quotes
   `SKILL.md` `e2d058d4…`, 1169 `wc -l` and the census `e2c4558a…`, 1472 `wc -l`
   (`:224-289`); the landed revisions are `SKILL.md` `d276ecea…`, 1374 `wc -l` and the
   census `e32aac98…`, 2349 `wc -l` (§3.3). Same for `SCORECARD.md` (20→21),
   `LOG.md` (171→172) and the record drafts; `corpus/README.md` (20) and the
   `corpus/knowledge/` note set are unchanged. The record quotes landed pins, never
   the plan's draft pins.
3. **The plan's D11 line references are of the round-8 revision.** The plan writes
   "the freeze revision has no such check: the rollup and verdict lines hardcode four
   keys, `:1456-1464`" (`:111-114`). At the landed revision the rollup parenthetical
   hardcodes **six** keys (`:2339`) and the emitters are `:2324-2329`; a key-set ==
   emitted-set check is still **absent** from the suite (the verdict regexes accept an
   optional trailing ` name=VERDICT` group instead — e.g. `:1947`, `:2113`). D11/D12
   remain **new, mechanical** rows — now against the six-plane realized set.
4. **The synthesis and the `--identity` mode are proposals.** The realized note name,
   section set, row numbering and the mode's name/fields are quoted at landing, never
   this draft's; a field the landed harness cannot support must print `unverifiable`,
   never a guess (`:123-137`, `:207-222`). At this freeze the census has **no**
   `--identity` mode (measured: `usage()` `:439-452`; the token appears only in
   comments).
5. **Round-9 contract debts measured open at HEAD** — the synthesis's debt ledger must
   carry them, not drop them: the `corpus/knowledge/update-safety-v2.md` append-only
   errata pointer (v2 unchanged, `92803aea…`, 353 `wc -l`); the `corpus/README.md`
   back-rows (unchanged since round 3, `98bd0066…`, 20 `wc -l`;
   `git log --oneline -- corpus/README.md` = `9bcd162` only); the round's own
   `corpus/lessons/round-9.md` (**`corpus/lessons/` = 0 files**, measured);
   `SCORECARD.md:16` still malformed verbatim; **plus** the row-21 content question
   and the LOG phrasing questions (§2's anomaly block).
6. **The round-9 verifiers have no landed artifact.** `LOG.md:172` names "Verifiers:
   VER-S9 | AUD-S9", but no VER-S9/AUD-S9 file exists in the tree at this freeze
   (grep over `*.md`, `.git` excluded: only `LOG.md:172` and the round-9 record
   draft's own template lines match). Scratch evidence exists, **shape only**:
   `/tmp/w9-ver-s9-scr/` (`ver-301141e7/` — `301141e7…` is the sha256 prefix of the
   interim five-plane census revision `0f72f4cf…`) and `/tmp/w9-aud-s9-tsukuroi/`
   (`VERDICT.md`, 14 384 B). The record states landed-vs-scratch; the round-10
   non-author verifier may re-derive the rows instead of quoting either.
7. **The round's own lesson obligation starts from a ledger that is still empty.**
   `corpus/lessons/` holds 0 files after nine rounds — round 9's obligation
   (`plans/round-9.plan.md`; `SKILL.md:1331-1332`) never landed. Round 10's lesson, if
   it lands, records round 10's own gate decisions; a retro Gate for rounds 1–9 would
   invent decisions that were never recorded (the round-9 plan's own candidate-(D)
   reasoning, `plans/round-9.plan.md:35-51`). The synthesis's §7 closing state must
   say which lesson files exist, whatever the answer at landing.

## 2. Step 0 — round-9 landing check against its own measure [observed]

Round-9's measure: its plan's contract (`plans/round-9.plan.md`, md5
`3a59d2edd068abf6281d7701d261ea5c`, 19 509 B, 270 `wc -l` / 271 as read) plus the
round-10 plan's Step 0 restatement (`:176-192`). Verdict: **round 9 landed its gate —
and more gate than its own draft anticipated (six planes, not five) — plus its note,
its SKILL append and its LOG/SCORECARD rows; it left four named obligations unpaid.**

| round-9 member | landed? | pin at draft time |
|---|---|---|
| census revision — update-safety plane (S9-1) | **yes** | part of the committed revision below; 14 `(R9)` cases `:2110-2183`; semantics distilled `SKILL.md:1219-1297` |
| census revision — oom plane (S9-2) | **yes** — the watch round 8 specified and did not land | 11 `(S9-2)` cases `:2198-2283`; emitter `:2329`; rollup term `:2339`; baseline embedded `R8_OOM_BASELINE :394-395` |
| committed census revision | **yes** | md5 `e32aac98c6b54f9d7fb8bc4f348cd467` · sha256 `c396662e…` · 2349 `wc -l` (2350 as read) · 123 410 B; 6 `PLANE` emitters `:2324-2329`; the append's first pin `0f72f4cf…` (2011 `wc -l`, 63 cases, 5 planes) was **superseded pre-commit** by the post-write addendum's `e32aac98…` (`SKILL.md:1345-1356`) |
| `PLANE update-safety` shape | **yes — a plane line**, not an extension | 5th emitter `:2328`; arm words/composition/mapping `SKILL.md:1219-1277`; fold exposure-only from the same-process reading (`PKG_FOREIGN_LIVE`, published `tools/tsukuroi-census.sh:651`; use `:1529-1531`) |
| selftest count | **yes — 74** | this seat's executed run (§3.1) = 49 legacy (35 base + 6 foreign-baseline + 8 S7-2) + 14 `(R9)` + 11 `(S9-2)`; `check '` labels counted = 74 |
| SKILL round-9 append | **yes** | `SKILL.md` md5 `d276ecea…`, 1374 `wc -l` / 1375 as read; append `:1172-1343`; post-write addendum `:1345-1374` |
| `corpus/knowledge/aur-drift-receipt-r9.md` (S9-3) | **yes** | md5 `e7d6f70b65e4846ad7001b5a66e8ec73`, 248 `wc -l` (unterminated) |
| `corpus/knowledge/update-safety-v2.md` errata pointer | **no — still owed** | v2 unchanged `92803aea…`, 353 `wc -l` (the append's own errata block names it owed, `SKILL.md:1329-1331`) |
| `corpus/README.md` back-rows (rounds 4–8 owed since round 3; round 9 adds its own) | **no — still owed** | `98bd0066…`, 20 `wc -l`, last touched `9bcd162` (round 3) |
| `corpus/lessons/round-9.md` (the lane's first lesson file) | **no — still owed** | `corpus/lessons/` = 0 files (measured) |
| SCORECARD round-9 move row | **yes** | `SCORECARD.md:21` (verbatim below); content questions named |
| LOG round-9 entry | **yes** | `LOG.md:172` (one line; verbatim below) |
| round-9 record | **yes** | `plans/round-9-record-draft.md` md5 `b5d6681e77702e20ee0f5d5bdbf52ca5`, 536 `wc -l` (committed); the record itself is the LOG entry |
| non-author verification of the round-9 plane | **no landed note** | LOG names VER-S9/AUD-S9; scratch only (§1 delta 6) — round 10's verifier owes the rows |

**The round-9 LOG line, verbatim** (`LOG.md:172`) [observed]:

```
- 2026-10-14 — round 9 (training r8): the 5-plane census landed (update-safety arms — the r7 AUD-X7 gap closed; PLANE oom); the AUR drift receipt; update-safety v3. Axis: coverage + operability. Verifiers: VER-S9 | AUD-S9.
```

Anomalies to record, not smooth (each an exact quote plus the landed measurement):

- "**5-plane census**" vs the realized **6** emitters: read as a total the numeral is
  low; the same line names `PLANE oom` separately. The record states the realized
  count (6); if the line is repaired, its original text is preserved.
- "**the r7 AUD-X7 gap closed**" attached to the update-safety arms: AUD-X7 was the
  **memory arm's** verification gap, closed by VER-S8 in round 8 (`LOG.md:171`,
  `SKILL.md:1042-1071`); what round 9 closed is round-7 claim (a), the update-safety
  plane's non-landing. Record both citations; do not silently reassign.
- "**update-safety v3**": the note is byte-identical to its round-8 landing
  (`2ac0c21d…`, 387 `wc -l`, unchanged); its presence in a round-9 line is at best
  carry-context; the record states the pin.
- `SCORECARD.md:21` verbatim: `| 9 | coverage + operability | round-8 state | the
  5-plane census landed (update-safety arms — the r7 AUD-X7 gap closed | wave-9
  32-lane (2 rerouted alibaba->hyper) |` — the After cell ends "…gap closed" with an
  unmatched `(` and without the "; PLANE oom" clause (6 pipes = 5 cells: structurally
  a normal row, **content** truncated; the pipe count measured). `SCORECARD.md:16`
  remains **malformed** (7 pipes — the unescaped `|` truncates the After cell to
  `boot plane (299 L`), verbatim: `| 4 | freshness + depth | round-3 state | boot plane
  (299 L | wave-4 32-lane; VER-S1 |`.

**The round-10 plan's Step 0 list, resolved** (`plans/round-10.plan.md:176-192`)
[observed]:

(i) census revision + selftest from an executed run — **6 planes, 74 cases** (§3.1).
(ii) `PLANE update-safety` as a plane line or an extension — **a plane line** (5th,
    §2 table).
(iii) realized arm words/composition/mapping and the fold — quoted
    `SKILL.md:1219-1277`; the 7 d `TSUKUROI_CHANNEL_MAX_AGE_D` rule, the `offline.db`
    exclusion and the same-process fold are realized as specified.
(iv) SKILL round-9 append — landed, with its post-write addendum.
(v) v2-note errata pointer — **owed**. (vi) README back-rows — **owed**.
(vii) `corpus/lessons/round-9.md` — **owed**. (viii) the round-9 record name —
    `plans/round-9-record-draft.md` (draft) + the `LOG.md` entry (record).
Then the round-8 carried ledger: `PLANE oom` — **landed** (round 10 verifies, never
re-lands); the round-2 note errata pointer — **still owed** (`update-safety-note.md`
unchanged, `5cc3067f…`, 478 `wc -l`); README rows — owed (same as vi);
`SCORECARD.md:16` — still malformed verbatim; the E4–E8 errata on
`oom-event-plane.md` — **not applied** (note unchanged `7e99d712…`, 433 `wc -l`; that
note's owner applies them).

**Consequence for round 10's order of work [inference].** Round 9 pre-empted none of
round 10's three claims; the synthesis's §1/§3 material is now sharper, not weaker:
the round-9 plan expected 5 planes and `PASS (49+M)`; the realized gate is **6
planes / 74 cases** — a plan-vs-landed mismeasure of exactly the kind the calibration
record exists to count. The four unpaid obligations (v2 pointer, README back-rows,
lesson file, plane verification) enter §5's debt ledger with owners; this draft
re-designs none of them.

## 3. Draft-time baseline receipts (this seat, read-only)

### 3.1 Gate, re-run 2026-10-14 20:51Z

Raw captures `/tmp/w10-tsukuroi-scr-s10/{selftest,live}.out`:

```bash
bash tools/tsukuroi-census.sh --selftest   # 20:51:0xZ, rc=0, 11.8 s wall
bash tools/tsukuroi-census.sh              # 20:51:29Z, rc=1, 2.8 s wall
```

Selftest last line verbatim: `TSUKUROI_CENSUS_SELFTEST: PASS (74 cases, 74 passed,
0 failed)`. Live run verbatim:

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T20:51:29Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2[user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922897 C5_swap_peak_pct=99% C5_pswp=74576922/96424269 C5_sock_throttled=73513; C6_psi_some_avg300=0.00 C6_psi_full_avg300=0.00 C6_psi_full_total_us=72724452 C6_avail_kb=17183848 C6_shmem_kb=8599904; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=798 (coredump=523 kernel=139 other=136); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
PLANE update-safety: DEGRADED (status=UNKNOWN-UPSTREAM; pending=none; qu=rc=1/0; sup=0; join=equal=1171 behind=0 ahead=1 src=sl+expac; expac=agree; chan=dbs=4 fetch=3d stamp=36d; offline.db=present(stamp=85d birth=11d); log=cmd=-S@2026-10-13T16:37:58-0300; refresh=none-in-window(last 300 lines); classes=offline-exile:14,aur-local:2; trap=-Suu:1[omarchy/1password-beta 8.12.42_32.BETA-1]; traps=[-Qu blind to shadowed-newer; '%s' is not a size]; vocab: SKILL.md:358-368)
PLANE oom: HEALTHY (window=boots=13 2026-10-03..2026-10-14; C1_kernel=3 killed_process=1; C2_events=3 C3_events=3 clusters=2[2026-10-13 23:44,2026-10-14 13:10]; base=r8(2) known=2[A, B] new=0 missing=0 out_of_window=0; ledger=vmstat.oom_kill=1; anchors=see drivers.mem; traps=presence-not-count,peak-not-datable,launch-not-live; rule=both-readings-carried; r8 vocab: kill-event-deep-r8.md §1)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=HEALTHY)
```

— **six** `PLANE` emitters, six rollup terms; zero-mutation receipt: `git status
--short` 0 lines before / 0 lines after, byte-identical (`status-before.txt` /
`status-after.txt`); `/var/lib/pacman/db.lck` absent. At landing the record quotes the
**post-round-10** run, never this one.

Drift note [observed]: against the round-9 addendum's 20:10:48Z capture — journal
`err=797 (coredump=522…)` → `err=798 (coredump=523…)`; drivers `C5_pswp`
74004334/96405737 → 74576922/96424269, `C6_avail_kb` 18111272→17183848, `C6_shmem_kb`
6586876→8599904; update-safety line differs only in `offline.db=… birth=10d` →
`birth=11d` (same `stamp=36d`); the oom plane line reads byte-same as the addendum's
quoted live line. Same-value readings are captures too, never confirmations.

### 3.2 Probe receipts, 20:53Z (fill material for the record's captures)

All read-only, unpiped rcs quoted [observed]:

- `pacman -Qu` — **rc=1, 0 lines** ("no candidates", not "unreadable").
- `pacman -Sup --print-format '%r/%n %v'` — **rc=0, 0 lines** (plan verb).
- `pacman -Suu --print-format '%r/%n %v'` — **rc=0, 1 line**: `omarchy/1password-beta
  8.12.42_32.BETA-1` — the downgrade trap row, byte-same across rounds 2/7/8/9/10.
- `/var/lib/pacman/db.lck` — **absent**.
- Sync-db **births**: core/extra/multilib/omarchy all `2026-10-11
  12:54:13.542054496 -0300`; `offline.db` `2026-10-03 17:41:33.994891750 -0300`.
  **Mtimes** (upstream content stamps): core `2026-09-08 15:23:46`, extra `:47`,
  multilib `:45`, omarchy `2026-10-11 10:16:17`, offline `2026-07-20 21:11:36`
  (**36 d** content stamp — a capture).
- `/var/log/pacman.log` — **2109 lines**; last entry `[2026-10-13T16:37:59-0300]`
  (`transaction completed` + `35-systemd-update.hook`).
- `expac` present (`/usr/bin/expac`, `10-13`); `pacman -Qm` **16 rows**;
  `journalctl --list-boots` **14 lines** (13 boots + header).
- `/var/lib/systemd/coredump` — **479 files / 3.5 G** (the coredump-storm class;
  owner: journal workstream — reported, not absorbed).

### 3.3 Artifact pins, hashed 2026-10-14 20:51–20:54Z (clean tree — committed bytes)

Convention: **U** = unterminated final line, **N** = newline-terminated. A pin must
state its convention (the rule's landed home: the round-9 append's identity blocks,
`SKILL.md:1186-1195`, `:1345-1356`; the round-8 block's `:1001-1006` has moved).

| artifact | md5 | `wc -l` | end |
|---|---|---|---|
| `tools/tsukuroi-census.sh` (round-9 revision) | `e32aac98c6b54f9d7fb8bc4f348cd467` | 2349 (2350 read) | U |
| `SKILL.md` (round-9 append + addendum) | `d276ecea1b1abaf5d6bbf6a6d7e31746` | 1374 (1375 read) | U |
| `LOG.md` | `68413998f6770e8b85ed88e5d8c693d3` | 172 | N |
| `SCORECARD.md` | `da962e185f874e4686d92ab21a58572a` | 21 | N |
| `SHONEN.md` | `9cf1d450685ae0ed0d15dee1b54e8fd5` | 51 | N |
| `MINT.md` / `PROVINCE.md` / `AGENTS.md` | `1d75fce9…` / `f1722b16…` / `390017cf…` | 19 / 19 / 6 | N |
| `corpus/README.md` | `98bd00668e84f18cf6781718c4d09ea0` | 20 | N |
| `corpus/QUALITY.md` | `e31cef8e56f3666406ab9314d3de3f0e` | 8 | N |
| `plans/round-9.plan.md` / `round-10.plan.md` | `3a59d2ed…` / `c905a263…` | 270 / 321 | U |
| `plans/round-9-record-draft.md` | `b5d6681e77702e20ee0f5d5bdbf52ca5` | 536 | U |
| `corpus/knowledge/aur-drift-receipt-r9.md` | `e7d6f70b65e4846ad7001b5a66e8ec73` | 248 | U |
| `corpus/lessons/` | — | **0 files** | — |

Earlier-plan pins re-hashed at this freeze (aids for §2's ledger; the ledger may also
re-derive via `git show <commit>:tools/tsukuroi-census.sh`): `plans/round-2.plan.md`
`3563bd41…` 10 · `round-3` `160a0272…` 13 · `round-4` `63c26bb1…` 10 · `round-5`
`0e9e8640…` 11 · `round-6` `81a9be07…` 38 · `round-7` `bb915954…` 160 · `round-8`
`0bef822d…` 216; record drafts `round-4` `a44f15db…` 300 · `round-5` `899db964…` 453 ·
`round-6` `4e9708ab…` 424 · `round-7` `c1eed63a…` 425 · `round-8` `9e7399c3…` 448.
**No round-1 plan file exists** (`git log --all -- plans/round-1.plan.md` empty —
re-measured; the ledger's round-1 row must use the commit `55b2186` as its anchor).

Knowledge-note pins re-hashed at this freeze (all 21 files incl. the r9 receipt; the
round-9 record draft's table reproduces): `aur-risk-plane.md` `1a584300…` 341 ·
`aur-risk-plane-ver-s6.md` `b0de352d…` 133 · `aur-risk-plane-ver-s7.md` `4608743d…`
184 · `boot-plane.md` `e722b7a9…` 312 · `degraded-triage-r4.md` `d57ae2d4…` 607 ·
`driver-firmware-plane.md` `518eda8f…` 256 · `executor-test-sufficiency.md`
`4b2c1d36…` 219 · `foreign-provenance-r6.md` `1b8f47a2…` 307 · `host-health-report-r3.md`
`98a0f263…` 563 · `journal-boot-plane.md` `e5ca40da…` 430 · `kill-event-deep-r8.md`
`6685e1da…` 340 · `memory-arm-mutants-s8.md` `a09e5604…` 181 · `memory-arm-ver-s8.md`
`861d83ad…` 251 · `oom-event-plane.md` `7e99d712…` 433 · `package-state-plane.md`
`ef93f1b7…` 323 · `systemd-user-plane.md` `af07a829…` 265 · `timer-drift-plane.md`
`fc0760c8…` 332 · `update-safety-note.md` `5cc3067f…` 478 · `update-safety-v2.md`
`92803aea…` 353 · `update-safety-v3.md` `2ac0c21d…` 387.

### 3.4 Census shape anchors re-resolved (the fills' line references)

Re-read at 20:51Z against the landed revision [observed]:

- header comments `:1-435` (round-9 additions `:28-45`); `usage()` `:439-452` — **no
  `--identity`**; helpers `:456-527` (`cap` `:456`, `rank` `:465`, `worse` `:474`,
  `class_counts` `:501`, `oom_keys` `:523`).
- overrides block `:327-355` (`PACMAN` `:327` … `CHANNEL_MAX_AGE_D` `:354`,
  `LOG_TAIL_N` `:355`); `R6_FOREIGN_BASELINE` `:368`; `R8_OOM_BASELINE` `:394-395`;
  `CLASS_OOM` `:397`, `CLASS_IO` `:398`, `CLASS_GPU` `:399`, `CLASS_FAILED` `:400`,
  `CLASS_OOM_SYS` `:401`, `CLASS_SIGKILL` `:402`; `R6_FOREIGN_CLASSES` `:409`;
  `PKG_FOREIGN_LIVE` `:437` (published `:651`, folded `:1529-1531`).
- probes: `probe_packages` `:530`, `probe_systemd` `:688`, `probe_drivers` `:754`,
  `probe_mem_arm` `:876`, `probe_oom_plane` `:1012`, `probe_journal` `:1153`,
  `version_join` `:1271`, `probe_update_safety` `:1303`.
- selftest: `run_selftest` `:1571`; fixture dispatcher `:1580-1649`; `check()`
  `:1757`; legacy + foreign-baseline + memory cases up to `:2101`; `(R9)` cases
  `:2110-2183`; `(S9-2)` cases `:2198-2283`; PASS printf `:2280`.
- `main()` `:2286`; emitters `:2324-2329`; rollup printf `:2339`; exit map
  `:2343-2346`; final line `main "$@"` `:2350` unterminated (2349 `wc -l`).

**Marginality note for the record:** the round-9 append's inner line refs (e.g.
`:1861-1949`, `:1081-1352`) are of the interim 2011-line revision; the record
re-anchors every fill at the landed revision (§3.4 is that re-anchoring for the
draft).

### 3.5 Case-layout attribution

74 executed = 49 legacy (35 base + 6 foreign-baseline + 8 S7-2 memory) + 14 `(R9)`
update-safety + 11 `(S9-2)` oom. Labels the record will quote from its own run; at
this freeze they are: the 14 `(R9)` labels listed verbatim in `SKILL.md:1280-1289`
(INERT over a fresh channel · REQUIRES-PREP with names · empty `-Qu` at rc=0
unreadable · empty over no channel · stale content stamp UNKNOWN-UPSTREAM ·
channel-freshness threshold honoured · fold names unknown-provenance arrivals ·
fold never off a missing baseline · joined class split = AUR-local pair · `-Suu`
trap row verdict-neutral · log window miss prints `cmd=unknown` · repo-side behind
row joins candidates · absent `expac` never a silent pass · unreadable join printed)
and the 11 `(S9-2)` labels measured at `:2198-2283` (clean window · embedded r8
baseline · external baseline file · new cluster named · declared wave missing ·
wave older than window (retention only) · absent baseline never HEALTHY · unreadable
ledger = named unknown · window unreadable · no boot measured · scan unreadable
fails closed).

## 4. Fill rules — what the record must state on landing

**(a) The self-sweep — the headline.** The realized synthesis note (path, md5,
sha256, `wc -l`, unterminated-or-not) and its realized section set. The §1 ten-round
ledger — one row per round: dispatch plan pin (**round 1: no plan file**, measured;
anchor = commit `55b2186`), the claim, the realized artifact + re-hashed pin, the
mismeasure the round caught (counted, cited), debt created/finished. §2's gate arc —
**executed runs only**; at this freeze the arc is: 744 / 17 / 3 planes (`7a3d3b94…`)
→ 976 / 26 / 4 (`41953ee9…`) → 1 032 / 35 (`e9327046…`, `SKILL.md:599-622`) →
1472 / 49 / 4 (`e2c4558a…`) → interim 2011 / 63 / 5 (`0f72f4cf…`; uncommitted,
superseded) → **2349 / 74 / 6 (`e32aac98…`)** — each row citing its source block or
commit; the record re-derives via `git show <commit>:tools/tsukuroi-census.sh` +
`md5sum` rather than quoting. §3's calibration record (round-1's four retractions,
round-4's 755-not-644, round-5's 1/4 survivors, round-8's M01 miss + 9
un-exercised clause sites, and round 9's 5→6-plane / 63→74-case realized count —
"the plan expected X, the run read Y" rows). §4 the D-rows realized set — quote the
landed numbering; **no row makes a new host claim**. §5 the debt ledger, which must
carry (not drop): the v2 errata pointer, README back-rows, `corpus/lessons/round-9.md`,
`SCORECARD.md:16`, the E4–E8 unapplied errata, `PLANE oom`'s own non-author
verification, the carried operator/boundary list, and `SCORECARD.md:21`'s content
question. §6 the unknowns register. §7 the closing state — probation rounds 1–10,
`SHONEN` boxes with evidence pointers, `[x]` left to the non-author review (**no
self-promotion**; `SHONEN.md` unchanged since round 3, `9cf1d450…`, 51 `wc -l`).
The ledger's round-10 row is the only plan-row and is marked as such.

**(b) The mechanical receipts.** The realized `--identity` mode (name/fields as
landed — or its absence, recorded); the executed `PASS (74+M cases, M≥4)` with the M
labels; the identity line's plane list == the rollup keys **of the same run**; the
identity fields recomputed; the unverifiable path (piped invocation / missing copy →
`unverifiable`, never `ok`, rc per the fail-closed stance); the mixed fixture
(BLOCKED+DEGRADED → crown BLOCKED, exit 2); a mutated fixture copy caught; the fifth
case only if non-vacuous — **state dropped-if-dropped**. **D13 stated**: the mode
re-derives, it never verifies (a self-identity is not a non-author check).

**(c) The contract artifacts.** `SKILL.md` round-10 append (standing-discipline
block citing the note §; count restatements moved together — current expected line
`PASS (74 cases, 74 passed, 0 failed)` at `:1359`, `:1373-1374`; a round-10 gate
revision makes the 26/35/49/63/74 restatements history and must move them with it).
`corpus/README.md` back-rows (rounds 4–9 + the gate rows for the round-7 and round-9
revisions + the synthesis note) and the `## Frontier` section (`LEARNING.md:57-58`) —
or the debt stated open, never silently skipped. `SCORECARD.md` the final move row
(axis: calibration; the ten-round axis summary) + the row-16 repair (original text
preserved verbatim; escaped `|` only; the repair recorded in the LOG) + the row-21
call (same discipline: quote, then repair-or-record — its unmatched paren and its
"5-plane" numeral against the realized six). `corpus/lessons/round-10.md` (`## Gate`:
candidates considered/admitted/rejected with reasons for round 10 **only** — no
retro-fabrication; plus the outside spot-check ≥1 admit, ≥1 reject, `agree/disagree`
with reason; `LEARNING.md:37-43,61-62`). The LOG closing entry (first line carries
the self-sweep). The commit carries the lane identity (`AGENTS.md:5`); message
pattern `probation round 10 (training r9): see LOG`. **Closing hygiene**: the
post-append no-oral-context re-test against the **final** `SKILL.md` revision
(`LOG.md:153-154`; `SHONEN.md:32-38`) — an executor seat, the tally recorded whatever
it is.

**(d) Headline placement.** §5's first line carries the self-sweep + the realized
gate pin, not the notes; the second thread states Step 0's verdict (six planes;
four unpaid obligations; the ledger's round-9 anomalies). If any sibling lane lands
a list item first, the record quotes the realized one and does not re-do it.

## 5. Record skeleton (what the `LOG.md` entry must carry on landing)

Round 8/9 used one-line entries; the round-10 headline (the self-sweep) must stay on
the first line. Candidate (fill at landing):

```
- 2026-10-14 — round 10 (training r9): the ten-round self-sweep lands — ⟨N⟩ standing
  rows (D1–⟨…⟩) + the rounds-1–10 claim-vs-realized ledger in
  `corpus/knowledge/⟨ten-round-synthesis⟩.md` (md5 ⟨…⟩, ⟨L⟩ ln); gate at ⟨md5⟩ /
  ⟨lines⟩ — selftest 74→⟨74+M⟩ (M≥⟨4⟩: ⟨case names⟩; identity mode ⟨…⟩), live
  ⟨6⟩-plane rollup ⟨verbatim⟩; contract: SKILL round-10 append + ⟨README back-rows +
  Frontier | owed⟩ + ⟨corpus/lessons/round-10.md | owed⟩ + ⟨SCORECARD row-16 repair |
  not repaired⟩. Axis: calibration (first). Verifiers: ⟨…⟩.
```

- **Work (observed in tree):** ⟨artifact list: path, seat/ID, md5, lines, mtime⟩ —
  expected members: the synthesis note, the census revision (identity mode),
  the SKILL append, the README rows, the lesson file, plus scribe-owned
  SCORECARD/LOG; each member's write scope is named, not absorbed; the closing
  re-test receipt recorded with its tally.
- **Scribe re-verification:** §6 command set; quote the selftest line, the identity
  line, the live six-plane rollup (plus any round-10 plane), one verbatim new case
  label, and the re-executed row probes (the non-author's rows named separately).
- **Ancillary scribe writes (owed at record time):** `SCORECARD.md` final move row
  (+ row-16 repair + row-21 decision; axis vocabulary per `AXES.md:9-16`);
  `corpus/README.md` back-rows + `## Frontier`; `SKILL.md` count restatements with
  any gate revision; this `LOG.md` entry; the commit.
- **SHONEN boxes:** stay `[~]` (asserted with verifier names); evidence pointers may
  refresh; `[x]` stays with the non-author promotion review. `SHONEN.md` unchanged
  since round 3 (`9cf1d450…`, 51 `wc -l`) [observed].
- **State at entry:** the round commit hash landed, or "round work uncommitted in
  tree" + exact `git status --short`; the scribe writes only its named files; the
  commit carries the lane identity; message pattern above.

## 6. Scribe re-run set (receipts owed by the record)

```bash
cd ~/Projects/shokunin/tsukuroi-shokunin
bash tools/tsukuroi-census.sh --selftest            # expect rc=0, 74+M/74+M PASS
bash tools/tsukuroi-census.sh                       # expect rc=1, 6-plane rollup (+ round-10 term if any)
bash tools/tsukuroi-census.sh --identity            # if landed: one machine-readable line; else record its absence
md5sum tools/tsukuroi-census.sh; sha256sum tools/tsukuroi-census.sh
wc -l tools/tsukuroi-census.sh; wc -c < tools/tsukuroi-census.sh
grep -n '^PLANE\|^TSUKUROI_CENSUS' <live-run-file>  # count emitters vs rollup keys
pacman -Qu; echo "rc=$?"                            # UNPIPED: rc=1 + empty = 0 candidates; other rc = unreadable
pacman -Sup --print-format '%r/%n %v'; echo "rc=$?" # plan verb; 0 lines today
pacman -Suu --print-format '%r/%n %v'; echo "rc=$?" # the trap row (1 line today)
test -e /var/lib/pacman/db.lck && echo present || echo absent
stat -c '%w | %y | %n' /var/lib/pacman/sync/*.db    # births (authoritative) + mtimes (stamps)
wc -l < /var/log/pacman.log; tail -2 /var/log/pacman.log
pacman -Qm | wc -l                                  # (pipeline rc — do not cite it as a measurement)
command -v expac && expac -Q '%v' expac
find . -path ./.git -prune -o \( -name '*.tsv' -o -name '*baseline*' \) -print
ls corpus/lessons/                                  # round-10.md exists? round-9.md?
sed -n '16p;21p' SCORECARD.md                       # :16 defect + round-9 row
git log --oneline -- corpus/README.md               # README row debt (last 9bcd162, round 3)
md5sum corpus/knowledge/update-safety-v2.md         # errata pointer landed?
git show <r2/r3/r5/r7/r9 commit>:tools/tsukuroi-census.sh | md5sum   # the arc, re-derived
git status --short                                  # zero-mutation receipt (before/after)
# + the realized synthesis note pin; + the round's own new case labels from the executed run
```

Rules restated: never carry a piped rc as a measurement (`| head`, `| wc -l`); a
probe's rc is the command's own only when unpiped; empty `-Qu` is only a pass with
the channel reading present and its age printed; an unreadable probe is `BLOCKED`,
never `INERT`; **no pin from a moving revision** (round 10 is concurrent — re-hash
only committed or frozen bytes; a moving file is observed shape-only).

## 7. Unknowns register (draft-time; owners)

1. The realized synthesis: note name, section set, D-row numbering/labels, ledger
   row set, the closing-state wording (owner: synthesis seat; the record quotes
   realized values, never this draft's).
2. The realized `--identity` mode: name, fields, exit shape; whether the fifth
   fixture case is non-vacuous; the realized M labels and the new count (owner:
   discipline seat). At this freeze the mode does not exist in the census.
3. Which hygiene items land this round vs stay owed: the v2 errata pointer, README
   back-rows + `## Frontier`, `corpus/lessons/round-10.md`, the SCORECARD repairs
   (owner: note/hygiene seat + scribe; the record states realized, never assumes).
4. Whether the round-9 verifier products (VER-S9/AUD-S9) are landed in round 10, or
   the rows are re-derived by the round-10 non-author verifier without them (owner:
   verifier seat; LOG names them, the tree does not hold them).
5. The row-16 repair-vs-keep call and the row-21 repair call; whether the LOG's
   "5-plane" / "AUD-X7" / "update-safety v3" phrasings are repaired or carried as
   errata (adjudicated at landing; historical text preserved either way).
6. Whether the SCORECARD's "axes" contract (`AXES.md:33-39` — axes scores,
   planned, retired) needs a pinning structure beyond the move-log row (owner:
   note/hygiene seat).
7. Whether the training ladder extends past round 10 [unknown — the synthesis stands
   either way, not contingent]; the promotion review outcome [non-author; `[x]` stays
   theirs].
8. Upstream Arch/omarchy delta since 2026-09-08 — **the** real update gate — stays
   [unknown] read-only (the 36 d stamp is a capture); `pacman.log` rotation window at
   landing [unknown — the `cmd=unknown` row is built for the miss]; carried: root
   `-Qkk` delta; the 18/19 sweep-summary split; `1password-beta` provenance
   (operator); `walker-restart.hook` (kagi/operator); dkms stale `7.1.4-arch1-1`;
   `snapper` empty; `offline.db` coverage; `omarchy-walker`↔`walker` linkage
   (kaidoku/revenger); the "20-min cap" item (integrator); V8 heap-OOM and
   coredump-storm boundaries; E4–E8 unapplied errata; H1–H3 and the OOM counter Q2
   as read-only-unmeasurable carries.

## 8. Errata / pending (append-only)

- 2026-10-14 — this draft file created by SCR-S10; it is prep, not a record. The
  `LOG.md` round-10 entry remains owed (`AGENTS.md:3`); measures are judged against
  the landed synthesis + gate revision + contract artifacts, not this skeleton.
- 2026-10-14 — all counts in §3 are captures on a live host (coredump storm live:
  523 in-boot entries, dir 479 files / 3.5 G; C5/C6 counters move between runs;
  `boots=13 current=yes` is the same boot as the round-9 captures); re-run, never
  quote.
- 2026-10-14 — Step 0 result recorded above: round 9 landed the **six-plane** census
  (update-safety + oom), `PASS (74 cases)`, its SKILL append with a post-write
  addendum, the AUR drift receipt, and its LOG/SCORECARD rows; still owed at HEAD:
  the v2 errata pointer, the README back-rows, `corpus/lessons/round-9.md`, and the
  round-9 plane's non-author verification (LOG names VER-S9/AUD-S9; no landed
  artifact). This draft re-designs nothing; it names the debts for the record scribe.
- 2026-10-14 — plan-vs-landed deltas measured (§1): plane count 6 (not the plan's
  expected 5); plan pins are round-8-era and moved (census 1472→2349, SKILL
  1169→1374, SCORECARD 20→21, LOG 171→172); D11's line refs re-anchor to
  `:2324-2329` / `:2339` with six hardcoded keys — the key-set check is still absent
  from the suite; `--identity` absent at this freeze; the round-9 LOG's
  "5-plane"/AUD-X7/v3 phrasings and `SCORECARD.md:21`'s truncation recorded as
  questions to adjudicate at landing, never smoothed.
- 2026-10-14 — concurrency: round 10 is in flight;
  `corpus/knowledge/census-closeout-receipt-r10.md` appeared at 20:53:44Z (15 176 B)
  and grew to 15 313 B by 20:54:38Z — **shape only, content not read, no pin taken**;
  sibling scratch dirs (tsukuroi s101–s104, ver-m10, scrb10, aud-*, preps11-*)
  observed names/timestamps only. If the tree moves before landing, the record quotes
  only committed bytes.
- 2026-10-14 — the lesson-ledger boundary, restated so it cannot be read as
  retro-fabrication: `corpus/lessons/` holds **0 files after nine rounds** (measured;
  round 9's own lesson never landed); earlier rounds' candidate/reject decisions were
  never recorded, so a retro Gate would invent them (`plans/round-9.plan.md:35-51`
  reasoning). `corpus/lessons/round-10.md`, if it lands, records **round 10's own**
  gate decisions and the outside spot-check, nothing earlier — and if it does not
  land, the record says so plainly.
- 2026-10-14 — final-file spot-check and this file's own line count/md5 are reported
  in the seat's handoff, not in-file (a further edit would invalidate them). All
  fix-ups stay append-only above this line.
- 2026-10-14 20:56–20:57Z — **post-draft tree movement (append-only, shape only)**:
  after this draft's write, the tree gained `?? corpus/knowledge/calibration-synthesis.md`
  (34 119 B, 457 `wc -l`, mtime 17:56:57 -03) and `?? plans/round-11.plan.md`
  (23 156 B, 348 `wc -l`, mtime 17:57:22 -03); the closeout receipt settled at
  15 506 B / 183 `wc -l` (mtime 17:54:47 -03). Names/sizes/timestamps only — **no
  content read, no pin taken**. The realized synthesis name is a landing-time fact
  (§7 item 1, never assumed from the observed filename); the round-11 plan belongs to
  the next wave, not this record. Nothing above is re-measured against the moving
  files.