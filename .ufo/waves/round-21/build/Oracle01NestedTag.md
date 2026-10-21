# Oracle01 · NestedTag object-ID selector — check-locator-clarification.py

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-locator-clarification.py-NestedTag-expected-source-only

Axes named: **C1 depth** (does source-grounded selector semantics reach the terminal commit through every tag layer), **C2 operability** (does the pinned round-20 matrix exercise this consumer/type pair), **C3 calibration** (expected result fixed from source before any candidate output exists; receipts below). Scope: only `check-locator-clarification.py` × NestedTag — a hex object ID (40-hex or unique ≥7-hex prefix) of a tag object whose target is another tag object, the chain ending at a commit. NO-EXEC leaf; source-only derivation.

## 1. Consumer propagation (read-only inspection, not executed)

`tools/check-locator-clarification.py` (#8D38, live lane copy) is original-nine (judge `TOOLS` :61–67; 5 legacy + 4 `R17_GATES` = 9 total).

- `build_parser` :472–481 — `--revision` (metavar REV, "hex commit … reads immutable objects only") mutually exclusive with `--selftest`; `--branch` default `master`.
- `main` :771–804 — `args.revision`/`args.branch` pass verbatim into `_revision.bind(ROOT, args.revision, branch)` (:784). No rewriting, no local resolution, no second binder.
- Refusal path :785–788, :793–795 — `RevisionError` → informational `tip = _revision.branch_tip(ROOT, branch)` (`branch_tip` never raises, returns None on invalid/missing branch, `_revision.py` :163–169) → `Cannot(exc.fid, exc.site, exc.detail)` → exit **2**, `status` `CANNOT_EVALUATE`, exactly one finding carrying binder fid/site/detail verbatim.
- Accept path :789–790 — `revision, tip = binding.sha, binding.branch_tip`; the four corpus FILES read via `read_git(revision, path)` → `git show <binding.sha>:<path>` (:459–460). A nested-tag bound sha therefore steers *which immutable tree is evaluated*, not just a label.
- `payload`/`emit` :427–436 — JSON `revision` = bound sha on accept, the **raw selector string** on refusal (`revision = args.revision` :787); `status` ∈ {PASS, FAIL, CANNOT_EVALUATE}; `findings` sorted/deduped by `evaluate` :409; `correction_count` = number of valid unblocked r15 corrections (0–2, `evaluate` :419–423); exit = `result.code` (0/1/2).
- Consumer selftest `binding_cases` :573–656 covers only ref/branch/landing classes in `BINDING_WANTS` :555–570 — no object-type selector rows at all, so it adds no NestedTag coverage.

## 2. Expected behavior, stated before candidate outputs exist

Input: `--revision <TN>` where TN uniquely selects a tag object → tag object → … → commit C (chain length ≥2 tag objects); C landed on `master` and, when `refs/remotes/origin/master` exists, pushed.

Binder path (pinned snapshot `tools/_revision.py` #1303, baseline SHA256 above):

- `bind` :172–192 — `validate_branch` first (:174); `REV.fullmatch` accepts 7–64 hex (:175, :41).
- `_object_commit` :112–146 — `rev-parse --disambiguate=<tn.lower()>` must return exactly one object line (:119–124); `cat-file -t` on it returns `tag` (:127–136); the peel `rev-parse --verify --quiet <oid>^{commit}` (:139–142) dereferences **recursively** through every tag layer and yields C's commit sha; the already-confirmed object ID is reparsed as a committish, never as a ref (:116–117 docstring).
- Landing/push checks run on C (:180–191): `E-BRANCH-MISSING` if `refs/heads/master` absent; `E-REVISION-NOT-LANDED` (site `refs/heads/master`, detail `f"{sha[:12]} is not an ancestor"`) if C not ancestor; `E-REVISION-NOT-PUSHED` (site `refs/remotes/origin/master`) if origin ref exists and lacks C. Returns `Binding(C, branch, tip, origin)`.

**Expected observable contract — well-formed NestedTag selector, C landed and pushed:**

- Exit **0** (PASS) or **1** (FAIL) per corpus evaluation at C — **never 2 from binding**.
- JSON **`revision` = C** — the full lowercase 40-hex terminal **commit** object ID. Never TN, never an intermediate tag OID, never the selector spelling.
- `branch` = `"master"`; `branch_tip` = resolved `refs/heads/master` commit sha; `correction_count` = valid unblocked corrections at C (2 on a fully clean corpus, :422–423).
- Selector case-insensitive (`--disambiguate` lowercased :119): `TN.upper()` binds the same C.
- Ref collision irrelevant: object IDs resolve before refs (:113), so a branch/tag literally named TN does not shadow the object.

**Expected refusal contract** (same pair, degenerate chains): exit **2**, `status` `CANNOT_EVALUATE`, exactly one finding, `findings[0].id` = binder fid verbatim, `revision` echoes the requested selector:

- Chain ends at non-commit (tag→tag→blob/tree): `<TN>^{commit}` fails, repo readable → `_object_commit` returns None (:143–145) → **`E-REVISION-INVALID`** "does not name one commit" (:178–179).
- Peeled C unlanded → **`E-REVISION-NOT-LANDED`**; landed-but-unpushed → **`E-REVISION-NOT-PUSHED`**.
- Prefix selector disambiguating to ≠1 objects → None → **`E-REVISION-INVALID`** (:123–124); zero objects → same.
- Ordering: `E-BRANCH-INVALID` precedes all revision checks (:174 before :175).

## 3. Does the pinned round-20 matrix cover this pair? — **No.**

`object_selector_probes` (pinned `check-revision-binding.py` #1C93, :475–673 — only reachable under `--object-selectors`, opt-in at `measure` :676/:722) creates exactly one annotated tag, `r20-object-selector-<name>` targeting `tip` (:498–509). Every tag row is **single-level tag→commit**:

- `annotated_tag_object` :631, `annotated_tag_prefix` :632, `full_tag_object_id_ref_shadow` :616–626 — selector is that same tag object or a prefix; target = tip commit.
- `ghost_full_hex_annotated_tag` :556–588 — a tag *named by* a ghost 40-hex string, still tag→commit; graded refusal because the *selector* resolves to zero objects.
- `noncommit_blob` :633 is the only non-commit object row. The default `probe_tool` path (:416–472) has no tag rows at all, and `clone_lane` passes `--no-tags` (:220). Nothing anywhere constructs tag→tag→commit.

The binder's own selftest does contain the proof this gap matters: `_revision.py` :362–365 `nested-annotated-tag-object` expects `bind(repo, nested_tag_oid).sha == tip` — i.e., the canonical semantics accept nested tags and return the commit sha — but the *graded round-20 matrix* that scores consumers never exercises it, so a nested-selector defect ships with `object_selector_tools` fully green.

## 4. Smallest realistic weakening mutant the round-20 matrix would miss

**M: bounded one-level peel.** Replace the recursive peel (:139–142) with a single tag dereference that does not re-enter the tag branch — e.g. `git cat-file -p <oid>` and return the `object ` header sha as the binding sha (equivalently any peel loop capped at depth 1, or a depth-1 check that returns None when the target type is still `tag`; both collapse to the same coverage hole). No token-swap mutant escapes the matrix: `^{commit}`→`^{tag}` or returning bare `oid` yields the tag OID for *single*-level tags too, which `annotated_tag_object` (:631, expects `revision == tip`) already kills; `^{commit}`→`^{}`/`^0` still peels recursively.

M behavior: single-level tag→commit rows still yield C — every existing row passes (judge `annotated_tag_object`/`annotated_tag_prefix`, shadow rows, binder `annotated-tag-*` selftest rows). On a nested TN it either (a) returns the **inner tag OID** as `Binding.sha` — a silent wrong-sha defect: `merge-base --is-ancestor <tag-oid> master` and `git show <tag-oid>:<path>` peel committish input recursively to C, so landing and reads still succeed and only `payload.revision` ≠ C exposes it — or (b) refuses with `E-REVISION-INVALID`, a silent refusal regression. Neither variant is distinguishable by any row in the round-20 matrix; detection requires a same-identity comparison of `revision` against the construction-fixed C on a ≥2-deep tag chain.

## 5. Oracle independence — the Git object-type invariant

The expected output must not be derived by running `_revision.bind`/`_object_commit`: the binder is the unit under test, and the judge's `object_commit` (:139–166) is already a line-for-line code twin — a shared algorithmic error would move expected and actual together (the F5 failure mode).

The invariant the oracle relies on instead is fixture construction plus two Git guarantees:

1. **Type is per-object, not per-chain**: `cat-file -t` on every tag object returns `tag` regardless of target type or nesting depth. NestedTag therefore exercises the `tag` branch of `_object_commit`, but the only honest *result* type is `commit`.
2. **`^{commit}` terminates at the first commit or fails**: for a chain of k≥1 tag objects ending at C, `rev-parse --verify TN^{commit}` yields exactly C's 40-hex ID; ending at a non-commit it exits nonzero. Hence `Binding.sha` ≡ C is the unique correct output — any intermediate OID (TN or an inner tag) is wrong by object identity, and the expected constant comes from fixture construction records (`git rev-parse <ref>^{tag}` on the *inner* tag), never from the binder.

## 6. Observations / inferences / limits

- **Observed**: consumer call chain and payload fields (:771–804, :427–436, :459–469); binder disambiguate→type→peel order and refusal ordering (:119–146, :172–192); consumer `BINDING_WANTS` selftest has no object-type rows (:555–570); pinned round-20 matrix tag rows all single-level (:498–633), selector probes opt-in (:722), clone `--no-tags` (:220); binder selftest `nested-annotated-tag-object` fixes `.sha == tip` (:362–365).
- **[INFERENCE]**: `merge-base --is-ancestor` and `git show <oid>:<path>` peel a tag committish recursively — standard Git committish resolution per gitrevisions; not executed in this seat. This is what makes mutant M(a)'s failure *silent* rather than `E-GIT-FAILED`.
- **[INFERENCE]**: `git tag -a <name> <tag-object>` accepts a tag target per the `git tag <tagname> [<commit> | <object>]` synopsis; fixture builders should verify.
- **Limits**: candidate outputs not yet observed — the expected contract is fixed from source here. Lane `check-locator-clarification.py` is the live file, not the pinned snapshot (the snapshot holds only `_revision.py`, `check-revision-binding.py`, `check-seat-scope.py`); consumer propagation claims cite the live copy #8D38. No execution, no git object access; all SHA claims are construction-relative.
- No tool installed or updated in this seat (NO-EXEC; none needed for source review; per contract, needs are reported to L1 — none required).

Scope: executed=none
