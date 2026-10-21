# Fx05TagTree — attack: measure-update-recheck.py × tag_to_tree (candidate C2 control)

Reviewed-SHA256: 0275af5a8afd6de26086d6901bd9c62b53a3390ba92ca950cb0602996326ccb7
Predicate: measure-update-recheck.py-tag_to_tree-candidate-control
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.

Candidate revision: 0a14952b59d20179e1c813af58befaecd6992a17.

The primary receipt covers only the consumer `candidate/tools/measure-update-recheck.py`, whose SHA-256 0275af5a… was supplied by the assignment and matches `candidate-files.json:24-27`. Nothing was recomputed: this seat is NO-EXEC.

Auxiliary frozen dependencies, read but not covered by the primary receipt. Their digests come from `candidate-files.json`:

- `candidate/tools/_revision.py`, SHA-256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf (`:64-67`). This is the same digest that `preregister.json:50-52` records for the round-21 snapshot `_revision.py`. Per the inventory, the binder is therefore unchanged from the snapshot that build oracle Oracle05TagTree reviewed.
- `candidate/tools/check-revision-binding.py`, SHA-256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6 (`:39-42`).

Comparison inputs were `build/Oracle05TagTree.md` and `preregister.json` (C2). No moving draft or production file was used for any verdict.

## Verdict

**There is no defect within this predicate.**

- **Prediction for the real consumer.** From the frozen source, the real consumer refuses the tag_to_tree case. That holds for both the full tag OID and the unique prefix. Each run should end with exit 2 and exactly one finding, `E-REVISION-INVALID`.
- **Prediction for the judge.** The candidate judge's `target_type_probes` grades exactly that outcome, with an expected value that is hard-coded rather than computed by the binder.
- **The tree-peel mutant.** The realistic peel-weakening mutant would be killed by the new tag_to_tree cell, and it survives the old matrix.
- **One survivor outside the predicate.** A concrete mutant survives everywhere, but only in a field the predicate does not grade: the `revision` value in the refusal payload. It is recorded below as a gap in the predicate's boundary, not as a C2 false green.

## Axes

- **A. Consumer propagation:** bind, argv, error and output.
- **B. Expected outcome:** the per-selector result for this consumer.
- **C. Judge cell integrity:** fixture, selectors, sandbox, grading, host reads.
- **D. Mutants:** which ones the cell kills and which survive.
- **E. Continuity:** commit-tag rows and the old matrix.
- **F. Separating mode from behaviour** in C2.

## A. Consumer propagation (observed from source)

- **Import.** `measure-update-recheck.py:33-34` sets `sys.dont_write_bytecode = True` and then runs `import _revision`. The consumer has no local revision regex or binder copy; the only `{7,64}`-style text is in `_revision.py:41`. The judge materialises the consumer as `<sandbox>/tools/measure-update-recheck.py` (`check-revision-binding.py:259-273`). The sandbox worktree is checked out at the measured tip (`prepare`, `:233-242`), so `sys.path[0]` is `<sandbox>/tools` and the `_revision` that gets imported is the measured revision's copy. `ROOT = Path(__file__).resolve().parents[1]` (`:37`), so ROOT is the sandbox.
- **Argv.** The judge calls `run_tool` (`check-revision-binding.py:359-371`) as `python3 <tool> --revision <sel> --branch master`. `EXTRA["measure-update-recheck.py"]` is `()` (`:77`), and the environment is the judge's `clean_env()` (`:100-104`).
- **Parsing.** `main` (`measure-update-recheck.py:733-778`) defines `--revision` and `--branch` with default `master`, and does not use `--selftest`. The value goes to `load(args.revision, branch)` unchanged (`:758-760`).
- **Binding.** `load` (`:471-481`) skips the worktree branch because `rev` is not None, then calls `_revision.bind(ROOT, rev, branch)` (`:476`). There is no lowercasing, stripping or prefix expansion beforehand.
- **Error mapping.** `RevisionError` becomes `Cannot(exc.fid, exc.site, exc.detail, revision=rev, tip=_revision.branch_tip(ROOT, branch))` (`:477-479`). `branch_tip` never raises (`_revision.py:163-169`).
- **Output.**
  - `main` catches `Cannot` and calls `emit(exc.revision or revision, "CANNOT_EVALUATE", [Finding(exc.fid, exc.site, exc.detail)], digest=None, …)` (`:769-772`).
  - `emit` prints one sorted-key JSON line (`:433`) and returns `CANNOT` = 2, because the status is not COUNTED or ABSENT (`:434`).
  - There is a single `print`, no stderr traceback, and exactly one finding.
- **Data reads on this path.** `read_git` (`:449-456`) and `read_tree` (`:459-468`) are never reached on the refusal path. RECORD and SNAPSHOT are never read, and no host-state command runs: `pacman` and `stat` appear only as selftest strings (`:625-640`).

## B. Expected outcome for this consumer (source prediction, not observed)

The binder path in `_revision.py`:

1. `validate_branch("master")` passes (`:84-95`).
2. `REV` matches 7–64 hex (`:41`, `:175`).
3. `_object_commit` (`:112-146`):
   - `rev-parse --disambiguate=<sel.lower()>` returns exactly one object, the tag. The judge chose the prefix to be unique over the whole object inventory.
   - `cat-file -t` returns `tag`, so the code reaches the peel `rev-parse --verify --quiet --end-of-options <tag>^{commit}` (`:139-140`).
   - A tag whose target is a tree cannot peel to a commit, so the return code is non-zero. [INFERENCE: git prints an "expected commit type" error and `--verify --quiet` exits 1. Any non-zero value takes the same branch.]
   - `rev-parse --git-dir` succeeds, so the function returns `None` (`:143-145`).
4. `bind` raises `E-REVISION-INVALID` at site `revision` with detail `<sel> does not name one commit` (`:177-179`). This happens before any branch, ancestry or origin check (`:180-191`).

Predicted consumer result for both selectors (full tag OID and the shortest unique prefix of at least 7 characters):

- exit 2;
- `status` = `CANNOT_EVALUATE`;
- `findings` = `[{"id":"E-REVISION-INVALID","site":"revision","detail":"<sel> does not name one commit"}]`;
- `revision` = `<sel>`, echoed as given;
- `branch` = `master` and `branch_tip` = the sandbox tip;
- `record_count` 0 and `snapshot_sha256` null.

This matches Oracle05TagTree §B (`build/Oracle05TagTree.md:27-48`). Its line citations (476, 477–479, 758–760, 769–772, 434) resolve to the same statements in the frozen candidate consumer.

## C. Judge cell integrity (`candidate/tools/check-revision-binding.py`)

- **Real typed object, built independently.**
  - The tree is `rev-parse <tip>^{tree}`, the measured commit's real root tree. Non-emptiness is asserted with `ls-tree` (`:677-682`).
  - The tag is created with `git tag -a r21-target-measure-update-recheck-tree -m tree <tree>` (`:685-695`, `:701`). Its OID is read back with `rev-parse --verify <ref>^{tag}` (`:694`), which asserts that the object is a tag.
  - Limit: the judge never checks that the tag's target type is `tree` (for example with `cat-file -p` or `%(*objecttype)`). The type is guaranteed only by construction. If that construction were wrong, the cell could only go false-red, never false-green.
  - A pre-existing fixture tag is refused before creation (`:688-689`).
- **Exact refusal ID and count.**
  - `expected_commit is None` routes the cell to `refused(…, ID_INVALID, branch)` (`:721-725`).
  - A cell passes only if all of these hold: exit == 2, first finding == `E-REVISION-INVALID`, `binding_ids == ["E-REVISION-INVALID"]`, and `finding_count == 1` (`:383-393`, `:723-725`).
  - The expected value is the literal constant `ID_INVALID`. It is not derived from the judge's own `object_commit`/`bind` (`:139-208`) or from the binder under test, so the oracle is independent.
- **Unique prefix sanity.**
  - The object inventory is captured after all three fixture tags exist, because the `classes` dict is built eagerly at `:698-704` and the inventory is read at `:705-707`.
  - The chosen prefix is the shortest width from 7 up to len−1 that matches exactly one inventory object, with no `refs/heads/<p>` or `refs/tags/<p>` alias (`:711-716`). If none exists, the run raises `E-SANDBOX` (CANNOT, not green).
  - The consumer's `--disambiguate` searches the same object database: ROOT is the sandbox, and the run's cwd is the sandbox (`:362-366`).
- **Fresh sandbox.**
  - `target_type_measure` creates a `TemporaryDirectory`, clones the lane with `--no-tags`, then `prepare` detaches at the tip, drops the `origin` remote and recreates only the tracking ref (`:742-746`, `:233-242`).
  - The sandbox is shared by the nine consumer rows in sequence (`:763-766`). Fixture tag refs are deleted in `finally` (`:734-736`), but their tag objects stay. Each row re-reads the inventory, so leftover objects cannot break prefix uniqueness.
  - measure-update-recheck is the fifth row (`:61-67`). Earlier rows' leftovers do not affect it: the refusal stops at contract row 3, before any branch or origin state is consulted.
- **No host read on this path.**
  - The judge's subprocess environment and `_revision.clean_env` (`_revision.py:62-66`) set `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, so neither the global nor the XDG git config is read on the refusal path.
  - The consumer never opens RECORD or SNAPSHOT here and runs no `pacman`/`stat`. Its git calls are `check-ref-format`, `rev-parse`, `cat-file` and `merge-base`, all through `_revision._git` against the sandbox.
- **Build oracle comparison.** Oracle05TagTree predicted the same refusal, judged that the round-20 matrix lacks this case (§C), and proposed the `^{}` peel mutant (§D). The candidate cell supplies exactly the missing tag-to-tree probe, with a hard-coded expectation as §E recommended. Oracle05TagTree §C also flagged that `json_revision` on refusals is not graded; that gap is still present (see D3).

## D. Mutants (proposed, NOT executed)

- **D1. Killed: real-consumer peel weakening.**
  - Mutation: in `_revision.py:140`, change `f"{oid}^{{commit}}"` to `f"{oid}^{{}}"`.
  - Predicted effect for tag_to_tree: the peel succeeds and yields the tree OID. Then `_ancestor(tree, "refs/heads/master")` runs `merge-base --is-ancestor <tree> …`. [INFERENCE] git exits ≥ 2 on a non-commit operand, so `_revision.py:156-160` raises `E-GIT-FAILED`.
  - Result: exit 2, but `finding = E-GIT-FAILED` ≠ `E-REVISION-INVALID`, so `refused().ok` is False for both selectors, `behavior_ok` is False (`:765`), and `target_type_tools` is below 9.
  - The old matrix stays green: tag→commit still peels to the commit, and `noncommit_blob` is not a tag. The judge's selftest witness encodes the same class with stub mode `target-generic-peel` (`:981-989`, `:1239-1259`), but only on `TOOLS[0]` (check-locator-clarification) and only as authored fixture code. For this consumer the kill is a source prediction, not an observation.
- **D2. Killed: peel failure misclassified as a git failure.** Mutation: replace `_revision.py:143-145` with an unconditional `raise RevisionError(E_GIT, …)`. Predicted result: `E-GIT-FAILED`, so the cell fails. tag_to_blob kills it as well.
- **D3. Survives everywhere, but outside the predicate.**
  - Mutation: in `measure-update-recheck.py:478`, change `revision=rev` to `revision=_revision.branch_tip(ROOT, branch)`.
  - Predicted effect for tag_to_tree: exit 2, one `E-REVISION-INVALID`, and `"revision": "<sandbox master tip, full 40-hex commit>"` under `CANNOT_EVALUATE`. The refusal payload then names a full commit SHA that was never bound.
  - Why it survives: `refused()` records `json_revision` (`:388-392`) but never includes it in `ok`, and `target_type_probes` adds only the ID and count checks (`:723-725`). The old matrix's `exact_refusal` likewise ignores it by design (`:480-486`).
  - Accept cases go through `binding.sha` (`:480`), so this mutant does not touch them, and it survives C2 and the old matrix together.
  - Classification: the C2 predicate requires only the exact refusal ID and count, plus the full SHA on acceptance. D3 is therefore a predicate-boundary gap with low severity (`status` still says `CANNOT_EVALUATE`), not a false green under the preregistered predicate.
- **D4. Uncovered sub-class, not a current defect.**
  - Mutation: a binder that reads the tag's direct `type` header, refuses `tree`/`blob`, and peels `tag`-typed targets with `^{}`. It passes tag_to_tree, tag_to_blob and nested_tag_to_commit, but it would return the tree OID for tag→tag→tree and then fail with `E-GIT-FAILED`.
  - No preregistered case builds nested_tag_to_tree. The current `^{commit}` peel walks the whole chain, so the frozen binder is not affected (Oracle05TagTree §B, last bullet).

## E. Continuity (not new coverage)

- **annotated_tag_to_commit.** This cell (`:703`) overlaps the old `annotated_tag_object`/`annotated_tag_prefix` (`:631-632`). It is continuity and must not be counted as new coverage; `build/ConnPlanner.md:29` and `build/CritBaseline.md:39` say the same. The same applies to the nested_tag_to_commit cell, which is a different object class with the same accept semantics.
- **Accept-path observations for this consumer** (outside tag_to_tree):
  - `accepted()` needs `exit != 2` (`:395-404`). An `E-C2-*`/`E-SNAPSHOT-*` record finding at the measured revision would make the commit-tag cells false-red, never false-green.
  - On that path `read_git` uses the consumer's own `git()` (`measure-update-recheck.py:437-446`). That function strips every `GIT_*` variable, including the judge's `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_NOSYSTEM`, without restoring them, so `git show` would read the host's global and system git config. This is a host config read, not a host-state read, and it is not on the tag_to_tree path.
- **Old matrix unchanged** [observation by line parity only, not a byte diff]: `object_selector_probes` and `probe_tool` have the same case keys at the same line numbers in the snapshot and the candidate (`:426-462`, `:475-672`). `--object-target-types` is a separate opt-in flag (`:924-925`, `:1391-1409`); in the candidate `main`, combining it with `--object-selectors` is refused with E-CLI (`:1392-1395`).

## F. Mode versus behaviour

- **What the mode measures.** `target_type_mode` (`:757-759`, `:773`) is a finite AST census of whether the judge at the measured revision defines `target_type_measure`, `target_type_probes` and `--object-target-types`. It is counted once.
- **What the behaviour count measures.** `target_type_tools` is the number of consumer rows whose five cells are all ok (`:763-767`).
- **They are already separated.** The selftest `target-type-missing-mode-is-not-behavior-failure` (`:1251-1254`) encodes mode 0 alongside behaviour 9 as distinct values.
- **Consequence.** The mode flip from 0 to 1 is availability, not a nine-fold behavioural uplift. This seat supports only the per-cell prediction for measure-update-recheck × tag_to_tree.

## Observations, inferences and limits

- **Observed (source reads):** every line citation above, the inventory digests, and the line parity between the candidate and snapshot matrices.
- **Inferred:** git exit statuses for `<tag-to-tree>^{commit}` and for `merge-base --is-ancestor <tree>`. The consumer's verdict does not depend on the exact non-zero value in the first case. D1's kill depends only on the second being non-zero and not 1, which git's commit-lookup fatal path satisfies [INFERENCE].
- **Not done:** no consumer, judge, selftest or mutant was executed. No digest was recomputed. `lsp` was not used, so call sites were confirmed by direct reads. No tool was installed, and none was needed.
- **No closure claim:** this report claims no closure by anyone other than its author and no promotion outside this wave.

Scope: executed=none
