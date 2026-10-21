# Oracle06TagBlob — check-boot-chain.py × TagBlob object-ID selector (source-only)

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-boot-chain.py-TagBlob-expected-source-only
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.

Reviewed: `.ufo/waves/round-21/snapshot/tools/_revision.py` (pinned binder; SHA-256 taken from the assignment, not recomputed — NO-EXEC);
`tools/check-boot-chain.py` (working tree, read-only; no pinned consumer copy exists under `.ufo/waves/round-21/`);
`.ufo/waves/round-21/snapshot/tools/check-revision-binding.py` (round20 matrix).

## Axes
- A1 expected exit / status
- A2 expected finding set (id, count, site)
- A3 full-SHA / `revision` field semantics
- A4 round20 matrix coverage
- A5 oracle independence from the binder algorithm

## Case definition (TagBlob)
Fixture: `B = git hash-object -w` some bytes; `git tag -a T -m … B`; `X = rev-parse refs/tags/T^{tag}`.
Selector = `X` (full 40-hex) or a unique ≥7-hex prefix of `X` with no colliding ref.
Invocation: `check-boot-chain.py --revision <selector> [--branch master]`, no `--statement-corrections`, no `--registry-from`.

## Observed: consumer propagation
- `import _revision` (line 54); `ROOT = Path(__file__).resolve().parents[1]` (line 57).
- `main()` (1570–1584): `revision, branch_tip = "unbound", None`, then `_revision.bind(ROOT, args.revision, branch)`, passing the argv string unchanged. On `RevisionError` it re-wraps the error as `Finding(exc.fid, exc.site, exc.detail)` and returns `emit(Result(CANNOT, [finding], 0, 0), revision, branch, branch_tip)` *before* reassigning `revision` or `branch_tip`.
- `emit()` (785–798) prints one sorted-keys JSON line and returns `result.code`. `CANNOT = 2` maps to `"CANNOT_EVALUATE"`.
- The consumer has no local revision regex or resolver; all selector semantics are delegated to the binder.

## Observed: pinned binder path for TagBlob
`bind` → `validate_branch("master")` passes → `REV` 7-64 hex passes → `_object_commit`:
`rev-parse --disambiguate=<sel>` returns one OID (`X`) → `cat-file -t X` gives `tag` → `rev-parse --verify --quiet --end-of-options X^{commit}` fails, because the peel chain ends at a blob → `rev-parse --git-dir` succeeds, so the result is `None` → `RevisionError(E-REVISION-INVALID, "revision", "<sel> does not name one commit")`.
The branch, ancestry and origin steps are never reached.

## Expected (preregistered before any candidate output)
- Exit code: **2**
- stdout: exactly one JSON object with:
  - `status = "CANNOT_EVALUATE"`, `revision = "unbound"`, `branch = "master"`, `branch_tip = null`
  - `verdicted_kernel_entries = 0`, `entry_count = 0`
  - `findings` = exactly one entry: `{"id": "E-REVISION-INVALID", "site": "revision", "detail": "<selector as typed> does not name one commit"}`
- Full-SHA semantics: no full SHA of `X`, `B` or any commit may appear as `revision` or `branch_tip`. The selector is echoed only inside `detail`, exactly as typed (not expanded, case preserved). An accept is impossible: neither the exit is ≠ 2 nor `revision` names a 40-hex value.
- The same expectation holds for the full ID and for a unique prefix. It is also independent of origin state, because refusal happens before step 4.

## Git object type invariant (why the oracle needs no binder code)
- An object's type is part of its hashed header (`<type> <len>\0`), so an OID's type cannot change.
- An annotated tag's `object` and `type` header lines fix its target and target type immutably.
- Peeling only follows tag → target. A blob has no outgoing links.
- Therefore a tag whose `type` is `blob` can never peel to a commit, in any repository state.

The expected result comes from fixture construction plus contract clause 3 ("uniquely matches an object ID, then peels to a commit else E-REVISION-INVALID"). It does not come from running `_object_commit` or the judge's `object_commit` copy, which is algorithmically the same (lines 139–166).

Permitted oracle precondition (fixture sanity only): `git cat-file -t X == tag` and `git cat-file -p X` header `type blob`. The expected-output table is then a constant: (tag → blob) gives exit 2 / `E-REVISION-INVALID` ×1 / `revision "unbound"`.

## Round20 matrix coverage (A4)
- **Not covered.** `object_selector_probes` (check-revision-binding.py 475–673) only uses tags that point at commits: `annotated_tag_object`, `annotated_tag_prefix`, `full_tag_object_id_ref_shadow`, and ghost annotated tags created on `tip`.
- Its non-commit selector is a **bare** blob: `noncommit_blob`, plus `probe_tool`'s `blob-revision` (449). No tag→blob or tag→tree selector exists in the matrix.
- The consumer's own `binding_cases()` (1324–1393) has no tag or blob selector either.
- Only the binder's own `--selftest` has `annotated-tag-to-blob-invalid` (`_revision.py` 413–419). That is self-grading, not the independent matrix.

## Smallest realistic weakening mutant the round20 matrix misses
In `_object_commit`, peel the tag with `f"{oid}^{{}}"` (peel to any non-tag object) instead of `f"{oid}^{{commit}}"`.
- Every round20 case still passes:
  - Tag → commit peels identically.
  - A bare blob still returns `None` through the `object_kind != "tag"` guard.
  - Ghost and shadow cases never reach the peel.
- TagBlob then returns the blob OID as `sha`. Step 4 passes, and step 5 `merge-base --is-ancestor B refs/heads/master` would exit ≥2 [INFERENCE: git's merge-base dies on a non-commit, conventionally exit 128; not executed].
- The result would be `E-GIT-FAILED`, with site `refs/heads/master`. Exit 2 is unchanged and `revision` is still `"unbound"`.
- So this mutant is caught only by grading the **finding id and site**, not by exit or `revision`. A TagBlob row graded with `exact_refusal(X, E-REVISION-INVALID)` would kill it.
- A sibling mutant that drops the `tag` branch and treats tags as commits (`return oid`) is already killed by `annotated_tag_object`, because `revision` ≠ `tip`.

## Limits / unresolved
- The consumer was read from the moving working tree, not a pinned snapshot. Line numbers are as observed at review time.
- In the judge sandbox, the consumer imports `tools/_revision.py` from the clone checked out at the measured commit. Whether that file's bytes equal the Reviewed-SHA256 snapshot is not verified here (NO-EXEC, no hashing).
- The `E-GIT-FAILED` outcome of the mutant is inference from git behaviour, not observed.
- No non-author closure or promotion is claimed.

Tooling: no installs or updates (none needed; NO-EXEC seat).

Scope: executed=none
