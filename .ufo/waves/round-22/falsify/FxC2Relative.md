# FxC2Relative: source-only falsification of check-seat-bindings.py

Seat FxC2Relative · predicate r22-fxc2relative · round 22 · baseline 894d1e20fb4939b0cc4fadf722c46d1429f257d2

## Result

No request-level bypass found. Relative, null-root and missing request paths all fail closed. Two medium counterexamples sit outside the event classifier: CLI input handling (F1) and the git trust root (F2). Expected fixture verdict is 42 of 42 pass, derived statically. Nothing was executed.

## Scope and limits

- Target: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`, 241 lines, read in full (1-241).
- Context read in full: `candidate/tools/_revision.py` (1-440), `candidate/tools/check-review-snapshots.py` (1-278), `preregister.json`, `sources/host-tool-boundary.json`, `candidate/corpus/knowledge/seat-boundary-r22.json` and `.md`, `skill://godspeed`.
- Digest: the declared c45c93e5…aa69c4 was not recomputed. NO-EXEC forbids hashing. The `#636F` in read output is a hashline tag, not SHA-256. The digest is taken as the declared identity of the reviewed bytes, unverified by this seat.
- "Expected" means derived by tracing source. "Observed" means run. Nothing was run.
- [INFERENCE] marks git, Python import, and pathspec behavior cited from documentation and source reading, not from execution.
- LSP and xd tools were not used.

## Axes

1. Request-path resolution: `path` in read, grep, glob and write events.
2. Root and cwd inference: `ROOT`, `LANE`, binding `root`, process cwd, module import.
3. Explicit-input presence at request, binding and CLI levels.
4. Fixture coverage of axes 1 to 3.

## Named vectors

| Vector | Request events | Binding entries | CLI inputs |
|---|---|---|---|
| Relative path | Denied (33-36, 54-55, 90-91). Fixture at 173 | Refused, exit 2 (113). No fixture | Accepted by design (39-40, 225). Resolved at committed tree root, not cwd (F3) |
| Null cwd or null root | No cwd field is read. No `getcwd`, `chdir` or `cwd=` in any of the three files. Holds | `root` null or missing is not LANE, exit 2 (109). No fixture | Not cwd-dependent for git (`-C`). Repository root inferred from `__file__` and never compared to LANE (F2) |
| Missing explicit path | Exit 2 for the whole audit, no silent allow (81-83, 145-147). Fixture is `read {}` only (179) | Missing `read_paths`, `write_paths` or `root`: exit 2 (109, 113). No fixture | Omitted `--manifest` and `--events` silently default (217-218). Counterexample (F1) |
| No inferred root | Holds. Exact string match against a LANE-absolute declared list | Holds | Violated at the trust root (F2). Relative CLI inputs (F3) |

## Findings

### F1 · Medium · counterexample: omitted CLI inputs are inferred, not refused

- 217-218: `--manifest` and `--events` have `default=` values and are not required. The `--revision`/`--selftest` group is required (213).
- 225-227 refuse an explicit empty, absolute or `.`/`..` path. Omitting the flag skips that gate, so the explicit-input contract is bypassed by leaving the flag out.
- 230 evaluates the default paths at the bound commit. 231 records revision, branch and branch_tip only. The output does not identify the manifest or events file used.
- Asymmetric failure: a missing committed manifest gives exit 1 (99-100). A missing committed events file gives exit 2 through the schema check (116-117). Both are non-PASS.
- Mitigation: preregister.json:6 passes both paths explicitly, and the defaults equal those paths. The preregistered command is unaffected. No false PASS is shown.
- Expected fixture verdict: none. `selftest()` (154-198) calls only `evaluate()` (193). `main()` is exercised only through `--selftest` (223-224). Revision and input handling (225-231) has no fixture. Contract expectation for omitted input: refusal, exit 2. Source behavior: evaluation of defaults.
- Observed runtime: none.
- Direction for main (not applied): make both flags required, or refuse omission. Echo manifest, events and ROOT in the result. Neither change alters any verdict for the preregistered command.

### F2 · Medium · repository root inferred from `__file__` and never bound to LANE

- 15: `ROOT = Path(__file__).resolve().parents[1]`. For this candidate path ROOT is `…/round-22/candidate`, not the lane root.
- 16: `LANE` is a literal. Nothing compares ROOT with LANE. ROOT appears only at 15, 202, 205 and 229.
- 229: `_revision.bind(ROOT, …)` binds the revision in whichever repository contains the tool file. The output (231) does not record the repository.
- 202, `git -C ROOT show rev:path`, is tree-root relative for `rev:path`. The candidate location does not change it.
- 205, the fallback probe `git --literal-pathspecs -C ROOT ls-tree -z rev -- path`, has no `--full-tree`. [INFERENCE from git-ls-tree's `--full-tree` and `--full-name` documentation] Its pathspec is then relative to the `-C` directory. Under the candidate layout it probes `candidate/<path>`.
- Effect in realistic trees: none on the verdict. Present files are read correctly. Absent files still return None, giving exit 1 for the manifest and exit 2 for events. No PASS from wrong bytes is shown.
- Latent hazard: running the tool from a different repository binds and reads that repository's commit, and the output does not show it. Not demonstrated. It requires a separate repository.
- Expected fixture verdict: none. No fixture exercises ROOT.
- Same pattern in the sibling: check-review-snapshots.py:17, 132, 136, 263.
- Direction for main (not applied): assert `Path(ROOT).resolve() == Path(LANE)` or pass the root explicitly. Pin the probe to the tree root. Echo the root in output.

### F3 · Low · relative CLI inputs resolve against the bound commit's tree root (decision needed)

- 39-40 `repo_path` accepts relative paths with no `.`/`..` component, no leading `/`, no control characters and no backslash. 225 gates them. 202 resolves them at the commit's tree root. 205 is the probe covered by F2.
- This is the only place a relative path resolves against an inferred root. Request paths never do.
- Same convention as the sibling: check-review-snapshots.py:26-30 `safe_path`, 131-142 `git_read`.
- Literal conflict with "no inferred root exception". Main should either accept this as the documented convention and state it in the module docstring, or require absolute paths together with the F2 assertion.

### F4 · Low · binding-level refusals and null root have no fixture

`selftest()` mutates the binding only for `fetches` (189). By source, each case below exits 2 with SCOPE-SCHEMA and is untested:
- a relative `read_paths` entry such as `source` (113)
- empty or missing `read_paths` or `write_paths` (113)
- `skill://godspeed` in `write_paths` (113)
- a duplicate entry (113)
- `root` null, missing, or `LANE + '/'` (109)
- `commands` or `fetches` missing (109)

### F5 · Low · missing request path: attribution lost, evaluation partial, fixture covers `read` only

- 81-83 raise ValueError for a missing, null or empty `path`. 145-147 catch it and record SCOPE-SCHEMA at `site: input` (146), with no seat or event index.
- Evaluation stops at the first such event. `rows`, `violations` and `requests_total` are then partial. Exit 2 holds, so no PASS.
- The check is shared by read, grep, glob and write (79-83). Only `read` with `{}` is tested (179).
- Holds as fail-closed. The defect is the attribution.

### F6 · Low · skill selector denied (false positive)

- 48-49 exact-match `skill://godspeed` before selector stripping (50-53). `skill://godspeed:1-5` strips to `skill://godspeed`, which fails `local()` (54-55) and returns SCOPE-PATH-DENIED.
- A compliant selector read of the declared skill is flagged. Expected by source: exit 1. No fixture.

## Adjacent observations (outside the named vectors)

- A1 · Low · `functions.multi_tool_use.parallel` misclassified. The parallel test (63) runs before the `functions.` strip (73-74). A prefixed wrapper falls to SCOPE-TOOL-UNKNOWN (79-80) and its children are never inspected. Fixtures use unprefixed names only (180-183).
- A2 · Low · `--help` exits 0 with no audit (220-222). An exit-code-only consumer reads PASS.
- A3 · Low · metric. `request_audit_mode` is 1 for every evaluated input (149-151), including FAIL and CANNOT_EVALUATE. preregister.json:6 targets this metric, so the C2 target is met by engagement alone.
- A4 · Low · [INFERENCE] tool-name vocabulary is bare (75-79). Qualified names other than `functions.`, such as the underscore-prefixed `_read` form used by this runtime's tool list, classify as SCOPE-TOOL-UNKNOWN. Compliant reads would be flagged. Exit 1 either way, so no PASS.
- A5 · Low · [INFERENCE] `import _revision` (13) precedes `__file__` use (15). For file invocation sys.path[0] is the script directory. Under stdin or `-c` it is the process cwd, so a `_revision.py` there would execute, and the run would then fail with NameError. Exit non-zero, no PASS.
- A6 · Info · a complete trace with zero events passes (130-143; fixture 190 expects 0). The report write is not required, so the checker trusts the `complete` flag.
- A7 · Medium · sibling, outside target. check-review-snapshots.py: `DEFAULT = ".ufo/waves/round-21/reviews.json"` (18) is the omitted `--manifest` default (250). A round-22 run without the flag evaluates round-21 reviews at the bound commit when they are present. Output omits the manifest path (266). Same defect class as F1, with a stale wave.

## Expected fixture verdict versus observed runtime

- Expected, by static trace of `selftest()` (155-190): 42 of 42 cases pass. Status PASS, exit 0.
  - Attack-relevant cases: relative `source` (173) gives 1 SCOPE-PATH-DENIED. `LANE/../…` and `LANE/./…` (173) give 1. Missing path with `read {}` (179) gives 2 SCOPE-SCHEMA. `https://` and `localhost:9222/` (169-170) give 1 SCOPE-FETCH-DENIED. `bash` (167) gives 1 SCOPE-EXEC-DENIED. Exact `skill://godspeed` (165) gives 0. `LANE/source:1-5:raw` (164) gives 0.
- Observed runtime: none. No test, selftest, import or invocation was run.

## Verification gaps

- Digest not recomputed.
- No semantic caller or definition checks: LSP and xd tools were not used.
- All fixture verdicts above are static. Main should confirm them with its single post-wave `--selftest` run.
- F2, A4 and A5 rely on [INFERENCE] about git, producer naming and Python import. Confirm before acting on them.

## Receipt

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2relative
Scope: executed=none
