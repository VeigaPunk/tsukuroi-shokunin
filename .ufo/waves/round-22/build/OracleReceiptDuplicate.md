# OracleReceiptDuplicate — r22 source-only oracle, duplicate receipt line

Seat: TsukuroiR22.OracleReceiptDuplicate-3 · Date: 2026-10-21 · Mode: source-only static derivation. NO-EXEC and NO-FETCH honored: no command, subprocess, import, test, or invocation of the case; no network.

## Godspeed axes

1. **Verdict fidelity** — does the derived verdict follow necessarily from `evaluate`'s code path?
2. **Ambiguity coverage** — edge variants of "duplicate receipt line" that could change or blur the outcome.
3. **Fixture minimality** — smallest literal manifest + report + source triple that isolates one finding.
4. **Policy/observation separation** — derivation vs. the (unobserved) runtime result, never conflated.

## Target

`.ufo/waves/round-22/snapshot/tools/check-review-snapshots.py`, declared SHA-256 `b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8` (trusted as declared; not recomputed — hashing is execution). Read in full, lines 1–278.

## Policy derivation (static reading)

Per review row, after the report decodes as UTF-8 (`evaluate`, ~lines 100–121):

- `physical_lines(text)` (~38–40): split only at LF; strip at most one trailing CR per line.
- `digest_lines = [line for line in lines if line.startswith("Reviewed-SHA256:")]` (~102–104), likewise `predicate_lines`, `scope_lines`.
- Verdict gate (~109–110): `if digest_lines != ["Reviewed-SHA256: " + row["sha256"]]: add("REVIEW-SNAPSHOT-MISMATCH", row["name"])`.

The gate is **full-list equality against a singleton**: the contract is *exactly one* digest line and it must be byte-equal to `"Reviewed-SHA256: " + sha256`. Any second line with that prefix — identical copy or not — makes the collected list length ≥ 2 and fails equality. The same finding ID is also emitted by the independent source-bytes gate (~86–88: `hashlib.sha256(source).hexdigest() != row["sha256"]`).

Exit rule (~122): `code = 2 if report_encoding_error or read_error else (1 if findings else 0)`; status tuple `("PASS", "FAIL", "CANNOT_EVALUATE")[code]`. A duplicate-receipt finding with clean reads/encoding therefore yields **exit 1 = FAIL**, row unpinned (`pinned_reviews` skips it, ~121: `if len(findings) == start: pinned += 1`).

## Smallest fixture (one review row, single finding)

Manifest (literal JSON; `S` is the one non-literal slot, see note):

```json
{"schema":"tsukuroi-review-snapshots-v1","reviews":[{"name":"One","report":"wave/One.md","source":"snapshot/tool.py","sha256":"S","predicate":"fixed-five-decisions"}]}
```

Surfaces: `snapshot/tool.py` → bytes whose SHA-256 hex is `S`; `wave/One.md` → UTF-8 bytes of:

```
Reviewed-SHA256: S
Predicate: fixed-five-decisions
Scope: executed=none
Reviewed-SHA256: S
```

i.e. the canonical three-line receipt with one duplicated digest line appended (`canonical + "Reviewed-SHA256: S\n"`), matching the source's own `duplicate-digest` selftest construction (~166–167) without invoking it.

Note on `S`: it must fullmatch `[0-9a-f]{64}` (schema gate, ~69). NO-EXEC forbids computing a digest, and fabricating a hex string from memory would be fabrication; `S` is therefore declared as "the SHA-256 hex of the fixture source bytes", the same binding the source expresses at ~156 (`sha = hashlib.sha256(b"fixed source\n").hexdigest()`). With `S` so bound, the source gate passes and the receipt gate is the only failure. Schema preconditions all satisfied: non-empty `reviews`, unique `name`/`report`, `safe_path`-clean relative paths, non-empty control-free predicate.

## Exact verdict/ID (policy expectation, derived)

- Findings: exactly `[{"id": "REVIEW-SNAPSHOT-MISMATCH", "site": "One"}]` — one entry; predicate and scope lists still equal their singletons, so no `REVIEW-PREDICATE-MISMATCH`/`REVIEW-SCOPE-MISMATCH`; source digest matches, report decodes, so no encoding/read findings.
- Exit code **1**, status **FAIL**.
- Payload: `distinct_source_files: 1`, `pinned_reviews: 0`, `total_reviews: 1`; scope string "primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution". Via `main`, plus `revision`/`branch`/`branch_tip` fields (not exercised here).

## Ambiguity attacks on the expectation

1. **Identical vs. differing duplicate** — both fail identically: the gate never compares duplicates to each other, only list shape vs. singleton. A second line `Reviewed-SHA256: <different-digest>` (or with doubled space, or no space after the colon — the prefix includes the colon) fails the same way.
2. **Position/order independence** — collection is an unordered-by-position comprehension; duplicate as line 1, mid-report, or final line all fail equally. No "first-wins" or "last-wins" semantics exists.
3. **EOF/termination variants** — duplicate without trailing LF is still the final list element → fails; bare-CR-terminated (`…\r` at EOF) is CR-stripped by `physical_lines` → still qualifies → fails.
4. **CRLF** — one trailing CR stripped per line; a CRLF report with a CRLF duplicate fails identically to LF. CR-only separators do not split lines: `DIGEST…\rDIGEST…` is one physical line whose content ≠ canonical → same finding ID anyway. No bypass.
5. **ID overloading (real observability limitation)** — `REVIEW-SNAPSHOT-MISMATCH` covers three distinct causes: source-bytes digest mismatch, report digest-line absent/wrong, and duplicate digest line. Site disambiguates only to the review name, never the cause; a fixture with a wrong `S` binding would emit **two** same-ID/same-site entries (findings list length 2), indistinguishable in kind from the single-entry duplicate case. The finding ID alone is not a duplicate-line detector signal.
6. **Trailing whitespace on the canonical line** — `"Reviewed-SHA256: S "` (one entry, trailing space) already fails equality → same ID without any duplicate. The ID fires for *any* deviation from exactly-one-exact-line, not specifically duplication.
7. **Syntactic, not semantic, receipt lines** — a counterfeit second receipt disguised with a leading BOM/ZWSP/NBSP or lowercase `reviewed-sha256:` does not `startswith` the prefix, is invisible to all three gates, and the report **passes** if the canonical line is intact. Policy defines "receipt line" purely by line-start prefix; a human-visible near-duplicate can evade it. This bounds what the mismatch verdict claims: detection of prefixed-line duplication, not of rendered-text duplication.
8. **No pseudoline loophole in the caught direction** — unlike substring checks, control characters inside a duplicate (`\f`, `\v` embedded after the prefix) do not defeat the gate; the line still starts with the prefix and fails equality.
9. **Surface condition** — the verdict holds only when the report reads and decodes cleanly; an unreadable report short-circuits to `REVIEW-READ-FAILED` + exit 2 *before* any receipt scan (the `continue` at ~93–95), so the duplicate would go unreported. Verdict presupposes readable, valid-UTF-8 report.

## Policy expectation vs. observed runtime result

- **Policy expectation (this derivation):** exit 1 / FAIL, findings exactly `[{"id":"REVIEW-SNAPSHOT-MISMATCH","site":"One"}]`, pinned 0/1, distinct sources 1.
- **Observed runtime result:** none. The case was not invoked — no `evaluate`, no `--selftest`, no `main` run (NO-EXEC). The source's embedded `duplicate-digest` selftest expectation (~166–167: exit 1, `{REVIEW-SNAPSHOT-MISMATCH}`) is source text agreeing with the derivation; it too was not executed and is not an observation.

## Residual risk and verification gaps

- Declared target SHA-256 accepted, not recomputed (execution forbidden); if the snapshot bytes differed from the declared hash, line citations could shift.
- `S` never instantiated to a concrete hex (same NO-EXEC reason); the fixture is a self-consistent family, unique up to that binding.
- `_revision.py` (imported at ~15) was outside my declared read_paths; its `bind`/`clean_env` behavior is unverified. The derivation targets `evaluate`, which does not depend on it; `main`-level behavior (revision binding, `E-READ`, `CANNOT_EVALUATE`) is out of scope here.
- Finding 5/6 stand as stated limitations of the checker's ID vocabulary; no fix proposed or applied (review seat, no edits made).

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclereceiptduplicate
Scope: executed=none
