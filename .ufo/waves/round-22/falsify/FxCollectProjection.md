# FxCollectProjection — source-only falsification of round-22 `collect.py`

Reviewed-SHA256: 3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a
Predicate: r22-fxcollectprojection
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.

Digest note: the digest above is the one assigned for the target. I read the bytes but did not hash them, because NO-EXEC was in force.

Target: `.ufo/waves/round-22/candidate/.ufo/waves/round-22/collect.py`, `projection()` (lines 20–33) and the event loop that calls it (lines 108–116).

Attack claim: the projection keeps the paths the audit needs and the children of wrapper calls, but leaves out secrets, code and query bodies.

## Verdict

**The claim is falsified.** Reading the source shows four concrete counterexamples:

- The projection drops audit-relevant paths: every `edit` path, plus the path scope that grep and glob use.
- It copies arbitrary non-string payloads, and URL query secrets, through the `path` key.
- It crashes on a malformed child of a wrapper call.
- It crashes on a lone-surrogate argument.

Everything I expect below is a fixture verdict derived from the source. I observed nothing at runtime, because nothing was executed.

Axes affected: operability (C2 request audit fidelity), calibration (evidence provenance), and the docstring's own claim that "path/tool arguments are retained … arbitrary tool payloads are not copied".

## Counterexamples

### CX1 — `edit` path is dropped (HIGH: audit-relevant path lost)

Line 31 keeps `path` only for `read`, `grep`, `glob` and `write`. All other tools get `{}`.

- **Input:** event `{"name":"edit","arguments":{"path":"tools/check-seat-bindings.py","edits":[...]}}`.
- **Expected projection:** `{}`.

The contract allows executor drafts in named separate worktrees, and `edit` is the main file-mutation tool. With the path gone, the auditor cannot tell an in-worktree draft edit from a production edit. It is left with two bad options:
- Deny every `edit` by name. Every legitimate executor edit becomes a false positive.
- Allow `edit` by name. Production edits become invisible.

Either way the evidence of which file was changed is gone. The docstring's "Path/tool arguments are retained" is false for `edit`.

The same evidence loss applies to `xd://ast_edit` and `xd://debug`. Those write calls keep only `xd://…` as the path, and the target files sit in `content`, which is dropped. Those calls still fail closed on a path mismatch, so the impact is lost evidence rather than a missed detection.

### CX2 — Non-string `path` copies an arbitrary payload (HIGH: secrets/code copied)

Line 32 returns `{'path': args.get('path')}` without checking the type.

- **Input:** `write {"path": {"body": "<code or credential>"}, "content": "x"}` (malformed, but a plain JSON object).
- **Expected projection:** `{"path": {"body": "<code or credential>"}}`.

This copies the payload verbatim into `events.json`. It directly contradicts "arbitrary tool payloads are not copied". A list or a very large string under `path` is copied the same way.

### CX3 — URL query and userinfo are kept inside `path` (MEDIUM: query/secret retained)

- **Input:** `read {"path": "https://user:pw@host/x?api_key=SECRET#frag"}`.
- **Expected projection:** the full string, credentials included.

NO_FETCH detection only needs to know that the path is a URL (scheme, host and path). It does not need the query, the fragment or the userinfo. This is a tradeoff rather than an outright bug, since audit fidelity favors keeping the path. It still falsifies "queries … credentials … are not copied".

### CX4 — grep/glob path scope is lost (MEDIUM, [INFERENCE] on the host schema)

For grep and glob, the projection keeps `path` and drops every other field. I did not read the host's tool schemas, because they were not among my declared paths. If glob takes a `pattern` that can be absolute, or grep takes a `glob` filter, consider:

- **Input:** `glob {"pattern": "/home/vgpnk/.ssh/*"}`.
- **Expected projection:** `{"path": null}`.

The real file-system reach of the request disappears. Detection then depends entirely on `check-seat-bindings.py` treating a `null` path as an UNKNOWN deny. That file was not readable in this seat, so I could not verify it.

A glob pattern is a path selector, not a query body. It belongs in the audit-relevant set.

### CX5 — A non-string child `recipient_name` crashes the collector (MEDIUM: wrapper descendants)

At line 28, `projection(child.get('recipient_name'), …)` is called. When the parameters are a dict, the code reaches `tool.removeprefix` at line 31.

- **Input:** `multi_tool_use.parallel {"tool_uses":[{"recipient_name":null,"parameters":{}}]}`.
- **Expected result:** `AttributeError: 'NoneType' object has no attribute 'removeprefix'`. The exception is uncaught, so `collect()` aborts before lines 122–123.

The top-level guard at line 110 (`tool = 'unknown'`) never reaches children.

Consequence ([INFERENCE]): no fresh `events.json` or `settlement.json` is written. If a prior run's files exist in the working tree or at the committed revision, the C2/C3 checkers grade stale evidence. That is not fail-closed.

Related: arbitrarily deep nesting of `parallel` raises `RecursionError` the same way.

### CX6 — Wrapper names are matched before prefix normalization (LOW)

Line 23 matches only `multi_tool_use.parallel` and `parallel`. A `functions.parallel` wrapper misses that check. Line 31 then strips its prefix to `parallel`, which is not a path tool, so the result is `{}`. All descendants vanish, including any forbidden children.

The auditor should still deny it by name, but the descendant evidence the claim promises is lost.

### CX7 — Lone surrogate in arguments crashes the hash (MEDIUM: whole-wave abort)

`json.loads` accepts `"\ud800"`. Line 113 then calls `json.dumps(..., ensure_ascii=False).encode()`, and strict UTF-8 encoding raises `UnicodeEncodeError`. That is uncaught, so the stale-output consequence from CX5 applies.

Adjacent crash paths, outside the projection but on the same event path: a JSONL line whose JSON value is not an object, a non-dict `message` or `data`, or a non-list `content`. Each raises `AttributeError` instead of setting `parsed = False`. This contradicts the UNKNOWN decision, which says malformed arguments should fail closed.

### Note — full-argument SHA-256 (tradeoff, not a defect)

`request_arguments_sha256` hashes the full arguments, including command and content bodies. For low-entropy bodies, such as a short command, it works as a confirm-a-guess oracle. Keep it for identity, but label it a correlation digest, not a redaction.

### Note — settlement error filter (outside the projection, same claim)

At line 97, an error that contains a known token and a secret not matched by `bearer |api[_-]?key|token=|cookie` is kept, up to 1200 characters. Examples are `sk-…`, `password=` or `Authorization: Basic`.

## What holds (bounded)

- Bodies are dropped for every non-path tool: bash, eval, task and web_search all project to `{}`.
- `write` content is dropped.
- String paths for the four path tools are kept verbatim, including the `skill://`, `xd://`, `agent://` and URL schemes NO_FETCH needs.
- Recursion into well-formed `multi_tool_use.parallel` children works, and children reuse the same body-dropping rule.
- The tool name in each event is the raw recorded name, so name-based denial still sees it.
- A non-dict `args` projects to `None`, and a non-list `tool_uses` projects to `{'tool_uses': None}`. Both are distinguishable from `{}`, but only if the auditor treats them as malformed, which I did not verify.

## Smallest safe correction

1. Normalize the name first:
   ```python
   name = tool.removeprefix('functions.') if isinstance(tool, str) else None
   ```
   If `name` is `None`, return `{'malformed': 'tool'}`. Match the wrappers on the normalized name (`'parallel'`, `'multi_tool_use.parallel'`). This fixes CX5 and CX6.
2. Use the path tools `('read', 'grep', 'glob', 'write', 'edit')`. For each, project the string path fields `path`, plus `glob`/`pattern` for glob and `glob` for grep. For any non-string value, emit `None` with `'malformed': 'path'` and never copy the value. This fixes CX1, CX2 and CX4.
3. For `scheme://` paths, drop the userinfo, query and fragment, and record `'redacted': ['query', …]`. Keep the scheme, host and path. This fixes CX3.
4. In the hash, use `ensure_ascii=True` (the default) so the hash cannot raise. Wrap each line's handling so that a non-object value, or a non-dict `message`, `data` or `content`, sets `parsed = False` and continues. This fixes CX7.
5. Fixtures: add negative cases CX1 through CX7 to the C2 checker's fixed-fixture set before C2 counts as improved.
   - CX1, CX4 and CX6 must show the path or descendant actually retained.
   - CX2 and CX3 must show the payload or query absent.
   - CX5 and CX7 must show that no traceback occurs and the seat is marked `complete: false`.

## Not evaluated

- `tools/check-seat-bindings.py`, so I could not check whether it handles `null` or `{}` projections as UNKNOWN denials.
- The host's grep and glob argument schemas.
- The runtime behavior of every fixture above.

None of these files were in this seat's read paths. No commands, fetches, installs or edits were made outside this report.
