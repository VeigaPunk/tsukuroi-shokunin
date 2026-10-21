# ADJ-04 locality review — R20

**Axis:** C1 adjacency.

## Findings

**No actionable ADJ-04 boundary defect found in scope.** `PROVINCE.md:37-42` defines recipients as analysis/report owners, not repair permission; Tsukuroi retains the OS finding, no row authorizes the listed mutations, and unresolved ownership goes to the protocol integrator. ADJ-04 (`PROVINCE.md:49`) routes only fleet/wave attribution, liveness, or progress correlation, retains “OS memory, journal and boot diagnosis; cumulative counters are not dated incidents,” and limits the packet to capture/window context, exact counter or PSI command/exit/value, and the distinction between presence, cumulative count, and dated event. It asks for correlation, not causal attribution.

Keep the exact checklist rule at `PROVINCE.md:59-61`: “Select the matching row by the **question being asked**, not the binary or service name. Split mixed questions: keep OS diagnosis here; name only the requested sibling analysis.” This is a routing rule, not a grant of remediation or an ownership transfer. Preserve the sanitized-packet instructions at `:62-64` and separate closure states at `:65-68`: `prepared`, `reported`, `acknowledged`, `accepted`, and `resolved` are distinct; “Acknowledgement is not acceptance”; resolution requires owner-side closure evidence, and a missing substrate or disputed owner is not successful downstream handoff. The JSON contract independently says prepared implies no delivery or acceptance (`corpus/knowledge/adjacency-handoffs-fleet-r1.json:128-140`).

The observed R20 clarification is specifically OUT-009 / ADJ-06 (`PROVINCE.md:148-152`; `.ufo/waves/round-20/ownership-correction.txt:1`): it identifies Revenger’s declaration, says it is not a Tsukuroi grant, leaves Kaidoku/Revenger arbitration unresolved, denies the listed write permissions, and states that the other nine locators and handoff states are unchanged. It neither changes ADJ-04’s trigger/retained diagnosis/minimum packet nor implies a Mori acceptance or write authority. Retain that correction verbatim and keep the ADJ-04 checklist and row wording above; the clarification is not a substitute for them.

**Finite negative control:** The ADJ-04 route record’s explicit counterexample is: “A driver/boot repair question without fleet attribution remains tsukuroi even when mori reads the same journal” (`corpus/knowledge/adjacency-handoffs-fleet-r1.json:74-85`). Its `negative_recipient` is `tsukuroi`; its forbidden inference rejects treating cumulative `memory.events` as dating a new kill or identifying a responsible wave. Separately, the R20 C1 checker assignment requires altered, broadened, arbitration-resolved, or permission-grant correction text to yield `OWNERSHIP-CORRECTION-INVALID` (`.ufo/waves/round-20/build/dispatch.json:436`), consistent with preregistered `altered` expectation (`preregister.json:31-35`). These are specified controls, not observed test results.

## Residual risk and verification gaps

This was a static, scoped source review. The supplied tool inventory exposes no LSP device, so references/definitions/diagnostics were unavailable; conclusions above come from reopened source text, not LSP semantic proof. NO-EXEC limits prevented a baseline diff or C1 checker/negative-test run; current publication/integration and control behavior are therefore unverified. This review did not perform the outbound source-hash check or assess sibling state or recipient response.

Scope: executed=none
