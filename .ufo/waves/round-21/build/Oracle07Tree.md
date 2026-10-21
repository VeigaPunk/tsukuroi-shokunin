# Oracle07Tree — check-freshness-r17.py × Tree object ID selector (expected source-only)

Axes: C1 depth (five source-grounded rows — one consumer/type pair here), C2 operability
(explicitly selected consumer target-type matrix), C3 calibration (preregistered receipt
before candidate outputs exist).

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-freshness-r17.py-Tree-expected-source-only

## Inputs reviewed (read-only, nothing executed)

- Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (the SHA above).
- Consumer: `tools/check-freshness-r17.py` (live tree; bind wiring inspected at
  lines 51–52, 379–394, 756–807, 308–322).
- Judge matrix: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.

## Bind wiring confirmed in the consumer

`import _revision` at line 52 (under `sys.dont_write_bytecode`). `main` resolves
`tip = _revision.branch_tip(ROOT, branch)` (line 771) then calls
`binding = _revision.bind(ROOT, args.revision, branch)` with **no argument
transformation** — `args.revision` is passed verbatim, `branch` defaults to `master`
(lines 769–775). On success `revision = binding.sha` (full resolved SHA replaces the
raw selector for all later `git show` reads and the emitted JSON). `_revision.RevisionError`
is converted to `Cannot` and emitted as a single-finding CANNOT result (lines 792–796).
`--registry-from` binds a second revision through the same `bind` (line 778).

## Expected behavior: `--revision <tree-object-id>` (any unique prefix or full SHA, any case)

Binder path for a tree selector: `REV` accepts 7–64 hex (line 175), so step 2 passes.
`_object_commit` → `rev-parse --disambiguate=<lower>` yields exactly one object →
`cat-file -t` returns `tree` → `object_kind != "tag"` → returns `None` (lines 134–137).
`bind` raises `RevisionError(E-REVISION-INVALID, "revision",
"<input> does not name one commit")` (line 179) — failure step 3 of the module
contract (lines 11–21), before branch/ancestor/origin checks, so repo branch state
cannot alter the outcome.

Consumer emission: exactly one JSON line (`sort_keys=True`) with

- `status`: `CANNOT_EVALUATE`, process exit **2** (`emit` returns `result.code`, line 322).
- `findings`: exactly one — `{"id": "E-REVISION-INVALID", "site": "revision",
  "detail": "<raw input> does not name one commit"}` (raw selector echoed verbatim).
- `revision`: the **raw CLI string**, not a resolved SHA — `binding` is never
  assigned, so `revision` stays `args.revision` (line 770 vs 774).
- `branch`: `master` (or `--branch` value); `branch_tip`: the commit tip of
  `refs/heads/<branch>` resolved pre-bind (null only if that branch is
  absent/unreadable); `resolved_records` 0, `record_count` 0, `scope` = the SCOPE
  literal, no `stale_records` key.
- No registry/target/capture reads occur; `evaluate` is never reached.

Full-SHA semantics: the raw-selector echo applies to every refusal; only an
accepted binding emits the canonical lowercase object ID (`binding.sha`). A tree
selector can never reach that path — refusal is unconditional given a readable
repository. With `--branch` invalid, `E-BRANCH-INVALID` still wins (bind step 1
precedes resolution), keeping first-failure-wins ordering.

## Git object-type invariant (oracle must not import the binder algorithm)

An expected-output oracle need only use Git's intrinsic type rule, independent of
`_revision.py`: an object database has blob/tree/commit/tag types; only a `commit`
is commit-ish directly and only a `tag` is peelable via `^{commit}`. A tree names a
directory snapshot — `<tree>^{commit}` is not a valid peel and `merge-base` cannot
compute ancestry on a non-commit. Therefore a uniquely-resolving hex selector of
type tree is INVALID at the "names one commit" step, identically to a blob and
distinctly from commits and commit-peeling tags. The oracle asserts
(exit, single finding id, site, status, raw-echo revision) from this type rule plus
the documented first-failure order — re-implementing disambiguate/peel ordering
would import the implementation under test.

## Does the pinned judge matrix cover this pair?

No. `check-revision-binding.py` covers `check-freshness-r17.py` as one of the
original nine (R17_GATES, line 73), but its only non-commit object probe is a blob:
`blob-revision`/`noncommit_blob` in `probe_tool` (line 449) and
`object_selector_probes` (line 633), the latter additionally gated behind
`--object-selectors` (lines 722–727, 815–816). Its selector matrix exercises
commit IDs/prefixes/case, annotated-tag object/prefix (peeling to a commit),
unlanded/unpushed commit selectors, and hex-shaped ref ghosts/shadows — never a
tree object ID and never an annotated tag peeling to a tree. (The binder's own
`--selftest` does pin `tree-revision-invalid` and `annotated-tag-to-tree-invalid`
at `_revision.py` lines 407–418, but that tests the module in isolation, not this
consumer's CLI wiring or JSON contract.)

## Smallest realistic weakening mutant the matrix would miss

A one-token widening of the commit-type check in `_object_commit` (or a copied
equivalent): `if object_kind == "commit":` → `if object_kind in ("commit", "tree"):`.
A tree selector then returns the raw tree oid, reaches
`merge-base --is-ancestor <tree> refs/heads/master`, which exits ≥2 on a non-commit
(the binder docstring, lines 23–24, states rc≥2 for non-commit ref arguments is
E-GIT-FAILED), so the consumer reports `E-GIT-FAILED` instead of
`E-REVISION-INVALID`. The matrix misses it because every probe is commit/tag/blob —
no row distinguishes "tree refused as INVALID" from "tree propagated to merge-base".
A blind blob↔tree symmetric mutant (`!= "tag"` → `== "blob"`) is *not* observably
different (tree falls through to the failing `^{commit}` peel and still returns
None), so the `(commit, tree)` widening above is the smallest missable weakening.

## Observations / inferences / limits

- Observation: wiring, finding id/site/detail text, JSON keys, and case coverage
  above are read directly from the three cited files.
- Inference: `merge-base` ≥2 on tree input rests on the binder docstring's own
  rc≥2 contract plus Git's commit-argument requirement; not executed here (NO-EXEC).
- Limit: expected values stated for a readable repository; an unreadable repo
  reclassifies step-3 failure as E-GIT-FAILED by design (lines 128–132).
- Limit: `--registry-from` tree selector behaves identically (same `bind`, line 778)
  but is a second selector, outside this pair's scope.
- No tool installs; this seat's NO-EXEC contract forbids them and none were needed.

Scope: executed=none
