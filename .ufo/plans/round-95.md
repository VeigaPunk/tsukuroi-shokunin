# Round 95 — declaration (frozen before any candidate is scored; controls committed with it)

Lane: tsukuroi (operability + freshness; host operability and repair). Fleet campaign: hyaku, run 15.
Round: 95 (attempt 1). Pre-round lane tip: `c0a20cef641ada6feeab1ca107ea62c1848d1da0`.

## Inputs read before this freeze

- The round-94 closure (`MANIFEST.json` `rounds[]`, tsukuroi r94): `rejected-honest-stop`; C1 NOT met
  (the N04 decoy read `met` 98/98), C2 met.
- The round-94 non-author spot-check `corpus/lessons/round-94-verifier-spotcheck.md` §6 routed 1-10
  (registry rows, `.ready` artifact, freeze-manifest-vs-plan, do-nothing arithmetic, prose counts,
  uncited final commit, r93 routed-item mapping, battery docstring vs fixture, coverage gaps,
  contested scope).
- The round-94 lesson `corpus/lessons/round-94.md` (M1-M4, Routed).
- `corpus/QUALITY.md` 124-139 (139 is the numeric-bound rule this round executes).
- `corpus/README.md` § "Round 94" and its Frontier bullets.
- `SCORECARD.md` axes (depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8)
  and the saturation declaration (line 9, window 3).
- Previous rejected closures (fresh-start history, not re-admitted): r88/r89/r90 decisions remain on
  the record; r94 is the immediate predecessor and its honest stop is not retroactively repaired.

Lowest non-retired axes: **depth 8** and **adjacency 8** (tied). C1 works depth. No adjacency move is
declarable this round: the one open adjacency item (kaidoku/revenger reverse-engineering ownership)
is operator-owned and unruled; reported, not absorbed.

## Claims (2; frozen sentences; the same sentence in `claims.json`)

### C1 — depth 8 (tied lowest) — the accepted leg of the published component bound

**Predicate.** `tools/limine-pin-battery-r95.py --gate G --runs 3` carries, on fixtures generated
fresh per run, the family `REFUSAL-VERSIONS-9DIGIT`: the version `999999999.9.9` — the largest
in-bound member of the gate's published 1-9-digit component cap, first component 999,999,999 — is
sent as the `--limine-version` of a fixture whose first physical line is an entry label; the landed
gate must answer rc 1, verdict `DEGRADED`, the LP-MISMATCH pin with consequence `panic` (era B:
999999999 is at or above the 12.9.5 split, so the key is invisible), and `on_panic` as the fixture
fixes it; against the one-clause bend `N05-strict-8` (the gate's bound `<= 9` bent to `<= 8`) the same
battery reports `unmet` with `REFUSAL-VERSIONS-9DIGIT` in `failed_families` in every run.

**Target.** Landed gate: `99/99` met in each of three runs, `failed_families []`, 0 error rows, in the
canonical lane and in a `git clone`; N05: `98/99` unmet in each of three runs in both layouts,
`failed_families == ["REFUSAL-VERSIONS-9DIGIT"]`, 0 error rows; the r94 do-nothing battery on N05:
`met` `98/98` in each of three runs (the before instrument cannot see the bend — the blindness this
claim closes); the r94 do-nothing battery on the landed gate: `unmet` `98/99` with no
`REFUSAL-VERSIONS-9DIGIT` row in its `case_log` (the family does not exist there).

**Kill rule.** Unmet if any landed-gate run reads below 99/99 or carries a non-null `error` row; unmet
if any N05 run is not `unmet`, or its `failed_families` is not exactly
`["REFUSAL-VERSIONS-9DIGIT"]`; unmet if any r94-battery run on N05 does not read `met` `98/98`; unmet
if any r94-battery run on the landed gate lists `REFUSAL-VERSIONS-9DIGIT` among its executed families;
void if any instrument byte differs from `.ufo/waves/round-95/before/instruments.sha256` at scoring
time.

**Counting command.**
`python3 tools/limine-pin-battery-r95.py --gate <GATE> --runs 3 --work <scratch> --json <out>` then
`python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family REFUSAL-VERSIONS-9DIGIT`.

**Do-nothing and near-miss controls (committed with this freeze).**
`before/controls/do-nothing-battery-r94.py` (the r94 roster, byte-identical to
`tools/limine-pin-battery-r94.py`), `before/controls/do-nothing-gate-r94.py` (the pre-round gate
bytes), `before/controls/bends/N05-strict-8.py` (emitted by `tools/make-r95-bends.py`, which refuses
a substitution that does not match exactly once), `before/controls/count-runs.py`.

**Declared limits.** The family sends one in-bound 9-digit version; the 10-digit refused leg stays
`REFUSAL-VERSIONS-10DIGIT` (r94, unchanged). The 1-9-digit cap is the gate's own published contract;
the family certifies the cap's membership boundary, not that nine digits is the right design. The
r92 launcher residuals, the `AUTO-*` host dependence and the r89 blanks-before-CRLF / ESP containment
/ empty-label frontier stay open and uncertified. Scope disclosure: the candidate battery was
developed before this freeze; no development run (`/fast/scratch/hyaku/tsukuroi-r95/l1/dev-*.json`)
is a receipt, and every number in the report comes from the post-freeze runs.

### C2 — operability 9 (assurance arm; the lane's own registry gate is red at the tip)

**Predicate.** `python3 tools/check-registry-coverage.py --revision R`, run at the round's landed
revision R, reports `status` `clean` with `counts.findings 0`, `counts.missing 0`,
`counts.tools_total 151` and `counts.registered 151`: the operative registry table in `SKILL.md`
carries rows for the r94 tools `limine-pin-battery-r94.py` / `make-r94-bends.py` and the r95 tools
`limine-pin-battery-r95.py` / `make-r95-bends.py`, and its `limine-pins` row names the default
`auto` and the selftest tally 39 (not `12.9.4` / 37).

**Target.** `status clean`, `findings 0`, `missing 0`, `tools_total 151`, `registered 151` at the
landed revision; the `limine-pins` cell reads `default auto` and `39`; the gate's own `--selftest`
passes.

**Kill rule.** Unmet if any count differs, if `status` is not `clean`, if the `limine-pins` row still
names `default 12.9.4` or a 37-case selftest, or if `check-registry-coverage.py --selftest` does not
pass. Void if the registry gate bytes differ from the freeze manifest at scoring time.

**Counting command.** `python3 tools/check-registry-coverage.py --revision <R>`.

**Do-nothing control.** No `SKILL.md` edit; the pre-round revision
`c0a20cef641ada6feeab1ca107ea62c1848d1da0` reads `status FAIL`, `findings 2`, `missing 2`,
`tools_total 149` (measured before this freeze; the two findings name the two r94 tools). Adding the
r95 tools without registry rows would raise the count, never lower it.

**Declared limits.** A row's presence is what this gate checks; the row's *content* is certified only
for the two cells named above (`limine-pins` default and selftest tally). `REGISTRY-SELFTEST-UNRESOLVED`
and `REGISTRY-KIND-INVALID` are the gate's other checks and must stay at 0 in the same run.

## Causal separability and no-harm

- C1 reads the battery roster, the bend and the do-nothing legs; C2 reads `SKILL.md` plus the
  registry gate. C1 lands no registry row and C2 changes no battery byte; either verifies with the
  other reverted (C2 alone leaves `tools_total` 149 + 2 = 151? No: without C1 the r95 tools do not
  exist, so C2's target is `149` tools and `149` rows — it is declared against the round's landed
  tree, and its counter is the gate's own finding count, which C1 cannot make green).
- No axis is harmed: the landed gate bytes are unchanged (`tools/check-limine-pins.py` is pinned and
  the only new tool is a battery), the r94 roster remains a committed do-nothing control and its
  98/98 met reading on N05 is the blindness proof, the corpus gains one entry and three SOURCES rows,
  and no existing row is removed (one `used-by` cell is extended, logged old→new).

## Round shape (run-15 band 8-16; L2 floor 8 in one v1 wave)

One v1 wave, 13 seats (§6 run-15 shape): 4 executors (`ExecBattery`, `ExecBend`, `ExecDoNothing`,
`ExecRegistry`), 2 scouts (`ScoutSources`, `ScoutDrift`), 2 scribes (`ScribeKnowledge`,
`ScribeLesson`), 2 reviewers (`ReviewBattery`, `ReviewRegistry`), 1 critic (`CriticClaims`), 1
mutation-tester (`MutBound`), 1 connector (`ConnectorOverlap`). Attack roles: 2 reviewer + 1 critic +
1 mutation-tester = 4/13 = 31 % (≥25 %); the connector is a fifth adversarial read for the pre-file
ledger. Residual call: none. The §3 planner seat is held by the L1 (the validator rejects `planner`);
the bounded planning data-walk rides `ScoutDrift`.

## Routed-defect dispositions (r94 spot-check §6)

1. Registry rows → **C2** this round.
2. `.ready` bookkeeping → the r95 wave commits `w1.ready` and `w1.ready.dispatched` as wave evidence
   (the dispatch path itself is the orchestrator's; the files are committed, not promised).
3. Freeze manifest vs plan → the frozen plan copy is `before/plan-frozen.md`; the live
   `.ufo/plans/round-95.md` is NOT in `freeze-manifest.sha256`, so post-freeze amendments cannot
   invalidate the manifest. The r94 sentence is corrected in the r95 report.
4. Do-nothing arithmetic and the stderr clause → corrected in the r95 report and lesson (the r93 gate
   reads `97/98` on the r94 roster; it refuses a stderr-only fake like the V4 probe, `p.stdout` only).
5. Report prose counts → every count in the r95 report is copied from a named artifact and re-counted
   by a command before filing; the ledger's row count is `grep -c` from the TSV.
6. Uncited final commit `029f6629` → named in the r95 report's landed-changes section.
7. r93 routed-item mapping → the r93 queue is mapped by its own text in the r95 lesson; routed 4's
   M12 timeout survivor and routed 5's `VERDICT-INCOMPLETE` stay open and are named, not closed.
8. Battery docstring vs fixture → `fam_auto_probe_shapes`'s docstring is corrected in r95's battery
   docstring history paragraph? No: the r95 battery keeps the r94 text byte-identical (it is a
   successor copy); the correction is recorded in the lesson and the docstring's r95 paragraph.
   `REFUSAL_DIGIT9` is now referenced by `REFUSAL-VERSIONS-9DIGIT` (C1), so the declared-and-unused
   defect is closed.
9. Coverage gaps → the `12.9.6.1` extra-component shape and a `<= 8` gate's reading are the r95 C1
   ground (the second is the bend); the extra-component shape stays on the Frontier.
10. Contested scope → carried, reported, not absorbed.

## Amendments

Free-text slot. After the freeze, an amendment may NARROW a claim to what the instrument enforces,
recorded here with the artifact that falsified the wider sentence. No amendment may widen a target or
re-define a predicate after a seat has scored it (fleet lesson, kumitate r42).

- **A4 (post-scoring scope correction, citing wave artifacts).** Two sentences claimed more than
  their instruments. (a) C1/A1 say the do-nothing battery "cannot see the bend"; that is true of its
  **family roster** (98/98 met, 0 nine-digit rows) but not of the same frozen bytes' `--usage-check`
  leg, which does see the cap (`999999999.0.0` wants rc 0 and the bend answers rc 64;
  `w1/ExecDoNothing.md`). The claim's sentence is therefore "the r94 **family roster** has no in-bound
  9-digit case", and the counting command is the roster run. (b) C2's predicate lists the
  `limine-pins` content cells after a colon as if the registry gate's `PASS` asserted them; it does
  not — `w1/ExecRegistry.md` §6 and `w1/ReviewRegistry.md` show a real table with wrong content still
  reads `PASS 151/151`, and the gate binds no row name to its path. The enforceable sentence is: the
  gate's `PASS` certifies row presence, kind, verdict-map completeness, orphan paths, selftest-flag
  resolution and the counts; the two `limine-pins` cells are certified by a direct `git show` grep at
  the measured revision and by `tools/check-limine-pins.py --selftest` (`selftest PASS 39/39`), not by
  the registry gate. C2's void clause is likewise corrected: the freeze manifest does not pin
  `tools/check-registry-coverage.py` or `SKILL.md`, so "void if the registry gate bytes differ from
  the freeze manifest" is unverifiable; the void rule binds the sha256 of
  `tools/check-registry-coverage.py` recorded in the C2 receipt at the measured revision
  (`sha256sum tools/check-registry-coverage.py`). No target number changes.

- **A3 (post-scoring narrowing, 2026-11-08T07:3x-03:00, citing a wave artifact).** C1's predicate
  called `999999999.9.9` "the largest in-bound member of the gate's published 1-9-digit component cap".
  `w1/ReviewBattery.md` F1 falsifies that superlative: the cap admits
  `999999999.999999999.999999999`, which the landed gate accepts (rc 1, `DEGRADED`, era `12.9.5+`;
  `w1/ReviewBattery/boundary-probe.txt`), and the battery sends neither that value nor any 9-digit Y
  or Z position — a bend of Y's bound to `<= 8` still reads `met` 99/99
  (`w1/ReviewBattery/middle-bound-probe.txt`). The claim is narrowed to the sentence the instrument
  enforces: **"a boundary member of the gate's published 1-9-digit component cap: the first
  component is 999,999,999 (the largest nine-digit value), with the second and third components at
  9"**. The description "era B: 999999999 is at or above the 12.9.5 split, so the key is invisible"
  stays; the observable it names (`panic`) is the enforced one. Declared limits carried from
  `w1/ReviewBattery.md` F1-F3: the true component-wise maximum and 9-digit Y/Z positions are not
  sent; the battery's `got` tuple carries no `visibility_era`, so the era *mechanism* is unclaimed
  (variant c clamping the era tuple reads `met` 99/99); the echoed `limine_version` is recorded but
  not compared for explicit-version cases (variant d reads `met`). `claims.json` is left byte-frozen
  (it is pinned in `before/instruments.sha256`); this amendment supersedes the predicate's superlative
  and is the ledger's `narrowing` pointer.

- **A2 (pre-scoring wording fix, 2026-11-08T07:0x-03:00, before the wave was dispatched).** C2's
  predicate said the registry gate "reports `status` `clean`"; the gate's actual clean token is
  `PASS` (`status FAIL` at the pre-round tip, `status PASS` at `b66e6be5`). The predicate, target and
  kill rule now say `PASS`. Evidence: `.ufo/waves/round-95/after/c2-before-c0a20cef.json` and
  `c2-after-b66e6be5.json` (the L1's own runs, committed as receipts). No target was widened.

- **A1 (pre-scoring narrowing, 2026-11-08T06:5x-03:00, before any seat was dispatched and before any
  receipt existed).** C1's first frozen target said the N05 leg reads "0 error rows" and that the r94
  do-nothing battery on the landed gate reads "unmet 98/99". Both sentences are wrong about the
  instruments. (a) `N05-strict-8` refuses the 9-digit value with rc 64 and no JSON, so the battery
  records four `error` rows for that family — that is the bend's refusal receipt, not a crash, and the
  0-error-row rule binds only the landed-gate legs. (b) The r94 battery runs its own 98-family roster,
  so on the landed gate it reads `met` 98/98 and cannot read 98/99; the family-absence evidence is 0
  `REFUSAL-VERSIONS-9DIGIT` rows in its `case_log`. Evidence pointer:
  `/fast/scratch/hyaku/tsukuroi-r95/l1/dev-n05-r95.json` and `dev-n05-r94.json` (development runs,
  never receipts). The live sentences are these (and `claims.json`), superseding the two sentences in
  the C1 row above; no target was widened and no receipt had been produced when this was recorded:

  > **Target (A1).** Landed gate with the r95 battery: `99/99` met ×3 canonical and clone,
  > `failed_families []`, 0 error rows. `N05-strict-8` with the r95 battery: `98/99` unmet ×3 both
  > layouts, `failed_families` exactly `["REFUSAL-VERSIONS-9DIGIT"]`, and its four N05 case rows carry
  > the battery's `error` text (the bend refuses rc 64 and emits no JSON — the bend's refusal receipt,
  > expected in this leg only). `N05-strict-8` with the r94 do-nothing battery: `met` `98/98` ×3, 0
  > error rows, 0 `REFUSAL-VERSIONS-9DIGIT` rows in `case_log`. Landed gate with the r94 do-nothing
  > battery: `met` `98/98` ×3, 0 error rows, 0 `REFUSAL-VERSIONS-9DIGIT` rows in `case_log`.
  >
  > **Kill rule (A1).** Unmet if any landed-gate r95 run reads below 99/99 or carries a non-null
  > `error` row; unmet if any N05 r95 run is not `unmet` or its `failed_families` is not exactly
  > `["REFUSAL-VERSIONS-9DIGIT"]`; unmet if any N05 r94 run is not `met` `98/98` or carries a non-null
  > `error` row; unmet if any landed-gate r94 run is not `met` `98/98`, carries a non-null `error`
  > row, or lists a `REFUSAL-VERSIONS-9DIGIT` row in `case_log`; void if any instrument byte differs
  > from `.ufo/waves/round-95/before/instruments.sha256` at scoring time.
