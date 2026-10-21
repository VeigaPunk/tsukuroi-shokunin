# Review23ActorKeys — round23 reviewer findings (structured-edit actor keys)

**Seat:** Review23ActorKeys (reviewer, leaf) · **Round:** 23 · **Attempt:** 1
**Reviewed artifact:** `.ufo/waves/round-23/sources/structured-edit-observations.json` (digest supplied by the seat binding; supplied identity, not independently computed).
**Deliverable:** this report only. No draft file was named for this seat, so none was written.
**Bound evidence actually read (no unbound path was opened):**
- `.ufo/waves/round-23/sources/structured-edit-observations.json` (whole file, raw)
- `.ufo/waves/round-23/preregister.json` (whole file, raw)
- `.ufo/waves/round-23/sources/godspeed-directive.txt` and `skill://godspeed` (both reachable; the copied directive and the installed skill agree)
- `.ufo/waves/round-23/snapshot/tools/check-review-cohort.py` (whole file, raw)

No raw session/transcript path was opened; no command was executed; no fetch of any kind was performed. Raw command/fetch body content was not copied anywhere in this report.

---

## Axes named

| Axis | Question this seat answers |
|---|---|
| **A — retention sufficiency** | Can all eight preregistered structured-edit decisions (C1) be decided from *presence-only* metadata, with no body value ever needed? |
| **B — retention safety** | Is body content excluded, and is that exclusion machine-checkable rather than prose? |
| **C — reconstructability** | Is each recorded request and each recorded adapter step individually identifiable and directionally unambiguous? |
| **D — generality** | Does the observed key vocabulary legitimately generalize to round-23-era request shapes? |
| **E — delivery / operability** | Does the round-23 seat report actually land in the bound revision and hash-match the settlement the cohort tool reads? |

---

## Evidence actually observed (counts computed from the bound JSON text)

Four request rows, two seats, two transcripts:

| # | seat | request_line | call_id | `argument_keys` | `recorded_starts` |
|---|---|---|---|---|---|
| 1 | CritRuntime | 15 | `toolu_014nToY7USd3cckcqeieNJ4o` | `path`, `stream_content` | line 12 `read` (path + `:raw` selector), line 13 `write` (same path) |
| 2 | OraclePathArtifact | 30 | `call_00_hvOTrbx3xphvC7xox3rH9470` | `i`, `new_string`, `old_string`, `path` | line 31 `edit` (same path) |
| 3 | OraclePathArtifact | 33 | `call_00_Q0S2EKfbY3zp9UWqAIj37496` | `i`, `new_string`, `old_string`, `path` | line 34 `edit` (same path) |
| 4 | OraclePathArtifact | 36 | `call_00_49kg5c5quaga33svwodl1gci` | `i`, `new_string`, `old_string`, `path` | line 37 `edit` (same path) |

Derived facts: `path` present 4/4; `i` present 3/4 (row 1 lacks it); `old_string` **and** `new_string` co-present 3/4; `stream_content` present 1/4 and never co-present with the old/new pair; no row carries two dialects at once; every row's `body_fields` is the constant string `"omitted; no report text copied"`.

---

## Findings by severity

### F1 — Medium — `recorded_starts` has no declared direction and no step identity, so `EXPANSION / CHECK_EACH` and read-authority corroboration are not decidable

Rows 1's steps (lines 12, 13) sit **before** its request (line 15); rows 2–4's single step sits **after** their request (line + 1). The field name `recorded_starts` does not disambiguate "precondition" from "consequence", and the step entries carry only `line`, `tool`, `path` — no `call_id`. A downstream v2 audit row therefore cannot tell whether a recorded step is evidence that the seat *read* the target before mutating it (row 1's `read` at line 12) or an *effect* of the request (rows 2–4's `edit` at line + 1). This directly threatens two preregistered decisions: `WRITE_ONLY_EDIT / DENY` (needs read authority for the exact target) and `EXPANSION / CHECK_EACH` (every recorded adapter read or write separately scoped). It also strains the source's own scope sentence, which disclaims "effects, or reading proof": a consumer that treats a recorded step as read proof would assert more than the collector can support.

Recommendation (source-only, bounded): give each step an explicit `relation` (`before` | `after`) and carry the step's own `call_id`; keep `line` as a human aid only, never as the identifier. This is a shape change in the collector, not a body-value change.

### F2 — Medium — a flat key list plus a prose placeholder cannot separate "no body key present" from "unrecognized body key", so `OPAQUE_PATCH / UNKNOWN` is not decidable from a row

`argument_keys` mixes metadata keys (`path`, `i`) with body-bearing keys (`stream_content`, `old_string`, `new_string`) in one flat list, and `body_fields` is a prose string, not a presence map. A consumer must therefore hardcode the body-key vocabulary to answer "did this request carry a structured target?". The preregistered answer for `OPAQUE_PATCH` is `UNKNOWN` — "Missing structured target is not inferred from opaque patch text" — so the *safe* direction is that a request with no recognized body key is `UNKNOWN`. But that default is only reachable if the collector also distinguishes it from a request that carried a body key under a name the vocabulary does not know (a third dialect). Without the distinction, a v2 authority either over-denies (misreading an unknown-but-structured key as opaque) or silently hardcodes a closed vocabulary — which would assert universal tool semantics that the source's own scope sentence explicitly disclaims.

Recommendation (source-only, bounded): record an explicit partition — `body_key_presence` (a map of declared body-key name → boolean, values never recorded), `metadata_keys`, and `unrecognized_keys` (any argument key in neither declared set). Classification then becomes: recognized body key present → structured target; no body key and no unrecognized keys → `OPAQUE_PATCH / UNKNOWN`; unrecognized keys present → also `UNKNOWN` under the prereg's conservative verdict, but for a *distinguishable* reason. This preserves the prereg's `UNKNOWN` (not `DENY`) semantics exactly.

### F3 — Medium (operability) — the seat report must exist **in the bound revision** and hash-match the settlement, or the seat lands as unresolved/drifted

`.ufo/waves/round-23/snapshot/tools/check-review-cohort.py` reads every seat report through `git_read(binding.sha, review['report'])` — the *committed* bytes at the bound revision, never the working tree — and then compares `hashlib.sha256(report).hexdigest()` against the settlement row's `report_sha256`, raising `COHORT-REPORT-DRIFT` on mismatch. A report that exists only in the working tree, or whose settlement digest was taken from pre-commit bytes, produces (a) `COHORT-REPORT-DRIFT` → exit 1, or (b) `report is None` → category `absent_unresolved` → `COHORT-UNRESOLVED` → exit 1. The selftest fixtures confirm both failure shapes (`report-drift` → code 1; `missing-unresolved` → code 1) and confirm that a receipt with a trailing period, a wrong predicate, a wrong digest, a duplicated digest line, or a trailing U+2028 is `delivered_faulty`.

Recommendation (for the L1 integrator, not executable by this seat): commit the report bytes *first*, then derive `settlement.seats[].report_sha256` from the committed bytes at the bound revision. Note also from the cohort tool's own `SCOPE`: `delivered_conformant` means receipt-well-formed only — it is **not** a claim of request-scope conformity, command nonexecution, reading, chronology, no-harm, or native enforcement. This report therefore makes no such claim.

### F4 — Low-Medium — the observed vocabulary is round-22-era and n=4; it must not be promoted into a required-key schema

The observations describe round-22 transcripts (`TsukuroiR22.*` agents), while C2 governs round-23-era requests. The sample spans two disjoint dialects (1 row `stream_content`, 3 rows `old_string`+`new_string`) and one row with no `i` key at all. A required-key schema derived from n=3 of the dominant dialect would mis-handle both the `stream_content` dialect and the intent-less request. The C2 claim text in the preregister speaks only of "explicit schema-v2 audit authority for exact predeclared structured edit targets" — it never asserts a fixed argument-name vocabulary.

Recommendation (source-only, bounded): the v2 authority must treat the observed key sets as **witnessed shapes with witness counts**, and default to `UNKNOWN` for any shape it has not seen, rather than encoding a canonical required-key set. Retain `argument_keys` verbatim (as the collector already does) so a new dialect is visible rather than filtered out at collection time.

### F5 — Low — body exclusion is asserted in prose, not machine-checkable

`body_fields: "omitted; no report text copied"` is a human-readable assertion embedded in a field whose name suggests a list of recorded body fields. A consumer could reasonably expect an object there and fall back to something else. Nothing in the row structure proves the absence of body content.

Recommendation (source-only, bounded): replace with two structured fields — `body_retention: "presence_only"` and `retained_body_values: []` — so the retention claim is assertable by inspection and by any future checker. If an emptiness distinction is later wanted (present-but-empty vs present-and-non-empty), it must be a labeled derived boolean per body key, never a copied value, and the source's scope sentence must be amended to say "body values not copied; presence only" rather than the current broader phrasing.

### F6 — Low — the census unit is not declared, and the exact rough-versus-lane unit difference is what C3 exists to explain

The collector emits one row per *request*. The outside round-22 figures carried in the preregister are file counts per seat group (`rough.build 25 / rough.falsify 33`, `lane.build 23 / lane.falsify 29`) — a different and partly ambiguous unit. C3's stated scope is an "exhaustive per-event/component explanation of rough-versus-lane path counts"; if request counts, target-path counts, and seat counts are mixed without a declared unit, the reconciliation reproduces the very classifier/unit difference it is meant to explain.

Recommendation (source-only, bounded): the collector should emit counts at three explicit units — request, distinct target path, seat — each labeled with its unit, so the C3 reconciliation can state which unit each reported number is in.

### F7 — Low — the source does not declare that it is a shape witness rather than the event census

The source's scope sentence bounds what the observations *mean* ("not universal tool semantics, native permission enforcement, effects, or reading proof") but never states coverage: four rows, two seats, two transcripts of a larger cohort. Nothing forbids a downstream reader from citing S086 as the per-event source that C3 must reconcile exhaustively.

Recommendation (source-only, bounded): add an explicit coverage clause to the source (row/seat/transcript counts, "shape witness, not an exhaustive census") and keep the census source (S085, the rough path-census source cell) as a separate, separately-cited input.

### F8 — Info / confirmed — presence-only retention is *sufficient* for all eight preregistered decisions; no body value is needed

This is the positive result for axis A, and it holds without weakening any safety property: every preregistered decision in `preregister.json → edit_decisions` is answerable from target-path identity plus key presence plus recorded step structure.

| Decision (preregistered verdict) | Metadata required | Retained today? | Gap |
|---|---|---|---|
| `DECLARED_EDIT` / ALLOW | verbatim target path + predeclared target set | path ✓ (declaration side is external, C2 scope) | none in collector |
| `UNDECLARED_EDIT` / DENY | verbatim target path + declaration set | ✓ | none |
| `READ_ONLY_EDIT` / DENY | seat read-vs-edit authority + path | ✓ (authority external) | none |
| `WRITE_ONLY_EDIT` / DENY | write authority + read authority for that exact target | path ✓; step evidence partially usable | F1 |
| `OPAQUE_PATCH` / UNKNOWN | "no structured target key" must be distinguishable from "unrecognized key" | ✗ not distinguishable | F2 |
| `EDIT_TRAVERSAL` / DENY | verbatim raw path (dot-segment / alternate spelling detectable; target list must not expand) | ✓ verbatim — **must stay verbatim** | none (see F5 note below) |
| `EDIT_EXTERNAL` / DENY | verbatim path incl. non-filesystem URI schemes | ✓ verbatim | none |
| `EXPANSION` / CHECK_EACH | every recorded adapter read/write, separately scoped and individually identifiable | steps present, identity/direction missing | F1 |

Two constraints follow and are load-bearing: the collector must **not** normalize or canonicalize the path (normalization would erase the dot-segment evidence `EDIT_TRAVERSAL` needs, and the authority — not the collector — is the right place for it, keeping both raw and resolved forms there), and the collector must **not** drop a request whose path is a non-filesystem URI, because that drop would silently convert an `EDIT_EXTERNAL` candidate into an absent row.

### F9 — Info — same-identity anchoring is present; effect claims are correctly withheld

`transcript_sha256` + `request_line` + `call_id` + `tool` + `path` is enough to pin a request's identity and to notice a same-target rerouting (row 1 shows a `write` step and an `edit` request against the same path — a visible write-then-edit pair on one target). The source's scope sentence, the prereg C2 scope ("Body data opaque, no native enforcement/effects claim"), and the prereg limits ("No native per-seat restrictive tool interface exists", "No runtime prevention, effect/reading/recorder-completeness or universal tool/patch semantics") are mutually consistent and correctly withhold runtime enforcement. A v2 edit-target audit authority built on this source is a **declarative** authority over captured events; it must not be described as preventing, enforcing, or proving anything at runtime.

---

## Proposed collector row shape (presence-only; fixture, indented, non-receipt)

Direction for the executing seats only; every value below is a placeholder or a boolean/boolean-set, never a body value.

```
  {
    "schema": "tsukuroi-structured-edit-observations-v2",
    "seat": "<seat>", "agent": "<agent>", "transcript_sha256": "<sha>",
    "request_line": 0, "call_id": "<call_id>", "tool": "<tool>",
    "path": "<verbatim request path, unresolved, never normalized>",
    "argument_keys": ["<observed key order preserved>"],
    "metadata_keys": ["<keys such as path / i>"],
    "body_key_presence": {"stream_content": false, "old_string": true, "new_string": true},
    "unrecognized_keys": [],
    "body_retention": "presence_only",
    "retained_body_values": [],
    "steps": [
      {"line": 0, "call_id": "<step call id>", "tool": "<step tool>", "path": "<step path>", "relation": "before"}
    ],
    "coverage": {"rows": 0, "seats": 0, "transcripts": 0, "kind": "shape_witness_not_census"}
  }
```

## Residual risk

1. **No runtime enforcement exists** — the C2 authority is a declarative audit over captured events only; no prevention, effect, or reading proof follows from it, and the prereg's own limits say so.
2. **Sample coverage** — four rows, two seats, two transcripts. Findings F2 and F4 are shape-diversity findings; they do not establish that the two observed dialects are the complete set of request shapes in the fleet.
3. **Vocabulary drift** — a future dialect that carries a structured body under an unseen key will land in `unrecognized_keys` and be judged `UNKNOWN`; that is the prereg-conservative outcome, but it is a coverage gap, not a clean classification.
4. **Semantic-vs-declarative** — the C1 "eight typed structured-edit policy/source rows" are decision rows over a contract; they do not by themselves change any tool's behavior.
5. **Evidence-vs-truth** — the observations are evidence of what was requested, not of what any seat was permitted to do.

## Verification gaps and recorded unavailability

- **No LSP server was usable from this seat.** The `xd://` device family is excluded by this seat's NO-FETCH scope, so `references` / `definition` / `diagnostics` could not be used. Fallback used: literal reading of the bound files only. No grep output is presented as semantic proof.
- **Production collectors are unbound.** `tools/check-edit-contract.py`, `tools/check-seat-bindings.py`, `tools/check-path-reconciliation.py`, the round-23 seat bindings, the round-23 review manifest and the settlement are **not** in this seat's `read_paths` and were not opened. Consequently: (a) the exact v2 collector source was reviewed only through the recorded observation rows, not as code; (b) the manifest's `report` path and the settlement row for this seat were not verified — the assumption that the manifest points at `.ufo/waves/round-23/build/Review23ActorKeys.md` follows from the seat binding, not from an observed manifest; (c) F3's digest-match requirement is stated from the cohort tool's code path, not from an observed round-23 settlement.
- **The strict receipt evaluator source is unbound.** `tools/check-review-snapshots.py` was not opened; the receipt-shape expectations above are derived from the cohort tool's own selftest fixtures (period, predicate, digest, duplicate-receipt, crlf, unicode, encoding cases) and from the seat instructions.
- **The r22 cohort was not re-run.** No historic check was retried for confirmation, and no historical manifest/report was rewritten.
- **Digest not independently computed.** The reviewed digest is the supplied declaration; no hash, list, word-count, import, or execution was performed against it.

## No-harm check on this seat's own actions

Reads: bound files only (5 declared paths). Writes: this report only, at the seat's declared write path. Git index/jj state, refs, routes, configs, fleet/sibling files, production files, and host/package/service/boot state: untouched. Commands executed: none. Fetches performed: none. Sub-agents dispatched: none (leaf member).

Reviewed-SHA256: 19d85129bf0f7fd71f5aea93c35660b21d305150500dc63b58104019851af12a
Predicate: r23-review23actorkeys
Scope: executed=none

