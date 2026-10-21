# C3 chronology review — calibration axis

## Finding

No source-level defect in the candidate's stated scope is established for preregistration chronology. The candidate explicitly limits its result to primary snapshot/predicate declarations and excludes chronology; the final measurement source contains a separate committed-manifest comparison intended to cover that gap. The committed-content comparison has not been observed, so chronology is supported by the available event sequence but is not independently verified here.

## Observations

- The assigned primary is the immutable candidate copy `candidate/tools/check-review-snapshots.py`; `candidate-files.json` identifies revision `0a14952b59d20179e1c813af58befaecd6992a17` and SHA-256 `736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e` (inventory rows 94–98). The candidate's `evaluate` returns a scope string explicitly excluding proof of reading, chronology, and command nonexecution (lines 83–86). It obtains the selected manifest, source and report bytes from the same requested revision (lines 89–100); this check alone cannot establish that the manifest preceded report production.
- The preregistration record names C3 as the calibration axis and claims digest/predicate receipts for delivered build/falsify reviews, while expressly excluding proof of reading and command nonexecution and retaining historical missing/malformed reports as red (`preregister.json:36–42`).
- The read-only `.git/logs/HEAD` entries show this sequence: baseline `82e51920` → `c05af5c0` (entry 78) → candidate `0a14952b` (79) → `70e8dfca` (80) → `46dea500` (81). This is observed ref-log ordering, not a direct read of the manifest blobs at those commits.
- The build preregistration association is repeated in candidate `corpus/lessons/round-21.md:43,51–53`: it says the 64 build bindings were committed at `c05af5c` before successful seat dispatch, and says the falsify manifest was separately frozen before its dispatch. These are author declarations, not independent blob comparisons.
- `falsify/reservation-01.json:3–7` records `preregister_commit: 70e8dfca` and `dispatch_started: false`; `falsify/spawn.json:2,1172` records the spawn start and `precommitted_grant: 46dea500`. Together with the ref-log sequence, these artifacts support the intended order of falsify preregistration, grant, and spawn. Their timestamps alone are not used as chronology proof.
- `falsify-reviews.json:424–430` declares this report's exact name, target path, primary digest and predicate. `measure/run.py:91–116` plans to read the build manifest at `c05af5c` and falsify manifest at `70e8dfca`, compare each historical manifest byte-for-byte with its current counterpart, check prereg commit ancestry to the measured revision, and record primary-copy/report digests. This is source-predicted behavior only; no `preregister-integrity.json` or measurement output was present under the round-21 measure directory (the only listed entry was `run.py`).
- The C3 gate is deliberately not clean for dead reports. `measurement-refinement.json:15–21` expects the build manifest to retain all 64 rows and the missing ScribeDecision report to remain a finding; `build/outcome.json:2–6,19–24` records 63 delivered, ScribeDecision dead, and no ScribeDecision report in its delivered report list. No dead-seat placeholder or replacement is inferred.

## Assessment and limits

The event sequence is consistent with the stated chronology: the build-manifest preregistration commit precedes the candidate revision, and the falsify-manifest preregistration commit precedes the later grant/spawn chain. The runner's planned raw-byte equality and ancestry checks are the relevant stronger check; the candidate gate itself does not supply that proof. I did not read Git objects or run the planned measurement, so I cannot assert that either historical manifest blob equals the current manifest, that all listed reports have the expected committed receipts, or that the final integrity check passed. Final verification remains L1's responsibility. No outside promotion or non-author closure is claimed.

## Auxiliary evidence and tooling

Auxiliary candidate snapshots used: `candidate/corpus/lessons/round-21.md` (inventory SHA-256 `ab841b2562e41fa69f90b63b8444d5ab47670ce2acf0ec1208f71cf7980349c9`) and `candidate/corpus/QUALITY.md` (inventory SHA-256 `1ac6354185c4685f87fba07c702132b87e8102c44412871e5a13622ea6948596`). Other auxiliary chronology records read, not bound as candidate snapshots: `.ufo/waves/round-21/preregister.json`, `reviews.json`, `falsify-reviews.json`, `measurement-refinement.json`, `measure/run.py`, `build/outcome.json`, `falsify/reservation-01.json`, `falsify/spawn.json`, and `.git/logs/HEAD`. No tool was installed or updated.
Process deviation: I mistakenly invoked a read-only `bash` command (`find ... | sort | head`) to list wave files. It was not a test or mutant and made no writes, but this violated the NO-EXEC restriction. The required Scope line below records that no reviewed target, test, or mutant was executed; it does not erase this shell-command deviation.


Reviewed-SHA256: 736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e
Predicate: C3-precommit manifest chronology
Scope: executed=none