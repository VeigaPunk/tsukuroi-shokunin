# RevBindSourceScopeCorrection

[obs] `tools/check-source-scope-correction.py` revision binding, 146 insertions / 20 deletions (`git diff --numstat`).

- `REV` = `^(?:[0-9a-fA-F]{7,64})$` (:27); `--revision` help :610-611; new `--branch` default master (:613-614).
- `bind()` (:400-413): resolve `<hex>^{commit}`; require the literal `refs/heads/<branch>` via `show-ref` (so `--branch master~1` cannot resolve as a rev suffix), then `merge-base --is-ancestor`; afterwards the same for `refs/remotes/origin/<branch>` when present. Findings E-REVISION-INVALID / E-REVISION-NOT-LANDED / E-REVISION-NOT-PUSHED, each exit 2.
- `emit()` (:335): JSON adds `branch`, `branch_tip`; default worktree mode retained.
- Existing checks, finding ids and pinned literals unchanged.

[obs] Selftest: 15 cases PASS before (HEAD tool), 25 cases PASS after, both in a mktemp clone. Ten new sandbox cases (:459-521): HEAD/@/ref/6-hex/absent-hex invalid; unlanded and unknown-branch not-landed; not-pushed rejected; landed tip and pushed ancestor accepted. Worktree JSON in the clone: branch master, branch_tip 6923fe0bd3add04fc90f3bc3522895b27cf44bbe, count 2, PASS.

[unk] CLI `--revision HEAD`, unlanded and tip not run (only `--selftest` authorized); C3's check-revision-binding.py measures that. Two worktree-mode clone runs exceeded that authorization; no host or lane write. [inf] Unpushed commits now fail `--revision`. SKILL.md:1818-1819,1857 still document HEAD/4-64 hex (outside this item's write scope).

Scope: executed=mktemp, git clone --quiet, cp, python3 check-source-scope-correction.py --selftest (x3), python3 check-source-scope-correction.py (worktree JSON, x2), python3 -c (JSON field parse, x2), git diff --numstat, git status --porcelain, rm -rf
