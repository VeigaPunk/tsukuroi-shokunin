Reviewed-SHA256: 3d720f6aa18b3b9f5e4ec0f5b3c82cb7d7becddf1d2b6a40bbccd3ca31a7a47a
Predicate: r22-fxcollectroot
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.

# FxCollectRoot: source-only falsification of round-22 collector ROOT and writes

Target: `.ufo/waves/round-22/candidate/.ufo/waves/round-22/collect.py`, 134 lines, read in full (L1-134). The digest above is the assigned value; it was not recomputed because NO-EXEC forbids hashing commands.

Method: source reading of the target; grep over the three declared Python files for write, path-resolution, symlink, and bytecode patterns; full reads of the declared JSON and Markdown context. Nothing was executed, imported, compiled, fetched, or delegated.

## Result

Attack line: ROOT and all writes lane-relative; caller transcripts read-only.

- ROOT lane-relative: holds only for an unlinked canonical placement. Counterexamples F1, F3, and F4 (F4 is round scope, still inside the lane). ROOT is never validated; it is inferred from the file's own location.
- All writes lane-relative: counterexamples F1 and F2. The write set itself is exact (H2).
- Caller transcripts read-only: holds (H1). The consequence of a bad transcripts path is F5.

## Findings (source-visible)

F1 — High if a symlink exists in the lane. ROOT follows symlinks.
- L16 `ROOT = Path(__file__).resolve().parents[3]`. `resolve()` follows symlinks on the script and on every ancestor, so ROOT is the tree containing the real file, not the tree the caller invoked from.
- Counterexample: `<lane>/.ufo/waves/round-22/collect.py` symlinked to `<other>/.ufo/waves/round-22/collect.py` makes ROOT = `<other>`; L122-123 then write under `<other>/.ufo/waves/round-22/build/`. A symlinked `.ufo`, `waves`, or `round-22` ancestor changes ROOT the same way. Nothing compares `__file__` with its real path or asserts that ROOT equals the invoking lane.
- Whether such a symlink exists in this lane cannot be checked under the binding.

F2 — High if any output-path component is a symlink or hardlink. Writes follow links.
- L37 `directory = WAVE_ROOT / wave`; L122-123 `(directory / name).write_text(...)`. `write_text` opens for write with truncation and without `O_NOFOLLOW`. The declared grep finds no `is_symlink`, `O_NOFOLLOW`, `symlink`, `mkdir`, `rename`, `unlink`, or `replace(` in any declared Python file, and no `open(` call in collect.py.
- A pre-existing `build/settlement.json` symlink redirects the write to any writable target. A hardlinked output is truncated and rewritten through a shared inode.

F3 — High when the candidate copy is run in place. File placement decides where outputs land.
- Path arithmetic: `parents[3]` of `…/round-22/candidate/.ufo/waves/round-22/collect.py` is `…/round-22/candidate`. ROOT is therefore the candidate snapshot, and WAVE_ROOT is `…/candidate/.ufo/waves/round-22`.
- A run from the candidate writes into the candidate snapshot, not the lane's `.ufo/waves/round-22/build/…` that preregister C2 and C3 read (preregister L6-7). Checklist item 1 requires frozen source snapshots (seat-boundary-r22.md L28).
- If `candidate/.ufo/waves/round-22/<wave>/swarm-registry.json` is absent, L38 raises before any write (fail-closed). If it is present, the snapshot gains new files.
- The file never asserts its own placement: no `--root` option, no toplevel check, no comparison with the preregistered output path.

F4 — Medium. WAVE_ROOT hardcodes round-22 (L17).
- A copy at `<repo>/.ufo/waves/round-23/collect.py` gets ROOT = `<repo>` and writes `<repo>/.ufo/waves/round-22/{build,falsify}/…`, overwriting round-22 evidence. The docstring claim "Writes only this round's wave evidence" (L4-5) is false for that placement.

F5 — Medium. A mistyped transcripts path replaces prior outputs with unknown rows and exits 0.
- L39 `transcripts.glob('*.jsonl')` has no `is_dir()` check; argparse L132 is `type=Path` only. A missing directory yields an empty index; L46-49 mark every seat `registered transcript unavailable` / `unknown`; L122-123 overwrite both files; L124 prints; exit 0.
- [INFERENCE, not executed] CPython `Path.glob` on a non-directory base yields nothing rather than raising. If it did raise, the crash would precede the writes and F6 applies instead. The source has no guard either way.
- Conflicts with seat-boundary-r22.md checklist item 3 (preserve sanitized request metadata, L30) and item 4 (never drop a denominator, L31).

F6 — Medium. Any exception before the writes leaves stale outputs; the pair is not atomic.
- Both writes run after the full loop (L122-123). Exceptions visible in source each leave the previous generation in place with no failure marker:
  - L59-63: a valid non-object JSON line (`null`, `[]`, `1`, `"s"`) makes `obj.get` raise AttributeError; only ValueError and UnicodeError are caught (L60).
  - L66-67: non-dict `message`. L79-80: non-dict `data`.
  - L42: missing `agentId` raises KeyError. L43: unhashable `agentId` raises TypeError.
  - L113: a lone surrogate in tool args makes `.encode()` raise UnicodeEncodeError.
  - Deep nesting raises RecursionError, which L60 does not catch.
- Non-atomic pair: L122 completes before L123. A failure or kill at L123 leaves this run's `events.json` beside an older `settlement.json`. A kill during L122 leaves truncated JSON, because `write_text` truncates first. Concurrent runs interleave. Nothing binds the two files to one run: no run id, registry digest, or collector digest; only per-transcript `transcript_sha256`.

F7 — Medium. Content of writes: the "credentials not copied" claim (L6) does not hold for some inputs.
- L94-98 copy `error[:1200]` whenever `stopReason == 'error'` and any L96 token appears (`rate_limit_error`, `rate limit`, …) and the L97 regex (`bearer |api[_-]?key|token=|cookie`) does not match. A bare key-shaped token or `sessionid=` in such an error passes and is written to settlement.json.
- L103-104 copy `provider` and `model` raw, with no type or shape check. L31-32 copy tool `path` arguments raw.

F8 — Low. Import and path-shadowing side effects.
- Run as a script it writes nothing extra. Importing it writes `__pycache__/collect.cpython-*.pyc` under `.ufo/waves/round-22/`: L10-14 omit the `sys.dont_write_bytecode = True` that check-review-snapshots.py L14 sets. No importer is visible in declared paths.
- `sys.path[0]` is the script's own directory, so a lane file named `json.py`, `re.py`, or `hashlib.py` there would shadow the stdlib import. [INFERENCE from standard import order, not executed.]

## Holds (bounded)

- H1 Transcripts are read-only. Transcript data is touched only by `glob` (L39), `read_bytes` (L50), and dict lookup. The only write sites in collect.py are L122-123, both under `directory`. Bound: symlinked transcripts are read through, read-only.
- H2 The write set is exactly two fixed names, `events.json` and `settlement.json`, under `WAVE_ROOT/<wave>`. The CLI restricts `wave` to `build|falsify` (L131), so there is no CLI traversal, and there is no mkdir, rename, or delete. Bound: `collect()` itself accepts any string.
- H3 No absolute-path literal and no argv or env override of ROOT. Bound: placement is the only control (F1, F3).
- H4 ROOT is independent of CWD (`__file__`-based). A relative `transcripts` argument resolves against CWD.
- H5 Outputs carry no transcript file paths; transcripts appear only as SHA-256 digests and byte counts (L51-52).
- H6 In canonical unlinked placement the collector writes only round-22 `build` or `falsify` outputs, leaving round-21 untouched (preregister L13). Bound: F4.

## Adjacent, outside this seat's attack surface

- A1 (relevant to request audit C2) L85-87: when a `tool_execution_start` reuses an id already declared by an assistant toolCall, its `toolName` and `args` are discarded. A declared `read` executed as `bash` is recorded as `read`.
- A2 L23 matches `multi_tool_use.parallel` without stripping `functions.`, while L31 strips it. A prefixed parallel wrapper gets `{}` args and its children disappear from events. Fail-closed only if the auditor denies unrecognized names; the auditor is not in declared paths.
- A3 Population is whatever `swarm-registry.json` lists (L38, L41), with no cross-check against a frozen declared population. A shorter registry shrinks the C3 denominator with exit 0.
- A4 Unavailable rows (L46-49) omit `transcript_sha256`, `answering_provider`, and `answering_model`, so the schema is not uniform.
- A5 L92: any non-empty content without a toolCall counts as final text, including thinking-only blocks.

## Expected fixture verdicts vs observed runtime

Observed runtime: none. No fixture was built or run (executed=none). The verdicts below are source predictions for named fixtures.

| Fixture (not run) | Predicate | Source-predicted verdict |
|---|---|---|
| Canonical unlinked placement; valid transcripts | writes only the two files under the invoking lane's build dir | PASS |
| collect.py symlinked into another lane | writes stay in the invoking lane | FAIL |
| `build/settlement.json` symlink to an outside path | writes stay in the lane | FAIL |
| Candidate copy run in place, registry present | outputs at the preregistered build path | FAIL |
| Copy placed under `round-23/` | writes only the invoking round | FAIL |
| Missing transcripts directory, prior outputs present | prior outputs not replaced unmarked | FAIL (exit 0 predicted) |
| One transcript containing a `null` JSON line | fresh outputs, or nonzero exit with no stale pair | FAIL (stale pair predicted) |
| Second write fails | pair is generation-consistent | FAIL |
| Transcript bytes and mtime before and after a valid run | transcripts unchanged | PASS |
| CLI wave argument `../x` | rejected | PASS (argparse choices reject it) |
| Error with `stopReason` error, `rate_limit_error`, and a placeholder key-shaped token | no credential-shaped text written | FAIL |

## Verification gaps

- SHA-256 3d720f… was not recomputed (NO-EXEC).
- Not readable under the binding: check-seat-bindings.py, check-review-cohort.py, swarm-registry.json, the transcripts, the lane's directory layout, and whether any ancestor is a symlink. The F1 and F3 conditions are therefore unconfirmed.
- No declared document names the collector's invocation path, CWD, or lane root; the intended placement is inferred from the C2 and C3 output paths.
- Standard-library behavior (pathlib glob, argparse, import order) is INFERENCE; the interpreter was not consulted.
- check-review-snapshots.py and _revision.py were read in full as sibling conventions only; neither is the target.

## Tooling

No tools installed or updated. No commands run.

## Suggested guards (not applied; no production edits)

- Derive the lane root from the invoking location and refuse when the script path or any ancestor is a symlink (`realpath` must equal `abspath`).
- Refuse symlinked `build/`, `falsify/`, or output names. Write temp files in the same directory and `os.replace` them as a pair. Delete or mark prior outputs before collecting.
- Require `transcripts.is_dir()`. Treat non-object JSON lines as `parsed=False`. Set `sys.dont_write_bytecode = True`.
- Replace substring error copying with an allowlist of exact provider categories. Drop raw provider and model values unless they are shape-checked.
