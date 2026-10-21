# Fx08TagBlob — check-recheck-commands.py × tag_to_blob (candidate control attack)

Reviewed-SHA256: 9dc46f46d322f92578b60027da3d7ea8138d90ef44eeae152531388e6c27e7e9
Predicate: check-recheck-commands.py-tag_to_blob-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Primary file is the candidate consumer
`.ufo/waves/round-21/candidate/tools/check-recheck-commands.py`, revision
0a14952b59d20179e1c813af58befaecd6992a17. `candidate-files.json` lines 44–48 record its SHA-256
as above. I did not recompute any digest, because I ran nothing. The receipt binds only that
file. It depends on two auxiliary candidate snapshots, which I read but which the receipt does
not cover:
- `candidate/tools/_revision.py`, SHA-256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf (inventory lines 64–68);
- `candidate/tools/check-revision-binding.py`, SHA-256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6 (inventory lines 39–43).

For comparison only, I also read the pre-round snapshot
`snapshot/tools/check-revision-binding.py` and the build oracle `build/Oracle08TagBlob.md`. All
statements below are source predictions, not observed runs, unless they are marked otherwise.

## Verdict
There is no false-green or defect in the consumer within this predicate.
- The frozen consumer, using the frozen binder, is predicted to refuse an annotated tag that
  points at a blob. It should return exit 2 with exactly one `E-REVISION-INVALID` finding, for
  both the full object ID and a unique prefix.
- The candidate `target_type_probes` row grades that refusal exactly.
- A plausible weakening mutant of the binder is predicted to be killed by this row (see the binder mutant section).

There is one secondary weakness, on the judge side and not in the reviewed file:
- The judge never checks at run time that the tag_to_blob fixture is really a tag pointing at
  a blob.
- The judge's own selftest never shows that the tag_to_blob row kills anything.
- The identity of the row therefore rests only on how the fixture code builds it.
- A judge mutant that changes the row's target is predicted to survive (see the judge-side calibration section).

## Axes
1. How the consumer binds, and how argv, errors and output propagate for a tag→blob selector.
2. How strictly the candidate row checks the refusal: exit code, finding ID, ID list and finding count.
3. Whether the fixture is real: an independently created typed object, a fresh sandbox, a
   sane unique prefix, and no reads of host state.
4. Whether the row kills mutants, compared with the build oracle.
5. Continuity: the old matrix stays unchanged, and commit-tag is continuity, not new coverage.

## 1. Consumer propagation (observed in the frozen source)
The judge calls the consumer from `run_tool` (judge lines 359–371) as
`[sys.executable, sandbox/tools/check-recheck-commands.py, "--revision", <sel>, "--branch", master]`.
`EXTRA` is empty for this tool (judge line 74). The working directory is the sandbox, and the
environment is `clean_env()`.

In the consumer:
- `ROOT` is `Path(__file__).resolve().parents[1]`, which is the sandbox (line 58). `import _revision` (line 55) resolves through `sys.path[0]` to `sandbox/tools/_revision.py`, the checkout at the measured tip.
- argparse (lines 878–897) accepts `--revision` and `--branch`, and `--forbid` defaults to the valid `DEFAULT_FORBID`.
- `forbid_list` runs before binding (line 916) and passes.
- Line 918 calls `_revision.bind(repo, args.revision, branch)`. The selector is passed unchanged.

In the binder, `_revision.bind` (lines 172–192) runs these steps:
1. `validate_branch("master")` passes.
2. `REV.fullmatch` passes for 40 hex, and also for prefixes of 7 to 39 hex.
3. `_object_commit` (lines 112–146) runs:
   - `rev-parse --disambiguate=<lower>` returns exactly one object ID, the tag object `T`;
   - `cat-file -t T` reports `tag`;
   - the peel `rev-parse --verify --quiet --end-of-options T^{commit}` fails, because a blob never reaches a commit;
   - the follow-up `rev-parse --git-dir` succeeds, so the function returns `None`.
4. Line 179 then raises `RevisionError(E-REVISION-INVALID, "revision", "<sel> does not name one commit")`.

Back in the consumer:
- Lines 919–921 set `tip = _revision.branch_tip(...)`. That call never raises.
- The error is re-raised as `Cannot(fid, site, detail)` with the values unchanged.
- Lines 930–934 emit `CANNOT_EVALUATE`. Here `revision` is the echoed selector, because `sha` is `None`, and the payload carries exactly one finding. `counts` is `None`.
- Line 795 maps the status to exit 2.
- `expand_paths`, `read_git` and the exec log (lines 923–929 and 941–951) are never reached.

Predicted output: exit 2 and `findings == [{"id": "E-REVISION-INVALID", ...}]`. This matches
the build oracle's expected table (`Oracle08TagBlob.md` lines 61–70). The line references the
oracle took from the working tree (916, 918, 919–921, 930–934, 795, 923) match the frozen
candidate bytes line for line. The oracle's binder digest, 06b71e8c…, equals the candidate
inventory digest for `_revision.py`.

## 2. How strictly the row grades
- Fixture classes are set up at judge lines 697–704, and the per-selector check is at lines 709–732.
- `"tag_to_blob": (tag("blob", blob), None)` sets `expected_commit` to `None`, so the row goes through `refused(..., ID_INVALID)` (lines 721–725).
- `refused` (lines 383–393) requires `code == 2` and that the first finding ID is `E-REVISION-INVALID`. The row then also requires `binding_ids == ["E-REVISION-INVALID"]` and `finding_count == 1`.
- The row is `ok` only if both the full-ID selector and the prefix selector pass.

This is the exact-ID requirement the oracle asked for at lines 76–77 and 113–115. Checking
only for exit 2 would not be enough, and the row does more than that. It does not check the
`revision`, `site` or `detail` fields on a refusal. That matches the old matrix's documented
echo tolerance (judge lines 482–483), so it is not a defect here.

## 3. Whether the fixture is real
**Typed object.**
- `blob_object` (lines 408–413) writes a blob with `hash-object -w`.
- `tag()` (lines 685–695) runs `git tag -a r21-target-check-recheck-commands-blob -m blob <blob>` under `must()`, then returns `rev-parse --verify ref^{tag}`. That call guarantees `T` is a tag object.
- The tag name is new: the r20 matrix uses `r20-object-selector-*` (line 498).

**Fresh sandbox.**
- `target_type_measure` (lines 739–747) creates its own `TemporaryDirectory`, `clone_lane --no-tags`, `prepare` (which removes the origin remote and pins `refs/remotes/origin/master` to the tip), and `materialize`. It does not share the sandbox from `measure()`.
- Within one measurement the nine tools run one after another in that same clone.
- Fixture refs are deleted in a `finally` block (lines 734–736). The tag objects stay in the object database as dangling objects.
- Every tool's tag name, and therefore its tag object, is different, so a full-ID selector cannot alias another tool's object.

**Unique-prefix sanity** (lines 711–718).
- Widths run from 7 to 39, so the full ID is excluded; it is already the first selector.
- Uniqueness is checked against `cat-file --batch-all-objects`. That inventory is taken at line 705, after all four tags for this call exist, and it includes dangling objects left by earlier tools.
- The check also requires that no `refs/heads/<p>` or `refs/tags/<p>` exists.
- This matches the object-only `--disambiguate` that the binder uses, and it raises `E-SANDBOX` if no suitable prefix exists.

**No host read on this path.**
- The consumer reads only the sandbox through `ROOT`.
- Every git call on the refusal path goes through `_revision._git` or `validate_branch` with `_revision.clean_env()` (`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`).
- The consumer's own `git()` (lines 798–809) removes every `GIT_*` variable, including the two isolation settings the judge sets, and does not add them back. It would therefore read host global and system git config. On the tag_to_blob path it is never reached. It is reached on the accept rows, through `expand_paths` and `read_git`.
- [INFERENCE] That host-config read affects the accept rows only, and it is outside this predicate.

## 4. Killing mutants and comparison with the oracle
**Binder mutant (source prediction, not executed).** In `_revision.py` line 140, change
`f"{oid}^{{commit}}"` to `f"{oid}^{{}}"`. This is the oracle's mutant.
- A tag pointing at a blob then peels to the blob `B`.
- `_ancestor(repo, B, refs/heads/master)` follows. [INFERENCE] `merge-base --is-ancestor` exits with 128 or higher on a non-commit, so the result is `E-GIT-FAILED`.
- The consumer's exit is still 2, but the finding ID is `E-GIT-FAILED`, so the row fails and the mutant is killed.

The oracle's second mutant (on a failed peel, `return oid`) is predicted to be killed the same
way. [INFERENCE] `merge-base` cannot peel a tag pointing at a blob to a commit either. The
r20 matrix misses both mutants, as the oracle notes at lines 79–93, so for this consumer the
tag_to_blob row is genuinely new coverage.

**Consumer mutant search.**
- Refusing every tag object (never peeling) passes tag_to_blob, but fails `annotated_tag_to_commit` and `nested_tag_to_commit`. It also fails the old `annotated_tag_object` check. Since `behavior_ok` requires all five classes, the composite result is not a false green.
- Mapping every binding error to `E-REVISION-INVALID` fails the old unlanded, not-pushed and git-failed rows.
- `^{}` peel plus a commit-type check before the ancestor test is behaviourally equivalent to the correct code, so it is not a mutant.

I found no realistic consumer mutant that survives this row together with its companion
rows. A refusal row on its own cannot tell *why* the consumer refused. That limit is inherent
to the row type and is covered by the companion accept rows.

**Judge-side calibration (secondary, outside the reviewed file).**
- The judge does not check at run time that the tag's target is a blob, for example with `rev-parse --verify T^{blob}` or `cat-file -t T^{}`.
- The selftest witness (judge lines 1234–1259) only requires the five classes to be `ok` on the correct stub. Under the `target-generic-peel` stub it checks only `tag_to_tree.ok == False` and that the overall result is false.
- `TARGET_TYPE_WITNESS.new_matrix_kills` reads only `tag_to_tree`.

Proposed judge mutant (not executed): change line 700 to `tag("blob", tree)`, or to `tag("blob", tip)` with `expected_commit` set to `tip`.
- Predicted result: the row stays green for the real consumer, and `target-types-five-fixed-classes` still passes.
- `tree-tag-mutant-new-matrix-rejects` also still passes, because it is satisfied by `tag_to_tree`.
- The mutant would therefore survive the judge's own selftest, and the tag→blob class would silently disappear.

Against the frozen candidate bytes this does not happen: line 700 uses the actual blob. It is
a weakness in how the judge calibrates the row's identity, not a false green in this predicate.

## 5. Continuity
- The pre-round snapshot judge has `refused` at line 383, `accepted` at 396, `object_selector_probes` at 475, `annotated_tag_object` at 631 and `noncommit_blob` at 633. Those are the same line numbers as in the candidate, and the snapshot has no `target_type_*` functions.
- [INFERENCE, based on matching line numbers rather than a byte diff] The old matrix is unchanged.
- `measure()` never calls `target_type_probes`.
- `--object-target-types` and `--object-selectors` are mutually exclusive and fail with `E-CLI` together (lines 1391–1395).
- `annotated_tag_to_commit` (line 703) repeats the old `annotated_tag_object` row, so it is continuity, not new coverage. `nested_tag_to_commit` peels through a tag of a tag, which the old matrix lacked.
- C2's `target_type_mode` 0→1 (line 773, `int(available)`) is a single availability bit counted once (line 779). It is not a ninefold behavioural uplift; `target_type_tools` is a separate behavioural count (lines 765–767).

## Observations, inferences and limits
- I observed only file contents read with Read and Grep. No consumer, judge, git or mutant run was executed.
- Inferred, not observed: the `merge-base --is-ancestor` exit code on a blob or on a tag pointing at a blob, the exact `git tag -a` blob-target type header, and the old-matrix line identity.
- SHA-256 object-format repositories were not examined. Only the selector length differs: the binder's `REV` allows up to 64 hex, and the prefix loop scales with `len(object_id)`.
- No tool installation was needed or performed. Scope is review only; I claim no closure by a non-author and no promotion outside this lane.

Scope: executed=none
