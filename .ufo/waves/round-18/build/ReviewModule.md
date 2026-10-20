# Shared revision module review

## Verdict: SURVIVES — requested static contract

- [obs] Error order is branch validation, revision syntax, commit resolution, local branch resolution, local ancestry, then optional origin ancestry; successful return carries `Binding(sha, branch, tip, origin)` (`tools/_revision.py:130-150`). Error IDs and `RevisionError(fid, site, detail)` are defined in `:43-59`. `_commit`, `_exists`, and `_ancestor` distinguish expected absence/non-ancestry from Git failures (`:97-118`). Each refusal raises one `RevisionError` with one `fid`.
- [obs] Branches must match the restricted ASCII pattern, cannot be exact `HEAD`, and must pass Git’s full `refs/heads/<branch>` check (`tools/_revision.py:41-42,83-94`). The selftest source covers `a..b`, trailing slash, whitespace, leading dash, `@`, `HEAD`, empty, `.lock`, `.hidden`, branch-before-revision precedence, and revision-before-missing-branch precedence (`:203-213`); these cases were not executed.
- [obs] The judge has its own binder (`tools/check-revision-binding.py:136-149`), and top-level imports shown at `:46-48` are standard-library only. No executable `_revision` import was found; its import scan is source-text counting (`:82,218-220`).

## Residual risk and verification gaps

- [inf] Ref reads and ancestry checks are separate Git calls (`tools/_revision.py:139-149`); concurrent ref mutation can make returned tip fields differ from the exact refs checked. No atomic-snapshot guarantee was established.
- [unk] LSP device unavailable (`xd://lsp` returned “No such tool”); text search was used only for source discovery. No target code or selftest was executed, per assignment.

Scope: executed=read-only git status/log/diff and shell grep discovery; target code/tests not executed