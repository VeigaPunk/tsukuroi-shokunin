# ReviewRegistry — r98 w1 (C2 attack)

Seat scope: attack C2 — try to make a false comma/span cell read PASS, and find what the
extended capture does not cover. Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`;
all receipts under `.ufo/waves/round-98/w1/ReviewRegistry/receipts/`.

## 0. Instrument integrity (before any measurement)

```
$ sha256sum -c .ufo/waves/round-98/before/instruments.sha256
tools/check-registry-content-r98.py: OK      (5bb1441e…, unchanged while I measured)
tools/check-registry-coverage.py: OK         (6fcb2d0a…)
tools/check-limine-pins.py: OK               (7d79ac29…, gate unchanged)
… 27/27 OK, exit 0
```

Receipt: `receipts/00-instruments.txt` (27 lines `: OK`, `rc=0`), re-run clean after the last
measurement as well.

## 1. Landed legs (expected: PASS, 7/7, selftest 14/14)

```
$ python3 tools/check-registry-content-r98.py --revision b3be3f90 --json receipts/01-landed-content.json
registry-content: status PASS bindings 7/7 findings 0        rc=0
{"bindings": 7, "findings": [], "revision": "b3be3f90", "rows": 157, "status": "PASS"}

$ python3 tools/check-registry-content-r98.py --selftest
selftest PASS 14/14                                          rc=0
```

PASS both. Receipts `receipts/01-landed.txt`, `01-landed-content.json`, `02-selftest.txt`.
Baseline blindness control: the r97 do-nothing checker on the same revision reads
`PASS bindings 7/7 findings 0` rc=0 (`receipts/04-r97-landed.json`), so the base row is not
itself discriminating — the doctored legs below carry the discrimination.

## 2. Committed doctored fixtures, re-run by me (not copied from `before/dev/`)

Fixtures live in a scratch `git clone --shared` of the lane at `b3be3f90`; the checker rides at
`fixture/` in the clone so the coverage gate's tool set is unchanged. The committed fixture tree's
copy of the checker differs from today's lane tool in its **module docstring only** (first line
renamed; the 10-line r98 explanatory paragraph is absent) — the recorded `diff` is exactly `2c2` and
`40a41,50`, and both hunks fall inside the docstring that ends at line 51. To remove the caveat I
re-ran every content leg in a fresh clone with `fixture/check-registry-content-r98.py` overwritten
by the lane's own bytes (`cmp` clean, sha256 `5bb1441e…`); those re-runs are the `receipts/20-*`
series and they reproduce the `03-*` verdicts exactly.

| fixture | revision | diff names | r98 content | r98 coverage |
|---|---|---|---|---|
| D1 | `aab954f1dbcdda9a8815621154873db427c9fec3` | `SKILL.md`, `fixture/*.py` (3) | FAIL, 1 finding `RC-VALUE-MISMATCH SKILL.md:5939 RC-BEND-SPAN states 'N01,N03', derives 'N01-N04'`, rc=1 | PASS 157/157 findings 0, rc=0 |
| D2 | `d17ebc56663017bf09810064a21b878cdbdade7b` | `SKILL.md`, `fixture/*.py` (3), `tools/make-r96-bends.py` | **PASS 7/7 findings 0**, rc=0 | PASS 157/157 findings 0, rc=0 |
| D2lie | `3155fd3d91a16ee0f39d6fd7eb6c87620c3f09e8` | same as D2 | FAIL, 1 `RC-VALUE-MISMATCH … states 'N01-N03', derives 'N01,N03'`, rc=1 | PASS 157/157 findings 0, rc=0 |

Cross-checks on the same three revisions:

| fixture | r97 do-nothing checker | M08 mutant |
|---|---|---|
| D1 | FAIL `RC-CELL-MISSING` (cell 5 no longer states `VARIANTS (N\d+-N\d+)`), rc=1 | FAIL 1 `RC-VALUE-MISMATCH`, rc=1 |
| D2 | FAIL `RC-CELL-MISSING`, rc=1 | **FAIL** `RC-BEND-SPAN states 'N01,N03', derives 'N01-N03'`, rc=1 |
| D2lie | FAIL `RC-VALUE-MISMATCH`, rc=1 | **PASS 7/7 findings 0**, rc=0 |

Receipts `receipts/03-D1*`, `03-D2*`, `03-D2lie*`, `12-r97-*`, `12-m08-*`, and the lane-byte
re-runs `receipts/20-*`. Every expected line in the claim's target matches; D2/D2lie invert
between r98 and M08 exactly as declared.

## 3. My own fixtures (a)–(e), built from scratch bodies, not the D1/D2 recipes

Driver `build_fixtures.py` (scratch) imports the shipped checker and calls `check(Tree(dir))`;
each case writes its own `VARIANTS` body and its own `SKILL.md` cell. Receipt
`receipts/10-a-to-e.txt`, `receipts/16-extra-probes.txt`.

| # | tool keys | row cell (5) | capture reads | derive returns | r98 | M08 |
|---|---|---|---|---|---|---|
| a | `N01,N03` | `N01,N03,N05` | `N01,N03,N05` | `N01,N03` | **FAIL** 1 `RC-VALUE-MISMATCH` | FAIL 1 |
| b | `N01,N03` | `N01-N03` | `N01-N03` | `N01,N03` | **FAIL** 1 | **PASS** (blind — the lie r98 catches) |
| c | `N01,N02,N03` | `N01,N03` | `N01,N03` | `N01-N03` | **FAIL** 1 | FAIL 1 |
| d | `N01,N03` | `N01,N03 (two bends)` | `N01,N03` | `N01,N03` | **PASS** 0 | FAIL 1 |
| e | `N01,N03` | `N01,N01,N03` | `N01,N01,N03` | `N01,N03` | **FAIL** 1 | FAIL 1 |
| e2 | `N01,N01,N03` | `N01,N03` | `N01,N03` | `N01,N03` | **PASS** 0 | FAIL 1 |

Answers to the posed questions:

- **(a)** over-wide comma row FAILs, and the id is `RC-BEND-SPAN` inside one `RC-VALUE-MISMATCH`;
  the checker prints both literals (`states 'N01,N03,N05'`, `derives 'N01,N03'`). No PASS lie.
- **(b)** the span form against gap keys FAILs on r98 and reads PASS on M08 — this is the
  discriminating leg, reproducing the committed D2lie shape independently.
- **(c)** contiguous keys with a comma cell: the capture **does** bind the comma form (that is the
  new coverage), the derivation returns the hyphen form, and the row FAILs. Comma and hyphen are
  not interchangeable — correct, and it means the row must state the derivation's own form.
- **(d)** a cell carrying `N01,N03 (two bends)` binds (`N01,N03`), the comparison is right, PASS.
  Prose *after* the span is harmless because the regex is anchored at `VARIANTS ` and stops at the
  last `,N<digits>`.
- **(e)** `N01,N01,N03` is captured whole and compared literally to `N01,N03` → FAIL. Duplicates in
  the **cell** are fail-closed. Duplicates in the **tool keys** (e2) collapse through the set
  derivation and PASS — correct under set semantics.

## 4. FINDINGS — false PASS the extended capture does not cover

**RR98-F1 (medium): hybrid `N01-N03,N05` truncates and reads PASS.** Cell
`VARIANTS N01-N04,N05` on the real r96 row, keys unchanged from `b3be3f90`. Revision
`9d8f6bda34d927dca04d82ba3e2efb10eb6b7e17` (scratch clone, diff names `SKILL.md`,
`fixture/*.py`):

```
r98 content : registry-content: status PASS bindings 7/7 findings 0   rc=0
r98 coverage: status PASS registered 157 tools_total 157 findings 0   rc=0
M08         : status PASS bindings 7/7 findings 0                     rc=0
```

Root cause: `capture = VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))` — after the first label the
alternation tries the **hyphen** branch first, so `N01-N04` matches and the `,N05` tail is never
consumed and never compared. A row that over-claims an extra bend label reads PASS. This is the
"false comma/span cell reads PASS" the seat was asked to find; it is a **coverage gap, not a
regression** (the landed cell `r96 VARIANTS N01-N04` at `SKILL.md:5939` is correct). Receipt
`receipts/17-f-mixed.txt`.

**RR98-F2 (low, same class): a second, contradictory mention in the same cell is unbound.**
`VARIANTS N01-N03; VARIANTS N09,N11` against contiguous keys → `re.search` binds the first
occurrence `N01-N03`, derives `N01-N03`, **PASS**, findings 0. The plan's limit says a prose
restatement *in another cell* stays unbound; measured, a restatement in the **same** cell is
unbound too, so the stated limit is narrower than the behaviour. Receipt
`receipts/16-extra-probes.txt` (`g-double`, `i-prose-other`).

**RR98-F3 (low, fail-closed, not a false PASS): whitespace variants do not bind.**
`N01, N03` (space after comma), `N01,N03` with a double space after `VARIANTS`, and
`VARIANTS = N01,N03` all read `RC-CELL-MISSING` rc=1 — noisy but safe. Receipt `receipts/16-extra-probes.txt`.

**RR98-F4 (informational): coverage gate cannot see any of this.** D1, D2, D2lie and F1 all read
`PASS 157/157 findings 0` on the coverage gate. The claim's blindness leg is therefore satisfied
(vacuous-by-design), but it must not be cited as evidence that a doctored cell was caught — only
the content gate carries that.

## 5. M08 kill — receipt, not assertion

- **`--selftest`:** M08 reads `selftest FAIL 12/14`, rc=1, with `span-gap FAIL ['RC-VALUE-MISMATCH']`
  and `span-gap-lie FAIL []` (expected one finding, got none). The other twelve cases pass, so the
  two new cases are exactly the added kill surface. Receipt `receipts/11-m08-selftest.txt`.
- **Killing leg:** the derivation leg `derive_variant_span` (returns `N01,N03` for a gap;
  M08 returns `N01-N03` for every input). On the shipped D2 fixture r98 PASS / M08 FAIL; on D2lie
  r98 FAIL / M08 PASS — both directions shown (`receipts/12-m08-D2.txt`, `12-m08-D2lie.txt`).
- **My (e) case does NOT discriminate M08** (both read FAIL 1) and must not be offered as a kill
  receipt; the discriminating cases are (b)/D2 and (d). Stated because the assignment asked and the
  honest answer is negative.

## 6. Fail-closed paths (each rc/status)

| leg | command surface | rc | status / finding |
|---|---|---|---|
| missing bound tool | `--root` on a fixture with `tools/check-limine-pins.py` deleted | 1 | `FAIL`, 3 × `RC-DERIVE-FAILED` (bindings 3/7) + the pre-existing span mismatch |
| missing row | `--root`, `make-r96-bends` row deleted | 1 | `FAIL`, `RC-ROW-MISSING make-r96-bends[5]` |
| 7/8-column table | `--root`, cell widened by `\|x` | 2 | `CANNOT_EVALUATE`, `E-TABLE` "malformed registry row at line 10" |
| non-ancestor revision | `--revision 1d971934…` (orphan branch in my clone-fc, `merge-base --is-ancestor` = 1) | 2 | `CANNOT-EVALUATE` "is not an ancestor of master" |
| unresolvable revision | `--revision deadbeef1234` | 2 | `CANNOT-EVALUATE` "does not resolve" |

Receipts `receipts/13-fc-*.txt`, `13b-fc-nonanc.txt`. Note the non-ancestor leg needs the checker
whose ROOT is the repo holding the orphan (a lane-root run reports "does not resolve" for the same
hash — same rc, different message; both receipts kept).

## 7. Ledger rows

`ledger-draft.tsv` in this seat dir: 7 rows (5 `falsifies-wording` narrowing the capture's stated
scope — over-wide, whitespace, hybrid-tail, duplicate semantics, coverage-gate blindness — and the
two F1/F2 rows above). No row claims a `falsifies-number`.

## 8. Residual risk / verification gaps

1. **F1 is real but latent.** No landed cell uses the hybrid form; the exposure is a future row
   that writes `N01-N04,N05` believing the capture reads it whole.
2. **`--root` vs `--revision` divergence.** The `--root` surface bypasses `check_revision`, so
   ancestry/landing checks are untested there by construction; I measured both surfaces separately
   and did not assume equivalence.
3. **Clone fixture checker is not byte-identical to the lane** (module docstring only, hunks
   `2c2` + `40a41,50`). A strict `sha256` comparison by a later reviewer will flag the committed
   fixture tree; the `receipts/20-*` re-runs use the lane's exact bytes and match.
4. **I did not modify any frozen instrument**, and `sha256sum -c` was clean at seat start; the
   scratch clone holds all commits (`git rev-parse --show-toplevel` asserted equal to the clone
   path before each commit). Scratch `/fast/scratch/hyaku/tsukuroi-r98/ReviewRegistry` deleted
   before yield.
5. **No new tool installed**; no pacman/`sudo` used.

{"seat":"ReviewRegistry","verdict":"findings","notes":"C2 legs reproduce: landed PASS 7/7 + selftest 14/14; D1 FAIL 1 RC-VALUE-MISMATCH, D2 PASS, D2lie FAIL 1, M08 inverted (D2 FAIL / D2lie PASS) and --selftest 12/14 with span-gap+span-gap-lie red; coverage PASS 157/157 on every doctored revision. Two false-PASS shapes found that the extended capture does not cover: (F1, medium) hybrid cell 'VARIANTS N01-N04,N05' truncates to N01-N04 and reads PASS 7/7 at revision 9d8f6bda with M08 also PASS and coverage PASS 157/157 — the hyphen branch of the alternation wins before the comma tail, so an over-claimed extra label is dropped; (F2, low) a second contradictory mention in the same cell is unbound (first match wins). Whitespace variants fail closed (RC-CELL-MISSING). My (e) duplicate-label case does not discriminate M08. No fake-fallback; no instrument edited; scratch removed."}
