# ADJ-01 no-write locality review — R20

Axes: C1 adjacency (reviewed); C2 operability and C3 calibration (not assessed).

## Findings by severity

**No actionable ADJ-01 boundary defect found in the reviewed text.** Question-based routing does not grant remedial permission or imply recipient acceptance: `PROVINCE.md:37-42` says the recipient is an analysis/report owner, “not permission to repair,” Tsukuroi retains the OS finding, no row authorizes configuration writes, service changes, credential reads, endpoint requests or target execution, and unresolved ownership goes to the protocol integrator—not whichever lane answered first.

The ADJ-01 contract is bounded at `PROVINCE.md:46`: the trigger is a wrong local endpoint or served-model identity, which GPU readiness alone cannot decide; Tsukuroi retains kernel, driver, device and user-unit state; the packet is capture time, driver query and unit-state command/exit, plus a reported endpoint symptom without credentials. The line explicitly requires Kama to obtain its own endpoint evidence and forbids endpoint diagnosis from `nvidia-smi`. Preserve this trigger, retained evidence, minimum packet, and independent-evidence clause verbatim.

Preserve the exact routing and lifecycle language at `PROVINCE.md:59-68`: “Select the matching row by the **question being asked**, not the binary or service name”; “Split mixed questions: keep OS diagnosis here; name only the requested sibling analysis”; and the separate `prepared`, `reported`, `acknowledged`, `accepted`, `resolved` states. “Acknowledgement is not acceptance”; resolution requires owner-side closure evidence; missing substrate or disputed ownership is an explicit limit, not a successful handoff. The checklist therefore routes an analysis question without transferring OS diagnosis, authorizing a fix, or claiming a recipient accepted the packet.

## R20 correction and finite negative control

The observed R20 text is scoped to OUT-009 / ADJ-06 (`PROVINCE.md:148-152`; `.ufo/waves/round-20/ownership-correction.txt:1`), not ADJ-01. Keep its exact boundary phrases: “It is not a tsukuroi grant of ownership”; “Kaidoku/Revenger arbitration remains unresolved; ask the protocol integrator before an internals handoff”; and “No configuration, service, package, boot or sibling-file write is authorized.” Preserve the explanation that it “explicitly supersedes only” the OUT-009 proposition wording and that “The other nine locators and all prepared/acknowledged handoff states are unchanged.” Read with that narrow scope, it neither replaces nor weakens ADJ-01's broader no-endpoint-request prohibition or its acceptance lifecycle.

The finite ownership-transfer negative control is explicit in the preregistration (`.ufo/waves/round-20/preregister.json:31-35`): missing correction → `OWNERSHIP-CORRECTION-MISSING`; altered correction → `OWNERSHIP-CORRECTION-INVALID`; positive correction → one ownership correction. The assigned-worktree checker encodes the direct mutation from “It is not a tsukuroi grant of ownership.” to “It grants tsukuroi ownership.” and expects `OWNERSHIP-CORRECTION-INVALID` with count 0; it also rejects removal of the arbitration lines (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:1096-1113`). This is source-level fixture evidence, not a run; it guards the R20 correction against an explicit ownership transfer, not every possible semantic rewrite of ADJ-01.

## Residual risk and verification gaps

Reviewed current `PROVINCE.md`, correction text, preregistration and assigned-worktree checker source only. No Git/baseline diff or gate/selftest was run, so publication and measured behavior are unverified. No LSP device was available in the supplied tool set; references, definition and diagnostics were not obtained. No outbound source-hash check was performed. Grep was used only to locate candidate text; semantic findings above rely on direct reads.

Scope: executed=none