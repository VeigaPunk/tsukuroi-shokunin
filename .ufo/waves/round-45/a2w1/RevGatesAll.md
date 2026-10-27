VERDICT: defect-found

## F-12 — committed read-only gate sweep

Ran all ten requested gates through `tools/run-receipt.py` at base `5bbd5ff588120fd8e7c744695351a6978b4241c1` and implementation `18389f44cf6ce414d7be205998b29c79fb0b490c`. I read each gate's `--help` first; every requested tool accepted a revision-bound invocation, and none required round-specific external data that was unavailable. The scrub-record gates were passed the sandbox lane explicitly. Receipts are under `.ufo/waves/round-45/a2w1/RevGatesAll/`.

### PASS → FAIL

- **`check-registry-coverage.py`: PASS → FAIL.** Base receipt reports `status=PASS`, `findings=0`, `registered=70`, `rows_total=70`, `tools_total=70` (`RevGatesAll/base-check-registry-coverage.jsonl:2`). Implementation reports `status=FAIL`, `findings=2`, `registered=70`, `rows_total=70`, `tools_total=72`; both findings are `REGISTRY-ROW-MISSING`: no operative row names `tools/check-scrub-grounding-r45.py` and no operative row names `tools/score-census-readers-r45.py` (`RevGatesAll/impl-check-registry-coverage.jsonl:2`). This is the sole PASS/FAIL transition found and is a concrete regression in the committed registry gate.

### No status transition

- `check-knowledge-header.py`: PASS at both revisions (`base-check-knowledge-header.jsonl:2`, `impl-check-knowledge-header.jsonl:2`).
- `check-appended-notices.py`: PASS at both (`base-check-appended-notices.jsonl:2`, `impl-check-appended-notices.jsonl:2`).
- `check-recheck-commands.py`: PASS at both (`base-check-recheck-commands.jsonl:2`, `impl-check-recheck-commands.jsonl:2`).
- `check-section-citations.py`: PASS at both (`base-check-section-citations.jsonl:2`, `impl-check-section-citations.jsonl:2`).
- `check-edit-contract.py`: FAIL at both; both report `EDIT-PROSE` at `corpus/knowledge/structured-edit-r23.md`, `total_decisions=8`, `validated_edit_decisions=0` (`base-check-edit-contract.jsonl:2`, `impl-check-edit-contract.jsonl:2`).
- `check-review-snapshots.py`: FAIL at both; identical findings: `REVIEW-REPORT-MISSING` at `ScribeDecision` and `REVIEW-SCOPE-MISMATCH` at `Oracle05TagTree`, `Oracle06TagBlob`, and `Oracle08NestedTag`; each reports 60 pinned and 64 total reviews (`base-check-review-snapshots.jsonl:2`, `impl-check-review-snapshots.jsonl:2`).
- `check-scrub-record-r43.py`: PASS at both (`base-check-scrub-record-r43.jsonl:2`, `impl-check-scrub-record-r43.jsonl:2`).
- `check-scrub-record-r44.py`: FAIL at both, as expected from the stated baseline condition (`base-check-scrub-record-r44.jsonl:2`, `impl-check-scrub-record-r44.jsonl:2`). Its counter fields are unchanged: `verdicts_ok=0`; SR7 rev verdict absent, SR8 rev `partly`, SR9 rev `partly`; all 3 row/source/quote/property/host and pointer checks remain 3/1 as shown in both receipts. The counter `revision` field necessarily changes from base hash to implementation hash; no other reported gate-result field changed.
- `check-adjacency-overlap.py`: PASS at both (`base-check-adjacency-overlap.jsonl:2`, `impl-check-adjacency-overlap.jsonl:2`).

The help outputs are in `RevGatesAll/helps/`. All actual gate receipts are JSONL with a revision/tool-revision header and exit-code footer. No gate was skipped. No host operation or lane mutation was performed.
