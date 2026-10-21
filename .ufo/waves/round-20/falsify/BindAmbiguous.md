# BindAmbiguous — round 20 attempt 1

## Scope and axes

Source-only review of ambiguous object-prefix construction, refusal ordering, and the corresponding independent selector probes. Axes: object-only refusal, public-path coverage, first-failure preservation, and honest measurability. The lane's `.ufo/waves/round-20/worktree-bindings.json:2-7` declares baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472` and the four authorized candidate worktrees. No source, refs, runtime, routing, or host state was changed.

## Findings, by severity

### P1 — Undefined `git` aborts the binder selftest before the ambiguity and malformed-origin cases

**Evidence:** `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:286-305` constructs an annotated ghost tag and calls `git(repo, ...)` at lines 291-292. This module imports no `git` symbol (`:30-39`); its subprocess wrapper is `_git` (`:69-77`), and the selftest's local checked wrapper is `run` (`:210-216`). The call is outside the `expect` helper, which in any event catches only `RevisionError` (`:198-208`). The standalone entrypoint calls `selftest()` directly (`:378-380`).

**Impact:** [INFERENCE] On the normal fixture path, evaluating this undefined name raises `NameError`, not a counted test refusal or completed selftest report. The new collision construction at `:332-353` and the retained malformed-origin/Git-failure controls at `:359-368` are downstream and cannot provide executed evidence from this source. This is a concrete source defect, not an observed test result.

**Required correction:** Use the existing correctly named Git wrapper at this callsite before treating the later ambiguity and origin controls as reachable evidence.

### P1 — The independent selector probe passes five arguments to a four-argument acceptance helper

**Evidence:** `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:393-401` defines `accepted(sandbox, name, rev, expect_sha)`. The new `exact_accept` calls `accepted(sandbox, name, revision, expected_sha, branch)` at `:479-482`. Its first normal use is `real_prefix_shadow_branch` at `:590-596`. Selector probing is enabled from `measure` at `:663-669`.

**Impact:** [INFERENCE] After successful fixture setup, the first positive shadow selector raises `TypeError` before any acceptance judgment. The CLI catches that exception as `E-INTERNAL` (`:1114-1118`); the cannot-evaluate payload sets `object_selector_tools` to zero (`:733-743`). Consequently this candidate cannot supply the preregistered 0→9 measurement through its advertised object-selector command. The command and nine-consumer scope are recorded in the lane's `.ufo/waves/round-20/preregister.json:13-19`.

**Required correction:** Make acceptance forwarding and the helper's signature agree while preserving the intended branch argument; otherwise the positive selector and subsequent ordering probes are not measurable through this evaluator.

### P2 — The constructed collision does not exercise a valid public selector or a same-name hex ref

**Evidence:** `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:332-351` chooses a **four-hex** prefix of an arbitrary existing object and stores a synthetic colliding blob. The sole assertion calls `_object_commit(repo, ambiguous_prefix)` directly and expects `None` (`:352-353`). Public `bind` accepts only 7–64 hex (`:41`, `:174-179`), so this four-character selector cannot traverse public object resolution. This collision block creates no branch or tag whose name equals that ambiguous prefix. The earlier `shadow` fixture instead requires a unique prefix of at least seven hex (`:309-314`). The independent judge's complete `object_selector_probes` body (`tools/check-revision-binding.py:471-632`) likewise contains ghost and unique-shadow cases, but no constructed ambiguous-prefix/ref case.

**Impact:** The helper test can establish rejection of multiple object matches, but it does not establish the requested end-to-end property: a syntactically valid ambiguous selector must not fall through to a same-name branch/tag pointing at a landed commit, and must retain its place in the first-failure chain. It also does not guarantee that the preexisting colliding object is a commit/tag rather than another noncommit. No present implementation fallback was found; this is a concrete coverage gap, not a demonstrated acceptance bypass.

**Required coverage:** A genuine collision at a publicly accepted width, including a commit or commit-peeling tag, with the same hex name installed as a ref to a known landed decoy; assert exactly `E-REVISION-INVALID` through `bind`/consumer output. Couple it with invalid-branch, missing-branch, and bad-origin conditions to distinguish the first failure. A four-character public call would only test the syntax gate and is not an adequate substitute.

## Bounded behavior and residual risk

- **No collision-to-ref fallback is present in the inspected binder control flow.** `_revision.py:119-124` enumerates matching object IDs and rejects any count other than one before inspecting object types or peeling. `bind` immediately raises `E-REVISION-INVALID` for that result (`:177-179`), before local or origin lookup. The independent selector uses the same ordering in its separately defined implementation (`tools/check-revision-binding.py:139-159`, `:192-207`). These are source-level observations, not runtime validation.
- **Branch/local/origin first-failure order is structurally retained.** Candidate `_revision.py:172-192` performs branch validation, revision syntax/object selection, local-branch resolution, local ancestry, then optional origin ancestry. The inherited sibling comparator `/tmp/tsukuroi-r20-registry-20261021/tools/_revision.py:134-154` has the same sequence, with `_commit(repo, revision)` replaced by the object-only selection step. Invalid branch therefore precedes ambiguity; ambiguity precedes missing branch/origin checks; an unlanded commit precedes an origin refusal. `_ancestor` still converts status greater than one to `E-GIT-FAILED` (candidate `:156-160`; comparator `:118-122`). No independent first-failure regression was identified within this bounded comparison.
- Retained assertions cover branch-before-revision and revision-before-missing (`_revision.py:249-253`), local-unlanded refusal while origin lags (`:257-263`), and malformed-origin Git failure (`:359-365`). Their presence is not evidence they ran; the P1 selftest defect blocks the later controls.
- A canonical shared binder remains the consumer binding entrypoint in the inspected source; the judge deliberately keeps its own grading implementation. Literal caller discovery was used only to locate imports/adapters, not as semantic proof of all nine consumers. No alternate runtime was invoked and no same-identity rerouting was performed. Neither nine-tool coverage nor universal/saturated selector behavior is established by this review.

## Verification gaps and limits

- `read xd://lsp` returned `No such tool: xd://lsp` and listed only `ast_edit` and `debug` as mounted devices. Language-server status/references/definition/diagnostics were unavailable; read/grep were the explicitly limited fallback. No grep result is presented as language-server semantic proof.
- Source comparison used the declared binder worktree and the inherited registry-worktree copy. No Git command or executable diff was run, and the comparator's bytes were not independently authenticated against the baseline Git object.
- No collision was generated, no object/ref was written, no selftest/consumer/evaluator was run, and no measured PASS/FAIL or 0→9 result is claimed. Exception outcomes above are explicitly static inferences.
- No tool installation/update, external request, package/service/boot operation, or code edit occurred. Resume continuity and admission are outside this leaf assignment. Boot images remain UNKNOWN; this report grants no host or boot-safety clearance. Findings are review recommendations only.

Scope: executed=none.
