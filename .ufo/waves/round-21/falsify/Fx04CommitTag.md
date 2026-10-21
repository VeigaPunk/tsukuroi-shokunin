# Round 21 · Fx04CommitTag — falsify attack
# Consumer: tools/check-source-scope-correction.py × target class annotated_tag_to_commit

Seat: TsukuroiR21.Fx04CommitTag (leaf, NO-EXEC, fresh attack seat). Candidate revision
0a14952b59d20179e1c813af58befaecd6992a17. Baseline 82e519203e676c532b1dc5ea91a85671f2286e7b.

Axes: C2 operability (does this row discriminate a wrong consumer outcome for this class),
C1 depth (does the row exercise the `tag-to-commit` decision row as written), C3 calibration
(digest-pinned primary file, exact predicate line).

## Evidence read (read tool only; nothing executed)

Primary file, bound by this receipt:
- `.ufo/waves/round-21/candidate/tools/check-source-scope-correction.py`
  (sha256 931504455caae52eaa2f2018a826c1b40c1eed83025ec0f13d1127c66fb85afc per candidate-files.json).

Auxiliary snapshot dependencies. These are cited in prose only and are not covered by this receipt:
- `candidate/tools/_revision.py` sha256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
  (equal to the preregistered snapshot digest in preregister.json:50-52).
- `candidate/tools/check-revision-binding.py` sha256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6.
- `candidate/corpus/knowledge/selector-contract-r21.md` sha256 b4966a9bcf4ac124a964718b0ed76104e2f07c41b63050dc8bda618ea5136353.
- Context only, not used as a verdict input: `build/Oracle04NestedTag.md`, `build/ConnPlanner.md:29,71`,
  `build/CritBaseline.md:23,36,39`, `preregister.json:21-34`.

## 1. Consumer propagation (observed in source)

- argv: the judge calls `run_tool` (judge :359-371) with `[python, sandbox/tools/check-source-scope-correction.py,
  --revision <sel>, --branch <branch>]`, using `cwd=sandbox`, `env=clean_env()` and stdin set to DEVNULL.
  `EXTRA[...] = ()` (judge :77), so no other argv is passed.
- Parsing: `main()` (:614-631) uses argparse with `exit_on_error=False`. A parse error emits
  `E-CLI` with CANNOT; neither path is reached for this row.
- Binding (:636-641): the consumer calls `_revision.bind(ROOT, args.revision, branch)`, where
  `ROOT = Path(__file__).resolve().parents[1]` (:18), which is the sandbox. A `RevisionError` is
  wrapped as `Cannot(fid, site, detail)` and emitted (:647-649) with exit 2, status CANNOT_EVALUATE,
  exactly one finding, and `revision` echoing the raw selector. Any other exception becomes
  `E-INTERNAL` with CANNOT (:650-652).
- Binder, tag path (`_revision.py` :112-146): `rev-parse --disambiguate=<sel>` must return exactly one
  object. `cat-file -t` must report `tag`. The tag is then peeled with
  `rev-parse --verify --quiet --end-of-options <oid>^{commit}`. Ancestry checks run on the peeled sha
  (:184-191).
- Accept output (:642-643, :657; `emit` :336-343): `revision, branch_tip = binding.sha, binding.branch_tip`.
  The content is read with `git show <peeled sha>:<path>` (:366-376), and the JSON line prints
  `revision` = peeled 40-hex commit. The exit is 0 or 1 depending on the content verdict, never 2,
  unless the R14 JSON at that revision fails to parse (:304-306), which gives CANNOT.
- The consumer has no object-type logic of its own. Every type decision is delegated to `_revision`.

## 2. Judge row under test (observed in source, judge :676-736)

- **Independently created object:** `tag("commit", tip)` (:697) runs `git tag -a r21-target-check-source-scope-correction-commit -m commit <tip>`
  in the sandbox (:685-695), after checking that the ref is absent (:687-689). The object ID comes from
  `rev-parse --verify <ref>^{tag}`, which fails unless the ref names a tag object. Row :703:
  `"annotated_tag_to_commit": (commit_tag, tip)`.
- **Expected commit:** `tip` comes from the judge's own `bind` (:192-208, an independent copy whose
  `object_commit` is at :139-166). It is not derived from the consumer or from `_revision`.
- **Selectors:** the full tag OID, plus the shortest prefix of length 7-39 that is unique in
  `cat-file --batch-all-objects` and collides with neither `refs/heads/` nor `refs/tags/` (:710-718).
  The inventory is taken after all four of this consumer's tags exist (:705-707). Earlier consumers'
  tags leave unreachable objects behind; they are in the inventory and carry distinct tag names, so
  the uniqueness check is sound. Nothing creates objects between the inventory and the consumer run
  (`read_git` and `bind` only read).
- **Grading:** `accepted()` (:396-404) requires exit != 2 and JSON `revision` equal to `tip`
  (case-insensitive). This row is an accept row only; no refusal ID or count applies.
- **Fresh sandbox:** `target_type_measure` (:739-781) uses `TemporaryDirectory` → `clone_lane --no-tags`
  → `prepare` (detached checkout at `tip`, `refs/heads/<branch> = tip`, origin remote removed,
  `refs/remotes/origin/<branch> = tip`; :233-242). The four refs are removed in a `finally` block
  (:734-736). One sandbox is shared, sequentially, by all nine consumers.
- **Host reads:**
  - The judge reads the lane only through `clone_lane` and `lane_tip`, which are the intended inputs.
    Its git calls use `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null` and
    `core.hooksPath=/dev/null` (:100-117).
  - Consumer-side limit, not a defect in this predicate: the consumer's own `git()` (:354-363)
    removes every `GIT_*` variable it inherits and then re-adds only `GIT_OPTIONAL_LOCKS`, `GIT_PAGER`
    and `LC_ALL`. That drops the judge's isolation, so `read_git` will read the host's system and
    global git config (HOME is preserved).
  - Source prediction: `git show <commit>:<path>` on a blob streams raw bytes without textconv, so
    this does not change the graded `revision` field [INFERENCE]. `_revision`'s own calls stay
    isolated (`_revision.py` :62-66).
- **Continuity:** this row duplicates the round-20 rows `annotated_tag_object` and
  `annotated_tag_prefix` (judge :631-632), which also build `tag -a … tip`. It is continuity, not new
  coverage, as stated in `ConnPlanner.md:29,71` and `CritBaseline.md:36,39`. The old matrix
  (`object_selector_probes`, `measure`, `probe_tool`) is unchanged by this row.
- **C2 mode:** `target_type_mode` (:758-759, :773) is an AST census of function and option presence.
  The 0→1 change is availability counted once. It is not a ninefold behavioral uplift.

## 3. Source prediction for the actual consumer (not observed)

Given candidate `_revision.py`, both selectors (full tag OID and unique prefix) should be accepted
with exit 0 or 1 and JSON `revision == tip`. The row should therefore be ok.

Precondition, not verified because reading git objects counts as execution here: the R14 JSON at
`tip` parses. If it does not, the consumer gives CANNOT and the row fails red, not false-green, and
the old `tip` and `annotated_tag_object` rows fail identically.

This agrees with the closest build oracle, `Oracle04NestedTag.md` §2-3: on accept, `revision` = the
peeled commit and exit is in {0, 1}. No AnnotatedTag oracle exists for this consumer
(`ConnPlanner.md:29`).

## 4. Attack result: two concrete gaps where a mutant survives

The consumer and binder are correct for this class. The defects are in the discriminating power of
the judge row. Both mutants below are proposals only and were not executed.

### F1 — Accept arm is blind to substituting the branch tip or HEAD

The tagged commit, the branch tip and the sandbox HEAD are all `tip`:
- the tag is built at :697;
- `prepare` sets the branch and does a detached checkout at :234-235;
- `target_type_measure` runs no `probe_commit`.

Therefore any wrong resolution that lands on tip or HEAD satisfies `revision == tip`.

- **Mutant M1 (consumer, :642):**
  `revision, branch_tip = binding.branch_tip, binding.branch_tip`.
  - Prediction: all five target-type rows still pass (both accept rows expect `tip`; refusals are
    unchanged), so `behavior_ok=True` and the tool counts toward `target_type_tools`.
  - Killed elsewhere: the old matrix row `probe_tool` "landed-parent" (judge :427,
    `accepted(parent, parent)`) catches it, provided `tip` has a parent.
- **Mutant M2 (binder, `_revision.py` :141-142):** on a successful `^{commit}` peel, return
  `_commit(repo, "HEAD")` instead of the peeled sha.
  - Prediction: it survives every row in `--object-target-types`, because HEAD is `tip` there.
  - Killed elsewhere, for three reasons:
    - `measure()` runs `probe_commit` first (judge :802), which moves HEAD to an unlanded commit, so
      `annotated_tag_object` then gets E-REVISION-NOT-LANDED.
    - `full_tag_object_id_ref_shadow` behaves the same way.
    - The binder selftest `annotated-tag-full-object-id` (`_revision.py` :360) fails, because HEAD
      there is the unlanded commit.

Within this predicate, F1 is a false-green that is limited to its mode. It is not a false-green
across the whole gate suite, because the unchanged old matrix kills both mutants.

Proposed fix (not applied): construct the `annotated_tag_to_commit` (and nested) fixture on a landed,
pushed, non-tip commit such as `tip^1`, and expect that commit. That makes expected ≠ branch tip ≠ HEAD.

### F2 — The `-if-landed-and-pushed` conjunct of `tag-to-commit` has no consumer-level probe

`selector-contract-r21.md:22` states that tag-to-commit is accepted only if the commit is landed and
pushed, and that ancestry failures keep E-REVISION-NOT-LANDED / E-REVISION-NOT-PUSHED. No annotated
tag that targets an unlanded or unpushed commit exists in any of these places:
- this row (:697);
- the old matrix (:502-505, tag at `tip`);
- the unlanded and unpushed shadow rows (:635-671, which use commit prefixes and ref names);
- the binder selftest (:353-365, :414-419).

- **Mutant M3 (`_revision.bind` :177-192):** when the unique object selected by `--disambiguate` is a
  `tag`, return `Binding(sha, branch, tip, None)` before the ancestry checks at :184-191. This is the
  "trust annotated release tags" weakening.
- Prediction: it survives this row (the tag targets the landed, pushed `tip`), the whole
  `--object-target-types` mode, the old `--object-selectors` matrix, and the binder selftest.

This is a coverage gap in both matrices for the tag-to-commit refusal arm, not only in this row.

Proposed fix (not applied): add `tag_to_unlanded_commit` (expect exactly one E-REVISION-NOT-LANDED)
and `tag_to_unpushed_commit` (origin lagging; expect exactly one E-REVISION-NOT-PUSHED) as a new opt-in
row set, leaving the old matrix unchanged.

## 5. No defect found within this predicate on

- Argv, error and output propagation in the consumer: one finding on refusal, peeled sha on accept.
- Independence of the typed object and of the expected commit.
- Prefix uniqueness: object-only, inventory taken after creation, no ref collision.
- Sandbox freshness and ref cleanup.
- Judge-side host isolation.

## 6. Limits

- Every statement is a source prediction; no consumer, judge, git command or mutant was run.
- Whether `tip` has a parent at 0a14952 (needed for the M1 kill) and whether the R14 JSON at `tip`
  parses were not checked.
- Separate from this predicate: `target_type_measure` binds `--tools-revision` through the judge's
  prefix- and tag-accepting `bind` (:742). `measure()` instead requires a full 40-hex commit (:785-790).
- No non-author closure or outside promotion is claimed.
- Tooling: nothing installed or updated; none needed; pacman pause respected.

Reviewed-SHA256: 931504455caae52eaa2f2018a826c1b40c1eed83025ec0f13d1127c66fb85afc
Predicate: check-source-scope-correction.py-annotated_tag_to_commit-candidate-control
Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
