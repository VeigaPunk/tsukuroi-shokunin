# Fx02TagTree — falsify check-root-dac-correction.py × tag_to_tree (candidate 0a14952b)

Reviewed-SHA256: 945081ef19d10661537fdac7b58a6627e4ca2dc072704b440c4eaf7fe1737b5f
Predicate: check-root-dac-correction.py-tag_to_tree-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Primary file: `.ufo/waves/round-21/candidate/tools/check-root-dac-correction.py` (SHA256 above, revision 0a14952b59d20179e1c813af58befaecd6992a17, as listed in `candidate-files.json`; digest not recomputed, NO-EXEC).
Auxiliary snapshot dependencies (frozen candidate copies, cited via `candidate-files.json`, not bound by this receipt):
- `candidate/tools/_revision.py` — sha256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
- `candidate/tools/check-revision-binding.py` — sha256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6
Build oracle compared: `.ufo/waves/round-21/build/Oracle02TagTree.md` (written against the pinned `snapshot/` binder and the live consumer, not these candidate copies).

## Verdict
**One located false-green, in the coverage of this row.** The candidate consumer and binder handle `tag_to_tree` correctly on every path I traced. However, the new `tag_to_tree` row only probes selectors that no ref collides with. A one-line binder mutant that falls back to ref parsing after a failed tag peel survives this row, the other four new rows, the old object-selector matrix, the consumer's own selftest, and the `_revision.py` selftest. The build oracle named this mutant, and the candidate added no control that kills it.

## Axes
1. Consumer bind / argv / error / output propagation for a tag→tree object ID.
2. Fixture realism: the probe creates a real annotated tag that points at a tree.
3. Grading strictness: exit code, exact refusal ID, and finding count.
4. Selector coverage: full ID, unique prefix, and ref-collision shadows.
5. Sandbox freshness and absence of host reads.
6. Continuity: the old matrix is unchanged, tag→commit is not counted as new coverage, and the mode 0→1 change is not counted as behavioral uplift.

## Observations (source read; nothing executed)
### Consumer propagation (check-root-dac-correction.py)
- The import is path-local: line 27 runs `sys.path.insert(0, <tools dir>)`, line 28 sets `dont_write_bytecode`, and line 29 runs `import _revision`. `ROOT = Path(__file__).resolve().parents[1]` (line 37). In the judge's sandbox, both therefore resolve inside the clone.
- `main` (533–545): `--revision` and `--selftest` are mutually exclusive, and `--branch` defaults to `master`. It calls `run_gate(ROOT, args.revision, args.branch)` and then `emit(...)`. `sys.exit(main())` propagates the exit code (548–549).
- `run_gate` (264–283): `_revision.bind(repo, revision, branch)` runs at line 275. On a `RevisionError`, line 277 sets `tip = branch_tip(...)`, and line 278 re-raises as `Cannot(exc.fid, exc.site, exc.detail)`. This produces `Result(CANNOT, [one Finding], 0)` with `label` equal to the raw selector (lines 268 and 282). `read_git` and `evaluate` are never reached, so no document findings can be added.
- `emit`/`payload` (224–233) print one JSON object: `status: CANNOT_EVALUATE`, `revision: <selector as typed>`, and `findings` containing exactly one entry. The function returns 2.

### Binder path for a tag→tree OID (_revision.py)
- In `bind` (172–192): `validate_branch("master")` passes, and the `REV` 7–64 hex check passes. Then `_object_commit` (112–146) runs. `rev-parse --disambiguate=<lower>` returns one object (line 119), and `cat-file -t` returns `tag` (127–137). The peel `<oid>^{commit}` (139–140) is nonzero. `rev-parse --git-dir` succeeds, so the function returns `None` (143–145). Lines 177–178 then raise `E-REVISION-INVALID` with detail "`<rev>` does not name one commit".
- **Source prediction:** exit 2 and exactly one finding, `E-REVISION-INVALID`, for both the full ID and a unique prefix. This matches the build oracle's expectation, Oracle02TagTree lines 22–27.

### Judge row (check-revision-binding.py `target_type_probes`, 676–736)
- **Real typed object:** the tree is `tip^{tree}` and must be non-empty (677–682). `tag("tree", tree)` (685–695) runs `git tag -a r21-target-check-root-dac-correction-tree -m tree <tree>` and returns `ref^{tag}`, which is the tag object ID. The expected outcome is hard-coded from how the fixture was built: `(tag(...), None)` at line 701 maps to `refused(..., ID_INVALID)` (721–725). It does not call the judge's `object_commit`, so it shares no code with the binder under test. This is good. One limit: nothing runs `cat-file -p` to assert that the tag's `type` header is `tree`; the row relies on `git tag` semantics.
- **Grading:** `refused` (383–393) requires `exit == 2` and that the first finding ID equals `E-REVISION-INVALID`. The row then adds two more requirements: `binding_ids == [E-REVISION-INVALID]` and `finding_count == 1` (723–725). Here `finding_count` counts all findings, not only binding ones. This is exact and strict.
- **Selectors:** the row probes the full lowercase ID, plus the shortest prefix from 7 to 39 characters that is unique in the `cat-file --batch-all-objects` inventory **and** has no `refs/heads/<p>` or `refs/tags/<p>` (712–718). The inventory is taken after all five fixtures exist (705–707), and the consumer creates no objects. Uppercase input is not probed for this class.
- **Sandbox:** `target_type_measure` (739–781) creates one `TemporaryDirectory` clone per measurement. `prepare` (233–242) detaches at the tip, pins `refs/heads/<branch>`, removes `origin`, and recreates only the tracking ref. `materialize` (259–274) writes the nine tools from the tip; `_revision.py` comes from the checkout at the tip. The sandbox is fresh per measurement, not per tool: `check-root-dac-correction.py` is `TOOLS[1]`, so it runs after `check-locator-clarification.py`. Earlier tools' tag refs are deleted in `finally` (734–736), but their tag objects stay in the object store. That is harmless here, because uniqueness is computed over the whole inventory and tag names are specific to each tool.
- **No host read by the consumer:** `run_tool` (359–371) runs `sys.executable sandbox/tools/<name> --revision X --branch master` with `cwd=sandbox` and `clean_env()`, which strips `GIT_*`, sets `GIT_CONFIG_NOSYSTEM=1`, and sets `GIT_CONFIG_GLOBAL=/dev/null`. The consumer's git calls all use `-C <sandbox ROOT>`. The judge itself reads the host lane only through `clone_lane`, which is intended. [INFERENCE] If the lane used `objects/info/alternates`, the clone would still reference host objects; I did not check this.

### Build-side witness
The judge selftest (1234–1259) runs the `target-generic-peel` stub, in which a tag peels via `^{}` (981–989). The stub peels the tag→tree to the tree OID, and then `merge-base --is-ancestor <tree>` gives `E-GIT-FAILED` (997–1001). The new `tag_to_tree` row rejects that result, while the old matrix stays at TOTAL. This kill is real, but the stub only models the `^{}` mutant.

## Located false-green (proposed mutant, NOT executed)
**M-PEELFALLBACK** is a single edit to the binder that the consumer imports. In `candidate/tools/_revision.py` at line 145, inside `_object_commit`'s tag branch, replace

```python
        return None
```

with

```python
        return _commit(repo, revision)
```

Predicted behavior:
- **`tag_to_tree` row, full ID:** for a full 40-hex string, git resolves the object before any ref [INFERENCE from git's full-hex rule]. The `^{commit}` peel fails, so `_commit` returns `None` and the result is `E-REVISION-INVALID` ×1. **The row passes.**
- **`tag_to_tree` row, prefix:** the row deliberately picks a prefix with no ref collision, so `_commit(prefix)` resolves the same tag, the peel fails, and the result is `None` and `E-REVISION-INVALID` ×1. **The row passes.** `tag_to_blob` behaves the same way. `nonempty_tree` never reaches line 145, because its kind is `tree` and it returns at line 137. The commit and nested-tag classes peel successfully. **All five new rows stay green.**
- **Old matrix:** every annotated tag in `object_selector_probes` targets a commit, so the peel succeeds. Ghost-hex selectors return at `len(objects) != 1` (123–124), and the blob returns at line 137. No old case reaches line 145. **The old matrix stays green.** The consumer's own `binding_cases` (386–495) has no tag→tree case. The `_revision.py` selftest cases `annotated-tag-to-tree/blob-invalid` (413–419) use a full ID with no ref shadow. **They stay green.**
- **Divergence that nothing probes:** take a selector `p` that is a unique prefix of a tag→tree OID, with `refs/heads/p` or `refs/tags/p` pointing at a landed commit `D`. `_commit(p)` then resolves the **ref** [INFERENCE: for a short hex, git prefers refs. This is the documented reason `_revision` uses `--disambiguate` first, and the reason the judge has `real_prefix_shadow_*` rows at 596–615]. `bind` then accepts `D`. `run_gate` reads the R12/R13 documents at `D` (line 280), exits 0 or 1, and reports JSON `revision = D`. This violates the oracle's stated expectation, Oracle02TagTree line 27: "...and for a branch or tag ref named like `T` pointing at a landed commit: the object lookup comes first". The build oracle described this "stronger mutant" at line 37.
- **Root cause in the candidate:** the old matrix shadows prefixes of commits and tag→commit objects with refs. The new target-type rows explicitly exclude ref collisions (714–715) and add no shadow controls. The type-failure branch of `_object_commit`, lines 143–145, therefore has no selector that could make a ref-parsing fallback observable.
- **Suggested kill control (not executed):** for `tag_to_tree` (and `tag_to_blob`), add `refs/heads/<prefix>` and `refs/tags/<prefix>` pointing at a landed decoy, then require exact refusal: `E-REVISION-INVALID`, `binding_ids == [ID]`, and `finding_count == 1`. This mirrors `real_prefix_shadow_*` and `unlanded_prefix_shadow_*`.

Within the predicate, no further defect was found. In particular, a consumer-local fallback in `run_gate` that falls back on any `E-REVISION-INVALID` would also accept the old matrix's ghost-hex branch and tag rows at 524–533, so the old matrix kills it.

## Continuity and limits
- `annotated_tag_to_commit` (line 703) repeats the old `annotated_tag_object` and `annotated_tag_prefix` checks (631–632). It preserves continuity and is not new coverage. `nested_tag_to_commit` is out of this row's scope.
- I treated `object_selector_probes` (475–673) as the unchanged old matrix based on its separate function body. I did not diff it against baseline 82e5192, so this is an observation of separation only.
- `target_type_mode` (749–759) is an AST census that counts once whether the functions and the `--object-target-types` option are present. `behavioral_tools` is counted separately. A move from mode 0 to mode 1 is not a ninefold behavioral uplift, and the selftest at 1251–1254 encodes the expectation (mode 0, tools TOTAL) for a stub lane without the mode.
- Git precedence claims (a full hex resolves the object first, a short hex resolves the ref first) and the merge-base exit code for a tree are inferences from git semantics and were not observed. No LSP was used; this was a textual trace of single-module call chains with read/grep only. Nothing was executed, compiled, imported, or installed, and no tools were needed. This is a review by the candidate's falsify seat, not a non-author closure or an outside promotion.

Scope: executed=none
