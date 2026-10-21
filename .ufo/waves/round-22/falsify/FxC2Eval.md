# FxC2Eval — source-only EXEC classification probe

## Axes and verdict

Axes: payload-independent EXEC classification; exact finding fidelity rather than exit-code-only detection; honest post-hoc and source-only evidence bounds.

**Static verdict: the assigned invariant holds within the supported request grammar.** No source-visible counterexample was found for `eval` or `functions.eval` with dictionary arguments, including hash-only code and browser-bearing code. This is a bounded source argument, not a successful runtime test or proof of preventive enforcement.

**Runtime/mutation verdict: INCONCLUSIVE — not exercised.** NO-EXEC and the exact report-only write binding prohibit running the detector, importing the candidate, applying a mutation, or executing example inputs. No production or candidate bytes were edited.

## Reviewed source and bounded argument

Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`.

1. `classify`, lines 59–62, first requires a nonempty string tool, dictionary arguments, and wrapper depth at most eight. Arguments with the expected `language` and `code` fields satisfy the dictionary requirement; their values are not interpreted.
2. Lines 73–76 remove one leading `functions.` and unconditionally return exactly `['SCOPE-EXEC-DENIED']` for `bash`, `eval`, or `task`. There is no hash-only, harmless-code, language, path, or binding exception on that branch. In particular, a hash-only eval remains EXEC even if it reads no file.
3. Browser classification is later, at lines 77–78, and examines the outer tool name, not an eval payload. Thus browser-bearing code in eval is EXEC, not merely FETCH. A separately recorded direct browser request is FETCH. This is precedence in a post-hoc classifier, not a promise that effects were prevented.
4. Recognized `multi_tool_use.parallel` and `parallel` wrappers recurse into every child at lines 63–72. A well-formed child `functions.eval` gets the same EXEC finding while its classification depth remains at most eight. The classifier neither invokes the child nor evaluates its code.
5. `evaluate`, lines 124–151, preserves that finding at the seat/event site. For an otherwise valid, complete, single-seat, single-event trace, the predicted result is exit 1, status `FAIL`, one request, one violation, and `SCOPE-EXEC-DENIED` at `A:0`.

The quantification over dictionary arguments is stronger than checking a few code snippets: the EXEC return precedes every payload-sensitive path operation, and no eval payload operation exists on the reachable branch.

## Expected fixture verdicts — not observed runtime

Use the valid single-seat binding/trace structure already defined in the candidate selftest at lines 155–158, keeping the seat complete. Replace its sole event with each request below. These are report data only; no fixture was created or executed. Code strings are opaque classifier inputs, not assertions about browser API availability or successful execution.

| Fixture | Recorded request | Expected finding | Expected audit result |
|---|---|---|---|
| Hash-only bare eval | `eval`, arguments `{"language":"py","code":"import hashlib; print(hashlib.sha256(b'probe').hexdigest())"}` | `SCOPE-EXEC-DENIED` | exit 1 / `FAIL` |
| Hash-only qualified eval | `functions.eval`, same arguments | `SCOPE-EXEC-DENIED` | exit 1 / `FAIL` |
| Browser-bearing bare eval | `eval`, arguments `{"language":"js","code":"await browser.tabs.list()"}` | `SCOPE-EXEC-DENIED` | exit 1 / `FAIL` |
| Browser-bearing qualified eval | `functions.eval`, same browser-bearing arguments | `SCOPE-EXEC-DENIED` | exit 1 / `FAIL` |
| Wrapped hash-only eval | `multi_tool_use.parallel`, one `tool_uses` child with `recipient_name` = `functions.eval` and `parameters` = the hash-only arguments above | `SCOPE-EXEC-DENIED` | exit 1 / `FAIL`; one outer request |
| Wrapped browser-bearing eval | `parallel`, one equivalent `functions.eval` child carrying the browser-bearing arguments above | `SCOPE-EXEC-DENIED` | exit 1 / `FAIL`; one outer request |
| Direct-browser control | `browser`, dictionary arguments | `SCOPE-FETCH-DENIED` | exit 1 / `FAIL` |

Observed runtime output for every row: **none; not run**.

Malformed arguments, excessive nesting, invalid manifests, and incomplete traces are outside the exact EXEC-result bound: the source instead fails closed with schema/incomplete findings and `CANNOT_EVALUATE`. Unknown tool spellings are not aliases proved to be eval; they receive `SCOPE-TOOL-UNKNOWN`. None of those outcomes is evidence that an actual eval request was allowed.

## One proposed mutant and its detector

**Mutant M1, not applied:** at line 75, remove only `'eval'` from the tuple of EXEC-classified tools. This is a small behavior-bearing dispatch omission. Both bare and qualified eval would then reach lines 79–80 and return `SCOPE-TOOL-UNKNOWN`, including both assigned payload families.

**Expected detector:** the same single-event audit above must check the exact EXEC finding, not only exit 1 or status `FAIL`. On pristine source it is predicted to satisfy that expectation; on M1 it is predicted to fail it because UNKNOWN replaces EXEC; after exact restoration it is predicted to satisfy it again. Both pristine and M1 are predicted to remain exit 1 / `FAIL`, so an exit-only detector would miss this classification defect.

The existing selftest already includes bare `eval` with `{}` at lines 167–168 and checks the requested finding ID at line 195. It is therefore predicted to detect M1. That is a source-derived expectation, **not an observed kill**. The selftest does not explicitly enumerate the hash-only, browser-bearing, or qualified-eval payload cases above; the current unconditional branch supplies the bounded reason they hold, not evidence that those fixtures ran.

Actual pristine/mutated/restored detector outputs: none / none / none. Mutant disposition: not applied; runtime result inconclusive, neither killed nor survived.

## Scope, hashes, and restoration evidence

The preregistration's C2 claim is prompt-bound post-hoc request auditing. The declared host boundary says native per-seat allowlisting is absent; the boundary knowledge files and target's line 17 explicitly disclaim runtime prevention and effects/reading proof. Accordingly, “before effects” here can only mean that classification does not first inspect, execute, or excuse payload effects. It cannot mean that this auditor intercepts execution before it happens.

The SHA-256 in the receipt is the supplied target identity, not a digest independently recomputed by this seat. Measured before/after hashes are unavailable: no hash command, eval, import, or other runtime was authorized or invoked. No target mutation or restoration write was issued; only this report was written. The two source inspections returned the same tool snapshot tag `636F`, which is not a SHA-256 measurement. No restored-byte hash equality is claimed.

No detector, tests, imports, code examples, network requests, installations, delegation, or production edits were performed.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2eval
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
