# FxMigRecheck — `tools/check-recheck-commands.py`

## Findings
None actionable in the requested binding migration. **SURVIVES (source review):** baseline `measure/c2-before-842a531.json:1` records this gate with `branch-first=E-REVISION-INVALID`, `branch-space=E-CLI`, `branch-missing=E-REVISION-NOT-LANDED`, `shared=false`, and one local regex. Landed source calls `_revision.bind(repo, args.revision, branch)` at `tools/check-recheck-commands.py:724`; the migration patch removes local `ref_sha`, `is_ancestor`, `bind`, and REV/BRANCH regexes (`build/patches/MigRecheck.patch:401-439`). `_revision.py:83-154` validates branch before revision, then branch existence, local ancestry, and optional origin ancestry. The caller converts the first `RevisionError` to one `Cannot`/finding (`:725-727,736-740`); fixtures assert one finding and exercise precedence/missing-branch cases (`:925-926,1231-1243`). Bytecode suppression precedes import (`:53-54`).

**Worktree behavior preserved:** this checker has no worktree mode; parser still requires `--revision` or `--selftest` (`:687-703`), and no-mode remains an `E-CLI` result labelled `worktree` (`:713-716,1327`). Fixtures call `run()` in-process (`:907-913`); there is no Python fixture subprocess/module-copy path to check. Git subprocesses are separate (`:604-615`).

## Residual risk / verification gaps
**UNPROVEN (final target runtime):** committed migration evidence reports 80/80 selftests, shared-module 37/37, and this tool bound/consistent/shared with zero regex at sandbox commit `010ad95` (`build/MigRecheck.md:5,18-19`), not integrated target `68a8ae0`. No final-target selftest or independent judge result was available. LSP is unavailable (`read xd://lsp` returned “No such tool”); source tracing used read/grep fallback, not semantic proof. No runtime checks run here.

Scope: executed=none