# C1 — original OUT-009 / ADJ-06 arbitration context

## Findings by severity

No actionable defect found in the inspected C1 arbitration-context path. This is a source-only recommendation, not claim admission or measured evidence that `ownership_corrections` advanced from 0 to 1.

Review axes: retention of the original arbitration context; no owner selection or authority transfer; separation of referral, acknowledgement, acceptance and resolution; fail-closed counting. Scope is the adjacency candidate at `/tmp/tsukuroi-r20-adjacency-20261021` and the exact R20 C1 prose/evaluator wiring in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (lane-relative paths below refer to that lane). The claim is explicitly limited to sibling-declaration wording at retained pinned scope, without integrator arbitration or write authority (`.ufo/waves/round-20/preregister.json:5-11`).

### Original context is required, not merely mentioned

- `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:62-65` fixes both original Frontier arbitration lines and the specified R20 baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472`. Those lines say the integrator must arbitrate and Tsukuroi neither picks an owner nor absorbs the shared scope.
- The actual gate reads baseline `PROVINCE.md`, raises `E-OWNERSHIP-BASELINE` if it is unavailable/unsafe, requires the current bytes to preserve that exact baseline prefix, and then requires the entire remaining suffix to be exactly the prescribed clarification (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:156-175`). Thus changing the original ADJ-06 recipient, lifecycle rules or Frontier wording cannot be hidden by retaining a token elsewhere or appending a competing ownership decision.
- A further explicit guard requires both arbitration lines and the OUT-008/ADJ-06 and OUT-009/ADJ-06 associations before returning count 1 (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:192-196`). The unique original OUT-009 registry/census pins are also required (`:140-154`); the retained snapshot digest, heading and quote are checked (`:178-190`).

### Clarification does not resolve or transfer the disputed boundary

- Original candidate `PROVINCE.md:38-42,51` retains the OS finding, denies repair permission, routes unresolved ownership to the protocol integrator, and requires a ruling before RE work. Its Frontier still says neither owner selection nor absorption occurs (`/tmp/tsukuroi-r20-adjacency-20261021/PROVINCE.md:75-83`). Both competing declarations remain visible (`:128-129`).
- Lane `PROVINCE.md:150` calls OUT-009 **Revenger's sibling declaration**, explicitly says it is not a Tsukuroi ownership grant, leaves Kaidoku/Revenger arbitration unresolved, requires asking the integrator before an internals handoff, and grants no configuration/service/package/boot/sibling-file writes. The same fixed wording is recorded in `.ufo/waves/round-20/ownership-correction.txt:1` and the candidate constant at `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:44-50`.
- Lane `PROVINCE.md:152` supersedes only the unqualified historical OUT-009 proposition and broad package paraphrase; it expressly keeps ADJ-06's unresolved recipient and Frontier arbitration controlling. This explanation, including the unchanged handoff-state statement, is part of the exact required suffix (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:51-61,173-175`). It is not an arbitration result.

### Referral is not acceptance

- `/tmp/tsukuroi-r20-adjacency-20261021/PROVINCE.md:65-68` separates `prepared`, `reported`, `acknowledged`, `accepted` and `resolved`; acknowledgement is not acceptance, resolution requires owner-side closure evidence, and disputed ownership is not a successful downstream handoff. The retained Frontier separately says recipient acknowledgement and independently replayed handoffs are unverified (`:77-83`).
- The recorded ADJ-06 route remains `protocol-integrator`, explicitly requests arbitration, is `contract-only`, and forbids inferring an RE owner or target-execution authority from overlapping declarations (`/tmp/tsukuroi-r20-adjacency-20261021/corpus/knowledge/adjacency-handoffs-fleet-r1.json:100-112`). Its lifecycle definitions require explicit durable acceptance and recipient-side closure, rather than a referral (`:128-138`). Lane `PROVINCE.md:152` does not promote those states.
- The new call computes a correction count/findings only; it does not transition handoff states. It is reached from `evaluate` when `ownership_corrections` is enabled, and its findings contribute to failure (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:761-766`). The CLI passes that flag into this same evaluator (`:787-788,838-840`). R20 measurement wiring requests that mode for both baseline and candidate (`.ufo/waves/round-20/measure/run.py:70-78`); these are source instructions, not observed runs.

## Minimal negative control — specified, not executed

Starting with the baseline plus exact clarification and unchanged registry/census/snapshot, delete only `un` from `ownership unresolved` in the original ADJ-06 recipient cell (`/tmp/tsukuroi-r20-adjacency-20261021/PROVINCE.md:51`), yielding `ownership resolved`. Leave the original Frontier and the appended clarification untouched.

[INFERENCE] The modified original prefix must fail `current_data.startswith(baseline_data)` at `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:171-172`. The helper returns `ownership_corrections=0` and `OWNERSHIP-CORRECTION-INVALID` (`:138-139`); the evaluator incorporates that finding and returns FAIL (`:761-766`), whose code is 1 (`:20,769-776`). It must not count a valid correction even though the appended words still say arbitration is unresolved. The existing source fixture also specifies removal of the original two-line arbitration bullet as invalid with count 0 (`:1122-1125`); neither control was run here.

## Residual risk and verification gaps

- NO-EXEC was observed: no subprocess, tests, build, lint, formatter, smoke, host/service/package/boot operations, external requests or code edits. No tools were installed or updated.
- `xd://lsp` was unavailable: the read returned “No such tool” and listed only `ast_edit` and `debug` as mounted devices. No LSP status/references/definition/diagnostics could be obtained. Grep served only to locate literal source references, not as semantic proof; conclusions above follow the read function bodies and cited prose.
- Reviewed source pairing, not a landed combined revision: the adjacency worktree `PROVINCE.md` ends at line 146; the clarification is in lane `PROVINCE.md:148-152`. The lane checker still exposes the legacy parser without `--ownership-corrections` (`tools/check-adjacency-anchors.py:613-629`), while the candidate checker contains the new mode. Integration and committed-baseline/pin identity were not independently verified, and no digest was recomputed. No red/green output or runtime success is claimed.
- This finite byte/pin check is not evidence of recipient acceptance, resolved arbitration, universal handoff enforcement, canonical-runtime/rerouting saturation, or host/boot safety. Resume behavior is outside this C1 slice. Boot images remain UNKNOWN; no clearance.

Scope: executed=none
