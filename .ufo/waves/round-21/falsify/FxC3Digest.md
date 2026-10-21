# FxC3Digest — primary-source digest tamper, source-only

Reviewed-SHA256: 736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e
Predicate: C3-tampered source digest

## Axes and boundary

- **Calibration (C3):** a changed primary source must not acquire a clean byte-identity receipt merely because its report still declares the preregistered digest and predicate.
- **Detector specificity:** distinguish the named snapshot finding from an already-red aggregate status; retain an isolated clean control and the exact built-in source-tamper control.
- **Provenance and scope honesty:** distinguish inspected source, predicted behavior, inventory-declared hashes, and unperformed execution. C1 depth and C2 consumer behavior are outside this assignment.

This is one proposed input mutation, not an executed mutation campaign, an integration decision, or non-author closure.

## Reviewed snapshots and auxiliary dependencies

All candidate evidence below is attributed to revision `0a14952b59d20179e1c813af58befaecd6992a17` by `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate-files.json` (inventory lines 2, 64–67, 94–97, 114–117, 134–137). Hashes are supplied/inventory declarations, not hashes calculated by this seat.

**Primary P:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-review-snapshots.py`, inspected lines 1–169. Its SHA-256 is the standalone receipt above; that receipt binds only P.

Auxiliary snapshot dependencies, explicitly not covered by the primary receipt:

- **R:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/_revision.py`, inspected the requested lines 1–250; relied on lines 62–66 and 172–192. Inventory SHA-256: `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf`. Used only for revision-binding/read-environment source reasoning, not its selftest.
- **L:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/corpus/lessons/round-21.md`, relied on lines 12–13, 31–37, 43, 51–53, and 62. Inventory SHA-256: `ab841b2562e41fa69f90b63b8444d5ab47670ce2acf0ec1208f71cf7980349c9`. Its chronology and missing-seat statements are author declarations, not independently observed events here.
- **Q:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/corpus/QUALITY.md`, relied on criteria 24, 38, 42, and 44 (lines 33, 82, 87, 89). Inventory SHA-256: `1ac6354185c4685f87fba07c702132b87e8102c44412871e5a13622ea6948596`. Used for the narrow execution/receipt/dead-evidence contract.

The candidate-files inventory is not the gate's reviews manifest. I did not read a moving manifest, live tool, report collection, draft, Git object, or branch state to substitute for these snapshots.

## Mutant: one altered committed primary-source byte

**Proposal only:** in the reviewed primary source blob, change the initial ASCII `C` in P line 2's module description from `Check declared review byte/predicate identity, never actual reading or nonexecution.` to `check declared review byte/predicate identity, never actual reading or nonexecution.` This changes one byte, `0x43` to `0x63`. The description is behavior-bearing through `argparse.ArgumentParser(description=__doc__)` at P line 137, while leaving the digest comparison and manifest selection logic untouched.

For the committed-input challenge, only the source blob returned for the primary review's declared source is altered. Keep its preregistered manifest SHA-256, report bytes, predicate, scope declaration, and all auxiliary inputs unchanged. The detector implementation remains the pinned original P; do not simultaneously weaken the detector or re-sign the receipt. A merely dirty working-tree edit is not this challenge: P lines 89–100 and 154–156 read source/report blobs through `git show` at the bound commit.

No altered file or commit was created. This is the exact proposed mutant for L1's authorized probe, not a claim that such a committed blob already exists.

## Observations from source

1. **The actual source bytes are checked, separately from receipt text.** P lines 59–62 obtain the declared source and add `REVIEW-SNAPSHOT-MISMATCH` when it is missing or its computed SHA-256 differs from the manifest digest. A report retaining the old digest does not bypass that comparison.
2. **Matching declarations cannot erase a source finding.** P lines 68–76 independently compare the complete digest/predicate/scope declaration lists. Lines 58 and 77–79 increment `pinned_reviews` only when the row acquired no finding, then return exit class 1 if any finding exists.
3. **The requested exact control is present.** P lines 104–110 define source bytes `b"fixed source\n"`, their digest, a matching report, and the `clean` expectation `(0, set())`. Line 113 defines precisely `("source-tamper", manifest, {**files, "snapshot/tool.py": b"changed\n"}, 1, {"REVIEW-SNAPSHOT-MISMATCH"})`. The manifest and matching report remain unchanged in that case; this is not merely a report-digest mutation.
4. **Selftest checks the named outcome, not just nonzero.** P lines 126–130 call the same `evaluate` function and compare both the exit class and exact finding-ID set. A source-tamper result containing only `REVIEW-REPORT-MISSING`, or a clean result, fails that control. Lines 131–133 print only an aggregate selftest result, not individual case payloads.
5. **Committed-input reachability is conditional.** P lines 154–156 bind the revision before reading its manifest/source/report blobs. R lines 172–192 require the selected commit to satisfy branch ancestry and, when applicable, origin ancestry. A rejected revision produces the separate could-not-evaluate path, not an exercised digest detector. No such binding was executed or independently established here.

## Predicted detector outputs — not execution observations

For the existing isolated one-row selftest surfaces, the following are source predictions from P, not captured output:

| Stage | Source supplied to the same `evaluate` detector | Predicted result | Predicted findings and counts |
|---|---|---|---|
| Pristine control | `b"fixed source\n"`; original manifest/report | Exit 0, `PASS` | Empty findings; `pinned_reviews=1`, `total_reviews=1`, `distinct_source_files=1` |
| Existing exact source-tamper control | `b"changed\n"`; original manifest/report | Exit 1, `FAIL` | Exactly `[{"id":"REVIEW-SNAPSHOT-MISMATCH","site":"One"}]`; pinned 0, total 1, distinct 1 |
| Restored control | Original `b"fixed source\n"`; original manifest/report | Exit 0, `PASS` | Same clean result as the pristine control |

For the proposed single-byte primary-source mutant, the corresponding prediction is `REVIEW-SNAPSHOT-MISMATCH` at that review row's declared `name`, with the row not counted as pinned. This assumes a valid unchanged manifest/receipt, readable inputs, successful revision binding for a committed-input run, and the altered bytes having a different SHA-256. No mutated digest was calculated here.

**Expected-red separation:** L line 52 explicitly says the build manifest retains all 64 rows, including dead ScribeDecision, without a replacement report; L lines 31–37 and Q criterion 44 preserve historical missing/malformed evidence. Those are inspected declarations, not an observed gate run or an inspected full manifest. An absent report becomes `REVIEW-REPORT-MISSING` at P lines 63–64. Therefore an already-failing full-manifest run is not evidence that this mutant was detected. L1's evidence must identify the target row's snapshot finding and use the isolated clean/source-tamper/restored controls; existing dead-report reds must not be dropped, renamed as digest failures, or treated as newly killed mutants.

## Actual output, verdict, and restoration evidence

- **Actual behavioral output:** none. No call to `evaluate`, `selftest`, `main`, Python, Git, or another runtime was made. The actual observations are the source text and supplied inventory entries cited above.
- **Mutation verdict:** **inconclusive / unexecuted under NO-EXEC**. The source predicts detection and supplies the requested exact selftest control; this is neither an observed killed mutant nor a surviving mutant. No baseline success is claimed. An eventual baseline failure would remain inconclusive rather than count as a kill.
- **Before hash:** primary inventory/prompt SHA-256 `736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e`; not independently recomputed.
- **Mutated/after hash:** not produced or measured, because no mutant bytes were written. No fictitious replacement digest is supplied.
- **Restoration:** no source restoration was necessary. Candidate, production, and sibling source paths were never write targets; the only filesystem write performed by this seat is this assigned report. There is no independently measured post-restoration hash; byte preservation here is supported by the read-only source operations, not an executed checksum.
- **Limits:** selftest compares an ID set and exit class, not finding multiplicity, sites, or all payload counters. It uses an in-memory surface and does not itself demonstrate Git/committed-input integration, preregistration chronology, actual reading/comprehension, authorship, or command nonexecution. None of those stronger claims is made.
- **Tooling:** read `/home/vgpnk/.omp/agent/RULES.md`; no tool install/update was needed or attempted. No package-manager transaction, service action, network program, test, import, compile, child dispatch, or VCS mutation was performed. Final runtime verification remains L1's responsibility; no promotion or outside closure is asserted.

Scope: executed=none
