# OracleV2Nested — nested-wrapper edit target scope and post-edit visibility

Seat: `TsukuroiR23-2.OracleV2Nested-7` · Round 23, attempt 1 · baseline `ae01e50f582016384e620022be38bf5367000e2e`
Axis: C2 operability — explicit schema-v2 audit authority for exact predeclared structured edit targets.
Mode: source-only design oracle. Read four declared local files; executed nothing; computed no digest.
Source identity: `snapshot/tools/check-seat-bindings.py` declared SHA256 `8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6` (supplied declaration, not recomputed).

## 0. Axes used for this seat

A1 target-scoping truth: does the decision come only from the child edit's own structured `path`?
A2 visibility: is every later recorded request still enumerated after a nested edit (allow or deny)?
A3 authority separation: edit authority distinct from read and write authority, in both directions?
A4 verdict vocabulary: are ALLOW / DENY / UNKNOWN all representable, without UNKNOWN being read as a violation?
A5 absence-vs-defect: is each historical v1 result attributable to missing capability rather than bad policy?

## 1. Observed facts in the reviewed snapshot (v1)

Facts below are read from `snapshot/tools/check-seat-bindings.py`; line numbers verified against the raw text.

O1. There is no structured-edit capability at all in this snapshot.
- The tool vocabulary is closed at `:72`–`:73`: `read`, `grep`, `glob`, `write`, `multi_tool_use.parallel`, `parallel`; anything else returns `SCOPE-TOOL-UNKNOWN`. `edit` is not a member.
- Selftest asserts that exact outcome: `:199` `case('unknown', 'edit', {}, 1, 'SCOPE-TOOL-UNKNOWN')`.
- The vocabulary test runs before argument shape (`:74`), so *every* observed edit shape, including a path-less opaque patch, collapses to the same `SCOPE-TOOL-UNKNOWN` at `:73`. No target is ever examined.
- Authority lookup is a two-way ternary at `:105`: `binding['write_paths' if tool == 'write' else 'read_paths']`. No edit list exists anywhere in the binding validator: `:126` iterates only `('read_paths', 'write_paths')`. The seat key set is not closed, so an `edit_paths` key would be silently ignored rather than rejected.
- No CLI mode for structured edits: `main` (`:280`–`:310`) has only `--revision` / `--selftest` plus `--branch`, `--manifest`, `--events`, whose defaults still point at round 22 (`:286`–`:287`).

O2. The manifest envelope is strictly `tsukuroi-seat-bindings-v1` (`:120`). A v2 envelope is rejected before any event is read: `:162` turns the `SCOPE-SCHEMA` at `:164` into exit 2 `CANNOT_EVALUATE`, and `requests_total` stays 0 because the event loop at `:149` never runs. Under a v2 envelope the v1 gate sees nothing at all, including the later Bash.

O3. Wrapper recursion preserves per-child scoping.
- A wrapper must have exactly `tool_uses` (`:78`); each child must have exactly `recipient_name` + `parameters` (`:83`), else `SCOPE-SCHEMA` for that child only (`:86`–`:87`).
- Each child is classified with its own `parameters` (`:85`), and each path-bearing tool is later checked against that child's own path (`:101`–`:106`). The wrapper contributes no path and no authority of its own.

O4. Every recorded request remains visible; there is no absorbing verdict and no short-circuit.
- `evaluate` iterates all events of a seat (`:149`), increments `total` unconditionally (`:150`), and appends findings without breaking (`:157`–`:160`). A classification exception becomes `SCOPE-SCHEMA` for that event and the loop continues (`:155`–`:156`).
- Selftest pins this for the two orderings that matter: `:224`–`:225` `malformed-before-exec` expects both `SCOPE-SCHEMA` and `SCOPE-EXEC-DENIED`; `:221` `mixed-parallel` expects both ids from one wrapper. So a later Bash stays visible even after an earlier malformed or denied request.
- The wrapper's accumulator returns *after* the child loop (`:88`), not from inside it; sibling children are not skipped.

O5. The `functions.` qualification is stripped exactly once (`:65`–`:66`), before the vocabulary test. `functions.multi_tool_use.parallel` is recognized (`:219` selftest); a doubled qualification would not be.

O6. Wrapper depth is bounded at eight levels. `depth > 8` raises at `:63`; each wrapper adds one at `:85`. The selftest confirms both sides: three wrappers plus a leaf are still classified (`:244`–`:247`), eight wrappers plus a leaf become `SCOPE-SCHEMA` (`:248`–`:250`).

O7. Read selectors are read/grep-only (`:102`, `selector=tool in ('read', 'grep')`). The selector grammar at `:50`–`:55` would rewrite `X:1-5` to `X`; a `:1-5`-decorated path therefore cannot be an alternate spelling of a file for any tool that passes `selector=False`.

O8. Two presentation properties of v1 that v2 must not inherit:
- `SCOPE-TOOL-UNKNOWN` is counted as a violation: `:160` counts every finding whose id is not `SCOPE-SCHEMA`. "We cannot decide" is therefore reported as "violation" in the `violations` counter.
- The result vocabulary has no UNKNOWN verdict (`:167` keys on the exit code only). v1 cannot express "target metadata is missing, do not infer" as anything other than a finding id; it has no decision carrier.

## 2. Absence of capability, not a defect in historical policy

The reviewed gate is post-hoc request audit under a stated scope: `SCOPE` (`:17`) says "Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness." Its v1 decisions are exhaustive for the tools it declares.

Therefore the historical result for `edit` — `SCOPE-TOOL-UNKNOWN`, exit 1 — is **not** a policy defect:
- v1 never claims edit semantics, so it must not decide one; returning UNKNOWN/"not in vocabulary" is the only honest finite answer it has.
- It also does not misroute an edit into read or write authority. It stops at the vocabulary test (`:72`) before the ternary at `:105` could apply. A naive "just add edit to the tuple" change is what would misroute.
- The `CANNOT_EVALUATE` on a v2 envelope (O2) is likewise refusal, not a judgement of the fixture.

Two things *are* real carry-over hazards, but they are presentation/vocabulary gaps, not historical policy reds: counting an undecided tool as a violation (O8), and having no UNKNOWN verdict at all.

What is genuinely absent, and is the whole of C2: an authority input (`edit_paths`), a distinct decision table, and a result carrier that can say ALLOW / DENY / UNKNOWN per structured target. Recorded round-22 edit requests (S086) could not have been evaluated even in principle by this file.

## 3. Exact expectation from the declared v2 authority

Declared authority: `sources/edit-decision-policy.json` (`schema: tsukuroi-edit-policy-v1`, `policy: round23-preregister`, `evidence: S086`, `source_path: .ufo/waves/round-23/sources/structured-edit-observations.json`), identical to `preregister.json` `edit_decisions`. Its scope line is binding on the whole seat: "Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof." C2 metric: `structured_edit_mode`, before 0, target 1; command is the same script with `--revision/--manifest/--events` (`preregister.json:42`), so the v2 mode is reached through the manifest, not through a new flag [INFERENCE: no new flag appears in the declared command].

Decision table, literal reading:

| id | decision | literal precondition (target T) | expected outcome |
|---|---|---|---|
| DECLARED_EDIT | ALLOW | T predeclared for edit **and for both read and write** | no finding; not a violation |
| UNDECLARED_EDIT | DENY | T not predeclared for edit; generic report/write ownership does not help | DENY |
| READ_ONLY_EDIT | DENY | T admitted by read authority only | DENY |
| WRITE_ONLY_EDIT | DENY | edit authority present with write, read authority absent | DENY |
| OPAQUE_PATCH | UNKNOWN | no structured target (`path`) in the recorded edit | UNKNOWN; content not parsed |
| EDIT_TRAVERSAL | DENY | dot segment or alternate spelling of T | DENY |
| EDIT_EXTERNAL | DENY | remote or internal URI | DENY |
| EXPANSION | CHECK_EACH | several recorded calls | every call evaluated separately |

The all-three precondition for DECLARED_EDIT is the literal text ("predeclared for edit and for both read and write"), and it is corroborated twice: `WRITE_ONLY_EDIT` says edit "also needs its explicit target read authority", and this seat's own v2 binding puts its report in `read_paths`, `write_paths`, and `edit_paths` simultaneously. Confidence: high, but see U1 for the one cell this table does not cover.

Nesting rules that follow from the declared rows plus the observed wrapper mechanics:
- E1 (target-scoping). The decision input is the child edit's own literal `path` compared for exact membership in `edit_paths` (plus the read and write preconditions). The wrapper is never an authority source, never supplies a target, and never widens the child's scope. EXPANSION means each recorded adapter call is assessed on its own; a wrapper is not itself an edit request with merged authority.
- E2 (visibility). An allowed or denied nested edit must not remove later events. The later Bash keeps its own event site index and its own v1 verdict (`SCOPE-EXEC-DENIED`). Site labels stay `seat:index` in recorded order.
- E3 (nesting depth). Up to eight wrapper levels inclusive are classified; nine or more yield `SCOPE-SCHEMA` (O6), which makes the whole run `CANNOT_EVALUATE` by `:162`. A v2 edit inside eight levels must still be target-scoped; beyond the cap the record is treated as malformed, never as silent permission.
- E4 (spelling). Exact membership only. A decorated path is never rewritten to the declared target: `X:1-5` is not `X`, `X/../X` is not `X`, `./X` is not `X`. `local`-style admission alone is insufficient (it admits any LANE-rooted path), so membership in `edit_paths` must be checked after admission, exactly as v1 does for read/write at `:105`.
- E5 (URIs before admission). Internal URIs contain `:`, which `local()` excludes at `:35`; and `requested_path` has a read-only exemption for the exact string `skill://godspeed` at `:48`–`:49`. An edit normalizer must therefore classify scheme URIs as EDIT_EXTERNAL *before* any read-style admission, and must not inherit the skill exemption.

## 4. Independent literal fixture

Authored from the declared decision table and the S086 observed argument keys, not from any expected implementation. Paths are literal and LANE-rooted; all satisfy `local()` (no `:`, no glob or separator metacharacters, no dot segments).

Constants:

```
LANE = /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
T    = LANE/.ufo/waves/round-23/build/OracleV2Nested.md               (read + write + edit)
R    = LANE/.ufo/waves/round-23/build/OracleV2Nested.readonly.md      (read only)
U    = LANE/.ufo/waves/round-23/build/OracleV2Nested.undeclared.md    (read + write, no edit)
W    = LANE/.ufo/waves/round-23/build/OracleV2Nested.writeonly.md     (write + edit, no read)
```

Binding (F1). The seat object is the invariant; the envelope string `tsukuroi-seat-bindings-v2` is the only fixture token not fixed by a source I may read (see U4).

```json
{
  "schema": "tsukuroi-seat-bindings-v2",
  "seats": [
    {
      "name": "OracleV2Nested",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Nested.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Nested.readonly.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Nested.undeclared.md"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Nested.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Nested.undeclared.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Nested.writeonly.md"
      ],
      "edit_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Nested.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Nested.writeonly.md"
      ],
      "commands": [],
      "fetches": []
    }
  ]
}
```

Trace (F2), one seat, `complete: true`, events in recorded order. `i` values are literal intent strings; body fields are opaque and never copied.

```json
{"schema": "tsukuroi-seat-events-v1", "seats": [{"name": "OracleV2Nested", "agent": "fixture-agent", "complete": true, "events": [
  {"tool": "read", "args": {"i": "Reading the declared edit target", "path": "T"}},
  {"tool": "multi_tool_use.parallel", "args": {"tool_uses": [
    {"recipient_name": "functions.edit", "parameters": {"i": "Editing the declared target", "path": "T", "old_string": "ALPHA", "new_string": "BETA"}}]}},
  {"tool": "bash", "args": {"i": "Claiming a follow-on command", "command": "true"}},
  {"tool": "multi_tool_use.parallel", "args": {"tool_uses": [
    {"recipient_name": "functions.edit", "parameters": {"i": "Editing the declared target", "path": "T", "old_string": "BETA", "new_string": "GAMMA"}},
    {"recipient_name": "functions.edit", "parameters": {"i": "Editing an undeclared target", "path": "U", "old_string": "ALPHA", "new_string": "BETA"}}]}},
  {"tool": "edit", "args": {"i": "Editing a read-only target", "path": "R", "old_string": "ALPHA", "new_string": "BETA"}},
  {"tool": "edit", "args": {"i": "Editing a write-only target", "path": "W", "old_string": "ALPHA", "new_string": "BETA"}},
  {"tool": "edit", "args": {"i": "Applying an opaque patch", "patch": "*** Begin Patch\n*** End Patch"}},
  {"tool": "edit", "args": {"i": "Editing via a dot-segment spelling", "path": "LANE/.ufo/waves/round-23/build/../build/OracleV2Nested.md", "old_string": "GAMMA", "new_string": "DELTA"}},
  {"tool": "edit", "args": {"i": "Editing a remote URI", "path": "https://example.invalid/OracleV2Nested.md", "old_string": "ALPHA", "new_string": "BETA"}},
  {"tool": "edit", "args": {"i": "Editing an internal URI", "path": "artifact://OracleV2Nested", "old_string": "ALPHA", "new_string": "BETA"}},
  {"tool": "edit", "args": {"i": "Editing with a read selector", "path": "T:1-5", "old_string": "DELTA", "new_string": "EPSILON"}},
  {"tool": "edit", "args": {"i": "Editing the skill URI", "path": "skill://godspeed", "old_string": "ALPHA", "new_string": "BETA"}}
]}]}
```

In F2 the `T`, `R`, `U`, `W`, `LANE` tokens are the literal constants above, expanded before the fixture is stored.

Exact expected v2 outcome for F1 + F2 (the policy expectation, not an implementation claim):

| event | request | expected decision | finding | site |
|---|---|---|---|---|
| 0 | read T | read admitted, exact member | none | — |
| 1 | wrapper > `functions.edit` T, depth 1 | DECLARED_EDIT / ALLOW | none | — |
| 2 | bash | existing v1 verdict retained | SCOPE-EXEC-DENIED | OracleV2Nested:2 |
| 3 | wrapper > edit T, edit U | T ALLOW; U UNDECLARED_EDIT / DENY | one, for the U child | OracleV2Nested:3 |
| 4 | edit R | READ_ONLY_EDIT / DENY | READ_ONLY_EDIT | OracleV2Nested:4 |
| 5 | edit W | WRITE_ONLY_EDIT / DENY | WRITE_ONLY_EDIT | OracleV2Nested:5 |
| 6 | edit without `path` | OPAQUE_PATCH / UNKNOWN | none; not a violation | — |
| 7 | edit `build/../build/…` | EDIT_TRAVERSAL / DENY | EDIT_TRAVERSAL | OracleV2Nested:7 |
| 8 | edit `https://…` | EDIT_EXTERNAL / DENY | EDIT_EXTERNAL | OracleV2Nested:8 |
| 9 | edit `artifact://…` | EDIT_EXTERNAL / DENY | EDIT_EXTERNAL | OracleV2Nested:9 |
| 10 | edit `T:1-5` | DENY (alternate spelling; label underdetermined, U3) | one DENY | OracleV2Nested:10 |
| 11 | edit `skill://godspeed` | EDIT_EXTERNAL / DENY | EDIT_EXTERNAL | OracleV2Nested:11 |

Aggregate: `requests_total` 12, findings 9, violations 9 (OPAQUE_PATCH excluded), `incomplete_seats` 0, no `SCOPE-SCHEMA`, exit 1 / status FAIL — FAIL here is the fixture's real exec denial and real edit denials, not an edit-mode failure. `structured_edit_mode` 1 (metric literal per C2; exact result key not declared, see U5). DECLARED_EDIT must contribute 0 findings and 0 violations; if decisions are surfaced separately it appears as an ALLOW record.

Minimal variants (same F1):

| variant | events | expected |
|---|---|---|
| clean | 0, 1 | exit 0 PASS, findings 0, requests 2, `structured_edit_mode` 1 |
| later-Bash-after-allow | 0, 1, 2 | exit 1, exactly one finding `SCOPE-EXEC-DENIED` at `OracleV2Nested:2` |
| later-Bash-after-deny | 4, 2 | exit 1, findings `READ_ONLY_EDIT@:0` and `SCOPE-EXEC-DENIED@:1` |
| depth-8 | 8 wrappers > edit T | DECLARED_EDIT / ALLOW, no finding |
| depth-9 | 9 wrappers > edit T | `SCOPE-SCHEMA`, whole run CANNOT_EVALUATE (exit 2) |
| wrapper shape | `tool_uses` plus a sibling key, or a child with a third key | `SCOPE-SCHEMA` for that child only, siblings still classified |

## 5. What the same fixture yields under the reviewed v1 gate (static derivation)

This is the absence/defect discriminator; derived from the source above, not executed.

V1-A, F1 as written (v2 envelope): rejected at `:120`, so exit 2 `CANNOT_EVALUATE`, `seats_bound` 0, `requests_total` 0, single finding `SCOPE-SCHEMA@input`, `request_audit_mode` 0. The later Bash is not visible because no event is read.

V1-B, the identical seat object and F2 under the v1 envelope string (the seat key set is not closed at `:123`–`:130`, so `edit_paths` is ignored): binding accepted, then every edit event returns `SCOPE-TOOL-UNKNOWN` (`:72`–`:73`) with no target examined, including event 6 which has no path at all. Counts: requests 12; findings 12 (event 1: 1; event 2: 1 exec; event 3: 2; events 4–11: 8); violations 12; exit 1 FAIL. The later Bash at site `:2` *is* visible here, which shows the visibility property (O4) is pre-existing and must be preserved, not invented.

V1-C, naive edit extension — the concrete harm the fixture is built to catch. If `edit` is added to the vocabulary at `:72` and to `allowed_keys` at `:89` but the ternary at `:105` is left alone:
- edit T (in read_paths) would be admitted; edit U (in read_paths) would be **falsely admitted** although UNDECLARED_EDIT requires DENY; edit R (read-only) would be **falsely admitted** although READ_ONLY_EDIT requires DENY.
- edit W would be denied for the wrong reason (absent from read_paths, not WRITE_ONLY_EDIT).
- the path-less opaque patch would raise at `:98` and become `SCOPE-SCHEMA` (exit 2) instead of UNKNOWN.
- `https://…` would become `SCOPE-FETCH-DENIED` (`:46`–`:47`) instead of EDIT_EXTERNAL; `artifact://…` and `skill://godspeed` would become `SCOPE-PATH-DENIED` instead of EDIT_EXTERNAL.

Routing edit through write authority instead is equally wrong in the other direction: U is in write_paths and would be falsely allowed, W is in write_paths and would be falsely allowed against WRITE_ONLY_EDIT. Using `edit_paths` alone is wrong in one direction: W would be falsely allowed. F1's three distinct targets (R, U, W) therefore separate all three authority conflations with a single literal vector.

## 6. Residual unknowns (explicit, not resolved here)

U1. **Undeclared decision cell.** The table has no row for a target in `edit_paths` + `read_paths` but not `write_paths`. DECLARED_EDIT's literal text requires all three, so this cell cannot be ALLOW under the declared wording, but no row assigns its DENY label. Same for an edit-only target (no read, no write). This is a coverage gap in the declared table, not something this oracle may fill; the fixture deliberately keeps every expected-DENY case unambiguous.
U2. **Full qualification.** `functions.functions.edit` is not `edit` under single-strip (`:65`–`:66`). Whether v2 should treat it as an alternate spelling (DENY under EDIT_TRAVERSAL) or as an unknown tool is not declared; the outcome (not ALLOW) is determined, the id is not.
U3. **Non-dot, non-URI decorated spelling** (`T:1-5`, `T/`, `T `). DENY is certain from exact predeclaration; the row label (EDIT_TRAVERSAL vs UNDECLARED_EDIT) is not declared. Event 10 is marked accordingly.
U4. **Envelope schema literal.** My readable authority fixes field names (`read_paths`, `write_paths`, `edit_paths`), decisions, and the decision-policy schema `tsukuroi-edit-policy-v1`; it does not contain the v2 seat-bindings schema string. `tsukuroi-seat-bindings-v2` in F1 is fixture-local and must be confirmed against the landed C2 implementation.
U5. **Result-key naming.** C2's declared metric literal is `structured_edit_mode`; the output key that carries it, and the shape of per-target decision records, are not declared. Expected semantics only: mode reported as 1 for a v2 manifest.
U6. **Site granularity for multi-child wrappers.** v1 sites are `seat:index` (`:158`); two findings from one wrapper share a site. Whether v2 adds a child ordinal is not declared; F1 event 3 pins exactly one finding, so it stays unambiguous either way.
U7. **Body-key allowlist.** S086 shows two observed edit argument shapes (`i`/`path`/`old_string`/`new_string`, and `path`/`stream_content`). The decision authority is target metadata only, so body-key names must not change the target decision; if v2 keeps a strict key allowlist it must at minimum admit both observed shapes, or it would re-red documented historical requests for body naming alone.
U8. **Unread dependency.** `_revision` (imported at `:13`, used at `:298`) is outside my read paths; the revision binding path and its failure ids were not examined. `main`'s relative-path validation (`repo_path`, `:294`) applies unchanged to the declared C2 command.

## 7. Confidence

- Section 1 and Section 5 V1-A/V1-B: high (line-verified source, no execution).
- Section 3 DECLARED_EDIT all-three precondition: high from literal text plus two corroborations; medium only on whether the reviewer reads "both read and write" the same way.
- Section 3 E1–E5: high on target-scoping and visibility (existing v1 invariants); medium on URI-before-admission ordering, which is a design consequence rather than a stated row.
- Section 6: no invented values; every U is a declared gap.

## 8. Files read

Declared read paths only: `snapshot/tools/check-seat-bindings.py`; `preregister.json`; `sources/edit-decision-policy.json`; `sources/structured-edit-observations.json`; `skill://godspeed`; `build/OracleV2Nested.md` (absent before this write). No production file, no sibling file, no command, no fetch, no digest computation.

Receipt lines are emitted in the seat result, not duplicated here.
