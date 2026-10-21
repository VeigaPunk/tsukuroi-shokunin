# Fx09TagTree — falsify check-seat-scope.py × tag_to_tree (candidate 0a14952b)

Reviewed-SHA256: add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac
Predicate: check-seat-scope.py-tag_to_tree-candidate-control

The primary file is `.ufo/waves/round-21/candidate/tools/check-seat-scope.py`. The digest above is the one the item supplied, and it matches `candidate-files.json` at `tools/check-seat-scope.py`. I did not recompute it, because this seat is NO-EXEC.

Auxiliary frozen snapshot dependencies, which I read but which this receipt does not bind:
- `candidate/tools/_revision.py`: sha256 `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf` per `candidate-files.json`.
- `candidate/tools/check-revision-binding.py`: sha256 `0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6` per `candidate-files.json`.

Comparison inputs, which are not candidate verdict sources:
- `build/Oracle09TagTree.md`
- `snapshot/tools/check-revision-binding.py`
- `snapshot/tools/_revision.py`
- `snapshot/tools/check-seat-scope.py`

I did not read any moving draft or production files.

## Verdict
For check-seat-scope.py × tag_to_tree, I found no binding defect and no binding false-green within the candidate predicate. The consumer passes the binder's refusal through unchanged, as exactly one `E-REVISION-INVALID`, exit 2, and the binder can never return a commit for a tag that targets a tree. The candidate row grades the exit code, the first finding ID, the binding-ID list (which must equal `[E-REVISION-INVALID]`) and the finding count (which must be 1). It covers both the full tag ID and a unique 7–39 hex prefix.

One divergence from the build oracle is in scope and recorded below. The candidate row does not grade the oracle's conjunct that the `revision` echo is neither the tree ID nor any commit. I give a concrete surviving mutant, ME, that I did not execute. It is a gap in the display echo, not a false-green on binding.

## Axes
- A1: how the consumer passes argv, binds, and propagates errors to output.
- A2: why the binder's type decision for a tag that targets a tree is correct.
- A3: whether the judge row's fixture is independent, its expected value fixed, its sandbox fresh, and its prefix unique.
- A4: whether the run avoids host reads.
- A5: which mutants the row kills and which survive.
- A6: matrix continuity and how to read the mode result.

## A1: what the consumer does (observed in source)
- argv: judge `run_tool` (`check-revision-binding.py:359-371`) runs `python <sandbox>/tools/check-seat-scope.py --revision <selector> --branch master --wave .ufo/waves/round-16/build`.
  - The wave comes from `EXTRA`/`R17_GATES` at `:71-78`.
  - The branch is `master` from the `target_type_measure` default (`:739`), passed to `target_type_probes` at `:764` and then to `refused(..., branch)` at `:722`.
  - The environment is `clean_env()`, cwd is the sandbox, and stdin is DEVNULL.
- Parsing: `build_parser` (`check-seat-scope.py:226-238`) and `args_issue` (`:241-247`) return None because `--wave` is present.
  - `wave_key` (`:186-193`) accepts `.ufo/waves/round-16/build` under the `WAVE` regex at `:46`. This happens before the bind (`:658`), so an invalid wave can't hide the binding verdict.
  - The `revision = revision_in` assignment at `:659-660` stores the selector exactly as typed.
- Bind: `collect` (`:260-264`) calls `bind_revision(root=ROOT, revision, branch)`. `ROOT` is `Path(__file__).resolve().parents[1]` (`:39`), which is the sandbox.
  - A `RevisionError` becomes `Cannot(exc.fid, exc.site, exc.detail)` with nothing added or dropped.
  - No wave read (`read_git` or `tree_paths`) happens before the bind succeeds (`:265-271`).
- Output: `main` (`:663-665`) emits `Result(CANNOT, [Finding(fid, site, None, detail)], 0)`.
  - `emit` (`:151-170`) prints one JSON line: `status: CANNOT_EVALUATE`, `counts[E-REVISION-INVALID]: 1` (added via `counts.get`, because the ID is not in `IDS`), `findings` with length 1, `revision` equal to the selector as typed, `branch_tip: null` and `seat_count: 0`. The return code is 2.
- Import: `from _revision import ...` (`:36`) resolves to `<sandbox>/tools/_revision.py`.
  - Correction to the oracle: `Oracle09TagTree.md` A1 says `materialize` copies `_revision.py`. In fact `materialize(sandbox, tip, TOOLS)` (`:747`, body `:259-274`) copies only the nine `TOOLS`. `_revision.py` comes from `prepare`'s `checkout --detach tip` (`:233-234`).
  - The outcome is the same, since the module is still the measured commit's version. Only the oracle's stated mechanism is wrong.

## A2: binder decision (observed in source; outcome predicted)
`_revision.bind` (`:172-192`) runs these steps in order:
1. `validate_branch("master")` passes.
2. `REV.fullmatch` passes: 40 hex for the full ID, 7–39 hex for the prefix.
3. `_object_commit` (`:112-146`):
   - `rev-parse --disambiguate=<lower>` finds exactly one object.
   - `cat-file -t` returns `tag`.
   - `rev-parse --verify --quiet --end-of-options <oid>^{commit}` exits non-zero, because a tag that targets a tree has no commit to peel to.
   - `rev-parse --git-dir` succeeds, so the function returns None.
4. `bind:178-179` then raises `RevisionError(E-REVISION-INVALID, "revision", ...)`. Steps 4–6 (`E-BRANCH-MISSING`, `NOT-LANDED`, `NOT-PUSHED`, `GIT-FAILED`) can't run.

The candidate `_revision.py` matches the snapshot on the type-decision lines: `object_kind` at `:133-136`, `^{commit}` peel at `:140`, and selftest `annotated-tag-to-<label>-invalid` at `:417`. I compared only these lines.

## A3: the judge row (observed in source)
- Typed object: `target_type_probes` (`:676-736`) creates the object independently.
  - `tree = rev-parse <tip>^{tree}`, and `ls-tree` must return entries (`:677-682`).
  - `tag("tree", tree)` runs `git tag -a r21-target-check-seat-scope-tree -m tree <tree>` and resolves `ref^{tag}` to the tag object ID (`:685-695`).
  - Before creating the tag it checks the ref doesn't already exist (`:688-689`). The ref is deleted in `finally` (`:734-736`).
- Expected value: `(tag_oid, None)` at `:701` sets the expected result to a refusal when the fixture is built. Neither the binder under test nor the judge's own `bind` is used to derive it.
- Refusal grading (`:721-725`):
  - `refused(...)`, which requires `exit == 2` and the first finding ID `== E-REVISION-INVALID` (`:383-393`),
  - AND `binding_ids == [E-REVISION-INVALID]`,
  - AND `finding_count == 1`.
- Selectors: the full ID, plus a prefix `object_id[:w]` for `w` from 7 to 39 (`:711-718`).
  - The prefix must match exactly one entry in the inventory, and no `refs/heads/<p>` or `refs/tags/<p>` may exist.
  - The inventory is taken after all five fixtures are built (`:705-707`). The loop creates no new objects, and on refusal the consumer writes none, so the uniqueness check is still valid when the consumer runs.
- Fresh sandbox:
  - `target_type_measure` makes one `TemporaryDirectory` clone per measurement (`:743-746`).
  - `prepare` removes the origin remote and pins `refs/heads/master` and `refs/remotes/origin/master` to the tip.
  - It is not fresh per tool. check-seat-scope is the 9th `TOOLS` entry (`:79`), so it runs after eight earlier tools' tag objects, which are now unreferenced but still in the object store. Those objects are counted in `inventory`, so prefix uniqueness still holds. This is a limit, not a defect.
- Status: this is a source prediction only. I have not observed any real `--object-target-types` run, or any receipt of one, for this consumer. The candidate selftest runs `target_type_probes` only against the stub `TOOLS[0]` (`:1234-1250`), never against check-seat-scope.

## A4: no host read (observed in source)
- The refusal path reads only the sandbox.
  - `_revision._git` and `validate_branch` use `clean_env()` with `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` (`_revision.py:62-66`).
  - The judge's `run_tool` also passes `clean_env()`.
  - `ROOT` is the sandbox, and its origin remote has been removed.
  - `sys.dont_write_bytecode` (`:35`) stops a `__pycache__` write.
- Adjacent, outside this class: the consumer's own `git()` (`check-seat-scope.py:173-183`) does not set `GIT_CONFIG_NOSYSTEM` or `GIT_CONFIG_GLOBAL`. So on accepted rows, `read_git` and `tree_paths` would read the host's system and global git config. tag_to_tree never reaches that code.
- Python start-up reads, such as site-packages, are not covered by this review.

## A5: mutants (none executed)
Killed by this row (predicted):
- M1, the oracle's: change `_revision.py:140` from `^{commit}` to `^{}`.
  - The tree ID becomes `sha`. Then `_ancestor` runs `merge-base --is-ancestor <tree> refs/heads/master`. [INFERENCE] That exits 128 or higher and raises `E-GIT-FAILED`. The row expects `E-REVISION-INVALID`, so it fails and the mutant is killed.
  - The candidate's analogous stub `target-generic-peel` (`:981-989`) is witnessed only on the stub, by `tree-tag-mutant-new-matrix-rejects` (`:1246-1250`).
- M2: change `:141-146` to raise `E_GIT` on any peel failure. The finding ID becomes `E-GIT-FAILED`, so the mutant is killed.
- Any consumer mutant that adds a second finding, or swallows the `RevisionError` into a `SCOPE-*` result or exit 0/1, is killed by the `finding_count`, `binding_ids` or exit checks.

Survives the candidate row but fails the oracle predicate:
- ME: in `check-seat-scope.py:659-660`, replace `revision = revision_in` with `revision = git(ROOT, "rev-parse", "--verify", "--quiet", revision_in + "^{}").stdout.decode().strip() or revision_in`.
- Predicted effect for tag_to_tree: exit 2, exactly one `E-REVISION-INVALID`, and `revision` set to the tree ID.
  - The candidate `refused` records `json_revision` but never grades it (`:390-393`).
  - `target_type_probes` adds only the `binding_ids` and `finding_count` checks (`:723-725`), so the row passes.
- `Oracle09TagTree.md` A3's pass predicate requires that `revision` is neither the tree ID nor any commit, so ME fails it.
- On accepted rows `revision` is overwritten by `collect`'s return (`:661`). The old matrix deliberately leaves the CANNOT echo ungraded (`:481-485`). So ME survives the whole candidate matrix.
- ME also adds a host-config read through the consumer's own `git()`.
- Classification: the docstring's binding contract does not specify the echo on CANNOT, and no commit is bound. This is an omitted oracle conjunct, not a binding false-green.

## A6: continuity and mode
- Commit-tag continuity: `annotated_tag_to_commit` and the nested case use the same `commit_tag`. For this consumer, the old matrix already had `annotated_tag_object` and `annotated_tag_prefix` accepted at the tip (snapshot and candidate `:631-632`). That is continuity, not new coverage.
- Old matrix unchanged (structural observation only):
  - In both snapshot and candidate, `probe_tool` is at `:416` and `object_selector_probes` at `:475-673`, with identical tail lines `:625-673`.
  - `target_type_probes` and `target_type_measure` are inserted at `:676-781` ahead of `measure`. `measure` itself is 100 lines in both versions (snapshot `:676-776`, candidate `:783-883`).
  - I did not do a byte-level diff.
- Mode: `target_type_mode = int(available)` (`:773`) is a one-time AST census of the judge's own function and option presence. It is reported separately from `behavioral_tools`.
- All nine consumers call the same `_revision.bind`. This row's only independent contribution is check-seat-scope's argv, wave, error and JSON propagation. So C2 mode 0→1 is not a nine-fold behavioural uplift.

## Observations, inferences, limits
- Observed: everything in A1–A4 and A6 comes from reading the frozen snapshots.
- Inferred: the git exit codes for M1, and every runtime outcome. Nothing was executed.
- Limits:
  - No byte comparison between the candidate and production, or between snapshot and candidate, beyond the lines cited.
  - No claim of closure by a non-author reviewer, and no claim of outside promotion.
  - No tools were installed; none were needed.

Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
