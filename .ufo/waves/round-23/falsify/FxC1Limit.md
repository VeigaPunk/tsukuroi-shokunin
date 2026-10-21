# FxC1Limit — round23 falsify, attempt1

Attacked claim: C1 (`validated_edit_decisions` 0→8). Specifically the non-enforcement limit guard in `candidate/tools/check-edit-contract.py` line 153:

    if data.get('scope') != LIMIT or PROSE_LIMIT not in '\n'.join(visible(text)):

Verdict: FALSIFIED as a guard. The guard only checks that the phrase is present somewhere. It does not check whether that phrase is the operative statement, it allows a contradicting sentence elsewhere, and it allows the phrase to be hidden when the Markdown is rendered. The JSON half (`scope` exact equality, exact top-level and row key sets) holds. The landed prose is NOT currently overclaiming. In a bounded read of `candidate/corpus/knowledge/structured-edit-r23.md`, the word "enforcement" appears only on line 30, and it is negated there. So this is a latent, fixable checker defect, not a defect in the landed content.

All results below come from statically tracing `evaluate()` and `visible()`. No command was run (NO-EXEC).

## Counterexamples (each traces to exit 0, PASS, validated_edit_decisions=8)

Base: the landed JSON and prose, unchanged except for the edit shown.

1. Appended affirmative overclaim (the assigned attack). Add a new visible paragraph:

       The checker additionally provides native permission enforcement and blocks every undeclared edit at runtime.

   Trace: `PROSE_LIMIT` is still a substring of visible line 30, so the limit check passes. The table rows and key sets are unchanged, so no other finding fires. The count stays at 8 because line 159 zeroes it only when some finding is present.

2. Negation inversion inside the matched phrase. Replace line 30's sentence with:

       It is not native permission enforcement that is missing: every edit target is natively enforced.

   This passes because the check is a substring test, not a sentence boundary or exact-line test.

3. Retracted phrase (strikethrough). Use `~~It is not native permission enforcement~~, it is native enforcement.` `visible()` has no inline-markup handling, so the substring survives and the check passes.

4. Phrase that never renders (link reference definition). Delete line 30 and add:

       [It is not native permission enforcement]: <>

   CommonMark renders nothing for a link reference definition. `visible()` drops only HTML comments, fenced code and 4-space-indented lines, so it keeps this line and the check passes. The reader never sees any limit.

5. Heading or front-matter overclaim. Change the title to `# Native-enforced structured edit authority`, or change `recheck:` to claim enforcement. These lines are never screened, so the change passes.

6. Silent deletion of companion limits. Remove "This is declared post-hoc audit authority only." and "The task API still has no restrictive per-seat allowlist." Neither sentence is pinned, so the change passes. The second sentence is the prose mirror of preregister `limits[0]`, "No native per-seat restrictive tool interface exists". Removing it leaves C1's prose without that preregistered limit.

Adjacent finding (same axis, evidence half). `evidence_ok()` does not restrict the top-level keys of the S086 observations file. Its `scope` ("…not … native permission enforcement…") can be rewritten to "native permission enforcement proven" and still pass. The `recorded_starts` entries are only checked to be a non-empty list. Their tool and path contents are not validated.

Selftest gap. `limit-omitted` covers only replacing the phrase. `hidden-limit` covers only an HTML comment. No case covers appending an overclaim, a negation inside the phrase, strikethrough, a link reference definition, or an unscreened heading. The clean fixture's own limit sentence ends after "a sandbox." and has no other text to screen against.

## Impacted axes

- C1 depth: the count of 8 can coexist with a document that asserts native enforcement. The metric says nothing about the limit's truth.
- Calibration / false provenance: the prose can claim prevention, which contradicts preregister `limits[0]` and `limits[1]` and the S086 source row ("not … runtime permission enforcement"). The checker would still certify it.
- C2 operability is indirectly affected. Its scope says "no native enforcement/effects claim", and C1's prose is the reader-facing carrier for that claim.

## Smallest safe in-scope remedy (checker + selftest only, no prose change needed)

1. Replace the substring test with an exact-line pin. Require exactly one visible line equal to the landed line 30, and keep the `scope` equality as is:

       This is declared post-hoc audit authority only. It is not native permission enforcement, a sandbox, body/patch interpretation, actual reading or effects proof, complete recorder coverage, or permission for host/package/service/boot actions. The task API still has no restrictive per-seat allowlist. Numeric mode availability is not compliance.

2. Reject any other visible line matching `(?i)enforc|sandbox|prevent`. In the landed prose these tokens occur only in the pinned line, so the landed state stays green. Also reject `~~` and link reference definition lines (`^\s{0,3}\[[^\]]+\]:`) anywhere in the visible text.
3. Add one literal selftest mutant for each of counterexamples 1–5, each expecting `EDIT-LIMIT-MISSING`.
4. Restrict the evidence top-level keys exactly to `{schema, observations, scope}` and pin its `scope` string.

Residual risk: a deny-list cannot catch synonyms such as "guarantees" or "cannot write outside". The complete fix is to pin the whole visible prose to a frozen SHA-256 declared in the preregister. That fix would need a preregister change, which is outside this seat's write scope and is left to L1.

Bounded search performed: every line of the bound checker, the landed prose and JSON, preregister lines 25–119, S086 in SOURCES.md, and the evidence `scope`. No further paths were read. No installs (NO-EXEC/NO-FETCH seat).

Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxc1limit
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
