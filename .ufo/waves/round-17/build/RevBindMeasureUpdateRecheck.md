# RevBindMeasureUpdateRecheck — scoped report

[obs] Diff `tools/measure-update-recheck.py`: +320/−19, one file.
- R1 closed: `REV` `^(?:HEAD|[0-9a-fA-F]{4,64})$` → `^[0-9a-fA-F]{7,64}$`; help text says "7-64 hex commit bound to --branch"; `resolve()` lowercases and still resolves `<hex>^{commit}`. HEAD/@/refs/short/unknown → `E-REVISION-INVALID`, exit 2.
- R2 closed: new `bind()` requires `git merge-base --is-ancestor <sha> refs/heads/<branch>` (`--branch`, default master) else `E-REVISION-NOT-LANDED`; when `refs/remotes/origin/<branch>` exists it also requires ancestry else `E-REVISION-NOT-PUSHED`; both exit 2.
- Payload gains `branch`, `branch_tip`; every pre-existing check, finding id, exit code and the worktree default are unchanged.
- `--selftest` added: mktemp git sandbox, writes only there.

[obs] Selftest before: flag absent (0 cases; unknown flag → `E-CLI`, exit 2). After: `MEASURE_UPDATE_RECHECK_SELFTEST: PASS (13 cases, 13 passed, 0 failed)` from a fresh mktemp clone of the lane. Cases: HEAD rejected, 6-hex rejected, detached unlanded commit rejected, unknown branch rejected, not-pushed rejected (origin/master behind tip), master tip accepted (`ABSENT`, `branch_tip`=tip), worktree default (`revision=worktree`, `branch_tip`=tip), plus 6 record fixtures (clean; digest, pending-value, boot-sysroot, duplicate-observation, observed-mismatch mutants).

[inf] C3 case (c) depends on the measured commit descending from the checker clone's `refs/remotes/origin/master`.

[unk] `SKILL.md:1819` still documents `HEAD or 4–64 hex` and "no self-test obligation"; outside my ownership — L1 must update.

Scope: executed=grep,ls,git log,git status,wc,awk,python3(json inspection),git clone,cp,python3 measure-update-recheck.py --selftest,python3 -c ast.parse,git diff,sed,rm -rf
