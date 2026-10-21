# FxC1Dead — source-only DEAD decision probe

Axes: C1 semantic fidelity; detector independence; evidence honesty and source-byte preservation.

## Assigned mutant and scope

One conceptual defect, M1: in `candidate/tools/check-boundary-contract.py:24`, change only the DEAD tuple's decision from `UNKNOWN` to `ALLOW`. Keep its surface, reason, source and all other code unchanged. No mutant was written: this seat permits source analysis and its named report only, not mutation or execution.

Read the bound boundary checker, its JSON/Markdown contract, preregistration, host-boundary evidence and the relevant strict-review checker sections. No command, import, test, example, subprocess, network fetch or delegation was performed. No production, candidate, build-report or sibling file was written.

## Source-visible result

**The pristine contract preserves the distinction, but the built-in selftest has a concrete oracle-coupling gap for M1.** This is a source-derived coverage finding, not an observed surviving runtime mutant.

The boundary checker pins DEAD to UNKNOWN at line 24. Its JSON contract independently contains that value at lines 40–44, and its visible Markdown table contains it at line 18. `evaluate()` compares every five-field JSON tuple and visible table row against `EXPECTED` (checker lines 83–92). Consequently, with otherwise valid inputs, an ALLOW decision in either contract representation produces `BOUNDARY-DECISION-MISMATCH` at DEAD; it cannot count as the sixth validated decision under the pristine checker.

However, `selftest()` generates both its clean JSON and its clean prose directly from the same `EXPECTED` tuple being challenged (lines 104–105). M1 therefore changes the implementation oracle and its positive fixture together. The six negative decision fixtures replace their selected value with FORGED (lines 110–113), so they still disagree with either UNKNOWN or ALLOW. None independently asserts that DEAD must remain UNKNOWN. The other fixtures do not introduce an independent DEAD oracle.

## Expected detector outputs — inference only

The following are static predictions, not captured output. The fixture verdict and runtime verdict must remain separate.

| Bounded detector/input | Pristine prediction | M1 prediction | Restored-byte prediction |
|---|---|---|---|
| Existing selftest, using its own fixture construction | Exit 0; PASS; 19 cases; 0 failed | Exit 0; PASS; 19 cases; 0 failed | Same as pristine |
| `evaluate()` with a fixed independent UNKNOWN contract fixture and the valid sources/host fixture literals at lines 106–108 | Exit 0; PASS; 6 validated decisions; no findings | Exit 1; FAIL; 5 validated decisions; `BOUNDARY-DECISION-MISMATCH` at DEAD | Same as pristine |

[INFERENCE] The first detector would let M1 survive because it regenerates its input from the mutated oracle. The second would kill M1 because its input remains pinned independently. These are two detector views of the same single conceptual mutation, not additional applied mutations.

The second prediction is bounded to valid fixture inputs. The actual revision-mode result is unobserved: revision binding and the committed source registry were not executed or inspected outside the seat's read binding. A baseline read/binding failure would be inconclusive, not a killed mutant.

## Absent is not zero earlier requests

A concrete logical counterexample consists of two possible histories:

- H0: a provider dies before any request; no final report exists.
- H1: a seat first requests a forbidden execution tool, then the provider dies; no final report exists.

These are analytical histories, not executed examples or newly observed incidents. Final-report absence is identical in H0 and H1. It therefore cannot establish zero earlier requests, much less permission or conformance. The candidate's own Markdown at lines 7 and 24 explicitly distinguishes earlier forbidden requests from later provider failure; underlying historical logs were not read in this seat.

A known forbidden request remains a request-audit violation despite death. Incomplete trace coverage leaves activity unresolved; it is not an empty request list. Even a complete empty trace supports only no recorded requests within that coverage, not a preventive runtime guarantee or proof of effects. The host evidence states there is no native per-seat allowlist (`sources/host-tool-boundary.json:9–12`), so death cannot substitute for one.

The separate strict-review checker likewise does not turn absence into success: `check-review-snapshots.py:98–99` adds `REVIEW-REPORT-MISSING`; lines 119–128 retain findings and explicitly bound the checker to declarations, not command nonexecution. Its `read-failed-retains-missing` fixture (lines 214–234) expects the missing-report finding to survive a later read failure. Preregistration's C3 bound separately accounts for absent-dead and absent-unresolved seats rather than calling either delivered-conformant. These are source observations, not runtime results.

## Actual output, verdict and preservation

Actual behavioral output: none. Pristine, mutated and restored detector runs were all prohibited and not attempted.

Runtime mutation verdict: **INCONCLUSIVE / NOT EXECUTED**. Static finding: **predicted selftest survival**, while a fixed independent UNKNOWN fixture is predicted to reject M1. No observed killed/survived result is claimed, and the UNKNOWN contract is not changed.

Before hash: the supplied target SHA-256 is recorded in the receipt below; it was not independently recomputed. After/restoration hash: not measured under NO-EXEC. Preservation evidence: tool actions consisted only of authorized source reads/search and creation of this report; no candidate bytes were written, so no restoration write was needed. Exact before/after hash equality is not presented as a measured result. No tool was installed or updated.

Reviewed-SHA256: 1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485
Predicate: r22-fxc1dead
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
