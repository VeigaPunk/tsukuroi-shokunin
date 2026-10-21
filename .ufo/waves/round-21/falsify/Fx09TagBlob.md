# Fx09TagBlob — falsify attack: check-seat-scope.py × tag_to_blob (candidate 0a14952b)

Reviewed-SHA256: add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac
Predicate: check-seat-scope.py-tag_to_blob-candidate-control
Lane bounds: leaf member — no subagent dispatch.
Report: .ufo/waves/round-21/falsify/Fx09TagBlob.md

Verdict: **no defect within this predicate.** The candidate `target_type_probes` row `tag_to_blob` grades `check-seat-scope.py` correctly. The strongest realistic weakening mutant (generic tag peel) is predicted to be killed by this row for this consumer. Every mutant I found that survives this row in isolation is killed by a sibling row in the same new matrix or by the unchanged old matrix. None of these mutants was executed.

Primary receipt binds only `candidate/tools/check-seat-scope.py` (add541d8…). Auxiliary snapshot dependencies read, digests from `candidate-files.json`:
- `candidate/tools/_revision.py` 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
- `candidate/tools/check-revision-binding.py` 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6
- Baseline comparison: `round-21/snapshot/tools/check-revision-binding.py` (preregister.json sha256 da000de4…); build oracle `round-21/build/Oracle09TagBlob.md` (prose, not a snapshot).

## Axes

- (A) Consumer bind/argv/error/output propagation in the frozen source.
- (B) Binder behaviour for an annotated tag whose target is a blob.
- (C) Judge row construction: an actual typed object, exact refusal id and count, a fresh sandbox, unique-prefix sanity, no host read.
- (D) Mutant kill power, with false-green search.
- (E) Comparison with the build oracle, old-matrix preservation, and C2 mode semantics.

## (A) Consumer propagation — source observations

- The judge runs `python3 <sandbox>/tools/check-seat-scope.py --revision <S> --branch master --wave .ufo/waves/round-16/build`:
  - argv: `run_tool` in `check-revision-binding.py:359-371`, `EXTRA` at :75.
  - cwd is the sandbox and env is `clean_env()` (:100-104).
- `ROOT = Path(__file__).resolve().parents[1]` (seat-scope :39). That resolves to the sandbox clone because the tool is materialized at `<sandbox>/tools/` (judge :259-274). `from _revision import RevisionError, bind as bind_revision` (:36) resolves to `<sandbox>/tools/_revision.py`, which the detached checkout at the measured tip provides (judge `prepare` :233-242).
- `main` (:640-669) order:
  1. argparse;
  2. `args_issue` (:241-247), which gives None;
  3. `wave_key` (:186-193), which accepts the lane-relative literal;
  4. `revision = revision_in` (:659-660);
  5. `collect` (:258-272), which calls `bind_revision(root, revision, branch)` as its first action (:262).
- `except RevisionError as exc: raise Cannot(exc.fid, exc.site, exc.detail)` (:263-264) passes the id and site through 1:1.
- `main` catches `Cannot` and calls `emit(Result(CANNOT, [one Finding], 0), revision=<S echoed>, branch, tip=None, wave)` (:663-665).
- `emit` (:151-170) prints exactly one JSON line and returns 2. `sys.exit(main())` (:673) gives exit 2.
- No `read_git`, `tree_paths` or seat-scope `git()` call is reached on this path. The refusal precedes :266. The existence of `.ufo/waves/round-16/build` at the tip is irrelevant to this row.

## (B) Binder — source observations (`_revision.py`)

- `bind` (:172-192) runs four steps:
  1. `validate_branch("master")` passes (:84-95);
  2. `REV` accepts the 40-hex tag ID and its 7+ hex prefix (:41, :175);
  3. `_object_commit` (:112-146) runs `rev-parse --disambiguate=<s>`, then requires exactly one OID (:119-124), then `cat-file -t` returns `tag` (:127-137);
  4. the peel `rev-parse --verify --quiet --end-of-options <oid>^{commit}` fails, `repo_check` succeeds, and the function returns `None` (:139-146).
- `bind` then raises `RevisionError("E-REVISION-INVALID", "revision", "<S> does not name one commit")` (:177-179) before any branch-existence, ancestry or origin check.
- Every `_git` call uses `clean_env()` (:62-66), which sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`.

**Source prediction (not observed):**
- exit 2;
- stdout `{"status":"CANNOT_EVALUATE","revision":"<S>","branch":"master","branch_tip":null,"wave":".ufo/waves/round-16/build","seat_count":0,"counts":{SCOPE-*:0,"E-REVISION-INVALID":1},"findings":[{"id":"E-REVISION-INVALID","site":"revision","role":null,...}],...}`.

This holds for both selectors: the full tag OID and the unique prefix.

## (C) Judge row — `check-revision-binding.py:676-736`

**Actual typed object, independently created:**
- `blob_object` (:408-413) runs `git hash-object -w --stdin` and gets a real blob.
- `tag("blob", blob)` (:685-695) runs `git tag -a r21-target-check-seat-scope-blob -m blob <blob>`. It returns the tag OID through `rev-parse --verify <ref>^{tag}`, so the selector is verified to be a tag object.
- Limit: the judge does not separately assert that the tag's target type is blob (for example `cat-file -t <tag>^{}` == blob, which the oracle recommends). It relies on construction from a hash-object blob. Because the tag OID hashes its own `type blob` line, this is sound by construction. It is not a defect.

**Exact refusal id and count:**
- `expected_commit is None` routes to `refused(..., ID_INVALID, branch)` (:721-725). It then tightens `ok` to require `binding_ids == ["E-REVISION-INVALID"]` and `finding_count == 1`, on top of `exit == 2` and first finding id == `E-REVISION-INVALID` (`refused` :383-393).
- The echoed `revision` field is not counted as acceptance. Matching the oracle's warning, `json_revision` is recorded but not graded for refusals.

**Selectors:** `[object_id, prefix]` (:710-718).
- The prefix is the shortest width in `range(7, len)` that is unique in a `cat-file --batch-all-objects` inventory. The inventory is taken after all five fixture tags exist (:705-707).
- It must also not collide with `refs/heads/<p>` or `refs/tags/<p>`.
- If no such prefix exists, the row fails with `E-SANDBOX`. It never silently skips. Uniqueness sanity holds.

**Fresh sandbox:**
- `target_type_measure` (:739-746) creates one `TemporaryDirectory` clone per invocation and runs `prepare` (pinned branch and origin refs, remote removed).
- The sandbox is shared sequentially across the nine tools. Fixture tag refs are deleted in `finally` (:734-736), but their objects persist. Tag names are tool-scoped and existence-checked (:686-689), and the inventory is recomputed per call. Fresh per measurement, not per tool; this does not affect this row.

**No host read (this row):**
- The tool's git calls on this path are only `_revision._git` and `validate_branch`, both of which use the isolating `clean_env`.
- The judge's own git calls use `clean_env` plus `core.hooksPath=/dev/null` (:107-116).
- The only host input is the lane clone, which is the measured artifact by design.

## (D) Mutants — proposed, NOT executed

- **M1, generic peel (strongest weakening):** `_revision.py:140` `f"{oid}^{{commit}}"` → `f"{oid}^{{}}"`.
  - Prediction: the peel returns the blob OID with rc 0, `_commit(refs/heads/master)` succeeds, and `_ancestor(blob, refs/heads/master)` runs.
  - Expected result is `merge-base` rc ≥ 2, giving `E-GIT-FAILED` at site `refs/heads/master` (:156-160). If Git instead returned rc 1, the result would be `E-REVISION-NOT-LANDED`. Both differ from `E-REVISION-INVALID`, so rc 0 is the only escape, and that is impossible for a blob.
  - Both selectors give `ok=False`, so **this row kills M1 for check-seat-scope**.
  - The old matrix does not kill M1: `noncommit_blob` and `blob-revision` exit early at `object_kind != "tag"`, and the tag→commit probes are equivalent under `^{}`. This matches the oracle's (D).
- **M2, trust the tag's `object` line without a type check:** same signature as M1, so it is killed.
- **M3, refuse every tag object** (`if object_kind != "commit": return None`): survives `tag_to_blob` by construction. Killed in the same matrix by `annotated_tag_to_commit` and `nested_tag_to_commit` (:701-702), and in the old matrix by `annotated_tag_object` and `annotated_tag_prefix` (:631-632).
- **M4, consumer collapses every `RevisionError` to `E-REVISION-INVALID`** at seat-scope :264: survives this row. Killed by the old matrix `unlanded`, `not-pushed`, `git-failed`, `branch-*` and `strict-refusals` probes (:416-472).
- **M5, double mutant** (M1 plus a consumer rewrite of only `E-GIT-FAILED` → `E-REVISION-INVALID`): this would false-green this row. The consumer half is killed by old-matrix `git-failed`, where an origin ref names a blob (:449-454). This is not a single-site false green.
- **Lookup-failure confound:** if `--disambiguate` on a full-length OID returned zero lines, the full selector would be refused for the wrong reason. Same-sandbox accept rows using the identical selector shapes (`annotated_tag_to_commit` full plus prefix) would fail, so attribution holds by elimination [INFERENCE]. The refusal row is not discriminating on its own; the matrix supplies the control.
- **Selftest gap (limit, not a predicate defect):** the candidate selftest pins the generic-peel kill only through `tag_to_tree` on a stub at `TOOLS[0]` (:1239-1258). Its `all(...)==False` assertion would hold from `tag_to_tree` alone. No selftest case asserts the `tag_to_blob` kill individually, and none runs the real check-seat-scope.py.
  - Stub prediction for `tag_to_blob` under `target-generic-peel` (:981-1001): the peeled blob SHA reaches `anc()`, git returns rc ≥ 2, and the stub outputs `E-GIT-FAILED`, so it would also be killed.

## (E) Oracle, preservation, C2

- **Build oracle `Oracle09TagBlob.md`** expects: exit 2, status `CANNOT_EVALUATE`, exactly one `E-REVISION-INVALID` at site `revision`, the input echoed and never counted as acceptance, `branch_tip` null, `seat_count` 0. This matches my prediction.
- **Candidate grading is a strict subset:** exit, id, `binding_ids` and count. It does not grade status string, site, counts dict or `branch_tip`. For this class, the id alone separates M1 (`E-GIT-FAILED`), so the omitted site check is redundant here. The oracle also prescribes plumbing-type ground truth, which the candidate replaces with construction (see C).
- **Consumer and binder are byte-identical to the preregistered baseline snapshots.** check-seat-scope.py add541d8… and _revision.py 06b71e8c… appear in both `preregister.json` and `candidate-files.json`.
  - check-seat-scope's `tag_to_blob` behaviour was therefore already correct at baseline [INFERENCE from identical bytes].
  - C2 `target_type_mode` 0→1 (:758-759, :773) is matrix availability, counted once. It is not a behavioural 9-fold uplift. The selftest pins that a missing mode still yields `target_type_tools == TOTAL` (:1251-1254).
- **Old matrix unchanged:**
  - Candidate and baseline snapshot have identical `def` offsets through :675 (`probe_tool` :416, `object_selector_probes` :475). The inspected `probe_tool` body and the `object_selector_probes` tail are textually identical.
  - `measure` (snapshot :676-776, candidate :783-883) is identical on inspection, and neither `measure` nor `grade` calls `target_type_probes`. Grep finds only :676, :764, :1234 and :1246.
  - Limit: this is a visual and offset comparison, not a byte diff (NO-EXEC).
- **Commit-tag continuity:** `annotated_tag_to_commit` and `nested_tag_to_commit` continue the old `annotated_tag_object` and `annotated_tag_prefix` rows and the binder's own nested selftest (`_revision.py:360-365`). They are continuity, not new coverage.

## Adjacent observation (outside this predicate)

- seat-scope's own `git()` (:173-175) drops every `GIT_*` key and re-adds only three. That strips the judge's `GIT_CONFIG_NOSYSTEM` and `GIT_CONFIG_GLOBAL`.
- Its `read_git` and `tree_paths` (:196-214) are reached on the accept rows (`annotated_tag_to_commit`, `nested_tag_to_commit`). There they would read the host `/etc/gitconfig` and `~/.gitconfig` [INFERENCE: HOME is inherited through clean_env].
- The `sandbox()` selftest fixture uses the same helper.
- This path is not reached on `tag_to_blob`; the refusal occurs at :262. Reported for the sibling rows and L1, not as a defect of this predicate.
- Residual exotic vector [INFERENCE]: a caller env with `PYTHONSAFEPATH` and `PYTHONPATH` could redirect `from _revision import` away from `<sandbox>/tools`, because clean_env keeps non-GIT variables.

## Remaining unknowns

- The exact Git exit codes for `rev-parse --verify --quiet <tag→blob>^{commit}` and for `merge-base --is-ancestor <blob> <commit>` were not observed. The binder returns INVALID for either peel rc, and M1's kill holds for either merge-base rc of 1 or ≥ 2.
- Live-repo agreement with these snapshots is not verified.
- Tools installed or updated: none.
- No non-author closure or outside promotion is claimed.

Scope: executed=none
