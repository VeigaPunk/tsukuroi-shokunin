# Fx03TagBlob — falsify: check-section-citations.py × tag_to_blob (candidate control)

Reviewed-SHA256: 1546d80403aa912e8f5b21710a85195e973216c120ec94457cfe5574c403aac3
Predicate: check-section-citations.py-tag_to_blob-candidate-control
Lane bounds: leaf member — no subagent dispatch.

Primary file: `.ufo/waves/round-21/candidate/tools/check-section-citations.py` (candidate
revision 0a14952b59d20179e1c813af58befaecd6992a17; digest as declared in
`.ufo/waves/round-21/candidate-files.json`, not recomputed — NO-EXEC).
Auxiliary snapshot dependencies (read only, digests from the same inventory, not bound by the
primary receipt):
- `candidate/tools/_revision.py` — 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
- `candidate/tools/check-revision-binding.py` — 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6
- comparison only: `snapshot/tools/check-revision-binding.py` (preregistered da000de4…) and
  build oracle `build/Oracle03TagBlob.md`.

## Axes
1. Exit class (0/1/2).
2. Finding identity and cardinality.
3. Full-SHA / echo semantics of the JSON `revision` / `branch_tip` fields.
4. Fixture integrity (actual typed object, fresh sandbox, unique-prefix sanity, no host read).
5. Mutant sensitivity of the new row; old-matrix preservation; C2 metric meaning.

## Observed — consumer bind/argv/error/output propagation (candidate consumer)
- L36 `from _revision import RevisionError, bind`; `sys.dont_write_bytecode = True` precedes it
  (L35). No local `{7,64}` regex, no `cat-file`/tag/blob logic in the file.
- L38 `ROOT = Path(__file__).resolve().parents[1]` — the repo holding the tool file. Under the
  judge, that is the sandbox clone (tool path `sandbox/tools/<name>`, judge L362).
- `main` L899–916: argparse (`--revision` / `--selftest` mutually exclusive, `--branch`
  default `master`); `branch = args.branch`; `revision, branch_tip = args.revision, None`;
  `bind(ROOT, args.revision, branch)` — argv passed verbatim, no normalization.
  `bind(ROOT, BASE, branch)` and every `read_git` run only after the revision bind returns.
- L923–927: `RevisionError` → `Cannot(exc.fid, exc.site, exc.detail)` →
  `emit(Result(CANNOT, [one Finding], 0), revision, branch, branch_tip)`; `revision` is still
  the raw selector and `branch_tip` still `None`. L928–930: other exceptions → `E-INTERNAL`.
- `emit` L394–402: one JSON line `{status, revision, branch, branch_tip, correction_count,
  scope, findings[{id,site,detail}]}`; returns `result.code`; L939 `sys.exit(main())`.
- The consumer `--selftest` has no tag, tag-to-blob or tree vector (L801–881: only
  invalid/short/range/HEAD/@/@-/ref selectors, branch validation, landed/unlanded/unpushed).

## Observed — binder path for an annotated tag whose target is a blob (`_revision.py`)
`bind` L172–179: `validate_branch("master")` passes → `REV` (L41) passes for a full OID or a
≥7-hex prefix → `_object_commit` L112–146: `rev-parse --disambiguate=<lower>` (objects only,
no refs) → exactly one OID → `cat-file -t` = `tag` → `rev-parse --verify --quiet
--end-of-options <oid>^{commit}` fails → `rev-parse --git-dir` succeeds → `None` → L179
`RevisionError(E-REVISION-INVALID, "revision", "<rev> does not name one commit")`. Branch
existence, landed and pushed checks (L180–191) are never reached. The binder's own selftest
L413–419 asserts `annotated-tag-to-blob-invalid` by calling `bind()` directly, not through any
consumer.

Source prediction (NOT observed by execution): for both the full tag OID and its unique
prefix, the consumer exits 2 and prints one JSON line with `status` `CANNOT_EVALUATE`,
exactly one finding `E-REVISION-INVALID` / site `revision`, `revision` = the selector as
typed, `branch_tip` null, `correction_count` 0. That matches build oracle
`Oracle03TagBlob.md` §Expected on every axis.

## Observed — candidate `target_type_probes` row `tag_to_blob` (judge L676–736, L739–780)
- **Actual typed object, created independently.** `blob_object` (L408–413) writes a fresh blob
  through `git hash-object -w --stdin`. `tag("blob", blob)` (L685–695) runs `git tag -a
  r21-target-check-section-citations-blob -m blob <blob>` (the name comes from
  `name[:-3]`), then reads the tag object with `rev-parse --verify refs/tags/…^{tag}`. Neither
  step imports or calls the binder under test. Limit: the judge confirms the object is a tag
  (`^{tag}`) but never asserts `cat-file -p` shows `type blob`. The blob type follows from
  how the tag was built. A wrong fixture would only make a correct consumer fail (red), so it
  cannot produce a false green.
- **Exact refusal ID and count.** L721–725: `refused(..., ID_INVALID)` requires `exit == 2`
  and first finding id `E-REVISION-INVALID` (L383–393). The row then also requires
  `binding_ids == ["E-REVISION-INVALID"]` and `finding_count == 1`. Because
  `expected_commit is None`, no acceptance path exists for this class. An accept requires
  exit ≠ 2 (L396–404), so the two outcomes cannot be confused.
- **Selectors.** Two selectors are tried: the full tag OID, and the shortest prefix of width
  7–39 (L712) that is unique across the full post-creation object inventory (L705–707, read
  after all four tags exist) and has no `refs/heads/<p>` or `refs/tags/<p>` collision.
  `E-SANDBOX` is raised if no such prefix exists. There is no uppercase variant.
- **Fresh sandbox.** `target_type_measure` makes one `TemporaryDirectory`, then runs
  `clone_lane` (`--no-tags --no-hardlinks`), `prepare` (detached checkout at tip,
  `refs/heads/<branch>` = tip, origin remote removed, only the tracking ref recreated at tip)
  and `materialize`. The sandbox is fresh per measure run, not per tool: all nine tools share
  one clone. Each tool's tag refs are deleted in `finally` (L734–735), but the unreachable tag
  objects stay in the object store, and section-citations is third in `TOOLS` (L64). This is
  harmless for this row because the prefix inventory includes those leftover objects.
  `_revision.py` reaches the sandbox through the clone checkout at tip, not through
  `materialize`, which writes `TOOLS` only.
- **No host read on this row's path.** The judge's git calls use `clean_env`
  (`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`) and `core.hooksPath=/dev/null`.
  `run_tool` uses `cwd=sandbox` and `env=clean_env()`. Inside the consumer, refusal touches
  only `_revision._git` / `validate_branch`, which apply the same `clean_env`. The consumer's
  own `git()` (L405–414) is never reached on this path. [INFERENCE] `GIT_CONFIG_GLOBAL` also
  suppresses `$XDG_CONFIG_HOME/git/config`. Limit: Python's own startup reads (stdlib, user
  site-packages) are not isolated. Only `GIT_*` is scrubbed, as the judge's trust-boundary
  docstring states.

## Comparison with the build oracle (Oracle03TagBlob)
The oracle and the row agree on exit 2, a single `E-REVISION-INVALID`, and count 1. The row
does not grade the oracle's full-SHA/echo axis: `site`, `detail`, the `status` string,
`revision` echoing the selector byte-for-byte, `branch_tip` being null, and
`correction_count` 0. This weakening is declared, not hidden. Judge L481–483 explicitly treats
a CANNOT `revision` echo as not being a binding, and the old matrix's
`object-selector-cannot-revision-echo` selftest expects PASS. Consequence: a consumer mutant
that puts a full commit SHA, such as the lane tip, into `revision` or `branch_tip` on the
CANNOT path still passes this row.

## Mutants (proposed, NOT executed)
- **Generic-peel mutant, killed by this row (prediction).** In `_revision._object_commit`
  L140, change `^{commit}` to `^{}`. The tag then yields the blob OID, and
  `merge-base --is-ancestor <blob> refs/heads/master` exits ≥ 2 ([INFERENCE]) → `E-GIT-FAILED`.
  Exit 2 is preserved, but the id differs, so the exact-id check rejects it. The candidate
  selftest witness (L1239–1259, stub L986–989) records this kill only for `tag_to_tree`. The
  `tag_to_blob` kill is predicted, not witnessed.
- **Ref-fallback mutant, survives this row and both matrices (adjacent gap).** In
  `_revision._object_commit` L141–146, when the tag peel fails, `return _commit(repo,
  revision)` instead of `None`. This adds a ref-alias fallback that violates the contract that
  refs are never a fallback.
  - Full tag OID: Git prefers a full 40-hex object over a ref ([INFERENCE]). The peel still
    fails → `None` → `E-REVISION-INVALID`.
  - Unique prefix: the judge guarantees no ref of that name exists → `None` →
    `E-REVISION-INVALID`.
  - So both `tag_to_blob` selectors stay ok.
  - Old matrix: ghost selectors match no object; shadow, unlanded and tag-shadow cases all
    resolve to commits or peelable tags, so they never reach the failed-peel branch. The other
    new rows peel successfully. The binder selftest `annotated-tag-to-blob-invalid` has no
    ref shadow.
  - Observable effect: with `refs/heads/<tag-to-blob prefix>` pointing at a landed commit, the
    consumer would bind that commit, evaluate it, and exit 0 or 1 with `revision` = that
    commit. Short-hex refs win in Git's resolution ([INFERENCE]).
  - Classification: this is outside the row's declared predicate. The row's unique-prefix
    sanity deliberately excludes ref collisions, so this is not a grading defect of the row.
    It is an unclosed tag-to-noncommit × ref-shadow cell.
- **Consumer mutant "reject every tag object".** It passes `tag_to_blob` but is killed by
  `annotated_tag_to_commit` and `nested_tag_to_commit`. A single row cannot tell whether a
  refusal happened for the right reason; the class set can.

## Old matrix, commit-tag continuity, and what the C2 metric means
- Old matrix: candidate `probe_tool`, `object_selector_probes` (L416–673) and `measure`
  (L783–883) have the same function layout and case keys as the preregistered snapshot (L416,
  L475, L676). The `measure` bodies read identical. This is visual review only, not byte
  proof. The new mode is a separate opt-in (`--object-target-types`, L924), and
  `--object-selectors` with `--object-target-types` → `E-CLI` (L1392–1395).
- `annotated_tag_to_commit` and `nested_tag_to_commit` continue the old matrix's
  `annotated_tag_object` / `annotated_tag_prefix` acceptance of tags that point at commits.
  They preserve continuity and are not new coverage.
- `_revision.py`'s candidate digest equals the preregistered snapshot digest (06b71e8…), so the
  binder is unchanged and `tag_to_blob` refusal behaviour already existed for this consumer.
  The C2 count going from 0 to 1 means the mode became available (`target_type_mode` =
  `int(available)`, L758–773). The selftest expects mode 0 with tools = TOTAL for a judge
  without the mode (L1251–1254). This is not a behavioural uplift across the nine tools.

## Adjacent observation (outside this predicate)
The accept rows (`nested_tag_to_commit`, `annotated_tag_to_commit`) do read host git config.
The consumer's `git()` (L405–407) copies `os.environ`, drops every `GIT_*` key (including the
judge-supplied `GIT_CONFIG_NOSYSTEM` and `GIT_CONFIG_GLOBAL`), and does not add them back. So
`read_git` (L417) in those rows reads the host's `/etc/gitconfig` and `~/.gitconfig`
([INFERENCE] from the code; not observed). The `tag_to_blob` row never reaches `read_git`.

## Verdict
No defect within this predicate. The row builds a real tag-to-blob object independently,
requires exit 2 with exactly one `E-REVISION-INVALID`, uses a fresh per-run sandbox, takes a
prefix that is unique with no ref collision, and its refusal path reads no host git config. It
is weaker than the oracle on the echo/full-SHA axis by declared design. The ref-fallback mutant
is a concrete survivor that sits just outside the row's scope. No non-author closure or
outside promotion is claimed.

Tooling: none installed or needed (NO-EXEC seat).

Scope: executed=none
