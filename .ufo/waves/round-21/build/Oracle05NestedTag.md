# Oracle05NestedTag — measure-update-recheck.py × NestedTag object-ID selector

Axes: exit-semantics, finding-fidelity, sha-echo (selector vs resolved commit), old-matrix coverage, mutation-sensitivity, oracle-independence.

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: measure-update-recheck.py-NestedTag-expected-source-only

## 1. Consumer bind-path confirmation (read-only inspection)

- `tools/measure-update-recheck.py:34` does `import _revision` (with `sys.dont_write_bytecode`, line 33).
- `load(rev, branch)` (lines 471–481): the only `--revision` gate is `_revision.bind(ROOT, rev, branch)` at line 476. The consumer's own `HEX64` (line 51) validates the record's snapshot-digest field, not the revision; no local `{7,64}` revision copy exists.
- `_revision.RevisionError` is wrapped verbatim into `Cannot(exc.fid, exc.site, exc.detail, revision=rev, tip=_revision.branch_tip(ROOT, branch))` (lines 477–479); `main` catches `Cannot` and emits `CANNOT_EVALUATE` with exactly one `Finding` (lines 769–772). `emit` returns `PASS=0` only for `COUNTED`/`ABSENT`, else `CANNOT=2` (lines 36, 434). No exit-1 path exists.
- On success the peeled `binding.sha` drives both `git show <sha>:<path>` reads (lines 480–481) and becomes the payload `"revision"` (line 760 → emit 412–434); `"branch"` and `"branch_tip"` ride along.

## 2. Pinned binder semantics for a tag→tag→commit object ID

`_revision.py` (snapshot SHA above), `bind` lines 172–192 → `_object_commit` lines 112–146:

1. `validate_branch` first (E-BRANCH-INVALID precedence), then `REV.fullmatch` (7–64 hex) else E-REVISION-INVALID.
2. `rev-parse --disambiguate=<sel.lower>`; unique result required, else INVALID.
3. `cat-file -t <oid>`; `commit` → return oid; non-tag → INVALID; `tag` → peel.
4. Peel: `rev-parse --verify --quiet --end-of-options <oid>^{commit}` — `^{commit}` dereferences **transitively** through every tag level to the terminal commit; peel failure in a readable repo → None → E-REVISION-INVALID; repo unreadable → E-GIT-FAILED.
5. `merge-base --is-ancestor <sha> refs/heads/<branch>` → E-REVISION-NOT-LANDED (rc 1); rc ≥ 2 → E-GIT-FAILED. Existing `refs/remotes/origin/<branch>` non-ancestor → E-REVISION-NOT-PUSHED.

## 3. Expected source-only outcomes (pre-registered before candidate outputs)

Let S = full 40-hex or unique ≥7-hex prefix of annotated tag object T2, T2→T1, T1→commit C.

- **C landed and pushed (or no origin ref):** exit 0; status `ABSENT` (record and snapshot both absent at C) or `COUNTED`; payload `"revision"` == lowercase full 40-hex sha(C) — never the tag oid, never the requested selector; `"branch"` == `"master"`; `"branch_tip"` == branch tip oid; `findings` == `[]`.
- **C not ancestor of `refs/heads/master`:** exit 2, `CANNOT_EVALUATE`, exactly one finding `E-REVISION-NOT-LANDED`.
- **Origin ref exists, C not ancestor of it:** exit 2, single finding `E-REVISION-NOT-PUSHED`.
- **Peel chain ending tree/blob (tag→tag→non-commit):** exit 2, single finding `E-REVISION-INVALID`.
- Any refusal: `findings` has exactly one entry (single-finding contract), and `"revision"` echoes the requested selector string verbatim (`exc.revision = rev`, line 478).

## 4. Old round-20 matrix coverage for this pair — NOT covered
In the same pinned `tools/check-revision-binding.py`:

- `probe_tool` (416–472): only tag-adjacent case is `blob-revision` (noncommit blob → INVALID). No tag-object selector at all.
- `object_selector_probes` (`--object-selectors`, 475–673): every tag selector is a **single-level** annotated tag→tip commit — `annotated_tag_object`, `annotated_tag_prefix`, `full_tag_object_id_ref_shadow` — plus ghost/ref-shadow ref-name cases. **No tag→tag→commit selector exists in the old matrix.**
- The new opt-in `--object-target-types` matrix (parser 919–920, dispatch 1381–1399; `target_type_probes` 676–736) is the only NestedTag coverage: `nested_tag_to_commit` builds `tag(tag→commit)` (line 702), exercises full object ID + unique prefix, expects commit `tip`, graded by `accepted()` — exit ≠ 2 and JSON `revision` == tip (396–404). It is not in the default run.

## 5. Smallest realistic weakening mutant the old matrix would miss

Replace the transitive peel `f"{oid}^{{commit}}"` (line 139) with a **single-level** dereference — read the tag object's `object` header and accept only when the immediate target's `cat-file -t` is `commit`. Every old-matrix tag case is single-level tag→commit, so all old cases still pass (blob/tree → INVALID preserved, sha echo correct). `nested_tag_to_commit` silently flips from accepted-with-sha(C) to an `E-REVISION-INVALID` refusal; only the new matrix detects it. Mutants that break single-level peeling (rejecting `tag` kind, returning the tag oid as sha, `^1`/`~1` parent) are already caught by `annotated_tag_object`/`annotated_tag_prefix`.

## 6. Why the oracle must not import the binder

The judge keeps an independent `object_commit` reimplementation (lines 139–166) precisely so a binder mutation cannot mutate the expected answers. Ground truth is the Git object-type invariant, not the binder: exactly four object types (blob/tree/commit/tag); a tag object's `object` header may name any type including another tag; `^{commit}`/`^0` peel transitively to the terminal commit and fail iff the chain ends tree/blob; a 40-hex object ID is content identity independent of any ref naming it. Expected results in §3 follow from that invariant alone.

Limits: source-only derivation; `^{commit}` transitivity assumed per gitrevisions(1) semantics; nothing executed (NO-EXEC).

Scope: executed=none