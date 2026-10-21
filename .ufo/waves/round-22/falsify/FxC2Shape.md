# FxC2Shape — source-only falsification of `check-seat-bindings.py`

Target: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py` (declared SHA256 `c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4`; byte hash not recomputed — NO-EXEC seat).
Attack brief: bad args type; missing/non-string/empty path; malformed event; schema could-not-evaluate.
Method: source reading only. Lines cited from the candidate bytes. No command, import, fixture run, or fetch was performed.

## Axes

1. Schema fail-closed correctness (malformed input → `SCOPE-SCHEMA` + `CANNOT_EVALUATE`).
2. Finiteness of the post-hoc audit (every input yields a bounded verdict).
3. Diagnostic attribution (finding id/site names the true failure surface).
4. Fixture coverage of the enumerated attack classes in `selftest`.

## 1. Enumerated attack cases — bounded reasons they hold

Every case below raises inside `evaluate`'s try block and is caught at line 145
(`except (ValueError, TypeError, KeyError, AttributeError, UnicodeError)`), producing
`SCOPE-SCHEMA` at `input`, code 2, status `CANNOT_EVALUATE` (lines 146–149).

| Case | Source behavior | Verdict path |
|---|---|---|
| args non-dict (`[]`, `"x"`, `None`, int) | line 61 `not isinstance(args, dict)` → `ValueError('malformed tool request or excessive wrapper nesting')` | code 2, `SCOPE-SCHEMA`, `CANNOT_EVALUATE` |
| missing `path` key | line 81 `args.get('path')` → `None`; line 82 raises `ValueError('missing explicit path')` | same; selftest `bad-args` (line 179) pins exactly this |
| non-string `path` (int/list/dict/bool/null) | line 82 `not isinstance(value, str)` → raise | same |
| empty-string `path` `''` | line 82 `or not value` → raise | same |
| malformed event (element of `seats[].events` not a dict) | line 135–136 `raise ValueError('event shape')` | same |
| parallel container malformed (`tool_uses` absent/non-list/empty, child non-dict, child missing `recipient_name`/`parameters`) | lines 63–71; child `get` → `None` re-enters line 61 guard; depth>8 guard line 61 bounds recursion | same |
| malformed binding/trace shape (bad schema, empty seats, non-string or unhashable seat name, duplicate seat/agent, non-bool `complete`, non-list `events`, duplicate JSON keys via `unique` hook) | lines 105–123 raise `ValueError`/`TypeError`/`KeyError`, all in the caught tuple | same |
| bad CLI `--manifest`/`--events` (empty, absolute, `..`, backslash, controls) | line 225 `repo_path` gate → line 226 `CANNOT_EVALUATE` / `SCOPE-SCHEMA` @ `input path`, exit 2 | bounded |
| bad `--revision`/`--branch` | `_revision.bind` raises typed `RevisionError` → line 232–233 `CANNOT_EVALUATE` with `E-*` fid | bounded |

Status mapping `('PASS','FAIL','CANNOT_EVALUATE')[code]` (line 149) makes the schema outcome exactly the expected could-not-evaluate verdict.

**Expected fixture verdict** (source-derived, per case in the table): exit 2, `status=CANNOT_EVALUATE`, finding id `SCOPE-SCHEMA`, site `input`.
**Observed runtime**: none. No execution permitted; `Scope: executed=none`.

## 2. Findings (severity order)

### F3 — Medium-High: selector regex exponential backtracking defeats the finite-verdict contract
`requested_path`, line 51: `re.fullmatch(r'(.+?)(?::(?:raw|img|conflicts|[0-9]+(?:[-+][0-9]*)?|-[0-9]+|[0-9,-]+))*', value)`.
Counterexample input (well-typed, passes every earlier gate): a recorded event
`{"tool":"read","args":{"path":"a:"+"1-"*30+"#"}}`.
- `classify` accepts it (str tool, dict args, nonempty str path, line 81–83).
- URL regexes (line 46) fail fast; not `skill://godspeed`; selector strip runs because `selector=tool=='read'` (line 87).
- The three suffix alternatives overlap (`A=[0-9]+(?:[-+][0-9]*)?`, `B=-[0-9]+`, `C=[0-9,-]+`) inside an ungrouped `*` loop with a lazy `.+?` prefix; Python `re` has no memoization or atomic groups. The `1-1-…` run admits ~2^L partitions and the trailing `#` forces exhaustive exploration before the (existing) match is found.
- Effect: `evaluate` does not return in practical time; the audit emits **no** verdict — not even `CANNOT_EVALUATE`. This contradicts the function contract "Return finite post-hoc findings" (line 60) and the fail-closed schema-could-not-evaluate expectation for malformed-but-typed inputs. It is reachable from the C2 metric command itself whenever a hostile or buggy recorded read path lands in `events.json`.
- Evidence basis: regex structure is source-visible; the hang is [INFERENCE] from backtracking semantics — no execution was performed.

### F2 — Low-Medium: `RecursionError` escapes the schema handler and is misattributed to the revision read
Line 145 catches `(ValueError, TypeError, KeyError, AttributeError, UnicodeError)` — not `RecursionError`. A `manifest`/`events` JSON blob nested deeper than the interpreter recursion limit makes `json.loads` (lines 102–103) raise `RecursionError` inside the try block; it leaves `evaluate` and hits `main`'s broad catch `except (OSError, RuntimeError, subprocess.TimeoutExpired)` (line 234) because `RecursionError` subclasses `RuntimeError`. Result: `CANNOT_EVALUATE` with `{'id':'SCOPE-READ','site':'revision'}` (line 235) — an **input schema failure reported as a revision read failure**. Exit code and status stay correct (2/`CANNOT_EVALUATE`), so C2's exit semantics survive; the finding identity is wrong, which matters in a pipeline whose purpose is strict error attribution. Under `--selftest` the same input would crash `selftest()` uncaught (fixed cases only, so not currently reachable there). [INFERENCE: CPython `json` recursion behavior; not executed.]

### F4 — Low: selftest does not pin the enumerated attack classes
`selftest` cases (lines 154–198) cover `bad-args` only as **missing** path (line 179). Absent: args non-dict type, non-string path, empty-string path, top-level non-dict event inside `seats[].events`, deeply nested JSON (F2), and any selector-path pathology (F3). The round rule "new checks require fixed negative fixtures" is only partially satisfied for this checker; F3 in particular could regress silently.

## 3. Observations (no defect)

- Over-denial, safe direction: `read` of `skill://godspeed:1-5` — the selector strips to `skill://godspeed` (line 51–53) but `local()` then denies it (line 54–55), so a selector-qualified read of the one approved non-local path records `SCOPE-PATH-DENIED`.
- `write` of `skill://godspeed` passes `requested_path` (line 48) but fails the allowlist check (line 90); binding validation (lines 111–114) permits the skill URI in `read_paths` only, so the write stays denied — fail-closed.
- Lone-surrogate or control-bearing path spellings are denied as data (`controls()` → `SCOPE-PATH-DENIED`), not crashes; `unicodedata.category` cannot raise on any decoded JSON string.
- `grep`/`glob` `;`-split parts re-enter the same checks; empty parts denied (line 54 via `local('')`).

## 4. Residual risk and verification gaps

- F3 and F2 runtimes were not observed — no execution permitted. A single bounded fixture run of the `a:1-1…#` path (with a timeout) and a deep-nesting events blob would convert both from inference to fact; the expected outcomes are `SCOPE-SCHEMA`/finite for a fixed tool, or the reported defects.
- F3 fix shape (out of scope here): bound suffix length before line 51 or replace the alternation with a possessive/atomic equivalent and a length cap; F2: add `RecursionError` to line 145.
- Threat-model bound: inputs are git blobs at the pinned revision recorded by the wave harness, so exploitation requires a recorded hostile path — but the auditor exists precisely to audit such records, so finiteness is in scope for it.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2shape
Scope: executed=none
