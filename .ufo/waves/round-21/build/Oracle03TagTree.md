# Oracle03 — TagTree object-ID selector × check-section-citations.py (source-only expectation)

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-section-citations.py-TagTree-expected-source-only

Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (SHA256 as supplied; not recomputed — NO-EXEC).
Consumer: `tools/check-section-citations.py` (read-only). Round20 matrix: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.

## Axes
1. Exit class (0/1/2).
2. Finding identity and cardinality (exact id, exactly one binding finding).
3. Full-SHA / `revision` field semantics in the JSON.
4. Round20 matrix coverage of this exact case.
5. Mutant sensitivity (smallest realistic weakening the matrix misses).

## Case definition
TagTree = `--revision <T>` where `T` is the full (40-hex SHA-1, or 64-hex SHA-256) object ID of an annotated tag object whose `object`/`type` header names a tree (e.g. `git mktree` output tagged with `git tag -a`), default `--branch master`, branch present, origin either absent or at tip.

## Observed: consumer propagation
- `check-section-citations.py:36` imports `RevisionError, bind` from `_revision`; no local revision regex or rev-parse in the binding path.
- `main()` `:913` calls `bind(ROOT, args.revision, branch)` with the raw argparse string and `branch = args.branch` (default `master`). No normalization, lowercasing or pre-validation of the selector before `bind`.
- The second `bind(ROOT, BASE, branch)` (`:916`) runs only after the first succeeds, so it is never reached for TagTree.
- `:923-927` catches `RevisionError`, converts it to `Cannot(fid, site, detail)` and emits `Result(CANNOT, [one Finding], 0)` with `revision` = still the raw `args.revision` (reassigned to `.sha` only on success, `:914`) and `branch_tip` = `None` (initialized `:911`, assigned only on success).
- `emit()` `:394-402` prints one JSON object: `status`, `revision`, `branch`, `branch_tip`, `correction_count`, `scope`, `findings` (sorted keys); returns `result.code`.

## Observed: pinned binder path for TagTree (`bind`, `_object_commit`)
1. `validate_branch("master")` passes (regex + `check-ref-format`).
2. `REV.fullmatch(T)` passes (7-64 hex).
3. `rev-parse --disambiguate=<t lower>` lists exactly one object (the tag; a full OID matches only itself).
4. `cat-file -t T` → `tag`, so neither the `commit` return nor the non-tag `None` return fires.
5. `rev-parse --verify --quiet --end-of-options T^{commit}` fails (exit 1, quiet); `rev-parse --git-dir` succeeds → `return None`.
6. `bind` raises `RevisionError(E-REVISION-INVALID, "revision", f"{T} does not name one commit")`. Branch-existence, ancestry (`merge-base`) and origin checks are never reached.

## Expected (stated before candidate outputs exist)
- Exit: `2` (CANNOT).
- stdout JSON: `status == "CANNOT_EVALUATE"`; `findings` has exactly one element `{"id": "E-REVISION-INVALID", "site": "revision", "detail": "<T verbatim> does not name one commit"}`; no other `E-*` binding id anywhere in the findings list; `correction_count == 0`; `branch == "master"`; `branch_tip == null`.
- Full-SHA semantics: `revision` is an echo of the selector exactly as typed (case preserved, not lowercased, not peeled). It is the tag OID, never a commit OID, and it MUST NOT be read as an accepted binding. No commit SHA appears anywhere in the output. Uppercase `T` gives the same id/exit; only the echoed `revision`/`detail` text keeps the caller's case.
- The same expectation holds for any unique 7+ hex prefix of `T` (the echo is then the prefix). An ambiguous prefix also yields E-REVISION-INVALID, but for a different reason (count ≠ 1), so it is not this case.
- Outcome is independent of refs: a branch or tag named `T`, or an origin ref, cannot change it, because the object-ID path is taken first and returns `None` before any ref is consulted.

## Git object-type invariant (why the oracle needs no binder code)
An object's ID is the hash of `"<type> <size>\0<body>"`, so its type is fixed by its ID and cannot change. An annotated tag's body records its target's ID and `type`, and those are covered by the tag's own hash. Peeling (`^{commit}` / `^{}`) follows tag→target links until it reaches a non-tag object. For a tag chain ending in a tree, that object is a tree forever. Trees have no parents and are never commit-ish, so no ref state, ancestry or origin configuration can ever make T name a commit.

An independent oracle can therefore compute the expectation from plain Git facts, without importing `_revision`:
- `cat-file -t T` must equal `tag`.
- The peeled target's type (`cat-file -t T^{}`, or the `type` header from `cat-file -p T`) must equal `tree`.
- `rev-parse --verify --quiet T^{commit}` must exit non-zero.
- Expected result: exit 2, single E-REVISION-INVALID, echoed `revision`.

This oracle should not reproduce `_object_commit`'s enumerate/type/peel sequence. It only has to state the type facts and the contract row "uniquely matches an object ID, then peels to a commit, else E-REVISION-INVALID" (`_revision.py` docstring, check 3).

## Round20 matrix coverage (pinned check-revision-binding.py)
**Not covered.** The matrix runs `object_selector_probes` (`:475-673`, only with `--object-selectors` and only for the original-nine `TOOLS`, which include this consumer) and `probe_tool` (`:416-472`). Together they contain:
- `annotated_tag_object` and `annotated_tag_prefix`: tag→commit, accept only.
- Ghost hex branch/tag cases (12-hex and 40-hex, lightweight and annotated): no object with that ID exists.
- Ref shadows.
- Direct blob: `noncommit_blob` and `blob-revision`.
- Unlanded/unpushed cases.

There is no direct-tree selector, no tag→tree selector, no tag→blob selector and no nested tag→non-commit selector. The only non-commit object the judge creates is `blob_object()` (`:408`); `grep tree` in the judge hits only `ls-tree`/AST uses. In the real matrix run, every tag that exists peels successfully, so the consumer path through `_object_commit`'s tag-peel-failure branch (`_revision.py:139-146`) is never executed. The binder's own selftest has `annotated-tag-to-tree-invalid` (`:412-418`), but that tests `bind()` directly, not this consumer. The consumer's `--selftest` has no tag or tree vector either (its binding probes are at `:802-879`).

## Smallest realistic weakening mutant the round20 matrix misses
In the pinned binder `_object_commit`, collapse the tag-peel failure handling (`:141-146`) into an unconditional git failure:

```python
if peel.returncode == 0:
    return peel.stdout.decode("ascii", "replace").strip()
raise RevisionError(E_GIT, oid, "tag peel failed")
```

This is a one-hunk edit that drops the `--git-dir` repository-availability distinction.
- With the mutant, TagTree gives exit 2 with E-GIT-FAILED instead of E-REVISION-INVALID. That violates the contract's "non-commit = INVALID, git failure only for real git failures".
- Every round20 case still passes: all its tags peel to commits, the blob cases exit at `object_kind != "tag"`, and ghosts exit at the disambiguate count.
- An equally invisible variant on the same branch is `return oid` instead of `None` (the tag OID goes on to `merge-base`). [INFERENCE] `merge-base --is-ancestor` then fails on a non-commit with an rc ≥ 2, which `_ancestor` maps to E-GIT-FAILED, again exit 2 with the wrong id.

A mutant that would make TagTree *accepted* (exit 0 or 1) is not realistic. It would need the binder to return some commit unrelated to T, because every ancestry check rejects a tree. So the realistic gap is the finding id, not acceptance. The matrix's `exact_refusal` grading (exit == 2, finding == expected, `binding_ids == [expected]`, `finding_count == 1`) would detect both mutants if a TagTree case were added.

## Inference / limits
- [INFERENCE] The exact `merge-base` rc for a tree argument was not observed (NO-EXEC). The primary mutant above does not depend on it.
- The consumer imports `tools/_revision.py` next to its own file. In a matrix run, that is the copy at the measured tools revision, not this snapshot. The working-tree copy contains the same tag/peel branch text (`tools/_revision.py:115,136,417`), but byte identity with the pinned SHA256 was not checked (no hashing under NO-EXEC).
- Scope is this one consumer and type pair. No other consumer or object type was assessed. No non-author closure or promotion is claimed.

Lane bounds: leaf member — no subagent dispatch.
Tooling: no installs or updates (none needed; NO-EXEC seat).
Scope: executed=none
