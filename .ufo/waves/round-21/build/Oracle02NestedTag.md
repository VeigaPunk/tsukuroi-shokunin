# Oracle02 · NestedTag object-ID selector — check-root-dac-correction.py

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-root-dac-correction.py-NestedTag-expected-source-only

Axes named: **C1 depth** (does the source-grounded selector semantic reach the terminal commit through every tag layer), **C2 operability** (does the graded round-20 matrix exercise this consumer/type pair), **C3 calibration** (expected result fixed from source before candidate output; receipts below). Scope: only `check-root-dac-correction.py` × NestedTag (a 40-hex object ID of a tag object whose target is another tag object, chain ending at a commit). NO-EXEC leaf; source-only derivation.

## 1. Consumer propagation (read-only inspection, not executed)

`tools/check-root-dac-correction.py` (#D63D, live lane copy) is original-nine (judge `TOOLS` :61–67; 5 legacy + 4 `R17_GATES` = 9 total).

- `main` :533–545 — `--revision` (mutually exclusive with `--selftest`) and `--branch` (default `master`) pass verbatim to `run_gate(ROOT, args.revision, args.branch)`. No rewriting, no defaulting, no extra binding logic in the consumer.
- `run_gate` :264–283 — with revision set, calls `_revision.bind(repo, revision, branch)` (:275). `RevisionError` → informational `branch_tip` lookup, then `Cannot(exc.fid, exc.site, exc.detail)` → `Result(CANNOT, [Finding(fid, site, detail)], 0)`. Success → `label, tip = bound.sha, bound.branch_tip`; each of the four FILES read via `git show <bound.sha>:<path>` (:280, :253–263).
- `emit`/`payload` :224–233 — JSON `revision` = `label` (bound commit sha on accept; the raw selector string on refusal, consistent with the judge's :482–483 caveat), `status` ∈ {PASS, FAIL, CANNOT_EVALUATE}, `findings` sorted, exit = `result.code` (0/1/2).

## 2. Expected behavior, stated before candidate outputs exist

Input: `--revision <TN>` where TN is the full 40-hex ID of a tag object → tag object → commit C; C landed on `master` (ancestor of `refs/heads/master`) and, if `refs/remotes/origin/master` exists, pushed (ancestor of it).

Binder path (snapshot `tools/_revision.py` #1303):

- `bind` :172–192 — `REV.fullmatch` accepts the 40-hex selector (:175); `_object_commit(repo, TN)` runs (:177).
- `_object_commit` :112–146 — `rev-parse --disambiguate=<tn.lower()>` returns exactly TN (one line, :119–124); `cat-file -t TN` = `tag` (:127–136); peel `rev-parse --verify --quiet TN^{commit}` (:139–142) dereferences **recursively** through both tag objects to C — per gitrevisions, `^{<type>}` dereferences until an object of that type is found (`sources/git-types.txt:3-6`, git 2.56.0 page). Returns C.
- Landing/push checks (:180–191) run on C, not on TN. Returns `Binding(C, branch, tip, origin)`.

**Expected observable contract for a well-formed nested-tag selector:**

- Exit **0** (PASS) or **1** (FAIL) per corpus evaluation at C — **never 2 from binding**. `status` = `"PASS"`/`"FAIL"`, `correction_count` = 1 iff PASS.
- JSON **`revision` = C** — the full lowercase 40-hex terminal **commit** object ID. Never TN, never the intermediate tag OID, never the selector spelling.
- `branch_tip` = resolved `refs/heads/master` commit; `branch` = `"master"`.
- Selector case-insensitive (`--disambiguate` lowercased :119): `TN.upper()` yields identical bound sha.

**Expected refusal contract** (same consumer/type pair, degenerate chains), one `RevisionError` → exit 2, `status` `CANNOT_EVALUATE`, exactly one finding, `findings[0].id` = binder fid verbatim:

- Chain ends at non-commit (tag→tag→blob/tree): `TN^{commit}` fails, repo readable → `_object_commit` returns None (:143–145) → **`E-REVISION-INVALID`** "does not name one commit" (:178–179).
- Peeled commit unlanded: **`E-REVISION-NOT-LANDED`**, detail carries `sha[:12]` of the peeled commit (:184–185).
- Peeled commit landed but origin ref exists and lacks it: **`E-REVISION-NOT-PUSHED`** (:188–190).
- Ambiguous selector (<7 hex impossible — REV gate; colliding 40-hex prefix impossible for a full OID): a *prefix* that disambiguates to ≠1 objects returns None → `E-REVISION-INVALID` (:123–124).
- Ordering: branch is validated first (:174), so an invalid `--branch` yields `E-BRANCH-INVALID` ahead of any revision check.

## 3. Does the pinned round-20 matrix cover this pair? — **No.**

`object_selector_probes` (snapshot `check-revision-binding.py` #1C93, :475–673) creates exactly one annotated tag `r20-object-selector-<name>` targeting `tip` (:498–509). Every tag row is **single-level tag→commit**:

- `annotated_tag_object` :631, `annotated_tag_prefix` :632, `full_tag_object_id_ref_shadow` :616–626 — selector is the same tag object or its prefix; target = tip commit.
- `ghost_full_hex_annotated_tag` :556–588 — a tag *named* by a ghost 40-hex string, still tag→commit; graded as refusal because the selector resolves to zero objects.
- `noncommit_blob` :633 — blob object ID; no tree, no tag-to-non-commit, no nested tag anywhere in the file.

The r20 `BindTagObject.md` design doc (:71) lists `R6 TN-nested` explicitly as **new — "positive control for recursive deref"**, confirming the gap. The binder selftest (`_revision.py:195–432`, incl. `annotated-tag-*` rows ~:360) is likewise single-level. So for NestedTag the graded matrix is silent: a nested-selector defect can ship with `object_selector_tools` fully green.

## 4. Smallest realistic weakening mutant the round-20 matrix would miss

**M: bounded one-level peel.** Rewrite the recursive peel (:139–142) as a single tag dereference — e.g. `git cat-file -p <oid>` → return the `object ` header sha without re-checking its type, equivalently any depth-1-capped peel loop. No smaller token-swap escapes the matrix: `^{commit}`→`^{tag}` or bare `oid` returns the tag OID for *single*-level tags too, which `annotated_tag_object` (:631, expects `revision == tip`) already kills.

M behavior: tag→commit rows still yield C — every existing row passes (judge `annotated_tag_object`/`annotated_tag_prefix`, shadow rows, binder `annotated-tag-*` selftest rows). On TN it returns the **inner tag OID** as `Binding.sha`. Then `merge-base --is-ancestor <tag-oid> master` silently peels committish input to C → landing check passes; `git show <tag-oid>:<path>` peels likewise → docs read fine; the only observable defect is `payload.revision` = inner tag OID ≠ C. The consumer accepts (exit ≠ 2), so the defect is a **silent wrong bound-sha**, invisible to every refusal row and undetectable without a same-identity comparison against the construction-fixed C.

## 5. Oracle independence — the Git object-type invariant

The expected output must not be derived by running `_revision.bind`/`_object_commit`: the binder is the unit under test, and the judge's `object_commit` (:139–166) is already a line-for-line code twin — a shared algorithmic error would move expected and actual together (r20 F5).

The invariant the oracle relies on instead is fixture construction plus two Git guarantees:

1. **Type is per-object, not per-chain**: `cat-file -t` on every tag object returns `tag` regardless of target type or nesting depth. Nested-tag therefore exercises the `tag` branch, but the only honest *result* type is `commit`.
2. **`^{commit}` terminates at the first commit or fails**: for a chain of k≥1 tag objects ending at C, `rev-parse --verify TN^{commit}` yields exactly C's 40-hex ID; ending at a non-commit it exits nonzero. Hence `Binding.sha` ≡ C is the unique correct output — any intermediate OID (TN or an inner tag) is wrong by identity, and the expected constant comes from `git rev-parse <inner-tag>^{tag}`/construction records, never from the binder.

## 6. Observations / inferences / limits

- **Observed**: consumer call chain and payload fields (:264–283, :224–233); binder disambiguate→type→peel order (:119–146); ordered contract checks docstring :11–24; round-20 matrix tag rows all single-level (:498–632); `BindTagObject.md` marking TN-nested as new.
- **[INFERENCE]**: `merge-base --is-ancestor` and `git show <oid>:<path>` peel a tag committish recursively — standard Git committish resolution per gitrevisions; not executed in this seat. This is what makes mutant M's failure *silent* rather than an `E-GIT-FAILED`.
- **[INFERENCE]**: `git tag -a <name> <tag-object>` accepts a tag target per the `git tag <tagname> [<commit> | <object>]` synopsis; fixture builders should verify (r20 §6 notes the `mktag` fallback).
- **Limits**: candidate outputs not yet observed — expected contract fixed from source here. Lane `check-root-dac-correction.py` is the live file, not the pinned snapshot (snapshot contains only `_revision.py`, `check-revision-binding.py`, `check-seat-scope.py`); consumer propagation claims cite the live copy #D63D. No execution, no git object access; all SHA claims are construction-relative.
- No tool installed or updated in this seat (NO-EXEC; none needed for source review).

Scope: executed=none