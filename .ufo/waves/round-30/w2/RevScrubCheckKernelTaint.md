# RevScrubCheckKernelTaint — attack on the C2 fix in tools/check-kernel-taint.py

Verdict: holds. The C2 fix in tools/check-kernel-taint.py at
29bf87fa3971df04cb96e4ad9a28805d8154ed2f covers every git subprocess the tool or its
helper can spawn, preserves observable behaviour in both modes I exercised, is not
hollow, and passes the declared probe 0-of-3 with no harness error.

## Findings

1. Coverage — every git call site is under the contract [obs].
   `tools/check-kernel-taint.py` contains five `subprocess.run` sites, all git:
   `GitReader._run` (new file lines 287-291, `env=git_env(tmp)` with a fresh
   TemporaryDirectory per call) and the four `run_fixture` calls (lines
   1019-1030, all `env=env` where `env = git_env(tmp)` at line 1018). Grep of the
   new file for `subprocess|Popen|os.system|check_output|sys.executable|spawn`
   finds no other child-process path. The only other git child is inside
   `tools/_revision.py` (`_git`, `validate_branch`, `selftest`), all of which use
   the module-level `clean_env()`; `main` now calls `revision_bind` (lines
   269-277) which monkey-patches `_revision.clean_env` to return `dict(env)` of a
   hardened `git_env` env for the duration of `bind` and restores it in a
   `finally`. `tools/_revision.py` is byte-identical between 8976ca92 and the tip
   (`git log 8976ca92..29bf87fa -- tools/_revision.py` empty; the only commit
   touching the tool is a3f1937).
   `git_env` (lines 249-266) strips every `GIT_*` from the inherited environment
   and sets `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`,
   `GIT_CONFIG_SYSTEM=/dev/null`, `HOME`/`XDG_CONFIG_HOME` to a fresh `home/`
   mkdir'd inside the temp dir, `PATH=/usr/bin:/bin`,
   `GIT_CEILING_DIRECTORIES=<parent of the temp dir>` (so discovery cannot climb
   from a temp fixture into an enclosing canary repo), `GIT_OPTIONAL_LOCKS=0`,
   `GIT_PAGER=cat`, `LC_ALL=C`. That closes all three probed channels:
   PATH-pinned children bypass any wrapper, per-user config/hooks/ignore files
   are unreachable, and enclosing-repo discovery is cut at the temp tree.

2. Behaviour unchanged in the probe's mode [obs].
   The probe's TARGETS entry is `('tools/check-kernel-taint.py', ['--selftest'])`
   (tools/probe-git-env-residual-r30.py:58). I exported the tree at 8976ca92 to
   /fast/scratch/hyaku/tsukuroi-r30/RevScrubCheckKernelTaint/old-tree/ via
   `git archive` (read-only) and ran `--selftest` on old and new under an
   identical minimal env (`env -i HOME=<scratch>/env-home
   XDG_CONFIG_HOME=<scratch>/env-home/.config TMPDIR=<scratch>/env-tmp
   PATH=/usr/bin:/bin LANG=C`):
   - old: exit 0, 8706 bytes stdout, status PASS, 56 cases, 0 failed.
   - new: exit 0, 8706 bytes stdout, status PASS, 56 cases, 0 failed.
   - `diff` of the two outputs byte-identical (no temp paths or 40-hex ids
     present, so normalisation was a no-op).
   Evidence files copied to this seat dir as old-selftest.out / new-selftest.out.

3. Behaviour unchanged in `--revision` mode (bind path exercises the
   monkey-patched `_revision.clean_env`) [obs].
   `python3 <tool> --repo <sandbox clone> --revision
   29bf87fa3971df04cb96e4ad9a28805d8154ed2f` under the same minimal env: both old
   and new exit 0 and print the identical JSON evaluation (old-rev.out /
   new-rev.out, `REVMODE_IDENTICAL`). The new `revision_bind` yields the same
   binding and `GitReader` reads the same tree.

4. Not hollow [obs].
   - No exit-code swallowing: the fixture `git init`/`add`/`commit`/`rev-parse`
     keep `check=True`; a failed git raises `CalledProcessError`, caught by
     `selftest`'s `except Exception` which marks the case `pass: False` and
     increments `failed` — so the run fails loudly instead of passing the probe.
     `--revision` mode keeps `except _revision.RevisionError` → CANNOT_EVALUATE
     exit 2, which the probe counts as a harness error, not a pass.
   - No early return keyed on HOME: `git_env` unconditionally mkdirs `home/`
     inside the temp dir and overwrites `HOME`; it never inspects the caller's
     HOME and never short-circuits.
   - The selftest really executed git: 56 cases ran in ~1.4 s and the reported
     `verified_rows` values (6 and 5 across cases) match the old run exactly —
     the same work is being done.
   - The `--revision` path's monkey-patch is restored in `finally`, so the
     non-bind code path is untouched [obs].
   - Minor cost, not a defect: `GitReader._run` creates one TemporaryDirectory
     per git read [obs]; `_revision.clean_env` is mutated globally for the
     duration of `bind` (single-threaded here) [obs].

5. Declared probe run [obs].
   `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3
   tools/probe-git-env-residual-r30.py --revision
   29bf87fa3971df04cb96e4ad9a28805d8154ed2f --lane
   /fast/scratch/hyaku/tsukuroi-r30/RevScrubCheckKernelTaint/repo --only
   tools/check-kernel-taint.py` printed, as its last line:

   {"revision": "29bf87fa3971df04cb96e4ad9a28805d8154ed2f", "targets": 1,
   "channels": ["path-wrapper", "user-files", "enclosing-repo"], "pairs": 3,
   "leaking": 0, "leaking_pairs": [], "harness_errors": [],
   "probe_sha256": "c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c",
   "scratch": "/fast/scratch/hyaku/git-env-residual-gjt_o7kz"}

   All three (tool, channel) pairs report `"leak": false`, `channel_rc` 0 ==
   `control_rc` 0. The probe sha256 c8f61996… matches the declared frozen probe.

6. Residual risk / gaps [inf].
   - I exercised `--selftest` (the probed mode) and `--revision`; no other mode
     exists (mutually exclusive group). No callers of the tool's internals were
     checked beyond the probe's TARGETS, since the tool is a leaf checker.
   - The monkey-patch approach depends on `bind` being the only `_revision` git
     user in the non-selftest path; grep confirms `main` calls nothing else from
     `_revision` before/after `bind` in either mode [obs].

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-kernel-taint.py (at 8976ca92 and 29bf87fa), tools/_revision.py, tools/probe-git-env-residual-r30.py, SCORECARD.md round-30 declaration; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevScrubCheckKernelTaint.md plus old-selftest.out, new-selftest.out, old-rev.out, new-rev.out in the same dir, and scratch under /fast/scratch/hyaku/tsukuroi-r30/RevScrubCheckKernelTaint/; executed=git clone/archive/log/diff (read-only on the lane, checkout in the sandbox clone), python3 selftest and --revision runs, python3 tools/probe-git-env-residual-r30.py --only tools/check-kernel-taint.py
Model: devin/swe-2
Installs: none
