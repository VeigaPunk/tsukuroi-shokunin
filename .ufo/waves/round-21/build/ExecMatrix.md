# Round 21 C2 object-target-type matrix — ExecMatrix

Axes: **operability** (explicit mode availability), **behavioral accuracy** (the original nine real CLIs), **calibration** (old-matrix miss versus new-matrix mutant kill), and **scope safety** (unchanged selector matrix; no extra-tool execution in the new finite mode).

## Findings

- Wrote the full replacement draft at `.ufo/waves/round-21/drafts/ExecMatrix/check-revision-binding.py`, starting from the pinned checker. It adds opt-in `--object-target-types`, the five requested per-tool cases, Git-derived object IDs/expected commits, exact single-finding invalid refusals, exact accepted commit checks, and unique tag prefixes where available.
- Mode availability is `0` in the pinned baseline (its parser has no `--object-target-types`) and `1` in the draft; this implementation-presence delta is not a behavioral uplift claim.
- Output separates `target_type_mode_available` from behavioral `target_type_tools` / `behavioral_tools` and reports `target_type_tools0` as a direct source-handler census, not as a behavioral count or grade gate. This avoids manufacturing consumer-source improvement from a behavioral pass. The finite mode skips CLI execution of discovered tools outside the original nine. The existing `--object-selectors` function, case names, count, and mode path are retained.
- Hermetic selftest fixtures encode a tag-to-tree peeling mutant, malformed refusal output, and multi-finding refusal. Their assertions require the old matrix to remain green while the new `tag_to_tree` case fails. These are authored fixtures, **not executed results**.

## Retained source evidence

- Pinned `snapshot/tools/_revision.py:112-146`: `_object_commit` uniquely resolves object IDs, checks `cat-file -t`, accepts commits directly, rejects non-tags, and only peels tags with `^{commit}`. The helper import/binding path is unchanged.
- Pinned checker `snapshot/tools/check-revision-binding.py:475-673`: the old object-selector matrix covers commit/annotated-commit tag and blob cases, but has no tag-to-tree decision row. This supports the inference that a tree-peeling mutant can remain green under the old matrix and be exposed by the new row.
- Assignment-provided baseline identity is recorded below; no hash command was run under NO-EXEC.

## Integration notes, checks, and limits

- L1 should run the draft selftest and the selected type-mode integration against the intended measured revision, then confirm the unchanged `--object-selectors` output/case set. No test, build, lint, formatter, import, or script was run in this lane.
- Runtime `behavioral_tools=9/9` and the old-matrix/new-matrix mutation outcome remain unobserved here; the selftest and output fields are prepared to report those separately. `target_type_tools0` is intentionally not promoted to nine on behavioral evidence.
- LSP was unavailable in the mounted tool inventory. No tools were installed or updated; installation is forbidden by this lane's NO-EXEC boundary.
- The existing checker trust boundary remains: a temporary clone is not OS process isolation. The new matrix limits additional-script execution but still runs the original-nine reviewed CLIs.

Reviewed-SHA256: da000de45b07ec2e4942ed798f6b9a7555c99180245d2139a94648cc4566b9e0
Predicate: C2-new-explicit-target-type-matrix
Scope: executed=none