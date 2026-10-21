# ScribeSources: S086 own-work A source-row draft (round 23)

Scope: read-only. No command, fetch, hash, list, or word count was run. The declared digest is recorded as supplied identity only.

## Inputs read
- `.ufo/waves/round-23/sources/structured-edit-observations.json` (read in full, raw). Schema `tsukuroi-structured-edit-observations-v1`, accessed 2026-10-21, four observation entries, `scope` field at line 101 of the default view.
- `.ufo/waves/round-23/preregister.json` (read in full, raw). Names S086 as "observed structured edit request keys and recorded adapter steps"; holds the eight-row `edit_decisions` table, the C1/C2/C3 claims, and `limits`.
- `.ufo/waves/round-23/sources/godspeed-directive.txt` and `skill://godspeed`. Directive text matches; no unsupported path.
- `.ufo/waves/round-23/sources/r22-closure.json` and `r22-rough-census.txt`: read for context only. They feed S085, not the S086 row.
- `.ufo/waves/round-23/build/ScribeSources.md` did not exist before this write.

## Draft S086 source row (not registered)
- id: S086
- kind: own-work A (as labeled in the assignment)
- title: Observed structured edit request keys and recorded adapter steps (round 22)
- locator: `.ufo/waves/round-23/sources/structured-edit-observations.json`
- declared sha256: `19d85129bf0f7fd71f5aea93c35660b21d305150500dc63b58104019851af12a` (supplied identity; not independently computed)
- accessed: 2026-10-21
- content basis: four observation entries from two round-22 seats: CritRuntime (1) and OraclePathArtifact (3). Each entry carries `transcript_sha256`, `request_line`, `call_id`, `tool`, `argument_keys`, `path`, and `recorded_starts`.
- body fields: recorded as "omitted; no report text copied". No edit body is in the source and none is copied here.
- located quote (20 words), at `scope` field, line 101: "Observed structured path metadata and recorded adapter steps only, not universal tool semantics, native permission enforcement, effects, or reading proof."

## Observed in the source (request shapes and adapter steps)
| # | seat | request_line | request tool | argument_keys | recorded_starts (line: tool) |
|---|------|--------------|--------------|---------------|------------------------------|
| 1 | CritRuntime | 15 | edit | path, stream_content | 12: read (path suffixed `:raw`); 13: write |
| 2 | OraclePathArtifact | 30 | edit | i, new_string, old_string, path | 31: edit |
| 3 | OraclePathArtifact | 33 | edit | i, new_string, old_string, path | 34: edit |
| 4 | OraclePathArtifact | 36 | edit | i, new_string, old_string, path | 37: edit |

Observed points, stated as recorded and not interpreted:
- The same request tool name `edit` appears with two argument-key shapes: `{path, stream_content}` (entry 1) and `{i, old_string, new_string, path}` (entries 2-4). The source records keys only, not values.
- Entry 1's recorded adapter steps are `read` then `write`. Entries 2-4 record one `edit` step each. The adapter step tool name does not uniformly mirror the request tool name.
- Entry 1's `read` step path carries a `:raw` selector suffix. The selector is part of the recorded path string.
- Entry 1's recorded starts (lines 12, 13) precede its `request_line` (15). Entries 2-4 each record their start on the line after the request. This ordering is recorded as-is; the source gives no reason for it.
- All four recorded paths sit under round-22 `build/` (`CritRuntime.md`, `OraclePathArtifact.md`).
- The source records no decision, permission outcome, or effect for any request.

## Separately authored (NOT observed; must not be attributed to the source)
- `preregister.json` `edit_decisions`: DECLARED_EDIT ALLOW; UNDECLARED_EDIT DENY; READ_ONLY_EDIT DENY; WRITE_ONLY_EDIT DENY; OPAQUE_PATCH UNKNOWN; EDIT_TRAVERSAL DENY; EDIT_EXTERNAL DENY; EXPANSION CHECK_EACH. These are policy authored for round 23.
- C1 target (8 validated decisions), C2 `structured_edit_mode` target (1, schema-v2 explicit audit authority), C3 target (0 unexplained cohorts). These are authored claims and targets.
- `preregister.json` `limits` (no native per-seat restrictive tool interface; no runtime prevention; no effect or reading proof; no round24).
- The v2 authority schema itself. It appears only in the preregister, not in the observations file.

The observations file cannot be used to show that any observed request was allowed or denied under the `edit_decisions` table. Nothing in it maps a request to an ALLOW, DENY, or UNKNOWN outcome.

## Narrowness of the draft row
The row supports only this claim: the source records four round-22 `edit` request records with the argument keys, tool names, paths, and recorded adapter starts listed above. It does not support enforcement, effects, universal tool semantics, authorization of any request, or reading proof. The source's own scope line disclaims all of these.

## Gaps
- The sha256 was taken as supplied and not verified, per the seat binding.
- Transcripts named by `transcript_sha256` were not opened (not declared for this seat).
- No registry row was created and no fetch was performed.
- The 20-word quote was counted by hand from the located text.

Reviewed-SHA256: 19d85129bf0f7fd71f5aea93c35660b21d305150500dc63b58104019851af12a
Predicate: r23-scribesources
Scope: executed=none
