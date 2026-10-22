# ScoutToolSites — subprocess inventory for C2 (data walk, no edits)

Verdict: done — all 34 Python subprocess sites in the eleven C2 targets, `tools/_revision.py`, and the two lane tools they start as children pass an explicit `env=` whose builder filters **only** `GIT_`; **none** drops `LD_*` or `PYTHON*`, and every bash descendant of `tools/tsukuroi-census.sh` inherits the same unscrubbed environment. There are **zero** sites that pass `env=None` in Python; the only inheritance path is bash's, via census.

Revision read: `8cff9e7cfb034b49c645d548801ac3185a827cb4` (sandbox clone `/fast/scratch/hyaku/tsukuroi-r31/ScoutToolSites/repo`, `git rev-parse HEAD` printed exactly that sha).

## Method

Read each file at the cloned revision with `read`/`grep` on the clone; no file in the lane was modified. Confidence `[obs]` = line read directly. No `lsp` server was queried for this walk because the answer is a call-site census (every hit is a literal `subprocess.run(` with a visible `env=` argument in the same statement or one frame up); this is recorded as a limitation, not as semantic proof of dynamic reachability.

## Table A — the eleven targets, `_revision.py`, and their children

Columns: site | program started | env argument | builder (file:line, filter) | LD_*/PYTHON* status.

| site (absolute path:line) | program | env argument at the call | builder | LD_/PYTHON status |
|---|---|---|---|---|
| tools/check-adjacency-overlap.py:229 | `git -C <repo> <args>` | `env=git_env(tmp)` | :210 `{... if not key.startswith('GIT_')}` | **UNSCRUBBED** |
| tools/check-freshness-r17.py:360 | `git --no-pager -C <root> <args>` | `env=git_env(tmp)` + `GIT_OPTIONAL_LOCKS/GIT_PAGER/LC_ALL` | :326, `GIT_` only | **UNSCRUBBED** |
| tools/check-freshness-r17.py:538 | `sys.executable <copy of check-freshness-r17.py> <args>` (selftest child, selftest copy at :494) | `env=git_env(env_tmp)` | :326, `GIT_` only | **UNSCRUBBED** (grandchild re-enters :360 and `_revision`) |
| tools/check-freshness-r17.py:347 | monkeypatch `_revision.clean_env = lambda: dict(env)`; routes `_revision.py:71`, `:89` | `env=git_env(tmp)` | :326, `GIT_` only | **UNSCRUBBED** |
| tools/check-kernel-taint.py:289 | `git --no-pager -C <repo> <args>` (`GitReader._run`) | `env=git_env(tmp)` | :249, `GIT_` only (+OPTIONAL_LOCKS/PAGER/LC_ALL) | **UNSCRUBBED** |
| tools/check-kernel-taint.py:1019 | `git init --quiet --initial-branch=master` | `env=git_env(tmp)` | :249 | **UNSCRUBBED** |
| tools/check-kernel-taint.py:1025 | `git -C <repo> add -A` | `env=git_env(tmp)` | :249 | **UNSCRUBBED** |
| tools/check-kernel-taint.py:1026 | `git -C <repo> -c user.name=selftest ... commit` | `env=git_env(tmp)` | :249 | **UNSCRUBBED** |
| tools/check-kernel-taint.py:1029 | `git -C <repo> rev-parse HEAD` | `env=git_env(tmp)` | :249 | **UNSCRUBBED** |
| tools/check-kernel-taint.py:273 | monkeypatch `_revision.clean_env` | `env=git_env(tmp)` | :249 | **UNSCRUBBED** |
| tools/check-memory-pressure.py:142 | `git --no-pager -C <repo> show <sha>:<path>` | `env=git_env(tmp)` | :103, `GIT_` only | **UNSCRUBBED** |
| tools/check-memory-pressure.py:905 | `git init --quiet <repo>` | `env=git_env(tmp)` | :103 | **UNSCRUBBED** |
| tools/check-memory-pressure.py:910 | `git -C <repo> add -A` | `env=git_env(tmp)` | :103 | **UNSCRUBBED** |
| tools/check-memory-pressure.py:911 | `git -C <repo> -c user.name=selftest ... commit` | `env=git_env(tmp)` | :103 | **UNSCRUBBED** |
| tools/check-memory-pressure.py:914 | `git -C <repo> rev-parse HEAD` | `env=git_env(tmp)` | :103 | **UNSCRUBBED** |
| tools/check-memory-pressure.py:127 | monkeypatch `_revision.clean_env` | `env=git_env(tmp)` | :103 | **UNSCRUBBED** |
| tools/check-registry-coverage.py:79 | `git --no-pager -C <root> <args>` (`GitReader._git`) | `env=clean_env()` | :29, `GIT_` only | **UNSCRUBBED** |
| tools/check-registry-coverage.py:456 | `git init --quiet -b master <repo>` | `env=clean_env()` | :29 | **UNSCRUBBED** |
| tools/check-registry-coverage.py:476 | `git -C <repo> add -A` | `env=clean_env()` | :29 | **UNSCRUBBED** |
| tools/check-registry-coverage.py:480 | `git -C <repo> -c user.name=Registry Selftest ... commit` | `env=clean_env()` | :29 | **UNSCRUBBED** |
| tools/check-registry-coverage.py:487 | `git -C <repo> rev-parse HEAD` | `env=clean_env()` | :29 | **UNSCRUBBED** |
| tools/check-registry-coverage.py:46 | module-level `_revision.clean_env = clean_env` | (rebinds the shared builder) | :29 | **UNSCRUBBED** |
| tools/check-storage-health.py:275 | `git --no-pager -C <repo> <args>` | `env=_revision.clean_env()` (rebound at :78 to local) | :61, `GIT_` only | **UNSCRUBBED** |
| tools/check-storage-health.py:993 | `git init --quiet --initial-branch=master <repo>` | `env=dict(_revision.clean_env())` | :61 via :78 | **UNSCRUBBED** |
| tools/check-storage-health.py:999 | `git -C <repo> add -A` | `env=env` (dict of `_revision.clean_env()`) | :61 via :78 | **UNSCRUBBED** |
| tools/check-storage-health.py:1000 | `git -C <repo> -c user.name=selftest ... commit` | `env=env` | :61 via :78 | **UNSCRUBBED** |
| tools/check-storage-health.py:1003 | `git -C <repo> rev-parse HEAD` | `env=env` | :61 via :78 | **UNSCRUBBED** |
| tools/check-storage-health.py:78 | module-level `_revision.clean_env = clean_env` | (rebinds shared builder) | :61 | **UNSCRUBBED** |
| tools/mutants-adjacency-overlap.py:56 | `git -C <lane> rev-parse --verify <base>^{commit}` | `env=clean_env()` | :18, `GIT_` only | **UNSCRUBBED** |
| tools/mutants-adjacency-overlap.py:58 | `git -C <lane> archive <rev>` | `env=clean_env()` | :18 | **UNSCRUBBED** |
| tools/mutants-adjacency-overlap.py:67 | `git -C <lane> show <counter-rev>:tools/check-adjacency-overlap.py` | `env=clean_env()` | :18 | **UNSCRUBBED** |
| tools/mutants-adjacency-overlap.py:80 | generic `sh(*a, cwd)` → `subprocess.run(list(a), cwd=..., env=clean_env())`; callers :84 `git -C <SBX> ...`, :220 `git -C <MORI sibling> cat-file`, and :122 `python3 <counter check-adjacency-overlap.py>` | `env=clean_env()` | :18 | **UNSCRUBBED** |
| tools/mutants-adjacency-overlap.py:122 | `python3 <SEAT>/counter/check-adjacency-overlap.py --repo <SBX> --revision <rev> --siblings-root <sib>` | `env=clean_env()` via :80 | :18 | **UNSCRUBBED** → child site `check-adjacency-overlap.py:229` |
| tools/mutants-kernel-taint.py:63 | `git -C <lane> rev-parse --verify <base>^{commit}` | `env=clean_env()` | :32, `GIT_` only | **UNSCRUBBED** |
| tools/mutants-kernel-taint.py:65 | `git -C <lane> archive <rev>` | `env=clean_env()` | :32 | **UNSCRUBBED** |
| tools/mutants-kernel-taint.py:73 | `git -C <lane> show <counter-rev>:tools/check-kernel-taint.py` | `env=clean_env()` | :32 | **UNSCRUBBED** |
| tools/mutants-kernel-taint.py:91 | `git -C <REPO> -c user.name=CritC1Tool ...` (sandbox commits/checkouts) | `env=clean_env()` | :32 | **UNSCRUBBED** |
| tools/mutants-kernel-taint.py:146 | `sys.executable <SEAT>/counter/check-kernel-taint.py --repo <REPO> --revision <sha> --branch m-<name>` | `env=clean_env()` | :32 | **UNSCRUBBED** → child sites `check-kernel-taint.py:289`, `:1019-1029` |
| tools/check-self-assessment.py:114 | `git -C <repo> ...` (composed `cmd`, `git()`) | `env=git_env()` | :92, `GIT_` only | **UNSCRUBBED** |
| tools/check-self-assessment.py:185 | `bash tools/tsukuroi-census.sh --selftest` (cwd = extracted archive; reached also from `--selftest` because `run_selftest`→`evaluate`→`census_case_count` :647) | `env=git_env()` | :92 | **UNSCRUBBED** (bash inherits it) → Table C |
| tools/check-self-assessment.py:1016 | `git init -q <repo>` | `env=git_env()` | :92 | **UNSCRUBBED** |
| tools/check-self-assessment.py:1022 | `git -C <repo> add -A` | `env=git_env()` | :92 | **UNSCRUBBED** |
| tools/check-self-assessment.py:1023 | `git -C <repo> -c user.name=fixture ... commit` | `env=git_env()` | :92 | **UNSCRUBBED** |
| tools/mutants-owed-statements-r29.py:49 | `git clone -q --no-local <lane> <repo>` | `env=ENV` | :40 dict, `GIT_` only | **UNSCRUBBED** |
| tools/mutants-owed-statements-r29.py:50 | `git -C <repo> rev-parse --verify <base>^{commit}` | `env=ENV` | :40 | **UNSCRUBBED** |
| tools/mutants-owed-statements-r29.py:55 | `git -C <lane> show <counter-rev>:tools/check-owed-statements-r29.py` | `env=ENV` | :40 | **UNSCRUBBED** |
| tools/mutants-owed-statements-r29.py:63 | `git -C <repo> -c user.name=shape ...` (sandbox) | `env=ENV` | :40 | **UNSCRUBBED** |
| tools/mutants-owed-statements-r29.py:76 | `sys.executable <check-owed-statements-r29.py> --revision HEAD --lane <repo>` | `env=ENV` | :40 | **UNSCRUBBED** → child site `check-owed-statements-r29.py:173` |
| tools/mutants-owed-statements-r29-landed.py:48 | `git clone -q --no-local <lane> <repo>` | `env=ENV` | :39 dict, `GIT_` only | **UNSCRUBBED** |
| tools/mutants-owed-statements-r29-landed.py:49 | `git -C <repo> rev-parse --verify <base>^{commit}` | `env=ENV` | :39 | **UNSCRUBBED** |
| tools/mutants-owed-statements-r29-landed.py:54 | `git -C <lane> show <counter-rev>:tools/check-owed-statements-r29.py` | `env=ENV` | :39 | **UNSCRUBBED** |
| tools/mutants-owed-statements-r29-landed.py:62 | `git -C <repo> -c user.name=shape ...` (sandbox) | `env=ENV` | :39 | **UNSCRUBBED** |
| tools/mutants-owed-statements-r29-landed.py:278 | `sys.executable <check-owed-statements-r29.py> --revision HEAD --lane <repo>` | `env=ENV` | :39 | **UNSCRUBBED** → child site `check-owed-statements-r29.py:173` |
| tools/_revision.py:71 | `git --no-pager -C <repo> <args>` (`_git`: used by `bind`, `branch_tip`, `_commit`, `_object_commit`, `_ancestor`, `_exists`) | `env=clean_env()` | :62, `GIT_` only | **UNSCRUBBED** |
| tools/_revision.py:89 | `git check-ref-format refs/heads/<branch>` | `env=clean_env()` | :62 | **UNSCRUBBED** |
| tools/_revision.py:211 | `git -C <repo> -c user.name=rev -c ... commit` (selftest) | `env=clean_env()` | :62 | **UNSCRUBBED** |
| tools/_revision.py:220 | `git init --quiet <repo>` (selftest) | `env=clean_env()` | :62 | **UNSCRUBBED** |
| tools/_revision.py:392 | `git -C <repo> hash-object -w --stdin` (ambiguous-prefix selftest blob) | `env=clean_env()` | :62 | **UNSCRUBBED** |
| tools/_revision.py:404 | `git -C <repo> hash-object -w --stdin` | `env=clean_env()` | :62 | **UNSCRUBBED** |
| tools/_revision.py:408 | `git -C <repo> mktree` | `env=clean_env()` | :62 | **UNSCRUBBED** |
| tools/check-owed-statements-r29.py:173 (child of both owed mutants) | `git -C <lane> <args>` (`git()`) | `env=clean_env(lane)` | :153, `GIT_` only; keeps ambient `HOME`/`XDG_CONFIG_HOME` (:156-166) | **UNSCRUBBED** |

Notes on Table A:
1. `[obs]` No site in Table A passes `env=None`: every `subprocess.run`/`Popen` call in the eleven, in `_revision.py`, and in `check-owed-statements-r29.py` supplies `env=`. The C2 contract's clause "a subprocess call that today passes no env= gets the same scrubbed environment" therefore has **no Python site** in this inventory; the only inheriting processes are bash's descendants in Table C.
2. `[obs]` Five of the eleven bind `tools/_revision.py` and then **override its builder**, so a change confined to `_revision.clean_env` would not reach their git children: `check-freshness-r17.py:347/351`, `check-kernel-taint.py:273/277`, `check-memory-pressure.py:127/131`, `check-registry-coverage.py:46`, `check-storage-health.py:78`. `check-adjacency-overlap.py`, `check-self-assessment.py`, and the four `mutants-*.py` do not import `_revision` at all.
3. `[obs]` Distinct environment constructors that need the `('GIT_', 'LD_', 'PYTHON')` filter: `check-adjacency-overlap.py:210`, `check-freshness-r17.py:326`, `check-kernel-taint.py:249`, `check-memory-pressure.py:103`, `check-registry-coverage.py:29`, `check-storage-health.py:61`, `mutants-adjacency-overlap.py:18`, `mutants-kernel-taint.py:32`, `check-self-assessment.py:92`, `mutants-owed-statements-r29.py:40`, `mutants-owed-statements-r29-landed.py:39`, `_revision.py:62`, `check-owed-statements-r29.py:153` — thirteen builders.
4. `[inf]` `check-owed-statements-r29.py:153` deliberately keeps the ambient `HOME`/`XDG_CONFIG_HOME` instead of a private one, unlike the round-30 contract. Widening its filter is safe for its output; replacing its `HOME` with a private directory is **not** obviously output-neutral and is not required to drop `LD_`/`PYTHON`. Flag for the executor, not a blocker.
5. `[inf]` Leak mechanism matches the probe's 11/11 loader-env reading: the tool's own `execve` is launched by the probe with `LD_PRELOAD=<inject>/libprobe-inject.so`, `LD_LIBRARY_PATH=<inject>`, `PYTHONPATH=<inject>`; every builder copies `os.environ` minus `GIT_`, so the first `git` child exec carries all three names. The child-contract and dotgit-pointer channels read 0 at base because `GIT_`/`GIT_CEILING_DIRECTORIES` isolation already holds.

## Table B — lane tools outside the eleven that import `tools/_revision.py`

Fifteen files contain `import _revision` and are not among the eleven. Column 3 says whether a change to `_revision.clean_env` reaches their children.

| tool | child env source | changes when `_revision.clean_env` changes |
|---|---|---|
| tools/check-boot-chain.py | own `{... if not k.startswith("GIT_")}` at :802 | **no** (imports `_revision` for `bind` only) |
| tools/check-boundary-contract.py | `env=_revision.clean_env()` at :198, :201 | **yes** |
| tools/check-edit-contract.py | `env=_revision.clean_env()` at :332, :335 | **yes** |
| tools/check-locator-clarification.py | own builder at :448 and :577 | **no** |
| tools/check-path-reconciliation.py | `env=_revision.clean_env()` at :257, :260 | **yes** |
| tools/check-pause-gate.py | `env=_revision.clean_env()` at :56 | **yes** |
| tools/check-recheck-commands.py | own builder at :799 | **no** |
| tools/check-review-cohort.py | `env=_revision.clean_env()` at :176, :179 | **yes** |
| tools/check-review-snapshots.py | `env=_revision.clean_env()` at :132, :136 | **yes** |
| tools/check-root-dac-correction.py | `{**_revision.clean_env(), **(identity or {})}` at :244, and `env=_revision.clean_env()` at :461 | **yes** (composed) |
| tools/check-seat-bindings.py | `env=_revision.clean_env()` at :371, :374 | **yes** |
| tools/check-selector-contract.py | `_clean_git_env()` derives from `_revision.clean_env()` at :84 | **yes** |
| tools/check-source-scope-correction.py | own builder at :355 | **no** |
| tools/measure-update-recheck.py | own builder at :438 and :485 | **no** |
| tools/report-red-causes.py | `env=_revision.clean_env()` at :59 | **yes** |

`[obs]` `tools/check-revision-binding.py` only mentions `import _revision` inside selftest fixture strings (:1109, :1282, :1286, :1288); it is not an importer.

## Table C — `tools/tsukuroi-census.sh`, started as a bash child by `check-self-assessment.py:185`

Bash has no `env=` argument; every child inherits the environment census itself received, i.e. `check-self-assessment.git_env()` (`GIT_`-filtered only). All rows are **UNSCRUBBED** for `LD_*`/`PYTHON*`.

| site (tools/tsukuroi-census.sh:line) | program started (default / fixture override) |
|---|---|
| :579, :594, :620, :1498, :1518, :1542, :1591, :1594 | `$PACMAN` / `$TSUKUROI_PACMAN` (`pacman` defaults; :352, overridden by fixtures via 1918) |
| :697 | `$PACMAN_CONF` (`pacman-conf`, :353) |
| :765, :774 | `env LC_ALL=C stat ...` (explicit `env` launcher, does not clear the rest) |
| :836, :853, :862, :875, :1322, :1381, :1391 | `$SYSTEMCTL` (`systemctl`, :362) |
| :902, :942 | `$DMESG` (`dmesg`, :363) |
| :920, :935, :1030, :1036, :1042, :1173, :1191, :1203, :1208, :1304, :1342, :1352 | `$JOURNALCTL` (`journalctl`, :364) |
| :954 | `$NVIDIA_SMI` (`nvidia-smi`, :365) |
| :964 | `$LSMOD` (`lsmod`, :366) |
| :1622 | `$EXPAC` (`expac`, via `TSUKUROI_EXPAC`) |
| :1918-1949 | `env <TSUKUROI_* fixture overrides> "$BASH" "$SELF"` — re-invokes the census itself with fixture commands; `env(1)` adds names, it does not clear `LD_*`/`PYTHON*` |
| :530, :704, :898, :1056, :1091, :1465, :1476, :1481, :1555, :1556, :1568, :1670, :2318, :2323, :2498, :2543, :2550, :2557, :2638, :2641 | non-`cap` external commands in the same script (`head`, `grep`, `awk`, `date`, `stat`, `tail`, `tr`, `touch`, `id`), all inheriting |

`[obs]` The census selftest path is reached in the probe run: `check-self-assessment.py --selftest` (:1090) → `run_selftest` (:1028) → `evaluate` (:431) → `census_case_count` (:647) → :185, once per fixture case (19 cases at :1030-1037). Each of those 19 `bash tools/tsukuroi-census.sh --selftest` runs its own `check` helper (a `cap`-driven case loop, :1910+), so one probe target expands into 19 census selftest runs, each exercising the 35-site `cap` surface and the `env "$BASH" "$SELF"` re-invocation.

## Observations, inferences, unknowns

- `[obs]` Every one of the eleven leaks by construction, matching the probe's base reading `11 of 33 leaking, all loader-env pairs`, because each tool's first child exec is a `git` started from a builder that copies `LD_*`/`PYTHON*` verbatim.
- `[obs]` `check-freshness-r17.py:538` and `mutants-kernel-taint.py:146` start copies of the tools themselves; `mutants-adjacency-overlap.py:122` starts `python3` (not `sys.executable`); `check-self-assessment.py:185` starts `bash`. These are the three ways a target re-enters the tool graph, so scrubbing the outer builder also cleans the inner run.
- `[inf]` Because the five `_revision`-overriding tools replace the shared builder, a fix that edits only `tools/_revision.py:62` would still leave `check-freshness-r17`, `check-kernel-taint`, `check-memory-pressure`, `check-registry-coverage`, `check-storage-health` leaking; the thirteen builders in Table A note 3 are the complete edit surface for the eleven plus children.
- `[inf]` Widening filters cannot change any tool's stdout/exit for the probe's channels: the dropped names (`LD_*`, `PYTHON*`) are not read by `git` or by the bash/Python children except as loader/import controls, and the probe's `child-contract` and `dotgit-pointer` channels already pass at base with `GIT_`-only filtering.
- `[unk]` I did not run the probe or any tool; the leak/no-leak reading per tool is taken from the round-31 declaration numbers, not re-measured by me. Dynamic reachability of each selftest-only site under the probe's exact argv is asserted from source paths, not from a trace.
- `[unk]` Whether any external `python3`/`bash` plugin or sitecustomize in the ambient environment reads `PYTHONPATH` inside the census subtree is not determinable from the lane.

## What this changes for the planner

- Edit surface for C2: the thirteen builders in Table A note 3; no `env=None` call exists, so no call sites need an `env=` added.
- Do not touch `tools/probe-git-child-env-r31.py` or `tools/check-btrfs-repair-r31.py` (C1 counter); no target starts either.
- `tools/check-owed-statements-r29.py:153` is a child counter started by both owed batteries, so it must be fixed too or the batteries keep leaking through their counter child.
- Collateral (not measured by the probe): Table B's ten `_revision.clean_env()` consumers change automatically; five importers with private builders do not and are outside the C2 contract.

Scope: read=tools/{probe-git-child-env-r31,check-adjacency-overlap,check-freshness-r17,check-kernel-taint,check-memory-pressure,check-registry-coverage,check-storage-health,mutants-adjacency-overlap,mutants-kernel-taint,check-self-assessment,mutants-owed-statements-r29,mutants-owed-statements-r29-landed,check-owed-statements-r29,_revision,tsukuroi-census.sh,check-revision-binding,check-boot-chain,check-boundary-contract,check-edit-contract,check-locator-clarification,check-path-reconciliation,check-pause-gate,check-recheck-commands,check-review-cohort,check-review-snapshots,check-root-dac-correction,check-seat-bindings,check-selector-contract,check-source-scope-correction,measure-update-recheck,report-red-causes}.py (relevant ranges only); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/ScoutToolSites.md, /fast/scratch/hyaku/tsukuroi-r31/ScoutToolSites/repo (sandbox clone); executed=git clone/checkout/rev-parse in /fast/scratch/hyaku/tsukuroi-r31/ScoutToolSites (HEAD 8cff9e7cfb034b49c645d548801ac3185a827cb4), grep/sed on the clone
Model: not exposed
Installs: none
