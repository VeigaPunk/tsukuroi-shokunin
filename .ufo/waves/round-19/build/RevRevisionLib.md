# RevRevisionLib — scoped findings

[obs] `bind(repo, revision, branch="master")` checks branch syntax first, then a 7–64-hex commit, local branch presence/ancestry, and optional `origin/<branch>` ancestry; it returns `Binding(sha, branch, branch_tip, origin_tip)` or raises one `RevisionError` carrying `fid/site/detail` (`tools/_revision.py:50-58,134-154`). The defined error IDs are at `tools/_revision.py:42-48`.

[obs] CLI accepts exactly `--selftest`; pass/failure exits are 0/1, other argv prints usage to stderr and exits 64. Tally form: `REVISION_SELFTEST: {PASS|FAIL} ({total} cases, {passed} passed, {failed} failed)`; failures print to stderr (`tools/_revision.py:239-252`).

[obs] Binding only reads Git refs/metadata and does not write refs, index, or worktree (`tools/_revision.py:26-28`). Exception: selftest creates a temporary Git repository, commits/checks out, updates refs and writes a blob with `hash-object -w` (`tools/_revision.py:180-189,220-234`); [inf] these writes are confined to the `TemporaryDirectory` (`tools/_revision.py:180-237`).

[obs] Direct importers from the `_revision` search: `tools/check-appended-notices.py:22`, `tools/check-boot-chain.py:54`, `tools/check-freshness-r17.py:52`, `tools/check-locator-clarification.py:19`, `tools/check-recheck-commands.py:55`, `tools/check-root-dac-correction.py:29`, `tools/check-seat-scope.py:36`, `tools/check-section-citations.py:36`, `tools/check-source-scope-correction.py:15`, `tools/measure-update-recheck.py:34`. `check-revision-binding.py` is not an importer: it retains independent binding by design (`tools/check-revision-binding.py:8-10`); its `tools/check-revision-binding.py:606` match is fixture source text.

[unk] No LSP device is mounted in this session; importer census is literal grep, not semantic proof. Runtime/selftest was not run. Confidence: high for source-defined interface and write scope; importer completeness is limited to literal census.

Scope: executed=none
