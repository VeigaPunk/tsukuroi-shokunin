# FxMigUpdate — `tools/measure-update-recheck.py`

Axes: binding coverage, duplicated logic, refusal contract, worktree continuity, fixture/import safety.

## Findings

None actionable. **SURVIVES — shared binding / no local revision copy.** Baseline C2 evidence records this tool `shared=false`, `local_rev_regex=1`, `branch-first=E-REVISION-INVALID`, and `branch-missing=E-REVISION-NOT-LANDED` (`.ufo/waves/round-18/measure/c2-before-842a531.json`, per-tool row). The committed build patch deletes local `REV`/`BRANCH`, `resolve`, `ref_commit`, `branch_ok`, `bind`, and `branch_tip` (`build/patches/MigUpdate.patch:42-105`). Landed `load()` routes every explicit revision through `_revision.bind`; worktree reads remain `read_tree` and use shared informational `branch_tip` (`tools/measure-update-recheck.py:471-481`).

**SURVIVES — single refusal and precedence.** `_revision.bind` validates branch before revision syntax/resolution, then branch presence and ancestry (`tools/_revision.py:135-154`); the caller maps its first `RevisionError` to one `Cannot`, and CLI emits one `Finding` (`measure-update-recheck.py:476-479,768-775`). Fixtures assert finding count and branch-first behavior (`:548-568,595-600`); the shared module also tests revision-before-missing-branch (`_revision.py:211-215`).

**SURVIVES — worktree and fixture/import guard.** The fixture copies the imported `_revision.py` beside its subprocess script (`measure-update-recheck.py:529-539`). `sys.dont_write_bytecode = True` precedes `import _revision` (`:33-34`). The remaining `HEX64` regex validates snapshot digest, not revision syntax (`:50`).

## Residual risk / verification gaps

**UNPROVEN:** final-target runtime/independent ledger was not available during this review; the committed build note reports sandbox 20/20 PASS but gives no exit code (`build/MigUpdate.md:5`), and is not the integrated-target run. LSP is unavailable (`read xd://lsp` returned “No such tool”); no semantic references/definition/diagnostics were possible. Static findings use direct source and patch; text search was only a locator. No execution performed.

Scope: executed=none
