# Round 31 wave 2 — RevScrubMutantsOwedR29Landed (C2 fix review, lane tip f3a5723a)

Verdict: **holds**. The C2 fix in `tools/mutants-owed-statements-r29-landed.py` and its parent `tools/check-owed-statements-r29.py` drops GIT_/LD_/PYTHON names at every child-process spawn site, keeps the round-30 contract, passes the frozen probe (leaking 0 of 3 pairs, exit 0), and is behavior-parity-identical to the 8cff9e7c version under the probe argv (exit 0, 29/29 normalized JSON lines equal). No hollow fix found.

## 1. The fix

1. [obs] The entire change on the target file is one line (`git diff 8cff9e7c f3a5723a -- tools/mutants-owed-statements-r29-landed.py`): line 35 `ENV = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'LD_', 'PYTHON'))}` (was `'GIT_'` only). The parent file's `clean_env` got the identical one-line change (`git diff 8cff9e7c f3a5723a -- tools/check-owed-statements-r29.py` line 154).
2. [obs] 13 environment builders across tools/ carry the same filter at the tip (grep `startswith(('GIT_', 'LD_', 'PYTHON'))` / `startswith(("GIT_", "LD_", "PYTHON"))`): `_revision.py`, `check-adjacency-overlap.py`, `check-freshness-r17.py`, `check-kernel-taint.py`, `check-memory-pressure.py`, `check-owed-statements-r29.py`, `check-registry-coverage.py`, `check-self-assessment.py`, `check-storage-health.py`, `mutants-adjacency-overlap.py`, `mutants-kernel-taint.py`, `mutants-owed-statements-r29-landed.py`, `mutants-owed-statements-r29.py`. Matches the declared "13 environment builders".

## 2. Spawn-site audit (item 1)

Target `tools/mutants-owed-statements-r29-landed.py` at f3a5723a has exactly 5 subprocess spawn sites, all `subprocess.run(...)` with explicit `env=ENV` and no shell:

- line 48 `git clone -q --no-local ARGS.lane REPO` (env=ENV);
- lines 49-50 `git rev-parse --verify` (env=ENV);
- lines 54-55 `git -C ARGS.lane show <counter-rev>:tools/check-owed-statements-r29.py` (env=ENV);
- lines 62-63 the `git()` helper (env=ENV), used for every checkout/clean/add/commit/rev-parse in the battery;
- lines 278-279 the counter child `[sys.executable, COUNTER, ...]` (env=ENV).

`ENV` (line 35) is built from `os.environ` minus `GIT_`/`LD_`/`PYTHON` prefixes, then lines 43-47 re-add only `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CEILING_DIRECTORIES` (dirname of SEAT), plus private `HOME`/`XDG_CONFIG_HOME` and `PATH=/usr/bin:/bin`. No `LD_`/`PYTHON` name is ever re-added. No other spawn mechanism exists (grep `subprocess|Popen|os.system|os.exec` → only the 5 sites; no `shell=True`).

Parent `tools/check-owed-statements-r29.py` at f3a5723a has exactly 1 spawn site: the `git()` helper lines 173-174, `env=clean_env(lane)`. `clean_env` (lines 153-169) drops `GIT_`/`LD_`/`PYTHON`, then sets `GIT_OPTIONAL_LOCKS=0`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_CEILING_DIRECTORIES`, `PATH=/usr/bin:/bin`, `LC_ALL=C`, `HOME`, `XDG_CONFIG_HOME`.

No spawn site fails to drop the injected names. The round-30 contract (GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_SYSTEM=/dev/null, non-empty GIT_CEILING_DIRECTORIES, private HOME, fixed PATH) is kept at every site.

## 3. Frozen probe (item 2)

Command (run in the sandbox clone at f3a5723a):
`python3 tools/probe-git-child-env-r31.py --revision f3a5723a988bf1c2835985880e7a38d477462cd0 --lane /fast/scratch/hyaku/tsukuroi-r31/RevScrubMutantsOwedR29Landed/repo --only mutants-owed-statements-r29-landed.py`

Summary (last line, exit 0):
`{"revision": "f3a5723a...", "targets": 1, "channels": ["loader-env", "child-contract", "dotgit-pointer"], "pairs": 3, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0", "scratch": "/fast/scratch/hyaku/git-child-env-or6_gq8m"}`

All three channel lines report `leak: false`, `evidence: []`, `control_rc 0 == channel_rc 0`, `git_execs 1044 == 1044`. The probe sha256 equals the declared b168b9b8…. No dotgit-pointer spuriosity occurred (3 pairs clean; the after-receipt at 13ca52d0 is likewise clean for this tool). This matches the integration receipt `measure/after-13ca52d0/c2-declared.jsonl` (pairs 33, leaking 0, harness_errors [], exit 0; same control_git_execs 1044 for this tool). Before the fix, the same tool leaked on loader-env at f4861f4d: `measure/c2-before-f4861f4d…jsonl` → `"evidence": ["1073 descendant execs carry the injection path"], "leak": true` (11 of 33 before-leaks, all loader-env).

## 4. Probe-argv parity at 8cff9e7c vs f3a5723a (item 3)

Ran the TARGETS argv for this tool at both revisions (each in its own sandbox checkout of that revision, `--lane <that clone>`):
`python3 tools/mutants-owed-statements-r29-landed.py --base <REV> --counter-rev <REV> --lane <clone>`

- 8cff9e7c: exit 0, 29 JSON lines.
- f3a5723a: exit 0, 29 JSON lines.
- Comparison after normalizing 40/64-hex and scratch paths (`/fast/scratch/hyaku/…`) — `python3 /fast/scratch/hyaku/tsukuroi-r31/RevScrubMutantsOwedR29Landed/cmp.py` → `diffs 0`, all 29 lines byte-identical. Both runs produce: control_marked 12, should_fail_total 19 → should_fail_accepted 0, semantic_total 7 → semantic_counted 6 (N13/N16/N18/N23/N24/N26), should_pass_total 1 → refused 0, no crashes, empty stderr_tail.

Note: the `counter_sha256` field legitimately differs between revisions (different check-owed.py blob); as a hex value it normalizes away, and no behavior field differs.

## 5. Hollow-fix check (item 4)

- No early exit, no output replay, no skipped work: the diff touches only the env-filter line; `main()` (lines 292-327) still executes the full battery — C0 control, 26 mutation shapes, P1 should-pass, one counter invocation per shape, final summary print, and the same 0/1 exit rule.
- The probe's own control/parity machinery confirms real work: 1044 git execve children per control run (clone, rev-parse, 27× checkout/clean/add/commit/rev-parse, plus 28 counter children each running the parent's git), and the injected loader-env run equals the control byte-for-byte (same stdout sha256, same rc, same git_execs) with no descendant carrying the injection path.
- The before-run (8cff9e7c) also executed the identical battery and passed — the fix is a strict env-shrink, not a behavior rewrite.

## 6. Findings by severity

No actionable defect found in scope. Observations:
1. [obs] Fix is minimal and correct at all 5 spawn sites of the target and the 1 site of the parent (evidence §2).
2. [obs] Frozen probe: leaking 0 of 3 pairs, exit 0, harness_errors empty, declared sha (evidence §3).
3. [obs] Parity before/after: exit 0 both, 29/29 normalized lines identical (evidence §4).
4. [obs] No hollow behavior: full battery executed, control/channel parity holds, git_execs 1044 (evidence §5).
5. [obs] Receipt consistency: integration after-receipt has subjects 0 of 33 for this tool's 3 pairs; before-receipt shows the loader-env leak this fix closes (evidence §3).

## 7. Residual risk and verification gaps

- [unk] This seat covers 2 of the 11 C2 targets; the other 9 tools and `_revision.py` are reviewed by sibling seats. The 13-builder inventory is confirmed by grep, but the per-tool probe results for the other targets come from the shared receipts, not from a run I executed.
- [inf] The direct parity runs used `--lane <working checkout>` rather than the probe's bare clone; the tool accepts any repo path as lane and the operations are read-only on the lane, so this does not change the comparison.
- [obs] The dotgit-pointer channel showed no spuriosity in my run; if the known intermittent false positive appears in later runs, the affected pair should be rerun per the round-31 directive.
- [inf] Env-filter changes to `tools/_revision.py` were verified by diff only (same one-line pattern), not by execution in this seat.

Scope: read=tsukuroi-shokunin SCORECARD.md declaration section (f4861f4d), corpus/lessons/round-30-verifier-spotcheck.md, prompt lines 343-365, sandbox clone tools/mutants-owed-statements-r29-landed.py, tools/check-owed-statements-r29.py, tools/probe-git-child-env-r31.py, tools/_revision.py diff, measure/c2-before-f4861f4d…jsonl, measure/after-13ca52d0/c2-declared.jsonl, measure/ controls listing; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevScrubMutantsOwedR29Landed.md; executed=git diff (read-only), sandbox clone/checkout, probe-git-child-env-r31.py --only (frozen), mutants-owed-statements-r29-landed.py runs at 8cff9e7c and f3a5723a in sandboxes, cmp.py comparison, grep/read-only git
Model: Mercury (inception/mercury-3)
Installs: none
