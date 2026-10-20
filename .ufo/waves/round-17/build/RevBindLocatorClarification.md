# RevBindLocatorClarification

Rows: `.ufo/waves/hyaku/jj-w1/reports/JjAuditTsukuroi.md:30,443,452,465,475` (R1/R2); only the tool changed [obs].

## Diff (683 → 799 lines)

- `REV = ^[0-9a-fA-F]{7,64}$` (HEAD dropped) :35; `BRANCH` :36; help :505-506; `--branch` default master :508.
- `resolve()` → `bind_revision()` :479-500: grammar → `rev-parse <rev>^{commit}` → `merge-base --is-ancestor <sha> refs/heads/<branch>` (E-REVISION-NOT-LANDED) → same against `refs/remotes/origin/<branch>` when present (E-REVISION-NOT-PUSHED); exit 2 via `BindCannot` :66-71. `git()` gained `repo=` :454; worktree mode still reads no git.
- `payload`/`emit` gain `branch`, `branch_tip` :437-446; refusals keep the resolved sha and observed tip.
- `binding_cases()` :596-648: mktemp repo removed in `finally`; c0/c1, unmerged `side`, `origin/master`→c0.

## Selftest

Before (clone of `6923fe0`): PASS 23/23. After: PASS 28/28 — +head-rejected, +unlanded-rejected, +not-pushed-rejected, +landed-tip-accepted, +payload-shape. No old case used HEAD; 21 fixtures, 2 CLI cases, digest pins unchanged.

## Limits

- `--revision`/worktree CLI not executed (grant: `--selftest`); emit covered above.
- SKILL.md:1818 still documents `HEAD`/4–64 hex, 23 cases — not mine to edit.
- Missing branch → NOT-LANDED, `branch_tip: null`; [inf] sibling gates keep the HEAD hole until their seats land.

Scope: executed=git clone -q (mktemp lane clone), git rev-parse HEAD in clone, python3 tools/check-locator-clarification.py --selftest (x3), cp tool into clone, rm -rf mktemp clones, grep -nE over the tool
