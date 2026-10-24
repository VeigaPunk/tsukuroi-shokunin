# W2CritFreeze — scoped findings

Axes: operability, C1, freeze.

- **Executable freeze PASS:** requested probe diff is empty, exit zero; both commit blobs hash to `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`. The two LOG-named final base controls name these exact bytes.
- **Documentary freeze FAIL:** SCORECARD is identical at declaration and freeze (blob `fee44721be1be2781d9b8f1488ce3c990f94cdb4`). Its correction block, restated kill rule, label/schema correction and declaration named limit first appear in change commit `c052bb7d41ced49aa888817069afd804eccfecf1`, despite claiming a corrections-before-freeze order. The frozen LOG points to that then-absent block. The probe's own named-limit bytes were already frozen; no executable post-freeze retuning is alleged.
- **Complete before/sensitivity gate NOT ESTABLISHED:** no final-byte all-five before/regression/positive MutPathCopy/live-view-before evidence found in freeze L1; its exact-byte MutAttrgetter receipt reads zero, not the required positive sensitivity. Three older development summaries have different probe hashes, contradicting SCORECARD's description of that sequence as “on final bytes”.

Smallest safe correction: append truthful provenance and evidence-eligibility corrections without rewriting the frozen history/counter or treating later observations as prior committed receipts. Documentation is repairable; historical freeze completeness cannot be repaired retroactively. No canonical C1 judgment performed.

Full verdicts, counterexamples and evidence: `freeze-conformance.md`. Machine-readable static observations: `freeze-evidence.json`.

Only read-only Git/hash/static inspection was performed. No probe/gate/test or alternate runtime/judge was invoked; no tools installed/updated; no production/index/VCS mutations. Writes confined to this seat directory.
