# Fx02TagBlob — falsify: check-root-dac-correction.py × tag_to_blob (candidate 0a14952b)

Reviewed-SHA256: 945081ef19d10661537fdac7b58a6627e4ca2dc072704b440c4eaf7fe1737b5f
Predicate: check-root-dac-correction.py-tag_to_blob-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Primary receipt binds only `candidate/tools/check-root-dac-correction.py` (SHA above, as listed in `candidate-files.json:9-13`, revision 0a14952b59d20179e1c813af58befaecd6992a17; digest supplied by the item and inventory, not recomputed — NO-EXEC).
Auxiliary frozen snapshot dependencies read (not bound by this receipt): `candidate/tools/_revision.py` (inventory SHA256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf, `candidate-files.json:64-68`) and `candidate/tools/check-revision-binding.py` (inventory SHA256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6, `candidate-files.json:39-43`). Build oracle compared: `build/Oracle02TagBlob.md`, `build/CritBaseline.md`, `build/ConnPlanner.md`. Structural comparison only: `snapshot/tools/check-revision-binding.py` def-line map.

## Axes
- **A1 consumer propagation**: argv → bind → error → JSON/exit for a tag→blob object ID.
- **A2 row construction**: actual typed object, fresh sandbox, unique prefix, no host read.
- **A3 row grading**: exact refusal ID/count versus the build oracle's expected output.
- **A4 discrimination/calibration**: which mutant this row kills that the old matrix misses, and whether the judge selftest witnesses that.

## Verdict
No consumer defect within this predicate: source predicts the frozen consumer refuses both tag_to_blob selectors (full tag OID and unique prefix) with exit 2 and exactly one finding, `E-REVISION-INVALID`, which is what the row grades. Two grading/calibration gaps were found. Neither makes the correct consumer fail, but each lets a concrete mutant go green:
- **G1, MEDIUM (A3)**: the row does not grade the `revision`/`status` output fields that the build oracle fixed. A consumer that refuses correctly but reports a commit SHA in `revision` passes.
- **G2, LOW (A4)**: no selftest assertion is specific to tag_to_blob. A judge mutant that turns the row into a raw-blob duplicate survives the judge selftest.

## A1 — Consumer propagation (source prediction, frozen candidate)
- `main` (`check-root-dac-correction.py:533-545`) passes `args.revision`/`args.branch` verbatim to `run_gate(ROOT, ...)`. `ROOT = Path(__file__).resolve().parents[1]` (`:37`), so inside the sandbox copy `sandbox/tools/<name>`, ROOT is the sandbox. `sys.path.insert(0, <tools dir>)` plus `import _revision` (`:27-29`) loads the sandbox's checked-out `tools/_revision.py` at the measured tip. `sys.dont_write_bytecode = True` is set before the import, so no `__pycache__` is written.
- `run_gate` (`:264-283`) has `revision` set, so it calls `_revision.bind(repo, revision, branch)` (`:275`).
- `_revision.bind` (`_revision.py:172-192`) runs these steps:
  - `validate_branch("master")` passes.
  - `REV.fullmatch` passes for 40-hex and for the ≥7-hex prefix.
  - `_object_commit` (`:112-146`) runs `rev-parse --disambiguate=<lower>`, which returns exactly one object (the prefix was chosen to be unique). `cat-file -t` gives `tag`, so it peels `oid^{commit}` (`:139-140`).
  - A tag→blob chain has no commit, so the peel fails. `rev-parse --git-dir` then succeeds, so the function returns `None` (`:143-145`).
  - `bind` raises `RevisionError(E_INVALID, "revision", "<rev> does not name one commit")` (`:177-179`) before the branch, ancestry or origin steps run.
- `run_gate`'s except branch (`:276-278`) sets `tip = branch_tip(...)` and raises `Cannot(exc.fid, ...)`. That is caught at `:281-282` and becomes `Result(CANNOT, [one Finding], 0)`. `label` stays the raw selector, because it is reassigned only on success (`:279`). `read_git` is never reached, so no documents are read.
- `emit` (`:231-233`) prints one JSON line: status `CANNOT_EVALUATE`, `revision` = the raw selector, `findings` = `[{"id":"E-REVISION-INVALID",...}]`, `correction_count` 0. `main` returns 2, which becomes the process exit code via `sys.exit` (`:548-549`).
- The prediction matches the build oracle's expected exit, finding id and field values (`Oracle02TagBlob.md:35-44`). The oracle's caveat that the consumer was "live/unpinned" is now resolved: this review reads the pinned candidate bytes.

## A2 — Row construction (`check-revision-binding.py:676-736`)
- **Actual typed object**: `blob_object` (`:408-413`) writes a real blob with `hash-object -w`. `tag("blob", blob)` (`:685-695`, `:700`) creates a real annotated tag object with `git tag -a r21-target-check-root-dac-correction-blob -m blob <blob>`. The selector is that tag's own OID (`ref^{tag}`), not a ref name. It is created independently with Git; the judge's `object_commit` is not used to build it, which satisfies the oracle requirement at `Oracle02TagBlob.md:22-23`.
- **Expected outcome**: `expected_commit=None` (`:700`), so both selectors go through `refused(..., ID_INVALID)`. The row is additionally tightened with `binding_ids == [ID_INVALID]` and `finding_count == 1` (`:721-725`). `finding_count` counts all findings, not only binding ones (`:391`), so an extra non-binding finding also fails the row.
- **Unique prefix sanity**: the inventory (`cat-file --batch-all-objects`, `:705-707`) is taken after all five fixture objects exist, because the dict literal at `:698-704` evaluates every `tag()` first. The prefix is the shortest one of at least 7 hex chars (and under the full length; the full OID is the other selector) that matches exactly one inventory object and has no `refs/heads/` or `refs/tags/` ref of the same name (`:712-718`). No objects are created between the inventory and the tool runs: the consumer is read-only, and `refused` writes nothing. Objects left behind by earlier tools' tags are included in the per-tool inventory, so uniqueness holds against them as well.
- **Fresh sandbox**: `target_type_measure` (`:739-781`) uses a new `TemporaryDirectory` per measurement, `clone_lane` (`--no-hardlinks --no-tags`), then `prepare` (detached checkout of the tip, origin remote removed, tracking ref recreated). One sandbox is shared by all nine tools, but the tag names include the tool name, a pre-existing ref raises `E-SANDBOX` (`:687-689`), and refs are deleted in `finally` (`:734-736`). The leftover objects only affect prefix uniqueness, which is handled above.
- **No host read**: the consumer reads only the sandbox (ROOT is the sandbox). `run_tool` sets `cwd=sandbox` and `env=clean_env()` (`:359-371`), which strips `GIT_*` and sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`. `_revision.clean_env` sets the same values (`_revision.py:62-66`). The lane is read only by the judge (`clone_lane`, `bind(lane,…)`, `lane_tip`), never by the consumer. Limit: as the judge docstring states (`:49-53`), this is not OS isolation; Python startup still reads the host interpreter and site-packages.

## A3 — Grading versus build oracle
The build oracle fixes these refusal facts: exit 2, exactly one `E-REVISION-INVALID`, status `CANNOT_EVALUATE`, and `revision` equal to the verbatim selector. It states that "any 40-hex commit appearing in `revision` ... is a failure" (`Oracle02TagBlob.md:38-40,50`).

The candidate `refused()` (`:383-393`) grades only `exit == 2` and the first finding id. The row adds `binding_ids` and `finding_count`. `json_revision` is recorded but never graded for refusals, and the JSON `status` field is never read. The comment at `:482-484` says "Grade the explicit status", but the code grades the process exit code, not `status`.

**G1 concrete false-green (proposed consumer mutant M1, NOT executed).** In the frozen consumer's `run_gate` except branch (`check-root-dac-correction.py:276-278`), change
`tip = _revision.branch_tip(repo, branch)` → `label = tip = _revision.branch_tip(repo, branch)`.
- **Source prediction for the tag_to_blob row**: exit 2 and a single `E-REVISION-INVALID` finding (`finding_count` 1), but `revision` is the full master tip commit SHA. The refused output now names a commit as if the selector had bound to it. `refused` returns ok, so the row passes for both selectors.
- **Other rows**: the same mutant passes every other refusal row in the new and old matrices, because `exact_refusal` (`:480-486`) and `probe_tool` also ignore `json_revision`. Accept rows are unaffected because the success path reassigns `label` at `:279`.
- **Oracle disagreement**: the build oracle would fail M1 at `Oracle02TagBlob.md:50`. This is a false-green against the preregistered expected output, not against the narrower implemented predicate.
- **Proposed control (not applied)**: in refusal grading, also require `json_revision in (None, selector)` and `doc.get("status") == "CANNOT_EVALUATE"`. Both the `object-selector-echo` stub (selector echo) and the default stub (`None`, `:948`) stay green under that control.

## A4 — Discrimination and calibration
- **New coverage for this class**: the old matrix has only a direct blob (`noncommit_blob` `:633`, `blob-revision` `:449`) and tag→commit (`annotated_tag_object`/`annotated_tag_prefix` `:631-632`). No old case tags a non-commit. Only two `tag -a` calls exist in the old region, and both target `tip`.
- **Mutant this row kills that the old matrix misses (generic peel `^{commit}`→`^{}` at `_revision.py:140`)**: source prediction is that the selector peels to the blob OID, then `_ancestor(blob, refs/heads/master)` exits ≥2, giving E-GIT-FAILED, or exits 1, giving E-REVISION-NOT-LANDED. Which exit path occurs is [INFERENCE]. Either way the id is not INVALID, so tag_to_blob kills it, while tag→commit and the direct blob stay green in the old matrix. This agrees with `CritBaseline.md:46` and `Oracle02TagBlob.md:64-68`.
- **G2 (calibration)**: the judge's mutant witness (`:1239-1259`) asserts only `tag_to_tree.ok == False` and `all(...) == False`. The second assertion is implied by the first. `TARGET_TYPE_WITNESS` reports only `tag_to_tree`. The five-class check (`:1234-1238`) asserts the key set and all-ok against the `object-selector` stub, which CritBaseline notes passes all five classes without a type gate (`CritBaseline.md:41`). No tag_to_blob-specific kill is asserted.
  - **Proposed judge mutant M2 (NOT executed)**: `:700` `(tag("blob", blob), None)` → `(blob, None)`.
  - **Source prediction**: every selftest check stays green. The key set is unchanged, the stub refuses a raw blob as INVALID, and the generic-peel stub still fails `tag_to_tree`. In production the row would silently degrade to a duplicate of `noncommit_blob` and stop killing generic peel through the blob path.
  - **Proposed control (not applied)**: also assert `new_mutant_cases["tag_to_blob"]["ok"] is False`, and/or check `cat-file -t <selector> == tag` and that the `type` line of `cat-file -p` is `blob`, as the oracle requires (`Oracle02TagBlob.md:19-21`).
- **Consumer-side gap, informational**: neither the consumer's own selftest (`check-root-dac-correction.py:386-495`) nor its CLI cases include a tag→blob selector. Coverage of this consumer rests on the judge row plus the binder selftest `annotated-tag-to-blob-invalid` (`_revision.py:413-419`), which exercises the binder only, not the consumer's CLI.

## Continuity and counting
- **annotated_tag_to_commit is continuity, not new coverage**: it overlaps the old `annotated_tag_object`/`annotated_tag_prefix` (`:631-632`; `ConnPlanner.md:29`).
- **Old matrix unchanged [INFERENCE]**: every `def` line from 1 through 672 has the same position in the snapshot and the candidate (`object_selector_probes` at 475, `noncommit_blob` at 633, `remove_ref(tag_ref)` at 672). The new functions are inserted after line 673. This is a structural comparison, not a byte diff.
- **C2 mode 0→1 is one availability fact**: `target_type_mode` is the AST function/option census (`:750-761`), counted once. It is not a ninefold behavioral uplift. The frozen binder is predicted to already refuse tag_to_blob at baseline, so `target_type_tools` measures non-regression (expected 9→9, not observed here).

## Observations vs inferences vs limits
- **Observed (source text read)**: every line citation above.
- **Inferences**:
  - Git exit codes: the `^{commit}` peel failing on tag→blob, and `merge-base` on a blob exiting ≥2 or 1.
  - `--disambiguate` and `cat-file --batch-all-objects` enumerating the same object set.
  - The old matrix being unchanged, which rests on def-line positions only.
- **Limits**:
  - Nothing was executed. M1 and M2 are proposals only.
  - No candidate or measured outputs were observed.
  - SHA256 digests come from the item and inventory and were not recomputed.
  - This is not non-author closure and not an outside promotion.
- **Tooling**: no tools were installed or updated; none were needed for a NO-EXEC source review.

Scope: executed=none
