# Fx03CommitTag — check-section-citations.py × annotated_tag_to_commit (falsify, source-only)

Reviewed-SHA256: 1546d80403aa912e8f5b21710a85195e973216c120ec94457cfe5574c403aac3
Predicate: check-section-citations.py-annotated_tag_to_commit-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Primary receipt binds only `candidate/tools/check-section-citations.py` (candidate 0a14952b59d20179e1c813af58befaecd6992a17; digest as listed in `candidate-files.json:29-32`). Auxiliary frozen snapshot dependencies, read only and cited by their predispatch digests from `candidate-files.json`:
- `candidate/tools/_revision.py`, 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf (`:63-66`)
- `candidate/tools/check-revision-binding.py`, 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6 (`:39-42`)
- Context only (not a candidate verdict input): `snapshot/tools/check-revision-binding.py` (old-matrix continuity) and the build reports `build/ConnPlanner.md`, `build/CritBaseline.md`, `build/Oracle03NestedTag.md`.

I did not recompute any digest; NO-EXEC. Every behavior statement below is a **source prediction**. No observations of a run exist.

## Verdict

**The control is correct for the real consumer. It does not discriminate, though: one concrete false-green mutant survives this cell.** The accepted commit this row expects is `tip`. In the sandbox, `tip` is also `refs/heads/<branch>`, `refs/remotes/origin/<branch>` and the detached `HEAD`. So the "exact expected full commit SHA" check cannot tell "peeled the tag to its target commit" apart from "substituted the branch tip". Every annotated-tag fixture in the frozen candidate set points at `tip`, so a binder that swaps any tag selector for the branch tip stays green everywhere (mutant M1 below). This weakens the oracle; it is not a behavioral defect in the candidate consumer or binder. Within the cell's own claim (accept a tag→commit selector, emit the exact full landed commit), I predict no false green and no false red.

## Axes

- **Resolution**: selector → one object → type → recursive peel → landed/pushed.
- **Propagation**: consumer argv → `bind` → bound sha → emitted JSON `revision` and `git show` input.
- **Discrimination**: whether the cell's expected value separates the correct peel from plausible wrong bindings.
- **Hygiene**: independently typed fixture, unique prefix, fresh sandbox, no host read.
- **Continuity**: old matrix unchanged; mode 0→1 is not behavioral uplift.

## 1. Consumer propagation (frozen `check-section-citations.py`)

- `:36` `from _revision import RevisionError, bind`. `:35` sets `sys.dont_write_bytecode = True` before the import, so no `__pycache__` is written. There is no local revision regex or rev-parse in the binding path.
- `:430-444` uses an argparse mutually exclusive group (`--revision` | `--selftest`) plus `--branch` (default `master`), with `exit_on_error=False`. A parse failure becomes `E-CLI` with exit 2 (`:900-907`).
- `:913` `bind(ROOT, args.revision, branch)` receives the raw selector and branch unmodified. `ROOT = Path(__file__).resolve().parents[1]` (`:39`), which is the sandbox when the judge runs `sandbox/tools/<name>`.
- `:914` `revision = revision_binding.sha` and `:915` `branch_tip = revision_binding.branch_tip`.
- `:916-917` then binds the baseline `BASE = db68e62…` (`:40`) on the same branch.
- `:918-922` reads every document via `read_git(<peeled sha>, path)` → `git show <sha>:<path>` (`:417-427`). The tag object ID is never used for reads.
- `:923-927`: any `RevisionError` or `Cannot` becomes exactly one finding, exit 2. The emitted `revision` is the raw selector **only when the first bind fails**. If the `BASE` bind fails, `:914` has already run, so the emitted `revision` is the resolved sha with exit 2. This corrects the `Oracle03NestedTag.md:22` wording ("echoes the raw selector"). It is harmless here because `accepted()` requires exit ≠ 2 (§3).
- `:394-402` `emit` prints a single sorted JSON line: `status`, `revision`, `branch`, `branch_tip`, `correction_count`, `scope`, `findings`. On success the exit code is the `evaluate()` result, 0 or 1 (`:931-936`).

## 2. Binder path for an annotated tag → commit (frozen `_revision.py`)

| step | location | prediction for `commit_tag` (full ID or unique prefix) |
|---|---|---|
| branch syntax and `check-ref-format` | `:84-95`, called at `:174` | `master` passes |
| 7-64 hex | `:175-176` | passes (40 hex, or a 7-39 hex prefix) |
| `rev-parse --disambiguate=<lower>` | `:119-124` | exactly one object |
| `cat-file -t` | `:127-137` | `tag` |
| `oid^{commit}` peel | `:139-142` | returns `tip` (the full 40-hex rev-parse output) |
| branch exists | `:180-183` | `refs/heads/master` = tip (`prepare` in the judge, `:235`) |
| landed | `:184-185` | tip is an ancestor of itself |
| pushed | `:186-191` | origin ref = tip (`prepare` at `:240`), so it passes |

Consumer prediction for both selectors: binding accepted; JSON `revision` = `tip`, full lowercase 40-hex; exit 0 or 1 depending only on the R16 document evaluation at tip (unknown and irrelevant to this cell). The `BASE` bind also has to succeed. That requires `db68e62…` to be an ancestor of `tip` in the clone [INFERENCE: not verified, since I ran no git]. If it were not, the cell would go **red** (exit 2), never false-green.

## 3. Candidate control row (frozen `check-revision-binding.py`)

- **Independently created typed object**: `tag("commit", tip)` (`:697`) runs `git tag -a r21-target-check-section-citations-commit -m commit <tip>` with `tag.gpgSign=false` and the judge's isolated env (`:685-695`). The object ID comes from `rev-parse --verify refs/tags/…^{tag}` (`:694-695`), so it is a real annotated-tag object. `expected_commit = tip` (`:703`). `tip` itself comes from the judge's **own** `bind` (`:192-208`, called at `:742`), not from `_revision`. The judge does not separately re-assert the tag's `object` header (no `cat-file -p`); that the tag targets tip holds by construction [minor limit].
- **Selectors**: the full tag ID plus the shortest unique prefix of 7-39 hex (`:710-718`). Uniqueness is computed over `cat-file --batch-all-objects`, taken **after** all five fixtures exist (`:705-707`). Prefixes that collide with `refs/heads/<p>` or `refs/tags/<p>` are excluded, and if none qualifies the judge raises `Cannot("E-SANDBOX")`, which makes the measurement CANNOT, never green. The consumer runs read-only and adds no objects, so the inventory stays valid between the judge's computation and the consumer's `--disambiguate`. Leftover dangling tag objects from earlier tools in the same sandbox are part of that inventory, so they do not break uniqueness.
- **Acceptance oracle**: `accepted()` (`:396-404`) requires exit ≠ `CANNOT`, a JSON `revision` that is a string, and `revision.lower() == tip.lower()`. A no-peel mutant (emits the tag ID) fails. Peeling to `^{tree}` fails. Any binding refusal fails, even when it echoes the resolved sha (§1). A crash with no JSON fails. The cell's `ok` requires every selector `ok` (`:732`).
- **Fresh sandbox**: `target_type_measure` uses `TemporaryDirectory`, `clone_lane --no-hardlinks --no-tags` (`:218-230`, `:743-745`), and `prepare` (detached `HEAD` = tip, branch = tip, origin remote removed, origin tracking ref = tip; `:233-242`). The sandbox is fresh per measurement but shared across the nine tools. Fixture refs are deleted in `finally` (`:734-736`); tag objects persist, and that is accounted for (above). The mode is mutually exclusive with `--object-selectors` (`:1392-1395`), so this mode cannot perturb the old matrix's prefix inventory. That addresses the hazard raised in `CritBaseline.md:49-57`.
- **Consumer under test**: `run_tool` runs `sys.executable sandbox/tools/check-section-citations.py --revision <sel> --branch master` with `cwd=sandbox` and the judge's `clean_env` (`:359-371`). `materialize` writes the tool from `tip` (`:259-274`). `_revision.py` comes from the tip checkout, so the cell grades the measured revision's binder, not the judge's.
- **Host read**: the judge's own git calls are isolated (`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `core.hooksPath=/dev/null`; `:100-117`), and so is `_revision._git` (`_revision.py:62-77`). **Limit**: the consumer's own `git()` (`check-section-citations.py:405-414`) rebuilds its env by dropping **every** `GIT_*` variable, including the judge's `GIT_CONFIG_NOSYSTEM` and `GIT_CONFIG_GLOBAL`. It re-adds only `GIT_OPTIONAL_LOCKS`, `GIT_PAGER` and `LC_ALL`. The document-stage `git show` reads (`:417-427`) therefore load host `/etc/gitconfig` and `$HOME/.gitconfig` [INFERENCE from git config precedence; `HOME` is inherited]. `git show` may also apply host-configured textconv to blobs [INFERENCE]. This does not touch the binding or the emitted `revision`, so it cannot flip this cell. It does mean the end-to-end "no host read" property holds for binding only, not for the consumer's evaluation stage.

## 4. Concrete surviving mutant (proposed, NOT executed)

**M1, tag selector → branch tip.** In frozen `_revision.py` `bind`, after `:177-183`:

```python
sha = _object_commit(repo, revision)
...
tip = _commit(repo, local)
if not sha.startswith(revision.lower()):   # mutant: any peeled (tag) selector binds the branch tip
    sha = tip
```

The guard compares against the lowercased revision, so commit selectors (full, prefix, uppercase, ref-shadowed) keep their own sha. Only peeled tag selectors are replaced.

Predicted survival across every frozen tag fixture:

| suite | tag fixtures | expected | M1 result |
|---|---|---|---|
| this cell (`:697`, `:703`) | `commit_tag` full + prefix | tip | tip → **green** |
| `nested_tag_to_commit` (`:702`) | nested → tip | tip | **green** |
| `tag_to_blob` / `tag_to_tree` (`:700-701`) | peel fails at `:139-146` before the mutant | E-REVISION-INVALID | **green** |
| old matrix `annotated_tag_object` / `_prefix` / `full_tag_object_id_ref_shadow` (`:502-504`, `:616-631`) | tag → tip | tip | **green** |
| `_revision.py` selftest `annotated-tag-full-object-id`, `-object-prefix`, `nested-annotated-tag-object`, `full-tag-object-id-ref-shadow` (`:353-377`) | all → tip | tip | **green** |
| `check-section-citations.py` selftest (`:590-615`, `:785-886`) | none; the binding sandbox creates commits only | — | **green** |

Harm: `--revision <annotated tag of an older landed commit>` would read and report the **branch tip** instead of the tagged commit, with `revision` = tip. That silently binds the wrong revision, and is a false green whenever tip passes and the tagged commit would not. A tag pointing at an **unlanded** commit would also be accepted, because tip is landed. That bypasses E-REVISION-NOT-LANDED, the lane's core binding contract (QUALITY27). Variants that resolve `HEAD^{commit}` survive this cell and the judge matrices too, because `prepare` detaches `HEAD` at tip. They are, however, killed by the `_revision` selftest, where `HEAD` is the detached unlanded commit (`_revision.py:226-228`).

Consumer-level variant M2: `:914` `revision = revision_binding.branch_tip`. This also survives this cell, but the old BOUND matrix `landed-parent` (`check-revision-binding.py:427`, expected parent ≠ tip) kills it. So within the whole suite, M1 is the survivor; M2 is not.

**Smallest kill without touching the old matrix**: target this new-matrix row (and `nested_tag_to_commit`) at a landed **non-tip** commit, for example `tip^1`, expecting that commit. Add a tag → unlanded-commit class expecting E-REVISION-NOT-LANDED with exactly one finding. `target_type_measure` currently computes neither a parent nor an unlanded commit (`:739-747`). The five-class hard-codes at `:765` (`len(cases) == 5`) and in the selftest at `:1235-1238` would need updating if a class is added. A retargeted row needs `CANNOT` when tip has no parent.

## 5. Continuity and counting

- The old matrix is unchanged. `object_selector_probes` case keys and line positions match between the candidate (`:475-673`) and `snapshot/tools/check-revision-binding.py` (`:475-673`), including `annotated_tag_object` `:631`, `annotated_tag_prefix` `:632`, and the tag name `r20-object-selector-*` at `:498`. The new fixtures use the `r21-target-*` names (`:686`), so they cannot collide.
- `annotated_tag_to_commit` duplicates the old `annotated_tag_object` and `annotated_tag_prefix` (same tag→tip shape, same `accepted` oracle). It is **continuity, not new coverage**, as `ConnPlanner.md:29,71` and `CritBaseline.md:36-39` already say. No AnnotatedTag build oracle exists (`ConnPlanner.md:29`). The nearest build predictions (`CritBaseline.md:23`, "accepted, exact landed commit"; `Oracle03NestedTag.md:24`) agree with my §2 prediction.
- `target_type_mode` is a single `int(available)` from an AST census of the judge at `tip` (`:748-761`, `:773`). It is counted once, not per tool. `target_type_tools` counts per-tool behavior separately (`:765-767`). C2 mode 0→1 is therefore one presence fact, not a nine-fold behavioral uplift. No consumer or binder bytes change for this class.

## Observations, inferences and limits

- **Observed (source text)**: every line cited above, read via `read` from the frozen candidate files, plus the snapshot judge for continuity.
- **[INFERENCE]**: git semantics (`--disambiguate` enumeration of a full ID, recursive `^{commit}`, config precedence, `git show` textconv), the `db68e62…` ancestry of the candidate tip, and every pass/fail prediction in §2-§4.
- **Limits**: nothing was executed, compiled or imported; M1/M2 are proposals, not run; no digest was recomputed; moving draft and production files were not used for the verdict. This is not non-author closure or outside promotion. No tool was installed or needed.

Scope: executed=none
