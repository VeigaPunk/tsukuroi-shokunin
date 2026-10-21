# Fx01Tree — `check-locator-clarification.py` × `nonempty_tree`

## Axes

- **C1 depth:** whether the real revision-binding path distinguishes a Git tree object from a commit and propagates that decision through the consumer CLI.
- **C2 operability:** whether the explicitly selected target-type mode sends a real tree object through this consumer in an isolated sandbox and grades the refusal.
- **C3 calibration:** whether the row catches a concrete output-contract mutation while preserving continuity with the pre-existing commit/tag matrix.

## Finding

### P2 — The `nonempty_tree` row can pass with a corrupted refusal payload

The current consumer's source path is correct for this input, but the new matrix grades only the refusal class and finding count, not the complete refusal fields that the consumer emits.

- `tools/check-revision-binding.py:676-683` obtains the tree object from the measured tip and checks `git ls-tree` produced entries, so this is a nonempty tree and not a mocked kind label. At `:697-704` the `nonempty_tree` case uses that tree OID with no expected commit.
- At `:709-732`, the tree selector remains the full object ID (`if label != "nonempty_tree"` skips prefix creation). Its refusal is expected to be `E-REVISION-INVALID`; lines 722-725 strengthen the row to require `binding_ids == [ID_INVALID]` and exactly one finding. The generic `refused()` at `:383-393` requires exit `CANNOT` and the expected first finding ID. It records `json_revision`, but does not include it in `ok`.
- The consumer's observable refusal is broader: `tools/check-locator-clarification.py:784-795` converts the binder error to a `Finding` and emits `CANNOT`; `payload()` at `:427-435` exposes `status`, raw `revision`, `branch_tip`, `correction_count`, and each finding's `id`, `site`, and `detail`. The historical source-only oracle `build/Oracle01Tree.md:18-23` specifically expects the raw selector to be echoed and the single finding to have site `revision` and detail `<selector> does not name one commit`.

**Concrete unexecuted false-green:** changing the consumer's error path to set `revision = "worktree"` instead of `args.revision` (or changing the emitted finding `site`/`detail` while retaining its ID) leaves the tree row's checked predicates satisfied: exit 2, one `E-REVISION-INVALID`, and finding count 1. The row does not assert JSON `revision`, status, site, detail, or correction count. This is a matrix-output-contract gap, not evidence that the current consumer produces the wrong payload. No mutant was executed.

## Source observations

- The frozen primary candidate is `candidate/tools/check-locator-clarification.py`, revision `0a14952b59d20179e1c813af58befaecd6992a17`, SHA256 `cd24d07ce71e3a3c5cff92802b69f3b2630aa5942a437ad00e53469387b05814` (assignment-provided; not recomputed).
- The consumer sets `ROOT` from the script location (`:23-24`); `main()` passes the raw `args.revision` to `_revision.bind(ROOT, args.revision, branch)` (`:780-790`). On `RevisionError`, it preserves `args.revision`, carries `exc.fid/site/detail` to one `Finding`, and returns through the `CANNOT` path (`:784-795`). Evaluation and corpus reads happen only after binding succeeds (`:799-804`).
- Candidate `_revision.py` (`:112-146`, `:172-192`) resolves the OID, checks its actual `cat-file -t` kind, returns `None` for a tree (only commits pass directly; only tags are peeled with `^{commit}`), and raises `E-REVISION-INVALID` before branch existence/ancestry checks. Thus the expected source prediction for a unique raw tree OID is one invalid-revision finding; no corpus read follows. That is a source prediction, not a runtime observation.
- The judge invokes the selected consumer with `--revision` and `--branch` in `run_tool()` (`candidate/tools/check-revision-binding.py:359-371`). `target_type_measure()` creates a `TemporaryDirectory`, clones the lane with `clone_lane()`, prepares the sandbox, and invokes the probes there (`:739-780`). The consumer's `ROOT` therefore resolves to that sandbox, and `_revision.bind` / `branch_tip` use that same root. For this row, `read_git()` is not reached after a tree refusal. This source establishes no consumer read of the host worktree; the judge necessarily reads/clones its selected lane to construct the sandbox.
- The row uses a full tree object ID, not a unique abbreviated tree prefix. The helper's prefix-generation check for the other classes at `:711-718` requires a prefix of at least seven characters, unique in the object inventory, with no branch/tag ref collision. No such prefix sanity claim applies to this tree selector. Consequently, this row does **not** establish behavior for a shortened tree prefix; `Oracle01Tree.md:23` describes that as a further expected case.

## Comparison and scope controls

- `build/Oracle01Tree.md` is a prior source-only oracle, not a candidate runtime receipt. Its type decision agrees with candidate `_revision.py`; its expected payload supplies the field-level contract used above. The oracle's historical statement that the old matrix did not test a raw tree is consistent with the new row.
- I compared the frozen snapshot and candidate `probe_tool()` / `object_selector_probes()` sections and the existing `measure()` path. The reviewed old selector cases and old measurement path are retained; the target-type path is separate (`target_type_measure()` and the `--object-target-types` dispatch at `:1391-1409`). The old object-selector matrix still covers annotated-tag-to-commit behavior. The new `annotated_tag_to_commit` acceptance case is continuity, not new coverage; the added raw-tree refusal is the relevant C2 increment here.
- The candidate reports matrix availability separately from target-type behavioral counts (`:739-780`); mode availability is an AST/option-presence check, not a 9-fold behavioral uplift. No runtime count is observed in this review.

## Residual risk and verification gaps

- To close the finding, the matrix would need to grade the relevant payload fields (at minimum the raw selector echo and finding site/detail, alongside the already-checked ID/count); a full unique-prefix tree case would be additional coverage beyond the present full-OID predicate.
- All conclusions are static source predictions. No test, selftest, candidate execution, mutation, build, or runtime observation was performed. The expected Git object-type behavior is inferred from the frozen source and the oracle, not independently executed.
- No `lsp` device was exposed in the mounted tool inventory, so no LSP status/references/definition/diagnostics result was available. I used direct `read` source locations and no grep; this is not semantic LSP proof. No tools were installed or updated; this lane's NO-EXEC restriction prohibited installs.
- Auxiliary frozen candidate dependencies read: `candidate/tools/_revision.py` SHA256 `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf`; `candidate/tools/check-revision-binding.py` SHA256 `0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6`; and `candidate-files.json` (revision and digest inventory). Auxiliary snapshot/oracle material read for comparison: `snapshot/tools/check-revision-binding.py`; `build/Oracle01Tree.md`; `build/Oracle01TagTree.md`; `build/ExecMatrix.md`. These are cited as historical/source-only context, not as candidate runtime observations.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: cd24d07ce71e3a3c5cff92802b69f3b2630aa5942a437ad00e53469387b05814
Predicate: check-locator-clarification.py-nonempty_tree-candidate-control
Scope: executed=none