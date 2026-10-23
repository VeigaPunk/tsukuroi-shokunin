# Round 31 wave 2 — RevScrubMutantsAdjacency (falsify)

Verdict: holds. The C2 fix in tools/mutants-adjacency-overlap.py drops GIT_/LD_/PYTHON names at every git spawn site while keeping the round-30 contract; the frozen probe reports leaking 0 of 3 pairs, and the tool's observable behavior is unchanged between 8cff9e7c and f3a5723a.

## Findings

1. [obs] Every subprocess spawn site uses clean_env() and drops GIT_/LD_/PYTHON names. The tool has exactly four subprocess.run sites, all passing env=clean_env(): tools/mutants-adjacency-overlap.py:56 (rev-parse), :58 (archive), :67 (show), :80 (sh(); all g() git calls route through sh()). No other spawn mechanism exists (grep for Popen/check_call/check_output/os.system/os.popen: only the four subprocess.run sites). Evidence: `grep -n "subprocess\.\|os\.system\|os\.popen\|Popen\|run(\|check_call\|check_output" tools/mutants-adjacency-overlap.py` → lines 56, 58, 67, 80; no site lacks clean_env().

2. [obs] clean_env() keeps the round-30 contract. After filtering GIT_/LD_/PYTHON prefixes, it sets GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_SYSTEM=/dev/null, HOME=<private mkdtemp home>, XDG_CONFIG_HOME, PATH=/usr/bin:/bin, and GIT_CEILING_DIRECTORIES (tools/mutants-adjacency-overlap.py:18-25). This matches the probe's CONTRACT tuple plus GIT_CEILING_DIRECTORIES (tools/probe-git-child-env-r31.py:83-84, 321-323). The diff 8cff9e7c..f3a5723a changes only line 19 (startswith('GIT_') → startswith(('GIT_','LD_','PYTHON'))).

3. [obs] Frozen probe at f3a5723a passes. Command: `python3 tools/probe-git-child-env-r31.py --revision f3a5723a988bf1c2835985880e7a38d477462cd0 --lane <sandbox clone> --only mutants-adjacency-overlap.py` → exit 0; summary: `{"revision": "f3a5723a...", "targets": 1, "channels": ["loader-env","child-contract","dotgit-pointer"], "pairs": 3, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "b168b9b8...", "scratch": "/fast/scratch/hyaku/git-child-env-32q09lx5"}` (probe sha256 matches the declared b168b9b8…). Per-channel records show evidence []/leak false on all three channels.

4. [obs] Control-run volume is real, not a stub: the probe's control run straced 991 git child execs (control_git_execs: 991) with rc 0 and no harness error (ctlA vs ctlB parity held). The dotgit-pointer channel produced no spurious "canary fingerprint changed" verdict this run (evidence empty), so no re-run was needed.

5. [obs] Tool behavior is identical at 8cff9e7c and f3a5723a under the probe's TARGETS argv (--base <rev> --counter-rev <rev> --lane <bare clone>): both exit 0 and both normalized stdout (40/64-hex and scratch predicates substituted) hash to sha256 7be2780859a8b0903af12a849202d96d4e39ed175605f7213e33525bf70ffa5e (18012 bytes), including all 34 per-mutant JSON records and the summary line (should_fail_total 24, accepted 0, should_pass_accepted 5 at both). Evidence: compare.py runs at /fast/scratch/hyaku/tsukuroi-r31/RevScrubMutantsAdjacency/cmp-8cff9e7c/ and cmp-f3a5723a/; normalized outputs saved at norm-8cff9e7c.out / norm-f3a5723a.out, diff-identical.

6. [inf] No hollow fix: the change is a one-line environment-filter extension, it does not touch output, exit, or control flow; parity of output does not come from replay or early exit (the tool ran its full battery in both step-3 runs, and the probe observed 991 real git execs in the straced control run). The loader-env channel exercises exactly the changed mechanism (injecting LD_PRELOAD/LD_LIBRARY_PATH/PYTHONPATH and verifying no descendant exec carries the injection path) and found no leak.

## Residual risk / verification gaps
- [unk] This review covers only mutants-adjacency-overlap.py's C2 fix; the other ten targets of the C2 claim are out of scope for this seat.
- [obs] Dotgit-pointer channel was clean on this single run; the wave-1 spurious-verdict rate (2/121) means a single clean run is not proof against noise, but no anomaly was observed here.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md@f4861f4d (declaration), tools/mutants-adjacency-overlap.py@f3a5723a, tools/probe-git-child-env-r31.py@f3a5723a, git diff 8cff9e7c..f3a5723a -- tools/mutants-adjacency-overlap.py; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevScrubMutantsAdjacency.md, /fast/scratch/hyaku/tsukuroi-r31/RevScrubMutantsAdjacency/{repo,compare.py,norm-8cff9e7c.out,norm-f3a5723a.out,cmp-8cff9e7c,cmp-f3a5723a}; executed=git diff/show/rev-parse/clone/checkout (read-only), python3 tools/probe-git-child-env-r31.py --revision f3a5723a… --lane <clone> --only mutants-adjacency-overlap.py (exit 0), python3 compare.py (both revisions, rc 0, identical normalized stdout).
Model: not exposed
Installs: none
