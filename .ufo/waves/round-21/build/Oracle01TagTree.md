# Oracle01 TagTree — check-locator-clarification.py × annotated-tag-to-tree object ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-locator-clarification.py-TagTree-expected-source-only
Lane bounds: leaf member — no subagent dispatch.

Scope of this row: one consumer (`tools/check-locator-clarification.py`, original-nine) and one selector type (TagTree: a 7–64-hex selector, full or unique prefix, naming an annotated tag object whose peel chain ends in a tree). Nothing else is covered.

## Axes
- A1 binder semantics: what the pinned `snapshot/tools/_revision.py` `bind()` does for this selector.
- A2 consumer propagation: whether the consumer passes the selector through unchanged and reports the binder's refusal unchanged.
- A3 expected observable: exit code, findings, and JSON `revision`/`branch_tip` (including what a full SHA means here).
- A4 judge coverage: whether the old round-20 matrix in the pinned `snapshot/tools/check-revision-binding.py` tests this case.
- A5 mutation gap: the smallest realistic weakening the A4 matrix would miss.

## Observations (source, read-only)
- O1 `_revision.py` contract, step 3 (docstring lines 16–17): the revision must match exactly one object ID and then peel to a commit, else `E-REVISION-INVALID`; checks run in order and the first failure wins; every failure is one `RevisionError` with exit class 2.
- O2 `bind()` (lines 172–192): `validate_branch` runs first, then the `REV` regex `^[0-9a-fA-F]{7,64}$`, then `_object_commit`. If that returns `None`, it raises `RevisionError(E_INVALID, "revision", f"{revision} does not name one commit")`. This happens before the branch-existence check, landing check and origin check.
- O3 `_object_commit` (lines 112–146) does the following, in order:
  - runs `rev-parse --disambiguate=<lower>`, which needs exactly one object;
  - runs `cat-file -t`: a `commit` is returned, and any other non-`tag` type returns `None`;
  - for a `tag`, runs `rev-parse --verify --quiet --end-of-options <oid>^{commit}`, which returns the peeled SHA on rc 0;
  - if that peel fails and `rev-parse --git-dir` succeeds, it returns `None` (lines 143–145);
  - only an unreadable repository becomes `E-GIT-FAILED`.
  The TagTree selector reaches lines 139–145 and returns `None` there.
- O4 The module's own selftest has `annotated-tag-to-tree-invalid` (lines 413–418, using `git mktree` and `tag -a`), which expects `E_INVALID`. That selftest belongs to the code being graded, not to the independent judge, and it never runs a consumer.
- O5 Consumer `main()` (lines 780–790): `_revision.bind(ROOT, args.revision, branch)` receives the raw argparse string (no lowercasing or stripping) and `ROOT = Path(__file__).resolve().parents[1]`. On a `RevisionError` it does three things:
  - sets `tip = _revision.branch_tip(ROOT, branch)`;
  - sets `revision = args.revision`;
  - raises `Cannot(exc.fid, exc.site, exc.detail)`.
  `emit(Result(CANNOT, [Finding(...)], 0), revision, branch, tip)` then prints the payload and returns code 2. `read_git`/`evaluate` are never reached.
- O6 `payload()` (lines 427–431) prints `status`, `revision`, `branch`, `branch_tip`, `correction_count` and `findings[{id, site, detail}]` as JSON with sorted keys.
- O7 The consumer's own `binding_cases()` (lines 573–647) has no tag, tree or object-selector cases (grep for `tag|tree|mktree` found none in the binding block).
- O8 The pinned judge's `object_selector_probes` (lines 475–673) creates only an annotated tag pointing to a **commit** (`tag -a … tip`, lines 502–505). Its object cases are:
  - `annotated_tag_object` and `annotated_tag_prefix`, both accepted, and `full_tag_object_id_ref_shadow`;
  - `noncommit_blob` (a raw blob);
  - the ghost and shadow ref cases.
  `probe_tool` adds `blob-revision` and the origin-blob `git-failed` case. Grep for `tree|mktree` in the judge finds only `ls-tree` and `ast` uses. There is no tag→tree, tag→blob or raw tree case.

## Expected behavior (stated before any candidate output exists)
The fixture is in the sandbox clone used for the consumer's `ROOT`:
- `refs/heads/master` is a valid commit; the origin ref may be present or absent;
- `T = git mktree` (any tree);
- `G = git tag -a <name> -m … T`;
- the selector is `G` (full 40/64-hex), or a prefix of it with 7 or more hex characters that matches only one object. Upper or lower case is fine.

Run: `check-locator-clarification.py --revision <selector>` with the default `--branch master`.
- **Exit: 2.**
- **stdout:** one JSON object, with:
  - `status: "CANNOT_EVALUATE"`;
  - `correction_count: 0`;
  - `findings` of length exactly 1: `{id: "E-REVISION-INVALID", site: "revision", detail: "<selector> does not name one commit"}`.
- **No other binding finding id:** there must be no `E-GIT-FAILED`, `E-BRANCH-MISSING`, `E-REVISION-NOT-LANDED` or `E-REVISION-NOT-PUSHED`.
- **What the full SHAs mean:**
  - `revision` echoes the selector **byte-for-byte as supplied** (a prefix stays a prefix; case is kept). It is not a full SHA and is not a binding. It must not be the expanded tag OID, the tree OID `T`, or any commit SHA.
  - `branch_tip` is the full lowercase hex SHA of the commit at `refs/heads/master`, from `branch_tip()`. It is informational only.
  - A full-length tag OID and a unique prefix must give identical output except for the echoed `revision`.
- **Precedence still holds:**
  - with `--branch nosuch`, the result is still `E-REVISION-INVALID`, because step 3 comes before step 4;
  - an origin ref that lags `master` or names a blob does not change the result, because steps 5–6 and the `_ancestor` calls are never reached;
  - with an invalid branch (for example `a..b`), the result is `E-BRANCH-INVALID`, because step 1 comes first.
- **Nested tags:** tag→tag→tree gives the same expectation, because peeling follows the tag chain to a non-commit.

## Oracle derivation without the binder algorithm
The expected values should come from two independent sources:
- the contract table (the constant string `E-REVISION-INVALID` and exit class 2);
- facts about the fixture taken from plain Git plumbing: `git cat-file -t G` = `tag`, and `git cat-file tag G` has a header `type tree`, or the last element of a nested chain has `type tree`.

The oracle must not import `_revision`, call `_object_commit`, or reuse the peel code path.

**Git object type invariant:** Git has four object kinds: blob, tree, commit and tag.
- An annotated tag records exactly one target object and its type.
- `^{commit}` peels only through tag objects. It never goes down into tree entries; a gitlink (mode 160000) entry is an OID reference and not a commit ancestry edge.
- So a tag whose chain ends at a tree is not commit-ish, and no peel or ref-lookup procedure can correctly turn it into a commit.
- Object IDs are content hashes, so `G ≠ T`, and prefix uniqueness is counted over all object kinds.

The expected result is therefore a property of the object graph, not of how the binder is written.

## Coverage verdict for the old round-20 matrix
**Not covered.** The pinned judge exercises a tag→commit selector (successful peel) and a raw blob selector. The raw blob takes the `object_kind != "tag"` branch, which returns `None` at line 136–137. No consumer probe reaches `_object_commit` lines 139–145 (the branch where a tag fails to peel and the repository is still readable). This consumer's own selftest has no tag or tree case either. The only tag→tree check is the graded module's own selftest (O4), and that is not independent and is not consumer-level.

## Smallest realistic weakening mutant the matrix would miss
**M1:** in the tag branch of `_object_commit`, delete the `repo_check` guard so that every failed peel raises:

```python
peel = _git(...f"{oid}^{{commit}}")
if peel.returncode == 0:
    return ...
raise RevisionError(E_GIT, oid, "repository unavailable: ...")
```

This is a two-line deletion; the refusal class drops from "invalid selector" to "git failed". With M1, a TagTree selector gives exit 2 with `E-GIT-FAILED` instead of `E-REVISION-INVALID`. Every round-20 case keeps the same result:
- the tag→commit cases still peel;
- the blob case takes the non-tag branch;
- `git-failed` still expects `E-GIT-FAILED`.

The exit code is unchanged at 2, so only an exact single-finding-id check on a TagTree probe can detect it.

**M2 (a close sibling, also missed):** change the peel target from `^{commit}` to `^{}`, which peels to any non-tag object. The tag→commit cases are unchanged. A TagTree selector then returns the tree OID as the "commit". [INFERENCE: not executed] `merge-base --is-ancestor <tree> refs/heads/master` then exits ≥2, which gives `E-GIT-FAILED`, again with exit 2 and the wrong id.

Both mutants are caught by the expected row above: one finding `E-REVISION-INVALID`, with `revision` neither `T` nor a commit.

## Limits / unresolved
- Nothing was executed. `Reviewed-SHA256` is the value supplied with the item; it was not recomputed here. The baseline `tools/_revision.py` was not compared with the snapshot byte-for-byte.
- No pinned snapshot or SHA was supplied for the consumer. It was read from the live `tools/check-locator-clarification.py`, which may change.
- Not observed directly: the `merge-base` exit code for a tree operand (M2), and the claim that `rev-parse --disambiguate` lists objects only and never refs. Both are inferences from Git semantics and binder comments.
- No LSP device was available in this seat; definition and caller tracing used literal grep plus reading the code, so it is not a semantic proof.
- No tool installs or updates.

Scope: executed=none
