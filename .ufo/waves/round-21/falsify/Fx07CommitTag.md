# Fx07CommitTag — check-freshness-r17.py × annotated_tag_to_commit (falsify, source-only)

Reviewed-SHA256: 836ade1b23ed459b922d8c680d2bbbb87d7abb4e6af7c84265e2ab1cffa01668
Predicate: check-freshness-r17.py-annotated_tag_to_commit-candidate-control

Candidate revision 0a14952b59d20179e1c813af58befaecd6992a17. The primary file is the frozen
`.ufo/waves/round-21/candidate/tools/check-freshness-r17.py` (SHA256 above, matching
`candidate-files.json:59-63`). Auxiliary frozen snapshot dependencies were read but are not
bound by this receipt:
- `candidate/tools/_revision.py`, sha256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf (`candidate-files.json:64-68`)
- `candidate/tools/check-revision-binding.py`, sha256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6 (`candidate-files.json:39-43`)

I read no live or draft tool for the verdict. The build-oracle comparison uses
`build/Oracle07NestedTag.md`, `build/CritBaseline.md` and `build/ConnPlanner.md`.

## Axes

- **A1 Resolution**: a tag-object selector, as a full ID or a unique prefix, goes through
  object enumeration, a type check and a `^{commit}` peel. The result is checked for landing
  and pushing.
- **A2 Propagation**: the consumer's bind call feeds the bound SHA into the emitted JSON
  `revision`, the `git show` reads, and the exit code. Error paths must emit exactly one finding.
- **A3 Row construction**: the judge builds an actual typed object, uses the expected full
  commit SHA, a fresh sandbox, a unique prefix, and no host reads.
- **A4 Discrimination**: does some realistic consumer mutant survive this row (false green)?

## A1/A2 — consumer trace (observed in source; predictions are not observations)

1. Argv: `--revision` is required and mutually exclusive with `--selftest`.
   `--branch` defaults to `master` (`check-freshness-r17.py:380-394`). The judge runs
   `--revision <selector> --branch master` with no extra arguments (`R17_GATES`
   `check-revision-binding.py:73`; `run_tool:359-371`).
2. Bind: `_revision.bind(ROOT, args.revision, branch)` receives the raw selector
   (`check-freshness-r17.py:773`). `ROOT = Path(__file__).resolve().parents[1]` (`:55`), which
   is the sandbox because the judge runs `sandbox/tools/<name>` with `cwd=sandbox`
   (`check-revision-binding.py:362-364`). `import _revision` (`:52`) resolves to the
   sandbox's checked-out `tools/_revision.py`, because `prepare` runs
   `checkout --detach <tip>` (`check-revision-binding.py:234`).
3. Resolution in the frozen `_revision.py`:
   - The selector must match `REV` 7-64 hex (`_revision.py:175-176`).
   - `rev-parse --disambiguate=<lower>` must return exactly one object (`:119-124`).
   - `cat-file -t` returns `tag`, so the object is peeled with
     `rev-parse --verify --quiet --end-of-options <oid>^{commit}` (`:126-142`).
   - The peeled SHA must be an ancestor of `refs/heads/master` (`:180-185`). It must also be an
     ancestor of `refs/remotes/origin/master` when that ref exists (`:186-191`).
   - Binding git calls use `clean_env()`, which sets `GIT_CONFIG_NOSYSTEM=1` and
     `GIT_CONFIG_GLOBAL=/dev/null` (`:62-66`, `:69-73`).
4. Propagation on success:
   - `revision = binding.sha`, `tip = binding.branch_tip` and `source = revision`
     (`check-freshness-r17.py:774-776`).
   - Every document read is `git show <sha>:<path>` (`read_git:345-355`, `:779-789`). The tag
     object ID and the short prefix never reach any downstream read.
   - `emit` prints `revision` = the peeled full commit SHA (`:308-322`). The exit code comes
     only from `evaluate`: 0 or 1, or 2 on a parse error or read failure.
5. Error propagation:
   - A `RevisionError` is converted to `Cannot`, and exactly one finding is emitted with exit 2
     (`:792-796`).
   - On that path, the emitted `revision` echoes the raw selector, or the bound SHA if the
     failure came from a later `read_git` or `--registry-from` bind. This happens because
     `revision` was already reassigned at `:774`.
   - In both cases exit is 2, so `accepted()` cannot be satisfied by an error path
     (`check-revision-binding.py:396-404` requires `code != CANNOT`).

**Source prediction (not observed) for the unmutated candidate:** both observations of this row
should be accepted:
- the full tag object ID
- the shortest unique 7–39-hex prefix

Each should exit 0 or 1 with JSON `revision` = the sandbox tip. Exit is 1 if the registry is
absent at tip (`R17-FRESH-MISSING`, `:263-269`). The peel requirement matches
`build/CritBaseline.md:23` ("accepted, exact landed commit"). It also matches the NestedTag
oracle's propagation claim for this consumer (`build/Oracle07NestedTag.md:39-48`, `:65-67`). The
build fan-out has no AnnotatedTag oracle (`build/ConnPlanner.md:29`), so the comparison is with
that sibling oracle's consumer trace only.

## A3 — row construction in the candidate judge (observed)

- **Actual typed object**: `tag("commit", tip)` runs
  `git tag -a r21-target-check-freshness-r17-commit -m commit <tip>`. It then requires
  `rev-parse --verify <ref>^{tag}` to succeed, so the object is a real tag object, not a
  lightweight ref (`check-revision-binding.py:685-697`). The row is
  `"annotated_tag_to_commit": (commit_tag, tip)` (`:703`). The tag's stored target is not
  re-read through `cat-file -p`. It is trusted from the `git tag -a ... <tip>` construction.
- **Expected value**: `accepted(sandbox, name, selector, tip)`. `ok` requires
  `code != CANNOT` and `json.revision.lower() == tip.lower()` (`:396-404`, `:726`). This is an
  acceptance row, so no refusal ID or count applies. The `binding_ids == [E-REVISION-INVALID]`
  and `finding_count == 1` strictness applies only to the `expected_commit is None` rows
  (`:721-725`).
- **Unique prefix sanity**: the prefix width runs from 7 to 39 (`range(7, len(object_id))`,
  `:712`).
  - Uniqueness is counted against `cat-file --batch-all-objects`, taken after all four tag
    objects and the blob exist (`:705-707`).
  - The prefix is also required not to collide with `refs/heads/<p>` or `refs/tags/<p>`
    (`:713-715`).
  - If no prefix qualifies, the row raises `E-SANDBOX` rather than passing (`:716-717`).
- **Fresh sandbox**:
  - `target_type_measure` makes its own `TemporaryDirectory` clone, separate from `measure()`
    (`:743-747`).
  - The same sandbox is reused across the nine tools in sequence.
  - Fixture refs are deleted in `finally` (`:734-736`), but earlier tools' unreachable tag
    objects stay in the object store. This is harmless here because the uniqueness inventory
    includes them.
- **No host read, judge side**:
  - The lane is read only by `clone` (`:218-230`).
  - The tool subprocess gets `clean_env()` (`:365`).
- **No host read, consumer side (limit)**:
  - `check-freshness-r17.py` `git_in` drops every `GIT_*` variable, including the judge's
    `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_NOSYSTEM`. It re-isolates only when
    `isolate=True` (`:325-330`), and `read_git` calls it without isolation (`:341-346`).
  - So the content reads, unlike the binding path, read the user's `~/.gitconfig` and
    `/etc/gitconfig`.
  - [INFERENCE] This can only push the row toward a false red: a host config that breaks
    `git show` leads to `E-GIT-READ-FAILED` and exit 2, which fails `accepted`. It is not a
    false green. The judge's trust-boundary paragraph already declares only `GIT_*`
    suppression (`:49-53`).
- **Continuity, not new coverage**: this class duplicates round-20 `annotated_tag_object` and
  `annotated_tag_prefix` (`check-revision-binding.py:631-632`; `build/CritBaseline.md:36-39`;
  `build/ConnPlanner.md:29,71`). The old `object_selector_probes` matrix is still present and
  unchanged in this snapshot (`:475-673`), and `--object-target-types` is a separate mode that
  is mutually exclusive with `--object-selectors` (`:1391-1395`). The C2 mode change from 0 to
  1 measures matrix availability (`:758-759`, `:773`). It is not a ninefold behavioral uplift.

## A4 — concrete false green within this predicate (proposed mutant, NOT executed)

**Defect.** In `target_type_probes`, every acceptance class expects `tip`
(`check-revision-binding.py:702-703`). In the sandbox, `prepare` makes `tip` equal to
`refs/heads/master`, equal to detached `HEAD`, and equal to the consumer's
`binding.branch_tip` (`:234-241`). So the `annotated_tag_to_commit` row cannot tell "peeled the
selected tag to its commit" apart from "reported the branch tip".

**Mutant M-TIP** (one line in the primary file): change `check-freshness-r17.py:774` from
`revision = binding.sha` to `revision = binding.branch_tip`. Equivalent variants are
`revision = tip` after line 775, or adding `if binding.sha != binding.branch_tip: raise
RevisionError(E_NOT_LANDED, ...)`, which makes the tool accept only the tip.

Source prediction for M-TIP:
- **`annotated_tag_to_commit`**: the full-ID and prefix observations both bind successfully,
  exit 0 or 1, and emit `revision` = branch tip = `tip`. Both are `ok`, so the row is green.
- **`nested_tag_to_commit`**: also expects `tip`, so it is also green.
- **The three refusal rows**: `bind` raises before line 774 runs, so the single
  `E-REVISION-INVALID` stays unchanged. They are green.
- **Result**: `behavior_ok = True` (`:765`) and `target_type_tools` stays 9/9 for a consumer
  that mis-reports the bound revision whenever the selected commit is not the tip.

M-TIP is killed only outside this predicate:
- The old matrix's `landed-parent` case, `accepted(parent, parent)` (`:426`), catches it, but
  only when `measure()` is run and the tip has a parent.
- The consumer's own `binding_sandbox` would not catch it, because it calls `_revision.bind`
  directly (`check-freshness-r17.py:495-504`) and its CLI cases are all refusals (`:547-572`).

A discriminating row would tag a landed non-tip commit, such as `tip^1` (already available as
`parent` in `measure`), and expect that SHA.

**Second limit (content binding, also unexecuted).** Mutant M-READ keeps `revision =
binding.sha` but reads documents at `binding.branch_tip` or the worktree. Every
`accepted()` in both matrices compares only exit status and the JSON `revision`, so M-READ
survives. Reads at the bound SHA are claimed from source (`:779-789`), but no row tests them.

**Unexercised call site.** The second bind, `--registry-from` (`check-freshness-r17.py:777-778`),
is never passed by any judge row. Replacing it with the raw selector would survive the judge.
Source prediction: it would be caught by the consumer's own CLI selftest cases at `:566-571`.

**No defect in the unmutated candidate for this predicate.** The frozen consumer peels the tag
through the shared binder and propagates the full commit SHA to both the output and the reads
(A2). The judge row builds a real tag object with a sound unique prefix in a fresh clone (A3).
The finding is a discrimination gap in the row design (the expected value equals the branch
tip), not a wrong verdict on this candidate.

## Observations / inferences / limits

- **Observed (source text)**: every line citation above, read from the frozen candidate
  snapshots, plus build oracle and critic prose.
- **[INFERENCE]**: Git semantics for `--disambiguate`, `^{tag}` and recursive `^{commit}`
  peeling come from documented behavior. I assume the lane's baseline object `6923fe0b…`
  (`check-freshness-r17.py:56`) is present in the sandbox clone. If it were absent, exit would
  be 2 with `E-GIT-READ-FAILED`, which is a false red only.
- **Limits**:
  - Nothing was executed: no test, mutant, selftest or git command.
  - No LSP server was available to this seat, so cross-references are literal reads of the
    frozen files. That is not semantic proof.
  - No candidate output was examined. All verdicts are source predictions.
  - I make no non-author closure or outside-promotion claim.
- Installs/tooling: none needed or performed. NO-EXEC was honored and the host pacman pause was
  respected.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none
