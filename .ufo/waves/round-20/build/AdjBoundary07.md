# ADJ-07 locality review — R20

## Finding

**No actionable ADJ-07 locality defect found in scope.** C1 is adjacency; this is a no-write boundary review, not a score or acceptance claim.

`PROVINCE.md:52` routes only a census blind spot that raises a reusable verification/mutation-testing question to `tameshi`. Tsukuroi explicitly retains the census bug, domain contract, implementation and repair; the minimum packet is a failing behavior, command/exit, measured census revision and expected invariant, asking for “method advice, not transfer of gate ownership or a general claim from one lane.” The matching JSON route remains `contract-only` (`corpus/knowledge/adjacency-handoffs-fleet-r1.json:115-125`); its finite counterexample is “A package repair or ordinary census implementation bug without a reusable-method question remains tsukuroi,” and its forbidden inference rejects both generalizing from one lane and transferring census-code ownership.

Question-based routing does **not** grant remediation authority or imply recipient acceptance. Preserve the exact checklist wording in `PROVINCE.md:59-68`: “Select the matching row by the question being asked, not the binary or service name. Split mixed questions: keep OS diagnosis here; name only the requested sibling analysis”; then prepare/report the sanitized packet. The distinct `prepared`, `reported`, `acknowledged`, `accepted`, `resolved` states remain controlling: acknowledgement is not acceptance, resolution requires owner-side closure evidence, and a disputed owner is not a successful handoff. ADJ-07’s recipient is for method advice, not gate repair. No ADJ-07 packet or recipient-side outcome is claimed by its `contract-only` route evidence (`...json:123-125`).

The observed R20 correction is explicitly OUT-009/ADJ-06, not an ADJ-07 request (`PROVINCE.md:148-152`; `.ufo/waves/round-20/ownership-correction.txt:1`). Preserve “It is not a tsukuroi grant of ownership” and “Kaidoku/Revenger arbitration remains unresolved; ask the protocol integrator before an internals handoff,” along with the no-write clause. Those words attribute a sibling declaration while refusing owner selection and write authority; they do not assert arbitrator or recipient acceptance, nor change ADJ-07's method-only boundary.

## Finite negative control

The finite ownership-transfer negative must alter the correction’s non-grant wording—for example, replace “It is not a tsukuroi grant of ownership” with “It grants tsukuroi ownership”—and require `OWNERSHIP-CORRECTION-INVALID`, never count it as a valid correction. This is consistent with preregistered C1 expected `altered: OWNERSHIP-CORRECTION-INVALID` (`preregister.json:31-35`) and the C1 task’s required invalidation of altered/broadened/permission-grant wording (`build/dispatch.json:436`). Separately, retain the ADJ-07 package-repair/ordinary-implementation counterexample above as the finite route-level negative: absent a reusable-method question, it remains in Tsukuroi.

## Residual risk and verification gaps

Static source reads only; no baseline diff or C1 checker/selftest was run, so the finite negative control is a specified expectation, not an observed test result, and publication/integration is not certified. The assigned tool inventory exposes no LSP device; no LSP references, definitions or diagnostics were obtained. This review did not perform the outbound source-hash check, inspect live sibling state, or infer any recipient response.

Scope: executed=none