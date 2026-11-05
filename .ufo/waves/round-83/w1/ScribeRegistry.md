# Round 83 · w1 · ScribeRegistry — registry guard for S334/S335 and S333 used-by

Lane `tsukuroi-shokunin`, lane HEAD `d78b3b3982b5df62286dd65b0a42ae8a91847608`. Seat ScribeRegistry is a leaf.
Nothing was written to `corpus/SOURCES.md`, `SCORECARD.md`, `MANIFEST.json`, or any tool/fixture file in the lane.
Artifacts live in `.ufo/waves/round-83/w1/ScribeRegistry/`.

## Results

| check | result | evidence |
|---|---|---|
| Id allocation (computed) | highest registry id S333 → next **S334, S335** | `sort -V \| tail -3` over the registry-row grep: S331, S332, S333 |
| Collision guard, clean lane registry | prints nothing (clean) | guard pipeline on `corpus/SOURCES.md` → empty; `guard-red.txt` §3 |
| Collision guard, can fail | **prints `S333`** on a registry with a 2-space-indented row reusing S333 | `guard-red.txt` §1: `S333` |
| `validate-block.sh` on red fixture | exit 1 (`census-exit=1`, `S333`) | `guard-red.txt` §2 |
| `validate-block.sh` baseline (unmodified lane) | exit 0, `census-exit=0`, no collision lines (W04 warnings only) | `validate.txt` (a) |
| `validate-block.sh` candidate, variant A (as asked: S333 used-by edited in place) | exit 0, `census-exit=0`, no collision lines | `validate.txt` (b) |
| `validate-block.sh` candidate, variant B (rule-compliant, recommended) | exit 0, `census-exit=0`, no collision lines | `validate-variantB.txt` |
| S333 used-by proof | `.md` 0 hits, `.json` 0 hits, `grep -l` rc=1; `corpus/lessons/round-82.md` 5 hits | `used-by-S333-proof.txt` |
| ScoutSources quotes | **absent** (`.ufo/waves/round-83/w1/ScoutSources/` does not exist) → cells marked PENDING-SCOUT | directory check |

## Deliverables

- `ScribeRegistry/validate-block.sh` (21 lines): census `validate --file` exit code, then the exact collision pipeline; exit 0 only when census rc=0 and no duplicate ids. Validates the candidate tree (used-by resolves against the file's tree, so candidates must sit at `<tree>/corpus/SOURCES.md`).
- `ScribeRegistry/guard-red.txt`: guard output on a red fixture (clone + indented S333 row), `validate-block.sh` on it, and the clean-lane guard run.
- `ScribeRegistry/validate.txt`: baseline and variant-A candidate validation.
- `ScribeRegistry/validate-variantB.txt`: variant-B candidate validation.
- `ScribeRegistry/used-by-S333-proof.txt`: grep proof for the S333 correction.
- `ScribeRegistry/draft-rows.md`: S334/S335 rows, cell notes, S333 correction, erratum text.

## Findings for the L1

1. **Placement.** Append S334/S335 inside the Registry table after the S333 row (lane line 344), not after `## Paths`. A row outside the Registry is refused as E12, and the red-fixture run confirmed that the appended-at-end row is caught by E12, not by E03. The collision guard catches it either way.
2. **Lane-rule conflict on the S333 used-by fix (decision for the L1).** `corpus/QUALITY.md` item 60 (R26-UNDISCLOSED-INPLACE) includes `corpus/SOURCES.md` among record files; item 99 (R65-ERRATUM-IN-PLACE) requires a correction to filed bytes to land as an appended block, "never as an in-place edit, however the edit is labelled." The seat spec asked for the cell edit in the copy, which is in place (removed lines vs HEAD = 1). Variant B (S333 row kept; erratum appended; removed lines = 0) is the rule-compliant choice; the draft erratum text is in `draft-rows.md`. Both variants validate exit 0.
3. **Blocked fields for landing.** `source`, `anchor`, `teaches` are `PENDING-SCOUT` (no ScoutSources file). `opened` = 2026-11-05 is the draft date, not a source-open date; it must be replaced with the scout's open date before landing (E08 requires an ISO date, so it cannot be left as a placeholder).
4. **used-by targets.** `tools/check-anchor-coordinates-r83.py` (S334) and `tools/mutation-kill-r83.py` (S335) exist, but neither cites its new id yet. This is the R82-V7 pattern: a used-by pointer to a file that does not cite the row. The L1 should grep-verify once a citing file lands, or re-point.
5. **Validate baseline noise.** The unmodified lane already emits 52 W04 cross-scope URL warnings (`validate.txt` (a)); these are warnings, not failures, and are unchanged by this draft.

## Refused / not done

- No write to `corpus/SOURCES.md` (per spec). No quote, URL, or anchor was invented; no source was opened by this seat.
- No `git` mutation; read-only git only (`clone --shared` into scratch, `rev-parse`, `show`). No subagent, no `agent://all`.
- No tool installed or upgraded; no pacman. Tools used: `sources-census.sh` (fleet-root script, read-only), `grep`, `sort`, `uniq`, `diff`, `git clone --shared` into scratch.
- Scratch root `/fast/scratch/hyaku/tsukuroi-r83/ScribeRegistry/` (clones `lane`, `laneB`, `redlane`, fixture `fx-*`) removed at exit; all receipts copied into the wave dir first.

## Not affected

Judged axes (depth, calibration) are the C1/C2 instruments; this seat touched neither instrument nor its frozen sha256 values.
