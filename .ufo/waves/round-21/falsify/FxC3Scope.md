# FxC3Scope — period-appended none, source-only probe

Reviewed-SHA256: 736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e
Predicate: C3-period appended none

## Axes and bounds

- **Calibration (C3):** distinguish an exact scope declaration from a punctuation-altered declaration; distinguish source predictions from measured detector results.
- **Operability:** check that the new receipt detector and existing scope detector have explicit non-clean paths for the same one-byte defect.
- **Historical preservation:** retain round20's malformed trailers and missing reports as historical reds; do not repair them by rewriting reports or dropping dead-seat receipts.

This is one leaf, source-only falsification probe of candidate revision `0a14952b59d20179e1c813af58befaecd6992a17`, against round21 baseline `82e519203e676c532b1dc5ea91a85671f2286e7b`. No subagents, runtime, imports, commands, tests, actual mutants, installations, production edits, or historical-report writes were used. Only this assigned report is written. No outside closure, admission, promotion, or ordinal gain is asserted.

## Snapshot identity and auxiliary dependencies

All candidate evidence below comes from immutable copies beneath `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/`. The primary receipt above binds only `tools/check-review-snapshots.py`, not these auxiliary files. SHA-256 values are the **observed predispatch declarations** in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate-files.json`, not independently recomputed hashes.

- Primary `tools/check-review-snapshots.py`: `736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e` (inventory lines 94–98).
- Auxiliary executable source `tools/check-seat-scope.py`: `add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac` (inventory lines 34–38).
- Auxiliary policy `corpus/QUALITY.md`: `1ac6354185c4685f87fba07c702132b87e8102c44412871e5a13622ea6948596` (inventory lines 114–118).
- Auxiliary historical/claim context `corpus/lessons/round-21.md`: `ab841b2562e41fa69f90b63b8444d5ab47670ce2acf0ec1208f71cf7980349c9` (inventory lines 134–138).
- Auxiliary historical/claim context `SCORECARD.md`: `04403120de891fa8eb1c90276da8ea339ec2b0f46442940dbd0fdd5d86ae4e25` (inventory lines 129–133).

Every listed inventory entry declares the same candidate revision. No moving draft or production checker supplied the verdict. Agent rules and the Godspeed/Shokunin skill instructions were read for process, not used as candidate-behavior evidence.

## Mutant and bounded expected detector

**Hypothetical mutant:** insert one ASCII period immediately after `none` and before the line ending of an otherwise-valid report's sole scope receipt: `Scope: executed=none` becomes `Scope: executed=none.`. Keep source bytes, expected source digest, predicate, manifest row, report identity, and all other report text unchanged. This models the historical punctuation defect; it is not a request to edit a historical report.

Use the existing new-gate single-review fixture at `tools/check-review-snapshots.py:104–109`: matching fixed source bytes, one manifest row named `One`, correct digest and predicate, and its valid report. For the old detector, the equivalent single registered NO-EXEC seat receives the same report text. This fixes the comparison boundary without depending on the intentionally red full-wave report set.

### Observed source: new receipt gate

At `tools/check-review-snapshots.py:67–76`, the detector gathers every column-zero `Scope:` line and requires the resulting list to equal exactly `["Scope: executed=none"]`. The period is retained by `splitlines()`. At lines 77–85, a finding prevents incrementing `pinned_reviews` and yields code 1/status `FAIL`.

The in-source `scope-period` case at line 116 already applies this precise replacement to the valid fixture and expects code 1 with the finding set `{REVIEW-SCOPE-MISMATCH}`. Lines 126–130 compare both code and finding-ID set. These are observed fixture assertions, **not an observed passing selftest**.

**[INFERENCE] Expected mutated result:** code 1, status `FAIL`, `distinct_source_files=1`, `total_reviews=1`, `pinned_reviews=0`, and findings `[{"id":"REVIEW-SCOPE-MISMATCH","site":"One"}]`, assuming the unchanged valid fixture. The source digest and predicate still match; this attack should not produce their mismatch IDs.

### Observed source: old scope gate

At `tools/check-seat-scope.py:44,58–61`, the anchored matcher captures the scope value and selects its last occurrence. At lines 75–87, `none.` remains `none.` after stripping/case folding: it is unequal to `none`, but matches `re.match(r"none\b", normalized)` because the period follows a word boundary. The detector appends `SCOPE-TRAILER-MALFORMED` with detail `annotated none is ambiguous; declare exactly none or an actual command list`, then continues before the execution-authorization branch. Lines 92–93 return `FAIL`/code 1 when findings exist; lines 151–170 emit the status and per-ID counts.

The existing clean and annotated-none source cases are visible at lines 331–357 and 360–364. They declare the expected distinction; no case was executed here.

**[INFERENCE] Expected mutated result:** code 1, status `FAIL`, one `SCOPE-TRAILER-MALFORMED` for the selected seat, and zero `SCOPE-EXEC-UNAUTHORIZED` findings for this defect. This is malformed evidence, not proof that a command executed, and an execution-authorization marker would not bypass the earlier malformed-none branch.

## Output and verdict

**Actual behavioral output:** none. Neither evaluator, selftest, CLI, baseline, mutant, nor restored case was run. The actual observations are the pinned source branches, fixture assertions, and inventory declarations cited above.

The following is a source prediction for the same bounded single-report detector inputs in each state, not a transcript:

| Report state | New receipt gate — predicted | Old scope gate — predicted |
|---|---|---|
| Pristine exact declaration | code 0 / `PASS`, pinned 1/1, no findings | code 0 / `PASS`, no findings |
| One period appended | code 1 / `FAIL`, pinned 0/1, `REVIEW-SCOPE-MISMATCH` | code 1 / `FAIL`, `SCOPE-TRAILER-MALFORMED` |
| Exact original declaration restored | same as pristine | same as pristine |

**Verdict:** the assigned literal-period attack exposes no source-level acceptance path in either gate. Both predict the required failure. The **runtime mutation verdict is inconclusive/unexecuted**, not a killed or surviving mutant: there is no exercised clean baseline or detector output to support either claim. L1 alone owns the final authorized measurements.

## Historical reds and missing dead reports

Observed policy in `corpus/QUALITY.md:87–89` requires immutable review predicates and preservation of dead/malformed evidence. `corpus/lessons/round-21.md:31–35,49–52` explicitly retains missing-report controls and the dead ScribeDecision row, with expected-red treatment rather than a substitute report. `SCORECARD.md:628,640–642` records the historical 13 missing reports and 20 period-appended trailers as immutable reds; those counts are **claims in the frozen documents**, not remeasured outcomes from this seat.

Observed implementation at `tools/check-review-snapshots.py:55–64,77–85` counts all supplied rows, adds `REVIEW-REPORT-MISSING` for each absent report, withholds its pinned count, and fails when findings remain. The old gate independently adds `SCOPE-REPORT-MISSING` at `tools/check-seat-scope.py:70–74`. **[INFERENCE]** A retained dead-seat manifest row whose report is absent therefore keeps the new gate red even if every delivered report has an exact scope line. Fixing punctuation on a separate hypothetical control cannot clear that missing-report finding. No report rewriting, row removal, death exemption, or historical waiver is part of this probe.

The actual preregistration/reviews manifest and historical report blobs are not dependencies reviewed here; they are not listed as copied inputs in the supplied candidate-files inventory. Therefore this review does not independently establish the final report count, full-wave status, manifest completeness, or historical byte preservation. Both gates judge declarations, not actual reading or absence of execution; the new gate says so at lines 2 and 86, and the old gate at lines 15–17 and 166–167.

## Restoration and hash evidence

No actual mutation was written, so there are no mutated bytes to restore and no pristine/mutant/restored runtime receipts. The before identity available is the supplied primary SHA-256 `736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e`; the old gate's supplied identity is `add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac`. An independently measured after hash and hypothetical mutant hash are **not produced** under NO-EXEC. The tool record contains read calls followed by this unique report write, with no candidate, report-fixture, or historical-source write. **[INFERENCE]** Those candidate hashes remain the before identities because this seat performed no writes to them; this is not a claimed rehash or restoration test.

No tool was installed or updated, and none was needed for source review. The host-wide pacman pause was not exercised.

Scope: executed=none