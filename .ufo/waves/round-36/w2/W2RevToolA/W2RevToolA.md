# W2RevToolA — per-tool behaviour review of the five C1 diffs

Seat: W2RevToolA (reviewer, leaf). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Diff under review: `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (declaration) → `c052bb7d41ced49aa888817069afd804eccfecf1` (C1 change).
Frozen counter: `tools/probe-child-env-allowlist-r36.py` VERSION 7, sha256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` (bytes at `1e926801…` and in the change tree, verified with `sha256sum`).
Written 2026-10-24T04:43Z (`date -u`).

## 0. Verdict in one paragraph

Production behaviour of all five tools is as claimed: **argv identical at every spawn site** (6/1/6/1/3 sites, zero positional or non-`env` keyword delta against the base), **every child environment is a fixed dict** (all five carry `GIT_CONFIG_NOSYSTEM=1` + `GIT_CONFIG_GLOBAL=/dev/null`, the frozen predicate's `KEPT_GIT_SETTINGS`), **no ambient read remains** (zero occurrences of `os.environ`/`getenv`/`environ.items` in all five files; independent AST scan finds zero ambient reads and every spawn call has an explicit `env=`), **no protection dropped** (every key the base builder set is present in the successor, no ambient-copying prefix filter remains), and **control flow is unchanged** (only dict construction, one docstring, one `import re`, and three added `env=` kwargs). I exercised the livefive argv of four of the five directly. **The declared C1 after value is nevertheless not met**: the frozen probe's `source` channel reads `tools/score-census-handoff-r32.py:source` as a leak at `c052bb7` (`leaking` 1, exit 1), so the livefive battery cannot read `leaking_pairs: []`. This is a counter/claim defect, not an ambient leak in the production code.

## 1. Findings by severity

### H1 (High, claim-blocking, counter not production) — `score-census-handoff-r32.py:source` reads 1 at the change commit

The frozen probe's source channel flags one line in `tools/score-census-handoff-r32.py`:

```
tools/score-census-handoff-r32.py:489 inheriting-spawn subprocess.Popen env name env bound by arg
```

`run_census(script, env, timeout)` (`:487`) spawns `subprocess.Popen(['/usr/bin/bash', script], env=env, …)` (`:489`); the probe's amendment-2 rule (`env_ok`, "a name every binding of which is one of those (never a parameter…)"; probe docstring) rejects any `env=` name that has a parameter binding. `env` is a parameter of `run_census` and `live_view`, so the rule fires even though every live caller passes a fixed dict.

Three independent readings, all with the frozen bytes `a2a5acac…`:

1. Direct call of the frozen function on the exported change tree (and on the base tree for comparison):

```
== c052bb7 tools/score-census-handoff-r32.py findings 1 scanned ['tools/score-census-handoff-r32.py']
    tools/score-census-handoff-r32.py:489 inheriting-spawn subprocess.Popen env name env bound by arg
```

2. My own full livefive invocation, `--set livefive --only score-census-handoff-r32.py` (145.98 s, scratch `mktemp -d /tmp/probeRevA.XXXXXX`):

```
{"revision": "c052bb7d41ced49aa888817069afd804eccfecf1", "targets": 1,
 "channels": ["names","quiet","source","untraced"], "pairs": 4, "leaking": 1,
 "leaking_pairs": ["tools/score-census-handoff-r32.py:source"], "harness_errors": [],
 "probe_sha256": "a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a",
 "probe_version": 7, "target_set": "livefive", "base": "6d76fb20…", "predicate_label": "leaking"}
probe_rc=1
```

3. Peer receipt `.ufo/waves/round-36/w2/W2MutTool3/probe-pristine.jsonl` and `score.json` (independent seat, same bytes): pristine `c052bb7` `leaking 1`, `leaking_pairs ["tools/score-census-handoff-r32.py:source"]`, exit 1, `channels_leaking {"names": false, "quiet": false, "source": true, "untraced": false}`.

Consequences for the declaration:
- The declared after value is "`leaking_pairs` 0 on all five targets, `harness_errors` empty, exit 0". With the frozen probe at `c052bb7` the full livefive summary is `leaking` ≥ 1, `harness_errors` `[]`, exit 1 — the harness is fine, the declared value is unmet. The claim therefore fails on its own counter, independently of the (separately GAP-verdict) sensitivity conjuncts and of any kill-rule attack.
- The measured after reading must be stated per target: score-census is 1; the other four are 0 (peer receipts quoted in §3).

**Production code is correct.** The only call sites of `run_census` are `live_view` (`:740`, receives `child_env()` at `:796` and `dict(env, TSUKUROI_JOURNALCTL=wrapper)` at `:809`, itself derived from `child_env()`) and the fixture selftest path (`:937`, `census_env`, already a fixed dict). No caller passes ambient. The defect is that the shape rule cannot see through one parameter hop.

**Repair options (L1 decision; the probe, predicate, label, set and after-value are frozen and MUST NOT change):**
- inline `child_env()` into the `Popen` call, or make `run_census` build `child_env()` itself (the live call sites already pass child_env-derived values, so a `run_census`-local `child_env()` plus dropping the parameter preserves semantics); or
- pass the environment through a name whose only bindings are dict displays / `child_env()` calls (the rule's accepted shapes).
Either is a change to the change commit, so it must be re-declared and the after battery re-run against the re-declared commit.

### M1 (Medium, declaration accuracy) — "the only true source-channel hit in the five files" is wrong

The correction block item 5(c) says the `__import__('re')` rewrite in `mutants-btrfs-space-r30.py` was "the only true source-channel hit in the five files". The frozen probe's own scan at the base finds six source findings across the five files, and one survives the change:

| revision | source findings |
|---|---|
| `6d76fb20` | `check-revision-binding.py:104 ambient-read .environ`; `check-report-receipts.py:311 ambient-read .environ`; `run-receipt.py:39 ambient-read .environ`; `mutants-btrfs-space-r30.py:362 ambient-read .environ` + `:145 hiding-construct __import__()`; `score-census-handoff-r32.py:489 inheriting-spawn … env bound by arg`, `:438` and `:843 inheriting-spawn … without env`, `:786 ambient-read .environ` |
| `c052bb7` | `score-census-handoff-r32.py:489 inheriting-spawn … env bound by arg` only |

Five of six were removed; the sixth is H1. The statement should be corrected to "the only source finding removed by a code rewrite" or, better, replaced by the per-file before/after table. The SCORECARD outcome block's "AST-verified: no ambient read on any spawn path, no inheriting spawn, no hiding construct" is true as an *ambient-read* statement (I reproduce it, §2) but, placed next to "C1 NOT VERIFIED", it must not stand in for the counter reading: the counter's source channel reads 1 at `c052bb7`, and that is the reason the declared after value fails (the kill rule is a separate, unscored attack class this round).

### L1 (Low, run-receipt) — `GIT_CEILING_DIRECTORIES` names the shared scratch parent, not the private home

`tools/run-receipt.py`'s `env(home)` adds `GIT_CEILING_DIRECTORIES=dirname(abspath(home))`. `home` and the sandbox clone `root` are both `mkdtemp(dir=parent)` (`:73-74`), so the ceiling is their common parent — an ancestor of the clone the measured tool runs in.

- This is harmless for the livefive target: the tool's cwd is `root`, `root/.git` is found at the first step, and the ceiling is above it. I reproduced the livefive invocation (below): rc 0, tool exit 0.
- It does block discovery of a repository *at* the parent: I verified with `env -i … GIT_CEILING_DIRECTORIES=/tmp/ceil/repo git rev-parse --show-toplevel` from `/tmp/ceil/repo/home` → `fatal: not a git repository`. So the setting is protective (git does not search the ceiling directory itself), and the only regression class is a measured tool that runs git from a non-repo directory directly under the shared parent and expects to discover a repo *there*. No such target exists in the livefive set.
- The disclosure is present (correction 5a). Suggest the docstring say "the scratch parent shared with the sandbox clone" rather than implying a per-home ceiling.

### L2 (Low, behaviour change, empirically safe) — the git helper calls now run without `HOME`

In `run-receipt.py` the clone / checkout / `ls-files` / `for-each-ref` calls pass `env()` with no `home`, so they no longer inherit ambient `HOME` (the base did). In `check-revision-binding.py` every git and gate-tool child now runs without `HOME` (the base inherited it). Evidence that this is safe for the operations used:

```
env -i PATH=/usr/bin:/bin LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 GIT_PAGER=cat \
  git clone --no-hardlinks --quiet --no-tags file://<lane> /tmp/revA/dest/clone        # rc 0
… git -C <clone> -c user.name=t -c user.email=t@invalid -c commit.gpgsign=false commit --allow-empty  # rc 0
… git -C <lane> rev-parse --verify HEAD^{commit}                                        # rc 0
… git -C <lane> archive --format=tar HEAD tools/tsukuroi-census.sh                      # rc 0
```

and the livefive runs in §3. The only in-tree consumer of `HOME` among the gate tools is `check-freshness-r17.py`, which builds its own private `HOME` in its round-32 fixed dict, and no gate tool invokes `git config --global` or `--global`-scoped config (grep over the nine `TOOLS`/`R17_GATES` files plus `tools/_revision.py`).

### I1 (Info) — the five fixed dicts are not key-identical, by the declaration's own qualifier

`PATH`, `LC_ALL`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null` in all five. `check-revision-binding.py` keeps `GIT_OPTIONAL_LOCKS=0`, `GIT_PAGER=cat` (base had them) and adds `PATH`; `check-report-receipts.py` keeps its seven base keys and adds `LC_ALL`; `run-receipt.py` keeps its three base keys, adds `PATH`, `LC_ALL`, and the run-private `GIT_CEILING_DIRECTORIES` when `home` is set; `mutants-btrfs-space-r30.py` and `score-census-handoff-r32.py` had no fixed keys at the base and now have exactly four. No key present in a base builder is missing from its successor. The probe's `KEPT_GIT_SETTINGS = ('GIT_CONFIG_NOSYSTEM=1','GIT_CONFIG_GLOBAL=/dev/null')` is satisfied in all five → no `git_missing_kept` false positive.

### I2 (Info) — mutants battery docstring is accurate

`tools/mutants-btrfs-space-r30.py`'s counter (`tools/check-btrfs-space-r30.py`) calls git only in its `--revision` branch (`:370-384`); the battery always runs `--tree` (`:369`), so "No Git subprocess is run by this battery" holds. The `__import__('re')` → top-level `import re` rewrite is semantically identical (`re.sub` used only in the F10 mutant).

### I3 (Info) — `LC_ALL=C` added to `check-report-receipts.py`

Paths are parsed from `ls-tree -rz` (NUL-delimited, no path quoting) and revisions/hashes are ASCII hex; the locale cannot change the parse. Selftest passes (§3). The added key is disclosed (correction 5b).

## 2. Method and the checks the assignment names

- **argv identical**: AST extraction of every spawn call (`subprocess.*`, `os.system/popen/exec*/spawn*`) from `git show 6d76fb20:<file>` and from the change tree; compared positional args and all non-`env` keywords as a multiset. Result per file — base sites / new sites, deltas:

```
check-revision-binding.py   6 / 6   (no ONLY-BASE, no ONLY-NEW)
check-report-receipts.py    1 / 1
run-receipt.py              6 / 6
mutants-btrfs-space-r30.py  1 / 1
score-census-handoff-r32.py 3 / 3
```

- **fixed values identical**: dict literals extracted per builder (`clean_env`, `find_receipts`' `env`, `env()`, the mutants `env`, `child_env`); values are the exact strings above; `os.devnull == '/dev/null'`. Additions are only the disclosed ones (PATH in four, LC_ALL in four, `GIT_CEILING_DIRECTORIES` in run-receipt when `home` is set; `GIT_CONFIG_SYSTEM` was already in `check-report-receipts` and `run-receipt`).
- **control flow identical**: the diff for the five files contains only the docstring hunks, `import re` + `re.sub`, the dict constructions, and three added `env=` kwargs. No branch, loop, timeout, error path or return value changed (e.g. `find_receipts` still raises the same `RuntimeError` strings; `run-receipt` still returns the tool's exit code and 124 on timeout).
- **no dropped protection**: all base fixed keys retained (I1); no `startswith('GIT_')`/`startswith('TSUKUROI_')` filter remains in any of the five (`grep` rc 1 = no match).
- **no remaining ambient read on any spawn path (AST)**: independent scan — zero `os.environ`/`environb`/`getenv` attribute nodes, zero `from os import environ|getenv`, and every spawn call carries an explicit `env=`; textual scan of the change tree for `os.environ|environ.items|getenv` returns 0 in all five files. The frozen probe's `source` channel independently reads 0 for four of the five (H1 is the fifth, and it is the env-shape rule, not an ambient read).

## 3. Per-tool behaviour evidence (runs I executed, plus peer receipts read)

| Tool | spawn sites / argv delta | base→new source findings | my run (exact livefive argv where applicable) | pristine after at `c052bb7` |
|---|---|---|---|---|
| `check-revision-binding.py` | 6 / 0 | 1 → 0 | `--tools-revision c052bb7 --object-target-types` rc 0, `target_type_status PASS`, 9/9 tools | peer W2MutTool1 `probe-base.jsonl`: leaking 0, pairs 4 |
| `check-report-receipts.py` | 1 / 0 | 1 → 0 | `--selftest` → `{"cases":2,"failures":[],"passed":2,"selftest":"PASS"}`, rc 0 | peer W2MutTool2 `probe-pristine.jsonl`: leaking 0, pairs 4 |
| `score-census-handoff-r32.py` | 3 / 0 | 4 → 1 | `--revision c052bb7 --lane <lane> --scenarios 1 --budget 180 --seed 36` rc 0, 20.23 s, live planes/rollup emitted | **mine + W2MutTool3: leaking 1 (source)** |
| `mutants-btrfs-space-r30.py` | 1 / 0 | 2 → 0 | default battery rc 0: `{"control":10,"should_fail_accepted":0,"should_pass_refused":0,"should_fail_total":72,"should_pass_total":11}` | peer/W2MutTool4 base receipt + LOG: 0 (selftest) |
| `run-receipt.py` | 6 / 0 | 1 → 0 | `--revision c052bb7 --tool-revision c052bb7 --lane <lane> --out /tmp/rr-livefive.jsonl -- tools/check-report-receipts.py --selftest` rc 0, tool `exit_code 0` | peer W2MutTool5 `m5-pristine-probe.jsonl`: leaking 0, pairs 4 |

So the five-target after summary at `c052bb7` is: `leaking` 1, `leaking_pairs ["tools/score-census-handoff-r32.py:source"]`, `harness_errors []`, exit 1. Runtime channels (`names`, `quiet`, `untraced`) read 0 on all five under the frozen probe (my score-census run: `reached {}`, `values_reached {}`, `untraced_record_count 0`; peer receipts for the others) — the production goal is met; the declared measure is not.

## 4. Residual risk and verification gaps

- **Not run by me** (`[unk]`): `tools/check-revision-binding.py --selftest` — the round-34 probe docstring records that its control run at another base was still unfinished after 45 minutes, so the nine-gate-tool mode under the `HOME`-less `clean_env()` is unverified here; I read the gate tools for `HOME`/`--global` dependence instead (none except check-freshness-r17, which builds its own private HOME) and ran the tool's livefive argv, which does not exercise `run_tool`. Risk: low, but the full-mode behaviour is an inference from source reading.
- **Not run by me**: the full five-target after battery; I ran score-census only and read the other four seats' pristine summaries as one-line receipts (paths in §3). The four 0s are peer evidence, not my execution.
- **In-flight outcome text**: `LOG.md` and `SCORECARD.md` were modified in the working tree at 04:39–04:43Z while wave-2 seats were still running (`SCORECARD.md:1761` "Round 36 measured outcome … — landed at budget deadline with wave-2 seats still settling"). It already says C1 NOT VERIFIED and cites "pristine after readings leaking 0 on three of five tools"; it must also state the measured fifth reading (`tools/score-census-handoff-r32.py:source` = 1 at `c052bb7`), otherwise the declared-after failure is attributed only to the separate kill-rule/attack class and the actual reason is missing. Artifact content is data for this seat; I did not modify it.
- **Peer harness error observed, not mine to score**: `.ufo/waves/round-36/w2/W2ReBefore/livefive.stdout` shows the before-receipt run dying with `RuntimeError: cannot create local master branch` (probe `:499`) on the check-revision-binding clone target; my score-census-only run did not take that path. The before/after receipt seat must resolve or record it.
- **Tool installs**: none this seat; no pacman transaction was run.

## 5. Machine output

- `per-tool-review.json` — the table of §3, per-file findings of §1, and the exact summary lines quoted above.
