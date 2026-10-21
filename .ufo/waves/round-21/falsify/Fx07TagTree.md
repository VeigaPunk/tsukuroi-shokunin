# Fx07TagTree — falsify check-freshness-r17.py × tag_to_tree (candidate control, source-only)

Reviewed-SHA256: 836ade1b23ed459b922d8c680d2bbbb87d7abb4e6af7c84265e2ab1cffa01668
Predicate: check-freshness-r17.py-tag_to_tree-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Primary file: `.ufo/waves/round-21/candidate/tools/check-freshness-r17.py` (candidate revision 0a14952b59d20179e1c813af58befaecd6992a17; SHA-256 taken from `candidate-files.json` line 61, not recomputed under NO-EXEC).
Auxiliary snapshot dependencies (read only, cited by inventory digest, not bound by this receipt):
- `candidate/tools/_revision.py` sha256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
- `candidate/tools/check-revision-binding.py` sha256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6
- Baseline comparison: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py` (old matrix, grep only)
- Build oracle: `.ufo/waves/round-21/build/Oracle07TagTree.md`

## Axes
- A1 consumer bind/argv propagation for a tag→tree selector
- A2 consumer error→output propagation (exit, findings, JSON fields)
- A3 candidate `target_type_probes` row `tag_to_tree`: actual typed object, exact refusal id/count, selectors (full + unique prefix), fresh sandbox, no host read
- A4 agreement with build oracle Oracle07TagTree
- A5 mutant kill / false-green search
- A6 old matrix unchanged; C2 mode 0→1 is not a behavioral uplift

## Observations (source, read only)
O1 argv/bind (consumer lines 756-778): `args.revision` is passed unchanged to `_revision.bind(ROOT, args.revision, branch)`; `branch = args.branch` (default `master`); `revision` and `tip` are overwritten only after a successful bind. `ROOT = Path(__file__).resolve().parents[1]` (line 55). `import _revision` (line 52) resolves from the script's own `tools/` directory, after `sys.dont_write_bytecode = True` (line 51).

O2 binder path for S = tag→tree (candidate `_revision.py`): `validate_branch` passes; `REV` matches 7-64 hex (lines 41, 175); `_object_commit` (lines 112-146) runs `rev-parse --disambiguate=<S.lower()>`, which returns one oid G. `cat-file -t G` is `tag`, so it peels `G^{commit}` with `--verify --quiet`. A tree cannot peel to a commit, so the peel returns nonzero. `rev-parse --git-dir` succeeds, so the function returns `None`, and `bind` raises `RevisionError(E-REVISION-INVALID, "revision", "<S> does not name one commit")` (lines 177-179). This is before the branch-existence, landing, origin and E-GIT checks (lines 180-191).

O3 error propagation (consumer lines 792-796, 308-322): `RevisionError` becomes `Cannot(fid, site, detail)`, then `emit(Result(CANNOT, [one Finding], 0, 0, None), revision=<raw S>, branch, tip=<pre-bind branch_tip>)`. The output is one sorted-key JSON line with `status` `CANNOT_EVALUATE`, exactly one finding, `resolved_records` 0, `record_count` 0, and no `stale_records`. Exit is 2 via `sys.exit(main())`. No `read_git` runs on this path.

O4 candidate row (`check-revision-binding.py` lines 676-736):
- Typed object: `tree = rev-parse <tip>^{tree}` is the measured commit's real root tree, and it is required to have at least one entry (lines 678-682). `tag("tree", tree)` creates a real annotated tag object over it in the sandbox with `git tag -a` and `tag.gpgSign=false` (lines 685-695, 701), then resolves it through `<ref>^{tag}`. The tag object is freshly created. The tree is not freshly created; it is an existing typed tree. That is enough for the class, because the type is fixed by the tag header (oracle invariant).
- Selectors: the full tag oid plus the shortest 7..39-hex prefix. That prefix must be unique in a `cat-file --batch-all-objects` inventory taken after all four fixture tags exist (lines 705-718), and it must not collide with any `refs/heads/` or `refs/tags/` name.
- Grade: for `expected_commit is None`, the row calls `refused(..., ID_INVALID)` and requires `code == 2`, first finding id `E-REVISION-INVALID`, `binding_ids == ["E-REVISION-INVALID"]` and `finding_count == 1` (lines 721-725, 383-393). Every selector must pass (line 732).
- Fixture cleanup: refs are deleted in `finally` (lines 734-736). Tag names are per-tool (`r21-target-<tool>-tree`), and the code refuses to proceed if one already exists (line 688).

O5 fresh sandbox / no host read: `target_type_measure` (lines 739-781) binds `tools_rev` on the lane, creates a fresh `TemporaryDirectory`, then runs `clone_lane` (`--no-hardlinks --no-tags`, line 220) and `prepare`. `prepare` detaches at tip, sets `refs/heads/<branch>`, removes `origin`, and recreates only `refs/remotes/origin/<branch>` = tip (lines 233-242). `materialize` writes the tools from `tip`, and the detached checkout supplies `tools/_revision.py` at tip.

`run_tool` runs `sandbox/tools/check-freshness-r17.py --revision S --branch master` with `cwd=sandbox` and `clean_env()` (lines 359-371). That environment strips `GIT_*` and sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and `_revision.clean_env` repeats this (lines 62-66). So consumer `ROOT` is the sandbox, and every git call targets the sandbox. `EXTRA["check-freshness-r17.py"]` is `()` (line 73).

O6 old matrix unchanged: the `cases[...]` and `shared_cases[...]` assignments in `probe_tool` and `object_selector_probes` sit at identical line numbers (427-666) with identical names in the baseline snapshot and the candidate. The baseline snapshot has no `def target_type_*` and no `"--object-target-types"` (grep returned no such hits). The new matrix is a separate function and CLI mode (lines 1391-1409). It is mutually exclusive with `--object-selectors` (line 1392).

O7 C2 mode: `target_type_mode = int(available)` is an AST census of function and option presence in the judge at `tip` (lines 748-761, 773). It is reported apart from behavioral `target_type_tools` (`behavior_ok` requires all 5 cases, line 765). The selftest asserts that a missing mode is not a behavior failure: mode 0 and tools = TOTAL (lines 1251-1254). Mode going from 0 to 1 is implementation presence, not a nine-fold behavioral uplift.

## Source predictions (not observed; nothing executed)
- P1: For both selectors (full G and the unique prefix), the consumer exits 2 with `{"status":"CANNOT_EVALUATE","findings":[{"id":"E-REVISION-INVALID","site":"revision","detail":"<S> does not name one commit"}],"revision":"<S>","branch":"master","branch_tip":<tip>,"resolved_records":0,"record_count":0,...}`.
- P2: The `tag_to_tree` row is `ok` for check-freshness-r17.py, so this consumer contributes to `behavior_ok` on this class.
- P3: This matches Oracle07TagTree on exit, status, the single finding id/site/detail, raw `revision` = S, `branch`, `branch_tip` from pre-bind, `resolved_records`/`record_count` = 0, and no `stale_records`. There is no divergence between the source and the oracle.

## Mutant / false-green search (proposed, NOT executed)
- M1 (oracle A5): change the binder tag peel `^{commit}` to `^{}`. `_object_commit` then returns the tree oid T, and `bind` reaches `merge-base --is-ancestor T refs/heads/master`.
  - Exit 0 is impossible for a non-commit. Exit 1 would give E-REVISION-NOT-LANDED; exit ≥2 would give E-GIT-FAILED (lines 156-160).
  - Either way the finding is not `E-REVISION-INVALID`, so the row's exact-id check kills M1. This holds whatever the exact merge-base exit is, which removes the oracle's L2 dependency.
  - The old matrix has no tree or tag→tree row, so M1 survives it (O6). The selftest encodes the same kill with the stub mode `target-generic-peel` (lines 981-989, 1239-1250), but on `TOOLS[0]`, not on this consumer. For this consumer, the kill is a source prediction only.
- M2: route `object_kind in ("tag","tree")` to the peel. The result is still INVALID, so M2 is behavior-equivalent and not a defect.
- M3: return the tag oid itself for tags. merge-base peels tags; for a tag→tree it cannot reach a commit and fails (≥2 gives GIT-FAILED). It is killed here and also by `annotated_tag_to_commit` (accepted revision ≠ tip).
- Residual ungraded fields (a limit, not a defect within this predicate): `refused()` grades only exit, first id, binding ids and count. It does not grade `status`, `revision`, `branch_tip` or `stale_records`; the design choice is documented at lines 482-483 for the old matrix and is reused here. Two consumer-output mutants would survive the row:
  - A consumer that emits `revision` = the peeled tree SHA on refusal.
  - A consumer that prints `"status":"PASS"` while still exiting 2 with the single INVALID finding.
  
  Neither changes the binding verdict. The oracle lists `revision == S` as a SHOULD, not a MUST.

## Verdict
No defect within this predicate. With the frozen consumer and the frozen `_revision.py`, the candidate `tag_to_tree` control has all of the following:
- an actual annotated-tag-to-tree object;
- an exact single `E-REVISION-INVALID` refusal check on the full selector and a unique-prefix selector;
- a fresh clone sandbox with no host-tree or host-config reads.

It kills the realistic `^{}` peel mutant that the unchanged old matrix misses.

## Inferences / limits
- L1: Digests are taken from `candidate-files.json` and not recomputed (NO-EXEC).
- L2: Git exit statuses (`rev-parse --verify --quiet` on a failed `^{commit}` peel; `merge-base` on a tree) are inferred from Git semantics, not observed.
- L3: Whether the candidate tree at 0a14952 actually contains `tools/check-freshness-r17.py` and `tools/_revision.py` for `materialize`/checkout is inferred from the inventory, not observed in a clone.
- L4: The ungraded refusal fields (see above) are an accepted limit of the refusal grader, not new coverage. The commit-tag rows (`annotated_tag_to_commit`, `nested_tag_to_commit`) are continuity with the old `annotated_tag_object`, not new coverage, and are outside this pair.
- No tools were installed or updated.

Scope: executed=none
