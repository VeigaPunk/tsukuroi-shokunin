# FxCollectCallJoin — request/start join, duplicate and reordered records

Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/.ufo/waves/round-22/collect.py` (134 lines).
Assignment digest: `3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a`; baseline `894d1e20fb4939b0cc4fadf722c46d1429f257d2`.
Method: source-only. The digest is the assignment's; re-hashing the file would need execution, so "bytes at that path equal that digest" is unverified here [INFERENCE]. No fixture was run; every verdict below is derived by reading the control flow.

Claim attacked: *"Assistant request IDs joined starts correctly, duplicate/reordered wrapper records not lost."*

## What the source does

- `projection` (lines 21–33) treats `multi_tool_use.parallel` / `parallel` by exact name (line 23), projects each `child.parameters` recursively (lines 27–29), returns `{'tool_uses': None}` for a non-list `tool_uses` (lines 24–26), and normalizes the `functions.` prefix only for leaf tools (line 31). Any other name returns `{}` (line 33).
- `collect` keeps `calls` (id → `(line, name, args)` from the assistant `toolCall` block, lines 72–77), `starts` (id → last `tool_execution_start` line, line 84) and `order` (first-seen insertion order, lines 77/87).
- Duplicate or non-string assistant call ids set `parsed = False` (lines 73–75). A start record whose id has no call yet manufactures the call from `data.toolName`/`data.args` (lines 85–87).
- `complete = parsed and (exit_seen or final or terminal_error)` (line 106); event fields are built at lines 108–116 with `request_line` from the stored tuple, `start_line = starts.get(ident)` (line 115) and a digest over the stored args (line 113).
- The docstring already disclaims recorder completeness (lines 7–8) and the artifacts repeat it (lines 119, 121), so the schema does not claim *every real operation*. The claim under attack is narrower: within an available trace, are request ids joined to the right start and are duplicate/reordered records preserved?

## Falsifying fixtures (expected verdicts only — not executed)

| ID | Fixture (transcript lines) | Source path | Expected source-derived verdict | Effect on the claim |
|---|---|---|---|---|
| F1 | assistant `toolCall` id `c1` (line 2); `tool_execution_start` id `c1` at line 3 and again at line 5; final assistant text line 6 | line 84 overwrites `starts[c1]`; lines 73/106 untouched | one event, `request_line=2`, `start_line=5`, `complete=True`; the line-3 start is absent from `events.json`; no duplicate field, no finding | **falsifies duplicate preservation, silently.** A retried/re-emitted start is collapsed and the trace still reports complete. Duplicate *requests* are flagged; duplicate *starts* are not. |
| F2 | `tool_execution_start` id `c1` line 2 (with name/args); assistant `toolCall` id `c1` with different `arguments` line 3; final text line 4 | lines 85–87 create the call from the start; lines 73–75 then drop the assistant record as a "duplicate" | event `c1` has `request_line=2`, `start_line=2`, name/args from `data.toolName`/`data.args`, and `request_arguments_sha256` hashed over those start args (line 113); `complete=False`; the real request line 3 never appears | **falsifies correct id joining under reordering.** Attribution is first-arrival-wins, not identity-attributed; `request_line` can name a start line, and the "request_arguments" digest can hash execution-start args. The row is flagged, so the loss is not silent, but the per-event provenance is. |
| F3 | assistant `toolCall` name `functions.multi_tool_use.parallel`, args `{"tool_uses":[{"recipient_name":"functions.bash","parameters":{"command":"true"}}]}`, then final text | line 23 matches only the bare name; line 31 normalizes `functions.` only for leaves; line 33 returns `{}` | event with the recorded tool name, `args={}`, `complete=True`; the nested `bash` child and its parameters are absent | **falsifies wrapper-record preservation, silently.** The file itself anticipates `functions.`-qualified names at line 31, so the same trace namespace is handled for leaves and dropped for wrappers — the exact shape that can hide a nested exec/fetch request. |
| F4 | assistant `toolCall` name `multi_tool_use.parallel`, args `{"tool_uses":[{"parameters":{}}]}` (child has dict parameters, no recipient_name) | line 28 recurses with `None`; line 31 evaluates `None.removeprefix`; no `isinstance` guard in the recursion, unlike lines 110–112 | uncaught `AttributeError` inside `collect`; the run ends before lines 122–123, so **no `events.json` and no `settlement.json` for any seat in the wave** | **falsifies "not lost" in the strongest form:** one malformed wrapper child destroys every seat's evidence, and no could-not-evaluate marker is written. |
| F5 | two assistant messages reusing id `c1` with different `arguments` | lines 73–76 | first occurrence kept, second dropped, `parsed=False`, `complete=False`; no line list for the duplicate | duplicate *request* records are lost, but at least flagged. Conversely a duplicated whole message line (resume/replay artifact) turns an otherwise clean seat incomplete — over-flagging, the reverse error. |
| F6 | wrapper args `{"tool_uses":{"recipient_name":"functions.bash","parameters":{}}}` (dict, not list) | lines 24–26 | `args={'tool_uses': None}`, `complete` unchanged (True if terminal metadata is present) | malformed arguments are represented as null but not classified: `seat-boundary-r22.json` (`UNKNOWN`: malformed arguments fail closed; "incomplete metadata is not command absence") and `.md` § What is enforced ("fails closed on … malformed data") expect a denial/schema verdict, not a complete row. |
| F7 | one legal JSON string containing U+2028 inside an otherwise unparseable-free transcript | line 57 uses `str.splitlines()` (splits on U+2028/U+2029, `\v`, `\f`, `\x1c`–`\x1e`), while `check-review-snapshots.py` line 44 splits LF-only | the record is split, both halves fail `json.loads`, `parsed=False`, and every later `request_line` shifts by one relative to the review tool's physical-line convention | line numbers are not comparable across the wave's two readers; a single legal character degrades a trace to incomplete. Flagged, not silent. |

## Bounded reason the claim holds on the happy path

For traces with (a) one `tool_execution_start` per id, (b) the assistant `toolCall` recorded before that start, (c) unique ids, (d) a bare or leaf-qualified tool name and (e) LF-only line separators, the join is exact: `request_line` is the assistant line, `start_line` is the start line, and order is request order. Unparseable lines, missing transcripts, non-string ids and duplicate request ids all force `complete=False` (lines 47–48, 61, 73–75, 81–83, 106), and start-only calls are retained rather than dropped (lines 85–87). The failures above are outside that envelope, and F1/F3/F6 remain `complete=True` — so they are the silent set a consumer of `events.json` cannot see.

## Inferences (labeled)

- The `functions.` normalization at line 31 is evidence that qualified names occur in recorded traces [INFERENCE]; whether a wrapper is ever recorded qualified is unverified (no transcript is readable in this seat).
- Whether any consumer reads `start_line`/`request_line` (the C2 auditor is outside this seat's read set) is unknown; if it does, F2's reordered attribution and F1's last-wins start line propagate.
- The wave's coverage text (lines 119, 121) is honest about recorder completeness but does not disclose these intra-trace losses, so a green `complete` count can coexist with F1/F3/F6.

## Remaining unknowns

1. Whether the substrate ever emits two `tool_execution_start` records for one id (retry/resume) — unobservable without transcripts and without execution.
2. Whether wrapper names are recorded with the `functions.` prefix.
3. Whether starts ever precede their request record in a settled transcript (the line-85 fallback implies the author expected start-only records, not necessarily ordering).
4. Whether the C2/C3 consumers treat any per-event provenance field as authoritative.
5. Whether a malformed wrapper child has occurred; F4 predicts a whole-wave abort, not a per-seat finding.

## Seat-scope note (self-disclosure)

One `grep` was issued against the candidate directory rather than the literal declared file list. It returned lines from an undeclared file (`candidate/tools/check-seat-bindings.py`). No finding above cites or depends on that file and its content was not used as evidence; all citations are to the declared paths. Disclosed for this wave's own post-hoc request audit. No command was executed and no fetch was made.

Reviewed-SHA256: 3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a
Predicate: r22-fxcollectcalljoin
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
