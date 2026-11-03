2026-11-03T22:39:00Z
# M1Mutation — C1 RW-row predicate, mutation test (round 68, w1)

Subject: an independent strict counter built from the frozen declaration text only
(`/fast/scratch/hyaku/tsukuroi-r68/M1Mutation/mycount.py`, sha256
`3ad6e99a929bc7e5273400e22345dc66afe7fc51283ed9457cf0b9f8a6646cc9`). The C1/E2 counter
(`drafts/c1/count-rw-r68.py`) was read and executed only after the kill matrix was written, and the
M1 counter was never edited after that read. The counter was built before `drafts/c1/note.md`
existed; no oracle value was taken from it.

## Result in one line

The strict predicate reproduces the declared oracle on all eight fixtures (8/8) and the literal
`grep -cE '^\| RW[0-9]+ \| '` alone does not (it deviates on m1, m2, m4), so the three strictness
clauses are behaviour-bearing; five of six single-point counter mutants are killed by the fixture
battery; one survives because it is equivalent on the declared m3 shape; and the cross-counter run
found one real defect in M1's own evidence clause plus one real defect in the live C1 draft note.

## Fixture matrix (item-literal verdict definition)

`KILLED` is defined as `observed != expected` for a red mutant, so a counter that agrees with the
declaration reports no kills. Observed = expected = oracle on all eight, control = 6:
red_killed = 0/7. This is not a predicate failure — it is the fixture set failing to trap a correct
counter. The three fixtures that do trap the literal counting command are m1 (naive 6 vs oracle 1,
duplicate ids), m2 (naive 6 vs 3, fenced rows) and m4 (naive 6 vs 5, blank evidence); m5/m6/m7 are
shape floors the literal grep already satisfies. Full matrix: `probes/m1-kill-matrix.txt`.

## Survivors and why they survive

1. **m1..m7 at fixture level (7 survivors).** Each returned its declared count, so no red fixture
   exposed a deviation. Survivors here mean "the battery is satisfied", not "a defect passed".
2. **c3 `drop leading-pipe guard` (counter-level, 1 survivor).** It removes
   `if not raw.startswith("|")` from M1's own counter and still returns the oracle on all eight
   fixtures. Why: the declared m3 shape is prose that *starts* with `RW1 |`, so its id lands in
   `split('|')[0]`, and every later clause reads `cells[1]` (the row-kind). Dropping the pipe guard
   therefore cannot move any count on that shape — c3 is **equivalent** for the declared fixture,
   not merely untested. Demonstrated: `'RW1 | verdict | ev a |'.split('|')` is
   `['RW1 ', ' verdict ', ' ev a ', '']` while `'| RW1 | verdict | ev a |'.split('|')` is
   `['', ' RW1 ', ' verdict ', ' ev a ', '']`. The guard is behaviour-bearing against a non-pipe-led
   line that carries the id in its second field: a scratch-only diagnostic `# note | RW9 | ev a | ev b |`
   gives pristine 0 and c3 1. Routed, not applied: a "preamble | RW<id> | ev | ev" prose case would
   kill c3; the eight declared fixtures were left unchanged.
3. **M1's positional evidence clause (a survivor of the *declared* battery, a defect under the note's
   layout).** On the item's 3-cell fixtures `cells[3]` is the evidence cell, so m4 is caught. Rebuilt
   as the note's 8-column row, `cells[3]` is the `fact` cell and the evidence cell is last: M1 then
   counts a blank-evidence row (m8/m4 = 6) where the oracle and the E2 counter both give 5. M1's
   other clause, "last non-empty cell non-empty", is vacuous as literally specified (the last
   non-empty cell is non-empty by construction, and a trailing pipe always supplies a final field),
   so M1 has no evidence guard at all once the table is not 3 columns wide. Recorded, not patched
   (step-5 freeze).

## Cross-counter comparison

Required set (3-cell fixtures): agree on 3/8 (m3, m5, m6); the five disagreements are one clause —
the E2 counter requires an 8/9-cell row and measures 0 on every fixture that contains a counted row.
Arity-matched set (same eight defects as 8-column rows): agree on 7/8, the exception being m8/m4
above, where E2 equals the oracle and M1 does not. Four clause probes isolate the readings still
open in the frozen text: id equality (M1 string 2 / E2 numeric 1 for RW1+RW01), placeholder evidence
(M1 2 / E2 1 for `-`), fence characters (M1 6 / E2 3 for `~~~`), table membership (M1 1 / E2 0 for a
pipe-led row with no separator above). All are reproducible from `probes/m1-vs-e2-counter.txt`.

## Live C1 draft note (read-only, not a fixture)

`drafts/c1/note.md` sha256 `30d3b2fd2ff0e75ad01b146f2abc0fc09bbbd8a03f820150aeeba766d124c6ea`:
frozen literal grep 6, M1 6, E2 5 (`LAYOUT=mixed`, `REJECT line=34 id=RW5 reason=SHAPE detail=11
data cells, 13 raw fields (need 8)`). The header at line 28 has 8 data cells and RW6 matches it;
RW1–RW4 are 9 cells (an unescaped `|` inside the literal `awk -F'|' on the S… row, field 7`);
RW5 is 11 cells (a further unescaped `|` in `grep -n '^| S185 ' corpus/SOURCES.md`). E2's 9-cell
tolerance admits RW1–RW4 and rejects RW5. So the row floor of the C1 claim is simultaneously 6
(frozen literal predicate, PASS) and 5 (arity-binding strict counter, below the ≥ 6 floor) on these
bytes. That is a predicate-scope question the L1 must settle, and the rows as written also break the
`awk -F'|'` field addressing the note itself uses.

## Scope notes

No contract text was changed; no tracked file was touched; the M1 counter was frozen before the E2
read; the eight declared fixtures and their oracle values are exactly those in the item. Six
counter mutants are separate scratch copies (`cm_c1..cm_c6.py`), all under the scratch dir that is
removed at exit; the receipts below are in the lane.

Receipts:
- `probes/m1-kill-matrix.txt` — fixture matrix, literal-grep calibration, 6 counter mutants, c3 diagnosis, hashes.
- `probes/m1-vs-e2-counter.txt` — required 8-fixture comparison, arity-matched set, clause probes, live-note measurement, freeze evidence.
- `w1/M1Mutation.md` — seat report.

## Addendum (2026-11-03T22:45:12Z, after the cross-counter exchange)

Measured, not inferred: the current `count-rw-r68.py` on disk is sha256
`b93f5912d91be4787c5c595e10f5a15501cd64e9af6cd87916b28cd350438458` (E2Battery's message names
`fa0d866d…`, which is not the byte state measured). On those bytes: the eight declared fixtures still
read 0 (COUNTERS_AGREE=3/8 unchanged); the live note (`1d2a4d8d…`) is now 8 data cells per row
(awk NF=10) and reads 6 under both the frozen literal grep and the strict counter with no REJECT, so
§Live C1 draft note's malformed-RW5 finding is resolved on the current bytes; the 9-cell row tolerance
is gone (a 9-cell row with blank evidence is rejected SHAPE and M1 reads 2 there; on a lone 9-cell row
the strict counter reads 0 and M1's rule reads 1, so the strict side counts nothing for that row). Two
divergences the probes isolate are still open on these bytes: numeric id equality (RW1/RW01: 1 vs 2)
and placeholder evidence `-` (1 vs 2). M1's own m8/m4 over-count stands; the counter is frozen.
