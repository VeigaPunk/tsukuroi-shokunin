# FxCollectParse: round-22 source-only falsification of collect.py

Target: `.ufo/waves/round-22/candidate/.ufo/waves/round-22/collect.py` (134 lines, read in full).
Assigned digest pin: `3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a`. Not recomputed, because no execution is permitted. The `#64A3` shown by the read tool is a snapshot tag, not a digest. No declared source records a digest of this file.
Attack: BadJSON, UTF-8 and missing transcript mark incomplete; no silent lost event.
Execution: none. No tests, imports, compiles, mutated inputs, fetches, subagents, installs or updates.
Declared reads used: collect.py; preregister.json; sources/host-tool-boundary.json; skill://godspeed; tools/check-review-snapshots.py (read L3-128, plus grep); corpus/knowledge/seat-boundary-r22.json and .md. tools/_revision.py was read as an outline only and is not relied on.

## Result

Counterexamples found. Seat-level marking holds for one narrow class: invalid JSON or invalid UTF-8 that raises ValueError or UnicodeError, absent transcripts, and non-string ids and tool names. The "no silent lost event" half does not hold. Settlement ignores parse state (F1). Conflicting duplicate execution-starts are dropped silently (F2). Several malformed inputs are normalized without a mark (F3 to F6, F9). Several others abort the whole run instead of marking the seat (F7).

## Axes

- A1 seat marking: `complete` (L44, L106).
- A2 settlement consistency: `outcome` (L45, L92-105) against `complete`.
- A3 event loss: requests dropped or normalized without a mark.
- A4 failure mode: mark-and-continue against uncaught abort.
- A5 decoding: bytes JSON and UTF-8 acceptance (L57-62, L113).
- A6 population: registry and transcript reconciliation (L38-43).

## Findings

Severity: P1 silent breach of the contract in the C2/C3 inputs. P2 material, conditional, or loud. P3 hygiene or adjacent.

### F1 (P1, A2): settlement ignores parse state

- `parsed` is cleared at L61, L74 and L82. It feeds only `complete` (L106). `outcome` is set at L92-102 from `last_assistant`, `final` and `exit_seen`, with no reference to `parsed`.
- The settlement entry (L45, L103-105, L117, L120-121) has no completeness field. Its vocabulary is completed, failed and unknown. The checklist requirement "Mark incomplete trace coverage could-not-evaluate" (seat-boundary-r22.md L30) has no representation here. The sibling maps read and decode failures to CANNOT_EVALUATE (check-review-snapshots.py L85-97, L101-105, L121-125).
- F1a: final stop line corrupted, then session_exit. Result: `failed`, "cause unproven" (L101-102). A false fault. preregister.json C3 consumes settlement.json (line 7), so this reaches cohort accounting [INFERENCE: the cohort checker is not declared].
- F1b: terminal-error line corrupted after an earlier text-only stop message, then session_exit. Result: `completed` (L92-93, L99-100). A false success.
- F1c: a corrupted non-request line after an otherwise complete run. Result: complete=false in events, `completed` in settlement.
- Expected fixture verdict: each case settles as could-not-evaluate with complete=false. Never completed or failed.
- Source prediction: complete=false holds. Outcome fails in all three.
- Observed runtime: none.
- Fix direction: derive outcome only from parsed input; add could-not-evaluate; carry `complete` into settlement.

### F2 (P1, A3): conflicting duplicate tool_execution_start dropped silently

- L84 overwrites `starts[ident]`. L85 skips `calls` when the id already exists. Nothing sets `parsed=False`.
- Asymmetric with L73-74, which marks a duplicate assistant toolCall id. Start-then-assistant duplicates are marked (L86, then L73). Assistant-then-start duplicates are silent (L76, then L85).
- Expected fixture verdict: complete=false when a second start for an id disagrees with the recorded name or args.
- Source prediction: complete=true. The first recorded tool and args stand, and start_line is the last start.
- Observed runtime: none.
- Why it matters: a conflicting duplicate is the one place where the recorded evidence contradicts itself, and the contradiction is discarded unmarked.

### F3 (P2, A3): unrecognized request-bearing shapes skipped silently

- Only `type=='message'` with `role=='assistant'` and content `type=='toolCall'` (L65-70), and `customType=='tool_execution_start'` (L78), are read. There is no else branch. Assistant content that is not a list of dicts, such as a string, is iterated per character and yields nothing (L69-71).
- Expected: unrecognized request-bearing records are counted or mark the seat.
- Source prediction: silent. Whether the recorder ever emits other shapes is not verifiable, because the recorder schema is not declared [INFERENCE].

### F4 (P2, A3): malformed arguments normalized to None or {} without a mark

- Non-dict args return None (L21-22). A non-dict parallel child becomes None (L27-29). A read, grep, glob or write whose args lack `path` records `{'path': None}` (L31-32). complete is not touched (L106). An empty-string tool name passes L110.
- Declared contract: seat-boundary-r22.json UNKNOWN is DENY with reason "Fail closed; incomplete metadata is not command absence" (lines 32-38). seat-boundary-r22.md L22 says the auditor fails closed on malformed data.
- Projection erases the malformation before any auditor sees it. Material for binding tools only. The target's own comment (L30) says the auditor denies exec, fetch and unknown tools by name [INFERENCE: auditor not declared].
- Expected fixture verdict: complete=false. Source prediction: complete=true, path None.

### F5 (P2, A1/A3): lost lines not counted; dead and unparseable seats look identical

- L57-62 `continue` drops the line with no line number, count or offset.
- L107 writes "available recorded requests" whether or not parsed is true.
- A seat with an unparseable line and no terminal metadata, and a DEAD seat, both get complete=false, generic coverage (L107) and outcome unknown with error '' (L45; no branch sets it).
- preregister.json C3_bound (line 9) requires absent-dead and absent-unresolved to be accounted separately. Neither artifact distinguishes them.
- Expected fixture verdict: a per-seat unparsed-line count or cause, and coverage that does not claim availability when parsed is false. Source prediction: neither.

### F6 (P2, A3; conditional on recorder naming): parallel wrapper prefix not normalized

- L23 matches the exact names `multi_tool_use.parallel` and `parallel`. L31 strips `functions.` for leaf names. A wrapper named `functions.multi_tool_use.parallel` falls through to L33, records args {} and keeps complete=true. Its children are never enumerated.
- Whether the recorder uses that name cannot be verified, because no transcript fixture is declared [INFERENCE].

### F7 (P2, A4): loud aborts where the contract requires a per-seat mark

Uncaught exceptions end collect() before L122-123, so the run writes neither events.json nor settlement.json. An earlier pair in the same directory, if present, remains and could be read by a consumer that ignores the exit status [INFERENCE on file presence]. Triggers:

- JSON-valid non-object line (`null`, `[]`, a number, a string): `obj.get` at L63 raises AttributeError. The except at L60 catches only ValueError and UnicodeError.
- `message` not a dict on a `message` line: L67 raises.
- `message.content` null or a number: L69 raises TypeError.
- `data` not a dict on a tool_execution_start line: L80 raises.
- Parallel child with a non-str recipient_name and dict parameters: L31 calls removeprefix on None or a non-str.
- Registered transcript present but unreadable, a directory named `<id>.jsonl`, or a dangling symlink: L50 is unguarded. Listing a dangling symlink through glob at L39 is [INFERENCE]. The sibling converts this case to REVIEW-READ-FAILED with code 2 (check-review-snapshots.py L85-97).
- Deeply nested JSON: RecursionError at L59 is not caught [INFERENCE].
- Lone surrogate in tool arguments: L113 `.encode()` is strict and sits outside the try (L58-62). See F8.
- Expected fixture verdict: per-seat complete=false, run continues. Source prediction: abort.

### F8 (P2, A5): surrogate-encoded bytes accepted unmarked; other invalid UTF-8 holds

- L59 calls json.loads on bytes. CPython decodes bytes input with the 'surrogatepass' error handler [INFERENCE: stdlib not declared and not read]. Bytes ED A0 80 through ED BF BF (CESU-style surrogates, invalid UTF-8) and JSON `\uD800`-`\uDFFF` escapes raise no error, so parsed stays true.
- Other invalid UTF-8 raises UnicodeDecodeError and is marked (holds).
- The sibling decodes reports strictly with UnicodeError, mapped to CANNOT_EVALUATE (check-review-snapshots.py L102-105), and rejects category Cs in identity strings (L21-23). Same wave, two decoders, different acceptance.
- Expected fixture verdict: complete=false for ED A0 80 in any line. Source prediction: complete=true when only text fields carry it; abort at L113 when it lands in arguments (F7).

### F9 (P2, A6; registry not declared): duplicate keys in the registry silently replace entries

- L38 `json.loads(...)` has no object_pairs_hook. The sibling uses `object_pairs_hook=unique_object` (check-review-snapshots.py L61). unique_object raises on duplicate keys (L33-39), which is mapped to CANNOT_EVALUATE (L122-124).
- Under last-wins semantics [INFERENCE], a duplicated member name silently replaces the earlier entry, and the replaced agentId is never checked. A duplicated `members` key replaces the whole population.
- Expected fixture verdict: fail closed. Source prediction: silent replacement. The registry is not declared, so whether a duplicate exists is unverified.

### F10 (P3, A6; conditional): unregistered transcripts and duplicate agentIds

- L39 indexes every `*.jsonl`. L41-43 consult only registry members. Extra transcripts are never counted or reported.
- Two members sharing one agentId produce two rows over one trace, with no uniqueness check. The requests are counted twice (L124-125).

### F11 (P3, A5): line numbering splits on bare CR

- L57 uses bytes.splitlines, which breaks on CR as well as LF. The sibling splits only at LF (check-review-snapshots.py L42-44, used at L107). request_line and start_line can disagree with LF-based references. This affects only transcripts with bare CR, which are invalid JSONL.

### F12 (P3): outputs are non-atomic; registry read is locale-dependent

- L122-123 write two files separately, with no temp file and rename. A failure between them leaves a mismatched pair.
- L38 read_text() has no encoding argument, so its decoding is locale-dependent [INFERENCE].

### F13 (P3, verification gap): no in-tree negative fixtures

- collect.py has no selftest or fixture. The sibling has one (check-review-snapshots.py L145-241), and so does _revision.py (L195-432). seat-boundary-r22.md QUALITY (line 35) requires fixed negative fixtures before a new check counts. No fixture is referenced or declared in the read set. The verdicts in the table below are therefore source-derived.

### F14 (P3, adjacent, outside the attack): privacy and credential claims

- L113 and L116 retain a digest of the canonical args for every call, including bash command bodies. The docstring (L5-6) says bodies are not copied. Low-entropy bodies are guessable from the digest [INFERENCE].
- L32 copies the path value whatever its JSON type. "Arbitrary tool payloads are not copied" holds only for string paths.
- L95-97 use a denylist (bearer, api key, token=, cookie), applied only when a known token matches. A provider error that matches a known token and carries another secret format is copied, up to 1200 characters.

## Holds, with bounded reasons

- H1: ValueError or UnicodeError on a line sets parsed=false (L59-62) and therefore complete=false (L106). Holds for the events flag only (F1, F5).
- H2: a registered agentId absent from the directory listing gives complete=false, coverage 'registered transcript unavailable' and outcome unknown (L43-49). Holds.
- H3: duplicate assistant toolCall ids (L73-75), non-string ids (L73, L81-83) and non-string tool names (L110-112) mark the seat. Holds.
- H4: no terminal metadata gives complete=false and outcome unknown, matching DEAD to UNKNOWN (seat-boundary-r22.json lines 39-45). Holds for the flag; F5 applies.
- H5: transcript_sha256 is computed from the same bytes that are parsed (L50-51, L105), so input and digest cannot diverge within a run. Holds.
- H6: the summary prints complete alongside seats (L124-126), so a run-level shortfall is visible. Holds at run level only.
- H7: a UTF-8 BOM at a line start is accepted. Benign: RFC 8259 section 8.1 allows parsers to ignore it [INFERENCE from memory; not fetched].
- H8: blank lines mark the seat incomplete, because empty bytes fail at L59. Over-marks, which is conservative.

## Expected fixture verdicts against source-derived predictions

Nothing was run. Observed runtime is none for every row. Predictions are readings of the source. Status PASS means the reading satisfies the contract. FAIL means the reading contradicts it.

| ID | Hypothetical input (described, not created) | Expected fixture verdict (contract) | Source-derived prediction (not run) | Observed runtime | Status |
|---|---|---|---|---|---|
| T1 | 0xFF byte in one line of a transcript with a final stop | events complete=false; outcome not completed | events complete=false (PASS); outcome completed (L98-100 ignore parsed) | none | FAIL (settlement) |
| T2 | final stop line corrupted; session_exit present | complete=false; could-not-evaluate | complete=false; outcome failed (L101-102) | none | FAIL (settlement) |
| T3 | terminal-error line corrupted after an earlier text-only stop; session_exit present | complete=false; could-not-evaluate | complete=false; outcome completed (L92-93, L99-100) | none | FAIL (settlement) |
| T4 | assistant toolCall X, then tool_execution_start X with a different toolName | complete=false | complete=true; first tool kept; start_line overwritten (L84-86) | none | FAIL (silent) |
| T5 | tool_execution_start X, then assistant toolCall X | complete=false | complete=false (L73-75) | none | PASS |
| T6 | JSON line `null` mid-transcript | complete=false; run continues | AttributeError at L63; no outputs | none | FAIL (loud) |
| T7 | read toolCall arguments containing JSON escape `\ud800` | complete=false; run continues | UnicodeEncodeError at L113; no outputs | none | FAIL (loud) |
| T8 | assistant text containing bytes ED A0 80; otherwise complete | complete=false | parsed stays true; complete=true [INFERENCE] | none | FAIL (silent) |
| T9 | read toolCall whose arguments omit path | complete=false (UNKNOWN fail-closed) | {'path': None}; complete=true (L31-32, L106) | none | FAIL (silent) |
| T10 | parallel wrapper named functions.multi_tool_use.parallel with a bash child | child enumerated or complete=false | args {}; complete=true (L23 miss, L33) | none | FAIL (silent, naming-conditional) |
| T11 | registered agentId backed by a dangling symlink | complete=false | listed at L39 [INFERENCE]; read_bytes raises at L50; abort | none | FAIL (loud) |
| T12 | registered agentId absent from the directory | complete=false; outcome unknown | L43-49 | none | PASS |
| T13 | registry member name duplicated | fail closed | earlier entry silently replaced at L38 [INFERENCE] | none | FAIL (silent) |
| T14 | request-bearing record of an unrecognized type | counted or complete=false | ignored; no else branch (L63-87) | none | FAIL (silent) |

## Residual risk and verification gaps

- Not declared and not read: swarm-registry.json, the transcript directory, the recorder schema, check-seat-bindings.py, check-review-cohort.py, and the stdlib json, pathlib and hashlib modules. Each claim that depends on them is marked [INFERENCE].
- The digest pin was not recomputed. No declared source records collect.py's digest.
- No runtime was observed. Every prediction is a reading of the source.
- F14 is outside the attack and was not pursued further.
- Tooling: no installs or updates were performed.

Reviewed-SHA256: 3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a
Predicate: r22-fxcollectparse
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
