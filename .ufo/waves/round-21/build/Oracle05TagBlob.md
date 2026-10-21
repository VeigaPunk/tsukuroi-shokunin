# Oracle05TagBlob — measure-update-recheck.py × annotated-tag-to-blob object selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: measure-update-recheck.py-TagBlob-expected-source-only

Lane bounds: leaf member — no subagent dispatch.

Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (baseline `tools/_revision.py`). The SHA-256 above is the one supplied in the item. This seat did not recompute it, because hashing would require execution.
Consumer: `tools/measure-update-recheck.py`, read-only. Old matrix: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.

## Axes
- A1 expected exit and status
- A2 finding identity and cardinality
- A3 full-SHA field semantics
- A4 coverage by the round-20 matrix
- A5 strength of the missed mutant

## Case definition (TagBlob)
The selector is the hex object ID (full 40-hex, or a prefix of at least 7 hex that matches exactly one object) of an annotated tag object whose `type` header is `blob`. The fixture is built with `git hash-object -w --stdin` followed by `git tag -a <name> <blob>`, and the selector is `rev-parse refs/tags/<name>^{tag}`. The tag ref name is not hex, so no ref shadowing is involved. Branch is the default `master`, landed and pushed.

## Observations (source)
- O1 consumer bind call. `import _revision` is at line 34. In `load(rev, branch)`, lines 471-481 call `_revision.bind(ROOT, rev, branch)`, with `rev` taken verbatim from `--revision` and `branch` from `--branch` (default `master`). On `_revision.RevisionError`, the consumer raises `Cannot(exc.fid, exc.site, exc.detail, revision=rev, tip=_revision.branch_tip(ROOT, branch))`. `main` (lines 758-772) catches that and calls `emit(exc.revision or revision, "CANNOT_EVALUATE", [one Finding], digest=None, branch=branch, branch_tip=exc.tip ...)`. `emit` returns `CANNOT` (2) for any status other than COUNTED or ABSENT (line 434). The consumer never touches the selector before bind. `read_git` and `git show` run only after a successful bind.
- O2 binder contract, item 3 (docstring line 17): "revision uniquely matches an object ID, then peels to a commit else E-REVISION-INVALID".
- O3 binder precedence. The checks run in order: branch (passes for `master`), then 7-64 hex (passes), then `_object_commit`, which raises E-REVISION-INVALID with site `revision` and detail `"<revision> does not name one commit"` (lines 177-179). This happens before the checks for branch-missing, landed and pushed, so the origin state and branch existence are irrelevant to this row.
- O4 binder self-coverage. The binder's own `--selftest` includes `annotated-tag-to-blob-invalid` (lines 413-419). That is a self-test of the module, not a consumer-level grade.
- O5 consumer self-test. The consumer's own `revision_case` list (lines 574-610) has no tag-to-blob or blob case.

## Expected behavior (fixed before any candidate output exists)
- E1 (axis A1): the process exits with code 2. `status` is `CANNOT_EVALUATE`. Stdout carries one sort-keyed JSON line.
- E2 (axis A2): `findings` contains exactly one entry, with id `E-REVISION-INVALID`, site `revision`, and detail `<selector as passed> does not name one commit`. No other binding id may appear. In particular E-GIT-FAILED, E-REVISION-NOT-LANDED, E-REVISION-NOT-PUSHED and E-BRANCH-MISSING are all excluded.
- E3 (axis A3), full-SHA semantics:
  - `revision` echoes the selector exactly as passed (no case change). For a full selector, that is the tag object's 40-hex ID. It is not an accepted binding, and it must never equal the blob's ID or any commit's ID.
  - The blob's ID must not appear anywhere in the payload.
  - `branch_tip` is the full 40-hex commit of `refs/heads/master`, produced by `branch_tip` → `_commit`, or null if that is unreadable.
  - `branch` is `master`, `record_count` is 0, `snapshot_sha256` is null, and every other assessment field is null or empty.
  - No record or snapshot is read at the tag's target.
- E4 (precedence): E1-E3 still hold when origin lags, when origin names a blob, and with `--branch nosuch`, because check 3 runs before checks 4-6.

## Git object type invariant (why the oracle needs no binder code)
A Git object ID is a hash over `"<type> <size>\0" + content`. The type is therefore part of the identity, so one ID has exactly one type, permanently. An annotated tag's content records `object <oid>` and `type <t>`, so the tag's own ID fixes its target and the target's type. Peeling (`^{commit}`) follows `object` links and can only reach a commit if one exists on that chain. A tag whose chain ends at a blob can never peel to a commit, whether the chain is direct or nested.

The expected verdict therefore follows from how the fixture was built (it wrote a blob, then tagged it) plus contract item 3. The oracle should check its preconditions independently: `cat-file -t <selector>` is `tag`, the tag header says `type blob`, and for a prefix, the prefix matches exactly one object. It should then hard-code `E-REVISION-INVALID`. It must not call `_revision._object_commit` or `bind`, and it must not reimplement them.

These preconditions matter because a missing object or an ambiguous prefix also yields E-REVISION-INVALID with the same detail. A row that skips them could pass for the wrong reason.

## Round-20 matrix coverage
Not covered.
- `probe_tool` has `blob-revision` (lines 448-449) and `object_selector_probes` has `noncommit_blob` (line 633). Both use a direct blob ID.
- `annotated_tag_object` and `annotated_tag_prefix` (lines 631-632) use a tag pointing to a commit, along with the ghost and shadow tag-ref cases.
- No case anywhere in the judge creates a tag whose target is a blob or a tree. A grep for `mktree`, `tree`, `tag-to` and `peel` matched nothing relevant.

## Smallest realistic weakening mutant it would miss
In `_revision._object_commit`, the tag peel is changed from `f"{oid}^{{commit}}"` to `f"{oid}^{{}}"`. This is a one-token change: peel to any object instead of peeling to a commit.

Every round-20 case still behaves the same:
- A tag pointing to a commit peels to that commit.
- A direct blob returns None at `object_kind != "tag"`, giving E-REVISION-INVALID.

For TagBlob, the mutant returns the blob's ID as `sha`. Execution then reaches `_ancestor(blob, refs/heads/master)`. I infer, without running it, that `merge-base --is-ancestor` on a blob exits with 128, which yields E-GIT-FAILED: still exit 2, but the wrong finding id and a site of `refs/heads/master`. If combined with an `_ancestor` that treats rc≥2 as False, the result would instead be E-REVISION-NOT-LANDED.

A TagBlob row graded by `exact_refusal` semantics (exit 2, `binding_ids == ["E-REVISION-INVALID"]`, `finding_count == 1`) kills both variants. A row that checks only the exit code does not.

There is no consumer-side mutant specific to TagBlob, because the consumer passes the selector through opaquely (O1). Consumer-side weakenings, such as swallowing `RevisionError` and falling back to the worktree, are already killed by the existing refusal rows.

## Inferences and limits
- I1 [INFERENCE]: `rev-parse --disambiguate=<full oid>` lists exactly that object when it exists.
- I2 [INFERENCE]: the `merge-base` exit code for a blob argument is 128. Neither I1 nor I2 was executed.
- L1: nothing was run. No candidate output exists yet. The binder SHA-256 was supplied in the item, not recomputed.
- L2: scope is limited to this consumer and type pair. Tree and nested tag-to-blob selectors behave analogously by the invariant above but were not assessed here.

Scope: executed=none
