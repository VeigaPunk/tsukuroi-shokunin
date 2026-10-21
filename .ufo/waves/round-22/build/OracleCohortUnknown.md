# OracleCohortUnknown — source-only oracle: declared review, no report

## Axes (godspeed)

- **Identity** — exact emitted finding ID, exit code, status, and counts for the
  "declared review, report absent" path.
- **Minimality** — smallest manifest literal that still survives shape validation and
  reaches that path.
- **Ambiguity** — every alternative reading of "no report" that changes the exit code
  or the ID set.

Moves kept: the fixture below passes every validator in `evaluate` and reaches the
missing-report branch by construction. No axis regressed; nothing was executed.

## Method and authority

- Read only the three seat-declared paths; wrote only this declared report; no
  bash/eval/subprocess/import, no fetches, case not invoked, no tools installed.
- `snapshot/tools/check-review-snapshots.py` read in full (278 lines). Token
  enumeration used `grep` on that file only. No `lsp` device is mounted in this seat,
  so grep is a literal fallback for enumeration, never semantic proof; all semantics
  below come from reading the whole file.
- The checker's own scope string disclaims proof of reading, chronology, or command
  nonexecution, so this oracle proves declaration-level identity only.

## Observed source facts

1. Manifest shape: top-level dict, `schema == "tsukuroi-review-snapshots-v1"`,
   `reviews` a non-empty list; otherwise `REVIEW-MANIFEST-SCHEMA`, exit 2
   (lines 61–66, 122–124).
2. Every row requires all five keys and rejects duplicates: `name` matching
   `[A-Za-z0-9][A-Za-z0-9._-]{0,127}` and unique, unique `report` via `safe_path`,
   `source` via `safe_path`, `sha256` as 64 lowercase hex, and a non-blank,
   control-free `predicate` (69–78).
3. Per row, the source is read first (85). A raising read emits `REVIEW-READ-FAILED`,
   sets `read_error`, and skips the row (86–89); a `None` source or digest mismatch
   emits `REVIEW-SNAPSHOT-MISMATCH` and continues to the report (90–93).
4. The report read raising emits `REVIEW-READ-FAILED` and sets `read_error` (94–97).
   A report of `None` emits `REVIEW-REPORT-MISSING` with `site` = the row name (98–99);
   a non-`None` report is decoded and its three receipt line families are compared
   exactly (100–118).
5. Exit selection: 2 if any encoding or read error occurred, else 1 if any finding
   exists, else 0 (121). Status map is `PASS`/`FAIL`/`CANNOT_EVALUATE` (125).
6. `git_read` returns `None` only when `git show` fails **and** `ls-tree` succeeds with
   empty output (131–140); any other git failure raises (141).

## Smallest literal fixture JSON

One row, five required keys, shortest valid literal per key. The manifest literal is:

```json
{"schema":"tsukuroi-review-snapshots-v1","reviews":[{"name":"a","report":"r","source":"s","sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","predicate":"p"}]}
```

Read surface that realizes "no report":

```text
source "s" -> b""        (empty committed blob)
report "r" -> None       (path absent from the pinned revision)
```

Minimality: two top-level keys and one row are forced (0 rows → schema error, line
65–66). Five row keys are forced (line 70–77). `name`/`report`/`source`/`predicate`
are one-character literals satisfying the regex and `safe_path`; `sha256` has a forced
64-hex width. `predicate` is `"p"` because a blank or control-bearing predicate is
rejected at schema level.

The digest is SHA-256 of the empty input, a published standardized constant. It was
not recomputed here (NO-EXEC). If that constant is not trusted, the digest-independent
variant below yields exit 1 with two IDs instead of one: `source "t" -> None`,
`sha256` = any 64-hex literal (e.g. 64 zeros), `report "r" -> None` →
`REVIEW-SNAPSHOT-MISMATCH` plus `REVIEW-REPORT-MISSING`, same exit 1, same counts.

CLI realization: commit `s` as an empty file in the pinned revision and do not commit
`r`; `git show rev:r` then fails, `ls-tree -z rev -- r` returns empty output with
return code 0, so `git_read` returns `None` (139–140) rather than raising. The JSON
alone does not determine the outcome — the committed tree and the `--manifest`
selector do.

## Derived verdict (source-derived; NOT executed)

Given the fixture and surface above, a single row, digest matching:

```json
{"distinct_source_files":1,"findings":[{"id":"REVIEW-REPORT-MISSING","site":"a"}],"pinned_reviews":0,"scope":"primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution","status":"FAIL","total_reviews":1}
```

- exit code: **1**
- status: **FAIL**
- exact finding ID: **REVIEW-REPORT-MISSING**, `site` = `a`
- `total_reviews` 1, `pinned_reviews` 0 (the row is not pinned because findings grew,
  119–120), `distinct_source_files` 1 (81).

CLI mode adds `revision`, `branch`, `branch_tip` after `evaluate` (266); the
`evaluate` payload above is the part derivable from source alone.

## Ambiguity attack on the expectation "absent_unresolved; exit 1"

**A1 — vocabulary.** `absent_unresolved` appears nowhere in the tool: grep over the
full file returns zero matches for `absent`, `unresolved`, or `cohort`. The tool's
finding IDs are exactly `REVIEW-MANIFEST-MISSING`, `REVIEW-READ-FAILED`,
`REVIEW-SNAPSHOT-MISMATCH`, `REVIEW-REPORT-MISSING`, `REVIEW-REPORT-ENCODING`,
`REVIEW-PREDICATE-MISMATCH`, `REVIEW-SCOPE-MISMATCH`, `REVIEW-MANIFEST-SCHEMA`, and
its statuses are exactly `PASS`/`FAIL`/`CANNOT_EVALUATE`. The policy label is C3
cohort vocabulary (preregister line 9, hyphenated `absent-unresolved`), not an
in-tool verdict. The expectation is therefore category-shifted: exit 1 is right, the
literal ID is `REVIEW-REPORT-MISSING`.

**A2 — absent vs unreadable.** `None` yields exit 1; an exception yields
`REVIEW-READ-FAILED` and exit 2. `git_read` returns `None` only on the
show-fails/ls-tree-empty branch; every other git failure raises. "No report" reaches
exit 1 only on the committed-absent branch.

**A3 — missing file vs empty file.** A committed empty report is `b""`, not `None`,
so it emits all three of `REVIEW-SNAPSHOT-MISMATCH`, `REVIEW-PREDICATE-MISMATCH`,
`REVIEW-SCOPE-MISMATCH` and still exits 1. Exit 1 cannot distinguish "no report" from
"report with no receipt"; only the ID set can.

**A4 — other exit-1 paths.** `REVIEW-MANIFEST-MISSING` (manifest itself absent,
57–58), digest mismatch, predicate mismatch, scope mismatch and duplicate digest line
also exit 1. Exit 1 is necessary but never sufficient to identify this case.

**A5 — digest coupling.** If the source surface does not match the declared digest,
`REVIEW-SNAPSHOT-MISMATCH` is added alongside `REVIEW-REPORT-MISSING` (90–91). A
single-ID expectation silently depends on a correct source digest, which the JSON
literal cannot express by itself.

**A6 — omission is not absence.** Dropping the `report` key, or setting it to `""` or
`null`, fails `safe_path` and produces `REVIEW-MANIFEST-SCHEMA` at exit 2 — the
opposite of the expectation. Absence must be a valid declared path with no committed
file. The same holds for omitting `source`, `sha256`, or `predicate`.

**A7 — any other read/encoding error escalates.** `read_error` and
`report_encoding_error` are global (121): one missing report plus any other
unreadable source, unreadable report, or non-UTF-8 report anywhere in the manifest
turns the whole run into exit 2. The single-row fixture deliberately excludes that
path.

**A8 — no per-review outcome field.** The payload has no per-seat/per-review outcome
enum; "unknown outcome" can only be a global `FAIL` plus a finding ID. An oracle that
requires a per-row `absent_unresolved` value cannot be satisfied by this tool.

**A9 — pinned-count trap.** `pinned_reviews` is 0 while `total_reviews` is 1 for this
case; a check asserting `pinned == total` would reject a correct missing-report
result.

**A10 — root resolution.** `ROOT = Path(__file__).resolve().parents[1]` (17). In the
snapshot copy this resolves to the snapshot directory, not the repo root, so
repo-relative fixture paths resolve differently under the snapshot copy than under a
repo-rooted `tools/` copy. The fixture is source-faithful, but invocation context is
part of the contract.

## Policy expectation vs observed runtime

- **Policy expectation supplied to this seat:** finite outcome `absent_unresolved`,
  exit 1.
- **Source-derived literal:** `REVIEW-REPORT-MISSING`, status `FAIL`, exit 1, counts
  `total=1`, `pinned=0`. Exit 1 confirmed; `absent_unresolved` refuted as an emitted
  identifier of this tool.
- **Observed runtime result:** none. NO-EXEC was honored; the case was not invoked,
  so no exit code was observed and none is claimed. The payload above is derived
  statically and independently corroborated by the embedded selftest expectations at
  lines 157 (`missing-report` → exit 1, `REVIEW-REPORT-MISSING`) and 221–222
  (a raising read escalates to exit 2 with `REVIEW-READ-FAILED` retained alongside
  `REVIEW-REPORT-MISSING`).
- **C3 boundary:** the preregister's C3 command targets `tools/check-review-cohort.py`
  with `build/reviews.json` and `build/settlement.json` (line 7). That tool and those
  manifests are outside this seat's declared paths, so whether it emits the literal
  `absent_unresolved` cannot be confirmed here. Reporting inability rather than
  improvising: only the snapshot checker's missing-report path was derivable.

## Remaining unknowns

1. Whether `tools/check-review-cohort.py` emits `absent_unresolved` literally and at
   which exit code — outside the declared read set.
2. Whether the live `tools/check-review-snapshots.py` is byte-identical to the
   snapshot copy — outside the declared read set.
3. The empty-string SHA-256 constant was cited from knowledge, not recomputed
   (NO-EXEC); the digest-independent variant removes that dependency at the cost of a
   second ID.
4. `_revision.bind` field semantics (`branch_tip` provenance) — outside the read set.
5. `DEFAULT` still points at `.ufo/waves/round-21/reviews.json` (18), so a CLI run
   that omits `--manifest` audits round 21, not round 22; the preregister command
   passes an explicit manifest, so this is a calibration hazard, not a defect in this
   case.

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclecohortunknown
Scope: executed=none
