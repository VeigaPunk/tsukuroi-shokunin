# Oracle09TagTree — check-seat-scope.py × annotated-tag→tree object selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-seat-scope.py-TagTree-expected-source-only

Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (baseline source `tools/_revision.py`).
Consumer, read-only: `tools/check-seat-scope.py`. Round20 matrix: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.
I did not recompute the SHA-256 because this seat is NO-EXEC. The Reviewed-SHA256 line above is the one the item supplied.

## Axes
- A1, the consumer calls the binder: the consumer delegates to the shared `bind` and doesn't resolve anything itself.
- A2, the expected exit code, finding and echo for TagTree.
- A3, what a full SHA means in this case: which SHA may show up and which must not.
- A4, whether the round20 matrix covers TagTree.
- A5, the smallest realistic weakening mutant that the matrix would miss.

## A1: how the consumer calls the binder (observed)
- `check-seat-scope.py:36` runs `from _revision import RevisionError, bind as bind_revision`. This is the sibling `tools/_revision.py`, which `sys.path[0]` resolves to the script's directory. Inside the judge sandbox, `materialize` copies it from the measured commit.
- In `main` (`:651-661`), `revision_in = args.revision` is passed through unchanged: no lowercasing, stripping or ref resolution. `branch` comes from `--branch` (default `master`). Then `collect(wave, revision_in, branch)` runs.
- In `collect` (`:260-264`), `bind_revision(ROOT, revision, branch)` runs. A `RevisionError` is turned into `Cannot(exc.fid, exc.site, exc.detail)` with nothing added or dropped. The consumer reads `bound.sha` and `bound.branch_tip` only after a successful bind.
- `wave_key(wave_arg)` (`:658`) runs before the bind. So a test fixture must pass a valid lane-relative wave, which the judge does through `EXTRA` with `--wave .ufo/waves/round-16/build`. Otherwise `E-WAVE-INVALID` fires before the bind and hides it.
- When `Cannot` is raised (`:663-665`), the consumer emits `Result(CANNOT, [one Finding], 0)`. The JSON field `revision` is set to `revision_in`, as typed (`:659-660`). `tip` is still `None`.
- Conclusion: the consumer makes no type decision of its own. The TagTree behaviour comes entirely from the binder's `_object_commit`.

## Git object type invariant (why the expected value is fixed without running the binder's algorithm)
- An object's type is part of the bytes that get hashed (`"<type> <size>\0"`). One object ID therefore has exactly one type, and that type never changes.
- An annotated tag records `object <oid>` and `type <kind>` for its target. Peeling to `^{commit}` follows tag→target links until it reaches something that isn't a tag. If the tag targets a tree, peeling stops at the tree. A tree only ever points to trees and blobs (gitlink entries aren't followed by `^{commit}`). So no commit is reachable from a tag-to-tree object, and the selector can never name a commit.
- This follows from the binder's contract row 3 ("uniquely matches an object ID, then peels to a commit", otherwise `E-REVISION-INVALID`) plus the invariant. An oracle needs neither `--disambiguate`, nor `cat-file -t`, nor `_object_commit`. The expected value is fixed when the fixture is built: the author creates a tree with `mktree` and then runs `tag -a <name> <tree>`.
- To build the fixture, record the tag object ID and the tree object ID. You may assert their types, `tag` and `tree`, as a check that the fixture is valid. Never derive the expected output by calling into the binder, or by copying its peel chain into the oracle.

## A2 and A3: expected behaviour, derived from source only, before any candidate output exists
Fixture preconditions:
- `refs/heads/master` exists and is a commit.
- The selector is either the tag object's full 40-hex ID, or a prefix of 7 or more hex that matches only that object among all objects.
- The wave argument is valid, and the branch is `master` or another valid existing branch.
- The origin ref's state doesn't matter, because step 3 fails before steps 4–6 run.

Expected result:
- The exit code is `2` (CANNOT). The steps run in order and step 3 fails first, so you never get `E-BRANCH-MISSING`, `E-REVISION-NOT-LANDED`, `E-REVISION-NOT-PUSHED` or `E-GIT-FAILED`. The binder flow is `_object_commit` → `kind == "tag"` → `rev-parse --verify --quiet <tag>^{commit}` exits non-zero → the repo is readable → `None` → `bind:178-179` raises `E-REVISION-INVALID`.
- stdout is exactly one JSON line with these fields:
  - `status` is `"CANNOT_EVALUATE"`.
  - `findings` is exactly one entry: `{"id":"E-REVISION-INVALID","site":"revision","role":null,"detail":"<selector as typed> does not name one commit"}`.
  - `counts["E-REVISION-INVALID"]` is `1`, and every `SCOPE-*` count is `0`.
  - `seat_count` is `0`, `branch` is the requested branch, `branch_tip` is `null`, and `wave` is the normalized wave key.
- What a full SHA means here: no commit SHA is bound or emitted. `revision` repeats the selector byte-for-byte: a prefix stays a prefix, and uppercase stays uppercase. That echo is not a binding, and the judge's `exact_refusal` deliberately doesn't grade it. These must never appear in `revision`:
  - the tree's object ID
  - the tag object ID lowercased or expanded from a prefix
  - any commit SHA
- Pass predicate: `exit == 2` AND exactly one finding AND `finding.id == "E-REVISION-INVALID"` AND the binding-ID list equals `["E-REVISION-INVALID"]` AND `revision` is neither the tree's ID nor any commit's ID.
- Grading on the exit code alone isn't enough, because the weakening mutant below also exits `2`.

## A4: does the round20 matrix cover this case? No (observed)
- `object_selector_probes` (`check-revision-binding.py:475-673`) builds exactly one annotated tag, and it targets the tip commit (`:502-505`). That tag feeds the following cases, which all expect to be accepted: `annotated_tag_object`, `annotated_tag_prefix` and `full_tag_object_id_ref_shadow`.
- The only non-commit case is `noncommit_blob` (`:633`). It uses a bare blob from `blob_object` (`:408-413`), not a tag.
- `probe_tool`'s `blob-revision` and `git-failed` cases (`:448-452`) also use a bare blob.
- The judge sandbox never creates a tree object. It never tags a tree or a blob. It has no nested tag-to-tag-to-commit chain either.
- The binder's own selftest has `annotated-tag-to-tree-invalid` (`_revision.py:413-418`). That only tests the binder itself, not the consumer as run. The consumer's own selftest (`check-seat-scope.py:518-581`) has no tag or tree cases.
- Conclusion: for `check-seat-scope.py`, TagTree isn't covered by the round20 matrix, by the consumer's own selftest, or by the consumer CLI path.

## A5: the smallest realistic weakening mutant the matrix misses
- Mutant M1 is a one-token change in `_revision.py:140`. Replace `f"{oid}^{{commit}}"` with `f"{oid}^{{}}"`, which peels to any type that isn't a tag.
- For a tag that targets a commit, M1 returns the same commit. So `annotated_tag_object`, `annotated_tag_prefix`, `full_tag_object_id_ref_shadow` and `noncommit_blob` (which never reaches the peel) all still pass, and the round20 matrix stays green.
- For TagTree, M1 returns the tree's ID as `sha`. Then `merge-base --is-ancestor <tree> refs/heads/master` runs.
  - [INFERENCE] Git can't turn a tree into a commit there, so it exits with code 128 or higher, and `_ancestor` raises `E-GIT-FAILED` with site `refs/heads/master`. The exit code is still `2`, so only the finding ID tells M1 apart from the correct binder.
  - [INFERENCE] If some Git version returned 1 instead, M1 would give `E-REVISION-NOT-LANDED`. That is still a wrong ID that the matrix doesn't see.
- Mutant M2 is just as small. Change the peel-failure branch at `:141-146` to raise `E_GIT` whenever `peel.returncode != 0`. It doesn't wait for the repository check to fail.
  - Every tag targeting a commit still peels, so the matrix stays green.
  - TagTree gives `E-GIT-FAILED` with exit `2` instead of `E-REVISION-INVALID`.
- Both mutants are caught only by a TagTree case that checks the exact finding ID, the single finding, and that `revision` is not the tree's ID. Both are also caught by the binder's own selftest at `:417`, but nothing tests that through the consumer.

## Limits
- Nothing was run. The exit code, finding and JSON shape above are derived from source and have not been observed.
- I did not compare the production `tools/_revision.py` with the pinned snapshot byte for byte. Running the consumer uses the production module, or the copy from the measured commit inside the judge. This review stands only if those are identical to the pinned snapshot.
- Only this consumer and this object type were reviewed. No other consumers or types, and no claim of closure by a non-author reviewer or of outside promotion.
- No tools were installed; none were needed.

Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
