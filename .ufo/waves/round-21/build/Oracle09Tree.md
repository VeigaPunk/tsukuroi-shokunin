# Oracle09Tree — check-seat-scope.py × Tree object ID selector (expected source-only)

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-seat-scope.py-Tree-expected-source-only

## Axes

- **Coverage**: does any exercised selector in the pinned judge matrix hit the tree-type decision in `_object_commit`.
- **Expected-behavior precision**: exit code, status, finding id/count/site, and `revision` field for the tree selector, stated before any candidate output exists.
- **Mutation-catch**: the smallest binder weakening that preserves every pinned-matrix case yet changes tree-selector behavior.

## Consumer wiring (read-only confirmation, tools/check-seat-scope.py)

- Line 36: `from _revision import RevisionError, bind as bind_revision` — shared binder, no local copy (also `sys.dont_write_bytecode = True`, line 35).
- Line 262: `bound = bind_revision(root, revision, branch)` inside `collect()` — arguments propagate verbatim: `root=ROOT` (repo root), `revision=args.revision` (raw CLI selector), `branch=args.branch` (default `"master"`). No re-validation, no selector rewriting in the consumer.
- Lines 263–264: `RevisionError` → `raise Cannot(exc.fid, exc.site, exc.detail)` — finder id, site, detail propagate unchanged into the JSON finding.
- `main()` (lines 651–668): `revision = revision_in` before `collect`; on `Cannot`, `emit(Result(CANNOT, [Finding(exc.fid, exc.site, None, exc.detail)], 0), revision, branch, tip=None, wave)`.

## Binder decision path for a tree object ID (pinned `_revision.py`, identical digest baseline/snapshot)

1. `bind()` line 175: `REV.fullmatch` — a 7–64 hex tree selector (full 40-hex or unique ≥7-hex prefix, either case) passes.
2. `_object_commit` line 119: `rev-parse --disambiguate=<selector.lower()>` returns exactly one line — the tree OID.
3. Line 127: `cat-file -t <oid>` → `"tree"`. Line 134 `== "commit"` false; line 136 `!= "tag"` true → **line 137 `return None`**.
4. `bind()` lines 178–179: `sha is None` → `RevisionError(E-REVISION-INVALID, "revision", "<selector> does not name one commit")`.
5. Consumer: `Cannot(E-REVISION-INVALID, "revision", detail)` → `emit` CANNOT.

## Expected behavior (pre-registered, source-only)

For `check-seat-scope.py --revision <tree-object-ID> --wave <w>` against a readable repo:

- **Exit**: 2 (CANNOT). **Status**: `"CANNOT_EVALUATE"`.
- **Findings**: exactly one, `id = "E-REVISION-INVALID"`, `site = "revision"`, `role = null`, `detail = "<selector> does not name one commit"` (detail echoes the *requested* selector, not the resolved OID; truncated only by the binder's own message text — no truncation here).
- **`revision` field**: the literal selector string (echo, not the resolved tree SHA). **`branch`**: `"master"` or `--branch` value. **`branch_tip`**: `null`; **`seat_count`**: 0.
- **No mutation, no wave read**: refusal fires before `refs/heads/<branch>` resolution, before `read_git`/`tree_paths`; a full-SHA tree, a unique ≥7-hex tree prefix, and uppercase-hex all converge to the same row. Same result whether or not any ref equals the selector digits (object IDs are resolved before refs).

## Git object-type invariant (why this does not need the binder's algorithm as oracle)

Git has four object types; `cat-file -t` returns exactly one of `commit`, `tag`, `tree`, `blob`. A revision selector names a *landed commit* iff the object it selects is a commit, or is a tag object reachable to a commit by peeling. A tree is neither: it cannot be peeled to a commit (`<tree>^{commit}` cannot resolve) and has no commit ancestry. Therefore any well-formed selector that resolves uniquely to a tree is invalid-as-commit by construction — independent of the binder's implementation. The independent oracle in the judge (`object_commit`, lines 139–166) already encodes this same four-type invariant without importing `_revision`.

## Round-20 matrix coverage (pinned check-revision-binding.py, snapshot sha da000de…)

The pinned judge's exercised object-ID rows — `probe_tool` shared cases plus `object_selector_probes` — contain exactly one non-commit type case: `noncommit_blob` (line 633) / `blob-revision` (line 449), both grading blob → `E-REVISION-INVALID`. Ghost/shadow/ref-collision rows exercise nonexistent or commit-typed objects only; `annotated_tag_*` rows exercise the accept path. **No selector naming a tree is ever exercised.** So the specific (consumer=check-seat-scope, type=tree) decision is *not covered* by the old matrix; it is covered only by the new `target_type_probes.nonempty_tree` row, which exists in the working tree (2e95984…) but is absent from the pinned snapshot.

## Smallest realistic weakening mutant the old matrix misses

Single-token mutation at `_revision.py` line 136: `if object_kind != "tag":` → `if object_kind not in ("tag", "tree"):` — reroutes a tree into the tag-peel branch. Every pinned-matrix case still passes (commits, tags, blobs, ghosts, shadows all unchanged), yet the tree row's *mechanism* changes — and with a slightly larger companion (peel fallback returning `oid`, or line 137 `return None` → `return oid`), the tree selector binds `sha=<tree-oid>`, degrading the expected `E-REVISION-INVALID` refusal into `E-GIT-FAILED` from `merge-base` (or worse). The strictest observable weakening in 4 characters — line 137 `return None` → `return oid` — keeps `noncommit_blob` looking like a refusal (CANNOT, wrong-but-present binding id) while silently dropping the tree type-invariant; nothing in the old matrix compares the tree row's expected `[E-REVISION-INVALID]`/`finding_count==1` pair, so the misclassification is invisible. A `nonempty_tree` selector probe is the minimum addition that exposes both forms.

## Observations / inferences / limits

- **Observation**: `_revision.py` snapshot digest equals the pinned baseline `06b71e8c…`; `check-seat-scope.py` is original-nine member via `R17_GATES` (`--wave .ufo/waves/round-16/build` extra argv).
- **Observation**: pinned `check-revision-binding.py` (1269 lines) lacks `target_type_probes`, `target_type_measure`, and `--object-target-types`; working copy (1416 lines) adds them.
- **Inference**: the `detail` string preserves the requested selector per line 179's f-string; the `revision` JSON field echoes the same selector per `main()` lines 659–665.
- **Limit**: expectations assume a readable repo and a selector that disambiguates to exactly one object; ambiguous-prefix tree prefixes take the `len(objects) != 1` → `None` path (same `E-REVISION-INVALID`, same detail shape) — already covered by existing ambiguity semantics, not a distinct row.
- **Limit**: `merge-base` behavior on tree arguments is stated from source-path reasoning (exit ∉ {0,1} → `E-GIT-FAILED`); not executed per NO-EXEC.

Scope: executed=none
