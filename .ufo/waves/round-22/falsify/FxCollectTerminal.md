# FxCollectTerminal — terminal assistant stop/error/session_exit rules in `collect.py`

Seat: scout (source-only, NO-EXEC, NO-FETCH). Target:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/.ufo/waves/round-22/collect.py`
Declared digest `3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a`.
The digest was **not recomputed** in this seat (NO-EXEC forbids shell/hash utilities); the reviewed
bytes are the file at the declared path, whose structure matches the target description. Nothing
was executed, imported, mutated, or run as a fixture.

## Axes (godspeed)

1. **Falsification sharpness** — a counterexample must be a literal record sequence, not a vibe.
2. **Evidence-shapedness** — every claim carries a line anchor and an expected-vs-derived split.
3. **Scope safety** — no exec, no fetch, no production edits, no build-report edits.

## Candidate property under attack

> A trace that is still running, or truncated before its terminal record, is never reported
> `complete: true` / `outcome: "completed"` ("clean").

Define clean = `complete == true AND outcome == "completed"` in `events.json` / `settlement.json`.

## Rules as written (literal reading, no execution)

| Anchor | Rule |
|---|---|
| `collect.py:50` | One `trace.read_bytes()` snapshot; no re-read, size/mtime stability, or quiescence probe. |
| `collect.py:57-62` | Per-line `json.loads`; any `ValueError`/`UnicodeError` sets `parsed = False` (global flag). |
| `collect.py:63-64` | `exit_seen = True` when **any** line has `type == "custom"` and `customType == "session_exit"`. Position in the file is not tracked. |
| `collect.py:65-68` | `last_assistant` is overwritten by every assistant `message`; only the file-final one survives. |
| `collect.py:88-90` | `terminal_error = isinstance(errorMessage, str) and bool(errorMessage) and stopReason == "error"` — a conjunction of two provider-normalized fields. |
| `collect.py:91-93` | `final_text = bool(content) and no content item is a toolCall`; `final = final_text and stopReason in ("stop","end_turn")`. |
| `collect.py:94-102` | Branch order: `terminal_error` → `failed`; else `final` → `completed`; else `exit_seen` → `failed`; else stays `unknown`. |
| `collect.py:106` | `complete = bool(parsed and (exit_seen or final or terminal_error))`. |
| `collect.py:36`, `129-134` | `collect(wave, transcripts)` accepts no liveness/settlement argument; the CLI exposes only `wave` and `transcripts`; no non-zero exit on an all-unknown cohort. |

Two structural consequences follow directly:

- `final` is **self-sufficient** at `:106`: a last assistant message of text + `stopReason:"stop"`
  marks the trace complete with no `session_exit` required. The `session_exit` rule is only a
  fallback for traces that lack such a message.
- `exit_seen` is **position-insensitive**: a `session_exit` anywhere, including one followed by
  more messages and tool starts, forces `complete = true`.

## Counterexamples (literal fixtures)

Fixtures are JSONL records, one object per line. They were **not** executed; the verdicts below are
obtained by literal evaluation of `collect.py:63-106`.

**F1 — live seat idle after a text-only stop message (no close marker).**

    {"type":"message","message":{"role":"assistant","content":[{"type":"text","text":"Which axis first?"}],"stopReason":"stop","provider":"p","model":"m"}}

A live seat waiting for steering has exactly this as its last record. `parsed` stays true
(no duplicate/non-string tool-call id is involved), `exit_seen` false, `terminal_error` false,
`content` non-empty with no `toolCall`, `stopReason == "stop"` → `final = true` → `:100`
`outcome = completed`, `:106` `complete = true`.
**Expected: not clean (running). Derived: clean.**

**F2 — truncation at the ordinary append boundary (final assistant message present, close record not yet written).**

    {"type":"message","message":{"role":"assistant","content":[{"type":"text","text":"Done; findings filed."}],"stopReason":"stop"}}
    {"type":"custom","customType":"session_exit","data":{}}

- Full two-line trace: `final` true → completed, `complete` true.
- Strict prefix = line 1 only: identical classification (completed, complete true), because
  `session_exit` was never load-bearing for this shape.

Deleting the only session-close evidence does not change the verdict, so the property fails for
every strict prefix that ends on a text-only stop message. A writer that flushes after each record
produces exactly such prefixes between records.

**F3 — `session_exit` followed by continued activity (records after the marker).**

    {"type":"message","message":{"role":"assistant","content":[{"type":"text","text":"panel A done"}],"stopReason":"stop"}}
    {"type":"custom","customType":"session_exit","data":{}}
    {"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"t1","name":"read","arguments":{"path":"x"}}],"stopReason":"toolUse"}}
    {"type":"custom","customType":"tool_execution_start","data":{"toolCallId":"t1","toolName":"read","args":{"path":"x"}}}

At read time the tool has started and produced no result line: the seat is mid-operation.
`last_assistant` is the `toolUse` message → `final` false; `exit_seen` true → `:102`
`outcome = failed` ("session_exit without successful final assistant text"), `:106` `complete = true`.
**Expected: not clean (running, and the exit marker is not terminal). Derived: complete, with a
stale failure attribution derived from a marker that precedes the live work.**

## Where the property does hold

| Fixture | Shape | Derived verdict |
|---|---|---|
| F4 | Truncated **inside** a JSON line (`{"type":"message","mess` …) | `json.loads` raises → `parsed = False` (`:61`) → `complete = false`, `outcome = unknown`. Holds. |
| F5 | Assistant `toolUse` message + `tool_execution_start`, no result, no exit marker | `final` false, `exit_seen` false, `terminal_error` false → `complete = false`, `outcome = unknown` (`:45`). Holds. |
| F6 | Last assistant message with `stopReason` `"length"`, `"toolUse"`, or absent | `final` false → clean only if an exit marker exists. Holds for output truncation. |
| F7 | Last assistant message with empty or `null` content | `bool(content)` false → `final` false. Holds. |
| F8 | Last message has a `toolCall` plus text | `final_text` false → `final` false. Holds. |
| F9 | Registered agent id absent from the transcript directory | `:46-49` `complete = false`, `outcome = unknown`, `coverage = "registered transcript unavailable"`. Holds and fails closed. |

**Bounded reason it holds elsewhere:** completeness requires a terminal *shape* (text-only stop,
or an error conjunction, or an exit record), and mid-line corruption forces the global
`parsed = False`. Those three gates structurally exclude the mid-line and mid-tool cases. The
property fails only at the seam where a text-only stop message is treated as terminal on its own,
and where the exit marker is trusted regardless of position.

## Error-rule gap (same rule family)

`terminal_error` (`:90`) requires **both** a non-empty `errorMessage` and `stopReason == "error"`.
Two source-visible consequences:

- `stopReason:"error"` with an empty/absent `errorMessage` → no terminal error; with no exit
  marker the seat is `unknown` and `complete = false`. Conservative, but the observed error is lost.
- A message carrying `errorMessage` but `stopReason` `"stop"`/`"end_turn"` with text content →
  classified `completed` (`:99-100`), while the coverage string at `:121` still claims
  "errors are observed outcomes". A provider that records the error only in `errorMessage`
  therefore produces a false `completed`.

This does not need an extra fixture beyond the branch text; it is a direct reading of the conjunction.

## Expected vs observed (kept separate)

- **Expected fixture verdicts**: F1, F2-prefix, F3 must be not-clean; F4–F9 as tabulated.
- **Derived (source) verdicts**: as above, by literal branch evaluation.
- **Observed runtime**: **none.** No `events.json`, `settlement.json`, transcript, or CLI run was
  produced or inspected in this seat. No claim here rests on a runtime observation, and no
  runtime result was rerun to confirm anything.
- **Implication for round 22**: `settlement.json` is the C3 cohort input, so a live or
  line-boundary-truncated seat can enter the cohort as delivered-conformant rather than
  absent-unresolved. This is a detection/evidence defect only; it is not, and must not be
  described as, preventive runtime enforcement.

## Adjacent observations (outside the assigned verdict, no weight)

- `collect.py:66,79` use `obj.get('message', {})` / `obj.get('data', {})` and then call `.get` on
  the result, and `:69` iterates `message.get('content', [])`. A line whose top-level JSON is not
  an object (`[]`, `"x"`, `null`), or with `"message": null`, raises `AttributeError`/`TypeError`
  and aborts the whole `collect` before either output file is written. Fail-closed, but
  cohort-wide rather than per-seat, and outside the `:46-49` "unavailable" path.
- `collect.py:97` retains `error[:1200]` when a known token is present and
  `(?i)(bearer |api[_-]?key|token=|cookie)` does not match. `password=`, `secret=`, and
  `Authorization: Basic` are not matched, so a "known category" error containing them is copied
  verbatim, against the `:95` comment "Credential material is never copied." Reported here only
  as an observation; it does not change the terminal-rule verdict.

## Remaining unknowns (unresolved, not asserted)

1. Whether omp writes exactly one `session_exit`, strictly at EOF. If it does, F3 is a
   resumed/continued-session artifact; if it can precede further records, F3 is direct.
2. Whether a live seat can emit a text-only assistant message with `stopReason:"stop"` and remain
   live while awaiting steering. This is the entire weight of F1/F2; the declared read paths
   contain no transcript-schema document, so this is `[INFERENCE]` from the code's own exit-fallback
   design, not an observed record.
3. Whether a trailing partial write can be valid JSON; if not, mid-line truncation is always
   caught, which is what makes F2 the only truncation window.
4. Digest identity: not recomputed (NO-EXEC).

## Verdict

**Falsified** for the assigned property at the final-assistant / exit-marker seam (F1, F2-prefix,
F3); **holds** for mid-line truncation, mid-tool traces, output-length truncation, tool-call-final
messages, and absent transcripts. The defect is confined to `collect.py:93` (self-sufficient
`final`), `:63-64` (position-blind `exit_seen`), and `:106` (disjunction), and it is a
post-hoc classification defect, never runtime enforcement.

Reviewed-SHA256: 3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a
Predicate: r22-fxcollectterminal
Scope: executed=none
