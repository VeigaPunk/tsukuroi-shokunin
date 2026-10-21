# Oracle09TagBlob — check-seat-scope.py × annotated-tag-to-blob object-ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-seat-scope.py-TagBlob-expected-source-only
Lane bounds: leaf member — no subagent dispatch.
Report: .ufo/waves/round-21/build/Oracle09TagBlob.md

Axes: (A) expected behaviour derived from source, (B) how the consumer passes the selector to the binder, (C) round20 matrix coverage, (D) the weakening mutant the matrix would miss, (E) the oracle staying independent of the binder.

## Expected result (stated before any candidate output exists)

Case: `check-seat-scope.py --revision <S> --wave <valid lane-relative dir> [--branch master]`. Here `<S>` is either the full 40-hex object ID or a unique 7+ hex prefix of an annotated tag object whose target is a blob. The branch is valid and exists, and the repository is readable.

- Exit code: `2` (CANNOT).
- `status`: `"CANNOT_EVALUATE"`.
- `findings`: exactly one entry, `{"id": "E-REVISION-INVALID", "site": "revision", "role": null, ...}`. The binder's detail text is `"<S> does not name one commit"`. The oracle SHOULD NOT pin that detail text, because it is the binder's own wording.
- `counts`: `E-REVISION-INVALID` = 1, and all four SCOPE-* ids = 0. There is no E-GIT-FAILED, E-REVISION-NOT-LANDED or E-BRANCH-* entry, and no second finding.
- `seat_count` = 0, `branch` = the input branch, `branch_tip` = `null`, `wave` = the normalised wave key.
- Full-SHA semantics: `revision` echoes the input string `<S>` exactly as given (same case, same length). With a full 40-hex selector, the echo is the tag object ID. It is never a commit ID, and it is never the blob's ID. The output never contains a resolved 40-hex commit. A 40-hex `revision` field therefore MUST NOT count as acceptance; only the status and the single finding id do.
- The result is the same for a nested chain (tag → tag → blob), with or without `refs/remotes/origin/<branch>`, and with any branch or tag ref that shadows the hex string.
- Expected precedence (observed in source):
  - An invalid `--wave` gives E-WAVE-INVALID first (`main` line 658 runs before `collect`).
  - A missing `--wave` gives E-CLI.
  - An invalid branch gives E-BRANCH-INVALID first.
  - An unreadable repository gives E-GIT-FAILED.
  - E-REVISION-INVALID always comes before E-BRANCH-MISSING and before any origin or ancestry check, so a non-commit origin ref cannot turn this case into E-GIT-FAILED.

## Observations (source, read-only)

- The consumer imports `from _revision import RevisionError, bind as bind_revision` (`tools/check-seat-scope.py:36`). That resolves to `_revision.py` in the script's own directory.
- `collect()` calls `bind_revision(root, revision, branch)` with the raw `--revision` and `--branch` values (lines 260–264). It maps `RevisionError` one-to-one to `Cannot(exc.fid, exc.site, exc.detail)`, so the finding id and site pass through unchanged.
- `main()` sets `revision = revision_in` before calling `collect` (lines 659–661). When binding fails, `emit` therefore echoes the raw input, `tip` stays `None`, and the code is CANNOT (lines 663–665).
- In the pinned binder, `bind()` runs the REV regex check and then `_object_commit()`:
  - `--disambiguate` must return exactly one object.
  - `cat-file -t` returns `tag`.
  - The peel `rev-parse --verify --quiet <oid>^{commit}` fails, `repo_check` succeeds, so the function returns `None`.
  - `bind()` then raises `E-REVISION-INVALID` at site `revision` (`_revision.py` lines 113–146 and 175–178).
- The binder's own selftest covers `annotated-tag-to-blob-invalid` and `annotated-tag-to-tree-invalid`, but only at the `bind()` level (lines 413–419). The consumer's selftest has no tag or blob case (grep for `blob|tag` returns 0 hits), so the consumer-level CLI output is not exercised for this pair.
- Limit: the consumer at runtime, and the judge's sandbox, import whatever `tools/_revision.py` exists at the measured commit, not this snapshot. Under NO-EXEC I could not confirm that the live copy hashes to 06b71e8c….

## Git object-type invariant (how the oracle stays independent of the binder)

- An object ID is a hash over `"<type> <size>\0<content>"`, so an object's type cannot change once the ID exists.
- An annotated tag's content includes its `object <oid>` and `type <type>` lines. Its target and the target's declared type are therefore fixed by the tag's own ID.
- Peeling (tag → … → first non-tag object) is fully determined by the object graph. Refs cannot change it.
- A blob has no commit to peel to. "Tag → blob is not one commit" therefore holds in every repository state.
- The oracle should get its ground truth from Git plumbing on the fixture, never from `bind()` or `_object_commit()`:
  - `git cat-file -t <S>` returns `tag`.
  - `git cat-file -t <S>^{}` returns `blob`, or `cat-file -p <S>` shows a `type blob` line.
  - The fixture should check that the selector is unique.
- The expected output is then the fixed literal above. The oracle must not reimplement the disambiguate-and-peel algorithm and compare against it.

## Coverage in the round20 matrix (pinned `check-revision-binding.py`)

**The matrix does not cover this case.** Its object-ID probes, `probe_tool` and `object_selector_probes`, include:

- a bare blob: `blob-revision` and `noncommit_blob`, both through `cat-file -t` returning `blob` and an early `None`;
- tag → commit: `annotated_tag_object`, `annotated_tag_prefix`, and `full_tag_object_id_ref_shadow`;
- a ghost annotated tag that points at the tip commit;
- an origin ref that names a blob (`git-failed`), which tests ancestry, not the selector.

No probe creates a tag whose target is a blob or a tree. Grep for `mktree|tree|tag.?to` in the judge finds only `ls-tree` and AST `tree` names. The judge's independent `object_commit` handles the case correctly (lines 139–166), but nothing calls it on this input.

## Smallest realistic weakening mutant the matrix misses

- **The mutant:** in `_revision._object_commit`, change the tag peel from `f"{oid}^{{commit}}"` to `f"{oid}^{{}}"`, a one-token edit that means "peel to the first non-tag object".
- **Why the matrix misses it:**
  - For tag → commit, `^{}` and `^{commit}` give the same commit, so every annotated-tag probe still passes.
  - Bare blobs return before reaching the peel, so `blob-revision` and `noncommit_blob` are unchanged.
  - The mutant is in the shared binder, so all nine consumers change together. Both `consistent_tools` and `object_selector_tools` would stay 9/9.
- **What changes for this pair [INFERENCE, not executed]:**
  - The peel returns the blob ID with exit code 0, so `bind` continues to `_commit(refs/heads/master)`, which succeeds.
  - `merge-base --is-ancestor <blob> refs/heads/master` then fails with an exit code of 2 or more (expected 128, "not a commit").
  - The binder raises E-GIT-FAILED at site `refs/heads/master`, not E-REVISION-INVALID at site `revision`.
- **Consequence:** the exit code stays 2 and there is still exactly one finding. An oracle that checks only the exit code, or only "a refusal happened", also misses the mutant. An oracle that checks the exact finding id (and site) catches it.
- **Related variant:** parsing the tag's `object` line and trusting it without checking its type has the same signature.
- **Not a concern:** a mutant that returns the unpeeled tag ID is already caught, because `annotated_tag_object` checks that the `revision` field equals the tip.

## Remaining unknowns

- The exact Git exit codes for `rev-parse --verify --quiet <tag-to-blob>^{commit}` (1 or 128) and for `merge-base --is-ancestor <blob> …` were not observed. The pinned binder returns `INVALID` for either peel exit code (the `repo_check` branch). The mutant's E-GIT-FAILED outcome is inferred.
- Whether the live `tools/_revision.py` matches the snapshot hash is unverified.
- Tools installed or updated: none.

Scope: executed=none
