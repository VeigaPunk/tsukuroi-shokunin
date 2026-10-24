# W2MutTool3 — kill-check after-mutant m3 (tools/score-census-handoff-r32.py)

Seat: Tsukuroi round 36, wave 2, FALSIFY. Written 04:41:38Z (UTC).
Frozen probe: `tools/probe-child-env-allowlist-r36.py` VERSION 7,
sha256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` (freeze commit `1e92680`).
Change commit under test: `c052bb7d41ced49aa888817069afd804eccfecf1`.

## 1. Mutant

`.ufo/waves/round-36/w1/MutToolMutants/mutant-3.diff` was present and applied verbatim (no reconstruction needed).
It restores the ambient copy in `live_check()` of the four/five-tool set's third member:

```diff
-    env = child_env()
+    env = {k: v for k, v in os.environ.items() if not k.startswith('TSUKUROI_')}
```

| item | value |
|---|---|
| file | `tools/score-census-handoff-r32.py` (line 795) |
| pristine bytes at `c052bb7` | `f9eb17f810e0768a3fe5b9d60c14d6cdafd7ec9ba1f7a38883790e404a83d51f` |
| mutated bytes | `db5eecb174ff592ee1b57e6cac1ced7d7413d64e8676cf267758e5ee65f2d6a1` (matches the `db5eecb174ff592e…` declared in `mutants.md` §3) |
| diff breadth | 1 file, 1 insertion / 1 deletion (`git diff --stat` against `c052bb7`) |
| syntax | `python3 -m py_compile` rc 0 |
| mutant commit in the sandbox | `95bcfd37db785b70c5821e23069f00199b930433`, parent `c052bb7`, tree `9fbfb4c24701e85a23c92cf3e16015917e7d6fe2` |

Why a rebuild was needed anyway: the probe materialises the target with `git -C <lane> archive <rev>`
and **re-clones `--lane` with `git clone --bare`** for the `{clone}` argv substitution. A bare clone copies
**refs only**, so an unreferenced mutant commit is invisible: `score-census` then fails `export_census` and
exits 2, which the probe reports as `harness_error: control run failed rc 2` (my first attempt, inconclusive —
recorded in `attempt1-harness-error.jsonl`). The probe therefore needs the mutant commit reachable from a ref
**in the sandbox clone**.

Construction (sandbox only, `/tmp/r36w2m3.bWqgsd/lane`, clone of the lane at `c052bb7`):
`GIT_INDEX_FILE=<tmp>/idx git read-tree c052bb7^{tree}` → `git hash-object -w` of the mutated file →
`git update-index --add --cacheinfo` → `git write-tree` → `git commit-tree <tree> -p c052bb7`;
then `git update-ref refs/heads/m3-mutant <commit>` **in the sandbox clone only**. No commit/checkout/index
operation ran in the worktree lane; `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain tools/`
stayed empty and the real `tools/score-census-handoff-r32.py` stayed `f9eb17f8…` throughout.

## 2. Invocation

```
python3 <frozen probe> --revision 95bcfd37db785b70c5821e23069f00199b930433 \
  --lane /tmp/r36w2m3.bWqgsd/lane --scratch /tmp/r36w2m3.bWqgsd/scratch \
  --set livefive --only tools/score-census-handoff-r32.py
```

`--only` only filters the target list (`main()`: `if a.only and tool not in a.only … continue`); each target is
measured independently, so the per-target reading is the one the full five-target `livefive` run would make.
The same invocation was run against `c052bb7` (pristine) as the do-nothing baseline.

## 3. Probe result — pristine vs mutant

| revision | exit | leaking | leaking_pairs | harness_errors | control_rc | control child execs |
|---|---|---|---|---|---|---|
| `c052bb7` (pristine) | 1 | **1** | `["…:source"]` | `[]` | 0 | 2558 |
| `95bcfd3` (mutant m3) | 1 | **3** | `["…:names","…:quiet","…:source"]` | `[]` | 0 | 2658 |

Per channel (`…` = `tools/score-census-handoff-r32.py`):

| channel | pristine | mutant m3 | what fired |
|---|---|---|---|
| `names` | leak **false** — 0 injected names reached, 0 value-channel strings, 0 any-name strings | leak **true** — **12 of 12** injected names reached, **10 of 10** value-channel `NAME=VALUE` strings (`HOME,LANG,LOGNAME,PATH,SHELL,TERM,TMPDIR,TZ,USER,XDG_CONFIG_HOME`), 551 any-name ambient-value strings; `channel_rc` 1 | injected-name + value channels |
| `quiet` | leak **false** — 0/0/0 | leak **true** — **8 of 8** injected names, **10 of 10** value-channel strings, 464 any-name strings; `channel_rc` 0 | injected-name + value channels |
| `source` | leak **true** — 1 finding: `…:489 inheriting-spawn subprocess.Popen env name env bound by arg` | leak **true** — 2 findings: the same line 489 **plus** `…:795 ambient-read .environ` (the mutant) | static scan; line 795 is the mutant's own signature |
| `untraced` | leak false, **0 records** | leak false, **0 records** | uninformative: the tool execs `/usr/bin/bash` by absolute path, so the wrapper dir is never consulted |

The mutant is therefore **KILLED on both dynamic channels**: `names` and `quiet` read 0 on identical bytes and
12/12 + 10/10 injected names/values on the mutated bytes, with `control_rc 0` on both trees, no harness error,
and the 2558 → 2658 control-child shift confirming the mutated tree is what ran. The probe's own exit is 1
(leak) on both trees.

## 4. Verdict and the one finding that matters

**Verdict: KILLED — with the baseline qualification that the probe's aggregate is 1 → 3, not 0 → >0.**

* The mutation-specific signal is unambiguous: `names` and `quiet` are clean at `c052bb7` and leak massively
  under m3. Under the seat rule "a baseline failure is inconclusive, not a killed mutant", the kill stands on
  those two channels, because their pristine reading is 0, not merely "non-zero elsewhere".
* **The C1 after-measure is falsified for this target, independently of any mutant.** At `c052bb7` the frozen
  probe reads `leaking: 1`, `leaking_pairs: ["tools/score-census-handoff-r32.py:source"]`, `harness_errors: []`,
  **exit 1** — so the declared measure "last JSON line `leaking == 0`, `leaking_pairs []`, `harness_errors []`,
  exit 0" does not hold for `--set livefive` as soon as this target is in the set. The declared run cannot be
  `leaking == 0` unless `--only` was used to drop this target, which the freeze checklist already forbids
  ("No `--only`, omitted failed target … can satisfy C1", `w1/CriticFreeze/freeze-checklist.md:87`).
* Cause: `run_census()` line 489, `subprocess.Popen(['/usr/bin/bash', script], env=env, …)`, where `env` is a
  function parameter. The source scanner reports `env name env bound by arg` and counts it as a finding →
  a leaking pair. This shape is **pre-existing**: the same file at the declaration base `6d76fb2` has that finding
  **plus** three more (`subprocess.run` without env, twice, and `ambient-read .environ`). C1's change reduced the
  static findings from 4 to 1 on this file but did not clear them, so the source channel was never 0 here.
  [inf] Whether the L1's recorded after-receipt used a different probe invocation or did not re-run the source
  channel cannot be settled from the seat copy; the frozen bytes I ran are the frozen bytes named by C1.
* `untraced` for this target is a **zero-records** channel (wrappers never invoked, absolute `/usr/bin/bash`):
  its silence is uninformative, exactly the named limit in the C1 claim — do not read it as clean.

## 5. Ordinary-run check (ambient marker reaches a child)

Detector: `w1/MutToolMutants/detector-det2.py` (copied here as `ordinary-detector.py`), same execve-env mechanism as
the probe, ambient `R36LEAKMARK=leak-<pid>`; argv `--revision 189d8a0… --lane <sandbox clone> --scenarios 1 --timeout 60`.

| tree | rc | children | marker leaks | non-fixed PATH | first leak |
|---|---|---|---|---|---|
| pristine `c052bb7` | 0 | 2151 | **0** | 465 (tool's own `work/<id>/bin:/usr/bin:/bin`, no marker) | — |
| mutant m3 | 0 | 3104 | **2637** | 3102 | `/usr/bin/bash <census>.sh` with `R36LEAKMARK=leak-1351735`, `PATH=/tmp/r36d-…/bin:/usr/bin:/bin`; its child `head -n1 /proc/sys/kernel/hostname` carries the same marker |

So the restored ambient environment really does reach the census bash child and everything it spawns, and the
mutant still exits 0 in an ordinary run — the leak is behavioural, not a crash.

## 6. Restoration evidence

* Reverse-apply `git apply -R mutant-3.diff` rc 0 (`--check` rc 0 first).
* Sandbox file `db5eecb174ff592e…` → `f9eb17f810e0768a…`; `git -C <sandbox> diff --stat c052bb7` empty,
  `git status --porcelain` empty → sandbox worktree byte-identical to the changed tree.
* The worktree lane was never written: `tools/score-census-handoff-r32.py` = `f9eb17f8…` before, during and after;
  `git status --porcelain tools/` empty; no `m3-mutant` ref exists anywhere in the real lane.
* Sandbox left in `/tmp/r36w2m3.bWqgsd` (871 MB, disposable; `lane`, `lane-det`, `t-base`, `t-pristine`,
  `t-mutant`, `verify.git`, probe JSONL logs). `refs/heads/m3-mutant` exists only there.

## 7. Files

| file | content |
|---|---|
| `score.json` | machine summary: verdict, both summaries, per-channel numbers, hashes |
| `probe-pristine.jsonl` | frozen-probe output at `c052bb7` (baseline) |
| `probe-mutant-livefive.jsonl` | frozen-probe output at the mutant commit |
| `attempt1-harness-error.jsonl` | first attempt: rc 2 harness error from the unreferenced-commit/bare-clone trap |
| `ordinary-run.json` | det2 ordinary-run readings and the leaking-child sample |
| `ordinary-detector.py` | the detector used (copy of `w1/MutToolMutants/detector-det2.py`) |
| `mutant-3.diff` | the applied mutant diff (byte copy of the wave-1 artifact) |
| `hash-mutant.txt`, `hash-restored.txt` | before/after sha256 of the mutated file |
| `environment.json` | sandbox layout, mutant commit construction, probe identity, real-lane-untouched statement |

Tool installs/upgrades: none (no pacman, no new tooling).

## 8. Seat-time note (observed, not inferred)

While this seat ran, the lane advanced from `c052bb7` to `d39da87` whose subject reads
"measured outcome (C1 not verified under declared battery - honest stop; C2 exploratory pending closure) …"
(observed at `d39da87a1647cca7bf36a1d171ee905e73ee97b0`, 04:42Z). `tools/score-census-handoff-r32.py` and the probe
were unchanged there (`f9eb17f8…`, `a2a5acac…`), so the measurements above hold for the lane as it stands.
That subject corroborates §4's baseline finding; it is not my evidence for it.
