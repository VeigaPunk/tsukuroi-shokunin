# Review23Receipts — Tsukuroi round 23, attempt 1

Seat: `TsukuroiR23-2.Review23Receipts-7` (reviewer, leaf).
Round baseline (preregister.json:2): `ae01e50f582016384e620022be38bf5367000e2e`.

Subject of review: the round-23 source `structured-edit-observations.json`
(schema `tsukuroi-structured-edit-observations-v1`, declared SHA-256
`19d85129bf0f7fd71f5aea93c35660b21d305150500dc63b58104019851af12a`), read
together with the bound round-23 snapshot tool `check-review-cohort.py` and
`preregister.json`.

Method and hard limits actually observed in this seat:

- NO-EXEC / NO-FETCH. No command was run: no hashing, listing, `wc`, import,
  test, lint, compile, subprocess or delegation was performed. Every statement
  below about checker behaviour is a literal reading of the bound source, not an
  executed result.
- The declared digest is a supplied identity. It was **not** independently
  computed or validated.
- Only the seat-bound local files were opened: the observations source,
  `preregister.json`, `godspeed-directive.txt`, `skill://godspeed`,
  `snapshot/tools/check-review-cohort.py`, and this report. No raw session
  path was opened; the source references transcripts by digest only
  (observations lines 8, 35, 57, 80) and exposes no session path, which is
  the correct shape.
- Round-22 report bodies (`build/CritRuntime.md`, `build/OraclePathArtifact.md`)
  are **not** in this seat's read binding and were not opened; they are
  referenced only as recorded paths inside the source.
- No LSP device is bound in this seat, and the seat binding forbids `xd://`
  use, so no semantic reference/definition/diagnostics service was queried.
  Findings below rest on literal reading of a single self-contained file, and
  are **not** presented as semantic proof about code outside the binding.
- Lane bounds (informational, not a receipt field): leaf member — no subagent
  dispatch.

## Axes

1. **Receipt well-formedness** — exactly one occurrence of each receipt
   prefix, and fixture/example copies indented so they cannot be read as a
   second receipt.
2. **Evidence honesty** — a well-formed receipt is a *declaration of scope*,
   never proof that no command ran, that nothing was read, or that no harm
   occurred.
3. **Structured-edit source fidelity** — whether the recorded rows can
   support the preregister's edit-decision table and C3 path arithmetic.
4. **Bound-tool identity integrity** — one canonical runtime and one
   same-identity rerouting path in the cohort checker.

## Findings

### F1 — HIGH — one of four rows is a whole-file write labelled `"tool": "edit"`, and its own evidence contradicts the label

Evidence (observations source):

- Row 0, seat `CritRuntime`: line 11 `"tool": "edit"`, lines 12–15
  `"argument_keys": ["path", "stream_content"]`, line 16 path
  `…/round-22/build/CritRuntime.md`, and `recorded_starts` (lines 19–28)
  record a **read** at line 12 and a **write** at line 13 on the same path.
  No recorded adapter step exists for the request itself (line 9
  `"request_line": 15`).
- Rows 1–3, seat `OraclePathArtifact`: line 37 / 60 / 83 `"tool": "edit"`
  with `"argument_keys": ["i", "new_string", "old_string", "path"]`.

Impact: two natural classifiers disagree on 25 % of the sample.

- A classifier keyed on `tool == "edit"` treats the row as a *structured* edit
  with an authoritative target path.
- A classifier keyed on `argument_keys` sees `path` + `stream_content` and no
  `old_string`/`new_string`, i.e. an **opaque** body with no structured target.

The preregister's decision table (preregister.json, `edit_decisions` rows
`OPAQUE_PATCH` → UNKNOWN, "Missing structured target is not inferred from
opaque patch text", and `EXPANSION` → CHECK_EACH, "Every recorded adapter
read or write remains separately scoped") requires the second reading for
this row: an opaque `stream_content` body must not inherit edit authority
from the path label. Conversely the `WRITE_ONLY_EDIT` → DENY row ("Edit also
needs its explicit target read authority") depends on the read step at line 12
being visible as a *separate* step, which the merged `recorded_starts` list
only weakly preserves.

Recommendation (source-only, bounded): the producer should record the request's
own adapter step kind and its argument shape as independent fields, and every
classifier should derive edit-ness from the argument shape
(`path` + `old_string` + `new_string`) rather than from the `tool` label; a
`stream_content` body must be classified UNKNOWN unless a separate, explicit
structured-target field asserts otherwise. Until then, no row of this source
may be cited as a structured-edit exemplar without quoting its
`argument_keys`.

### F2 — HIGH — `recorded_starts` has no ordering contract, and the four rows exhibit two mutually incompatible orders

Evidence (observations source):

- Row 0: `"request_line": 15` (line 9) with `recorded_starts` lines **12**
  (read) and **13** (write) — both *before* the request line, and neither is
  the request line itself.
- Rows 1–3: `"request_line": 30 / 33 / 36` (lines 35, 58, 81) with
  `recorded_starts` lines **31 / 34 / 37** — each *after* the request line by
  exactly one.

No single reading covers both shapes:

- "recorded steps are the adapter records of this same request" — fits rows
  1–3 (request + its record), fails row 0 (records precede the request and
  the request's own step at line 15 is missing entirely).
- "recorded steps are the seat's surrounding steps for this path" — fits row
  0, fails rows 1–3 (each row lists exactly one step, so the seat's other two
  edits at lines 34 and 37 are not enumerated there).

Impact: this is exactly the "declared arithmetic" surface of C3 and the
`EXPANSION` / CHECK_EACH row. Any per-event expansion of the rough-versus-lane
path census (preregister `outside_round22.path_counts_as_reported`: build
25 vs 23, falsify 33 vs 29) that sorts or de-duplicates by line number will
produce different expansions under the two readings of the same field, and
neither is currently defined. The source's own scope string (line 101) does
not disclaim chronology — it disclaims semantics, enforcement, effects and
reading proof only — so the field is silently under-specified.

Recommendation: add an explicit per-step role (`pre_step` / `request` /
`post_step`) or a monotonic sequence number, or state in the schema that
`recorded_starts` lines may fall on either side of `request_line`. Until
then, cite only counts and paths from this source, never a chronology claim.

### F3 — MEDIUM — the source enumerates only path-bearing steps and carries no completeness field, so its silence is not absence evidence

Evidence: observations line 101 scope — "Observed structured path metadata and
recorded adapter steps only, not universal tool semantics, native permission
enforcement, effects, or reading proof." Every recorded step in the file is a
path-bearing tool (`read` at line 21, `write` at line 26, `edit` at lines 49,
72, 95); the schema has no field for the set of tools observed per seat, no
per-seat tool inventory, and no statement of any filter applied to the
transcripts.

Impact: this is the concrete instance of "a valid receipt is not proof of
command absence". The absence of any `bash`/fetch row is a property of the
*recorded subset*, not of the seat's behaviour. Any consumer that cites S086
for "no commands were executed", "nothing was read", or "no effect occurred"
would be inferring absence from a non-exhaustive enumeration. The bound
cohort checker states the same limit in its own scope constant
(check-review-cohort.py:20): "delivered_conformant means receipt-well-formed,
not request-scope conformity, command nonexecution, reading, chronology,
no-harm or native enforcement."

Recommendation: any absence claim requires a separate enumerated-tool-
inventory artifact with a completeness statement; receipt conformance must
never be reported as command nonexecution. Cite the two scope strings above
wherever the inference is at risk.

### F4 — MEDIUM — singleton-prefix enforcement is demonstrated in the bound cohort file for one prefix only; the enforcing module is outside this seat's binding

Evidence (check-review-cohort.py):

- Line 127 — `case('duplicate-receipt', …, report + f'Reviewed-SHA256: {sha}\n'.encode(), 0, 'delivered_faulty', strict_exit=1)`:
  a second `Reviewed-SHA256:` line is a fault and the seat is accounted
  `delivered_faulty`, not converted to a pass (module docstring line 2: "…without
  converting strict receipt faults to passes").
- Line 126 — the prefix/value cases `period` (`executed=none` → `executed=none.`),
  `predicate` (`Predicate: p` → `Predicate: q`) and `digest` each mutate a
  **single** line's value. None of them duplicates the `Predicate:` or
  `Scope:` prefix, so the bound artifact contains **no** case proving that a
  duplicated `Predicate:` or `Scope:` line is detected.
- Lines 17–19 — the strict evaluator lives in `tools/check-review-snapshots.py`
  and is loaded by `importlib` at import time. That file is **not** in this
  seat's read binding, so its prefix set and duplicate rule could not be read.

Impact: the "exactly singleton receipt prefixes" requirement is only partially
evidenced inside the bound artifacts. If the strict module's duplicate rule
covers only the digest prefix, a report with two `Scope:` lines would be
classified `delivered_conformant` while violating the requirement; if it
covers all three, the requirement holds but the bound file does not show it.
Both readings are consistent with the bound evidence.

Recommendation: the round-23 review-cohort selftest should carry its own
`duplicate-Predicate` and `duplicate-Scope` cases so the property is visible
in the bound artifact rather than inherited; until then, treat duplicated
`Predicate:`/`Scope:` as **unverified** rather than as detected.

### F5 — MEDIUM — unindented fixture copies of a receipt line are a live fault vector; the bound file demonstrates the failure mode

Evidence: line 127 shows a duplicated `Reviewed-SHA256:` line is a strict
fault; line 129 (`case('unicode', …)`) shows that a trailing U+2028 after the
receipt makes the report `delivered_faulty`; line 126's `period` case shows
that a trailing character on the `Scope:` value is a fault. Line 128
(`case('crlf', …)`) shows CRLF line endings are *tolerated*
(`delivered_conformant`).

Impact: any review report that quotes the receipt format as an inline example
at column 0 manufactures exactly the duplicate-prefix fault that line 127
detects; and any trailing prose or stray separator after the receipt block
invalidates the last line.

Recommendation (applied in this report): quote receipt examples **indented
only**, never fenced and never at column 0; end the file with exactly the
three unfenced receipt lines and no content after them. Emit LF endings —
CRLF is tolerated by the strict check but changes the report bytes, which are
compared byte-exactly against the settlement digest (see F8).

### F6 — LOW — "delivered_conformant" is not the same as settlement-consistent, and byte drift is a separate finding

Evidence: line 76 sets `category = 'delivered_conformant' if one_code == 0 else
'delivered_faulty'` — a category decision based on strict receipt conformance
only. Lines 79–81 compute the report digest and add `COHORT-REPORT-DRIFT`
when the bytes differ from the settlement's `report_sha256`. Line 142's
`report-drift` case shows the combination: category `delivered_conformant`,
`strict_exit` 0, yet the cohort exits 1 with `COHORT-REPORT-DRIFT`.

Impact: a seat can be receipt-conformant and still fail the cohort on byte
identity. The scope constant (line 20) states that "Report hashes bind
evaluated-revision bytes to the trusted producer settlement, not independently
proven timing or provider causes" — the hash is a *binding to the producer's
own settlement*, not independent attestation. The same caveat applies to the
declared digest in this seat's own receipt: it is a supplied identity, never a
self-computed proof.

Recommendation: report receipt conformance and settlement byte-binding as two
distinct facts; never let `delivered_conformant` be summarised as "report
accepted".

### F7 — LOW — the observations sample cannot discriminate the eight preregister decision rows

Evidence: the file holds 4 observations, 2 seats (CritRuntime,
OraclePathArtifact), and every target is a round-22 build report
(lines 16, 44, 67, 90). There is no traversal/dot-segment path, no external
or remote URI, no declared-vs-undeclared pair, no read-only target, and no
write-only target; exactly one row has an opaque body.

Impact: the preregister rows `DECLARED_EDIT`, `UNDECLARED_EDIT`,
`READ_ONLY_EDIT`, `WRITE_ONLY_EDIT`, `EDIT_TRAVERSAL` and `EDIT_EXTERNAL`
have **no** observed instance in the bound source; only the adapter *shape*
(path + old_string + new_string versus path + stream_content) is evidenced.
C1's "Eight finite source-grounded structured-edit authority decisions" must
therefore be grounded in the new contract document, not in S086 — consistent
with the preregister's own separability note ("C1 reads only new
decision/prose/source contract"), but it means S086 must not be cited as
corroboration of any specific decision row.

Recommendation: cite S086 only for argument-shape vocabulary; cite the new
contract for each of the eight rows.

### F8 — LOW — the census counting unit is undefined in the source; three defensible units give three different numbers

Evidence: the file contains 4 observations, 5 recorded adapter steps
(read, write, and three edits), and 2 distinct target paths
(CritRuntime.md at line 16; OraclePathArtifact.md at lines 44, 67, 90).
CritRuntime's single path appears in three steps (read at line 20, write at
line 25, and the unrecorded request at line 9).

Impact: C3 requires "exhaustive per-event/component explanation" of the
rough-versus-lane deltas (build 25 vs 23 = 2; falsify 33 vs 29 = 4) with
"declared arithmetic". A census that counts recorded *events* (4), recorded
*steps* (5) or *distinct seat-paths* (2) differs by exactly the magnitudes in
question with no fault anywhere. Without a stated unit, "exhaustive" is
unfalsifiable in both directions.

Recommendation: the reconciliation record must state its counting unit
explicitly — distinct seat-path, recorded step, or observation — and show the
per-event components of the deltas under that unit before claiming
exhaustiveness.

### F9 — INFO — same-identity rerouting and one canonical runtime are enforced at the read layer

Evidence: check-review-cohort.py:203–204 — `binding = _revision.bind(ROOT,
args.revision, args.branch)` followed by
`evaluate(git_read(binding.sha, args.manifest), git_read(binding.sha, args.settlement), lambda path: git_read(binding.sha, path))`.
Every report byte is read from the single bound commit, so a seat cannot
substitute a report from another revision; line 81 then binds each report to
the settlement digest.

Limitation, per F6: the settlement is the trusted producer, so this is
identity binding *within* the producer's account, not independent attestation.

## Verification gaps

1. `tools/check-review-snapshots.py` (loaded at check-review-cohort.py:17–19)
   is outside this seat's binding; the exact prefix set and duplicate-detection
   rule could not be read. F4 therefore reports a gap in visible evidence, not
   a proven defect.
2. Round-22 report bodies for the two observed seats are outside the binding;
   whether their receipt blocks are in fact singleton could not be checked.
3. No LSP service is bound to this seat and `xd://` use is forbidden by the
   binding, so caller/definition/diagnostics checks were done by literal
   reading of one self-contained file. No grep output is offered as semantic
   proof of behaviour in unbound code.
4. The declared digest of the reviewed source was not computed, and no
   checker was executed; all behavioural statements about the checker are
   source-derived expectations, not observed runs.
5. No resume path appears in any bound artifact, so no claim is made about
   `resume_continuity_v1` preflight rejection or zero-mutation behaviour.
6. The round-23 wave bindings/events manifests referenced by the preregister
   commands are not bound to this seat; C2's captured-events side was not
   reviewed here.

## Residual risk

- If the strict module detects only digest-prefix duplication, the cohort would
  report `delivered_conformant` for a report carrying two `Scope:` lines or two
  `Predicate:` lines (F4). Until the selftest shows it, this should be treated
  as open.
- Any consumer that derives edit authority from the `tool` label rather than
  from `argument_keys` will mis-classify opaque `stream_content` writes as
  structured edits on 25 % of the observed sample (F1).
- A path census that does not declare its unit cannot be falsified against the
  rough-versus-lane deltas (F8); an "exhaustive" reconciliation without a
  stated unit is unfalsifiable rather than exhaustive.
- Receipt-conformant seats are exposed to being summarised as "no commands
  ran" or "no harm" (F3, F6); the two bound scope strings are the only
  textual guard against that reading.
- This seat could not observe execution, effects, reading completeness, or
  any native enforcement; every conclusion here is a source-level claim.

## Self-check of this report

- Each receipt prefix appears exactly once at column 0, in the three final
  unfenced lines.
- All example/fixture receipt copies below are indented and are illustrative
  only; none is at column 0.
- Nothing follows the final receipt line.
- Illustrative receipt shape (indented, not a receipt):

      Reviewed-SHA256: <64-hex-digest>
      Predicate: <predicate>
      Scope: executed=none

Reviewed-SHA256: 19d85129bf0f7fd71f5aea93c35660b21d305150500dc63b58104019851af12a
Predicate: r23-review23receipts
Scope: executed=none
