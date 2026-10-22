# RevScrubMutantsKernelTaint — C2 attack on tools/mutants-kernel-taint.py (8976ca92 → 29bf87fa)

**Verdict: holds.** The C2 fix in `tools/mutants-kernel-taint.py` covers every git
subprocess and its one python child, is behaviourally transparent (byte-identical
normalized stdout, same exit code), is not hollow, and the declared probe reports
0 of 3 pairs leaking for this target.

## Findings

1. **Coverage — no call site escaped.** The file at 29bf87fa has exactly five
   process-spawning sites, all carrying `env=clean_env()`:
   `_export()` git rev-parse/archive/show at
   `tools/mutants-kernel-taint.py:63-74`, the `git()` wrapper at lines 90-93
   (used by `setup()` lines 100-104 and `run()` lines 140-149, plus the
   `check=False` recovery at line 381), and the counter child
   `subprocess.run([sys.executable, TOOL, ...], env=clean_env())` at lines
   146-148. Greps for `subprocess|Popen|os.system|os.exec|spawn|check_output`
   and for the literal `git` token find no other spawn; `shutil.copytree`,
   `tarfile.extractall`, `write_bytes` are in-process. The only python child
   (`check-kernel-taint.py`) both inherits the sanitized env and implements the
   same contract itself (`tools/check-kernel-taint.py:252-265` builds GIT_*-free
   env with private HOME, fixed PATH, GIT_CEILING_DIRECTORIES; every subprocess
   at lines 289-291 and 1019-1030 passes it).

2. **Contract contents — fix matches.** `clean_env()` now strips inherited
   `GIT_*`, adds `GIT_CONFIG_NOSYSTEM/GLOBAL/SYSTEM` isolation, private `HOME`
   (=`SEAT/home`, `HOME.mkdir()` at line 52 runs before any subprocess),
   `XDG_CONFIG_HOME`, fixed `PATH=/usr/bin:/bin`, and
   `GIT_CEILING_DIRECTORIES=str(SEAT.parent)` (lines 32-38). This is exactly what
   blocks the three probe channels: PATH-reset defeats the path-wrapper canary,
   private HOME+devnull global config defeat user-files hooks, and
   ceiling-directories stop repository discovery at `TMPDIR`'s parent when the
   probe sets `TMPDIR=<canary>/tmp` in the enclosing-repo channel (all git work
   happens under `SEAT=mkdtemp()`, and `_export`'s `git -C ARGS.lane` targets the
   bare clone directly, so discovery never walks into the canary). The added
   `-c user.name=CritC1Tool -c user.email=seat@invalid` per-invocation flags in
   `git()` (lines 91-92) make commits independent of ambient config even if
   `GIT_CONFIG_*` were weakened later; `setup()` still writes repo config, so
   identity is belt-and-suspenders, not a substitute. [obs]

3. **Transparency — stdout and exit code unchanged.** Ran the probe's own
   argv (`--base <rev> --counter-rev <rev> --lane <clone>`), controlled env
   (`HOME`, `XDG_CONFIG_HOME`, `TMPDIR`, `PATH=/usr/bin:/bin`, `LC_ALL=C`,
   `GIT_*` unset), three executions, each rc 0, each 25 stdout lines, empty
   stderr:
   - A: `mut-kt-8976ca92.py` (bytes of `git show 8976ca92:tools/mutants-kernel-taint.py`)
     with base/counter 29bf87fa → `/fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsKernelTaint/runA-out.log`
   - B: tip script with base/counter 29bf87fa → `runB-out.log`
   - C: tip script with base/counter 8976ca92 → `runC-out.log`
   After normalising `mut-kt-*` tmpdirs and 40-hex ids, `diff runA.norm
   runB.norm` is empty (rc 0) — the patch changes no observable output. B vs C
   differ only in the `base`/`counter_rev`/`counter_sha256` fields, i.e. the
   input revisions, never in structure or verdicts. [obs]

4. **Not hollow.** No early return, no HOME-conditional skip, no new
   try/except: the patch is purely additive env hygiene plus `-c` flags. Real
   work is evidenced by runB's output — 24 mutant lines each with real
   `exit`/`verified_rows`/`blocking` findings (e.g.
   `"pipe_quote_control_no_pipe", "exit": 1, "verified_rows": 5, "blocking":
   ["KT-QUOTE-TOO-SHORT"]`), summary `control_exit:0,
   control_verified_rows:6, should_fail_total:5, should_fail_accepted:0,
   harness_errors:[]`
   (`runB-out.log:25`). Exit-code swallowing is impossible to hide: the probe
   compares `channel_rc` to `control_rc`, and all observed rc values are 0.
   `check=False` at line 381 predates the patch and only guards the cleanup
   checkout inside the harness-error path. [obs]

5. **Probe run (declared probe, sha256 c8f61996… matches lane bytes).**
   Command (from `/fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsKernelTaint/repo`):
   `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3
   tools/probe-git-env-residual-r30.py --revision
   29bf87fa3971df04cb96e4ad9a28805d8154ed2f --lane
   /fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsKernelTaint/repo --scratch
   /fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsKernelTaint/probe-scratch
   --only tools/mutants-kernel-taint.py` → rc 0, stderr empty. All three
   channel results: `control_rc:0, channel_rc:0, evidence:[], leak:false`.
   Summary line:
   `{"revision": "29bf87fa3971df04cb96e4ad9a28805d8154ed2f", "targets": 1,
   "channels": ["path-wrapper", "user-files", "enclosing-repo"], "pairs": 3,
   "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256":
   "c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c",
   "scratch":
   "/fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsKernelTaint/probe-scratch/git-env-residual-_64gi_8c"}`
   (full log: `/fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsKernelTaint/probe-out.log`).
   `--scratch` was added to keep the probe's internal bare clone inside the
   assigned seat scratch instead of the default `/fast/scratch/hyaku` root;
   the probe itself strips `GIT_*` from its own env (`probe…r30.py:75-78`). [obs]

## Residual risk / gaps

- [inf] Grandchild git calls belong to `check-kernel-taint.py`'s own contract
  compliance, which is a sibling target's responsibility; within this file the
  child's env is sanitized regardless.
- [inf] `clean_env()` still inherits `TMPDIR` (deliberately — the probe's
  enclosing-repo channel relies on it) and other non-GIT vars like `LC_ALL`;
  neither affects the three channels.
- [obs] Lane branch tip has moved to `32e5d848c5fcd0246b9dfb56eadc50fea024d501`
  since the assignment; verified `sha256(tip file)=sha256(29bf87fa
  file)=c61e00d2…` for `tools/mutants-kernel-taint.py`, so the attacked bytes
  are unchanged.
- [unk] Nothing found that would falsify C2 for this target.

Scope: read=lane diff 8976ca92→29bf87fa for tools/mutants-kernel-taint.py, full
new/old file audits, probe + counter sources; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevScrubMutantsKernelTaint.md plus scratch artifacts under /fast/scratch/hyaku/tsukuroi-r30/RevScrubMutantsKernelTaint/ (clone, mut-kt-8976ca92.py, run{A,B,C}-out/err.log, run{A,B,C}.norm, probe-out/err.log, probe-scratch/); executed=git diff/cat-file/show/rev-parse (read-only), clone+checkout in seat scratch, 3× python3 mutants-kernel-taint.py, 1× python3 probe-git-env-residual-r30.py --only tools/mutants-kernel-taint.py, sha256sum, diff, sed normalization
Model: devin/swe-2
Installs: none
