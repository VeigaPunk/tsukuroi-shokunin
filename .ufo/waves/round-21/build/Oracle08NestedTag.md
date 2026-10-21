# Oracle08 — NestedTag object-ID selector, source-only expected behavior

Consumer: `tools/check-recheck-commands.py` (original-nine member via `R17_GATES` at
`check-revision-binding.py:71-79`). Shared binder: pinned snapshot
`.ufo/waves/round-21/snapshot/tools/_revision.py`.
Scope: this one consumer/type pair only. No execution; observations cite source lines.

## Axes

- **A1 Semantic completeness** — expected exit / finding / `revision`-field semantics per
  NestedTag sub-case before any candidate output exists.
- **A2 Matrix coverage** — does the pinned round-20 `check-revision-binding.py`
  `--object-selectors` matrix instantiate this case.
- **A3 Mutant sensitivity** — smallest realistic binder weakening the matrix cannot catch.
- **A4 Oracle independence** — expectation derived from the Git object-type/revision-syntax
  invariant, not by importing the binder algorithm.

## Consumer wiring (observation)

- `:54-55` `sys.dont_write_bytecode = True; import _revision` — shared binder, no local copy.
- `:918` `binding = _revision.bind(repo, args.revision, branch)`; `:919-921` `RevisionError`
  propagates verbatim as `Cannot(exc.fid, exc.site, exc.detail)`; `:920` refusal path also
  calls `_revision.branch_tip(repo, branch)` for the `branch_tip` field.
- `:922` success unpacks `binding.sha / branch_tip / origin_tip`; `:923-926` that `sha`
  feeds `expand_paths`/`read_git` as `{sha}:{path}` (`:813,:847`); `:965` `emit` writes
  JSON `"revision": sha` (`:775`).
- `Cannot` → `emit("CANNOT_EVALUATE", sha or args.revision, branch, tip, [Finding...])`
  (`:930-934`); on a bind refusal `sha` is still `None`, so `revision` echoes the
  requested selector. `origin_tip` remains `None` on refusal (`:914,:933-934`).
- `emit` maps status → exit 0 PASS / 1 FAIL / 2 CANNOT_EVALUATE (`:795`).
- CLI contract: `--revision` help "7-64 hex commit; HEAD/@/refs are rejected" (`:882-884`),
  `--branch` default `master` (`:892`).

## Pinned binder semantics relevant to NestedTag (observation)

- `REV` admits 7–64 hex, upper-hex accepted (`:41,:175`); `bind` order is `validate_branch`
  → `REV.fullmatch` → `_object_commit` → ancestor gates (`:174-192`). A selector that is
  not exactly one object → `None` → `E-REVISION-INVALID` (`:123-124,:178-179`).
- `_object_commit` (`:112-146`): `rev-parse --disambiguate=<rev.lower()>` enumerates
  **objects**, not refs; `cat-file -t` types the unique result; `commit` → that oid;
  `tag` → `rev-parse --verify --quiet <oid>^{commit}` and the printed sha is returned;
  peel failure in a readable repo → `None` → `E-REVISION-INVALID`.
- `^{commit}` is Git's recursive type-peel: it dereferences tag objects until a commit is
  reached. For tag₂ → tag₁ → commit C the binder returns **C's full SHA-1**, and the
  ordinary landed/pushed ancestor gates then apply to C (`:184-190`).

## Expected source-only behavior — `check-recheck-commands.py --revision <nested-tag selector>`

Fixture model: master tip T, origin ref pinned or absent per case; nested annotated tag N
(tag→tag→C) present in the object database; selector is N's full 40-hex or a unique ≥7-hex
prefix; no ref literally named that hex.

1. **Peel target landed and pushed** — accept: exit 0 or 1 (file-evaluation verdict,
   never 2); JSON `revision` = the resolved commit's full 40-hex SHA-1 — never the tag
   object ID, never the input prefix or uppercase form; `status` PASS|FAIL, `branch_tip` =
   master tip, `origin_tip` = origin tip or `null` when `refs/remotes/origin/master` is
   absent; exactly the findings `evaluate` produces.
2. **tag→tag→unlanded commit U** — CANNOT_EVALUATE (exit 2), single finding
   `E-REVISION-NOT-LANDED`, `revision` echoes the requested selector, `branch_tip` = master tip.
3. **tag→tag→non-commit (blob/tree)** — `^{commit}` fails → CANNOT_EVALUATE,
   `E-REVISION-INVALID`, selector echo.
4. **Landed-but-unpushed target** (origin lagging) — CANNOT_EVALUATE,
   `E-REVISION-NOT-PUSHED`.
5. **Ambiguous prefix** (nested tag + any other object sharing it) —
   `E-REVISION-INVALID` (`len(objects) != 1` precedes typing, so the tag's peelability
   does not rescue a collision; binder `:115-124`).
6. **Ref shadowing** — hex-named `refs/heads|refs/tags` colliding with the selector do
   not divert it: disambiguation consults objects only; same verdicts as 1–4
   (binder selftest `:321-325,:368-377`; matrix shadow rows `:606-626`).
7. **Uppercase selector** — same as lowercase (`REV` allows A-F; disambiguate lowercases).
8. **<7 hex / non-hex / non-string** — `E-REVISION-INVALID` at the `REV` gate, before any
   object lookup.

## Does the pinned round-20 matrix cover this case? — No

- `object_selector_probes` creates exactly one annotated tag: `tag -a <name> <tip>`
  (`:502-505`) — **depth-1 tag→commit only**. Tag-ID probe rows:
  `annotated_tag_object` (`:631`), `annotated_tag_prefix` (`:632`),
  `full_tag_object_id_ref_shadow` (`:622`), plus ghost/tag-ref-shadow refusal rows.
  No `tag -a … <tag_object>` step exists anywhere in `:475-673`; no `tag→tag` fixture is
  ever built, so no case name corresponds to NestedTag.
- The matrix's independent oracle `object_commit` (`:139-166`) models disambiguate →
  `cat-file -t` → `^{commit}` peel correctly and *would* predict the nested-tag accept,
  but nothing instantiates the fixture. Matrix also lacks a depth-1 **tag→non-commit**
  peel-failure row (`noncommit_blob` `:633` selects the blob object directly, not
  tag→blob; binder selftest covers that at `:413-419`).
- The binder's own selftest does pin nested tag at unit level (`:362-365`
  `peel-nested` → `bind(...).sha == tip`), confirming the intended invariant — the gap is
  specifically the consumer-level matrix not propagating it.
- Context limit: `object_selector_probes` runs only under `--object-selectors`
  (`:815,:704-724`); a NestedTag row would be additive to that optional lane.

## Smallest realistic weakening mutant the matrix misses

**Single-hop tag peel.** Replace the recursive peel at `_revision.py:139-140`
(`rev-parse <oid>^{commit}`) with a one-level dereference — e.g. parse the `object`
header of `git cat-file -p <oid>` and return that target only when its `cat-file -t`
is `commit`, else `None` (equivalently `<oid>^{tag}` then commit-type check).

- Depth-1 matrix rows unchanged: `annotated_tag_object`/`annotated_tag_prefix`/
  `full_tag_object_id_ref_shadow` still resolve to T and are accepted; commit/blob
  branches are decided before the peel; all refusal rows still refuse.
- Divergence confined to tag→tag: target type is `tag`, mutant returns `None` →
  `E-REVISION-INVALID` + selector echo, where the true spec accepts with
  `revision` = the full commit SHA. Nothing in the matrix observes this.
- Contrast (caught, for calibration): a mutant returning the tag oid itself as `sha`
  *is* caught — `exact_accept` requires `json_revision == expected_sha` (`:403-404`)
  and `tag_oid != tip`. The missed mutant must preserve the correct depth-1 output;
  single-hop peel is the minimal such weakening.

## Git object-type invariant and oracle independence

A hex selector names an **object**, never a ref: `rev-parse --disambiguate=<prefix>`
enumerates objects in the database by prefix regardless of same-named refs; the object's
type is an intrinsic property (`cat-file -t` ∈ commit|tree|blob|tag); `^{commit}` is a
recursive type-peel that collapses *chains* of tag objects to the terminal commit, failing
when the chain terminates in a non-commit. The expected-output oracle is therefore: unique
object → `commit` ⇒ itself; `tag` ⇒ terminal commit of the peel chain; `tree`/`blob`,
non-unique, or absent ⇒ invalid. Nested tag adds no new rule — it is the same recursive
peel applied twice. An oracle implementing this invariant directly (as the matrix oracle
does at `:139-166`) stays independent of the binder under test; one importing
`_revision._object_commit`/`bind` would certify nothing, and one hard-coding the matrix's
depth-1 fixtures would inherit exactly the gap above.

## Findings

- **Medium** — Pinned `check-revision-binding.py --object-selectors` matrix contains no
  nested-tag (tag→tag→commit) row for any original-nine tool including
  `check-recheck-commands.py`; a single-hop-peel regression in the shared binder (or a
  consumer reimplementation) ships undetected by this matrix.
- **Low** — Same matrix lacks even a depth-1 tag→non-commit peel-failure row, so the
  `E-REVISION-INVALID`-on-failed-peel branch (`:143-145`) is consumer-unprobed.
- **Informational** — Canonical binder selftest already pins NestedTag
  (`_revision.py:362-365`); `check-recheck-commands.py` binds through the shared module
  verbatim, so its correct expected behavior is fully determined by that pinned source.
  No defect in either file for this pair; the risk is coverage, not implementation.

## Limits

- NO-EXEC source review; no git commands run. The recursive-peel behavior of `^{commit}`
  is stated from the Git revision-syntax contract and corroborated by binder selftest
  intent (`:362-365`), not re-verified by execution. [INFERENCE]
- Acceptance semantics describe binding only; PASS/FAIL of the file-evaluation gate is
  orthogonal to selector kind.
- Report covers only this consumer/type pair; no closure or promotion claims beyond it.

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-recheck-commands.py-NestedTag-expected-source-only
Scope: executed=none
