# MigRootDac — check-root-dac-correction.py on tools/_revision.py

Clone `/tmp/migrootdac.22hlh1/repo` (51dd9ee, origin removed); sandbox master `b4c2b888cc9cba955bc7c38308c20b526522504c`. Patch `patches/MigRootDac.patch` (sha256 `bd9445b6…`, +123/−91, one file) passes `git apply --check` at lane f7fb978, whose tools/ is unchanged [obs].

## Change [obs, lines at b4c2b88]
- `import _revision` :27-29. `run_gate` :264-283 calls `_revision.bind`. RevisionError becomes `Cannot`: one finding, exit 2 (:276-282). main: `run_gate(ROOT, …)` :544.
- Removed VALID_REV, resolve, ref_tip, safe_tip, is_ancestor, binding and revision_outcome. `{7,64}` copies: 0.
- Worktree mode never binds; its branch tip comes from `_revision.branch_tip`, informational only (:270-272). git env: `_revision.clean_env()` (:244).
- The tool has no `--registry-from` or E-CLI path; argparse errors are unchanged.

## Selftest
23 → 54 PASS; the 13 domain fixtures are untouched. `_revision` 37/37 PASS.
- unlanded: {NOT-LANDED, NOT-PUSHED} → [NOT-LANDED] (:427)
- absent branch: NOT-LANDED → E-BRANCH-MISSING (:437)
- added: invalid-branch ×7, precedence ×5, invalid-revision ×11, origin-blob E-GIT-FAILED, worktree ×2, landed-parent reads its own bytes, CLI ×5 on copies that include `_revision.py` (:452-483)
- payload on refusal: `revision` is the raw input (was the resolved sha); `branch_tip` is always the informational tip.
- 8/8 scratch mutants killed.

## Judge
Root-dac, before (51dd9ee): bound true, consistent/shared false, regex 1. Failing probes: branch-* → NOT-LANDED, branch-first → INVALID, single-id carried two ids, git-failed exit 0.
After (b4c2b88): bound/consistent/shared true, local_rev_regex 0, 14/14 probes ok. Overall FAIL rc 1: consistent 2/9, shared 1/9, copies 8 (siblings unmigrated).

## Risks
- If `_revision.py` is absent, ImportError exits 1, which reads as FAIL [inf].
- Only this tool sets `sys.dont_write_bytecode`; siblings write `tools/__pycache__`, which is gitignored (.gitignore:2).
- SKILL.md:1737 still says "selftest in memory" (for L1).

Installs: none.

Scope: executed=mktemp; sandbox git clone/checkout/remote remove/commit/diff --output; mkdir -p patches; root-dac --selftest ×2 + 8 /tmp mutants; _revision.py --selftest; check-revision-binding.py ×2 (51dd9ee, b4c2b88); read-only git log/show/rev-parse/status/check-ignore/apply --check, sha256sum, wc, cat, python3 JSON reads
