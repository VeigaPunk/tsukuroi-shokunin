# FxC3Unresolved — source-only falsification of `tools/check-review-cohort.py`

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3unresolved
Scope: executed=none

Lane bounds: leaf member — no subagent dispatch.

The digest above is the assignment's declared target digest. This seat could not recompute it because it may not execute anything. The candidate bytes were read with the `read` tool only.

## Attack

The claim under attack: when a report is missing and the settlement outcome is `completed` or `unknown`, the seat is counted as `absent_unresolved`, the tool exits 1, and the cohort cannot pass ("cannot green").

## Verdict

The claim **holds as literally stated.** There is one refinement: the exit code is 1 *or 2*, never 0. Separately, there are three counterexamples to the *intent* of the claim. Each one lets a seat that has no usable report reach exit 0 without ever being counted as `absent_unresolved`.

### Why the literal claim holds (bounded source reasoning)

- Lines 58–59 cover the category assignment. When `report is None` and `outcome['outcome'] != 'failed'`, the only outcomes left are `completed` and `unknown`, because line 42 restricts outcome to `('completed','failed','unknown')`. The seat is therefore categorised as `absent_unresolved`.
- Lines 66–67 add a finding: any nonzero `counts['absent_unresolved']` appends `COHORT-UNRESOLVED`.
- Line 70 sets `code = 2 if strict_code == 2 else (1 if findings else 0)`. Because the findings list is non-empty, the code is 1, or 2 if the strict evaluator could not evaluate. No later statement clears `findings` or resets `code`.
- The exception paths at lines 75–78 all set code 2. An uncaught exception ends the interpreter with a traceback and status 1. Neither path can produce 0.
- `--revision` mode: in `git_read` (lines 124–131), a missing path returns `None` only when `git show` fails *and* `ls-tree` prints nothing. Every other failure raises `RuntimeError`, which becomes `COHORT-READ` with exit 2. So an unreadable report cannot be silently treated as delivered.
- Refinement: if a missing `completed` report shares the cohort with any seat whose report is invalid UTF-8, the full strict pass returns `strict_code == 2` and the exit is **2**, not 1. A read error elsewhere has the same effect. The verdict is CANNOT_EVALUATE rather than FAIL. It is still not green, but "exit 1" is not unconditional.

**Expected fixture verdict.** The selftest case `missing-unresolved` (line 97) should give exit 1, `absent_unresolved == 1`, finding `COHORT-UNRESOLVED`, and `strict_receipt_exit == 1`. **Observed runtime:** none, because nothing was executed.

### Counterexample 1: relabelling the settlement turns `absent_unresolved` into `absent_dead` and exits 0 (strongest)

The settlement file is the only authority that separates a dead seat from an unresolved one. Line 44 rejects `failed` only when `error` is blank. Any non-blank free text is accepted, such as `"x"` or `"observed provider failure"`.

Consider a seat that actually completed but left no committed report. If the settlement row records it as `{"outcome":"failed","error":"x"}`, then:

- line 59 classifies it as `absent_dead`;
- `COHORT-UNRESOLVED` is never added;
- line 70 gives `code = 0` and status `PASS`.

The selftest `dead-missing` (line 95) asserts exactly this exit 0. `false-death` (line 104) covers only the blank-error variant. Nothing ties `error` to retained provider evidence or event traces. This matters because checklist item 3 asks for "observed error attribution" to be preserved, and the tool checks only that the field is non-blank.

There is also a cross-authority tension. `seat-boundary-r22.json` decision `DEAD` classifies "missing final or provider death" as **UNKNOWN**, while the cohort tool's `absent_dead` resolves to green. Two authorities disagree on the same seat.

- **Expected fixture verdict:** exit 0, category `absent_dead`, `strict_conformance: FAIL`.
- **Observed runtime:** none.

### Counterexample 2: a placeholder report turns `absent_unresolved` into `delivered_faulty` and exits 0

A report counts as "missing" only when the committed path is absent (`git_read` returns `None`). If any bytes exist at the path, even `b''` or `b'partial'`, line 61 assigns `delivered_faulty`.

`delivered_faulty` adds no cohort finding, so line 70 yields 0. The selftest cases `partial-failed`, `period`, `predicate`, `digest`, `duplicate-receipt` and `unicode` all assert exit 0 for faulty reports.

Two further shapes are treated as delivered rather than absent:

- A report path that is a **tree** in the commit. `git show rev:dir` prints a listing with return code 0. **[INFERENCE]**, git behaviour not exercised.
- A report path that is a **symlink** blob.

So committing an empty file greens a seat that delivered nothing. `C3_bound` explicitly scopes C3 as "detection and evidence, not an every-receipt-conforms claim", and `strict_conformance` stays `FAIL` in the output. This is therefore a **tradeoff the judge must weigh, not a tool defect**, but it does weaken "missing ⇒ cannot green".

- **Expected fixture verdict:** exit 0, category `delivered_faulty`, `strict_receipt_exit == 1`.
- **Observed runtime:** none.

### Counterexample 3: the metric reads 1 even when the cohort is not green

`cohort_accounting_mode: 1` is emitted on:

- the `absent_unresolved` exit-1 result (line 71);
- `COHORT-SCHEMA` exit 2 (line 76);
- `COHORT-READ` exit 2 (line 78).

It is 0 only when the manifest is missing (line 24). It is absent entirely on `RevisionError` and on the `main` read-error paths (lines 156–158).

`preregister.json` C3 names the metric `cohort_accounting_mode` with target 1. If a scorer reads only the metric and not the exit or status, an `absent_unresolved` or CANNOT_EVALUATE run would score the target. **[INFERENCE]**: the judge's scoring rule was not in the bound read paths.

## Impacted axes

- **calibration (C3):** the dead/unresolved split relies on an unverified settlement authority (counterexample 1). Placeholder bytes count as delivered (counterexample 2). The metric is decoupled from the verdict (counterexample 3).
- **operability:** the boundary contract says `DEAD` = UNKNOWN, while the cohort tool treats `absent_dead` as green. That is a duplicate authority.
- **depth:** none of this conflicts with the six boundary decisions.

## Smallest safe corrections

1. **Defect, fixable.** Emit `cohort_accounting_mode: 1` only when `code == 0`, or require the judge to read exit and status together with the metric. Add fixtures asserting the metric value on the `missing-unresolved` and `COHORT-SCHEMA` cases.
2. **Tradeoff, the judge must decide.** Require each `failed` settlement row to cite verifiable evidence, for example an event or trace identifier the request-audit manifest can cross-check. Otherwise, state in the `SCOPE` string and in `seat-boundary-r22.md` that the settlement is trusted Main-authored attribution. Add a fixture with a free-text `failed`/`"x"` row that documents the accepted exit 0. Reconcile `absent_dead` with the contract's `DEAD` = UNKNOWN by renaming or documenting it, so the two authorities do not disagree.
3. **Tradeoff, document it.** Either add a cohort finding, such as `COHORT-FAULTY`, so that `delivered_faulty` cannot be green, or keep the current behaviour and state explicitly that exit 0 means "accounted", never "delivered".
