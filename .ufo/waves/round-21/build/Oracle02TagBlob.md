# Oracle02TagBlob — check-root-dac-correction.py × annotated-tag→blob object ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-root-dac-correction.py-TagBlob-expected-source-only
Lane bounds: leaf member — no subagent dispatch.

Axes: (A) expected exit/finding/field semantics, derived from the spec and Git invariants; (B) consumer bind propagation; (C) round-20 matrix coverage; (D) a weakening mutant the matrix misses.
Reviewed bytes: `.ufo/waves/round-21/snapshot/tools/_revision.py` (SHA as above, supplied by item, not recomputed — NO-EXEC). Also read: snapshot `tools/check-revision-binding.py` and the live `tools/check-root-dac-correction.py`. The snapshot has no pinned copy of this consumer, so the consumer read is of a moving file and is unhashed (limit).

## Case definition
TagBlob = the object ID of an annotated tag object whose `object`/`type` header names a blob. Example: `git hash-object -w` followed by `git tag -a <name> <blob>`; the selector is `refs/tags/<name>^{tag}`. The selector is used as a hex object ID, either the full 40 hex or a unique prefix of at least 7 hex with no colliding ref name. It is not used as a tag name.

## Git object type invariant (oracle basis, not binder code)
- Git has exactly four object types: commit, tree, blob, tag. An annotated tag records exactly one target and its type. Peeling follows tag→target until it reaches a non-tag object.
- A tag→blob chain therefore ends at a blob. `<oid>^{commit}` has no answer for it: rev-parse fails, no commit exists anywhere on the chain.
- The tag OID, the blob OID and every commit OID are distinct objects. Ancestry (`merge-base --is-ancestor`) is defined only between commits.
- So no ref state can make this selector "one commit", "landed" or "pushed". This follows from the type system alone.
- The oracle should derive the expected result from the binder contract table, step 3 ("revision uniquely matches an object ID, then peels to a commit, else E-REVISION-INVALID"), applied to that invariant.
- The fixture should be checked with plain Git, not with the code under test:
  - `cat-file -t <sel>` must print `tag`.
  - The `type` line of `cat-file -p <sel>` must say `blob`.
- The oracle must not call `_revision._object_commit` or `_revision.bind`.
- It must also not call the judge's `object_commit` (lines 139–166). Although labelled "independent", that function mirrors the binder line for line (disambiguate, then `cat-file -t`, then peel `^{commit}`), so using it would import the same algorithm under another name.

## Consumer propagation (observed, `tools/check-root-dac-correction.py`)
- `main` passes `args.revision` and `args.branch` unmodified to `run_gate(ROOT, ...)` (lines 543–545). `ROOT` is the parent of the script's directory, so a sandbox copy binds against the sandbox.
- `run_gate` calls `_revision.bind(repo, revision, branch)` (line 275). On `RevisionError` it:
  - sets `tip = _revision.branch_tip(repo, branch)`;
  - re-raises the error as `Cannot(exc.fid, exc.site, exc.detail)`;
  - returns `Result(CANNOT, [that one finding], 0)` with `label` still equal to the raw selector, because `label` is reassigned only on success (line 279).
- `read_git` is never reached, so no documents are read.
- The consumer imports the sibling file `tools/_revision.py` (lines 27–29). At runtime it uses whatever binder sits beside it at the measured revision, not this snapshot. Equivalence between the two is [INFERENCE] and not verified here.

## Expected behavior (stated before any candidate output)
For `--revision <TagBlob OID>` with a valid, existing `--branch master`:
- **Exit code:** 2.
- **Output:** exactly one JSON object on stdout, with these fields:
  - `status`: `"CANNOT_EVALUATE"`.
  - `findings`: exactly `[{"id":"E-REVISION-INVALID","site":"revision","detail":"<selector> does not name one commit"}]`. That is one finding, and its id is one of the binding ids.
  - `revision`: the selector string echoed verbatim (full 40 hex or prefix, original case). It is NOT the tag's peeled target, the blob OID, a lowercased form, or any commit SHA. An echo is not acceptance; the judge's `exact_refusal` comment says the same.
  - `branch`: `"master"`.
  - `branch_tip`: the full 40-hex OID of `refs/heads/master`, informational only.
  - `correction_count`: 0.
  - `scope`: `"narrow-conformance-not-semantic-proof"`.
- **Precedence variants (contract order):**
  - With `--branch a..b`, the result is E-BRANCH-INVALID with `branch_tip` null.
  - With `--branch nosuch`, it stays E-REVISION-INVALID (step 3 runs before step 4) with `branch_tip` null.
  - With `refs/remotes/origin/master` pointing at a blob, it stays E-REVISION-INVALID, not E-GIT-FAILED, because the failure happens before step 6.
  - An ambiguous prefix is also E-REVISION-INVALID. Use the full OID so the probe isolates type and not ambiguity.
- **Full-SHA semantics:** the pass condition is the exact single id plus the verbatim echo. Any 40-hex commit appearing in `revision`, or any exit other than 2, is a failure.

## Round-20 matrix coverage (pinned `check-revision-binding.py`)
Not covered. The per-tool `object_selector_probes` (lines 475–673) and `probe_tool` (416–472) contain these related cases:
- `annotated_tag_object` and `annotated_tag_prefix`: tag→commit, expected accept.
- `full_tag_object_id_ref_shadow`: tag→commit.
- `ghost_full_hex_annotated_tag`: a tag *name* pointing at a commit.
- `noncommit_blob` and `blob-revision`: a direct blob.
- `git-failed`: origin ref set to a blob.

No case creates an annotated tag whose target is a non-commit. Grep of the snapshot finds only two `tag -a` calls (lines 504 and 566), and both target `tip`. The judge's self-test region was not separately read, but this grep covers the whole file.

The binder's own self-test has `annotated-tag-to-blob-invalid` (`_revision.py` lines 413–419). That tests the binder only, not this consumer's CLI path. The consumer's self-test has no tag or blob revision cases at all.

## Smallest realistic weakening mutant the matrix misses
In `_object_commit`'s tag branch (`_revision.py` lines 139–140), peel with `f"{oid}^{{}}"` instead of `f"{oid}^{{commit}}"`. This is a one-token change that reads as a "generic peel" cleanup.
- **Tag→commit:** `^{}` and `^{commit}` resolve to the same commit, so every round-20 accept case still passes.
- **Direct blob:** the `kind != "tag"` path is unchanged, so it still returns INVALID.
- **TagBlob:** the mutant returns the blob OID as `sha`. `bind` then reaches `_ancestor(blob, refs/heads/master)`. That yields either E-GIT-FAILED (if merge-base exits ≥2 on a non-commit) or E-REVISION-NOT-LANDED (if it exits 1). Either way the id is not E-REVISION-INVALID, and the TagBlob probe catches it. Which of the two git exit paths occurs is [INFERENCE], since nothing was executed.

A coarser variant also survives the matrix: `if object_kind in ("commit", "tag"): return oid` without peeling. It does not survive in general, though: the existing `annotated_tag_object` accept case catches it, because the echoed revision would be the tag OID instead of `tip`.

## Limits and unknowns
- No candidate outputs exist and nothing was run. Every expected value above is derived from the source.
- The consumer bytes are unpinned (no snapshot copy, no SHA).
- Which git exit code the mutant hits is not verified.
- No tools were installed or needed.

Scope: executed=none
