# C1 before-receipt expected output

`run-before.sh` puts each receipt in the directory from which it is invoked. The outer `run-receipt.py` JSONL header must carry `revision` equal to `6d76fb20f6ecbc940e5c8fff36c74060c885e161` and `tool_sha256` equal to the SHA-256 of the committed probe at `tool_revision`. The probe's final JSON object is the last non-empty line before the receipt footer. Dynamic values (`probe_sha256`, `scratch`, and timestamps) vary; the keys and state constraints below are the expected exact JSON shape.

## Before: `livefive`

One summary object, with `targets: 5`, `channels: ["names", "quiet", "source"]`, `pairs: 15`, `target_set: "livefive"`, `revision` and `base` both the declaration base, `predicate_label: "leaking_pairs"`, `probe_version: 5`, a 64-hex `probe_sha256`, a scratch-path string, and `harness_errors: []`. `leaking` is at least 5 and `leaking_pairs` is a list containing at least one `<target>:<channel>` entry for each of these five distinct targets:

- `tools/check-revision-binding.py`
- `tools/check-report-receipts.py`
- `tools/score-census-handoff-r32.py`
- `tools/mutants-btrfs-space-r30.py`
- `tools/run-receipt.py`

Expected summary-key shape (angle-bracket values and ellipses are predicates/placeholders, not literal JSON tokens):

```text
{"revision":"6d76fb20f6ecbc940e5c8fff36c74060c885e161","targets":5,"channels":["names","quiet","source"],"pairs":15,"leaking":<integer >= 5>,"leaking_pairs":["tools/check-revision-binding.py:<channel>","tools/check-report-receipts.py:<channel>","tools/score-census-handoff-r32.py:<channel>","tools/mutants-btrfs-space-r30.py:<channel>","tools/run-receipt.py:<channel>",...],"harness_errors":[],"probe_sha256":"<64-hex>","probe_version":5,"target_set":"livefive","base":"6d76fb20f6ecbc940e5c8fff36c74060c885e161","scratch":"<temporary-path>","predicate_label":"leaking_pairs"}
```

The array must contain at least one actual `target:channel` string for each named target; `...` permits further leaking channels/targets. The exact `leaking` value and which of `names`, `quiet`, or `source` leaks for each target are not declared; do not replace those with invented observations. The acceptance condition is every target represented in `leaking_pairs`, not merely a total.


## Base sensitivity sets


The three expected summary objects have identical keys and types, `revision` and `base` equal to the declaration base, `harness_errors: []`, `leaking: 0`, and `leaking_pairs: []`; receipt/run exit is 0. With the inherited set definitions unchanged, expected totals are claim `targets: 9, pairs: 27`; r33claim `targets: 5, pairs: 15`; regression `targets: 11, pairs: 33`.

```text
{"revision":"6d76fb20f6ecbc940e5c8fff36c74060c885e161","targets":9,"channels":["names","quiet","source"],"pairs":27,"leaking":0,"leaking_pairs":[],"harness_errors":[],"probe_sha256":"<64-hex>","probe_version":5,"target_set":"claim","base":"6d76fb20f6ecbc940e5c8fff36c74060c885e161","scratch":"<temporary-path>","predicate_label":"leaking_pairs"}
{"revision":"6d76fb20f6ecbc940e5c8fff36c74060c885e161","targets":5,"channels":["names","quiet","source"],"pairs":15,"leaking":0,"leaking_pairs":[],"harness_errors":[],"probe_sha256":"<64-hex>","probe_version":5,"target_set":"r33claim","base":"6d76fb20f6ecbc940e5c8fff36c74060c885e161","scratch":"<temporary-path>","predicate_label":"leaking_pairs"}
{"revision":"6d76fb20f6ecbc940e5c8fff36c74060c885e161","targets":11,"channels":["names","quiet","source"],"pairs":33,"leaking":0,"leaking_pairs":[],"harness_errors":[],"probe_sha256":"<64-hex>","probe_version":5,"target_set":"regression","base":"6d76fb20f6ecbc940e5c8fff36c74060c885e161","scratch":"<temporary-path>","predicate_label":"leaking_pairs"}
```

## Mutant sensitivity sets

Each mutant receipt still has the outer runner header `revision` equal to the declaration base and `tool_sha256` equal to the same committed probe bytes. In the probe summary, `revision` is the named mutant commit and `base` is its parent (`879daa95b898b5c624c609eced31f7d0d5b933e8`); the set is `claim` (9 targets / 27 channel pairs). For each mutant, expect `harness_errors: []`, `leaking > 0`, and a nonempty `leaking_pairs` list. MutAttrgetterCopy changes `tools/check-section-citations.py`; MutPathCopy changes `tools/measure-update-recheck.py`. The prior round-34 evidence records that these mutants survived the old probe, so no exact r36 leak count or channel is asserted here.

The success condition for the full procedure is the summary predicates above and receipts for all five sensitivity runs plus the livefive run. A missing historical mutant repository is a dependency, not a passing sensitivity result.
