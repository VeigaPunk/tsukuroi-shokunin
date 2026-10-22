# RevScrubMutantsAdjacencyOverlap — attack on C2 fix in tools/mutants-adjacency-overlap.py

Verdict: holds. The C2 fix to tools/mutants-adjacency-overlap.py covers every git-bearing
subprocess, does not change observable behaviour, is not hollow, and the declared probe scores
0 of 3 pairs leaking with no harness errors.

## Findings

1. [obs] Diff scope. `git diff 8976ca92 29bf87fa -- tools/mutants-adjacency-overlap.py` touches
   only three things: the docstring contract sentence, `clean_env()` (adds `HOME` =
   `ROOT/home`, `XDG_CONFIG_HOME` = `$HOME/.config`, `PATH` = `/usr/bin:/bin`,
   `GIT_CEILING_DIRECTORIES` = `dirname(ROOT)`), and the unconditional `HOME = ROOT/'home'` +
   `os.mkdir(HOME)` right after `ROOT = tempfile.mkdtemp(...)` (lines 37-39 at tip). No logic,
   control-flow, or mutant changes. Full diff captured in this seat's sandbox work.

2. [obs] Call-site coverage (check 1). Every subprocess in the file runs with
   `env=clean_env()`: `_export()` lines 56-57 (`git -C <lane> rev-parse`), 58-59
   (`git -C <lane> archive`), 67-68 (`git -C <lane> show`); helper `sh()` line 80 is the sole
   path for `g()` (all sandbox `init/add/commit/checkout/clean/rev-parse` at lines 93-95, 97,
   106-107, 117-119, 399), `m_other_real_mori_file` line 220 (`git -C <mori> cat-file`), and
   the counter child at line 122 (`python3 TOOL --repo SBX ...`). `grep -nE 'subprocess\.|
   os\.system|Popen|check_output|check_call|spawn|execv|os\.exec' tools/mutants-adjacency-
   overlap.py` on the tip checkout returns no other exec site; no `shell=True`. The python
   child counter `tools/check-adjacency-overlap.py` additionally applies its own `git_env()`
   (lines 75, 92-95) on top of the inherited clean env, so no grandchild escape. No call site
   escaped the contract.

3. [obs] Channel coverage, by construction. path-wrapper: `PATH='/usr/bin:/bin'` in
   `clean_env` means tool git calls and the `python3` child lookup bypass any wrapper.
   user-files: `GIT_CONFIG_NOSYSTEM=1` + `GIT_CONFIG_GLOBAL=/dev/null` +
   `GIT_CONFIG_SYSTEM=/dev/null` already neutralised per-user config in v1; the new private
   `HOME`/`XDG_CONFIG_HOME` also defeats default `~/.config/git/ignore` and `attributes`
   paths (children never see the canary HOME). enclosing-repo: `TMPDIR` under the canary puts
   `ROOT` inside the canary worktree; `GIT_CEILING_DIRECTORIES=dirname(ROOT)` blocks repo
   discovery upward from any temp path under `ROOT`, and every git invocation is `-C`-pinned
   to SBX/MORI/the lane anyway, so nothing enumerates the canary `.git` or index.

4. [obs] Behaviour unchanged (check 2). Ran the probe's argv shape
   (`--base <rev> --counter-rev <rev> --lane <clone>`) with `<rev>` = 29bf87fa… against the
   tip clone, once with the tool bytes at 8976ca92 (oldrepo checkout) and once at 29bf87fa…:
   both exit 0, 34 stdout lines each, and `diff` after normalising `/tmp/mut-adj-*` and
   40-hex ids is empty (in fact the raw outputs were byte-identical — every 40-hex field is a
   lane-side input rev or blob digest, not a sandbox commit id). Summary both runs:
   `should_fail_total 24, should_fail_accepted 0, should_pass_accepted 4,
   control_live_anchored_rows 6, counter_sha256 26cc77ea…`. Recorded outputs:
   /fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsAdjacencyOverlap/{out-old,out-new}.txt.

5. [obs] Not hollow (check 3). All 33 MUTANTS entries execute unconditionally — the stdout
   record count (33 mutant JSON lines + summary = 34) proves the full battery ran in both
   revisions. `os.mkdir(HOME)` is unconditional; there is no branch on HOME contents or oddity,
   no early return, no try/except around subprocess errors: `_export` uses `check=True`, `g()`
   raises `SystemExit` on non-zero rc, and `run()`'s `except Exception` only converts a
   counter crash into `accepted=False` — the conservative direction (a miss stays loud).
   `accepted` still requires `exit==0 and anchored_rows==6`, so passing the probe requires the
   real work to keep succeeding.

6. [obs] Probe run (check 4).
   `python3 tools/probe-git-env-residual-r30.py --revision 29bf87fa3971df04cb96e4ad9a28805d8154ed2f --lane /fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsAdjacencyOverlap/repo --only tools/mutants-adjacency-overlap.py`
   output, all three pairs `"leak": false`, `channel_rc` = `control_rc` = 0, `evidence: []`;
   summary:
   `{"revision": "29bf87fa…", "targets": 1, "channels": ["path-wrapper", "user-files", "enclosing-repo"], "pairs": 3, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c", ...}`
   probe_sha256 matches the declared unchanged probe (c8f61996…), exit 0.

7. [obs] Pre-existing (unchanged) quirk, out of scope for C2: `should_pass_accepted` is 4 of
   6 should-pass mutants at BOTH revisions — identical counts, so the C2 fix neither helped
   nor regressed it; it is a counter-strictness question about check-adjacency-overlap.py,
   not this file's env fix. [unk] Whether 4/6 is the round-28 intended value for the counter;
   the battery's own semantics (accepted = counter verdict) make non-accepted should-pass
   mutants a counter problem, not an env-leak problem.

## Residual risk

- [inf] `GIT_CEILING_DIRECTORIES` protects only the subtree of `dirname(ROOT)`; a git run
  with `cwd` inside the canary and no `-C` would still discover the canary repo. No such
  call exists (all git is `-C`-pinned; the python child also self-protects), and the probe's
  enclosing-repo channel shows no leak, so this is a latent-not-live gap.
- [inf] The probe's leak oracle is canary side-effects plus exit-code equality; stdout drift
  under attack is not judged. Finding 4's identical-behaviour result plus `evidence: []`
  covers the practical risk.

Scope: read=SCORECARD.md declaration, tools/mutants-adjacency-overlap.py at both revisions,
tools/probe-git-env-residual-r30.py, tools/check-adjacency-overlap.py grep;
wrote=.ufo/waves/round-30/w2/RevScrubMutantsAdjacencyOverlap.md, scratch artifacts under
/fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsAdjacencyOverlap/ (sandbox clones, out-*.txt);
executed=git clone/checkout/diff/grep (read-only on lane), two battery runs at each revision
(byte-identical outputs, exit 0), probe --only run (0 of 3 leaking, exit 0)
Model: devin/swe-2
Installs: none
