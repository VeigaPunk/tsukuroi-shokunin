# ADJ-03 locality review — R20

## Finding

**No actionable ADJ-03 boundary defect found in scope.** C1 is adjacency; this is a no-write locality review, not a score or acceptance claim.

`PROVINCE.md:48` routes only a configuration-level desktop question—“Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis”—to mado. It retains “User-manager/unit, package and driver health” in Tsukuroi, says an active unit does not prove UI operation, and limits the packet to an observed UI symptom/time, relevant OS probe/exit, and a configuration-surface pointer “without copying its contents”; “Mado verifies file/screenshot behavior itself.” This matches mado's declaration that config trees are read-only and the operator applies changes, and that it never mutates compositor state (`../mado-shokunin/PROVINCE.md:11-16`).

The question-based rule does **not** grant remediation or imply recipient acceptance. The exact locality wording to preserve is `PROVINCE.md:59-61`: “Select the matching row by the **question being asked**, not the binary or service name. Split mixed questions: keep OS diagnosis here; name only the requested sibling analysis.” Preserve the closure distinction at `:65-68`: `prepared`, `reported`, `acknowledged`, `accepted`, `resolved` are separate; “Acknowledgement is not acceptance”; resolution needs owner-side closure evidence; a disputed owner is not a successful handoff. Do not turn the mado recipient cell into write authority, acceptance, or a transfer of Tsukuroi's retained OS diagnosis.

The proposed R20 OUT-009 clarification is separate from ADJ-03: the observed lane text at `PROVINCE.md:148-152` attributes OUT-009 to Revenger, says it is not a Tsukuroi grant, leaves Kaidoku/Revenger arbitration unresolved, and denies configuration/service/package/boot/sibling-file write authorization. That wording does not amend ADJ-03 or its handoff lifecycle. Keep the explicit non-grant, unresolved-arbitration, and no-write wording; it is consistent with, not a replacement for, the ADJ-03 locality text above.

## Finite ownership-transfer control

The C1 preregistration expects a missing correction to yield `OWNERSHIP-CORRECTION-MISSING`, altered correction to yield `OWNERSHIP-CORRECTION-INVALID`, and the positive correction to count as 1 (`.ufo/waves/round-20/preregister.json:31-35`). The assigned-worktree checker defines the exact correction and requires the exact unique section plus the original ADJ-06 arbitration context (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:43-64,158-178`). Its finite fixtures explicitly mutate “It is not a tsukuroi grant of ownership.” to “It grants tsukuroi ownership.” and expect INVALID; removing the arbitration lines also expects INVALID. Missing section, duplicate heading, and unpinned snapshot are separate negative fixtures (`:1096-1113`). These are source-defined controls, **not executed results**; they reject the concrete ownership-transfer mutant but do not establish runtime authorization enforcement or cover arbitrary semantic rewrites.

## Residual risk and verification gaps

Current working-tree wording was read, but no Git/baseline comparison or C1 gate/selftest was run, so publication, integration, and measured outcomes are unverified. This review intentionally does not perform the outbound source-hash check. The requested LSP device is unavailable in the supplied tool set (`xd://lsp` returned “No such tool”; only `ast_edit` and `debug` are mounted), so no LSP references/definitions/diagnostics were obtained; static source reads above are the evidence, not semantic LSP proof. No live UI symptom or recipient response was examined.

Scope: executed=none