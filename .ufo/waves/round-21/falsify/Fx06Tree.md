# Fx06Tree — check-boot-chain.py × nonempty_tree (candidate control)

Round 21 falsify wave, fresh attack seat. Godspeed axes named: (A1) candidate
correctness — does the frozen consumer actually refuse a nonempty tree object
with the exact finding id and count this row grades; (A2) matrix soundness —
would the row go red if the binder under test wrongly accepted trees; (A3)
continuity / non-inflation — old matrix unchanged, commit-tag continuity
preserved, C2 mode0→1 not counted as behavioral uplift; (A4) receipts — exact
reviewed bytes and predicate lines. All citations are to frozen candidate
copies; nothing was executed.

## Receipts

Primary reviewed file (candidate snapshot, predispatch digest per
candidate-files.json, matching the assigned digest):
`tools/check-boot-chain.py` — assigned SHA256
91312f103e694daafc95006fc0c083f6bfbe3abad03a2abed370f50e7ff22982
(inventory entry `.ufo/waves/round-21/candidate-files.json` lines 54-58 lists
the identical value).

Auxiliary snapshot dependencies read for this verdict (all under
`.ufo/waves/round-21/candidate/`, digests as provided by
candidate-files.json; snapshot copies under `.ufo/waves/round-21/snapshot/`,
digests as provided by preregister.json):

- `tools/check-revision-binding.py` — SHA256
  0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6 (candidate;
  row under attack lives here: `target_type_probes` :676-736,
  `target_type_measure` :739-780, grading helpers `refused`/`accepted`
  :383-404, build oracle `object_commit`/`bind` :139-208).
- `tools/_revision.py` — SHA256
  06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
  (candidate; the shared binder the consumer imports).
- `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py` — SHA256
  da000de45b07ec2e4942ed798f6b9a7555c99180245d2139a94648cc4566b9e0 (round-20
  frozen copy, used only to verify old-matrix unchangedness).
- `.ufo/waves/round-21/snapshot/tools/_revision.py` — SHA256 06b71e8cb4aa541a…
  (per preregister.json snapshots) — byte-identical digest to the candidate
  `_revision.py`: the shared binder did not change in this round.
- `.ufo/waves/round-21/preregister.json` (C2 case list names `nonempty_tree`
  and "preserve: Round20 --object-selectors matrix and metric unchanged").

Primary receipts bind only `tools/check-boot-chain.py`; the files above are
auxiliary context.

## Observations (read-only source facts)

1. Row construction, candidate judge `target_type_probes` :676-736. The tree
   target is built independently of the binder under test:
   `tree = must(git(sandbox, "rev-parse", f"{tip}^{{tree}}"))` (:678-679) —
   the tip commit's root tree from the sandbox object database; nonemptiness
   is enforced by `git ls-tree <tree>` with a fail-closed
   `Cannot("E-SANDBOX", "nonempty_tree", ...)` when empty (:680-682). The
   class maps to refusal-only: `"nonempty_tree": (tree, None)` (:699), so the
   graded expectation is exit=CANNOT(2), finding id `E-REVISION-INVALID`,
   `binding_ids == [E-REVISION-INVALID]` and `finding_count == 1`
   (:720-725 wrapping `refused` :383-393).
2. Selector set asymmetry: for every class except nonempty_tree a unique
   7–39-hex prefix of the object is appended (`selectors.append(prefix)`,
   :710-718, guarded by `if label != "nonempty_tree"` at :711 and a
   uniqueness-plus-no-ref-collision search :712-715). The nonempty_tree row
   feeds exactly one selector: the full 40-hex tree OID (:709-710).
3. Consumer trace, candidate `tools/check-boot-chain.py`. `ROOT =
   Path(__file__).resolve().parents[1]` (:57); `main` binds through the shared
   module only: `binding = _revision.bind(ROOT, args.revision, branch)`
   (:1573, import at :53-54, `sys.dont_write_bytecode = True` keeps the
   import read-only). On `RevisionError` it emits exactly one finding and
   exits CANNOT: `revision, branch_tip = "unbound", None` (:1571) stays
   unmutated on the failure path, `emit(Result(CANNOT, [finding], 0, 0), …)`
   at :1578-1584; the emitted JSON carries `findings: [{id: E-REVISION-INVALID,
   site: "revision", …}]`, `"revision": "unbound"`, no other E-ident tokens in
   scope/detail strings (`emit` :785-798).
4. Binder behavior for a tree selector, candidate `_revision.py`. `bind`
   validates branch, then `REV.fullmatch` (40 hex passes), then
   `_object_commit` (:172-179). `_object_commit` enumerates
   `rev-parse --disambiguate=<lowercased>` (:119), requires exactly one object
   (:122-124), types it with `cat-file -t` (:127-133); kind `tree` is neither
   `commit` nor `tag`, so it returns None (:134-137) → `RevisionError(
   E_INVALID, "revision", "<tree> does not name one commit")` (:177-179). The
   returned commit is "never [reparsed] as a ref" (:117), so no
   branch/tag named like hex can shadow the verdict.
5. Build oracle agreement for this consumer: judge's independent
   implementation `object_commit` (:139-166) classifies a lone tree object as
   None exactly the same way (type check after disambiguation, no commit, no
   tag → None), and its `bind` raises `Cannot(ID_INVALID, …)` at :195-199.
   Oracle and under-test agree on `E-REVISION-INVALID` for the full tree OID.
6. Sandbox / no host read: `target_type_measure` (:739-780) runs everything in
   `tempfile.TemporaryDirectory(prefix="tsukuroi-target-types-")` (:743),
   `clone_lane` (`git clone --no-hardlinks --quiet --no-tags`, :218-230),
   `prepare` detaches at tip and pins only local + origin tracking refs
   (:233-242), `materialize` copies each tool from `git show <tip>:tools/<name>`
   into the sandbox (:259-274), and `run_tool` executes
   `sys.executable <sandbox>/tools/check-boot-chain.py --revision <selector>
   --branch master` with `cwd=<sandbox>` and a GIT_*-stripped env (:359-371;
   EXTRA for check-boot-chain.py is `()` per :71-76). Because the consumer's
   ROOT is derived from its own copied path and every corpus read is
   `git -C <ROOT> show <sha>:<path>` (:801-824, DocSet at :1616-1619), the
   sandboxed consumer reads nothing from the host lane. Fixture tags are
   per-tool/per-label names (`r21-target-check-boot-chain-*`, :685-695) and
   are deleted in a `finally` (:734-736).
7. Old matrix unchanged: snapshot (round-20) and candidate judge have
   identical function boundaries for lines 1-675 (every def at the same line
   number), and the read-back bodies of `refused`/`accepted`/`blob_object`/
   `probe_tool`/`object_selector_probes` (:383-473, :475-673) are verbatim
   identical; `measure`'s body is identical and merely shifted +107 lines by
   the insertion of `target_type_probes`/`target_type_measure` (:676-780).
   The snapshot judge has no target-type functions at all (its `measure` sits
   at :676). `_revision.py` digests are equal between snapshot and candidate
   (see receipts). C2 mode is additive and opt-in: `--object-target-types`
   (:912-926), mutually exclusive with `--object-selectors` (main :1389-1403).
8. C2 semantics: `target_type_mode = int(available)` where `available` is a
   finite AST census of `target_type_measure`/`target_type_probes` function
   presence plus the `--object-target-types` option string (:750-761, :773),
   self-described as `"availability_limit": "finite AST function/option
   presence census, not universal judge semantics"` (:780). Behavioral
   counting is separate: `behavior_ok` per tool (:762-767) and
   `target_type_tools = count` (:767). Mode0→1 therefore flips only the
   availability flag, not any behavioral counter.

## Predictions (source-derived, never executed)

- P1 (A1): running the candidate consumer with `--revision <40-hex tree>
  --branch master` in the sandbox prints one JSON line
  `status=CANNOT_EVALUATE, revision="unbound", findings=[{id:
  E-REVISION-INVALID, site: revision, …}]` and exits 2. Grading
  (:720-725) then sees exit==2 ✓, `finding_id` = first list id =
  E-REVISION-INVALID ✓, `binding_ids == [E-REVISION-INVALID]` ✓ (no other
  BINDING_IDS token appears anywhere in the payload), `finding_count == 1` ✓
  → the nonempty_tree row for check-boot-chain evaluates ok=true. This
  prediction follows from O3+O4; it is a source prediction, not a run.
- P2 (A2): if the binder wrongly accepted the full tree OID, the consumer
  would proceed to read the corpus at `<tree>:corpus/...` — `git show
  <tree>:<path>` resolves paths inside a root tree whose bytes equal tip's —
  and return PASS/FAIL/CANNOT with either zero findings or corpus finding
  ids; no path produces `exit==2 ∧ exactly-one E-REVISION-INVALID finding`,
  so the row goes red. The full-OID direction of the row is sound.
- P3 (echo-robustness): a tool that exits 2 while echoing E-REVISION-INVALID
  outside a single finding (empty findings list, or token in a non-findings
  field) is still graded red because `finding_id`'s regex fallback
  (:349-356) is overridden by the row's `finding_count == 1` requirement
  (:723-725). The row cannot be greened by echo alone.

## Findings by severity

- Fx06Tree-1 — Low (false-green window in the new row's selector coverage;
  located, mutant proposed and NOT executed). The nonempty_tree row is the
  only one of the five classes without a unique-prefix selector
  (`if label != "nonempty_tree"`, candidate judge :711-718), although the
  prefix machinery (:712-715) works identically for a tree OID and the
  object inventory (:705-707) already includes it. Concrete falsifier: in
  candidate `_revision.py` :133-137 mutate
  `if object_kind == "commit": return oid` to
  `if object_kind == "commit" or (object_kind == "tree" and
  len(revision) < 40): return oid`. A unique 7–39-hex tree prefix then binds;
  the consumer reads the corpus through the root tree (`git show
  <tree>:<path>`, check-boot-chain.py :814-824) with byte-identical content
  and passes in production, while the nonempty_tree row (full OID only) — and
  every other row of this judge, since no r20 selector row feeds a tree
  selector either (`object_selector_probes` :475-673; `noncommit_blob` is
  full-OID, :633) — stays green. This is a completeness gap of the new row,
  not a defect of the shipped candidate: as written, `_object_commit`
  refuses tree prefixes too (same type check at :133-137 regardless of
  selector length). Fix is one line: drop the label exclusion so
  nonempty_tree also appends its unique prefix; the refusal grading at
  :720-725 already handles multiple selectors.
- No defect within this predicate for the exercised dimension. For the
  selector the row actually feeds (full 40-hex nonempty tree OID), the
  candidate consumer's refusal (O3+O4) matches the row's exact expectation
  (id, count, exit) and the independent build oracle (O5); the row is strict
  enough that echo/over-reporting mutants fail it (P3), and any
  tree-accepting mutant of the full-OID path fails it (P2). Commit-tag
  continuity: the `annotated_tag_to_commit` acceptance restates round-20
  coverage (`annotated_tag_object`/`annotated_tag_prefix` at
  :616-632 already accepted an annotated tag object/prefix peeled to tip);
  per assignment it is preserved as continuity, not new coverage, and no
  uplift is claimed from it here.
- Informational (non-inflation, A3): C2 mode0→1 (`target_type_mode`) is an
  AST availability census only (O8) and is not a behavioral 9-fold uplift;
  the behavioral counter (`target_type_tools`) is computed from
  `behavior_ok` separately (:762-767). The round-20 matrix and metric are
  unchanged per O7, matching preregister.json's "preserve" clause.

## Residual risk and verification gaps

- Nothing was executed: P1-P3 are source predictions; runtime agreement
  (actual exit codes, actual JSON bytes, actual git disambiguation behavior
  on the lane) is unverified by this seat and belongs to an executor lane.
- Fx06Tree-1 leaves a one-dimensional blind spot (prefix-scoped tree
  acceptance) until the row gains a tree-prefix selector; the same prefix
  dimension is absent for the bare blob class across both matrices (r20
  `noncommit_blob` is full-OID only) — out of this predicate, noted for L1.
- `finding_id` returns the first finding id, so the row cannot attribute
  which layer refused (shared binder vs tool-local pre-check) when a tool
  duplicates the binder's regex locally; identical limitation applies to
  every row of this judge and predates round 21.
- Row behavior assumes the lane corpus at tip passes the gate when binding
  succeeds (P2's red verdict holds for any exit because the graded id/count
  cannot occur post-bind); the corpus-at-tip state itself was not evaluated.
- No tool installation or upgrade was performed or needed (source-only
  review; NO-EXEC contract).

Reviewed-SHA256: 91312f103e694daafc95006fc0c083f6bfbe3abad03a2abed370f50e7ff22982
Predicate: check-boot-chain.py-nonempty_tree-candidate-control
Scope: executed=none
