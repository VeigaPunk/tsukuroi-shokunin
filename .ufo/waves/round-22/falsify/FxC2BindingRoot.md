# FxC2BindingRoot — falsification report, round-22 C2 seat-binding checker

Target: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`
Reviewed-SHA256 (as declared in the assignment; recomputation forbidden — NO-EXEC, no command ran): `c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4`
Mode: static source-only review. NO-EXEC honored (no bash/eval/subprocess/import/selftest run); NO-FETCH honored (no URL/web access). All line cites are to the target file (241 lines).

## Verdict per attack clause

### 1. Manifest root outside exact lane — REJECTS

Single gate, no alternate acceptance path (`root` occurs only at L109 and the selftest literal L156):

- L109: `... or seat.get('root') != LANE or ...` with LANE hard-coded at L16 = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Exact string identity: a foreign lane, a trailing-slash spelling, a subdirectory root, a sibling root, a non-string, or a missing key all compare unequal → `raise ValueError('binding identity/root/allowlist')` (L110).
- The raise is caught in `evaluate`'s except (ValueError/TypeError/KeyError/AttributeError/UnicodeError) → `add('SCOPE-SCHEMA','input')`, code 2, status `CANNOT_EVALUATE`. Never exit 0.
- `ROOT` (L15, `Path(__file__).resolve().parents[1]`) is used only for git reads in `main`/`git_read`, never in the lane comparison — a relocated candidate tree still demands the canonical lane string; fail-closed.

### 2. Path outside root — REJECTS

- `local()` (L34–37): requires `path.startswith(LANE + '/')` — appending `'/'` to the prefix blocks the classic sibling-prefix confusion (`LANE + '-evil/x'` does not start with `LANE + '/'`); bans `\`, control/format/surrogate/line-separator characters (`controls()`), the glob metachar set `*?[];:` (which includes `:`), and any empty, `.`, or `..` segment in `path.split('/')[1:]`. So `LANE + '/../sibling/file'`, `LANE + '/x/../source'`, `LANE + '/./source'`, `LANE + '/a//b'`, trailing-slash and relative spellings all fail. Absolute POSIX spelling only.
- `requested_path` (L43–56): http/https (case-insensitive) and `host:port/` forms return `SCOPE-FETCH-DENIED` before containment; `skill://godspeed` passes by exact equality only; for `read` (and only `read`), trailing selector suffixes (`raw|img|conflicts|digits|-n|comma-ranges`, repeated) are stripped, then `local()` is re-checked on the stripped value. **No normalization is applied anywhere**: no `PurePosixPath`/`resolve`/`normpath`/`realpath` use exists in the file (the L7 `PurePosixPath` import is dead), so `..` can never be normalized away before the containment check.
- Manifest-freeze gate L111–114 applies `local()` to every `read_paths`/`write_paths` entry; the `skill://godspeed` exception is restricted to `read_paths` (`field == 'read_paths' and p == 'skill://godspeed'`), duplicates are rejected by `len(paths) != len(set(paths))`, and empty path lists are rejected.
- Per-tool membership in `classify` (L88–93): `write` checks `binding['write_paths']` only. A write spelled `skill://godspeed` passes `requested_path`'s equality shortcut but fails membership → `SCOPE-PATH-DENIED`; a manifest trying to bind it under `write_paths` is already rejected at L113. `xd://`/`artifact://`/globs (`LANE + '/**'`) fail `local()`.
- CLI surface independently rejects outside-root argument spellings: `repo_path()` (L39–40) requires a relative, `..`-free, backslash-free path for `--manifest`/`--events`, else `CANNOT_EVALUATE` `SCOPE-SCHEMA` at the `input path` site.
- Selftest expectations agree (source-visible): `LANE + '-extra'`, `LANE + '/child'`, `LANE + '/../sibling/file'`, `LANE + '/x/../source'`, `LANE + '/./source'`, `source`, `xd://tool`, `artifact://a`, `LANE + '/**'`, and write variants each expect exit 1 (`FAIL`) with `SCOPE-PATH-DENIED`.

### 3. Nonempty command/fetch lists — REJECTS

- L109: `seat.get('commands') != [] or seat.get('fetches') != []` — any nonempty list, wrong type, or missing key (None) is unequal to `[]` → same `ValueError` → exit 2, `SCOPE-SCHEMA`. The lists must be exactly empty.
- These fields are freeze-validated only; `classify` denies `bash`/`eval`/`task` by tool name (L77–78), `web_search`/`browser*` (L79–80), and everything unrecognized (L81–82, `SCOPE-TOOL-UNKNOWN`), including `functions.`-prefixed spellings (L75–76) and nested `multi_tool_use.parallel` children (L65–74, depth-capped). No code path consults a nonempty list to allow anything, so no list content can widen scope; the checker stays spelling-level detection, not prevention — consistent with `native_per_seat_allowlist: false` in `.ufo/waves/round-22/sources/host-tool-boundary.json` and the preregister C2 framing.

## Expected fixture verdicts (source-derived) vs observed runtime

Expected:

- Binding with foreign root (e.g. `LANE + '-sibling'`, `LANE + '/'`, or `LANE + '/sub'`): exit 2, `CANNOT_EVALUATE`, finding `SCOPE-SCHEMA` at site `input`.
- Binding with nonempty `commands` (e.g. `['true']`): exit 2, `CANNOT_EVALUATE`, `SCOPE-SCHEMA` at `input` — identical gate to the fetches case.
- Binding with nonempty `fetches` — existing selftest case `nonempty-fetch-allowlist` (L189, L190): expected exit 2, `SCOPE-SCHEMA`.
- Path-escape reads/writes — existing selftest cases: expected exit 1 (`FAIL`) with `SCOPE-PATH-DENIED` at `<seat>:<index>`.

Observed runtime: **none**. This seat forbids execution; neither `--selftest` nor the CLI was run, and the fixture expectations above are byte-level derivations from the reviewed source, not runtime observations. Any runtime contradiction would supersede them as a separate finding.

## Findings (non-blocking)

- F1 (fixture-coverage gap, medium-low): the selftest mutates only `fetches` (L189). No negative fixture flips `root` to a foreign lane and none fills `commands`. Both rejections are source-visible at L109 but lack the fixed negative fixtures the round-22 checklist requires before a new check's improvement counts. Authoring two cases (`root := LANE + '-sibling'` and `commands := ['true']`, each expecting 2 + `SCOPE-SCHEMA`) closes this.
- F2 (attribution granularity, informational, declared): read selector suffixes are stripped (L50–53) before allowlist checking, so a compliant event recorded with `path: LANE + '/source:1-5:raw'` is attributed to `LANE + '/source'`; range intent is not retained for compliant events. Containment is unaffected (the stripped spelling is still allowlist-checked) and the `SCOPE` string (L17) already declares recorded-spelling-only semantics.
- F3 (hygiene, trivial): `PurePosixPath` imported at L7, never used.
- F4 (declared non-goal, not a defect): `local()` is lexical; no symlink resolution, effect proof, or reading proof — exactly what `SCOPE` (L17) and the host-tool-boundary record disclaim. This tool is post-hoc detection; never describe it as preventive runtime enforcement.

## Residual risk / verification gaps

- Runtime behavior unobserved (NO-EXEC); source-derived verdicts could in principle differ at runtime only through Python semantics not visible in the reviewed bytes — none identified.
- Digest not independently recomputed (no execution permitted); reviewed bytes are the declared path's content at read time.
- Callers must read exit 2 `CANNOT_EVALUATE` as a rejection, never as a pass; incomplete trace coverage maps to `SCOPE-TRACE-MISSING`/`SCOPE-TRACE-INCOMPLETE` with could-not-evaluate status, matching the r22 boundary contract's DEAD/UNKNOWN separation.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2bindingroot
Scope: executed=none
