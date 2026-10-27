VERDICT: supports

# F-13 — committed read-only gates at base 2042117 vs impl a447704 (round 46, wave w1, seat RevGatesAll, 2026-10-27)

Method: every one of the eight named gates accepts `--revision` (checked via `--help` before running), so none was skipped for missing data. Each was run twice through the committed wrapper, e.g.:

`python3 tools/run-receipt.py --revision <REV> --out .ufo/waves/round-46/w1/RevGatesAll/<gate>.<base|impl>.jsonl -- tools/<gate>.py --revision {rev}`

run-receipt executes the gate from a private `git clone --no-local` clone checked out at the revision, never the working copy (tools/run-receipt.py:5-13), and removes its sandbox in a `finally` (tools/run-receipt.py:122-124). 16 receipts (8 gates × 2 revisions) are in `.ufo/waves/round-46/w1/RevGatesAll/`; gate stdout is receipt line 2, exit code in the line-3 footer.

## Results

| gate | base 2042117 | impl a447704 | transition |
|---|---|---|---|
| check-knowledge-header | PASS (66 notes, 0 findings) | PASS (67 notes, 0 findings) | none |
| check-registry-coverage | PASS (72 tools / 72 rows) | **FAIL** (74 tools / 72 rows) | **PASS->FAIL** |
| check-appended-notices | PASS (97 records, 0 findings) | PASS (97 records, 0 findings) | none |
| check-recheck-commands | PASS (66 files, 0 flagged / 81 invocations) | PASS (67 files, 0 flagged / 81 invocations) | none |
| check-section-citations | PASS (2 corrections, 0 findings) | PASS (2 corrections, 0 findings) | none |
| check-edit-contract | FAIL | FAIL (identical finding) | none (pre-existing at base) |
| check-review-snapshots | FAIL | FAIL (identical findings) | none (pre-existing at base) |
| check-adjacency-overlap | PASS (6/6 anchored rows, sibling-verified) | PASS (6/6, sibling-verified) | none |

## The one PASS->FAIL: registry coverage — the declared, expected gap

`.ufo/waves/round-46/w1/RevGatesAll/check-registry-coverage.impl.jsonl:2`:

```
{"branch":"master","branch_tip":"b57740c21f0c68ac7eefeba0adb9c67fbeae3228","counts":{"findings":2,"missing":2,"registered":72,"rows_total":72,"tools_total":74},"findings":[{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/check-scrub-admission-r46.py"},{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/score-census-identity-r46.py"}],...,"status":"FAIL"}
```

Exactly the two round-46 counters are unregistered; the base receipt shows 72/72 with zero findings (`check-registry-coverage.base.jsonl:2`). This matches the item's stated expectation ("registry coverage is expected to open a gap for the two new counters until the round-46 registry table lands") and closes as soon as the registry table adds the two rows. No other tool is missing a row (missing=2 of tools_total=74).

## Standing FAILs, byte-identical at base and impl — not introduced by this round

1. check-edit-contract FAIL at both revisions; identical finding `{"id": "EDIT-PROSE", "site": "corpus/knowledge/structured-edit-r23.md"}`, `validated_edit_decisions: 0` of `total_decisions: 8` (`check-edit-contract.base.jsonl:2`, `check-edit-contract.impl.jsonl:2`). Because the base (round-start) revision already fails with the same finding, the impl diff did not cause it; it is an open lane defect pre-dating round 46.
2. check-review-snapshots FAIL at both revisions; identical findings `REVIEW-REPORT-MISSING` at site `ScribeDecision` and `REVIEW-SCOPE-MISMATCH` at sites `Oracle05TagTree`, `Oracle06TagBlob`, `Oracle08NestedTag`; 60 of 64 reviews pinned, 6 distinct source files (`check-review-snapshots.base.jsonl:2`, `check-review-snapshots.impl.jsonl:2`). Same reasoning: pre-existing at base, unchanged by impl.

Neither gate needed data this round lacks — they ran to completion and produced findings; they are genuine standing failures, not skips.

## Everything else: PASS at both revisions, no no-change regressions

- knowledge-header: finding_count 0 at both; note count 66->67 (the new `corpus/knowledge/census-identity-r46.md` entry is present and clean at impl).
- recheck-commands: flagged_count 0 at both; forbidden list pacman/checkupdates/yay/paru/mkinitcpio/limine-update.
- appended-notices: 97/97 records resolved at both, findings [].
- section-citations: findings [] at both.
- adjacency-overlap: 6 expected / 6 anchored rows, shape_errors [], sibling_check sibling-verified at both.

## Environment notes

- Branch binding: base-revision runs recorded `branch_tip a44770491e...`; impl-revision runs recorded `branch_tip b57740c21f...` — master (`git rev-parse refs/heads/master` = b57740c21f0c68ac7eefeba0adb9c67fbeae3228, subject "round-46: GR2/GR3 narrowed per counted partly findings ...") advanced between my two waves. Ancestry verified: base is ancestor of impl, impl is ancestor of b57740c2 (`git merge-base --is-ancestor`, both "yes"). The sweep therefore ran against a moving tip; each receipt header pins `revision`, `tool_revision`, `lane_branches`, `tool_sha256` at run time.
- No C1 counter or census selftest was run (not in this item's scope); concurrency cost rule not exercised.
- Scratch `/fast/scratch/hyaku/tsukuroi-r46/RevGatesAll/` used only as cwd/TMPDIR and removed after this report. run-receipt's own sandboxes (`/fast/scratch/hyaku/run-receipt-*`) are cleaned by the tool itself; ~16 dirs from other seats' runs (timestamps 23:5x and 02:2x local) were observed but left untouched — none attributable to this seat's 16 completed runs.
- Not done: no `--selftest` runs, no `--baseline-tools`/`--registry-from` variant invocations, no gates beyond the eight named — outside the item.
