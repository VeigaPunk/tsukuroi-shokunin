# Oracle04TagTree — check-source-scope-correction.py × TagTree object-ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-source-scope-correction.py-TagTree-expected-source-only
Lane bounds: leaf member — no subagent dispatch.

Reviewed bytes: `.ufo/waves/round-21/snapshot/tools/_revision.py` (pinned binder). The digest
line above is the one the item supplied; it was not recomputed (NO-EXEC). Consumer
`tools/check-source-scope-correction.py` and pinned judge
`.ufo/waves/round-21/snapshot/tools/check-revision-binding.py` were read only.

## Axes
- A1 expected outcome: exit code, status, finding id/count, `revision`/`branch_tip` echo.
- A2 oracle independence: expectation derived from fixture construction plus the contract, not the binder algorithm.
- A3 coverage: whether the round20 `--object-selectors` matrix exercises TagTree for this consumer.
- A4 mutant sensitivity: the smallest realistic weakening that the old matrix still passes.

## Case definition
TagTree is an annotated tag object whose header is `type tree`, for example
`git tag -a <name> -m m <tree-oid>`, where the tree comes from `git mktree`. The selector
is that tag object's full 40-hex ID, or a unique 7+ hex prefix of it, passed as
`--revision <sel> --branch master`. In the fixture, `refs/heads/master` exists and the
branch name is valid.

## Observed: binder path (snapshot `_revision.py`)
- Contract docstring rule 3: "revision uniquely matches an object ID, then peels to a commit else E-REVISION-INVALID".
- `bind()` follows four checks in order:
  1. `validate_branch` passes for `master`.
  2. `REV` (`^[0-9a-fA-F]{7,64}$`) matches.
  3. `_object_commit` runs `rev-parse --disambiguate=<lower>`, which returns one OID. `cat-file -t` reports `tag`, so the binder peels with `rev-parse --verify --quiet --end-of-options <oid>^{commit}`.
  4. A tree cannot peel to a commit, so that command returns nonzero. `rev-parse --git-dir` succeeds, so the result is `None`, and `bind` raises `RevisionError("E-REVISION-INVALID", "revision", "<sel> does not name one commit")`.
- Branch existence, ancestry and origin checks are never reached. INVALID takes precedence over BRANCH-MISSING, NOT-LANDED and NOT-PUSHED.
- The binder's own selftest covers this as `annotated-tag-to-tree-invalid`, lines 404-419. That is a binder-level test, not a consumer-level one.

## Observed: consumer propagation (`tools/check-source-scope-correction.py`)
- `import _revision` at line 15 resolves the live `tools/_revision.py`, not the snapshot. Grep of the live file shows the same `_object_commit` / `^{commit}` / `annotated-tag-to-` lines at the same line numbers (112, 133-140, 417). That is structural agreement, not a byte-identity proof.
- `main` lines 634-652 work as follows:
  - `revision = args.revision`, which is the raw selector.
  - `_revision.bind(ROOT, args.revision, branch)` is called with the argument unchanged. The default branch is `master`.
  - A `RevisionError` is re-raised as `Cannot(exc.fid, exc.site, exc.detail)`, keeping the id, site and detail.
  - `emit(Result(CANNOT, [Finding], 0), revision, branch, branch_tip)` runs with `branch_tip` still `None`, because it is assigned only after a successful bind.
  - `read_git` and `evaluate` are never reached, so no content findings are added.
- `emit` prints one sorted-key JSON line and returns `CANNOT`, which is 2.

## Expected output (preregistered, before candidate outputs)
- Exit 2. One stdout JSON line with:
  - `"status": "CANNOT_EVALUATE"`
  - `"correction_count": 0`
  - `"branch": "master"`
  - `"branch_tip": null`
  - `"findings": [{"id": "E-REVISION-INVALID", "site": "revision", "detail": "<sel> does not name one commit"}]`, exactly one entry
- Full-SHA semantics: `revision` echoes the selector verbatim, including its case and length, because `.lower()` is applied only inside disambiguation. It is the tag OID or its prefix. It is never a commit SHA and never the tree OID. A grader must not read this echo as an accepted binding; the pinned `exact_refusal` comment at lines 481-483 already says so.
- The outcome stays the same with or without `refs/remotes/origin/master`, and regardless of whether refs named like the tag OID or its prefix exist. Object-first lookup never consults ref aliases.
- Stderr is expected to be empty, because Git stderr is captured. [INFERENCE]

## Oracle independence and the Git object-type invariant
- Git has four object types: blob, tree, commit and tag. An object's type is part of its hashed header (`tree <len>\0…`), so an OID's type is immutable.
- A tag object names exactly one target and its type in its `object`/`type` headers. Peeling follows tag→target links only; a tree has no link to any commit. So a tag→tree chain can never reach a commit, and `^{commit}` peeling has no valid result for it.
- The expected-output oracle should derive "not a commit-ish, so INVALID" from how the fixture was built (the tag was created over a `mktree` OID) and from contract rule 3. It may optionally confirm with `cat-file -p <tag>` that the header reads `type tree`.
- The oracle must not call `_revision._object_commit` or `bind`, and must not reimplement disambiguate-then-peel. If it did, a binder bug would propagate into the expectation.
- The pinned judge's `object_commit` (lines 139-166) is the same algorithm copied again. It is fine as a judge resolver for accepted cases, but it is not an independent type oracle.

## Round20 matrix coverage (pinned `check-revision-binding.py`)
- `probe_tool` cases are `head`, `at-parent`, `branch-name`, `unlanded`, `tip`, `short-tip`, `landed-parent`, `not-pushed`, the branch-* cases, `single-id`, `blob-revision`, `git-failed`, `origin-absent` and `strict-refusals`.
- `object_selector_probes` cases are the ghost hex/full/lightweight/annotated refusals, the shadow accepts, `uppercase_object`, `full_object_id`, `annotated_tag_object`, `annotated_tag_prefix`, `noncommit_blob`, `unlanded_object`, the unlanded-prefix shadows and the unpushed cases.
- None of these is a tag→tree case, a bare-tree case or a tag→blob case. A grep for `tree|mktree` in the judge finds only the `ls-tree` and AST uses.
- The consumer's own `binding_cases` (lines 462-521) has no tag or tree case either.
- **Verdict: TagTree for this consumer is uncovered by the round20 matrix.**

## Smallest realistic weakening mutant the round20 matrix misses
- In `_object_commit`, change the peel from `f"{oid}^{{commit}}"` to `f"{oid}^{{}}"`. This is the "generic peel" confusion the ScribeDecision item explicitly rejects.
- Under the round20 matrix:
  - Tag→commit still peels to the commit, so `annotated_tag_object`, `annotated_tag_prefix` and `full_tag_object_id_ref_shadow` stay green.
  - A blob is rejected by the earlier `object_kind != "tag"` check, so `noncommit_blob` and `blob-revision` stay green.
  - The ghost and shadow cases are unaffected.
  - Every consumer-level case passes. [INFERENCE from reading the case list; not run]
- On TagTree, `^{}` returns the tree OID, so `sha` is the tree. Then `merge-base --is-ancestor <tree> refs/heads/master` dies with "not a valid commit name" (rc 128, [INFERENCE] from Git behavior). `_ancestor` maps that to `E-GIT-FAILED`, site `refs/heads/master`.
- The output is still exit 2, `CANNOT_EVALUATE`, one finding, `branch_tip: null`. Only the finding id is wrong. A grader that checks only the exit code or status would also miss it, so the TagTree case must assert the exact id `E-REVISION-INVALID` and count 1.
- The binder selftest `annotated-tag-to-tree-invalid` would catch this mutant. The consumer-facing matrix would not.
- Equivalent, non-weakening change: deleting the `if object_kind != "tag": return None` guard leaves the outcome unchanged, because blob and tree peeling fails and returns `None`, giving INVALID. A selftest should not count it as a killed mutant.
- No single-point mutant gets TagTree accepted past the old matrix. To accept it, a mutant would also need to map rc ≥ 2 to "ancestor", and the existing `git-failed` probe kills that.

## Limits
- Source review only. No run of the consumer, the binder selftest or the judge.
- The Git exit-code behavior for `merge-base` with a tree argument is [INFERENCE].
- Live `tools/_revision.py` was confirmed equal to the snapshot only at the grepped lines, not by digest.
- This report covers only this consumer and the TagTree type. It makes no non-author closure or promotion claim.

Tooling: no installs or updates. None were needed, and NO-EXEC forbids them.

Scope: executed=none
