# ExecRegistry — round 100, wave w1 (C2 landed table / selftest / twelve fixtures / r99 control)

Seat: `ExecRegistry` (executor, leaf). Lane: `tsukuroi-shokunin`, campaign hyaku, round 100,
attempt 1. Working tree at start: detached HEAD `60b5636f`, lane branch `master` =
`69474c55` (= `origin/master`). Scope executed: **C2 only** — the landed table, the `--selftest`
leg, the twelve-fixture matrix, the r99 control readings, in both readings of the live table,
plus the coverage gate.

Lane-state note (adaptation, not this seat's write): the lane HEAD moved during the run — at the
seat's first command it was detached `60b5636f` with in-flight uncommitted `SKILL.md`/`corpus/`
edits; by the topology check HEAD was `69474c55` = `master` = `origin/master` and the tree clean.
Every cited reading is pinned to a revision (committed bytes); the working-tree `--root` reading
was taken on both sides of the move and reads PASS 7/7 for both checkers (`receipts/10-*` before,
`receipts/22-*` after).

Nothing under `tools/`, `SKILL.md`, `corpus/`, `SCORECARD.md`, `LOG.md`, `.ufo/plans/`,
`.ufo/waves/round-100/before/` or `claims.json` was written. No generator
(`make-r100-bends.py` / `make-r9*-bends.py`) was run. No git/jj mutation was run (read-only
`git show`, `git diff`, `git rev-parse`, `git merge-base --is-ancestor` only). No tool was
installed or upgraded (no package manager touched; nothing to record under the tooling
authorization).

## 0. Instrument integrity (gate before any citation)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-100/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r99.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r99.py: OK
tools/check-registry-content-r100.py: OK
tools/make-r100-bends.py: OK
tools/make-r96-bends.py: OK
tools/check-registry-coverage.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r99.py: OK
.ufo/waves/round-100/before/controls/do-nothing-checker-r99.py: OK
.ufo/waves/round-100/before/controls/bends/N12-x-echo.py: OK
.ufo/waves/round-100/before/controls/bends/N13-y-echo.py: OK
.ufo/waves/round-100/before/dev/make-fixtures.py: OK
.ufo/waves/round-100/claims.json: OK
.ufo/plans/round-100.md: OK
```
16/16 OK, rc 0. **PASS.** (`tools/check-registry-content-r100.py` = `7a23a522…`,
`tools/check-registry-content-r99.py` = `b489f5b8…` = the committed control copy,
`tools/check-registry-coverage.py` = `6fcb2d0a…`, `before/dev/make-fixtures.py` = `846c7813…`.)

## 1. Live table — both readings and the control

Commands (run from the lane root; `--json` payload path under the seat dir; every run also
re-run with `TMPDIR=/fast/scratch/hyaku/tsukuroi-r100/ExecRegistry/tmp` and byte-identical):

```
python3 tools/check-registry-content-r100.py --revision 743ce449490f4e9ff004f423ecc3fa456cbc77ec --branch master --json .ufo/waves/round-100/w1/ExecRegistry/c2-content-freeze.json
python3 tools/check-registry-content-r100.py --revision ce73ccaf75d0279385977f03ccb35945c1cf8e07 --branch master --json .ufo/waves/round-100/w1/ExecRegistry/c2-content-tip-r100.json
python3 tools/check-registry-content-r99.py  --revision 743ce449490f4e9ff004f423ecc3fa456cbc77ec --branch master --json .ufo/waves/round-100/w1/ExecRegistry/c2-r99-freeze.json
python3 tools/check-registry-content-r99.py  --revision ce73ccaf75d0279385977f03ccb35945c1cf8e07 --branch master --json .ufo/waves/round-100/w1/ExecRegistry/c2-r99-tip.json
```

Raw stdout of all four (receipts `receipts/tmpdir/01…04`):

```
registry-content: status PASS bindings 7/7 findings 0
rc=0
registry-content: status PASS bindings 7/7 findings 0
rc=0
registry-content: status PASS bindings 7/7 findings 0
rc=0
registry-content: status PASS bindings 7/7 findings 0
rc=0
```

JSON payloads (same four receipts, `--json` files):

| revision | checker | status | bindings | findings | rows | schema |
|---|---|---|---|---|---|---|
| `743ce449` (freeze) | r100 | PASS | 7 | [] | 163 | `tsukuroi-registry-content-r100-v1` |
| `ce73ccaf` (pre-round tip) | r100 | PASS | 7 | [] | 163 | `tsukuroi-registry-content-r100-v1` |
| `743ce449` (freeze) | r99 control | PASS | 7 | [] | 163 | `tsukuroi-registry-content-r99-v1` |
| `ce73ccaf` (pre-round tip) | r99 control | PASS | 7 | [] | 163 | `tsukuroi-registry-content-r99-v1` |

Extra readings, under the L1's ruling (2026-11-08, this seat's dispatch): "the landing tip" is the
**final round-100 lane tip** (`69474c55` and later round-100 commits), **not** the intermediate
`c450cd68` commit. C2 is scored at the freeze tip (`743ce449`) and the final tip; both PASS. The
intermediate `c450cd68` reading is reported raw below and named as the round's disclosed defect
**R100-REGISTRY-ROW-CELL-COUNT**.

| revision | checker | status | rc | counts / finding |
|---|---|---|---|---|
| `c450cd68` (intermediate land commit — NOT the landing tip; defect R100-REGISTRY-ROW-CELL-COUNT) | r100 + r99 | **CANNOT_EVALUATE** | 2 | `E-TABLE SKILL.md: malformed registry row at line 5951` |
| `69474c55` (**landing tip** = final round-100 lane tip) | r100 | PASS 7/7 | 0 | rows 165, findings [] |
| `69474c55` (landing tip) | r99 | PASS 7/7 | 0 | rows 165, findings [] |
| working tree (`--root <lane>`, HEAD `60b5636f` / `69474c55`) | r100 | PASS 7/7 | 0 | findings [] |
| working tree (`--root <lane>`) | r99 | PASS 7/7 | 0 | findings [] |

Receipts: `receipts/09-coverage-*` (coverage), `receipts/11-content-{r100,r99}-c450cd68.txt`,
`receipts/13-content-{r100,r99}-master.{txt,json}`, `receipts/10-live-{r100,r99}-worktree.txt`.

**Expected line: r100 `PASS bindings 7/7 findings 0` at both named revisions → PASS.**
**Expected line: r99 control `PASS 7/7` at both → PASS.**

## 2. `--selftest`

```
$ python3 tools/check-registry-content-r100.py --selftest
clean                PASS
default-cell         PASS
fixtures-cell        PASS
schema-cell          PASS
roster-pinned-cell   PASS
roster-verdict-cell  PASS
cases-cell           PASS
span-cell            PASS
span-gap             PASS
span-gap-lie         PASS
span-hybrid          PASS
span-restated        PASS
span-sep-space       PASS
span-sep-semicolon   PASS
span-sep-and         PASS
span-sep-slash       PASS
span-sep-plus        PASS
span-union           PASS
span-letter-suffix   PASS
span-prose           PASS
span-union-lie       PASS
row-missing          PASS
tool-missing         PASS
derivation-lie       PASS
tally-lie            PASS
ancestor             PASS
selftest PASS 26/26
rc=0
```

```
$ python3 tools/check-registry-content-r99.py --selftest
clean                PASS
default-cell         PASS
fixtures-cell        PASS
schema-cell          PASS
roster-pinned-cell   PASS
roster-verdict-cell  PASS
cases-cell           PASS
span-cell            PASS
span-gap             PASS
span-gap-lie         PASS
span-hybrid          PASS
span-restated        PASS
row-missing          PASS
tool-missing         PASS
derivation-lie       PASS
tally-lie            PASS
ancestor             PASS
selftest PASS 17/17
rc=0
```

**Expected line: r100 `PASS 26/26`, r99 `17/17` → PASS.** Receipts
`receipts/tmpdir/05-selftest-r100.txt`, `receipts/tmpdir/06-selftest-r99.txt` (identical to the
first run `receipts/05…`, `receipts/06…`; both clean up their temp trees — zero leftovers under
the scratch `tmp/`).

Note (case coverage): the r100 addition is 9 cases (`span-sep-space`, `span-sep-semicolon`,
`span-sep-and`, `span-sep-slash`, `span-sep-plus`, `span-union`, `span-letter-suffix`,
`span-prose`, `span-union-lie`), 17 + 9 = 26.

## 3. Twelve fixtures — build and matrix

Build (the pinned builder, which calls the frozen r100 checker's own `build_fixture`; no
hand-copied bytes, and **no generator** was run):

```
$ python3 .ufo/waves/round-100/before/dev/make-fixtures.py /fast/scratch/hyaku/tsukuroi-r100/ExecRegistry/fixtures
/fast/scratch/.../fixtures/SEP-SPACE
… twelve absolute paths printed, rc=0
```
Receipt `receipts/16-fixtures-built.txt`; fixture `SKILL.md` + `tools/make-r96-bends.py` sha256s in
`receipts/14-fixture-sha256.txt`; the twelve `SKILL.md` and `make-r96-bends.py` copies are under
`receipts/fixture-skill/` (so the cells are re-readable without the scratch tree).

Each fixture was read by **both** checkers with `--root` (24 runs), one JSON per
(checker, fixture) under `receipts/fixtures-json-tmpdir/` (+ the identical earlier set
`receipts/fixtures-json/`). Table (`receipts/15b-fixture-matrix-tmpdir.txt`):

| fixture | r99 status / id | r100 status / id | frozen dev table |
|---|---|---|---|
| SEP-SPACE | FAIL `RC-CELL-MISSING` | PASS `none` | MATCH |
| SEP-SEMICOLON | FAIL `RC-CELL-MISSING` | PASS `none` | MATCH |
| SEP-AND | FAIL `RC-VALUE-MISMATCH` | PASS `none` | MATCH |
| SEP-SLASH | FAIL `RC-CELL-MISSING` | PASS `none` | MATCH |
| SEP-PLUS | FAIL `RC-CELL-MISSING` | PASS `none` | MATCH |
| UNION | FAIL `RC-VALUE-MISMATCH` | PASS `none` | MATCH |
| LETTER | FAIL `RC-CELL-MISSING` | FAIL `RC-CELL-MISSING` | MATCH |
| PROSE | FAIL `RC-CELL-MISSING` | FAIL `RC-CELL-MISSING` | MATCH |
| UNION-LIE | FAIL `RC-VALUE-MISMATCH` | FAIL `RC-VALUE-MISMATCH` | MATCH |
| HYBRID | FAIL `RC-CELL-MISSING` | FAIL `RC-VALUE-MISMATCH` | MATCH |
| RESTATED | FAIL `RC-CELL-AMBIGUOUS` | FAIL `RC-CELL-AMBIGUOUS` | MATCH |
| GAP | PASS `none` | PASS `none` | MATCH |

Mechanical comparison against `.ufo/waves/round-100/before/dev/c2-fixtures.txt`:
`DEV_MISMATCHES=0 []` (`receipts/17-fixture-matrix-vs-dev.txt`). The 24 JSON payloads are
byte-identical between the two runs (default TMPDIR vs scratch TMPDIR), 24/24.

Raw finding details of the fail-closed cells (r100):

```
LETTER     RC-CELL-MISSING    SKILL.md:10 :: make-r96-bends cell 5 label set: token 'N01a-N03' is not an N-label or N-label range
PROSE      RC-CELL-MISSING    SKILL.md:10 :: make-r96-bends cell 5 label set: token 'through' is not an N-label or N-label range
UNION-LIE  RC-VALUE-MISMATCH  SKILL.md:10 :: RC-BEND-SPAN states N01,N02,N04, tools/make-r96-bends.py derives N01,N02,N04,N05 (missing N05, extra -)
HYBRID     RC-VALUE-MISMATCH  SKILL.md:10 :: RC-BEND-SPAN states N01,N02,N03,N04,N05, tools/make-r96-bends.py derives N01,N02,N03,N04 (missing -, extra N05)
RESTATED   RC-CELL-AMBIGUOUS  SKILL.md:10 :: make-r96-bends cell 5 mentions 'VARIANTS' 2 times; the first mention is not the cell's value
```
And the r99 control's details on the six acceptance cells:

```
SEP-SPACE/SEMICOLON/SLASH/PLUS  RC-CELL-MISSING   :: cell 5 no longer states 'VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))(?![0-9,-])'
SEP-AND   RC-VALUE-MISMATCH :: RC-BEND-SPAN states 'N01-N02', tools/make-r96-bends.py derives 'N01-N03'
UNION     RC-VALUE-MISMATCH :: RC-BEND-SPAN states 'N01-N02', tools/make-r96-bends.py derives 'N01,N02,N04,N05'
```

**Expected lines: six acceptance cells PASS on r100 with a finding on r99 → PASS; LETTER/PROSE
`RC-CELL-MISSING` → PASS; UNION-LIE/HYBRID `RC-VALUE-MISMATCH` → PASS; RESTATED
`RC-CELL-AMBIGUOUS` → PASS; GAP PASS on both → PASS.**

## 4. The six acceptance cells, by eye (exact cell text and key list)

Fixture table header (all twelve fixtures): `| Name | Kind | Entry command | Verdict map |
Self-test | Pinned values | Write scope | Owner |`; the bound cell is cell index 5 on the
`make-r96-bends` row at `SKILL.md:10`.

| tag | cell 5 text (verbatim) | `VARIANTS` keys | derived set | declared set | result |
|---|---|---|---|---|---|
| SEP-SPACE | `VARIANTS N01 N02 N03` | `N01-one`, `N02-two`, `N03-three` | N01,N02,N03 | N01,N02,N03 | equal → PASS |
| SEP-SEMICOLON | `VARIANTS N01; N02; N03` | `N01-one`, `N02-two`, `N03-three` | N01,N02,N03 | N01,N02,N03 | equal → PASS |
| SEP-AND | `VARIANTS N01-N02 and N03` | `N01-one`, `N02-two`, `N03-three` | N01,N02,N03 | N01,N02,N03 | equal → PASS |
| SEP-SLASH | `VARIANTS N01/N02/N03` | `N01-one`, `N02-two`, `N03-three` | N01,N02,N03 | N01,N02,N03 | equal → PASS |
| SEP-PLUS | `VARIANTS N01 + N02 + N03` | `N01-one`, `N02-two`, `N03-three` | N01,N02,N03 | N01,N02,N03 | equal → PASS |
| UNION | `VARIANTS N01-N02 and N04-N05` | `N01-one`, `N02-two`, `N04-four`, `N05-five` | N01,N02,N04,N05 | N01,N02,N04,N05 | equal → PASS |

Fail-closed siblings for the same cell, same file: `LETTER` `VARIANTS N01a-N03` (keys N01-N03),
`PROSE` `VARIANTS N01 through N03` (keys N01-N03), `UNION-LIE` `VARIANTS N01-N02 and N04` (keys
N01,N02,N04,N05), `HYBRID` `VARIANTS N01-N04,N05` (keys N01-N04), `RESTATED`
`VARIANTS N01,N03 then VARIANTS N01-N03` (keys N01,N03), `GAP` `VARIANTS N01,N03` (keys N01,N03).
Receipt `receipts/08-fixture-cells-and-variants.txt`; file copies `receipts/fixture-skill/`.

## 5. Coverage gate

The seat's literal command was issued first, and the tool **has no `--json` option** (its parser:
`--revision | --selftest`, `--branch`, `--baseline-tools`, `--audit-live-map`); argparse rejected
the unknown flag under `exit_on_error=False` and the tool emitted its own usage payload:

```
$ python3 tools/check-registry-coverage.py --revision 743ce449… --json …/coverage-freeze.json
{"branch":"master","branch_tip":null,"counts":{"findings":1,"missing":0,"registered":0,"rows_total":0,"tools_total":0},"findings":[{"detail":"--revision REV or --selftest required","id":"E-CLI","site":"cli"}],"revision":null,"status":"CANNOT_EVALUATE"}
rc=2
```
Receipt `receipts/07-coverage-freeze.txt`. The valid form (stdout is the JSON payload) is:

```
$ python3 tools/check-registry-coverage.py --revision 743ce449490f4e9ff004f423ecc3fa456cbc77ec
{"branch":"master","branch_tip":"69474c55…","counts":{"findings":2,"missing":2,"registered":163,"rows_total":163,"tools_total":165},"findings":[{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/check-registry-content-r100.py"},{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/make-r100-bends.py"}],"revision":"743ce449…","status":"FAIL"}
rc=1
```

Readings across the round's commits (receipts `09-*`, `12-*`):

| revision | status | rc | registered / rows_total / tools_total | missing | findings |
|---|---|---|---|---|---|
| `743ce449` (freeze) | FAIL | 1 | 163 / 163 / 165 | 2 | the two new r100 tools have no operative row yet |
| `ce73ccaf` (pre-round tip) | PASS | 0 | 163 / 163 / 163 | 0 | [] |
| `60b5636f` (wave dispatch, same table as freeze) | FAIL | 1 | 163 / 163 / 165 | 2 | same two rows |
| `c450cd68` (intermediate commit; defect R100-REGISTRY-ROW-CELL-COUNT) | CANNOT_EVALUATE | 2 | 0 / 0 / 0 | 0 | `E-REGISTRY-TABLE SKILL.md: malformed registry row at line 5951` |
| `69474c55` (**landing tip**, final round-100 lane commit) | **PASS** | 0 | **165 / 165 / 165** | 0 | [] |

**Expected line: coverage `PASS` with the freeze-revision counts → PASS at the landing tip
`69474c55`** (`165/165/165` = the pre-round `163` plus the round's two new tools, i.e. the
freeze's counts), **FAIL at the literal freeze revision `743ce449`** (the landing rows exist only
from the intermediate `c450cd68` onward). Reported raw; the freeze-revision failure is the
pre-landing state, not a regression.

## 6. Disclosed defect `R100-REGISTRY-ROW-CELL-COUNT` (intermediate commit; raw, repaired)

`c450cd68` — an **intermediate** round-100 commit, not the landing tip — writes the
`check-registry-content-r100` row with **7 of 8 cells** (the write-scope cell is absent). Both
content checkers therefore read `CANNOT_EVALUATE` (`E-TABLE`, `malformed registry row at line
5951`) at that revision, and the coverage gate reads `E-REGISTRY-TABLE` for the same row. This is
the round's disclosed defect, **R100-REGISTRY-ROW-CELL-COUNT**; it is repaired at the landing tip
`69474c55` by a one-line fix that adds the cell, where both checkers read PASS 7/7 rows 165 and
coverage reads PASS 165/165/165:

```
$ git diff --stat c450cd68 69474c55 -- SKILL.md
 SKILL.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```
Cell count measured with the instrument's own `split_row`: `c450cd68` 7 cells, no write-scope;
`69474c55` 8 cells, write-scope present. Receipts `receipts/18-land-fix-diff.txt`,
`receipts/20-land-row-cells.txt`, `receipts/11-content-*`, `receipts/13-content-*`.
Per the L1 ruling (2026-11-08): "the landing tip" is the final round-100 lane tip (`69474c55` and
later round-100 commits); C2 is scored at `743ce449` and `69474c55`, both PASS. The intermediate
`c450cd68` `CANNOT_EVALUATE` reading above is disclosed raw and is **not** a landing-tip failure.

## 7. Byte-level re-derivation of the binding (QUALITY 141)

Measured with `bytes.find` on the pinned bytes (`receipts/19-byte-anchors.txt`):

```
tools/check-registry-content-r100.py  bytes 38009  sha256 7a23a522…
  byte 12025  'TOKEN = re.compile'            (N<digits>(?:-N<digits>)? token)
  byte 12073  'SEPARATORS = re.compile'       (,\s ; + / \band\b)
  byte 12134  'def parse_label_set'
  byte 16954  '"set": True, "derive": "variant_labels"'   (the RC-BEND-SPAN binding)
  byte 21232  'declared_set != derived_set'   (the equality arm → RC-VALUE-MISMATCH)
  byte 19386  'mentions = len(re.findall'     (the >1 mention arm → RC-CELL-AMBIGUOUS)
  byte  4774  'RC-CELL-AMBIGUOUS'
tools/check-registry-content-r99.py   bytes 30756  sha256 b489f5b8…  (= control copy)
  byte 14208  '"capture": r"VARIANTS'         (r99 span capture: N[0-9]+(-N[0-9]+|(,N[0-9]+)+))
  byte  9563  'def derive_variant_span'
  byte 14310  '"unique": True'
  byte  4773  'RC-CELL-AMBIGUOUS'
```
The r99 capture's alphabet is `N<digits>` joined by `,`/`-` only (no whitespace/`;`/`+`/`/`/
`and`), which is exactly the round-99 named limit the r100 label set closes; the six acceptance
cells and the five fail-closed controls above are the instrument-measured witness.

## 8. What this seat did not do (scope, honestly)

- Did not run C1 (the gate/battery/bends legs) — another seat's surface; no battery JSON read or
  produced here.
- Did not run any `make-r*-bends.py` generator and did not create or commit in any git repo.
- Did not edit any instrument, registry, corpus, plan, claim or wave `before/` byte.
- Did not install/upgrade any tool (no pacman, no `uv tool`, no `npx`).
- First selftest/fixture invocations used the default TMPDIR; the cited runs are the
  `TMPDIR=/fast/scratch/hyaku/tsukuroi-r100/ExecRegistry/tmp` re-runs, and the two runs are
  byte-identical (verified by `diff`), with zero temp leftovers.

## 9. Receipts (all under this seat dir)

| path | content |
|---|---|
| `receipts/tmpdir/01-live-r100-freeze.txt`, `02-live-r100-tip.txt` | r100 live table at `743ce449`, `ce73ccaf` (stdout + rc) |
| `receipts/tmpdir/03-live-r99-freeze.txt`, `04-live-r99-tip.txt` | r99 control on the same table |
| `c2-content-freeze.json`, `c2-content-tip-r100.json`, `c2-r99-freeze.json`, `c2-r99-tip.json` | the four `--json` payloads |
| `receipts/tmpdir/05-selftest-r100.txt`, `06-selftest-r99.txt` | every selftest line + tally + rc |
| `receipts/16-fixtures-built.txt`, `receipts/14-fixture-sha256.txt` | fixture build output and hashes |
| `receipts/15b-fixture-matrix-tmpdir.txt` (+ `15-fixture-matrix.txt`) | twelve-fixture matrix |
| `receipts/fixtures-json-tmpdir/*.json` (+ `receipts/fixtures-json/`) | one JSON per (checker, fixture), 24 each |
| `receipts/08-fixture-cells-and-variants.txt`, `receipts/fixture-skill/` | cell 5 text + `VARIANTS` keys per fixture |
| `receipts/17-fixture-matrix-vs-dev.txt` | matrix vs the frozen dev table (`DEV_MISMATCHES=0`) |
| `receipts/07-coverage-freeze.txt`, `07b-coverage-freeze-valid.txt`, `coverage-freeze.json`, `receipts/07-coverage-freeze.rc.txt` | coverage CLI deviation + valid freeze reading |
| `receipts/09-coverage-{ce73ccaf,60b5636f,c450cd68}.json`, `receipts/12-coverage-master-69474c55.json` | coverage at the other commits |
| `receipts/11-content-{r100,r99}-c450cd68.txt`, `receipts/13-content-{r100,r99}-master.{txt,json}`, `receipts/10-live-{r100,r99}-worktree.txt` | live-table readings at the intermediate commit / landing tip / worktree |
| `receipts/18-land-fix-diff.txt`, `receipts/20-land-row-cells.txt` | the 7→8-cell land fix |
| `receipts/19-byte-anchors.txt` | byte-level binding anchors |
| `receipts/21-instruments-recheck.txt` | `sha256sum -c` re-run after all measurements (16/16 OK, rc 0) |
| `receipts/22-live-{r100,r99}-worktree-after-head-move.txt` | working-tree table on the clean `69474c55` tree |

{"seat":"ExecRegistry","verdict":"met","notes":"C2 met at the scored revisions under the L1 ruling of 2026-11-08 (landing tip = the final round-100 lane tip): freeze tip 743ce449 and final tip 69474c55 both PASS, r100 bindings 7/7 findings 0 (rows 163 / 165), r99 control PASS 7/7 at both; selftest PASS 26/26 (r99 17/17) with every line recorded; all 12 fixture readings reproduce the frozen dev table exactly (DEV_MISMATCHES=0) - six acceptance cells PASS on r100 with r99 ids RC-CELL-MISSING (SPACE, SEMICOLON, SLASH, PLUS) and RC-VALUE-MISMATCH (AND, UNION); LETTER/PROSE RC-CELL-MISSING, UNION-LIE/HYBRID RC-VALUE-MISMATCH (HYBRID r99 RC-CELL-MISSING), RESTATED RC-CELL-AMBIGUOUS, GAP PASS both. Raw disclosures: (1) coverage at the literal freeze revision 743ce449 is FAIL rc 1 with 2 REGISTRY-ROW-MISSING (the landing rows exist only from the intermediate c450cd68 onward) - it reads PASS 165/165/165 at the landing tip 69474c55 and PASS 163/163/163 at ce73ccaf; (2) R100-REGISTRY-ROW-CELL-COUNT: the intermediate commit c450cd68 has a 7-of-8-cell check-registry-content-r100 row, so both content checkers read CANNOT_EVALUATE E-TABLE at that revision until 69474c55 adds the write-scope cell - disclosed, not a landing-tip failure; (3) the coverage tool has no --json flag, so the seat-spec command form returns its own E-CLI CANNOT_EVALUATE rc 2 (valid stdout form used). No instrument was edited; instrument manifest 16/16 OK."}
