# OracleCohortStrictRed — C3 strict-receipt oracle (source-only)

## 1. Seat, inputs, and method

- Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/snapshot/tools/check-review-snapshots.py`. The assignment states its SHA-256 is `b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8`; that digest was **not** recomputed in-seat (NO-EXEC) and is used verbatim from the ticket.
- Declared read set actually used: the target file, `.ufo/waves/round-22/preregister.json`, `.ufo/waves/round-22/sources/host-tool-boundary.json`, and the godspeed skill. No other path was read.
- Constraints honored: NO-EXEC (no bash/eval/subprocess/import/selftest/compile), NO-FETCH (no URL, search, browser, or network tool), no delegation or child work. No installs or upgrades were attempted, so there is no tool/version/channel record.
- Method: literal reading of `safe_path` (lines 26-30), `physical_lines` (42-44), `evaluate` (47-128), `selftest` (145-238), and `main` (244-274). The case was **not invoked**; the only runtime claim in this report is `executed=none`.

## 2. What the strict checker actually decides (observed source facts)

For each declared review row, `evaluate` requires three exact physical lines, each the unique line beginning with its literal prefix, in an otherwise UTF-8-decodable report (lines 102, 107-112):

- digest line equals `Reviewed-SHA256: ` + `row["sha256"]` (114);
- predicate line equals `Predicate: ` + `row["predicate"]` (116);
- scope line equals `Scope: executed=none` (118).

Each unequal singleton list adds one finding; a row with zero added findings is counted in `pinned_reviews` (119-120). Exit code: 0 when there are no findings, 1 when there are content findings, 2 when any read or decode error occurred (121). The emitted `status` is `("PASS", "FAIL", "CANNOT_EVALUATE")[code]` (125). Source-hash equality is a separate comparison against the same declared digest (90), and it emits the same `REVIEW-SNAPSHOT-MISMATCH` id as a bad digest line (114).

The tool's own scope disclaimer (128): `primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution`.

## 3. Fixture F1 — smallest literal faulty-receipt fixture

Manifest bytes, one physical line, compact:

```json
{"schema":"tsukuroi-review-snapshots-v1","reviews":[{"name":"A","report":"r","source":"s","sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","predicate":"p"}]}
```

Surface files:

- `s` is the zero-length file.
- `r`, shown as a JSON string literal whose decoded value is the file's bytes:

```json
"Reviewed-SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\nPredicate: q\nScope: executed=none\n"
```

The digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` is the published SHA-256 of the zero-length input. This is the fixture's only externally sourced value; NO-EXEC forbids recomputing it here. A non-empty source variant requires hashing outside this seat (the selftest's `fixed source\n` digest is computed at runtime at line 148 and is therefore not literal).

Validation trace, with anchors:

- manifest shape: exact schema, reviews is a non-empty list (66-68); name `A` matches the 1-128 character pattern (70); `r` and `s` pass `safe_path` (26-30, 70-80); digest is lowercase 64-hex (78); predicate `p` is non-blank and control-free (79-80).
- source comparison: `sha256(b"")` equals the declared digest (90), so no snapshot finding arises from source bytes.
- report decodes as UTF-8 (102), so no encoding finding.
- digest line is the exact singleton expected value (114) — no finding.
- predicate line is `Predicate: q` while the expected value is `Predicate: p` (116) — exactly one finding.
- scope line is the exact singleton expected value (118) — no finding.
- the row is not pinned (119-120); code is 1 (121); status is FAIL (125).

### Exact source-derived verdict for F1

| field | value |
|---|---|
| exit code | `1` |
| status | `FAIL` |
| distinct_source_files | `1` |
| pinned_reviews | `0` |
| total_reviews | `1` |
| findings | exactly `[{"id": "REVIEW-PREDICATE-MISMATCH", "site": "A"}]` |
| returned scope string | `primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution` |

This is a prediction from source, not an observation: the case was not run.

C3 policy class under the preregister's four-way scheme: declared 1 = delivered-faulty 1, absent-dead 0, absent-unresolved 0. Accounting is clean relative to the declared roster, and the strict red is preserved as one finding plus exit 1. The tool does not emit that class; only the policy text supplies it.

Byte-smaller variant with the identical id: omit the predicate line entirely. `predicate_lines` becomes an empty list and line 116 fires identically (selftest cases at 175-177). The id does not distinguish a missing line from a wrong value.

## 4. Fixture F2 — minimal non-degenerate complete-accounting witness

A one-row cohort makes "accounting clean" degenerate: there is no conformant seat and no faulty seat to separate. F2 is the smallest literal manifest in which the accounting arithmetic is observable, and it is the fixture that matches the C3 policy sentence directly.

```json
{"schema":"tsukuroi-review-snapshots-v1","reviews":[{"name":"A","report":"ra","source":"sa","sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","predicate":"p"},{"name":"B","report":"rb","source":"sb","sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","predicate":"p"}]}
```

Surfaces: `sa` and `sb` are zero-length files; `ra` is the clean receipt (`Predicate: p`); `rb` is the faulty receipt (`Predicate: q`), both otherwise with the exact digest line and the exact scope line used in F1.

Exact source-derived verdict:

| field | value |
|---|---|
| exit code | `1` |
| status | `FAIL` |
| distinct_source_files | `2` (`sa`, `sb` are distinct path strings; line 84 counts strings, not contents) |
| pinned_reviews | `1` (seat A) |
| total_reviews | `2` |
| findings | exactly `[{"id": "REVIEW-PREDICATE-MISMATCH", "site": "B"}]` |

C3 policy reading: 2 declared = 1 delivered-conformant (A, pinned) + 1 delivered-faulty (B) + 0 absent-dead + 0 absent-unresolved. Accounting is clean and the strict red remains (exit 1, finding preserved). This is the finite policy outcome the preregister describes; it is not an every-receipt-conforms claim (C3_bound).

## 5. Finite outcome set for a delivered, readable receipt

The policy sentence "accounting clean; strict red remains" constrains the class but not the id. The complete finite set for a seat whose report was read and decoded is:

| surface condition | finding id | exit |
|---|---|---|
| digest line not exactly the singleton expected value, or source bytes differ from declared digest | `REVIEW-SNAPSHOT-MISMATCH` | 1 (91, 114) |
| predicate line not exactly the singleton expected value | `REVIEW-PREDICATE-MISMATCH` | 1 (116) |
| scope line not exactly the singleton expected value | `REVIEW-SCOPE-MISMATCH` | 1 (118) |
| report path absent | `REVIEW-REPORT-MISSING` | 1 (99) |
| report not decodable as UTF-8 | `REVIEW-REPORT-ENCODING` | 2 (104, 121) |
| read raises | `REVIEW-READ-FAILED` | 2 (87, 95, 121) |
| manifest invalid or manifest absent | `REVIEW-MANIFEST-SCHEMA` / `REVIEW-MANIFEST-MISSING` | 2 (123-124) / 1 (57) |

For a delivered receipt that is readable and UTF-8, exactly three ids are reachable at exit 1; F1 and F2 pin the middle one. "Strict red" alone is compatible with exit 2 as well, so the policy sentence by itself pins neither the id nor the exit code.

## 6. Ambiguity attacks on the expectation

1. **"Accounting clean" is not an output of this tool.** The only verdict vocabulary is PASS/FAIL/CANNOT_EVALUATE (125). Read as conformance, "clean" means PASS, which directly contradicts "strict red remains". The expectation is coherent only as a two-layer statement: the cohort accounting layer (four-class coverage, from C3_bound) plus the strict layer (this file). The readable source implements only the strict layer.
2. **`pinned_reviews` is a conformance count, not a delivery count.** A delivered row with one finding contributes zero (119-120). F1 reports `pinned_reviews: 0` with one delivered seat; reading that zero as "unaccounted" inverts the accounting.
3. **Findings do not one-to-one map to faulty seats.** An empty report triggers all three receipt mismatches (114, 116, 118) for one seat; a duplicate correct line also triggers a mismatch (selftest 162). Per-seat accounting requires grouping findings by `site`, which the tool does not output.
4. **"Faulty receipt" underdetermines the id and the exit code** (section 5). The policy sentence cannot select among `REVIEW-SNAPSHOT-MISMATCH`, `REVIEW-PREDICATE-MISMATCH`, and `REVIEW-SCOPE-MISMATCH`, nor exclude exit 2. Only the fixture pins the id.
5. **A digest fault is not attributable to the receipt.** Source tamper (90) and a mistyped digest line (114) emit the same `REVIEW-SNAPSHOT-MISMATCH`. The output never says which artifact is wrong, so "faulty receipt" is an interpretation, not a source-decidable fact.
6. **Predicate and scope faults are also two-sided.** The manifest declares the expected predicate (79-80) and the receipt is compared to it (116); a wrong manifest and a wrong report line are indistinguishable in output. No authority direction is encoded anywhere in the file.
7. **Omission is invisible.** `total_reviews` is `len(reviews)` (67). A seat missing from the manifest is never read and cannot be flagged. Completeness is provable only relative to *declared* seats, which is exactly the C3_bound wording, not relative to any external roster.
8. **Site identity is not the path.** Per-row findings use `row["name"]` (91, 99, 104, 114, 116, 118); manifest-level findings use the default round-21 path (57), truncated exception text (123), the literal `manifest path` (260), or arbitrary exception text (272). An "exact id" claim that omits the site is under-specified.
9. **Manifest-only defects change the code.** Uppercase digest, traversal, absolute paths, duplicate names/reports, and blank or control-bearing predicates all become `REVIEW-MANIFEST-SCHEMA` at exit 2 (69-80; selftest 169, 196-208), not receipt mismatches. Also, a schema failure after line 67 still reports `total_reviews = N` with `pinned_reviews = 0`, while a JSON parse failure reports 0; `CANNOT_EVALUATE` therefore does not imply zero totals.
10. **"Smallest" is two-valued.** One row is the structural floor (non-empty list, 66-68), but a one-row cohort cannot exhibit a conformant/faulty split. F1 is byte-minimal; F2 is the minimal non-degenerate witness. Additionally, the manifest JSON alone cannot constitute the fixture: the fault lives in the report bytes read through `read_bytes` (93), so a fixture is at least three surfaces.
11. **Receipt "faultiness" is not ordinary reading correctness.** `physical_lines` strips at most one CR before LF (42-44), so CRLF receipts pass. Only lines with the three exact prefixes are inspected (107-112); all other prose is ignored, so extra text cannot make a receipt faulty. Conversely, a UTF-8 BOM prevents the first prefix match and yields `REVIEW-SNAPSHOT-MISMATCH` despite identical visible text; an embedded `\f` or `\v` does not split a line and yields a mismatch (selftest 181-190); a duplicate correct line yields a mismatch (162-174). The predicate is exact singleton-line multiset equality, not semantic correctness.
12. **The CLI cannot consume a working-tree fixture.** `main` requires `--revision` (246-247) and reads every surface through `git_read(binding.sha, path)` (263-266), so manifest, sources, and reports must exist at the bound revision. `--selftest` is the only revision-free mode and accepts no fixture (249-250). `_revision` is outside the declared read set, so CLI fields (`revision`, `branch`, `branch_tip`) and any `RevisionError` id are not verified by this oracle.
13. **Policy compatibility of exit 2.** Because C3_bound includes `absent-unresolved` as a legitimate accounting class, an unreadable seat could still be "accounted" while the strict layer reports CANNOT_EVALUATE. The policy sentence therefore does not force FAIL; it forces FAIL only for the delivered, readable family.

## 7. Policy expectation vs source-derived prediction vs observed runtime

| layer | content | basis |
|---|---|---|
| policy expectation | complete accounting of every declared seat under the four classes, preserving strict findings; "clean" means no unaccounted seat, explicitly not every-receipt-conforms | preregister `C3_bound`; `host_decision` |
| source-derived prediction | F1 and F2 produce exit 1, status FAIL, one `REVIEW-PREDICATE-MISMATCH` at the named site, with the pinned/total/distinct values above | literal reading of 47-128; not executed |
| observed runtime result | none — the case, `--selftest`, and the CLI were all invoked zero times | `executed=none` |

No preventive runtime-enforcement claim is made or implied. The host boundary source records `native_per_seat_allowlist: false` and `tools_semantics` as additive eval-defined extras; this seat only supplies detection/evidence reasoning, consistent with C3.

## 8. Remaining unknowns and source-only falsifiers

- `tools/check-review-cohort.py`, the settlement file, and the round-22 `reviews.json` are not in the declared read set, so the cohort verdict string, its four-class mapping, and whether it consumes this manifest schema are unverified. If "verdict" means the cohort verdict, it is not derivable from my sources; only the strict half is.
- `_revision` is unreadable here, so revision binding, clean-environment semantics, and revision-error ids are out of scope.
- Completeness relative to an external seat roster cannot be checked by this file at all; only declared-seat completeness is in scope.
- The target file's digest is ticket-stated, not recomputed.
- Falsifiers, designed but deliberately not executed: if `evaluate` were run on F1 and returned exit 0, or any finding set other than the single predicate mismatch, the trace in section 3 would be wrong; if the empty-input digest constant were wrong, an extra `REVIEW-SNAPSHOT-MISMATCH` would appear, which would isolate that external constant; if a cohort tool classified a lone faulty seat as unaccounted, "accounting clean" would fail and the C3_bound reading would be contradicted. Per contract, source-only falsifiers do not execute mutated inputs.

## 9. Compliance

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclecohortstrictred
Scope: executed=none
