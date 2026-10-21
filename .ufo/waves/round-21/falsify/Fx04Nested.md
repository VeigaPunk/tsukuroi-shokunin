# Round 21 · Fx04Nested — falsify review
# Consumer: `check-source-scope-correction.py` × `nested_tag_to_commit`

Axes: **C1 depth** (nested annotated-tag decision and recursive terminal commit), **C2 operability** (real consumer invocation and exact result discrimination), **C3 calibration** (pinned primary bytes and exact predicate).

## Reviewed source identity and dependencies

Primary reviewed file:
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-source-scope-correction.py` — SHA-256 `931504455caae52eaa2f2018a826c1b40c1eed83025ec0f13d1127c66fb85afc`, revision `0a14952b59d20179e1c813af58befaecd6992a17` (`candidate-files.json`).

Auxiliary frozen candidate dependencies reviewed (not covered by the primary receipt):
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/_revision.py` — SHA-256 `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf` (`candidate-files.json`; also the preregistered snapshot digest).
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-revision-binding.py` — SHA-256 `0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6` (`candidate-files.json`).
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/snapshot/tools/check-revision-binding.py` — preregistered SHA-256 `da000de45b07ec2e4942ed798f6b9a7555c99180245d2139a94648cc4566b9e0` (`preregister.json`).

No source, judge, test, or mutant was executed. All outcome claims below are source predictions unless explicitly labelled otherwise.

## Findings (by severity)

### MEDIUM — `nested_tag_to_commit` can green a nested-tag-to-branch-tip substitution mutant

**Observed source facts.** Candidate judge `target_type_probes()` constructs `commit_tag = tag("commit", tip)`, then `tag("nested", commit_tag)`, so the tested object is a real tag→tag→commit chain (`check-revision-binding.py:685-704`). It sets `expected_commit` to `tip` for this class. `target_type_measure()` prepares the fresh clone with the measured commit at both the selected local branch tip and detached `HEAD` (`:743-746`; `prepare()` at `:233-242`). The full nested-tag object ID and a prefix are tested (`:709-718`). `accepted()` grades only `exit != CANNOT` plus JSON `revision == expected_commit` (`:396-404`).

**Concrete proposed mutant — NOT executed.** For a nested-tag selector, a consumer/binder could skip deriving the terminal commit and substitute the sandbox branch tip as the accepted `revision`/`Binding.sha`. Because this fixture’s terminal commit, branch tip, and `HEAD` are all `tip`, both nested-tag selectors would still satisfy the current accepted check. This is a false-green for the nested-tag row: it does not distinguish recursive resolution of the tag chain from a nested-tag-specific branch-tip fallback. The same identity also means the binder selftest’s nested-tag assertion (`_revision.py:362-365`) would not distinguish that particular fallback. The existing round-20 consumer rows exercise direct tag→tip, not nested tags, so they do not independently test a nested-only fallback.

**Why this is actionable.** The declared decision is to accept the terminal commit reached through nested tags, not merely to report the branch tip. A discriminating fixture would target an independently chosen landed non-tip commit (and require that exact full SHA), with branch tip/`HEAD` left distinct. Availability of such a parent commit in the measured revision was not checked here; no execution is proposed.

### LOW — Consumer-side Git config isolation is not preserved through the accepted path

**Observed source fact.** The judge launches the tool in the sandbox with `cwd=sandbox` and `env=clean_env()` (`check-revision-binding.py:359-371`; `clean_env()` at `:100-104` sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`). But the consumer’s `git()` rebuilds its environment by removing every `GIT_*` variable, then restores only `GIT_OPTIONAL_LOCKS`, `GIT_PAGER`, and `LC_ALL` (`check-source-scope-correction.py:354-363`). After binding, `read_git()` invokes `git show` for the document reads (`:366-376`, called at `:643`). Thus the consumer drops the judge’s Git-config isolation on this path.

**Limit / inference.** Git may then consult host system/global Git configuration even though repository reads resolve against the sandbox `ROOT`; this is a host-config read opportunity inferred from the environment construction, not an observed read. The sandbox does not point the consumer at the host repository, and no host config or repo was inspected. Therefore the requested “no host read” condition cannot be affirmed strictly for this consumer path.

## Consumer propagation and expected result (source-derived)

- Judge `run_tool()` passes `[python, sandbox/tools/check-source-scope-correction.py, --revision, selector, --branch, branch]`, with no `EXTRA` arguments for this tool (`check-revision-binding.py:77`, `:359-371`). The consumer computes `ROOT = Path(__file__).resolve().parents[1]` (`check-source-scope-correction.py:18`), so under this invocation the binder repository is the fresh sandbox.
- In `main()`, `--revision` calls `_revision.bind(ROOT, args.revision, branch)` (`check-source-scope-correction.py:614-643`). A `RevisionError` is wrapped and emitted as `CANNOT_EVALUATE` with one finding (`:640-641`, `:647-652`); on refusal, the requested selector remains the output `revision`. On success, the consumer uses `binding.sha` for `revision` and `binding.branch_tip` for the separate branch-tip field, then reads the five content paths from the bound commit (`:642-646`). `emit()` outputs the JSON payload (`:336-343`); content evaluation can exit 0 or 1, while the judge’s accept rule allows either but requires the exact accepted SHA.
- The frozen `_revision.py` requires one object from `rev-parse --disambiguate`, accepts commit objects directly, rejects non-tag/non-commit objects, and peels tags with `^{commit}` (`_revision.py:112-146`). `bind()` then checks ancestry of the peeled SHA against the requested branch and, if present, the origin tracking ref (`:172-192`). Source prediction for the generated nested tag is therefore acceptance with output revision equal to the underlying commit SHA, subject to those ancestry checks.
- Candidate `target_type_probes()` creates actual annotated tag objects with `git tag -a` and gets each tag object ID using `^{tag}` (`check-revision-binding.py:685-707`). It inventories objects after creating the fixtures and chooses a 7+-hex prefix only when unique in that object inventory and absent as a head/tag ref (`:705-718`). For `nested_tag_to_commit`, both full ID and unique prefix go through the real consumer CLI; each accepted observation must return the exact `tip` SHA (`:719-732`). This class is accepted, so an exact refusal ID/count does not apply. Refusal controls in the same matrix require exit `CANNOT`, the requested finding ID, and exactly one finding (`:722-725`).
- `target_type_measure()` creates a `TemporaryDirectory`, clones the lane, prepares a sandbox, and runs the cases there (`:739-747`, `:763-766`); tag refs created by the row are removed in `finally` (`:734-736`).

## Oracle comparison, continuity, and metric framing

- Exact-consumer build oracle: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/build/Oracle04NestedTag.md`. Its source-only expectation is the same: recursively peel the tag→tag→commit chain, accept only after ancestry checks, and report the exact terminal commit SHA. It records that the pinned old consumer matrix had no nested-tag consumer case, despite `_revision.py`’s own nested-tag selftest. The candidate matrix now constructs this consumer-level case. My false-green above is an additional discrimination limitation: the oracle expectation is terminal commit, but this fixture makes that commit identical to branch tip/`HEAD`.
- The candidate `probe_tool()` and `object_selector_probes()` blocks (`check-revision-binding.py:416-673`) match the corresponding frozen snapshot block (`snapshot/tools/check-revision-binding.py:416-673`) in the read ranges. The new target-type mode is a separate `target_type_measure()` dispatch (`candidate/check-revision-binding.py:739-781`, `:1391-1409`); the ordinary `measure()` path retains its separate `object_selectors` handling (`:783-883`). Thus the old matrix and its case set are unchanged in the reviewed source; nested-tag coverage is opt-in, not silently merged into the old mode.
- `annotated_tag_to_commit` also targets `tip` and overlaps the old direct annotated-tag→commit cases. It is continuity, not new coverage. The new nested-tag decision is the genuinely new depth case here.
- C2 mode availability and behavior are separate: the target-type mode’s AST availability is `target_type_mode`, while actual per-tool behavior is `target_type_tools`/`behavioral_tools` (`:750-779`). The 0→1 mode-availability transition is one explicit mode becoming available, not a ninefold behavioral uplift; the preregistration says to preserve the round-20 matrix (`preregister.json:21-34`).

## Residual risk and verification gaps

- The MEDIUM false-green is limited to this predicate/fixture identity. Other old-matrix rows may expose a global branch-tip substitution when a landed parent is available, but I did not establish that precondition for this candidate revision. A nested-only fallback remains untested by the old consumer matrix.
- The LOW host-config issue is source-derived; no host configuration was read, and no claim is made that its values change this result.
- All Git semantics, consumer outcomes, and mutant outcomes remain predictions: no command, consumer, test, or mutant was run. No non-author closure or outside promotion is claimed.
- Tooling: no tools were installed or updated; none was needed.

Reviewed-SHA256: 931504455caae52eaa2f2018a826c1b40c1eed83025ec0f13d1127c66fb85afc
Predicate: check-source-scope-correction.py-nested_tag_to_commit-candidate-control
Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none