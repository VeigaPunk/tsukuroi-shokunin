# ExecReplicate — clean-room replication of the C1 counting command (round 86, w1)

Lane revision measured: `1e1caabcdd740a6429dd31d7aba3b725ff8c677d` (`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`),
which is the entry commit named in the seat spec. Clean room: `git clone --shared` of the lane into
`/fast/scratch/hyaku/tsukuroi-r86/ExecReplicate/lane`; nothing under the lane repo was modified
(`git status --porcelain` empty after the clone, controls only read).

All receipts: `ExecReplicate/` beside this file. Base: host `7.2.11-arch1-1`, `Python 3.14.8`.

## Verdict

C1 reproduced: **30/30 families in each of three consecutive runs, rc 0, `verdict: met`**, with the
frozen instrument bytes, and every freeze control reproduced from `controls-summary.txt` to the family.
No defect found; two operability observations below, neither touching the frozen counting command.

## 1. Instrument identity (freeze check)

`ExecReplicate/freeze-check.txt`:

```
a49a18aa21322579f723cbddd38f0fcdff686cde85f525a9a81976ef176fbc21  tools/resume-gate-battery-r86.py
8123d033c0ccf8e3c6bdbdd1f1bb392125d661084731a324794501239ea3f024  tools/check-hibernate-resume.py
496156f6bb6560f8bfac23f16bb72efcd9ca052a3c40b198125423c4469a79cc  .ufo/waves/round-85/before/host/facts-v2.json
# manifest expectation
a49a18aa21322579f723cbddd38f0fcdff686cde85f525a9a81976ef176fbc21  ../../../../tools/resume-gate-battery-r86.py
```

Battery sha256 equals the freeze-manifest entry in `.ufo/waves/round-86/before/freeze-manifest.sha256:44`
— so the void rule ("void if the battery bytes differ from the freeze manifest") does not fire.
Gate at the measured tip is byte-identical to the gate at the candidate commit
`dc8849494cefe92c4a562de07fee667c4ec0bcc8` (`git diff --stat dc88494 1e1caab -- tools/` empty), so
"30/30 at the landed tip" and "30/30 of the candidate" are the same instrument.

K1 provenance re-checked from the repo, not from the receipt text: the pre-round tip
`3f56789829b84a97b2a8aa786618022195ef53cb:tools/check-hibernate-resume.py` is byte-identical to
`controls/K1-r85-gate-do-nothing.py` (`diff` → `IDENTICAL`) and hashes `88041b75…483e7`, the manifest value.

## 2. C1 counting command, three consecutive runs (the counted evidence)

cwd = clone root. Verbatim (`ExecReplicate/c1-runs-stdout.txt`, exit code 0 each):

```
### run1: python3 tools/resume-gate-battery-r86.py --gate tools/check-hibernate-resume.py --out run1.json
{"bases": ["host", "random0", "random1", "random2", "random3", "random4"], "cases": 231, "failed_families": [], "families_passed": 30, "families_total": 30, "order_head": ["POSITIVE", "PREC-NO-RESUME-ARG", "EMPTY-RESUME", "NORESUME-VALUED", "MULTI-SWAP"], "target": 30, "verdict": "met"}
exit=0
run1 wall=7.95s rc=0

### run2: python3 tools/resume-gate-battery-r86.py --gate tools/check-hibernate-resume.py --out run2.json
{"bases": ["host", "random0", "random1", "random2", "random3", "random4"], "cases": 231, "failed_families": [], "families_passed": 30, "families_total": 30, "order_head": ["OFFSET-SSCANF", "MALFORMED", "HR-SWAP-TOO-SMALL", "HR-NO-RESUME-ARG", "OFFSET-DUP"], "target": 30, "verdict": "met"}
exit=0
run2 wall=9.45s rc=0

### run3: python3 tools/resume-gate-battery-r86.py --gate tools/check-hibernate-resume.py --out run3.json
{"bases": ["host", "random0", "random1", "random2", "random3", "random4"], "cases": 231, "failed_families": [], "families_passed": 30, "families_total": 30, "order_head": ["HR-OFFSET-MISMATCH", "HR-OFFSET-MISMATCH", "MULTI-FAULT", "HR-LOCKDOWN-BLOCKS", "OFFSET-SSCANF"], "target": 30, "verdict": "met"}
exit=0
run3 wall=8.61s rc=0
```

Per-run: **families_passed 30, 30, 30 of 30** (`failed_families: []`), cases 231 each
(6 bases × 30 families, r86 family case counts as declared: NORESUME-VALUED 1, NOHIB-VALUED 1,
EMPTY-RESUME 1, OFFSET-DUP 2, OFFSET-SSCANF 3, HIBERNATE-NOX 3, SWAP-BOUNDARY 2, MULTI-SWAP 2,
BOOL-FOR-INT 1, DECOYS-R86 1 per base → observed 6 cases for the 1-case families, 15 for
OFFSET-SSCANF, matching the docstring).
`order_head` differs on every run, so the shuffle is live and no position counter can answer.
Full `case_log` (with per-case `got`/`want`/`why`) retained as `run1.json`–`run3.json`; each run is
a different OS-entropy case order and different random bases.

## 3. Controls, replayed once each (K1 + N01-N12) and `--selftest`

`ExecReplicate/verdicts.txt` (first replay) — every line equals `before/controls/controls-summary.txt`
to the failing family:

```
ctl-K1-r85-gate-do-nothing.json	passed=26/30	cases=231	failed=EMPTY-RESUME,NOHIB-VALUED,NORESUME-VALUED,OFFSET-SSCANF
ctl-N01-noresume-exact.json	passed=29/30	cases=231	failed=NORESUME-VALUED
ctl-N02-nohib-exact.json	passed=29/30	cases=231	failed=NOHIB-VALUED
ctl-N03-empty-resume.json	passed=29/30	cases=231	failed=EMPTY-RESUME
ctl-N04-first-offset.json	passed=29/30	cases=231	failed=OFFSET-DUP
ctl-N05-offset-malformed.json	passed=29/30	cases=231	failed=OFFSET-SSCANF
ctl-N06-no-dash.json	passed=29/30	cases=231	failed=OFFSET-SSCANF
ctl-N07-hib-literal.json	passed=29/30	cases=231	failed=HIBERNATE-NOX
ctl-N08-boundary-le.json	passed=29/30	cases=231	failed=SWAP-BOUNDARY
ctl-N09-first-swap.json	passed=29/30	cases=231	failed=MULTI-SWAP
ctl-N10-no-bool-guard.json	passed=29/30	cases=231	failed=BOOL-FOR-INT
ctl-N11-substring.json	passed=28/30	cases=231	failed=DECOYS-R86,PREC-DECOYS
ctl-N12-short-prefix.json	passed=26/30	cases=231	failed=DECOYS-R86,EMPTY-RESUME,HR-NO-RESUME-ARG,PREC-NO-RESUME-ARG
run1.json	passed=30/30	cases=231	failed=-
run2.json	passed=30/30	cases=231	failed=-
run3.json	passed=30/30	cases=231	failed=-
```

A second independent replay of all 13 controls (fresh shuffle, fresh random bases) reproduced every
count and every failing-family set exactly — K1 26 / `EMPTY-RESUME,NOHIB-VALUED,NORESUME-VALUED,OFFSET-SSCANF`;
N01-N10 29 each on the same single family; N11 28 / `DECOYS-R86,PREC-DECOYS`; N12 26 /
`DECOYS-R86,EMPTY-RESUME,HR-NO-RESUME-ARG,PREC-NO-RESUME-ARG`. Verbatim both replays:
`ExecReplicate/controls-stdout.txt` (replay 2) and the JSONs `control-*.json` (replay 1, `case_log` dropped).

The 13 control files were hashed against the freeze manifest before use: K1 `88041b75…`,
N01 `61d2543c…`, N02 `6873a661…`, N03 `ee5168ce…`, N04 `d8dcf5d9…`, N05 `92cfb327…`, N06 `edf04119…`,
N07 `7302e816…`, N08 `fa26ba65…`, N09 `8afe4d25…`, N10 `53a8f409…`, N11 `f285cac9…`, N12 `87fc75e0…`
— all match `.ufo/waves/round-86/before/freeze-manifest.sha256`.
Best control is 29/30 (near-miss) and 26/30 (K1), so the gate's 30/30 is separated from every control
by at least one family, i.e. the discrimination declared at the freeze is reproduced from a clean clone.

`--selftest` (from the clone root), verbatim (`ExecReplicate/selftest.txt`):

```
{"case": "absent", "missing_failures": [], "pass": true, "rc": 1, "want_rc": 1}
{"case": "const-healthy", "missing_failures": [], "pass": true, "rc": 1, "want_rc": 1}
{"case": "not-json", "missing_failures": [], "pass": true, "rc": 1, "want_rc": 1}
{"case": "base-unreadable", "pass": true, "rc": 2, "want_rc": 2}
{"failed": [], "selftest": "PASS"}
selftest_exit=0
```

## 4. Independent checks beyond the counted command

(a) **Expectations vs the frozen rule set, not vs the gate.** I re-implemented the frozen rule set from
the battery docstring alone — `parameqn` prefix match with `-`/`_` equal, A1/A2/A3, `r` = rest of the
last `resume=` (rule 1 on `None` or `""`), `o` = leading decimal digits of the last `resume_offset=`
whose rest starts with a digit (skipped otherwise), rules 2-8, CANNOT-EVALUATE types — as
`ExecReplicate/independent-oracle.py`. Replaying it over each run's `case_log`:
`cases=231 disagreements=0` for run1, run2 and run3 (`freeze-check.txt`). So the battery's `want`
vectors follow the docstring, and a 30/30 is not the battery grading its own gate's output.

(b) **Gate vs the independent oracle, battery harness bypassed.** Every `case_log` entry of the three
runs (693 cases) was written to a fresh facts file and fed straight to
`python3 tools/check-hibernate-resume.py --facts FILE` (`ExecReplicate/direct-gate-replay.txt`):

```
gate invocations=693 disagreements_vs_oracle=0 max_single_call_wall=0.059s
```

The 20 s per-case budget in the predicate is not close: slowest single call 0.137 s across a first
pass and 0.059 s in the receipted pass.

(c) **Honest failure on a non-lane cwd.** Running the battery from outside the lane root with absolute
paths gives `{"verdict": "cannot-evaluate", "reason": "base-unreadable:FileNotFoundError"}`, exit 2 —
the host base is a lane-relative constant (`BASE = ".ufo/waves/round-85/before/host/facts-v2.json"`).
This is fail-closed and cannot silently score a lucky 30/30; the frozen counting command fixes cwd to
the lane root, so this is an observation, **not** a defect against C1. If the L1 wants a
cwd-independent probe, the one-line patch is to resolve `BASE` against the script directory:
`BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".ufo/waves/round-85/before/host/facts-v2.json")`.

## 5. Refused / not done

- No lane file edited, nothing committed, no `git`/`jj` mutation in the lane; the clone was the only
  write, plus this seat's wave dir.
- Host read-only throughout: no hibernate/procfs/sysctl/boot action; no pacman (guard respected);
  no tool installs, so no tooling record to add.
- Not measured (out of this seat): the C2 entry (BP1-BP8) — that is the hyaku closure's row, not a
  counting replication; and the r85-carried forgers/mutants set, which the seat spec did not name.
- Scratch `/fast/scratch/hyaku/tsukuroi-r86/ExecReplicate` removed after receipts were copied;
  free space before removal was ample (`/fast` 49 % used, 417 G free).
