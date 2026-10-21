# Oracle07NestedTag — check-freshness-r17.py × NestedTag expected behavior (source-only)

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-freshness-r17.py-NestedTag-expected-source-only

## Axes

- **Resolution**: selector → unique object → type → peel → landed/pushed chain.
- **Propagation**: consumer `bind` call → bound sha → emitted `revision` + `git show` input.
- **Coverage**: whether the pinned round-20 `check-revision-binding.py` object-selector matrix exercises this pair.
- **Sensitivity**: smallest realistic weakening mutant that matrix would miss.

## Expected behavior (before any candidate output)

Observed from pinned `_revision.py` (round-21 snapshot, SHA256 above) and live consumer
`tools/check-freshness-r17.py` source; no execution.

1. **Admission** (`bind`, `_revision.py:174-176`): `--revision` must fullmatch
   `^[0-9a-fA-F]{7,64}$`; anything else → exit 2 `CANNOT_EVALUATE`, single finding
   `E-REVISION-INVALID` at site `revision`. A NestedTag selector is the *outer* annotated
   tag's object ID: full 40-hex or a unique ≥7-hex prefix of it.
2. **Uniqueness** (`_object_commit:119-124`): `rev-parse --disambiguate=<lowered selector>`
   enumerates object IDs only (refs never consulted). Exactly one line required;
   0 or ≥2 → `E-REVISION-INVALID`.
3. **Type + peel** (`_object_commit:126-146`): `cat-file -t` → `tag` triggers
   `rev-parse --verify --quiet <oid>^{commit}`.
   - **Git object-type invariant**: an annotated tag object stores exactly one target
     object ID plus a declared type; `cat-file -t` reads the outer object's own header and
     reports `tag` at any chain depth — it never reports the target's type. The
     `^{commit}` suffix dereferences tag objects *recursively* until a commit; nesting
     depth is not bounded by the selector syntax, so tag→tag→commit is legal and resolves
     to the innermost commit. Peel failure on a readable repo → `None` →
     `E-REVISION-INVALID`; a non-`tag` non-`commit` kind (blob/tree) → `None` → same id.
4. **Landed/pushed** (`bind:180-191`): peeled sha must be `merge-base --is-ancestor` of
   `refs/heads/master` (else `E-REVISION-NOT-LANDED`, site `refs/heads/master`, detail
   names the *peeled* sha[:12]) and of `refs/remotes/origin/master` when that ref exists
   (else `E-REVISION-NOT-PUSHED`, site `refs/remotes/origin/master`). `merge-base` exit
   ≥2 → `E-GIT-FAILED`, never "not an ancestor" (`:156-160`).
5. **Consumer propagation** (`check-freshness-r17.py:769-796`): `_revision.bind(ROOT,
   args.revision, branch)` — raw selector and `--branch` (default `master`) passed
   unmodified. On success `revision = binding.sha`, `tip = binding.branch_tip`,
   `source = revision`; every doc read is `git show <sha>:<path>` (`read_git:345-355`)
   for registry `corpus/knowledge/freshness-recheck-r17.json`, probed target paths, the
   fixed `BASE` paths, and the two round-17 captures. `--registry-from` applies the same
   `bind` to its selector for the registry source only (`:777-778`). On `RevisionError`
   the emitted `revision` echoes the *raw selector string* and `branch_tip` carries the
   value `_revision.branch_tip(ROOT, branch)` already computed at `:771` — the live tip
   when readable, `None` only when that informational call failed (`:792-796`).

### Expected verdicts for NestedTag input

- Outer tag → inner tag → commit landed on master and pushed (or origin ref absent):
  **binding accepted**; exit 0 (PASS) or 1 (FAIL) purely from registry evaluation;
  never a binding CANNOT. JSON `revision` = the peeled commit's full 40-hex ID — never
  the outer or inner tag object ID; `branch_tip` = master tip; `findings` contain only
  `R17-FRESH-*`/`STALE-UNFLAGGED`/`E-REGISTRY-*`/`E-*-READ` doc-level ids from
  `evaluate`/`record_issues`, no `E-REVISION-*`/`E-BRANCH-*`/`E-GIT-FAILED` binding ids.
- Peeled commit not an ancestor of `refs/heads/master`: exit 2, exactly one finding
  `E-REVISION-NOT-LANDED`; `revision` field echoes the selector.
- Landed locally but `refs/remotes/origin/master` exists and does not contain it:
  exit 2, `E-REVISION-NOT-PUSHED`.
- Tag chain terminating in a blob/tree, ambiguous prefix, or missing object:
  exit 2, `E-REVISION-INVALID` ("does not name one commit").
- Same matrix applies to a NestedTag given to `--registry-from` (`:778`).
- **Full-SHA semantics**: bound identity is always the rev-parse-returned full commit
  hex, used both as emitted `revision` and as the `git show` prefix; the tag object ID
  and any short selector prefix never propagate downstream.

## Round-20 matrix coverage

Pinned `check-revision-binding.py` `object_selector_probes` (:475-673), gated on
`--object-selectors` and `name in TOOLS` (:722); `check-freshness-r17.py` is in TOOLS via
`R17_GATES` (:73, :79). Every tag fixture is a depth-1 `git tag -a` pointing **directly
at `tip` (a commit)** (:502-504, :564-567): `annotated_tag_object`,
`annotated_tag_prefix`, `full_tag_object_id_ref_shadow`,
`ghost_full_hex_annotated_tag`. `noncommit_blob` covers a bare blob; `blob-revision`/
`git-failed` cover blob-as-selector/origin. **Nothing constructs tag→tag or
tag→non-commit, so NestedTag is not covered.** The consumer's own `binding_sandbox`
(:458-575) creates only commits c1/c2/c3 — no tag objects — and its `expect` asserts
`binding.sha.startswith(rev)`, which would misfire for any tag selector anyway
(:500-503); so the consumer selftest adds no NestedTag coverage. The binder's own
hermetic `selftest` does cover it (`nested-annotated-tag-object`, `_revision.py:362-365`)
— but that is the shared module testing itself, not the judge probing this consumer.

## Smallest realistic weakening mutant the matrix misses

A **depth-limited (single-hop) peel**: replace the recursive `oid^{commit}` peel
(`_revision.py:139-142`) with a one-level dereference that accepts only when the tag's
*immediate* target is a commit — e.g., read the tag's stored `object` field once and
require `cat-file -t` == `commit` on it. Every round-20 tag case is depth-1
tag→commit, so all `annotated_tag_*`/`full_tag_*` accepts still pass; the mutant then
either wrongly refuses NestedTag with `E-REVISION-INVALID` or binds the inner tag SHA —
undetected by the matrix. Mutants that drop peeling entirely (return `oid` as
`binding.sha`) or peel to `^{tree}`/`^` are already caught: `accepted` (:396-404)
requires emitted `revision` == expected commit. A sibling gap: replacing `^{commit}`
with `^{}` (peel to first non-tag) keeps tag→tag→commit accepted but wrongly accepts a
chain ending in blob/tree — also missed, since the matrix has no tag→non-commit row.

## Observations / inferences / limits

- **Observed**: consumer bind call and propagation (`:52` import, `:771` pre-bind
  `branch_tip`, `:773-778` binds and sha assignment, `:779-791` reads via `read_git`,
  `:792-796` refusal echo); pinned binder lines cited above; matrix fixtures depth-1
  only; consumer sandbox commit-only.
- **[INFERENCE]**: `^{commit}` recursion and `--disambiguate` object enumeration per
  documented Git object-model behavior; no nested-tag fixture exists in either probe
  harness, so Git-side nested-tag resolution for this consumer was not observed. The
  expected oracle needs only the type invariant (kind = tag ⇒ peel via `^{commit}` ⇒
  full commit SHA) plus the fixture's known commit — not the binder's algorithm — so no
  binder logic is imported into the expected output.
- **Limits**: NO-EXEC review — nothing run, no candidate output examined; lsp not
  consulted (no server registered for this review; all claims cite pinned source lines).
  `E-GIT-FAILED` repo-unavailable branches fire only when `rev-parse --git-dir` itself
  fails (`:106-109, :129-132, :143-146`).
- Installs/tooling: none required (source-only review; NO-EXEC contract honored; pacman
  pause respected — nothing installed).

Scope: executed=none
