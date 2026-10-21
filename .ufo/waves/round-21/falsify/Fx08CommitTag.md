# Fx08CommitTag — falsify `check-recheck-commands.py` × `annotated_tag_to_commit`

Candidate revision 0a14952b59d20179e1c813af58befaecd6992a17. Primary file:
`.ufo/waves/round-21/candidate/tools/check-recheck-commands.py`
(SHA256 9dc46f46…e7e9, per `candidate-files.json:44-47`).

Auxiliary snapshot dependencies (read only, cited by their predispatch digest in `candidate-files.json`):
- `candidate/tools/_revision.py` — 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
- `candidate/tools/check-revision-binding.py` — 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6
- `candidate/corpus/knowledge/selector-contract-r21.md` — b4966a9bcf4ac124a964718b0ed76104e2f07c41b63050dc8bda618ea5136353
- Pinned round-20 judge `snapshot/tools/check-revision-binding.py`, used only to compare line anchors of the old matrix. Its digest is not in `candidate-files.json`.
- Build reports `build/Oracle08NestedTag.md`, `build/ConnPlanner.md` and `build/CritBaseline.md`, used as prose context only. They are not a verdict source.

## Axes

- **A1 Consumer propagation**: how the consumer binds the revision, builds argv, propagates errors and writes output for an annotated tag that points at a commit.
- **A2 Row construction**: whether the probe uses an independently created typed object, a fresh sandbox, a sane unique prefix, and no host read.
- **A3 Oracle discrimination**: whether the row's accept test can tell a correct consumer from a realistic wrong one.
- **A4 Continuity versus new coverage**: whether the old matrix is unchanged, and why this class does not count as uplift.

## A1 — Consumer trace (observed in source)

- **Import.** `:54-55` sets `sys.dont_write_bytecode = True` and runs `import _revision`. There is no local binder copy. The judge launches the tool as `sandbox/tools/check-recheck-commands.py` (`check-revision-binding.py:362`), so `_revision` resolves to the sandbox checkout at the measured tip.
- **Arguments.** The judge's argv is `--revision <sel> --branch master` with no extra arguments, because `R17_GATES["check-recheck-commands.py"] = ()` (`judge:74, :360-363`). The consumer parser (`:877-897`) therefore keeps `--paths` at its default `corpus/knowledge` and `--forbid` at its default list.
- **Bind.** `:916` calls `forbid_list` first, then `:918` calls `_revision.bind(repo, args.revision, branch)`, where `repo = ROOT = sandbox` (`:58`, `:900`).
  - The `_revision.bind` order is: `validate_branch`, then the 7–64 hex check, then `_object_commit`, then the branch ref check, then the landed check, then the pushed check (`_revision.py:172-192`).
  - `_object_commit` (`_revision.py:112-146`) lists objects with `rev-parse --disambiguate=<sel.lower()>` and requires exactly one. It types the object with `cat-file -t`, which returns `tag` here. It then runs `rev-parse --verify --quiet --end-of-options <oid>^{commit}` and returns the peeled commit SHA, which is the tip.
  - The landed and pushed checks then run against that commit. `prepare` sets both `refs/heads/master` and `refs/remotes/origin/master` to the tip (`judge:233-242`), so both pass.
  - All of these git calls use the hermetic environment `_revision.clean_env` (`:62-66`), which sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`.
- **Errors.** A `RevisionError` becomes a `Cannot` carrying the same `fid`, `site` and `detail` (`:919-921`). The output is `CANNOT_EVALUATE`, exit 2, with exactly one finding. Because `sha` is still `None` at that point, the `revision` field echoes the selector (`:930-934`).
- **Success.** `:922` takes `sha = binding.sha`, which is the peeled commit. The file reads use that SHA: `expand_paths(repo, sha, …)` at `:923` and `read_git(repo, sha, path)` at `:926`. The final call `emit(status, sha, branch, tip, …)` (`:965`) writes the JSON field `"revision": sha` (`:775`). Exit is 0 for PASS and 1 for FAIL (`:795`).
- **Default paths.** `corpus/knowledge` is expanded at the bound commit. The candidate's new entry `selector-contract-r21.md:3` reads `recheck: on-release`, which is non-empty, so `assess_file` raises neither `E-RECHECK-MISSING` nor `E-RECHECK-EMPTY` for it (`:658-663`). [INFERENCE] The other knowledge files at 0a14952 are not in the frozen set. They are the same inputs that the old matrix's accepted rows (`tip`, `short-tip`, `annotated_tag_object`) already depend on.

**Source prediction** for both selectors (the full tag object ID and its unique prefix): exit 0 or 1, never 2. The JSON `revision` is the tip's full 40-hex SHA. It is never the tag object ID and never the prefix. So `accepted()` is `ok` and the case is `ok`.

## A2 — Row construction (`check-revision-binding.py:676-736`, observed in source)

- **Independently created typed object.** `tag("commit", tip)` runs `git tag -a r21-target-check-recheck-commands-commit -m commit <tip>` (`:685-695`). It then reads the object ID with `rev-parse --verify refs/tags/<name>^{tag}`. The `^{tag}` suffix fails on anything that is not a tag object, and `must` turns that failure into `E-SANDBOX`. The object is therefore a real annotated tag. Its target is fixed by the creation argv. The expected commit is the judge's own `bind(lane, tools_rev)` result (`:742`), and no consumer code is imported.
- **Expected result.** This class is accepted, not refused: `"annotated_tag_to_commit": (commit_tag, tip)` (`:703`), graded by `accepted()` (`:726`). `accepted()` requires `code != CANNOT` and a JSON `revision` that equals the tip, compared case-insensitively (`:396-404`). No refusal ID or count applies to this class.
- **Unique prefix.** The prefix is the shortest one from 7 to 39 hex characters (`:712-715`). It must match exactly one object in a `cat-file --batch-all-objects` inventory, and neither `refs/heads/<p>` nor `refs/tags/<p>` may exist.
  - The inventory is taken after all four fixture tags exist (`:705-707`), and the consumer creates no objects, so the inventory stays valid while the row runs.
  - The full object ID is always the first selector (`:710`).
- **Fresh sandbox.**
  - `target_type_measure` creates one `TemporaryDirectory` clone made with `--no-tags`. `prepare` detaches at the tip and removes the remote (`:743-746`, `:218-242`).
  - Per-tool tag refs are deleted in `finally` (`:734-736`). The unreferenced tag objects stay in the object database.
  - The clone is fresh per measurement, not per tool. This consumer is the 8th entry in `TOOLS` (`:61-79`), so seven earlier consumers run in the same clone first. [INFERENCE] That has no effect here: leftover objects only make the prefix-uniqueness check stricter, and this consumer's run path only reads (`cat-file`, `show`, `ls-tree`, `rev-parse`, `merge-base`).
- **Host reads.**
  - The judge's git calls (`:100-117`) and the consumer's binder calls (`_revision.py:62-77`) suppress host git configuration.
  - The consumer's own `git()` (`:798-809`) removes every `GIT_*` variable, including the `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1` that the judge passed in, and does not set them again. So the path reads at `:851,:860,:814,:819` read the host's `~/.gitconfig`, the XDG git config and `/etc/gitconfig`.
  - Effect on this row: the `revision` value the oracle compares comes only from the hermetic `binding.sha`. Host configuration can therefore only make a path read fail, which gives `E-PATH-MISSING` or `E-GIT-FAILED` and exit 2, a false red. It cannot produce a false green.
  - This is a limit on the row's no-host-read claim, not a false-green defect. The judge's own trust boundary already says that tool subprocesses keep the caller's user-level authority (`judge:49-53`).
- **Selftest witness.** `target-types-five-fixed-classes` (`:1234-1238`) runs the row against stub tools in `object-selector` mode, not against the real consumer. The real consumer's verdict exists only from an actual `--object-target-types` run, and none was executed or observed here.

## A3 — Concrete mutant: emit the branch tip as `revision` (proposed, NOT executed)

**Mutant M1.** Swap the two positional arguments at consumer `:965`:

```python
    return emit(status, tip, branch, sha, result.findings + exec_findings, result.counts,
                out, origin_tip=origin_tip, extra=extra)
```

Any other path that writes `binding.branch_tip` into `revision` behaves the same way.

**Prediction against this row.**
- In the sandbox, `refs/heads/master = refs/remotes/origin/master = tip`, which is also `expected_commit` (`judge:234,:240,:703`).
- For both selectors, M1 exits 0 or 1 and reports `revision == tip`, so `accepted()` returns `ok` and `annotated_tag_to_commit` stays green.
- `nested_tag_to_commit` (`:702`) has the same expected value, tip, so it is also green.
- The three refusal classes never reach `:965`, so they are unchanged.
- The predicted result is `behavior_ok = True` for this consumer, so M1 survives the whole target-type matrix (`:764-766`). That is a row-local false green: the commit-tag row's accepted SHA is aliased to the branch tip, so it cannot tell "peeled to the tag's target" apart from "reported the branch tip".

**Where it is killed.**
- The old BOUND matrix's `landed-parent` row, `accepted(sandbox, name, parent, parent, branch)` (`judge:427`), expects the parent and gets the tip, so it fails.
- `target_type_measure` (`:739-780`) does not run `probe_tool`. So M1 is killed only when the existing `measure` lane is also run, not by this row.
- **Severity: Low.** The same aliasing already exists in the round-20 continuity row `annotated_tag_object = exact_accept(tag_object, tip)` (`:631`), so this is inherited, not introduced. It does not affect the candidate's binding correctness.
- **Minimal fix** (proposal only, nothing was edited): point the commit tag at a landed non-tip commit. For example, call `tag("commit", parent)` with `expected_commit = parent`, so the expected commit differs from `branch_tip`.

**Mutants checked and killed by this row** (source predictions):
- **M2, no peel.** The binder returns the tag object ID. `merge-base --is-ancestor` peels tags, so the landed and pushed gates pass, but `revision` is the tag object ID, not the tip, so the row fails.
- **M3, tags refused.** The binder only accepts the `commit` type. This gives `E-REVISION-INVALID` and exit 2, so the row fails.
- **M4, selector echo on success.** `revision` would be the selector, not the tip. That fails for both the full object ID and the prefix.

**Equivalent for this class, so not defects:**
- **M5, generic peel.** Using `^{}` instead of `^{commit}` gives the same result for a tag that points at a commit. That mutant is killed by `tag_to_tree`, per the `TARGET_TYPE_WITNESS` at `:1255-1259`.
- **M6, reads at the selector.** Calling `expand_paths` and `read_git` with `args.revision` instead of `sha` still works, because git peels `<tag>:<path>` to the same tree. No ref with the prefix's name exists (`:714-715`), so the content read is identical.

## A4 — Continuity and the old matrix

- The old-matrix line anchors are identical in the snapshot and the candidate:
  - `object_selector_probes` at `:475`
  - `r20-object-selector-` at `:498`
  - `full_{label}_object_id_ref_shadow` at `:622`
  - `annotated_tag_object` at `:631`
  - `annotated_tag_prefix` at `:632`
  - `accepted`, `refused` and `run_tool` at `:396`, `:383` and `:359`
- `target_type_probes` and `target_type_measure` are additive, at `:676` and `:739`. This is an anchor comparison, not a byte diff. [INFERENCE] The old matrix is unchanged.
- `annotated_tag_to_commit` repeats `annotated_tag_object` and `annotated_tag_prefix` (`:631-632`) with a freshly named tag. It is continuity, not new coverage. The build docs agree: `build/ConnPlanner.md:29,71` and `build/CritBaseline.md:36-39` count only four new classes, 4 × 9 = 36 cells, and no AnnotatedTag oracle was dispatched.
- **Build oracle comparison.** There is no `Oracle08CommitTag`. `build/Oracle08NestedTag.md` (consumer-wiring section, lines 18-32) gives the same consumer trace as A1: `:918` bind, `:919-921` error propagation, `:922-926` reads at `sha`, `:965` emit. Its expectation for case 1, accept with the full commit SHA and never the tag object ID, matches the prediction here for depth 1. There is no disagreement.
- **C2 mode.** `target_type_mode` changes from 0 to 1 only because the AST census finds the `--object-target-types` option and the two functions (`:750-759`). The selftest `target-type-missing-mode-is-not-behavior-failure` (`:1251-1254`) checks for the pair (0, TOTAL). That mode change is availability, not a nine-fold behavioral uplift.

## Verdict

- No binding defect in `check-recheck-commands.py` for annotated tag → commit. The consumer reports the peeled full commit SHA and never echoes the tag. Errors propagate as exactly one typed finding with exit 2.
- The row is well built: a real tag object, a judge-side expected commit, a sane unique prefix, and a clone-confined repository.
- Residual row-local false green: M1, emitting `branch_tip` as `revision`, survives `annotated_tag_to_commit` and the whole target-type matrix, because expected commit = branch tip = origin tip. Only the old BOUND `landed-parent` row kills it. Severity Low, inherited from round-20 `:631`.
- Hermeticity limit: the consumer's path-read `git()` re-enables host git configuration (`:798-801`). That can cause a false red, never a false green.

## Limits

- NO-EXEC: no git, Python, test or mutant was run. Every outcome above is a source prediction. That `^{commit}` and `merge-base` peel tag objects comes from Git's revision-syntax contract and the binder selftest (`_revision.py:353-361`); it was not re-observed here. [INFERENCE]
- Knowledge files at 0a14952 other than `selector-contract-r21.md` are not in the frozen set, so whether the default-path evaluation exits 0 or 1 is not established. Neither exit affects acceptance.
- The old-matrix comparison was by line anchors only.
- No tool was installed or upgraded.
- This is author-side falsify review. It is not non-author closure or outside promotion.

Reviewed-SHA256: 9dc46f46d322f92578b60027da3d7ea8138d90ef44eeae152531388e6c27e7e9
Predicate: check-recheck-commands.py-annotated_tag_to_commit-candidate-control
Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
