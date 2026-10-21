# Oracle01Tree — check-locator-clarification.py × Tree object-ID selector

Axes: C1 depth (source-grounded expected behavior before candidates exist), C2 operability (does the pinned round20 matrix exercise this consumer/type pair), C3 calibration (reviewed-byte receipt, no execution).

## Consumer wiring (confirmed read-only)

- `check-locator-clarification.py` is original-nine `TOOLS[0]` in pinned `check-revision-binding.py`; `EXTRA` needs no extra argv.
- `main()` calls `_revision.bind(ROOT, args.revision, branch)` — `ROOT` = repo root from `__file__`, `args.revision` verbatim, `branch` = `--branch` (default `"master"`). On `RevisionError` it sets `tip = _revision.branch_tip(ROOT, branch)`, `revision = args.revision` (raw selector echo), and re-raises as `Cannot` → `emit(Result(CANNOT, [Finding(fid, site, detail)], 0), revision, branch, tip)`. Binding `sha`/`branch_tip` replace `revision`/`tip` only on success; `binding.origin_tip` is discarded by design.

## Expected behavior, source-only (before any candidate output)

`--revision <TREE>` where TREE resolves uniquely to a Git **tree** object:

1. `validate_branch` runs first — invalid `--branch` yields `E-BRANCH-INVALID` regardless of the tree.
2. `REV.fullmatch` accepts 7–64 hex; a tree SHA passes syntax.
3. `_object_commit`: `rev-parse --disambiguate=<lowercased>` → exactly one oid; `cat-file -t` → `"tree"`; not `"commit"`, not `"tag"` → returns `None` → `RevisionError(E-REVISION-INVALID, "revision", "<selector> does not name one commit")`.

Observable contract:
- Exit code **2**; stdout is one sorted-key JSON object `{branch, branch_tip, correction_count, findings, revision, status}`.
- `status: "CANNOT_EVALUATE"`; `correction_count: 0`; `revision` echoes the **raw selector as typed** (case preserved — never a resolved object ID); `branch_tip` is the full sha of `refs/heads/<branch>` or `null`.
- `findings` is exactly one entry `{id: "E-REVISION-INVALID", site: "revision", detail: "<selector> does not name one commit"}`.
- No `git show` of the four corpus files, no PASS/FAIL verdict, no worktree reads, no writes.
- Same refusal for a unique 7–39-char prefix of a tree, an uppercase tree SHA, a selector matching zero objects, or a prefix matching ≥2 objects (all → `len(objects) != 1` or non-commit/non-tag → `E-REVISION-INVALID`). `--branch nosuch` still yields `E-REVISION-INVALID` (revision check precedes branch existence); unreadable repo yields `E-GIT-FAILED`.

## Does the pinned round20 matrix cover this case? — No.

`object_selector_probes` (gated on `--object-selectors`, original-nine only) probes commit objects (tip/short-tip/parent/unlanded/ghost/shadow/uppercase), annotated tag **objects and prefixes peeling to commits**, absent objects under hex-lookalike refs — and exactly one noncommit: a **blob** (`noncommit_blob`, `blob-revision`; `git-failed` uses that blob only as an *origin ref target*). No tree object ID is ever passed as `--revision`. The consumer's own `binding_cases()` selftest also has no tree row (its blob appears only as the origin-ref target). Only the binder's module selftest (`_revision.py` lines 407–418: `tree-revision-invalid`, `annotated-tag-to-tree-invalid`) exercises a tree — at `bind()` level, not through this consumer's CLI/findings path.

## Smallest realistic weakening mutant the matrix would miss

Change `_object_commit` line 134 `if object_kind == "commit":` → `if object_kind in ("commit", "tree"):` — a one-token widening returning the tree oid as the bound sha. For this consumer the tree then reaches `merge-base --is-ancestor <tree> refs/heads/master`, which exits ≥2 → `E-GIT-FAILED` instead of `E-REVISION-INVALID`: same exit 2, but wrong finding id, site, and detail. Every existing matrix case (blob revision, blob origin ref, tags, shadows) still passes — the divergence lives only on the unprobed Tree input. (A mutant letting `"tree"` fall into the peel branch is observation-dead — `<tree>^{commit}` fails → still `None` → still `E-REVISION-INVALID`; the oid-as-commit mutant is the smallest *live* weakening. A full false-accept is unreachable by one mutation because git itself refuses tree ancestry — the realistic failure is the finding-id shift, which is precisely what `exact_refusal`'s `binding_ids == [expected_id]` grading would catch *if* a tree selector existed in the matrix.)

## Git object-type invariant / why the oracle must not import the binder

An object ID names exactly one object of exactly one immutable type (blob/tree/commit/tag). Only commits carry parents and thus participate in the DAG that ancestry, landing, and push checks quantify over; a tree is a directory listing — `^{commit}` peeling and `merge-base` are undefined for it. The contract therefore maps any uniquely resolved non-commit, non-commit-peeling-tag object to `E-REVISION-INVALID` before ref checks, and a tree SHA must never appear in `revision`/`branch_tip` fields. The expected-output oracle states this declaratively (selector type → refusal id/exit/payload shape), not by re-running the same disambiguate/cat-file/peel algorithm under test — the same independence the judge asserts with its own `object_commit` copy ("must not share the code it grades").

## Limits

Source-only derivation; nothing executed (NO-EXEC). Peel-failure exit codes for `<tree>^{commit}` and `merge-base` on trees are stated from Git semantics, not observed this round. The mutant analysis covers single-point weakenings of the type gate, not multi-site conspiracies.

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-locator-clarification.py-Tree-expected-source-only
Scope: executed=none
