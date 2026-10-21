# Oracle05TagTree — measure-update-recheck.py × annotated-tag-to-tree object ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: measure-update-recheck.py-TagTree-expected-source-only
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.

The digest above was supplied by the assignment. It was not recomputed because this seat is NO-EXEC. The pinned file read was `.ufo/waves/round-21/snapshot/tools/_revision.py` (440 lines). The consumer `tools/measure-update-recheck.py` was read only and not executed.

Axes covered: (A) consumer propagation, (B) expected exit, finding and SHA output, (C) whether the round-20 matrix covers this case, (D) the smallest mutant it would miss, (E) an oracle that stays independent of the binder.

## Case definition

TagTree means `--revision X`, where X is 7 to 64 hex characters that uniquely identify an annotated tag object, and that tag's target (or the end of its chain) is a tree object. For example, `git mktree` followed by `git tag -a t -m m <tree>`, with X as the full tag OID or a unique prefix of it.

## A. Consumer propagation (observed)

- The consumer imports the shared binder with `import _revision` (line 34). It keeps no local copy of the binder.
- `main` passes `args.revision` and `args.branch` to `load(...)` without changing them (lines 758–760). `load` then calls `_revision.bind(ROOT, rev, branch)` (line 476). There is no lowercasing, trimming or prefix expansion first.
- A `RevisionError` becomes `Cannot(exc.fid, exc.site, exc.detail, revision=rev, tip=_revision.branch_tip(ROOT, branch))` (lines 477–479).
- `main` catches `Cannot` and calls `emit(exc.revision or revision, "CANNOT_EVALUATE", [one Finding], digest=None, ...)` (lines 769–772).
- `emit` returns `CANNOT` = 2 for any status other than COUNTED or ABSENT (line 434).
- `read_git` and `git show` are never reached on this path. The judge's `EXTRA` for this tool is `()`, so it runs with no extra arguments.

## B. Expected behavior, stated before any candidate output exists (source-only)

The binder path, as observed in the pinned snapshot:

1. `validate_branch("master")` passes.
2. `REV` matches.
3. `_object_commit` runs `rev-parse --disambiguate=<x.lower()>`, which returns exactly one OID (the tag).
4. `cat-file -t` returns `tag`.
5. The peel `rev-parse --verify --quiet --end-of-options <oid>^{commit}` fails, and `rev-parse --git-dir` succeeds, so `_object_commit` returns `None`.
6. `bind` raises `E-REVISION-INVALID`, site `revision`, with detail `"<X> does not name one commit"`. This is contract row 3, so the branch, ancestry and origin checks (rows 4–6) never run.

Expected consumer output:

- **Exit code:** 2.
- **stdout:** exactly one sorted-key JSON line, with no traceback.
- `status`: `"CANNOT_EVALUATE"`.
- `findings`: exactly one entry, `{"id":"E-REVISION-INVALID","site":"revision","detail":"<X> does not name one commit"}`. It contains no other binding ID, and in particular not `E-GIT-FAILED`, `E-REVISION-NOT-LANDED` or `E-BRANCH-MISSING`.
- `revision`: the literal input X, with case and length as given. This is the tag OID or prefix the caller passed. It is never the tree OID or any commit SHA.
- **Full-SHA semantics:** no 40-hex commit SHA is produced, because the binding was refused.
- `branch_tip`: the full 40-hex commit of `refs/heads/<branch>` from `branch_tip()`, which never raises. It is `null` only if that branch ref is absent. With an absent branch, the revision check still comes first, so the result is still `E-REVISION-INVALID`.
- `branch`: the given branch, default `"master"`.
- `record_count`: 0. `snapshot_sha256`: null. `pending_count`, `pending_exit`, `installed_libinput`, `observed_at`, `snapshot_captured_at` and `declared_decision`: null. `source_ids`: `[]`. `health`: `"not_assessed"`.
- **Same result for:** a uniquely matching prefix of the tag OID, an uppercase spelling of X (only `revision` and `detail` echo the original case), and a tag-to-tag-to-tree chain, since `^{commit}` peels the whole chain and still fails.
- **Outside this case:** an ambiguous prefix also gives `E-REVISION-INVALID`, but for a different reason.

## C. Coverage by the round-20 matrix in the pinned `check-revision-binding.py`

The matrix does not cover this case.

- `probe_tool` only has a direct-blob case, `blob-revision` (line 449).
- `object_selector_probes` covers:
  - ghost hex branch and tag names, lightweight and annotated;
  - real-prefix shadows;
  - full commit and tag OIDs shadowed by refs;
  - uppercase OIDs;
  - full object IDs;
  - an annotated tag pointing to a **commit**, by full OID and by prefix (lines 631–632);
  - a direct blob, `noncommit_blob` (line 633);
  - unlanded and unpushed objects and their prefix shadows.
- No case builds a tree object or a tag that points to a tree. A search for `tree|mktree` only matches `ls-tree` and the AST `tree` variable. Tag-to-blob and nested tags are also absent from the judge.
- The binder's own selftest does include `tree-revision-invalid` and `annotated-tag-to-tree-invalid` (lines 407–419). That is the code being graded checking itself, not the independent judge.
- One more gap: when grading refusals, `refused` and `exact_refusal` check exit 2, the finding ID, and a single finding. They record `json_revision` but never grade it.

## D. Smallest realistic weakening mutant the round-20 matrix misses

Change the peel target in `_revision._object_commit` (line 140) from `f"{oid}^{{commit}}"` to `f"{oid}^{{}}"`, so the tag peels to any non-tag object. This is a one-token edit.

- **What still passes:**
  - Annotated tag to commit, full OID and prefix, and the nested-tag case still return the commit.
  - A direct blob still returns `None`, because its kind is not `tag`.
  - Ghost and shadow cases still behave the same.

  So every round-20 case still passes.
- **What changes for TagTree:** the peel now returns the **tree** OID as `sha`. `bind` goes on to `merge-base --is-ancestor <tree> refs/heads/master`. [INFERENCE] git rejects a non-commit operand with an exit code of 2 or more (fatal 128), so the result becomes `E-GIT-FAILED` at site `refs/heads/master`. The consumer still exits 2 with one finding, but the finding ID is wrong.
- **Why nothing catches it:** a tag-to-tree probe expecting `E-REVISION-INVALID` would detect it, and the old matrix has no such probe.
- **A second missed mutant:** dropping the `repo_check` distinction after a failed peel (raising `E_GIT` instead of returning `None`) gives the same misclassification and is also undetected.
- **What would still go undetected after adding the probe:** the judge does not grade `json_revision` on refusals. A mutant that echoed a peeled OID into `revision` would not be caught. The consumer echoes `rev`, so this is a judge gap and not a current defect in the consumer.

## E. Keeping the oracle independent, and the Git object-type rule it relies on

Git has four object types: blob, tree, commit and tag. Each object's type is part of its hashed header (`<type> <len>\0`), so an OID's type cannot change.

- A tag object's header names one target and that target's type. Peeling a tag only follows tag headers until it reaches a non-tag object.
- A tree has no parents and no commit identity. Nothing peels from a tree to a commit, so `<tree>^{commit}` cannot succeed, and ancestry is undefined for it.
- Therefore a selector whose tag chain ends at a tree never names a commit, under any correct binder.

The expected result should be derived from fixture construction plus this rule, not from calling `bind`, `_object_commit` or the judge's own `object_commit`:

1. Build the tree with `git mktree`, then the tag with `git tag -a`.
2. Confirm the fixture's types with `git cat-file -t <tag>` returning `tag`, and the tag's `type tree` header line.
3. Hard-code the expected output: exit 2, finding `E-REVISION-INVALID`, a single finding, `revision` equal to the input, no commit SHA.

If the judge's `object_commit` were reused to compute the expected value, any mutant shared by both copies would pass.

## Limits

- Nothing was executed. Exit codes, JSON fields and the git `merge-base` exit code for a tree operand are derived from reading the source. The `merge-base` behavior is marked [INFERENCE].
- `lsp` was not available in this seat, so call sites were confirmed by reading the code directly, using the cited line numbers.
- The consumer file is the live `tools/` copy, not a pinned snapshot, and its digest was not supplied. Line numbers refer to what was read on 2026-10-21.
- No tools were installed.
- No claim is made about closure by anyone other than the author, or about promotion outside this wave.

Scope: executed=none
