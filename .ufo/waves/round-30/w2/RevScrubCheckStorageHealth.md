# RevScrubCheckStorageHealth — C2 fix review: tools/check-storage-health.py

Verdict: holds. The C2 fix in tools/check-storage-health.py covers every git child
call site, behaviour is unchanged (byte-identical stdout at both modes tested), the
fix is not hollow, and the declared probe run shows 0 of 3 pairs leaking with exit 0.

## Findings

1. [obs] Diff 8976ca92 → 29bf87fa3971df04cb96e4ad9a28805d8154ed2f is purely additive:
   `import os`, a module-level `tempfile.TemporaryDirectory` sandbox home, a new
   `clean_env()`, and `_revision.clean_env = clean_env` (tools/check-storage-health.py:56-78
   at the tip). No control flow, no early return, no except-swallowing was added or
   removed. Diff obtained via `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
   diff 8976ca92 29bf87fa -- tools/check-storage-health.py`.

2. [obs] Call-site audit (grep of every subprocess spawn in both files, tip revision):
   - tools/check-storage-health.py:275-277 GitReader._run passes
     `env=_revision.clean_env()` → resolves to the patched clean_env.
   - tools/check-storage-health.py:993-1004 the four selftest git children
     (`init`, `add -A`, `commit`, `rev-parse HEAD`) all pass `env=env` where
     `env = dict(_revision.clean_env())` at line 992.
   - tools/_revision.py every subprocess.run calls the module-global `clean_env()`
     (lines 71-73, 89-91, 211-213, 392-394, 404-410 and all selftest `run()` calls),
     so the monkeypatch at check-storage-health.py:78 applies to `_revision.bind()`
     (check-ref-format, rev-parse, merge-base) and to any `_revision` selftest git
     writes as well. `env=clean_env()` is looked up at call time, after the patch.
   No call site escapes: `grep -n "subprocess.run" ... | grep -v "env="` finds none
   without env (the multi-line invocations list env on their own continuation lines;
   each of the 5 tool sites was read verbatim and all carry env). The tool spawns no
   other python child and no non-git subprocess.

3. [obs] The contract itself defeats all three probe channels:
   `GIT_*` stripped, `PATH=/usr/bin:/bin` (path-wrapper: probe's fake `git` earlier on
   PATH is never resolved), `HOME`/`XDG_CONFIG_HOME` redirected into a private
   TemporaryDirectory plus `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`,
   `GIT_CONFIG_NOSYSTEM=1` (user-files: canary `.gitconfig`, `.config/git/config`,
   `git/ignore` `*` and `git/attributes` are all unreachable), and
   `GIT_CEILING_DIRECTORIES` = parent of the private sandbox = inside TMPDIR
   (enclosing-repo: upward discovery from the fixture repos is capped below any
   enclosing repository). PATH pinning to /usr/bin:/bin is a hardcoded trade-off
   shared by the contract; it assumes git lives there (true on this host,
   /usr/bin/git). [inf]

4. [obs] Behaviour unchanged. The probe's mode for this tool is `--selftest`
   (tools/probe-git-env-residual-r30.py:61 TARGETS entry). Runs against exported trees:
   - old 8976ca92: `python3 .../old/tools/check-storage-health.py --selftest` →
     exit 0, stdout 6859 bytes (`PASS`, 44 cases, 0 failed).
   - new 29bf87fa: same command on the clone → exit 0, stdout byte-identical
     (6859 bytes) even before normalising; after sed normalisation of
     `/tmp/tsukuroi-sh-st-*`, `storage-health-git-*` and 40-hex ids the outputs are
     identical (`diff` exit 0, printed STDOUT_IDENTICAL).
   - Also compared `--revision 8976ca92 --repo <clone>` mode (not the probe's mode,
     extra assurance): exit 0 both, stdout identical after 40-hex normalisation.
   Artifacts: /fast/scratch/hyaku/tsukuroi-r30/RevScrubCheckStorageHealth/
   selftest-{old,new}.json, rev-{old,new}.json.

5. [obs] Not hollow. `run_fixture` still invokes each git write with `check=True`,
   so a blocked or failing git child raises, the case records `pass: False`, and the
   tool exits 1 — the fix cannot pass the probe by skipping work. There is no
   HOME-based early return; the new code only builds the env dict. The selftest at
   the tip still exercises all 44 fixture cases including the git-writing commits
   (the before-receipt shows the selftest's `git -C …/repo add -A` calls were the
   leaking children in the path-wrapper channel, so the same work is being done now,
   just under the scrubbed env).

6. [obs] Probe run (declared probe sha c8f61996…, matching the declared value):
   `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/probe-git-env-residual-r30.py
   --revision 29bf87fa3971df04cb96e4ad9a28805d8154ed2f --lane
   /fast/scratch/hyaku/tsukuroi-r30/RevScrubCheckStorageHealth/repo --only
   tools/check-storage-health.py` → exit 0; summary line:
   `{"revision": "29bf87fa3971df04cb96e4ad9a28805d8154ed2f", "targets": 1,
   "channels": ["path-wrapper", "user-files", "enclosing-repo"], "pairs": 3,
   "leaking": 0, "leaking_pairs": [], "harness_errors": [],
   "probe_sha256": "c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c",
   "scratch": "/fast/scratch/hyaku/git-env-residual-262i7z02"}`
   Each channel row: control_rc 0, channel_rc 0, evidence empty, leak false.

7. [obs] Before-state confirms the channels were real for this tool:
   .ufo/waves/round-30/measure/c2-before-8fb2cef081787ccb52b38e9f74d95d2a480de18f.jsonl
   shows check-storage-health.py leaking on path-wrapper (canary log captured
   `-C …/tsukuroi-sh-st-*/repo` init/add calls) and on user-files (channel_rc 1 vs
   control 0 — the canary `ignore=*` emptied the `add -A` staging and `commit`
   failed), enclosing-repo already clean. The tip now reports all three clean.

Residual risk: [unk] GIT_CEILING_DIRECTORIES is pinned to the TemporaryDirectory
parent, so if TMPDIR itself lived inside a repo whose discovery the tool needed it
would still block it — but the tool never relies on upward discovery (`--repo` always
names the directory holding .git directly; selftest repos are freshly init'ed), so
no reachable regression was found. [inf] The monkeypatch of `_revision.clean_env` is
unusual style but correct: it is assigned at import time before any use, and every
caller resolves the attribute dynamically.

Scope: read=SCORECARD.md round-30 declaration, corpus/lessons/round-29-verifier-spotcheck.md §5, tools/check-storage-health.py and tools/_revision.py at 8976ca92 and 29bf87fa (sandbox clone), tools/probe-git-env-residual-r30.py, c2 before/after receipts; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevScrubCheckStorageHealth.md plus scratch artifacts under /fast/scratch/hyaku/tsukuroi-r30/RevScrubCheckStorageHealth/; executed=git clone/diff/archive/cat-file/merge-base (read-only, env-scrubbed), python3 check-storage-health.py --selftest and --revision at both revisions from exported/cloned trees, python3 probe-git-env-residual-r30.py --only tools/check-storage-health.py, grep/sed/diff on outputs
Model: not exposed
Installs: none
