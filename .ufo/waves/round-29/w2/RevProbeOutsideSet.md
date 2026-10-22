# RevProbeOutsideSet — git-env leak probe of tools OUTSIDE the C2 frozen eight

Verdict: none of the twelve git-writing lane tools outside C2's frozen eight leaks inherited GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE at 10d5288fc1051364e711203855e7c53710dfcc21 — all pass --selftest identically under the canary env and every canary fingerprint is unchanged.

## Method

Mirrors tools/probe-git-env-leak.py's contract exactly: for each tool, CONTROL run `python3 tools/<tool>.py --selftest` with every GIT_* removed (plus GIT_CONFIG_NOSYSTEM=1, LC_ALL=C), then CANARY run with GIT_DIR=<canary>/.git, GIT_WORK_TREE=<canary>, GIT_INDEX_FILE=<canary>/.git/index pointed at a fresh one-commit canary under /fast/scratch/hyaku/tsukuroi-r29/RevProbeOutsideSet/runs/. Verdict rule identical: leak iff canary fingerprint changed or canary_rc != control_rc; a failed control is a harness error. One widening vs the probe: my fingerprint hashes every file under the canary directory (covers .git/config, logs/, hooks/, COMMIT_EDITMSG, ORIG_HEAD and worktree files — the blind spots named in RevProbeDesign finding 3). Runs used a --no-local clone of the lane checked out at the tip, executed from the clone root (the natural `cwd=tree` equivalent); 12 runs in parallel via ThreadPoolExecutor, 300 s timeout each (263 s wall).

## Findings

1. **All twelve targets clean; 0 of 12 leak, 0 harness errors.** Per-tool results (control_rc == canary_rc == 0, canary_changed false, selftest PASS each time): check-adjacency-anchors (25 cases), check-boot-chain (83), check-boot-writers (12), check-recheck-commands (95), check-revision-binding (78), check-root-dac-correction (54), check-seat-scope (54), check-section-citations (68), check-self-assessment (fixture JSON, all PASS), check-source-scope-correction (29), measure-update-recheck (20), _revision (57). Full JSONL: /fast/scratch/hyaku/tsukuroi-r29/RevProbeOutsideSet/runs/outside-probe.jsonl; harness: /fast/scratch/hyaku/tsukuroi-r29/RevProbeOutsideSet/probe_outside.py.

2. **[obs] Source review corroborates the runs.** Every tool routes git through a scrubbed env: check-adjacency-anchors.py:264/459/933 (clean_env), check-boot-chain.py:802-807, check-boot-writers.py:98/604, check-recheck-commands.py:799-805, check-revision-binding.py:104-115/186/226/369/415, check-root-dac-correction.py:247/_revision.clean_env() at :461, check-seat-scope.py:174-179, check-section-citations.py:406-410/568-575, check-source-scope-correction.py:355-359, measure-update-recheck.py:438-442/485-489, _revision.py:63-73/91/213/220/394. None uses os.system, Popen, or shell=True (grep over all twelve files: no hits).

3. **[obs] The wave-1 check-self-assessment fix is real at tip.** RevProbeDesign finding 2 found build_fixture's `git init -q repo` at line 975 with no env= at the base; at tip check-self-assessment.py:999-1010 passes `env=git_env()` to init, add and commit (fc07fec "C2 GIT_* scrub"), and the canary run confirms: exit 0, canary unchanged. This was the only demonstrated real leak outside the frozen list and it is now closed. [inf] Its omission from TARGETS means the C2 counter did not measure this fix; my run is the disclosure, not the claim.

4. **[unk, pre-existing] check-revision-binding.py's stub-tool helper `git()` at :1020 calls `git -C ROOT` with inherited env — but it is the source for stub tools written into selftest sandboxes, not invoked during --selftest with GIT_DIR set (canary run passed). If a future code path runs it under a polluted env it would follow GIT_DIR; out of current scope.

5. **[inf] Method symmetry note:** the frozen probe runs tools from a `git archive` export; I ran from a clone (assignment: "from a sandbox clone"). A clone keeps .git present, which can only make GIT_DIR-following more observable, not less — the clean result is conservative.

## Residual risk

- The same two detection gaps RevProbeDesign named apply here: an env-following `git init` onto an existing canary may leave the fingerprint unchanged (git init in-place writes config only — which my wider fingerprint DOES catch, unlike the frozen probe), and pure GIT_DIR-following reads that don't change exit code are invisible.
- One canary run per tool per code path exercised by --selftest; paths the selftest does not reach are unmeasured.

Scope: read=probe source, RevProbeDesign report, SCORECARD round-29 declaration, git-call sites in all 12 tools; wrote=.ufo/waves/round-29/w2/RevProbeOutsideSet.md, /fast/scratch/hyaku/tsukuroi-r29/RevProbeOutsideSet/{repo/,probe_outside.py,runs/}; executed=sandbox clone+checkout at 10d5288f, 24 --selftest runs (12 control + 12 canary) under env-scrubbed python3, read-only git log/grep in clone
Model: devin/swe-2
Installs: none
