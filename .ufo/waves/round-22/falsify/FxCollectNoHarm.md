# FxCollectNoHarm — round-22 source-only falsification

Target: `.ufo/waves/round-22/candidate/.ufo/waves/round-22/collect.py` (134 lines; read under hashline tag 64A3).
Declared SHA256 (echoed, not recomputed under NO-EXEC): 3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a
Attack: cross-axis. No ordinal, host, freshness, reading or noharm certificate from accounting (`settlement.json` rows) or terminaltrace (`events.json` rows built from transcript lines).
Method: source-only over declared paths. No fixture executed, no mutated input, no production edit, no tool installed. Expected fixture verdicts are derived from source; observed runtime is "not executed" throughout.
Lane bounds (informational): leaf member, no subagent dispatch.

## Result

Overall: PARTIAL. No explicit certificate is emitted on any of the five axes. Implicit support is falsified for noharm and for accounting completeness.

| Axis | Verdict | Basis |
|---|---|---|
| Ordinal | HOLDS (bounded) | No ordinal emitted or computed; preregister ordinals are never read. |
| Host | HOLDS (bounded) | No host or allowlist field emitted; host decision never read; a missing `start_line` is not a refusal record. |
| Freshness | HOLDS as certificate; FAILS as currency | No timestamp, run id, registry digest or transcript-directory identity. Output can be stale, root-redirected or silently replaced (CX-10, CX-11). |
| Reading | HOLDS (bounded) | Only assistant `toolCall` blocks and `tool_execution_start` are read; no result or end handling. Requests are not reads. |
| NoHarm | FAILS as implicit support | No harm verdict is emitted, but events and settlement can read clean (no forbidden name, `complete: true`, outcome `completed`) for transcripts that contain forbidden requests (CX-1 to CX-6). |

Severity: High 4 (CX-1, CX-3, CX-4, CX-7). Medium 7 (CX-2, CX-5, CX-6, CX-8, CX-9, CX-10, CX-11). Low 2 (CX-12, CX-13).
Most consequential: the request projection can omit or misname forbidden calls (CX-1, CX-4, CX-6), and accounting can call an incomplete seat delivered (CX-3) or shrink or double the denominator (CX-7).
Conditional items (CX-1, CX-2, CX-5, CX-6) depend on transcript shapes or consumer handling that declared reads cannot observe. Each states its trigger. Unobserved facts are marked [INFERENCE].

## Reads performed (declared paths only)
- collect.py: whole file (bare read plus ranges 24-30, 42-117, 128-134).
- preregister.json, sources/host-tool-boundary.json, corpus/knowledge/seat-boundary-r22.json, seat-boundary-r22.md, skill://godspeed: whole files.
- tools/check-review-snapshots.py: lines 3-14, 26-73, 99-178, 202-213, 243-277 (partial; cited for precedent only).
- tools/_revision.py: lines 1-41 (header; not relied on).
- Not readable: check-seat-bindings.py (C2 consumer), check-review-cohort.py (C3 consumer), swarm-registry.json, bindings.json, reviews.json, any transcript.

## Counterexamples

Each entry gives source lines, an input shape (prose, not a fixture file), emitted output, expected fixture verdict, observed runtime, conditionality and a fix direction (not applied).

### CX-1 (High, noharm): prefixed parallel wrapper is never expanded
- Source: line 23 tests the raw name against `multi_tool_use.parallel` and `parallel`. Line 31 strips `functions.` for leaf names only. Line 33 returns `{}` for everything else.
- Input shape: assistant toolCall named `functions.multi_tool_use.parallel` (or `functions.parallel`) whose `tool_uses` holds a `functions.bash` child.
- Emitted: `{'tool': 'functions.multi_tool_use.parallel', 'args': {}}`. The child never reaches events.json. `complete` is unaffected because line 106 ignores tool identity.
- Expected fixture verdict: the child's recipient name projected as lines 27-29 do for the unprefixed spelling, or seat `complete: false`. A bash child must be visible to any name check.
- Observed runtime: not executed (NO-EXEC).
- Conditionality: the leaf branch's prefix handling (line 31) suggests prefixed names occur [INFERENCE]. The bypass needs the auditor to normalise `functions.` before its wrapper allow-check. A non-normalising auditor denies the wrapper as unknown, which fails closed. The auditor is outside declared reads.
- Fix direction: normalise the prefix once, before line 23, and project children for both spellings.

### CX-2 (Medium, noharm): parallel children dropped without a flag
- Source: lines 24-26 (`tool_uses` not a list gives `{'tool_uses': None}`). Line 29 (non-dict child gives `None`). Lines 21-22 (non-dict `parameters` gives `None`). Children under any other key are never read.
- Input shapes: `tool_uses` as an object or string; a child given as a bare string; children under a different key.
- Emitted: wrapper row with `tool_uses: None` or a `null` child entry. `complete` stays true.
- Expected fixture verdict: `complete: false`, or CANNOT_EVALUATE for the seat, because requested children cannot be projected.
- Observed runtime: not executed.
- Conditionality: if the substrate also emits a `tool_execution_start` per child with its own `toolCallId` [INFERENCE], that child is recorded as its own call (lines 85-87) and is visible.
- Fix direction: mark the row incomplete rather than emit null children.

### CX-3 (High, accounting to noharm and calibration): settlement says `completed` for an incomplete trace; no declared consumer sees both
- Source: line 61 (an unparseable line sets `parsed = False`). Lines 99-100 (`completed` from final text alone). Line 106 (`complete` false). Lines 103-105 (settlement row has no coverage or `complete` field). Preregister line 7: C3 reads reviews.json and settlement.json only. Preregister line 6: C2 reads bindings.json and events.json only.
- Input shape: one unparseable line inside an otherwise final trace. A forbidden request could sit in that line.
- Emitted: settlement row `outcome: completed`; events row `complete: false`. C3 never sees the events row, so the seat is counted delivered.
- Expected fixture verdict: outcome not `completed` (could-not-evaluate, per seat-boundary md line 30), or a coverage field in the settlement row that C3 must consume.
- Observed runtime: not executed.
- Conditionality: none for the source behaviour. C3 internals are unread.
- Fix direction: carry `complete` into the settlement row; downgrade `completed` when `parsed` is false.

### CX-4 (High, noharm): execution identity is discarded when a request shares the id; duplicate starts collapse
- Source: line 76 stores request name and args. Lines 84-86 read the start event's `toolName` and `args` only when the id is absent from `calls`. Line 84 overwrites `starts[ident]` each time. The asymmetry: start-before-request is flagged (lines 72-75 set `parsed = False`); request-before-start is silent.
- Case A (request first): toolCall id X, name `read`, path `a.md`; then start event id X with `toolName: bash`. Emitted: `read`, with `start_line` of the bash start, and `complete: true`.
- Case B (no request): start id X `read`, then start id X `bash`. Emitted: `read`, with `start_line` of the second line. The bash execution is absent and `complete: true`.
- Expected fixture verdict: `complete: false` for both cases, with both executed names visible.
- Observed runtime: not executed.
- Conditionality: needs an id collision or a substrate mismatch [INFERENCE that the substrate can produce one]. The source has no defence.
- Fix direction: compare name and args across request and start, flag mismatches, and keep every start rather than last-wins.

### CX-5 (Medium, scope and noharm): arguments silently dropped or defaulted; `complete` ignores it
- Source: lines 21-22 (non-dict args give `None` for every tool). Lines 31-32 (only `path` retained for read, grep, glob and write; a missing key becomes `null`; other keys such as `file_path` are discarded). Line 33 (every other name, including exec and edit-class tools, gets `{}`). Line 106 (`complete` ignores all of this). Line 30 states an assumption: "The auditor denies exec/fetch/unknown tools by name."
- Emitted examples: `write` with a JSON-string arguments value gives `args: null` [INFERENCE that such a shape occurs]. `write` with `file_path` instead of `path` gives `{'path': null}`. `grep` without `path` gives `{'path': null}` (default `.`, not a literal bound path). `edit` gives `{}`.
- Expected fixture verdict: `complete: false`, or the path surfaced so the scope check can judge it.
- Observed runtime: not executed.
- Conditionality: this is a bypass only if the auditor accepts `null` paths. The auditor is not readable [INFERENCE]. The line-30 assumption is under test here. A path-scoped write outside the report path cannot be judged once its path is dropped.
- Fix direction: retain the raw argument shape, and mark non-dict or missing-path rows incomplete.

### CX-6 (Medium, noharm): invocations outside the two read sources are invisible; non-`toolCall` blocks count as final text
- Source: lines 65-67 (only `type == 'message'` and `role == 'assistant'`). Line 69 iterates `content` as a list, so a single-object `content` yields keys and no calls. Line 70 (only `type == 'toolCall'`). Line 78 (only `customType == 'tool_execution_start'`). Line 92 (any non-toolCall block makes the final message "final text"). No reading of `tool_execution_end`, results or other entry kinds.
- Input shapes, each [INFERENCE] that the substrate can emit it: an invocation block with another type in a last assistant message whose `stopReason` is `stop`; `content` as one object; an invocation recorded in a non-message entry; a call visible only as an end event.
- Emitted: outcome `completed` and `complete: true`, with no event for the invocation.
- Expected fixture verdict: `complete: false` for any unrecognised invocation-shaped block or unread entry kind.
- Observed runtime: not executed.
- Mitigation not verified: a fresh-id `tool_execution_start` for the same invocation would be recorded (lines 85-87).
- Fix direction: count unrecognised invocation-shaped blocks and fail completeness on any nonzero count.

### CX-7 (High, accounting and ordinal): population is the registry alone; duplicate keys collapse; duplicate ids double-count
- (a) Line 38: `json.loads` has no `object_pairs_hook`. A duplicated member name keeps the last value, so the earlier entry is silently replaced and `seats` drops by one. Precedent in this repo: check-review-snapshots.py line 61 uses `object_pairs_hook=unique_object` (defined lines 33-39), and its selftest case `duplicate-json-key` (lines 204-208) expects CANNOT_EVALUATE (exit 2).
- (b) Line 41 iterates `registry['members']` only. No frozen seat list or digest is checked. Preregister.json carries no seat list (lines 1-15). A registry that omits a declared seat yields a smaller `seats` count with no finding. Seat-boundary md line 31 forbids dropping a denominator.
- (c) Lines 42-43: two members with the same `agentId` share one trace. Both rows are `completed` with identical `transcript_sha256`. No uniqueness check.
- Expected fixture verdict: duplicate member key gives CANNOT_EVALUATE. Population differing from the declared list gives CANNOT_EVALUATE. Duplicate `agentId` gives CANNOT_EVALUATE.
- Observed runtime: not executed.
- Consequence: any ordinal or calibration value computed from these counts inherits the error.
- Fix direction: reuse a unique_object-style hook, compare against a frozen declared population, and reject shared agentIds.

### CX-8 (Medium, freshness and identity): transcript-to-seat binding by filename only
- Source: line 39 indexes by `p.stem`. Line 43 looks up by `agentId`. The loop reads no identity field from inside the transcript.
- Input shape: a transcript copied or renamed to another seat's stem.
- Emitted: that transcript's requests, outcome and `transcript_sha256` are attributed to the other seat.
- Expected fixture verdict: CANNOT_EVALUATE for the seat, or an identity check against the dispatch record.
- Observed runtime: not executed.
- Note: sha256 proves byte identity, not provenance.

### CX-9 (Medium, harm from output): "credentials not copied" is not enforced
- Source: docstring lines 5-6 and comment line 95 state that credentials are never copied. Line 96 gates on substring presence of listed phrases. Line 97 retains up to 1200 characters unless the regex on that line matches `bearer `, `api[_-]?key`, `token=` or `cookie`. Line 32 copies `path` values verbatim. Lines 103-104 copy provider and model strings with no length cap or filter. Lines 113-116 store unsalted digests of the full argument JSON, including command and write bodies.
- Input shapes, described by class only (no secret material in this report): an error string containing one listed phrase plus a provider-key-style token, or a `key=`, `password=` or `secret=` parameter, passes the gate and is copied. A read, grep or glob `path` carrying URL userinfo or a query secret is copied verbatim. A low-entropy command body can be confirmed from its digest by guessing.
- Expected fixture verdict: category-only output or omission for each shape.
- Observed runtime: not executed.
- Fix direction: reduce error text to categories, redact path values by pattern before copying, and key or drop the argument digest.

### CX-10 (Medium, operability and freshness): one malformed record aborts the whole wave; stale outputs remain
- Triggers (only ValueError and UnicodeError are caught, line 60):
  - a JSON line that is not an object (`null`, `[]`, a number, a string) raises AttributeError at line 63;
  - `message` not an object (lines 66-67); `content: null` (line 69, TypeError); `data` not an object (lines 79-80);
  - nested `recipient_name` null or non-string with an object `parameters` (lines 28 to 31, AttributeError). Top-level non-string names are normalised to `unknown` with `complete` false (lines 110-112), so the two paths disagree;
  - a lone surrogate in arguments raises UnicodeEncodeError at line 113 (`.encode()` is outside the try);
  - a member without `agentId` (line 42, KeyError) or with an unhashable one (line 43, TypeError).
- Consequence: the exception fires before lines 122-123. No incomplete row is emitted for the seat, and the earlier `events.json` and `settlement.json` remain. Nothing in those files distinguishes old from new.
- Expected fixture verdict: the bad seat as `complete: false` with outcome `unknown`, and the other seats still emitted. Or prior outputs removed before any write.
- Observed runtime: not executed.
- Fix direction: per-seat try and except that converts errors to incomplete rows, and atomic replacement of both outputs.

### CX-11 (Medium, freshness): outputs are location-derived, unbound and non-atomic
- Source: lines 16-17 derive ROOT from `__file__` via `parents[3]`. At the declared candidate path, ROOT is `.../round-22/candidate`. A run there reads `candidate/.ufo/waves/round-22/<wave>/swarm-registry.json` (or fails at line 38 if absent) and writes `candidate/.../<wave>/events.json` and `settlement.json`. Preregister lines 6-7 read `.ufo/waves/round-22/build/*.json` at the repo root, which such a run does not touch.
- Docstring line 2 says "after a wave settles". No settled-state check exists in code.
- Emitted top-level keys (lines 118-121): `schema`, `seats`, `coverage`. No timestamp, nonce, registry digest, transcript-directory identity or run id.
- Lines 122-123 are two sequential overwrites. A crash between them leaves the pair inconsistent. A rerun silently replaces prior evidence.
- Expected fixture verdict: outputs carry a registry digest, transcript-directory identity and run id. The run refuses when the wave is not settled. Both files are replaced atomically or neither is.
- Observed runtime: not executed.
- Fix direction: take the repo root as an explicit argument, record digests, and write to a temp file then rename.

### CX-12 (Low, accounting display): summary conflates unavailable coverage with zero activity
- Source: lines 124-126. `requests` sums only available events. No could-not-evaluate or unavailable count is printed.
- Shape: all transcripts missing gives `complete: 0`, `requests: 0`, `outcomes.unknown: N`. `requests: 0` reads as zero activity, which seat-boundary md line 30 forbids.
- Expected fixture verdict: an explicit could-not-evaluate count, and no bare request total when coverage is missing.
- Observed runtime: not executed.

### CX-13 (Low, accounting and ordinal semantics)
- (a) Lines 101-102: exit without final gives `failed` with "cause unproven". Seat-boundary JSON line 42 and md line 18 map missing final to UNKNOWN. A cohort mapping `failed` to absent-dead would assert a cause the code says is unproven.
- (b) Lines 88-93 read only the last assistant message. An earlier assistant error followed by success leaves no record, although line 121 says errors are observed outcomes.
- (c) Line 86 stores the start line as `request_line` for start-only calls, so `request_line` means either a request line or a start line. Adjacency or ordering claims cannot rely on it.
- Expected fixture verdict: `unknown` for exit without final. Earlier errors recorded. One field per meaning.
- Observed runtime: not executed.

## Bounded reasons where an axis holds
- Ordinal: collect.py never reads preregister.json, so no ordinal value is computed or emitted. Residual: C2 and C3 metrics are decided by unread checkers, and any count-based metric inherits CX-7.
- Host: no host identity, tool surface or allowlist is read (host JSON line 10 is never consulted). A missing `start_line` (line 115) is not a refusal record, because no refusal event kind is parsed. Residual: a reader may treat a null `start_line` as a host refusal. The code does not claim this.
- Reading: no result or end handling exists (lines 57-87 read only assistant toolCall blocks and tool_execution_start). `path` (line 32) is a request projection. A `read` of a missing bound path yields the same row as a successful read. `complete` means terminal metadata is present, not that all requests executed (docstring lines 7-8, coverage line 107).
- Freshness, as a certificate: no emitted field can establish currency. CX-10 and CX-11 show how stale or redirected output looks current.
- Positive controls present in source: one buffer is both hashed and parsed (lines 50-57), so `transcript_sha256` and events cannot diverge. A missing transcript becomes `unknown` with `complete: false` and no events (lines 45-49). Duplicate and missing request ids set `parsed = false` (lines 72-75, 81-83). A non-string top-level tool name sets `complete: false` (lines 110-112). The wave name is restricted to build or falsify (line 131), and writes go to two fixed files (lines 122-123).

## Not verified
- check-seat-bindings.py (C2) and check-review-cohort.py (C3): the consumers that would catch CX-1 to CX-7. Every mitigation above is conditional on them.
- Transcript format: block types, naming (`functions.` prefix), whether execution starts are logged for nested children, and id semantics. Each CX states its trigger.
- swarm-registry.json, bindings.json, reviews.json and transcripts: not declared, not read.
- collect.py SHA256: not recomputed under NO-EXEC. The declared value is echoed above. Tag 64A3 is the read tool's hashline tag, not a digest.

## Checks for main agent (not run here)
- Negative fixtures for CX-1, CX-3, CX-4 and CX-7 run through the C2 and C3 checkers. Expected CANNOT_EVALUATE or FAIL per entry.
- A duplicate-member-key registry fixture for collect. Expected CANNOT_EVALUATE, mirroring the check-review-snapshots selftest case `duplicate-json-key`.

Reviewed-SHA256: 3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a
Predicate: r22-fxcollectnoharm
Scope: executed=none
