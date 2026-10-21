# Fx06CommitTag — check-boot-chain.py × annotated_tag_to_commit (falsify, source-only)

Reviewed-SHA256: 91312f103e694daafc95006fc0c083f6bfbe3abad03a2abed370f50e7ff22982
Predicate: check-boot-chain.py-annotated_tag_to_commit-candidate-control

Candidate revision 0a14952b59d20179e1c813af58befaecd6992a17. The primary receipt binds only `candidate/tools/check-boot-chain.py` (the SHA above, matching `candidate-files.json`). Auxiliary frozen snapshot dependencies were read but are not bound by this receipt:
- `candidate/tools/_revision.py` sha256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf. This is the same digest as the preregistered baseline snapshot in `preregister.json:50-52`.
- `candidate/tools/check-revision-binding.py` sha256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6.
- `snapshot/tools/check-revision-binding.py` (preregistered da000de4…), used only for the old-matrix positional comparison.
- `build/Oracle06NestedTag.md`, the build oracle for this consumer. No Oracle06CommitTag exists.

## Verdict
**This predicate has a defect: the row can pass a wrong consumer (false green).** The `annotated_tag_to_commit` row accepts any consumer that emits the sandbox branch tip, whether or not it peeled the tag. The reason is that the row's expected commit is the measured `tip`. In the `--object-target-types` sandbox, `tip` is also `refs/heads/<branch>`, `refs/remotes/origin/<branch>` and `HEAD`. A consumer that reports any of those instead of the peeled tag target gets `ok=True`. The CLI makes `--object-target-types` mutually exclusive with `--object-selectors` and runs it without `probe_tool`. So the C2 metric `target_type_tools` never runs the old `landed-parent` row, which is the only discriminator. The correct consumer also passes the row (no false red is predicted). The commit-tag row is continuity, not new coverage.

## Axes
1. Selector form: the full tag object ID, or a unique 7–39-hex prefix.
2. Object type and peel: an annotated tag whose recursive `^{commit}` peel reaches commit C.
3. Landed/pushed status of C relative to `refs/heads/master` and `refs/remotes/origin/master`.
4. Consumer propagation: the selector passes through `bind`, `binding.sha` flows to `read_git` and to the payload `revision`, and the process exits with a code.
5. Discriminating power of the judge row: is `expected_commit` distinguishable from every other commit a wrong consumer could report?
6. Sandbox hygiene: fresh clone, unique prefix, no host read.

## Observations (from frozen source, read-only)

### Consumer propagation (check-boot-chain.py)
- `build_parser` (`check-boot-chain.py:828-847`) takes `--revision` verbatim. `--branch` defaults to `master`, and the judge passes `--branch master` (`check-revision-binding.py:360`).
- `main` (`:1570-1575`) calls `binding = _revision.bind(ROOT, args.revision, branch)`, then sets `revision = binding.sha` and `branch_tip = binding.branch_tip`. `ROOT = Path(__file__).resolve().parents[1]` (`:57`) points at the sandbox, because the judge materializes the tool at `sandbox/tools/` (`check-revision-binding.py:259-274`). `import _revision` (`:54`) resolves to `sandbox/tools/_revision.py` from the `checkout --detach tip` (`check-revision-binding.py:234`).
- Any `RevisionError` produces exactly one finding, `Result(CANNOT, [finding])`, with `revision="unbound"` (`:1578-1584`).
- On success, `read_git(revision, …)` (`:1622-1624`), then `evaluate`, then `emit(result, revision, …)` (`:1636`). `emit` prints one JSON line containing `revision` and `branch_tip` (`:785-798`). The exit code is 0 or 1 from corpus conformance. The other CANNOT paths are `Cannot` from `read_git`, `E-JSON-PARSE` and `E-INTERNAL` (`:1625-1635`, `:570`). Each one only turns an accept into a red, never a green.

### Binder path for an annotated tag to a commit (_revision.py)
`REV` (`:41`, `:175`), then `_object_commit` (`:112-146`):
1. `rev-parse --disambiguate=<lower>` returns exactly one object (`:119-124`).
2. `cat-file -t` reports `tag` (`:127-137`).
3. `rev-parse --verify --quiet --end-of-options <oid>^{commit}` gives C (`:139-142`).
4. `_commit(refs/heads/master)` and `_ancestor` checks (`:180-185`), then the origin check when the ref exists (`:187-191`).
5. The function returns `Binding(C, branch, tip, origin)`.

All of these git calls use `clean_env()` with `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` (`:62-66`).

### Judge row (check-revision-binding.py `target_type_probes`, `:676-736`)
- **Independent typed object:** `commit_tag = tag("commit", tip)` (`:697`). This creates a new annotated tag `r21-target-check-boot-chain-commit` with message `commit` and gpg signing off, and resolves it with `rev-parse --verify <ref>^{tag}` (`:685-695`). It is a different object from the old matrix's `r20-object-selector-…` tag (`:498-509`) because the name and message differ.
- **Expected commit:** `"annotated_tag_to_commit": (commit_tag, tip)` (`:703`), so the expected commit is `tip`.
- **Selectors:** the full tag OID, plus a prefix found by `range(7, len(object_id))`. The prefix must be unique in a `cat-file --batch-all-objects` inventory taken after all four r21 tags exist (`:705-718`), with no `refs/heads/<p>` or `refs/tags/<p>` collision. The prefix check holds: the binder is object-only for hex selectors, so ref collisions are irrelevant to it anyway, and the 39-hex upper bound is harmless.
- **Grading:** `accepted()` (`:396-404`) sets `ok = exit != 2 and JSON revision == expected_commit` (case-insensitive). The row ok is the AND over both selectors (`:730-732`). It does not check `branch_tip`, `status`, or the absence of binding finding IDs. For this consumer, exit ≠ 2 already implies `bind` succeeded, so binding IDs cannot appear on an exit 0/1 output (`:1578-1584`).
- **Fresh sandbox:** `target_type_measure` (`:739-746`) does `bind(lane, tools_rev)`, a new tempdir clone with `--no-tags --no-hardlinks` (`:218-230`), `prepare` and `materialize`. Fixture tags are removed in `finally` (`:734-736`). Tag objects stay loose in the shared per-run sandbox, but each tool's inventory is re-read, so uniqueness still holds.
- **Not run in this sandbox:** `probe_commit` and parent probing. `measure` does both (`:799-802`). `target_type_measure` does neither.

## Defect: false green on the commit-tag row (predicted from source, not executed)

**Degenerate expected commit.** `prepare` sets three things to `tip`:
- `refs/heads/<branch>` (`:235`)
- `refs/remotes/origin/<branch>` (`:240`)
- detached `HEAD` (`:234`)

`target_type_measure` creates no further commits. The row expects `tip` (`:703`), and the tag also points at `tip` (`:697`). So within this row, "C, the peeled tag target" and "the branch tip" (also "HEAD" and "the origin tip") are the same commit.

**Mutant M-TIP, in the primary file (proposed, not executed).** In `check-boot-chain.py:1574`, change

```python
revision = binding.sha
```

to

```python
revision = binding.branch_tip
```

Predicted trace for selector = `commit_tag` OID or its unique prefix:
1. `bind` succeeds unchanged.
2. `binding.branch_tip` comes from `_commit(refs/heads/master)`, which equals `tip` (`_revision.py:181`).
3. `read_git(tip, …)` reads the same bytes as for C, because C = tip.
4. Exit is identical to the correct tool.
5. JSON `revision` = tip = `expected_commit`, so `accepted.ok` is True.

The `annotated_tag_to_commit` row reports ok for a consumer that never reports the commit the tag names.

M-TIP also passes the other four classes in the same mode:
- `nested_tag_to_commit` expects `tip` too (`:702`).
- `nonempty_tree`, `tag_to_blob` and `tag_to_tree` refuse inside `bind`, before `branch_tip` is ever used.

So `behavior_ok` is True (`:765`) and the C2 `target_type_tools` count is unaffected.

**What kills M-TIP, and why C2 does not.** Only `probe_tool`'s `landed-parent` row kills it: `accepted(parent, parent)` at `:427`, where the mutant would emit `tip ≠ parent`. That row runs in `measure` (default mode and `--object-selectors` mode). It does not run under `--object-target-types`: `main` rejects combining the two modes (`:1391-1395`) and calls only `target_type_measure` (`:1397`). Every `object_selector_probes` accept also expects `tip` (`:608-632`), so it cannot kill M-TIP either.

**Equivalent variants with the same outcome:**
- Report `git rev-parse HEAD`. The sandbox HEAD is the detached `tip` and is never moved in this mode.
- Report `binding.origin_tip`.
- An auxiliary `_revision.bind` that returns `Binding(tip, …)`. This one lives outside the primary file.

**Fix direction (not applied):** point the commit-tag fixture at a landed non-tip commit and expect that commit:

```python
tag("commit", parent)  # expected_commit = parent
```

`parent` is `tip^1`, which is already required elsewhere. Alternatively, run `probe_commit` and assert that `expected_commit` differs from the branch tip and HEAD. Either way, the row would then distinguish "peeled target" from "branch tip, HEAD or origin".

## Build-oracle comparison
`Oracle06NestedTag.md` is the closest oracle for this consumer. It shares the same `commit_tag` object and the same `tip` expectation (`:702-703`). It expects:
- exit ≠ 2
- zero binding findings
- payload `revision` = the peeled commit's full SHA, "never the tag object id, never the selector text"
- `branch_tip` = the branch tip

The candidate row enforces exit ≠ 2 and `revision == tip`. It does not enforce `branch_tip`. Because the oracle's "peeled commit" and "branch tip" are the same commit in the candidate's fixture, the row cannot separate the oracle's two fields. That is the M-TIP gap.

The oracle's single-level-peel mutant is killed by `nested_tag_to_commit`, not by this row. The tag-object-ID or selector-echo mutant (`revision = args.revision`) is killed by this row: the tag OID and the prefix both differ from `tip`. The old `annotated_tag_object` and `annotated_tag_prefix` rows (`:631-632`) and `short-tip` already kill it.

## Continuity, not new coverage
- **Same class as the old matrix.** `annotated_tag_to_commit` is the same depth-1 annotated-tag-to-`tip` class as the old `annotated_tag_object` and `annotated_tag_prefix` rows. In the preregistered snapshot those rows are at the same lines, 631-632. `probe_tool` is at 416/427 and `object_selector_probes` at 475 in both the snapshot and the candidate. This positional match is consistent with the old matrix being unchanged; no byte diff was performed.
- **No consumer behavior change.** The `_revision.py` digest is identical to the baseline snapshot. The Oracle06 consumer line citations (`main` 1554–1636, `emit` 785–798, `binding_cases` 1324–1393) match the candidate's line numbers. [INFERENCE] The consumer's behavior on this class is unchanged from baseline.
- **C2 is a measurement change only.** Mode 0→1 for commit-tag is availability of the new measurement, not a behavioral uplift for nine tools.

## Host-read observation (outside the predicate's accept/refuse outcome)
`check-boot-chain.py:801-803` (`git()`, used by `read_git`) copies the environment minus every `GIT_*` key. That drops the judge's `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` (`check-revision-binding.py:100-104`), and `HOME` is kept. [INFERENCE] The accept path's `git show <C>:<path>` therefore loads the host's system and global git config. The judge's docstring (`:49-53`) says only GIT_* environment/config inheritance is suppressed; this consumer undoes that for corpus reads. The bind path stays isolated through `_revision.clean_env`. Effect on this row: the payload `revision` comes from `binding.sha`, not from `read_git` content, and any config-induced `git show` failure becomes `Cannot`, then exit 2, then a false red. So this can produce a false red but not a false green. It is still a host config read the row does not detect.

## Adjacent limit (outside this predicate)
Neither matrix has an annotated tag pointing at an unlanded or unpushed commit. The old `unlanded_*` and `unpushed_*` rows use commit selectors only (`:633-669`), and `_revision.py`'s selftest covers tags only toward `tip` (`:353-365`). A consumer that skips the landed/pushed checks only for tag selectors would survive every row. This predicate only asserts acceptance, so this is recorded as a gap, not as this row's false green.

## Inferences and limits
- Every behavior above is a source prediction from frozen bytes plus documented Git semantics (`--disambiguate`, recursive `^{commit}`, `merge-base --is-ancestor`). Nothing was executed: no test, mutant, judge, git, import or compile.
- The predicted pass of the correct consumer assumes the corpus JSON at the measured revision parses. If it does not, the result is `E-JSON-PARSE` with exit 2: a false red that equally affects every accept row.
- No tool installs were needed or performed (NO-EXEC seat).
- This is a source-only author-independent attack seat. It claims no non-author closure and no outside promotion.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none
