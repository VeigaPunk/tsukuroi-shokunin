# MapMetricExact — C3 metric mutation design, not executed

## Scope and axes

Primary axis: **calibration**, specifically the exact `audit_live_map_errors` transition **1 → 0**, not merely a failing-before/passing-after process exit. Secondary concern: consistency between that metric and the emitted findings. C1 adjacency and C2 operability are outside this probe. No host, boot-image, or boot-readiness conclusion follows.

This is one proposed mutation only. No candidate bytes, fixtures, Git state, or execution artifacts were changed. All numeric behavior below is **[INFERENCE] from inspected source**, not observed detector output.

Evidence aliases:

- `G` = `/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py`.
- `I` = `/tmp/tsukuroi-r20-registry-20261021/SKILL.md`.
- `L` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
- `P` = `L/.ufo/waves/round-20/preregister.json`.
- `M` = `L/.ufo/waves/round-20/measure/run.py`.

The registry candidate assignment is recorded at `L/.ufo/waves/round-20/worktree-bindings.json:2-7`. The preregistered C3 metric, baseline/target values, mode, and finite contract are `P:21-27`; its explicit legacy/corrected expectations are `P:49-53`.

## One smallest behavior-bearing mutation

**Target: `G:355`, inside the existing `if args.audit_live_map:` block (`G:354-355`).**

Original expression:

```python
counts["audit_live_map_errors"] = len(map_findings)
```

Proposed replacement, not applied:

```python
counts["audit_live_map_errors"] = len(map_findings) or 1
```

This single-expression mutation models a plausible truthiness-default defect: a developer uses `1` as an error/default sentinel and accidentally treats the legitimate count `0` as missing. It does not change the map parser, the expected map constant, the finding list, source fixtures, mode selection, or exit-code calculation.

**[INFERENCE] Effect:** corrected source produces no map findings, but `0 or 1` reports **1**, so the measured metric remains **1 → 1**. Legacy source still produces one map finding and still reports **1**. The underlying rejection/acceptance exits remain **1 → 0**, because `G:361-362` computes the return code from `findings`, not from the metric.

## Source evidence and bounded inputs

1. The canonical corrected map explicitly separates live `0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate` from selftest `0 PASS;1 FAIL`, usage `2`, and the no-live-DEGRADED/no-clearance qualifications (`G:31-34`). `_audit_live_map` requires exactly one matching row and an exact whitespace-normalized map; it returns one finding for a mismatch and an empty list for a match (`G:277-288`). The operative table selector chooses the unique highest round rather than historical rows (`G:137-158`).
2. The inherited candidate documentation still has the round19 heading and legacy `0 CONSISTENT;1 DEGRADED;2 UNKNOWN` row (`I:2060`, `I:2073`). The lane contains the appended round20 heading and corrected row (`L/SKILL.md:2096-2109`). These are distinct inspected sources; this report does not pretend the inherited worktree already contains the lane's corrected table or prove either file's committed revision identity.
3. Existing declared clean fixtures provide a tighter detector without depending on unrelated lane coverage: the corrected row and its exact success assertion are at `G:565-581`; the legacy fixture inserts live `1 DEGRADED` and requires exactly one `REGISTRY-AUDIT-LIVE-MAP` finding and metric 1 (`G:569-590`). Their common fixture tool declares `--selftest` (`G:565`), and the normal probe coverage check requires codes 0 and 2, which both maps contain (`G:233-240`).
4. Production mode appends map findings to normal findings and derives the new metric only in explicit audit mode (`G:350-355`). `_emit` serializes `counts` and `findings` independently (`G:297-303`). Thus this mutation creates a metric-only false error, not an actual newly detected map error.

## Finite before/after assertion and expected detector

**Detector design, not an instruction executed by this seat:** freeze the two existing C3 fixture cases `audit-live-map-live1` and `audit-live-map-correct`, their explicit `audit_live_map=True` invocations, and their assertions from `G:575-590`. Use those same inputs and unchanged assertions for pristine evaluator bytes, the single proposed mutation, and exact restored evaluator bytes. The helper adds `--audit-live-map` and captures the returned JSON (`G:433-443`).

For clean fixtures, the fixed before/after assertion is:

- **Before / legacy:** exit `1`, status `FAIL`, `counts.audit_live_map_errors == 1`, and exactly one finding with ID `REGISTRY-AUDIT-LIVE-MAP`.
- **After / corrected:** exit `0`, status `PASS`, `counts.audit_live_map_errors == 0`, and `findings == []`.
- Therefore the ordered metric pair must be **(1, 0)**, not just the ordered exit pair **(1, 0)**. Additionally, the metric must equal the number of emitted `REGISTRY-AUDIT-LIVE-MAP` findings for these inputs.

Predicted projections, all **[INFERENCE]**, assuming the declared clean fixtures reach the normal result path:

| Evaluator bytes | Source fixture | Exit / status | `audit_live_map_errors` | `counts.findings` / finding IDs |
| --- | --- | --- | --- | --- |
| Pristine | Legacy / before | `1 / FAIL` | `1` | `1 / [REGISTRY-AUDIT-LIVE-MAP]` |
| Pristine | Corrected / after | `0 / PASS` | `0` | `0 / []` |
| Mutated | Legacy / before | `1 / FAIL` | `1` | `1 / [REGISTRY-AUDIT-LIVE-MAP]` |
| Mutated | Corrected / after | `0 / PASS` | **`1`** | `0 / []` |
| Exactly restored | Legacy / before | `1 / FAIL` | `1` | `1 / [REGISTRY-AUDIT-LIVE-MAP]` |
| Exactly restored | Corrected / after | `0 / PASS` | `0` | `0 / []` |

The corrected-case predicate at `G:579-581` explicitly requires metric 0, so **[INFERENCE] it would reject this mutant**, even though its process exit remains 0 and findings remain empty. The separate highest-table corrected case also explicitly requires metric 0 (`G:595-603`). These predicates are literal numeric assertions, not comparisons against the mutated assignment.

A pristine detector failure would make any later mutation result **inconclusive**, not a kill. Likewise, failure to return to the pristine result after restoration would invalidate the probe. Neither baseline success nor restoration success has been measured here.

## Exit-only evidence limitation

The R20 measurement recorder saves stdout/stderr and sets `matched_exit` solely from the return code (`M:31-44`). The C3 pair supplies the expected exits 1 then 0 (`M:70-78`); those two exit receipts alone would not detect this metric corruption. **[INFERENCE] both `matched_exit` values could remain true while the metric pair is (1, 1).**

This is a limitation of those receipts, not a claim that the complete evaluator would let the mutant survive: the full measurement script also schedules tool selftests (`M:65-69`), and the candidate's declared corrected-case assertion checks the precise metric. No selftest or measurement output was produced or observed by this seat.

## Actual output, verdict, and restoration evidence

- **Actual detector stdout/stderr/exit:** none; no detector was invoked.
- **Verdict:** **NOT EXECUTED / empirical outcome inconclusive**. The source-level prediction is detection by the exact-metric corrected-case predicate, but no killed or survived result is claimed.
- **Mutation/restoration:** neither applied nor performed. The only write by this seat is this named report; inspected candidate and lane source files were read-only.
- **Before / mutated / restored hashes:** not computed and not asserted. There is no mutated image or restored image to hash. No hash-equality or exact-restoration measurement is fabricated. An authorized future execution would need byte snapshots and before/mutated/restored hashes, and exact restoration even on detector failure; that is outside this NO-EXEC assignment.
- **Tools installed or updated:** none.

## Limits

This is a finite metric-wiring challenge to one explicit mode and two declared fixtures, not a general parser proof, arbitrary-shell analysis, runtime enforcement claim, or evidence of current host state. Binding failures, malformed tables, or unrelated coverage errors must not be mistaken for this mutation's result: table/revision exception paths return `CANNOT_EVALUATE` without the audit metric (`G:363-373`). Source inspection cannot establish that the complete pristine suite passes. Default mode never reaches the changed assignment (`G:354-355`), but no default-mode run was performed. Boot images remain **UNKNOWN**; neither live 0 nor live 2 is operational clearance (`L/SKILL.md:2086`, `L/SKILL.md:2109`).

Scope: executed=none.
