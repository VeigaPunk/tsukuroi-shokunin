# Fx05CommitTag — measure-update-recheck.py × annotated_tag_to_commit (falsify attack)

Reviewed-SHA256: 0275af5a8afd6de26086d6901bd9c62b53a3390ba92ca950cb0602996326ccb7
Predicate: measure-update-recheck.py-annotated_tag_to_commit-candidate-control

Candidate revision: 0a14952b59d20179e1c813af58befaecd6992a17. The primary file is `candidate/tools/measure-update-recheck.py`. Its digest was taken from `candidate-files.json:24-28` and was not recomputed (NO-EXEC).

Auxiliary snapshot dependencies were read but are not covered by the primary receipt:
- `candidate/tools/_revision.py`, sha256 `06b71e8c…cbf` (`candidate-files.json:64-68`);
- `candidate/tools/check-revision-binding.py`, sha256 `0722537d…6fa6` (`candidate-files.json:39-43`).

Comparison-only reads (no verdict rests on them):
- `build/Oracle05NestedTag.md`;
- `build/ConnPlanner.md`;
- `snapshot/tools/check-revision-binding.py`, a grep for function line positions only.

Axes:
- A1. Consumer bind/argv propagation.
- A2. Error and exit propagation.
- A3. Output `revision` fidelity.
- A4. Typed-object construction.
- A5. Expected-commit discrimination.
- A6. Sandbox freshness and prefix sanity.
- A7. Host-read isolation.
- A8. Continuity with the old matrix.

## Verdict

**Defect found: a concrete false-green.** This is a source prediction. Nothing was executed.

The `annotated_tag_to_commit` row cannot tell "peel the tag to the commit it names" apart from "resolve to the branch tip", "resolve to the origin tip" or "resolve to the sandbox `HEAD`". In the row's sandbox, all four are the same commit, `tip`.

A consumer-local mutant (M1, below) is predicted to pass this row, the nested row, the whole old matrix and the consumer's own selftest. On real input it would report the wrong revision and read the wrong record and snapshot bytes, while exiting 0.

## Observations (from the frozen source)

### O1. Bind and argv propagation (A1)
- `main` passes `args.revision` and `args.branch` unchanged to `load` (`measure-update-recheck.py:758-760`).
- `load` calls `_revision.bind(ROOT, rev, branch)` (`:476`). The result's `binding.sha` is used for both `read_git` calls (RECORD and SNAPSHOT) and becomes the payload `revision` (`:480-481`, then `:777`, then `emit` at `:416`).
- `ROOT` is `Path(__file__).resolve().parents[1]` (`:37`). When the judge runs `sandbox/tools/measure-update-recheck.py` (`check-revision-binding.py:362`), `ROOT` is therefore the sandbox clone.

### O2. Error and exit propagation (A2)
- A `RevisionError` is rewrapped as `Cannot(fid, site, detail, revision=rev, tip=branch_tip)` (`:477-479`).
- `main` then emits one `CANNOT_EVALUATE` finding with exit 2 (`:769-772`).
- Success paths are `ABSENT` with exit 0 (`:761-762`) and `COUNTED` with exit 0 (`:776-778`). Any record finding gives exit 2 (`emit` at `:434`). There is no exit-1 path.

### O3. Binder behaviour for an annotated tag that points at a commit (A3)
- `_revision.bind` validates the branch first, then checks the selector against the 7–64 hex pattern (`_revision.py:174-176`).
- `_object_commit` (`:119-145`) then runs four steps: `--disambiguate` must return exactly one object; `cat-file -t` returns `tag`; `rev-parse <oid>^{commit}` peels it; the result is the full commit SHA.
- Two ancestry checks follow: against the local branch (`:184`) and, when an origin ref exists, against origin (`:188-190`).
- The selector and the payload `revision` therefore come out as the full SHA of the tagged commit [PREDICTION].

### O4. The typed object is real and built independently (A4)
- `target_type_probes.tag()` runs `git tag -a` with the judge's own `git()` and resolves `ref^{tag}`, so the result must be a tag object (`check-revision-binding.py:685-695`).
- `commit_tag = tag("commit", tip)` (`:697`), and the row is `"annotated_tag_to_commit": (commit_tag, tip)` (`:703`).
- The expected commit `tip` comes from the judge's own independent `bind` and `object_commit`, which return the full object ID (`:742`, `:139-166, 192-208`).

### O5. How acceptance is graded
- `accepted()` passes when exit is not 2 and the payload `revision` equals `expect_sha`, compared case-insensitively (`:396-404`).
- It does not check `status`, `findings`, `branch_tip`, or the bytes that were read.
- Selectors tested: the full tag object ID, plus the shortest unique prefix of 7 to 39 characters (`:710-718`).

### O6. Sandbox and prefix sanity (A6)
- `target_type_measure` makes one `TemporaryDirectory` clone per run (`:743-746`) and reuses it for all nine tools in turn (`:763-764`).
- Tag names are unique per tool (`:686`), with an existence guard (`:688-689`). Tag refs are deleted in `finally` (`:734-736`), but the tag objects stay in the object store.
- The object inventory is taken after all five fixture objects exist (`:705-707`), so prefix uniqueness counts leftovers from earlier tools. The ref-collision guard checks `refs/heads/` and `refs/tags/` only. That is enough here, because the consumer resolves object IDs only (`--disambiguate`).
- Freshness is per measurement, not per row. No defect in this part.

### O7. Host reads (A7)
Binding uses the sandbox repository only. `_revision.clean_env()` sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` (`_revision.py:62-66`).

The consumer's own `git()` is different:
- It strips **every** `GIT_*` variable it inherits, including the two isolation variables the judge sets (`check-revision-binding.py:100-104`, `362-366`).
- It re-adds only `GIT_OPTIONAL_LOCKS`, `GIT_PAGER` and `LC_ALL` (`measure-update-recheck.py:437-439`).

So the accepted-path `git show <sha>:<path>` (`:450`) reads the host's system and global git config, via the inherited `HOME`. This is a host config-file read, not a host-state probe: no pacman/stat/grep is run (agrees with CritNoHarm H2). It applies to every accepted cell, so it is continuity rather than something specific to this row. Severity is low. Whether it changes any output depends on the host's git config [INFERENCE].

### O8. The tag target equals the branch tip, the origin tip and HEAD (A5)
In `target_type_measure`, `prepare()` checks out `tip` detached, sets `refs/heads/<branch>=tip` and recreates `refs/remotes/origin/<branch>=tip` (`:233-242`). Unlike `measure()` (`:802`), it never calls `probe_commit`, so the sandbox `HEAD` stays at `tip`.

Both accepted target-type classes expect `tip`: `annotated_tag_to_commit` (`:703`) and `nested_tag_to_commit` (`:702`). The old matrix's tag cases also all point at `tip` (`:505`, `:631-632`, `:616-626`). No probe anywhere accepts a tag, or a short prefix, that names a landed commit other than the tip. The only non-tip accepted selector is `landed-parent`, which is the full 40-hex parent (`:427`).

## Mutants (proposed, NOT executed)

### M1. Consumer-local false-green
The edit is in `measure-update-recheck.py:480-481`. Replace `binding.sha` with:

`sha = binding.sha if binding.sha == rev.lower() else binding.branch_tip`

Use `sha` for the returned revision and for both `read_git` calls.

Predicted outcomes [PREDICTION]:

| Probe | Selector | Mutant resolves to | Expected | Outcome |
|---|---|---|---|---|
| `annotated_tag_to_commit` | full tag object ID | `tip` (selector ≠ peeled SHA, so it falls back to `branch_tip`) | `tip` | survives |
| `annotated_tag_to_commit` | unique prefix | `tip` | `tip` | survives |
| `nested_tag_to_commit` | full ID and prefix | `tip` | `tip` | survives |
| tree, tag-to-blob, tag-to-tree rows | any | refused by `bind` before the mutant line | refusal | unchanged |
| Old `probe_tool` | `tip`, `short-tip`, `landed-parent` (full, equal), `origin-absent`; all refusals unchanged | as expected | as expected | survives |
| Old `object_selector_probes` | `uppercase_object` (`rev.lower()==tip`), `full_object_id`, `annotated_tag_object` and `annotated_tag_prefix`, `real_prefix_shadow_*`, `full_*_object_id_ref_shadow` | `tip` | `tip` | survives |
| Consumer selftest `landed-tip-accepted` | full `tip` | `tip` | `tip` | survives |
| `_revision` selftest | n/a | binder bytes unchanged | n/a | survives |

Real-world effect: `--revision <annotated tag pointing at an older landed commit>`, or a short prefix of an older commit, exits 0. It reports `revision = branch tip` and measures the RECORD and SNAPSHOT bytes from the tip instead of the requested commit. That is a wrong-revision measurement reported as green.

### M2. Row-local weakness, killed by companion checks
The edit is in `_revision.py:139-140`: peel `HEAD^{commit}` instead of `{oid}^{commit}`.
- The target-type `annotated_tag_to_commit` and `nested_tag_to_commit` rows would pass, because `HEAD` is `tip` in this sandbox (O8).
- It is killed by the old matrix's `annotated_tag_object`, because in `measure()` the `HEAD` is the unlanded probe commit (`:802`), giving NOT-LANDED.
- It is also killed by `_revision` selftest `annotated-tag-full-object-id` (`_revision.py:227-228`, `:360`).

So M2 is not an end-to-end false-green. It does show that the new row adds no kill power of its own.

### Smallest discriminating control (recommendation to L1, not implemented)
Within the new matrix only, so the old matrix stays unchanged, add an accepted class with a tag to the landed non-tip parent (`tip^1`), expecting `parent`. Exercise it with both the full tag object ID and a unique prefix. Optionally also add a unique short prefix of `parent`. Under M1 this cell returns `tip` instead of `parent` and fails. It requires a landed parent, like `object_selector_probes` (`:476-478`).

## Continuity (commit-tag is not new coverage)
- `annotated_tag_to_commit` repeats the round-20 `annotated_tag_object` and `annotated_tag_prefix` cases (`:631-632`): same target `tip`, same full and unique-prefix selector shapes, same `accepted()` grader. This agrees with ConnPlanner O2 and CritBaseline.
- Every mutant this row kills is predicted to be killed by the old pair as well. The reverse is false: M2 is killed by the old pair but not by this row. The row is continuity only, and is slightly weaker than the old pair because of its sandbox `HEAD`.
- Build oracle: none exists for this consumer × AnnotatedTag. The fan-out covers Tree, TagBlob, TagTree and NestedTag only (`ConnPlanner.md:29`). `Oracle05NestedTag.md:24-31` predicts exit 0 and `revision` equal to the full commit for the single-level case, which agrees with O3. Its "Smallest mutant" section (§5) does not cover the tip-equality blind spot.
- Old matrix: the pinned snapshot has `object_selector_probes` at line 475 and `annotated_tag_object` / `annotated_tag_prefix` at 631-632. These are the same positions as in the candidate, which is consistent with the old matrix being unchanged. This was a grep of line positions, not a byte diff [LIMIT].
- C2 `target_type_mode` 0→1 is an AST presence census of functions and options (`:750-759`, `:780`). It is not a behavioural uplift, and it is not a ninefold increase.

## Limits
- Everything here is a source-only prediction. Git semantics (`^{commit}` peeling, `--disambiguate`, `git show` reading config) are as I understand them from the documentation [INFERENCE].
- Whether `RECORD` and `SNAPSHOT` exist at the lane tip (`ABSENT` vs `COUNTED` vs a findings-driven exit 2) is unresolved. Production files were not read. This affects all accepted cells equally and does not affect the M1 argument.
- No digests were recomputed. No test, mutant, selftest, install or subprocess was run. No production edit was made.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none
