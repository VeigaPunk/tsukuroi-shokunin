# ExecSelftests — routed defect 1 (Gate standard Self-test)

Lane revision measured: `1e1caabcdd740a6429dd31d7aba3b725ff8c677d` (`git -C …/tsukuroi-shokunin rev-parse master`).
No lane file was edited: `git status --porcelain -- tools` is empty; the only new path is
`.ufo/waves/round-86/w1/`. Everything below is a proposal for the L1.

## Delivered

| path (under `.ufo/waves/round-86/w1/ExecSelftests/`) | what |
|---|---|
| `check-nonauthor-label-r85.py` | `tools/check-nonauthor-label-r85.py` + `--selftest` (8 cases, self-written fixtures) |
| `check-nonauthor-label-r85.patch` | unified diff of the above vs the lane file |
| `resume-gate-battery-r86-selftest.patch` | proposed fix for defects D1+D2 in `tools/resume-gate-battery-r86.py` |
| `resume-gate-battery-r86-fixed.py` | the patched battery, measured (not for landing as a new file) |
| `mutants/` (10 files) | one-line mutants, each marked `# MUTANT` |
| `MUTANTS.md` | mutant → base → one-line change → selftest rc |
| `receipts/` (18 files) | verbatim stdout/stderr of every run, `rc=` appended |

## Check 1 — `check-nonauthor-label-r85.py --selftest` (new mode)

Self-invocation over fixtures it writes under `tempfile.mkdtemp()`: a two-seat census
(`ReviewEntry`, `ExecSelftests`), a red file with two labeled lines (2, 6) plus one decoy
and two exempt lines, a green file, three broken results files, an unreadable FILE and two
malformed CLIs. Each case asserts rc, `status`, finding `id`s, `site`s (`PATH:LINE`) and the
counts (`seat_count`, `file_count`, `finding_count`, `clean_count`).

```
{"case": "red-and-green", "mismatched": [], "pass": true, "rc": 1, "want_rc": 1}
{"case": "green-only", "mismatched": [], "pass": true, "rc": 0, "want_rc": 0}
{"case": "results-unreadable", "mismatched": [], "pass": true, "rc": 2, "want_rc": 2}
{"case": "results-malformed", "mismatched": [], "pass": true, "rc": 2, "want_rc": 2}
{"case": "results-empty", "mismatched": [], "pass": true, "rc": 2, "want_rc": 2}
{"case": "file-unreadable", "mismatched": [], "pass": true, "rc": 2, "want_rc": 2}
{"case": "cli-no-files", "mismatched": [], "pass": true, "rc": 2, "want_rc": 2}
{"case": "cli-selftest-with-files", "mismatched": [], "pass": true, "rc": 2, "want_rc": 2}
{"cases": 8, "failed": [], "selftest": "PASS"}
rc=0
```
(`receipts/01-nonauthor-patched-selftest.txt`; the shipped copy re-run from `/tmp` is
`receipts/14`, also rc 0.)

Equivalence with the lane gate on a normal invocation is byte-identical:
`receipts/13-nonauthor-normal-invocation.diff` is empty (`diff` rc 0) for
`--results eq/results.json eq/doc.md` (rc 1, one `NONAUTHOR-SEAT-LABEL` at `…/doc.md:2`).
Malformed CLI keeps rc 2, `id: E-CLI`, `site: argv`, `status: CANNOT_EVALUATE`; only the
detail text changed (`the following arguments are required: FILE` →
`--results and at least one FILE are required`), because `--results`/`files` can no longer
be argparse-required once `--selftest` takes no positional.

It can fail — three one-line mutants, each caught by a different assertion axis
(`receipts/02-nonauthor-mut{1,2,3}-selftest.txt`):

```
mut1 (exemptions disabled)   rc=1  failed: ["red-and-green", "green-only"]
mut2 (site loses :line)      rc=1  failed: ["red-and-green"]  mismatched: ["sites"]
mut3 (empty census passes)   rc=1  failed: ["results-empty"]  rc 0 vs want 2
```

## Check 2 — `tools/check-hibernate-resume.py --selftest`

```
{"cases": 13, "failed": [], "selftest": "PASS"}
rc=0
```
(`receipts/03-hibernate-lane-selftest.txt`.) It already has a positive control
(`SELFTEST_CASES` line 221, case `positive` → rc 0, no findings), so it is not exposed to
D2. Three rule mutants all make it exit non-zero:
`mut1` parameqn→exact match rc 1 (10/13 cases fail), `mut2` `noresume=<value>` ignored
rc 1 (`noresume-valued`), `mut3` first-token-wins rc 1 (`empty-resume-last`)
(`receipts/04-hibernate-mut{1,2,3}-selftest.txt`).

## Check 3 — `tools/resume-gate-battery-r86.py --selftest`

From the lane root: `{"failed": [], "selftest": "PASS"}` rc 0 (`receipts/05`).
Three mutants fail it: family expectation flipped rc 1 (`const-healthy`, missing
`NORESUME-VALUED`), findings comparison dropped rc 1 (26 missing families), base-unreadable
rc 1 instead of 2 (`receipts/06-battery-mut{1,2,3}-selftest-cwd-lane.txt`).

**Two defects, both operability, both in the selftest itself:**

- **D1 — `--selftest` is cwd-dependent and crashes outside the lane root.**
  `tools/resume-gate-battery-r86.py:105` `BASE = ".ufo/waves/round-85/before/host/facts-v2.json"`
  is relative, and `selftest()` line 448 calls `main([...])` without `--base`, so every case
  inherits it. Run from `/tmp`:
  ```
  File "…/resume-gate-battery-r86.py", line 455, in selftest
      with open(out, encoding="utf-8") as fh:
  FileNotFoundError: [Errno 2] No such file or directory: '…/battery-r86-selftest-…/absent.json'
  rc=1
  ```
  (`receipts/08-battery-lane-selftest-cwd-tmp.txt`.) The `--out` file is never written
  because `main` returned 2 on the unreadable base, before the selftest can judge anything.
- **D2 — no positive control: a battery that never reports `met` passes its own selftest.**
  `SELFTEST_GATES` (line 434) expects rc 1 for all three gates and 2 for base-unreadable;
  no case expects rc 0. Proof: `mutants/battery-r86-mut4-never-met.py` (`return 0 if
  summary["verdict"] == "met" else 1` → `return 1`) gives
  `{"failed": [], "selftest": "PASS"}` rc 0 (`receipts/06-battery-mut4-selftest-cwd-lane.txt`).
  The battery would then report `unmet` on a correct gate and its own selftest would agree.

Proposed patch `resume-gate-battery-r86-selftest.patch` (29 lines): anchor `BASE` to the
repo root via `__file__`, and add a `positive-control` case that runs the battery against
the real `check-hibernate-resume.py` beside it, expecting rc 0, `verdict: met`, no failed
families. Measured on `resume-gate-battery-r86-fixed.py` from `/tmp`:
```
{"case": "positive-control", "pass": true, "rc": 0, "verdict": "met", "want_rc": 0}
{"failed": [], "selftest": "PASS"}                      rc=0   (receipts/09)
{"case": "positive-control", "pass": false, "rc": 1, "verdict": "met", "want_rc": 0}
{"failed": ["positive-control"], "selftest": "FAIL"}    rc=1   (receipts/10, fix + mut4)
```

## C1 corroboration (not my claim to adjudicate)

At the measured tip, `python3 tools/resume-gate-battery-r86.py --gate
tools/check-hibernate-resume.py` reports
`{"cases": 231, "failed_families": [], "families_passed": 30, "families_total": 30,
"target": 30, "verdict": "met"}` rc 0 (`receipts/07-battery-c1-real-gate.txt`, full case log
in `07-battery-c1-real-gate.full.json`). One run only; the three-consecutive-run target is
the C1 seat's measurement.

## Risks / notes

- The battery patch adds one full battery run (≈5–7 s) to `--selftest` and makes the
  selftest fail if `check-hibernate-resume.py` is not beside the battery — intended, but it
  couples the two files.
- The nonauthor patch relaxes argparse `required`; the explicit guard preserves rc 2,
  `E-CLI`, `site: argv` (verified above). If the L1 wants the old detail string, keep
  `required=True` on `--results` and add `--selftest` via a pre-parse `sys.argv` check.
- No tool was installed or upgraded; no host state touched; lane index untouched.
- Scratch `/fast/scratch/hyaku/tsukuroi-r86/ExecSelftests` removed after copying receipts.
