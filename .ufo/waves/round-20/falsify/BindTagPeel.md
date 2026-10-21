# BindTagPeel — Round 20 attempt 1 source review

## Findings, by severity

### High — The C2 object-selector evaluator cannot reach its annotated-tag acceptance cases

Evidence in `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py`:

- `accepted` accepts four arguments and invokes `run_tool` without a branch: lines 393–401.
- The new `exact_accept` passes five arguments, including `branch`, to that function: lines 479–482.
- The first such call is `real_prefix_shadow_branch` at lines 590–594. The full annotated-tag OID and unique-prefix acceptance cases occur later, at lines 617–618; the full tag-object/ref-shadow case is at lines 602–609.
- `measure` invokes this path for each original-nine tool when `--object-selectors` is requested: lines 663–669. Its CLI catches an ordinary exception as `E-INTERNAL` and returns `CANNOT`: lines 1114–1118. The corresponding payload reports `object_selector_tools=0`, `object_selector_status=CANNOT_EVALUATE`, and no per-tool selector results: lines 733–743. `CANNOT` is 2: line 59.

**Impact:** [INFERENCE: static Python call/exception flow] Provided the earlier setup/probes complete, the first positive selector produces a positional-argument `TypeError`, before any annotated-tag acceptance is measured. The current candidate evaluator therefore cannot establish the preregistered C2 `0→9` result or distinguish returning a tag-object OID from returning its peeled commit. This is a production measurement-path defect, not a reproduced runtime result. The canonical R20 evaluation explicitly requests this path in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/measure/run.py:70-78`.

**Recommendation:** Make the acceptance helper's branch contract consistent with its caller and forward the selected branch to `run_tool` (which already supports it at candidate lines 359–366). Do not count the currently unreachable positive cases as exercised evidence.

### Medium — The binder's annotated-tag fixture setup uses an undefined helper before the positive peeling cases

`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:291-292` calls `git(repo, ...)` while constructing the annotated hexadecimal-name tag fixture. The module's Git helper is `_git` at lines 69–77; its imports are at lines 30–39 and the selftest's local checked helper is named `run` at lines 210–216. There is no `git` helper in this module's inspected declarations. This call is outside `expect`; `expect` itself catches only `RevisionError` at lines 198–208. The valid annotated-tag full-OID/prefix fixtures are later, at lines 315–323.

**Impact:** [INFERENCE: static name resolution/control flow] Once the setup loop reaches an unused candidate, it raises `NameError` rather than reaching either valid annotated-tag fixture. This is separate from the evaluator arity defect above. It prevents this source fixture from supplying corroborating tag-peeling evidence. R20's retained evaluator schedules each tool's selftest at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/measure/run.py:65-69`; no such execution was performed by this reviewer.

**Recommendation:** Use the module's defined Git helper for this lookup before relying on the subsequent fixture cases.

## Exact selector behavior supported by the inspected source

Review axes: object identity, tag-to-commit normalization, non-tag refusal, and honesty of finite C2 evidence. The assigned baseline and annotated-tag expectation are recorded at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:3,13-20,38-47`. The binder candidate location is recorded at that directory's `worktree-bindings.json:3-7`.

The following are source facts and static behavioral inferences, not executed outcomes:

| Input or invariant | Candidate implementation and fixture evidence |
| --- | --- |
| Full annotated tag-object OID | `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:119-142` enumerates objects, requires exactly one, checks its type, and requests `rev-parse <full-oid>^{commit}` only for type `tag`. `bind` stores the returned peeled SHA in `Binding.sha`, not the input tag OID: lines 172–192. |
| Unique abbreviated tag-object prefix | The same path lowercases the selector and disambiguates across **all object types before peeling**: `_revision.py:119-137`. Zero matches or multiple objects return `None`; `bind` raises `E-REVISION-INVALID`: lines 175–179. It does not merge different tag objects merely because they might peel to the same commit. |
| Tag-object OID versus peeled commit SHA | The source fixture creates an annotated tag targeting `tip`, obtains `tag_oid` with `refs/tags/peel-object^{tag}`, and expects `bind(...).sha == tip` for both full OID and unique prefix: `_revision.py:315-323`. The independent evaluator likewise obtains `tag_object` using `^{tag}` at `check-revision-binding.py:490-505`, selects a unique prefix at lines 576–583, and expects JSON `revision == tip`, not `tag_object`, at lines 617–618 and 393–401. These are dynamic fixture variables; no literal tag/peeled hashes or successful output for them were observed. |
| Actual commit object | `_revision.py:133-135` returns its already-disambiguated full OID directly. It does **not** run `^{commit}` for this non-tag case. |
| Blob or tree object | `_revision.py:136-137` returns `None` immediately for every type other than `commit` or `tag`; no peel call and no selector-ref retry follows. `bind` converts that to `E-REVISION-INVALID` before local-branch lookup: lines 177–181. Blob refusal is encoded at `_revision.py:359-362` and evaluator lines 619, 473–477. No tree fixture was observed in this path. |
| Hexadecimal ref without a matching object | Object enumeration with no unique match returns before type inspection/peeling: `_revision.py:119-124`. The hexadecimal lightweight/annotated ghost-ref cases explicitly expect `E-REVISION-INVALID`: evaluator lines 527–574. A ref name is not accepted as a substitute object selector in this control flow. |
| Existing tag-object OID shadowed by branch/tag names | The evaluator deliberately creates both refs named after the full tag-object OID pointing at a decoy, then expects the selected object's peeled `tip`: `check-revision-binding.py:590,602-612`. The binder fixture encodes the same distinction at `_revision.py:324-331`. These are intended assertions, not observed passes; the failures above prevent relying on them as executed evidence. |
| Tag that cannot peel to a commit | `_revision.py:139-146` returns `None` after a failed peel in a still-readable repository, without retrying the original selector as a ref. `bind` then reports `E-REVISION-INVALID` at lines 177–179. No nested-tag or tag-to-blob/tree fixture outcome was observed. |
| Landing/pushing checks use the commit, not the tag | `_revision.py:184-192` checks the resolved `sha` against the explicit local/origin branch refs and returns that same `sha`. An annotated tag is not an exemption from ancestry checks. |

The independent judge has its own object resolver, not an import of the binder: `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:139-166,192-208`. Its commit/non-tag/tag branches agree with the canonical module for this scoped path. This is a separate evaluator implementation, not a second production binder.

## Caller identity and error propagation

Literal import/call discovery was followed by targeted source reads. The original-nine denominator is defined in `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:61-80`. Each inspected production entrypoint uses the shared binding's **peeled commit SHA** for its successful revision label and committed-file reads, rather than retaining the tag-object selector as its successful revision identity:

- `/tmp/tsukuroi-r20-binder-20261021/tools/check-locator-clarification.py:782-795`
- `/tmp/tsukuroi-r20-binder-20261021/tools/check-root-dac-correction.py:264-283`
- `/tmp/tsukuroi-r20-binder-20261021/tools/check-section-citations.py:911-927`
- `/tmp/tsukuroi-r20-binder-20261021/tools/check-source-scope-correction.py:634-649`
- `/tmp/tsukuroi-r20-binder-20261021/tools/measure-update-recheck.py:471-481`
- `/tmp/tsukuroi-r20-binder-20261021/tools/check-boot-chain.py:1570-1584`
- `/tmp/tsukuroi-r20-binder-20261021/tools/check-freshness-r17.py:772-796`
- `/tmp/tsukuroi-r20-binder-20261021/tools/check-recheck-commands.py:744-763`
- `/tmp/tsukuroi-r20-binder-20261021/tools/check-seat-scope.py:258-272`

Those ranges also show the typed binding refusal being propagated through each caller's failure path; success and refusal are not interchangeable. Additional literal shared-binder consumers preserve the same identity: `/tmp/tsukuroi-r20-binder-20261021/tools/check-adjacency-anchors.py:651-676`, `check-appended-notices.py:475-502`, `check-boot-writers.py:569-595`, and `check-registry-coverage.py:312-342` under that same `tools/` directory. They are not additional C2 denominator credit.

## Residual risk and verification gaps

- No source-level defect in the canonical tag-only peeling/type gate was established in this slice. That is not a runtime pass or C2 admission; the two concrete evidence-path defects above remain actionable.
- The evaluator's canned `object-selector` stub is weaker than the production type gate: `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:813-818` unconditionally appends `^{commit}` after disambiguation, without checking `cat-file -t`. Its selftest at lines 1021–1030 therefore does not independently establish the invariant that non-tag objects are never peeled. A blob can be refused merely because that generic peel fails.
- The positive prefix fixture permits the full OID as its last candidate (`range(7, len(tag_object) + 1)` at evaluator lines 576–580; analogous binder fixture lines 319–321). Without retained concrete values it does not prove that this run selected a strictly abbreviated tag prefix. Prefix shadows are explicitly exercised for commit prefixes; the tag-prefix case avoids existing ref collisions, while tag-object shadow assertions use full OIDs.
- LSP was unavailable: reading `xd://lsp` returned `No such tool`, with only `ast_edit` and `debug` mounted. Status, references, definition, and diagnostics could not be obtained. The permitted literal-search fallback was used; grep matches are not semantic or runtime proof.
- Review used only scoped source/artifact reads and literal searches. No Git diff command, immutable-baseline materialization, candidate import, command, test, build, formatter, host probe, or external request was performed. The observed production helper calls `_commit` at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/_revision.py:134-141`, while the candidate calls `_object_commit` at candidate lines 172–179; this is a file-snapshot comparison, not independent proof of production HEAD or landing. No tools were installed or updated.
- Scope is finite selector behavior and its existing R20 evidence. No saturation, resume-continuity, host readiness, or boot-safety conclusion follows. Boot images remain UNKNOWN; no clearance is given.

Scope: executed=none.
