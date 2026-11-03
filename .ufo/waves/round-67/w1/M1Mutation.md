# M1Mutation — mutation battery on C1's frozen SL counter

- UTC: 2026-11-03T21:53:19Z (battery run; this note follows the same run)
- Receipt (authoritative, embedded fixture bytes): `.ufo/waves/round-67/probes/m1-c1-counter-battery.txt`
  sha256 `76e99cf0d883babcaa944b8f83bd10ae86f0a4e353e333a5b2273494cb4acf37`, 618 lines / 31868 bytes
- Lane head during the run: `071a55c9c0fd022890d1b255c2782e4761e7a7d8` (unchanged before/after; no tracked
  file written, `SCORECARD.md` and `tools/` clean)
- Tools: GNU grep 3.12-modified, GNU Awk 5.4.1
- Fixtures were synthetic and lived under `/fast/scratch/hyaku/tsukuroi-r67/M1Mutation` (deleted after
  copy-out; their verbatim bytes are embedded in the receipt, hash-stamped per file)

## Counter under test (frozen, not reinterpreted)

Predicate bytes, extracted from the C1 row of the declaration: `grep -cE '^\| SL[0-9]+ \|'`, pass at `>= 4`.

Honest base: at 071a55c9 the note `corpus/knowledge/btrfs-scrub-limit-revert-r67.md` is absent, so the real
counter has no honest-base run in this battery; only the control fixture K0 establishes that the detector
works at all on a well-formed input. That makes every mutant verdict below meaningful rather than a
detector-wide failure (`CONTROL=VALID`).

## Results (one row per fixture; counts are the counter output, rc of the `>= 4` test in parentheses)

| fixture | defect | frozen count | frozen verdict | strict count | strict verdict |
|---|---|---|---|---|---|
| K0 control | none — 4 rows, ids SL1..SL4 | 4 | PASS (0) | 4 | PASS (0) |
| Ma | header `\| SL \| claim \| evidence \|` + 3 rows | 3 | FAIL (1) | 3 | FAIL (1) |
| Mb | four rows, all id `SL1` | 4 | PASS (0) | 1 | FAIL (1) |
| Mc | 3 rows + one `\| SL5 \|` row inside a fenced block | 4 | PASS (0) | 3 | FAIL (1) |
| Md | 3 rows + prose line starting `\| SL4 \|`, no evidence cell | 4 | PASS (0) | 3 | FAIL (1) |
| Me | 4 rows, every evidence cell empty | 4 | PASS (0) | 0 | FAIL (1) |

`SURVIVES_FROZEN=4 of 5`, `SURVIVES_STRICT=0 of 5`.

## What the battery shows

1. The frozen counter counts **row shapes anchored at column 1**, nothing else. It cannot see a duplicated
   id (Mb: four `SL1` lines count as four), a row inside a fenced code block (Mc), a prose line that merely
   begins `| SL4 |` and carries no cells (Md), or an empty evidence cell (Me). Only Ma — which removes a
   row — fails it. So C1's `>= 4` is a floor on the number of matching *lines*, not on evidenced rows.
2. Mc and Md are authoring accidents, not contrived adversarial shapes: a fenced example row and a wrapped
   prose line that begins with a row id are what a long note accumulates. Me is the cheapest escape: four
   ids, no evidence anywhere, predicate satisfied.
3. Strict counter used here (defined in the receipt, **not landed**): one valid row requires outside a
   fence, the exact frozen anchor, 3 visible columns, a unique `SL<n>` id, a non-empty claim, and a
   non-empty evidence cell matching a line-number pattern (`scrub.c:1640`, `1640-1649`, …). It kills all
   four shape-preserving mutants with no false kill on K0, and its anchor axis is byte-faithful: it agrees
   with the frozen counter on `| SL1|` (B1: 3 vs 3), `| SL10 |` (B2: 4 vs 4) and two-space indentation
   (B3: 0 vs 0), so its extra discrimination comes only from columns/ids/evidence/fences.
4. The strict counter has its own defect class, found and fixed inside the battery: a naive `awk -F'|'`
   column split counts a markdown-escaped `\|` inside a cell as a column break and would reject a
   legitimate row (B4: frozen 4, v1 3). Protecting `\|` before the split (v2) accepts it (B4: 4) and leaves
   all six fixture verdicts unchanged (v1 = v2 on every fixture), so v2 improves one axis and harms none.
5. S6 is the remaining cost of strictness: a row whose evidence cites a command rather than a line number
   is rejected even when the command is valid. Any adoption decision has to choose that burden knowingly;
   this battery does not decide it.

## Carrier notes (no verdict claimed)

- C1's predicate is frozen this round; this note reports detector discrimination only, on synthetic
  fixtures, and does not amend the predicate.
- If the L1 wants the strict reading retained as evidence, the receipt's `strict.awk` (sha256
  `91dee1cff8976edc3d1e12606abe9433de1edd3344a530b367f27d132f56f965`) plus the v1/v2 divergence at B4 is
  the whole story; nothing else in this seat needs to land.
