# Fx04Tree — `check-source-scope-correction.py` × `nonempty_tree`

## Axes and disposition

- **C2 operability / target-type predicate sensitivity:** two source-level false-green gaps in the candidate `check-revision-binding.py` matrix for accepted commit-tag selectors and abbreviated bare-tree selectors.
- **C2 continuity:** candidate code keeps `--object-selectors` and the new `--object-target-types` in separate mode paths. This source inspection does not establish historical equality or any runtime uplift. In particular, a mode-availability transition from 0 to 1 is not a behavioral nine-fold uplift claim.

**Disposition:** actionable test-oracle findings below. Current `_revision.py` source predicts correct refusal for a tree object; no candidate, test, or mutant was executed.

## Frozen candidate identities

- Target `tools/check-source-scope-correction.py`, revision `0a14952b59d20179e1c813af58befaecd6992a17`, SHA-256 `931504455caae52eaa2f2018a826c1b40c1eed83025ec0f13d1127c66fb85afc`.
- Auxiliary candidate snapshot `tools/check-revision-binding.py`, same revision, SHA-256 `0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6`.
- Auxiliary candidate snapshot `tools/_revision.py`, same revision, SHA-256 `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf`.
- The comparison oracle is the non-candidate draft at `.ufo/waves/round-21/drafts/ExecMatrix/check-revision-binding.py`; it is cited only for comparison, not represented as a pinned candidate dependency.

## Consumer bind/argv/error/output trace (source evidence)

1. The consumer defines `ROOT` from its own script path (`candidate/tools/check-source-scope-correction.py:18`). Its `--revision` path calls `_revision.bind(ROOT, args.revision, branch)` before any `read_git` calls (`:614-646`). A bind error is converted to `Cannot` and returned as a `CANNOT_EVALUATE` JSON result (`:639-649`). `emit` serializes status, revision, findings and count (`:336-343`). Only after successful binding does the revision path read the five documents through `read_git` (`:643`), then evaluate and emit (`:653-658`).
2. In `_revision.py`, `_object_commit` resolves a unique object ID, checks its actual type with `git cat-file -t`, accepts commits, and only peels tags with `^{commit}`; other types return `None` (`:112-146`). `bind` maps that `None` to `E-REVISION-INVALID` before branch ancestry checks (`:172-185`). Thus the current source predicts that a bare tree selector is refused before consumer document reads. This is a source prediction, not an observed invocation.
3. The target-type harness invokes each copied consumer by its real CLI with `--revision <selector> --branch <branch>`, with cwd set to the sandbox (`candidate/tools/check-revision-binding.py:359-371`). The harness creates a fresh temporary directory and clone before its matrix run (`:739-747`); the child consumer's `ROOT` therefore resolves inside that clone. The outer harness necessarily reads/binds the selected lane revision and clones the lane; the no-host-read statement here is limited to the consumer's tested selector/document access, not those harness setup reads.
4. For a refusal, the target-type row asks `refused` for `E-REVISION-INVALID` and then requires the one binding ID and exactly one finding (`:721-725`; `refused` records exit, finding count and IDs at `:383-393`). Current `_revision.py` source supports that expected refusal for the full tree object.

## Findings

### High — accepted target-type cases count exit 1 as success

**Evidence:** candidate `check-revision-binding.py:396-404` defines `accepted(...).ok` as `code != CANNOT` plus a matching JSON revision. `target_type_probes` uses this helper for both accepted classes (`:727`, `nested_tag_to_commit` and `annotated_tag_to_commit`). It does not require exit 0 or a success status. The consumer's normal post-bind path can instead return `FAIL`/exit 1 while retaining the resolved commit SHA: `emit` maps `FAIL` to status `FAIL` and prints the supplied revision (`check-source-scope-correction.py:336-343`); after binding, `main` evaluates documents and emits that result (`:653-658`). Therefore a consumer result with exit 1 and the expected SHA is graded `ok` by these accepted rows even though the gate reports failure.

**Concrete false-green prediction (not executed):** a post-bind consumer failure on a commit-tag input that emits `status: FAIL`, exit 1, and the resolved expected SHA passes the candidate acceptance predicate. The comparison oracle explicitly avoids this: draft `check-revision-binding.py:730-750` requires `case["exit"] == PASS` as well as the expected full SHA. This discrepancy is in the target-type acceptance oracle, not evidence that the current binder mishandles tags.

### Medium — `nonempty_tree` lacks the unique-prefix selector check

**Evidence:** candidate `target_type_probes` derives the commit's root tree and requires `ls-tree` to return entries (`check-revision-binding.py:678-682`), then stores `"nonempty_tree": (tree, None)` (`:697-704`). Its selector loop adds a unique prefix only when the label is not `nonempty_tree` (`:709-718`), so this row exercises only the full tree object ID. The refusal result is strict for each selector it does exercise (`:721-725`).

The comparison oracle builds a unique object prefix for the tree and includes both `full` and `unique_prefix` in `nonempty_tree` (`drafts/ExecMatrix/check-revision-binding.py:803-818`; its `target_type_case` grades all supplied selectors at `:723-750`). The candidate therefore omits a preregistered-type control present in the available build oracle.

**Concrete false-green prediction (not executed):** a consumer mutant that rejects a full bare-tree OID but mistakenly treats a unique abbreviated bare-tree OID as the landed commit could pass the candidate's `nonempty_tree` row, which never supplies the abbreviation; the oracle row would exercise it and fail. The tag-to-tree prefix control is not a substitute: it supplies an abbreviated *tag object* ID, not an abbreviated bare-tree ID. Current `_revision.py`'s object-kind branch is selector-width-independent in source (`:119-137`), but the candidate matrix does not test that bare-tree-prefix case.

## Oracle, limits, and verification gaps

- The candidate's `target_type_measure` counts five cases per present consumer and separates `target_type_mode` from `behavioral_tools` (`check-revision-binding.py:739-780`). Candidate CLI dispatch makes `--object-target-types` a separate path, disallows combining it with `--object-selectors`, and leaves the old default `measure(..., args.object_selectors)` path separate (`:912-926`, `:1381-1422`). This is source structure only; no execution or old-matrix equivalence was checked.
- No candidate tool, test, build, import, or proposed mutant was run. No actual runtime outcome is claimed.
- No LSP device/status route was mounted, so references/definition/diagnostics were not checked; cited conclusions are direct snapshot-text observations, not semantic-xref claims.
- Tool-policy disclosure: two exploratory read-only shell calls were inadvertently used to locate oracle text. They ran grep/head/ls-style queries only; no candidate script or test was invoked. Their output is not used as semantic proof; all evidence above comes from `read` results.
- No tool was installed or updated.

Reviewed-SHA256: 931504455caae52eaa2f2018a826c1b40c1eed83025ec0f13d1127c66fb85afc
Predicate: check-source-scope-correction.py-nonempty_tree-candidate-control
Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none