# Oracle06NestedTag — check-boot-chain.py × NestedTag object-ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-boot-chain.py-NestedTag-expected-source-only

## Sources reviewed
- Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (same snapshot tag `1303` as baseline `tools/_revision.py`), contract lines 41–49, `_object_commit` 112–146, `bind` 172–192, selftest 353–365.
- Consumer (read-only inspection, not executed): `tools/check-boot-chain.py` — `main` 1554–1636, `build_parser` 828–847, `emit` 785–798, `binding_cases` 1324–1393.
- Pinned round-20 matrix: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py` — `TOOLS`/`R17_GATES` 61–79 (`check-boot-chain.py` member at 72), independent `object_commit` 139–166, `probe_tool` 416–472, `object_selector_probes` 475–673, `measure`/`--object-selectors` gating 676–817, selftest oracle-isolation 990–1000 and selector exercise 1112–1138.

## Axes
1. Selector class: hex object ID (7–64, case-insensitive) vs ref name/range — hex always takes the object path, never refs.
2. Unique-match object type (`cat-file -t` of the single `--disambiguate` result): commit / tag / blob / tree / ambiguous / absent.
3. Peel depth and terminal type for `tag`: `^{commit}` dereferences tag chains recursively; terminal commit → commit sha, terminal non-commit → no commit.
4. Landed/pushed status of the resolved commit: ancestor of `refs/heads/<branch>`; when `refs/remotes/origin/<branch>` exists, ancestor of it too.

NestedTag decision row: selector = the full 40-hex object ID (or a unique ≥7-hex prefix) of an annotated tag T2 whose `object` header names another annotated tag T1, which names a commit C.

## Expected source-only behavior (pre-registered, before candidate outputs)

Binder contract: `REV` accepts the hex selector (`_revision.py:175`); `--disambiguate` enumerates exactly one object = T2 (123–124); `cat-file -t` = `tag` (136); `git rev-parse --verify --quiet T2^{commit}` (139–142) — Git's `^{commit}` peel is recursive, dereferencing T2→T1→C and printing C's full sha. Peel succeeds → `bind` proceeds. With C an ancestor of `refs/heads/master` (and of `refs/remotes/origin/master` when that ref exists): `Binding(sha=C, branch, tip, origin)`; no `RevisionError`.

Consumer propagation (confirmed read-only): `main:1573` calls `_revision.bind(ROOT, args.revision, branch)` with the selector verbatim; `binding.sha` (1574) feeds every `git show <sha>:<path>` corpus read (1588, 1603–1605, 1622–1624) and the payload `revision` field (785–798). `--registry-from` (1577) binds through the same call.

Expected observable semantics for `check-boot-chain.py --revision <nested_tag_oid>` (or unique prefix):
- Exit: not 2. Exit is 0/1 purely from corpus conformance at C; selection mechanics cannot influence evaluation.
- Findings: zero binding findings — none of `E-REVISION-INVALID`, `E-REVISION-NOT-LANDED`, `E-REVISION-NOT-PUSHED`, `E-BRANCH-INVALID`, `E-BRANCH-MISSING`, `E-GIT-FAILED` may appear; only corpus verdict ids.
- Full-SHA: payload `revision` = C's full 40-hex sha — the peeled terminal commit, never the tag object id, never the selector text. `branch_tip` = branch tip commit sha.
- Refusal variants completing the row: nested tag whose peel terminates in blob/tree → `E-REVISION-INVALID` single finding, exit 2 (`revision:"unbound"`, `branch_tip:null`, 1571–1584); peeled commit not landed → `E-REVISION-NOT-LANDED`; landed but unpushed when origin exists → `E-REVISION-NOT-PUSHED`; ambiguous prefix → `E-REVISION-INVALID`.

## Does the pinned round-20 matrix cover this case? — No.
- `probe_tool` cases (417–424) contain no tag objects at all.
- `object_selector_probes` (475–673; exercised in selftest via `measure(..., object_selectors=True)` at 1116–1138) creates exactly one annotated tag, `tag_object → tip` commit (502–509) — depth 1 only. Covered tag rows: `annotated_tag_object` (631), `annotated_tag_prefix` (632), `full_tag_object_id_ref_shadow` (616–626). No tag→tag object is ever constructed; no depth-2 selector is probed.
- The binder's own selftest does cover `nested-annotated-tag-object` → tip (`_revision.py:362–365`), but that is the binder under test, not the consumer matrix — it cannot substitute for consumer coverage.
- The live candidate `tools/check-revision-binding.py` shows rows such as `nested_tag_to_commit`/`tag_to_blob`/`tag_to_tree`; those do not exist in the pinned `#1C93` copy, so no coverage claim may be borrowed from candidate output.

## Smallest realistic weakening mutant the pinned matrix would miss
Single-level peel: replace the recursive `^{commit}` dereference with a one-step dereference — resolve T2's `object` header once and accept that OID as the commit sha without re-checking its type or peeling further. On every pinned case the results coincide: depth-1 tag→commit yields the same C, so `annotated_tag_object`, `annotated_tag_prefix`, and `full_tag_object_id_ref_shadow` all still pass; the blob case stays `E-REVISION-INVALID`. Only at depth ≥2 does it diverge: tag→tag→commit either yields the inner tag OID as `sha` (breaking the full-SHA-commits-only invariant — `merge-base` peels commit-ish args, so it can still look bound, but the emitted `revision` names a tag object, not a commit) or is refused `E-REVISION-INVALID` when it must be accepted. The pinned matrix cannot see either divergence; a depth-2 nested-tag case is the minimal discriminator.

## Oracle independence / object-type invariant
`check-revision-binding.py:139–166` `object_commit` reimplements the selector against raw plumbing — docstring: "do not import the binder under test" — and selftest (990–1000) forbids deriving expected identity via `bind`. The verdicts above are stated from Git object semantics, not by replaying `_object_commit`. Invariant: object IDs are content-addressed typed objects; a hex selector must uniquely name exactly one object (enumerate before typing — ambiguity refusal prevents silently accepting a commit that shares a prefix with a colliding blob, 115–118). Object type, never a ref name, decides meaning: only `commit` and `tag` may name a commit; a tag names a commit iff its recursive `^{commit}` peel ends in a commit. NestedTag preserves "one selector → at most one unambiguous commit" and must be accepted; tag→blob/tree names no commit and must stay `E-REVISION-INVALID`.

## Limits
- Source-only: nothing executed; expected exit/finding/sha derive from pinned source and documented git behavior. Consumer read at current worktree state; the snapshot binder is the Reviewed-SHA256 baseline.
- Peel depth >2 follows the same recursive contract; depth-2 is this decision row.
- Candidate-matrix rows (`nested_tag_to_commit`, `tag_to_blob`, `tag_to_tree`, `target-tree-blind`) were sighted but not reviewed; they are candidate output, not evidence.
- No tool installs needed; none performed (NO-EXEC seat).

Scope: executed=none
