# CritBaseline — C2 coverage versus behavior (round 21)

Reviewed-SHA256: da000de45b07ec2e4942ed798f6b9a7555c99180245d2139a94648cc4566b9e0
Predicate: C2-coverage-versus-behavior
Lane bounds: leaf member — no subagent dispatch.

Axes: operability (C2 metric `target_type_tools`), calibration (truth of the before/after figures), coverage (whether the checks can tell good tools from bad ones). Pinned inputs: snapshot `tools/check-revision-binding.py` (da000de4…) and, as context, snapshot `tools/_revision.py` (06b71e8c…) and `preregister.json`.

## Verdict

Yes, the claimed `before: 0` can be misleading. The new type probes will almost certainly pass against the baseline binder. If `target_type_tools` counts behavior, the honest result is 9 before and 9 after, so nothing improved. If it is forced to 0 at baseline through a check for "the judge has this mode", that one fact about the judge gets multiplied across nine tools. That is count inflation and false provenance, not a measured consumer delta. This is a defect that can be fixed by splitting the metric (see the correction below). It is not a tradeoff that must be rejected outright.

## Counterexample: baseline behavior is already correct

[INFERENCE from source; nothing executed.] I traced the pinned `_revision.bind` → `_object_commit` (lines 112-146) for each of the five new cases:

| case | path in baseline binder | predicted outcome |
|---|---|---|
| nonempty_tree | object type `tree` is neither `commit` nor `tag`, so it returns None | exit 2, E-REVISION-INVALID, one finding |
| tag_to_blob | type `tag`; peeling with `oid^{commit}` fails, so it returns None | exit 2, E-REVISION-INVALID, one finding |
| tag_to_tree | same as tag_to_blob | exit 2, E-REVISION-INVALID, one finding |
| nested_tag_to_commit | `^{commit}` peels recursively through both tag levels | accepted, exact landed commit |
| annotated_tag_to_commit | peels to the commit | accepted, exact landed commit |

- Observation: all nine original tools import `_revision` (grep of the current `tools/`; those files are not pinned, so the per-tool details are in the Oracle reports). Consumer behavior therefore collapses to one binder, and every predicted green is green ×9.
- Observation: round-20 lessons line 61 recorded `object_selector_tools` 0/9→9/9, measured by running the new judge against the baseline revision. That was a real behavioral delta, because the old binder accepted hex ref aliases. Repeating the same procedure in round 21 should give about 9/9 at baseline [INFERENCE]. "0 before" is only true if the procedure changes.
- Observation: the preregistered command is `check-revision-binding.py --tools-revision <REV> --object-target-types`, and it does not pin which judge's bytes produce the before figure:
  - Running the baseline judge fails at the CLI with E-CLI, exit 2 (`build_parser` has no such flag). That result is CANNOT_EVALUATE with no `target_type_tools` key, so recording it as 0 is false provenance.
  - Running the new judge with `<REV>=baseline` gives about 9.
- Observation: `measure()` runs whatever judge is in the working tree (`ROOT`, line 1254). Any "implementation presence" check on `REV:tools/check-revision-binding.py` therefore grades bytes that are not the ones executing. That splits identity between the evidence and the measurement.

## The old matrix already covers part of this

The existing `--object-selectors` matrix (20 cases, lines 474-673) already includes:

- `annotated_tag_object` and `annotated_tag_prefix`, which are the same as the new annotated_tag_to_commit.
- `noncommit_blob`. Most realistic mutants handle tree and blob the same way (anything not a commit or tag returns None, or the `^{commit}` peel fails), so nonempty_tree adds little for those.

Counting annotated_tag_to_commit as new coverage double-counts. The cases that are genuinely new are tag_to_blob, tag_to_tree and nested_tag_to_commit. nonempty_tree only adds discriminating power against a mutant that admits trees specifically, for example `kind in {commit, tree}`.

The selftest stub `object-selector` (lines 872-877) is weak in the same way. It uses `--disambiguate` plus `^{commit}` with no type gate, and it would pass all five new cases [INFERENCE]. Green results therefore cannot separate a type-checking binder from a non-type-checking one. Only targeted mutants can.

## Mutants that fail the new cases while the old matrix stays green [INFERENCE]

- **One-level peel.** For a tag, read its `object` header and require that target to be a commit. nested_tag_to_commit is wrongly refused; `annotated_tag_object` stays green.
- **Generic peel.** For a tag, peel with `oid^{}` and take the result whatever its type. tag_to_blob and tag_to_tree come out as E-GIT-FAILED or as accepted, not INVALID. The old matrix has no tag-to-noncommit case, so it stays green.
- **Tree admitted.** Treat `tree` like `commit`. `merge-base` on a tree exits 128, giving E-GIT-FAILED, so nonempty_tree fails; `noncommit_blob` stays green.

## Hazard to the existing matrix

When both modes run in one sandbox, `object_selector_probes` builds its prefix-uniqueness inventory with `cat-file --batch-all-objects` (lines 510 and 568). Extra tag objects from the type mode change which prefix widths get chosen, which changes the old cases' inputs. Deleting a ref does not remove annotated tag objects from the object database.

To preserve the old matrix exactly:

- Run the type mode only after the old matrix finishes, or in a fresh inventory.
- Use tag names that cannot collide with `r20-object-selector-*`.
- Leave the 20 old case keys, `object_selector_tools/total/status`, and `grade()` unchanged when `--object-target-types` is not given.

## Smallest safe correction (for L1 and ExecMatrix)

1. **Split C2 into three fields; never publish "target_type_tools 0→9".**
   - `target_type_mode`: 0→1. The before value is the observed baseline judge result (E-CLI, exit 2). It is recorded as "absent", not as 0 tools.
   - `target_type_tools`: behavioral, from the new judge run at both baseline and final revisions. Expected 9→9 [INFERENCE]. Report it as non-regression, not as gain.
   - `target_type_mutants_killed`: from the hermetic selftest. Count the mutants above that fail the new cases while the old `--object-selectors` result stays PASS on the same fixture. 0 before, k after. This is the actual coverage improvement.
2. **Do not zero the behavioral count.** Do not set `target_type_tools` to 0 for "source lacking explicit type coverage" when the probes are green. If a presence bit is kept:
   - Derive it from the AST of the executing judge (a real `add_argument("--object-target-types")` call), not from a byte search that a comment could satisfy.
   - Emit it once, not once per tool.
   - Report the SHA-256 of the executing judge and whether it equals the `REV` blob.
3. **Amend the preregistered C2 wording to name which judge produces each figure.** Before: the baseline judge for mode presence, and the new judge at the baseline revision for behavior. Otherwise the 0→9 headline overstates the improvement.

## Limits

- Everything above comes from reading the pinned snapshot plus context files. The per-case predictions are [INFERENCE] and were not run against Git.
- I did not inspect the ExecMatrix draft (it is a moving candidate) or the consumer argument propagation (that belongs to the Oracle seats).
- No tool installs were needed or done.
- This review does not judge, admit or close C2.

Scope: executed=none
