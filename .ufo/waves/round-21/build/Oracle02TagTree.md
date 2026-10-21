# Oracle02TagTree — check-root-dac-correction.py × annotated-tag→tree object-ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-root-dac-correction.py-TagTree-expected-source-only
Lane bounds: leaf member — no subagent dispatch.

Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (SHA256 as supplied in the item; not recomputed — NO-EXEC).
Consumer read: `tools/check-root-dac-correction.py` (live file, read-only; no pinned snapshot copy exists under `.ufo/waves/round-21/snapshot/`).
Judge read: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.

## Axes
1. Expected exit class. 2. Expected finding set (id, count, site). 3. Full-SHA / `revision` field semantics. 4. Round-20 matrix coverage. 5. Surviving weakening mutant.

## Selector under test
`T` = object ID (full 40-hex, or any unique ≥7-hex prefix, any case) of an annotated tag object created by `git tag -a <name> -m … <tree-oid>`; tag ref name is not hex-colliding. Branch `master` exists and is valid; origin ref state irrelevant (binding fails before step 4).

## Git object type invariant (why the expectation needs no binder code)
Git has exactly four object types (blob, tree, commit, tag), and an OID's type is fixed by its content hash. A tag object names one target object plus its type; peeling follows tag→tag chains until a non-tag. A tree only references blobs, trees and (gitlink) commit IDs, and peeling never follows tree entries; commits point to trees, never the reverse. Hence a tag whose terminal target is a tree is not commit-ish: `T^{commit}` can never resolve, in any repository state. The expected outcome is therefore fixed by how the fixture was constructed (it knows it tagged a tree), not by running any selector algorithm. An oracle should hard-code `E-REVISION-INVALID` from that construction fact. It must not call the judge's `object_commit()` (judge lines 139–166), which is a line-for-line mirror of the binder's `_object_commit()` and would share any defect.

## Source trace (observations)
- Consumer: `main()` → `run_gate(ROOT, args.revision, args.branch)` (line 544); `--branch` default `master` (539). `run_gate` passes `revision` and `branch` unchanged to `_revision.bind(repo, revision, branch)` (275); `_revision` is imported from the consumer's own `tools/` directory (27–29). On `RevisionError` it sets `tip = _revision.branch_tip(repo, branch)` and re-raises the binder's `fid/site/detail` verbatim as `Cannot` (276–278), returning `Result(CANNOT, [one Finding], 0)` with `label` still equal to the raw input (268, 282). `read_git`/`evaluate` are not reached, so no R12/R13 doc findings can appear. `emit` prints one JSON object and returns `result.code` (231–233).
- Binder `bind` (pinned 172–192): branch valid → `REV` 7–64 hex passes → `_object_commit`. `rev-parse --disambiguate=<lower>` returns exactly one line (the tag OID) → `cat-file -t` = `tag` → `rev-parse --verify --quiet --end-of-options <oid>^{commit}` is nonzero → `rev-parse --git-dir` succeeds → `None` (113–146) → `RevisionError(E-REVISION-INVALID, "revision", "<T> does not name one commit")` (177–178). The result does not depend on the exact peel exit code (1 or 128), because any nonzero exit in a readable repository yields `None`.

## Expected behavior (stated before any candidate output)
- Exit: **2**.
- stdout JSON: `status` `"CANNOT_EVALUATE"`; `findings` is exactly one entry, `{"id":"E-REVISION-INVALID","site":"revision","detail":"<T as typed> does not name one commit"}`; `correction_count` `0`; `branch` `"master"`; `scope` `"narrow-conformance-not-semantic-proof"`.
- Full-SHA semantics: `revision` echoes the caller's selector verbatim (case and length preserved; a prefix stays a prefix). It is never the tree OID, never a peeled commit, and never lowercased. This echo is not an accepted binding (the judge comment at lines 482–483 agrees). `branch_tip` is the full 40-hex commit at `refs/heads/master`, from `branch_tip()`.
- The same outcome holds for a unique prefix or uppercase form of `T`, and for a branch or tag ref named like `T` pointing at a landed commit: the object lookup comes first, and refs are never consulted for a hex selector.

## Round-20 matrix coverage (pinned judge)
**Not covered.** `probe_tool` covers only a bare blob (`blob-revision`, line 449). `object_selector_probes` covers tag→commit (`annotated_tag_object`/`annotated_tag_prefix`, 631–632), a bare blob (`noncommit_blob`, 633), ghost-hex refs, ref shadows, and unlanded/unpushed commits. Grep finds no `tree`, `mktree`, `^{tree}` or `nested` cases. No path tags a tree, so no round-20 case reaches the peel-failure branch of `_object_commit`. The consumer's own selftest `binding_cases` (416–450) has no tag→tree case either. Only the binder's author-side selftest has one (`annotated-tag-to-tree-invalid`, pinned 413–418), and that is not the independent judge.

## Smallest realistic weakening mutant the round-20 matrix misses
In the pinned binder's tag branch (line 140), change `f"{oid}^{{commit}}"` to `f"{oid}^{{}}"`, a "peel the tag" simplification.
- Tag→commit still peels to the commit, so `annotated_tag_object` and `annotated_tag_prefix` pass. Blob and ghost cases never reach this line. **All round-20 cases still pass.**
- TagTree: the peel succeeds and returns the tree OID, which `bind` treats as `sha`. `merge-base --is-ancestor <tree> refs/heads/master` then fails with exit ≥ 2, giving `E-GIT-FAILED` instead of `E-REVISION-INVALID` [INFERENCE: merge-base refuses non-commit-ish arguments; not executed]. The exit code stays **2**, so an oracle that grades only exit or status cannot detect the mutant. It must grade the exact finding id and `finding_count == 1`.
- A stronger mutant the matrix also misses: on peel failure, fall back to `_commit(repo, revision)`, i.e. re-parse the selector as a ref. With a unique prefix of `T` and a same-named branch at a landed commit, this accepts a decoy commit (exit 0 or 1, `revision` = decoy SHA). The round-20 ref-shadow cases only use commit and tag→commit prefixes, which never reach the fallback.

## Limits / unresolved
- I did not recompute the SHA256 of the pinned binder or the consumer (NO-EXEC). At runtime the consumer imports the `_revision.py` sitting next to it (live `tools/` or the judge's clone at the measured commit), not the snapshot. The expectation above holds only if that file is byte-identical to the reviewed snapshot.
- The `E-GIT-FAILED` effect of the `^{}` mutant is inferred from Git semantics; it was not observed.
- No LSP was used (leaf with read/grep/glob only). Call tracing is a textual read of a single-file consumer.
- No tools installed; none needed.

Scope: executed=none
