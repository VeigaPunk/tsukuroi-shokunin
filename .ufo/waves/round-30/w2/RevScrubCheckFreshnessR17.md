# RevScrubCheckFreshnessR17 — attack on the C2 fix in tools/check-freshness-r17.py

Verdict: **holds** — every git-spawning call site in the fixed tool follows the round-30 GIT CHILD ENV CONTRACT, the probe-exercised `--selftest` behavior is byte-identical to 8976ca92, the fix is not hollow, and the probe passes 0/3 with the declared probe sha.

Findings:

1. No escape [obs]. The fixed file (sandbox clone at 29bf87fa3971df04cb96e4ad9a28805d8154ed2f) has exactly two subprocess sites: tools/check-freshness-r17.py:360 (`git_in`, `env=git_env(tmp)`) and :537 (selftest child, `env=git_env(env_tmp)`); grep for `subprocess|Popen|os.system|check_call|check_output|spawn` finds no others. All four `_revision` call sites (:525, :800, :802, :807) go through `revision_call`, which monkey-patches `_revision.clean_env`; tools/_revision.py:73 and :91 resolve `clean_env()` by module-global lookup at spawn time, so those git children receive the full contract env (GIT_* stripped, private HOME/XDG_CONFIG_HOME, PATH=/usr/bin:/bin, GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL/SYSTEM=/dev/null, GIT_CEILING_DIRECTORIES). The `isolate` keyword is fully removed and `os.environ` is read only inside `git_env` (:329-330). Python children that run git: only the :537 child, which inherits the contract env and re-applies it transitively in its own helpers.

2. Behavior otherwise unchanged [obs]. The probe's mode for this target is `--selftest` (tools/probe-git-env-residual-r30.py:57). Run at 8976ca92 (old file plus its period `_revision.py` extracted beside it) and at 29bf87fa in the sandbox, both exit 0 with byte-identical 67-byte stdout `CHECK_FRESHNESS_R17_SELFTEST: PASS (59 cases, 59 passed, 0 failed)` and empty stderr; stdout contains no temp paths or 40-hex ids, so normalization is the identity. The identical case count (59/59) shows no assertion was dropped or skipped. Note: my first old-version run exited 1 with `ModuleNotFoundError: No module named '_revision'` — my extraction artifact (missing sibling module), not a tool defect; the rerun above is the valid comparison.

3. Not hollow [obs + inf]. No exit-code swallowing: `git_in` still raises `Cannot` on timeout/OSError (:363-366) and selftest exit reflects failures identically at both revisions. No early return on odd HOME: `git_env` unconditionally replaces HOME (:328-338) and the only env filtering is the GIT_* strip. The fix mechanistically blocks all three probe channels — path-wrapper via PATH=/usr/bin:/bin, user-files via private HOME/XDG plus devnull configs plus GIT_CONFIG_NOSYSTEM, enclosing-repo because every repo-touching spawn uses `-C` sandbox paths and the only cwd-dependent git call (tools/_revision.py:89, check-ref-format) writes nothing.

4. Probe run [obs]. `python3 tools/probe-git-env-residual-r30.py --revision 29bf87fa3971df04cb96e4ad9a28805d8154ed2f --lane /fast/scratch/hyaku/tsukuroi-r30/RevScrubCheckFreshnessR17/repo --only tools/check-freshness-r17.py` (sandbox clone, GIT_* unset, exit 0, 2.5 s):
```
{"tool": "tools/check-freshness-r17.py", "channel": "path-wrapper", "argv": ["--selftest"], "control_rc": 0, "channel_rc": 0, "evidence": [], "leak": false}
{"tool": "tools/check-freshness-r17.py", "channel": "user-files", "argv": ["--selftest"], "control_rc": 0, "channel_rc": 0, "evidence": [], "leak": false}
{"tool": "tools/check-freshness-r17.py", "channel": "enclosing-repo", "argv": ["--selftest"], "control_rc": 0, "channel_rc": 0, "evidence": [], "leak": false}
{"revision": "29bf87fa3971df04cb96e4ad9a28805d8154ed2f", "targets": 1, "channels": ["path-wrapper", "user-files", "enclosing-repo"], "pairs": 3, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c", "scratch": "/fast/scratch/hyaku/git-env-residual-ivijtyz5"}
```
probe_sha256 c8f61996… matches the declared probe identity.

5. Main path sanity [obs]. The fixed tool's `--revision 29bf87fa…` run in the sandbox clone exits 0: `{"status": "PASS", "record_count": 48, "resolved_records": 48, "branch_tip": "7165f11e7bd9bf06ac6b998fa820803d6ef4a3b2", "findings": []}` — the fix did not break the mode the probe does not exercise.

6. Residual risks, none rising to a defect [inf]. (a) `revision_call`'s monkey-patch is process-global and not reentrant or thread-safe; safe today (single-threaded, no nested revision_call), a maintenance fragility only. (b) The :537 child env omits the GIT_OPTIONAL_LOCKS/GIT_PAGER/LC_ALL additions (base `git_env` only) — not a contract violation; the child re-adds them in its own helpers. (c) PATH hardcodes /usr/bin:/bin, matching the probe's SYSTEM_GIT assumption; on a host with git elsewhere the tool fails loudly (E-GIT-FAILED), never silently passes. (d) XDG_CONFIG_HOME points at a directory `git_env` never creates; git tolerates missing config dirs, harmless.

Verification gaps [unk]: `--registry-from` mode was not executed, and the comparison covers the `--selftest` and `--revision` modes only; no gap on contract coverage — both spawn sites and all `_revision` sites were verified individually.

Scope: read=lane diff 8976ca92..29bf87fa (tools/check-freshness-r17.py), SCORECARD.md:1139-1142, sandbox copies of probe-git-env-residual-r30.py, check-freshness-r17.py, _revision.py; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevScrubCheckFreshnessR17.md, /fast/scratch/hyaku/tsukuroi-r30/RevScrubCheckFreshnessR17/{old-check-freshness-r17.py,_revision.py,out/*}; executed=read-only git show/diff in lane, sandbox clone+checkout at 29bf87fa, --selftest at both revisions, probe --only, --revision smoke run
Model: zai/glm-5.3-flash
Installs: none
