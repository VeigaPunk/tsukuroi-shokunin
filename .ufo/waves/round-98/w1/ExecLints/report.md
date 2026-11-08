# ExecLints — round-98 wave w1 gate-hygiene receipt

Seat: ExecLints (instrument-integrity receipt; no claim rests on this seat).
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
Scratch: `/fast/scratch/hyaku/tsukuroi-r98/ExecLints` (removed before yield).

Reads first (already read): `.ufo/waves/round-98/claims.json`, `.ufo/plans/round-98.md`,
`.ufo/waves/round-98/before/instruments.sha256`, `corpus/lessons/round-97-verifier-spotcheck.md`,
`corpus/QUALITY.md` 139–141 (as routed; raw lines 139–141 = criteria 71–73 in current numbering —
byte/quote offsets below are measured at the byte level per QUALITY 141).

Tooling authorization note: read `/home/vgpnk/.omp/agent/RULES.md`. No tool installs were needed
or performed; `python3` 3.14.8 used as found. pacman was not invoked. No `sudo`.

## 1. Manifest

Command: `sha256sum -c .ufo/waves/round-98/before/instruments.sha256`
Receipt: `receipts/01-sha256sum-c.txt`. Raw output (27 lines, rc=0):

```text
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r98.py: OK
tools/make-r98-bends.py: OK
tools/check-registry-content-r98.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-98.md: OK
.ufo/waves/round-98/before/plan-frozen.md: OK
.ufo/waves/round-98/claims.json: OK
.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py: OK
.ufo/waves/round-98/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-98/before/controls/do-nothing-checker-r97.py: OK
.ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py: OK
.ufo/waves/round-98/before/controls/bends/N08-echo-norm.py: OK
.ufo/waves/round-98/before/registry-baseline-r98.json: OK
.ufo/waves/round-98/before/fixtures/build-doctored-fixture-r98.sh: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D1: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2lie: OK
.ufo/waves/round-98/before/dev/c1-gate-runs3.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c2-selftest-r98.txt: OK
.ufo/waves/round-98/before/dev/c2-selftest-r97.txt: OK
.ufo/waves/round-98/before/dev/c2-doctored-summary.txt: OK
```

PASS: all 27 entries OK, including the unchanged gate `tools/check-limine-pins.py`
(`7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32`, matching the seat spec).

## 2. py_compile

Command: `for f in <six manifest instruments>; do python3 -m py_compile "$f"; done`, then `rm -rf tools/__pycache__`
Receipt: `receipts/02-pycompile.txt`. All six `rc=0`; `tools/__pycache__` removed; confirmed gone
(`ls: cannot access 'tools/__pycache__': No such file or directory`). PASS.

## 3. Gate selftest + byte identity

Commands:
- `python3 tools/check-limine-pins.py --selftest` → last line `selftest PASS 39/39`, gate rc=0
  (receipt `receipts/03a-gate-selftest.txt`). PASS (expected `PASS 39/39`).
- `cmp tools/check-limine-pins.py .ufo/waves/round-98/before/controls/do-nothing-gate.py` →
  `cmp_rc=0 IDENTICAL`. sha256 of both: `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32`.
  PASS.

## 4. Coverage gates at b3be3f90

- `python3 tools/check-registry-coverage.py --revision b3be3f90` →
  `{"status":"PASS","counts":{"findings":0,"missing":0,"registered":157,"rows_total":157,"tools_total":157},...}`
  coverage rc=0 (receipt `receipts/04a-coverage.txt`). PASS (157/157).
- `python3 tools/check-knowledge-header.py --revision b3be3f90` →
  `{"clean_count":113,"complete_count":113,"finding_count":0,"note_count":113,...}`, knowledge rc=0
  (receipt `receipts/04b-knowledge-header.txt`). PASS.
- Calibration leg item 6: `python3 tools/check-r96-calibration.py --root .` →
  `{"status":"PASS","findings":[],"unreadable":[]}`, cal rc=0 (receipt `receipts/06a-calibration.txt`). PASS.
- Line endings item 6: `python3 tools/check-line-endings-r64.py --check` →
  `CHECK_LINE_ENDINGS: PASS (504 file(s) checked, 0 violation(s))`, le rc=0
  (receipt `receipts/06b-line-endings.txt`). PASS.

## 5. Seven bound registry cells re-derived by hand at b3be3f90

Bytes extracted with read-only `git show b3be3f90:<path>` to scratch (`receipts/05-prep.txt`:
`check-limine-pins.py` sha256 `7d79ac29…` = manifest value; `check-r96-calibration.py`
`7ff63524…` = manifest value). Operative SKILL.md rows are at lines 5923/5938/5939/5940/5943
(`receipts/05f-skill-offsets.txt`, `05g`, `05h`). BINDINGS read from the b3be3f90 checker
`check-registry-content.py`: 7 entries; the derivation functions are at lines 130–190 of that file.

Derivation method (hand, per assignment item 5): argparse default via regex on
`add_argument("--limine-version", default=...)`; selftest tallies via running each tool's
`--selftest` and parsing the printed `selftest PASS N/N` plus static AST decomposition; schema
literal via regex; roster size by AST over `FAMILY_ROSTER` and, second way, over `FAMILIES` keys;
VARIANTS span via AST over the `VARIANTS` dict keys (contiguous → `N01-N04`, else comma form).

| # | Binding ID | SKILL cell (captured) | Re-derived from tool bytes at b3be3f90 | Result |
|---|---|---|---|---|
| 1 | RC-ENTRY-DEFAULT | `auto` (cell 2, line 5923) | `auto` (`add_argument("--limine-version", default="auto"`, byte offset 28594 in `check-limine-pins.py`) | PASS match |
| 2 | RC-SELFTEST-COUNT | `39` (cell 4, line 5923, `(39 fixtures`) | `selftest PASS 39/39` (rc=0); static AST: 36 `case(` calls + 4 `results.append` sites = 40 — see note | PASS match (run tally) |
| 3 | RC-SCHEMA | `tsukuroi-limine-pins-v3` (cell 5, line 5923) | `tsukuroi-limine-pins-v3` (line 315, byte offset 16863) | PASS match |
| 4 | RC-ROSTER-VERDICT | `103` (cell 3, line 5938, `FAMILY_ROSTER, 103,`) | AST `FAMILY_ROSTER` tuple len 103 | PASS match |
| 5 | RC-ROSTER-PINNED | `103` (cell 5, line 5938, `roster 103 (`) | AST #2: `FAMILIES` dict 103 keys | PASS match |
| 6 | RC-CAL-SELFTEST | `7` (cell 4, line 5940, `(7 cases`) | `selftest PASS 7/7` (rc=0; clean + F1–F6) | PASS match |
| 7 | RC-BEND-SPAN | `N01-N04` (cell 5, line 5939) | AST `VARIANTS` keys N01,N02,N03,N04 → contiguous → `N01-N04` | PASS match |

Receipts: `receipts/05b-gate-selftest-rev.txt` (39/39 at pinned rev), `05c` (7/7 at pinned rev),
`05d-ast.txt` (103/103, VARIANTS keys), `05j-seven-cell.txt` (full derivation run), `05k`/`05l`.

Note on cell 2 static decomposition: a naive `grep -c "case("` (37) or AST walk over all
`append` (14) misleads. The exact decomposition is 36 `case(` calls (each appends exactly one
result through the inner `results.append((name, ok, …))` at line 362) plus 3 top-level
`results.append` sites (`version-parser`, `probe-version`, `conf-absent`) = 39. That matches the
run tally `selftest PASS 39/39` and the r97 verifier's independent re-derivation. No mismatch.

Also verified incidentally (not a claim): `tools/check-registry-content-r98.py --selftest` →
`selftest PASS 14/14` rc=0 (`receipts/05m-r98-selftest.txt`), and
`--revision b3be3f90` → `status PASS bindings 7/7 findings 0`. Cross-checks against C2's
frozen targets; no drift.

## 6. Verdict

No drift between any manifest entry and its file. Gate byte-identical to the do-nothing control.
All seven cells re-derive. All standing gates green.

Receipts (all under `.ufo/waves/round-98/w1/ExecLints/receipts/`): `00-index.txt`,
`01-sha256sum-c.txt`, `02-pycompile.txt`, `03a-gate-selftest.txt`, `04a-coverage.txt`,
`04b-knowledge-header.txt`, `05-prep.txt`, `05b-gate-selftest-rev.txt`, `05c-cal-selftest-rev.txt`,
`05d-ast.txt`, `05e-skill-rows.txt`, `05f-skill-offsets.txt`, `05g-skill-lines.txt`,
`05h-skill-cols.txt`, `05i-derive1.txt`, `05j-seven-cell.txt`, `05k-append.txt`,
`05l-results-append.txt`, `05m-r98-selftest.txt`, `06a-calibration.txt`, `06b-line-endings.txt`.

{"seat":"ExecLints","verdict":"met","notes":"manifest 27/27 OK; py_compile 6x rc=0 (__pycache__ removed); gate selftest PASS 39/39 rc=0 and cmp IDENTICAL (7d79ac29); coverage PASS 157/157; knowledge-header rc=0 (113/113); calibration PASS; line-endings PASS 504 files; seven bound cells re-derived by hand at b3be3f90 — all match (auto, 39, tsukuroi-limine-pins-v3, 103 x2, 7, N01-N04); r98 checker selftest PASS 14/14 and content PASS 7/7 at b3be3f90; no drift, no tool installs; scratch removed"}
