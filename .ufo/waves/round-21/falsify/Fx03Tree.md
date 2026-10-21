# Fx03Tree — falsify attack on C2 target-type row `nonempty_tree` for consumer check-section-citations.py

Reviewed-SHA256: 1546d80403aa912e8f5b21710a85195e973216c120ec94457cfe5574c403aac3
Predicate: check-section-citations.py-nonempty_tree-candidate-control

Primary (this receipt binds only this file): `.ufo/waves/round-21/candidate/tools/check-section-citations.py`, candidate revision `0a14952b59d20179e1c813af58befaecd6992a17`, digest as stated in the assignment and in `candidate-files.json` (not recomputed by me — NO-EXEC).

Auxiliary frozen candidate dependencies, read only, cited by their `candidate-files.json` digests:
- `candidate/tools/_revision.py` 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
- `candidate/tools/check-revision-binding.py` 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6

Non-candidate advisory material (not candidate verdict inputs): round-20 pinned snapshot `snapshot/tools/check-revision-binding.py` (digest `da000de45b07ec2e4942ed798f6b9a7555c99180245d2139a94648cc4566b9e0` per `preregister.json`), `build/Oracle03Tree.md`, `build/ExecMatrix.md`, `build/ReviewOracle.md`, `preregister.json`, `measurement-refinement.json`, `falsify/spec.json` (my own item), `sources/git-types.txt`.

## Axes

- **Refusal-contract correctness (consumer):** for `--revision <nonempty-tree object id>`, does the frozen consumer actually produce exit 2, exactly one `E-REVISION-INVALID` finding, JSON `revision` = the literal selector, `correction_count` 0, and no target evaluation?
- **Row fidelity (judge):** is the `nonempty_tree` cell built from an independently created, actually typed tree object, with the exact refusal id/count asserted, in a fresh sandbox, without host reads?
- **Oracle agreement:** does the candidate control match `build/Oracle03Tree.md`'s source-only expectation for this consumer × tree cell?
- **Continuity / no-harm:** is the round-20 object-selector matrix byte-for-byte carried, with commit-tag acceptance kept as preserved coverage (not new coverage), and mode 0→1 not counted as behavioral uplift?

## Observations (all read from frozen bytes; nothing executed)

### Consumer bind/argv/error/output propagation (primary file)

1. `--revision` is a bare argparse string, mutually exclusive with `--selftest`, both required (primary 434–439); `--branch` defaults to `master` (440–443). The raw argv string reaches `bind(ROOT, args.revision, branch)` unmodified at 913; `revision, branch_tip = args.revision, None` at 911, overwritten only by the binding at 914–915 on success.
2. Frozen `_revision.py::bind` (172–192): `validate_branch` first (174), then `REV.fullmatch` 7–64 hex (175–176), then `_object_commit` (112–146): `git rev-parse --disambiguate=<selector.lower()>` (119), exactly one object required (122–124), `cat-file -t` type check (127–133); kind `commit` → oid (134–135); kind `tag` → peel `<oid>^{commit}` (139–142); **any other kind returns None** (136–137). `bind` then raises `RevisionError(E_INVALID, "revision", f"{revision} does not name one commit")` at 178–179.
3. A nonempty tree object id satisfies the hex shape but its kind is `tree`, so the observable is, by source derivation: exit 2 (`emit` returns `result.code`; `sys.exit(main())` 939–940), stdout one JSON line with `status=CANNOT_EVALUATE`, `revision` = the selector **as typed** (never a resolved SHA), `branch_tip` null, `correction_count` 0, and `findings` = exactly one `{"id": "E-REVISION-INVALID", "site": "revision", ...}` (main 923–927 wraps the RevisionError into a single `Cannot` → `Result(CANNOT, [Finding(...)], 0)`; `emit` 394–402). `read_git` is never reached; no document is evaluated.
4. No host read: the consumer's `git()` (405–414) runs `git --no-pager -C ROOT` with `GIT_*` stripped; `ROOT = Path(__file__).resolve().parents[1]` (39) — when the judge materializes the tool into the sandbox clone (`materialize` 259–274), ROOT is the sandbox root. `validate_branch`'s `git check-ref-format` (89–95) reads no repository. `clean_env` (62–66) isolates git config. The judge's own plumbing matches (`run_tool` 359–371 executes `[sys.executable, sandbox/tools/<name>, --revision, rev, (--branch), *EXTRA]` with cwd=sandbox; judge `git()` 107–116 and `clean_env` 100–104).

### Judge row construction (auxiliary `check-revision-binding.py`)

5. `target_type_probes` (676–736) derives the tree independently of the binder under test: `git rev-parse "{tip}^{tree}"` (678–679) where `tip` is the measured commit verified only by the judge; a nonempty guard uses `git ls-tree <tree>` with an explicit `Cannot("E-SANDBOX", "nonempty_tree", ...)` if empty (680–682). This is an actual `tree`-typed object created by Git from the measured commit — not a fabricated string, not derived through `_revision.bind`.
6. `nonempty_tree` maps to `(tree, None)` (699): `expected_commit=None` means the row demands a refusal — `refused(sandbox, name, tree, ID_INVALID, branch)` strengthened to `binding_ids == [ID_INVALID]` **and** `finding_count == 1` (721–725). That is the exact refusal id/count. Expected values are fixed before `run_tool` (dict 698–704 precedes the loop 719–729); the case's `ok` aggregates per-observation rows (730–732).
7. Selector sanity for this class: full-ID only (710–711 — the prefix branch is explicitly skipped for `nonempty_tree`). A full 40-hex object id is trivially unambiguous, and no shadowing ref named after the tree OID is created; a binder that resolved object IDs before refs (the frozen contract) is unaffected. For the tag classes the judge does derive unique prefixes with ref-collision guards (712–718), mirroring the round-20 pattern.
8. Fresh sandbox and hygiene: `target_type_measure` (739–780) clones the lane into a `tempfile.TemporaryDirectory` (743–746), `prepare` detaches and fabricates only in-sandbox branch/origin refs (233–242), tags are created (685–695) and deleted in reverse order in `finally` (734–736); any `Cannot` aborts to CANNOT_EVALUATE — fail-closed, no false-green path. `behavior_ok` requires `len(cases) == 5 and all ok` (765), so the strengthened refusal is inside the count.

### Comparison with the build oracle

9. `build/Oracle03Tree.md` predicts for this consumer × tree selector: exit 2, single `E-REVISION-INVALID` at site `revision`, literal selector echo, `branch_tip` null, count 0, no `read_git` reach, no mutation (observations 1–6 there). My independent source trace (items 1–4) reaches the same observables from the frozen candidate bytes; the candidate control satisfies the oracle as far as static derivation can establish. The oracle's LIMIT that no candidate snapshot of the consumer existed is discharged here by reading the frozen candidate copy at the assigned digest.
10. The oracle also records (its section "Does the pinned round20 matrix cover this case?") that the round-20 `object_selector_probes` never creates a tree — the only non-commit object there is a blob (`blob_object` snapshot 408–413). I confirmed the same on the round-20 pinned snapshot directly: no `mktree`/`^{tree}` object creation anywhere in its probe paths. The new `nonempty_tree` row therefore adds the previously unexercised cell for this consumer — exactly what preregister C2 claims (`cases` list includes `nonempty_tree`), while `measurement-refinement.json` scopes mode 0→1 as implementation presence, "not claimed uplift".

### Continuity (commit-tag) and old-matrix no-harm

11. `annotated_tag_to_commit` and `nested_tag_to_commit` (judge 702–703, expected commit `tip`) restate acceptance already pinned by the round-20 rows `annotated_tag_object`/`annotated_tag_prefix`/`full_tag_object_id_ref_shadow` (snapshot 629–632) and by the binder selftest (`annotated-tag-full-object-id`, `-prefix`, `nested-annotated-tag-object`, frozen `_revision.py` 360–365). This is **preserved continuity, not new coverage**.
12. Old matrix unchanged: the candidate's `probe_tool` (416–472) and `object_selector_probes` (475–673) are textually identical to the round-20 snapshot's same functions (snapshot 416–472, 475–673); `measure` (783–883) keeps the same case set and grade; the new behavior is opt-in `--object-target-types` (parser 924–925, main 1391–1409), mutually exclusive with `--object-selectors` (1392–1395). The C2 mode0→1 delta is a source-presence census (`target_type_measure` `available` check 750–761), not a behavioral 9-fold uplift claim — matching `measurement-refinement.json` and `ExecMatrix.md:8`.

## Mutant analysis (predictions; NOT executed)

- **M1 accept-tree mutant** (`_revision.py:134` `object_kind == "commit"` → `in ("commit", "tree")`): predicted observable on the primary is exit 2 with a single **`E-GIT-FAILED`** finding (merge-base `--is-ancestor <tree> <ref>` exits ≥2 → `_ancestor` 156–160 raises E_GIT), instead of `E-REVISION-INVALID`. The `nonempty_tree` row's exact-id assertion (judge 723–725) kills it. `Oracle03Tree.md:38` reaches the same conclusion. Not run.
- **M2 generic-peel mutant** (judge selftest stub `target-generic-peel`, 1239–1259): a tag-only `^{}` peel; the selftest already asserts the old object-selector matrix stays green while `tag_to_tree` fails and `all(ok)` is false (1244–1250); `nonempty_tree` is inside that `all`. The witness for "old matrix survives / new matrix kills" exists at source level. Not run.
- **M3 ref-aliasing binder** (resolves hex through refs first): no ref named for the tree OID exists in the sandbox, and the round-20 ghost-hex rows (snapshot 515–588) already pin object-before-refs; no false-green avenue specific to this cell.

## Findings by severity

1. **No defect within this predicate** (`check-section-citations.py` × `nonempty_tree` candidate control). Consumer propagation (argv → bind → single-finding CANNOT emit), judge row construction (independent typed object, exact refusal id/count, expected-before-run, fresh sandbox, ref cleanup, fail-closed errors, no host reads), oracle agreement, and old-matrix continuity all hold on the frozen bytes.
2. **LOW — tree class is full-ID-only** (judge 710–711): no unique short-prefix tree selector is probed, unlike commit/tag classes (old matrix prefix-shadow rows; new tag prefix derivation 712–718). A binder correct at 40-hex trees but wrong on short tree prefixes would not be discriminated by this row. Mitigation: the frozen binder's `--disambiguate` path is type-agnostic after resolution (one code path for all kinds), and the round-20 prefix rows pin prefix mechanics generally; residual risk is a type-conditional length bug, which no current row targets.
3. **INFO — refusal echo not graded**: `refused()` (383–393) never compares the echoed `json_revision` against the requested selector; the explicit comment at 482–484 makes echo-looseness intentional for refusals. Inherited round-20 grading shape, not introduced by C2; noted because the predicate says "exact refusal ID/count", which is graded exactly — the echo is not part of that contract.

## Residual risk and verification gaps

- Nothing was executed: the M1–M3 outcomes and all "exit/finding" observables are source predictions, marked as such; the only executed-behavior authority remains L1's run of the judge/selftest commands (`measurement-refinement.json`).
- All digests are taken from the assignment and `candidate-files.json`; none recomputed (NO-EXEC).
- `merge-base` exit ≥2 for a non-commit operand is Git contract per `sources/git-types.txt`-adjacent knowledge and `Oracle03Tree.md`; the exact stderr text is [INFERENCE] — the finding id mapping in `_revision.py:156–160` is not, since every non-{0,1} status maps to E_GIT regardless of text.
- `nonempty_tree`'s tree object is the measured tip's root tree; subdirectory trees are not probed. A binder keyed on root-tree OIDs specifically (implausible: kind check is per-object) would slip; noted for completeness, no evidence any implementation branches on that.
- LSP was not available in this seat's tool inventory; all call-site checks are text reads of frozen files (recorded per role requirement).

## Limits

Read/grep/glob only; no bash/eval/import/compile/network; no installs (none needed — nothing to report to L1); no production or candidate-file edits; this report is the only byte I wrote. Author-dispatched leaf: no subagent dispatch; this is a recommendation to L1, not closure or promotion.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none