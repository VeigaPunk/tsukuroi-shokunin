# Fx07TagBlob — falsify check-freshness-r17.py × tag_to_blob (candidate 0a14952b)

Reviewed-SHA256: 836ade1b23ed459b922d8c680d2bbbb87d7abb4e6af7c84265e2ab1cffa01668
Predicate: check-freshness-r17.py-tag_to_blob-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Primary file: the frozen copy `.ufo/waves/round-21/candidate/tools/check-freshness-r17.py` (revision 0a14952b59d20179e1c813af58befaecd6992a17; the digest is the one in `candidate-files.json`, not recomputed under NO-EXEC).
The review also read these auxiliary frozen snapshots, which this receipt does not bind:
- `candidate/tools/_revision.py` (sha256 06b71e8c…8cbf per `candidate-files.json`).
- `candidate/tools/check-revision-binding.py` (sha256 0722537d…6fa6 per `candidate-files.json`).
- For the old-matrix comparison only: `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.
- Build oracle: `.ufo/waves/round-21/build/Oracle07TagBlob.md`. That oracle read the live consumer, which was a moving file, so it is only used here as a comparison.

No live or draft tools were read to reach the verdict.

## Verdict
- **The consumer and binder have no defect for tag_to_blob.** The candidate code refuses this class with exactly one `E-REVISION-INVALID` finding, and it also refuses it when a ref named after the selector exists.
- **The candidate row has a real gap in what it can tell apart.** A binder mutant that falls back to ref resolution when a tag fails to peel (M2 below) would get past the tag_to_blob row. Every other row in the old and new matrices would also report it as clean (source prediction, not executed). The row reports green for M2, while M2 would accept a prefix selector that is shadowed by a ref.
- **Result:** within the stated predicate, the row passes for the candidate as written. As a control it is incomplete, and there is one concrete mutant it misses.

## Axes
1. How the consumer binds the selector and passes argv through.
2. Exit status, finding id, finding count and the JSON fields the consumer emits.
3. Whether the fixture is really a tag object pointing at a blob, and whether it was built independently of the code under test.
4. Prefix sanity: uniqueness and ref collisions.
5. Sandbox freshness and host reads.
6. Mutant sensitivity: which mutants are killed and which survive.
7. Old-matrix continuity and how the C2 mode is counted.

## Source trace through the consumer (observed in frozen source)
- argv: `--revision` is a mutually exclusive required option (l.383-386). For this probe there is no `--registry-from`, and no extra argv because `EXTRA["check-freshness-r17.py"] = ()` (judge l.73, l.77-78).
- Binding:
  - `main` sets `revision = args.revision` (l.770).
  - It then computes the informational `tip = _revision.branch_tip(ROOT, branch)` (l.771).
  - It calls `_revision.bind(ROOT, args.revision, branch)` (l.773) with no local regex and no normalization.
  - `ROOT = Path(__file__).resolve().parents[1]` (l.55). Because the judge copies the tool to `<sandbox>/tools/` (judge l.269-272), `ROOT` is the sandbox.
  - `import _revision` (l.52) resolves from the script directory, i.e. the sandbox checkout at the measured tip (judge `prepare` l.234). `sys.dont_write_bytecode` stops a `__pycache__` being written (l.51).
- Binder path for a tag object whose target is a blob (`_revision.py`):
  - `validate_branch("master")` passes (l.84-95), and `REV` matches the full ID or the 7+ hex prefix (l.175).
  - `--disambiguate` returns exactly one object ID (l.119-124), and `cat-file -t` reports `tag` (l.126-137).
  - `rev-parse --verify --quiet <oid>^{commit}` fails (l.139-142). `rev-parse --git-dir` then succeeds, so the binder returns `None` (l.143-145) and raises `RevisionError(E-REVISION-INVALID, "revision", "<sel> does not name one commit")` (l.177-179).
- How the error propagates: `main` converts the `RevisionError` into `Cannot` and emits `Result(CANNOT, [one Finding], 0, 0, None)` (l.792-796). The predicted output is:
  - exit status 2, `status` `CANNOT_EVALUATE`;
  - exactly one finding, `E-REVISION-INVALID` at site `revision`;
  - `resolved_records` 0, `record_count` 0, and no `stale_records` key;
  - `revision` set to the raw selector as typed, which is not a binding;
  - `branch_tip` set to the informational master tip.
- The refusal happens before any `read_git`, so the registry, target, baseline and capture files are never read.

## Judge row `target_type_probes["tag_to_blob"]` (observed in frozen source)
- **Typed object:**
  - `blob_object()` writes a fixed blob with `hash-object -w` (judge l.408-413).
  - `tag("blob", blob)` runs `git tag -a r21-target-check-freshness-r17-blob` with `tag.gpgSign=false` and the environment isolated by `clean_env()` (l.685-695). It reads the object ID back through `rev-parse --verify <ref>^{tag}`, which proves that object is a tag.
  - The judge never asserts that the tag's target type is `blob`: there is no `cat-file -p` header check and no `^{}` type check. The build oracle recommended that check (Oracle07TagBlob "SHOULD … assert `cat-file -p` shows `type blob`"). The target type here holds because of how `git tag -a <blob-oid>` works [INFERENCE], not because the judge checks it.
- **Expectation:** the expected value is hard-coded. `expected_commit=None`, so the row requires `refused(..., ID_INVALID)`, which means exit status 2 and first finding `E-REVISION-INVALID` (l.383-393). It also requires `binding_ids == [E-REVISION-INVALID]` and `finding_count == 1` (l.721-725).
  - The expectation is not computed by the judge's `object_commit` or by `_revision.bind`, which keeps it independent.
  - The row does not check the site or the detail text. In the mutants considered below, the id alone carries the weight.
- **Selectors:** the row runs the full object ID, then one prefix (l.710-718).
  - The prefix width runs from 7 to 39 (`range(7, len(object_id))`), and the prefix must be unique in the `cat-file --batch-all-objects` inventory, which is taken after every fixture tag exists (l.705-707).
  - The prefix also must not exist as `refs/heads/<p>` or `refs/tags/<p>` (l.714-715). That deliberately excludes any ref shadow (see M2).
- **Fresh sandbox:**
  - `target_type_measure` makes a `TemporaryDirectory`, then runs `clone_lane` (`--no-hardlinks --no-tags`), `prepare` (detached checkout at the tip, `refs/heads/<branch>` and `refs/remotes/origin/<branch>` set to the tip, origin remote removed) and `materialize` (l.743-747).
  - Fixture tags are deleted in a `finally` block (l.734-736). Tag objects left over from earlier tools stay in the object database, but they are inside the inventory used for the uniqueness check, so they cannot cause a false prefix.
  - The sandbox is fresh per measure run, not per tool. For freshness, which is the 7th of the nine `TOOLS`, that is harmless.
- **Host reads on this row:**
  - The judge's `run_tool` uses `clean_env()`, which sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` (l.100-104, l.359-371). The consumer's binder `_git` re-applies the same isolation (`_revision.py` l.62-66).
  - On the refusal path every git call has `-C <sandbox>`, apart from `check-ref-format`, which needs no repository and runs with cwd set to the sandbox. No host file is read [source prediction].
- **Limit on the accept rows (not this row):** the consumer's own `git_in(..., isolate=False)` (l.325-330, used by `read_git` l.345-355) removes `GIT_*` from the environment and does not set `GIT_CONFIG_GLOBAL` or `GIT_CONFIG_NOSYSTEM`. On the accept rows (`annotated_tag_to_commit`, `nested_tag_to_commit`), the consumer therefore reads the user's global and system git config. The tag_to_blob refusal never reaches `read_git`.

## Mutants (proposed, not executed; outcomes are source predictions)
- **M1: generic peel.** In `_object_commit` l.140, peel with `f"{oid}^{{}}"` instead of `f"{oid}^{{commit}}"`.
  - For a tag pointing at a blob, the binder returns the blob ID. `merge-base --is-ancestor <blob> refs/heads/master` then exits with status ≥2, which becomes `E-GIT-FAILED` (l.156-160) [INFERENCE about git's exit status].
  - The row's `found == want` check fails, so **M1 is killed** by tag_to_blob. The judge's own `target-generic-peel` stub selftest shows the same mechanism for tag_to_tree (l.986-989, l.1239-1250).
- **M2: ref fallback after a failed peel. This one survives.** In `_object_commit`, replace l.143-145 (`if repo_check.returncode == 0: return None`) with `if repo_check.returncode == 0: return _commit(repo, revision)`.
  - **Row as written:** no ref is named after the selector.
    - The full-ID selector falls back to `rev-parse <tagoid>^{commit}`. For a full 40-hex string, git resolves the object, so the peel fails again and the result is `None`, giving `E-REVISION-INVALID` [INFERENCE: git prefers the object for full-length hex].
    - The prefix selector also has no matching ref, resolves to the same tag, fails the peel, and gives `E-REVISION-INVALID`.
    - The row is **ok** for both selectors.
  - **Other rows:** M2 is invisible to everything else.
    - `noncommit_blob` and the raw-blob/tree `blob-revision` rows return at `object_kind != "tag"` (l.136-137) before the fallback.
    - The `ghost_*` rows return at `len(objects) != 1` (l.123-124).
    - The tag→commit and nested rows peel successfully.
    - `tag_to_tree` has the same unshadowed shape as tag_to_blob.
    - The binder selftest `annotated-tag-to-blob-invalid` (`_revision.py` l.413-419) is also unshadowed.
    - The consumer's `binding_sandbox` (l.458-575) has no tag rows.
  - **The defect M2 introduces:** suppose `refs/heads/<p>` or `refs/tags/<p>` points at a landed commit, where `<p>` is a unique prefix of a tag object whose target is a blob. Git's ref lookup wins for an abbreviated name, so `bind` would return the decoy's commit. The consumer would then exit 0 or 1 with `revision` set to that decoy SHA.
  - That breaks the binder contract on l.115-117 ("Return commits by their already-confirmed object ID, never by reparsing") and the contract on l.264-266 ("Hex-looking references are not revision aliases"). The build oracle (Oracle07TagBlob) already named this weakening, but the candidate row excludes exactly that shape at l.714-715.
  - **Smallest kill:** after the unshadowed prefix observation, add an observation that creates `refs/heads/<prefix>` and then `refs/tags/<prefix>`, each pointing at a landed commit. Expect `E-REVISION-INVALID` with `finding_count == 1`, then remove the ref in a `finally` block. This mirrors the existing `unlanded_prefix_shadow_*` pattern (l.643-650).
- **M3: collapse every binding failure to `E-REVISION-INVALID` in the consumer** (`main` l.792-796). This survives tag_to_blob, as any refusal-only row would, but the old matrix kills it through `unlanded`, `not-pushed` and `branch-missing`. That is outside this predicate's discriminating job and is not a defect of the row.

## Old matrix and C2 counting
- **Old matrix unchanged (observed):** the `object_selector_probes` row inventory, meaning every `cases[...] = exact_*` assignment, sits at identical line numbers with identical labels in the snapshot and the candidate (l.526-666). `target_type_probes` does not exist in the snapshot.
  - `measure()` and `object_selector_probes` do not call `target_type_probes` (candidate l.474-673, l.783-849). The new classes are reached only through `--object-target-types`, via `target_type_measure` (l.1391-1409).
  - This comparison covers labels and line positions only; it is not a byte diff.
- **C2 counting:**
  - `target_type_mode = int(available)` is an AST presence census counted once (l.750-761, l.773).
  - Behavioural credit is per tool: `behavior_ok` requires all five cases (l.764-766), and tag_to_blob is one of them.
  - Going from mode 0 to mode 1 is not a nine-fold behavioural uplift.
- **Continuity:** `annotated_tag_to_commit` repeats the old `annotated_tag_object` and `annotated_tag_prefix` shape and gives continuity, not new coverage. Relative to the consumer-level CLI matrix, tag_to_blob itself is new coverage, because before this the only tag→blob case was in the binder selftest.

## Observations, inferences and limits
- **Observed in frozen source:**
  - the consumer's bind and error path, and the one-finding emission;
  - how the judge constructs and grades the row;
  - that prefix selection excludes ref collisions;
  - that the old row inventory is unchanged;
  - that the judge does not assert the tag's target type and does not check the site.
- **Inferred, not executed:**
  - the `rev-parse ^{commit}` peel failure for a tag→blob chain;
  - `merge-base` exiting with status ≥2 on a blob;
  - git resolving a full 40-hex string as an object but an abbreviation as a ref;
  - all three mutant outcomes.
- **Limits:**
  - Nothing was executed, and no digests were recomputed.
  - Whether the accept rows succeed for this consumer depends on `BASE` 6923fe0b being reachable in the sandbox clone. Otherwise `read_git` raises `E-GIT-READ-FAILED` (l.352-355), which is a false red and could not be checked here.
  - A signed-tag configuration and ambiguous prefixes are out of scope.
- **Tooling:** no tools were installed or upgraded, and none were needed. This report claims neither non-author closure nor outside promotion.

Scope: executed=none
