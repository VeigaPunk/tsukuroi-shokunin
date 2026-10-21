# Oracle05Tree — measure-update-recheck.py × Tree object ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: measure-update-recheck.py-Tree-expected-source-only

Pinned source: `.ufo/waves/round-21/snapshot/tools/_revision.py`
(binder, Reviewed-SHA256 above). Consumer read-only: `tools/measure-update-recheck.py`.
Old judge read-only: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.

## Axes

- C1 (depth): five source-grounded object-type decision rows for the selector path.
- C2 (operability): whether the pinned round-20 matrix already exercises this
  consumer/type pair, and the smallest weakening mutant it would miss.
- C3 (calibration): preregistered reviewed-byte receipt (SHA above) and predicate.

## Bind call / argument propagation (observed)

`main` (measure-update-recheck.py:738–760): `--revision` → `load(args.revision,
args.branch)`; `--branch` defaults to `"master"` (DEFAULT_BRANCH, line 48).
`load` (471–481): `binding = _revision.bind(ROOT, rev, branch)` — direct call,
no argument rewriting; ROOT = repo root (parents[1] of the tool file, line 37).
On `RevisionError`: `raise Cannot(exc.fid, exc.site, exc.detail, revision=rev,
tip=_revision.branch_tip(ROOT, branch))` — fid/site/detail copied verbatim;
`revision` stored is the raw selector string, not a resolved SHA.
`main` (769–772): `emit(exc.revision or revision, "CANNOT_EVALUATE",
[Finding(exc.fid, exc.site, exc.detail)], digest=None, branch=branch,
branch_tip=exc.tip)`; `emit` returns `CANNOT` = exit 2 for any status other than
COUNTED/ABSENT (line 434).

## Expected behavior (derived source-only, before any candidate output exists)

For `--revision <S>` where S is 7–64 hex (`REV` allows mixed case) uniquely
naming a `tree` object — full OID or an unambiguous ≥7-char prefix:

1. `bind` step 1: `validate_branch("master")` passes.
2. Step 2: `REV.fullmatch(S)` passes (hex syntax is all that is checked).
3. `_object_commit(ROOT, S)` (lines 119–137): `rev-parse --disambiguate=<S.lower()>`
   returns exactly one OID (the tree's full ID); `cat-file -t` yields `"tree"`;
   `object_kind == "commit"` fails and `object_kind != "tag"` is true →
   `return None`. **No `^{commit}` peel is attempted for a tree** — only `tag`
   reaches the peel path.
4. `sha is None` → `RevisionError(E-REVISION-INVALID, "revision",
   "<S> does not name one commit")` (line 179; detail interpolates S verbatim,
   preserving input case). Ancestor/pushed checks never run; no RECORD/SNAPSHOT
   reads occur.

Expected observable output: exit 2; stdout JSON `"status": "CANNOT_EVALUATE"`;
`"findings"` = exactly one object `{"id": "E-REVISION-INVALID",
"site": "revision", "detail": "<S> does not name one commit"}` (single-finding,
single-binding-id contract); `"revision"` echoes S verbatim (refusal path does
NOT normalize to full SHA); `"branch": "master"`; `"branch_tip"` =
`refs/heads/master` tip OID or `null`; `record_count` 0, `snapshot_sha256` null,
all assessment fields null/empty.

Full-SHA semantics (contrast): on the *acceptance* path `revision` is
`binding.sha` — the full lowercase 40-hex commit OID from `--disambiguate`
(`load` line 480 reassigns `revision`) — independent of selector width/case.
A tree selector can never reach that path.

## C1 — five object-type decision rows (unique-selector outcomes via `_object_commit`)

| Selector resolves to | `_object_commit` path | Expected consumer result |
|---|---|---|
| commit (OID or prefix, any ref shadow) | `kind=="commit"` → oid | binding.sha = commit; ancestor/pushed gates decide |
| tag (annotated, uniquely selected) | peel `<oid>^{commit}` → commit sha | binding.sha = *peeled commit*; accepted iff landed |
| **tree** | `kind not in (commit, tag)` → None | E-REVISION-INVALID, exit 2, one finding |
| blob | same fall-through → None | E-REVISION-INVALID, exit 2, one finding |
| zero/ambiguous (ghost hex, non-unique prefix) | `len(objects) != 1` → None | E-REVISION-INVALID, exit 2, one finding |

Git object-type invariant (why the tree row is derivable without running the
binder): `--disambiguate` enumerates object IDs of *all* four types; only
`commit` names a commit directly and only `tag` can peel via `^{commit}`.
`tree` and `blob` have no commit target — `rev-parse <tree>^{commit}` always
fails — so a unique tree selector must terminate at "does not name one commit".
This is the binder's documented contract step 3 (docstring line 17).

## C2 — does the pinned round-20 matrix cover this pair?

`measure-update-recheck.py` is an original-nine member (TOOLS line 66; TOTAL=9
after R17_GATES). With `--object-selectors`, `object_selector_probes` runs for
every TOOLS name including this consumer (lines 722–724). Its case list
(522–671) covers: commit accept paths (full OID, unique prefix, uppercase,
ref-shadowed by decoy branch/tag), annotated-tag accept paths (full OID,
unique prefix — always peeling to tip), ghost selectors (12-hex and 40-hex
branch/lightweight/annotated-tag refs → E-REVISION-INVALID), `noncommit_blob`
(blob OID → E-REVISION-INVALID, line 633), unlanded/unpushed commit and
shadowed prefixes.

No case ever supplies a **tree** OID: `blob_object` (408–413) writes only a
blob; the annotated tag always peels to an accepted commit; trees are never
materialized. **Verdict: the old round-20 matrix does NOT cover the
measure-update-recheck.py × Tree pair** — it covers the consumer against
commit, tag, blob, and ghost classes only.

## C2 — smallest realistic weakening mutant it would miss

In `_object_commit` (lines 134–137):

```python
if object_kind == "commit":          # mutant: `in ("commit", "tree")`
    return oid
if object_kind != "tag":
    return None
```

Changing line 134 to `if object_kind in ("commit", "tree"):` admits a unique
tree OID as `binding.sha`. `_ancestor(repo, tree_oid, refs/heads/master)` then
runs `merge-base --is-ancestor` on a non-commit → git exits ≥2 →
`RevisionError(E-GIT-FAILED)`. Observable divergence: consumer reports
`CANNOT_EVALUATE` with `E-GIT-FAILED` instead of the contract `E-REVISION-INVALID`
— the refusal stays a refusal (exit still 2) but the finding id and reason class
are wrong, and `binding.sha` would carry a non-commit to `read_git`/`git show`
if reached. The matrix misses it entirely: no tree selector exists, and every
probed class behaves identically under the mutant (blob still falls through
`!= "tag"` → E-INVALID; commit/tag unchanged). One-token edit, wrong diagnostic
contract, zero matrix coverage — the minimal missed weakening. (A mutant routing
tree to the tag-peel branch instead, e.g. `object_kind == "blob": return None`,
is also missed by the matrix but is *unobservable*: `^{commit}` on a tree fails
→ `return None` → same E-REVISION-INVALID.)

## Oracle-independence note

Expected output must not be generated by importing or re-executing the binder
algorithm: an oracle built from the code under test is tautological — it can
only detect consumer-glue divergence, never binder regression. The pinned judge
follows the same rule (`object_commit` docstring line 140: "do not import the
binder under test"; module docstring lines 8–9). The expectation above is
grounded in the Git type lattice plus the consumer's verbatim fid/site/detail
propagation, both cited to pinned source lines.

## Limits / inference

- Exit-2 and single-finding shape are observed in source; exact stderr/stdout
  bytes and `branch_tip` value depend on repo state — [INFERENCE] for live run.
- Ambiguous-prefix tree collisions (tree + blob sharing a 7-char prefix) were
  not enumerated in the matrix either; outcome is still E-REVISION-INVALID via
  the `len(objects) != 1` row.
- Reviewed only the pinned snapshot for the binder and the live consumer source;
  no candidate outputs were examined (preregistration per predicate).

Scope: executed=none
