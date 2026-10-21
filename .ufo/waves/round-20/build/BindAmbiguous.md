# C2 object-prefix ambiguity and first-failure oracle

## Axis and source evidence

C2 is **operability** (`object_selector_tools`, preregistered 0→9). This is a baseline-only fixture proposal, not a verdict on an implementation or candidate diff.

- `tools/_revision.py:11-24` defines the normative first-failure sequence: branch validation → hex syntax → commit resolution → local branch existence → local ancestry → optional origin ancestry. It explicitly classifies merge-base errors (including an origin ref naming a non-commit) as `E-GIT-FAILED`.
- `tools/_revision.py:97-108,134-154` shows the baseline resolution path: `_commit` passes the supplied string directly to `rev-parse <ref>^{commit}`; `bind` then performs local-branch/ancestry checks before origin checks. There is no visible object-ID-only disambiguation step before interpreting the hex input as a ref expression.
- The independent judge is separate: `tools/check-revision-binding.py:130-176` has its own `rev_parse`/`bind` implementation. Its current `probe_tool` cases at `:380-436` cover ordinary `HEAD`/`@-`/branch-name rejection, abbreviated lowercase tip, landing, branch precedence, and origin failures, but not ghost hex refs, real hex-prefix ref shadows, uppercase/full object IDs, tag-object IDs, or ambiguous object prefixes. `build_parser` at `:515-525` currently exposes only `--tools-revision` and `--selftest`.
- `.ufo/waves/round-20/preregister.json:37-47` requires ghost branch/tag rejection, actual-object selection under branch/tag shadowing, uppercase/full IDs, noncommit rejection, tag-object peeling, landing and push outcomes. The binder assignment in `.ufo/waves/round-20/build/spec.json:10` additionally requires ambiguity rejection and preservation of first-failure/branch/origin semantics.

## Exact hermetic fixture proposal

Build one isolated Git repository with a linear `master` history `A → B → C` and a separate side commit `U` based on before `A`; set `refs/remotes/origin/master` to `C` initially. Use the generated full OIDs as symbolic fixture values below. Build refs only inside the fixture. For each unique-prefix case, choose the shortest prefix of length ≥7 for which the fixture's complete object-ID set has exactly one match. For the ambiguity case, generate distinct commit and blob objects until one seven-hex bucket contains at least one of each; call that prefix `P`, and select a bucket containing exactly one commit and one blob if available. Point a synthetic hex ref at another landed commit `V` so ref fallback/type-filtering cannot masquerade as object resolution.

| Case | Fixture mutation and call | Required result |
|---|---|---|
| Ghost branch | Choose a 40-hex `G` absent from the fixture's object IDs; create `refs/heads/G → C`; call `bind(repo, G, "master")`. | `E-REVISION-INVALID` (CLI exit 2, exactly one binding finding); never bind `C`. |
| Ghost tag | Same absent `G`, in a separate fixture; create `refs/tags/G → C`; call `bind(repo, G, "master")`. | `E-REVISION-INVALID` (exit 2, exactly one finding); never bind `C`. |
| Real branch shadow | Let unique prefix `P_A` name commit `A`; create `refs/heads/P_A → C`; call `bind(repo, P_A, "master")`. | Accept and return `A`'s full canonical SHA, not `C`'s SHA. |
| Real tag shadow | In a separate fixture, let unique prefix `P_A` name `A`; create `refs/tags/P_A → C`; call `bind(repo, P_A, "master")`. | Accept and return `A`'s full canonical SHA, not `C`'s SHA. |
| Ambiguous object prefix | The seven-hex `P` matches both a commit object and a blob object; create `refs/heads/P → C` (and, in a separate variant, `refs/tags/P → C`). Call `bind(repo, P, "master")`. | `E-REVISION-INVALID` (exit 2, one finding), despite the ref naming a valid commit. The prefix is ambiguous over object IDs, including non-commit objects. |
| Branch first | Use the ambiguous `P` above with branch `a..b`. | `E-BRANCH-INVALID` (exit 2, one finding), before attempting object disambiguation. |
| Revision resolution before missing branch | Use ambiguous `P` with valid-but-absent local branch `nosuch`. | `E-REVISION-INVALID`, not `E-BRANCH-MISSING` (exit 2, one finding). |
| Missing local branch before origin | Use valid unique object `A`, no `refs/heads/nosuch`, but create `refs/remotes/origin/nosuch` pointing to a blob; call `bind(repo, A, "nosuch")`. | `E-BRANCH-MISSING`, before inspecting the origin ref. |
| Local landing before origin | With `master → C`, call `bind(repo, U, "master")` after setting `refs/remotes/origin/master` to a blob. | `E-REVISION-NOT-LANDED`, not `E-GIT-FAILED`; local ancestry is the earlier failing check. |
| Origin error after local landing | Call with landed `A`, `master → C`, and `refs/remotes/origin/master` pointing to a blob. | `E-GIT-FAILED` (exit 2, one finding), not `E-REVISION-NOT-PUSHED`. |
| Origin lag after local landing | Restore origin to valid commit `A` while local master remains `C`; call with `B`. | `E-REVISION-NOT-PUSHED` (exit 2, one finding). |
| Case/length controls | Call with `A` as the full lowercase ID, its uppercase spelling, and its selected unique ≥7-hex prefix, with origin containing it. | Each is accepted with the same canonical full SHA `A`. |
| Annotated tag object | Create annotated tag object `T` pointing to landed commit `A`; select `T` by its unique object-ID prefix (not the tag's ref name). | Accepted and returns peeled commit SHA `A`. |
| Noncommit object | Select the full OID of a blob object. | `E-REVISION-INVALID` (exit 2, one finding). |

For each rejected original-nine CLI probe, the independent judge should require exit 2, the exact single `finding` ID, `binding_ids == [finding]`, and `finding_count == 1` (matching `refused()` at `check-revision-binding.py:351-359`). For accepted probes, use the judge's existing acceptance contract (`:361-369`): exit is not 2 and JSON `revision` equals the expected canonical SHA. Run all selector/ordering cases against each of the original nine; keep discovered tools outside C2's denominator as the preregistered scope states.

The ambiguity generator is intentionally collision-driven rather than relying on hard-coded SHA-1 values: create unique objects until a seven-hex prefix has both a commit and a blob, then attach the branch/tag alias at that prefix. This makes the fixture self-contained and exercises the minimum accepted selector length; the object population is larger than the other probes.

## Smallest wrong implementations killed

1. Replacing object-only resolution with the baseline-style `rev-parse "$rev^{commit}"` (or falling back to branch/tag lookup when object lookup returns no match) is killed by the ghost and real-shadow cases; the ambiguous-prefix case additionally catches a ref fallback even when multiple objects share the prefix.
2. Counting only commit-type matches rather than all object IDs is killed by the ambiguous commit+blob prefix: despite one matching commit and a usable hex ref, the required result is `E-REVISION-INVALID`.
3. Moving local-branch lookup ahead of revision resolution is killed by ambiguous `P` + `nosuch`; moving origin evaluation ahead of local branch/ancestry is killed respectively by missing-local-branch + origin-blob and unlanded `U` + origin-blob. Treating origin merge-base rc≥2 as “not pushed” is killed by the landed `A` + origin-blob case.

## Residual risk and verification gaps

This report proposes fixtures from the pinned baseline and preregistration only. No candidate implementation/output was inspected, and no fixture, command, test, build, or runtime was executed. A literal `lsp` device/status endpoint was not exposed in the permitted tool surface, so LSP references/definition/diagnostics were unavailable; source conclusions above are based on the cited reads, not grep as semantic proof. The collision generator is practical rather than a mathematical bound on SHA-1 search time. No host, boot, or runtime-safety claim is made.

Scope: executed=none
