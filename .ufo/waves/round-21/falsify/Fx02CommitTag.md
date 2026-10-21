# Fx02CommitTag · check-root-dac-correction.py × annotated_tag_to_commit (falsify)

Reviewed-SHA256: 945081ef19d10661537fdac7b58a6627e4ca2dc072704b440c4eaf7fe1737b5f
Predicate: check-root-dac-correction.py-annotated_tag_to_commit-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Candidate revision 0a14952b59d20179e1c813af58befaecd6992a17. Primary file: `candidate/tools/check-root-dac-correction.py` (945081ef…). Auxiliary frozen snapshot dependencies, cited by digest from `candidate-files.json`: `candidate/tools/_revision.py` (06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf) and `candidate/tools/check-revision-binding.py` (0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6). For old-matrix comparison only: `round-21/snapshot/tools/check-revision-binding.py` (baseline). Build context: `build/Oracle02NestedTag.md`, `build/CritBaseline.md`, `build/ConnPlanner.md`. No moving draft or production file was read for the verdict.

## Verdict

The real candidate consumer is predicted to pass this row correctly. The row is still a degenerate control, and there is a concrete false-green mutant. The fixture tag always targets `tip`, and in the sandbox `tip` is also `refs/heads/<branch>` and `refs/remotes/origin/<branch>`. So the row's expected full commit SHA cannot tell "peeled the tag to its target" apart from "substituted the branch tip". A consumer-local mutant that reports and reads the branch tip for a tag selector stays green on this row, on its unique-prefix sibling, and on every other accept row in the judge and in the consumer selftest (section 4). This blind spot is inherited from round-20 `annotated_tag_object`. The new row preserves continuity, adds no new coverage, and does not regress anything.

Axes: C2 operability (is the consumer row discriminating?), C3 calibration (is the expected value fixed by construction, not by the binder?), and C1 depth only as context (is the source-grounded peel semantic reached?).

## 1. Consumer propagation (source trace, not executed)

- `main` (lines 533–545): `--revision` is mutually exclusive with `--selftest`, and `--branch` defaults to `master`. Both pass verbatim to `run_gate(ROOT, args.revision, args.branch)`. `ROOT = Path(__file__).resolve().parents[1]` (line 37), which is the sandbox clone when the judge runs `sandbox/tools/<name>`.
- Import (lines 27–29): `sys.path.insert(0, <tools dir>)` puts the sandbox `tools/_revision.py` ahead of PYTHONPATH and site paths. That file is the checkout at `tip` from `prepare` (judge lines 233–242, `checkout --detach tip`). `materialize` writes only the nine TOOLS names (judge lines 259–274), so `_revision.py` comes from the checkout, not from the host lane.
- `run_gate` (lines 264–283): calls `_revision.bind(repo, revision, branch)` (line 275). On `RevisionError` it records an informational `branch_tip` and raises `Cannot(fid, site, detail)`, which becomes `Result(CANNOT, [one Finding], 0)`. On success, `label, tip = bound.sha, bound.branch_tip` (line 279), and the four FILES are read with `git show <bound.sha>:<path>` (lines 280, 253–263).
- `payload` and `emit` (lines 224–233): one JSON line. `revision` is the label, which is the bound commit SHA on accept and the raw selector on a binding refusal. Exit code is `result.code` (0, 1 or 2).
- Error paths after a successful bind (`E-GIT-READ-FAILED`, `E-READ-FAILED`, missing r12 giving `E-R12-MISSING`) return exit 2 with `revision` set to the bound SHA. The judge's `accepted()` requires `code != CANNOT` (judge lines 396–404), so these paths can only produce a false red, never a false green.

## 2. Binder path for an annotated tag pointing at a commit (frozen `_revision.py`)

- `bind` (lines 172–192): `validate_branch` runs first. The selector, either the full tag OID T or a unique prefix of T, matches `REV` (7–64 hex).
- `_object_commit` (lines 112–146): `rev-parse --disambiguate=<lower>` returns exactly one OID, T. `cat-file -t T` returns `tag`. `rev-parse --verify --quiet --end-of-options T^{commit}` returns C = tip.
- Landing checks: `refs/heads/master` = tip, so tip is its own ancestor. `refs/remotes/origin/master` = tip after `prepare`, so the pushed check passes. The result is `Binding(tip, master, tip, tip)`.
- Source prediction for both selectors (full T and its unique prefix): exit 0 or 1 depending on the corpus at tip, never 2. JSON `revision` = tip in full lowercase 40-hex. Judge `accepted(...)` returns ok.

## 3. Judge row inspection (`target_type_probes`, candidate lines 676–736)

- Independently created typed object: met. `tag("commit", tip)` runs `git tag -a r21-target-check-root-dac-correction-commit -m commit <tip>` (lines 685–697). The tag OID comes from `rev-parse --verify <ref>^{tag}`, which is fixture creation, not the binder under test.
- Expected full commit SHA: met, but degenerate. The expected value is `tip`, the literal input to the tag creation (line 703 `(commit_tag, tip)`). So it is construction-fixed, which satisfies the spec's "Obtain expected object IDs directly from Git fixture creation, never binder" (build `spec.json` line 9). However, `tip` is also the result of the judge's own `bind(lane, tools_rev, branch)` (line 742), the sandbox branch tip, and the origin tip (lines 234–241). Those three identities collapse into one value (section 4).
- Unique prefix sanity: met. The inventory is taken after all four tags exist (lines 705–707). Prefix widths run from 7 to 39 (`range(7, len(object_id))`, line 712). The prefix must match exactly one inventory object and have no `refs/heads` or `refs/tags` name collision. If no prefix qualifies, `Cannot(E-SANDBOX)` is raised, which is a could-not-evaluate result rather than a silent skip. Each per-tool call rebuilds the inventory, so tag objects left over from earlier tools cannot break uniqueness.
- Accept grading: met. `accepted()` requires exit != 2, a string `revision`, and a case-insensitive match against `expect_sha` (judge lines 396–404). A selector-echo mutant is killed, because neither T nor its prefix ever equals tip. This is stronger than the commit `full_object_id` row, where an echo would pass.
- Fresh sandbox: met. `target_type_measure` makes its own `TemporaryDirectory` clone with `--no-tags` (lines 743–746), separate from `measure()`. `--object-target-types` and `--object-selectors` are mutually exclusive at the CLI (lines 1391–1395), so the old matrix's prefix inventory cannot be perturbed by these tags. That addresses the hazard raised in CritBaseline.md.
- No host read by the consumer: met (section 1). The consumer reads only the sandbox worktree and the sandbox object DB through `git -C <sandbox>`, using `clean_env` (GIT_* stripped, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`). The judge itself reads the lane (`bind(lane…)` and `lane_tip(lane…)`, lines 742 and 771). That is documented judge behavior, not a consumer read.
- Refusal ID and count: not applicable. This class is an accept row. The exact refusal-ID and count checks apply to `nonempty_tree`, `tag_to_blob` and `tag_to_tree` only (lines 721–725).

## 4. Concrete false-green mutant (proposed, NOT executed)

Mutant M-TIP edits only line 279 of `check-root-dac-correction.py`:

```python
label = bound.sha if len(revision) < 40 or revision.lower() == bound.sha else bound.branch_tip
tip = bound.branch_tip
```

The read at line 280 is unchanged and uses `label` in place of `bound.sha`. M-TIP triggers only when the selector is a full 40-hex OID that is not the bound commit, which means a full annotated-tag OID. Behavior: `--revision <tag OID>` reads the docs at the branch tip and reports the branch tip, whatever commit the tag actually targets.

Predicted survival, from source:

- This row, `annotated_tag_to_commit`: full T gives label = branch tip = tip = expected, so it passes. The prefix selector takes the unmutated path and also passes.
- `nested_tag_to_commit` (line 702): the expected value is also tip, so it passes.
- `nonempty_tree`, `tag_to_blob` and `tag_to_tree` refuse inside `bind` before line 279, so they are unchanged and pass.
- Old `--object-selectors` matrix: `annotated_tag_object` (line 631), `full_tag_object_id_ref_shadow` (lines 616–626) and every other accept row expect tip (lines 608, 613, 629–632), so it passes.
- Base `probe_tool`: `landed-parent` uses the full parent commit SHA, which equals `bound.sha`, so the mutant does not trigger and the row passes. The other accept rows expect tip (lines 422–427, 457), so they pass.
- Consumer selftest: `revision-short-tip`, `revision-upper-hex` and `revision-reads-landed-parent` (lines 419–422) all use commit selectors, so they pass.
- Judge selftest: the only typed mutant is `target-generic-peel`, which targets `tag_to_tree` only (lines 1239–1258). Nothing targets commit tags.

Defect consequence: a landed release tag on an older commit is graded against the tip's corpus and reports the tip SHA. This is a silent wrong-revision bind, the same identity class as Oracle02's nested-tag mutant M, reached here by tip substitution instead of a shallow peel. M-TIP is a consumer-local defect behind a correct shared binder, so the AST census `shared()` (judge lines 277–307) still counts the consumer as shared.

Killing control (suggestion only; no edit made): add, or switch to, an annotated tag targeting a landed non-tip commit, `tag("commit-parent", parent)` with expected = parent. Here `parent = tip^1^{commit}`, computed in `target_type_measure` the same way `measure()` computes it (lines 799–801). With that control, M-TIP returns tip ≠ parent and is killed. The same change applies to `nested_tag_to_commit`, which shares the collapse but is outside this predicate.

## 5. Build oracle comparison and old matrix

- No build oracle exists for this class. `ConnPlanner.md` line 29 records that the oracle fan-out covers Tree, TagBlob, TagTree and NestedTag only, "with no AnnotatedTag oracle", and labels `annotated_tag_to_commit` as overlap with round-20 `annotated_tag_object` (lines 29 and 71). `CritBaseline.md` lines 23 and 36–39 make the same overlap point.
- The nearest same-consumer oracle, `Oracle02NestedTag.md`, traced the consumer through `main` 533–545, `run_gate` 264–283 and `payload` 224–233. Those line ranges match the frozen candidate exactly, and that oracle's Reviewed-SHA256 is the same `_revision.py` digest 06b71e8c… as the candidate. My trace in sections 1 and 2 agrees with it.
- Old matrix unchanged: grep of `probe_tool` and `object_selector_probes` case keys shows identical keys at identical line positions (416–673) in the baseline `snapshot/tools/check-revision-binding.py` and the candidate. The new code starts at candidate line 676, where the baseline's `measure()` began. Limit: this is a positional key comparison, not a byte diff.
- C2 framing: `target_type_mode` 0→1 is an AST presence bit on the judge at the measured revision (lines 750–759, counted once). For this consumer the row is predicted green at baseline as well, because the binder digest is unchanged and the baseline trace matches CritBaseline.md line 23. So it is not a behavioral 9-fold uplift. For commit tags, `target_type_tools` reflects continuity and non-regression only.

## 6. Observations, inferences and limits

- Observed (source read): consumer call chain and payload fields; binder disambiguate → type → peel order; `target_type_probes` construction, inventory, prefix rule and grading; every accept row's expected value (tip, or full parent only in `landed-parent`); CLI mutual exclusion; old-matrix case keys at the same positions as the baseline.
- [INFERENCE]: the git behaviors `tag -a <name> <commit>`, `^{tag}` and `^{commit}`, `--disambiguate` uniqueness, and the absence of auto-created refs in a `--no-tags` clone; the corpus files existing at revision 0a14952 (a missing file would give a false red, not a false green); and the bytes materialized at `tip:tools/check-root-dac-correction.py` equaling the frozen 945081ef… snapshot.
- Limits: nothing was executed, so all predicted exits and JSON values are source predictions, not observations. M-TIP was not executed. This review does not claim non-author closure or outside promotion. No tool was installed or updated; none was needed for source review, and the seat is NO-EXEC.

Scope: executed=none
