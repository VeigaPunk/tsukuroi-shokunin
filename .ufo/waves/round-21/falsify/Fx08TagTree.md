# Fx08TagTree — falsify check-recheck-commands.py × tag_to_tree (candidate 0a14952)

Reviewed-SHA256: 9dc46f46d322f92578b60027da3d7ea8138d90ef44eeae152531388e6c27e7e9
Predicate: check-recheck-commands.py-tag_to_tree-candidate-control

Primary receipt binds only `candidate/tools/check-recheck-commands.py` (SHA as above, taken from the item and `candidate-files.json:43-47`; not recomputed — NO-EXEC).
Auxiliary snapshot dependencies, read only, digests cited from `candidate-files.json`:
- `candidate/tools/_revision.py`: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf (`:63-67`).
- `candidate/tools/check-revision-binding.py`: 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6 (`:38-42`).
- Build oracle `build/Oracle08TagTree.md`. It was a comparison input only. It reviewed the live consumer, which was unpinned at the time, as its own line 7 states.
- Pinned `snapshot/tools/check-revision-binding.py`. Used only for the old-matrix shape comparison.

Everything below is a prediction from source. Nothing was executed, so there are no observations of tool runs.

## Axes
1. Exit class. 2. Finding id and cardinality. 3. `revision` field semantics (echo, not acceptance). 4. Fixture fidelity (typed object, fresh sandbox, prefix uniqueness). 5. Host isolation. 6. Mutant sensitivity of the C2 `tag_to_tree` row. 7. Old-matrix invariance and C2 mode accounting.

## Consumer bind/argv/error/output propagation (frozen source)
- Import: `import _revision` at `check-recheck-commands.py:55`, after `sys.dont_write_bytecode = True` (`:54`). The judge launches `sandbox/tools/check-recheck-commands.py` (`check-revision-binding.py:362`). That puts `sandbox/tools` at `sys.path[0]`, so `_revision` resolves to the sandbox checkout of the measured tip (`prepare`, `:233-242`, `checkout --detach tip`).
- Repository: `ROOT = Path(__file__).resolve().parents[1]` (`:58`), and `run(argv, repo=ROOT)` (`:900`). The repository is therefore the sandbox clone, not the lane or the host repo.
- Argv from the judge: `--revision <selector> --branch master` (`check-revision-binding.py:360-363`; `EXTRA["check-recheck-commands.py"] == ()` at `:74`). argparse accepts it (`:878-897`).
- Only `forbid_list(DEFAULT_FORBID)` runs before bind (`:916`). It is valid, so it cannot intercept.
- `_revision.bind(repo, args.revision, branch)` (`:918`):
  - `validate_branch("master")` passes (`_revision.py:84-95`). `REV` 7-64 hex passes (`:175`).
  - `_object_commit` (`:112-146`): `--disambiguate` returns exactly one oid (`:119-124`), and `cat-file -t` returns `tag` (`:127-137`).
  - The peel `rev-parse --verify --quiet --end-of-options <oid>^{commit}` fails, because the tag→tree chain ends at a tree. The repository check passes, so the function returns `None` (`:139-145`).
  - `bind` raises `RevisionError(E-REVISION-INVALID, "revision", "<sel> does not name one commit")` (`:177-179`). This happens before the branch, landed and pushed checks.
- Consumer handler (`:919-921`): `tip = _revision.branch_tip(...)` is informational only. The error is re-raised as `Cannot(fid, site, detail)` and caught at `:930-934`. `emit("CANNOT_EVALUATE", sha or args.revision, ...)` then produces:
  - exactly one finding;
  - `revision` equal to the selector string verbatim (`sha` is still None);
  - `origin_tip` null and every count 0 (`:771-790`);
  - exit 2 via `:795`.
- Path expansion, `read_git`, `--exec-log` and `evaluate` (`:923-966`) are unreachable on this path.

Predicted consumer result for both selectors (full tag-object ID and the unique prefix): exit 2, `status` CANNOT_EVALUATE, `findings == [{"id":"E-REVISION-INVALID","site":"revision","detail":"<sel> does not name one commit"}]`, `revision == <sel>`. This matches the build oracle's expectation (`Oracle08TagTree.md:37-46`) in every field.

## C2 `tag_to_tree` row (candidate `check-revision-binding.py`)
- Typed object, independently created: `tree = rev-parse <tip>^{tree}`, with a guard that the tree is non-empty (`:677-682`). `tag("tree", tree)` runs `git tag -a r21-target-check-recheck-commands-tree -m tree <tree>` and takes `ref^{tag}` as the object ID (`:685-695`, `:701`). It does not use the binder under test.
  - Limit: there is no construction self-check (`cat-file -p` containing `type tree`). Fidelity rests on `git tag -a` semantics.
- Exact refusal: `refused(..., ID_INVALID, branch)` (`:722`) requires `code == 2` and a first finding id of E-REVISION-INVALID (`:383-393`). The row then also requires `binding_ids == [E-REVISION-INVALID]` and `finding_count == 1` (`:723-725`).
  - The echoed 40-hex `revision` is not graded as acceptance: `refused` does not use `json_revision` in `ok`.
  - For the consumer path above, both observations are predicted `ok=True`.
- Fresh sandbox: each `target_type_measure` call creates one new `TemporaryDirectory` clone (`:743-747`), shared serially by the nine tools.
  - Remote: `--no-tags` clone (`:220`), `origin` removed, and `refs/remotes/origin/<branch>` recreated at the tip (`:238-241`).
  - Tag refs: per-tool names (`:686`), refused if they already exist (`:688-689`), deleted in `finally` (`:734-736`).
  - Objects from earlier tools stay in the object store, unreachable. The inventory (`:705-707`) is taken after all five fixture tags exist, so the uniqueness test counts them.
- Unique prefix sanity: the shortest width in 7..39 that is unique across `cat-file --batch-all-objects` and has no colliding `refs/heads/` or `refs/tags/` name (`:711-715`). If none exists, the result is `Cannot(E-SANDBOX)` (`:716-717`), which is CANNOT, never green.
- No host read:
  - On this path the consumer touches git only through `_revision._git`/`validate_branch`, which use `clean_env()`. That function strips `GIT_*` and then sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` (`_revision.py:62-66`, `:71-73`, `:89-91`).
  - The repository is the sandbox (`ROOT`), the working directory is the sandbox (`check-revision-binding.py:364`), and the judge's subprocess env is `clean_env()` (`:365`, `:100-104`).
  - Continuity observation, outside this class and not new coverage: the consumer's own `git()` (`check-recheck-commands.py:798-801`) strips `GIT_*`, which includes the judge's `GIT_CONFIG_GLOBAL=/dev/null`, and does not re-isolate config. Accepted paths therefore read host `~/.gitconfig` and `/etc/gitconfig`. That affects the commit-tag and nested rows (via `expand_paths`/`read_git`), not `tag_to_tree`, which refuses before `:923`.
- Build oracle comparison: the row exercises 2 of the oracle's stated selector variants, the full ID and a unique prefix (`Oracle08TagTree.md:37-49`). It does not exercise the other five: uppercase, `--branch nosuch`, origin lag, nested tag→tag→tree, and ref-shadow (`:50-54`).

## Mutant analysis (proposed, NOT executed)
- **Generic peel, killed.** Change `_revision.py:140` from `^{commit}` to `^{}`, which is the candidate's own `target-generic-peel` stub (`check-revision-binding.py:986-989`).
  - Tag→tree then yields the tree oid, which reaches `_ancestor` (`_revision.py:156-160`).
  - Whatever `merge-base --is-ancestor <tree>` returns, the row fails. rc ≥ 2 gives E-GIT-FAILED, rc 1 gives E-REVISION-NOT-LANDED, and rc 0 is accepted with exit ≠ 2. The finding-id check at `:383-393` rejects all three. The kill is robust to the inferred git exit code.
- **Accept-tag-without-peel, killed.** Return the tag oid when `object_kind == "tag"`. `merge-base` on a tag→tree either errors or produces a non-INVALID id, and the row fails.
- **Concrete surviving mutant M3, a false-green surface of this row.** At `_revision.py:143` (after the failed peel at `:141`), insert:
  `alias = _commit(repo, revision); if alias is not None: return alias`.
  This is a ref fallback after a confirmed-tag peel failure, and it violates the docstring invariant at `:115-117` ("never by reparsing that full hex as a ref").
  - Suppose the selector is a unique prefix P of the tag→tree object, and `refs/heads/P` or `refs/tags/P` names a landed commit. Then `P^{commit}` resolves through the ref [INFERENCE: git dwim_ref precedes the short-hex lookup in `get_oid_basic`]. M3 returns the decoy, bind succeeds, and the consumer goes on to read files and exits 0 or 1 with `revision` set to the decoy.
  - The candidate row never builds that state. It chooses P only when neither ref exists (`check-revision-binding.py:713-714`), and for the full 40-hex ID the object wins over a same-named ref [INFERENCE: 40-hex `get_oid_hex` fast path]. So under M3 both row observations still refuse with exactly one E-REVISION-INVALID: the row stays green.
  - Every other candidate surface also misses M3:
    - The old object-selector matrix has no tag→noncommit selector. Its shadows use only the tip and tag→commit (`:597-626`).
    - `nonempty_tree` returns before the tag branch (`_revision.py:136-137`).
    - `tag_to_blob` has the same unshadowed construction.
    - The commit-tag rows peel successfully, so M3 is inert there.
    - The binder selftest `annotated-tag-to-tree-invalid` uses the full ID with no shadow (`_revision.py:413-418`).
  - The build oracle names exactly this variant ("Ref-shadow: `refs/heads/<S>` and `refs/tags/<S>`", `Oracle08TagTree.md:54`) and this mutant (M3, `:73-76`). The candidate did not carry it into `target_type_probes`.
- Verdict on the actual frozen code: no product defect. The frozen binder returns None at `_revision.py:143-145`, so check-recheck-commands.py refuses correctly.
- Verdict on the control: the row is a valid control for the peel-type class (generic peel, tag passthrough, wrong id, multiple findings, accept with exit ≠ 2). It is not a control for M3, the ref fallback after peel failure.
- Smallest repair, proposed and not implemented: add a shadowed tag_to_tree prefix observation. Create `refs/heads/<prefix>` and `refs/tags/<prefix>` pointing at the tip or a landed decoy, and expect exactly one E-REVISION-INVALID. This mirrors the existing `create_ref`/`remove_ref` shadow pattern at `:604-615`.

## Old matrix and C2 accounting
- Old matrix unchanged [INFERENCE from source shape, not a byte diff]:
  - `object_selector_probes` starts at line 475 in both the snapshot and the candidate, and spans the same lines (snapshot `measure` and candidate `target_type_probes` both start at 676).
  - The case-key grep count differs by exactly the 3 new `target_type` references (39 → 42).
  - `target_type_measure` is a separate mode (`:739-780`, selected at `:1391-1397`) that does not call `probe_tool` or `object_selector_probes`.
- Mode accounting: `target_type_mode = int(available)` is counted once (`:773`), and the behavioral count is separate (`:764-767`). The selftest asserts that a missing mode gives `(0, TOTAL)` (`:1251-1254`). The C2 mode change from 0 to 1 is therefore +1 availability, not a ninefold behavioral uplift.
- The consumer behaviour for tag_to_tree is predicted correct at baseline too: the same shared binder is pinned in `snapshot/tools/_revision.py`, with the same digest. The candidate witness (`:1239-1259`) mutates only stub `TOOLS[0]`, not this consumer.
- `annotated_tag_to_commit` for this consumer is continuity with the old `annotated_tag_object`, not new coverage.

## Limits
- NO-EXEC: no run of the judge, the consumer, git or the mutant. Git exit codes and ref-versus-short-hex precedence are [INFERENCE].
- SHA256 values were cited, not recomputed.
- The fixture's tag target type is not self-checked by the judge.
- Prior source-only reviewers, including Oracle08TagTree, are not outside closure. No non-author closure or promotion is claimed.
- Tooling: none installed; none needed.

Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
