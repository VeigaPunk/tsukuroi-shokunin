# FxSimplify — final migration cleanup (read-only; no EXEC-AUTHORIZED)

**No duplicated local binding funcs/regex in the nine consumers — SURVIVES.**
- All nine import shared code before any bind: `check-boot-chain.py:53-54`, `check-freshness-r17.py:51-52`, `check-locator-clarification.py:18-19`, `check-recheck-commands.py:53-54`, `check-root-dac-correction.py:27-29`, `check-seat-scope.py:33-34`, `check-section-citations.py:35-36`, `check-source-scope-correction.py:14-15`, `measure-update-recheck.py:33-34`.
- Revision/branch grammar exists only in `tools/_revision.py:41-42`; `bind()` only `:134-154`, plus the judge's deliberate independent copy (`check-revision-binding.py:147-163`, rationale `:9-10`). No consumer defines `resolve`, `ref_sha`, `is_ancestor`, `rev_parse`, `bind_revision`, `BindCannot`, or a `{7,64}` regex (grep count 0 in the nine). Residual `rev-parse` is fixture plumbing (`check-source-scope-correction.py:379-383`, `check-boot-chain.py:1286`), not `--revision` binding.
- Adapters are direct calls plus one `RevisionError→Cannot` map, e.g. `check-recheck-commands.py:724-728`, `check-root-dac-correction.py:275-279`; no wrapper layer.

**No orphan imports — SURVIVES.** Every shared name is used: `check-appended-notices.py:22` imports `E_GIT, RevisionError, bind, clean_env` (uses `:119,121,478,572`). Binding-era imports (`shutil`, `tempfile`, `subprocess`) retain live uses.

**No bytecode creation — SURVIVES (static).** `sys.dont_write_bytecode = True` precedes the shared import in all nine, plus tenth `check-appended-notices.py:17` vs `:22`; no `__pycache__`/`*.pyc` under `tools/` (glob, gitignore:false).

**`_revision.IDS` preserved and consumed — SURVIVES.** Defined `tools/_revision.py:49`; used `tools/check-root-dac-correction.py:405` inside `binding_cases()` (called at `:516`, `--selftest` `:543`). Use is selftest-only, not the production bind path; deleting it breaks root-dac `--selftest`.

**Deletion candidates (not applied).**
- `tools/_revision.py:40` `EXIT = 2`: zero references lane-wide (grep count 1, its definition). Safe weight cut.
- `tools/check-revision-binding.py:91` `SHARED_IMPORT`: unused after the AST census (`:233-260`); keep or regenerate mutant evidence first — `FxMutJudge.HTur9a/deadimport.diff:10` depends on it.

Preserved contract: exit 0/1/2, branch-first precedence, one finding, independent judge. Per-tool `git()` readers stay because they own reader-specific `E-GIT-*` ids; sharing them would couple read-path semantics, not binding.

Unknowns: runtime selftest PASS not executed (read-only seat); no `lsp` device mounted, so reference evidence is textual grep, not semantic-server proof.

Scope: executed=bash (ls/grep/wc read-only text inspection; no git/python/sudo; no production edit)
