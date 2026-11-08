# Round 99 — w1 seat ReviewRegistry — C2 capture attack

Lane `tsukuroi-shokunin`, campaign hyaku, round 99, wave w1. Seat **ReviewRegistry** (roster id
`ReviewRegistry-3`), reviewer. Target: *"Attack C2's capture: forge cells and revisions the round did
not think of, and say exactly what each reads."*

Judge axes: depth, freshness. Leaf member — no subagent dispatch. All fixtures and git commits were
made **only** under `/fast/scratch/hyaku/tsukuroi-r99/ReviewRegistry` (toplevel asserted before every
commit; the driver prints it) and that scratch tree was deleted before yield. Nothing outside
`.ufo/waves/round-99/w1/ReviewRegistry/` and `.ufo/waves/round-99/w1/ReviewRegistry.md` was written.
No `git`/`jj` mutation was run in the lane; `git init/add/commit/tag/checkout` ran only inside the
scratch fixture repo.

## 0. Instrument integrity (before any measurement)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-99/before/instruments.sha256
tools/limine-pin-battery-r99.py: OK
tools/make-r99-bends.py: OK
tools/check-registry-content-r99.py: OK
tools/check-limine-pins.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-99/before/controls/do-nothing-checker-r98.py: OK
.ufo/waves/round-99/before/controls/bends/N09-y-era.py: OK
.ufo/waves/round-99/before/controls/bends/N11-x-era.py: OK
.ufo/waves/round-99/before/dev/make-fixtures.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/plans/round-99.md: OK
```

**PASS 16/16** (receipt: `receipts/byte-anchors.txt`).

Instrument identity (one canonical runtime): the tree's `tools/check-registry-content-r99.py` is
`b489f5b86fa2fa706698ee32ce05cdefa514e9e7a17d4c0af537535bc597d20d` = the manifest; the r98 do-nothing
control in `before/controls/` is `5bb1441e…` = `tools/check-registry-content-r98.py` (byte-identical
copy, not a reroute). The diff r98→r99 contains the two declared changes (capture guard + `unique`; the `ancestor` case
with `span-hybrid`/`span-restated`) plus docstring text, the `HYBRID`/`RESTATED` fixture bodies, a
selftest tempdir-prefix rename and the payload schema token `…-r97-v1`→`…-r99-v1` (neither affects a
verdict). `diff -u` was read in full; the only `BINDINGS` delta is the `RC-BEND-SPAN` capture +
`"unique": True` — no other binding, capture, deriver or row/column selector changed.

Byte anchors on the pinned bytes (QUALITY 141, `grep -Fabo`, byte offsets not string indices):
`12446` `"merge-base", "--is-ancestor"`; `14221` `VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))`;
`14265` `(?![0-9,-])`; `14310` `"unique": True`; `16685` `if binding.get("unique")`.

## 1. The claim's own C2 legs (re-derived, not trusted)

| Leg | Command | Raw reading | Expected | Verdict |
|---|---|---|---|---|
| landed content at pre-round tip | `python3 tools/check-registry-content-r99.py --revision f107da3afe511f7db8cdc30235a992b774903158 --json …` | `status PASS bindings 7/7 findings 0`, rows 160, rc 0 | PASS / 0 findings / 7 bindings | **PASS** |
| r98 control at same tip | `python3 tools/check-registry-content-r98.py --revision f107da3a…` | `status PASS bindings 7/7 findings 0`, rc 0 | PASS | **PASS** |
| committed `hybrid` fixture | `make-fixtures.py <scratch>/fx` then `--root fx/hybrid` on both checkers | r98 `PASS bindings 7/7 findings 0` rc 0; r99 `FINDING RC-CELL-MISSING SKILL.md:10 …` rc 1 | r98 PASS, r99 FAIL one frozen id | **PASS** |
| committed `restated` fixture | same | r98 `PASS bindings 7/7 findings 0` rc 0; r99 `FINDING RC-CELL-AMBIGUOUS SKILL.md:10 make-r96-bends cell 5 mentions 'VARIANTS' 2 times…` rc 1 | r98 PASS, r99 FAIL one frozen id | **PASS** |
| r99 `--selftest` | `python3 tools/check-registry-content-r99.py --selftest` | 17 case lines all PASS, `selftest PASS 17/17`, rc 0 | PASS 17/17 | **PASS** |
| r98 `--selftest` | `python3 tools/check-registry-content-r98.py --selftest` | 14 case lines all PASS, `selftest PASS 14/14`, rc 0 | PASS 14/14 | **PASS** |
| M07 direction (own re-derived mutant: `merge-base --is-ancestor` refusal replaced, nothing else) | `python3 receipts/m07-ancestor-skip-mutant.py --selftest` | `ancestor FAIL rc=0 registry-content: status PASS bindings 7/7 findings 0`; `selftest FAIL 16/17`, rc 1 | FAIL 16/17, exactly `ancestor` red | **PASS** |

Receipts: `receipts/landed-tip.txt`, `receipts/landed-tip-r99.json`, `receipts/landed-tip-r98.json`,
`receipts/committed-fixtures.txt`, `receipts/committed-hybrid-{r98,r99}.json`,
`receipts/committed-restated-{r98,r99}.json`, `receipts/selftests.txt`,
`receipts/m07-mutant-selftest.txt`, `receipts/m07-ancestor-skip-mutant.py`,
`receipts/m07-mutant.diff`, `receipts/m07-mutant.sha256`
(`fda4e047ed65e2fab41b9d9a97580a921673fdd13290678d0e163ef6d5d6d67b`).

Every frozen C2 leg therefore reproduces. The rest of this seat attacks the capture *beyond* the
frozen legs.

## 2. Forged-cell matrix

Driver: `receipts/drivers/forge.py` (matrix 1), `forge2.py` (matrix 2), and the inline batch recorded in
`receipts/forge-matrix3.json` + `receipts/forge-run-3.txt`. Each case is a scratch copy of a
committed fixture base (`clean` / `gap` / `hybrid` / `restated`) with the `make-r96-bends` tool's
`VARIANTS` keys replaced and the `Pinned values` cell (cell index 5) rewritten; both checkers then run
`--root <case> --json …`. `derived` is this seat's own AST re-derivation of the span from the case's
tool bytes (independent of the checker's `derive_variant_span`).

Legend for **fail-closed?**: `closed-correct` = FAIL and the stated value really differs from the
derived one; `closed-overstrict` = FAIL although the stated value is right and only the spelling is
outside the capture (false red, no false green); `GREEN` = PASS.

| # | shape (cell text) | keys → derived | r98 reading | r99 reading | r99 finding id | fail-closed? |
|---|---|---|---|---|---|---|
| a | `VARIANTS N01-N04,N05` | N01-N04 | **PASS** rc 0, `[]` | **FAIL** rc 1 | `RC-CELL-MISSING` | closed-correct (**r98 survivor closed**) |
| b | `VARIANTS N01,N03 then VARIANTS N01-N03` | N01,N03 | **PASS** rc 0, `[]` | **FAIL** rc 1 | `RC-CELL-AMBIGUOUS` | closed-correct (**r98 survivor closed**) |
| c | `VARIANTS N01,N03,N05` | N01-N05 | FAIL `RC-VALUE-MISMATCH` | FAIL `RC-VALUE-MISMATCH` | `RC-VALUE-MISMATCH` | closed-correct (N02/N04 missing from the stated list) |
| d | `VARIANTS N01, N03` | N01,N03 | FAIL `RC-CELL-MISSING` | FAIL `RC-CELL-MISSING` | `RC-CELL-MISSING` | closed-overstrict |
| e | `VARIANTS n01-n03` | N01-N03 | FAIL `RC-CELL-MISSING` | FAIL `RC-CELL-MISSING` | `RC-CELL-MISSING` | closed-overstrict |
| f | `VARIANTS N01-N04 and VARIANTS N01-N04` | N01-N04 | **PASS** rc 0, `[]` | **FAIL** rc 1 | `RC-CELL-AMBIGUOUS` | closed-correct (**r98 survivor closed**) |
| g | `pinned values N01-N04` (no `VARIANTS` token) | N01-N04 | FAIL `RC-CELL-MISSING` | FAIL `RC-CELL-MISSING` | `RC-CELL-MISSING` | closed-overstrict |
| g1 | `VARIANTS N01-N04;` | N01-N04 | PASS rc 0 | PASS rc 0 | — | GREEN, legitimate (delimiter) |
| g2 | `VARIANTS N01-N04.` | N01-N04 | PASS rc 0 | PASS rc 0 | — | GREEN, legitimate (delimiter) |
| g3 | `VARIANTS N01-N04extra` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — token truncated after `N04`** |
| g4 | `VARIANTS N01–N03` (en dash, U+2013) | N01-N03 | FAIL `RC-CELL-MISSING` | FAIL `RC-CELL-MISSING` | `RC-CELL-MISSING` | closed-overstrict |
| x1 | `VARIANTS N01-N04 N05` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — extra label `N05` dropped** |
| x2 | `VARIANTS N01-N04,N05 and VARIANTS N01-N04` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — hybrid span stated, unbound** |
| x3 | `VARIANTS N01-N04 and VARIANTS N01-N04,N05` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — hybrid span stated, unbound** |
| x4 | `VARIANTS N01-N04 and VARIANTS n01-n03` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — contradictory 2nd mention** |
| x5 | `VARIANTS N01-N04 and VARIANTS N01, N03` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — contradictory 2nd mention** |
| x6 | `VARIANTS N01-N04x` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — token truncated** |
| x7 | `VARIANTS N01-N04 \| VARIANTS N01-N05` | N01-N04 | PASS rc 0 | **FAIL** rc 1 | `RC-CELL-AMBIGUOUS` | closed-correct (escaped pipe does not hide it) |
| x8 | cell 5 `VARIANTS N01-N04`, cell 6 `VARIANTS N01-N05` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | GREEN, outside `BINDINGS` scope (other column) |
| x9 | cell 5 `VARIANTS N01-N04`, cell 3 `VARIANTS N01-N05 0 ok;…` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | GREEN, outside `BINDINGS` scope (other column) |
| x10 | `VARIANTS N01-N04 (keys N01-N05)` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — second span stated in prose** |
| y1 | `VARIANTS N01-N04; N05` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — extra label after `;`** |
| y2 | `VARIANTS N01-N04+N05` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — extra label after `+`** |
| y3 | `VARIANTS N01-N04/N05` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — extra label after `/`** |
| y4 | `VARIANTS N01-N04 and N05` | N01-N04 | PASS rc 0 | **PASS rc 0** | — | **GREEN — extra label after `and`** |
| y5 | `VARIANTS N01,N02,N03,N04,N05` | N01-N05 | FAIL `RC-VALUE-MISMATCH` | FAIL `RC-VALUE-MISMATCH` | `RC-VALUE-MISMATCH` | closed-correct (comma list is not the derived span) |
| y6 | `VARIANTS N01-N04VARIANTS N01-N05` | N01-N04 | PASS rc 0 | **FAIL** rc 1 | `RC-CELL-AMBIGUOUS` | closed-correct |
| y7 | `VARIANTS N01-N04\|VARIANTS N01-N05` (tight) | N01-N04 | PASS rc 0 | **FAIL** rc 1 | `RC-CELL-AMBIGUOUS` | closed-correct |
| y8 | ``VARIANTS N01-N04 and `VARIANTS N01-N05` `` (2nd in backticks) | N01-N04 | PASS rc 0 | **FAIL** rc 1 | `RC-CELL-AMBIGUOUS` | closed-correct |
| z1 | `VARIANTS N01,N03-N05` | N03-N05 | FAIL `RC-VALUE-MISMATCH` | FAIL `RC-CELL-MISSING` | `RC-CELL-MISSING` | closed-correct (leading `N01,` genuinely unstated by the capture, and the capture is token-anchored: it does **not** rebase to `N03-N05`) |
| z2 | `VARIANTS N01-N04, N05` | N01-N04 | **PASS** rc 0 | **FAIL** rc 1 | `RC-CELL-MISSING` | closed-correct (extra `N05` stated) — **r98 false green, r99 closes it** |
| z4 | `VARIANTS  N01-N04` (double space) | N01-N04 | FAIL `RC-CELL-MISSING` | FAIL `RC-CELL-MISSING` | `RC-CELL-MISSING` | closed-overstrict |
| z5 | `VARIANTS N01-N04   ` (trailing spaces) | N01-N04 | PASS rc 0 | PASS rc 0 | — | GREEN, legitimate (`split_row` strips) |
| z3 | the `make-r96-bends` row duplicated | N01-N04 | FAIL `RC-ROW-AMBIGUOUS` | FAIL `RC-ROW-AMBIGUOUS` | `RC-ROW-AMBIGUOUS` | closed-correct |

Receipts: `receipts/forge-matrix.json`, `receipts/forge-matrix2.json`, `receipts/forge-matrix3.json`,
one `receipts/forge-<case>-<r98|r99>.json` per leg, plus the run logs
`receipts/forge-run-1.txt`, `receipts/forge-run-2.txt`, `receipts/forge-run-3.txt`.

**Newly rejected by r99 (r98 was GREEN):** a, b, f, x7, y6, y7, y8 (all `RC-CELL-AMBIGUOUS` except a =
`RC-CELL-MISSING`), and z2 (`RC-CELL-MISSING`). That is 8 of the 34 forged legs.
**Remain outside the capture after r99 (still GREEN):** g3, x1, x2, x3, x4, x5, x6, x10, y1, y2, y3,
y4, plus the two other-column shapes x8/x9 and the legitimate-delimiter shapes g1, g2, z5.

## 3. Guard-break table (the `(?![0-9,-])` boundary itself)

The guard refuses exactly `[0-9,-]`. Measured readings:

| cell | r98 | r99 | what the guard did |
|---|---|---|---|
| `VARIANTS N01-N04;` | PASS | PASS | `;` allowed — correct, `;` is a delimiter |
| `VARIANTS N01-N04.` | PASS | PASS | `.` allowed — correct, `.` is a delimiter |
| `VARIANTS N01-N04extra` | PASS | **PASS** | **break: `e` allowed, `extra` silently discarded** |
| `VARIANTS N01-N04x` | PASS | **PASS** | break: same, one letter |
| `VARIANTS N01-N04 N05` | PASS | **PASS** | break: space allowed, `N05` silently discarded (the exact A1 class, different separator) |
| `VARIANTS N01-N04; N05` / `+N05` / `/N05` / `and N05` | PASS | **PASS** | break: same, four more separators |
| `VARIANTS N01–N03` (en dash) | FAIL `RC-CELL-MISSING` | FAIL `RC-CELL-MISSING` | ASCII-only capture; fail-closed (over-strict, no false green) |
| `VARIANTS  N01-N04` (two spaces) | FAIL `RC-CELL-MISSING` | FAIL `RC-CELL-MISSING` | single-space literal; fail-closed (over-strict) |

So the guard closes the *comma/hyphen* continuation only. Any other separator, and any alphabetic
suffix on the last label, is a token boundary the capture does not enforce. The frozen sentence claims
fail-closed for "a cell that states a hybrid span"; the shapes above state an extra label that the
tools do not derive and read PASS.

## 4. Can the `unique` rule be defeated?

`unique` counts `len(re.findall(binding["capture"], cell))`, i.e. **capturable** mentions, not literal
`VARIANTS` tokens. Attempts and readings:

| attempt | cell | r99 reading | defeated? |
|---|---|---|---|
| second mention after an escaped pipe (space padded) | `VARIANTS N01-N04 \| VARIANTS N01-N05` | `RC-CELL-AMBIGUOUS` rc 1 | **no** — `split_row` keeps the cell intact and `\|` stays inside it; both mentions are seen (x7) |
| second mention after a tight escaped pipe | `VARIANTS N01-N04\|VARIANTS N01-N05` | `RC-CELL-AMBIGUOUS` rc 1 | **no** (y7) |
| second mention inside backticks | ``VARIANTS N01-N04 and `VARIANTS N01-N05` `` | `RC-CELL-AMBIGUOUS` rc 1 | **no** (y8) |
| second mention concatenated with no separator | `VARIANTS N01-N04VARIANTS N01-N05` | `RC-CELL-AMBIGUOUS` rc 1 | **no** (y6) |
| second mention in a **different column** (cell 6, Write scope) | cell 5 `VARIANTS N01-N04`, cell 6 `VARIANTS N01-N05` | **PASS** rc 0 | yes, but only because `BINDINGS` binds cell 5 (named limit "only the cells in BINDINGS are bound") — x8 |
| second mention in a **different column** (cell 3, Verdict map) | cell 5 `VARIANTS N01-N04`, cell 3 `VARIANTS N01-N05 …` | **PASS** rc 0 | same, x9 |
| second mention that the capture **cannot match** (lowercase) | `VARIANTS N01-N04 and VARIANTS n01-n03` | **PASS** rc 0 | **yes — genuine defeat** (x4) |
| second mention that the capture cannot match (spaced comma) | `VARIANTS N01-N04 and VARIANTS N01, N03` | **PASS** rc 0 | **yes — genuine defeat** (x5) |
| first mention un-capturable, second capturable | `VARIANTS N01-N04,N05 and VARIANTS N01-N04` | **PASS** rc 0 | **yes — genuine defeat, and it re-opens a hybrid span** (x2) |

The rule is therefore defeatable *inside the bound cell*, without relying on the other-column limit:
an un-capturable mention is invisible to both `unique` and `search`, so a cell can carry a hybrid span
or a contradictory spelling as long as one capturable `VARIANTS …` mention is present. x2/x3 are the
sharpest: they state exactly the r98 A1 hybrid `VARIANTS N01-N04,N05` and read PASS with `findings []`.

## 5. Forged revisions (`--revision` leg)

Fixture repo built in scratch (`receipts/rev-matrix.json`; commits: `root` = docs only, `master1` =
clean fixture, `master2` = hybrid cell committed on master, `master3` = tool keys doctored to
N01..N05, `side` = `master1` + one unrelated file, tag `tag-m2` on `master2`).
Note learned while forging: `--revision` mode always inspects `ROOT = dirname(dirname(__file__))`, so a
fixture must hold a copy of the checker under its own `tools/` (the `ancestor` selftest does exactly
that); running the lane's tool against a foreign repo reads `does not resolve` (rc 2) — fail-closed,
not a bypass.

| # | invocation | rc | status | ids |
|---|---|---|---|---|
| R1 | `--revision side --branch master` (side **not** an ancestor) | 2 | — | `CANNOT-EVALUATE: revision '…' is not an ancestor of master` |
| R2 | same, ancestor-skip mutant | **0** | **PASS** | `[]`, `bindings 7/7` — mutant reads *better*, so it is killed by the `ancestor` case |
| R3 | `--revision side --branch side` | 0 | PASS | `[]` |
| R4 | `--revision master2` (hybrid cell committed) | 1 | FAIL | `RC-CELL-MISSING` (the `git show` leg rejects it exactly as `--root` does) |
| R5 | `--revision master2 --branch side` | 2 | — | not an ancestor of `side` |
| R6 | `--revision tag-m2 --branch master` | 1 | FAIL | `RC-CELL-MISSING` |
| R7 | `--revision root` (no `SKILL.md` at that revision) | 2 | — | `CANNOT-EVALUATE: git show <root>:SKILL.md failed` |
| R8 | `--revision 000…0` | 2 | — | does not resolve |
| R9 | `--revision --` | 2 | — | argparse: expected one argument |
| R10 | `--revision master1 --branch nosuch` | 2 | — | not an ancestor of `nosuch` |
| R11 | `--revision master2^{tree}` | 2 | — | does not resolve |
| R12 | `--revision master3` (tool keys doctored at the revision) | 1 | FAIL | `RC-VALUE-MISMATCH` — proves the derivation reads the **revision's** tool bytes, not the worktree |
| R13 | `--revision master1` (clean ancestor) | 0 | PASS | `[]`, `bindings 7/7` |

R1 vs R2 is the M07 kill direction measured on one and the same revision: the pristine tool refuses
(rc 2); the mutant that skips the ancestor check proceeds and reads PASS (rc 0) — i.e. the mutant's
reading moves *away* from the refusal the case expects, so it is killed, and the `ancestor` selftest
case is causal (independently reproduced by `m07-ancestor-skip-mutant.py --selftest` → `FAIL 16/17`,
exactly `ancestor` red). R7/R8/R9/R10/R11/R12 are all fail-closed; none of them yields a green.

## 6. Findings, by severity

### F1 — HIGH — a hybrid span PASSes whenever one clean `VARIANTS` mention shares the cell
`tools/check-registry-content-r99.py` byte `14310` (`"unique": True`) and `16685`
(`if binding.get("unique")`), plus the capture at byte `14221`. `unique` counts *capturable* mentions
only. Fixtures:

* driver case `x2-hybrid-plus-clean` (fixture rebuilt by `receipts/drivers/forge.py`; cell text in `receipts/forge-matrix.json`) — cell `VARIANTS N01-N04,N05 and VARIANTS N01-N04`, tool keys
  N01..N04 → r99 `status PASS`, `findings []`, rc 0 (`receipts/forge-x2-hybrid-plus-clean-r99.json`).
* driver case `x3-clean-plus-hybrid` (fixture rebuilt by `receipts/drivers/forge.py`; cell text in `receipts/forge-matrix.json`) — `VARIANTS N01-N04 and VARIANTS N01-N04,N05` → PASS, `[]`
  (`receipts/forge-x3-clean-plus-hybrid-r99.json`).

Both cells state the r98 A1 hybrid span `VARIANTS N01-N04,N05`, which the tools do not derive, and
both read PASS. Also a wording problem at face value: the frozen predicate says *"a cell that mentions
`VARIANTS` more than once … reads the new `RC-CELL-AMBIGUOUS`"* and *"a cell that states a hybrid span
… reads `RC-CELL-MISSING`"*; x2 does both (two literal `VARIANTS` tokens, one hybrid span) and reads
PASS. Either the sentence is narrowed to "more than one *capturable* mention / a cell whose only
mention is hybrid", or the check must count literal tokens (`cell.count("VARIANTS")`).

### F2 — HIGH — the boundary guard alphabet is `[0-9,-]`, so any other separator lets an extra label ride
Byte `14265` `(?![0-9,-])`. PASSing fixtures each stating a label the tools do not derive:
`x1` `VARIANTS N01-N04 N05`, `y1` `VARIANTS N01-N04; N05`, `y2` `VARIANTS N01-N04+N05`,
`y3` `VARIANTS N01-N04/N05`, `y4` `VARIANTS N01-N04 and N05`
(`receipts/forge-{x1,y1,y2,y3,y4}-…-r99.json`, all `status PASS`, `findings []`). This is the same
"extra label silently dropped" class as the r98 A1 survivor, reached through a separator the guard
does not name. A token boundary (e.g. `(?![0-9A-Za-z,+-])`, or requiring end-of-cell / a known
delimiter) would close it; the current guard closes two of the many ways to continue a span.

### F3 — MEDIUM — a second span stated outside the `VARIANTS` token PASSes
driver case `x10-uncovered-prose` (fixture rebuilt by `receipts/drivers/forge.py`; cell text in `receipts/forge-matrix.json`): cell `VARIANTS N01-N04 (keys N01-N05)`, tool keys N01..N04,
derived N01-N04 → r99 `PASS`, `[]` (`receipts/forge-x10-uncovered-prose-r99.json`). The cell states
`N01-N05`; only the `VARIANTS`-prefixed span is bound. The converse shape (g, `pinned values N01-N04`
with no token) is fail-closed `RC-CELL-MISSING`, so the binding is token-anchored in one direction only.

### F4 — MEDIUM — the trailing token can be truncated by any alphabetic suffix
`VARIANTS N01-N04extra` and `VARIANTS N01-N04x` read PASS
(`receipts/forge-g3-suffix-extra-r99.json`, `receipts/forge-x6-suffix-x-r99.json`). The bound value is
`N01-N04` while the cell's token is not `N01-N04`.

### F5 — MEDIUM — `unique` is defeated by an un-capturable second mention inside the same cell
`x4` (`… and VARIANTS n01-n03`) and `x5` (`… and VARIANTS N01, N03`) read PASS
(`receipts/forge-x4-clean-plus-lower-r99.json`, `receipts/forge-x5-clean-plus-spaced-r99.json`).
Recorded as part of F1's mechanism but reachable without a hybrid: a contradictory second spelling
survives because the ambiguity counter and the value search share one regex.

### F6 — LOW (inside the named limit, reported not claimed) — a second span in another column PASSes
`x8` (cell 6) and `x9` (cell 3) read PASS while the row states `VARIANTS N01-N05`
(`receipts/forge-x8-second-in-other-col-r99.json`, `receipts/forge-x9-second-in-verdict-col-r99.json`).
The predicate's named limit "only the cells in BINDINGS are bound" covers this; it is recorded so the
next freeze does not mistake it for coverage.

### Verified-strong (no finding)
* The two r98 survivors named in the claim are genuinely closed in their frozen shapes (a, b, f),
  including through the `git show` leg (R4/R6).
* The escaped-pipe and no-separator second mentions do **not** defeat `unique` (x7, y6, y7, y8).
* The capture is token-anchored: it does not rebase onto a suffix (`z1` → `RC-CELL-MISSING`, not a
  green reading of `N03-N05`).
* `z2` (`VARIANTS N01-N04, N05`) was an r98 false green and is now closed.
* The ancestor branch is fail-closed on every forged revision and the mutant's *better* reading is
  killed; `--revision` derives from the revision's bytes (R12), not the worktree.
* Over-strict spellings (d, e, g, g4, z4) are fail-closed: false reds, no false green.

## 7. Residual risk and verification gaps

* The forged PASS shapes F1–F5 are **not** covered by any selftest case; the 17 cases pin exactly the
  three frozen shapes plus the ancestor branch. A later round that repairs them needs a case for the
  compound cell (`hybrid + clean mention`) and for one non-`[0-9,-]` separator.
* My `derived` column is my own AST re-derivation; it agrees with the checkers' verdicts in every case
  (no disagreement observed), but I did not audit `derive_variant_span`'s label regex beyond the
  `N<digits>` family the fixtures use.
* Out of scope for this seat (not run, other seats own them): the landed battery gate, N09/N11 bends,
  the two lie wrappers, the coverage gate. `rows: 160` is printed by my landed run but I did not
  re-derive the coverage tally.
* The M07 mutant I ran is my own one-clause re-derivation (diff in `receipts/m07-mutant.diff`), not the
  r98 MutRegistry bytes; the direction result is independent of the exact mutant text.
* Scratch tree `/fast/scratch/hyaku/tsukuroi-r99/ReviewRegistry` (fixtures, case trees, git repo) was
  deleted after the receipts were copied; the drivers are preserved at `receipts/drivers/` so every
  case is rebuildable.

## 8. Verdict

The frozen C2 legs reproduce exactly as declared (landed PASS/0 findings/7 bindings, selftest 17/17,
r98 PASS on both capture fixtures where r99 FAILs with exactly the frozen single id, M07 killed with
`FAIL 16/17` and only `ancestor` red). At the same time the capture still emits false greens: a hybrid
span PASSes when paired with one clean mention (F1), any non-`[0-9,-]` separator lets an extra label
ride (F2), and a prose span, a truncated token, or an un-capturable second mention all PASS
(F3–F5). Under this seat's acceptance rule — *any shape that reads PASS on r99 while stating a value
the tools do not derive is a finding against C2* — those are findings against C2, each named with its
fixture and receipt.

{"seat":"ReviewRegistry","verdict":"findings","notes":"C2 legs reproduce (landed PASS 0 findings 7 bindings at f107da3a, selftest 17/17, r98 PASS on hybrid+restated vs r99 FAIL one frozen id, own M07 mutant FAIL 16/17 only ancestor red, ancestor branch fail-closed on 13 forged revisions). 5 forged cell classes still read PASS while stating an underived span: hybrid+clean mention (x2/x3), non-[0-9,-] separator extra label (x1/y1/y2/y3/y4), prose span outside the VARIANTS token (x10), truncated token suffix (g3/x6), un-capturable second mention defeating unique (x4/x5). 8 shapes newly rejected by r99 vs r98."}
