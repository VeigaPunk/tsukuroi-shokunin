# ExecReview — round 21 C3 receipt gate

## Axes
- **Correctness:** the draft binds a landed revision, checks each committed source blob against its declared SHA-256, and requires unique exact standalone receipt lines.
- **Operability:** supports `--revision HEX`, optional `--manifest` and `--branch`, plus an in-memory `--selftest`; missing declared reports remain explicit failures.
- **Calibration:** malformed schema/path/duplicate-name inputs are could-not-evaluate; receipt checks are intentionally limited to committed declarations.

## Observations
- Read the pinned `snapshot/tools/check-seat-scope.py` named by the assignment. Its source describes immutable-object revision reads and imports the shared `_revision.bind`; the pinned binder checks landed commit ancestry and optional origin ancestry.
- Added `.ufo/waves/round-21/drafts/ExecReview/check-review-snapshots.py`. It reads manifest, source and report data only from Git objects after `_revision.bind`, emits `pinned_reviews`, `total_reviews`, and typed findings, and includes isolated dictionary-fixture cases for clean receipts, missing manifest/report, tampered source, report digest mismatch, wrong predicate, scope punctuation, duplicate name, traversal, and malformed input.
- The selftest and gate were not run under the NO-EXEC assignment.
- LSP was not available among mounted tools; source inspection used the provided read/grep tools. No tool was installed.

## Inferences and limits
- `pinned_reviews` counts rows whose committed source bytes match the manifest digest; `total_reviews` counts validated manifest rows. These are byte/receipt checks, not proof a reviewer read the bytes or that no command ran.
- The gate does not verify chronology from timestamps. Preregistration chronology must be evidenced by the committed preregistration/spec; the gate does not discover unlisted reports.
- Exact retained source identity and required receipt predicate are recorded below. No non-author closure or outside promotion is claimed.

Reviewed-SHA256: add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac
Predicate: C3-pinned-review-receipt-contract
Scope: executed=none