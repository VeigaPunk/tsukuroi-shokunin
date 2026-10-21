# Oracle01 TagBlob — check-locator-clarification.py × annotated-tag-to-blob object-ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-locator-clarification.py-TagBlob-expected-source-only
Lane bounds: leaf member — no subagent dispatch.

Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (Reviewed-SHA256 is the item-supplied value; not recomputed — NO-EXEC).
Consumer (read-only): `tools/check-locator-clarification.py`.
Round20 matrix: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.

## Axes
1. Exit class  2. Finding id/site/count  3. `revision`/`branch_tip` (full-SHA) payload semantics  4. Matrix coverage  5. Mutant sensitivity

## Case definition
Selector = the object ID (full 40-hex, or a unique ≥7-hex prefix, any case) of an annotated tag object whose `type` header is `blob`. `--branch` default `master`, branch exists, selector otherwise well-formed.

## Observed: consumer propagation (source lines)
- `import _revision` (l.19) resolves to the sibling `tools/_revision.py` (script dir on `sys.path[0]`); in the matrix sandbox that is the clone's checked-out tip copy.
- `main` l.782-788: `_revision.bind(ROOT, args.revision, branch)` — argv `--revision` passed verbatim (no lowercasing/trim), `branch` = `args.branch`. On `RevisionError`: `tip = _revision.branch_tip(ROOT, branch)`, `revision = args.revision`, re-raised as `Cannot(exc.fid, exc.site, exc.detail)`; l.793-795 emits `Result(CANNOT, [one Finding], 0)`.
- `read_git` (l.790) is never reached on refusal: no `git show` of the blob or any file.
- `emit` prints one `json.dumps(..., sort_keys=True)` line and returns `result.code`; `sys.exit(main())`.
- Consumer's own `binding_cases`/`BINDING_WANTS` (l.556-569) contain no tag or blob selector.

## Observed: pinned binder path (contract check 3)
`bind` → `validate_branch` ok → `REV` matches (7-64 hex) → `_object_commit`: `rev-parse --disambiguate=<lower>` yields exactly one OID → `cat-file -t` = `tag` → `rev-parse --verify --quiet --end-of-options <oid>^{commit}` fails → `rev-parse --git-dir` ok → `None` → `RevisionError(E-REVISION-INVALID, "revision", f"{revision} does not name one commit")`. Checks 4-6 are never reached.

## Expected (source-only, stated before any candidate output)
- Exit: `2` (CANNOT).
- stdout: exactly one JSON object, keys exactly `branch, branch_tip, correction_count, findings, revision, status`:
  - `status` = `"CANNOT_EVALUATE"`
  - `findings` = exactly one: `{"id": "E-REVISION-INVALID", "site": "revision", "detail": "<selector verbatim> does not name one commit"}`
  - `correction_count` = `0`
  - `revision` = the selector string exactly as supplied (case and length preserved; NOT the tag OID expanded, NOT the blob OID, NOT the tip). A refusal never emits a resolved full SHA here.
  - `branch` = `"master"` (or the given branch)
  - `branch_tip` = full lowercase hex OID of `refs/heads/<branch>` (from `branch_tip` → `_commit`), or `null` if that ref is absent.
- Precedence corollaries: with `--branch nosuch` the result is still `E-REVISION-INVALID` (check 3 precedes E-BRANCH-MISSING) with `branch_tip: null`; a lagging or blob-pointing `refs/remotes/origin/<branch>` does not matter (checks 5-6 and their E-GIT-FAILED are never reached). Full ID, unique prefix and uppercase forms give identical id/site; only `revision`/`detail` echo differs.
- No E-GIT-FAILED, no E-INTERNAL, no second binding id, no traceback; stderr carries no finding.

## Git object-type invariant (oracle basis, independent of binder code)
An object ID is the hash of `"<type> <len>\0<body>"`, so type is fixed by the ID. An annotated tag body records `object <oid>` and `type <kind>`, which its own ID covers. `<tag>^{commit}` follows the tag chain to its terminal object and succeeds only when that object is a commit. A tag→blob therefore can never denote a commit, whatever refs, branches or origin state exist. The expected E-REVISION-INVALID follows from contract check 3 ("uniquely matches an object ID, then peels to a commit") plus this invariant. The oracle MUST NOT import `_revision` or the judge's `object_commit`: it should build the fixture with `hash-object -w` + `tag -a <name> <blob>`, record the tag OID from `rev-parse refs/tags/<name>^{tag}`, assert fixture facts only (`cat-file -t <tagoid>` = `tag`, `cat-file -p` header `type blob`), then compare the consumer's output against the literals above.

## Matrix coverage (pinned check-revision-binding.py)
Not covered. `object_selector_probes` (l.475-673) runs `check-locator-clarification.py` (TOOLS[0], `EXTRA` empty) only with an annotated tag → **commit** (`annotated_tag_object`, `annotated_tag_prefix`, `full_tag_object_id_ref_shadow`: exact_accept) and a **direct** blob (`noncommit_blob`; also `probe_tool` `blob-revision`: exact_refusal E-REVISION-INVALID). No tag→blob (or tag→tree) selector exists in `probe_tool` or `object_selector_probes`. The binder's own `--selftest` has `annotated-tag-to-blob-invalid` (l.413-418), but that tests the binder alone, not this consumer's propagation, and is not part of the matrix grade.

## Smallest realistic weakening mutant the matrix misses
In `_object_commit`, peel to any object instead of a commit: `f"{oid}^{{commit}}"` → `f"{oid}^{{}}"` (removing the word `commit`).
- Tag→commit: `^{}` lands on the same commit, so every matrix accept case still passes. Direct blob: still refused by the `cat-file -t` kind gate. The matrix grade stays the same.
- Tag→blob: returns the blob OID as `sha`, then `merge-base --is-ancestor <blob> refs/heads/master` exits ≥2 → `E-GIT-FAILED` at site `refs/heads/master` [INFERENCE: Git's exit code for a non-commit is not observed here]. The exit is still 2, so an oracle that only checks the exit code would also miss it; the finding id (`E-REVISION-INVALID` vs `E-GIT-FAILED`) and site (`revision`) are what tell them apart.
- Variant that is also missed: on peel failure fall back to `return oid` (the tag OID). Same E-GIT-FAILED [INFERENCE].

## Limits / unresolved
- The SHA-256 of the snapshot and its byte-identity with live `tools/_revision.py` were not computed. A grep confirms the live file has the same `_object_commit` tag-peel lines (l.113, 136, 140), but this does not prove byte equality.
- Git exit codes for `merge-base` on a blob were inferred, not observed.
- SHA-256-format repositories: `branch_tip` would be 64-hex; the semantics are unchanged.
- No non-author closure or promotion is claimed.

Scope: executed=none
