# MutProbeC2 — mutation test of the C2 frozen probe (round 31, wave 1)

Verdict: **partly holds** — the frozen probe `tools/probe-git-child-env-r31.py` kills 3 of the 10
mutations on the committed control battery (base / H1 / H2); **7 mutants survive** because they
change no outcome on any of the three lane states. The load-bearing structure is narrower than it
looks: the probe's **stdout and git-exec-count parity terms are individually redundant** (M02 and
M03 each survive; only dropping both, M10, kills the hollow control H1), the **loader-env channel's
first-exec exclusion is load-bearing** (M04 turns the genuine fix H2 into a false positive, 5/5
runs), and **two harness guards are unexercised** by the committed controls (M08, M09). Separately
the probe has a **non-deterministic dotgit-pointer reading** (2 spurious `canary fingerprint
changed` verdicts in 121 probe runs, 0 reproduced in 56 targeted re-runs), which makes one lane
state unusable as a one-shot gate.

## 1. Setup and containment

1. [obs] Sandbox clone: `/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo`, created with
   `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-local
   /home/vgpnk/Projects/shokunin/tsukuroi-shokunin …` and checked out at
   `8cff9e7cfb034b49c645d548801ac3185a827cb4`. Every git invocation was prefixed
   `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`; no git write was run in the lane
   (`git -C …/tsukuroi-shokunin status --porcelain` returns empty output) and none in the fleet
   repo. No `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` was ever set to a lane or fleet path.
2. [obs] The probe under test is byte-identical to the lane copy and to the sha256 recorded in the
   committed control receipts: `sha256sum …/tools/probe-git-child-env-r31.py` →
   `b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0`, equal to the
   `probe_sha256` field in `.ufo/waves/round-31/measure/controls/c2/c2-H1.jsonl` and `c2-H2.jsonl`.
   The mutants were applied to **copies** under
   `/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants/`; the pristine probe was never modified
   (hash re-verified after every batch: still `b168b9b8…`).
3. [obs] The two committed control patches were applied in the sandbox clone and committed on two
   branches off the base revision: H1 → `dc220b013e969b9e05584c0095ed14be8bdf0707` ("H1 hollow
   control"), H2 → `5f41145a7f7ea75e0d568dc7ae65e4f50a67e2a6` ("H2 genuine control"). Both applied
   cleanly with `git apply --check` (exit 0). The lane's own base revision `8cff9e7c…` is the
   "base" state (unmodified `tools/check-kernel-taint.py`).
4. [obs] Every probe run was `python3 <probe> --revision <rev> --lane <sandbox repo> --scratch
   <seat scratch> --only check-kernel-taint.py`, i.e. the frozen argv of the committed receipts
   plus an explicit `--scratch` inside the seat's own area.

## 2. Baseline: the pristine probe reproduces the committed control receipts

5. [obs] Pristine probe, base revision `8cff9e7c…`: `leaking = 1`,
   `leaking_pairs = ["tools/check-kernel-taint.py:loader-env"]`, `harness_errors = []`, exit 1.
   Evidence: `933 descendant execs carry the injection path` — the base tool passes
   `LD_PRELOAD`/`LD_LIBRARY_PATH`/`PYTHONPATH` down to its 933 git children
   (`tools/check-kernel-taint.py:252-253` filters only the `GIT_` prefix).
6. [obs] Pristine probe, H1 (`dc220b0…`): `leaking = 1`, exit 1, evidence
   `stdout_sha256 e3b0c44… differs from control f028f847…` and `git_execs 0 differs from control
   933`. This matches the committed receipt `c2-H1.jsonl` line for line (same two evidence
   strings, same `control_git_execs = 933`, same exit 1).
7. [obs] Pristine probe, H2 (`5f41145…`): `leaking = 0`, `harness_errors = []`, exit 0 — identical
   to the committed receipt `c2-H2.jsonl` (same `control_git_execs = 933`, exit 0).
8. [obs] The pristine probe is stable: across 71 re-runs of the three lane states
   (8 base, 25 H1, 38 H2) every run returned the same verdict, `harness_errors = []` in all of them.
   Therefore the committed control battery does separate the three lane states with the pristine
   probe, and it is a valid oracle for this mutation test.

## 3. The ten mutants

9. [obs] Each mutant is one exact-substring edit of the pristine probe, applied to a **copy**;
   every copy compiles (`python3 -m py_compile`, exit 0). Diffs and sha256s are in
   `.ufo/waves/round-31/w1/MutProbeC2/mutant-diffs.md` and `mutants/manifest.json`; the raw run
   outputs are in `runs/*.jsonl`, the consolidated table in `mutant-results.json`, the survivor
   table in `survivor-table.md`.

| id | edit | source anchor |
|---|---|---|
| M01 | `for k in ():` — drop the parity comparison entirely | `tools/probe-git-child-env-r31.py:242` |
| M02 | `for k in ('rc', 'git_execs'):` — drop the stdout term | same line 242 |
| M03 | `for k in ('rc', 'stdout_sha256'):` — drop the git-exec-count term | same line 242 |
| M04 | `r['execs']` instead of `r['execs'][1:]` — drop the first-exec exclusion | line 335 |
| M05 | match `LD_PRELOAD`/`LD_LIBRARY_PATH`/`PYTHONPATH` by **name** instead of by path | line 335 |
| M06 | drop `LD_LIBRARY_PATH` from the injected env | lines 331-332 |
| M07 | drop `PYTHONPATH` from the injected env | lines 331-332 |
| M08 | delete the `elif parity(ca, cb):` control-B determinism branch | lines 300-301 |
| M09 | delete the `elif ca['git_execs'] < 1:` "control run started no git child" branch | lines 302-303 |
| M10 | `for k in ('rc',):` — drop **both** stdout and exec-count (supplementary) | line 242 |

10. [obs] **Outcome table** (per lane state: `leaking` / `leaking_pairs`; `harness_errors = []`
    everywhere). The reference is the pristine probe: base `1`/`loader-env`, H1 `1`/`loader-env`,
    H2 `0`/none. Where a (mutant, lane) pair was run more than once, the majority verdict is
    used and the vote counts are in `survivor-table.md`.

| mutant | base | H1 | H2 | verdict |
|---|---|---|---|---|
| pristine | 1 loader-env | 1 loader-env | 0 | reference |
| M01 drop-parity-check | 1 loader-env | **0** | 0 | **killed** |
| M02 drop-stdout-comparison | 1 loader-env | 1 loader-env | 0 | **survivor** |
| M03 drop-git-exec-count | 1 loader-env | 1 loader-env | 0 | **survivor** |
| M04 skip-first-exec-exclusion | 1 loader-env | 1 loader-env | **1 loader-env** | **killed** (5/5 runs) |
| M05 injection-by-variable-name | 1 loader-env | 1 loader-env | 0 | **survivor** |
| M06 no-LD_LIBRARY_PATH in injection | 1 loader-env | 1 loader-env | 0 | **survivor** |
| M07 no-PYTHONPATH in injection | 1 loader-env | 1 loader-env | 0 | **survivor** |
| M08 drop-control-B determinism | 1 loader-env | 1 loader-env | 0 | **survivor** |
| M09 no-require-git-child | 1 loader-env | 1 loader-env | 0 | **survivor** |
| M10 drop stdout AND exec-count | 1 loader-env | **0** | 0 | **killed** |

**Killed: M01, M04, M10. Survivor: M02, M03, M05, M06, M07, M08, M09.**

## 4. What each surviving mutant means

11. [obs] **M02 (drop stdout term) survives**: the H1 hollow fix is still caught, because the
    `git_execs 0 differs from control 933` term fires on its own. Only the *evidence text* differs
    (M02's H1 evidence is `git_execs 0 differs from control 933` alone; pristine carries both
    terms). The stdout term is therefore **redundant on this battery** — the round-30 routed
    defect 5 ("stdout comparison (hollow fixes score 0)") is closed, but by the git-exec-count
    term rather than by stdout.
12. [obs] **M03 (drop git-exec-count term) survives** for the mirror-image reason: the stdout
    digest term alone still catches H1. The two parity terms are **mutually substitutable** on
    this battery, which is exactly why M10 (dropping both) is killed: M10's H1 reads `leaking = 0`,
    i.e. **the hollow control H1 becomes indistinguishable from the genuine fix H2**. That is the
    probe's real load-bearing structure: the parity block must compare at least one of
    {stdout digest, git-exec count} beyond `rc`.
13. [obs] **M04 (drop the first-exec exclusion) is killed, and it kills in the false-positive
    direction**: on H2 the genuine fix now reads `leaking = 1` with the evidence
    `1 descendant execs carry the injection path` — reproduced 5/5 on re-runs
    (`runs/M04-skip-first-exec-exclusion.H2.jsonl`, `flake/M04-H2-1..4.jsonl`), so it is a
    deterministic mutant effect, not a flake. The reason is structural: the tool's *own* first
    execve carries the ambient `LD_PRELOAD` by construction (the probe injects it into the tool's
    environment), and `r['execs'][0]` is that execve. The exclusion at line 335 is therefore
    load-bearing and correct; a probe that "simplifies" it away would reject the genuine fix.
14. [obs] **M05 (compare injection by variable name instead of path) survives** with identical
    verdicts on all three lane states. [inf] This is a *weaker* rule than the path rule, not an
    equivalent one: by name, a child carrying `LD_PRELOAD=/some/other/path` would count as
    carrying the injection, and a child carrying the inject path under a non-`LD_`/`PYTHON`
    variable would be missed. It survives only because the committed controls never produce
    either shape. [unk] Whether the lane wants the stricter path rule or the name rule is a
    contract question, not a defect: the frozen docstring says "an environment string containing
    the <inject> path", so the path rule is the specified one and M05 is a specification-violating
    mutant that the battery cannot see.
15. [obs] **M06 (drop `LD_LIBRARY_PATH` from the injection) and M07 (drop `PYTHONPATH`) both
    survive**: `LD_PRELOAD` alone still carries the `<inject>` path into the 933 git children, so
    the loader-env verdict is unchanged on all three lane states. [inf] This is a real coverage
    limit of the loader-env channel as frozen: the probe cannot show that a tool is *specifically*
    scrubbing `LD_LIBRARY_PATH` or *specifically* scrubbing `PYTHONPATH`, because the channel
    never separates the three names. Given the C2 fix contract requires dropping **every**
    `GIT_`/`LD_`/`PYTHON` name, a tool that scrubbed only `LD_PRELOAD` would still read as clean
    on this battery.
16. [obs] **M08 (drop the control-B determinism branch) survives**: the branch
    (`elif parity(ca, cb):` at line 300) fires only when two control runs of the *same* tool
    disagree, which does not happen for a deterministic target. Its only difference from pristine
    was one `dotgit-pointer` verdict in one of 13 M08-H2 runs, which 12 re-runs did not reproduce
    (see §5). [inf] M08 is a genuine coverage hole of the same kind as M09: the probe's determinism
    guard is unexercised by the committed controls, so a non-deterministic target would be scored
    on a single control run with no warning.
17. [obs] **M09 (drop the "control run started no git child" harness branch) survives**: for
    `check-kernel-taint.py` the control run always starts 933 git children, so the branch never
    fires and the removal is invisible. [inf] This branch is what stops a target that **never
    runs git at all** from being scored as clean; the committed controls contain no such target,
    so the branch is untested by this battery. It is not exercised by `--only
    check-kernel-taint.py` at all — a target whose selftest never touches git would be a new
    *fixture*, not a new mutation.

## 5. The dotgit-pointer channel is not deterministic

18. [obs] Two runs in the whole campaign produced a **spurious** `canary fingerprint changed`
    verdict on a lane state where pristine reads clean: `runs/M04-skip-first-exec-exclusion.H1.jsonl`
    (evidence `["canary fingerprint changed"]`, making that run read `leaking = 2`) and
    `runs/M08-drop-control-B-determinism-check.H2.jsonl` (evidence
    `["canary fingerprint changed"]`, making that run read `leaking = 1` on the *genuine fix*
    lane). Neither reproduced: M08-H2 re-run 12× clean (`flake/M08-H2-1..4.jsonl`,
    `flake4/M08-H2-r1..r8.jsonl`), M04-H1 re-run 4× clean (`flake/M04-H1-1..4.jsonl`), and the
    pristine probe itself re-run 71× clean across `flake2/PR2-H2-1..12.jsonl`,
    `flake3/PR3-base-1..6.jsonl`, `flake3/PR3-H1-1..4.jsonl`, `flake4/PR-H1-r1..r6.jsonl`,
    `flake4/PR-H2-r1..r8.jsonl` and the initial `runs/pristine.*` set.
19. [obs] The canary fingerprint is stable in isolation: `canary_stability.py` measured the
    probe's own `fingerprint()` over a 20 s idle window and after an explicit `git gc --auto` on
    the canary — identical digest `8eb485b16fec43b7f379a2295271c8c7a26d4372682d7074cbadcdf96b806db4`
    at t0, t+20 s and after gc, with the `objects/` file-name list unchanged. `gc_race.py` created
    six fresh canaries and watched each for 15 s: no canary mutated. `watch_canary.py` watched
    four canaries for 30 s each: no mutation.
20. [obs] `flaky_dotgit.py` reproduced the probe's dotgit-pointer shape directly (canary made with
    the probe's own `make_canary_repo`, `.git` pointer files written into the tree copy and TMPDIR,
    the tool run under strace, the canary re-fingerprinted and its file table diffed): 8/8 trials
    left the canary **unchanged** (`files_changed = []`).
21. [obs] `trace_canary.py` ran the tool under strace with the canary in place and grepped the
    whole trace for the canary path: **0 lines** mention it (934 execve records). So the target
    never touches the canary directly in its argv or envp.
22. [obs] `gitfile_discovery.py` tested the remaining plausible write path — a git command run
    under a directory holding a `.git` FILE pointer (the probe drops one into TMPDIR, so a git
    command without `-C` would *discover* the canary through the gitfile): `git rev-parse HEAD`,
    `git for-each-ref`, `git status --porcelain` and `git init` under that directory all left the
    canary's file set and index digest **unchanged**
    (`aabac51f89ac1a9aeb10d64a583c9d041b8d0f6631db95913adbc457c89126b0` before and after).
23. [inf] The two spurious readings are therefore not a canary-mutation race that the probe's own
    helpers can trigger, and their trigger remains unidentified: the dotgit-pointer verdict is
    **not reproducible run-to-run**, and one of the two spurious readings landed on the *genuine
    fix* lane state, where it would flip the round's headline "H2 reads 0" claim to "H2 leaks".
    [unk] Exact cause not established within this seat's time box. Two mechanisms remain open and
    I could not separate them: (a) a background `git maintenance run --auto --quiet --detach`
    spawned by the canary's own `git commit` (confirmed present via `GIT_TRACE=1` on a throwaway
    repo: `trace: run_command: git maintenance run --auto --quiet --detach`) landing in the
    canary between the probe's two fingerprint calls, and (b) an interaction with the probe's own
    fingerprint implementation, which hashes the canary's `index`, `config`, `HEAD` and
    `packed-refs` digests **and** the file-name list under `objects/`, `refs/`, `logs/`, `hooks/`,
    `info/` — a set that a detached maintenance run or an index refresh could alter without any
    semantic change to the repository.

## 6. Coverage findings for the L1

24. [obs] **The battery can only see the parity block, not its individual terms.** M02 and M03
    survive; M10 (dropping both) is killed. The committed controls establish "the parity block
    must compare something beyond `rc`", not "it must compare stdout" and not "it must compare
    the git-exec count".
25. [obs] **The loader-env channel cannot separate the three injected names.** M06 and M07
    survive for the same reason M05 survives. A target that scrubbed only `LD_PRELOAD` and left
    `LD_LIBRARY_PATH`/`PYTHONPATH` in place would read clean on this battery, even though the
    round's fix contract requires dropping all three prefixes. This is a *coverage* statement
    about the battery, not a defect in the probe: the probe's job is to catch a child carrying the
    inject path, and it does.
26. [obs] **Two harness guards (control-B determinism at line 300, "control run started no git
    child" at line 302) are unexercised** by the committed controls, so the mutants that remove
    them (M08, M09) survive. Closing those two holes needs new *fixtures* — a target that never
    starts a git child (for the git-child guard) and a target whose two control runs disagree (for
    the determinism guard) — not new probe logic.
27. [obs] **M04 is the one mutant whose kill direction matters for the round's own claim.** A
    probe variant that counted the tool's own first execve as a leaking descendant would report
    the genuine fix H2 as leaking. The frozen probe at `8cff9e7c…` excludes it correctly; this
    must be preserved by any refactor of `one_run`/`parity`.
28. [obs] **The dotgit-pointer channel should not be used as a one-shot gate.** Two spurious
    `canary fingerprint changed` verdicts in 121 runs, one of them on the genuine-fix lane state,
    means a single run of the probe can report "H2 leaks" for a correct H2. [inf] A repeated-read
    rule (require the verdict to be stable over ≥2 runs, or make the canary fingerprint immune to
    background maintenance) would remove that risk; this is a coverage/robustness observation
    about the frozen probe, and the frozen bytes are not changed by this seat.

## 7. Deliverables

29. [obs] Under `.ufo/waves/round-31/w1/MutProbeC2/`:
    `mutants/` (the ten mutant copies plus `DIAG-canary-diff.py`, and `manifest.json` with each
    sha256 and diff), `mutant-diffs.md`, `mutant-table.md`, `survivor-table.md`, `survivors.txt`,
    `mutant-results.json`, `runs/` (37 raw probe JSONL outputs plus `index.tsv` of exit codes),
    `flake/`, `flake2/`, `flake3/`, `flake4/`, `diag/` (the re-run campaigns of §5), and the
    scripts `make_mutants.py`, `run_matrix.sh`, `analyze.py`, `survivors.py`, `write_diffs.py`,
    `flake_recheck.sh`, `flaky_dotgit.py`, `gc_race.py`, `canary_stability.py`,
    `watch_canary.py`, `watch_canary2.py`, `trace_canary.py`, `gitfile_discovery.py`.
30. [obs] The pristine probe was never modified: `sha256sum
    /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/probe-git-child-env-r31.py` and
    `…/MutProbeC2/repo/tools/probe-git-child-env-r31.py` both give
    `b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0` after the whole campaign,
    equal to the committed receipts' `probe_sha256`.
31. [obs] No file outside this seat's paths was written except the report at
    `.ufo/waves/round-31/w1/MutProbeC2.md`. `git -C …/tsukuroi-shokunin status --porcelain` at
    the end of the seat lists this seat's two paths (`.ufo/waves/round-31/w1/MutProbeC2.md` and
    `.ufo/waves/round-31/w1/MutProbeC2/`) plus sibling seats' paths (`SentinelChildEnv`,
    `SentinelRepoLocal`, `MutCounterC1`, `RevDeclaration`,
    `.ufo/waves/round-31/measure/after-13ca52d0/`) — this seat wrote none of those. Per the L1's
    containment reminder, no git write (`add`/`commit`/`push`) was run in the lane or the fleet
    repo; the L1 integrates.

Scope: read=`tools/probe-git-child-env-r31.py`, `tools/check-kernel-taint.py`, the committed C2 control patches and receipts under `.ufo/waves/round-31/measure/controls/c2/`, `corpus/lessons/round-30-verifier-spotcheck.md` §5; wrote=`.ufo/waves/round-31/w1/MutProbeC2.md` and `.ufo/waves/round-31/w1/MutProbeC2/**` (mutants, diffs, tables, raw runs, re-run campaigns, scripts), sandbox writes under `/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/**`; executed=`git clone --no-local` + `git apply`/`commit` in the sandbox clone only (branches `mut/h1`, `mut/h2`), `python3` of the ten mutant copies and the pristine probe against base/H1/H2 with `--only check-kernel-taint.py`, re-run campaigns (121 probe runs total), `python3 -m py_compile` on each mutant, `sha256sum`, `diff -u`, `git status --porcelain` (read-only).
Model: not exposed
Installs: none
