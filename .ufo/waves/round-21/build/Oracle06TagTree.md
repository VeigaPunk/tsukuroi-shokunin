# Oracle06TagTree — check-boot-chain.py × annotated-tag-to-tree object-ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-boot-chain.py-TagTree-expected-source-only
Lane bounds: leaf member — no subagent dispatch.

Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (the SHA above is supplied by the item; I could not hash it without executing anything). Consumer: `tools/check-boot-chain.py`, which I read in its live state. Judge: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.

## Axes
- A1: how the consumer propagates the bind call (argv to `bind`, and `RevisionError` to JSON and exit code).
- A2: the expected behavior for a TagTree selector, derived from the contract and Git invariants only.
- A3: whether the round-20 matrix covers this case.
- A4: the smallest weakening mutant that the matrix misses.

## A1 — consumer propagation (observed)
- The consumer imports `_revision` directly (line 54) and does not copy the regex (help text at lines 834-837).
- `main()` at 1570-1584 sets `revision, branch_tip = "unbound", None` and then calls `_revision.bind(ROOT, args.revision, branch)`. `ROOT` is the parent of `tools/` (line 57). `--branch` defaults to `master` (line 840), and `--revision` is passed through unmodified.
- On `_revision.RevisionError`, the consumer makes one `Finding(exc.fid, exc.site, exc.detail)` and then calls `emit(Result(CANNOT,[finding],0,0), revision, branch, branch_tip)`. With `--statement-corrections` it calls `emit_statement_corrections` instead. In both cases `revision` and `branch_tip` keep their pre-bind values, because they are only assigned after `bind` returns.
- `emit` (785-798) prints a sorted JSON object, and its return value becomes the exit code: `CANNOT = 2` (line 56).
- The consumer's own `binding_cases` (1324-1393) contain no tag, tree or blob vectors.

## A2 — expected behavior, source-only (derived before any candidate output exists)
The Git object-type invariant behind this expectation:
- An object ID is the hash of `"<type> <size>\0<body>"`, so an object ID's type cannot change.
- An annotated tag object records the type of its target (`type tree`).
- Peeling only follows tag objects. A tree has no commit to peel to, so `<tagoid>^{commit}` cannot resolve for a tag that points at a tree. The same holds for any chain of tags that ends at a tree.
- Therefore the expected result follows from contract step 3 ("uniquely matches an object ID, then peels to a commit, else E-REVISION-INVALID") plus this invariant. It does not depend on the binder's code.

For the fixture, an independent oracle needs only these facts:
- `git cat-file -t <sel-oid>` returns `tag`.
- The tag body's `type` line is `tree`.
- The selector is the unique object match for its hex prefix.
- The default branch `master` is valid and exists.

Expected result for `--revision <S>`, where S is the full 40-hex tag object ID, its upper-case form, or a unique prefix of at least 7 hex characters, in default mode:
- The process exits with code 2.
- stdout is exactly one JSON object with:
  - `status` = `"CANNOT_EVALUATE"`;
  - `findings` = exactly one item, `{"id":"E-REVISION-INVALID","site":"revision","detail":"<S> does not name one commit"}`. The detail echoes S as typed, without lower-casing (binder line 179);
  - `revision` = `"unbound"`;
  - `branch` = `"master"`;
  - `branch_tip` = `null`;
  - `verdicted_kernel_entries` = 0 and `entry_count` = 0.
- Full-SHA semantics: no 40-hex value appears in `revision` or `branch_tip`. That excludes the tag ID, the tree ID and the current branch tip.
- The outcome does not depend on landed, pushed or origin state, because step 3 runs before steps 4-6.
- With `--statement-corrections`, the same single finding is reported, `correction_count` is 0, and the exit code is 2.
- No finding other than `E-REVISION-INVALID` is acceptable. In particular, `E-GIT-FAILED`, `E-REVISION-NOT-LANDED` and `E-BRANCH-MISSING` are all wrong, even though each also exits with code 2.

## A3 — coverage by the round-20 matrix (observed)
The round-20 matrix does not cover this case.
- `object_selector_probes` (judge 475-673) does run for `check-boot-chain.py`, because `R17_GATES` is part of `TOOLS` (lines 71-79).
- Its object-type cases are limited to:
  - annotated tag to commit (`annotated_tag_object`, `annotated_tag_prefix`, `full_tag_object_id_ref_shadow`);
  - a direct blob (`noncommit_blob`, and `blob-revision` in `probe_tool`).
- It has no direct-tree case, no tag-to-tree case, no tag-to-blob case and no nested-tag case. A grep of the judge for `mktree`, `tree` or `^{}` finds only `ls-tree` and `ast` usage.
- The pinned lessons file `corpus/lessons/round-20.md:46` (R20-BIND-TARGET-TYPE) records the same gap. Tag-to-tree is covered only by the binder's own selftest (`annotated-tag-to-tree-invalid`, `_revision.py` 404-419), not at the consumer level.

## A4 — smallest realistic weakening mutant the matrix misses
- M1: a one-token change in `_object_commit` (binder line 140), replacing `f"{oid}^{{commit}}"` with `f"{oid}^{{}}"`.
  - For tag-to-commit and nested tag-to-commit, the result is unchanged, so every round-20 tag row passes. Direct blob and direct tree never reach this branch, so `noncommit_blob` also passes.
  - For tag-to-tree, `bind` gets the tree ID and passes it to `merge-base --is-ancestor`. [INFERENCE: git refuses a non-commit there with exit code ≥2, which the binder maps to `E-GIT-FAILED`, site `refs/heads/master`, exit 2.]
  - An oracle that checks only the exit code, or only "refused", misses M1. An exact single-finding check like `exact_refusal` would catch it, but only if a tag-to-tree row existed.
- M1′ is equally small: in the tag-peel failure path (binder 143-146), raise `E_GIT` instead of returning `None`. It has the same blind spot.
- Separate residual, consumer side: the judge does not grade `revision` on refusals (judge comment at 482-483). A consumer that echoed S into `revision` would pass every matrix row. The expected oracle above therefore requires `revision == "unbound"`.

## Observations, inferences and limits
- Observed: everything cited by file and line above.
- Inferred: git's exit code for `merge-base --is-ancestor` on a tree, and that `^{commit}` peeling of a tag-to-tree exits non-zero with `--quiet`. Both come from Git semantics; I did not run them.
- Limits:
  - I did not hash the snapshot or the live `tools/_revision.py`, so equality between the binder the consumer actually imports and the pinned snapshot is not established here.
  - I made no claim about any other consumer or object type.
  - No tools were installed or needed.

Scope: executed=none
