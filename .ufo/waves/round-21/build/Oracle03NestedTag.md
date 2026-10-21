# Oracle03NestedTag — check-section-citations.py × NestedTag expected behavior (source-only)

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-section-citations.py-NestedTag-expected-source-only

## Axes

- **Resolution**: selector → unique object → type → peel → landed/pushed chain.
- **Propagation**: consumer `bind` call → bound sha → emitted `revision` + `git show` input.
- **Coverage**: whether the pinned round-20 `check-revision-binding.py` object-selector matrix exercises this pair.
- **Sensitivity**: smallest realistic weakening mutant that matrix would miss.

## Expected behavior (before any candidate output)

Observed from pinned `_revision.py` and consumer source; no execution.

1. **Admission** (`bind`, `_revision.py:174-176`): `--revision` must fullmatch `^[0-9a-fA-F]{7,64}$`; anything else → exit 2 `CANNOT_EVALUATE`, single finding `E-REVISION-INVALID` at site `revision`. A NestedTag selector is the *outer* annotated tag's object ID: full 40-hex or a unique ≥7-hex prefix.
2. **Uniqueness** (`_object_commit:119-124`): `rev-parse --disambiguate=<lowered selector>` enumerates object IDs only (refs ignored). Exactly one line required; 0 or ≥2 → `E-REVISION-INVALID`.
3. **Type + peel** (`_object_commit:126-146`): `cat-file -t` → `tag` triggers `rev-parse --verify --quiet <oid>^{commit}`.
   - **Git object-type invariant**: an annotated tag object stores exactly one target object ID plus a declared type. The `^{commit}` suffix dereferences tag objects *recursively* until a commit; nesting depth is not bounded by syntax, so tag→tag→commit is legal and peels to the innermost commit. `cat-file -t` on the outer object reports `tag` regardless of chain depth — only the peel resolves depth. Peel failure with a readable repo → `None` → `E-REVISION-INVALID`.
4. **Landed/pushed** (`bind:180-191`): peeled sha must be `merge-base --is-ancestor` of `refs/heads/master` (else `E-REVISION-NOT-LANDED`, site `refs/heads/master`) and of `refs/remotes/origin/master` when that ref exists (else `E-REVISION-NOT-PUSHED`, site `refs/remotes/origin/master`).
5. **Consumer propagation** (`check-section-citations.py:911-927`): `bind(ROOT, args.revision, branch)` — raw selector and `--branch` (default `master`) passed unmodified. On success `revision = binding.sha`; all doc reads are `git show <sha>:<path>` (`read_git:417-427`). On `RevisionError`, emitted `revision` echoes the *raw selector* and `branch_tip` is null.

### Expected verdicts for NestedTag input

- Outer tag → inner tag → commit landed on master and pushed (or origin ref absent): **binding accepted**; exit 0 (PASS) or 1 (FAIL) purely from doc evaluation; never a binding CANNOT. JSON `revision` = the peeled commit's full 40-hex ID — never the outer or inner tag object ID; `branch_tip` = master tip; `findings` contain only `R16-*` doc findings.
- Peeled commit not ancestor of `refs/heads/master`: exit 2, exactly one finding `E-REVISION-NOT-LANDED`.
- Landed locally but `refs/remotes/origin/master` exists and does not contain it: exit 2, `E-REVISION-NOT-PUSHED`.
- Tag chain terminating in blob/tree, ambiguous prefix, or missing object: exit 2, `E-REVISION-INVALID`.
- Repo unreadable during any lookup: `E-GIT-FAILED`.
- **Full-SHA semantics**: bound identity is always the rev-parse-returned full commit hex, used both as emitted `revision` and as the `git show` prefix; the tag object ID and any short prefix never propagate downstream.

## Round-20 matrix coverage

Pinned `check-revision-binding.py` `object_selector_probes` (:475-673), gated on `--object-selectors` and `name in TOOLS` (:722; `check-section-citations.py` is in TOOLS :61-79). Every tag fixture is a depth-1 `git tag -a` pointing **directly at `tip` (a commit)** (:502-504, :564-567): `annotated_tag_object`, `annotated_tag_prefix`, `full_tag_object_id_ref_shadow`, `ghost_full_hex_annotated_tag`. `noncommit_blob` covers blob; nothing constructs tag→tag or tag→non-commit. **NestedTag is not covered.** The consumer's own `binding_sandbox` (:590-615) creates only commits — no tag objects — so its selftest adds no NestedTag coverage either.

## Smallest realistic weakening mutant the matrix misses

A **depth-limited (single-hop) peel**: replace the recursive `oid^{commit}` peel (:139-142) with a one-level dereference that accepts only when the tag's *immediate* target is a commit (e.g., resolve the tag's stored object once and require type `commit`, or equivalently `rev-parse` the immediate target and reject if it is still a tag). All round-20 tag cases are depth-1 tag→commit, so every `annotated_tag_*`/`full_tag_*` case still accepts; the mutant then either wrongly refuses NestedTag with `E-REVISION-INVALID` or binds the inner tag SHA instead of the commit — undetected. By contrast, mutants that drop peeling entirely (return the tag `oid` as `binding.sha`) or peel to `^{tree}` are already caught: `accepted` (:396-404) requires emitted `revision` == `tip` commit SHA, so `annotated_tag_object`/`full_tag_object_id_ref_shadow` fail. The matrix gap is precisely peel-depth ≥2, not peel-vs-no-peel.

## Observations / inferences / limits

- **Observed**: consumer bind call and argument propagation (:36 import, :913-916 call, :914 sha assignment, :417-427 reads, :926-927 refusal echo); pinned binder logic lines cited above; matrix fixtures depth-1-only.
- **[INFERENCE]**: `^{commit}` recursion and `--disambiguate` object enumeration semantics per documented Git behavior; no tag-object fixtures exist in either probe harness, so Git-side nested-tag resolution was not observed.
- **Limits**: NO-EXEC review — no command run, no candidate output examined; repo-unreachable `E-GIT-FAILED` branches reachable only when `rev-parse --git-dir` itself fails (:106-109, :129-132, :143-146).
- Installs/tooling: none required (source-only review; NO-EXEC contract honored).

Scope: executed=none
