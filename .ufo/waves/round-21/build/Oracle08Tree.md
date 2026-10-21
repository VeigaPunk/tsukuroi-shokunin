# Oracle08Tree — check-recheck-commands.py × Tree object selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-recheck-commands.py-Tree-expected-source-only

Axes: (a) selector-resolution correctness (object-type gating), (b) exit/finding
contract fidelity (exit 2, exactly one finding, exact id/site/detail), (c)
full-SHA / echo semantics of the emitted `revision` field, (d) round20 matrix
coverage completeness for this consumer/type pair, (e) oracle independence
(expected output derived from the object-type invariant, not by importing the
binder algorithm).

## Bind propagation (observation)

`tools/check-recheck-commands.py` run():918 calls
`_revision.bind(repo, args.revision, branch)` with `args.revision` verbatim —
no consumer-side normalization, truncation, or re-validation — and
`branch=args.branch` (parser default `"master"`, :892). A
`_revision.RevisionError` is re-raised as `Cannot(exc.fid, exc.site, exc.detail)`
(:919-921) after filling `tip` via `_revision.branch_tip`, then emitted as
`CANNOT_EVALUATE` with exactly one Finding (:930-934). On success, `binding.sha`
(the fully resolved commit id) feeds `expand_paths`/`read_git`/`--exec-log` and
the emitted `revision` field (:922-923, :932, :965). No repo file is read before
bind completes.

## Expected behavior — Tree selector (source-derived, pre-output)

Given `--revision` = hex selector (full 40-hex or unique >=7-hex prefix, any
case) that uniquely names a **tree** object, `--branch master` valid and present:

1. `REV` (:41) accepts: pure hex, 7-64 chars — even a full 40-hex tree ID.
2. `_object_commit` (:119-137): `rev-parse --disambiguate=<lowered>` returns the
   tree's full ID as the single match; `cat-file -t` returns `"tree"` — neither
   `"commit"` (:134) nor `"tag"` (:136) → `return None`.
3. `bind` raises `RevisionError(E-REVISION-INVALID, "revision",
   "<raw selector> does not name one commit")` (:178-179).
4. Consumer emits JSON `status: CANNOT_EVALUATE`, **exit 2**, `findings` =
   exactly one `{id: E-REVISION-INVALID, site: "revision", detail: "<raw
   selector> does not name one commit"}`. `revision` echoes the raw selector
   string as typed (:932); `branch_tip` = current master tip; `origin_tip` =
   null; no knowledge files are read.

Ordering notes: `validate_branch` precedes revision checks (:174), so tree +
invalid branch → `E-BRANCH-INVALID`; tree + valid-but-missing branch →
`E-REVISION-INVALID` (step 3 precedes step 4), matching the contract ordering in
the module docstring (:11-21). Ambiguous tree prefix (>=2 objects) → same id via
`len(objects) != 1` (:123). Uppercase input is equivalent — disambiguate is
lowercased (:119).

Full-SHA semantics: on refusal the `revision` field echoes the input selector
verbatim (prefix stays a prefix); on acceptance it is always the resolved full
40-hex commit SHA from `binding.sha`, never the raw selector — confirmed by the
matrix's `accepted()` comparing `doc["revision"]` to the expected commit
(:396-404).

## Git object-type invariant (why the oracle need not import the binder)

Git object IDs name exactly four types: blob, tree, commit, tag. Only commits
carry parent edges, so "landed on branch" (merge-base ancestry) is defined only
for commits. An annotated tag is an *indirect* commit name — `^{commit}` peeling
is a deterministic Git-defined deref — so peeling a uniquely selected tag keeps
the "one commit" invariant. A **tree** names a directory snapshot, not history:
it has no parent chain and cannot peel to a commit; like a blob it must fail
step 3 with `E-REVISION-INVALID`. The expected row therefore follows from the
type enumeration plus the contract's check ordering — "tree must reject as
non-commit, one finding, exit 2" — without copying the binder's procedure.

## Round-20 matrix coverage for this pair (observation)

`check-recheck-commands.py` is in the original-nine `TOOLS` via `R17_GATES`
(:74), so `object_selector_probes` applies when `--object-selectors` is passed
(:722-727, :815-816). Object-type rows exercised: **commit** (full/prefix,
uppercase, ref-shadowed — :629-632, :616-626), **annotated tag object**
(peeled→accepted — :631-632), **blob** (`noncommit_blob` → E-REVISION-INVALID —
:633). **No tree object is ever created**: fixtures write only a blob
(`hash-object -w --stdin`, :408-413), an annotated tag (:502-509), and commits;
no `mktree`/`write-tree`/`hash-object -t tree` exists anywhere in the file
(grep `tree` → only `ls-tree` listing, `ast.parse`, unrelated). The non-commit
negative class is sampled only at blob. → **No: the old matrix does not cover
the Tree selector for this consumer.**

## Smallest realistic weakening mutant it would miss

One-token change in `_object_commit`: widen the commit accept to
`if object_kind in ("commit", "tree"): return oid`. Every matrix case is
untouched — commit, tag-peel, blob, ghost, unlanded paths behave identically —
but a tree selector now reaches `_ancestor`, where
`merge-base --is-ancestor <tree> refs/heads/master` exits non-0/1 (tree is not
committish) → `E-GIT-FAILED` at site `refs/heads/master` instead of
`E-REVISION-INVALID` at `revision`. Still refused, still exit 2 — a weakening of
the single-finding-id/site diagnostic contract that `strict-refusals` (:460-465)
cannot see because no tree selector is probed. [INFERENCE: merge-base on a tree
exits 128 per standard `^{commit}` deref failure; not executed here.] A stronger
admission-weakening variant (mapping a tree to a containing commit, e.g.
returning the branch tip for `object_kind == "tree"`) is equally invisible to
the matrix but requires more machinery than a kind-list edit; the diagnostic
weakening is the minimal realistic miss. Note the subtler inert trap: widening
the *fallthrough* (`object_kind != "tag"` → also admit `"tree"` to the peel
block) produces identical behavior — peel fails → `None` → E-INVALID — so
mutant-kill claims on this pair need the tree row, not type-list reasoning alone.

## Residual risk / verification gaps

- Source-only: nothing executed; exit/stderr values for git edge cases are
  documented-behavior inference, flagged above.
- Matrix grading of a CANNOT path checks id + count, not `site`/`detail` text —
  a site-mangling mutant could pass even a hypothetical tree row
  (`refused`/`exact_refusal` grade `binding_ids == [expected_id]` only,
  :480-486).
- The consumer's own `selftest` (:1097+) exercises path-type "tree"
  (`expand_paths`) but never a tree `--revision`; selftest is not evidence here.

Scope: executed=none
