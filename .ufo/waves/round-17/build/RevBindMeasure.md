# RevBindMeasure — C3 counting command

Files changed: `tools/check-revision-binding.py` (new, executable). Nothing else written.

Behavior [obs: selftest]: `--tools-revision` is itself bound (`:101`): 7–64 hex only; HEAD/@/refs → `E-REVISION-INVALID`, unlanded → `E-REVISION-NOT-LANDED`, unpushed → `E-REVISION-NOT-PUSHED`. The count clones the lane into `mktemp` (`:251`), sets `refs/heads/<branch>` to the measured commit, pins `refs/remotes/origin/<branch>` likewise (sandbox control), materializes the five tools via `git show` (`:149`), adds one empty unlanded commit on detached HEAD (`:164`), runs each tool at HEAD/unlanded/tip (`:229`). Bound = 2+`E-REVISION-INVALID`, 2+`E-REVISION-NOT-LANDED`, ≠2 with JSON `revision` == tip. Output `{status, tools_revision, revision, branch, branch_tip, bound_tools, total:5, per_tool[]}`; 0 iff 5/5, 1 else, 2 cannot-evaluate (`:478`).

Selftest `:388`: `CHECK_REVISION_BINDING_SELFTEST: PASS (23 cases, 23 passed, 0 failed)` — hermetic stubs: all-bound, 3/5, wrong-id, absent tool, binding cases.

Not verified [unk]: live 5/5 count (exec scope: selftest only). At baseline `6923fe0` `check-root-dac-correction.py` emitted text, so case (c) requires its landed edit's JSON `revision` [obs baseline; worktree edit unmeasured].

Risk: the measured commit must already be pushed to `origin/master`, else this gate exits 2 per contract. Blockers: none. Installs: none.

Scope: executed=python3 tools/check-revision-binding.py --selftest, read-only git reads (log/rev-parse/merge-base/branch/status), shell reads (ls, sed, awk, grep, du, cat)
