# Fx04TagBlob — falsify check-source-scope-correction.py × tag_to_blob (candidate control)

Reviewed-SHA256: 931504455caae52eaa2f2018a826c1b40c1eed83025ec0f13d1127c66fb85afc
Predicate: check-source-scope-correction.py-tag_to_blob-candidate-control
Lane bounds: leaf member — no subagent dispatch.

## What this review covers

- Primary file: `candidate/tools/check-source-scope-correction.py`, revision 0a14952b59d20179e1c813af58befaecd6992a17. The SHA-256 above is the value that `candidate-files.json:14-18` lists for this file.
- Auxiliary snapshot dependencies, all read only from `.ufo/waves/round-21/candidate`:
  - `tools/_revision.py`, inventory SHA-256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf, from `candidate-files.json:64-68`.
  - `tools/check-revision-binding.py`, inventory SHA-256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6, from `candidate-files.json:39-43`.
- Context only, not candidate evidence:
  - The build oracle `build/Oracle04TagBlob.md`.
  - `build/CritBaseline.md`.
  - The pinned `snapshot/tools/check-revision-binding.py`, which I read only to compare case keys.
- I did not hash any file myself. Every SHA-256 above is quoted from the inventory.

## Verdict

**There is no defect in this predicate.** By source prediction, the frozen consumer refuses both `tag_to_blob` selectors with:
- exit code 2,
- status `CANNOT_EVALUATE`,
- exactly one finding, `E-REVISION-INVALID`.

The candidate judge row grades exactly that tuple. I found no false-green path for the actual candidate consumer.

There is one weakness in the control itself:
- The judge's selftest never shows that the `tag_to_blob` row can kill anything.
- Its generic-peel witness only asserts the `tag_to_tree` row.
- So a judge mutant that weakens only the `tag_to_blob` row would survive the judge's own selftest (mutant M-J1 below).

This is a calibration gap in the control. It is not a false green for this consumer.

## Axes

- **A1 binding/argv:** the consumer's selector and branch reach `_revision.bind`.
- **A2 error/output propagation:** the exit code, finding id and count, and the JSON `revision` field.
- **A3 judge-row construction:** a real typed object, the selectors, a sandbox, unique-prefix sanity, and no host read.
- **A4 grading strictness:** what the row accepts.
- **A5 mutant discrimination:** what this row kills, and what the selftest actually witnesses.
- **A6 continuity:** old matrix unchanged, the commit-tag row, and C2 mode 0→1 versus behavior.

## A1/A2 — consumer path

Everything in this section is observed in the source and was not run.

**Command line.** The judge runs the consumer with `--revision <sel> --branch master` (`run_tool`, judge L359-371). The consumer gets no extra arguments, because `EXTRA[name] = ()` (L77). argparse puts `--revision` and `--selftest` in a mutually exclusive group, and `--branch` defaults to `master` (consumer L617-623).

**Binding call.** The consumer sets `revision = args.revision` and calls `_revision.bind(ROOT, args.revision, branch)` with the selector verbatim (L636-639).
- `ROOT = Path(__file__).resolve().parents[1]` (L18), which is the sandbox clone.
- `import _revision` (L15) resolves to `sandbox/tools/_revision.py`, because the script directory is `sys.path[0]`.

**Inside `bind`** (`_revision.py` L172-179):
1. `validate_branch("master")` passes.
2. `REV` (7-64 hex) passes for both the 40-hex tag ID and the 7-39-hex prefix.
3. `_object_commit` (L112-146) runs `rev-parse --disambiguate=<lower>`, which returns exactly one object, the tag.
4. `cat-file -t` returns `tag`.
5. The binder peels with `rev-parse --verify --quiet --end-of-options <oid>^{commit}`. A tag whose target is a blob cannot peel to a commit, so that call returns non-zero.
6. `rev-parse --git-dir` succeeds, so `_object_commit` returns None.
7. `bind` raises `RevisionError(E-REVISION-INVALID, "revision", "<sel> does not name one commit")`. This happens before any check on the branch, landed state or origin, so the origin ref does not affect the result.

**Error and output.** The consumer converts the error 1:1 into `Cannot(exc.fid, exc.site, exc.detail)` (L640-641). It then emits `Result(CANNOT, [one Finding], 0)` with:
- `revision` equal to the selector as given,
- `branch` = `master`,
- `branch_tip=None`, because `branch_tip` is only assigned after a successful bind (L642, L647-649).

`emit` prints one sorted-keys JSON line with `"status": "CANNOT_EVALUATE"` and returns 2 (L336-343). `sys.exit(main())` turns that into exit code 2 (L661-662). No `read_git` call happens and `evaluate` is not reached.

**Prediction:** for both the full and the prefix selector, exit 2, `findings == [{"id": "E-REVISION-INVALID", "site": "revision", ...}]`, and `correction_count` 0. This matches `build/Oracle04TagBlob.md:24-39` on every field.

## A3 — the candidate judge row

Everything in this section is observed in the source and was not run.

- **Fresh sandbox.** `target_type_measure` (L739-781):
  - It binds `--tools-revision` independently with the judge's own `bind` (L192-208).
  - It creates its own `TemporaryDirectory` clone (L743-745) and runs `prepare`: detached checkout of the tip, `refs/heads/master` set to the tip, origin remote removed, `refs/remotes/origin/master` set to the tip (L233-242).
  - The mode is mutually exclusive with `--object-selectors` (L1391-1395), so the two matrices never share one object inventory. That resolves the inventory hazard raised in CritBaseline:49-57.
  - Limit: the sandbox is fresh per run, not per tool. All nine tools share it. This consumer is fourth in `TOOLS`, at L65.
- **Real typed object, created independently:**
  - `blob_object` writes the blob with `git hash-object -w --stdin` (L408-413).
  - `tag("blob", blob)` creates an annotated tag with `git tag -a r21-target-check-source-scope-correction-blob -m blob <blob>`. It refuses if that tag name already exists, and it takes the tag object ID from `rev-parse --verify <ref>^{tag}` (L685-695, L700).
  - Because the target was created by `hash-object`, it is a blob by construction.
  - [Limit] The judge never asserts `cat-file -t` = `tag` or a `type blob` header on the created object. The class label rests on how the fixture is built, which is sound, but nothing re-checks it.
- **Selectors.** The row tests the full tag object ID plus one prefix (L710-718). The prefix is the shortest width from 7 to 39 that:
  - is unique against `cat-file --batch-all-objects`, taken after all four tags were created (L705-707), and
  - has no colliding `refs/heads` or `refs/tags` entry.
  The prefix lookup excludes the full width. If no prefix qualifies, the judge reports `E-SANDBOX` rather than a green. The inventory comes from the same object database that the consumer's `--disambiguate` reads, so the "exactly one object" step holds.
- **No host read.** The tool runs with `cwd=sandbox` from `sandbox/tools/<name>`. The consumer's `ROOT` and its imported `_revision` both resolve inside the sandbox, and `clean_env()` strips `GIT_*` and sets `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1` (L100-104).
  - [INFERENCE, environment-conditional] `clean_env` passes `PYTHON*` variables through. If `PYTHONSAFEPATH=1` were set and `PYTHONPATH` pointed at a host `tools/` directory, `import _revision` could load a host copy.
  - This needs an unusual caller environment, and it is not a consumer source defect.
- **Cleanup.** The tag refs are deleted in a `finally` block (L734-736). The tag and blob objects stay in the shared sandbox inventory, and later prefix calculations account for them.

## A4 — grading strictness

- The refusal branch requires all of the following (L721-725, using `refused` at L383-393):
  - `code == CANNOT`,
  - the first finding id equals `E-REVISION-INVALID`,
  - the binding-id list is exactly `[E-REVISION-INVALID]`,
  - `finding_count == 1`.
- The echoed `revision` is correctly not treated as an accepted binding.
- At tool level, `behavior_ok` needs all five classes (L765). A consumer that refuses everything passes the `tag_to_blob` row alone but fails the `annotated_tag_to_commit` and `nested_tag_to_commit` accept rows. Those rows require the JSON `revision` to equal the tip exactly (L396-404).

## A5 — mutants (proposed, NOT executed)

### Consumer and binder mutants the row kills (source prediction)

**M-B1, the oracle's generic peel.** In `_revision._object_commit` L139-140, change `f"{oid}^{{commit}}"` to `f"{oid}^{{}}"`.
- `sha` becomes the blob ID, and `_ancestor(blob, refs/heads/master)` runs.
- [INFERENCE] `merge-base` exits with 2 or more, which gives `E-GIT-FAILED`. If a git version returned 1 instead, the result would be `E-REVISION-NOT-LANDED`.
- Either way the finding is not `E-REVISION-INVALID`, so the row fails.
- The old matrix stays green: `noncommit_blob` is a bare blob and is rejected at L134-137, and the tag→commit cases still peel correctly.
- So this row (together with `tag_to_tree`) is real new discrimination.

**M-B2.** For a tag, return the tag ID without peeling. `merge-base` then fails on a tag that points at a blob, so the result is `E-GIT-FAILED` and the row fails.

**M-C1.** In the consumer, replace `exc.fid` at L641 with a constant. This is killed by the old matrix's `unlanded`, `not-pushed` and `branch-missing` probes, not by this row. Recorded only for completeness.

### Control gap that survives the judge selftest (proposed, NOT executed)

**M-J1.** In `target_type_probes` L723-725, relax only the `tag_to_blob` row, for example:

```python
observed["ok"] = observed["exit"] == CANNOT if label == "tag_to_blob" else (observed["ok"] and ...)
```

Prediction: the judge selftest stays green, because:
- `target-types-five-fixed-classes` (L1234-1238) runs the correct `object-selector` stub. That stub's `^{commit}` peel refuses tag→blob with `E-REVISION-INVALID` (L981-993), so every row is still ok.
- `tree-tag-mutant-new-matrix-rejects` (L1246-1250) and the `TARGET_TYPE_WITNESS` line (L1255-1259) check only `new_mutant_cases["tag_to_tree"]["ok"]` and the all-rows conjunction. `tag_to_tree` still fails under the generic-peel stub, so `(False, False)` holds.

The stub would actually produce `E-GIT-FAILED` for `tag_to_blob` (L986-989 and L997-1001; `LEGACY` is false at L941). That is a kill which exists but is never asserted.

Consequence: the selftest does not show that the `tag_to_blob` row is discriminating on its own. A false green from this would need M-J1 plus a binder mutant that fails only on blob targets, for example one that rejects tree targets after a generic peel but lets blobs through. Neither exists in the candidate snapshots. **It is a gap in the control's calibration, not an observed false green.**

Smallest fix (for L1, not applied): add `new_mutant_cases["tag_to_blob"]["ok"] is False` to the check at L1248-1250, or have the witness report each row's kill separately.

## A6 — continuity

- **Old matrix unchanged.** The `object_selector_probes` case keys are line-identical in the snapshot and the candidate judge (L475-673, including `annotated_tag_object` L631, `annotated_tag_prefix` L632 and `noncommit_blob` L633), and the new mode runs in a separate sandbox. I observed this by comparing the grep output for the case keys. I did not diff the whole file.
- **Commit-tag rows.** `annotated_tag_to_commit` (L703) duplicates the old `annotated_tag_object`/`annotated_tag_prefix` accept path. It continues that coverage and is not new coverage. Per ConnPlanner:29, the genuinely new cells for this consumer are `tag_to_blob`, `tag_to_tree`, `nested_tag_to_commit` and `nonempty_tree`.
- **C2 mode.** `target_type_mode` is a single AST presence bit computed once per run (L750-761, L773). The behavior count `target_type_tools` is computed separately per tool (L763-767). A mode change from 0 to 1 is one fact about the judge, not a ninefold behavioral uplift. By source prediction, this consumer is already green at baseline, because `_revision.py` has the same inventory digest as the baseline (06b71e8c…, matching the Oracle04 Reviewed-SHA256), and its own selftest has `annotated-tag-to-blob-invalid` at `_revision.py` L413-419.

## Observations, inferences and limits

- **Observed (source text):** every line citation above.
- **Inferred:**
  - the exact exit code from `git merge-base --is-ancestor <blob> <ref>`,
  - the `PYTHONSAFEPATH` import hazard,
  - that real git behaves as the source assumes for `--disambiguate` and `^{commit}`.
- **Limits:**
  - No LSP server was used. I traced definitions and callers by reading the source directly and with literal grep, so this is not semantic proof.
  - I did not compute any SHA-256.
  - I did not read any moving draft or production file.
  - Nothing was executed, so no candidate output was observed.
  - I make no claim about non-author closure or outside promotion.
- **Tooling:** I installed or updated nothing, and nothing was needed.

Scope: executed=none
