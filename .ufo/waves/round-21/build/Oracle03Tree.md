# Oracle03Tree — check-section-citations.py × Tree object-ID selector (expected, source-only)

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-section-citations.py-Tree-expected-source-only

## Axes
- Contract correctness: exit code, finding id/site/detail, JSON field shape for a Tree selector.
- Matrix coverage honesty: does the pinned round20 `--object-selectors` matrix exercise (this consumer, Tree).
- Mutation sensitivity: smallest realistic weakening the existing matrix misses.

## Bind/argument propagation (observation)
- `tools/check-section-citations.py:36` imports `RevisionError, bind` from `_revision`; `sys.dont_write_bytecode = True` (line 35).
- `--revision` is a bare `metavar="REV"` argparse string with no `type=` validator (lines 435–437); the raw argv string reaches `bind(ROOT, args.revision, branch)` unmodified at line 913. `bind(ROOT, BASE, branch)` follows at line 916 only on success.
- `revision, branch_tip = args.revision, None` (line 911); both are overwritten only at lines 914–915 on successful bind. On `RevisionError`, line 924–925 re-wraps it as `Cannot(exc.fid, exc.site, exc.detail)` and emits `Result(CANNOT, [Finding(...)], 0)` with the **raw selector** and `branch_tip=None`.
- Pinned `_revision.py` `bind` (172–192): `REV.fullmatch` passes for 7–64 hex; `_object_commit` (112–146) does `rev-parse --disambiguate=<lower>` → require exactly one object → `cat-file -t oid` → `commit` returns oid, `tag` peels `<oid>^{commit}`, **any other type returns None** (line 136–137) → `RevisionError(E-REVISION-INVALID, "revision", "<sel> does not name one commit")`.

## Expected observable behavior for `--revision <tree object id>`
For a full 40-hex tree SHA, a unique 7–39-hex tree prefix, or uppercase variants (disambiguated via `revision.lower()`, line 119):
- exit code: **2** (CANNOT; `emit` returns `result.code`, `sys.exit(main())` line 940).
- stdout: single JSON line, `sort_keys=True`, with exactly:
  - `"status": "CANNOT_EVALUATE"`
  - `"revision": <literal selector as typed>` — echo, never a resolved SHA; no full-SHA binding is produced because `bind` raises before `sha` exists
  - `"branch": "master"` (or `--branch` value)
  - `"branch_tip": null`
  - `"correction_count": 0`
  - `"findings"`: exactly one object `{"id": "E-REVISION-INVALID", "site": "revision", "detail": "<sel> does not name one commit"}` — identical for ambiguous-prefix and non-commit-type paths, since both funnel to `sha is None` at line 178–179.
- No `git show` (`read_git`) is reached; the gate evaluates nothing (count 0). No repo mutation: the binder is read-only subprocess plumbing (`rev-parse`, `cat-file`, `merge-base`, `update-ref` absent).

## Git object-type invariant (why the oracle needs no binder import)
A tree is a non-commit, non-tag object. `^{commit}`/`^{type}` peeling dereferences **tag objects recursively to a non-tag object**; only a tag may peel to a commit (gitrevisions/git-rev-parse docs, `sources/git-types.txt`). A bare tree has no commit to peel to, and `cat-file -t` reports `tree`, not `commit`. So the selector contract is: one uniquely disambiguated object whose type is `commit`, or `tag` that peels to a commit; `tree` is neither ⇒ `E-REVISION-INVALID`. Expected output derives from that invariant plus the consumer's CANNOT emit shape — no algorithm reimplementation.

## Does the pinned round20 matrix cover this case? — No
`.ufo/…/snapshot/tools/check-revision-binding.py` (SHA da000d…):
- `object_selector_probes` (475–673) cases: ghost branch/tag refusals, shadow acceptances, uppercase, full commit id, annotated tag→commit acceptances, `noncommit_blob` refusal (line 633), unlanded/unpushed object refusals. **The only non-commit object ever created is a blob** (`blob_object` → `git hash-object -w`, 408–413); no `mktree`, no tag→tree, no nested tag→tree. The `check-section-citations.py` row exists (TOOLS line 64) but its Tree cell is unexercised.
- Cross-check (observation): the pinned `_revision.py` selftest *does* cover the row internally — `tree-revision-invalid` (line 412) and `annotated-tag-to-tree-invalid` (417–418) via `mktree` at 407–410. The gap is strictly at the consumer-facing matrix layer, which is what C2 `--object-target-types` adds.

## Smallest realistic weakening mutant the matrix misses
One-token widening in `_revision.py` line 134: `if object_kind == "commit":` → `if object_kind in ("commit", "tree"):` (equivalently, `object_kind != "tag"` → `object_kind == "blob"` at line 136 leaves blob refused but lets a tree fall into the peel — that variant then yields `peel.returncode != 0` → `None` → same observable, so it is a pure dead-code weakening, not killable even by the new row). The `in ("commit","tree")` mutant returns the tree OID as `sha`; `_ancestor` then runs `git merge-base --is-ancestor <tree> refs/heads/master`, which exits ≥2 (non-commit operand), so `_ancestor` (156–160) raises `E_GIT`. Observable delta vs. expected: finding id `E-GIT-FAILED`, site `refs/heads/master` (or `refs/remotes/origin/master` if it were a commit-like object that passed the local ancestor check — here it fails at the local check), detail `merge-base --is-ancestor exited 128…`, instead of `E-REVISION-INVALID` at site `revision`. Exit stays 2; the finding id/site is the discriminator. The matrix passes under this mutant: `noncommit_blob` still yields `INVALID`, every accept case is unchanged, and no tree object exists in its sandbox. Binder selftest `tree-revision-invalid` would kill it, but the matrix never invokes the binder selftest for this row.

## Limits
- No pinned snapshot of `check-section-citations.py` exists under `.ufo/waves/round-21/snapshot/tools/` (only `_revision.py`, `check-revision-binding.py`, `check-seat-scope.py`); consumer semantics were read from the live file at the stated path. [LIMIT]
- `merge-base` exiting ≥2 for a non-commit operand is git contract; exact stderr text is [INFERENCE] — the finding id `E-GIT-FAILED` is not, since `_ancestor` maps every non-{0,1} status to `E_GIT` regardless of text.
- Branch-error precedence (`E-BRANCH-*` raised before revision resolution, `validate_branch` at `bind` line 174) is out of this cell's scope; default `master` assumed present.
- No execution: all expected outputs are static derivations from the pinned binder and live consumer source; zero commands were run.

Scope: executed=none
