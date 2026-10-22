# RevScrubMutantsOwedStatementsr29 — wave-2 falsification of the C2 fix in tools/mutants-owed-statements-r29.py

**Verdict: holds.** The env-contract change in `tools/mutants-owed-statements-r29.py` covers every
subprocess call site, does not change observable behaviour, is not hollow, and the declared probe
reports 0 of 3 leaking pairs for this tool.

## 1. GIT CHILD ENV CONTRACT coverage [obs]

The diff (`git diff 8976ca92 29bf87fa -- tools/mutants-owed-statements-r29.py`, 10 insertions / 1
deletion) adds only a docstring paragraph and, at lines 42–48 of
`/fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsOwedStatementsr29/repo/tools/mutants-owed-statements-r29.py`,
a private `HOME` under `SEAT` plus `ENV.update` setting `GIT_CONFIG_NOSYSTEM=1`,
`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `HOME`, `XDG_CONFIG_HOME`,
`PATH=/usr/bin:/bin`, `GIT_CEILING_DIRECTORIES=os.path.dirname(SEAT)`. `ENV` already strips every
inherited `GIT_*` at line 36.

All subprocess call sites (grep for `subprocess|Popen|os.system|os.exec|os.popen|os.spawn|
check_output|run(`) — lines 49 (`git clone`), 50–51 (`git rev-parse`), 55–56 (`git show` for the
counter blob), 63–64 (the `git()` helper used for checkout/commit/rev-parse) and 76–77 (the counter
python child) — pass `env=ENV`. No call site escapes.

The only python child is `check-owed-statements-r29.py`, which was not changed in a3f1937. Its own
`git()` wrapper (lines 139–140) uses its own `clean_env()` (lines 133–135) that re-strips `GIT_*` and
adds `GIT_OPTIONAL_LOCKS`/`LC_ALL`; HOME and PATH propagate from the parent's sanitized ENV. All of
its git invocations are read-only `git -C <lane>` (`show` line 144, `rev-parse` line 374) against the
sandbox clone, so repository discovery never walks upward. [inf] The counter re-strips
`GIT_CEILING_DIRECTORIES`, but that is harmless because every counter git call lands directly on a
repo root via `-C`.

## 2. Behaviour unchanged [obs]

Ran the probe's mode for this tool (`--base 81a061a67466c5e1be812814a895a4b5ed89b4ff --counter-rev
29bf87fa… --lane <sandbox>`; `81a061a` is an ancestor of both compared revisions, verified via
`merge-base --is-ancestor`):

- old tool (blob `8976ca92:tools/mutants-owed-statements-r29.py`): exit 0, 38 stdout lines, empty stderr
- new tool (tip blob): exit 0, 38 stdout lines, empty stderr

After normalising `mut-owed-*` temp names and 40-hex ids, **zero differing lines**. Identical summary:
`control_marked: 12`, `should_fail_total: 29`, `should_fail_accepted: 0`, `should_pass_total: 7`,
`should_pass_refused: 0`, `crashes: []`, `counter_sha256: 3516d57911f2af…461a2d`. Outputs saved at
`/fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsOwedStatementsr29/{old,new}-run.{out,err}`.

## 3. Fix is not hollow [obs]

The diff is purely additive env setup plus docstring; no control flow changed. `git()` still raises
`SystemExit` on any nonzero rc (lines 65–66); the three setup calls keep `check=True` (lines 49–56);
exit 0 still requires `control_marked == 12`, zero accepted should-fails and zero crashes (line 335).
No early return keyed on `HOME`, no exit-code swallowing. The private HOME lives inside `SEAT`, so the
existing `atexit` cleanup removes it.

## 4. Probe run [obs]

`python3 tools/probe-git-env-residual-r30.py --revision 29bf87fa… --lane …/repo --only
tools/mutants-owed-statements-r29.py` → exit 0:

- path-wrapper: control_rc 0, channel_rc 0, evidence [], leak false
- user-files: control_rc 0, channel_rc 0, evidence [], leak false
- enclosing-repo: control_rc 0, channel_rc 0, evidence [], leak false
- summary: `{"targets": 1, "pairs": 3, "leaking": 0, "leaking_pairs": [], "harness_errors": [],
  "probe_sha256": "c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c",
  "revision": "29bf87fa3971df04cb96e4ad9a28805d8154ed2f"}` — probe sha matches the declared bytes.

## Residual risk / gaps

- `GIT_CEILING_DIRECTORIES=dirname(SEAT)` is defence-in-depth only: every git call already pins a
  repo via `-C`/`clone`, and `SEAT` is created under `/fast/scratch/hyaku` (explicit `dir=`), immune
  to a canary `TMPDIR`. [inf]
- The counter child's env is one indirection removed (parent ENV → counter clean_env); no channel
  reaches it because it only reads `-C REPO`. [inf]
- No actionable finding.

Scope: read=tools/mutants-owed-statements-r29.py@{8976ca92,29bf87fa}, tools/check-owed-statements-r29.py, tools/probe-git-env-residual-r30.py, diff 8976ca92..29bf87fa; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevScrubMutantsOwedStatementsr29.md plus sandbox files under /fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsOwedStatementsr29/; executed=git clone/checkout/show/merge-base (read-only), two mutants-tool runs, one probe run
Model: devin/swe-2
Installs: none
