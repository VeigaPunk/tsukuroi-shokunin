# Round 97 verifier spot-check — tsukuroi

author: hyaku closure (non-author integrator, @m_zfl)

## Conformance (step 1)

- Report `.ufo/reports/round-97/tsukuroi.md` committed in the fleet repo by the lane identity:
  `git log --format='%an %ae %H' -- .ufo/reports/round-97/tsukuroi.md` →
  `tsukuroi-shokunin tsukuroi@shokunin.local 797957a2aac638f63c96142cba453f83798f8a01`.
- Report carries `## SHONEN` with one line per box (4 lines, all `[~]` with evidence pointers),
  and `## Work performed`, `## Landed changes`, `## Before → after measurements`,
  `## Sources & frontier`, `## Trend verdicts`, `## Prefile falsification gate` — no missing
  contract section.
- Every cited lane commit exists and is an ancestor of the branch
  (`git -C …/tsukuroi-shokunin merge-base --is-ancestor <h> master`): `a57e88cd` (freeze),
  `dafcd5df` (wave), `b492f17f` (settle), `5eb475cd` (header repair), `b3db56a4` (measured),
  `9c4b7b16` (L1 receipts) — all YES. `46fae1ba`/`9e052291`/`227a4b7c` are scratch-clone fixture
  revisions, not lane commits (see defect R97-D1).
- Lane repo clean and pushed: `git status --porcelain` → empty;
  `jj-lane.sh state` → `ahead=0 behind=0 head=detached tracked=0 untracked=0`
  (`local=remote=9c4b7b164f926ee2cb1f8683b4fe8f3f5796b1a9`).
- Report lands last: lane tip `9c4b7b16` committed 09:25:34, report commit 09:25:55 (author date
  09:18:45), driver `complete` line 09:26:51 — commit-then-report ordering holds.
- Prompt `.ufo/prompts/tsukuroi-round-97.md` (996 lines, committed by the lane identity 049cbcdc)
  is the template rendering: `diff` of `templates/round-prompt.md` §1–§5 against the prompt's
  first 140 lines is 42 diff lines, every one a `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}`
  substitution. All five child-lane items present (report path, commit-before-report, `## SHONEN`
  check, `landed <hash>` citation rule, write scope at line 448/582). §6 addendum carries the
  run-15 map; the stated 8–16 band matches `scripts/hyaku/ufo-wave-policy.json`
  (`waveMinLanes 8`, `waveMaxLanes 16`) and MISSION.md §L2's ≥8 floor.
- Wave shape (`w1-results.json`, `w1-validate.err` 0 bytes): 14 seats, 14 settled, 0 dead
  (5 executor, 2 scout, 2 scribe, 2 reviewer, 1 critic, 1 mutation-tester, 1 connector) — inside
  the 8–16 band, 1 connector ≤2. Attack share 5/14 = 36 % under the prefile gate's `ATTACK_ROLES`
  (which includes connector); 4/14 = 29 % under the strict reviewer/critic/mutation-tester/labrat
  set — both above the 25 % floor.
- Misroot sweep at closure: `git -C /home/vgpnk/Projects/shokunin status --porcelain` → 11 paths
  (`.scratch/`, `.ufo/reports/round-97/kama.md` = another lane, `scripts/hyaku/__pycache__/*.pyc`,
  `census/`); none names tsukuroi or round 97. No lane misroot.
- Marker rule: the report names real committed work (6 lane commits, receipts, a measurable
  `9c4b7b16`) — not a marker.
- Verdict: conformant. Defects named below are status-neutral.

## Per-claim re-check

### C1 — depth 8 (roster 103 → 105)

Re-derived by the closure judge from committed bytes at `9c4b7b16`:

- Roster count, static AST over the committed tool: `FAMILY_ROSTER len=105`,
  both `REFUSAL-VERSIONS-9DIGIT-Z` and `LEADING-ZERO-NORMALIZE` present; the same parse of
  `f48d1642:tools/limine-pin-battery-r96.py` → `len=103`. **Re-measured.**
- New-family definitions read at the tip: Z members `12.9.999999999` (era B) / `0.9.999999999`
  (era A); LZ members `12.09.4`, `000000012.9.4` (era A), `12.000000009.000000005` (era B),
  `000000000.000000000.000000000` (era A) — exactly the frozen predicate. **Verified.**
- Do-nothing control integrity: `sha256sum .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py`
  → `f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba`;
  `git show f48d1642:tools/limine-pin-battery-r96.py | sha256sum` → the same hash.
  **Re-measured.**
- Instrument manifests: `sha256sum -c .ufo/waves/round-97/before/instruments.sha256` → 19 OK,
  1 FAILED (`before/fixtures/build-doctored-fixture.sh`, the A1 recipe correction);
  `sha256sum -c .ufo/waves/round-97/before/instruments-r97-after-fixture-pin.sha256` → 20 OK.
  The four scoring instruments match the live tree (`check-limine-pins 7d79ac29…`,
  `limine-pin-battery-r97 e678c34f…`, `make-r97-bends 972c672b…`,
  `check-registry-content 2daf5926…`). **Re-measured.**
- Landed-gate receipts: `w1/ExecBattery/count-canonical.txt` and `count-clone.txt` each carry
  3 runs `met`, `families_passed 105/105`, `cases 420`, `error_rows 0`, `failed_families []`;
  `after/c1/l1-c1-gate-runs3.{json,txt}` → 3 × `105/105 met` at `b492f17f`. **Evidence-verified.**
- Bend legs (`w1/ExecBend.md` + per-layout JSONs): N05 `103/105` ×3 canonical and ×3 clone,
  `failed_families` exactly `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 6 non-null
  error rows per run (4 Z + 2 LZ); N06 `104/105` ×3 + ×3, `[LEADING-ZERO-NORMALIZE]`, 4 rows;
  every row `bad-output: JSONDecodeError rc=64` — the bend's own refusal. **Evidence-verified.**
- Do-nothing legs: `w1/ExecDoNothing` → `met 103/103` ×3 on the landed gate and on both bends,
  412 case rows, 0 error rows. **Evidence-verified.**
- Instrument self-check at the tip: `after/c1/battery-selftest-reference.txt` →
  18/18 PASS rc=0, reference gate `105/105`; `after/c1/isolation-check.json` →
  `lane_visible false`, `battery_visible false`. **Evidence-verified.**
- Axis verdict: depth **improved** (103 → 105 certified families, the Z leg of the published
  1–9-digit bound and the accepted leading-zero spelling each witnessed by a one-clause bend the
  do-nothing control is blind to; the SCORECARD's ordinal stays 8, "no ordinal uplift").

### C2 — freshness 9 (0 → 7 bound registry cells)

- `BINDINGS` parsed statically from the committed checker → 7 entries (`RC-ENTRY-DEFAULT`,
  `RC-SELFTEST-COUNT`, `RC-SCHEMA`, `RC-ROSTER-VERDICT`, `RC-ROSTER-PINNED`, `RC-CAL-SELFTEST`,
  `RC-BEND-SPAN`) over 4 rows. **Re-measured.**
- Independent re-derivation of every declared cell from the tool bytes at `9c4b7b16`:
  `check-limine-pins.py` line 503 `add_argument("--limine-version", default="auto"` → `auto`;
  selftest tally 39 `--selftest` (39 …) = 36 `case(` calls + 3 direct `results.append` = 39
  fixtures, committed receipt `w1/ExecGateHygiene/receipts/03a-gate-selftest.txt` →
  `selftest PASS 39/39`; `schema "tsukuroi-limine-pins-v3"` at line 315 and in the SKILL cell;
  r96 roster 103 by AST against `FAMILY_ROSTER, 103,` and `roster 103 (` in two SKILL cells;
  `check-r96-calibration.py` selftest 7 = clean + F1–F6; `make-r96-bends.py` `VARIANTS` keys
  `N01`…`N04` against `VARIANTS N01-N04` (two SKILL rows). All seven re-derive. **Re-measured.**
- Landed run: `after/c2/content-tip.json` → `status PASS`, `bindings 7`, `findings []`,
  revision `b492f17f`; `w1/ExecRegistryContent/01-landed-content.txt` → `PASS bindings 7/7
  findings 0`. **Evidence-verified.**
- Selftest: `02-selftest.txt` → `selftest PASS 12/12` rc 0, each one-cell doctor id-exact.
  **Evidence-verified.**
- Doctored leg: `05b-doctored2-content.txt` → `status FAIL`, exactly six `RC-VALUE-MISMATCH`
  (one per doctor, each naming its row and the derived value), rc 1; `06b-doctored2-coverage.txt`
  → coverage gate `PASS 154/154 findings 0` on the same revision (`9e052291`); the dev pair
  `before/dev/c2-content-doctored.txt` + `c2-coverage-doctored.json` shows the same six findings
  and `PASS 154/154` at `84c95e25` (base `f48d1642`). **Evidence-verified** (revision attribution
  defect R97-D1 below).
- Settled tip: `after/c2/coverage-tip.json` → `PASS`, `registered 157`, `tools_total 157`,
  `findings 0`. **Evidence-verified.**
- Fail-closed legs (`w1/ReviewRegistryContent/receipts/04-*`): missing tool → rc 1 with three
  `RC-DERIVE-FAILED`; missing row → rc 1 `RC-ROW-MISSING`; 7-column table → rc 2 `E-TABLE`;
  non-ancestor → rc 2; unresolvable revision → rc 2. **Evidence-verified.**
- Axis verdict: freshness **improved** (a drift gate that re-derives declared values from the
  bytes of the tool each row names, and that catches six content-only doctors the row-presence
  coverage gate certifies `PASS 154/154`; score holds at 9, the arm is assurance).

### Gate-standard binding

Both claims rest on lane-owned gates. Per PROTOCOL §Gate standard (Closure consequence) the
closure verified committed evidence — the self-test tallies (`18/18` with `--reference` at
`9c4b7b16`; `12/12`; the subject gates' own `39/39` and `7` cases), the frozen-run verdicts and
the revision each was measured at — and did **not** execute either sibling gate. C1's bends and
do-nothing legs are wave receipts under frozen instruments; C2's doctored leg is a committed
receipt pair. Registry rows for all three r97 tools exist at the lane's registry home
(`SKILL.md:5941-5943`), each with entry command, verdict map, self-test and pinned values.

### Falsification ledger (2b)

- `python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tsukuroi
  --round 97` → `PREFILE-FALSIFICATION: pass claims=2 rows=16 attack_seats=5 findings=0`, exit 0.
- Ledger `.ufo/waves/round-97/claim-falsification.tsv`: 16 rows (5 `falsifies-wording`, 0
  `falsifies-number`, 11 `neutral`), covering C1 and C2 and all five attack seats
  (`ReviewBattery`, `ReviewRegistryContent`, `CriticClaims`, `MutRegistry`, `ConnectorOverlap`).
  Every wording row names a narrowing: A3 (blindness is the roster leg; the r96 `--usage-check`
  already sends `12.09.4`/`00.00.00`), A7 ×2 (`visibility_era` and the echoed version are not
  asserted for the new members), A6 (the LZ docstring names the wrong text-comparer member), A4
  (the blindness leg holds only at the pinned `f48d1642` base). **PASS, no adjudication needed.**
- Amendments A1–A7 verified present in `before/plan-amendments-r97.md`.

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| depth | improved | roster 103 → 105 by AST at the tip; two families witnessed by one-clause bends the r96 control is blind to (`103/103`); knowledge entry `limine-bound-9digit-z-r97.md` with the provenance trio |
| coverage | unchanged | PROVINCE.md unchanged; no coverage claim; the 150 unbound registry rows are a named limit, not a regression |
| operability | unchanged | three new registry rows are registered and runnable, but no operability claim was declared and no existing runnable artifact changed |
| freshness | improved | `check-registry-content.py` binds 7 cells to tool bytes and reads FAIL on six content-only doctors the coverage gate certifies PASS; `S389`/`S391` re-opened byte-identical |
| calibration | unchanged | report numbers match the closure's re-derivations except the provenance slips R97-D1/D2, which are label defects, not false measurements; SHONEN lines are honestly `[~]` |
| adjacency | unchanged | `ConnectorOverlap` swept 20 sibling repos, 0 duplicate claims / 0 contradictions; kaidoku/revenger ownership stays operator-owned and unruled, reported not absorbed |

No axis harmed: the gate `tools/check-limine-pins.py` is byte-unchanged (`7d79ac29…`), the r96
control still reads `103/103`, the coverage gate certified `154/154` before the round's rows and
`157/157` after them, and the corpus is additive (one SOURCES row, one knowledge entry, five
lesson mistakes, QUALITY 141).

## Discernment spot-check (LEARNING.md)

Re-opened by the closure judge on 2026-11-08 (live fetch, not the lane's pin):

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S392 (new row) | admit | `https://docs.python.org/3/library/functions.html#int` → fetched 331022 bytes, sha256 `d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7` (byte-identical to the lane's pin); `grep -abo` | **agree** | the ≤25-word quote "have leading zeros, be surrounded by whitespace," is at BYTE 157767, `id="int"` at 153202 and the base-0 contrast at 159315 — exactly the row's anchor; the quote grounds the teach (explicit base accepts leading zeros) and the tier A scoping is right |
| rejected candidate | reject | `https://man.archlinux.org/man/python.1` → fetched 41788 bytes, sha256 `11c40ea1…` (byte-identical to the pin); `grep -c 'int('` → 0, `leading zero` → 0, `limine` → 0 | **agree** | the page documents CLI options only; it grounds neither the `int()` string form nor any Limine behaviour, so the reject reason is accurate and the source cannot support an admitted entry |
| S389 / S391 re-open | admit (no drift) | committed pins `page-822fd828.html` 815447 bytes `6bf2ce2b…` and `page-b1b43819.html` 280632 bytes `a7e00587…` | **agree** | the re-opened pins are byte-identical to the r96 values the rows cite; nothing was touched in place |

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 0,
`tsukuroi ok`, 392 rows, 0 E findings, 57 W04 + 1 W01 (the same pre-existing warning set as r96;
S392 is not flagged). SOURCES rows 391 → 392 measured independently:
`grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → 392;
`git show f48d1642:corpus/SOURCES.md | grep -cE …` → 391. S392's `used-by` paths exist.

## Trend verdicts

- **expansion — improved.** One admitted `knowledge/` entry
  (`corpus/knowledge/limine-bound-9digit-z-r97.md`) on ground the coverage map did not hold, its
  `source:` citing S392 — a row opened and admitted this round with a byte-located quote — and
  S389/S391 re-opened without drift; net +1 row (391 → 392), none removed.
- **quality — improved.** The two named r96 Frontier limits are closed by families whose bends
  fail exactly them (N05 two families / 6 refusal rows, N06 one / 4 rows), the r96 Y-family
  docstring defect is corrected in both the successor and the r96 tool with its manifest relation
  stated, the provenance-header gate is green at the tip (113/113 clean, 0 findings, from 110/112
  + 5 findings), and C2 adds a drift gate that catches six content-only doctors while the
  coverage gate certifies the same table.
- **discernment — improved.** Five claim clauses were falsified or narrowed by wave seats (A3,
  A4, A6, A7 ×2) and the surviving attacks were left named rather than smoothed (era-field/echo
  survivors, M07/M08, the three C2 scope gaps); the lane's own locator unit error (character vs
  byte index) was caught by an independent seat and became QUALITY 141, a criterion with its
  captured-by — and this spot-check agrees with both re-opened gate decisions.

## Routed defects (the lane must fix next round)

- **R97-D1 — C2 doctored-leg revision attribution.** The report pairs receipt
  `before/dev/c2-content-doctored.txt` with revision `46fae1ba`, but that receipt's committed
  JSON sibling records `84c95e25`; `46fae1ba` appears only in the A1 amendment's prose and has no
  committed receipt. Both are scratch-clone builds of the identical tree at base `f48d1642` and
  both show the same six findings + `PASS 154/154`, so the claim is unaffected — but a reader
  re-deriving sees a different hash. r98: cite the receipt's own revision, or commit the A1
  re-run receipt.
- **R97-D2 — numeric decomposition in the r96-tool sentence.** The report states the r96 tool
  diff is "8 +/− 2 lines"; `git diff --numstat f48d1642 9c4b7b16 -- tools/limine-pin-battery-r96.py`
  → `6 2` (6 insertions, 2 deletions; the diffstat `8 +-` is the total changed-line count). Minor
  numeric-label defect; correction goes in the r98 report/erratum, never a rewrite of filed bytes.
- **R97-D3 — LZ docstring sentence (A6, already self-routed).** `fam_leading_zero_normalize`'s
  docstring still says a text comparison orders `000000012.9.4` as era B; measured, text
  comparison orders it era A and the discriminator is `12.000000009.000000005`. Second instance
  of the class in two rounds — r98 corrects the sentence in the successor (frozen bytes are not
  edited) and adds the QUALITY criterion the lesson calls for.
- **R97-D4 — C2's three measured gaps stay on the queue.** Unbound-cell doctoring reads PASS
  (7 cells of 4 rows), a co-doctored tool reads PASS (same-revision scope), and a printed-tally
  fake survives (parse-only derivation); M08 survives for want of a non-contiguous `VARIANTS`
  fixture. Named limits, not regressions; carry them into the r98 Frontier.

## Verdict

Both declared claims verify from committed evidence; no axis is harmed; the prefile ledger
passes with zero findings; the gate decisions spot-check agrees on one admit and one reject.
Status `ok`, **admitted**. SHONEN note for the operator: boxes 1, 2 and 4 are checkable from this
round's artifacts by a non-author; box 3 is only partially checkable (two recipes executed
end-to-end, the whole-SKILL replay still unexecuted). Promotion remains operator-owned.
