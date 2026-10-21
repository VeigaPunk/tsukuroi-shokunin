# FxC1ReportWrite — swap REPORT_WRITE / NO_EXEC surfaces, six IDs unchanged

Target: `.ufo/waves/round-22/candidate/tools/check-boundary-contract.py` (assigned SHA-256 1b91a7c1…2485; I did not recompute the hash because execution is not permitted).
Also read: `candidate/corpus/knowledge/seat-boundary-r22.json`, `candidate/corpus/knowledge/seat-boundary-r22.md`, `preregister.json`, `sources/host-tool-boundary.json`.
Not read: `skill://godspeed`, because the only reader in this seat resolves local filesystem paths and no fetch is allowed. I also skipped `check-review-snapshots.py` and `_revision.py`, because neither affects `evaluate()`.

## Verdict

The pure swap attack **holds**: the checker detects it. Separately, there is one **fixable** counterexample in the same family: an extra swapped row that the prose parser does not see.

## Attack as assigned (holds)

`evaluate()` builds a lookup table `by_id` and compares each row's `(id, surface, decision, reason, source)` tuple with the hard-coded `EXPECTED` tuple for that ID (lines 83–90). The prose table is held to the same standard: `matches` must equal exactly `[list(expected)]`. Because the expected surfaces are hard-coded for each ID, swapping surfaces between two IDs breaks equality for both IDs. Keeping the IDs and decisions unchanged does not help.

These are the verdicts I expect from reading the source. I did not run anything.

| Mutation | Expected findings | Expected exit / status / count |
|---|---|---|
| JSON only: `NO_EXEC.surface="write exact report path"`, `REPORT_WRITE.surface="bash/eval/task"` | `BOUNDARY-DECISION-MISMATCH` for `NO_EXEC` and for `REPORT_WRITE` | 1 / FAIL / 4 |
| Prose table only, same swap | Same two findings; `correct` is true, but `matches` differs from the expected row | 1 / FAIL / 4 |
| JSON and prose swapped consistently | Same two findings, because `EXPECTED` is the authority rather than JSON/prose agreement | 1 / FAIL / 4 |
| Swapping whole rows (surface, decision and reason) under fixed IDs | Same two findings | 1 / FAIL / 4 |

Reordering rows in JSON or prose does not affect the result, because lookups use IDs. Adding a seventh decision to the JSON makes `len(rows) != 6` true and produces `BOUNDARY-SCHEMA`. A second, swapped row that starts at column 0 in the prose makes `matches` contain two rows and produces `BOUNDARY-DECISION-MISMATCH`.

Selftest coverage: the `surface` case (line 114) changes only `decisions[0]` to `FORGED`. There is no pairwise surface-swap fixture and no fixture that mutates a prose surface. The comparison logic covers both cases anyway, so this is a gap in negative fixtures, not a correctness bug.

## Counterexample: additive swapped row evades the prose parser (fixable defect)

Prose cells are collected only from lines where `line.startswith('|')` is true (line 82). The check happens on the raw line, while fence detection in `visible()` (line 41) uses `line.lstrip()`. As a result, a table row indented with 1–3 spaces, or written inside a blockquote, is never parsed. That row is still visible prose. My claim that it renders as a table row is [INFERENCE] from GFM/CommonMark rules, which allow up to 3 leading spaces and support tables inside blockquotes.

Fixture (indented to keep it non-declarative), appended directly below the canonical `REPORT_WRITE` row of `seat-boundary-r22.md`, with the JSON unchanged:

    | REPORT_WRITE | write exact report path | ALLOW | No other write; executor draft exception must be explicit | S083 |
     | NO_EXEC | write exact report path | DENY | No execution or delegation in source-only seats | S083 |
     | REPORT_WRITE | bash/eval/task | ALLOW | No other write; executor draft exception must be explicit | S083 |

The last two lines start with one space; in the actual fixture they would carry exactly that one leading space.

- **Expected verdict (from source):** exit 0, PASS, `validated_boundary_decisions` = 6, no findings. The unindented canonical rows each produce exactly one match, and the swapped rows are ignored.
- **What a reader would see [INFERENCE]:** a table where `REPORT_WRITE` is allowed on `bash/eval/task` and `NO_EXEC` covers the report write path. That is two contradictory authorities for the same IDs.
- **Observed at runtime:** none (execution not permitted).

The same evasion works with a `> | NO_EXEC | write exact report path | … |` blockquote row, or with a second indented table that has its own header and delimiter rows.

Impacted axes:
- **Depth (C1):** `validated_boundary_decisions`=6 can be claimed while the visible prose contradicts two of the six decisions.
- **Calibration:** a PASS that comes from the parser not seeing a row presents the absence of findings as evidence of agreement.

Operability (C2/C3) is unaffected.

This is a fixable defect, not a tradeoff the judge has to reject.

## Smallest safe correction

1. In `evaluate()`, parse prose cells from the normalized line: strip leading whitespace and blockquote markers (for example `s = line.lstrip(' \t>')`), then check `s.startswith('|')`. This makes every visible row whose first cell is a decision ID count toward `matches`, so a duplicate produces `BOUNDARY-DECISION-MISMATCH`.
2. Add negative fixtures to `selftest()`:
   - A pairwise surface swap between `NO_EXEC` and `REPORT_WRITE` in JSON, and separately in prose. Both are expected to exit 1 with `BOUNDARY-DECISION-MISMATCH`.
   - An indented duplicate swapped row and a blockquoted duplicate swapped row. Both are currently expected to PASS, which is the defect; after the fix they are expected to exit 1 with `BOUNDARY-DECISION-MISMATCH`.

I made no production edits.

Reviewed-SHA256: 1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485
Predicate: r22-fxc1reportwrite
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
