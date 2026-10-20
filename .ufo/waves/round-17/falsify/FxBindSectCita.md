# FxBindSectCita — C3 attack: tools/check-section-citations.py revision binding

Verdict: **SURVIVES** (this slice). Every revision form binds exactly as claimed; no pre-round finding id or check was removed.

Evidence [obs], all in mktemp clone /tmp/tmp.pZTf38sPxX/lane (origin = lane; tip dd15c183f2f2…):
- `--revision HEAD` / `@-` / `master` → rc=2 CANNOT_EVALUATE, finding E-REVISION-INVALID "7-64 hex commit required" (branch_tip null).
- 6-hex prefix `6923fe` → rc=2 E-REVISION-INVALID, though `git rev-parse 6923fe^{commit}` resolves — gate's 7–64-hex REV regex refuses shorts by design (tools/check-section-citations.py:433,509).
- Landed non-tip ancestor 6923fe0bd3add… → rc=0 PASS, correction_count=2.
- Tip dd15c183f2f2… → rc=0 PASS, correction_count=2.
- Detached unlanded commit 1ce1cf5b7ff7… (git commit-tree) → rc=2 E-REVISION-NOT-LANDED "not an ancestor of refs/heads/master".
- Unpushed commit fc695248216e… on local master → rc=2 E-REVISION-NOT-PUSHED "not an ancestor of refs/remotes/origin/master".
- Origin pinned behind tip (update-ref origin/master=6923fe0…): `--revision dd15c183…` → rc=2 E-REVISION-NOT-PUSHED; `--revision 6923fe0…` still rc=0 PASS. branch_tip echoed local master (clone artifact, not a gate defect).

Pre-round preservation [obs]: `git diff 6923fe0… dd15c183… -- tools/check-section-citations.py` = +208/−29; id-set comm: ADDED E-BRANCH-INVALID, E-REVISION-NOT-LANDED, E-REVISION-NOT-PUSHED; REMOVED none.

Could not verify [unk]: behavior against the lane's uncommitted worktree edits (tool reads committed objects only); `--selftest` sandbox not run (outside authorized scope).

Scope: executed=git clone,git rev-parse,python3 tools/check-section-citations.py (9 runs),git commit-tree,git checkout,git commit,git update-ref,git show,git diff,comm id-set diff
