# Fx06TagTree — falsify check-boot-chain.py × tag_to_tree (candidate 0a14952)

Reviewed-SHA256: 91312f103e694daafc95006fc0c083f6bfbe3abad03a2abed370f50e7ff22982
Predicate: check-boot-chain.py-tag_to_tree-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Primary file: `.ufo/waves/round-21/candidate/tools/check-boot-chain.py` (revision 0a14952b59d20179e1c813af58befaecd6992a17). The SHA256 above is the one supplied by the item and listed in `candidate-files.json`. I did not hash the file myself, because hashing would have meant executing something.

Auxiliary snapshot dependencies (read only, digests taken from `candidate-files.json`, not bound by this receipt):
- `candidate/tools/_revision.py`, sha256 `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf`. This equals the baseline binder digest quoted in `build/dispatch.json`.
- `candidate/tools/check-revision-binding.py`, sha256 `0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6`.

Comparison oracle: `build/Oracle06TagTree.md`.

## Verdict
**No defect within this predicate.**
- The `tag_to_tree` row grades the real consumer against an actual annotated tag object that points at a non-empty tree. It requires all of the following, for both the full object ID and the shortest unique prefix of 7 to 39 hex characters:
  - exit code 2;
  - a first finding of `E-REVISION-INVALID`;
  - binding IDs equal to exactly `[E-REVISION-INVALID]`;
  - exactly one finding.
- Every single-point weakening of the binder or consumer I could construct is predicted to fail this row, the old matrix, or a sibling target-type row.
- One residual is real but sits outside the predicate: the row does not grade the `revision` field on a refusal. In that respect it is weaker than the build oracle (see R1).

## Axes
- A1: how the consumer propagates argv, bind, errors and output (frozen consumer plus frozen `_revision.py`).
- A2: the judge's `tag_to_tree` row: fixture construction, the exactness of the refusal check, sandbox freshness, prefix uniqueness, and host reads.
- A3: comparison with the build oracle.
- A4: the mutant search for a false green.
- A5: continuity and accounting (commit-tag continuity, an unchanged old matrix, mode 0→1).

## A1 — Consumer propagation (observed, frozen source)
- **Judge argv.** `run_tool` (judge 359-371) runs `[sys.executable, <sandbox>/tools/check-boot-chain.py, --revision, S, --branch, master]`.
  - `EXTRA["check-boot-chain.py"]` is `()` (judge 72, 77-78).
  - The working directory is the sandbox, and the environment is `clean_env()` (judge 100-104: GIT_* removed, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`).
  - The executed file is materialized from `<tip>:tools/check-boot-chain.py` (judge 259-274). `_revision.py` comes from the `prepare` checkout at the tip (judge 233-234).
- **Import.** `sys.dont_write_bytecode = True` is set before `import _revision` (consumer 53-54), so no `__pycache__` is written into the sandbox. `ROOT` is the sandbox root (consumer 57).
- **Bind call.** `main` (consumer 1570-1573) sets `revision, branch_tip = "unbound", None` and then calls `_revision.bind(ROOT, args.revision, branch)` with argv passed through unmodified.
- **Predicted binder path for a tag-to-tree selector S:**
  1. `validate_branch("master")` passes (`_revision` 84-95).
  2. `REV` matches (176).
  3. `_object_commit` runs `rev-parse --disambiguate=<s.lower()>`, which yields exactly one object (119-124).
  4. `cat-file -t` reports `tag` (127-137).
  5. The peel `rev-parse --verify --quiet --end-of-options <oid>^{commit}` fails, `rev-parse --git-dir` succeeds, and the function returns `None` (139-146).
  6. `bind` then raises `RevisionError(E-REVISION-INVALID, "revision", "<S> does not name one commit")` (177-179).
  - Steps 4-6 of the contract (landed, pushed, origin) are never reached.
- **Error propagation.** The consumer catches `RevisionError` and builds exactly one `Finding` (consumer 1578-1580). It then calls `emit(Result(CANNOT,[finding],0,0), "unbound", "master", None)` (1584).
  - `emit` prints one sorted JSON line with `status: CANNOT_EVALUATE` and returns 2 (785-798, 56). That return value is the process exit code (1640).
- **Host reads on this path (predicted).** Only `_revision._git` and `validate_branch` run, and both use `_revision.clean_env()` (62-66, 88-91). No `read_git` call happens: the consumer's own `git()` (801-811) is first reachable at 1588 or 1622, which is after a successful bind. So the refusal path reads no user or system gitconfig.

## A2 — Judge `tag_to_tree` row (observed, frozen candidate judge)
- **Fixture.** The tree is `<tip>^{tree}`, and it must be non-empty: `ls-tree` must produce output, or the judge raises Cannot (676-682).
  - `tag("tree", tree)` creates a real annotated tag named `r21-target-check-boot-chain-tree` with `git tag -a`, using `tag.gpgSign=false` and an isolated config. It verifies the result with `<ref>^{tag}` (685-695, 701).
  - The tag name embeds the tool name, so each of the nine tools gets an independently created tag object.
- **Selectors.** The judge uses the full tag object ID plus the shortest prefix, of width 7 to 39 (`range(7, len(object_id))`), that is unique in an inventory taken after every class fixture is created (705-718). The same prefix must not collide with `refs/heads/` or `refs/tags/`.
  - The consumer resolves selectors with `--disambiguate` over the same object database, and consumer runs are read-only. So the uniqueness the judge computes is the uniqueness the consumer sees ([INFERENCE] the inventory and `--disambiguate` enumerate the same loose and packed objects; a `--no-hardlinks` local clone has no alternates, 220).
- **Exact refusal check.** Because `expected_commit is None`, each observation must satisfy `refused(..., ID_INVALID)` (exit 2 and first finding `E-REVISION-INVALID`, 383-393). It must also have `binding_ids == [ID_INVALID]` and `finding_count == 1` (720-725).
  - The row passes only if every observation is ok (730-732).
  - `target_type_measure` counts a tool only when all five classes pass (764-765).
- **Sandbox.** Each invocation uses a fresh `TemporaryDirectory`, then `clone_lane`, then `prepare` (742-746). The nine tools run sequentially in that one sandbox.
  - Fixture refs are deleted in `finally` (734-736). Orphan tag objects from earlier tools stay in the object database, but the per-tool inventory includes them, so prefix uniqueness still holds.
- **Host read by the judge.** Every judge `git` call carries `-c core.hooksPath=/dev/null` and `clean_env` (107-112). The lane is only read, through the clone.

## A3 — Comparison with build oracle `Oracle06TagTree.md`
- **Agreement.** The oracle expects exit 2, exactly one finding `E-REVISION-INVALID`, and no other ID acceptable (oracle 35-47). The row grades exactly that: exit, ID and count.
- **Oracle stricter than the row:**
  - `revision == "unbound"` and `branch_tip == null`: the row does not grade these (see R1).
  - The exact `detail`/`site` and the status string are not graded.
  - The upper-case form of S is listed by the oracle but not exercised by this row.
- **Oracle facts superseded.** The oracle's A3 ("no tag-to-tree case") described the round-20 matrix. The candidate adds the row, so that gap is closed for the consumer-level exit/ID/count axis.

## A4 — Mutant search (proposed, NOT executed; outcomes are source predictions)
| Mutant (one point) | Predicted `tag_to_tree` outcome | Killed by |
|---|---|---|
| M1 `_revision.py:140` `^{commit}` → `^{}` | The tree ID reaches `_ancestor`. `merge-base --is-ancestor <tree>` exits ≥2 ([INFERENCE] git semantics), giving `E-GIT-FAILED` | the `tag_to_tree` row (found ≠ `E-REVISION-INVALID`) |
| M2 `_revision.py:143-146` peel failure → raise `E_GIT` | `E-GIT-FAILED` | the `tag_to_tree` row |
| M3 `_revision.py:134` accept `tag` as a commit (`return oid`) | `merge-base` peels the tag to a tree and exits ≥2, giving `E-GIT-FAILED` | the `tag_to_tree` row. The old matrix `annotated_tag_object` also fails, because the JSON revision is the tag ID, not the tip |
| M4 one-level peel (accept only a tag whose direct target is a commit) | `E-REVISION-INVALID`, so this row passes correctly | sibling row `nested_tag_to_commit` (tag→tag→commit refused) |
| M5 refuse every tag object | this row passes correctly | `annotated_tag_to_commit`, `nested_tag_to_commit`, and old `annotated_tag_object` |

The judge's own selftest witness matches M1 on a stub, not on the real consumer:
- Stub mode `target-generic-peel` (judge 981-989) survives the old matrix and is rejected by the new `tag_to_tree` row (1239-1250).

**No single-point mutant was found that is a false green on this row's predicate.**

Residuals (outside the predicate, or graded elsewhere):
- **R1 — revision echo on refusal is ungraded.**
  - Mutant: consumer 1571 `revision, branch_tip = "unbound", None` → `args.revision, None`.
  - Predicted result: still exit 2, `[E-REVISION-INVALID]`, count 1, so the row stays ok, while the JSON `revision` carries the 40-hex tag ID.
  - This is by design: judge 482-483 says so, and selftest `object-selector-cannot-revision-echo` (1269-1276) asserts that echo passes.
  - There is no false acceptance, because the exit code stays 2. But it diverges from the oracle's `revision == "unbound"` requirement.
- **R2 — upper-case selector not exercised for `tag_to_tree`.**
  - Lower-casing happens before the type branch (`_revision.py:119`), so case handling does not depend on object type, and it is covered by old `uppercase_object` (judge 629).
  - I found no type-specific mutant.
- **R3 — the judge does not independently assert the tag's `type tree` line.**
  - It relies on `git tag -a ... <tree>` plus the `^{tag}` check (690-695), and on a non-empty `ls-tree` of the target tree. The risk is low.
- **R4 — outside this predicate, flagged for the accept-class seats.**
  - On the accept rows (`annotated_tag_to_commit`, `nested_tag_to_commit`), the consumer reaches its own `git()` (801-811). That function rebuilds its environment from `os.environ` minus every `GIT_*` key. This strips the judge's `GIT_CONFIG_NOSYSTEM`/`GIT_CONFIG_GLOBAL`, so `git show` there would read host gitconfig ([INFERENCE]).
  - This is not reachable on the `tag_to_tree` refusal path.

## A5 — Continuity and accounting (observed)
- **Commit-tag continuity.** `annotated_tag_to_commit` (judge 697, 703) repeats the old matrix's `annotated_tag_object` and `annotated_tag_prefix` (631-632). It is continuity, not new coverage.
  - `tag_to_tree`, `tag_to_blob`, `nonempty_tree` and `nested_tag_to_commit` are the new classes.
- **Old matrix unchanged.** Every `def` and `cases[...]` anchor at lines 100-673 sits at identical line numbers in the snapshot judge and the candidate judge. I did not byte-diff or hash the two ranges.
  - `measure()` never calls `target_type_probes`. Its only callers are 764, 1234 and 1246.
  - `--object-target-types` is mutually exclusive with `--object-selectors` (1391-1395).
  - `grade()` (886-890) does not use the target-type matrix.
- **Mode accounting.** `target_type_mode = int(available)` comes from a single AST census of the judge's functions and options at the tip (748-761, 773). It is reported separately from `target_type_tools`, the behavioral count over the original nine (764-772, 779).
  - Mode 0→1 is availability counted once. It is not a ninefold behavioral uplift.
  - Selftest `target-type-missing-mode-is-not-behavior-failure` (1251-1254) pins mode 0 together with behavior equal to `TOTAL`.

## Observations, inferences and limits
- **Observed:** every line citation above, read from the frozen candidate files and the snapshot judge only.
- **Inferred (marked [INFERENCE] above):**
  - git's exit status for `merge-base --is-ancestor` on a tree;
  - that `--disambiguate` and `--batch-all-objects` enumerate the same object set;
  - the gitconfig read on accept paths.
- **Not done:**
  - Nothing was executed: no consumer, judge, selftest or mutant.
  - No hashing.
  - No live or draft files were used for any verdict.
  - No tools were installed or needed.
- **Not claimed:** non-author closure, outside promotion, or any result for other consumers or classes.

Scope: executed=none
