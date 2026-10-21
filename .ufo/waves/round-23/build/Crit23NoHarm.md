# Crit23NoHarm — round 23 attempt 1 critic report

Seat: Crit23NoHarm (critic, leaf). Mode: source-only, NO-EXEC, NO-FETCH. Tool installs/updates: none.
Files read: `.ufo/waves/round-23/preregister.json`, `.ufo/waves/round-23/sources/godspeed-directive.txt` (used instead of `skill://godspeed`), `.ufo/waves/round-23/sources/r22-closure.json`, `.ufo/waves/round-23/sources/structured-edit-observations.json`. Before this write, `.ufo/waves/round-23/build/Crit23NoHarm.md` did not exist.
The digest is the supplied declaration and was not independently computed.

## Verdict

The preregistration states the non-enforcement limit correctly ("No native per-seat restrictive tool interface exists"; "No runtime prevention…"). I found no explicit claim of native restriction. I found seven ways an implementation of this preregistration could still overclaim restriction or no-harm, or quietly launder r22 violations. All seven are fixable defects. A correction for each fits inside C1, C2 or C3. If none of these guards lands, the canonical judge SHOULD treat findings 1, 2 and 4 as grounds to reject. Those three either let an unaudited write pass as conformant or relabel retained r22 reds.

Axes: depth (C1), operability (C2), calibration (C3), plus no-harm/quality (preserving r22 and r21 debt).

## Findings

### 1. UNKNOWN from OPAQUE_PATCH is an evasion path unless it is fail-capable

- Counterexample: a seat sends a patch-body edit whose target exists only inside opaque body text, for example a production file. The edit table gives `OPAQUE_PATCH → UNKNOWN`, and the C2 scope says "Body data opaque". The recorder is explicitly not claimed complete ("No … recorder-completeness"). So if the adapter records no write start, `CHECK_EACH` has nothing to scope. If UNKNOWN does not count toward violations or a non-zero exit, the audit reports zero violations while a file was written.
- Evidence: `preregister.json` sets the edit decision for `OPAQUE_PATCH` to `UNKNOWN`, gives the C2 scope as "Body data opaque, no native enforcement/effects claim", and lists "No … recorder-completeness" among its limits. In r22, C2's value was being "fail-capable post-hoc detection" whose "red exits are the retained conformance result" (`r22-closure.json` notes).
- Impacted axes: operability (C2), no-harm.
- Smallest correction: C2 MUST report UNKNOWN in its own unresolved tally. It MUST never count UNKNOWN as conformant, and any UNKNOWN MUST make the exit non-zero. Add one fixture: an opaque patch with no recorded start, which must exit non-zero.

### 2. Two table rows can give opposite verdicts on one event; CritRuntime is the witness

- Counterexample: CritRuntime's r22 edit request (`call_id toolu_014nToY7USd3cckcqeieNJ4o`, path `…/round-22/build/CritRuntime.md`) has a recorded read start on `…/CritRuntime.md:raw`. Suppose a v2 binding declares the exact `.md` path for read, write and edit:
  - `DECLARED_EDIT` returns ALLOW for the request.
  - `EXPANSION/CHECK_EACH` scopes the `:raw` read separately. `EDIT_TRAVERSAL` says "No dot-segment or alternate spelling expands the target list", so that read is DENY under exact matching.
  
  One event therefore gets both ALLOW and DENY, and the table names no precedence. That is two competing authorities. If the checker instead strips `:raw` silently, that is the same unstated selector normalization r22 flagged for its path counts ("25/33 vs checker23/29 (selector-normalization differences, not decisive)").
- Evidence: `structured-edit-observations.json` observation 1, recorded start at line 12 with path suffix `:raw`; `preregister.json` rows `EDIT_TRAVERSAL` and `EXPANSION`.
- Impacted axes: depth (C1), operability (C2), calibration (C3).
- Smallest correction: C1 prose MUST say that a request is conformant only if both the request-level decision and every step-level `CHECK_EACH` decision are ALLOW. It MUST also state one explicit selector-suffix rule: either `:raw`-style read selectors resolve to the base path, or they are distinct targets. C2 and C3 MUST cite that same rule. C2 MUST NOT add a private normalizer.

### 3. CritRuntime's "recorded adapter steps" come before its request, so the attribution is unproven

- Counterexample: the CritRuntime request is at transcript line 15, but its recorded starts (read, then write) are at lines 12 and 13, before the request. For OraclePathArtifact, every start comes after its request (30→31, 33→34, 36→37). Steps recorded before a request cannot be shown to be that request's adapter expansion. They are more plausibly separate earlier read and write requests. The edit at line 15 may then have no recorded start at all; r22 counted edit as unknown-tool 16/17 [INFERENCE: whether this call is one of those 16/17].
- Evidence: `structured-edit-observations.json` (`request_line` 15 versus start lines 12 and 13); `r22-closure.json` ("edit16/17=unknown-tool16/17").
- Impacted axes: depth (C1 source grounding), operability (C2 `CHECK_EACH` attribution).
- Smallest correction: C2 MUST link a start to a request only when the start comes after the request and the call id matches, where call ids are recorded. Otherwise the start is a separate event. C1 MUST NOT cite CritRuntime as an observed witness of edit-to-read+write adapter expansion unless that link is shown.

### 4. Retroactive authorization risk: S086 events are r22 v1 violations

- Counterexample: all four S086 edit events are r22 seats whose bindings were schema v1, which has no `edit_paths`. The r22 closure counted them inside the retained reds (edit counted as unknown-tool, violations 41/46, exits 1/1/1). Suppose C1 or C2 fixtures pair these real events with a synthesized v2 binding to show `DECLARED_EDIT → ALLOW`. Any output, report or prose that says these edits were "allowed" or "conformant" becomes a retroactive authorization, which the limits forbid ("No historical manifest/report rewrite or retrospective authorization").
- Evidence: `preregister.json` (C2 scope: "legacy schema-v1 policy and historical reds unchanged"; limits); `r22-closure.json` ("violations41/46, exits1/1/1 (detections retained)"; "edit16/17=unknown-tool16/17").
- Impacted axes: operability (C2), no-harm/quality.
- Smallest correction:
  - Select v2 only from an explicit schema-v2 field in the manifest. There MUST be no defaulting or upgrade of v1 manifests.
  - Add a regression pin: re-running the C2 command on the r22 manifests must still give requests 378/995, violations 41/46, and exit 1.
  - Label any fixture that reuses S086 metadata as a counterfactual v2 binding, never as an r22 outcome.

### 5. C3 reconciliation must explain the 25/33 versus 23/29 gap without lowering violation tallies

- Counterexample: C3 explains the rough census (build 25, falsify 33) against the lane census (build 23, falsify 29), a gap of 2 and 4 paths. It could assign that gap to "normalization" (for example `:raw` suffixes, the two typo paths, or the internal URI) and then treat those paths as non-violations. That would relabel the out-of-binding reads r22 kept visible ("including two typo paths and one internal URI").
- Evidence: `preregister.json` (`path_counts_as_reported`; C3 scope: "does not relabel old violations"); `r22-closure.json` notes.
- Impacted axes: calibration (C3), no-harm.
- Smallest correction: give the C3 reconciliation record per-component explanation categories only. Its checker MUST assert that r22's frozen tallies are unchanged:
  - violations 41/46;
  - Bash requests 2 (OracleReceiptCRLF, DebtFetch);
  - receipt faults: FxC2TraceMissing (two Reviewed-SHA256 lines) and FxC2ParallelExec (period-suffixed Predicate);
  - 7 native failures, with faulty buckets 3+5;
  - r21 debt of 13 Bash calls across 9 seats and 6 fetches across 2 seats, kept as "debt, not cleared".
  
  The explanation MUST NOT change any of these counts.

### 6. "Source-grounded" overstates evidence for 6 of the 8 decisions

- Counterexample: S086 contains only same-target report edits (CritRuntime once, OraclePathArtifact three times). These are `DECLARED_EDIT`-shaped events, plus one `CHECK_EACH` case. No observed event exists for UNDECLARED_EDIT, READ_ONLY_EDIT, WRITE_ONLY_EDIT, OPAQUE_PATCH, EDIT_TRAVERSAL or EDIT_EXTERNAL. CritRuntime's `stream_content` still carries a structured `path`, so it is not OPAQUE_PATCH. Calling all eight decisions "source-grounded" in the observed-event sense would be false provenance.
- Evidence: `structured-edit-observations.json` (4 observations, each with a structured `path`); `preregister.json` (C1 scope: "Eight finite source-grounded … decisions; new document contract").
- Impacted axes: depth (C1).
- Smallest correction: tag each C1 row's provenance as either `observed: <S086 call_id>` or `synthetic fixture grounded on <contract clause>`. The C1 metric then counts validated document decisions, not observed behaviors. This matches the preregistered scope "not eight repaired runtime behaviors".

### 7. This seat is itself live evidence that native restriction is absent; decision labels must not read as permissions

- Counterexample: this seat is bound with `commands: []` and `fetches: []`. Its exposed tool surface still includes shell execution, file deletion, web fetch/search, subagent spawn, and a dynamic namespace with `eval`/`task`/`web_search`. The binding is honored by prompt compliance only. Any C2 prose or label saying "ALLOW/DENY" without qualification can be read as a runtime permission decision.
- Evidence: this session's own exposed tool schema [observed by this seat; not reproduced by command]. It matches the r22 S084 admission (`native_per_seat_allowlist=false`; the task `tools` parameter "has no restriction semantics").
- Impacted axes: operability (C2 truthfulness), no-harm.
- Smallest correction: C1 and C2 prose MUST define ALLOW/DENY/UNKNOWN/CHECK_EACH as post-hoc audit classifications of recorded requests, never as permissions granted or prevented. Keep the preregistered limits verbatim in the C2 output header. NEVER claim runtime enforcement.

## Checked and not attacked

- `ordinal_delta: 0`, `capability_acquisition: false`, `retired: []` and "No round24 starts" are consistent with bounded instruments. No ordinal inflation was found.
- The separability statement (C3 never reads new C1/C2 content) is sound if finding 2's shared selector rule lives in the C1 contract, and C3 cites only the frozen r22 evidence plus its own reconciliation record.
- This seat's binding is internally consistent with `DECLARED_EDIT`: the report path appears in read, write and edit. `skill://godspeed` is a declared read, not an edit target, consistent with `EDIT_EXTERNAL`.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23-crit23noharm
Scope: executed=none
