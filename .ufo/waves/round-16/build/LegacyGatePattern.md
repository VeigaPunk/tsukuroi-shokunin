# LegacyGatePattern — reusable gate conventions

Static read of `tools/check-locator-clarification.py`; target absent; no execution.

## Reuse
- CLI `build_parser`: `exit_on_error=False`; exclusive `--revision REV`/`--selftest`; `REV=^(?:HEAD|[0-9a-fA-F]{4,64})$`; default worktree; `--help`→0. Invalid args emit one CANNOT JSON finding `E-CLI`, site `cli`, exit 2.
- `resolve`→`rev-parse --verify --quiet REV^{commit}`. `read_git`→`git show <resolved>:<path>`, scrubbing `GIT_*`, `GIT_OPTIONAL_LOCKS=0`, 30s timeout. `revision` = `worktree` or resolved commit.
- `emit`: one sorted-key JSON line — `status` (PASS|FAIL|CANNOT_EVALUATE), `revision`, `correction_count`, `findings[]{id,site,detail}`; dedupe/sort by id/site/detail; `site` repo-relative; `detail` ≤120 chars.
- Taxonomy: `E-*` (CLI/revision/read/git/parse/internal)→2; absent input at valid revision→FAIL `R16-*-MISSING`; malformed present JSON→2.
- `correction_count` counts conforming records still blocked by shared findings; never `len(corrections)` or `1 if PASS`.
- `selftest`: in-memory `(name, docs, exit, exact id set, count)`; exact set equality, not subset; CLI cases pin `E-CLI`/`E-REVISION-INVALID`; prints `CHECK_SECTION_CITATIONS_SELFTEST: PASS (N cases, P passed, 0 failed)`; returns 0/1.
- Registry row (`SKILL.md:1818`): eight columns `Name|Kind|Entry command|Verdict map|Self-test|Pinned values|Write scope|Owner`; prose only, unread by tools, so counts must match enumeration.

## Avoid
`tools/check-root-dac-correction.py`: plain-text output, no `E-CLI`, subset selftest.

Limits: static only. Unknown: R16 IDs/constants pending CitationGate.
