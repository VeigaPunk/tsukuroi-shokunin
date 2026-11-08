# tsukuroi — round 100 report

Lane: `tsukuroi-shokunin` (operability + freshness; host operability and repair). Campaign: hyaku,
run 15. Round 100, attempt 1 — the lane's graduation round. Pre-round tip
`ce73ccaf75d0279385977f03ccb35945c1cf8e07`; freeze `743ce449490f4e9ff004f423ecc3fa456cbc77ec`;
wave dispatch `60b5636ff6b64ea90ba6cc2bb83e65d52a34a2ff`; landing `c450cd68`;
registry-row repair `69474c55`; after receipts `ef12af4c`; amendments `7961738a`. No inherited
state: the round-100 wave directory did not exist at start, and the lane was clean at `ce73ccaf`
(`jj-lane.sh state`: `ahead=0 behind=0 tracked=0 untracked=0`).

Declared claims — **C1 depth 8** (tied-lowest non-retired axis): `tools/make-r100-bends.py` emits two
component-keyed one-clause bends of the unchanged gate (`N12-x-echo` on the first version component
`999999999`, `N13-y-echo` on the second), and the unchanged r99 battery must move the accepted-cap
families' `check_echo` assertion that the round-99 Frontier names as having no spelling-targeted
committed bend; the r98 battery is the do-nothing control. **C2 freshness 9**:
`tools/check-registry-content-r100.py` binds `RC-BEND-SPAN` as a label set (tokens
`N<digits>`/`N<digits>-N<digits>`, ranges expanded, separators `,` whitespace `;` `+` `/` `and`, set
equality against the tool's `VARIANTS` keys), closing the r99 named capture limits, with the r99
checker as the do-nothing control. Adjacency (8, tied lowest) carried no claim: the
kaidoku/revenger reverse-engineering ownership stays operator-owned and unruled.

## Work performed

- **C1 — depth.** `tools/make-r100-bends.py` (exact-once substitution guard; refuses a no-op) emits
  `N12-x-echo` (the returned `limine_version` falsified when the first component is `999999999`) and
  `N13-y-echo` (same for the second component), each a one-line diff against the unchanged gate
  `tools/check-limine-pins.py` (`7d79ac29…`, BYTE 16931 emission). Evidence: `before/dev/`
  (development runs at the freeze), `w1/ExecGateRuns.md` (landed `met 105/105` ×3 canonical + ×3
  clone, cases 420, schema `tsukuroi-limine-pin-battery-r99-v1`, usage-check, selftest 5/5,
  0 error rows), `w1/ExecBends.md` (`N12` `unmet 103/105` with exactly
  `[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]` and `N13` `unmet 104/105` with exactly
  `[REFUSAL-VERSIONS-9DIGIT-Y]`, ×3 in both layouts, 0 error rows; one-line diffs; the extra
  unasserted-spelling probe `key13` `met 105/105`), `w1/ExecControl.md` (r98 control `met 105/105` on
  the gate and on N13 — blind — and `unmet 104/105` exactly `[EXPLICIT-VERSION-ECHO]` on N12),
  `w1/ReviewBends.md` (15 legs × 3 runs; 45/45 runs 0 error rows; the early `conf unreadable` return
  at BYTE 11230 is untouched — amendment A2), `w1/MutInstruments.md` (generator mutants B1-B3 killed;
  checker mutants M1-M6, M8 killed; M7 survivor named), `w1/CriticClaims.md` (clause-by-clause
  adjudication; the X leg is a family-unit flip of `EXPLICIT-VERSION-ECHO` inside an already-unmet
  run — amendment A3).
- **C2 — freshness.** `tools/check-registry-content-r100.py` replaces the span capture with a label
  set: six cells that the r99 control rejects now bind (`SEP-SPACE`, `SEP-SEMICOLON`, `SEP-PLUS`,
  `SEP-SLASH` — r99 `RC-CELL-MISSING`; `SEP-AND`, `UNION` — r99 `RC-VALUE-MISMATCH`), five forged
  shapes stay closed (`LETTER`/`PROSE` `RC-CELL-MISSING`, `UNION-LIE`/`HYBRID` `RC-VALUE-MISMATCH`,
  `RESTATED` `RC-CELL-AMBIGUOUS`), `GAP` PASS on both; `--selftest` 17 → 26. Evidence:
  `after/c2/{content-tip,content-tip-r99,fixtures,selftest-r100,selftest-r99,coverage-tip}.json|txt`,
  `w1/ExecRegistry.md` (both checkers `PASS 7/7` at the freeze tip and the final tip; 12/12 fixture
  readings; coverage `PASS 165/165`), `w1/ReviewRegistry` (forgery battery; see the wave note),
  `w1/MutInstruments.md` (M1-M6/M8 killed by named cases; M7 survivor routed).
- **Frontier step.** `corpus/SOURCES.md` rows S396 (own-work: the two new instruments) and S397
  (`re` docs, `fullmatch`/`\b`) admitted, S398 (limine v12.9.6 `CONFIG.md`) kept as a rejection with
  its flip; census before 395 rows exit 0 → after 398 rows exit 0; lesson
  `corpus/lessons/round-100.md` mines five mistakes (the X delta, the S395 one-anchor-two-members
  correction, the stale r99 LOG headings, the census exit omission, the clone-path harness fault, the
  coverage gap at the freeze, and the brief's asserted `key12` example); knowledge entry
  `corpus/knowledge/limine-echo-bends-r100.md`; QUALITY 142 added from the harness-fault lesson;
  `considerthese` mined by the connector (0 in-province proposals adopted; `10-26 #2`, `#5` and
  `10-25 #3` already implemented).
- **Verification.** `git diff ce73ccaf 743ce449` names only the freeze paths (22 files, all additions);
  at `69474c55` the coverage gate reads `PASS 165/165/165 findings 0`, the r100 checker
  `PASS 7/7 findings 0`, the r99 control `PASS 7/7`; the gate, r98 battery, r99 battery and r99
  checker are byte-identical to `ce73ccaf` (`w1/SentinelHarm.md`, `w1/ScoutFrontier.md`).

## Landed changes

| change | LOG entry | commit |
|---|---|---|
| freeze: the two tools, claims, plan, controls, development receipts | `## Round 100 — freeze (743ce449)` | `743ce449` |
| wave w1 spec/dispatch/ready (14 seats, validated band 8-16) | same entry | `60b5636f` |
| SKILL.md registry rows + `R100-REG-1`, SCORECARD declaration, LOG freeze, knowledge/lesson/README, SOURCES S396-S398 | same entry | `c450cd68` |
| registry-row repair (8th cell restored) | lesson correction + `R100-REGISTRY-ROW-CELL-COUNT` | `69474c55` |
| after receipts (C1 both layouts, C2 fixtures/selftests), QUALITY 142, lesson defect rows, plan A1 | `## Round 100 — measured` | `ef12af4c` |
| wave amendments A2-A7 and corpus corrections (S397 verbatim quote, S396 clause-start pair) | same entries | `7961738a` |
| LOG measured entry + SCORECARD measured rows + falsification ledger | `## Round 100 — measured` | `<LANE_TIP>` |

## Before → after measurements

**C1 — depth** (measured at the final lane tip; receipts `after/c1/`, independent re-runs
`w1/ExecGateRuns.md`, `w1/ExecBends.md`, `w1/ExecControl.md`).

Counting command: `python3 tools/limine-pin-battery-r99.py --gate <ARTICLE> --runs 3 --work <scratch>
--json <out>`, then `python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family
REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family EXPLICIT-VERSION-ECHO`.

| article | instrument | before (the round-99 state) | after (measured) |
|---|---|---|---|
| landed gate | r99 battery | `105/105 met []` | `105/105 met []` ×3 canonical + ×3 clone, 0 error rows |
| `N12-x-echo` | r99 battery | the article did not exist | `103/105 unmet [EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]` ×3 both layouts, 0 error rows |
| `N13-y-echo` | r99 battery | the article did not exist | `104/105 unmet [REFUSAL-VERSIONS-9DIGIT-Y]` ×3 both layouts, 0 error rows |
| `N12-x-echo` | r98 battery (control) | — | `104/105 unmet [EXPLICIT-VERSION-ECHO]` ×3 both layouts (delta of one family) |
| `N13-y-echo` | r98 battery (control) | — | `105/105 met []` ×3 both layouts (blind) |

No-work control: the pre-round tip has no `tools/make-r100-bends.py`
(`git cat-file -e ce73ccaf:tools/make-r100-bends.py` exits nonzero), and the r98 battery on the same
articles reads the blind/delta values above — the Y closure cannot be reached without this round's
article, and the X closure needs the X family's own assertion (one family beyond the control).

**C2 — freshness** (measured at `743ce449` and `69474c55`; receipts `after/c2/`).

Counting command: `python3 tools/check-registry-content-r100.py --revision <R> --json <out>`;
`python3 tools/check-registry-content-r100.py --selftest`;
`python3 .ufo/waves/round-100/before/dev/make-fixtures.py <dir>` then both checkers with `--root`.

| surface | before (r99 at `ce73ccaf`) | after (r100 at `69474c55`) |
|---|---|---|
| live table | `PASS 7/7 findings 0`, rows 163 | `PASS 7/7 findings 0`, rows 165 (r99 control `PASS 7/7`) |
| six acceptance cells | `RC-CELL-MISSING` ×4, `RC-VALUE-MISMATCH` ×2 | `PASS` each |
| five fail-closed cells | their r99 ids | `LETTER`/`PROSE` `RC-CELL-MISSING`; `UNION-LIE`/`HYBRID` `RC-VALUE-MISMATCH`; `RESTATED` `RC-CELL-AMBIGUOUS` |
| selftest | `PASS 17/17` | `PASS 26/26` |
| coverage | `PASS 163/163/163` | `PASS 165/165/165 findings 0` |

**Disclosed defect (not a scoring surface).** The first landing commit `c450cd68` carried a
7-of-8-cell row, so all three registry gates read `CANNOT_EVALUATE` there; the repair `69474c55`
restores the cell and the pair sweep (`git diff -U0 c450cd68 69474c55 -- … | grep -E '^-[^-]'`)
prints exactly one removed line. Recorded as `R100-REGISTRY-ROW-CELL-COUNT`; the freeze commit also
carried two tools without rows for one commit (coverage `missing 2` at `743ce449`), recorded as
`R100-TOOL-WITHOUT-ROW-AT-FREEZE`. Both are disclosed raw in the seat reports.

## Sources & frontier

Census, frozen command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tsukuroi`:
`before` — 395 rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`), **exit 0**;
`after` — 398 rows, **exit 0** (57 W04 + 1 W01 warnings, 0 errors). The receipt records both commands,
both outputs and both exit codes: `.ufo/waves/round-100/before/census-before-after.txt` (R99-D4).
Rows added: **two A** (S396 own-work, S397 `re` docs) and **one C rejection** (S398). Rows touched
in place: none (no `status`/`recheck`/`used-by` change). Frontier rows advanced: the r99 Frontier's
two named limits — the missing X/Y echo bends (Y closed as a met→unmet flip, X narrowed to a
one-family delta) and the fail-closed one-span rule (six separator/union cells now bind).

Corrections recorded append-only in the lesson: the S397 Gate quote is verbatim `return a
corresponding Match` (13 words at BYTE 112171; the first writing said "match object", which is absent
at that offset), and S396's N13 anchor is the clause start BYTE 3365 (3384 is its lie literal between
the paired N12 clause start 2615). `Assimilation: none` — no shokuknow package entry was adopted this
round; the `considerthese` survey is recorded by ConnectorOverlap and adopted no proposal
(`10-26 #2`, `#5`, `10-25 #3` were already implemented).

## Wave and round shape

One v1 wave, 14 seats under `ufo-wave-policy.json` (band 8-16), validated by
`ufo-swarm-wave.mjs` (`w1-validate.err` 0 bytes; `counts` 14 spawn / 0 resume / 14 total): 4 executors
(ExecGateRuns, ExecBends, ExecControl, ExecRegistry), 2 scouts (ScoutSources, ScoutFrontier), 2
scribes (ScribeKnowledge, ScribeLesson), 2 reviewers (ReviewBends, ReviewRegistry), 1 critic
(CriticClaims), 1 mutation-tester (MutInstruments), 1 connector (ConnectorOverlap), 1 sentinel
(SentinelHarm). Attack roles (reviewer/critic/mutation-tester/sentinel/connector) 6/14 = **42.9 %**
(floor 25 %), connector seats 1 (limit 2). Handoff: `w1.ready` taken at 12:11:12. `<WAVE_RESULTS>`.

The planner seat is held by the L1 (the validator rejects `planner`); the bounded planning data-walk
rode ScoutFrontier's limit-closure ledger.

## Trend verdicts

| trend | verdict | evidence |
|---|---|---|
| expansion | improved | two admitted source rows on ground the coverage map did not hold (S396 own-work instruments with byte anchors; S397 the `re` primitives the tokeniser relies on) plus one kept rejection (S398) with its flip; one admitted knowledge entry (`limine-echo-bends-r100.md`) citing both mined rows; census 395 → 398 with 0 errors |
| quality | improved | two frozen shapes that the r99 instruments could not distinguish now fail closed and are mutation-killed: the Y echo lie flips from the r98 control's blind `105/105` to `104/105`, and six registry cells the r99 checker rejected now bind while five forged shapes stay closed (selftest 17 → 26; M1-M6/M8 killed by named cases). No admitted entry fails its re-check; the gate/r98/r99 bytes are unchanged |
| discernment | improved | the round's own wording was narrowed by its wave before filing: A2 (the bends cover the main return, not the early path), A3 (the X control flips `EXPLICIT-VERSION-ECHO` at the family unit inside an already-unmet run), A4 (the plan's "no bend has ever exercised" is wider than the Frontier's "no spelling-targeted committed bend"), A5 (N13's payload is a fixed string), A6 (the tokeniser skips empty separator runs), A7 (set vs keys sharpening); two corpus precision defects were re-measured and corrected append-only (S397 quote, S396 anchor pair); the mistyped `key12` brief example was caught by ExecBends (99/105 six families) and replaced by the measured `key13` `met 105/105`; QUALITY 142 was added from a harness fault the round itself committed |

No trend is harmed: `SCORECARD.md` is append-only, `PROVINCE.md` and `SHONEN.md` are byte-identical
between `ce73ccaf` and the tip, the gate and both control instruments keep their bytes, and the corpus
changes are additive.

## SHONEN

- `[~]` SKILL.md contains real decision tables, error patterns, checklists, cited sources — this
  round appends `R100-REG-1` (the two instruments, their measured legs and their limits) and two
  registry rows with their verdict maps; non-author verification owed.
- `[~]` At least one end-to-end domain task executed and logged in LOG.md — the round's freeze,
  wave, landing, repair and measured entries execute the round contract end to end; the wave's own
  re-derivations are the independent legs.
- `[~]` Instructions executable by an agent without oral context — every wave item names absolute
  paths, the frozen instruments, its receipt dir and the report trailer resolution; 12 of 14 seats
  produced receipts from that text alone.
- `[~]` No cross-domain bleed (PROVINCE.md still accurate) — ConnectorOverlap found no sibling
  limine instrument or label-set binder and no write into the lane; `PROVINCE.md` is byte-identical
  between the tips.

## Other required lines

**Stale-lane:** none — respawn-per-round driver; no other mission of this lane is open.
**Tool installs:** none this round (no `pacman`, no `uv tool`, no `npx`; the wave's tooling note was
carried in the context and no seat installed anything).
**Prefile ledger:** `<PREFILE_LINE>`.
