# RevScrubCheckMemoryPressure — C2 fix review for tools/check-memory-pressure.py

Verdict: holds. The C2 fix in `tools/check-memory-pressure.py` covers every git
subprocess, behaviour is byte-identical in the probed mode, the fix does the work
rather than faking it, and the declared probe reports 0/3 leaking pairs at
29bf87fa3971df04cb96e4ad9a28805d8154ed2f.

## 1. Call-site coverage (no escape found)

Every subprocess call in the file is a git invocation and every one receives the
contract env. Call-site census at 29bf87f (sandbox clone
`/fast/scratch/hyaku/tsukuroi-r30/RevScrubCheckMemoryPressure/repo`):

- `git_reader` `git show` — line 142-144: `env=git_env(tmp)` under a per-call
  `TemporaryDirectory(prefix='memory-pressure-git-')`.
- `run_fixture` `git init` — line 905: `env=env` where `env = git_env(tmp)`
  (line 904).
- `run_fixture` `git add -A` — line 910: same env.
- `run_fixture` `git commit` — lines 911-913: same env, identity via
  `-c user.name=… -c user.email=… -c commit.gpgsign=false`.
- `run_fixture` `git rev-parse HEAD` — lines 914-915: same env.
- `_revision.bind` git calls — `main` line 1143 now calls `revision_bind`
  (lines 120-131), which monkey-patches `_revision.clean_env` to return
  `dict(git_env(tmp))` for the duration of `_revision.bind` and restores it in
  `finally`. Verified that every subprocess in `tools/_revision.py` passes
  `env=clean_env()` (lines 71-73, 89-91, 211-213, 220, 392-394, 404-409); none
  bypass it. `_revision.py` is unchanged between 8976ca92 and 29bf87f
  (`git diff --stat 8976ca92 29bf87f -- tools/_revision.py` empty).

`git_env` (lines 103-117) matches the GIT CHILD ENV CONTRACT in
`.ufo/waves/round-30/w1-spec.json` point by point: drops all `GIT_*` names;
sets `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`,
`GIT_CONFIG_SYSTEM=/dev/null`; `HOME` = fresh dir `home` created inside the
tool's own temp dir; `XDG_CONFIG_HOME` = `HOME/.config`; `PATH=/usr/bin:/bin`;
`GIT_CEILING_DIRECTORIES` = parent of the tool temp dir. Commit identity is
passed explicitly. It also sets `GIT_OPTIONAL_LOCKS=0`, `GIT_PAGER=cat`,
`LC_ALL=C` — superset identical to `check-kernel-taint.py`'s copy (lines
249-265). No `sys.executable` children exist in this tool (grep for
`sys.executable`, `os.exec`, `Popen`, `spawn` returns nothing), so the
"python children" clause is vacuous here. Docstring line 43 names the contract
as required.

## 2. Behaviour unchanged

Probe mode is `--selftest` (TARGETS line 59 of
`tools/probe-git-env-residual-r30.py`). Ran:

    python3 <old-export>/tools/check-memory-pressure.py --selftest   (8976ca92)
    python3 <sandbox>/tools/check-memory-pressure.py --selftest     (29bf87f)

Both exit 0. Stdout is BYTE-IDENTICAL (`diff` reports no differences; both emit
`{"status":"PASS","cases":41,"failed":0,…}`); normalization was unnecessary.
Both stderrs empty. The `--revision` path also works: `--revision 29bf87f` in
the sandbox prints status PASS, verified_rows 6/6, exit 0.

## 3. Not hollow

- No new `return`/`exit` before the env build, no detection of probe conditions
  (`HOME`/`PATH`/canary markers) anywhere in the diff — the only changes are
  the new `git_env`/`revision_bind` helpers, env wiring, and one docstring line.
- Probe is non-vacuous for this tool: at 8976ca92 the same probe flags 2 of 3
  channels leaking (path-wrapper: 349 canary log lines; user-files: channel rc 1
  vs control 0; enclosing-repo clean). At 29bf87f all three are clean, so the
  diff itself removed a real leak.
- `check=True` on init/add/commit/rev-parse means a broken env fails fixtures,
  which marks cases failed (not PASS): a hollow env cannot produce the observed
  41/41 PASS plus rc 0 in both control and channels.
- `selftest()` output reports per-case findings/verified_rows; identical to the
  pre-fix output, so no work was skipped.

## 4. Probe summary (verbatim)

    {"tool": "tools/check-memory-pressure.py", "channel": "path-wrapper", "argv": ["--selftest"], "control_rc": 0, "channel_rc": 0, "evidence": [], "leak": false}
    {"tool": "tools/check-memory-pressure.py", "channel": "user-files", "argv": ["--selftest"], "control_rc": 0, "channel_rc": 0, "evidence": [], "leak": false}
    {"tool": "tools/check-memory-pressure.py", "channel": "enclosing-repo", "argv": ["--selftest"], "control_rc": 0, "channel_rc": 0, "evidence": [], "leak": false}
    {"revision": "29bf87fa3971df04cb96e4ad9a28805d8154ed2f", "targets": 1, "channels": ["path-wrapper", "user-files", "enclosing-repo"], "pairs": 3, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c", "scratch": "/fast/scratch/hyaku/git-env-residual-3l7_kci8"}

Probe rc=0; `probe_sha256` matches the declared `c8f61996…`.

## Residual risk / observations

- [obs] `revision_bind`/`git_reader` set `GIT_CEILING_DIRECTORIES` to the parent
  of the tool's temp dir, not the lane. For the `--revision` path run from an
  exported tree inside an enclosing repo, `git -C ROOT rev-parse --git-dir` can
  still climb to an enclosing `.git` and bind there — but this is identical
  pre-fix behaviour (8976ca92 did the same with no ceiling at all), the
  contract itself declares ceiling harmless for explicit `-C` paths, and the
  probed mode (`--selftest`) never touches ROOT. Not a regression; noted only.
- [obs] `_revision.py`'s own `clean_env` (HOME/PATH unset) is unchanged; tools
  that call `_revision.bind` without the `revision_bind` wrapper would still
  leak — irrelevant to this tool's claim, which wraps correctly.
- [unk] Nothing found that invalidates C2 for this target.

Scope: read=tools/check-memory-pressure.py, tools/_revision.py, tools/probe-git-env-residual-r30.py, tools/check-{adjacency-overlap,freshness-r17,kernel-taint}.py, .ufo/waves/round-30/w1-spec.json in lane clone and lane repo (read-only); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevScrubCheckMemoryPressure.md, /fast/scratch/hyaku/tsukuroi-r30/RevScrubCheckMemoryPressure/{diff.patch,selftest-old.json,selftest-old.err,selftest-new.json,selftest-new.err,tree-old/,repo/}; executed=git clone/checkout/archive/diff/log (read-only), python3 selftests and probe runs, grep/diff/json comparisons
Model: devin/swe-2
Installs: none
