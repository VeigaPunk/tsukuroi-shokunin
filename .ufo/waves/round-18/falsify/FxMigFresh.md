# FxMigFresh — `tools/check-freshness-r17.py`

**Verdict: SURVIVES; no actionable regression found in the assigned migration.**

## Findings by severity

- **None.** The retained diff removes local `REV`/`BRANCH` and binding helpers (`.ufo/waves/round-18/build/patches/MigFresh.patch:30-99`). Landed source imports `_revision` after setting `sys.dont_write_bytecode` (`tools/check-freshness-r17.py:51-52`) and binds both `--revision` and `--registry-from` (`:768-774`). Shared order is branch validation, revision syntax/resolution, branch existence, then ancestry (`tools/_revision.py:11-24,134-154`). The handler maps a `RevisionError` to one finding (`check-freshness-r17.py:787-791`); subprocess fixtures assert exit 2 and exactly one expected ID, including branch-first and revision-before-missing precedence and both registry-from errors (`:506-523,542-568`).
- **Worktree/domain path preserved:** `ROOT` remains the script's repository root (`:55`); existing `git_in` still uses `git -C root` (`:325-343`), and the shared binder receives that same root (`:768`). The retained patch only changes binding, binding fixtures, and main's binding/error mapping; domain evaluation fixtures remain intact.
- **Fixture import guard:** subprocess sandbox copies both checker and `_revision.py` (`:461-469`); bytecode suppression precedes the shared import (`:51-52`).

## Residual risk and verification gaps

Committed `build/MigFresh.md:6-8` reports checker selftests 53/53→57/57, shared selftest 37/37, and judge exit 1 due to eight sibling migrations; these are reported results, not reruns. LSP was unavailable (`xd://lsp` is not mounted), so conclusions use direct source and retained patch, not grep as semantic proof. The existing `--registry-from` refusal can still emit the primary target under JSON `revision` rather than identifying the failing selector (`check-freshness-r17.py:308-318,772-791`; also noted in `build/CritNoHarm.md:15`); this behavior is unchanged from the pre-migration flow and does not alter the single finding or precedence.

Scope: executed=none