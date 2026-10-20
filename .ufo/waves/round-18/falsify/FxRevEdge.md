# FxRevEdge

Axes: input classification, judge parity, evidence coverage.

## Finding

- **Medium — FAILS (independent judge misclassifies unavailable Git).** `tools/check-revision-binding.py:131-135` maps every nonzero `rev-parse` in `rev_parse()` to `ID_INVALID`; `bind()` calls it at `:154`. `git()` at `:108-117` returns a nonzero process result for a bad `-C` repository path rather than raising, so the judge reports `E-REVISION-INVALID` where the shared contract requires `E-GIT-FAILED`. In contrast, `tools/_revision.py:105-108` checks `--git-dir` and raises `E-GIT-FAILED` when the repository is unavailable; its selftest includes `not-a-repo` at `:235`. The judge's retained selftest does not cover this case (`:767-778`; retained `.ufo/waves/round-18/build/RerunHarness-selftest.txt:1` says 40/40).

## Remaining review

- **SURVIVES (shared source):** `tools/_revision.py:41,137-141` enforces 7–64 hex and commit-only resolution. `_commit()` maps failed resolution to invalid in a readable repository, and unavailable repository to `E-GIT-FAILED` (`:97-108`); `_ancestor()` maps fatal statuses to `E-GIT-FAILED` (`:118-122`). Origin-blob handling reaches that fatal path (`:148-154`). Author-side receipt `.ufo/waves/round-18/build/MutateShared.md:9-12` reports restored/pristine 37/37, and `_revision.py:204-205,228-235` includes unknown, blob, origin-blob, and unavailable-repo cases.
- **UNPROVEN:** no explicit ambiguous-noncommit fixture, nor exact 7- or 64-character boundary selftest (`_revision.py:196,202-205`). No runtime checks were run. LSP is unavailable (`read xd://lsp`: “No such tool”); grep was used for literal caller location only, not semantic proof.

Scope: executed=none