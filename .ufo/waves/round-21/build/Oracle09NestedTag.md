# Oracle09 — NestedTag object-ID selector × check-seat-scope.py (expected source-only)

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-seat-scope.py-NestedTag-expected-source-only

Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py`.
Consumer (original-nine member): `tools/check-seat-scope.py`.
Round-20 matrix: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.

## Axes

- **Fidelity**: expected verdict/finding/JSON `revision` field for a selector whose
  disambiguated object is an annotated tag pointing to another tag (chain length ≥ 2).
- **Coverage**: whether the pinned round-20 `--object-selectors` case list exercises
  this type pair.
- **Robustness**: the smallest realistic weakening mutant in `_revision.bind` the
  existing matrix cannot distinguish.

## Consumer propagation (observed, read-only)

- `main()` collects `args.revision` as `revision_in` and calls
  `collect(wave, revision_in, branch)` (check-seat-scope.py:651, 661).
- `collect()` calls `bind_revision(root, revision, branch)` only when
  `revision is not None` (line 260–262); `bind_revision` is `_revision.bind`
  imported at line 36. A `RevisionError` is re-raised as `Cannot(exc.fid,
  exc.site, exc.detail)` (263–264), so binder finding ids, sites, and details
  pass through unchanged and exit as CANNOT_EVALUATE (exit 2) with exactly one
  finding (663–665).
- On success `collect` returns `bound.sha` as the displayed revision (265, 272),
  and `emit` prints it as JSON `"revision"` (158). Reads are `git show
  <sha>:<path>` / `ls-tree <sha>` (196–214), i.e., the resolved commit object,
  never the raw selector.
- No tag of any depth appears in the consumer's own selftest (`tag` has zero
  matches in the file); all NestedTag behavior is delegated to the shared binder.

## Expected NestedTag semantics (derived from pinned source)

`bind()` flow for a hex selector of length 7–64 (else E-REVISION-INVALID, "7-64
hex commit required"):

1. `rev-parse --disambiguate=<lowered selector>` must yield exactly one object;
   zero or two-plus → `None` → E-REVISION-INVALID "does not name one commit"
   (_revision.py:119–124, 177–179).
2. `cat-file -t <oid>` on the disambiguated oid reports the outermost object
   type. For a nested-tag chain the outer object is still `tag`, so the tag
   branch runs (127–137).
3. `rev-parse --verify --quiet <oid>^{commit}` peels the chain. Git's
   `^{commit}` suffix dereferences tag objects **transitively** to the first
   non-tag object and requires it to be a commit. A nested annotated tag whose
   terminal target is a commit therefore resolves to that commit's full 40-hex
   SHA (139–142). Peel failure on a readable repo → `None` → E-REVISION-INVALID
   (this is the nested-tag-to-blob/tree case).
4. `merge-base --is-ancestor <sha> refs/heads/<branch>` must hold or
   E-REVISION-NOT-LANDED (180–185); if `refs/remotes/origin/<branch>` exists,
   ancestry there too or E-REVISION-NOT-PUSHED (186–191).

Expected consumer outcomes, before any candidate output exists:

- **Nested tag → landed, pushed commit**: exit 0 or 1 per seat reports (PASS /
  FAIL), never CANNOT_EVALUATE on binding grounds; JSON `"revision"` equals the
  **full 40-hex terminal commit SHA** — not the outer tag oid, not the inner
  tag oid, not the input prefix. `branch_tip` is the resolved tip commit.
- **Nested tag → unlanded commit**: exit 2, single finding
  `E-REVISION-NOT-LANDED`, site `refs/heads/<branch>`; `"revision"` echoes the
  raw selector string (collect raises before returning a bound sha).
- **Nested tag → non-commit terminus** (chain ends at blob/tree): peel fails →
  exit 2, `E-REVISION-INVALID`, detail "<sel> does not name one commit".
- **Tag oid prefix selector** (7–39 hex uniquely naming the outer tag): same
  as above; `--disambiguate` lowercases the input, so uppercase prefixes work.

## Round-20 matrix coverage: NO for NestedTag

`object_selector_probes` (check-revision-binding.py:475–673) builds exactly one
annotated tag — `git tag -a … <tip>` (502–509) — a **one-level tag pointing
directly at a commit**. Every tag-typed case uses that object or its prefix:
`full_tag_object_id_ref_shadow`, `annotated_tag_object`, `annotated_tag_prefix`
(616–632). No `git tag … <tag>` chain is ever constructed, so **no case exercises
a tag whose direct target is another tag**. This holds whether or not the suite
is invoked: it is additionally opt-in behind `--object-selectors`
(815–816, 722–727), so even an enabled run stays silent on NestedTag.
The type pairs actually covered: commit, tag→commit (depth 1), blob, ghost
refs, unlanded commit. `tag→tag→…` and `tag→blob/tree` are absent.

## Smallest realistic weakening mutant the matrix misses

In `_object_commit` change the peel at _revision.py:139–140 from
`f"{oid}^{{commit}}"` to `f"{oid}^{{}}"` (single dereference). For every
round-20 case `^{}` is observationally identical: the only tags in the
fixture are depth-1, where `tag^{}` is already the commit. Under NestedTag the
mutant resolves `outer^{}` to the **inner tag object**; `merge-base
--is-ancestor` on a tag object fails → the consumer reports
E-REVISION-NOT-LANDED (exit 2) where the pinned binder binds and continues.
A depth-1-peel binder could alternatively accept then report the wrong
`"revision"`, which `accepted()`'s `json_revision == expect_sha` comparison
(396–404) would catch — but no matrix case supplies a nested tag to expose
either failure mode. Both variants pass 100% of the existing object-selector
and consistency cases.

## Why the oracle must not import the binder / Git type invariant

An expected-output oracle that calls `_revision.bind` (or `_object_commit`)
grades the implementation against itself: any weakening of the peel rule would
be reproduced verbatim in the "expected" value. The independent invariant is
Git plumbing semantics, reproducible without the module: the disambiguated oid's
`cat-file -t` is `tag`; `<oid>^{commit}` is defined by Git as the transitive
tag peel to the first non-tag object, which must be a commit; and
`merge-base --is-ancestor` is defined over commits. The judge already honors
this separation — its own `object_commit` (139–166) reimplements the same
plumbing sequence rather than importing `_revision`.

## Limits

- Source-only derivation; no tool was executed and no candidate outputs exist.
- `^{commit}` transitivity is asserted from Git's documented peel semantics and
  the binder's own reliance on it, not re-verified against a live repository.
- Scope restricted to this consumer/type pair; other tools and other object
  types are out of scope.

Scope: executed=none
