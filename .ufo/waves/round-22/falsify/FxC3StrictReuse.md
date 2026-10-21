Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3strictreuse
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.

# FxC3StrictReuse — source-only falsification of check-review-cohort.py (round-22)

## Basis and limits

- Source reading only. Nothing was executed: no command, test, import, compile, git call, mutation, URL read, or delegation. Observed runtime: none. Verification exercised: none. Installs or updates: none.
- The declared digest is carried as the reviewed value and is NOT verified here. Computing SHA-256 needs execution, which NO-EXEC forbids. The read tool's tags (ADD3, DA85, 1303, CCDA, 06D1, 1169, 5412) are hashline snapshot tags, not SHA-256. The digest string occurs in no declared file.
- Read coverage: check-review-cohort.py in full (164 lines); check-review-snapshots.py in full (278 lines); _revision.py lines 1–192 plus a grep of the whole file (selftest body, lines 195–440, not read); preregister.json, sources/host-tool-boundary.json, corpus seat-boundary-r22.json and .md in full; skill://godspeed. Not read because outside the binding: build/ inputs, snapshot/, other falsify reports.
- "Expected fixture verdict" means what the file's own selftest table asserts, traced by hand. "Observed runtime" is always none.

## Answer

- Per-row strict receipt identity (check-review-snapshots.py): holds against every attack tried (B1–B5).
- Cohort layer, four source-visible failures: strict receipt faults never reach the exit code or status (F1); the calibration field reads 1 on exit-2 failure (F2); a failed or unknown seat holding a well-formed receipt is accounted delivered-conformant (F3); and the executing evaluator is bound neither to the reviewed digest nor to the revision it validates (F5).
- Primary hashes against final evaluator provenance: the primary hashes (manifest sha256, digest line, report_sha256) are compared only with source bytes and with each other. None is compared with the evaluator's own identity, and that identity is never emitted. Counterexample: F5.

## Findings

### F1 — High — Strict receipt faults exit 0 with status PASS

- Target L70: `code = 2 if strict_code == 2 else (1 if findings else 0)`. `findings` (L25, L28, L67, L69) can hold only COHORT-UNRESOLVED or COHORT-STRICT-UNAVAILABLE, so a strict exit of 1 never reaches the exit code. L79 derives status from that code.
- One object can therefore show `status: PASS`, `findings: []`, `strict_conformance: FAIL` (L73), and a nonempty `strict_receipt_findings` (L72).
- Preregister C3_bound (preregister.json L9) intends accounting, not conformance. The conflict is the shared PASS label and exit code, which a consumer reads as conformance. It also contradicts target docstring L2 ("without converting strict receipt faults to passes") and corpus seat-boundary-r22.md L24 ("Clean accounting is never a clean strict receipt verdict or permission to waive a failed receipt").
- Expected fixture verdict (selftest table): dead-missing, partial-failed, period, predicate, digest, duplicate-receipt, unicode all expect exit 0 (L95–L102). Observed runtime: not run.
- Proposed negative fixture: one review, outcome completed, scope line `executed=none.`. Expected: exit 1 or 2, status not PASS, top-level findings nonempty. Observed: not run.

### F2 — High — C3 metric reads 1 on CANNOT_EVALUATE exits

- Target L76 (COHORT-SCHEMA) and L78 (COHORT-READ) return exit 2 with `cohort_accounting_mode: 1`; L79 sets status CANNOT_EVALUATE. Schema failures occur before any category is computed (L31–L51), so the metric asserts accounting that never ran. A read failure at L55 propagates out of the loop and discards the rows already collected, yet the metric is still 1.
- The field is also inconsistent elsewhere: 0 on manifest-missing (L24); absent on the unsafe-path and RevisionError exits (L149–L150, L156, L158).
- Preregister C3 (preregister.json L7) targets `cohort_accounting_mode` = 1. The selftest never asserts this field or `status` (L117).
- Expected fixture verdict (L110, duplicate-json-key): exit 2, COHORT-SCHEMA; metric not asserted. Proposed: metric 0 or absent with exit 2. Observed: not run.

### F3 — Medium — Failed or unknown seat with a well-formed receipt is accounted delivered-conformant

- Target L58–L61: outcome is consulted only when the report is absent. A row with outcome `failed` (non-empty error, passes L44–L45) and a well-formed report gets category delivered_conformant (L61), exit 0, no finding. The emitted row shows `outcome: failed` beside `category: delivered_conformant`.
- Nothing binds a receipt to its seat, agent, round or time. The receipt has three lines and no agent identity, and strict scope disclaims chronology (check-review-snapshots.py L127–L128). A stale or copied receipt at a dead seat's path is credited as delivery.
- The selftest has no failed-plus-conformant case (L93–L110).
- Conflicts with corpus checklist item 3 (seat-boundary-r22.md L30: "Mark incomplete trace coverage could-not-evaluate, not zero activity") and DEAD → UNKNOWN (seat-boundary-r22.json L40–L45).
- Expected fixture verdict (proposed): not delivered_conformant without a could-not-evaluate marker or a finding. Source trace: delivered_conformant, exit 0. Observed: not run.

### F4 — Medium — Absent seats: failed exits PASS, unknown exits FAIL; an all-dead cohort passes

- Target L59: absent + failed → absent_dead; absent + completed or unknown → absent_unresolved. Only absent_unresolved adds a finding (L66–L67). absent_dead never affects `code` (L70).
- Consequences: a provider-failed seat with no report exits 0 (status PASS), while the same seat with outcome unknown exits 1. A cohort where every seat failed with observed errors and left no reports exits 0 (status PASS). The selftest pins the single-seat form (L95).
- Corpus DEAD → UNKNOWN (seat-boundary-r22.json L40–L45; seat-boundary-r22.md L18) is not applied to the exit.
- Expected fixture verdict (existing, L95): exit 0. Proposed: all-dead cohort gives exit ≠ 0 or could-not-evaluate. Observed: not run.

### F5 — High (provenance) — Executed evaluator is not bound to the reviewed digest, its imports, or the validated revision

- L13 `import _revision` resolves through sys.path[0], the running script's tools/ directory. L15–L18 load check-review-snapshots.py from ROOT/tools, where ROOT is the checkout containing the running script. Both are working-tree files.
- L152–L153: `--revision` binds the data reads (git_read, L124–L131). It does not bind the code that evaluates them. `_revision.bind` (_revision.py L172–L192) is working-tree code too.
- The reviewed digest 34b532… covers check-review-cohort.py only. No declared file pins a digest for check-review-snapshots.py or _revision.py, and a grep for a 64-hex run found none in the declared files.
- The output carries no evaluator identity. Result keys (L71–L74) plus main's additions (L154) are counts, strict fields, seats, findings, scope, revision, branch and branch_tip. No evaluator or imported-module digest appears.
- Consequences: (a) a manifest entry that pins the committed cohort file validates committed bytes, while the code doing the validation is the working-tree copy, and nothing compares the two; (b) an edit to check-review-snapshots.py or _revision.py changes C3 verdicts with no change to the reviewed file; (c) "imported unmodified" is a convention. Call sites are unpatched (B7), but the imported code's identity is neither verified nor recorded.
- Expected fixture verdict (proposed): output includes evaluator and imported-module digests, and the run refuses when they differ from pins. Source trace: no such check. Observed: not run.

### F6 — Medium (needs local ref write) — Replace refs can substitute bytes behind a bound revision

- git invocations without `--no-replace-objects`: target L125 and L128; check-review-snapshots.py L132 and L136; _revision.py `_git` L69–L77, used by rev-parse (L100, L119), cat-file (L127) and merge-base (L157).
- clean_env (_revision.py L62–L66) strips every GIT_* variable, so GIT_NO_REPLACE_OBJECTS cannot arrive from the environment, and it sets no replacement control.
- Documented git behaviour (git-replace(1)): object reads, including the tree and blob reads behind `rev:path`, and ancestry walks, honour refs/replace/* unless disabled. A local replace object can therefore substitute the manifest, settlement, sources, reports or ancestry. The "landed" check (_revision.py L184) uses that same ancestry.
- Precondition: a refs/replace/* object present in the checkout. [INFERENCE: default clone and push refspecs do not carry refs/replace.]
- Expected (source-only): every git argv carries `--no-replace-objects`. Observed: not run.

### F7 — Low — One receipt credited to two seats

- Target L52–L65 categorizes each row independently. Strict L69–L81 checks report uniqueness by path string only (L72). Two rows whose report paths reference the same committed blob, with the same source and predicate and distinct settlement agents, each yield delivered_conformant with identical report_sha256 (L65), exit 0, no finding.
- Holds under the declaration-only scope (cohort SCOPE L19; strict SCOPE L125–L128). Recorded as undetected reuse, not as a violated stated claim.
- Expected (proposed): duplicate report_sha256 across rows surfaces as a finding. Source trace: none. Observed: not run.

### F8 — Low — No path-scope constraint on report references

- strict safe_path (L26–L30) checks syntax only. A round-22 manifest may name round-21 receipts whose digests and predicates still match, and they will be delivered_conformant. Chronology is disclaimed, so this holds by stated scope.
- The cohort never calls strict.main or strict DEFAULT (L18, round-21), so the round-21 default is unreachable from C3.

### F9 — Low — Read failures are labelled as receipt faults

- strict L86–L89 and L94–L97 set read_error, so one_code is 2 (L121) and cohort L61 labels the row delivered_faulty. The whole-cohort exit is 2 regardless (L70). The effect is on counts and on F2's metric.

### F10 — Low — Identity and vocabulary

- Agent uniqueness is exact-string (L42). Spelling variants of one agent ("X" and "X ") are accepted as two agents.
- The code emits absent_dead, absent_unresolved, delivered_faulty. Preregister C3_bound (line 9) and the corpus use hyphens. A consumer matching the preregister text misses these keys.

## Attacks that hold (bounded)

- B1 Receipt equality. Digest, predicate and scope matching is whole-physical-line equality on column-0 lines (strict L42–L44, L107–L118). Bare CR, U+2028, FF and VT do not split lines and cannot create or hide a declaration; they produce mismatches (strict L181–L190; cohort L101–L102). Indented copies are ignored, which fails closed when a declaration is only indented. Column-0 fenced copies produce duplicates, which fail closed. No bypass found.
- B2 Duplicates. Duplicate JSON keys are rejected at every load (strict unique_object L33–L39; cohort L30–L31). Duplicate review names and report paths are rejected (strict L72). Duplicate names and duplicate agents are rejected in settlement rows (cohort L42). The settlement name set must equal the manifest name set (L50).
- B3 Path safety. safe_path rejects absolute, traversal, empty, `.`, `..`, backslash, and control or surrogate characters (strict L26–L30; has_controls L21–L23 includes Cs) before any git argument is built. Cohort main also checks paths (L148). Git arguments are argv lists; no shell.
- B4 Per-row consistency. The one-manifest re-evaluation (L56–L57) cannot diverge from the full evaluation for a row, because full-manifest validation (L34–L35) runs first and rejects every cross-row defect, and the per-row checks are identical.
- B5 Single snapshot. Every data read (manifest, settlement, sources, reports and the repeated per-seat reads) goes through binding.sha (L152–L153). No working-tree read is on the data path, so a seat's category and the strict verdict cannot read different bytes (subject to F6).
- B6 Infrastructure fails closed. Strict code 2 always yields cohort exit 2 (L70) with COHORT-STRICT-UNAVAILABLE (L68–L69). Encoding and read failures are not converted to PASS (selftest L103 expects 2). A missing settlement with a present manifest raises TypeError at L31 and exits 2 as COHORT-SCHEMA.
- B7 No patching. The cohort never assigns to strict attributes. Calls at L33 and L57 (and strict.safe_path at L148) use strict's functions as loaded. Call-site unmodified holds; file identity does not (F5).
- B8 Completed-but-absent seats. absent_unresolved exits 1 with COHORT-UNRESOLVED (L58–L59, L66–L67).
- B9 Import-time effects. sys.dont_write_bytecode is set before both imports (cohort L12–L13). Strict has a main guard (L277–L278), as does _revision (L435). No import-time I/O appears in the ranges read.
- B10 Revision binding. Non-landed or unreadable revisions return CANNOT_EVALUATE with findings (cohort L155–L158). Documented limit: the origin-pushed check applies only when refs/remotes/origin/<branch> exists (_revision.py L173, L186–L191).
- B11 Attribution. Each row emits name, agent, outcome, error, strict_exit, strict_findings and report_sha256 (L63–L65), which preserves observed-error attribution (checklist item 3). report_sha256 is evidence only; nothing compares it.

## Selftest expectations (expected fixture verdict; observed runtime: none)

Cohort selftest (target L93–L110). Source trace agrees with every row.

| Case | Line | Expected exit | Expected category / finding | Source trace | Observed |
|---|---|---|---|---|---|
| clean | 93 | 0 | delivered_conformant; strict 0 | agrees | not run |
| dead-missing | 95 | 0 | absent_dead; strict 1 | agrees (F1, F4) | not run |
| partial-failed | 96 | 0 | delivered_faulty; strict 1 | agrees (F1) | not run |
| missing-unresolved | 97 | 1 | absent_unresolved; COHORT-UNRESOLVED | agrees | not run |
| period, predicate, digest | 98–99 | 0 | delivered_faulty; strict 1 | agrees (F1) | not run |
| duplicate-receipt | 100 | 0 | delivered_faulty; strict 1 | agrees (F1) | not run |
| crlf | 101 | 0 | delivered_conformant; strict 0 | agrees | not run |
| unicode | 102 | 0 | delivered_faulty; strict 1 | agrees (F1) | not run |
| encoding | 103 | 2 | delivered_faulty; COHORT-STRICT-UNAVAILABLE; strict 2 | agrees | not run |
| dropped, duplicate, unknown, false-death | 104–106 | 2 | COHORT-SCHEMA | agrees | not run |
| manifest-missing | 107 | 1 | COHORT-MANIFEST-MISSING | agrees; metric 0, not asserted | not run |
| duplicate-manifest | 108–109 | 2 | COHORT-SCHEMA | agrees | not run |
| duplicate-json-key | 110 | 2 | COHORT-SCHEMA | agrees; metric 1 emitted (F2) | not run |

Strict selftest (check-review-snapshots.py L155–L222), 24 cases; source trace agrees with each:
- exit 0: clean.
- exit 1, MANIFEST-MISSING: missing-manifest.
- exit 1, REPORT-MISSING: missing-report.
- exit 1, SNAPSHOT-MISMATCH: source-tamper, report-digest, duplicate-digest.
- exit 1, PREDICATE-MISMATCH: predicate, duplicate-predicate, missing-predicate, case-shifted-predicate, form-feed-pseudoline, vertical-tab-pseudoline.
- exit 1, SCOPE-MISMATCH: scope-period.
- exit 2, MANIFEST-SCHEMA: duplicate, traversal, absolute, empty, control-path, control-predicate, whitespace-predicate, malformed-json, duplicate-json-key.
- exit 2, REPORT-ENCODING: invalid-report-utf8.
- exit 2, REPORT-MISSING and READ-FAILED, total 2, pinned 0: read-failed-retains-missing.

## Proposed negative fixtures (not added; no production edits)

Each is stated with its expected verdict in F1–F7. None was executed.
