# FxMigSourceScope

Axes: shared binding/no local copy; refusal semantics and precedence; worktree parity; fixture/import isolation.

## Findings

None actionable in the reviewed source diff.

## Review

- **SURVIVES — shared binding and no local binder.** The committed patch index changes this file from blob `3a074d6` to `5522543`; its diff removes the local `REV` 7–64 regex and `resolve`/`ancestor`/`ref_exists`/`bind` helpers (`.ufo/waves/round-18/build/patches/MigSourceScope.patch:17,25-63`). Current revision entrypath calls `_revision.bind(ROOT, args.revision, branch)` at `tools/check-source-scope-correction.py:636-643`; no `--registry-from` option exists in this tool (`:617-623`). `_revision.bind` checks branch syntax before revision syntax and revision syntax before branch existence, raising one typed error (`tools/_revision.py:83-154`). The caller converts that error to `Cannot`; its handler emits one finding (`check-source-scope-correction.py:639-649`).
- **SURVIVES — worktree and fixtures.** Worktree mode still reads the same `FILES` via `read_tree`; only informational tip lookup now uses `_revision.branch_tip` (`:644-646`; patch `:160-181`). Binding subprocess fixtures copy both the checker and `_revision.py` before invocation (`:462-490`); cases cover invalid-branch-first, invalid-revision-before-missing-branch, missing branches, unlanded, and not-pushed single-ID refusals (`:494-520`). `sys.dont_write_bytecode = True` precedes `import _revision` (`:14-15`).
## Residual risk

**UNPROVEN:** no post-integration measurement or target selftest is available. The migration report says neither was run (`.ufo/waves/round-18/build/MigSourceScope.md:6`); the recorded harness is baseline-only (`.ufo/waves/round-18/build/RerunHarness.md:4-11`). The committed baseline vector is `consistent_tools=1`, `shared_tools=0`, `local_rev_regex_copies=9` (`.ufo/waves/round-18/measure/c2-before-842a531.json:1`). Source review supports this tool's migration but does not establish target 9/9.

## Verification gaps

LSP unavailable (`xd://lsp`: no such tool; mounted-tool list contained no LSP), so no semantic references/definition/diagnostics. Read-only source/patch review only; no execution.
This checker diff adds no runtime-selection/rerouting behavior or saturation claim; those axes are not asserted by this scoped change.

Scope: executed=none