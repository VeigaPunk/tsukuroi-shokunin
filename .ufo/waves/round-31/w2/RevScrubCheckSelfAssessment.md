# Round 31 wave 2 — RevScrubCheckSelfAssessment (C2 fix review: tools/check-self-assessment.py)

Verdict: **holds**. The C2 fix in `tools/check-self-assessment.py` (git_env filter broadened from GIT_ to GIT_/LD_/PYTHON) closes the loader-env leak at every subprocess spawn site, keeps the round-30 child contract, preserves the tool's observable behavior, and is not hollow.

Sandbox: /fast/scratch/hyaku/tsukuroi-r31/RevScrubCheckSelfAssessment/repo (clone at f3a5723a988bf1c2835985880e7a38d477462cd0).

## Findings

1. [obs] Every subprocess spawn site in the tool uses `git_env()`. Enumerated by target-site read (grep `subprocess|Popen|os\.system|os\.exec|run\(` on the tip file): `subprocess.run` appears only at line 115 (`git()` wrapper), lines 186–187 (`census_case_count` runs `bash tools/tsukuroi-census.sh --selftest` with `env=git_env()`), and lines 1017/1023/1024 (`build_fixture` git init/add/commit with `env = git_env()` at line 1016). None omits the cleaned environment; no site is left to inherit ambient GIT_/LD_/PYTHON names.

2. [obs] `git_env()` (file lines 92–107) drops every `GIT_`/`LD_`/`PYTHON`-prefixed name and re-asserts the round-30 contract on its children: `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, non-empty `GIT_CEILING_DIRECTORIES` (set to the temp-sandbox parent), plus `HOME`/`XDG_CONFIG_HOME` redirected into a private temp home, `PATH=/usr/bin:/bin`, `LC_ALL=C`, `GIT_NO_REPLACE_OBJECTS=1`, `GIT_TERMINAL_PROMPT=0`.

3. [obs] Frozen probe at the attacked revision, command:
   `python3 tools/probe-git-child-env-r31.py --revision f3a5723a988bf1c2835985880e7a38d477462cd0 --lane /fast/scratch/hyaku/tsukuroi-r31/RevScrubCheckSelfAssessment/repo --only check-self-assessment.py` → exit 0; summary: `{"targets": 1, "channels": ["loader-env","child-contract","dotgit-pointer"], "pairs": 3, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0", ...}` (sha256 matches the declared b168b9b8…; control git execs 331 per run). Per-channel evidence arrays are all empty: loader-env no descendant exec carries the injection path; child-contract all 331 git children carry the full contract; dotgit-pointer canary fingerprint unchanged.

4. [obs] The probe is sensitive — the pre-fix revision leaks. Same probe with `--revision 8cff9e7c` → exit 1, `leaking_pairs: ["tools/check-self-assessment.py:loader-env"]`, evidence `"348 descendant execs carry the injection path"`, sample first git child: `git init -q <scratch>/loader-env-8/tmp/self-assessment-selftest-j4qbw80x/clean`. At base, child-contract and dotgit-pointer were already clean; the only delta is the filter broadening — consistent with the fix's one-hunk diff (`git diff 8cff9e7c f3a5723a988bf1c2835985880e7a38d477462cd0 -- tools/check-self-assessment.py`: index 17c4740..fdca63b, only lines 93–94 change from `not k.startswith("GIT_")` to `not k.startswith(("GIT_", "LD_", "PYTHON"))`).

5. [obs] Tool parity across the fix: ran the probe's TARGETS argv for this tool (`['--selftest']`) from trees exported at each revision (`git archive 8cff9e7c` and `git archive f3a5723a988bf1c2835985880e7a38d477462cd0`, extracted under the seat scratch). Both exited 0; stdout identical after normalising 40/64-hex strings and scratch paths (`sed -E 's/\b[0-9a-f]{64}\b/<HEX64>/g; s/\b[0-9a-f]{40}\b/<HEX40>/g; s#self-assessment-selftest-[a-zA-Z0-9]+#<SCRATCH>#g'` → `diff st8.norm stF.norm` → `IDENTICAL_AFTER_NORM`; 5665 bytes each; stderr empty). Both ran the full 19 fixture cases: `"selftest": "PASS", "cases": 19, "failures": []` in both outputs.

6. [obs] No hollow-fix pattern: no output replay (the selftest recomputes K01–K27 against fresh temp repos each run — control_git_execs 331 per run), no early exit (full evaluate + 19 cases ran), no skipped work (identical case set and counts at both revisions).

## Residual risk / verification gaps

- [inf] The loader-env channel injects exactly LD_PRELOAD/LD_LIBRARY_PATH/PYTHONPATH; the filter also covers other LD_/PYTHON-prefixed names (e.g. PYTHONHOME), but those are not separately exercised by any channel.
- [unk] No channel asserts that the tool itself never sets a GIT_ variable for children; source review shows it sets only the contract keys in finding 2 (read-only, required by the contract).

## Scope

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md (round-31 declaration + errata), /fast/scratch/hyaku/tsukuroi-r31/RevScrubCheckSelfAssessment/repo/tools/check-self-assessment.py, /fast/scratch/hyaku/tsukuroi-r31/RevScrubCheckSelfAssessment/repo/tools/probe-git-child-env-r31.py, git diff 8cff9e7c f3a5723a988bf1c2835985880e7a38d477462cd0 -- tools/check-self-assessment.py; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevScrubCheckSelfAssessment.md; executed=probe runs at f3a5723a988bf1c2835985880e7a38d477462cd0 and 8cff9e7c (exit 0 and 1), check-self-assessment.py --selftest at both revisions (both exit 0), normalization diff, git archive/rev-parse (read-only).
Model: not exposed.
Installs: none
