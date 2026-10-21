# Fx04TagTree — falsify: check-source-scope-correction.py × tag_to_tree (candidate control)

Reviewed-SHA256: 931504455caae52eaa2f2018a826c1b40c1eed83025ec0f13d1127c66fb85afc
Predicate: check-source-scope-correction.py-tag_to_tree-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Seat: TsukuroiR21.Fx04TagTree (fresh attack seat, NO-EXEC). Candidate revision
0a14952b59d20179e1c813af58befaecd6992a17; baseline 82e519203e676c532b1dc5ea91a85671f2286e7b.

## Bytes reviewed
- Primary (bound by the receipt above): `.ufo/waves/round-21/candidate/tools/check-source-scope-correction.py`.
  The digest is the one `candidate-files.json:14-17` lists. I did not recompute it (NO-EXEC).
- Auxiliary snapshot dependencies (read only, not bound by the receipt):
  - `candidate/tools/_revision.py`, inventory sha256 `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf` (`candidate-files.json:63-66`).
  - `candidate/tools/check-revision-binding.py`, inventory sha256 `0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6` (`candidate-files.json:39-42`).
- Comparison only: build oracle `.ufo/waves/round-21/build/Oracle04TagTree.md`. It is not candidate evidence.
- No live `tools/` file and no moving draft was read for this verdict.

## Axes
- A1 bind/argv: how the judge invokes this consumer, and how the consumer forwards the selector to the binder.
- A2 error/output propagation: how `RevisionError` becomes the exit code and JSON (status, findings, revision, branch_tip).
- A3 judge row strength: whether the fixture is a real typed object, the exact refusal ID and count are checked, the sandbox is fresh, the prefix is unique, and there is no host read.
- A4 mutant sensitivity: whether a concrete weakening survives this class.
- A5 accounting: old matrix unchanged, commit-tag kept as continuity only, and mode 0→1 not counted as a behavioral uplift.

## A1 — argv and bind (source observations)
- Judge `run_tool` (`check-revision-binding.py:359-371`) runs
  `[sys.executable, <sandbox>/tools/check-source-scope-correction.py, --revision, <sel>, --branch, master]`
  with `cwd=<sandbox>`, `stdin=DEVNULL` and `env=clean_env()`.
  - `EXTRA["check-source-scope-correction.py"]` is `()` (`:77`), so no extra argv is added.
  - The branch comes from `target_type_probes(sandbox, name, tip, branch)` through `refused(..., branch)` (`:722`).
- Consumer `main` (`check-source-scope-correction.py:614-658`):
  - argparse uses a mutually exclusive group, `--revision` vs `--selftest` (`:617-621`); `--branch` defaults to `master` (`:622`).
  - `:637` sets `revision = args.revision` to the raw selector.
  - `:639` calls `_revision.bind(ROOT, args.revision, branch)` with the selector unchanged.
  - `ROOT = Path(__file__).resolve().parents[1]` (`:18`) resolves to the sandbox, because the judge materializes the tool at `<sandbox>/tools/` (`:259-273`).
  - `import _revision` (`:15`) resolves to `<sandbox>/tools/_revision.py`, which comes from the `prepare` checkout of the tip (`:233-234`). The script directory is first on `sys.path`.
  - `sys.dont_write_bytecode = True` (`:14`) is set before that import, so no `__pycache__` is written into the sandbox.
- Binder path for a tag→tree selector (`_revision.py`):
  1. `bind` (`:172`): `validate_branch("master")` passes (`:84-95`), and `REV` 7-64 hex matches the 40-hex tag OID or its 7..39-hex prefix (`:175`).
  2. `_object_commit` (`:112-146`):
     - `rev-parse --disambiguate=<lower>` returns exactly one OID (`:119-124`).
     - `cat-file -t` reports `tag` (`:127-137`).
     - The `<oid>^{commit}` peel (`:139-140`) fails for a tree target, and `rev-parse --git-dir` succeeds, so the function returns `None` (`:141-145`).
  3. `bind` raises `RevisionError("E-REVISION-INVALID", "revision", "<sel> does not name one commit")` (`:178-179`).
  4. The branch, ancestor and origin checks (`:180-192`) are never reached.

## A2 — error and output propagation (source prediction for the tag_to_tree row)
- `:640-641` re-raises `RevisionError` as `Cannot(exc.fid, exc.site, exc.detail)`.
- The outer `except Cannot` (`:647-649`) calls `emit(Result(CANNOT, [Finding], 0), revision, branch, branch_tip)`:
  - `revision` is still the raw selector.
  - `branch_tip` is still `None`, because it is assigned only after a successful bind (`:642`).
  - `read_git` and `evaluate` are never reached (`:643`, `:653`).
- `emit` (`:336-343`) prints one sort-keyed JSON line and returns 2; `sys.exit(main())` (`:661-662`).
- Predicted output for both the full-OID selector and the unique-prefix selector:
  - Exit 2.
  - `{"branch":"master","branch_tip":null,"correction_count":0,"findings":[{"detail":"<sel> does not name one commit","id":"E-REVISION-INVALID","site":"revision"}],"revision":"<sel>","status":"CANNOT_EVALUATE"}`
- This matches the build oracle's preregistered expectation (`build/Oracle04TagTree.md:45-52`). That is agreement between two source readings, not an observation.

## A3 — judge row `target_type_probes` "tag_to_tree" (source observations)
- **Actual typed object, created independently:**
  - `tree = rev-parse <tip>^{tree}` (`:678-679`), and `ls-tree` must be nonempty (`:680-682`).
  - `tag("tree", tree)` creates a fresh annotated tag. It refuses a pre-existing ref (`:688-689`), runs `git tag -a r21-target-<tool>-tree -m tree <tree>` (`:690-692`), and resolves the tag object through `ref^{tag}` (`:694-695`).
  - The expected value is the hard-coded `None`, meaning a refusal is required (`:701`). It is not derived from the judge's or the binder's resolver.
  - Limit: the judge does not read back the tag header `type tree` (for example with `cat-file -p`). Correctness rests on how the fixture was built.
- **Exact refusal ID and count:**
  - `refused()` (`:383-393`) requires `exit == 2` and first finding id `== E-REVISION-INVALID`.
  - `:723-725` additionally requires `binding_ids == [E-REVISION-INVALID]` and `finding_count == 1`.
  - Both selectors (full OID and prefix) must pass (`:720-732`).
- **Fresh sandbox:**
  - `target_type_measure` creates a `TemporaryDirectory` (`:743`), runs `git clone --no-hardlinks --no-tags` (`:218-230`, `:745`), and `prepare` (`:746`, `:233-242`) detaches at the tip, sets `refs/heads/<branch>` and recreates only `refs/remotes/origin/<branch>`.
  - One sandbox is shared across the nine tools. Each tool's tags are removed in `finally` (`:734-736`); their objects remain and are included in the next inventory.
  - The selftest oracle (`:1234`, `:1246`) runs the probes directly in a mktemp fixture repository, not in a clone.
- **Unique prefix:**
  - The inventory is taken with `cat-file --batch-all-objects` after all five fixture objects exist (`:705-707`).
  - The prefix is the shortest width in 7..39 that is unique in that inventory and has no `refs/heads/` or `refs/tags/` alias (`:712-718`). If none qualifies, the run stops with CANNOT (`:716-717`).
  - The refusal path creates no objects, so the inventory stays valid for the whole row.
- **No host read on this row:**
  - The consumer reaches only `_revision._git` and `validate_branch`. Both run with `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` (`_revision.py:62-66`, `:71-73`, `:89-91`), against `repo=ROOT`, which is the sandbox.
  - The consumer's own `git()` (`:354-363`) strips every `GIT_*` variable, including the two isolation variables the judge set, so it would read the host's `/etc/gitconfig` and `~/.gitconfig` [INFERENCE]. It is reached only through `read_git` after a successful bind (`:643`), so it is not reached on this row.
  - The judge's own lane read (`bind(lane, …)` at `:742`, then the clone) is by design and is not a consumer read.

## A4 — mutants (all proposed, none executed)

**Killed within the predicate (source prediction):**
- **K1, generic peel.** In `_revision.py:139-140`, change `f"{oid}^{{commit}}"` to `f"{oid}^{{}}"`.
  - On tag→tree, `sha` becomes the tree OID, and `_ancestor` (`:156-160`) runs `merge-base --is-ancestor <tree> refs/heads/master`.
  - The judge kills it for every possible Git exit code:
    - rc ≥ 2 gives `E-GIT-FAILED`.
    - rc 1 gives `E-REVISION-NOT-LANDED`.
    - rc 0 accepts, so the exit is not 2.
  - The rc value itself is [INFERENCE]; the kill does not depend on it.
  - The old object-selector matrix (`:475-673`) has no tag→non-commit case, so K1 survives there.
  - This agrees with build `Oracle04TagTree.md:70-79`. The judge selftest witness `tree-tag-mutant-new-matrix-rejects` (`:1239-1259`) shows the same thing, but only for the STUB `target-generic-peel` (`:981-989`) placed at `TOOLS[0]` (check-locator-clarification.py). It does not run this real consumer, so the selftest provides no consumer-specific oracle here.
- **K2, tree→commit resolution.** A peel that maps the tree to a commit owning it would resolve to the tip, because the fixture tree is `tip^{tree}`. The tool then accepts with an exit other than 2, so the row fails.
- **K3, wrong error id.** Rewriting the error id in `main` (for example, `:641` emitting `E-INTERNAL`) breaks the id equality check.
- **K4, extra finding.** Appending a content finding to the refusal breaks the `finding_count == 1` check.
- **Equivalent, not a kill.** Dropping the guard `if object_kind != "tag": return None` (`_revision.py:136-137`) still returns `None` for this class, because a non-tag object also fails to peel to a commit.

**Survivors outside this predicate (not tag_to_tree-specific; they affect every refusal row in both the old and new matrices):**
- **S1, refusal `revision` echo replaced.** At consumer `:648-649`, pass `_revision.branch_tip(ROOT, branch) or revision` instead of `revision`.
  - Output: exit 2, `CANNOT_EVALUATE`, one `E-REVISION-INVALID`, but `"revision": <tip commit SHA>`. Downstream readers would see a landed SHA on a refused tag→tree selector.
  - `refused()` records `json_revision` (`:388-392`) but never grades it (`:393`, `:721-725`). The consumer's own `cli_probe` (`:471-492`) checks only exit, status and ids. So S1 survives both.
  - The build oracle preregistered that the echo must be the selector (`Oracle04TagTree.md:52`), so the judge grades less than the oracle preregistered.
- **S2, status ignored.** Make `emit` report `"status":"PASS"` on CANNOT.
  - The judge's refusal checks never read `status`. The comment "Grade the explicit status and exact finding" (`:482-483`) does not match the code (`:484-485`).
  - S2 is killed only by the consumer selftest (`:487`), which is not part of the judge row.
- **Environment hazard [INFERENCE].** The judge's `clean_env` (`:100-104`) keeps `PYTHON*` variables, and `run_tool` does not pass `-I` or `-P`.
  - Under `PYTHONSAFEPATH=1`, the script directory is not on `sys.path`:
    - With no `PYTHONPATH`, `import _revision` fails, exit is 1, and the row fails closed.
    - If `PYTHONPATH` names a production `tools/` directory, the measured binder would not be the candidate's.
  - This needs an operator environment I did not observe.

## A5 — accounting (source observations)
- **Old matrix unchanged:**
  - `target_type_probes` is called only from `target_type_measure` (`:764`) and from selftest (`:1234`, `:1246`).
  - `measure()` and `object_selector_probes` (`:475-673`, `:783-883`) contain no tree or tag-target class.
  - `--object-target-types` is a separate flag (`:924-925`) and is refused when combined with `--object-selectors` (`:1391-1395`).
- **Commit-tag continuity:** `annotated_tag_to_commit` (`:703`) re-exercises the old `annotated_tag_object` and `annotated_tag_prefix` cases (`:631-632`). It is continuity, not new coverage. The new cell for this consumer is `tag_to_tree`, alongside `tag_to_blob`, `nested_tag_to_commit` and `nonempty_tree`, as described in `build/ConnPlanner.md:29`.
- **Mode vs behavior:** `target_type_mode = int(available)` is counted once from an AST census (`:750-761`, `:773`). It is reported separately from `behavioral_tools = count` (`:767`, `:775`), and each tool's `behavior_ok` requires all five classes (`:765`). Mode 0→1 is therefore not a nine-fold behavioral uplift.

## Verdict
- **Within the predicate, no defect.** On the tag_to_tree row, the frozen consumer plus the frozen `_revision.py` are predicted to emit exit 2 with exactly one `E-REVISION-INVALID` finding for both the full-OID and the unique-prefix selector. The judge row requires exactly that, uses an independently built tag→tree object in a fresh clone with a prefix-uniqueness check, and kills K1 through K4.
- **Concrete survivors outside the predicate:** S1, the unchecked refusal `revision` echo, located at consumer `:647-649` and judge `:383-393` / `:721-725`; and S2, the ungraded `status`, located at judge `:482-485`. Both affect every refusal row and are not tag_to_tree-specific.

## Limits
- Source review only. Nothing was executed: no consumer, judge, selftest or mutant run.
- Git exit codes for `merge-base` with a tree argument are [INFERENCE], but the K1 kill holds for any rc.
- Digests are quoted from `candidate-files.json`, not recomputed.
- No non-author closure and no outside promotion is claimed.

Tooling: no installs or updates. None were needed, and NO-EXEC forbids them.

Scope: executed=none
