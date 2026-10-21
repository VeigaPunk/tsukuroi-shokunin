# Oracle04 TagBlob — check-source-scope-correction.py × annotated-tag→blob object-ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-source-scope-correction.py-TagBlob-expected-source-only

Lane bounds: leaf member — no subagent dispatch.

Axes: (A1) expected exit, (A2) finding id/count/site, (A3) the JSON `revision`/full-SHA semantics, (A4) whether the round-20 judge matrix covers this case, (A5) the smallest weakening mutant the judge would miss.

## Observations (from source, read-only)

Pinned binder `.ufo/waves/round-21/snapshot/tools/_revision.py`:
- `bind()` runs these steps in order: `validate_branch`, then the `REV` 7-64 hex check, then `_object_commit`. If `_object_commit` returns `None`, it raises `RevisionError(E-REVISION-INVALID, "revision", f"{revision} does not name one commit")` (L172-179). That happens before the branch-tip, landed, and pushed checks.
- `_object_commit` (L112-146): runs `rev-parse --disambiguate=<lower>`; a non-zero rc gives E-GIT-FAILED, and anything other than exactly one object gives None. It then runs `cat-file -t`. `commit` returns the OID, any other non-`tag` type returns None, and `tag` is peeled with `rev-parse --verify --quiet --end-of-options <oid>^{commit}`. A failed peel in a readable repository returns None. Only an unreadable repository raises E-GIT-FAILED.
- The binder's own selftest has `annotated-tag-to-blob-invalid`, which expects E-REVISION-INVALID (L413-419). That is the graded code testing itself, not an independent oracle.

Consumer `tools/check-source-scope-correction.py`:
- `import _revision` at L15. The tool resolves the copy next to the script, so in the judge sandbox that is `sandbox/tools/_revision.py` at the measured revision.
- `main()` L636-642: sets `revision = args.revision` (echo, unmodified), then calls `_revision.bind(ROOT, args.revision, branch)`. The selector and `--branch` (default `master`) are passed through unchanged, with no lowercasing, stripping or re-resolution. `ROOT` is the script's repo, which is the sandbox clone.
- A `RevisionError` is converted 1:1 to `Cannot(exc.fid, exc.site, exc.detail)`. `emit()` then outputs `Result(CANNOT, [that one finding], 0)`, together with `revision` (still the echoed selector), `branch`, and `branch_tip=None`, because `branch_tip` is only assigned after a successful bind. No `read_git` happens and `evaluate` is not reached.
- `emit()` prints one sorted-keys JSON line, maps `CANNOT` to `"CANNOT_EVALUATE"`, and returns code 2.
- The consumer's own selftest (`binding_cases`, L462-521) has no tag→blob probe, and no blob probe at all.

## Expected behaviour (fixed before any candidate output exists)

The fixture is a sandbox with `refs/heads/master` = landed tip, plus a blob `B` (from `hash-object -w`) and an annotated tag object `T` whose target is `B`. The selector is either the full 40-hex `T` or a unique ≥7-hex prefix of `T` that has no colliding ref. The default branch is used, and the origin ref may or may not be present.

- Exit code: `2`.
- stdout is exactly one JSON object with:
  - `status == "CANNOT_EVALUATE"`
  - `correction_count == 0`
  - `findings` of length exactly 1, with `id == "E-REVISION-INVALID"` and `site == "revision"`. The `detail` is `"<selector> does not name one commit"`; treat it as informational, not graded.
  - `branch == "master"`
  - `branch_tip == null`
- Full-SHA semantics: `revision` echoes the selector exactly as given. That is the tag OID or its prefix, which is never a commit. It must not be read as an accepted binding.
  - It must not equal the landed tip, the blob OID `B`, or any other commit SHA, unless the selector was itself that string.
  - No commit is bound and no file is read at any revision.
- The finding order makes this result independent of landed or pushed state. Changing the origin ref to lag or to be absent must not change the id to E-REVISION-NOT-PUSHED, E-REVISION-NOT-LANDED or E-BRANCH-MISSING.
- A nested chain (tag→tag→blob) has the same expected result.

### Git object-type invariant (why the expectation needs no binder logic)

- An object ID is the hash of `<type> <len>\0<content>`, so an object's type cannot change for a given ID.
- An annotated tag's header (`object <oid>` / `type <t>`) points at one immutable target.
- Peeling follows tag→target until it reaches a non-tag object. Here that terminal object is the blob `B`.
- A blob has no outgoing references, so no chain starting at `T` can ever reach a commit.

So "T does not name a commit" is fixed by how the fixture is built. The oracle derives it from fixture facts: it created `B` with `hash-object`, `cat-file -t T` reads `tag`, and the tag header reads `type blob`. It does not reimplement `_object_commit`, and it does not import `_revision` or the judge's mirrored `object_commit`. The expected tuple is a constant.

## Round-20 matrix coverage (pinned `check-revision-binding.py`)

The matrix does **not** cover this case. What the probes do cover:
- `probe_tool` has `blob-revision`, which is a bare blob (L448-449). It also has `git-failed`, an origin ref pointing at a blob.
- `object_selector_probes` (L475-673) has:
  - `noncommit_blob`: a bare blob.
  - `annotated_tag_object` and `annotated_tag_prefix`: tag→commit, accepted.
  - `full_tag_object_id_ref_shadow`: tag→commit.
  - Ghost lightweight and annotated tags: ref-name selectors, not tag-object IDs.

No case builds an annotated tag whose target is a blob (or a tree). The tag→blob refusal path is exercised only by the binder's own selftest.

## Smallest realistic weakening mutant the judge misses

In `_object_commit`, change the peel target from `f"{oid}^{{commit}}"` to `f"{oid}^{{}}"`, i.e. "peel to the first non-tag object".

What the judge's existing cases still see under this mutant:
- tag→commit still returns the commit, so `annotated_tag_object`, `annotated_tag_prefix`, `full_tag_object_id_ref_shadow` and the nested tag case still pass.
- A bare blob is still rejected at the `cat-file -t` check, so `noncommit_blob` and `blob-revision` still pass.

What changes for tag→blob: the mutant returns `B` as `sha`, and `bind` goes on to `_ancestor(repo, B, refs/heads/master)`. [INFERENCE] `merge-base --is-ancestor` with a non-commit argument exits ≥2, so the result becomes E-GIT-FAILED. This is analogous to the observed origin-blob case, which the selftest expects to be E_GIT. Exit stays 2, but the finding id is wrong. If a git version instead returned rc 1, it would be E-REVISION-NOT-LANDED, which is also wrong.

Only a tag→blob selector graded on the exact single id E-REVISION-INVALID catches this mutant. A cheaper variant, `if object_kind != "tag": return oid` for any non-commit, is already caught by `noncommit_blob`, so it is not the smallest mutant the judge misses.

## Limits / unknowns

- I did not compute or verify SHA-256 (no exec). The Reviewed-SHA256 line is the value supplied by the assignment for the baseline/snapshot binder.
- I did not check whether the live `tools/_revision.py` is byte-identical to the snapshot.
- The exact git exit code for `merge-base --is-ancestor <blob> <ref>` is unobserved [INFERENCE].
- No LSP was used. Bind call and argument propagation were confirmed by direct source reading of both files, not by semantic reference queries.
- Tooling: no install or update was performed or needed.

Scope: executed=none
