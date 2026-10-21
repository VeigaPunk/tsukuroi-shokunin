# Oracle08TagTree — check-recheck-commands.py × annotated-tag→tree object selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-recheck-commands.py-TagTree-expected-source-only

Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (SHA as above, taken from the item; not recomputed — NO-EXEC).
Consumer: `tools/check-recheck-commands.py` (live file, read-only; no pinned snapshot copy exists under `snapshot/tools/`, so its bytes are unpinned — limit).
Judge: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py` (round-20 object-selector matrix).

## Axes
1. Exit class. 2. Finding identity and cardinality. 3. Full-SHA / `revision` field semantics. 4. Coverage by the round-20 matrix. 5. Mutant sensitivity.

## Observed — consumer propagation
- `import _revision` (line 55); `run()` passes `args.revision` and `args.branch` unchanged to `_revision.bind(repo, args.revision, branch)` (line 918). No normalization, lowercasing, or prefix handling in the consumer.
- Only `forbid_list(args.forbid)` (line 916) runs before bind; the default forbid list is valid, so it does not intercept.
- On `RevisionError`: `tip = _revision.branch_tip(repo, branch)`, re-raised as `Cannot(exc.fid, exc.site, exc.detail)` (lines 919-921). The handler emits `CANNOT_EVALUATE` with `revision = sha or args.revision`. `sha` is still None, so the field echoes the selector string (lines 930-934). `origin_tip` remains None.
- `emit` maps `CANNOT_EVALUATE` to exit 2 (`PASS, FAIL, CANNOT = 0, 1, 2`, lines 57 and 795). Counts are None, so all counts are 0 and `forbidden` is `[]`.
- Paths, `--exec-log`, and evaluation run only after a successful bind, so they are unreachable for this selector.

## Observed — binder path for an annotated tag whose target is a tree
`bind` (line 172): branch validation passes, then `REV` 7-64 hex passes, then `_object_commit` runs:
- `rev-parse --disambiguate=<lower>` returns exactly one object (full ID or a unique prefix).
- `cat-file -t` returns `tag`.
- The peel `rev-parse --verify --quiet --end-of-options <oid>^{commit}` exits non-zero. The repository is readable, so the function returns None (lines 139-145).
- `bind` raises `E-REVISION-INVALID`, site `revision`, with detail `"<revision> does not name one commit"` (lines 177-179). This happens before the branch-existence, landed, and pushed checks, so `--branch nosuch` and a lagging origin cannot change the finding.
- The binder's own selftest asserts `annotated-tag-to-tree-invalid`, which gives E_INVALID (lines 413-418). That test belongs to the graded module and does not count as independent evidence.

## Git object-type invariant (why the oracle can be a constant)
- An object ID is the hash of `<type> <len>\0<content>`. An annotated tag's `object <id>` / `type tree` header is part of that content, so its target type cannot change while its ID stays the same.
- `^{commit}` dereferences tag objects until it reaches a non-tag object. A tree is terminal: it contains blobs, trees, and gitlinks (mode 160000), and peeling never follows a gitlink. No commit is reachable by peeling tag→tree.
- So "tag→tree names no commit" is a property of the fixture's construction. It does not depend on refs, the branch, origin, or the binder.

The oracle MUST derive its expectation from the fixture recipe and MUST NOT call `--disambiguate` or the peel itself:
- Recipe: `hash-object -w`, `mktree`, `tag -a X <tree>`.
- Fixture self-check, permitted because it checks construction rather than reproducing the algorithm: `cat-file -t T` is `tag`, and `cat-file -p T` contains `type tree`.

## Expected (stated before any candidate output)
For selector S equal to T (the full tag-object ID), with default `--branch master` and master landed:
- Exit code 2. One JSON line on stdout.
- `status` is `"CANNOT_EVALUATE"`.
- `findings` contains exactly one entry: `{"id":"E-REVISION-INVALID","site":"revision","detail":"<S> does not name one commit"}`. There are no other binding ids.
- `revision` equals S verbatim: case preserved, and short if S is short. It is the tag-object ID, not a commit. The oracle MUST NOT treat a 40-hex `revision` as acceptance. Assert `revision == S` and that `revision` is not equal to any commit in the fixture.
- No full commit SHA is reported as the bound revision.
- `branch` is `"master"`. `branch_tip` is the independently recorded full 40-hex master tip.
- `origin_tip` is null even when `refs/remotes/origin/master` exists, because the consumer only sets it from a successful Binding.
- `file_count`, `invocation_count`, and the other counts are 0. `forbidden` is `[]`.

The following variants have the same expectation:
- A unique prefix of T with 7 or more hex characters.
- `S.upper()`.
- `--branch nosuch`, which still gives E-REVISION-INVALID because revision is checked before branch existence.
- Origin lagging behind master.
- A nested tag (tag→tag→tree).
- Ref-shadow: `refs/heads/<S>` and `refs/tags/<S>` both pointing at a landed commit. The result is still INVALID, because object IDs take precedence over refs.

## Round-20 matrix coverage: not covered
- `object_selector_probes` (judge lines 475-673) covers:
  - tag→commit (`annotated_tag_object`, `annotated_tag_prefix`, accepted)
  - a direct blob (`noncommit_blob`)
  - ghost hex refs, prefix and ref shadows
  - unlanded and unpushed selectors
- `probe_tool` adds `blob-revision` and an origin pointing at a blob.
- No case covers a tree, tag→tree, or tag→blob.
- A direct blob is rejected at `object_kind != "tag"` (line 136) and never reaches the peel branch. The only tag case that reaches the peel uses a commit target, where the peel succeeds.
- So the peel-failure path (lines 141-145) is never exercised for this consumer. The judge's independent `object_commit` (lines 139-166) agrees with the binder in source, but the matrix never feeds it a tag→tree.

## Smallest realistic weakening mutants the matrix would miss
- **M1 (one token, line 140): `f"{oid}^{{commit}}"` changed to `f"{oid}^{{}}"`.** `^{}` is the common "peel tag" idiom.
  - Tag→commit still peels to the commit, so every round-20 case still passes.
  - Tag→tree returns the tree ID as `sha`. `merge-base --is-ancestor <tree>` then fails with rc ≥ 2, which surfaces as `E-GIT-FAILED`. The binder docstring documents this rc ≥ 2 non-commit behaviour; the rc for a tree specifically is [INFERENCE].
  - The consumer still exits 2 and still echoes `revision`, so only the exact-finding-id assertion catches M1. An exit-only oracle would miss it.
- **M2 (line 145):** change `return None` to `raise RevisionError(E_GIT, ...)`. This also misclassifies the selector as E-GIT-FAILED and is also missed.
- **M3 (false acceptance):** on peel failure, fall back to `_commit(repo, revision)`. Without a shadow ref this stays INVALID.
  - With a ref named after a short prefix of T that points at a landed commit, git resolves the ref instead of the object [INFERENCE: git refname-vs-short-hex precedence], so the bind wrongly succeeds (exit 0 or 1, `revision` set to the decoy).
  - The round-20 shadow cases only use the commit tip and tag→commit, so they miss M3. The ref-shadow tag→tree variant above catches it.

## Limits
- NO-EXEC: no candidate run. Git exit codes for merge-base on a tree and for refname precedence are inferred, not observed.
- The consumer file is unpinned, and its SHA was not computed.
- Scope is only this consumer and type pair.

Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
