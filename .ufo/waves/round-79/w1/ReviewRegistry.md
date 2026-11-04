claim=C2
verdict=met — the frozen C2 predicate ("zero duplicate current rows and two gate-standard rows") is reproduced independently on the integrated worktree: `duplicates=0 shape_ok=2/2 met=1` rc 0, against a reproduced before value of `duplicates=6 shape_ok=0/2 met=0` rc 1 at both the freeze `afe1f261…` and the base `9086589a…`. Nine findings below (F1, F1b, F1c, F2–F7 in `ReviewRegistry/findings.md`); none overturns the numeric leg, but F1b falsifies this item's own acceptance sentence for the instrument: a row whose self-test cell names a nonexistent `--selftest` still passes. The delivered rows name their own tools and I ran those modes green, so the current green is substantively backed — the gap is in the counter, not in the delivered bytes. One seat-text expectation — "freeze coverage must stay PASS" — is contradicted by measurement (F3): coverage at the freeze is FAIL because the freeze introduced both r79 tools before any row named them; the repair under review is exactly what restores 119/119. No self-test referenced by the repaired rows is missing or red at the final digests.

# ReviewRegistry — independent verification of the C2 repair

Date: 2026-11-04. Measured revisions: base `9086589a82f221d130ed6711fbe70b85f0d07aea`,
freeze `afe1f26128bde87484001cd02ebf11fa524c4059`, integration HEAD
`883aae6107cace30795d3163092b08498e8d4b73` (the dispatch commit — the L1 had not committed
the integrated tree when this seat measured; see residual gaps). Scratch:
`/fast/scratch/hyaku/tsukuroi-r79/ReviewRegistry/` (deleted before yield). Receipts with
every argv/rc/stdout: `ReviewRegistry/receipts.json`. Per-finding detail:
`ReviewRegistry/findings.md`.

## Measured digests of the bytes this review certifies

| path | sha256 |
|---|---|
| `SKILL.md` (post-edit) | `97716dd920cca67f3c948ebed02f5a29b56a3afce3e8f93c2b82a449f2a8054d` |
| `tools/check-r71-routed-r72.py` | `3060dcfe4f126d3eb6474a1f543bf415a3996065c410e9a898f70d22588c5175` |
| `tools/count-md-rows-r72.py` | `58f7397ea39186afc8f2e476391715d3d482c9c1139d72e44023364be845063c` |
| `tools/check-gate-standard-r79.py` (frozen checker, unchanged from freeze) | `0b32ddbcaf1fcab3721745ef9629d20ff1d249403d0d590655e537b2ad72cfda` |
| `tools/measure-unit-deps-r79.py` (frozen, unchanged) | `132be669e367670e8af15d8830443097c6c22f91ce36d1088e7282cf48882d1d` |
| `.ufo/waves/round-79/before/expected.json` | `0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21` |
| `.ufo/waves/round-79/before/src/systemd.unit.xml` | `eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6` |

## The five required reproductions

1. **Worktree `--root`** — `python3 tools/check-gate-standard-r79.py --root
   /home/vgpnk/Projects/shokunin/tsukuroi-shokunin` → **rc 0**,
   `duplicates=0 shape_ok=2/2 met=1` (this is the integrated worktree, both executors
   landed; the unedited worktree earlier read `duplicates=6 shape_ok=0/2` rc 1).
2. **Freeze before value** — `--revision afe1f261…` → **rc 1**,
   `duplicates=6 shape_ok=0/2 met=0 revision=afe1f261… branch=master`; the six rows are
   `check-r72-routed-r73`, `check-r75-routed-r76`, `check-selftest-tally`,
   `count-jd-rows-r76`, `count-ul-rows-r73`, `measure-journal-arithmetic-r77` — exactly the
   declared six. Base `9086589a…` reads the same six.
3. **Coverage at the freeze** — `python3 tools/check-registry-coverage.py --revision
   afe1f261…` → **rc 1, status FAIL**: two `REGISTRY-ROW-MISSING`
   (`tools/check-gate-standard-r79.py`, `tools/measure-unit-deps-r79.py`),
   `tools_total=119 rows_total=117 registered=117 missing=2`. Base `9086589a…` is PASS
   117/117; `--baseline-tools 9086589a…` names the same two files as the discovered
   newcomers. The freeze text's "must stay PASS" is therefore not what the bytes say
   (F3): coverage is *projected* PASS after the appended rows — 0 findings, 119/119, using
   the tool's own `_operative_rows`/`_coverage` over the worktree — and the revision-bound
   confirmation needs the L1 commit.
4. **Both new selftests** — `check-gate-standard-r79.py --selftest` rc 0,
   `SELFTEST total=8 passed=8 failed=0`; `measure-unit-deps-r79.py --selftest` rc 0,
   `SELFTEST total=32 passed=32 failed=0`. The two modes the repaired rows actually
   advertise were run too: `check-r71-routed-r72.py --selftest` rc 0,
   `SELFTEST: PASS (8 cases, 8 passed, 0 failed)`; `count-md-rows-r72.py --selftest`
   rc 0, `SELFTEST: PASS (23 cases, 23 passed, 0 failed)` (5 consecutive runs at the final
   digest). Harness refusals measured: both tools rc 2 `HARNESS-TMPDIR-REFUSED
   reason=tmpdir-unset` and `…reason=tmpdir-under-tmp`.
5. **SKILL.md inspection** — four `> NON-OPERATIVE — carried for history; the round-71
   table is the sole operative registry.` lines, each strictly adjacent (next line, no
   blank) under: Round 72 `selftest-tally` continuation, Round 73 continuation (one
   literal covers both of that section's tables), Round-76 continuation, round-77
   addition. Exactly two replaced lines (`check-r71-routed-r72`, `count-md-rows-r72`),
   and cell-wise comparison against the freeze shows **only cells 3 and 4** differ:
   self-test cell → the row's own `--selftest`; verdict map gains a standalone `3
   self-test failed`, with code 2 / code 128 text preserved. Exactly two rows appended
   inside the operative table (`measure-unit-deps-r79`, `check-gate-standard-r79`; gate;
   0/1/2/3). Historical preservation: the line-multiset diff against the freeze removes
   exactly the two old row lines and adds exactly 8 instances (2 replaced rows + 4 markers
   + 2 new rows); continuation tables are row-for-row identical; 6144 → 6150 lines;
   `check-line-endings-r64.py --check` PASS.

## Independent reimplementation (not trusting the reported numbers)

`ReviewRegistry/verify_registry.py` (scratch) re-implements the frozen clauses without
importing the lane counters. Before (freeze root): duplicates **6**, the same six paths,
operative rows 117, markers absent. After: duplicates **0**, operative rows **119**,
markers `OK` ×4, `selftest_has_own_tool`/`source_has_selftest` true for both rows, two new
rows complete, coverage-style recount 119/119 with no multi-covered path and no ambiguous
row. Black-box controls against the real counter: `good` rc 0 (0/2/1); `lying`,
`tool-without-selftest`, `verdict-no-3` each rc 1 shape 1/2; `unmarked` rc 1 duplicates 2;
two borrowed-selftest forgeries rc 1 (`duplicates=1 shape=2/2` and `shape=1/2`). The
counter's green is clause-sensitive, not vacuous.

## Findings (detail and evidence in `ReviewRegistry/findings.md`)

- **F1 (medium, instrument limit)** — the shape leg is presence-based: a tool whose
  `--selftest` exits 3 still yields `met=1` (fixture `red-selftest`: counter rc 0, shape
  2/2, stub rc 3). Declared boundary; the rows under review name green modes.
- **F1b (medium, instrument gap)** — the self-test cell is substring-checked only; a cell
  naming `tools/does-not-exist-r79.py --selftest` plus the row name still yields met=1
  (fixture `phantom-selftest`). Falsifies the item's "names a `--selftest` its tool does
  not contain is a finding" sentence. Live rows name their own real tools; coverage would
  flag the orphan, so the pair of gates catches it, the C2 counter alone does not.
- **F1c (low, fragility)** — an exact duplicate of a registry heading line earlier in the
  file makes `lines.index()` drop the real table and stop counting its duplicate
  (fixture `heading-collision`: met=1). No live instance: every registry heading in the
  delivered SKILL.md is unique as a full line.
- **F2 (low)** — the two replaced verdict cells describe code 2 as "argparse usage error"
  only, while the new `--selftest` mode also exits 2 on `HARNESS-TMPDIR-REFUSED`.
  Neighbouring rows state that second condition; these do not.
- **F3 (measurement discrepancy)** — freeze coverage is FAIL (two missing rows), not PASS;
  the appended rows are the repair; worktree projection 0 findings / 119 covered.
- **F4 (observation)** — one rc 3 `count-md-rows-r72.py --selftest` run during the
  integration window (tool file being rewritten, mtime 16:14:00; `map-digest` case red);
  5/5 green at the final digest `58f7397e…`. The executed bytes' digest was not captured;
  not certified as a defect and not smoothed away. It demonstrates the declared code-3
  mapping is real and is an instance of F1.
- **F5 (killed attacks)** — see the control table above; the only survivor is the
  presence-only `red-selftest`, by design.
- **F6 (low)** — the tool edits make `--revision` and `--fixture` mutually exclusive
  (freeze copy accepted both, rc 1; current rc 2 argparse error). Documented single-mode
  invocations unchanged; recorded as a tightening.
- **F7 (pass detail)** — no historical row removed, no duplicate tool path, both modes
  present and green, frozen checker bytes unchanged, line endings clean.

## Residual verification gaps

1. **Revision-bound after-state coverage/final gate were not run** — no integration commit
   existed during this seat (`HEAD 883aae61`). After the L1 commits, run
   `python3 tools/check-registry-coverage.py --revision <landed REV>` (expect PASS,
   `missing=0`, no findings) and `python3 tools/check-gate-standard-r79.py --revision
   <landed REV>` (expect `duplicates=0 shape_ok=2/2 met=1`, rc 0).
2. F4's transient red is not reconstructible; only the final digests are certified.
3. Attacked fixtures are synthetic stubs; they demonstrate clause reactions, not the real
   tools' hermeticity. The real selftests were run directly (above), and their harness
   refusals measured.

## Hygiene

No tool installed or updated; no pacman transaction; nothing written to `~/.local/bin`.
Only my wave-dir files were written: `ReviewRegistry.md`, `ReviewRegistry/findings.md`,
`ReviewRegistry/receipts.json`. Python bytecode caches under `tools/__pycache__` are
gitignored runtime byproducts of running/importing the lane tools (the directory already
held pre-round entries); no tracked file was touched. Scratch tree
`/fast/scratch/hyaku/tsukuroi-r79/ReviewRegistry/` is deleted; `TMPDIR` was always set
inside it, never `/tmp`. Git was read-only (`log`, `show`, `rev-parse`, `status`,
`diff`, `cat-file`); no commit/stage/stash/checkout/reset anywhere.

## Checks for the main agent

- `python3 tools/check-gate-standard-r79.py --root .` → rc 0, `duplicates=0 shape_ok=2/2` (observed here).
- `python3 tools/check-gate-standard-r79.py --revision <landed REV>` and
  `python3 tools/check-registry-coverage.py --revision <landed REV>` → rc 0 after the commit.
- `python3 tools/check-r71-routed-r72.py --selftest` → rc 0 (8/8);
  `python3 tools/count-md-rows-r72.py --selftest` → rc 0 (23/23), with `TMPDIR` set outside `/tmp`.
- If the record wants the F2 wording fixed, the owner is ExecRegistry next round — this seat
  did not edit `SKILL.md`.
