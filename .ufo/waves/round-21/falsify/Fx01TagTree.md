# Fx01TagTree — falsify: check-locator-clarification.py × tag_to_tree (candidate control)

Reviewed-SHA256: cd24d07ce71e3a3c5cff92802b69f3b2630aa5942a437ad00e53469387b05814
Predicate: check-locator-clarification.py-tag_to_tree-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Candidate revision 0a14952b59d20179e1c813af58befaecd6992a17. The primary receipt binds only
`candidate/tools/check-locator-clarification.py` (sha256 cd24d07c…05814 per `candidate-files.json:19-22`).

Auxiliary snapshot dependencies (read only, not bound by the receipt):
- `candidate/tools/_revision.py`, sha256 06b71e8c…cbf (`candidate-files.json:63-67`). This is the same digest as the preregistered pinned binder (`preregister.json:50-52`), so the binder is unchanged this round.
- `candidate/tools/check-revision-binding.py`, sha256 0722537d…6fa6 (`candidate-files.json:39-42`).
- `snapshot/tools/check-revision-binding.py`, sha256 da000de4…9e0 (`preregister.json:46-48`). Used only for the old-matrix continuity comparison.
- `build/Oracle01TagTree.md`, the build oracle. Used for comparison only, never as a candidate verdict input.

## Axes
- **A1 consumer propagation:** how the selector string reaches the binder (bind/argv) and how the refusal propagates back (error → finding → JSON → exit).
- **A2 judge row fidelity:** whether the actual typed object is independently constructed; the exact refusal id and count; prefix uniqueness; a fresh sandbox; no host read.
- **A3 discrimination:** which mutants the cell kills, and which survive.
- **A4 continuity and metric honesty:** the old matrix is unchanged; commit-tag is not counted as new coverage; mode 0→1 is not a behavioral uplift.

## A1 — Consumer propagation (source observations, frozen candidate)
- **O1:** `import _revision` (line 19) resolves from the script directory. `ROOT = Path(__file__).resolve().parents[1]` (line 24). Under the judge, the script runs as `<sandbox>/tools/check-locator-clarification.py`, so `ROOT` is the sandbox clone, not the host lane. `_revision.py` comes from the sandbox worktree, which is checked out at the measured tip (judge `prepare`, lines 233-242). `materialize` writes only `TOOLS` (lines 259-274).
- **O2:** `build_parser` (lines 472-481): `--revision` is mutually exclusive with `--selftest`, and `--branch` defaults to `master`. The judge's argv is `--revision <sel> --branch master`, with `EXTRA[name] == ()` (judge lines 359-366 and 78).
- **O3:** In `main` (lines 780-790), `_revision.bind(ROOT, args.revision, branch)` receives the raw selector. On `RevisionError`, the consumer does three things:
  - sets `tip = _revision.branch_tip(ROOT, branch)` (never raises: `_revision.py:163-169`);
  - sets `revision = args.revision`;
  - raises `Cannot(exc.fid, exc.site, exc.detail)`. The outer `except Cannot` at lines 793-795 catches it and emits `Result(CANNOT, [one Finding], 0)`.

  `read_git` and `evaluate` are never reached.
- **O4:** `emit`/`payload` (lines 427-436) print one sorted-key JSON line with `status`, `revision`, `branch`, `branch_tip`, `correction_count` and `findings`. `sys.exit(main())` exits 2 (line 808).
- **O5:** Binder path for a tag→tree selector (`_revision.py:172-179`, `112-146`):
  1. `validate_branch("master")` passes.
  2. The selector matches `REV`.
  3. `--disambiguate` returns exactly one object, and `cat-file -t` reports `tag`.
  4. `rev-parse --verify --quiet --end-of-options <oid>^{commit}` fails, `rev-parse --git-dir` succeeds, and the function returns `None` (lines 139-146).
  5. The result is `RevisionError(E-REVISION-INVALID, "revision", "<sel> does not name one commit")`. The branch, landed and pushed checks are never reached.
- **O6:** No host Git config is read on this path. Every git call made by `_revision` uses `clean_env()`, which strips `GIT_*` and then sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` (lines 62-66, 70-73, 88-91). The consumer's own `git()` (lines 447-456) strips the judge-supplied `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_NOSYSTEM` without re-adding them. However, it runs only in `read_git`, which this refusal path never reaches.

**Prediction from source (not observed):** for both the full tag OID and a unique ≥7-hex prefix, the consumer exits 2 with one finding, `{"id":"E-REVISION-INVALID","site":"revision"}`, and `revision` equal to the raw selector.

## A2 — Judge row `target_type_probes` (candidate `check-revision-binding.py`)
- **Independently created actual typed object.** `tree = rev-parse <tip>^{tree}`; `ls-tree` must be non-empty, otherwise `Cannot` (lines 678-682). `tag("tree", tree)` runs `git tag -a r21-target-check-locator-clarification-tree -m tree <tree>` with a fixed identity, `tag.gpgSign=false` and hooks set to /dev/null (lines 107-112). The object ID is read back with `rev-parse --verify <ref>^{tag}` (lines 685-695, 701).
  - The tag name embeds the tool name, so this tag object differs from the other eight consumers' objects.
  - Limit: the judge never asserts `cat-file tag <oid>` has `type tree`. The target type follows from construction (an annotated tag of a tree OID). [INFERENCE: standard `git tag` behavior; not executed]
- **Exact refusal id and count.** Lines 720-725 use `refused(..., ID_INVALID, branch)`, which requires exit `== 2` and a first finding id of `E-REVISION-INVALID` (lines 383-393, 349-356). The row then additionally requires `binding_ids == ["E-REVISION-INVALID"]` and `finding_count == 1`. Both the full OID and the prefix selectors must pass (lines 710-732).
- **Unique prefix sanity.** The inventory is taken with `cat-file --batch-all-objects` after all five fixtures exist (lines 705-707). The chosen prefix width is 7–39, appears exactly once in the inventory, and collides with no `refs/heads/<p>` or `refs/tags/<p>`. If no such prefix exists, the judge raises `Cannot` and fails closed (lines 712-718). The consumer's binder selects objects first (`--disambiguate`), so ref collisions cannot change its answer anyway.
- **Fresh sandbox.** `target_type_measure` uses a new `TemporaryDirectory`, `clone_lane` (`--no-tags --no-hardlinks`) and `prepare`: detached checkout, the remote removed, only `refs/remotes/origin/master` recreated at the tip (lines 739-746, 218-242).
  - `check-locator-clarification.py` is `TOOLS[0]` (line 62), so it is probed first, before any other consumer's fixture objects exist.
  - Fixture refs are deleted in `finally` (lines 734-736). The unreferenced tag objects stay in the database and are counted by later prefix inventories.
  - A pre-existing fixture tag raises `Cannot` (lines 688-689).
- **No host read.** The tool runs with `cwd=sandbox` and `env=clean_env()` (lines 362-366), and its `ROOT` is the sandbox (O1). The only host access is the judge's own lane clone, which is inherent to measuring.
  - Limit: the host `PYTHONPATH`/`PYTHONSAFEPATH` pass through. If `PYTHONSAFEPATH` were set, `import _revision` would fail with exit 1, and the row would fail closed (red, not green). [INFERENCE]

**Verdict for the graded predicate:** the candidate row matches the consumer's source-predicted output. It grades exit 2 plus exactly one `E-REVISION-INVALID` for the full and unique-prefix selectors of a freshly built tag→tree object. **No false green found within this predicate.**

## A3 — Mutants (proposed, NOT executed; outcomes are source predictions)
| Mutant | Location | tag_to_tree row | Old matrix |
|---|---|---|---|
| Oracle M1: drop the `repo_check` guard so a failed peel raises E-GIT-FAILED | `_revision.py:143-146` | killed (finding E-GIT-FAILED, not INVALID) | survives |
| Oracle M2 / selftest `target-generic-peel`: `^{commit}` → `^{}` | `_revision.py:139-140`; stub at judge lines 981-989 | killed: tree OID → `merge-base --is-ancestor` exits ≥2 → E-GIT-FAILED [INFERENCE on the rc] | survives (old matrix lines 629-633 have no tag→noncommit case) |
| **M-tree-only:** generic peel, then return `None` only when the peeled type is `blob` | `_revision.py:139-146` | killed (E-GIT-FAILED) | survives; `tag_to_blob` **also survives**, so tag_to_tree is the sole killer |
| Consumer collapses every RevisionError to INVALID | consumer line 788 | survives this cell | killed by the unlanded, not-pushed and branch-* rows |
| **M-echo:** `revision = args.revision` → `revision = tip` (or the peeled OID) | consumer line 786 | **survives** | **survives** (`exact_refusal`, lines 480-485, deliberately does not grade `revision` on CANNOT) |

Findings from these mutants:
- **F1 (discrimination; calibration note, not a defect).**
  - The only class of mutant that this cell kills and `tag_to_blob` does not is a binder that admits trees, such as M-tree-only. Those mutants live in the shared `_revision.py`, so they flip all nine consumer cells together (common mode).
  - For this consumer alone, the cell adds coverage of the binder's tag-peel-failure branch, reached through the consumer CLI. It adds no consumer-local propagation check beyond what `noncommit_blob`/`blob-revision` plus `strict-refusals` already grade.
  - The selftest witness (lines 1239-1259) uses `target-generic-peel`, which `tag_to_blob` also kills. `"new_matrix_kills"` is keyed to tag_to_tree, but the witness does not show tag-to-tree-specific discrimination. M-tree-only would be the specific witness.
- **F2 (oracle-vs-candidate gap; concrete surviving mutant).** `build/Oracle01TagTree.md:48-58` expects all of the following, and the candidate row grades none of them:
  - `status:"CANNOT_EVALUATE"`;
  - `correction_count:0`;
  - `site:"revision"`;
  - `revision` that echoes the selector and is "not the expanded tag OID, the tree OID T, or any commit SHA";
  - `branch_tip` equal to the master tip.

  `refused()` records `json_revision` (line 392) but leaves it out of `ok`. M-echo would therefore pass the new and old matrices while emitting a refusal whose JSON `revision` is a commit SHA. This is a gap against the oracle, not against the candidate's declared contract (exit, id and count). The exit-2 status still signals refusal.
- **F3 (oracle precedence not exercised):** the oracle's precedence rows (tag_to_tree with `--branch nosuch` → INVALID; lagging or blob origin with no effect) are not probed by this cell, which uses only `branch="master"` with origin at the tip. The binder's own selftest covers the precedence generically.

## A4 — Continuity and metric honesty
- **Old matrix unchanged** (structural evidence, not a byte diff): `probe_tool` and `object_selector_probes` case names and line positions 416-673 are identical between snapshot and candidate (the two grep listings match). The new code is inserted at lines 676-780, before `measure`, and `measure`'s object-selector path never calls `target_type_probes`.
- **Commit-tag continuity:** `annotated_tag_to_commit` (line 703) overlaps the old `annotated_tag_object`/`annotated_tag_prefix` (lines 631-632). It is preserved continuity, not new coverage.
- **C2 mode 0→1 is not a behavioral uplift.** `target_type_tools` is the behavioral count, `== behavioral_tools`, independent of `target_type_mode` (lines 767-774). The candidate selftest asserts mode 0 with tools == TOTAL on a fixture lacking the mode (lines 1251-1254).
  - So, measured by the candidate judge, a baseline whose consumers are already correct would report `target_type_tools` 9 with mode 0 [INFERENCE: not executed].
  - The preregistered "before 0" (`preregister.json:21-25`) is therefore a judge-mode presence fact: the baseline judge lacks `--object-target-types`. It is not nine consumer improvements.

## Limits
- Nothing was executed: no git, Python, selftest or mutant was run. All outcomes are predictions from the frozen source. The digests are the inventory and item values and were not recomputed.
- No LSP device was available in this seat. Definitions and callers were traced by literal grep and direct reads of the frozen files, so this is not semantic proof.
- Git behaviors taken as [INFERENCE]:
  - `merge-base --is-ancestor <tree>` exits ≥2;
  - `rev-parse --disambiguate=<40-hex>` lists the single object;
  - `git tag -a` on a tree writes `type tree`.
- No claim of non-author closure or outside promotion.
- No tool was installed or updated, and none was needed.

Scope: executed=none
