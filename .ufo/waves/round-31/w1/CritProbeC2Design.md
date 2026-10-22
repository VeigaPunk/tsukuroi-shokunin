# CritProbeC2Design — attack on the frozen C2 probe (round 31, wave 1)

Verdict: partly holds. The frozen probe `tools/probe-git-child-env-r31.py` (sha256 b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0) catches the naive hollows (H1-style early exit, plain stdout replay, a shell re-export, a dropped `GIT_CONFIG_NOSYSTEM`, a writing git call through the `.git` pointer) and its strace parser is robust for interleaved and quoted lines. But four sandbox mutants of `tools/check-kernel-taint.py` reach loader-env leaking 0 with harness_errors [] while all 933 of their git children still receive a working loader injection. Three more mutants break the child contract or follow the `.git` pointer and still read 0 on every channel. So on the probe alone, a C2 reading of leaking 0 is necessary but not sufficient; it needs diff review against the C2 FIX CONTRACT.

All mutants are sandbox commits on top of either the H2 genuine control (commit 8e8da23f766b62d656087ebcdde741f0044db784, which is `measure/controls/c2/0001-H2-…patch` applied to 8cff9e7c) or the base 8cff9e7cfb034b49c645d548801ac3185a827cb4. They live in `/fast/scratch/hyaku/tsukuroi-r31/CritProbeC2Design/repo` and its worktrees. Each was run with `python3 tools/probe-git-child-env-r31.py --revision <REV> --lane /fast/scratch/hyaku/tsukuroi-r31/CritProbeC2Design/repo --only check-kernel-taint.py`. Patches are in `.ufo/waves/round-31/w1/CritProbeC2Design/patches/<mutant>/`, probe outputs in `…/runs/probe-<mutant>.jsonl`, and revisions in `…/runs/revisions.txt`.

## Results table (frozen probe, check-kernel-taint.py)

| mutant | base | loader-env | child-contract | dotgit-pointer | probe exit | should leak? |
|---|---|---|---|---|---|---|
| h2 (reference) | 8cff9e7c | 0 | 0 | 0 | 0 | no |
| q1-realpath | h2 | 0 | 0 | 0 | 0 | yes (loader) |
| q1-pad | h2 | 0 | 0 | 0 | 0 | yes (loader) |
| q2-fingerprint | base | 0 | 0 | 0 | 0 | yes (loader) |
| q2-replay | base | 1 (git_execs 877≠933) | 0 | 0 | 1 | yes, caught |
| q2-replay-v2 | base | 0 | 0 | 0 | 0 | yes (hollow) |
| q3-cc-nosystem | h2 | 0 | 1 (56 of 933) | 0 | 1 | yes, caught |
| q3-cc-bingit | h2 | 0 | 0 | 0 | 0 | yes (contract) |
| q3-dp-write | h2 | 0 | 0 | 1 (canary changed) | 1 | yes, caught |
| q3-dp-read | h2 | 0 | 0 | 0 | 0 | yes (pointer followed) |
| q3-ceiling | h2 | 0 | 0 | 0 | 0 | yes (contract and pointer) |

## Findings

1. [obs] **Q1, realpath evasion: leaking 0 while every git child preloads the injected library.** Mutant q1-realpath (commit 2adeebbf975a97c4bb34e6ba4e1ee2683962e9eb) keeps the H2 scrub and then adds back `env['LD_PRELOAD'] = os.path.realpath(os.environ['LD_PRELOAD'])`.
   - Frozen probe: loader-env `"evidence": [], "leak": false`, summary leaking 0, exit 0 (`runs/probe-q1-realpath.jsonl`).
   - Out-of-band (`effect_check.py`, output in `effect_check.out.json`): 933 of 933 git execs carry `LD_PRELOAD=/usr/lib/libm.so.6`, and stdout sha256 f028f847… is identical to H2.
   - Cause: the probe only tests whether the inject directory appears as a substring, at probe line 335: `carried = [e for e in r['execs'][1:] if any(inject in x for x in e[3])]`. The inject library is a symlink, and its realpath has no `<inject>` substring.
   - Effect is real: case L-realpath in `parse_trace_tests.out.json` shows `libm_loaded_in_child=True` read from the child's /proc/self/maps, with carried 0.
   - A renamed copy behaves the same way: case L-copy in `parse_trace_tests2.out.json` gives `copy_loaded_in_child=True`, carried 0.

2. [obs] **Q1, truncation evasion through strace's `-s 65536`.** Mutant q1-pad (commit 9d47c56bf66dbb412d6769d526544eca41064a11) re-adds `LD_PRELOAD=' ' * 70000 + <inject>/libprobe-inject.so`.
   - glibc skips the leading spaces as list separators, so the library still loads (L-pad-truncate: `libm_loaded_in_child=True`).
   - strace cuts the string at 65536 characters (probe line 220: `'-s', '65536'`), so the inject path never appears in the trace.
   - Frozen probe: loader-env leak false, leaking 0, exit 0 (`runs/probe-q1-pad.jsonl`).
   - Out-of-band with `-s 262144`: 933 of 933 git children carry a 70092-character LD_PRELOAD whose stripped value is the inject library.

3. [obs] **Q1, routes the probe does not observe at all.**
   - Argv route: a Python child given the inject path in argv and calling `sys.path.insert` shows carried 0 with the path in effect (L-argv-python: `pythonpath_via_argv=b'True'`). The probe never inspects argv.
   - execveat route: `os.execve(fd, …)` makes the kernel call execveat, which `-e trace=execve` does not record. Case G-execveat-loader traces 2 records (both python), carried 0, and `execveat_child_libm=True`.
   - Shell re-export is caught: a child shell runs `LD_PRELOAD=$(cat file) exec cat`, and the probe sees it (L-reexport-shell: carried 1), because strace records the final execve environment.

4. [obs] **Q2, a probe-fingerprinting hollow passes.** Mutant q2-fingerprint (commit 36285801982b54f7a137a8129dbfea6ff451a453, on the unfixed base) drops LD_/PYTHON names only when `'libprobe-inject' in os.environ.get('LD_PRELOAD', '')`.
   - Frozen probe: leaking 0 on all three channels, exit 0 (`runs/probe-q2-fingerprint.jsonl`).
   - Out-of-band with the same library under another name (`alt/libalt.so`): 933 of 933 git children carry LD_PRELOAD=…/alt/libalt.so (`effect_check.out.json`, row q2-fingerprint/other-name).
   - Cause: the injection values are fixed and public (probe docstring lines 20-22 and line 286 name `libprobe-inject.so`; the scratch prefix is `git-child-env-`), so a tool can recognise the probe.

5. [obs] **Q2, an output-replay hollow passes once the git exec count is tuned.**
   - The scratch state is not fresh between runs. `one_run` deletes only the tree copy (probe line 236: `shutil.rmtree(wtree, ignore_errors=True)`), so control A's `home/` and `tmp/` stay under the shared scratch root at `<root>/ctlA-<i>/tmp`. That root is the grandparent of every run's TMPDIR.
   - Mutant q2-replay (commit c2910c67…) records its stdout, exit code and Python-level git call count into `$TMPDIR/replay.json` during control A. Under LD_PRELOAD it replays that output and runs `git --version` the recorded number of times with a scrubbed environment, doing no real work.
   - The probe caught v1 by parity: `git_execs 877 differs from control 933`. The 56 missing execs are the git children that `git commit` starts itself, one per fixture.
   - Mutant q2-replay-v2 (commit cb160068ba70f1a438e3c7ad76eb76b1e4a8eca4) counts each `commit` call as 2. It reads loader-env `"git_execs": 933, "evidence": [], "leak": false`, leaking 0, exit 0 (`runs/probe-q2-replay-v2.jsonl`).
   - Out of the probe (no control A cache), v2 falls through to base behaviour: 933 of 933 git children carry the injection under both library names.
   - Parity compares only `('rc', 'stdout_sha256', 'git_execs')` (probe line 242). A count is cheap to forge.

6. [obs] **Q3, child-contract can fail.** Mutant q3-cc-nosystem (commit 6ca2478d…) drops GIT_CONFIG_NOSYSTEM from the fixture `rev-parse` call only. The probe reports child-contract `"56 of 933 git children lack the contract"`, with sample `'missing': ['GIT_CONFIG_NOSYSTEM']`, exit 1 (`runs/probe-q3-cc-nosystem.jsonl`). The channel's 0 at the base is therefore not structural.

7. [obs] **Q3, child-contract is blind to git reached by any path other than `/usr/bin/git` or `/usr/lib/git-core/*`.**
   - Probe line 166: `return fname == SYSTEM_GIT or fname.startswith('/usr/lib/git-core/')`.
   - Mutant q3-cc-bingit (commit 97e98850…) runs the same `rev-parse` as `/bin/git` with `env={'PATH': '/usr/bin:/bin'}`, so the child has no contract at all.
   - Result: child-contract leak false, leaking 0, exit 0. Control git_execs drops consistently to 877 in all runs, so parity holds (`runs/probe-q3-cc-bingit.jsonl`).
   - The same blind spot covers `/usr/bin/../bin/git` and `git` resolved through `PATH=/bin:/usr/bin`. Cases G-usr-dotdot-git and G-path-order both count 0 git execs. On this host `/bin` is a symlink to `usr/bin`.
   - execveat (G-execveat) runs git (it printed `git version 2.56.0`) with no trace record.

8. [obs] **Q3, dotgit-pointer can fail, but only on writes or output changes.**
   - Mutant q3-dp-write (commit 60d446a8…) runs `git config probe.mutant 1` in its working directory without `-C`, under the full contract. The probe reports `canary fingerprint changed`, exit 1 (`runs/probe-q3-dp-write.jsonl`).
   - Mutant q3-dp-read (commit c999d5c8…) runs `git rev-parse HEAD` in the working directory and discards the output. All channels read 0 (`runs/probe-q3-dp-read.jsonl`), yet that call shape resolves the canary HEAD through the pointer file (`dotgit-read-follow-demo.txt`: `dp-read shape (cwd, ceiling=TMPDIR): b6de37d6… rc=0`).
   - `GIT_CEILING_DIRECTORIES` never stops discovery in the working directory itself.
   - The routed defect was that the pointer "is followed". The probe only sees a follow that changes the fingerprint (probe line 346) or the normalised stdout. Any hex the follow prints is folded to `<HEX>` (line 82).

9. [obs] **Q3, the ceiling predicate only checks that the value is non-empty.**
   - Probe line 322: `if not kv.get('GIT_CEILING_DIRECTORIES'):`.
   - Mutant q3-ceiling (commit 90d822e5…) sets `GIT_CEILING_DIRECTORIES=/nonexistent` and runs `git -C <TMPDIR>/x/sub rev-parse HEAD`. Discovery climbs to the TMPDIR `.git` file and reads the canary (demo: `ceiling shape (ceiling=/nonexistent, -C TMPDIR/sub): b6de37d6…`).
   - The probe reads child-contract 0 and dotgit-pointer 0 (`runs/probe-q3-ceiling.jsonl`). With the ceiling at TMPDIR, the same call fails with `fatal: not a git repository`.

10. [obs] **Q4, parse_trace is robust in what it parses but fails open in what it drops.**
    - Robust:
      - Case P-concurrent: 84 `<unfinished ...>` and 84 `execve resumed>` lines; 96 git execs counted for 96 raw git lines; 108 carried.
      - Case P-quote-bracket: argv `a", "b]`, values `v", "Y]` and `] , ["q` parse into the right elements, and the inject value after them is still detected (carried 1).
    - Fails open:
      - Strings are kept strace-escaped and never decoded. [inf] A scratch path containing a non-printable byte, `"` or `\` would no longer match as a substring. The default scratch path is ASCII.
      - A truncated string loses its tail (finding 2).
      - In the synthetic trace, `execve("/usr/bin/git", NULL, ["LD_PRELOAD=<inject>…"]) = 0` parses as argv [] and envp [] (probe line 149: `argv, envp = [], []`). That is a counted git exec with no environment: it fails closed for child-contract but open for loader-env.
      - The non-`-v` form `0x7ffd /* 3 vars */` and truncated arrays `["A=1", ...]` also drop entries silently.
    - Harmless here [inf]: unfinished records are appended when they resume, so trace order can change. `execs[0]` is still the target's own exec, because a child cannot exec before its parent.

11. [obs] **Probe strengths worth keeping.** These hollows were caught: plain replay (finding 5, v1), H1 (`measure/controls/c2/c2-H1.jsonl`), shell re-export (finding 3), NOSYSTEM drop (finding 6) and a writing pointer follow (finding 8). H2 reads 0/0/0 here too (`runs/probe-h2.jsonl`).

12. [obs] **Base sweep and the landed integration diff.**
   - At the base 8cff9e7c, the frozen probe was run on six more targets one at a time: check-adjacency-overlap, check-freshness-r17, check-memory-pressure, check-registry-coverage, check-storage-health and check-self-assessment (`runs/base-sweep-8cff9e7c.txt`). Each shows loader-env leaking, child-contract 0, dotgit-pointer 0 and harness_errors []. So on every target measured, the two channels this attack questions read 0 at the base. Findings 6 and 8 show that 0 is not structural: the channels can fail when a tool really drops the contract or writes through the pointer.
   - The integration commit 13ca52d (landed during this attack) changes 13 tools. In `git diff 8cff9e7 13ca52d -- tools`, every hunk only widens the name-prefix filter from `'GIT_'` to `('GIT_', 'LD_', 'PYTHON')`. No hunk re-adds an `LD_*`/`PYTHON*` value, reads `LD_PRELOAD` contents, uses TMPDIR or HOME, or changes a git path. So the diff passes the diff check proposed under "Smallest safe correction", and none of the hollow shapes in findings 1, 2, 4 and 5 appears in it.
   - [inf] The probe still cannot rule out a child that never passes through those builders but gets an injection some other way. Plain inheritance would still be visible, because the inject path stays a substring.

## Impacted axes

- C2 operability. A leaking-0 reading does not show that children get a clean environment (findings 1, 2, 4, 5) or the contract (findings 7, 9, 8).
- Provenance of the "after" receipt. A receipt could be honest while the fix is hollow.
- No C1 impact.

## Defect or tradeoff

- Fixable probe defects:
  - finding 1, value matching instead of name matching;
  - finding 2, truncation;
  - finding 3, argv and execveat not observed;
  - finding 5, scratch state that persists and a count-only parity;
  - finding 7, the path test in `is_git`;
  - finding 8, reads not observed;
  - finding 9, the ceiling only checked for non-empty;
  - finding 10, parse failures fail open.
- Tradeoff: adversarial probe detection (finding 4, and finding 5 in general) cannot be fully closed by any black-box probe. The canonical judge should require diff review in addition to the probe reading.
- The probe is frozen for round 31 ("never change a rule after data"), so these corrections belong to a later round. For this round, the C2 FIX CONTRACT plus a diff review closes the gap.

## Smallest safe correction

- **This round, no rule change:** admit a C2 "after" reading only together with a per-tool diff check. Every child-process `env` must come from a builder that applies `k.startswith(('GIT_', 'LD_', 'PYTHON'))` and then adds nothing from `LD_*`/`PYTHON*`. The diff must not branch on `LD_PRELOAD` contents and must not touch TMPDIR or HOME outside the tool's own temporary directories.
- **Next probe revision:**
  - loader-env: leak on any descendant exec that has any `LD_*` or `PYTHON*` name at all (the control has none), plus any argv string containing `<inject>`. Use a random library and directory name for each run.
  - Tracing: trace `execve,execveat`. Treat a parse failure or `...` truncation inside an LD_/PYTHON/GIT_ string as a harness error.
  - `is_git`: test the realpath of the file name.
  - Scratch: delete each run's whole work directory, not just `wtree`.
  - Parity: compare the normalised sequence of git `argv[1:]` instead of the count.
  - child-contract: require `GIT_CEILING_DIRECTORIES` to contain the run's TMPDIR.
  - dotgit-pointer: also trace `%file` and leak on any path under `<canary>`.

## Artifacts (under /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/CritProbeC2Design/)

- `patches/<mutant>/0001-*.patch`: 11 sandbox commits (h2 plus 10 mutants).
- `runs/revisions.txt` and `runs/probe-<mutant>.jsonl`: frozen probe outputs. sha256 of `probe-q2-replay-v2.jsonl` is d473d043…, of `probe-q1-pad.jsonl` 3b54c535…, of `probe-q1-realpath.jsonl` 659b0a64….
- `parse_trace_tests.py`, `parse_trace_tests2.py` and their `.out.json` files: real-strace and synthetic parser cases.
- `effect_check.py` and `effect_check.out.json`: out-of-band injection effect for h2, q1-realpath, q1-pad, q2-fingerprint and q2-replay-v2.
- `dotgit-read-follow-demo.txt`: proof that the call shapes in findings 8 and 9 follow the pointer.
- `runs/base-sweep-8cff9e7c.txt`: frozen probe summary lines for six base targets (finding 12).

Scope: read=frozen probe (full), tools/check-kernel-taint.py (git_env, run_fixture, main), measure/controls/c2 (H1/H2 patches and receipts); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/CritProbeC2Design.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/CritProbeC2Design/ (patches, runs, test scripts and outputs, demo), sandbox /fast/scratch/hyaku/tsukuroi-r31/CritProbeC2Design/ (clone, worktrees, traces); executed=sandbox git clone/checkout/am/worktree/commit/format-patch (sandbox only), frozen probe --only check-kernel-taint.py on 11 revisions plus 6 base targets (loader-env leaking 1 each, other channels 0), git diff 8cff9e7 13ca52d -- tools (read-only), parse_trace_tests.py, parse_trace_tests2.py, effect_check.py, dotgit demo shell
Model: not exposed
Installs: none
