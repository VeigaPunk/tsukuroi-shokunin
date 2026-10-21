# Fx06TagBlob — falsify check-boot-chain.py × tag_to_blob (candidate 0a14952b, source-only)

Reviewed-SHA256: 91312f103e694daafc95006fc0c083f6bfbe3abad03a2abed370f50e7ff22982
Predicate: check-boot-chain.py-tag_to_blob-candidate-control
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.

Primary file: `.ufo/waves/round-21/candidate/tools/check-boot-chain.py` (Reviewed-SHA256 above, taken from
`candidate-files.json`; not recomputed — NO-EXEC).
Auxiliary frozen snapshot dependencies (read, not bound by this receipt):
- `.ufo/waves/round-21/candidate/tools/_revision.py` — candidate-files.json sha256 `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf`
  (same digest Oracle06TagBlob reviewed for the round-21 snapshot binder ⇒ binder bytes unchanged baseline→candidate, by listed digest only).
- `.ufo/waves/round-21/candidate/tools/check-revision-binding.py` — sha256 `0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6`.
- Comparison oracle (context, not candidate): `.ufo/waves/round-21/build/Oracle06TagBlob.md`, `build/CritBaseline.md`;
  old-matrix comparison read from `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.

## Verdict

**No defect within this predicate.** The candidate tag_to_blob row for check-boot-chain.py independently builds a real
annotated tag whose target is a blob, grades exit 2 + exactly one `E-REVISION-INVALID` finding for both the full tag
OID and a unique prefix, in a fresh clone sandbox, and the consumer's refusal path performs no host read. Every
realistic consumer mutant I could construct that is wrong on tag→blob is killed by the row; the row-green mutants that
remain are either (a) right-answer-for-wrong-reason and killed by sibling rows of the same per-tool `behavior_ok`
conjunction, or (b) outside the graded contract (JSON `status`/`site`/`detail`), listed below as blind spots, not defects.
All outcomes below are **source predictions**, not observations; nothing was run.

## Axes
- A1 consumer bind/argv propagation
- A2 error → JSON/exit propagation
- A3 fixture independence and object-type truth
- A4 grading exactness (exit, id, count, accept SHA)
- A5 sandbox freshness / unique-prefix sanity / no host read
- A6 old-matrix invariance and C2 counting honesty
- A7 agreement with build oracle

## A1 — argv → bind (observed in source)
- Judge invocation `run_tool` (`check-revision-binding.py:359-371`): `[sys.executable, <sandbox>/tools/check-boot-chain.py,
  "--revision", <selector>, "--branch", "master"]` + `EXTRA["check-boot-chain.py"] == ()` (`:72`, `:77-78`), `cwd=sandbox`,
  `env=clean_env()` (`:100-104`: GIT_* stripped, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`).
- Consumer `build_parser` (`check-boot-chain.py:828-847`, `exit_on_error=False`): `--revision` in a required mutually
  exclusive group with `--selftest`; `--branch` default master. `main` (`:1554-1569`): no `--registry-from`, not selftest.
- `main` `:1570-1573`: `branch = args.branch`; `revision, branch_tip = "unbound", None`;
  `_revision.bind(ROOT, args.revision, branch)` with the argv string unchanged. `ROOT = Path(__file__).resolve().parents[1]`
  (`:57`) ⇒ the sandbox clone root. `import _revision` (`:54`) resolves via `sys.path[0] = <sandbox>/tools`, i.e. the
  `_revision.py` checked out at the measured tip by `prepare` (`check-revision-binding.py:233-242`, `checkout --detach tip`).
  `sys.dont_write_bytecode = True` precedes the import (`:53`) ⇒ no `__pycache__` write into the sandbox.
- The consumer has no local selector regex or resolver; all selector semantics are the shared binder's.

## A2 — binder path and error propagation for tag→blob (predicted)
`_revision.bind` (`_revision.py:172-192`):
1. `validate_branch("master")` passes (`:84-95`).
2. `REV` 7-64 hex passes for the 40-hex tag OID and for its ≥7-hex unique prefix (`:41`, `:175`).
3. `_object_commit` (`:112-146`): `rev-parse --disambiguate=<sel.lower()>` → exactly one OID (the tag) → `cat-file -t` →
   `tag` → `rev-parse --verify --quiet --end-of-options <oid>^{commit}` fails (peel chain ends at a blob) →
   `rev-parse --git-dir` succeeds → `None`.
4. `bind` raises `RevisionError(E-REVISION-INVALID, "revision", "<sel> does not name one commit")` (`:177-179`);
   branch/ancestry/origin steps are never reached, so origin state is irrelevant.

Consumer (`check-boot-chain.py:1578-1584`): wraps as `Finding("E-REVISION-INVALID", "revision", detail)`; not
`--statement-corrections` ⇒ `emit(Result(CANNOT, [finding], 0, 0), "unbound", "master", None)`. `emit` (`:785-798`) prints one
sorted-keys JSON line, `status "CANNOT_EVALUATE"`, `revision "unbound"`, `branch_tip null`, counts 0, one finding, and returns
2 ⇒ `sys.exit(2)` (`:1639-1640`). Git stderr from the failed peel is captured by `_revision._git` (`:69-77`), not printed.
`read_git` (`:814-824`) is never reached on this path.

## A3 — fixture independence (observed in source)
`target_type_probes` (`check-revision-binding.py:676-736`):
- `blob = blob_object(sandbox)` (`:408-413`, `git hash-object -w --stdin` of fixed bytes) — a real blob written to the sandbox.
- `tag("blob", blob)` (`:685-695`, `:700`): `git tag -a r21-target-check-boot-chain-blob -m blob <blob>` with hooks disabled,
  gpg off, isolated config; returns `rev-parse --verify refs/tags/<name>^{tag}` — guaranteed to be a tag object.
  The tag name embeds the consumer name ⇒ a distinct tag object per consumer.
- `expected_commit = None` ⇒ refusal row. The expected result is a type constant (a tag whose header `type` is `blob` can
  never peel to a commit), not derived from running the binder; the judge's own `object_commit` copy (`:139-166`) is not
  invoked in this row.
- Limit: the row trusts `git tag -a` for the target type; it does not itself assert `cat-file -p <tag>` header
  `type blob` (the oracle's "permitted fixture sanity"). Predicted harmless: a wrong target (e.g. a failed/empty blob id)
  makes `git tag` fail and `must()` raise `E-SANDBOX`, it cannot silently retarget.

## A4 — grading exactness (observed in source)
For each selector of `tag_to_blob` (`:710-729`):
- `refused(..., ID_INVALID, "master")` (`:383-393`): `ok = exit == 2 and first finding id == E-REVISION-INVALID`;
  then `:723-725` additionally requires `binding_ids == ["E-REVISION-INVALID"]` and `finding_count == 1`.
- Case `ok = all(observations ok)` (`:730-732`) over the full OID and the unique prefix.
- Per-tool `behavior_ok` requires all five classes ok (`:765`).
Predicted for the candidate consumer: both observations `exit 2`, `finding E-REVISION-INVALID`, `binding_ids [E-REVISION-INVALID]`,
`finding_count 1`, `json_revision "unbound"` ⇒ row ok.

## A5 — sandbox, prefix, host read
- Fresh sandbox: `target_type_measure` (`:739-781`) makes a new `TemporaryDirectory("tsukuroi-target-types-")`, `clone_lane`
  (`--no-hardlinks --no-tags`, no alternates), `prepare` (origin remote removed, `refs/heads/master` and
  `refs/remotes/origin/master` := tip), `materialize`. One sandbox is shared by the nine consumers in order; check-boot-chain
  is the sixth (`TOOLS`, `:61-80`), so tag objects left by the five earlier consumers persist (refs deleted in `finally`
  `:734-736`, objects not). Predicted harmless: prefix uniqueness is recomputed against the full post-fixture inventory.
- Unique prefix sanity: inventory is `cat-file --batch-all-objects` taken after all five fixture tags exist (`:705-707`);
  prefix = shortest width in `7..39` with exactly one inventory match and no `refs/heads/<p>` / `refs/tags/<p>` (`:712-718`);
  absent ⇒ `E-SANDBOX`, never a silent skip. The consumer resolves objects before refs (`--disambiguate`), so other ref
  namespaces cannot shadow. The full OID is always also probed.
- No host read on this path: consumer git calls run `-C <sandbox>` under `_revision.clean_env` (system/global config
  suppressed); the refusal returns before any `read_git`. Only Python's own interpreter/site start-up touches host files
  (not a git/lane read) [INFERENCE].

## A6 — old matrix and C2 counting
- Old matrix unchanged: the `object_selector_probes` case keys and line numbers in the candidate (`:526-666`) are identical to
  the snapshot (`snapshot/tools/check-revision-binding.py:526-666`); `measure()` (`:783-880`) never calls
  `target_type_probes`; `main` refuses `--object-selectors` together with `--object-target-types` (`:1391-1395`); the type mode
  uses its own sandbox, so it cannot perturb old-matrix prefix inventories (addresses CritBaseline's hazard).
- Counting: `target_type_mode = int(available)` is one AST fact about the measured judge (`:748-761`, `:773`), counted once;
  `target_type_tools` / `behavioral_tools` is the behavioral count. Because the binder digest is identical baseline→candidate,
  this consumer's tag_to_blob behavior is predicted green at baseline too: the row is **new coverage (new matrix cell) with
  zero behavioral delta**. C2 mode 0→1 must not be read as a nine-fold behavioral uplift.
- Commit-tag continuity (not new coverage): `annotated_tag_to_commit` (`:703`) re-covers old `annotated_tag_object`
  (`:631`); it is the sibling row that kills the "refuse every tag" mutant below.

## A7 — comparison with build oracle (Oracle06TagBlob)
- Agreement: oracle expects exit 2, one finding `E-REVISION-INVALID`, for full ID and unique prefix, independent of origin —
  matches A2 and the candidate grader.
- Oracle's named mutant (`^{commit}`→`^{}` generic peel in `_object_commit`): blob OID becomes `sha`; `merge-base
  --is-ancestor <blob> refs/heads/master` exits ≥2 ⇒ `E-GIT-FAILED` [INFERENCE: git behavior]. Candidate row grades the id
  ⇒ **killed** (`found != want`). The selftest stub `target-generic-peel` (`:981-989`) models this mutant, but its witness
  (`:1246-1258`) asserts only `tag_to_tree` individually plus the aggregate; tag_to_blob's kill is not individually witnessed.
- Oracle fields the candidate does **not** grade: `status`, `revision == "unbound"`, `branch_tip == null`, finding `site`,
  finding `detail`, single-line stdout (`parse_json` falls back to the last `{` line, `:322-337`).

## Mutants considered (proposed, NOT executed; outcomes predicted)
| mutant (location) | tag_to_blob row | caught by |
|---|---|---|
| generic peel `^{}` (`_revision.py:139-140`) | fails (E-GIT-FAILED) | this row |
| tag→blob peel failure raised as E-GIT-FAILED (`_revision.py:143-146`) | fails | this row |
| consumer exits 1 instead of 2 on RevisionError (`check-boot-chain.py:1584`) | fails | this row |
| double finding on refusal | fails (count 2) | this row |
| fallback to branch tip when peel fails | fails (exit ≠ 2) | this row |
| drop tag branch: `if object_kind != "commit": return None` (`_revision.py:134-137`) | green (right answer, wrong reason) | `annotated_tag_to_commit`, `nested_tag_to_commit`, old `annotated_tag_object` |
| hard-code consumer `ROOT` to the host lane (`check-boot-chain.py:57`) | green (fixture tag unknown on host ⇒ INVALID) | accepted rows (tag objects absent on host ⇒ refused) |
| `emit` maps CANNOT → `"PASS"` status, exit still 2 (`check-boot-chain.py:786`) | green | **nothing in the judge** — outside graded contract |
| refusal finding `site`/`detail` altered | green | nothing — outside graded contract |

The `status`-field mutant is a real blind spot of every refusal row, but SCORECARD (`candidate/SCORECARD.md:561`) declares
refused payloads diagnostics, never certificates, and the consumer's contract is the exit class; I record it as a predicate
limit, not a defect within `check-boot-chain.py-tag_to_blob-candidate-control`.

## Out-of-predicate observation (for commit-tag / nested seats)
On accepted paths the consumer's own `git()` (`check-boot-chain.py:801-811`) strips all `GIT_*` including the judge's
`GIT_CONFIG_GLOBAL=/dev/null` and does not re-add `GIT_CONFIG_NOSYSTEM`/`GIT_CONFIG_GLOBAL`, so `read_git` would read host
`/etc/gitconfig` and `~/.gitconfig` [INFERENCE]. Not reached on tag_to_blob (refusal returns at `:1584`).

## Limits
- All exit/finding outcomes are source predictions plus documented git semantics; none observed.
- Digests come from `candidate-files.json`; not recomputed.
- No non-author closure or outside promotion is claimed. Prior source-only oracles are not outside closure.
- Tooling: none installed or updated (NO-EXEC seat; none needed).

Scope: executed=none
