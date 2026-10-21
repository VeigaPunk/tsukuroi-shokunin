# Fx05Nested — `measure-update-recheck.py` × `nested_tag_to_commit`

Reviewed-SHA256: 0275af5a8afd6de26086d6901bd9c62b53a3390ba92ca950cb0602996326ccb7
Predicate: measure-update-recheck.py-nested_tag_to_commit-candidate-control

Primary: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/measure-update-recheck.py`, candidate revision `0a14952b59d20179e1c813af58befaecd6992a17`; digest supplied by the assignment and candidate inventory.

Auxiliary candidate snapshot dependencies (digests from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate-files.json`):
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/_revision.py`: `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf`.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-revision-binding.py`: `0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6`.

## Axes

- **Consumer binding and propagation:** the selected `--revision` reaches the shared binder, and the resolved commit—not the selector or branch tip—is used and reported.
- **Nested-object control:** the fixture is actually tag→tag→commit, with distinct object identities and a full expected commit SHA.
- **Predicate discrimination:** a wrong consumer result must differ from the expected result; acceptance must mean the intended behavior, not merely an exit other than 2.
- **Isolation and continuity:** sandbox/object construction, legacy matrix continuity, and honest separation of mode availability from behavioral coverage.

## Observations from frozen candidate source

1. **Consumer path.** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/measure-update-recheck.py` imports `_revision` (`:33–34`). `load(rev, branch)` calls `_revision.bind(ROOT, rev, branch)` for `--revision`, wraps a `RevisionError` into one `Cannot` preserving its finding ID and requested selector (`:471–482`), then reads both blobs at `binding.sha` and returns `binding.sha` as the first tuple value (`:480–482`). `main` emits one finding on a refusal; `emit` prints the JSON and returns 2 except for `COUNTED`/`ABSENT`, which return 0 (`:412–434`, `:734–780`). On success, the first tuple value becomes JSON `revision` (`:750–780`). Thus the current source predicts that the reported revision is the peeled commit SHA, not the input tag SHA.

2. **Binder semantics.** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/_revision.py` `bind` validates the branch, accepts only 7–64 hex, resolves a unique object ID, verifies the result is landed on the selected local branch, and, if present, pushed to the origin-tracking ref (`:112–146,172–192`). For a tag object, `_object_commit` uses `rev-parse --verify ... <oid>^{commit}`; Git's typed peel is transitive. A readable repository whose tag chain does not peel to a commit produces `E-REVISION-INVALID`; an unlanded or unpushed terminal commit produces the corresponding single binding refusal. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/measure-update-recheck.py` propagates those IDs as one finding rather than accepting a refusal (`:477–479,769–776`). These are source predictions, not observed executions.

3. **The target row creates a real nested annotated tag.** In `target_type_probes` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-revision-binding.py:676–736`), helper `tag()` makes an annotated tag and obtains its tag-object ID with `rev-parse ...^{tag}`. `commit_tag = tag("commit", tip)` is T1→C; `tag("nested", commit_tag)` makes T2→T1, so `nested_tag_to_commit` is T2→T1→C. Its expectation is `tip`, the full commit SHA. It tests T2's full object ID and a generated unique prefix. The candidate source therefore has genuine nested-tag construction, not a lightweight tag or a tag ref name.

4. **Prefix and sandbox controls.** Before the row loop, the judge obtains all object IDs with `cat-file --batch-all-objects`. For every non-tree target it chooses a prefix of length 7 through 39 only if exactly one inventoried object starts with it and there is no colliding `refs/heads/<prefix>` or `refs/tags/<prefix>` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-revision-binding.py:705–719`). Failure to find one raises `E-SANDBOX`, rather than silently dropping prefix coverage. `target_type_measure` creates a `TemporaryDirectory`, clones the lane, prepares the temporary repo at `tip`, and materializes the tool there (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-revision-binding.py:739–755`); `run_tool` runs it with that sandbox as cwd (`:359–371`). The consumer's `ROOT` is derived from its materialized `__file__`, so its Git/blob reads are source-predicted to use the sandbox, not host record/snapshot paths. No host-state command is part of this path. This is not an OS process sandbox: the inherited process still has user-level authority (as also cautioned by the judge docstring).

5. **Expected predicate.** For non-commit targets, the row requires the exact `E-REVISION-INVALID`, one binding finding, and `finding_count == 1`. For `nested_tag_to_commit`, `accepted()` requires a non-`CANNOT` exit and a JSON `revision` equal case-insensitively to `expected_commit` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-revision-binding.py:383–404,725–733`). That expectation is the full `tip` SHA. The accepted helper does not separately require status `COUNTED`/`ABSENT`, empty findings, or exit exactly 0; however the current consumer's `emit` return mapping has only 0 for those success statuses and 2 for refusals, so this looseness alone is not a false-green for the unmodified source.

## Finding — target-type matrix false-green (medium)

**Source-predicted mutant, not executed:** change only the first value returned by `load()` from `binding.sha` to `binding.branch_tip`, leaving its two `read_git(..., binding.sha, ...)` arguments unchanged (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/measure-update-recheck.py:480–482`). This confuses the payload's resolved-revision field with the separately emitted branch tip. In the target-type fixture, `tip` is both the terminal commit of T2→T1→C and the branch tip. The consumer would therefore report `revision == tip` for `nested_tag_to_commit`, and `accepted()` would mark the row `ok` even though the consumer no longer reports the commit selected by its tag. The same substitution passes the direct `annotated_tag_to_commit` row, also rooted at `tip`; the three refusal rows are unaffected. Consequently, this mutant is predicted to leave all five target-type classes green for this consumer. A nested tag ending at a landed non-tip commit would distinguish the wrong branch-tip report from the expected commit SHA.

This is a control-design defect, not an observed candidate runtime defect: the candidate `load()` currently returns `binding.sha`. The new matrix's expected commit is correct for its constructed object, but because it always tags the measured tip, that exact expectation aliases the branch tip and cannot discriminate this consumer-level regression.

## Build-oracle comparison and continuity

The available `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/build/Oracle05NestedTag.md` is explicitly source-only (`:25–50`), reviewed against `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/_revision.py`'s digest rather than this consumer's digest. It correctly describes transitive `^{commit}` peeling and identifies the new `nested_tag_to_commit` matrix as nested coverage; it also proposes a one-level-peel mutant, which the nested row should reject. The false-green above is different: it preserves nested acceptance but substitutes branch tip for the resolved SHA, so it survives the row because the fixture's terminal commit is the tip. The oracle does not address this aliasing mutant.

The oracle also correctly distinguishes old and new coverage: the prior matrix has single-level annotated-tag→commit cases and no tag→tag→commit selector. Its `landed-parent` case does distinguish a resolved parent from the branch tip. The new `--object-target-types` dispatch calls `target_type_measure` instead of the old `measure` path (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-revision-binding.py:1381–1426`), so this finding is specific to the explicitly selected new matrix and does not change the old matrix. The `annotated_tag_to_commit` row is continuity for an already-covered direct tag→commit case; it is not new coverage. Keep the matrices' results separate.

`target_type_measure` also separates availability (`target_type_mode` is `int(available)`) from the behavioral count over five classes for each original tool (`target_type_tools`/`behavioral_tools`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-revision-binding.py:739–780`). A mode 0→1 change is one mode-availability gain, not a behavioral nine-fold uplift. No such uplift is claimed here.

## Limits

All statements above are source observations or explicitly marked source predictions. No candidate test, mutant, script, command, or runtime was executed; no hashes were recomputed. The build oracle is a source-only comparison, not an independent runtime observation. No tool was installed or updated. This review is not non-author closure or outside promotion.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none