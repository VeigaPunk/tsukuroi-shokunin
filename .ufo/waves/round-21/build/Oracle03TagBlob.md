# Oracle03TagBlob — check-section-citations.py × annotated-tag-to-blob object selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-section-citations.py-TagBlob-expected-source-only
Lane bounds: leaf member — no subagent dispatch.

Pinned binder: `.ufo/waves/round-21/snapshot/tools/_revision.py` (SHA-256 supplied by the
item; not recomputed — NO-EXEC). Consumer: live `tools/check-section-citations.py`, read only
(no snapshot copy exists under `.ufo/waves/round-21/snapshot/`). Round-20 matrix: pinned
`.ufo/waves/round-21/snapshot/tools/check-revision-binding.py`.

## Axes
1. Exit class (0/1/2).
2. Finding identity and cardinality (id, site, count).
3. Full-SHA semantics (what the JSON `revision`/`branch_tip` fields carry).
4. Round-20 matrix coverage of this exact case.
5. Mutant sensitivity (smallest realistic weakening the old matrix misses).

## Case definition (TagBlob)
Selector = the object ID of an annotated tag object whose `object` header points to a blob
(`type blob`). Variants: full 40-hex, a unique ≥7-hex prefix, uppercase form. Branch `master`
valid and present; origin state irrelevant.

## Observed — consumer bind propagation (`tools/check-section-citations.py`)
- Line 36: `from _revision import RevisionError, bind` — the shared module, no local copy
  (no `{7,64}` regex, no `cat-file`/`tag`/`blob` logic anywhere in the file; grep for
  `tag|blob|cat-file|hash-object` returns zero matches).
- `main` lines 910–916: `branch = args.branch`; `revision = args.revision`;
  `bind(ROOT, args.revision, branch)` — argv passed verbatim, no strip/lower/normalize. The
  baseline `bind(ROOT, BASE, branch)` runs only after the revision bind succeeds.
- Lines 923–927: `RevisionError` → `Cannot(exc.fid, exc.site, exc.detail)` →
  `emit(Result(CANNOT, [one Finding], 0), revision, branch, branch_tip)` with `revision` still
  the raw argv string and `branch_tip` still `None` (both assigned only after `bind` returns).
- `emit` lines 394–402: JSON `{"status","revision","branch","branch_tip","correction_count",
  "scope","findings":[{id,site,detail}]}`, returns `result.code`; `sys.exit(main())`.
- `ROOT = Path(__file__).resolve().parents[1]`: binds the repository containing the tool file,
  not the cwd.
- Consumer `--selftest` has no tag, blob, or annotated-tag-to-blob vector (lines 801–856).

## Observed — pinned binder path for TagBlob (`_revision.py`)
1. `validate_branch("master")` passes.
2. `REV` (`^[0-9a-fA-F]{7,64}$`) passes for 40-hex / ≥7 prefix / uppercase.
3. `_object_commit`: `rev-parse --disambiguate=<lower>` lists objects only (refs are never
   consulted) → exactly one OID (the tag object) → `cat-file -t` = `tag` → peel
   `rev-parse --verify --quiet --end-of-options <oid>^{commit}` fails → `rev-parse --git-dir`
   succeeds → returns `None`.
4. `bind` raises `RevisionError(E-REVISION-INVALID, "revision", "<rev> does not name one commit")`.
   Steps 4–6 (branch-missing, not-landed, not-pushed) are never reached.
- Binder selftest (lines 413–419) already asserts `annotated-tag-to-blob-invalid` → E_INVALID,
  but by calling `bind()` directly, not through any consumer.

## Expected behaviour (stated before candidate outputs exist)
For every TagBlob variant against this consumer:
- Exit: 2 (CANNOT / could-not-evaluate). Never 0 or 1.
- Status: `CANNOT_EVALUATE`; `correction_count` 0.
- Findings: exactly one, `id = "E-REVISION-INVALID"`, `site = "revision"`,
  `detail = "<selector as typed> does not name one commit"`. No `E-GIT-FAILED`, no
  `E-BRANCH-*`, no `E-REVISION-NOT-*`, no `E-INTERNAL`, no section-citation finding (evaluation
  never runs; the BASE bind never runs).
- Full-SHA semantics: no commit SHA is emitted. `revision` echoes the selector byte-for-byte
  (prefix stays a prefix, uppercase stays uppercase — never expanded, lowered, or peeled);
  `branch_tip` is `null`. With a full 40-hex selector, the echoed value is the tag object's
  OID, which an oracle MUST NOT read as acceptance: acceptance is only exit≠2 with `revision`
  equal to an independently resolved 40-hex commit, and Git can never report this OID as a
  commit (see invariant).
- Ref shadows: a branch or lightweight tag named with the tag's hex and pointing at the landed
  tip does not change the outcome (still exactly one E-REVISION-INVALID), because object IDs
  are resolved before refs and refs are never a fallback.
- Nested tag→tag→blob: same outcome (`^{commit}` peels recursively and still ends at a blob).

## Independent oracle construction (no binder import)
Expected values come from Git plumbing facts about the fixture, not from `bind`:
create a blob (`hash-object -w`), annotate it (`tag -a <name> -m … <blob>` or `mktag`), read
the tag OID via `rev-parse refs/tags/<name>^{tag}`, and assert `cat-file -t <oid>` = `tag` and
`cat-file -p <oid>` carries `type blob`. The expected row is then a constant
(exit 2, `[E-REVISION-INVALID]`, count 1, `revision == selector`, `branch_tip is None`),
derived from the written contract (docstring rule 3: "uniquely matches an object ID, then
peels to a commit else E-REVISION-INVALID"), not from rerunning the binder's resolution steps.

## Git object type invariant
An object ID is the hash of `"<type> <size>\0<body>"`, so one OID has exactly one immutable
type. A blob has no outgoing object references; an annotated tag has exactly one `object`
target with a declared `type`. Peeling to `^{commit}` follows tag targets only, so a tag chain
ending in a blob can never yield a commit, regardless of refs, landedness, or origin state.
Hence TagBlob's expected outcome is fixed at rule 3 and is independent of every later check.

## Round-20 matrix coverage (pinned `check-revision-binding.py`)
`check-section-citations.py` is in `TOOLS` (line 64), so it receives `probe_tool` and, with
`--object-selectors`, `object_selector_probes`. Annotated-tag cases there all target the
commit tip: `annotated_tag_object`, `annotated_tag_prefix`, `full_tag_object_id_ref_shadow`
(accept → tip), `ghost_full_hex_annotated_tag` (tag *name*, refusal). Non-commit cases are the
raw blob only: `noncommit_blob` / `blob-revision` (→ E-REVISION-INVALID) and `git-failed`
(origin ref = blob → E-GIT-FAILED). No case creates an annotated tag whose target is a blob
(or tree). Verdict: the round-20 matrix does NOT cover TagBlob for this consumer.

## Smallest realistic weakening mutant the round-20 matrix misses
In `_revision._object_commit`, weaken the peel target from `f"{oid}^{{commit}}"` to
`f"{oid}^{{}}"` (peel to any non-tag object; a 7-character deletion).
- Tag→commit: still returns the commit → every round-20 annotated-tag accept case passes.
- Raw blob / tree: still rejected earlier by `object_kind != "tag"` → `noncommit_blob` passes.
- TagBlob: returns the blob OID as `sha`; `bind` proceeds to `_ancestor(blob, refs/heads/master)`,
  where `merge-base --is-ancestor` fails with rc ≥ 2 [INFERENCE: Git rejects a non-commit
  there, the same behaviour the matrix's `git-failed` case relies on] → `E-GIT-FAILED`, exit 2.
The exit class is unchanged, so an exit-only oracle also misses it. Only an exact-id TagBlob
oracle (`binding_ids == ["E-REVISION-INVALID"]`, count 1) catches it. A sibling mutant —
returning the tag `oid` itself when the peel fails — produces the same E-GIT-FAILED symptom and
is missed by the round-20 matrix for the same reason.

## Inferences / limits
- [INFERENCE] `rev-parse --verify --quiet <tag-to-blob>^{commit}` exits non-zero without
  reaching `rev-parse --git-dir` failure; consistent with binder selftest expectation
  `annotated-tag-to-blob-invalid` → E_INVALID, not observed by execution here.
- The consumer resolves `_revision` from its own directory at runtime. The expectation holds
  only when the `tools/_revision.py` materialised beside the consumer at the measured revision
  is byte-identical to the pinned snapshot; the live `tools/_revision.py` was not hashed
  (NO-EXEC).
- The consumer is a live, unpinned file; its bind call site (lines 36, 910–927) was read once
  and has no reviewed SHA in this item.
- No candidate outputs were read; no non-author closure or promotion is claimed.

Scope: executed=none
