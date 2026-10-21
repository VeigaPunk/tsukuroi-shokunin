# OracleV2WriteOnly — C2 v2 write-only edit authority

Root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Source-only; no command, no import, no hash, no
checker run. Digest `8fccb655…04b6` is the supplied declaration of the reviewed checker.

## Question answered

"Edit authority lacks required read authority" — is the shipped gate defective, or does it simply lack
the v2 capability? Sources read: `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py`,
`.ufo/waves/round-23/preregister.json`, `.ufo/waves/round-23/sources/edit-decision-policy.json`,
`.ufo/waves/round-23/sources/structured-edit-observations.json`.

## Observed facts (source)

F1. Gate self-description, lines 1–2 and 15: `"""Audit recorded requests against frozen prompt scopes;
not preventive enforcement."""`; `SCOPE = 'Recorded request spellings only; not runtime prevention,
symlink/effect proof, reading proof or universal trace completeness.'`

F2. The tool-kind allowlist has no edit kind, lines 72–73:
`if tool not in ('read', 'grep', 'glob', 'write', 'multi_tool_use.parallel', 'parallel'): return
['SCOPE-TOOL-UNKNOWN']`. Selftest pins the behavior at line 199: `case('unknown', 'edit', {}, 1,
'SCOPE-TOOL-UNKNOWN')`.

F3. The per-tool argument-key table (lines 89–94) has no `edit` entry; `write` admits exactly
`{'i','path','content'}`. `unknown_keys` (line 95) is only reached after the tool-kind gate, so an edit
payload's extra keys are never examined.

F4. The binding schema is `tsukuroi-seat-bindings-v1` with top-level key set exactly `{'schema','seats'}`
(line 120). The seat loop validates only `read_paths` and `write_paths` (lines 126–129). No `set(seat)`
check exists, so a seat key such as `edit_paths` is neither validated nor rejected: it is silently carried
and never consulted. There is also no disjointness or coupling requirement between read and write lists.

F5. Write authority is single-class and read-independent, line 105:
`elif path not in binding['write_paths' if tool == 'write' else 'read_paths']`. Selftest lines 187, 212 and
213 pin the asymmetry: `write-exact` (write on `write_paths`) → 0; `read-write-only` (read on
`write_paths`) → `SCOPE-PATH-DENIED`; `write-read-only` (write on `read_paths`) → `SCOPE-PATH-DENIED`.
Nothing in v1 requires a write target to also be readable.

F6. External/URI handling is two-valued, lines 46–49: `http(s)://` and `host:port/` → `SCOPE-FETCH-DENIED`;
`skill://godspeed` is exempt for **reads**; every other non-local spelling falls through `local()` (lines
33–36) to `SCOPE-PATH-DENIED`. There is no distinct "external edit target" class and no edit selector
policy: selectors are parsed only `if selector and ':' in value` with `selector=tool in ('read','grep')`
(lines 50, 100), so writes and any future edit never get selector parsing.

F7. Preregister v2 declaration, lines 38–43: C2 metric `structured_edit_mode`, `before 0`, `target 1`,
command `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json
--events .ufo/waves/round-23/<WAVE>/events.json`, scope "New explicit schema-v2 audit authority for exact
predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data
opaque, no native enforcement/effects claim."

F8. Preregister `edit_decisions` (line 56 onward) and the mirrored `sources/edit-decision-policy.json`
declare eight rows: `DECLARED_EDIT/ALLOW` ("predeclared for edit and for both read and write"),
`UNDECLARED_EDIT/DENY` ("No implicit edit permission from generic report ownership"),
`READ_ONLY_EDIT/DENY` ("Read authority never grants a write"), `WRITE_ONLY_EDIT/DENY` ("Edit also needs its
explicit target read authority"), `OPAQUE_PATCH/UNKNOWN`, `EDIT_TRAVERSAL/DENY`, `EDIT_EXTERNAL/DENY`,
`EXPANSION/CHECK_EACH`. Policy scope: "Declared audit authority for structured target metadata only".

F9. S086 observations record two literal edit argument-key shapes and body omission:
`["path","stream_content"]` (CritRuntime, r22 build report, request line 15; preceding starts: `read`
line 12 on same path `:raw`, `write` line 13) and `["i","new_string","old_string","path"]`
(OraclePathArtifact, three requests at lines 30/33/36, each with only itself in `recorded_starts`).
`body_fields` is `"omitted; no report text copied"`. Scope disclaims effects and reading proof.

F10. This seat's own binding is a live v2 instance: the report path appears in `read_paths`, `write_paths`
and `edit_paths` alike, i.e. the DECLARED_EDIT triple.

## Verdict: capability absence, not a defect in historical policy

- v1 never claims edit authority. It classifies an edit request as `SCOPE-TOOL-UNKNOWN` at the tool-kind
  gate (F2) before any path is examined (F3), and its published scope disclaims universal tool semantics
  (F1). A defect would require v1 to emit ALLOW for a write-only edit; it cannot reach any ALLOW row for
  edit, because edit is rejected on tool identity.
- v1 cannot even read a v2 document: schema equality with `tsukuroi-seat-bindings-v1` is enforced at line
  120, and any added top-level authority key raises `SCOPE-SCHEMA`. Loading round-23 bindings through the
  unmodified gate is therefore CANNOT_EVALUATE by construction, not a policy contradiction.
- `edit_paths` in a v1 manifest is invisible (F4): accepted without validation, never indexed. So the
  manifest cannot state "edit but no read" in a way the old gate can observe; the corresponding event can
  only be `SCOPE-TOOL-UNKNOWN`.
- The residual risk is normalization, not v1 policy: since v1's write row is read-independent (F5), a
  recorder that labels a structured edit as `write` yields ALLOW on a write-only path. v2 must therefore
  key on recorded tool spelling `edit` and must not derive edit authority from `write_paths`.
- S086 does not resolve the historical cases (F9): body is omitted and OraclePathArtifact's edit starts do
  not record an earlier read of the edited path. Reading authority for those r22 edits is unestablished,
  which is exactly why v2 needs an explicit declared triple rather than retroactive inference.

## Exact v2 policy expectation

Identity: new schema (tombstone `tsukuroi-seat-bindings-v2` is a naming inference from the v1 literal plus
preregister's "schema-v2"; the preregister itself does not spell the tombstone). Seat fields keep
`name/root/read_paths/write_paths/commands/fetches` with v1 constraints, plus `edit_paths`. `edit_paths`
must be a unique list of `local()`-valid absolute paths; absence or empty list means **no** edit authority
(never inferred from `write_paths` or report ownership). Inheritance: v2 additionally rejects an `edit` on
`skill://godspeed` with EDIT_EXTERNAL even though that spelling stays a valid *read*.

Decision total order per recorded edit event, applied to the structured `path` only:

| Order | id | Condition | Verdict | Required finding |
|---|---|---|---|---|
| 1 | `EDIT_EXTERNAL` | `http(s)://`, `host:port/`, or any non-local/internal scheme (`xd://`, `artifact://`, `skill://…`, `ssh://…`) | DENY | `EDIT_EXTERNAL` |
| 2 | `EDIT_TRAVERSAL` | empty/`.`/`..` segment, `//`, backslash, control char, `*?[];:`, or any spelling/value not byte-equal to a declared entry (selectors such as `:raw` included) | DENY | `EDIT_TRAVERSAL` |
| 3 | `OPAQUE_PATCH` | edit args carry no string `path` at all (patch/diff text only) | UNKNOWN | `OPAQUE_PATCH` |
| 4 | `WRITE_ONLY_EDIT` | `path ∈ edit_paths`, `path ∉ read_paths` | DENY | `WRITE_ONLY_EDIT` |
| 5 | `READ_ONLY_EDIT` | `path ∈ read_paths`, `path ∉ edit_paths` and `path ∉ write_paths` | DENY | `READ_ONLY_EDIT` |
| 6 | `UNDECLARED_EDIT` | `path ∉ edit_paths` after order 5 (covers `read+write` report ownership without edit) | DENY | `UNDECLARED_EDIT` |
| 7 | `DECLARED_EDIT` | `path ∈ read_paths ∩ write_paths ∩ edit_paths` | ALLOW | none |

Notes on the table:
- Row 4 is the ticket's headline: edit authority present but read authority absent → DENY
  `WRITE_ONLY_EDIT`; row 6 covers its dual, read+write without any edit declaration (preregister reason:
  "No implicit edit permission from generic report ownership").
- `UNKNOWN` is a third outcome, not a deny: it must be emitted as `OPAQUE_PATCH`, must not be counted as
  ALLOW, and must not print `PASS`. Projecting UNKNOWN to exit 2 / `CANNOT_EVALUATE` mirrors v1's
  non-decidable code path (line 160) — this projection is [INFERENCE]; the preregister fixes only the
  verdict string.
- Missing-path handling must be split: non-string/empty `path` key present → `SCOPE-SCHEMA`; no path key →
  `OPAQUE_PATCH`. Adding `edit` to `allowed_keys` without this split routes opaque patches through the
  generic `raise ValueError('missing explicit path')` (v1 lines 84–86) and wrongly reports schema failure.
- Allowed edit argument keys, exact sets per S086: `{'i','path','old_string','new_string'}` and
  `{'path','stream_content'}`; body values opaque. Other key sets → `SCOPE-SCHEMA`.
- Per-event non-edit rows are unchanged from v1: `write` → membership in `write_paths` only; `read/grep/glob`
  → membership in `read_paths` only; `bash/eval/task` → `SCOPE-EXEC-DENIED`; fetch tools → `SCOPE-FETCH-DENIED`.
- `EXPANSION/CHECK_EACH`: each `multi_tool_use.parallel` child is classified independently with the same
  binding; no aggregate allow, and no de-duplication of per-child findings.
- Output must expose the preregister metric literally: `structured_edit_mode: 1` for a v2 run (`0`/absent
  for v1), alongside `request_audit_mode: 1`; v1 manifests must keep byte-identical v1 rows and exits.

## Independent literal fixture (declarative; never executed)

Independent of the checker's selftest fixture (`/source`, `/report`) and of this seat's own binding.
Paths abbreviated with `$ROOT` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

```json
{
  "schema": "tsukuroi-seat-bindings-v2",
  "seats": [
    {
      "name": "EditAuthorityFixture",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FxReadAllowed.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FxDeclared.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FxReportOnly.md"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FxWriteOnly.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FxDeclared.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FxReportOnly.md"
      ],
      "edit_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FxWriteOnly.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FxDeclared.md"
      ],
      "commands": [],
      "fetches": []
    }
  ]
}
```

Event trace (one seat, `complete: true`, events in order; `$W` = `$ROOT/.ufo/waves/round-23/build`):

| # | tool | args | Expected v2 | Expected v1 (snapshot tool) |
|---|---|---|---|---|
| 0 | `edit` | `{"i":"e0","path":"$W/FxWriteOnly.md","old_string":"a","new_string":"b"}` | DENY `WRITE_ONLY_EDIT` | `SCOPE-TOOL-UNKNOWN` |
| 1 | `write` | `{"i":"e1","path":"$W/FxWriteOnly.md","content":"x"}` | ALLOW | ALLOW (identical) |
| 2 | `read` | `{"i":"e2","path":"$W/FxWriteOnly.md"}` | DENY `SCOPE-PATH-DENIED` | DENY (identical) |
| 3 | `edit` | `{"i":"e3","path":"$W/FxReadAllowed.md","old_string":"a","new_string":"b"}` | DENY `READ_ONLY_EDIT` | `SCOPE-TOOL-UNKNOWN` |
| 4 | `edit` | `{"i":"e4","path":"$W/FxDeclared.md","old_string":"a","new_string":"b"}` | ALLOW (`DECLARED_EDIT`) | `SCOPE-TOOL-UNKNOWN` |
| 5 | `edit` | `{"i":"e5","path":"$W/FxDeclared.md:raw","old_string":"a","new_string":"b"}` | DENY `EDIT_TRAVERSAL` | `SCOPE-TOOL-UNKNOWN` |
| 6 | `edit` | `{"i":"e6","path":"$W/../build/FxDeclared.md","old_string":"a","new_string":"b"}` | DENY `EDIT_TRAVERSAL` | `SCOPE-TOOL-UNKNOWN` |
| 7 | `edit` | `{"i":"e7","path":"https://example.invalid/fx.md","old_string":"a","new_string":"b"}` | DENY `EDIT_EXTERNAL` | `SCOPE-TOOL-UNKNOWN` |
| 8 | `edit` | `{"i":"e8","path":"xd://ast_edit"}` | DENY `EDIT_EXTERNAL` | `SCOPE-TOOL-UNKNOWN` |
| 9 | `edit` | `{"i":"e9","path":"skill://godspeed"}` | DENY `EDIT_EXTERNAL` (read of same remains ALLOW) | `SCOPE-TOOL-UNKNOWN` |
| 10 | `edit` | `{"path":"stream_content_placeholder"}` (no `path`; body opaque) | UNKNOWN `OPAQUE_PATCH` | `SCOPE-TOOL-UNKNOWN` |
| 11 | `edit` | `{"i":"e11","path":"$W/FxReportOnly.md","old_string":"a","new_string":"b"}` | DENY `UNDECLARED_EDIT` | `SCOPE-TOOL-UNKNOWN` |
| 12 | `edit` | `{"i":"e12","path":"$W/FxUndeclared.md","old_string":"a","new_string":"b"}` | DENY `UNDECLARED_EDIT` | `SCOPE-TOOL-UNKNOWN` |
| 13 | `write` | `{"i":"e13","path":"$W/FxReportOnly.md","content":"x"}` | ALLOW | ALLOW (identical) |
| 14 | `multi_tool_use.parallel` | two children: event 0 and event 4 | CHECK_EACH → `WRITE_ONLY_EDIT` + ALLOW, no aggregate allow | two `SCOPE-TOOL-UNKNOWN` |

Row 10 literal shape caveat: S086's opaque edit was `["path","stream_content"]`; the fixture's
no-path case exists to pin `OPAQUE_PATCH` independently of that spelling. An edit with a `path` plus
`stream_content` and no `i` must also be accepted (exact key set, row 0 variant).

Aggregate exit projection: the all-edit subset rows 0/3/5/6/7/8/9/11/12 → FAIL code 1,
`structured_edit_mode: 1`; adding row 10 must not yield PASS and, under the recommended projection,
yields code 2 with both `OPAQUE_PATCH` and the deny findings retained.

## Remaining unknowns / gaps

- Exact v2 schema tombstone and per-seat edge policy for an omitted `edit_paths` are not literal in the
  preregister; tombstone and "omitted = no authority" are labelled inference.
- Exit-code projection for `UNKNOWN` (1-as-finding vs 2-as-cannot-evaluate) is undeclared; recommendation
  above, not a source fact.
- `tools/check-edit-contract.py` (C1's gate) is outside this seat's declared read set and was not read;
  its row-to-`edit_decisions` mapping is not assessed here.
- No native prevention, effect, or reading proof is claimed anywhere in this report, consistent with the
  v1 gate's own scope and the preregister's C2 scope.

Reviewed-SHA256: 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6
Predicate: r23-oraclev2writeonly
Scope: executed=none
