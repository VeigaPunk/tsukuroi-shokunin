# Fx05TagBlob — measure-update-recheck.py × tag_to_blob (candidate control)

Reviewed-SHA256: 0275af5a8afd6de26086d6901bd9c62b53a3390ba92ca950cb0602996326ccb7
Predicate: measure-update-recheck.py-tag_to_blob-candidate-control

Lane bounds: leaf member — no subagent dispatch.

Primary file: `.ufo/waves/round-21/candidate/tools/measure-update-recheck.py` (candidate revision 0a14952b59d20179e1c813af58befaecd6992a17, digest as supplied in the item and in `candidate-files.json:24-28`; not recomputed, NO-EXEC).
Auxiliary snapshot dependencies, read only and not bound by this receipt:
- `.ufo/waves/round-21/candidate/tools/_revision.py`, listed in `candidate-files.json:64-68` at sha256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf.
- `.ufo/waves/round-21/candidate/tools/check-revision-binding.py`, listed in `candidate-files.json:39-43` at sha256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6.
- For comparison only: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py` (preregistered da000de4…, `preregister.json:46-48`), the build oracle `.ufo/waves/round-21/build/Oracle05TagBlob.md`, and `preregister.json`.

Verdict: no defect within this predicate. The judge's `tag_to_blob` row for this consumer builds a genuine annotated tag whose target is a blob, independently of the binder under test. It runs the real consumer in a fresh sandbox clone, uses a unique-prefix selector alongside the full object ID, and grades exit 2 with exactly one finding, `E-REVISION-INVALID`. The consumer passes that refusal through unchanged. Every realistic tag-peel mutant I traced is killed by this row. The mutants that survive change output fields the predicate does not grade; they are listed below as being outside the predicate.

## Axes
- A1 Consumer propagation: bind call, argv, error mapping, exit code, stdout.
- A2 Fixture realism: the object is actually created, its type is real, and it is built without the binder under test.
- A3 Grading exactness: refusal finding ID and finding count.
- A4 Selector sanity: full object ID plus a unique prefix, with no wrong-reason refusal.
- A5 Isolation: fresh sandbox, and no host read on this path.
- A6 Mutant kill power, with a residual mutant if one exists.
- A7 Continuity and claim framing: commit-tag rows, the old matrix, and the meaning of C2 0→9.

## Observations (source, read only)

### A1 Consumer propagation (`measure-update-recheck.py`)
- O1. `sys.dont_write_bytecode = True` is set, then `import _revision` (lines 33-34). Because `sys.path[0]` is the script's own directory, the import resolves to `<sandbox>/tools/_revision.py` from the checkout at the measured tip. `ROOT = Path(__file__).resolve().parents[1]` (line 37), which is the sandbox.
- O2. argparse uses `exit_on_error=False` (lines 735-751). `--revision` and `--branch` (default `master`) are passed as received. The judge invokes the tool as `--revision <sel> --branch <branch>` (`check-revision-binding.py:359-366`), and `EXTRA` for this tool is `()` (lines 77, 66).
- O3. `load(rev, branch)` (lines 471-481) calls `_revision.bind(ROOT, rev, branch)`. On `RevisionError` it raises `Cannot(exc.fid, exc.site, exc.detail, revision=rev, tip=_revision.branch_tip(ROOT, branch))`. The fid is passed through unchanged. `read_git` is reached only after a successful bind (lines 480-481).
- O4. `main` (lines 759-772) catches `Cannot` and calls `emit(exc.revision or revision, "CANNOT_EVALUATE", [one Finding], digest=None, branch=..., branch_tip=exc.tip ...)`. `emit` prints one `json.dumps(..., sort_keys=True)` line (line 433) and returns `CANNOT`=2 for any status other than COUNTED or ABSENT (line 434).
- O5. Binder path for a tag whose target is a blob (`_revision.py`): branch validation passes (lines 84-95, 174), then the 7-64-hex check passes (lines 175-176), then `_object_commit` (lines 112-146) runs `--disambiguate`. That returns one oid. `cat-file -t` reports `tag`, so the code peels with `oid^{commit}` (lines 139-140). The peel fails. `rev-parse --git-dir` succeeds, so the function returns None, and line 179 raises `E-REVISION-INVALID` with site `revision`. All of this happens before the branch-missing, landed and pushed checks (lines 180-192), so the origin state is irrelevant.
- Prediction P1 (not observed): exit 2, `status` CANNOT_EVALUATE, `findings == [{"id":"E-REVISION-INVALID","site":"revision","detail":"<sel> does not name one commit"}]`, `revision` echoes the selector, `record_count` 0, `snapshot_sha256` null. This agrees with oracle E1-E4 (`Oracle05TagBlob.md:28-35`).

### A2 Fixture (`check-revision-binding.py` `target_type_probes`, lines 676-736)
- O6. The blob is written with `git hash-object -w --stdin` (`blob_object`, lines 408-413). The tag is created by `tag("blob", blob)` using `git tag -a r21-target-measure-update-recheck-blob -m blob <blob>` with `tag.gpgSign=false` (lines 685-695, 700). The object ID is read back via `rev-parse --verify <ref>^{tag}`, which guarantees that the selector is a tag object. The judge's own `object_commit` and `bind` are not used to derive it, and the judge never imports `_revision` (docstring lines 8-10, `object_commit` lines 139-140).
- O7. Each tag name contains the tool name, so this consumer's tag object is distinct from the other eight tools' tags. Because the tag object for this class does not resolve to any commit, `expected_commit=None` (line 700), and the row is graded as a refusal.
- Gap G1 (hardening, not a defect): the row never asserts the target type, for example that `cat-file -p` shows `type blob`. The class identity depends only on the argument at line 700. The current bytes do pass the blob, so this does not affect the predicate.

### A3 Grading (lines 720-725, 383-393)
- O8. `refused(..., ID_INVALID)` sets ok only when `code == 2` and the first finding id equals `E-REVISION-INVALID`. The row then also requires `binding_ids == ["E-REVISION-INVALID"]` and `finding_count == 1`. The case is ok only if every selector observation is ok (line 732). At the tool level, `behavior_ok` requires `len(cases) == 5` and all of them ok (line 765).

### A4 Selector sanity (lines 705-718)
- O9. Selectors are the full tag oid and the shortest prefix of width 7 to 39 that matches exactly one entry in `cat-file --batch-all-objects` and has no `refs/heads` or `refs/tags` collision. The inventory is taken after all fixtures for this tool are created (line 705), and the consumer creates no objects. A missing object or an ambiguous prefix would also produce E-REVISION-INVALID, so this check is what rules out a refusal for the wrong reason; it matches the oracle precondition at `Oracle05TagBlob.md:41-43`. The full oid exists by construction.
- [INFERENCE] `rev-parse --disambiguate=<full oid>` lists exactly that object, and `--batch-all-objects` covers the same object set as `--disambiguate` in a `--no-hardlinks` clone with no alternates.

### A5 Isolation
- O10. `target_type_measure` (lines 739-746) creates a new `TemporaryDirectory`, clones the lane with `--no-hardlinks --no-tags`, and in `prepare` detaches to the tip, sets `refs/heads/<branch>`, removes `origin`, and recreates only `refs/remotes/origin/<branch>` (lines 233-242). Fixture tag refs are removed in `finally` (lines 734-736). The unreachable tag objects stay in the sandbox only. The sandbox is fresh per measure run; within a run it is shared across the nine tools, and refs are cleaned between tools.
- O11. No host read on the tag_to_blob path. The judge runs `git()` with `core.hooksPath=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` (lines 100-112). Every consumer git call made before the refusal goes through `_revision._git` and `validate_branch`, which use `clean_env` with the same isolation (`_revision.py:62-77, 89-91`). The `branch_tip` call in the error path uses the same isolation. The consumer's own `git()` and `read_git` (lines 437-456) are never reached on this path.
- Limit L-host-1 (continuity only, not this class): on the accept path (commit-tag rows), the consumer's `git()` removes every `GIT_*` variable, including the `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_NOSYSTEM` that the judge injected, and re-adds only `GIT_OPTIONAL_LOCKS`, `GIT_PAGER` and `LC_ALL` (lines 437-439). As a result, `read_git` would read the host's system and global git config. The old-matrix tip accept rows go through the same path, so this was already true before the candidate; it is not part of tag_to_blob.
- Limit L-host-2: Python and git are host binaries, and the judge's docstring (lines 49-54) states that the clone confines git writes but is not OS isolation. The judge does not watch for side effects.

## A6 Mutants (proposed, NOT executed; outcomes are source predictions)

| Mutant | Location | Predicted tag_to_blob outcome | Row verdict |
|---|---|---|---|
| K1: generic peel `^{commit}` changed to `^{}` | `_revision.py:140` | sha=blob, then `_ancestor` merge-base exits ≥2 [INFERENCE 128], giving E-GIT-FAILED | killed (finding ≠ INVALID) |
| K1b: K1 plus `_ancestor` treating rc≥2 as False | `_revision.py:140,157-160` | E-REVISION-NOT-LANDED | killed |
| K2: return the tag oid unpeeled for `kind == "tag"` | `_revision.py:136-146` | merge-base on a tag whose target is a blob fails, giving E-GIT-FAILED [INFERENCE] | killed |
| K3: consumer swallows `RevisionError` and falls back to the worktree | `measure-update-recheck.py:476-479` | exit 0 ABSENT or COUNTED | killed (exit ≠ 2) |
| K4: consumer accepts only 40-hex selectors | `measure-update-recheck.py:471-481` | tag_to_blob still green; the `annotated_tag_to_commit` prefix accept fails | killed by a sibling row |
| S1: refusal echoes `"worktree"` or the blob oid instead of the selector | `measure-update-recheck.py:770` (`exc.revision or revision`) | exit 2, one INVALID finding, wrong `revision` | survives; outside the predicate |
| S2: refusal status set to a string other than COUNTED or ABSENT | `measure-update-recheck.py:770` | `emit` still returns 2 (line 434) | survives; outside the predicate |
| S3: every `RevisionError` collapsed to E-REVISION-INVALID | `measure-update-recheck.py:478` | correct output for this class | survives the new matrix; killed by the old unlanded, not-pushed and branch rows; not a false green for this class |

- S1 and S2 contradict oracle E1 (status) and E3 (revision echo, and the blob ID must not appear in the payload) at `Oracle05TagBlob.md:29-34`. The judge deliberately does not grade the revision field of a refusal (comment at lines 481-483; ok formula at line 393), and `status` is never graded. The predicate is "exact refusal ID/count", so neither mutant is a false green inside it. Recorded for L1 as an oracle-versus-judge divergence.
- The judge self-test leaves the class-identity gap G1 open. Swapping line 700 to `tag("blob", tree)` would keep `target-types-five-fixed-classes` green (lines 1234-1238 check only the label set and that all rows are ok). It would also keep `tree-tag-mutant-new-matrix-rejects` green, because that check only examines `tag_to_tree` (lines 1246-1250). The candidate bytes do not contain this swap.

## A7 Continuity and claim framing
- `annotated_tag_to_commit` and `nested_tag_to_commit` here are accept rows that expect `tip` (lines 701-703). The consumer reports `revision = binding.sha` (line 480), and `accepted` compares it case-insensitively with `tip` and requires exit ≠ 2 (lines 396-404). The accept rows therefore depend on the record and snapshot at the tip being absent or consistent, just as the old `tip` accept row does. `annotated_tag_to_commit` overlaps the round-20 cases `annotated_tag_object` and `annotated_tag_prefix` (`check-revision-binding.py:631-632`; `ConnPlanner.md:29`). It is continuity only, not new coverage.
- Old matrix: in both the snapshot and the candidate, `object_selector_probes` starts at line 475, and the next definition is at line 676. Snapshot lines 626-673 read the same as candidate lines 626-673 by visual comparison. `measure` spans 103 lines in both copies. This is consistent with an unchanged old matrix, but no byte diff was run [INFERENCE].
- C2 framing: the candidate `_revision.py` digest (06b71e8c…) equals the preregistered baseline snapshot digest (`preregister.json:50-52`, declared, not recomputed). The consumer's line anchors cited by the build oracle (34, 471-481, 434, 574-610, 758-772) also match the candidate. The tag_to_blob refusal behavior of this consumer therefore predates the candidate. `target_type_measure` counts behavior separately from mode availability (lines 758-774). The self-test asserts that a missing mode still yields `target_type_tools == TOTAL` (lines 1251-1254). So target_type_mode going from 0 to 1 is a change in measurement availability. It is not a 9-fold uplift in consumer behavior.

## Comparison with the build oracle (`Oracle05TagBlob.md`)
- Agrees on E1 exit 2, E2 (one finding, `E-REVISION-INVALID`, other binding IDs excluded), E4 precedence, the fixture recipe (`hash-object -w` then `tag -a`, selector from `^{tag}`), the unique-prefix precondition, and K1 as the smallest mutant that this row kills.
- Differs: the oracle also expects the `CANNOT_EVALUATE` status, the selector echo, the absence of the blob ID, and an explicit check that the target type is blob. The candidate row grades none of these (S1, S2, G1). None of them is in this predicate.

## Inferences and limits
- Nothing was executed: no test, mutant, judge, consumer, import, compile or hash. All outcomes above are source predictions, and no candidate output was observed.
- [INFERENCE] the git exit codes for `merge-base --is-ancestor` on a blob (≥2, likely 128) and for a failed `^{commit}` peel on a tag whose target is a blob (non-zero).
- [INFERENCE] `GIT_CONFIG_GLOBAL` replaces both `~/.gitconfig` and the XDG global config.
- No tools were installed or updated.
- No claim of non-author closure or outside promotion.

Scope: executed=none
