# Oracle07TagBlob — check-freshness-r17.py × annotated-tag-to-blob object ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-freshness-r17.py-TagBlob-expected-source-only
Lane bounds: leaf member — no subagent dispatch.

Reviewed: pinned binder `.ufo/waves/round-21/snapshot/tools/_revision.py` (digest per item, not recomputed — NO-EXEC);
pinned judge `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`; consumer `tools/check-freshness-r17.py`
(live working-tree file, read-only; it is not in the snapshot, so it is a moving file — see Limits).

## Axes
1. Exit class. 2. Finding id + count + site. 3. Full-SHA / `revision` field semantics.
4. Round-20 matrix coverage. 5. Mutant sensitivity. 6. Oracle independence.

## Case definition
Selector = the object ID (full 40-hex, or a 7+-hex prefix unique across *all* objects) of an annotated tag object
whose header says `type blob`. Default `--branch master`, `refs/heads/master` present, origin ref present or absent.

## Consumer propagation (observed)
- `main()` passes `args.revision` and `args.branch` unchanged to `_revision.bind(ROOT, args.revision, branch)` (l.773).
  There's no local regex, no normalization, and no pre-resolution (`import _revision` l.52).
- `tip = _revision.branch_tip(ROOT, branch)` is computed **before** `bind` (l.771). `revision = args.revision` (l.770)
  is only overwritten by `binding.sha` on success (l.774).
- `RevisionError` is converted to `Cannot(fid, site, detail)` and emitted as `Result(CANNOT, [one Finding], 0, 0, None)` (l.792-796).
- There is a second bind site: `--registry-from` → `_revision.bind(ROOT, args.registry_from, branch).sha` (l.778).

## Expected behavior (preregistered, source-only)
For `--revision <tag-to-blob-oid>`:
- exit **2**, `status` = `"CANNOT_EVALUATE"`.
- `findings` contains exactly one item: `{"id": "E-REVISION-INVALID", "site": "revision", "detail": "<selector as typed> does not name one commit"}`.
- `resolved_records` = 0, `record_count` = 0, and there is no `stale_records` key.
- `revision` = the raw selector string, echoed with its case preserved. It is **not** a binding: no commit SHA is bound.
  For a full ID it is a 40-hex value that names a tag, never a commit. For a prefix it is not a full SHA at all.
- `branch` = `"master"`. `branch_tip` = the full 40-hex master tip from the informational `branch_tip()`. This field is also not a binding of the selector.

For `--revision <landed commit> --registry-from <tag-to-blob-oid>`: the same exit, the same single finding and the same detail.
The difference is that `revision` is the full bound commit SHA of `--revision` and `branch_tip` = `binding.branch_tip`.

Invariance (from contract order, steps 1-3 precede 4-6):
- The result is unchanged by `--branch nosuch`, which still gives `E-REVISION-INVALID` because revision precedes branch existence.
- The result is unchanged by origin lag or origin absence, by landedness, and by refs named like the OID. Object IDs are resolved before refs, and the result is never reparsed as a ref.
- Only an invalid branch (`E-BRANCH-INVALID`) or an unavailable repo (`E-GIT-FAILED`) pre-empts it.

Binder path: `REV` matches → `--disambiguate` yields exactly one OID → `cat-file -t` = `tag` → `rev-parse --verify --quiet <oid>^{commit}` fails.
Then `rev-parse --git-dir` succeeds → `None` → `E-REVISION-INVALID` (`_revision.py` l.119-146, l.177-179).

## Git object-type invariant (oracle basis, not binder algorithm)
- An object ID is the hash of `"<type> <size>\0<content>"`. The type is inside the hashed bytes, so one ID names exactly one object of one type: a tag ID is never a commit ID.
- An annotated tag's target and target type (`object`/`type` header lines) are part of its own hashed content, so its peel chain is fixed forever.
- A tag→blob chain ends at a blob, and a blob has no commit dereference.
- Therefore "does this selector name one commit?" is answered *no* by fixture construction alone, independent of any repository state, refs or binder code.

The oracle SHOULD derive its expectation from fixture facts:
- `git hash-object -w` the blob; `git tag -a` on it; take the OID from `rev-parse refs/tags/<n>^{tag}`.
- Assert `cat-file -t` = `tag` and that `cat-file -p` shows `type blob`.
- Assert that the prefix is unique with a plain object inventory.
- Then hard-code the expected `{exit 2, ["E-REVISION-INVALID"], count 1, site "revision"}`.

It MUST NOT compute expectations by calling `_revision.bind`/`_object_commit` or the judge's `object_commit`. The judge's "independent" `object_commit` (l.139-166) is a near line-for-line copy of `_object_commit`, so it shares any shared misconception.

## Round-20 matrix coverage: **not covered**
- `probe_tool` has a `blob-revision` row, but it uses a raw blob, not a tag. `object_selector_probes` has `noncommit_blob` (raw blob), `annotated_tag_object` and `annotated_tag_prefix` (tag→commit, accepted), plus ghost tag names and ref shadows.
- No row creates a tag whose target is a non-commit.
- The consumer's own `binding_sandbox` (l.458-575) has no tag rows at all.
- The tag→blob row exists only in the binder's own selftest (`annotated-tag-to-blob-invalid`, `_revision.py` l.413-419). That calls `bind` directly and not through this consumer's CLI.
- `QUALITY.md` item 40 agrees: "the preregistered per-consumer matrix still lacks tree/tag-to-noncommit rows".

## Smallest realistic weakening mutant missed by the round-20 matrix
**M1 (one token):** in `_object_commit`, peel with `f"{oid}^{{}}"` instead of `f"{oid}^{{commit}}"`. This is the common "fully peel a tag" idiom.
- On tag→commit (and on nested tags) the result is identical, so `annotated_tag_object`, `annotated_tag_prefix` and `full_tag_object_id_ref_shadow` still pass.
- Raw blob rows still refuse at `object_kind != "tag"`.
- On tag→blob, M1 returns the blob OID, and `merge-base --is-ancestor <blob> refs/heads/master` fails with exit status ≥ 2. The expected result is then **exit 2, `E-GIT-FAILED`, site `refs/heads/master`** instead of `E-REVISION-INVALID` at site `revision`. [INFERENCE: merge-base exit status ≥ 2 on a blob argument; not executed]
- M1 is caught only by the binder selftest, not by any per-consumer row.
- Consequence for the oracle: exit code alone (2 in both cases) cannot distinguish M1. The assertion that carries the weight is finding id + count + site.

A second missed weakening: on peel failure, fall back to `_commit(repo, revision)`, i.e. ref resolution. This accepts a shadow branch or tag named `<tag-oid>` that points at a landed commit, which shows up as exit ≠ 2 with the decoy's SHA. The matrix's ref-shadow row exists only for tag→commit, where the object path wins before the fallback.

## Observations / inferences / limits
- Observed: the consumer has two pass-through bind call sites; the binder path ends in `E-REVISION-INVALID` for tag→blob; there is no tag→noncommit row in the judge or the consumer sandbox.
- Inference: the exit status of `merge-base` on a blob (M1 outcome); the `rev-parse --verify --quiet` peel failure is non-zero for tag→blob.
- Limits:
  - Nothing was executed, and the snapshot digest was taken from the item, not recomputed.
  - The consumer was read from the live tree, not a pinned snapshot.
  - The expectation assumes the `tools/_revision.py` imported at run time is byte-identical to the pinned snapshot; this is unverified.
  - The expectation does not cover an ambiguous prefix (still `E-REVISION-INVALID`, but via the `len != 1` branch, which does not exercise the peel path) or a signed-tag configuration.
- This is not a claim of non-author closure or outside promotion. No tools were installed; none were needed for source review.

Scope: executed=none
