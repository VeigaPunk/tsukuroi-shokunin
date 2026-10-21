# Round 21 · Oracle04NestedTag — expected source-only behavior
# Consumer: tools/check-source-scope-correction.py · Selector type: NestedTag (tag→tag→commit)

Seat: TsukuroiR21.Oracle04NestedTag-5 (leaf, NO-EXEC). Baseline 82e519203e676c532b1dc5ea91a85671f2286e7b.
Axes named: C1 depth (does a consumer-level NestedTag decision row exist and what does it decide),
C2 operability (exact observable exit/status/finding/revision semantics before candidate output exists),
C3 calibration (pinned receipts; this report reviews the pinned snapshot bytes, SHA256 below).

## 1. Evidence inspected (all read-only, nothing executed)

- Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (snapshot tag `#1303`).
  The live `tools/_revision.py` carries the identical snapshot tag `#1303`, i.e. byte-identical
  content under this reader, consistent with the declared SHA256 `06b71e8c…58cbf`.
- Consumer `tools/check-source-scope-correction.py` (tag `#43DD`): `main()` :614–658,
  `emit()` :336–343, `binding_cases()` :462–521, `read_git()` :366–376.
- Pinned judge `.ufo/waves/round-21/snapshot/tools/check-revision-binding.py` (tag `#1C93`):
  `object_selector_probes()` :475–673, `refused()`/`accepted()` :383–404, `run_tool()` :359–371,
  `TOOLS`/`EXTRA` :61–79.
- `.ufo/waves/round-21/preregister.json` — C2 preregistered `target_type_tools` case list:
  `nonempty_tree`, `tag_to_blob`, `tag_to_tree`, `nested_tag_to_commit`, `annotated_tag_to_commit`.
- `corpus/knowledge/selector-contract-r21.md` — five fixed decision rows; `tag-to-commit`
  explicitly covers "annotated tag, **including nested annotated tags**, peels recursively
  to the commit → accept-if-landed-and-pushed" (lane doc, line 22).
- `.ufo/waves/round-20/build/BindTagObject.md` — prior oracle; its R6 `TN-nested` row predicted
  exactly this accept semantics (binder sha = C, tool accept revision = C).

## 2. Argument propagation through the consumer (source-verified)

- `main()` :636–643 — `--revision` present → `binding = _revision.bind(ROOT, args.revision, branch)`;
  the raw selector string and `--branch` value are passed verbatim. `RevisionError` is wrapped in
  `Cannot(exc.fid, exc.site, exc.detail)` → `emit(Result(CANNOT, [finding]), revision, branch, None)`
  (:647–649): exit 2, status `CANNOT_EVALUATE`, `findings` = exactly one finding with the binder's id.
  On refusal the JSON `revision` echoes the requested selector (assignment at :642 never ran);
  per judge `refused()`/:482–485 that echo is not an accepted binding.
- On success `revision, branch_tip = binding.sha, binding.branch_tip` (:642) — so the JSON
  `revision` is the peeled 40-hex commit SHA, never a tag OID or selector prefix. `branch_tip`
  is `_commit(refs/heads/<branch>)`. Reads then run `git show <sha>:<path>` (:643, :366–376) on the
  peeled commit and `evaluate()` decides PASS/FAIL independently of object type.
- The consumer contains zero object-type logic of its own: every NestedTag decision is delegated
  to `_revision._object_commit` + `bind`. No per-type branch exists in the consumer to mutate.
- `EXTRA["check-source-scope-correction.py"] = ()` (judge :77) — no extra argv; `--revision` +
  optional `--branch` is the complete contract.

## 3. Expected behavior — NestedTag selector (fixture: TN tag→T tag→C commit; C landed on
## `refs/heads/master` and, when `refs/remotes/origin/master` exists, ancestor of it; TN unique)

Derived from pinned binder `_object_commit()` :112–146 and `bind()` :172–192, cross-checked
against S081/S082 (`sources/git-types.txt`, `selector-contract-r21.md`):

- `--disambiguate=<tn.lower()>` must yield exactly one object (TN); a 7+-hex unique prefix
  of TN is also a legal selector (REV regex :41 admits 7–64 hex; same code path).
- `cat-file -t TN` → `tag`; peel `rev-parse --verify --quiet TN^{commit}` follows the tag chain
  recursively → C (S081: `^{}` dereferences "recursively until a non-tag object is found";
  `^{commit}` requires that terminal object be a commit).
- Ancestry gates apply to **C, never to TN or T**: `merge-base --is-ancestor C refs/heads/master`
  then, when the origin ref exists, `... refs/remotes/origin/master`.
- **Accept** (all gates pass): exit ∈ {0,1}, never 2 — 0 when `evaluate()` finds no issues,
  1 when the evaluated docs at C have findings; for this consumer the content verdict is
  orthogonal to object type. JSON: `status` ∈ {PASS, FAIL}, `revision` = exact 40-hex `C`,
  `branch_tip` = local branch tip commit, `correction_count` = count of correction objects,
  `findings` = content findings (none binding-class). Judge `accepted()` (:396–404) requires
  exactly: `exit != 2` and `json.revision.lower() == C.lower()`.
- **Refuse** (any gate fails): exit 2, `status` `CANNOT_EVALUATE`, `findings` = exactly one
  binding finding; `revision` echoes the selector string; `correction_count` = 0.
  - `TN^{commit}` unpeelable to a commit (chain bottoms in tree/blob, or tag→noncommit): `E-REVISION-INVALID`,
    site `revision`, detail `"<sel> does not name one commit"` (:178–179; the `^{commit}` peel
    returns nonzero, repo-check succeeds → `_object_commit` returns None :141–145).
  - `C` not ancestor of branch: `E-REVISION-NOT-LANDED`, site `refs/heads/master` (:184–185).
  - `C` landed but not ancestor of `refs/remotes/origin/master` when that ref exists:
    `E-REVISION-NOT-PUSHED` (:189–190). A tag chain whose commit is unlanded/unpushed must refuse
    on the peeled commit — the tag object itself is never tested for ancestry.
  - Prefix matching >1 object, or zero objects: `E-REVISION-INVALID` (:123–124 → :178–179).
  - Selector not 7–64 hex, or branch syntax invalid first: `E-REVISION-INVALID` /
    `E-BRANCH-INVALID` in `bind()` order :174–176 (branch validated before revision).

## 4. Does the old round-20 `--object-selectors` matrix cover this consumer/type pair? — **No.**

- `object_selector_probes()` (:475–673) builds exactly one annotated tag: `tag -a <name> <tip>`
  (:502–505), tag object resolved at :506–509. Consumer-side tag rows are only
  `annotated_tag_object` (:631) and `annotated_tag_prefix` (:632) — both depth-1 tag→commit.
  The ghost-tag/ref-shadow/unlanded-prefix-tag rows use tag **ref names** as selector context,
  never a tag-of-tag object. No `git tag -a <name> <tag-object>` call exists anywhere in the
  judge; grep for `nested`/`{tag}` construction confirms only the `^{tag}` *introspection* at :507.
- The pinned **binder selftest** does contain `nested-annotated-tag-object` (:362–365:
  `tag -a peel-nested <tag_oid>`; `bind(repo, nested_tag_oid).sha == tip`). So the recursion
  mechanism is pinned at binder unit level — but the consumer CLI path (argv → `main()` →
  `bind` → emitted JSON `revision`) is never exercised with a nested tag. The round-20 matrix
  therefore covers this specific consumer/type pair only by shared-code inference, not by any
  executed consumer case. The new preregistered `nested_tag_to_commit` (C2) fills exactly that gap.
- The consumer's own `binding_cases()` (:462–521) has no tag selector row at all.

## 5. Smallest realistic weakening the old matrix misses (NestedTag-specific)

Git offers **no non-recursive single-step peel operator**: `^{commit}`, `^{}`, `^0`, `^*` all
dereference tag chains to their terminal object (S081). Therefore no one-token change at
`_revision.py:139–140` produces a peel that is right at depth 1 but wrong at depth 2 —
`^{}` is wrong only at tag-to-noncommit (a different row), `^{object}`/`oid`/omitting the suffix
is wrong at depth 1. The smallest realistic NestedTag-only weakening is a **hand-rolled
one-step peel**: replace `rev-parse --verify {oid}^{commit}` (:139–142) with a
`cat-file -p {oid}`-based read of the tag object's `object <hex>` header and return that
target directly. For TN it yields inner tag T, not C.

Observable consequence for this consumer (no exec performed): if `merge-base --is-ancestor`
peels the tag argument T recursively — expected, since `--is-ancestor` resolves commit-ish
operands [INFERENCE] — the ancestry gates pass, `bind` returns `Binding.sha = T`, and the tool
exits 0/1 with `revision = T` (40-hex tag OID). That defeats only the full-SHA identity
assertion (`revision == C`), which is precisely what `accepted()` checks and what the new
`nested_tag_to_commit` row requires. If merge-base instead rejects T, the refusal is
`E-REVISION-NOT-LANDED` — still wrong, since expectation is accept [INFERENCE]. Either way the
mutation is invisible to every depth-1 consumer row and to the round-20 matrix.

Contrast rows: the `^{commit}`→`^{}` substitution is also missed by the old matrix but is the
tag-to-noncommit discriminator (preregistered `tag_to_tree`/`tag_to_blob`), not NestedTag's;
it is named here only to keep the two mutants distinct.

## 6. Git object-type invariant and oracle independence

Git stores four object types (commit, tree, blob, tag); `cat-file -t` reports the stored type
of the addressed object. A tag object's type is `tag` **regardless of chain depth** — nesting
is a property of the object graph (the `object` header inside each tag payload), not of any
selector or ref. `^{<type>}` peeling follows that graph to its terminal object. Hence for any
tag chain the invariant is: `cat-file -t` = `tag` ∧ terminal object = `commit` → peel yields
that commit. The oracle needs only the fixture's declared construction (TN→T→C, TN unique in
the inventory, C landed/pushed) to fix the expected outcome — accept, `revision` = C — plus the
source-verified JSON shape in §2. Nothing is derived by running or simulating `bind`'s
algorithm; the expected value is the constructor-fixed commit SHA, satisfying the "no binder
algorithm in the expected-output oracle" rule (`BindTagObject.md` §2 step 9 states the same
principle: expectations from construction, never from `object_commit`/`bind`).

## 7. Residual risk / limits

- All expectations are source-derived; no consumer, binder, or git command was executed.
  `merge-base` tag peeling is flagged [INFERENCE]; both branches of it yield a detectable
  failure for the peel-once mutant, so the verdict does not hinge on it.
- Refusal `detail` strings cite line-derived templates; exact truncation at 120 chars is
  code-verified but untested.
- The live `tools/_revision.py` matches the pinned snapshot tag byte-for-byte under this
  reader; no hash recomputation was performed (NO-EXEC). The Reviewed-SHA256 below is the
  preregistered binder digest.
- Scope restricted to this consumer/type pair as assigned; no other consumer asserted.
- No tool installed or updated in this seat; pacman pause respected; need: none.

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-source-scope-correction.py-NestedTag-expected-source-only
Scope: executed=none
