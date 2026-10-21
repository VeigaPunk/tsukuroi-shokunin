# Oracle07TagTree — check-freshness-r17.py × TagTree object-ID selector (source-only)

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-freshness-r17.py-TagTree-expected-source-only
Lane bounds: leaf member — no subagent dispatch.

Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (SHA-256 above, as supplied by the item; not recomputed under NO-EXEC).
Consumer: `tools/check-freshness-r17.py` (read-only, not executed).
Old matrix: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.

## Axes
- A1 expected exit/finding for a TagTree selector (annotated tag object whose target is a tree)
- A2 full-SHA / JSON field semantics on refusal
- A3 bind call/argument propagation in the consumer
- A4 round20 matrix coverage of this exact case
- A5 smallest realistic weakening mutant the old matrix misses
- A6 oracle independence (Git object-type invariant, no binder algorithm)

## Observations (source)
- O1 Consumer `main()` (lines 769-775): `revision = args.revision`; `tip = _revision.branch_tip(ROOT, branch)`; then `binding = _revision.bind(ROOT, args.revision, branch)`; only on success `revision = binding.sha`, `tip = binding.branch_tip`. `branch` is `args.branch`, default `master`. The selector goes to `bind` unmodified (not lowercased or expanded).
- O2 On `_revision.RevisionError` (lines 792-796) the consumer maps it to `Cannot(exc.fid, exc.site, exc.detail)` and emits `Result(CANNOT, [one Finding], 0, 0, None)` with the still-raw `revision`, `branch`, and the pre-bind `tip`. `emit` prints one sorted-key JSON line. `stale_records` is absent because `stale is None`. Exit code is `CANNOT` = 2 via `sys.exit(main())`.
- O3 Import (lines 51-52): plain `import _revision` resolves from the script's own `tools/` directory (sys.path[0]), so it uses the live `tools/_revision.py` or the sandbox copy that the judge materializes. Live `tools/_revision.py` has the same `_object_commit` structure at lines 112-136 (grep), but byte identity with the pinned snapshot was not verified (limit L1).
- O4 Binder contract rows 2-3 (docstring lines 16-17): a revision must be 7-64 hex, must uniquely match one object ID, and must then peel to a commit; otherwise the error is `E-REVISION-INVALID`. `bind` (lines 172-179): `_object_commit(...) is None` raises `RevisionError(E_INVALID, "revision", f"{revision} does not name one commit")`. This happens before the branch-existence, landing, origin, and E-GIT checks (lines 180-191).
- O5 `_object_commit` (lines 112-146): the object type is checked after enumeration. A `tag` is peeled with `^{commit}`, and a failed peel in a readable repo returns `None`.
- O6 The binder's own selftest contains `annotated-tag-to-tree-invalid` (lines 413-419), which expects `E_INVALID`. That is a binder-internal test, not a consumer/judge grade.

## Expected behavior (fixed before any candidate output exists)
Fixture facts (built by the fixture, not computed by the oracle): T is a tree written with `mktree`. G is an annotated tag object whose header has `type tree` / `object <T>`. `cat-file -t G` = `tag`. The selector S is G's full 40-hex or a unique ≥7-hex prefix (any case). Run the consumer with `--revision S` and default `--branch master`. The branch is valid and present.

- Exit: `2`.
- stdout: exactly one JSON object with `status` = `CANNOT_EVALUATE`.
- `findings`: exactly one item, `{id: "E-REVISION-INVALID", site: "revision", detail: "<S> does not name one commit"}`. There must be no second binding id.
- `revision`: the byte-exact raw selector S, without lowercasing or prefix expansion. It must equal neither T, nor G's full ID when S is a prefix, nor any commit SHA.
- `branch`: `"master"`.
- `branch_tip`: the full 40-hex commit of `refs/heads/master`, taken from the pre-bind `branch_tip` call. It is not derived from S.
- `resolved_records`: 0. `record_count`: 0. `scope`: the SCOPE constant. The `stale_records` key is absent.
- Precedence controls (expected id unchanged): `E-REVISION-INVALID` still wins when `--branch nosuch` (otherwise E-BRANCH-MISSING), when `refs/remotes/origin/master` lags (otherwise NOT-PUSHED), and when origin names a blob (otherwise E-GIT-FAILED), because the refusal at row 3 comes first. This holds even if T is the root tree of a landed commit.
- Adjacent case, outside this pair's grade: with a valid `--revision` and `--registry-from S`, the result is the same single finding, but `revision` = the full bound SHA of `--revision` (it is set before the second bind).

## Git object-type invariant (why the oracle needs no binder algorithm)
Every Git object has exactly one type (blob, tree, commit, or tag), and that type is part of the hashed header, so an object ID fixes its type. A tag chain ends at the first non-tag target. A tree entry lists only blobs, trees, and gitlinks; it has no pointer to a commit and no parents. Ancestry (`merge-base --is-ancestor`) is defined only between commits. So a tag whose chain ends at a tree names no commit, and the contract outcome must be "does not name one commit" for every repo state. The expected value is therefore a constant refusal. The oracle should take its expected values from contract rows 2-3 plus fixture construction. It should not call `_revision.bind` or `_object_commit`, and it should not use the judge's `object_commit` copy (judge lines 139-166), which mirrors the binder's peel step and would share any defect in it.

## Round20 matrix coverage (A4): NOT covered
- `object_selector_probes` (judge lines 475-673) contains only `annotated_tag_object`/`annotated_tag_prefix` (tag→commit, accept), `noncommit_blob` (direct blob, refusal), plus ghost-hex, shadow, unlanded, and unpushed rows. There is no tree row and no tag→tree row.
- `probe_tool` shared cases contain only `blob-revision` (direct blob).
- The consumer's own `binding_sandbox` (lines 458-545) has no tag or tree selector.
- Only the binder's internal selftest contains `annotated-tag-to-tree-invalid`, and it does not grade this consumer.

## Smallest realistic weakening mutant missed (A5)
In `_object_commit`, change the tag peel from `f"{oid}^{{commit}}"` to `f"{oid}^{{}}"` (peel to any non-tag object).
- tag→commit: same commit, so `annotated_tag_object`/`annotated_tag_prefix` still pass.
- direct blob and direct tree: the `object_kind != "tag"` branch still returns None, so `noncommit_blob` passes.
- TagTree: the function returns T's full ID as `sha`, and `bind` reaches `merge-base --is-ancestor T refs/heads/master`. [INFERENCE] Git rejects a non-commit there with exit ≥2, so the result would be `E-GIT-FAILED` (still exit 2, wrong id, and the tree is misclassified as a git failure rather than an invalid selector).

The round20 judge stays green. Only a TagTree row that checks the exact finding id kills this mutant. A second variant, `object_kind in ("tag", "tree")` routed to the peel, is also missed by the matrix; it still yields INVALID, so it is behavior-equivalent for this pair. A row that grades only the exit code would also miss the `^{}` mutant. The row MUST assert `binding_ids == ["E-REVISION-INVALID"]` and `finding_count == 1`, and SHOULD assert `revision == S`.

## Inferences / limits / unknowns
- L1: Byte identity between the live `tools/_revision.py` and the pinned snapshot was not checked under NO-EXEC. The consumer binds whichever copy sits beside it.
- L2: The exact `merge-base` exit code for a tree argument in the `^{}` mutant is inferred from Git semantics, not observed.
- L3: The judge's `refused()`/`exact_refusal` do not grade `json_revision` for refusals (comment at lines 482-483). The full-SHA semantics above are stricter than the old judge.
- Confidence: high for A1-A4 and A6 (direct source reading); medium for the A5 failure id (L2).
- No tool installs were needed or done.

Scope: executed=none
