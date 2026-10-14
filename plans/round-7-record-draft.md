# Round-7 record — DRAFT (scribe prep, seat SCR-S7)

Status: **draft, pre-landing.** This file is the scribe's working skeleton for the
round-7 `LOG.md` entry and for the round's artifact families (the update-safety
plane joining `tools/tsukuroi-census.sh` + the v2 decision note). It is not the
record; the record is the append-only `LOG.md` entry written after every round-7
artifact has landed (`AGENTS.md:3`). Every number below is a draft-time capture
with its command and time; the host is live, so re-run, never quote.

Draft seat: SCR-S7. Draft window: 2026-10-14 18:20:18–18:23Z (15:20–15:23 -03),
host `plazir27`, user `vgpnk` (non-root). Write scope: this file only. Scratch:
`/tmp/w7-scr-s7-tsukuroi/` (ephemeral). All probes read-only; no
install/upgrade/remove/restart verb was run (`PROVINCE.md:16-17`); `yay` was
asked only for `--version`, no yay transaction verb; no external site contacted.

Tags used throughout: [observed] = measured now, command named; [inference] =
join from measurements; [unknown] = named gap with owner.

Round state at draft time [observed]: HEAD `dc3436d` ("probation round 6
(training r5): see LOG", committed 2026-10-14 15:17:26 -0300); `git status
--short` empty (clean tree). **Round 6 is fully committed** — register, receipt,
verifier note and OOM plane all landed in `dc3436d` (pins §3). **Round 7 has
landed nothing yet**: `corpus/knowledge/update-safety-plane.md` absent, the
census unchanged (`e9327046b05b5c71e07fe511ad7e82dd`, 1032 lines), tree clean.
Sibling round-7 scratch dirs are live (names/shape only, 15:21Z):
`/tmp/w7-s73-tsukuroi/`, `/tmp/w7-tsukuroi-s74/` (poll.sh + poll.log),
`/tmp/w7-tsukuroi-vers7/` (`poll-s71.sh`, `probe-foreign-pre.txt`) — the work is
concurrent; this draft's job is to have the fills ready when the artifacts land.

Post-freeze observation (18:24Z; **shape only, no content claim**): the tree
gained `M tools/tsukuroi-census.sh` — the arm seat landing the round-6 baseline
debt in the working tree. Three hashes 6 s apart:
`b4c73a591087957deb80f8fef18b9dab` (1134 lines) →
`321cdf44d18dd6c3c4c665bfede22ced` (1135) →
`47570bc25d3bd71477acf1bfbe42fc3a` (1136) — the revision is **uncommitted and
still moving**, so no pin is taken and no gate run was made against it; every
census pin elsewhere in this draft is the committed `e9327046…` revision.
Shape, per the file's own header comments: an embedded R6 foreign snapshot
(`R6_FOREIGN_BASELINE`, the register's §1 rows) plus a `TSUKUROI_FOREIGN_BASELINE`
external `name<TAB>version` override, fail-closed both ways; the fifth plane is
**not** in the revision yet (4 `PLANE` emitters, 35 `check` cases at 18:24:24Z).
The record re-hashes at entry; never quote this draft's reading of an in-flight
file as landed state.

## 1. Plan anchor and the round's measure

`plans/round-7.plan.md` (md5 `bb9159549bfdad7516af381f6f12965d`, 10 557 B, 161
lines, mtime 2026-10-14 14:45 -03; committed in `dc3436d`; drafted by PREP-S7
during the round-6 wave and citing round 6 as a plan, never as landed state):

> Axis move: operability — the fifth plane becomes executable: **update-safety
> joins the census**, and the post-AUR fold is its content.
> Claim (a): the update-safety plane joins `tools/tsukuroi-census.sh` (4→5
> planes, worst-plane rollup unchanged); plane note line carries the arm word
> (PASS · INERT · REQUIRES-PREP · BLOCKED · UNKNOWN-UPSTREAM · DO-NOT; BLOCKED >
> UNKNOWN-UPSTREAM > REQUIRES-PREP > INERT > PASS); gate-verdict mapping is
> **recorded, not silently applied**; probes = `pacman -Qu` (rc/emptiness) +
> `pacman -Sup --print-format '%n %v'` (the one allowed plan verb) + db births +
> `offline.db` shape + bounded `pacman.log` tail; the risk-class fold reads the
> round-6 baseline and names exposure only; pins/holds stay in the packages
> plane (no double-probe). Claim (b): the v2 decision note lands; the round-2
> note keeps its pins and gains a one-line errata pointer (append-only).
> Measure: `--selftest` rc=0 `PASS (35+N cases, N≥4)` (four new cases:
> inert-clean 5-plane rollup, candidates>0→REQUIRES-PREP, `-Qu`
> unreadable→BLOCKED, baseline absent→DEGRADED-never-HEALTHY); live run prints
> the 5-plane rollup with a verbatim `PLANE update-safety:` note; zero mutation;
> note v2 + `corpus/README.md` row + SKILL round-7 append + SCORECARD move row +
> `LOG.md` entry; ≥3 note rows spot-checked by a non-author.

**Plan anchors re-resolved at draft time [observed]** against the settled
`dc3436d` tree:

- Census (pre-round-7 revision, 1032 lines): foreign arm `tools/tsukuroi-census.sh:303-306`
  (`cap "$PACMAN" -Qm` → `foreign_n`), note assembly `:322`, verdict arm `:325`;
  `VERSION='census-v2'` `:142`; `cap()` `:191`; main probes `:1006-1009`
  (`probe_packages|systemd|drivers|journal`); the four `PLANE` emitters
  `:1011-1014`; rollup `local roll=HEALTHY` `:1016-1020`; verdict printf `:1022`;
  exit map after it. The plan's "4→5 planes" resolves to: one new probe
  function, one new emitter, one new rollup term, one new verdict field.
  Fixture machinery for the new cases: `TSUKUROI_FIXTURE` dispatcher `:637-641`,
  `check()` `:744-780`, per-case `case_home` blocks from `:789`; the pre-round-7
  `degraded-foreign` fixture is `:820-822` (pattern `^PLANE packages: DEGRADED
  .*foreign=3`).
- SKILL: the arm-vocabulary section head is `SKILL.md:359` ("Round-2
  update-safety note — verdict arms and boundaries"), the arm list + composition
  `:363-368` (the plan's `:358-368` re-resolves here); the one allowed plan verb
  text is `:409-416` (the plan's `:408-413`); the packages row `:41` already
  carries the round-6 foreign-risk rule; the DEGRADED bullet `:318-320` states
  the "accepted baseline is an operator question" reading; the round-6 append
  `:710-838` already tags the baseline as specified-not-landed (`:760-771`).
- Note (pre-round-7): `corpus/knowledge/update-safety-note.md` md5
  `5cc3067fec33d261d8bff6a5c7e8ac48`, 478 lines — candidate table §1 `:19-40`
  (the plan's `:19-72` bracket = §1 + §2), §7 decision table arms `:332-339`,
  hazards `:286-330`.
- Register (the round-6 debt contract): `corpus/knowledge/aur-risk-plane.md` §8
  `:314-329`; the realized per-class decision rows are §4's table `:212-221`.

## 2. Step 0 — round-6 landing check against its own measure [observed]

Round-6's measure (per its plan/register contract): register with one row per
live foreign package + both named classes + the `unknown-provenance` rule;
provenance/freshness receipt; a machine-readable baseline the census reads
(`foreign=` known-vs-new, fail-closed); ≥3 new selftest fixtures (hit / new /
version-drift); every class cites its probe; zero host mutation; SKILL rows.

| round-6 member | landed? | pin at draft time |
|---|---|---|
| register (name as landed, ≠ plan draft name) | **yes** | `corpus/knowledge/aur-risk-plane.md` md5 `1a584300f6b07da78bc8332f04b4fd30`, 341 `wc -l` (342 as read), 28 228 B |
| provenance/freshness receipt | **yes** | `corpus/knowledge/foreign-provenance-r6.md` md5 `1b8f47a2a807fc8bd2fc7302f15577c8`, 307 lines |
| verifier note (non-author recompute) | **yes** | `corpus/knowledge/aur-risk-plane-ver-s6.md` md5 `b0de352dec653891d5d36dd742536198`, 133 lines — CONFIRMED 2/2 rows per its own header |
| OOM-event plane (landed extra, S6-3) | **yes** | `corpus/knowledge/oom-event-plane.md` md5 `7e99d712ead088727c0980e52a121199`, 433 lines |
| **machine-readable baseline** | **no** | no file matches `*baseline*` or `*.tsv` anywhere in the tree (`find` excluding `.git`), and `git ls-files` has none. The register's own §8 heads "**written, not implemented**" (`aur-risk-plane.md:314-329`) and the SKILL round-6 append carries the tag (`SKILL.md:760-771`) |
| **census delta (`foreign=` known-vs-new + ≥3 fixtures)** | **no** | `tools/tsukuroi-census.sh` untouched since round 5: md5 `e9327046b05b5c71e07fe511ad7e82dd`, 1032 lines, foreign arm still bare-count (`:303-325`), no `TSUKUROI_*BASELINE` env name in the file's env inventory (`:131,146-161`), `degraded-foreign` fixture still the only foreign case (`:820-822`) |
| selftest count (executed, not quoted) | 35 | `bash tools/tsukuroi-census.sh --selftest` → rc=0, `PASS (35 cases, 35 passed, 0 failed)` (§3) |

**Consequence for round 7's order of work [inference, from the table].** Step 0's
"an unlanded part is named debt finished first (against the round-6 plan's
contract, not re-designed)" (`plans/round-7.plan.md:96-101`) means the round-7
arm seat lands, before or with the fifth plane: the baseline file (the register's
§8 spec is the contract — one row per foreign package:
`name version class validation first_seen`, path/format adjudicated by the arm
seat), the census read arm (env override in the `TSUKUROI_*` family, default =
the committed file), and ≥3 fixtures (hit / new / version-drift). The round-6
plan's own fixture-shape prerequisite still applies: a version-drift fixture is
vacuous unless the fixture `pm` file carries `name version` lines
(`plans/round-6-record-draft.md:284-290`). The record must state explicitly
whether the debt was finished inside round 7 or carried again — never imply it
landed. Note the coupling: round-7's own proposed fold says an absent/unreadable
baseline → `unavailable` → DEGRADED; at draft time the baseline **is** absent,
so a fifth plane landed without the debt would read `unavailable` on the live
host by construction.

**Post-freeze (18:24Z, shape only).** The arm seat began landing exactly this:
an uncommitted `tools/tsukuroi-census.sh` revision (header observation) whose
header comments describe an **embedded** R6 snapshot by default plus a
`TSUKUROI_FOREIGN_BASELINE` external `name<TAB>version` override — so the two
proposed standalone baseline paths (register §8's `aur-risk-plane.tsv`,
round-6 draft §4's `foreign-aur-baseline.tsv`) may both stay proposals; the
record quotes whatever realizes. No gate run was made against the moving
revision.

## 3. Draft-time baseline receipts (this seat, read-only)

Gate, re-run 2026-10-14 18:20:56–18:20:59Z (raw captures in
`/tmp/w7-scr-s7-tsukuroi/`):

```bash
bash tools/tsukuroi-census.sh --selftest   # 18:20:56Z, rc=0
bash tools/tsukuroi-census.sh              # 18:20:58Z, rc=1
```

Selftest last line verbatim: `TSUKUROI_CENSUS_SELFTEST: PASS (35 cases, 35
passed, 0 failed)`. Live run verbatim:

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T18:20:59Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16; pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=433 (coredump=270 kernel=139 other=24); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

The journal `err=` count is the only mover against the round-6 draft's capture
(432 at 17:38Z → 433 at 18:21Z): live storm drift, a capture, not disagreement
(`host-health-report-r3.md:441-462` precedent). At landing the record quotes the
**post-round-7** run (5-plane line), not this one.

Artifact pins, hashed 2026-10-14 18:20–18:22Z (clean tree — every hash is of
committed bytes):

| artifact | md5 | lines |
|---|---|---|
| `tools/tsukuroi-census.sh` (pre-round-7 revision) | `e9327046b05b5c71e07fe511ad7e82dd` | 1032 |
| `SKILL.md` (round-6 append landed) | `7b5dcf08b3143839301b7044a130a8cf` | 837 |
| `LOG.md` / `SCORECARD.md` / `SHONEN.md` | `2d6df41d8a77f32c4e7533ce2abb946d` / `9b04eb4d05fd720b0d3ca7addee31682` / `9cf1d450685ae0ed0d15dee1b54e8fd5` | 169 / 18 / 51 |
| `PROVINCE.md` / `AGENTS.md` / `MINT.md` / `corpus/QUALITY.md` | `f1722b163a5c433b003de362ab93ee11` / `390017cff803cc8798dd3b51d48a82f0` / `1d75fce9ed65ac6a22be115cc0c84055` / `e31cef8e56f3666406ab9314d3de3f0e` | 19 / 6 / 19 / 8 |
| `corpus/README.md` | `98bd00668e84f18cf6781718c4d09ea0` | 20 |
| `plans/round-6.plan.md` | `81a9be07fecfbf2af7540ea958143d3a` | 38 |
| `plans/round-7.plan.md` | `bb9159549bfdad7516af381f6f12965d` | 161 |
| `corpus/knowledge/aur-risk-plane.md` (r6) | `1a584300f6b07da78bc8332f04b4fd30` | 341 |
| `corpus/knowledge/foreign-provenance-r6.md` (r6) | `1b8f47a2a807fc8bd2fc7302f15577c8` | 307 |
| `corpus/knowledge/aur-risk-plane-ver-s6.md` (r6) | `b0de352dec653891d5d36dd742536198` | 133 |
| `corpus/knowledge/oom-event-plane.md` (r6) | `7e99d712ead088727c0980e52a121199` | 433 |
| `corpus/knowledge/update-safety-note.md` | `5cc3067fec33d261d8bff6a5c7e8ac48` | 478 |
| `corpus/knowledge/timer-drift-plane.md` (r5) | `fc0760c8070c9387ff5334f0f8c645cc` | 332 |
| `corpus/knowledge/boot-plane.md` (r4) | `e722b7a931858aa5ff1a89ce91cccca9` | 312 |
| `corpus/knowledge/degraded-triage-r4.md` (r4) | `d57ae2d48e01777e1ef3c8c0ffb642c9` | 607 |
| `corpus/knowledge/package-state-plane.md` (r1) | `ef93f1b78b6a9e17e8c9d096e7852a02` | 323 |
| `corpus/knowledge/journal-boot-plane.md` (r3) | `e5ca40dafc4d1d2a2158fded39067df6` | 430 |
| `corpus/knowledge/systemd-user-plane.md` (r1) | `af07a829cfd0307fbe970a2cdc054e18` | 265 |
| `corpus/knowledge/driver-firmware-plane.md` (r1) | `518eda8f0f39f25ee95c715571a9cf95` | 256 |
| `corpus/knowledge/host-health-report-r3.md` (r3) | `98a0f263f801245f6069e57a9f72d4af` | 563 |
| `corpus/knowledge/executor-test-sufficiency.md` (r3) | `4b2c1d3612db7db1477da92aaec39862` | 219 |

Every round-6-era pin above reproduces its round-6 value exactly at the draft
freeze (18:22Z). Post-freeze (18:24Z) the arm seat began landing the round-6
debt into `tools/tsukuroi-census.sh` as an uncommitted, still-moving working-tree
revision (header observation) — the pins above stay pinned to the committed
`e9327046…` revision and the record re-hashes at entry.

**Round-7 plan's own draft-time pins, re-measured 18:20:56–18:22Z — all
reproduced [observed]:**

- `pacman -Qu` → rc=1, 0 lines (no pipe; the pipeline-rc trap stays live:
  `-Qu | head` reports `head`'s rc — round-6 draft §2, re-stated).
- `pacman -Sup --print-format '%n %v'` → rc=0, 0 lines (the one allowed plan
  verb; no `db.lck` created).
- `stat -c '%w' /var/lib/pacman/sync/{core,extra,multilib,omarchy}.db` → all
  four birth `2026-10-11 12:54:13.542054496 -0300`; `offline.db` birth
  `2026-10-03 17:41:33.994891750 -0300` (mtimes are upstream stamps: 2026-09-08
  core/extra/multilib, 2026-07-20 offline, 2026-10-11 omarchy — the
  birth-vs-mtime trap, printed rule unchanged).
- `pacman-conf IgnorePkg IgnoreGroup` → rc=0, empty; `pacman-conf HoldPkg` →
  `pacman` + `glibc` (removal-protection, not a version hold).
- `pacman -Qm` → rc=0, **16** rows: 13 × `elephant-*` 2.21.0-1 + `omarchy-walker`
  1.0.0-2 + `android-apktool-bin` 3.0.3-1 + `obsidian-cli-inspector` 1.0.3-1
  (set unchanged since round 1). `pacman -Q` = 1188, `-Qe` = 207.
- `/var/log/pacman.log` readable: 157 286 B, 2109 lines, mtime 2026-10-13
  16:37:59.486 (-03). Refresh/upgrade lines: `:1405` `pacman -Sy --noconfirm
  fuse2` at `2026-10-11T12:54:13-0300` (second-exact with the db births);
  `:1414` `pacman -Syu --noconfirm godot blender …` at `2026-10-11T16:13:19-0300`
  ("starting full system upgrade" `:1416`; last full `-Syu` on the host); the
  two yay-cache installs `:2090` (13:52:59) and `:2097` (16:21:20) 2026-10-13.
  `:2058`-era `-S` lines are ordinary installs; nothing newer than 10-13 16:37.
- `yay --version` → `yay v13.0.1 - libalpm v16.0.1` (no yay transaction verb);
  `~/.cache/yay/` → 2 package dirs.
- boot id `d7f0bc8d938e4249b4a1f250cbfacf58` (still the plan's draft pin).
- memcg: `/sys/fs/cgroup/user.slice/user-1000.slice/memory.events` →
  `oom_kill 1`; `memory.swap.events` → `fail 5922849`; `memory.peak`
  30 699 745 280 B; `memory.swap.peak` 36 744 949 760 B. **Divergence worth
  recording:** the plan's `memory.peak` pin is the `user-1000.slice` value; the
  parent `/sys/fs/cgroup/user.slice/memory.peak` reads 30 699 819 008 B. Both
  captured; the record must name the cgroup it quotes (parent vs child), or two
  honest readers will disagree.

## 4. Fill rules — what the record must be able to state on landing

**(a) The fifth plane in the gate.** Ink the realized revision: new md5 + line
count of `tools/tsukuroi-census.sh`; the five-emitter block and the rollup with
`update-safety` in the verdict parentheses; the verbatim `PLANE update-safety:`
note line from an **executed** live run (the plan's proposal carries
`classes=offline-exile:<n>,aur-local:<m>` (+ `unknown-provenance` names when the
packages arm reports `new`; `unavailable` when the baseline is absent/unreadable
→ DEGRADED — the realized spelling is quoted, never this proposal). The arm
word (PASS · INERT · REQUIRES-PREP · BLOCKED · UNKNOWN-UPSTREAM · DO-NOT;
composition `BLOCKED > UNKNOWN-UPSTREAM > REQUIRES-PREP > INERT > PASS`) is
carried in the note line. The gate-verdict mapping is **recorded, not silently
applied** — the record states either the proposed mapping
(INERT/PASS→HEALTHY, REQUIRES-PREP/UNKNOWN-UPSTREAM→DEGRADED, BLOCKED→BLOCKED,
DO-NOT stays note content) or the realized one, and which one was implemented.

- Probes, all already-exercised read-only verbs: `-Qu` rc/emptiness (unreadable
  → BLOCKED, never a pass); `-Sup --print-format` count (candidates>0 →
  REQUIRES-PREP with count and names); db births (`stat -c %w`); `offline.db`
  presence/inertness; bounded `pacman.log` tail for the last refresh/upgrade
  commands (birth authoritative; a log-window miss → `command=unknown` row,
  verdict unaffected). Pins/holds stay in the packages plane — no double-probe;
  the new plane *references* that reading (verify no duplicated `IgnorePkg` /
  `HoldPkg` probe in the diff).
- Fixtures: ≥3 for the round-6 debt (baseline hit / new / version-drift) **plus**
  the four round-7 cases (inert-clean 5-plane rollup, candidates>0→
  REQUIRES-PREP, `-Qu` unreadable→BLOCKED, baseline absent→DEGRADED-never-
  HEALTHY). The record quotes the executed `PASS (35+N cases, N≥4)` line and
  **attributes** which cases are round-6 debt vs round-7 — no conflation. If the
  debt is carried instead, N counts only round-7 cases and the debt is named
  again.
- Fail-closed receipts: fixture byte-unchanged assertion; `git status
  --short` byte-identical before/after the live run; no `db.lck` created; no
  `-Sy`/`-Syu`/install/remove/restart verb anywhere in the diff or the run log.

**(b) The v2 decision note.** Name as landed (plan's draft name
`corpus/knowledge/update-safety-plane.md`; assignment wins — quote the realized
path). Content the record must spot-check: the class × update-path truth table
(offline-exile → `-Syu` reach none; aur-local → out-of-band via yay;
unknown-provenance → the register's probe order, never a guessed class) using
the **landed register's** action vocabulary — note the round-7 plan cites
`plans/round-6-record-draft.md:305-307`'s proposed vocabulary
(accept-and-recheck · freeze/pin decision · replace-from-channel · remove ·
route-out), while the realized register phrases per-class actions in prose in
`aur-risk-plane.md:212-221` (preserve/re-test; diff-then-build; probes). The
note must cite the landed wording, tagged, not the superseded proposal. Plus:
re-measured round-2 pins, refreshed U1–U8 status, hazard rows (rollback net =
`snapper list-configs` empty; dkms stale registration; cache size — full `du`
stays in the checklist, never in the gate's latency budget), and the
**append-only** one-line errata pointer added to `update-safety-note.md` (its
pins stay).

**(c) Non-author verification.** ≥3 note rows re-executed by the verifier seat
against live probes, with the verifier's own commands (round-6 precedent:
`aur-risk-plane-ver-s6.md`, CONFIRMED 2/2). The record quotes the verdict and the
rows chosen; a refutation is recorded, not smoothed.

## 5. Record skeleton (what the `LOG.md` entry must carry on landing)

Keep a compact multi-line bullet (round-3 shape; rounds 4–6 used one-liners —
only admissible if the entry still names artifacts + verifiers + axes; the
round-7 measure is finer than one line can carry).

- **Work (observed in tree):** `⟨artifact list: path, seat/ID, md5, lines,
  mtime⟩` — expected members: the census revision (new md5 + case count), the v2
  note, the baseline file (if the debt lands), the SKILL round-7 append, the
  round-2 note's errata pointer, plus scribe-owned README/SCORECARD/LOG.
- **Scribe re-verification:** §6 command set; quote the selftest line, the
  live 5-plane rollup, one verbatim `PLANE update-safety:` note, and ≥3 note rows
  re-executed (with the non-author's rows named separately).
- **Ancillary scribe writes (owed at record time):**
  - `SCORECARD.md` round-7 move-log row (axes: operability — confirm against
    `AXES.md` vocabulary before writing), Before/After: before = 4-plane gate,
    update-safety note-only; after = 5-plane gate.
  - `corpus/README.md` coverage rows — **collapsed debt since round 3**
    [observed: `git log --oneline -- corpus/README.md` last touched `9bcd162`
    (round 3); the map has no rows for `boot-plane.md`, `degraded-triage-r4.md`,
    `timer-drift-plane.md`, `aur-risk-plane.md`, `foreign-provenance-r6.md`,
    `aur-risk-plane-ver-s6.md`, `oom-event-plane.md`, the round-4/5/6 census
    revisions, or round 7]. Land the back-rows or state the debt stays open —
    never silently skip.
  - `SKILL.md` round-7 append (5-plane contract, arm word semantics, mapping,
    case-count sync). **Count restatements elsewhere must move in the same
    round if the gate count changes** — the round-6 append explicitly left
    `:470`, `:519-521`, `:600-602`, `:686-688` (and the `:831` note) as history
    because the gate did not change; a round-7 gate revision void that deferral.
  - Form defect to correct with evidence: `SCORECARD.md:16` (round-4 row) is
    still malformed — an unescaped `|` truncates the After cell to
    `boot plane (299 L` [observed 18:21Z].
- **SHONEN boxes:** stay `[~]` (asserted with verifier names, `SHONEN.md`); the
  round-7 record may refresh evidence pointers but must not upgrade to `[x]` —
  that stays with the non-author promotion review.
- **State at entry:** the round commit hash landed, or "round work uncommitted in
  tree" + exact `git status --short`; the scribe writes only its named files;
  the commit carries the lane identity.
- **Candidate entry skeleton (fill at landing):** `round 7 (training r6):
  update-safety joins the gate — 5-plane census (selftest 35→35+N; N≥4: 5-plane
  rollup / candidates>0→REQUIRES-PREP / -Qu unreadable→BLOCKED / baseline
  absent→DEGRADED) + `⟨baseline file⟩`(`⟨md5⟩`, round-6 debt finished|carried) +
  v2 decision note `⟨path⟩` (class × update-path table) + round-2 note errata
  pointer. Axis: operability. Verifiers: ⟨names⟩.`

## 6. Scribe re-run set (receipts owed by the record)

```bash
cd ~/Projects/shokunin/tsukuroi-shokunin
bash tools/tsukuroi-census.sh --selftest            # expect rc=0, 35+N/35+N PASS
bash tools/tsukuroi-census.sh                       # expect rc=1(frame), 5-plane rollup + PLANE update-safety:
md5sum tools/tsukuroi-census.sh; wc -l tools/tsukuroi-census.sh   # landed revision vs e9327046…
pacman -Qu; echo "rc=$?"                            # unpiped; expect rc=1, 0 lines
pacman -Sup --print-format '%n %v'; echo "rc=$?"    # expect rc=0, 0 lines; no db.lck after
stat -c '%w | %y | %n' /var/lib/pacman/sync/*.db    # births, not mtimes
pacman -Qm | wc -l; pacman -Qm                      # 16, name+version
pacman-conf IgnorePkg IgnoreGroup; pacman-conf HoldPkg
grep -nE "\-Sy |\-Syu |synchronizing|full system upgrade" /var/log/pacman.log | tail -8
yay --version                                       # read-only; no yay verb beyond this
git status --short                                  # zero-mutation receipt (before/after)
# + per-round-7: re-execute >=3 rows of the v2 note's tables against live probes
# + baseline file md5/lines + its selftest fixtures read from the executed run
```

Pipeline-rc rule restated: never carry a piped rc as a measurement (`| head`,
`| wc -l`); `-Qu`'s rc is only meaningful unpiped.

## 7. Unknowns register (draft-time; owners)

1. Does the round-6 baseline/census debt land inside round 7 or get carried
   again? (owner: round-7 arm seat; answered by Step 0 + the landed diff, never
   by this draft).
2. Baseline path/format/env-override name and the realized `foreign=` note shape
   (owner: arm seat; the record quotes the realized values). At draft time the
   path does not exist, so "resolve from the round-6 record" resolves to the
   register's §8 spec `aur-risk-plane.md:314-329` + the plan's proposal
   `corpus/knowledge/aur-risk-plane.tsv` — land it, then quote it.
3. Realized arm word + gate mapping in the landed note (plan proposes; the
   record states the realized one — the two must not be conflated).
4. Realized name of the v2 note (owner: note seat; plan's draft
   `update-safety-plane.md`).
5. Whether the four round-7 cases plus the debt fixtures are exactly 4+3 = 7 new
   cases, or more; only the executed count line decides (owner: arm seat).
6. `pacman.log` rotation window at dispatch: whether the last refresh event is
   still retained (`:1405` today); the arm's `command=unknown` row is built for
   the miss (owner: arm seat).
7. The note's hazard-row owners unchanged from round 2/3: `snapper
   list-configs` empty, dkms stale `7.1.4` registration, cache size (owner:
   note seat; reported, never remediated).
8. Whether the note cites the round-6 draft's proposed action vocabulary or the
   landed register's prose actions (owner: note seat + record scribe; cite the
   landed one, tag the other as superseded proposal).
9. Carried rounds 1–6, unchanged: root `-Qkk` delta; `1password-beta`
   provenance (operator); `walker-restart.hook` (kagi/operator);
   `omarchy-walker`↔`walker` linkage (out of province → kaidoku/revenger);
   `offline.db` coverage debt; `corpus/README.md` collapsed rows + the
   malformed `SCORECARD.md:16` row; the "20-min cap" item (owner: integrator).
10. Candidate B (OOM-plane watch) anchors for a future draft are recorded in
    `plans/round-7.plan.md:140-147` and the landed `oom-event-plane.md`; whether
    it is the next round's move is an integrator/operator call, not this
    draft's.

## 8. Errata / pending (append-only)

- 2026-10-14 — this draft file created by SCR-S7; it is prep, not a record. The
  `LOG.md` round-7 entry remains owed (`AGENTS.md:3`); measures are judged
  against the landed census revision + note + baseline, not this skeleton.
- 2026-10-14 — all counts in §3 are captures on a live host (journal `err`
  432→433 in 43 min; coredump storm live); re-run, never quote.
- 2026-10-14 — Step 0 result recorded above: round 6's **baseline + census
  delta is the one unlanded member** of its own measure, self-tagged by the
  register (§8 "written, not implemented", `SKILL.md:760-771`). This draft does
  not re-design it; it names it as the round-7 first task per
  `plans/round-7.plan.md:96-101`.
- 2026-10-14 — pin nuance: the plan's memcg `memory.peak` value is the
  `user-1000.slice` figure; the parent `user.slice` differs by 7 728 B. Quote
  the cgroup path with the value.
- 2026-10-14 — the round is concurrent: sibling round-7 scratch dirs observed
  shape-only at 15:21Z (`/tmp/w7-s73-tsukuroi/`, `/tmp/w7-tsukuroi-s74/`,
  `/tmp/w7-tsukuroi-vers7/`); no round-7 artifact had landed and the tree was
  clean at 18:20Z. The record scribe fills every generic slot with actual
  filenames, md5s and executed lines at entry.
- 2026-10-14 18:24Z — **post-freeze tree movement (append-only)**: the arm seat's
  round-6-debt landing entered the working tree as `M tools/tsukuroi-census.sh`
  (three hashes 6 s apart; 1134→1136 lines; uncommitted, still moving). The
  draft-time readings above are kept as the freeze-time state; nothing was
  re-measured against the moving revision, and no pin in this file describes it.
  If the final landed revision differs in shape (embedded snapshot vs external
  baseline file, 4-plane vs 5-plane), the record states the landed shape — this
  errata line is why the draft did not claim one.
- 2026-10-14 — final-file spot-check and this file's own line count/md5 are
  reported in the seat's handoff, not in-file (a further edit would invalidate
  them).