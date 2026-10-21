# BindUnpushed — R20 attempt1 scoped source review

## Findings, by severity

### P1 — The object-selector judge cannot reach its new unpushed-object probe

**Evidence.** `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:393-401` defines `accepted(sandbox, name, rev, expect_sha)` with four positional parameters. The new `exact_accept()` calls it with five positional arguments, adding `branch`, at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:479-482`. The first positive selector case invokes that path at `:592-596`, before the unpushed-object case at `:621-630`. The helper has no alternative definition or reassignment in the inspected source.

**Impact.** [INFERENCE] Any object-selector evaluation reaching that first positive case raises `TypeError` before the remote is moved to its lagging parent and before `unpushed_object` is recorded. The top-level exception handler converts that exception to `E-INTERNAL`/exit 2 (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:1114-1118`), and the cannot-evaluate payload reports `object_selector_tools=0` with an empty per-tool selector list (`:733-743`). Thus the new mode cannot currently supply its promised unpushed-object evidence or the C2 0→9 result. This is a judge-source call-contract defect, not an observed candidate execution or an identified ancestry bypass.

**Required correction.** Make the `accepted()` definition and its callers agree, including forwarding the selected branch to `run_tool()`, before using the object-selector measurement. The existing four-argument callers must remain valid. The precise unpushed refusal already specified by `.ufo/waves/round-20/preregister.json:45` remains `E-REVISION-NOT-PUSHED`, exit 2; an internal exception is not that result.

## Scoped invariant review

Axes: C2 operability, object identity, landed/pushed ancestry, refusal classification, and evidence reachability. Baseline/worktree identity is recorded in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:2-7`; the C2 claim and its original-nine scope are in `preregister.json:13-20`.

### Object-first resolution does not itself skip the canonical pushed gate

- `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:119-137` enumerates object IDs before inspecting object type. A hex-looking ref with no matching object yields no bound commit; the direct-commit path returns the enumerated object ID rather than the selector's ref target. A unique tag-object selector peels to a commit at `:139-146`.
- Every successful resolver path returns into the same `bind()` function. The result is assigned to `sha` at `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:177`; missing/invalid objects fail at `:178-179`, local-branch ancestry is required at `:180-185`, and existing `refs/remotes/origin/<branch>` ancestry is required at `:186-190`. The tested operand is the resolved `sha`, not the user's original prefix or ref-like spelling. Only afterward is `origin_tip` resolved and the `Binding` returned (`:191-192`).
- `_ancestor()` accepts only Git statuses 0/1 as ancestry answers; other statuses raise `E-GIT-FAILED` (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:156-160`). `_exists()` also rejects statuses outside 0/1 (`:149-153`). The object-first change supplies no separate success return from `bind()` ahead of those gates.
- The retained production reference has the same local/origin ancestry sequence at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/_revision.py:142-154`; its selector previously used `_commit()` at `:139`. The candidate changes selector resolution, not that sequence. Under stable, valid refs, I found no source-level new route that marks the selected unpushed commit as pushed.
- The judge's independent own-input binder likewise sends its object-resolved SHA through local then remote ancestry checks at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:192-208`.

### Existing unpushed setup and expected refusal are correctly aimed, but finite

- The shared binder selftest creates distinct base and tip commits (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:222-225`), points `refs/remotes/origin/master` at base, expects tip to raise `E-REVISION-NOT-PUSHED`, accepts base, then moves origin to tip and checks the returned `origin_tip` (`:257-263`). These are source assertions, not executed results.
- The judge pins local and tracking refs to the measured tip in its temporary repository (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:233-242`). It derives the tip's first parent at `:646-648`. The new unpushed case moves only the tracking ref to that parent, requires exact refusal of tip, and restores the tracking ref in `finally` (`:621-630`). If no parent exists, the case explicitly fails instead of silently passing (`:622-624`). `exact_refusal()` requires exit 2, the expected binding ID, and exactly one finding (`:473-477`, `:383-390`). This is the correct shape for distinguishing landed-but-unpushed from invalid/unlanded, subject to the P1 reachability defect above.

### Affected callers retain the shared refusal path

The original nine consumer paths bind before revision content evaluation and preserve a binding error as a cannot-evaluate finding; none of these inspected call paths independently upgrades object resolution to pushed status:

| Consumer in `/tmp/tsukuroi-r20-binder-20261021/tools/` | Binding/error evidence |
| --- | --- |
| `check-locator-clarification.py` | `:782-795` |
| `check-root-dac-correction.py` | `:274-282` |
| `check-section-citations.py` | `:913-927` |
| `check-source-scope-correction.py` | `:636-649` |
| `measure-update-recheck.py` | `:475-481` |
| `check-boot-chain.py` | `:1572-1584` |
| `check-freshness-r17.py` | `:773-796` |
| `check-recheck-commands.py` | `:743-763` |
| `check-seat-scope.py` | `:260-272`, `:661-665` |

The actual execscope candidate also initializes `origin_tip=None`, obtains it only from the successful shared binding, and preserves `RevisionError` as a cannot-evaluate finding (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:831-851`). The candidate registry and adjacency entrypoints likewise bind before their new modes and propagate binding failure (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:339-373`; `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:819-844`). Other inspected shared consumers retain that pattern: `/tmp/tsukuroi-r20-binder-20261021/tools/check-appended-notices.py:475-502` and `check-boot-writers.py:569-595`.

## Residual risk and verification gaps

1. **No combined lagging-origin/ref-shadow coverage.** The shadow branch/tag cases are exercised while origin is pinned to tip, and their shadows are removed before the origin-lag case (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:592-630`). The explicit unpushed case uses only the full commit ID, not a short/uppercase selector or a peeled tag-object selector while a same-spelling ref points at a pushed decoy. The shared control-flow review above supports those combinations; the finite probe corpus does not independently demonstrate them. This is a coverage limit, not a demonstrated false-pushed result.
2. **Tracking-ref ancestry is not live remote proof.** The contract is conditional on the presence of a local `refs/remotes/origin/<branch>` (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:186-192`). With no tracking ref, `origin_tip` remains `None`; accepted landed status must not be reported as proof of a push to an actual remote. No fetch, remote endpoint, or host was inspected. Concurrent ref movement is not made atomic by this change: ancestry checks and the returned tip are separate reads of ref names (`:181-191`), as in the retained production reference (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/_revision.py:143-153`). No new concurrency guarantee is established here.
3. **Static review only.** The mounted-device lookup returned `No such tool: xd://lsp`; therefore LSP status/references/definition/diagnostics were unavailable. Caller/definition inspection used literal grep and source reads, not semantic-index proof. No Git command or Git-derived diff extraction was permitted; comparison used the observed candidate files and the retained production source. Runtime outcomes above are expressly marked as inference. The retained R20 measurement source schedules C2 before/after runs (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/measure/run.py:70-78`); source scheduling is not successful execution evidence.
4. No commands, imports, tests, builds, linters, formatters, subprocesses, target execution, external requests, or package/tool installations were performed. No code, refs, index, routes, configuration, or sibling artifacts were changed. Only this report was written. This report is a scoped recommendation, not claim admission or host/boot clearance. Boot images remain UNKNOWN.

Scope: executed=none.
