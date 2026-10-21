# ExecEditAudit — round23 attempt1 seat report

Seat: TsukuroiR23-2.ExecEditAudit-7. Declared branch round23/ExecEditAudit at ae01e50f582016384e620022be38bf5367000e2e (supplied declaration; not independently verified — NO-EXEC seat). Scope: C2 operability, explicit v2 structured-edit audit authority for `tools/check-seat-bindings.py`. Target snapshot: `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py`, declared SHA256 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6 (supplied identity; never hashed).

## Files changed (draft worktree only; no production/VCS edits)

- `​.ufo/waves/round-23/worktrees/ExecEditAudit/draft/check-seat-bindings.py` — COMPLETE COPY of the 310-line snapshot gate, extended in place. Write result reported 28269 bytes. Standard library only; `sys.dont_write_bytecode = True` before `import _revision`; `--revision HEX / --branch master / --selftest` and the `_revision.bind` + `git_read` conventions reused unchanged.

## Behavior added (v2)

- Top-level manifest schema `tsukuroi-seat-bindings-v2` accepted alongside v1 (exact key set `{schema, seats}` unchanged). Legacy v1 classification, output shape, missing-manifest early return and argparse defaults are untouched.
- Per-seat mandatory `edit_paths` list under v2: every entry must be a canonical `local()` spelling, duplicates rejected, and the list must be an exact subset of both `read_paths` and `write_paths` (subset violation, duplicates, nonlocal spelling, or missing field → `SCOPE-SCHEMA`, exit 2). An empty list is valid and means "no edit authority" (documented interpretation; "mandatory" = key present and a list).
- `allow_structured_edit` flag is derived only from the validated top-level v2 schema string and threaded through `classify` recursion (parallel wrappers included). No binding-row, seat, or event-argument marker can enable it.
- `edit` classification when (and only when) the flag is set: argument key shapes exactly `{path, stream_content}` or `{path, old_string, new_string}`, each optionally with `i` (shapes grounded in `structured-edit-observations.json` `argument_keys`: `["path","stream_content"]` and `["i","new_string","old_string","path"]`). Unknown keys, mixed shapes, missing body fields, non-dict args, or a non-string/dict `path` value → `SCOPE-SCHEMA`. Body field values are opaque: presence/shape only, never interpreted (fixtures classify dict-valued `stream_content` and null `old_string`/`new_string` as clean). No generic tool/body semantics is claimed anywhere.
- Edit target resolution: `requested_path` first (http/https → `SCOPE-FETCH-DENIED`; dot-segment, dot-dot, double-slash, internal URIs such as `xd://tool`, colon-selector spellings → `SCOPE-PATH-DENIED`), then exact membership required in `edit_paths` AND `read_paths` AND `write_paths`; any other target → `SCOPE-EDIT-DENIED` (undeclared, prefix spellings like `report.extra`, `skill://godspeed`). `functions.edit` prefix stripping handled; `edit` stays `SCOPE-TOOL-UNKNOWN` under v1.
- `structured_edit_mode` appears only on v2-schema results: 1 on fully evaluated exits 0/1, 0 on exit 2. v1 results, unsupported schemas (e.g. v3), and missing manifests keep the legacy output shape — the field is absent there, which is the only representation compatible with "legacy v1 output unchanged"; v2 code-2 results carry the explicit 0.
- Native extra read/write starts around a structured edit (`recorded_starts`) are not modeled: existing per-event read/write audits remain their independent authority (policy EXPANSION = CHECK_EACH).
- Policy mapping to `edit-decision-policy.json`: DECLARED_EDIT → clean; UNDECLARED_EDIT / READ_ONLY_EDIT / WRITE_ONLY_EDIT → `SCOPE-EDIT-DENIED` (subset validation makes read-only or write-only edit authority unreachable in any valid v2 binding); OPAQUE_PATCH (missing structured target) → `SCOPE-SCHEMA` / CANNOT_EVALUATE, never inferred from body text; EDIT_TRAVERSAL → `SCOPE-PATH-DENIED`; EDIT_EXTERNAL → `SCOPE-FETCH-DENIED` / `SCOPE-PATH-DENIED`.

## Selftest (independent, literal, in-memory; NOT run — NO-EXEC)

- All 73 v1 controls retained with byte-identical expected exits and IDs (old v1 results unchanged; v1 seat carrying an extra `edit_paths` field and a forged `allow_structured_edit` argument marker both remain `SCOPE-TOOL-UNKNOWN`, exit 1 — no grant through v1 extra fields, no forged-row marker).
- 35 new v2 fixtures with exact expected exits, finding IDs and `structured_edit_mode` (None = field absent): 9 positive (stream, patch, both with `i`, qualified, two opaque-value cases, parallel and doubly nested parallel edit — flag proven through recursion), 10 authority denials exit 1 (`SCOPE-EDIT-DENIED`: undeclared target, prefix, skill, empty edit_paths, parallel-denied; `SCOPE-PATH-DENIED`: dot, traversal, internal URI, selector spelling; `SCOPE-FETCH-DENIED`: URL), 13 shape/validation cases exit 2 mode 0 (unknown key, mixed shape, missing replacement, unstructured target, nested dict path, malformed-then-Bash continuation, incomplete trace, subset-read, subset-write, duplicate, nonlocal, missing field), 4 mode-absent cases (v3 schema, missing manifest, v1 continuity pair). Expected aggregate at integration: `PASS, cases: 108, failed: 0`.

## Retained evidence

- Read in full: snapshot `check-seat-bindings.py` (310 lines), `snapshot/tools/_revision.py`, `sources/structured-edit-observations.json`, `sources/edit-decision-policy.json`, `preregister.json` (C2 claim, edit_decisions, limits), `skill://godspeed`.
- Written: the draft file named above and this report. No other filesystem, Git, route, or host state touched. Zero commands executed, zero fetches (declared empty lists honored): the supplied digest was not computed and the selftest was not run.

## Risks

- The draft was never executed, imported, or compiled (seat scope): syntax and the 108 fixture expectations are grounded in the read source, not a run. L1 integration should run `python3 tools/check-seat-bindings.py --selftest` (expect exit 0, cases 108, failed 0) and the C2 command `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`.
- `--manifest`/`--events` defaults still point at the round-22 build paths, unchanged from the snapshot tool; the C2 command template always passes explicit round-23 paths, so this is legacy-behavior preservation, not a gap.
- Interpretations flagged for review: flat recorded argument shape for "dictionary target path"; `structured_edit_mode` absent (reads as 0) rather than literal 0 on v1/missing-manifest results; empty `edit_paths` allowed; prefix-spelling denial id `SCOPE-EDIT-DENIED` versus spelling-level `SCOPE-PATH-DENIED`.

## Blockers

None.

Reviewed-SHA256: 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6
Predicate: r23-execeditaudit
Scope: executed=none
