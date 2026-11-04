# Round 71 — lesson (tsukuroi, hyaku run 15, attempt 1)

author: tsukuroi L1 (round 71), integrating the wave `.ufo/waves/round-71/` (14 seats, one v1 wave).
basis: declaration `0fcfca31` (frozen before data; base `930d5530`); pre-data receipts in
`.ufo/waves/round-71/before/`; wave results `.ufo/waves/round-71/w1-results.json`; seat reports in
`.ufo/waves/round-71/{w1,probes}/`.

## Gate

**Trigger and sources.** Four source documents were fetched before the declaration text and committed
byte-exact under `.ufo/waves/round-71/before/src/` with `SHA256SUMS` (4/4 OK) and `SOURCES.json`, all at
Linux stable **v7.2.11** (the host's own kernel), access date **2026-11-04**. `S1Scout` re-fetched all
four by a second route (raw.githubusercontent.com/gregkh/linux at the same tag) and read
`ROUTE2_OK=4/4`, byte-identical, and located every planned quote with line numbers
(`probes/S1Scout/{route2.txt,quotes.tsv}`).

| id | snapshot | URL | sha256 | rows |
|---|---|---|---|---|
| **S297** | `kernel/params.c` | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/kernel/params.c?h=v7.2.11` | `923610d5…782a4` | MP1, MP2 |
| **S298** | `include/linux/moduleparam.h` | `…/include/linux/moduleparam.h?h=v7.2.11` | `220f2dac…14846` | MP3 |
| **S299** | `kernel/module/main.c` | `…/kernel/module/main.c?h=v7.2.11` | `e1e1a1c8…95929` | MP4, MP5 |
| **S300** | `Documentation/admin-guide/kernel-parameters.rst` | `…/Documentation/admin-guide/kernel-parameters.rst?h=v7.2.11` | `45587d8e…88799` | MP6 |

Gate quotes (each ≤ 25 words, located in its snapshot): S297 `params.c:669` "Do not allow runtime DAC
changes to make param writable."; S298 `moduleparam.h:65` "Returns length written or -errno.  Buffer is
4k (ie. be short!)"; S299 `main.c:3393` "unknown parameter '%s' ignored"; S300
`kernel-parameters.rst:20-21` "Module parameters can be specified in two ways: via the kernel command
line with a module name prefix, or via modprobe".

**Admitted.** Four rows, all tier A `mined`: S297-S300, cited by
`corpus/knowledge/module-parameter-plane-r71.md` (MP1-MP6). At the measured revision `2b358d2d` the frozen
counter reads `MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0`, `met=1`, rc 0; the
registry reads 300 rows and all four new rows are `NF=13`.

**Rejected / refused.** One candidate row was not opened: a kmod `modprobe.d(5)` row for the
`options`/`blacklist` precedence question — the kmod tree's `man/modprobe.d.xml` path returned HTTP 404 at
tag v34, and the kernel documentation already grounds the two specification routes. It is recorded as an
unopened lead in `SOURCES.md`, not as a row (the register stays free of rows whose source was not opened).

**Non-author spot-check.** OWED. The closure judge re-opens the four URLs live, compares digests and
located quotes, and records its admit/reject agreement. No author-side `[x]` is written.

**Census.** Round start (declaration receipt `before/absence-controls.txt`): canonical validate rc 0,
296 registry rows, 88 knowledge notes. Round end at `2b358d2d`: rc 0, **300 rows, 89 notes** (W04
duplicate-URL warnings only).

**QUALITY 98 watch.** No upstream release fired for the pinned artifacts: the kernel tag is the host's own
v7.2.11 and no pinned package moved this round.

## Mistakes

- **R71-C2-PARTIAL-BOUND** — class `claim-overreach inside a frozen predicate` · evidence: the C2
  predicate says "every selftest case"; the landed harness bounded `check`/`check_cli` only, while
  `arm_run()` (`tools/tsukuroi-census.sh:4238-4247`) and the six `--identity` case children still ran
  `$(env … "$BASH" "$SELF")` unbounded (`probes/R2Reviewer/attacks.txt`, E1Harness
  `harness-vs-landed.diff`) · captured-by: `R2Reviewer` and `E1Harness` in this wave · fix: `arm_run`
  and an `id_run` wrapper route those children through `bounded_run`; the suite re-reads PASS 218/218 and
  the four R71-C2 arms still fire.
- **R71-C2-DAEMON-LEAK** — class `resource leak the harness did not own` · evidence: a case child that
  backgrounds a descendant and exits returns rc 0 with the descendant alive (R2Reviewer's
  `bounce`/daemonizing probe) · captured-by: `R2Reviewer` · fix: `bounded_run` kills the child's process
  group after `wait` unconditionally, and a fourth `R71-C2` arm asserts the recorded descendant pid is
  gone; the arm is red without the group kill.
- **R71-C2-STDIN-LOST** — class `harness regression found by its own suite` · evidence: routing the
  `--identity` stdin case through `bounded_run` made it read `/dev/null` (async children get stdin from
  `/dev/null`), so the case emitted zero lines and the suite read `FAIL (219 cases, 217 passed, 2 failed)`
  · captured-by: the suite itself and `R2Reviewer` · fix: the background start carries an explicit
  `<&0`, and the suite reads PASS 218/218; the failure receipt is `probes/R2Reviewer/repaired-selftest.txt`.
- **R71-DECL-BATTERY-COUNT** — class `stale-tally drift` (r70 D1 family) · evidence: the declaration says
  "12 cases: 1 well-formed control + 11 mutants"; `before/control/battery.txt` prints `cases=11` (1
  control + 10 mutants) · captured-by: `SC3Lesson` and `K1Critic` D3 · fix: declaration erratum (a);
  the frozen predicate is untouched.
- **R71-DECL-MODPROBE-COUNT** — class `count contradicted by its own capture` · evidence: the declaration
  says 4 files under `/usr/lib/modprobe.d`; `before/host.txt` lists **5** · captured-by: `K1Critic` D1 ·
  fix: declaration erratum (b).
- **R71-BATTERY-DUPID-ATTRIBUTION** — class `case-attribution gap` · evidence: the `mutant-duplicate-id`
  case emits `MP1..MP7` with positional ids, so it is killed by row count + snapshot reuse and never
  exercises the `duplicate-id` clause; a true `MP1,MP2,MP2,…` fixture does · captured-by:
  `E2CounterAttack` and `K1Critic` D4 · fix: recorded as a limit; the next battery amendment carries the
  true fixture (the frozen predicate is unchanged).
- **R71-C1-LEXICAL-SUBSTANCE** — class `predicate channel, named not closed` · evidence: a row that
  negates its snapshot while keeping its vocabulary reads `met=1` (`probes/L1Channels/semantic-channel.txt`)
  · captured-by: the L1's own self-attack · fix: recorded as a named limit; row semantics rest on
  R1Reviewer's substance audit and on the closure judge, never on the counter alone.
- **R71-WAVE-LINEAGE** — class `provenance ambiguity between parallel implementations` · evidence: the
  C2 commit `db58e7c9` is byte-identical to the L1 prototype and predates E1Harness's patch; N1Sentinel
  F3 flagged that the round could otherwise claim a seat-authored artifact was applied · captured-by:
  `N1Sentinel` · fix: the report and SCORECARD name the lineage (L1 implementation; seat patch as the
  independent alternative) and the post-wave repairs adopt the seats' findings.
- **R71-RELATIVE-RECEIPT-PATHS** — class `receipt not replayable as written` · evidence:
  `probes/SC3Lesson/sweep-receipt.txt` records lane-relative invocations with no `cd`, and from the fleet
  root one of those paths shadows a different file · captured-by: `N1Sentinel` F2 · fix: recorded; later
  receipts name absolute lane paths.

Not Mistake rows: the inherited untracked dispatcher markers (`.ufo/waves/round-66|67/w1.ready.dispatched`)
and the open L0 questions (`tsukuroi | round-64`, `round-60`, `round-57`) are operator/closure items,
routed around rather than answered.

## Considerthese

No proposal is mined this round; the measured status of the five proposals in the latest file
(`considerthese/2026-10-26.md`) is recorded, each verified by grep rather than restated:

- **"Counter-attack scoreboard"** — standing `SKILL.md` ledger since r41/r42, resumed at r64; continued by
  this round's scoreboard rows below.
- **"Seat-harm incident log"** — lessons-only per-round tally since r66; this round's tally is in the last
  section.
- **"Burst-aware reading"** — one mining record (r46); explicitly not a gate.
- **"Cross-note correction propagation map"** — recorded partial at r43/r54; r57/r58 say "none clears this
  round's bar"; not adopted.
- **"Downstream patch-offset check"** — adopted at round 69 as QUALITY 103; recorded here so a later round
  does not re-adopt it.

### Counter-attack scoreboard — round 71 (continuation of the r64 ledger)

| Counter | Round / arm source | Arms fielded (receipts) | Survivors | Class that beat it |
|---|---|---|---|---|
| `count-mp-rows-r71.py` (C1) | r71 pre-data battery (`before/control/battery.txt`) | 11 cases: 1 control + 10 mutants | 0 (control met=1, ten mutants met=0) | the frozen clauses fired; the duplicate-id case is mis-attributed (R71-BATTERY-DUPID-ATTRIBUTION) |
| `count-mp-rows-r71.py` (C1) | r71 wave `probes/E2CounterAttack/` | 13 source-level clause removals | **11** | clause redundancy: another clause still rejects the matched fixture; the battery catches 3 of the 11 |
| `count-mp-rows-r71.py` (C1) | r71 wave `w1/R1Reviewer/` | independent re-implementation + 16 own mutants | 0 | independent checker agrees 105/105 parsed rows and 18/18 whole-input rc |
| `selftest-case-timeout` (C2) | r71 pre-data red-before (`before/redbefore-timeout.txt`) | 1 blocking probe, external 20 s bound | n/a (rc 124, 0 verdict lines) | nothing bounded the case child pre-fix |
| `selftest-case-timeout` (C2) | r71 wave `probes/M1Mutation/` | 8 harness mutants | **1** (capture moved to `/tmp`; no case asserts where the capture lives) | hermeticity/location channel; also: deleting the four R71-C2 cases makes all 8 mutants invisible |
| `selftest-case-timeout` (C2) | r71 wave `w1/R2Reviewer/` | 6 attack groups + the daemonizing probe | 0 after repair | pre-repair: arm_run/identity unbounded and the daemonizing descendant survived (R71-C2-PARTIAL-BOUND, R71-C2-DAEMON-LEAK) |

## Trend verdicts

- **expansion: improved.** Four admitted registry rows (S297-S300, tier A `mined`) on ground the lane never
  held — at base, `modprobe.d`, `kernel-parameters`, `module_blacklist`, `NVreg`, `module_param`,
  `kernel_param_ops` and `param_attr_store` each read 0 file hits across `corpus/ SKILL.md PROVINCE.md`
  and no note named the surface; one admitted entry (MP1-MP6) cites them; the registry goes 296 -> 300 and
  the notes 88 -> 89.
- **quality: improved.** Two attack-found C2 gaps are repaired with the suite able to fail (218/218 after;
  217/219 with the two identity cases red before the stdin fix); the C1 note's three R1Reviewer precision
  findings are corrected in the note; three r70 routed defects land (D1 tallies, D2 receipt line, D3
  shebang) with a committed tool for D1's class (QUALITY 105, `tools/check-selftest-tally.py`, red 4
  mismatches on r70 bytes / green 0 on the corrected control); the round's own declaration defects are
  errata, not smoothed.
- **discernment: unchanged (author-side).** The wave caught seven of the lane's own defects (two C2 gaps,
  three declaration errors, the battery attribution, the lineage ambiguity) and the L1's self-attack named
  the lexical-substance channel; the outside non-author admit/reject spot-check is owed by the closure
  judge, and no author-side `[x]` is claimed.

## Seat-harm tally (standing per-round tally, r66 adoption continued)

Round 71: **0** seat-to-seat harms. `N1Sentinel` measured `SECRETS=0 SUDO_NONREADONLY=0 TMP_EVIDENCE=0
MISROOT=0 LANE_DIRTY_SEAT_AUTHORED=0`, with 73 in-wave writes all inside the wave dirs and 6
misroot-risk invocations that landed nowhere (F2 records one receipt that is not replayable as written).
Running tally since r66: 0, 0, 0, 0, 1, 0.
