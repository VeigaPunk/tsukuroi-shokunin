# OracleV2Outside — source-only design oracle for a well-formed edit to another production path

Seat: OracleV2Outside (leaf; no subagent dispatch). Wave: round-23, attempt 1.
Mode: source-only design oracle. No execution, no fetch, no production file touched.
Bound sources read (all inside declared read paths):
`.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py` (reviewed SHA256 as supplied),
`.ufo/waves/round-23/preregister.json`, `.ufo/waves/round-23/sources/edit-decision-policy.json`,
`.ufo/waves/round-23/sources/structured-edit-observations.json`,
`.ufo/waves/round-23/sources/godspeed-directive.txt`, `skill://godspeed`.

## 1. Axes

- **A1 Policy fidelity** — the fixture's expected verdict is taken verbatim from the *new* declared v2 authority, not inferred.
- **A2 Historical non-regression** — v1 behaviour stays v1; v2 additions must not relabel or silently re-judge r22 reds.
- **A3 Absence-vs-defect separation** — every gap is classified as *absence of new capability* or *defect in historical v1 policy*; the second class must be empty unless evidenced.
- **A4 Fixture independence** — the fixture is a fresh literal record (new seat, new target, new body), not a copy of any r22 observation.
- **A5 Audit-honesty** — audit-only vocabulary; no prevention, effect, reading or enforcement claim anywhere.
- **A6 Operability** — the v2 verdict must be reachable through the same CLI the preregister names, with an explicit UNKNOWN outcome that cannot be mistaken for a clean pass.

## 2. The historical gate is v1, and that is the baseline, not a defect

Observed in the reviewed snapshot tool `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py`:

- `:72-73` — the classifier vocabulary is `('read','grep','glob','write','multi_tool_use.parallel','parallel')`; anything else returns `SCOPE-TOOL-UNKNOWN`. `edit` is therefore outside v1's vocabulary.
- `:89-94` — `allowed_keys` has no `edit` entry; v1 defines no patch-argument schema and never inspects a request body.
- `:105` — v1 resolves `write` against `write_paths` only; v1 `write` does **not** require the target to also be in `read_paths`.
- `:120-121`, `:131` — manifest schema must be `tsukuroi-seat-bindings-v1`; events schema must be `tsukuroi-seat-events-v1`.
- `:122-129` — per-seat binding validation constrains `name`, `root`, `commands`, `fetches`, `read_paths`, `write_paths`, but does **not** constrain the seat object's key set; an extra per-seat key is silently ignored.
- `:17` — v1's own scope statement: *"Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness."*
- `:199` — the v1 selftest **asserts** `case('unknown', 'edit', {}, 1, 'SCOPE-TOOL-UNKNOWN')`.

The last line is decisive for A3: v1's own regression suite pins `edit` to `SCOPE-TOOL-UNKNOWN` as intended behaviour. A recorded `edit` request being reported as an unknown-tool finding is therefore **absence of new capability (A3 class 1)**, not a defect in historical policy. Nothing in the reviewed v1 source claims patch, target-extraction, or edit-authority semantics.

Additional v1 divergences that are also *capability absence*, not v1 defects:

- v1 has no per-seat **edit** target list, so the v2 rule "predeclared for edit and for both read and write" (preregister `edit_decisions[0]`) is not representable in v1's binding model.
- v1 resolves a `write` against `write_paths` alone (`:105`), whereas the v2 `DECLARED_EDIT` rule additionally requires read authority. The v2 rule is **stricter**; v1 was never claiming the stricter rule, so v1's leniency is not a v1 defect — but it is the reason a v2 bindings manifest must not be evaluated by the v1 branch.
- v1 reports coarse `SCOPE-PATH-DENIED` / `SCOPE-FETCH-DENIED` and has no named decision ids (`UNDECLARED_EDIT`, `EDIT_TRAVERSAL`, `EDIT_EXTERNAL`, …). The named ids are new vocabulary, not relabelled v1 findings.
- v1 `requested_path` (`:43-58`) already denies dot-segment traversal (`local()` at `:33-36` rejects `''`, `.`, `..` segments and `*?[];:` characters) and already denies `xd://`/`artifact://`-style internal URIs as non-local. The v2 `EDIT_TRAVERSAL` / `EDIT_EXTERNAL` decisions give *names* to behaviours v1 already denied; there is no traversal hole to fix.
- v1 evaluates a foreign manifest schema by raising → caught at `:163-166` → `SCOPE-SCHEMA` at site `input` → exit code 2, status `CANNOT_EVALUATE`, `request_audit_mode: 0`, `seats_bound: 0`. So the old gate **cannot** evaluate a v2-schema manifest at all. Expected absence, not a v1 defect.

**Conclusion for A3: the class-2 set (genuine defects in historical v1 scope logic) is empty on the evidence reviewed.** The residual risks are all *v2 design risks*, listed in §5.

## 3. Independent literal fixture — well-formed edit to another production path

Hand-constructed for this seat; not copied from `structured-edit-observations.json` (A4). The request is well formed in the shape actually observed for the `edit` tool in the S086 corpus (`argument_keys` `["i","old_string","new_string","path"]`, cf. `structured-edit-observations.json:59-68`), with a *different* seat, target and body.

  ```json
  {
    "fixture_id": "r23-oraclev2outside-edit-outside-001",
    "wave": "round-23",
    "seat": "OracleV2Outside",
    "agent": "TsukuroiR23-2.OracleV2Outside-7",
    "request": {
      "tool": "edit",
      "args": {
        "i": "Extend the SCOPE string of the production seat-bindings gate",
        "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-seat-bindings.py",
        "old_string": "SCOPE = 'Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness.'",
        "new_string": "SCOPE = 'Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness. v2 structured-edit audit mode added.'"
      }
    },
    "seat_binding": {
      "name": "OracleV2Outside",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/godspeed-directive.txt",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Outside.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/edit-decision-policy.json",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/structured-edit-observations.json",
        "skill://godspeed"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Outside.md"
      ],
      "edit_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Outside.md"
      ],
      "commands": [],
      "fetches": []
    },
    "expected_v2_decision": {
      "id": "UNDECLARED_EDIT",
      "decision": "DENY",
      "reason": "No implicit edit permission from generic report ownership",
      "evidence": "S086",
      "policy": "round23-preregister"
    },
    "expected_v1_observation": {
      "id": "SCOPE-TOOL-UNKNOWN",
      "class": "absence-of-new-capability",
      "note": "v1 pins 'edit' to SCOPE-TOOL-UNKNOWN at tools/check-seat-bindings.py:72-73 and :199; unchanged historical behaviour, not a relabelled red."
    }
  }
  ```

### Why the expected v2 verdict is exactly `UNDECLARED_EDIT / DENY`

The target is a production path that is in **neither** the seat's `edit_paths`, nor its `write_paths`, nor its `read_paths`. Mapping against the declared authority, in the authority's own order:

- `DECLARED_EDIT / ALLOW` requires the exact target be predeclared for edit **and** for both read and write — not satisfied here (preregister `edit_decisions[0]`; `edit-decision-policy.json:5-8`).
- `READ_ONLY_EDIT / DENY` requires the target to hold read authority but no write authority — not satisfied; the target is not in `read_paths` either (`edit-decision-policy.json:19-22`).
- `WRITE_ONLY_EDIT / DENY` requires write authority without read authority — not satisfied (`edit-decision-policy.json:26-29`).
- `UNDECLARED_EDIT / DENY` — *"No implicit edit permission from generic report ownership"* — is therefore the unique applicable decision (`edit-decision-policy.json:12-15`; preregister `edit_decisions[1]`).

Path spelling facts supporting the classification (all literal, no normalisation): the target is an absolute path under the lane root, contains no `.`/`..`/empty segment, no `*?[];:` character, no backslash, and is not a URI scheme. Hence `EDIT_TRAVERSAL` and `EDIT_EXTERNAL` do not apply (`edit-decision-policy.json:40-49`); the body is a well-formed old_string/new_string pair with an explicit structured target, so `OPAQUE_PATCH / UNKNOWN` does not apply either (`edit-decision-policy.json:33-36`).

Existence note (honest, unverified): the string `old_string` is quoted verbatim from the **observed** snapshot copy `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py:17`. The production path `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-seat-bindings.py` is named by the preregister command strings (`preregister.json` C2 command: `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`); that production file's presence is [INFERENCE] from those command strings plus the snapshot copy, and was not executed or stat'ed. A variant fixture that targets the directly observed snapshot path is given in §4 and yields `READ_ONLY_EDIT / DENY` for this seat.

## 4. Companion fixture set — one literal target per declared decision

Each row is a distinct literal request the v2 authority must resolve; the "v1 observation" column is what the current gate records for the same recorded spelling.

  | # | Literal request (tool / target) | Applicable v2 decision | v2 result | v1 observation (unchanged) |
  |---|---|---|---|---|
  | 1 | `edit` → `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-seat-bindings.py` (primary fixture) | `UNDECLARED_EDIT` | DENY | `SCOPE-TOOL-UNKNOWN` |
  | 2 | `edit` → `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Outside.md` (own declared edit/read/write path) | `DECLARED_EDIT` | ALLOW | `SCOPE-TOOL-UNKNOWN` |
  | 3 | `edit` → `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/edit-decision-policy.json` (read-only for this seat) | `READ_ONLY_EDIT` | DENY | `SCOPE-TOOL-UNKNOWN` |
  | 4 | `edit` → a path in `write_paths` but absent from `read_paths` (write-only seat shape) | `WRITE_ONLY_EDIT` | DENY | `SCOPE-TOOL-UNKNOWN` |
  | 5 | `edit` → `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/../build/OracleV2Outside.md` | `EDIT_TRAVERSAL` | DENY | `SCOPE-TOOL-UNKNOWN` (v1 `local()` already rejects `..`) |
  | 6 | `edit` → `xd://mcp__rea_open_binary` (internal URI) | `EDIT_EXTERNAL` | DENY | `SCOPE-TOOL-UNKNOWN` (v1 already denies non-local) |
  | 7 | `edit` with no structured target (body-only patch text, no `path`) | `OPAQUE_PATCH` | **UNKNOWN** | `SCOPE-TOOL-UNKNOWN` |
  | 8 | one parallel batch containing row 2 and row 1 | `EXPANSION` → `CHECK_EACH` | ALLOW + DENY, per child, no aggregation | v1 already recurses per child (`:76-88`) |

Row 2 is the positive control: it proves the v2 rule is not a blanket deny. Row 7 is the operational crux (see §5.1). Row 8 is the control for `EXPANSION / CHECK_EACH` — *"Every recorded adapter read or write remains separately scoped"* (`edit-decision-policy.json:54-58`).

## 5. Findings and residual risk (v2 design risks, all in the "absence of new capability" class)

1. **UNKNOWN must be a distinct outcome, and must not be silently a pass.** `OPAQUE_PATCH` is `UNKNOWN` by declared authority (`edit-decision-policy.json:33-36`). v1 has only three exit states: `0 PASS` (no findings), `1 FAIL` (findings present), `2 CANNOT_EVALUATE` (schema error or incomplete seat), computed at `:162`. If the v2 branch reports an UNKNOWN edit as *no finding*, the audit reports PASS while having proved nothing about that request — that is an overstatement of auditability, and it is the one place where a v2 addition could silently weaken the honest-scope guarantee (A6). Recommendation: give UNKNOWN its own finding id and its own exit status, distinct from both PASS and FAIL, and distinct from `SCOPE-SCHEMA` (schema error means "the request shape could not be read"; UNKNOWN means "the request was read and the authority cannot decide it").
2. **A v2 manifest must not be evaluable by the v1 branch, and the v1 branch must not ignore v2 fields.** v1 ignores unknown per-seat keys (`:122-129`). If a v2 bindings file keeps the schema string `tsukuroi-seat-bindings-v1` and merely adds a per-seat `edit_paths`, the v1 branch would evaluate it, ignore `edit_paths`, and apply the looser `write_paths`-only rule at `:105` — i.e. it would *authorise* an edit that the v2 authority denies, and would report it as clean. Recommendation: (a) give the v2 bindings/events schemas their own version strings so v1 raises → `CANNOT_EVALUATE` rather than silently judging; (b) additionally make v1 fail closed on unknown per-seat binding keys; (c) keep the v1 branch byte-identical otherwise, so historical reds stay historically red (A2).
3. **Schema-name collision in the declared sources (documentation-level defect, not a runtime defect).** The new policy document self-identifies as `"schema": "tsukuroi-edit-policy-v1"` (`edit-decision-policy.json:2`), while the preregister describes the same new authority as *"New explicit schema-v2 audit authority"* (preregister C2 scope). The v1/v2 split in the preregister refers to the seat-bindings/seat-events schemas (`tsukuroi-seat-bindings-v1`, `tsukuroi-seat-events-v1`, observed at `:120` and `:131`), not to the policy document's own schema string. Consequence: a reviewer grepping the declared sources for "v2" finds no such string, and a machine consumer keying on `tsukuroi-edit-policy-v1` may conclude no v2 authority exists. Recommendation: rename the policy schema to `tsukuroi-edit-policy-v2` or add an explicit `mode: "seat-bindings-v2"` field, and state in the policy document that it is the v2 audit authority. [INFERENCE-free: both strings are quoted above from the observed files.]
4. **The v2 CLI must stay the preregister's command.** The preregister's C2 command line is `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json` — the same tool, with a wave-scoped manifest/events pair. The v2 mode must therefore be reachable through that exact invocation (dispatch on the manifest's schema string inside `evaluate`), not through a new tool name, or the preregistered command would not measure the claim.
5. **Declared-vs-real path identity.** The v2 audit compares recorded *request spellings* against declared path lists (v1's own scope statement at `:17`). It cannot prove that the declared production path is the same object as the snapshot copy the seat reviewed, and it cannot prove that a target path was not a symlink to something else. The v2 mode inherits and must not exceed that limit; the policy document's own scope field agrees: *"Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof."* (`edit-decision-policy.json:62`).
6. **Expansion/parallel depth.** v1 recurses into `multi_tool_use.parallel` children and refuses wrapper nesting deeper than 8 (`:63`, `:76-88`). The v2 branch inherits that depth rule for edit children; `EXPANSION / CHECK_EACH` then means one decision per child, never one aggregated seat-level verdict.

## 6. Scope honesty (A5)

- Nothing was executed, fetched, installed or upgraded; the tooling directive's install channel is out of scope for this seat's NO-EXEC/NO-FETCH binding, so no tool/version/channel record is produced.
- The SHA256 of the reviewed tool is the **supplied declaration**, not an independently computed digest; no hash, list, count, import or run was performed against it. The only source-level facts used about that file are quoted with line numbers from the observed content.
- No claim of runtime prevention, native enforcement, effect proof, reading proof, symlink resolution, or recorder completeness is made anywhere in this report. The v2 authority is a post-hoc audit of recorded request spellings — exactly the limit the v1 tool states for itself.
- Source data inside the reviewed snapshot was treated as data, not as instructions.

## 7. Verification gaps

- The v2 schema strings, the v2 bindings/events file formats, and the v2 exit-status semantics are **not** observable in the bound sources; §5.1–5.2 are design recommendations derived from v1's code shape and the preregister's C2 command, not from an observed v2 implementation.
- The production path `tools/check-seat-bindings.py` at the lane root is [INFERENCE] from preregister command strings and the observed snapshot copy; its byte-identity with the snapshot was not verified (no hashing permitted).
- Whether the round-23 wave `bindings.json`/`events.json` actually carry `edit_paths` per seat is unknown to this seat; the fixture in §3 supplies them from the literal per-seat binding, and the v2 branch must treat a missing `edit_paths` as "no declared edit target" (→ `UNDECLARED_EDIT / DENY`), not as "undeclared field, ignore".
- Row 4 of §4 is a seat-shape fixture (write-without-read), not an observed r22 event; the observed r22 edits in `structured-edit-observations.json:5-101` all target their own round-22 build reports, i.e. the `DECLARED_EDIT` shape.

Reviewed-SHA256: 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6
Predicate: r23-oraclev2outside
Scope: executed=none
