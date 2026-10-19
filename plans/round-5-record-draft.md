# Round-5 record — DRAFT (scribe prep, seat SCR-S5)

Status: **draft, pre-landing.** This file is the scribe's working skeleton for the
round-5 `LOG.md` entry and for the round's two artifact families (mutation sweep +
timer-drift plane). It is not the record; the record is the append-only `LOG.md`
entry the round's scribe writes after every round-5 artifact has landed
(`AGENTS.md:3`). Every number below is a draft-time capture with its command and
time; the round keeps moving (a live coredump storm, a 5-minute timer), so
re-run, never quote.

Draft seat: SCR-S5. Draft window: 2026-10-14 17:01:34–17:05:30Z (14:01–14:05
-03), host `plazir27`, user `vgpnk` (non-root). Write scope: this file only.
Scratch: `/tmp/w5-tsukuroi-scr-s/` (ephemeral; selftest leftovers checked = none).
All probes read-only; no install/upgrade/remove/restart verb was run
(`PROVINCE.md:16-17`). `mutate-and-run.sh` was **not executed** by this seat —
only read (shape + version + md5).

Tags used throughout: [observed] = measured now, command named; [inference] =
join from measurements; [unknown] = named gap with owner.

## 1. Plan anchor and the round's measure

`plans/round-5.plan.md` (md5 `0e9e8640e8c6b1d2fd116d05c5acf19b`, 720 B, 11
lines, mtime 2026-10-14 13:59):

> Axis move: adjacency (consume a sibling's craft) + freshness.
> Claim: (a) tameshi's mutate-and-run.sh is applied to tsukuroi's OWN census
> gate (read-only on the tool; copies in /tmp) — the lane measures its own
> suite's kill-rate and hardens whatever survives (new selftest cases land in
> the same round); (b) the timer-drift plane: enabled timers' last-run vs
> next-run vs wall-clock drift measured and classified.
> Anti-claim: mutate-and-run doesn't fit bash — record the fit gap and run
> the mutation manually per tameshi's published recipe (the adjacency claim
> is about the METHOD, not the tool).
> Measure: own-gate kill-rate + hardening commits; drift-class table.

**Plan-revision note [observed 17:0xZ].** The plan file itself carries two
revisions. Committed HEAD (`165307f`) holds a 142-line mutation-centric plan
(md5 `2858d36de9b5e388cda61d42ebc22dff`): it pre-registers the defect classes,
names the sweep case note `corpus/knowledge/mutation-case-tsukuroi-census.md`,
pins the target census at sha256 `084951be…78c5` (= HEAD bytes) and the runner
at sha256 `597e1419…331b` (42291 B, r4-2), and records timer-drift as
*deferred* (`:45`). The worktree's 11-line revision quoted above (md5
`0e9e8640…`, mtime 13:59) folds drift in as claim (b) — this is the dispatch
plan the lanes read. The record must state which revision it judged each claim
against and must not merge the two.

Interpretation to check when the artifacts land:

- **(a) own-gate kill-rate + hardening.** The sweep artifact must carry the
  tool's executed verdict lines (control, per-defect verdicts, `MUTATE: DONE`
  headline with `killed/survived/inconclusive/kill-rate`), tied to a pinned
  revision of `tools/tsukuroi-census.sh`; the hardening must land **in the
  same round** as new selftest cases, and the record quotes the executed
  post-hardening count line (`TSUKUROI_CENSUS_SELFTEST: PASS (26+N cases, …)`).
  Two revisions are named, never conflated: *swept* (what the table measures)
  and *hardened* (what lands).
- **(b) drift-class table.** One row per measured timer carrying last-run,
  next-run, wall-clock capture, and a class; the record states the **selector
  actually realized** (see §3 — "enabled" is ambiguous on this host).
- **Anti-claim / fit check [observed at draft time].** The tool's suite
  contract is `bash -c CMD` with `$MUTANT` = the artifact under test, exit 0 =
  green, non-zero = red, 124/126/127 = inconclusive (tool header, r4-2). The
  census gate's hermetic `--selftest` prints its own case count and an rc 0/1
  verdict — so the contract *fits* `--suite 'bash "$MUTANT" --selftest'`; the
  fallback (manual recipe, `tameshi-shokunin/SKILL.md:131-244`, steps 1–10 +
  defect catalog) was therefore not obviously triggered. The lane owns that
  call; whichever path is taken, the record carries the justification and the
  executed lines. The adjacency claim is about the METHOD (plan), not the tool.
- **Cross-lane note (read-only, sibling tree).** tameshi's own round-5 plan
  (`tameshi-shokunin/plans/round-5.plan.md`, 12 lines) states it sweeps
  **this same gate** as its third cross-author case ("third gate from a
  DIFFERENT author and style — tsukuroi-shokunin/tools/tsukuroi-census.sh …
  8-10 fresh mutants"). Two independent sweeps of one artifact may therefore
  exist in two corpora. The tsukuroi record reports tsukuroi's **own** sweep;
  tameshi's is cited only as cross-reference if it lands — never merged,
  never absorbed (out-of-province → report). Ordering discipline for the
  shared artifact: both sweep pins must cite committed bytes; tsukuroi's
  hardening edit lands after its sweep pin, and both shas go in the record.

## 2. Draft-time baseline receipts (measured by this seat)

Gate, re-run 2026-10-14 (raw captures in `/tmp/w5-tsukuroi-scr-s/`):

```bash
bash tools/tsukuroi-census.sh --selftest   # 17:02:01Z, rc=0
bash tools/tsukuroi-census.sh              # 17:02:02Z, rc=1
```

Selftest last line verbatim: `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26
passed, 0 failed)`. Gate file md5 unchanged from the round-3 pin:
`41953ee9f2099281c91759249fe8708f`, 976 lines — all deltas below are host
state, not gate drift [observed].

Live run verbatim (17:02:02Z):

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T17:02:02Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16; pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=427 (coredump=264 kernel=139 other=24); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

Delta table vs the round-4 draft's captures (same boot
`d7f0bc8d938e4249b4a1f250cbfacf58`, boots=13 still):

| capture | err | coredump | kernel | kerr (io/other) | failedhist | timer_drift |
|---|---|---|---|---|---|---|
| round-4 draft, 16:20:04Z | 405 | 244 | 137 | 137 (70/66) | 8 | 0 |
| **this draft, 17:02:02Z** | **427** | **264** | **139** | **139 (70/68)** | **8** | **0** |

Arithmetic checks [observed]: 405→427 = +22 (coredump +20, kernel +2); kerr
+2 = other 66→68; `io=70` unchanged since 16:20 (the sr0 burst did not repeat
in this window). The coredump storm is live; every value is a capture.

Artifact md5s at draft time (17:03Z, scratch `md5-full.out`):

| artifact | md5 | lines |
|---|---|---|
| `tools/tsukuroi-census.sh` (sweep target) | `41953ee9f2099281c91759249fe8708f` | 976 |
| `SKILL.md` | `63b0900e8f3a5d850a035cef94c03ce0` | 543 |
| `PROVINCE.md` | `f1722b163a5c433b003de362ab93ee11` | — (971 B) |
| `LOG.md` / `SCORECARD.md` / `SHONEN.md` | `d0b2eb2d…` / `728e614d…` / `9cf1d450…` | 167 / 16 / 51 |
| `MINT.md` / `corpus/README.md` | `1d75fce9…` / `98bd0066…` | 20 / 20 |
| `corpus/knowledge/boot-plane.md` (r4) | `e722b7a931858aa5ff1a89ce91cccca9` | 312 |
| `corpus/knowledge/degraded-triage-r4.md` (r4) | `d57ae2d48e01777e1ef3c8c0ffb642c9` | 607 |
| `corpus/knowledge/host-health-report-r3.md` | `98a0f263f801245f6069e57a9f72d4af` | 563 |
| `corpus/knowledge/journal-boot-plane.md` | `e5ca40dafc4d1d2a2158fded39067df6` | 430 |
| `corpus/knowledge/package-state-plane.md` | `ef93f1b78b6a9e17e8c9d096e7852a02` | 323 |
| `corpus/knowledge/systemd-user-plane.md` | `af07a829cfd0307fbe970a2cdc054e18` | 265 |
| `corpus/knowledge/driver-firmware-plane.md` | `518eda8f0f39f25ee95c715571a9cf95` | 256 |
| `corpus/knowledge/update-safety-note.md` | `5cc3067fec33d261d8bff6a5c7e8ac48` | 478 |
| `corpus/knowledge/executor-test-sufficiency.md` | `4b2c1d3612db7db1477da92aaec39862` | 219 |
| `plans/round-5.plan.md` | `0e9e8640e8c6b1d2fd116d05c5acf19b` | 11 |

Sibling tool pin (read-only; for the adjacency): `tameshi-shokunin/tools/
mutate-and-run.sh` md5 `26a27d352690e64b2396a4aabaf4ddf6`, 1001 lines, version
string `mutate-and-run.sh r4-2 (tameshi-shokunin, 2026-10-14)`. Its default
scratch is `/tmp/tameshi-r4-2-run.XXXXXX` — a tsukuroi sweep lane should pass
`--workdir` under its own `/tmp/w5-…` scratch to honor lane naming.

Repo state at 17:03Z (draft entry captures): HEAD `165307f` (probation round 4);
`git status --short` = ` M plans/round-5.plan.md` only. **Erratum — repo/gate
capture drift while drafting [observed 17:07:2xZ]:** between 17:02:01Z (the
baseline receipt above: worktree = HEAD bytes, md5 `41953ee9…`, 976 lines,
26/26) and 17:06:23Z (mtime) the round's hardening edit landed **uncommitted**
(`git diff --numstat tools/tsukuroi-census.sh` = +56/−0; ` M
tools/tsukuroi-census.sh`). At 17:07:2xZ the worktree gate is md5
`e9327046b05b5c71e07fe511ad7e82dd`, 1032 lines, selftest **`PASS (35 cases,
35 passed, 0 failed)`**, live run unchanged in its five plane lines (rc=1,
same counts as 17:02:02Z). The nine added case labels (from the diff):
`blocked-empty-pkgdb`, `healthy-nonroot-artifact`, `healthy-sample-bound`,
`degraded-timer-unknown`, `degraded-scope`, `blocked-no-node`,
`degraded-kerr-classes`, `blocked-pci-unreadable`, `degraded-jrn-timer-plane`.
This makes the two-revision discipline (§1, §4) concrete: swept-pin candidate =
committed HEAD bytes `41953ee9…` (976 lines, 26 cases); hardened worktree
revision = `e9327046…` (1032 lines, 35 cases) — if the sweep pins uncommitted
bytes, recipe step 2's stop must be addressed explicitly. Also new in the
worktree (not this seat's writes): `?? plans/round-6.plan.md` (mtime 17:05:40Z).
Re-pin everything at record time.

## 3. Timer inventory at draft time (drift-plane baseline)

**Selector realization [observed] — the record must state its selector, because
"enabled timers" is ambiguous on this host:**

| scope | `list-unit-files --type=timer --state=enabled` | `list-timers --all` | note |
|---|---|---|---|
| user | 1 row: `ai-usage.timer enabled enabled` | 1 row | the census gate's arm reads exactly this selector |
| user (all states) | — | — | 3 unit files: `ai-usage.timer` enabled; `omarchy-battery-monitor.timer`, `systemd-tmpfiles-clean.timer` disabled |
| system | **0 rows** | 5 rows | 4 `static` + `man-db.timer` `disabled`; all active via vendor/static enablement — the round-3 note's vendor-wants nuance (`journal-boot-plane.md` §6) |

So: literal `UnitFileState=enabled` yields **1** timer (user scope, the gate's
arm); the meaningful measured set is the **5 active system timers** from the
round-3 §6 table plus the one user timer. Proposed plane scope (final call:
drift lane): user-scope enabled ∪ system-scope active-with-next.

**User-scope verbose capture, `ai-usage.timer` (17:02:11Z):**

```
NEXT LEFT LAST                         PASSED UNIT           ACTIVATES
-       - Wed 2026-10-14 14:02:11 -03 1ms ago ai-usage.timer ai-usage.service
```

unit file (`systemctl --user cat ai-usage.timer`) verbatim:

```
[Unit]
Description=Refresh AI usage cache every 5 minutes

[Timer]
OnBootSec=30
OnActiveSec=15
OnUnitActiveSec=300
Persistent=true
AccuracySec=10
Unit=ai-usage.service

[Install]
WantedBy=timers.target
```

`show` subset verbatim (17:02:1xZ): `ActiveState=active SubState=waiting
Result=success`; `LastTriggerUSec=Wed 2026-10-14 14:02:11 -03`;
`LastTriggerUSecMonotonic=1d 3h 4min 12.373808s`; `NextElapseUSecRealtime=`
(empty); `NextElapseUSecMonotonic=1d 3h 9min 12.374592s`; three
`TimersMonotonic` entries (`OnUnitActiveUSec=5min → next_elapse=1d 3h 9min
12.374592s`; `OnActiveUSec=15s → 1d 2h 13min 23.500417s`; `OnBootUSec=30s →
30s`).

Arithmetic checks [observed]: last-trigger + 5 min = `1d 3h 9min 12.373808s`
vs `NextElapseUSecMonotonic` `1d 3h 9min 12.374592s` → Δ = 0.784 ms; the live
next elapse is the `OnUnitActiveUSec` arm. `list-timers` shows `NEXT -` because
`NextElapseUSecRealtime` is empty [inference from the two captures; record the
systemd version for this faithfulness].

**Cadence evidence (draft capture; journal since 2026-10-13 11:00):** 317
`Starting Probe AI CLI usage limits into cache...` lines; deltas between
consecutive starts (n = 316): `300:11, 301:26, 302:13, 303:12, 304:11,
305:13, 306:10, 307:7, 308:7, 309:6, 310:199`, plus **one 277 s outlier** at
13:06:46 → 13:11:23 [observed] whose manager PID changes `systemd[1573] →
systemd[1203171]` — that is the round-4 E1 session restart (OOM, 13:10:59),
re-arming the timer, not an early fire [inference]. [inference, unproven] the
`300…310` spread is lateness within `AccuracySec=10` with a mass at the +10 s
edge; the drift lane classifies, the draft does not.

Journal receipts for the last two runs (verbatim timestamps):
`13:57:14` Finished → `14:02:11` Starting → `14:02:13` Finished; the 14:02 run
consumed `1.994s CPU time over 2.524s wall clock time`.

**Clock anchors [observed]:** `uptime -s` = `2026-10-13 10:57:58`; boot 0's
first record = monotonic `[244.159301]` @ `2026-10-13T11:02:03-03`; `/proc/
uptime` = `97493.55` at ~17:02:51Z. `LastTriggerUSecMonotonic` 97452.37 s vs
wall since `uptime -s` = 97453 s → Δ ≈ 0.6 s: the two clocks agree; consistent
with `journal-boot-plane.md` §5.3 (kernel phase = first-record monotonic −
0.81…0.84 s). Useful as a clock-anchoring receipt; confirm or drop at record
time.

**System-scope rows verbatim (`systemctl list-timers --all`, 17:04:29Z):**

```
Thu 2026-10-15 00:00:00 -03     9h Wed 2026-10-14 00:00:13 -03      14h ago shadow.timer                     shadow.service
Thu 2026-10-15 00:40:30 -03    10h Wed 2026-10-14 00:34:38 -03      13h ago plocate-updatedb.timer           plocate-updatedb.service
Thu 2026-10-15 09:50:40 -03    19h Wed 2026-10-14 03:50:48 -03      10h ago man-db.timer                     man-db.service
Thu 2026-10-15 11:13:22 -03    21h Wed 2026-10-14 11:13:22 -03 2h 51min ago systemd-tmpfiles-clean.timer     systemd-tmpfiles-clean.service
Sat 2026-10-17 04:18:20 -03 2 days Sat 2026-10-10 03:53:00 -03            - archlinux-keyring-wkd-sync.timer archlinux-keyring-wkd-sync.service
```

These match the round-3 §6 set (5 timers, all `success` then); NEXT/LEFT have
advanced normally in the ~5.5 h since that capture [observed]. All LASTs still
sit inside their declared randomization/accuracy windows per the round-3 note
— re-verify per timer with `show` at record time, do not inherit.

**`list-timers` quirks to keep in the record (measured, not theory):**
`NEXT`/`LEFT` print `-` for monotonic-only timers (ai-usage.timer); `PASSED`
prints `-` when LAST predates the current boot (keyring timer); `PASSED` can
race the capture (`1ms ago` above — the timer fired in the capture second).

**Drift-class table skeleton (fill on landing).** Columns: scope/unit |
selector source | declared cadence (unit file, lines) | LAST | NEXT | wall-clock
capture | nominal vs actual interval | drift | class | receipts (`show` props +
last two journal runs) | status. Class vocabulary **proposal** (final: drift
lane; record states the vocabulary actually used): `ON-WINDOW` ·
`LATE-IN-WINDOW` · `OUT-OF-WINDOW` (missed/overdue: a nominal fire with no run,
or next elapse in the past) · `UNARMED` (enabled but `ActiveState≠active` — the
gate's existing arm) · `MONOTONIC-ONLY` (realtime elapse empty, NEXT `-`) ·
`UNKNOWN-UNREADABLE` (fail-closed). Fill rule: no class without a receipt; each
cell a capture with time.

## 4. Mutation sweep skeleton (fill rule)

The sweep's executed receipt lines the record must quote (from tool r4-2
verdict grammar): `CONTROL: GREEN (exit=… pristine-sha256=…)`; one
`DEFECT <id>: KILLED|SURVIVED|INCONCLUSIVE` per defect; `MUTATE_RESTORE: OK`;
`MUTATE: DONE|DEGRADED (… defects=… killed=… survived=… inconclusive=…
kill-rate=…%)`. Adjudication: killed = suite red **and** full case count still
enumerated (exit-only is insufficient); survived = green at the same count — a
finding, never a footnote; inconclusive excluded from the rate and named beside
it; `kill-rate = killed/(killed+survived)`. Bands (tameshi's stated band,
`SKILL.md:127-133`) are a report convention, not a gate.

Two-revision discipline (see §1): the table is tied to the **swept** revision
of `tools/tsukuroi-census.sh`; the **sweep pin must be committed bytes**
(recipe step 2), sha256 + md5 + lines recorded; the hardening lands after, and
the hardening ledger maps each survivor → new selftest case label → the line it
was added at. The post-hardening selftest count is quoted from an executed run.
If a survivor is judged equivalent code (no observable input differs), that is
a calibration item, not a gap (recipe step 8).

**Prior evidence the sweep lane inherits [observed in the committed plan].**
The committed plan's "Planning probe (PREP-S5, 2026-10-14 — not the round-5
sweep)" section records three probe defects run with this runner and suite:
P1 exit-map KILLED (9 failing cases), P2 rollup seed KILLED (5 failing cases),
P3 sample default (`TSUKUROI_SAMPLE_N:-8` → `:-4`) **SURVIVED** 26/26 —
kill-rate 67 %, `MUTATE_RESTORE: OK` — and names P3's strengthening ("a fixture
with ≥5 candidate packages and the altered one beyond position 4, run at the
default, asserting drift is detected"). The 17:06Z hardening added a
`healthy-sample-bound` case [observed label; whether it pins P3's exact
mechanism is to be verified at landing]. The round's sweep must run fresh runs
— the probe is prior evidence, never the round's table.

**Arm map for the class column (draft-time line anchors, v2 976 lines):**
helpers `:189-246` (`worse()` `:209`); packages `:248-330`; systemd-user
`:331-395` (timer arms `:365-393`); drivers `:397-509`; journal/boot
`:510-627` (failedhist `:590`, timer drift `:594-620`); hermetic selftest
`:628-919` (26 `check` calls `:792-913`; fixture dispatcher `:635-690`;
harness counters/summary `:692-694, :915-917`); main/rollup/exit `:921-976`.
The class vocabulary may reuse tameshi's arm-class matrix classes A–G
(`tameshi-shokunin/corpus/knowledge/arm-class-matrix.md`: verdict paths,
fail-closed arms, counts, reported-but-unasserted surfaces, unreached arms,
coordinated edits, behavior predicates) for cross-author comparability;
amendments are wins and must be recorded, not smoothed (their matrix rule).

**Hardening ledger skeleton:** survivor id | site (swept revision line) | why
the suite missed it | new case label | new `check()` line | executed count
after. Same-round landing is the round's term (`round-5.plan.md`); the record
holds the ledger.

## 5. Record skeleton (what the `LOG.md` entry must carry on landing)

Fill on landing; keep the round-3/4 scribe shape (single append-only bullet,
`LOG.md:83-166`, `:167`).

**Work (observed in tree).** `⟨artifact list: path, seat/ID, md5, lines,
mtime⟩` — expected: the mutation sweep note; the hardened
`tools/tsukuroi-census.sh` (new md5, 26+N cases); the drift-plane artifact
(note or table; name as landed); plus SKILL/coverage/move-log updates. Hash
every artifact at entry; do not quote stale md5s (the live storm drifts in
seconds; the report changed under the round-4 scribe once — that precedent is
recorded, `host-health-report-r3.md:408-412`).

**Scribe re-verification (re-executed, read-only).** §6 command set; quote the
selftest line, the live line, the sweep's executed headline (re-run if the
scratch evidence survives, otherwise spot-re-run one defect), and the drift
caveat.

**Ancillary scribe writes (owed at record time):**
- `SCORECARD.md` move-log row for round 5 (axes adjacency + freshness —
  confirm against `AXES.md` vocabulary).
- `corpus/README.md` coverage rows: the map at draft time still ends at round
  3 — round-4 rows for `boot-plane.md` and `degraded-triage-r4.md` are
  **missing** [observed: `git log -- corpus/README.md` last touched
  `9bcd162`, round 3], plus rows for the round-5 artifacts.
- `SKILL.md` sync: the hardening has *already* changed the selftest count in
  the worktree (26 → 35 by 17:07Z, §2 erratum) while `SKILL.md`'s census-v2 row
  still documents 26 — re-grep and land the sync with the record; a stale count
  is an executor-sufficiency finding, not a footnote.
- form defect to correct with evidence, not silently: `SCORECARD.md:16` (the
  round-4 row) is malformed at draft time — an unescaped `|` truncates the
  After cell to `boot plane (299 L`.

**SHONEN boxes.** At draft time all four remain `[~]` asserted with round-3
verifier names; the promotion review (non-author `[x]`) is still owed. The
round-5 record may refresh evidence pointers but must not upgrade boxes itself.

**State at entry.** Commit landed for the round (hash), or "round work
uncommitted in tree" with the exact `git status --short`; the record is written
by the scribe seat, which writes only its named files; commit carries the lane
identity.

**Open (carried + new).** Carried from rounds 1–4: root `-Qkk` delta;
`offline.db` coverage; round-2 wave-1 errata merge into SKILL round-1 blocks;
v1 census md5-prefix transcription candidate; literal `source:`/`verified-at:`/
`recheck:` keys; `corpus/lessons/round-1.md`; "20-min cap" resolution (owner:
integrator); E1 kernel-detail gap; E2 generator-collision masking question; E3
sr0 media check; E5 USB-audio/pipewire cluster. New, from this draft: sweep-pin
ordering; two-author sweeps of one artifact; drift selector realization; 310 s
mass mechanism; NEXT `-` semantics vs systemd version.

## 6. Scribe re-run set (receipts owed by the record)

```bash
cd ~/Projects/shokunin/tsukuroi-shokunin
bash tools/tsukuroi-census.sh --selftest           # expect rc=0, 26+N/26+N PASS
bash tools/tsukuroi-census.sh                      # expect rc=1, DEGRADED rollup
md5sum tools/tsukuroi-census.sh                    # vs swept + hardened pins
sha256sum tools/tsukuroi-census.sh                 # the sweep table's pin
md5sum ../tameshi-shokunin/tools/mutate-and-run.sh # adjacency pin (r4-2)
systemctl --user list-timers --all --no-pager      # user scope: LAST/NEXT/LEFT
systemctl --user list-unit-files --type=timer --state=enabled --no-legend --no-pager
systemctl --user show ai-usage.timer -p ActiveState -p SubState -p Result \
  -p LastTriggerUSec -p LastTriggerUSecMonotonic -p NextElapseUSecRealtime \
  -p NextElapseUSecMonotonic -p TimersMonotonic -p AccuracyUSec --no-pager
journalctl --user -u ai-usage.service -o short-iso --no-pager --since '<boot>' \
  | grep -c 'Starting'                             # cadence capture (drifts: time it)
systemctl list-timers --all --no-pager             # system scope: 5 rows expected
for t in shadow.timer plocate-updatedb.timer man-db.timer \
         systemd-tmpfiles-clean.timer archlinux-keyring-wkd-sync.timer; do
  systemctl show "$t" -p ActiveState -p Result -p LastTriggerUSec \
    -p NextElapseUSecRealtime -p NextElapseUSecMonotonic --no-pager; done
systemd --version | head -n1                       # NEXT '-' semantics context
journalctl -b -p err -o json --no-pager | wc -l    # storm drift, capture time it
git status --short                                 # zero-mutation receipt
```

## 7. Unknowns register (draft-time; owners)

1. Sweep-pin ordering: which revision the kill table is tied to, and whether
   tsukuroi's hardening landed before/after tameshi's sweep of the same gate —
   both artifacts must name their shas (owners: mutation lane / integrator).
2. Two-author sweeps of one artifact: cross-reference policy so the corpus
   does not present two tables for one file as one measurement (owner:
   integrator / record scribe).
3. Drift selector: which realization the round's table uses ("enabled" liter
   = 1 user timer; active system set = 5) — must be stated, not implied
   (owner: drift lane).
4. `ai-usage.timer` +310 s mass: coalescing-at-accuracy-edge hypothesis,
   unproven; also why no delta exceeds +10 s (owner: drift lane).
5. `list-timers` `NEXT -` for monotonic-only timers: systemd-version behavior
   — the record should pin `systemd --version` beside the quirk (owner: drift
   lane).
6. Post-restart re-arm: which activation the new manager used for
   `OnUnitActiveSec` after the E1 restart (277 s outlier), and whether
   `OnBootSec`/`OnActiveSec` re-armed across the manager restart (owner: drift
   lane).
7. Hardening changes the SKILL-pinned selftest count (26) — SKILL sync owed
   in the same round (owner: record scribe / mutation lane).
8. Round-4 coverage/scorebook debt: `corpus/README.md` lacks round-4 rows;
   `SCORECARD.md:16` row is malformed (owner: record scribe).
9. Round-3/4 register items still open (root `-Qkk`, crypttab, `/boot`,
   elephant provenance, upstream delta, dwell mechanism; E1–E5) — unchanged.

## 8. Errata / pending (append-only)

- 2026-10-14 — this draft file created by SCR-S5; it is prep, not a record.
  The `LOG.md` round-5 entry remains owed (`AGENTS.md:3`); the record's
  measures are judged against the landed sweep note + hardened gate and the
  landed drift artifact, not against this skeleton.
- 2026-10-14 — counts in §2/§3 are captures in a live storm and a live timer;
  re-run, never quote (drift precedent: `host-health-report-r3.md:441-462`).
- 2026-10-14 — the round is concurrent: sibling lanes will land the artifacts
  named generically in §5; the record scribe fills the slots with the actual
  filenames, md5s and measured lines at entry.
- 2026-10-14 — capture-drift event observed during drafting (§2 erratum):
  `tools/tsukuroi-census.sh` moved 26 → 35 selftest cases (committed bytes
  `41953ee9…` / 976 lines → worktree `e9327046…` / 1032 lines, +56/−0,
  uncommitted) at 17:06:23Z; `plans/round-6.plan.md` appeared 17:05:40Z. The
  record must pin both gate revisions and state which one its sweep table and
  its re-run receipts name. This seat wrote no file but this one.
- 2026-10-14 — final-audit additions (sources in scratch): §1 plan-revision
  note (committed 142-line plan md5 `2858d36d…` vs worktree 11-line plan md5
  `0e9e8640…`) and §4 prior-probe evidence. Census sha256 pair for the record:
  committed HEAD `084951be…78c5` (976 ln) vs worktree `aae45531…7df6` (1032
  ln, 35 cases); runner sha256 `597e1419…331b` (42291 B, r4-2) matches the
  committed plan's pin. Final-file spot-check (this seat, just before
  handoff): all §1–§8 headers present; final line count + md5 are reported in
  the seat's handoff, not in-file (a further edit would invalidate them).
- 2026-10-14 — while finalizing (17:10:54Z): the drift artifact appeared in
  the worktree — `?? corpus/knowledge/timer-drift-plane.md` (mtime 17:10:45Z,
  25026 B, 321 lines at capture; possibly still in flight; this seat read none
  of it — hash its settled revision at record time). The planned sweep note
  `corpus/knowledge/mutation-case-tsukuroi-census.md` had not appeared yet.
