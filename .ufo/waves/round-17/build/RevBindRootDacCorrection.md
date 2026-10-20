# RevBindRootDacCorrection — tools/check-root-dac-correction.py

[obs] Sole writes: this report + the owned tool. Diff: 177 insertions(+), 35 deletions(-).

## Behaviour (R1/R2 closed)
- `VALID_REV=^[0-9a-fA-F]{7,64}$`; HEAD/`@`/refs/<7-hex → `E-REVISION-INVALID`, exit 2; help drops HEAD.
- `--branch` (default master): resolve `<hex>^{commit}`; `merge-base --is-ancestor` vs `refs/heads/<branch>` → `E-REVISION-NOT-LANDED`; when `refs/remotes/origin/<branch>` exists, vs it → `E-REVISION-NOT-PUSHED`; exit 2 before blob reads.
- stdout: one JSON object (`status`, `revision`, `branch`, `branch_tip`, `correction_count`, `scope`, `findings[]`); worktree mode keeps file reads, `revision:"worktree"`, non-fatal tip.
- `git()`: 30 s timeout, `E-GIT-TIMEOUT`/`E-GIT-FAILED` (`JjAuditTsukuroi.md:229`).
- 13 doc fixtures, finding ids and baseline pins byte-unchanged; none used HEAD.

## Selftest (mktemp clone)
before `PASS (13 cases, 13 passed)` rc=0 → after `PASS (23 cases, 23 passed)` rc=0. New sandbox cases: HEAD/`@`/`master`/6-hex rejected; detached unlanded → NOT-LANDED+NOT-PUSHED; landed tip accepted (tip asserted); origin lagging → NOT-PUSHED; absent branch; origin removed; payload keys. Clone worktree run: `{"branch_tip":"6923fe0bd3add04fc90f3bc3522895b27cf44bbe","revision":"worktree","status":"PASS"}` rc=0.

## Not verified
[inf] `--revision` unexecuted (authorization: `--selftest` only); `main()` mirrors the tested `revision_outcome`. [obs] `SKILL.md:1737` still says "in memory", omits `--branch`; the round-13 text pin is historical. Outside my scope.

Scope: executed=git diff --stat/--numstat (owned file), wc -w (report), mktemp -d + git clone (lane), python3 tools/check-root-dac-correction.py --selftest in clone, cp owned tool into clone, python3 tools/check-root-dac-correction.py --selftest (patched), python3 tools/check-root-dac-correction.py (clone worktree), rm -rf clone
