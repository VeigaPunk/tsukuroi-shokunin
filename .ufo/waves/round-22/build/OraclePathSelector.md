# OraclePathSelector — r22 source-only oracle for `functions.read` boundary case

Seat: `TsukuroiR22.OraclePathSelector-3` (leaf; no subagents, no exec, no fetch).
Target under review: `.ufo/waves/round-22/sources/host-tool-boundary.json` (claimed SHA-256 `d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30`), exact allowed read `1-5:raw`.

## Godspeed axes

- **A1 fixture-minimality** — smallest literal JSON that reproduces the exact request.
- **A2 verdict-determinism** — ALLOW derivable from binding/assignment text alone, zero runtime.
- **A3 ambiguity-surface** — every dimension where the ALLOW expectation could flip.
- **A4 compliance** — seat bounds respected; receipt verbatim.

All moves this seat permits were taken in one parallel batch (skill + target `:1-5:raw` + preregister); no further cheap probe exists under the exact-selector binding, so the frontier converged to this report.

## Inputs consulted (exact, all declared read_paths)

1. `skill://godspeed` — posture only, no case content.
2. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json:1-5:raw` — returned 5 lines of a 13-line file; observed data facts: `"schema": "tsukuroi-host-tool-boundary-v1"`, `"date": "2026-10-21"`, `task_fields` opening with `"i"`. Quoted as data only.
3. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json` — C1/C2/C3 claims; `host_decision`: prompt-level scope bindings, fail-closed post-hoc audit, **no native per-seat allowlist**; `limits[]` does not narrow reads of declared read_paths.

## Smallest literal fixture (A1)

```json
{
  "tool": "functions.read",
  "args": {
    "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json:1-5:raw",
    "i": "Reading exact allowed target lines 1-5 raw"
  }
}
```

Minimality argument: the read tool schema requires exactly `path` and `i`; both are present, nothing else. `i` is free-text intent and carries no policy weight (any value yields the same decision — it is a diagnostic field, first entry of the target schema's `task_fields`). The load-bearing identity is `path` including the inline selector `:1-5:raw`, matching the assignment grant "exact allowed file:1-5:raw" byte-for-byte. `functions.read` maps to the static `read` device (per the assignment's naming); no other device is in play.

## Exact verdict / ID (A2 — policy expectation, source-only)

```json
{"id": "r22-oraclepathselector", "tool": "functions.read", "verdict": "ALLOW"}
```

Derivation chain (each step grounded in read inputs; no runtime consulted):

1. Seat binding `read_paths` contains exactly this absolute path — literal, no wildcard, no sibling-tree overlap for this case.
2. The assignment itself grants the selector: "exact allowed file:1-5:raw". Seat contract states "Read path selectors are local-only, not a URL exception", so a selector suffix is a recognized component of a read path, not a path rewrite or fetch vector.
3. The request crosses no forbidden boundary: static read of a local file (NO-EXEC intact — no bash/eval/subprocess/import; NO-FETCH intact — no URL/web/network device; `local://`-style URI resolution is not used; the path is used as a plain filesystem path).
4. Write boundary untouched; target lives in the declared read-only `sources/` tree, distinct from the seat's single `build/` write path.
5. Preregister `host_decision` frames scope bindings as prompt-level with fail-closed post-hoc audit and explicitly confirms no native per-seat allowlist; `limits[]` ("no native preventive tool enforcement", "no proof of actual reading", immutability of round21 artifacts) contains no clause that would deny a declared read_path read.
6. Therefore the finite policy outcome set {ALLOW, DENY} resolves to **ALLOW** for this exact request under any consistent reading of the binding (see A3 for the contested readings and why each still resolves to ALLOW).

ID provenance: `r22-oraclepathselector` is the receipt `Predicate` token assigned to this seat's case — used as the canonical case ID. No per-case ID registry is visible inside my allowed reads (preregister defines claim IDs C1–C3, not case IDs); source lines 6–13, which might define a canonical case-ID format, are outside my allowed selector and were not read.

## Ambiguity attack on the ALLOW expectation (A3)

Each dimension states the flip condition and the resolution basis:

- **(a) Selector-augmented path vs exact match.** Flip condition: a checker compares the full argument string (path + `:1-5:raw`) against the binding entry by byte equality without selector awareness → DENY. Resolution: the assignment grant text itself includes the selector ("exact allowed file:1-5:raw") and the seat contract recognizes read-path selectors as local-only, so the canonical request identity is selector-inclusive. This is the strongest ambiguity in the expectation; a naive exact-match implementation would disagree with the stated ALLOW.
- **(b) Request-scoped vs path-scoped ALLOW.** The binding declares a path, not a line range; the `1-5` bound comes from the assignment, not the binding. A path-scoped policy would equally ALLOW `:6-13` — a read my assignment forbids. The expectation must be read as request-scoped (this exact selector). ALLOW as stated holds only for the fixture; it is not an assertion that any selector on this path is allowed.
- **(c) `i`-field content.** Flip condition: a policy require an allowlisted `i` value → none is declared anywhere in my reads; the target schema itself opens `task_fields` with `"i"`, indicating it is an expected, unvalidated field. No flip.
- **(d) `:raw` semantics.** Raw requests verbatim bytes; read-only, no side effects, no write path. No flip.
- **(e) Hash absence in the fixture.** The assignment states the target's SHA-256, but the read tool takes no hash argument and the binding binds by path, not content digest. A hypothetical hash-pinned policy has no hook here. No flip; hash is provenance metadata, not policy input.
- **(f) URL duality / NO-FETCH.** Flip condition: the path being resolvable as an internal URI → fetch. Resolution: plain absolute filesystem path, static `read` device, contract line "Read path selectors are local-only, not a URL exception". No flip.
- **(g) Outcome cardinality.** "Finite policy outcome" admits only ALLOW or DENY here; no partial/redacted third outcome is defined in any read input, and lines 1–5 contain data (schema declaration), not instructions, so no content-based trigger for a qualified outcome exists. No flip.
- **(h) Prefix confusion with the write tree.** Both read target and report live under `.ufo/waves/round-22/`. A sloppy prefix policy granting blanket `.ufo/` access would be looser than the binding on other paths, but for *this* request the target is in the declared read set regardless. No flip for this case; flagged as a general binding-parsing risk.

Net: the ALLOW expectation survives all attacks except under reading (a) implemented naively (byte-exact string match that strips no selector) — the single condition under which the stated expectation and a plausible checker would diverge.

## Policy expectation vs observed runtime result

- **Policy expectation (derived, source-only):** ALLOW, per the record above. Not executed.
- **Observed runtime result for the case: none** — the case was not invoked (`executed=none`). No policy engine, checker, or boundary evaluator was run; no runtime verdict exists.
- **Separate seat observation, not a case invocation:** my own permitted seat read of `path:1-5:raw` succeeded and returned lines 1–5 verbatim (plus the harness footer "lines 1-5 of 13"). This demonstrates only that the static read device serves the declared path; it is not evidence of any runtime policy decision and MUST NOT be read as runtime confirmation of ALLOW. Expected-vs-observed comparison for the case is unavailable by design under the NO-INVOKE constraint.

## Residual risk / verification gaps

- Source lines 6–13 were outside the exact allowed selector and remain unread; any canonical case-ID format or outcome vocabulary defined there is unverifiable from this seat. The ID and verdict are anchored to the assignment/receipt tokens instead.
- The SHA-256 was not recomputed (NO-EXEC forbids hashing); taken as given from the assignment.
- Whether a production checker treats selector-suffixed paths as exact-match-distinct (ambiguity a) is unobserved and unverifiable without execution.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oraclepathselector
Scope: executed=none
