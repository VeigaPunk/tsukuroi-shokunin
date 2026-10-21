# Oracle04Tree — check-source-scope-correction.py × Tree object-ID selector

Axes: depth (C1 decision row: `tree` class), operability (C2 consumer target-type), calibration (C3 reviewed-byte receipt below).

## Scope

- Consumer (original-nine member, TOOLS row 4 of pinned check-revision-binding.py:65): `tools/check-source-scope-correction.py`, read at candidate location for read-only inspection only.
- Selector class: `tree` — a hex object ID (40-hex or unique prefix ≥7) resolving to exactly one Git tree object.
- Binder reviewed: pinned snapshot `.ufo/waves/round-21/snapshot/tools/_revision.py` (Reviewed-SHA256 below).

## Observations (source-grounded)

1. Consumer `main` (tools/check-source-scope-correction.py:634-642): `revision` is set to the raw `args.revision` string, `_revision.bind(ROOT, args.revision, branch)` is called verbatim, a `_revision.RevisionError` is converted to `Cannot(exc.fid, exc.site, exc.detail)`, and only on success is `revision` rebound to `binding.sha` with `branch_tip = binding.branch_tip`. No doc read (`read_git`) happens when bind raises.
2. Binder path for a tree selector (snapshot `_revision.py`):
   - `bind` line 175: `REV.fullmatch` — `^[0-9a-fA-F]{7,64}$` — a hex tree ID (40-hex or ≥7 prefix, either case) passes.
   - `_object_commit` line 119: `git rev-parse --disambiguate=<revision.lower()>` enumerates all object types; a unique tree yields exactly one line (the full tree SHA); an absent/ambiguous selector yields `len(objects) != 1` → `None`.
   - Lines 127-137: `cat-file -t` returns `"tree"` → `object_kind != "tag"` → `return None` (never peeled).
   - `bind` line 178-179: `sha is None` → `RevisionError("E-REVISION-INVALID", "revision", "<sel> does not name one commit")`.
   - Detail truncation at line 87-equivalent `[:120]` applies to this detail only via the f-string at line 179, which is not truncated — [INFERENCE: line 179 builds the detail without `[:120]`; selectors are ≤64 chars so immaterial].
3. `emit` (consumer line 336-343): refusal JSON carries `revision` = the raw selector (not the resolved object ID), `branch_tip` = `null`, `correction_count` = 0, `findings` = exactly one entry sorted single.

## Expected behavior (source-only, pre-candidate)

`--revision <tree-sha-or-unique-tree-prefix>` on `check-source-scope-correction.py`:

- exit code: **2** (`CANNOT`)
- status: **`CANNOT_EVALUATE`**
- findings: exactly `[{"id": "E-REVISION-INVALID", "site": "revision", "detail": "<selector> does not name one commit"}]`
- JSON `revision`: echoes the selector as typed (lowercasing is NOT applied — `args.revision` verbatim; `disambiguate` lowercasing is internal only)
- `branch_tip`: `null`; `correction_count`: 0; no corpus file is read at the tree object.
- Full-SHA semantics: a full 40-hex tree SHA is identical in outcome to a unique prefix — type decides, not precision. An uppercase tree SHA also yields the same refusal (REV admits mixed case; `--disambiguate` receives the lowered form).
- A tree prefix colliding with any other object (commit/blob/tag) also yields `E-REVISION-INVALID` via the `len(objects) != 1` arm — same id, same shape.

## Does the pinned round20 matrix cover this case?

No dedicated row. `object_selector_probes` (check-revision-binding.py:475-673) exercises non-commit selectors only via `noncommit_blob` (line 633) and the same `blob` in `probe_tool`'s `blob-revision` (line 449); `tree` never appears as a probed object type in either matrix. Tree SHAs exist in every sandbox (each commit has a root tree) but no case feeds one to a tool. Coverage is therefore implicit-by-shared-code-path only (blob and tree share the `object_kind != "tag"` arm at `_revision.py:136-137`), not an explicit consumer×tree assertion. The old matrix also has no tree-vs-commit prefix-collision row (the exact ambiguity the `_object_commit` docstring at line 115-117 defends against).

## Smallest realistic weakening mutant the round20 matrix would miss

One-token widening of the accept arm:

```
-    if object_kind == "commit":
+    if object_kind in ("commit", "tree"):
```

Tree selector then reaches `merge-base --is-ancestor <tree> <branch>` (line 157-160): git exits non-zero outside {0,1} → `E-GIT-FAILED` at `merge-base` instead of `E-REVISION-INVALID` at `revision` — a real contract break (wrong finding id, wrong site, honest refusal replaced by a fabricated git-failure diagnosis). Blob behavior is unchanged, so `noncommit_blob`/`blob-revision` stay green and no tree row exists to catch it. A still-smaller delete-the-type-check mutant is *not* behavior-observable (the surviving `^{commit}` peel rejects trees and blobs identically, gitrevisions `^{<type>}` requires type-ish-ness), so the above is the smallest *observable* weakening that escapes the matrix.

## Git object-type invariant (why no binder re-derivation is needed)

From the pinned reader-text (`sources/git-types.txt`, gitrevisions 2.56.0): `<rev>^{<type>}` peels to `<type>` only when `<rev>` is `<type>`-ish; `^{}` recursively peels only *tags*. A tree is the container payload a commit points to — it is never commit-ish and never a tag — so `tree^{commit}` is a syntax/lookup error, not a resolution. Independent ground truth therefore states: a selector naming a tree cannot name a landed commit, and the only truthful binding outcome is invalid-revision refusal. This derives the expected verdict from the Git object model plus the observed control flow, without importing the binder's algorithm into the oracle.

## Limits

- Source-only derivation; no command executed, no candidate output consulted.
- `--disambiguate` enumerating trees is stated by git docs (all object types) and relied on at line 119-124; if a git build excluded trees, `len != 1` still yields the same `E-REVISION-INVALID` — outcome robust either way.
- Detail-string equality asserted only up to the f-string at `_revision.py:179`; site `revision` and id `E-REVISION-INVALID` are exact.

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-source-scope-correction.py-Tree-expected-source-only
Scope: executed=none
