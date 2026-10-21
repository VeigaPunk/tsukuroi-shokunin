# Fx01TagBlob — falsify check-locator-clarification.py × tag_to_blob (candidate 0a14952b)

Reviewed-SHA256: cd24d07ce71e3a3c5cff92802b69f3b2630aa5942a437ad00e53469387b05814
Predicate: check-locator-clarification.py-tag_to_blob-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Primary file (receipt binds only this): `.ufo/waves/round-21/candidate/tools/check-locator-clarification.py`
(candidate-files.json: sha256 cd24d07c…05814, revision 0a14952b59d20179e1c813af58befaecd6992a17).

Auxiliary frozen snapshot dependencies read (not bound by the receipt):
- `.ufo/waves/round-21/candidate/tools/_revision.py`, candidate-files.json sha256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf. That digest equals the preregistered round-21 snapshot `_revision.py` digest in `preregister.json:50-52`, so the binder is declared byte-unchanged from baseline.
- `.ufo/waves/round-21/candidate/tools/check-revision-binding.py`, candidate-files.json sha256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6.
- Build oracle `.ufo/waves/round-21/build/Oracle01TagBlob.md`, used only for comparison. It reviewed the live consumer, not this snapshot.

Digests are the values declared in candidate-files.json. Under NO-EXEC they were not recomputed.

## Axes
1. Exit class: the exit code is 2 (CANNOT).
2. Finding identity: id, site and count of findings.
3. Payload `revision` / `branch_tip` semantics on refusal.
4. Fixture realism: an actual annotated tag whose target is a blob, created in a fresh sandbox, with a unique-prefix selector and no host read.
5. Mutant kill power of the `tag_to_blob` row.
6. Continuity and separation: the old matrix stays unchanged, and the C2 mode change is not a behavioural uplift.

## Observed from source: consumer bind, argv, error and output propagation
- `check-locator-clarification.py:18-19`: `sys.dont_write_bytecode = True`, then `import _revision`. Python puts the script directory first on `sys.path`, so this resolves to the sibling `tools/_revision.py`. In the judge sandbox that sibling is the checked-out copy at the measured tip (`prepare` does `checkout --detach tip`, `check-revision-binding.py:233-234`). No `__pycache__` is written.
- `:472-481`: argparse is built with `exit_on_error=False`, and `--revision` and `--selftest` are mutually exclusive. `--branch` defaults to `master`.
- `:780-788`: `_revision.bind(ROOT, args.revision, branch)` receives argv verbatim, with no lowercasing or trimming. On `RevisionError` the consumer sets `tip = _revision.branch_tip(ROOT, branch)` and `revision = args.revision`, then raises `Cannot(exc.fid, exc.site, exc.detail)`.
- `:793-795`: this emits `Result(CANNOT, [one Finding], 0)`. `read_git` (`:790`) is not reached, so nothing from the tag, the blob or the tree is read.
- `:427-436`: the output is one `json.dumps(sort_keys=True)` line with keys `branch, branch_tip, correction_count, findings, revision, status`. `main` returns `result.code`, and `sys.exit(main())` passes it on.
- `ROOT = Path(__file__).resolve().parents[1]` (`:24`) is the sandbox, because the judge runs `sandbox/tools/<name>` with `cwd=sandbox` (`check-revision-binding.py:359-371`).

## Observed from source: binder path for tag→blob (`_revision.py`)
The call chain in `bind` (`:172-192`) for a tag→blob selector:
1. `validate_branch` passes.
2. `REV` (7-64 hex) matches.
3. `_object_commit` (`:112-146`) runs `rev-parse --disambiguate=<lower>` and gets exactly one OID.
4. `cat-file -t` returns `tag`.
5. `rev-parse --verify --quiet --end-of-options <oid>^{commit}` fails, because a tag chain that ends in a blob cannot reach a commit.
6. `rev-parse --git-dir` succeeds, so the function returns `None`.
7. `bind` raises `RevisionError(E-REVISION-INVALID, "revision", "<sel> does not name one commit")` (`:178-179`).

The branch-missing, landed and pushed checks (`:180-191`) are never reached, so neither is `E-GIT-FAILED` from `merge-base`. The binder's own selftest asserts the same outcome in `annotated-tag-to-blob-invalid` (`_revision.py:413-419`). That covers the binder alone.

## Source prediction (not observed)
For `check-locator-clarification.py --revision <tag→blob full OID or unique prefix> --branch master` in the sandbox:
- exit 2
- `status` = `CANNOT_EVALUATE`
- `findings` = one entry, `[{"id":"E-REVISION-INVALID","site":"revision","detail":"<selector> does not name one commit"}]`
- `correction_count` = 0
- `revision` = the selector, echoed verbatim
- `branch_tip` = the full SHA of `refs/heads/master` in the sandbox

This matches the build oracle `Oracle01TagBlob.md` (Expected section) on every field. The oracle was written against the live consumer. The frozen snapshot has the same propagation lines (`:780-795`), so the agreement holds for this snapshot too.

## Observed from source: `target_type_probes` `tag_to_blob` row (`check-revision-binding.py:676-736`)
- **Actual typed object, created independently.** `blob_object` (`:408-413`) runs `hash-object -w --stdin` on `b"revision-binding probe blob\n"`. Then `tag("blob", blob)` (`:685-695`, `:700`) runs `git tag -a r21-target-check-locator-clarification-blob -m blob <blob>` with a pinned identity and `tag.gpgSign=false`. It records the tag object with `rev-parse --verify <ref>^{tag}`, which fails if the tag is lightweight. The judge does not import `_revision`. Its independent `object_commit` (`:139-166`) is not used by this row.
- **Expected outcome.** `expected_commit=None`, so the row is a refusal row. Grading (`:721-725`) uses `refused()` (`:383-393`): `exit == 2` and the first finding id must be `E-REVISION-INVALID`, and then the row requires `binding_ids == ["E-REVISION-INVALID"]` and `finding_count == 1`. The row demands an exact refusal ID with a count of one. An accepted full commit SHA does not apply to this class.
- **Selectors.** The full object ID and one unique prefix (`:710-718`). The prefix has width 7 to 39. It must be unique against `cat-file --batch-all-objects`, which is taken after all four fixture tags exist (`:705-707`), and no `refs/heads/<p>` or `refs/tags/<p>` may exist. Because the binder uses `--disambiguate` (object IDs only), ref collisions are irrelevant to the result. Excluding them is still a sound sanity check.
- **Fresh sandbox.** `target_type_measure` (`:739-781`) creates a `TemporaryDirectory`, does a `git clone --no-hardlinks --no-tags` of the lane (no alternates), runs `prepare` (detach at tip, set `refs/heads/<branch>`, remove origin, recreate `refs/remotes/origin/<branch>` at tip) and calls `materialize`. Fixture tag refs are deleted in `finally` (`:734-736`). The tag objects stay in the object store as dangling objects. They carry per-tool names, so each tool's inventory is still recomputed correctly.
- **No host read.** The consumer runs inside the sandbox under `clean_env()` (`:100-104`): GIT_* is stripped, `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`. `_revision.clean_env` repeats this. The host lane is read only by the judge itself (`bind(lane, …)`, `clone_lane`, `lane_tip`), which is expected.
- **The old matrix is unchanged.** `target_type_probes` is called only from `target_type_measure` (`:764`), which is reached only through `--object-target-types` (`:924`, `:1391-1409`). `measure()` and `object_selector_probes` (`:475-673`) contain no `tag_to_blob` row. `measure()` calls `object_selector_probes` at `:830` but not `target_type_probes`.
- **Commit-tag continuity.** `annotated_tag_to_commit` (`:703`) overlaps the old `annotated_tag_object` and `annotated_tag_prefix` cases (`:631-632`). It is continuity only, not new coverage.
- **C2 separation.** `target_type_mode` comes from an AST census of the judge (`:750-761`). Behaviour is counted separately per tool (`:763-767`). The binder is declared byte-identical to baseline, so this consumer's `tag_to_blob` behaviour is pre-existing. The mode going from 0 to 1 is a newly available measurement, not a 9-fold behavioural uplift (compare selftest `target-type-missing-mode-is-not-behavior-failure`, `:1251-1254`).

## Mutant analysis (proposed, NOT executed)
- **M1, generic peel in the binder:** `_revision.py:140` changes `f"{oid}^{{commit}}"` to `f"{oid}^{{}}"`. Prediction: for tag→blob, `sha` becomes the blob OID. `_commit(local)` still succeeds, so `_ancestor` runs `merge-base --is-ancestor <blob> refs/heads/master`. [INFERENCE] Git cannot resolve a blob as a commit and exits with code 128 or higher, so the result is `E-GIT-FAILED` at site `refs/heads/master`. `refused()` sees finding `E-GIT-FAILED` instead of `E-REVISION-INVALID`, so the row is not ok and the mutant is **killed**. This mutant survives the old matrix: tag→commit still peels to the same commit, and a direct blob is still stopped by the `cat-file -t` kind gate.
- **M1b, generic peel plus the legacy rule that merge-base exit ≥2 means "not ancestor":** the result becomes `E-REVISION-NOT-LANDED`. **Killed**, because the finding id differs.
- **M1c, peel failure falls back to `return oid` (the tag OID):** `merge-base` on a tag that peels to a blob also fails, giving `E-GIT-FAILED` [INFERENCE]. **Killed.**
- **M2, consumer change at `check-locator-clarification.py:788` that hard-codes the finding id `E-REVISION-INVALID` for every `RevisionError`:** this **survives the `tag_to_blob` row** because the expected id is the same. It is killed elsewhere, by the unlanded, not-pushed, branch-missing and git-failed rows of the old matrix. It is therefore not a false green for the tool-level grade.
- **M3, peel generically (`^{}`) only when the tag's direct target is a tag or commit, and refuse direct blob or tree targets:** for single-level tag→blob this gives `E-REVISION-INVALID`, so it **survives the row**, and that behaviour is correct for this class. A nested tag→tag→blob would come out as `E-GIT-FAILED`. No row tests a nested tag to a non-commit (`nested_tag_to_commit` only), so M3 survives all five classes. This gap is adjacent to the predicate (a nested-noncommit class), not inside it.

## Verdict for this predicate
No defect within `check-locator-clarification.py-tag_to_blob-candidate-control` on the frozen bytes:
- The consumer propagates the binder's single `E-REVISION-INVALID` unchanged.
- The row builds a real annotated tag over a real blob in a fresh sandbox clone, probes both the full ID and a sanity-checked unique prefix, and grades the exact ID with a count of one.
- The realistic false-accept and wrong-ID mutants (M1, M1b, M1c) are killed.

## Residual calibration gap (judge self-witness, not consumer behaviour)
- The selftest mutant witness (`check-revision-binding.py:1246-1259`) asserts only `tag_to_tree.ok == False` and `all(...) == False`. It never asserts that `tag_to_blob` kills `target-generic-peel`.
- `target-types-five-fixed-classes` (`:1234-1238`) checks only the set of class names and that the correct stub is all-ok.
- Proposed judge mutant J1, NOT executed: change `:700` to `"tag_to_blob": (blob, None)`, so the row uses a direct blob and duplicates `noncommit_blob`. Prediction: the judge selftest still passes. The correct stub refuses the direct blob. In the generic-peel stub (`:981-989`), a direct blob is not a `tag`, so `^{commit}` is used and fails, giving `E-REVISION-INVALID`. `tag_to_tree` stays False, so `all()` stays False.
- So the judge's own selftest does not pin that the `tag_to_blob` row really is a tag→blob fixture. The frozen candidate does build it correctly (`:700`), so this is a C3 self-verification limit, not a false green on the current bytes.

## Limits
- Git exit codes for `merge-base --is-ancestor` on a blob, or on a tag that peels to a blob, are inferred, not observed.
- If the host environment sets `PYTHONSAFEPATH`, the script directory drops off `sys.path` and `import _revision` fails. That would turn the row red (exit 1 with a traceback), never green. `clean_env` does not strip it.
- An uppercase selector is not exercised for this class. Uppercase is covered only by the old `uppercase_object` case on the tip.
- The fixture's `type blob` header is guaranteed by construction. The judge does not assert it.
- No outputs were observed, no non-author closure is claimed, and nothing is promoted. No tools were installed, and none were needed.

Scope: executed=none
