# FxC2OracleWriteOnly — v2 edit authority against a write-only target

Target: `tools/check-seat-bindings.py` in the landed round-23 candidate tree
(`.ufo/waves/round-23/candidate/`), declared identity
`4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6` (supplied; not
independently computed). Method: static hand-derivation from the landed source only.
`executed=none` — no command, import, test, lint, hash, or fetch was run.

Attacked claim: **C2** (`preregister.json:36-44`), metric `structured_edit_mode`,
before 0, target 1, scope "New explicit schema-v2 audit authority for exact predeclared
structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body
data opaque, no native enforcement/effects claim." The decision row under test is
`WRITE_ONLY_EDIT` → `DENY` ("Edit also needs its explicit target read authority",
`preregister.json:72-76`). C1, C3 and the frontier are untouched by this seat.

## Verdict

No falsifier found under the literal claim. The landed selftest already contains the
equivalent control at both possible readings of the scenario (request-time denial and
declaration-time rejection), so no new fixture is required. Two bounded gaps remain that
constrain how the C2 metric may be read; neither contradicts the claim text.

## Hand-derivation

Scenario: a v2 binding where the edit request's target is present in `write_paths` and
absent from `read_paths`. Two distinct objects can carry that description, and the tool
treats them differently.

### A. Request-time target (the event path) — exit 1, `SCOPE-EDIT-DENIED`, mode 1

Binding: the landed selftest fixture (`check-seat-bindings.py:296-298`):

    target, other = LANE + '/drafts/A.md', LANE + '/drafts/B.md'
    v2 = {'schema': 'tsukuroi-seat-bindings-v2', 'seats': [{'name': 'A', 'root': LANE,
          'read_paths': [src, target, other, 'skill://godspeed'],
          'write_paths': [target, LANE + '/w-only.md'], 'edit_paths': [target],
          'commands': [], 'fetches': []}]}

Trace: one complete seat `A`/`agent-A` with one event
`{'tool': 'edit', 'args': {'path': LANE + '/w-only.md', 'stream_content': None}}`.
`/w-only.md` is in `write_paths`, absent from `read_paths`, absent from `edit_paths`.

1. `evaluate` (`:135-207`): `json`/dict input, `data['schema']` is
   `tsukuroi-seat-bindings-v2`, so `v2 = True` (`:147`).
2. Manifest validation: name/root/commands/fetches pass; `read_paths` and
   `write_paths` are non-empty, local, duplicate-free. Nothing in the path loop requires
   `write_paths ⊆ read_paths`. The v2 authority check (`:156-161`) validates only
   `edit_paths`; `[target]` is local and in both `read_paths` and `write_paths`, so it
   passes. The write-only path is therefore a *legal* manifest entry.
3. Trace validation passes; one seat bound, `complete: true`.
4. Event loop (`:184-193`) calls
   `classify('edit', args, binding, allow_structured_edit=True)` (`:186`).
5. `classify` (`:82-113`): `edit` is not in `('bash','eval','task')`, not a fetch tool;
   `tool == 'edit' and allow_structured_edit` → `classify_edit(args, binding)` (`:104`).
6. `classify_edit` (`:119-130`): `set(args) - {'i'} == {'path','stream_content'}`, which is
   `EDIT_SHAPES[0]` (`:116,121`); `path` is a non-empty string; it matches neither the
   `https?://` nor the `host:port` regex (`:126-127`); `value not in
   binding['edit_paths']` because `edit_paths == [target]` → returns
   `['SCOPE-EDIT-DENIED']` (`:128-129`).
   Observed: `classify_edit` never consults `read_paths` or `write_paths`. The denial is
   produced by `edit_paths` non-membership alone. The write-only property enters only
   indirectly: because the manifest check at `:160` forces every `edit_paths` entry to be
   in `read_paths`, a read-absent path can never be an edit target. The two checks agree
   by construction, not by a second runtime test.
7. `evaluate` accounting: `findings = [{'id': 'SCOPE-EDIT-DENIED', 'site': 'A:0'}]`;
   `violations = 1`; `incomplete = 0`; no `SCOPE-SCHEMA`. Disposition (`:198`):
   `code = 2 if ... else (1 if findings else 0)` → `1`. `request_audit_mode =
   int(code != 2) = 1`. `structured_edit_mode = int(code != 2) = 1` (`:205-206`).

Exact result object returned by `evaluate`:

    {"status": "FAIL", "request_audit_mode": 1, "seats_bound": 1, "requests_total": 1,
     "violations": 1, "incomplete_seats": 0, "missing_seats": 0,
     "present_incomplete_seats": 0,
     "seats": [{"name": "A", "agent": "agent-A", "requests": 1, "complete": true,
                "violations": ["SCOPE-EDIT-DENIED"]}],
     "findings": [{"id": "SCOPE-EDIT-DENIED", "site": "A:0"}],
     "scope": "Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness.",
     "structured_edit_mode": 1}

Process exit status: **1** (audit path returns `code` from `evaluate` via `main`,
`:388-395`). Exactly one finding ID, `SCOPE-EDIT-DENIED`, one site `A:0`.

Consequence for the mechanism: a write-only path is writable (`write` is gated only by
`write_paths`, `:107-109`) and readable-denied (`read` would yield `SCOPE-PATH-DENIED`)
and edit-denied. All three behaviors are independently declared.

### B. Declaration-time target (an `edit_paths` entry that is write-only) — exit 2, `SCOPE-SCHEMA`, mode 0

Same fixture, but the manifest declares `edit_paths = [LANE + '/w-only.md']`
(the literal landed mutation at `:326`). `v2 = True` is set before validation
(`:147`). At `:160`, `p not in seat['read_paths']` is true for that entry, so
`raise ValueError('v2 edit authority')` (`:161`); caught by the broad handler
(`:196-199`) → `add('SCOPE-SCHEMA', 'input')`, `code = 2`,
`bound = locals().get('bound', {})` (empty for a single-seat manifest, since
`bound[seat['name']] = seat` at `:162` is never reached).
Result: `status = CANNOT_EVALUATE`, `request_audit_mode = 0`, `seats_bound = 0`,
`requests_total = 0`, `findings = [{'id': 'SCOPE-SCHEMA', 'site': 'input'}]`,
`structured_edit_mode = int(2 != 2) = 0`. Process exit **2**. The whole manifest is
untrusted at that point: no seat is audited at all, not merely the bad one. For a
multi-seat manifest the failure lands at the first offending seat and `seats_bound`
reports only seats validated before it (`:162`); rows are never populated because the
audit loop at `:174-194` is not entered.

So the attacked path is not merely denied as an edit; declaring it as edit authority
invalidates the manifest. The `WRITE_ONLY_EDIT` decision is enforced in both directions.

## Selftest control check

Equivalent controls exist; no fixture has to be added.

- Request-time, literal (`:305`):

      v2case('v2-write-only-target', 'edit', {'path': LANE + '/w-only.md', 'stream_content': None}, 1, 'SCOPE-EDIT-DENIED')

  Default `mode=int(code != 2)=1` (`:301`), so the case asserts exit 1, that finding, and
  `structured_edit_mode == 1` — exactly the hand-derived tuple.
- Declaration-time, literal (`:326`):

      v2case('v2-edit-not-readable', 'read', {'path': src}, 2, 'SCOPE-SCHEMA', manifest=v2mut(lambda s: s.update(edit_paths=[LANE + '/w-only.md'])))

  Asserts exit 2, `SCOPE-SCHEMA`, and mode 0. Its complement, write-present/read-absent
  authority via a read-only path, is `v2-edit-not-writable` (`:327`).
- Corroborating neighbors: `v2-read-still-scoped` (`:319`) pins `read` on the same
  write-only path to `SCOPE-PATH-DENIED`; `v2-write-target` (`:320`) pins `write` on the
  edit target to exit 0; `v2-empty-edit-paths` (`:332`) pins edit denial with mode 1.

Boundary of the controls: there is no case that writes the write-only path itself
(`write` to `/w-only.md` expecting 0). The writable half of the asymmetry is therefore
asserted only for `target` (`:320`), not for the path that `v2-write-only-target` denies
as an edit. That is a control-completeness gap, not a claim violation.

## Falsifier search

Bounded search over the whole v2 decision surface: `classify` (`:82-113`),
`classify_edit` (`:119-130`), v2 manifest gate (`:155-161`), disposition and mode
(`:196-206`), the v2 selftest block (`:295-335`), the C2 and decision rows in
`preregister.json` (`:36-44`, `:56-76`), and the landed v2 build bindings
(`build/bindings.json:1-1316`, including the two seats named for this scenario,
`OracleEditWriteOnlyEdit` at `:249-267` and `OracleV2WriteOnly` at `:774-795`, whose
`edit_paths` equal their own report and thus never exercise a write-only edit target).

No input in that surface produces an allowed edit for a path absent from the seat's own
`read_paths` or `edit_paths`. Exact string membership against `edit_paths`, with every
`edit_paths` entry forced into `read_paths ∩ write_paths`, closes the alternate-spelling
routes the selftest enumerates at `:308`. Cross-seat borrowing is closed by per-seat
`binding` and duplicate-name/duplicate-agent rejection (`:150-166`). Prefix stripping
(`functions.`) is one level only and cannot reach `classify_edit` from a non-edit name.

Non-falsifier limits observed (report, do not promote to violations):

1. **The metric is schema-engagement, not edit coverage.** `structured_edit_mode` is
   `int(code != 2)` (`:206`), so 1 is reported for any evaluable v2 trace, including
   an all-read trace and including every denied-edit case (`:305`, `:326`, `:332` all
   yield mode 1). C2 target 1 is therefore reachable without a single allowed or even
   present edit event. The selftest deliberately pins this. The claim's literal text
   survives ("audit authority ... mode"), but a reading of `structured_edit_mode: 1` as
   "v2 edit authority was exercised/operable on an edit" is contradicted by the tool's
   own cases.
2. **`before: 0` is a normalization outside the tool.** Under a v1 manifest, `edit`
   yields `SCOPE-TOOL-UNKNOWN` and the result carries *no* `structured_edit_mode` key
   (`:205-206`, asserted at `:334-335`, `:348`), not `0`. The r22 baseline output is
   key-absent, so the before/after comparison must state that absent is being read as 0.
3. **Write channel is not gated by `edit_paths`.** `write` to any `write_paths` entry
   succeeds even when `edit_paths` is empty (`:107-109`, `:332`, `:320`). This does not
   falsify C2 — the v2 invariant is explicitly one-directional at `:156`
   ("every exact edit target is also literally readable and writable") — but it means
   `edit_paths` is not a necessary condition for mutation.
4. **Unauthorized-edit classes share one ID.** Write-only, read-only, undeclared, and
   traversal spellings all report `SCOPE-EDIT-DENIED` (or, at declaration, all
   `SCOPE-SCHEMA`). The preregister pins outcomes, not per-decision IDs, so this is not a
   defect against C2/C1 text; it does mean the audit output cannot be used to count the
   eight edit decisions individually.
5. **Malformed v2 JSON suppresses the mode key.** `v2` is assigned only after both
   `json.loads` calls (`:147-148`), so a v2-schema manifest with a duplicate key or a
   malformed events document yields `CANNOT_EVALUATE` with no `structured_edit_mode`
   field, unlike a v2 manifest rejected at validation, which yields `0`. Both are
   code 2; the difference is cosmetic but unpinned by any selftest case.

## Smallest in-scope remedy

One line, in the v2 selftest block, to pin the writable half of the attacked asymmetry:

    v2case('v2-write-only-write', 'write', {'path': LANE + '/w-only.md'}, 0)

This adds no new fixture (reuses the existing `v2` dict and `w-only.md`), is independent
of production manifests, and makes the write-only path's three-way behavior (write 0,
read 1, edit 1) self-asserting. Its expected mode is 1 under the same default at `:301`.
Optionally, one v2 case pinning `structured_edit_mode` for an empty-edit-authority trace
already exists (`v2-empty-edit-paths`, `:332`); the only documentation change needed is
recording that C2's target 1 means "schema-v2 evaluation ran", not "an edit was
audited". No production file was edited by this seat; the remedy is a handoff item for L1.

## Observed / inferred / unresolved

Observed: all source citations above, read directly from the landed candidate; the
selftest controls at `:305` and `:326`; the landed v2 schema and the per-seat
`edit_paths ⊆ read_paths ∩ write_paths` shape in `build/bindings.json` spot-checked at
`:1-70`, `:249-267`, `:774-795`, `:1297-1316`.

Inference: the general statement that every seat in `build/bindings.json` satisfies the
v2 authority invariant. The sampled seats do; the file was not exhaustively re-derived,
and no execution was permitted to validate it. If any seat violated it, `evaluate` would
exit 2 with `SCOPE-SCHEMA` and `structured_edit_mode: 0`, so the C2 measurement depends
on that invariant holding.

Unresolved: `build/events.json` is outside this seat's declared read paths, so whether
any landed event actually requests an edit on a write-only path is unverified. The
baseline commit's `check-seat-bindings.py` is likewise not in read scope, so "historical
reds unchanged" is confirmed only against the landed selftest's v1 assertions
(`:334-335`), not against the baseline source. No native per-seat restrictive tool
interface is claimed or observed; this report proves recorded-request classification
only, not runtime enforcement.

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2oraclewriteonly
Scope: executed=none
