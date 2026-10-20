# FxMigBoot — read-only review

**Axes: shared binding; error contract; worktree behavior; fixture/import safety.**

- **SURVIVES — shared binding, no local revision validator.** Landed `tools/check-boot-chain.py:1511` binds `--revision` via `_revision.bind`; `:1514-1515` does the same for optional `--registry-from`. The retained baseline-to-migration patch deletes local `REV`/`BRANCH` regexes (`.ufo/waves/round-18/build/patches/MigBoot.patch:91-95`) and `resolve`/`ref_sha`/`is_ancestor`/`bind_revision` (`:290-335`). Target `BLOCK_SHA` at `:134` validates capture digests, not revision arguments.
- **SURVIVES — one finding and precedence.** `_revision.py:134-154` validates branch, then revision syntax/identity, branch existence, local ancestry and optional origin ancestry. Checker `:1516-1522` maps the first `RevisionError` to one `Finding`; `binding_cases` asserts branch-before-revision and invalid-revision-before-missing-branch (`check-boot-chain.py:1333-1342`), while the CLI selftest asserts a one-ID result (migration patch `:413-430`). Baseline CLI also checked branch before revision (`MigBoot.patch:658-668`).
- **SURVIVES — detached-worktree and fixtures.** Baseline and target bind explicit `refs/heads/<branch>` / optional origin refs (patch `:313-327`; `_revision.py:142-154`). Target fixture detaches HEAD, creates an unlanded commit and expects `E-REVISION-NOT-LANDED` (`check-boot-chain.py:1355-1364`). Fixture calls `bind` in-process; its subprocess helper runs Git only (`:777-783`), so no Python fixture copy can omit `_revision.py`. `sys.dont_write_bytecode = True` immediately precedes `import _revision` (`:53-54`).

**Residual risk / verification gap:** no LSP device/server was exposed (`read xd://lsp` returned “No such tool”); semantic references/definition/diagnostics were unavailable. Static review only; no commands or tests executed here. No actionable defect found.

Scope: executed=none