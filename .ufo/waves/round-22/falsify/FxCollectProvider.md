# FxCollectProvider — source-only falsification

## Axes and scope

Axes: faithful observed-error attribution; safe omission of unknown/sensitive error text; source-only evidence integrity.

Reviewed the assigned candidate collector and the declared supporting contract/receipt sources only. No commands, imports, tests, examples, mutations, network access, delegation, installations, or production edits were performed. This is post-hoc evidence review, not preventive runtime enforcement.

Primary source: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/.ufo/waves/round-22/collect.py`, especially lines 88–107 and 120–123. The receipt digest below is the assignment's supplied fingerprint; it was not independently recomputed.

## Finding: a known substring admits an otherwise unknown sensitive error

**Source-visible counterexample to the sanitization claim.** The behavior-bearing point is line 97: any occurrence of a listed token admits the entire first 1,200 characters of the original error, provided a narrow sensitive-text blacklist does not match. This is substring admission, not extraction of a known provider category.

One bounded, hypothetical terminal assistant message has these field values (synthetic data, not executed):

    stopReason = "error"
    content = []
    provider = "fixture-provider"
    model = "fixture-model"
    errorMessage = "TransportError: unexpected payload; note=rate limit; password=R22_SYNTHETIC_ONLY"

This is an otherwise unclassified transport error with an incidental known phrase and a synthetic password field. No real credential is included.

Source derivation:

1. Lines 89–90 classify the nonempty string plus `stopReason="error"` as a terminal error.
2. Line 96 lists `rate limit`, which occurs in the message. It need not be the error's category or leading text.
3. Line 97 checks only `bearer `, `api[_-]?key`, `token=`, and `cookie`, case-insensitively. None occurs in this message; `password=` is not covered.
4. The message is shorter than 1,200 characters, so line 97 selects it unchanged instead of the omission marker.
5. Lines 98 and 123 place that value in the failed settlement row and write it to `settlement.json`. JSON serialization does not remove the sensitive field.

**Expected detector:** for this unknown/sensitive terminal error, require `outcome="failed"`, omission of `R22_SYNTHETIC_ONLY`, and an omitted/unclassified error representation rather than the raw diagnostic. Independently require that provider/model metadata not be transformed into an inferred provider-death cause.

**Expected fixture verdict:** FAIL for safe sanitization on the pristine candidate; PASS for the bounded no-provider-cause-inference check. These are source-derived expectations, not exercised detector results.

**Predicted output [INFERENCE]:** the settlement row has `outcome="failed"`, `error="TransportError: unexpected payload; note=rate limit; password=R22_SYNTHETIC_ONLY"`, `answering_provider="fixture-provider"`, and `answering_model="fixture-model"`. The intended generic omission string is not selected.

**Observed runtime output:** none. The collector and detector were not run. There is no measured baseline failure, killed mutant, or surviving mutant.

## Bounded attribution result

Within the visible terminal classification, the collector does not infer provider death from missing output:

- Lines 94–98 record an observed terminal assistant error as `failed`.
- Lines 99–100 record successful terminal assistant text as `completed`.
- Lines 101–102 explicitly say `cause unproven` when a session exit lacks a successful final assistant text.
- Without these conditions, the initialized outcome remains `unknown` (line 45).
- Lines 103–104 copy provider/model fields from the last recorded assistant message; line 121 explicitly disclaims inferred provider causes. This supports metadata attribution only, not causal proof or proof that the named provider successfully answered.

For a terminal error without any listed known token, line 97 does select the generic omission marker. The counterexample defeats that bound because a known substring anywhere in unknown diagnostic text authorizes copying the surrounding text. No claim about actual host/provider failures follows from this synthetic case.

## Probe verdict and byte preservation

- Mutant: none applied; source-only tasking prohibits mutations. The single challenged defect is line 97's raw-error admission condition.
- Verdict: concrete source-visible sanitization counterexample. Runtime mutation verdict: **INCONCLUSIVE / not executed**, not killed or survived. A predicted pristine failure cannot count as killing a mutant.
- Before hash: assignment-supplied fingerprint in the receipt; no independently measured hash.
- After/restored hash: not measured. No writes were made to the collector or any source file, so no restoration operation was needed. Exact-byte restoration was not independently verified.
- Actual artifact output: this scoped report only. Build reports remain untouched.

Reviewed-SHA256: 3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a
Predicate: r22-fxcollectprovider
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
