# Fx08Tree — falsify check-recheck-commands.py × nonempty_tree (candidate 0a14952)

Reviewed-SHA256: 9dc46f46d322f92578b60027da3d7ea8138d90ef44eeae152531388e6c27e7e9
Predicate: check-recheck-commands.py-nonempty_tree-candidate-control

Primary receipt binds only candidate `tools/check-recheck-commands.py`; SHA-256 is the supplied item value and matches the predispatch declaration in `candidate-files.json:44-47` (not recomputed). Auxiliary candidate snapshots used, also not rehashed:
- `tools/_revision.py`: `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf` (`candidate-files.json:64-67`).
- `tools/check-revision-binding.py`: `0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6` (`candidate-files.json:39-42`).
- Comparison input only: `build/Oracle08Tree.md`; it is not an executed result or closure evidence.

Everything below is source observation or prediction. No consumer, judge, Git command, test or mutant was run; there are no runtime observations.

## Axes and scope

1. Consumer revision binding, refusal ID/cardinality, and emitted JSON/exit.
2. Target-type fixture fidelity, selector uniqueness, and test sensitivity.
3. Sandbox and host-path containment on the selected refusal path.
4. Separation from C2's old matrix and honest mode/behavior accounting.

This is only `check-recheck-commands.py × nonempty_tree`. No production or candidate source was edited. No other review's conclusion is treated as closure.

## Consumer bind/argv/error/output propagation (frozen source)

- Candidate tool imports `_revision` after setting `sys.dont_write_bytecode` (`check-recheck-commands.py:54-58`). The measured tool is launched as `sandbox/tools/<name>` with `--revision <selector> --branch master`, cwd `sandbox`, and no extra args for this tool (`check-revision-binding.py:359-371`, `:74`).
- `run()` parses the supplied branch and, after `forbid_list`, invokes `_revision.bind(repo, args.revision, branch)` before path expansion (`check-recheck-commands.py:900-923`). The default forbid list is nonempty and syntactically valid (`:62`, `:895-897`), so it does not preempt the bind.
- The test judge's `target_type_measure` prepares `refs/heads/master` at the measured tip before probing (`check-revision-binding.py:739-747`; `prepare`, `:233-242`). For this input, `_revision.validate_branch("master")` succeeds; `REV` permits the full hexadecimal tree ID (`_revision.py:41`, `:172-177`).
- `_object_commit` resolves object IDs with `rev-parse --disambiguate`, requires exactly one object, and checks its actual type using `cat-file -t` (`_revision.py:112-137`). For a direct tree, the type is neither `commit` nor `tag`, so it returns `None` (`:134-137`). `bind()` turns that into `E-REVISION-INVALID` before landed/pushed checks (`:172-190`).
- Consumer handling converts that `RevisionError` to `Cannot` (`check-recheck-commands.py:918-921`), catches it at `:930-934`, and emits `CANNOT_EVALUATE` with the raw selector echoed in `revision`; `emit()` produces one serialized finding and maps that status to exit 2 (`:771-795`). The predicted finding is `{id:E-REVISION-INVALID, site:revision, detail:<selector> does not name one commit}`. `expand_paths`, `read_git`, exec-log handling and `evaluate` are unreachable (`:923-966`).

**Prediction for the candidate's full tree SHA:** exit 2; `status=CANNOT_EVALUATE`; exactly one `E-REVISION-INVALID`; `revision` echoes the full tree SHA. `branch_tip` is looked up in the sandbox; the failing bind has no returned `origin_tip`. This matches the tree-type refusal described by the comparison oracle (`build/Oracle08Tree.md:26-47`), as a source prediction only.

## Candidate target-type row

- The judge resolves `tip^{tree}`, runs `ls-tree`, and refuses to proceed if the tree has no entries (`check-revision-binding.py:676-682`). This is a real Git tree object, not a fabricated selector. It is the measured commit's tree rather than a separately written tree fixture; its nonempty condition is checked directly from the object. The judge makes an independent blob with `hash-object` and annotated tags with `git tag -a`, without calling the binder to construct their IDs (`:683-695`, `:408-413`).
- `classes["nonempty_tree"]` supplies `(tree, None)` (`:697-704`). `refused()` checks exit `CANNOT` and the expected first finding ID; the row strengthens this to `binding_ids == [E-REVISION-INVALID]` and exactly one finding (`:383-393`, `:720-725`). The refusal's recorded `json_revision` is not part of its `ok` condition. For accepted target classes, `accepted()` requires a non-CANNOT exit and JSON `revision` equal to the independently expected full commit SHA (`:396-404`, `:726-727`).
- **Unique-prefix gap:** selectors start as `[object_id]`; the prefix-construction branch explicitly excludes `nonempty_tree` (`:709-718`). Thus this row tests only the full tree ID. The code does not check prefix uniqueness for this class, nor a ref-shadowed prefix. Other target classes do select the shortest 7..N-1 prefix unique in the object inventory and absent as a branch/tag (`:711-717`); that is not applied to this tree row.
- The build oracle describes the tree selector contract for full IDs and unique prefixes (`build/Oracle08Tree.md:28-48`). The candidate's new direct-tree case improves on the earlier matrix's blob-only non-commit class, but does not cover the oracle's abbreviated tree selector.

## Finding — minor control false-green on direct-tree abbreviations

The current consumer source correctly rejects a unique abbreviated direct-tree selector too: it lowercases the selector, uses `--disambiguate`, and rejects the resolved `tree` kind (`_revision.py:112-137`). The candidate row, however, does not exercise that form. A concrete **proposed mutant, not executed**, is a ref-fallback bug in `_object_commit`: for `object_kind == "tree"` and a non-full selector, fall back to `_commit(repo, revision)` and accept the resulting landed commit when a branch/tag ref named by that unique tree prefix resolves to it. Keep full tree object IDs rejected. The existing row still probes only the full tree SHA, receives its expected single `E-REVISION-INVALID`, and remains green under this mutant. `object_selector_probes` has prefix/ref-shadow controls for commits and tag objects, but no direct-tree case (`check-revision-binding.py:475-673`); the new row omits the needed tree prefix as well. This mutant violates `_object_commit`'s stated invariant to resolve object IDs directly rather than reparsing the hex as a ref (`_revision.py:112-117`). Ref-name precedence in the hypothetical fallback is **[INFERENCE]**, not exercised here; the same ref-fallback hazard is discussed for tag-to-tree in the comparison-only `build/Oracle08TagTree.md:59-70`.

Smallest control improvement: add a unique direct-tree prefix selector and a ref-shadowed variant (create a branch or tag named by that prefix pointing to a landed commit, then require the same exact refusal). A merely unshadowed prefix tests abbreviated tree typing but would not kill the proposed ref-fallback mutant. This is a predicate/test-coverage finding, **not a defect in the current frozen consumer's tree handling**.

## Sandbox, host reads, continuity and accounting

- `target_type_measure` creates one `TemporaryDirectory` clone per measurement call, prepares that clone, and runs the nine named tools serially in the same sandbox (`check-revision-binding.py:739-767`). This is fresh per measurement, not one fresh clone per tool or class. Target tags are namespaced by tool, checked absent before creation, tracked, and removed in `finally` (`:685-695`, `:734-736`).
- The judge invokes the sandbox copy with sandbox cwd and its `clean_env()` (`:359-371`, `:100-104`). The consumer computes `ROOT` from its sandbox script location (`check-recheck-commands.py:58`) and `_revision.clean_env()` strips inherited `GIT_*`, disables system/global Git config, and uses explicit `git -C <repo>` (`_revision.py:62-77`, `:89-95`). For this selected refusal, bind fails before the consumer's own `git()` helper or knowledge-file reads. Source predicts no host project/knowledge-path read by the consumer on this row. This is not OS process isolation: the judge's own trust-boundary documentation says subprocesses retain caller filesystem/network authority (`check-revision-binding.py:49-53`).
- `annotated_tag_to_commit` is continuity with the old matrix's `annotated_tag_object`/prefix acceptance (`check-revision-binding.py:629-632`, `:697-704`), not new coverage.
- New-mode selection is separate: `main()` routes `--object-target-types` to `target_type_measure` (`:1391-1409`), while the original `measure()` and `object_selector_probes()` are on the ordinary mode route (`:1410-1422`, `:783-883`). This supports additive routing in the candidate source. No pinned baseline source file was supplied among the permitted candidate snapshots, so byte-for-byte old-matrix invariance is not independently established here.
- `target_type_mode` is `int(available)` and is counted once; `behavioral_tools` separately counts tools whose five target-type rows all pass (`:758-780`). Therefore a C2 mode 0→1 is one availability-mode change, not a ninefold behavioral uplift.

## Residual risk and verification gaps

- The row checks refusal exit, ID set and count, but does not grade `status`, finding `site`/`detail`, or the echoed refusal `revision` (`refused`, `:383-393`; row, `:720-725`). The consumer source predicts these fields correctly; they are not row assertions.
- No execution means the predicted stdout, exit status, Git object inventory and proposed mutant result are not observed. Prefix/ref behavior in the mutant analysis is explicitly inferred.
- Candidate SHA declarations were cited from the supplied inventory, not recomputed. `build/Oracle08Tree.md` and sibling reviews are comparison material only, not closure. No outside promotion or non-author closure is claimed.
- No tools were installed or updated; none was needed for this source review.

Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none