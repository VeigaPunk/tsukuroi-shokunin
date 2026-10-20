# SafetyPath — gate path/revision audit (pre-deliverable)

Limit: `tools/check-section-citations.py` and `section-citation-errata-r16.*` are absent at audit time; findings are against the plan and reused patterns (`check-locator-clarification.py:19-30,431-468`). Nothing executed.

1. **HIGH (planned):** each errata record carries `path`/`old_locator`. If the gate does I/O with them, `ROOT / rec["path"]` with absolute input (for example `~/.omp/agent/agent.db`) discards ROOT, and `../` climbs out of the repo. Finding details (`str(exc)[:120]`, quote diffs) then echo host bytes. Fix: hard-code `{R16-BOARD-SECTION: corpus/knowledge/host-health-report-r3.md, R16-RANK-SECTION: corpus/knowledge/update-safety-v3.md}`. Compare `rec.path` by string equality and FAIL on mismatch. Never open a record-supplied path.
2. **MEDIUM:** the worktree `read_tree` (`is_file`/`read_bytes`) follows symlinks. The repo has no symlinks today (`find -type l` came back empty). Make `--revision` the only mode, or reject anything that is not a regular file via `lstat`.
3. **OK to reuse:** the `REV` regex rules out option injection, `rev-parse ^{commit}` checks the revision, `GIT_*` variables are stripped, argv has no shell, and the git call has a 30s timeout. Do not copy R13's git call, which has no timeout (`check-root-dac-correction.py:229`).

Installs: none.
