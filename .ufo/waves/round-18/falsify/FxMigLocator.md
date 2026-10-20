# FxMigLocator

## Findings by severity
None; no actionable defect found in scope.

- **SURVIVES — shared binding / no local binding copy.** The migration patch records removal of local `REV`, `BRANCH`, `bind_revision`, and `revision_finding` (`.ufo/waves/round-18/build/patches/MigLocator.patch:22-30,46-91`). Current source imports `_revision` at `tools/check-locator-clarification.py:18-19` and its sole `--revision` entrypath calls `_revision.bind` at `:782-790`. Remaining `git`/`read_git` at `:447-469` read revision content, not bind it. Parser `:472-481` has no `--registry-from` path.
- **SURVIVES — refusal shape and precedence.** `tools/_revision.py:83-95,134-154` validates branch before revision syntax, then checks branch presence and ancestry. Locator fixtures declare mixed-invalid and missing-branch expectations at `tools/check-locator-clarification.py:555-568,617-625`; `main` maps a shared `RevisionError` to one `Cannot` and emits one `Finding` at `:783-795`. Committed build evidence reports locator 37/37 and per-tool `bound=true, consistent=true, shared=true, local_rev_regex=0` at sandbox commit `80fc748b` (`.ufo/waves/round-18/build/MigLocator.md:3-7`); this is not final-target runtime evidence.
- **SURVIVES — worktree / fixtures / import guard.** The non-revision path remains `read_tree` at `tools/check-locator-clarification.py:791-792` (also preserved by patch `:230-233`). Fixture subprocesses at `:583-634` invoke Git only; the checker’s CLI assertion calls `main` in-process (`:635-647`), so no checker subprocess needs a copied module. `sys.dont_write_bytecode` precedes `import _revision` (`:17-19`).

## Residual risk and verification gaps
LSP is unavailable: `read xd://lsp` returned “No such tool.” Grep was only a locator; conclusions rely on directly read source and committed patch, not semantic-LSP proof. Per the read-only assignment, no execution was performed; final target `68a8ae0` runtime selftest/exit remains unverified. The build report gives a sandbox selftest count but no recorded exit code.

Scope: executed=none