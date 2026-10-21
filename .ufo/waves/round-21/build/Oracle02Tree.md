# Oracle02Tree — check-root-dac-correction.py × Tree object selector (source-only)

Axes: depth (source-grounded decision rows), operability (consumer target-type matrix), calibration (preregistered byte/predicate receipts).

## Scope and artifacts

- Consumer: `tools/check-root-dac-correction.py` (original-nine member; listed in pinned
  `check-revision-binding.py` `TOOLS` at lines 61-67). Read-only inspection only.
- Binder under review: pinned snapshot `.ufo/waves/round-21/snapshot/tools/_revision.py`
  (reviewed file; SHA256 below).
- Prior matrix: pinned snapshot `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.
- No execution of consumer, binder, or git; all behavior derived from source.

## Bind-call / argument propagation (observed in source)

- `main()` (consumer lines 533-545): `--revision` string passes verbatim to
  `run_gate(ROOT, args.revision, args.branch)`; `--branch` defaults to `"master"`.
- `run_gate()` (lines 264-283): non-None revision → single canonical call
  `_revision.bind(repo, revision, branch)` at line 275. `RevisionError` is caught, the
  informational `branch_tip` is recomputed (line 277), and the error is re-raised as
  `Cannot(exc.fid, exc.site, exc.detail)` — one finding, fields preserved exactly.
- `emit()`/`payload()` (lines 224-233): exit = `result.code`; single JSON line,
  `sort_keys=True`, `"findings"` sorted; `"revision"` echoes the raw selector (label is
  set before binding, line 268 — the raw selector text, not a normalized SHA).

## Source-derived decision rows (binder `_object_commit`/`bind`, snapshot lines 112-192)

| Step | Mechanism | Tree selector outcome |
|---|---|---|
| Branch validation first | `validate_branch` (line 174) runs before any revision check | default `master` passes; a malformed `--branch` would yield `E-BRANCH-INVALID` and preempt the revision row entirely |
| Selector syntax | `REV.fullmatch` (line 175): 7-64 hex | tree full SHA (40 hex) and any ≥7 hex prefix pass; non-hex/short selectors die here with `E-REVISION-INVALID` |
| Unique object resolution | `rev-parse --disambiguate=<rev>` (line 119); `len(objects) != 1` → `None` (line 123) | unique tree SHA/prefix → exactly one line, proceeds; ambiguous prefix → `None` → refused below |
| Type gate | `cat-file -t <oid>` (line 127); `commit`→accept (134), `tag`→peel (136-140), **all else → `None` (137)** | `tree` hits the `!= "tag"` fallthrough → `None`; **no peel attempt, no ancestor check, no `git show` run** |
| Refusal | `sha is None` → `RevisionError(E_INVALID, "revision", f"{revision} does not name one commit")` (lines 178-179) | site is the literal `"revision"`; detail interpolates the raw selector |

## Expected behavior (pre-registered, before candidate outputs)

`check-root-dac-correction.py --revision <tree-sha>` in a readable repo with valid
`--branch` (default `master`):

- **Exit:** `2` (`CANNOT`).
- **Findings:** exactly one finding — `id` = `E-REVISION-INVALID`, `site` = `"revision"`,
  `detail` = `"<selector> does not name one commit"` (raw selector echoed).
- **Status:** `"CANNOT_EVALUATE"`; `"correction_count": 0`;
  `"scope": "narrow-conformance-not-semantic-proof"`.
- **Revision echo:** the selector exactly as typed (raw 40-hex or prefix), not the
  resolved object id.
- **Branch tip:** `"branch_tip"` is the full hex tip of `refs/heads/master` or `null`
  (informational; failure path recomputes it via `branch_tip()`, which never raises).
- **Full-SHA semantics:** identical for a full 40-hex tree SHA and a unique ≥7-hex
  prefix — `--disambiguate` resolves both to one object and the type gate refuses both
  identically; the only difference is the `revision`/`detail` echo text.
- **Non-mutation:** the refusal happens before `read_git`/`git show`; the consumer is a
  read-only gate (`sys.dont_write_bytecode`, no `update-ref`/writes) — zero repository
  or filesystem mutation.

## Does the pinned round-20 matrix cover this case?

**No.** `object_selector_probes()` (pinned `check-revision-binding.py` lines 475-673)
exercises: ghost-hex branch/tag ref-shadows, full-hex ghost refs (branch, lightweight,
annotated), real-prefix shadow decoys, full commit/tag object-id ref-shadows, uppercase
object, annotated tag object + prefix (accepted via peel), `noncommit_blob` (line 633,
blob → `E-REVISION-INVALID`), unlanded object + prefix shadows, unpushed shadows.
`probe_tool()` adds `blob-revision` (line 449). **No tree-object selector case exists**
anywhere in the pinned matrix — the non-commit/non-tag class is represented by blob
alone. Blob and tree share the binder code path (the `!= "tag"` fallthrough), so the
matrix generalizes by proxy, not by exercised coverage of this consumer/type pair.

## Smallest realistic weakening mutant the pinned matrix would miss

A one-token type-class widening in `_object_commit`, e.g. line 134:
`if object_kind == "commit":` → `if object_kind in ("commit", "tree"):`.

- Tree SHA then returns `oid`; `merge-base --is-ancestor <tree> refs/heads/master`
  exits with a non-0/non-1 status (operand is not committish) → `_ancestor` raises
  `RevisionError(E_GIT, refs/heads/master, ...)` (lines 156-160).
- Observable signature the mutant produces: `status = CANNOT_EVALUATE`, exit 2, but
  `findings[0].id = E-GIT-FAILED`, `site = refs/heads/master` — instead of
  `E-REVISION-INVALID` at `site = revision`.
- Pinned matrix result under this mutant: every exercised case still passes —
  `noncommit_blob`/`blob-revision` still refuse (blob still returns `None`), all
  commit/tag/shadow/ancestry cases are untouched. The mutant survives the matrix
  precisely because no tree selector is ever sent.

## Why no imported binder algorithm — the Git object-type invariant

The oracle need not reimplement `--disambiguate`/`cat-file`: Git object type is
intrinsic to the stored object, not derivable from any ref or selector spelling.
`rev-parse <oid>^{commit}` peels only tag→commit; a tree is never committish, and
`merge-base --is-ancestor` requires committish operands. Therefore a uniquely
resolved tree selector can only terminate at the type gate as "does not name one
commit" — refusal with `E-REVISION-INVALID` before ancestry — independent of the
binder's internals. Any acceptance, misclassification (`E-GIT-FAILED`), or mutation
along this path violates that invariant.

## Limits

- Behaviors are source-derived, not executed; git exit statuses cited (merge-base
  non-committish → non-0/1) are Git contract, applied to the binder's 0/1 split at
  lines 157-160.
- Scope is exactly this consumer/type pair; no claim about sibling consumers or other
  object types.
- No install performed: seat contract forbids execution/installs; no tool was needed
  beyond read/grep/glob.

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-root-dac-correction.py-Tree-expected-source-only
Scope: executed=none
