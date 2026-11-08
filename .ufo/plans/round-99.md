# Round 99 — declaration (frozen before any candidate is scored; controls committed with it)

Lane: tsukuroi (operability + freshness; host operability and repair). Fleet campaign: hyaku, run 15.
Round: 99 (attempt 1). Pre-round lane tip: `f107da3afe511f7db8cdc30235a992b774903158`.

## Inputs read before this freeze

- The round-98 closure (`MANIFEST.json` `rounds[]`: ok, admitted) and its non-author spot-check
  `corpus/lessons/round-98-verifier-spotcheck.md`: routed defect **R99-D1** (commit the settled-tip
  coverage receipt the r98 report/SCORECARD cite as `160/160`, and drop the stale
  `after/report-draft.md` pointer) plus the carried wave limits (Y-cap field fidelity, the battery
  selftest's missing echo/era lie kind, the checker M07 ancestor branch, hybrid and
  same-cell-restatement capture shapes).
- `corpus/lessons/round-98.md`: Mistakes R98-FIELD-NOT-ASSERTED, R98-ANCHOR-FIRST-SITE,
  R98-SPAN-BRANCH-UNTESTED, R98-MUTANT-DIRECTION-READ, R98-RECEIPT-NAME-MISMATCH; the
  counter-attack scoreboard's survivors (**g6 Y-cap-only era lie `met 105/105`**, **B03 Z echo, no
  committed witness**, **lie-kind structural gap**, **M07 ancestor**, **hybrid cell `PASS 7/7`**,
  **same-cell restatement**).
- `corpus/QUALITY.md` 136-141 (136 named-limit-to-family closure; 139 the numeric bound's two legs;
  140 a target clause is re-read against one development run before the freeze; 141 byte-level
  anchors).
- `corpus/README.md` § "Round 98" and its Frontier (round-98 addition).
- `SCORECARD.md` axes: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8.
  Lowest non-retired axes: **depth 8** and **adjacency 8** (tied). C1 works depth; C2 works
  freshness. No adjacency move is declarable: the kaidoku/revenger reverse-engineering ownership is
  operator-owned and unruled — reported, not absorbed.
- `considerthese/2026-10-26.md` (newest batch; the connector evaluates its open proposals).

MANIFEST tsukuroi closures r95-r98 are all `ok`; no fresh-start window is open for this round.

## Claims (2; frozen sentences; the same sentence in `claims.json`)

### C1 — depth 8 (tied lowest) — the two accepted-cap families assert the reported fields, and the battery selftest sees an assertion removal

**Predicate.** `tools/limine-pin-battery-r99.py --gate G --runs 3` is the r98 battery (roster
unchanged at 105, its two field-asserting families unchanged) with exactly two changes:

- `REFUSAL-VERSIONS-9DIGIT` (X cap, `999999999.9.9`) and `REFUSAL-VERSIONS-9DIGIT-Y`
  (`12.999999999.4` era B, `0.999999999.0` era A) set `check_echo` and `check_era`, so each case
  asserts `limine_version` equals the flag spelling verbatim with source `flag` and `visibility_era`
  equals the label the whole tuple selects. The r98 Frontier states both limits by name: the metadata
  assertion "is bound to the two r97 families only" and "the X leg rides on one EXPLICIT case"
  (amendment A5).
- `LIE_KINDS` gains `limine-version` (the echoed value falsified) and `visibility-era` (the era label
  falsified), so the `--selftest --reference` leg falsifies the two fields the round asserts. The
  r98 scoreboard's "lie-kind coverage" row records that no lie kind falsifies either field.

**Target.** Landed gate: `105/105` met, `failed_families []`, 0 error rows, in each of three runs,
canonical lane and `git clone --shared`. Bend `N09-y-era` (era label swapped exactly when the second
component is the cap `999999999`; pins correct): `unmet 104/105` with `failed_families` exactly
`["REFUSAL-VERSIONS-9DIGIT-Y"]`, 0 error rows, in each of three runs in both layouts. Bend
`N11-x-era` (era label swapped exactly when the first component is `999999999`): `unmet 103/105`
with `failed_families` exactly `["EXPLICIT-VERSION-ERA", "REFUSAL-VERSIONS-9DIGIT"]`, 0 error rows,
in each of three runs in both layouts. The r98 do-nothing battery
(`before/controls/do-nothing-battery-r98.py`, byte-identical to `f107da3a:tools/limine-pin-battery-r98.py`)
on the landed gate: `met 105/105` x3; on N09: `met 105/105` x3 (blind to the Y assertion); on N11:
`unmet 104/105` x3 with `failed_families` exactly `["EXPLICIT-VERSION-ERA"]` (it catches the article
through one EXPLICIT case and not through the X family). `--selftest` (no reference) `PASS 5/5`.

**Kill rule.** Unmet if any landed-gate run reads below 105/105 or carries a non-null `error` row;
unmet if any bend run is not `unmet` or its `failed_families` is not exactly the frozen list or its
non-null error-row count is not 0; unmet if any do-nothing leg differs from its frozen reading; unmet
if either new lie kind fails to make the battery read `unmet`; void if any instrument byte differs
from `.ufo/waves/round-99/before/instruments.sha256` at scoring time.

**Counting command.**
`python3 tools/limine-pin-battery-r99.py --gate <GATE> --runs 3 --work <scratch> --json <out>`;
then `python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family
REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family REFUSAL-VERSIONS-9DIGIT-Z`.

**Do-nothing and near-miss controls (committed with this freeze).**
`before/controls/do-nothing-battery-r98.py` (the r98 landed battery), `before/controls/do-nothing-gate.py`
(the unchanged gate, `7d79ac29…`), `before/controls/bends/N09-y-era.py` and `N11-x-era.py` (emitted by
`tools/make-r99-bends.py`, each exactly one clause). Development receipts: `before/dev/c1-*`.
A drafted third bend (Z-only echo lie) was dropped as a **twin** under QUALITY 136: the r98 battery
already sets `check_echo` on the Z family, so that article reads `unmet 104/105` on the r98 control
(`before/dev/c1-N10-twin-r98.json`) and witnesses r98's assertion, not r99's.

### C2 — freshness 9 — the registry checker's capture refuses a hybrid cell and its selftest exercises the ancestor branch

**Predicate.** `tools/check-registry-content-r99.py --revision R` is the r98 checker with exactly two
changes:

- The `RC-BEND-SPAN` capture carries a boundary guard (`(?![0-9,-])`) and the binding is marked
  `unique`, so a cell that states a hybrid span (`VARIANTS N01-N04,N05`, the r98 A1 survivor that
  read `PASS 7/7`) reads `RC-CELL-MISSING`, and a cell that mentions `VARIANTS` more than once (the
  r98 same-cell-restatement survivor) reads the new `RC-CELL-AMBIGUOUS`. Both are fail-closed.
- `--selftest` gains `span-hybrid`, `span-restated` and `ancestor` (14 -> 17). The `ancestor` case
  builds a two-branch git fixture and runs this file's real CLI on a revision that is not an ancestor
  of the selected branch; the pristine tool reads rc 2 / `CANNOT-EVALUATE`, the r98 MutRegistry M07
  mutant (ancestor check skipped) reads rc 0 / `PASS`.

**Target.** Landed: `status PASS`, `findings []`, `bindings 7`; `--selftest` `PASS 17/17`; the M07
mutant of this file `FAIL 16/17` with exactly the `ancestor` case red; the r98 checker
(`before/controls/do-nothing-checker-r98.py`) reads `PASS 7/7` on the hybrid and restated fixtures
where r99 reads `FAIL` with exactly one finding (`RC-CELL-MISSING` / `RC-CELL-AMBIGUOUS`); the
coverage gate reads `PASS 160/160 findings 0` at the pre-round tip and its post-settle count
registered.

**Kill rule.** Unmet if the landed run is not PASS with 0 findings; unmet if `--selftest` is not
`PASS 17/17`; unmet if the M07 mutant passes `--selftest` or fails a different case; unmet if the r98
checker is not `PASS` on both capture fixtures, or r99 is not `FAIL` with the frozen single finding
id on each; unmet if the coverage gate does not read `PASS` at the pre-round tip; void if
`tools/check-registry-content-r99.py` differs from the instruments manifest at scoring time.

**Counting command.** `python3 tools/check-registry-content-r99.py --revision <R> --json <out>`;
`python3 tools/check-registry-content-r99.py --selftest`; fixtures built by
`python3 .ufo/waves/round-99/before/dev/make-fixtures.py <dir>`.

**Do-nothing control (committed with this freeze).** `before/controls/do-nothing-checker-r98.py`
(the r98 landed checker).

## R99-D1 repair (routed, not a claim)

The r98 report and SCORECARD cite coverage `PASS 160/160`; the tree holds only the freeze-time
receipts. This round commits the settled-tip coverage receipt for `f107da3a` (the pre-round tip) into
`.ufo/waves/round-99/before/`, and the r98 pointer to a non-committed `after/c2/coverage-tip.json` is
named in the round report and lesson rather than edited (the r98 lesson is append-only).

## Limits (named, not claimed)

- The X/Y **echo** leg has no spelling-targeted committed bend: N09/N11 falsify `visibility_era`
  only. The echo legs are exercised by the blanket `lie-limine-version` wrapper (which fails X, Y,
  Z and LZ) and by the r98-carried fixed-echo attack, not by a one-clause bend of their own.
- C1 keeps the roster at 105; it adds no family and no version spelling.
- C2 binds the same 7 cells of 4 rows. The unbound rows and the three r98-measured C2 gaps
  (uncovered cells, tool+cell co-doctoring, printed-tally parsing) stand unchanged.
- A hybrid cell and a restated cell now read a finding, so a legitimately-written registry cell that
  states two spans in one cell must be rewritten to one span; that is the fail-closed choice, stated.

## Amendment slot

Empty on purpose: the declaration bytes are pinned in `before/instruments.sha256`, so a pre-report
narrowing is an append-only sidecar (`before/plan-amendments-r99.md`) the falsification ledger's
`narrowing` pointers name, never an in-place edit of this file.

## Axis and separability

C1 (depth 8) changes the battery's metadata assertions and its selftest lie kinds; C2 (freshness 9)
changes the registry checker's capture and selftest. They share no instrument: C1's legs read battery
JSON, C2's legs read the registry table and the fixture tools. No axis is harmed: the gate bytes are
unchanged (`7d79ac29…`), the r98 battery keeps its bytes and stays the do-nothing control, the r98
checker keeps its bytes and reads `PASS 7/7` on the landed table, and no corpus entry is removed.
