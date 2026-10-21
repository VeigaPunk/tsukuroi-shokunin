# Fx09CommitTag — attack: check-seat-scope.py × annotated_tag_to_commit (candidate control)

Reviewed-SHA256: add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac
Predicate: check-seat-scope.py-annotated_tag_to_commit-candidate-control

Primary file: `.ufo/waves/round-21/candidate/tools/check-seat-scope.py` (candidate revision
0a14952b59d20179e1c813af58befaecd6992a17, sha256 add541d8…829dac per `candidate-files.json`).
Auxiliary frozen snapshot dependencies, read but not bound by the receipt above:
- `candidate/tools/_revision.py`, sha256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
- `candidate/tools/check-revision-binding.py`, sha256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6
- Build-wave context, not a candidate input: `round-21/build/Oracle09NestedTag.md`, `ConnPlanner.md`, and the pinned baseline `round-21/snapshot/tools/check-revision-binding.py`, used only to compare the old matrix.

## Verdict

**The binding path has no defect for this class. The control row does have a concrete false-green.** The
`annotated_tag_to_commit` row (and, through the same construction, `nested_tag_to_commit`)
always expects the commit that is also `refs/heads/<branch>`. So the row cannot tell "emit
the commit the tag peels to" apart from "emit the branch tip". A consumer or binder mutant
that substitutes the branch tip passes this row for both selectors (the full tag object ID and
the unique prefix). The whole `--object-target-types` mode would also count that consumer as
`behavior_ok`. Other controls outside this mode kill the commit-path form of the mutant. No
control at any level kills the tag-path-only form, because every tag fixture in every suite
targets the branch tip. This row continues the existing coverage and is not new coverage.

## Axes

- **Fidelity:** does the row's verdict (exit code ≠ 2 and JSON `revision` equal to the expected full commit) depend on the consumer resolving the tag object rather than some other source?
- **Isolation:** fresh sandbox, a real typed object, a unique prefix, and no host read.
- **Discrimination:** the smallest realistic mutant the row cannot kill.
- **Continuity:** the old matrix is unchanged, and the commit-tag row is not counted as new coverage.

## Consumer propagation (observed in source; predictions are marked)

- Judge argv: `run_tool` runs `[python, sandbox/tools/check-seat-scope.py, --revision <sel>, --branch master, --wave .ufo/waves/round-16/build]` with `cwd=sandbox` and `env=clean_env()` (check-revision-binding.py:359-371, EXTRA at :75).
- Consumer: `main` sets `revision = revision_in` (check-seat-scope.py:659-660), then `collect(wave, revision_in, branch)` (:661). `collect` calls `bind_revision(root, revision, branch)` (:262). On success it uses `sha, tip = bound.sha, bound.branch_tip` (:265), reads `git show <sha>:<wave>/…` and `ls-tree <sha>` (:266-271), and returns `sha` as the displayed revision (:272). `emit` prints `"revision": revision` (:158) and exits with `result.code`: 0 for PASS, 1 for FAIL (:170).
- Errors: `RevisionError` becomes `Cannot(exc.fid, exc.site, exc.detail)` (:263-264) and goes to `emit(Result(CANNOT, [one finding]))` with exit 2 (:663-665). A generic exception becomes `E-INTERNAL` with exit 2 (:666-668). The CANNOT path echoes the raw selector as `revision` (:660, :664). That cannot create a false accept, because `accepted()` requires `code != CANNOT` (check-revision-binding.py:402-404).
- Binder for a tag selector: `bind` → `validate_branch` → `REV` 7-64 hex (_revision.py:174-176) → `_object_commit`. That function runs `rev-parse --disambiguate`, requires exactly one object (:119-124), runs `cat-file -t` (:127-133), takes the `tag` branch, and peels with `rev-parse --verify <oid>^{commit}` (:139-142). Then come the branch ancestry check (:180-185) and the origin ancestry check (:186-191). It returns `Binding(sha, branch, tip, origin)` (:192).
- Prediction for this row (not executed): both selectors give exit 0 or 1 and `revision` equal to the 40-hex `tip`. That matches the `Oracle09NestedTag.md` derivation for the depth-1 case.

## Row construction (target_type_probes, check-revision-binding.py:676-736)

- **Real typed object: yes.** `tag("commit", tip)` runs `git tag -a r21-target-check-seat-scope-commit -m commit <tip>` and takes the object ID from `rev-parse --verify <ref>^{tag}` (:685-695, :697). Git creates it; the binder under test plays no part.
- **Independent expected value: yes.** `expected_commit = tip`, where `tip = bind(lane, tools_rev, branch)` uses the judge's own `object_commit` and `bind` (:139-209, :742) and does not import `_revision`.
- **Fresh sandbox: yes, one per measure call.** `TemporaryDirectory` → `clone_lane` → `prepare` (:743-746). All nine tools share that one clone in sequence. Each tool's tag refs are deleted in `finally` (:734-736), but the dangling tag objects stay in the object database. That is harmless, because `inventory` from `--batch-all-objects` (:705-707) includes them, and `--disambiguate` sees the same set.
- **Unique prefix: yes.** It takes the shortest width in `range(7, 40)` that is unique in the post-creation inventory and has no `refs/heads` or `refs/tags` collision (:711-718). The full ID is checked separately as `selectors[0]` (:710).
- **Accept predicate:** `accepted()` checks `code != CANNOT` and JSON `revision.lower() == expected.lower()` (:396-404). Findings and the status string are not graded. Exit 1 with SCOPE findings is a valid accept.
- **No host repository read: yes.** The consumer's `ROOT = Path(__file__).resolve().parents[1]` is the sandbox (check-seat-scope.py:39), and `_revision` is imported from `sandbox/tools`, which is checked out at `tip` by `prepare` (:234).
- **Limit, host git configuration (side observation, not a false-green):** the consumer's own `git()` filters out every `GIT_*` variable and re-adds only `GIT_OPTIONAL_LOCKS`, `GIT_PAGER` and `LC_ALL` (check-seat-scope.py:173-179). That filter drops the `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` values the judge set. As a result, `read_git` and `tree_paths` read the host's `/etc/gitconfig` and `~/.gitconfig`. The `revision` field comes only from `_revision`, which re-applies `clean_env()` (_revision.py:62-66), so this can at worst cause a false red (CANNOT), never a false green, in this row.

## Concrete false-green (proposed mutants, NOT executed)

**Root cause (observed).** `prepare` sets `refs/heads/<branch> = tip` and origin to `tip` (check-revision-binding.py:233-242). The row tags `tip` and expects `tip` (:697, :703). So `expected_commit == Binding.branch_tip` holds by construction in every run.

- **M2, consumer level.** Change check-seat-scope.py:265 from `sha, tip = bound.sha, bound.branch_tip` to `sha, tip = bound.branch_tip, bound.branch_tip`.
  - Predicted: `annotated_tag_to_commit` stays green for the full and prefix selectors, and so does `nested_tag_to_commit`. The three refusal rows are unchanged, because `bind` raises before the return. So `behavior_ok` stays true for this tool (:765).
  - Killed elsewhere: by the consumer's own selftest `wave-partial`, where `collect(partial)` returns the tip and fails the `got_rev == rev` check (check-seat-scope.py:583-590). Also by the old `probe_tool` `landed-parent` case, `accepted(parent, parent)` (check-revision-binding.py:427), which runs in `measure()` but not in `target_type_measure()`.
- **M1, binder level.** Change _revision.py:192 from `return Binding(sha, …)` to `return Binding(tip, branch, tip, origin)`.
  - Predicted: the new mode reports 9 of 9 behavior passes while every consumer prints the branch tip.
  - Killed elsewhere: by the `_revision` selftest `landed-parent` (_revision.py:235) and by `probe_tool` `landed-parent`.
- **M3, tag path only (a class of mutants that no current control kills).** Any defect that returns the branch tip only when the disambiguated object is a `tag`, while commit selectors stay correct.
  - Every tag fixture in every suite targets the branch tip: _revision.py:299, :353, :362 (nested → tip); check-revision-binding.py:502-509 (old matrix), :564-567, :697, :702; and the consumer selftest has no tags at all.
  - All accept cases for tag selectors therefore expect the tip: old `annotated_tag_object` and `annotated_tag_prefix` (:631-632), new `annotated_tag_to_commit` and `nested_tag_to_commit`, and `_revision` `annotated-tag-full-object-id`, `annotated-tag-object-prefix` and `nested-annotated-tag-object` (:360-365).
  - Predicted: M3 survives the old matrix, the new matrix, the `_revision` selftest and the consumer selftest.
- **Minimal remedy, inside the new function only (the old matrix stays untouched).** Tag a landed commit that is not the tip:
  - resolve `parent = tip^1^{commit}` and raise `Cannot E-SANDBOX` when it is absent;
  - use `commit_tag = tag("commit", parent)` with expected value `parent`;
  - make `nested_tag_to_commit` expect `parent` as well;
  - add a selftest stub that emits the branch tip for tag selectors, and check that the new matrix rejects it. The existing `tip-only` stub (S1, check-revision-binding.py:957-963) already passes both commit-tag rows by construction. It fails only on the refusal rows, which raise `NOT-LANDED` instead of `INVALID`.

## Continuity and counting

- Commit-tag is the same type class as the round-20 cases `annotated_tag_object` and `annotated_tag_prefix` (check-revision-binding.py:631-632). The new row builds a different tag object, but the class is unchanged. This matches `build/ConnPlanner.md:29,71` and `CritBaseline.md:36-39`. **It is continuity, not new coverage.**
- **Old matrix unchanged (observed, partial check).** The case-assignment lines in `probe_tool` and `object_selector_probes` have identical line numbers and keys in the candidate and the pinned baseline (`snapshot/tools/check-revision-binding.py`, :416-666). This was compared by grep only; there is no byte-level diff of the full function bodies.
- **C2 mode 0→1** is an AST presence census (:750-761, `availability_limit` at :780). It is not a nine-fold behavioral uplift. For this cell, `behavior_ok` was already expected to pass at baseline [INFERENCE: neither the consumer nor `_revision` changes in the candidate inventory; not measured].
- **Build oracle comparison.** There is no AnnotatedTag oracle (`ConnPlanner.md:29`). The closest is `Oracle09NestedTag.md`, whose consumer-propagation trace (lines 20-31) matches mine line for line. Its expected depth-1 behavior (accept, `revision` = terminal commit) matches this row's expected value. That oracle does not raise the tip-coincidence blind spot.

## Observations, inferences, limits

- Observed (source reads only): every line citation above, plus the existence of `round-16/build/{spec.json,swarm-registry.json}` in the current worktree.
- Inference: that wave directory is present at the measured revision. If it is absent, the consumer raises `E-SEAT-SOURCE-MISSING` (exit 2) and the row goes red, not green.
- Inference: Git's `^{commit}` peels tags transitively (S081), as the oracle also assumes.
- Limits: no command, test or mutant was executed, so every outcome above is a source prediction. This is author-side source review, not non-author closure or outside promotion. No tools were installed or updated, and none are needed.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none
