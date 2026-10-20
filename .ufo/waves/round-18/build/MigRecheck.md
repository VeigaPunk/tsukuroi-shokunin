# MigRecheck — tools/check-recheck-commands.py

Model: anthropic/claude-opus-5-5 (session context). No installs.

Clone `/tmp/tsukuroi-r18-migrecheck-SfbzB4/repo` (51dd9ee, origin removed); master `010ad95a08d9996fd06750058c518b45b990631d`. Patch `patches/MigRecheck.patch` (sha256 `f5c2f41e…`), base blob `5ca4dab` = current lane file. No production edit.

## Behaviour
- `import _revision`; `_revision.bind(repo, rev, branch)`. A RevisionError becomes Cannot: one finding, exit 2, informational `branch_tip`. Deleted: local REV/BRANCH regexes, `ref_sha`, `is_ancestor`, `bind`. `--forbid` and argparse errors stay E-CLI.
- Pointers in the last `recheck:` line (`§7`, `§7's`, `§§1–5`, `§4.2`, `Appendix[ A]`) resolve to same-file headings outside fences, subsections included:
  - forbidden command in the section: RECHECK-FORBIDDEN-INVOCATION;
  - no matching heading: RECHECK-POINTER-UNRESOLVED;
  - pointers inside spans or after a `*.md` name are skipped.
  New field: `pointer_section_count`.
- `## R18-RECHECK` is accepted. The latest round is operative; its `procedure:` pointers are followed.
- A word-initial `#` starts a comment (degraded-triage-r4.md:597).

## Evidence [obs]
- Own selftest 43 → 80 PASS, also against the lane's uncommitted `_revision.py`. Module selftest 37 PASS. All 12 mutants killed.
- Judge at 010ad95, this tool: bound, consistent and shared, local_rev_regex 0. Before: not consistent, not shared, 1 copy. Totals: 2/9 consistent, 1/9 shared, 8 copies (siblings unmigrated here). Tip and parent probes exit 1 (was 0).

## Changed expectations
- `--branch nosuch`: NOT-LANDED → BRANCH-MISSING.
- `a..b`, `master/`: NOT-LANDED → BRANCH-INVALID.
- `"bad branch"`: E-CLI → BRANCH-INVALID.
- HEAD with `a..b`: REVISION-INVALID → BRANCH-INVALID.
- Non-repo path: REVISION-INVALID → GIT-FAILED.

## Risks [inf, static]
- At 51dd9ee, 10 files are flagged:
  - aur-risk-plane §7:309
  - aur-drift-receipt-r9
  - aur-risk-plane-ver-s6 and -s7
  - census-closeout-receipt-r10
  - host-health-report-r3
  - journal-boot-plane
  - update-safety-note, -v2 and -v3
- The 5 R17 files stay resolved.
- Limits: one pointer level; spans read per line; fenced output lines count as commands.

Scope: executed=sandbox clone/checkout/remote-remove/commit×2; own selftests (+temp mutants, lane-module copy); _revision selftest; judge×2; git diff/apply --check
