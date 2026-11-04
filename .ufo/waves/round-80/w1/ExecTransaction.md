# ExecTransaction — round80 w1 — C2 hermetic `--selftest` for tools/check-transaction-order-r39.py

Execution class: EXEC-AUTHORIZED (selftest built and run on a scratch COPY; Git commits only inside
throwaway selftest fixtures; zero lane/fleet mutations; instrument/expected untouched).

Axes: **depth** (selftest actually pins the public evaluator's behavior per defect class) and
**operability** (one exact registry-runnable command, byte-bound receipt, honest usage semantics).

## Deliverables (all beneath /home/vgpnk/Projects/shokunin/tsukuroi-shokunin)

- `.ufo/waves/round-80/w1/ExecTransaction/check-transaction-order-r39.py` — full repaired source,
  sha256 `c7055a81f98b8462b3a34ba17545087bdb09bb17532594dd1a9823aa9b5aec33`
  (frozen original `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`, byte-identical
  at lane working tree, blob at 61ec89e, blob at lane HEAD aad05ef1 — corroborated, not altered).
- `.ufo/waves/round-80/w1/check-transaction-order-r39.py.receipt.json` — binding receipt:
  `tool_sha256` = the final repaired bytes, `argv ["python3","tools/check-transaction-order-r39.py","--selftest"]`,
  `rc 0`, `passed 9`, `failed 0`. Satisfies measure-round80 C2 receipt contract (argv list equality,
  rc 0, failed 0, passed int ≥ 4).
- `.ufo/waves/round-80/w1/ExecTransaction/` evidence: `selftest.stdout`, `selftest.stderr`
  (final receipt run), `usage.stdout`, `usage.stderr` (no-args usage path), `redbefore.stdout`,
  `redbefore.stderr` (mutated control), `diff-vs-frozen.txt` (complete delta vs frozen bytes),
  `digests.txt`, this report.

## Behavior added (single new mode; production semantics preserved)

- `--selftest`: hermetic, exit 0 pass / **3 failed**. Builds one `$TMPDIR` root of throwaway Git
  repos (`git -c init.defaultBranch=master init`, fixture-only committer identity
  `tsukuroi-selftest <selftest@scratch.invalid>`, `git rev-parse --show-toplevel` asserted equal to
  the fixture dir before any write, every write path checked against the repo root). Nine cases each
  drive **this file's public CLI** via subprocess (`[sys.executable, __file__, --repo <fixture>,
  --revision <sha>]`) — the real `main()` → `_revision.bind` → `load_frozen` → `git_show` evaluator,
  not helper-only assertions:
  - POSITIVE: rc 0, `PASS`, `rules_verified 8`, `duplicate_rows 0`, `duplicate_headings 0`,
    `source_ok 1`, `counts_ok 2`, `oracle_violations 0` (fixture entry quotes are lifted from the
    tree's own digest-pinned frozen snapshots; TO1/TO8 host cells carry the real frozen-capture
    counts, so `counts_ok == 2` is earned, not mocked);
  - ENTRY-MISSING (missing data): rc 1, `entry_present false`, `rules_verified 0`;
  - WRONG-SOURCE-FILE / QUOTE-CORRUPTED / SID-NOT-ON-SOURCE-LINE (wrong source/quote): rc 1 with the
    stable reasons `no 4-25 word quote found in <file> at the cited lines` /
    `cited S-id not on source: line: S299`;
  - ROW-MALFORMED (host cell dropped → 3 cells): rc 1, reason `fewer than 4 cells`;
  - DUPLICATE-BLOCK: rc 1, `duplicate_rows 1`, `duplicate_headings 1`;
  - HOST-COUNTS-WRONG: rc 1, `counts_ok 0`;
  - REVISION-INVALID: rc 2, stable id `E-REVISION-INVALID`.
  Summary line `SELFTEST total=9 passed=9 failed=0`; per-case `PASS (SELFTEST-<ID>)` /
  `FAIL (SELFTEST-<ID>): …` lines; no exception is swallowed (case-level surprises are reported and
  counted as failures; setup failures print a full traceback and return 3). Fixtures are removed in
  `finally`; post-run `$TMPDIR` verified empty; no write outside `$TMPDIR` (verified with a
  `find -newer` probe over the whole scratch tree).
- `--revision` is no longer `required=True`; when `--selftest` is absent and `--revision` is missing,
  `ap.error('the following arguments are required: --revision')` reproduces the exact previous usage
  error (exit 2, same message — see `usage.stderr`). Binding path (`_revision.bind`), frozen-input
  digest checks, predicate, JSON shapes and exit codes 0/1/2 are untouched. Docstring documents the
  mode. `_revision.py` is imported from the tool's own directory (copied verbatim to the scratch
  tree; in the lane it resolves as today).

## Verification exercised (scratch copy of identical bytes)

- `python3 -m py_compile` clean; final selftest rc 0, 9/9 (`selftest.stdout`).
- Red-before control: single-point evaluator mutant `dup_rows = 0` (duplicate-row counting dropped)
  → selftest rc 3, `FAIL (SELFTEST-DUPLICATE-BLOCK): duplicate_rows=0 != 1`, other 8 cases still
  pass (`redbefore.stdout`) — the selftest fails when the evaluator is broken, passes on repaired
  bytes.
- Usage path: no args → exit 2 with the unchanged argparse message (`usage.stderr`).
- Hermeticity: no writes outside `$TMPDIR`; fixture repos deleted; scratch tree inventory unchanged.

## Draft registry cell (REPORT ONLY — registry NOT changed by this seat)

Placement: append exactly one row to the table inside the existing `## Gate and probe registry —
round71 superseding current rows` section (SKILL.md section currently ending at line 5907/heading at
5908). Do NOT create a new `## Gate and probe registry — round<N> …` heading (it would become the
operative table and drop every carried row) and do NOT duplicate the name row inside that section
(measure-round80 requires exactly one `| check-transaction-order-r39 |` row there). The Self-test
cell must be the bare exact command — measure-round80 compares that cell for string equality, so no
annotation may follow it; the case detail belongs in Pinned values. Cell layout matches the existing
8-cell header:

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| check-transaction-order-r39 | gate | `python3 tools/check-transaction-order-r39.py --revision <REV> [--branch <BRANCH>] [--repo <PATH>]` | 0 PASS (`rules_verified == 8` and `duplicate_rows == 0` and `duplicate_headings == 0` and `source_ok == 1` and `counts_ok == 2` and `oracle_violations == 0`); 1 FAIL (per-rule reasons: cited S-id not on the `source:` line, no mined upstream row at 54d9411, no 4-25 word quote at the cited lines, fewer than 4 cells; duplicate rows/`## ` headings; `counts_ok < 2`; entry absent); 2 could-not-evaluate (`E-REVISION-INVALID`, `E-REVISION-NOT-LANDED`, `E-REVISION-NOT-PUSHED`, `E-BRANCH-MISSING`, `E-GIT-FAILED`, frozen-input tamper) and the unchanged argparse usage error when `--revision` is missing without `--selftest`; 3 self-test failed | `python3 tools/check-transaction-order-r39.py --selftest` | hermetic nine-case selftest over `$TMPDIR` fixture Git repos (fixture-only identity, top-level verified before writes): POSITIVE rc 0 8/8; ENTRY-MISSING, WRONG-SOURCE-FILE, QUOTE-CORRUPTED, SID-NOT-ON-SOURCE-LINE, ROW-MALFORMED, DUPLICATE-BLOCK, HOST-COUNTS-WRONG rc 1 with the named findings; REVISION-INVALID rc 2 `E-REVISION-INVALID`; red-before `dup_rows = 0` mutant → rc 3 `FAIL (SELFTEST-DUPLICATE-BLOCK)`; measured run bound by the round-80 C2 receipt `.ufo/waves/round-80/w1/check-transaction-order-r39.py.receipt.json`; no selftest tally copied here | snapshot digests `SRC_SHA` and capture `CAP_MANIFEST_SHA` pinned in the tool; frozen inputs `.ufo/waves/round-39/frozen/` read from the tool's own tree | committed git reads through `_revision.bind`; the tool writes only inside its selftest's `$TMPDIR` root; lane read-only | tsukuroi |

The sibling C2 tool (`count-kr-rows-r69.py`) and its row/receipt are out of this seat's scope
(presently the round71 row carries `none: no self-test mode`).

## Risks / handoff notes for main

- The receipt binds the bytes, not the location: after the repaired source lands at
  `tools/check-transaction-order-r39.py`, rerun exactly `python3 tools/check-transaction-order-r39.py
  --selftest` (TMPDIR may stay default; the mode is hermetic anywhere) and confirm rc 0 before/with
  scoring — the receipt's rc/passed/failed must describe the landed bytes (sha256 must equal
  `c7055a81…`).
- First import of `_revision.py` in a fresh worktree creates `tools/__pycache__` (standard CPython
  behavior, same as existing tools importing `_revision`).
- The selftest's fixture Git repos are created and deleted inside one invocation; a hostile/absent
  `$TMPDIR` fails loudly as a selftest failure (rc 3), it does not fall back to any fixed path.

## Cleanup

Scratch `/fast/scratch/hyaku/tsukuroi-r80/ExecTransaction/` (single live tree + receipts + tmp)
deleted after the durable receipts above were copied out.

Tools installed/updated: none (python3 + git 2.56.0 already present; channels untouched). No pacman
transaction, no sudo, no service restart, no secret/config reads.

Scope: executed=cp(tree staging: tools/_revision.py, tools/check-transaction-order-r39.py,
.ufo/waves/round-39/frozen/{src,txcapture} lane→scratch); python3 -m py_compile
tools/check-transaction-order-r39.py; TMPDIR=<scratch>/tmp python3
tools/check-transaction-order-r39.py --selftest (scratch tree; 3 runs: 1st caught a fixture-builder
bug in ROW-MALFORMED, 2nd/3rd green — 3rd is the receipt run); python3 tools/check-transaction-order-r39.py
(no args, usage check); python3 tools/mutant-check-transaction-order-r39.py --selftest (red-before
control); git -C <scratch fixtures> init/add/commit/rev-parse/rev-parse --show-toplevel (inside
selftest fixtures only, fixture identity); git -C <lane> rev-parse HEAD; git -C <lane> cat-file blob
61ec89e…:tools/check-transaction-order-r39.py | sha256sum; git -C <lane> show
HEAD:tools/check-transaction-order-r39.py | sha256sum; sha256sum; diff -u; find; wc -l; du; ls; cat;
grep; cp (deliverable + evidence lane-side); write (report, receipt, digests); rm -rf
/fast/scratch/hyaku/tsukuroi-r80/ExecTransaction. No other verification run; no lane/fleet/Git/jj
mutation; instrument and expected untouched.
