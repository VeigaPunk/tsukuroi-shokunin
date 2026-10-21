# Fx09Nested — check-seat-scope.py × nested_tag_to_commit (candidate control row)

Axes: (a) does the consumer's frozen bind path actually peel a tag→tag→commit object to the
expected full commit SHA; (b) does the row exercise both full-OID and unique-prefix selectors
against a real typed object in a fresh sandbox; (c) can anything read the host lane instead of
the sandbox; (d) does the row's acceptance criterion catch identity/echo and refusal-shape
mutants, or only type classes.

All statements below are source-derived predictions from frozen snapshots; nothing was executed.
Auxiliary snapshot dependencies (predispatch digests from candidate-files.json):
`tools/_revision.py` SHA256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf,
`tools/check-revision-binding.py` SHA256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6,
both at candidate revision 0a14952b59d20179e1c813af58befaecd6992a17.

## 1. Consumer bind/argv/error/output propagation (frozen source)

- `check-seat-scope.py:36` imports `RevisionError, bind as bind_revision` from `_revision`.
  `sys.path[0]` is the script's own directory, so under the judge it resolves to the
  sandbox copy `sandbox/tools/_revision.py`, not a host file (inference from Python import
  semantics; the file is checked out into the sandbox clone at `sandbox/tools/_revision.py`
  by `prepare`, judge:233-242).
- argv built by `run_tool` (judge:359-371):
  `sys.executable sandbox/tools/check-seat-scope.py --revision <selector> --branch master
  --wave .ufo/waves/round-16/build`, `cwd=sandbox`, `stdin=DEVNULL`, `env=clean_env()`
  (judge:100-104 strips all `GIT_*`, sets `GIT_CONFIG_NOSYSTEM=1`,
  `GIT_CONFIG_GLOBAL=/dev/null`, `LC_ALL=C`, `GIT_OPTIONAL_LOCKS=0`).
- Tool parse path: `build_parser` (check-seat-scope.py:226-238) makes `--revision` one of a
  required mutually-exclusive group; `args_issue` (241-247) requires `--wave` for
  non-selftest; `wave_key` (186-193) keeps `.ufo/waves/round-16/build` lane-relative.
- `collect` (258-278) with `revision is not None` calls `bind_revision(root, revision,
  branch)` where `root = ROOT = Path(__file__).resolve().parents[1]` (line 39) — inside the
  sandbox this is `sandbox/`, so every `git -C` targets the throwaway clone, never the lane.
- Frozen `_revision.bind` (frozen _revision.py:172-192): `validate_branch` → `REV` 7-64 hex
  fullmatch → `_object_commit` (112-146): `rev-parse --disambiguate=<sel.lower()>` must yield
  exactly one object; `cat-file -t` yields `tag`; then `rev-parse --verify --quiet
  --end-of-options <oid>^{commit}` peels transitively tag→tag→commit and returns the tip
  commit SHA. Then `_commit(refs/heads/master)` = tip, `_ancestor(tip, refs/heads/master)`
  = true, `_exists(refs/remotes/origin/master)` true (judge `prepare` pins it at tip,
  judge:240-241) and `_ancestor(tip, remote)` = true → `Binding(sha=tip, branch_tip=tip,
  origin_tip=tip)`.
- Error propagation: any `RevisionError` becomes `Cannot(exc.fid, exc.site, exc.detail)`
  (check-seat-scope.py:263-264) → `main` (663-665) emits `CANNOT_EVALUATE`, exactly one
  finding, exit 2. A nested tag is never on a refusal path, so this row only needs the
  accept shape; refusal rows (tree/blob/tag-to-tree/tag-to-blob classes) rely on
  `E-REVISION-INVALID` raised at _revision.py:179 when `_object_commit` returns None
  (peel failure on tag→blob/tag→tree) — single finding, single binding id.
- Output propagation: `emit` (151-170) writes `"revision": sha` = the peeled full 40-hex
  tip commit SHA, `"branch_tip"`/`"branch"`, `"status"` `PASS`/`FAIL`, exit 0/1.
- Host reads: none on this path. All object access is `git -C <sandbox>` inside
  `_revision`/`git()` (check-seat-scope.py:173-183); the wave files are read via
  `git show <sha>:<wave>/<file>` from the sandbox object DB (`read_git`, 196-206).
  The lane is touched only by the judge's `clone_lane`/`bind` before sandboxing.

## 2. Row construction (target_type_probes, judge:676-736)

- Object is independently created: `commit_tag = tag("commit", tip)` creates a real
  annotated tag object T1→tip (judge:697); `tag("nested", commit_tag)` creates T2→T1
  (judge:702). Tag refs are `refs/tags/r21-target-check-seat-scope-commit` and
  `-nested`; `ref_exists` guards uniqueness and raises E-SANDBOX on collision (686-689).
- Fresh sandbox: `target_type_measure` (739-780) uses `tempfile.TemporaryDirectory`
  + `clone_lane` (`git clone --no-hardlinks --no-tags`, judge:218-230) + `prepare`
  (detached checkout at tip, `refs/heads/master`→tip, origin removed then
  `refs/remotes/origin/master`→tip). Refs created by the probes are deleted in
  `finally` (734-736).
- Selectors per class: full object id plus, for non-tree classes, a prefix of width 7-39
  that is unique over the post-fixture `cat-file --batch-all-objects` inventory AND has no
  same-named `refs/heads/` or `refs/tags/` entry (judge:710-718). Uniqueness is computed
  after all four tag objects exist (705-707), so the prefix really is unique in the object
  DB the tool will disambiguate in.
- Expected value: `"nested_tag_to_commit": (nested_tag_oid, tip)` — the expected accepted
  commit is the full 40-hex tip, matching the independent oracle (below).
- Acceptance: `accepted` (judge:396-404) requires `exit != 2` AND the tool's JSON
  `revision` field equals `tip` (case-insensitive). Both selectors (full OID and unique
  prefix) get an observation; `cases[label]["ok"]` requires all observations ok (730-732).

## 3. Oracle comparison

The judge keeps an independent binder (`object_commit` judge:139-166, `bind` judge:192-208)
that mirrors the frozen `_revision` step-for-step: disambiguate → exactly one → `cat-file -t`
→ tag → `^{commit}` peel → branch commit → ancestor → optional origin ancestor. For a
tag→tag→commit object it likewise predicts the peeled tip SHA; the row's `expected_commit`
(hardcoded `tip`) agrees with both oracles. `_revision.py`'s own selftest constructs the
identical class (`nested-annotated-tag-object`, frozen _revision.py:362-365) expecting
`bind(...).sha == tip` — consistent expectation.

## 4. Mutant / false-green analysis within this predicate

- Killed uniquely by this row (not by `annotated_tag_to_commit`): a single-level peel
  mutant — e.g. in `_object_commit` replace `f"{oid}^{{commit}}"` with a one-step
  tag-target read, or a mutant that peels `^{}` once then requires type commit. On T2→T1
  the result is tag object T1, not a commit → `E-REVISION-INVALID` (exit 2) or emitted
  revision = T1 ≠ tip → `accepted.ok` False. This is the row's discriminating depth.
- Survives this row, killed by sibling rows: the `^{}`-generic-peel mutant (the judge's
  own `target-generic-peel` stub, judge:981-989). On tag→tag→commit, `^{}` still yields the
  tip commit, so both observations pass; the mutant is killed by `tag_to_blob`/`tag_to_tree`
  (`sha` becomes a blob/tree, `merge-base --is-ancestor` exits ≥2 → `E-GIT-FAILED` ≠
  `E-REVISION-INVALID`). The selftest models exactly this (judge:1244-1259).
- Survives this row, killed only outside this matrix: a mutant resolving
  `rev-parse --verify <selector>^{commit}` directly (ref names win over object ids). No
  branch/tag ref shadows these selector strings in this matrix, so the row cannot see it;
  the ref-shadow cases live in `object_selector_probes` (round-20 matrix), untouched here.
- Survives this row, killed by the old matrix: a "report branch tip instead of bound sha"
  mutant — `revision` echoes tip, accepted passes; `landed-parent`/`short-tip` in
  `probe_tool` distinguish it. Not this row's job.
- Structural observations, not defects: `accepted` treats exit 1 (FAIL with findings) the
  same as exit 0 — the row measures binding, not wave verdicts; `findings`/`counts` are not
  asserted on accept rows. `nonempty_tree` gets one selector (no prefix) — by design
  (judge:711). Sandbox-construction `Cannot` (e.g. no unique prefix) aborts the whole
  `target_type_measure` to CANNOT_EVALUATE, not a per-tool false FAIL.

## 5. Verdict

No defect within the predicate. The row is a correctly constructed control: it builds a
genuine tag→tag→commit object plus a unique-prefix twin in a fresh clone, expects exactly
the full 40-hex tip commit the consumer's frozen peel chain yields (`<oid>^{commit}` →
tip → `revision` field), requires exit ≠ 2 with the canonical SHA echoed, reads nothing
outside the sandbox, and preserves the commit-tag continuity already covered by the
round-20 `annotated_tag_object`/`annotated_tag_prefix` cases (new depth here is the nested
level, not the single tag→commit). Concrete false-greens exist for mutants outside this
row's contract (generic `^{}` peel, ref-name resolution, branch-tip echo) — each is killed
by sibling rows or the older matrices, so they are coverage boundaries, not holes in this
row. The old matrix is unchanged (`probe_tool` and `object_selector_probes` untouched by
this row), and `target_type_mode`/availability is gated separately
(judge:748-761, selftest 1251-1254), so C2 mode0→1 is not claimed as a behavioral 9-fold
uplift by the source.

Limits: all outcomes are source predictions; no test, mutant, or gate was run. Whether the
measured tip's tree actually contains `.ufo/waves/round-16/build/` does not affect the row
verdict (binding is resolved and echoed before wave reads; a missing wave yields
CANNOT_EVALUATE with `revision` still equal to tip, which `accepted` treats as failure —
[INFERENCE] the fixture lane presumably contains it, as probe-tool accept cases for the
same EXTRA args are expected to pass upstream).

Reviewed-SHA256: add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac
Predicate: check-seat-scope.py-nested_tag_to_commit-candidate-control
Scope: executed=none
