# BindFullOidShadow — round20 attempt1

Axes: C2 object identity, exact-object precedence, honest finite-coverage claims. C1/C3 and host/boot safety are outside this review.

Candidate root: `/tmp/tsukuroi-r20-binder-20261021`. Below, `tools/_revision.py` and `tools/check-revision-binding.py` refer to that root. The lane registers this binder worktree at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:2-7` and preregisters actual-object selection and annotated-tag peeling at `preregister.json:37-47` in the same round directory. Baseline identity is assignment-provided, not independently checked through Git.

## Findings, by severity

### P2 — Undefined helper aborts the selftest before either full-OID shadow case

Evidence: `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:291-292` calls `git(repo, ...)` while constructing the annotated ghost tag. This module imports no `git` name (`:32-39`), defines its subprocess helper as `_git` (`:69-77`), and defines its local selftest helper as `run` (`:210-216`). Inspection of the complete module found no binding for bare `git`.

[INFERENCE] With the ordinary successful fixture setup, the first absent repeated-character OID in the loop at `:287-290` reaches this call and raises `NameError`. The call is outside `expect`; moreover, `expect` only catches `RevisionError` (`:198-208`). Thus execution cannot reach the full commit/tag shadow loop at `:324-331` or the final selftest summary at `:370-375`. This is a concrete candidate-source defect, not an observed execution result.

Recommendation: use the existing `_git` helper for this return-code existence check. Do not simply substitute `run`, because its documented implementation raises on nonzero status instead of returning a process (`:210-216`). Until corrected, neither full-OID shadow assertion can supply executable selftest evidence. No code was changed here.

## Full-OID fixture checks

The assertions themselves have the correct decoy and exact expected identity:

| Selector | Refs installed | Expected binding | Evidence |
|---|---|---|---|
| Full commit OID `tip` | `refs/heads/<tip>` and `refs/tags/<tip>` both point to `base` | Exactly `tip`, not `base` | `tools/_revision.py:324-329` |
| Full annotated-tag OID `tag_oid` | `refs/heads/<tag_oid>` and `refs/tags/<tag_oid>` both point to `base` | Exactly the peeled commit `tip`, not `base` and not `tag_oid` | `tools/_revision.py:315-316,324-329` |

- `base` and `tip` come from successive distinct commits, with `master` retained at `tip` (`tools/_revision.py:221-228`). The tag object is created with target `tip` and obtained through the qualified `refs/tags/peel-object^{tag}` expression (`:315-316`). Thus `base` is a genuine different, landed decoy; this is not a same-target collision.
- `origin/master` is restored to `tip` before these cases (`:262-263`); the intervening selector cases do not move it. Both the intended commit and ancestor decoy satisfy the local/origin reachability conditions. A wrong selection cannot be hidden behind an ancestry refusal.
- The lambda captures `object_id` by default argument, calls `bind(...).sha`, and compares with `ok(tip)` (`:328-329`). `expect` compares returned values, not just successful status (`:198-208`). The annotated-tag case correctly expects the peeled commit SHA.
- Each iteration deletes both full-OID refs on its normal path (`:330-331`). An ordinary binding mismatch is collected by `expect`, so normal cleanup still follows. No cleanup or fixture was executed in this review.
- The independent judge contains analogous full commit/tag decoy assertions at `tools/check-revision-binding.py:590,602-612`; this corroborates the source-level intended oracle, not a passing result or an independent Git-precedence proof.

## Exact-object precedence: established behavior and remaining limits

The changed selection path now goes from `bind` to `_object_commit` (`tools/_revision.py:172-179`), rather than the lane's baseline direct `_commit` call (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/_revision.py:134-141`). `_object_commit` lowercases the selector, enumerates matching object IDs, and requires exactly one before type inspection (`tools/_revision.py:119-127`). A commit result is the enumerated full OID itself (`:133-135`), so this return path does not substitute a same-named ref's commit SHA.

The annotated-tag path still asks Git to interpret the confirmed full `oid` as `oid^{commit}` (`tools/_revision.py:139-142`), and type inspection also passes that full OID to `cat-file -t` (`:127`). The module does not independently parse tag contents or verify the peeled target against tag contents. This is a dependency on Git's full-object-name semantics, not, by itself, a demonstrated precedence defect. In particular, general refname lookup order is not proof that a real full OID loses to a hex-named ref: the existing source assessment explicitly excludes that conclusion (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/build/SrcGitRevisions.md:15-21`). No full-OID misbinding is established here.

Missing controls/proof in this narrow fixture:

1. Both namespaces are installed simultaneously and both point to the same decoy (`tools/_revision.py:325-327`). There is no separate full-OID branch-only or tag-only assertion, nor a case with different branch/tag decoys. These assertions therefore do not independently distinguish every namespace or simultaneous-ambiguity-dependent implementation.
2. The short-prefix branch/tag refs created at `:309-314` are not removed before `:324-331`. If the selected unique prefix ever equals the full `tip`, the commit full-OID case reuses that pre-existing collision; the loop does not assert independent fixture isolation. This does not make its expected SHA wrong.
3. The correctly specified full-tag shadow assertion is currently unreachable because of the P2 defect. No existing passing output for it was inspected. Neither these two finite cases nor this source review establishes arbitrary ref/object precedence or the claimed original-nine `object_selector_tools=9` result.

## Verification gaps and boundaries

Only static reads and literal searches were used; searches are navigation, not semantic caller proof. No LSP status/references/definition/diagnostics device was available through this seat's permitted NO-EXEC tool surface. No selftest, Git command, subprocess, runtime, build, lint, formatter, external request, or host probe was invoked. Source-to-source comparison is not a Git-produced diff or checkout-identity verification. No tools were installed or updated. Only this named report was written.

Recommendation only: correct the undefined helper before relying on the full-OID selftest cases; retain their exact `tip` oracle. No integration/admission judgment and no host or boot-readiness clearance are issued. Boot images remain UNKNOWN.

Scope: executed=none
