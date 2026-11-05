# Round 83 w1 ScribeRegistry — draft rows and used-by correction

Lane root `tsukuroi-shokunin`, lane HEAD `d78b3b3982b5df62286dd65b0a42ae8a91847608`
(`corpus/SOURCES.md` at HEAD equals the worktree). Nothing here writes
`corpus/SOURCES.md`; the L1 appends after WAVE-DONE.

## Id allocation (computed, not guessed)

`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -V | tail -3`
→ `S331`, `S332`, `S333`. Highest registry id = S333, so the next two are **S334** and **S335**.

## New rows (census schema: 11 cells, NF=13, no `|` inside any cell)

Insert inside the Registry table directly after the S333 row (lane line 344), **not** after `## Paths`.

```
| S334 | NIST FIPS 180-4 — URL PENDING-SCOUT | spec | A | SHA-256 digest definition | PENDING-SCOUT | PENDING-SCOUT | mined | 2026-11-05 | annual | tools/check-anchor-coordinates-r83.py |
| S335 | Python subprocess documentation — URL PENDING-SCOUT | docs | A | subprocess timeout semantics | PENDING-SCOUT | PENDING-SCOUT | mined | 2026-11-05 | on-release | tools/mutation-kill-r83.py |
```

Cell notes:
- `source`, `anchor`, `teaches`: **PENDING-SCOUT**. `.ufo/waves/round-83/w1/ScoutSources/sources.json`
  does not exist (checked: directory absent), so no quote was filled and no URL was invented.
  The source-name prefix is the registry title only, not a quoted or fetched fact.
- `opened` = `2026-11-05`: this is the **draft date**, not a date on which a source was opened by
  this seat (no source was opened here). The scout's open date must replace it before landing;
  `opened` must stay an ISO date or E08 fires.
- `recheck`: `annual` (S334), `on-release` (S335). Symbolic cadences pass E09 (`sources-census.sh` regex `^[A-Za-z][A-Za-z0-9 _-]*$`).
- `used-by`: both paths exist in the lane (`tools/check-anchor-coordinates-r83.py` carries 7 `sha256` hits;
  `tools/mutation-kill-r83.py` carries 7 `subprocess` and 17 `timeout` hits). **Caveat (R82-V7 pattern):**
  neither file cites S334/S335 yet. The used-by cell must point at a file that actually cites the id; once the
  round-83 lesson or instrument cites S334/S335, the L1 should grep-verify before landing.

## S333 used-by correction

Old cell (S333, lane line 344, last cell):
```
corpus/knowledge/mount-unit-fstab-plane-r81.md, corpus/knowledge/mount-unit-fstab-plane-r81.json
```
New cell:
```
corpus/lessons/round-82.md
```
Proof (`used-by-S333-proof.txt`): `grep -c S333` on the `.md` → 0, on the `.json` → 0,
`grep -l S333` on both → rc=1 (neither matches). `corpus/lessons/round-82.md` → 5 hits.

**Lane-rule conflict — decision for the L1.** `corpus/QUALITY.md` item 60 (R26-UNDISCLOSED-INPLACE) lists
`corpus/SOURCES.md` among record files whose non-append changes must be disclosed, and item 99
(R65-ERRATUM-IN-PLACE) says a correction to filed bytes lands as an appended block naming the superseded text,
"never as an in-place edit, however the edit is labelled." The seat spec asked for the cell change applied in
the copy, which is an in-place edit. Two variants were built and validated:

- **Variant A (as asked):** S333 used-by cell replaced in place. Removed lines vs HEAD = 1. Validate exit 0
  (`validate.txt`, section b).
- **Variant B (rule-compliant, recommended):** S333 row untouched; S334 and S335 inserted; an appended erratum
  block at the tail names the superseded text and the correct target. Removed lines vs HEAD = 0. Validate exit 0
  (`validate-variantB.txt`).

Erratum block used in variant B:
```
- Round-83 erratum (R82-V7, 2026-11-05): the S333 row as filed names `used-by` `corpus/knowledge/mount-unit-fstab-plane-r81.md, corpus/knowledge/mount-unit-fstab-plane-r81.json`; neither file contains `S333` (`grep -c S333` returns 0 for both), so that pointer is superseded. The correct used-by target is `corpus/lessons/round-82.md`, which cites S333 in its registry-change and quote tables. The S333 row is kept as filed; this appended block is the correction, per QUALITY.md items 60 and 99.
```
Trade-off: variant B leaves the filed S333 cell pointing at the two files that do not cite it, so `validate`
(which only checks existence, E11) cannot see the error; the erratum is the only record. Variant A fixes the cell
but breaks the append-only rule.
