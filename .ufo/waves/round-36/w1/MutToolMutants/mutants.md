# Round-36 wave-2 after-mutants for C1 (five live tools, fixed-dict child envs)

Seat: `MutToolMutants` (mutation-tester). Lane: `tsukuroi-shokunin`.
Date (UTC): 2026-10-24. Scope: patch design only — no production file was edited; every
byte written by this seat lives under `.ufo/waves/round-36/w1/MutToolMutants/`.

## 0. Base and input

**Input artifact.** `ExecC1Design/c1-five-tools.diff` was **absent** when this seat started
(the directory `.ufo/waves/round-36/w1/ExecC1Design/` did not exist). It appeared mid-seat
while its owning peer was still writing it, and was read at three distinct states:

| observation | md5 of `c1-five-tools.diff` | state |
|---|---|---|
| first read | `f89922491b449afca59112e55c95f42a` | 111 lines; `git apply --check` → `error: corrupt patch at …:75` |
| second read | (peer mid-edit) | 114 lines; `patch -p1` → `Hunk #1 FAILED at 437`, `malformed patch at line 64` |
| final read | `a2eebc9915e0c5649f893199dd0faadb` | 129 lines; applies only with `--unidiff-zero` |

**Dependency finding (F-1).** The input diff is a *zero-context* diff: several hunks carry no
leading/trailing context lines (e.g. `@@ -52,2 +52,2 @@`, `@@ -440,1 +440,1 @@`,
`@@ -8,1 +8,1 @@`). Plain `git apply` **rejects** it (`patch failed: tools/check-revision-binding.py:52`,
`… score-census-handoff-r32.py:440`, `… mutants-btrfs-space-r30.py:8`); `git apply --unidiff-zero`
applies it cleanly (rc=0); `patch -p1` applies it with fuzz 2 and fuzz 1. The L1 that lands the
C1 change must use one of those two modes, or regenerate the diff with real context.

**Changed tree used here.** The mutants are diffs against the tree obtained by applying
`c1-five-tools.diff` to the lane base. The base is commit `189d8a080ba8d508d5faab12cad9e688aee91dab`
(lane HEAD; the five tool files are byte-identical to the declaration commit
`6d76fb20f6ecbc940e5c8fff36c74060c885e161` — verified with `git diff --name-only`, output empty).
The changed tree was materialised by `git archive HEAD | tar -x` into a scratch directory
(`/tmp/mutw/t3`) followed by `git apply --unidiff-zero c1-five-tools.diff`.

All six `mutant-N.diff` files are unified diffs with `a/`…`b/` prefixes that apply to that
changed tree with **plain `git apply`** (verified: `git apply --check` rc=0 for all six) and
reverse-apply to restore the changed tree byte-for-byte (verified, see §3).

## 1. The six mutants

Each mutant is the smallest behaviour-bearing point that restores one ambient-copy builder.
Every one is a **real leak**: the ordinary (untraced) run of the tool starts a child that
receives the ambient environment.

| id | file | site | the ambient copy it restores | the child that receives it |
|---|---|---|---|---|
| **m1** | `tools/check-revision-binding.py` | `clean_env()` (line 103) | `os.environ` minus `GIT_*` | `git` — `git --no-pager -c core.hooksPath=… -C <repo> …` |
| **m2** | `tools/check-report-receipts.py` | `find_receipts()` env (line 313) | `os.environ` minus `GIT_*` | `git` — `git -c user.name=tsukuroi-round30-receipt-check -C <lane> …` |
| **m3** | `tools/score-census-handoff-r32.py` | `live_check()` env (line 795) | `os.environ` minus `TSUKUROI_*` | `/usr/bin/bash <census>.sh` — the census child, plus everything it spawns (`journalctl`, `head`, `tr`, `date`, …) |
| **m4** | `tools/mutants-btrfs-space-r30.py` | `run_case()` env (line 362) | `os.environ` minus `GIT_*` | `/usr/bin/python3 tools/check-btrfs-space-r30.py --tree …` — the counter child |
| **m5** | `tools/run-receipt.py` | `env()` (line 38) | `os.environ` minus `GIT_*` | `git` — `git -C <lane> rev-parse …`, then the clone/checkout/`ls-files`/`for-each-ref` children, then the receipted tool itself |
| **m6** | `tools/check-report-receipts.py` | `find_receipts()` fixed dict `PATH` (line 319) | ambient `PATH` only, via `os.environ["PATH"]` | `git` — `git -c user.name=… -C <lane> …` (the PATH value reaches it) |

m1–m5 are the *revert* of one builder each. m6 is the narrower "keep the fixed dict but let
`PATH` come from the ambient environment" shape: it leaves every other key fixed, so only the
ambient `PATH` value leaks — the same shape that survived in round 34
(`.ufo/waves/round-34/w2/MutPathCopy.md`, which replaced a PATH literal with
`os.pathsep.join(os.get_exec_path())` and read `leaking=0/27`). m6 is designed to be the
variant that closes that gap: `os.environ["PATH"]` yields the *exact* ambient PATH value, which
the frozen probe's PATH value-channel clause (`PATH=/usr/bin:/bin:<inject>/<random>`) matches by
the exact `NAME=VALUE` string.

## 2. Bounded ordinary behavioural detector — evidence that each leak is real

Detector: `/tmp/mutw/det2.py` (scratch; also copied to `detector-det2.py` in this directory).
It runs the target under `strace -f -e trace=execve -v -s 8192` — the **same execve-environment
mechanism the frozen probe uses** (`tools/probe-child-env-allowlist-r34.py`, docstring:
"observes every process a target starts with `strace -f -e trace=execve -v`, so it reads each
child's real argv and environment"). The ambient environment carries a run-unique marker name
`R36LEAKMARK=leak-<pid>`; a child whose traced envp contains `R36LEAKMARK=…` received it from
the ambient environment. The detector also flags any child whose `PATH` is not the fixed
`/usr/bin:/bin`.

Ordinary runs, one per mutant, against the **changed tree** (pristine) and the **mutant tree**:

| id | pristine: children / marker leaks / non-fixed PATH | mutant: children / marker leaks / non-fixed PATH | the leaking child (argv) |
|---|---|---|---|
| m1 | 3 / **0** / 0 | 6 / **6** / 6 | `git --no-pager -c core.hooksPath=/dev/null -C …` |
| m1 (`--selftest`) | 42576 / **0** / 134 | 9358 / **9358** / 9358 | `git --no-pager -c …` |
| m2 | 2 / **0** / 0 | 2 / **2** / 0 | `git -c user.name=tsukuroi-round30-receipt-check -C <lane> …` |
| m3 | 2204 / **0** / 481 | 2132 / **1699** / 2130 | `/usr/bin/bash <census>.sh` → `journalctl`, `head`, `tr`, `date` |
| m4 | 84 / **0** / 0 | 84 / **84** / 84 | `/usr/bin/python3 …/check-btrfs-space-r30.py --tree …` |
| m5 | 10 / **0** / 3 | 16 / **16** / 16 | `git -C <lane> rev-parse --verify …` and the clone/`ls-files` children |
| m6 | 2 / **0** / 0 | 4 / **0** / **4** | `git -c user.name=… -C <lane> …` — ambient PATH only, no marker |

Readings, with what they mean:

* **Marker leaks are the C1 predicate.** A count of 0 on pristine and >0 on mutant for the same
  command is exactly the frozen probe's `leaking_pairs` shape: the ambient name reached a child
  that the pristine tool never starts with that name. m1, m2, m3, m4, m5 all fire it.
* **m6 does not fire the marker clause — by design, and it still leaks.** m6 copies only the
  ambient `PATH` value; no ambient *name* is added. It is caught by the probe's PATH **value**
  channel (the probe assigns PATH the ambient value `/usr/bin:/bin:<inject>/<random>` and a
  child carrying that exact `NAME=VALUE` string leaks). My detector's `non-fixed PATH` column
  is the same measurement: 0 pristine, 4 for m6. Under the frozen probe this is the clause
  that round 34's `MutPathCopy` evaded by rewriting PATH rather than copying it.
* **The pristine non-zero PATH counts are not leaks of the ambient env.** m3 pristine shows 481
  and m5 pristine 3 non-fixed PATH children: those are the tools' *own* run-private PATHs
  (`m3`: the census stub dir `…/work/<id>/bin:/usr/bin:/bin`; `m5`: git's own
  `PATH=/usr/lib/git-core:…` prefix, added by git itself to its own upload-pack children).
  They carry **no** `R36LEAKMARK`, so the marker column is the clean ambient-copy signal.
* **Exit codes.** m2/m3/m4/m6 exit 0 on both trees. m1 and m5 exit 2 on both trees for reasons
  unrelated to the leak (m1: the tool's revision gate rejects the argument, `E-REVISION-INVALID`;
  m5: the receipted r34 probe rejects `--version`, `error: the following arguments are required:
  --revision`). In every case the leak is measured on children that were actually started, and the
  same exit code appears on the pristine tree, so the exit code is not a mutant-induced change.

## 3. Restoration evidence

`restoration.json` in this directory records, for each mutant: the sha256 of every mutated `.py`
file before and after, and a full-tree comparison against the changed tree.

* Each `mutant-N.diff` reverse-applies (`git apply -R`) with rc=0.
* After reverse-apply, every `.py` file under `tools/` is byte-identical to the changed tree
  (`restored_exactly_to_changed_tree: true` for all six).
* Each mutant touches exactly **one** file; the other four of the five tools keep their changed-tree
  hashes. Measured hashes (changed tree → mutant):

  | file | changed tree sha256 | mutant sha256 | mutant |
  |---|---|---|---|
  | `tools/check-revision-binding.py` | `41a6f76bb8aaacdc…` | `1dfd5b48364f2cf7…` | m1 |
  | `tools/check-report-receipts.py` | `7b79122ad0482099…` | `ccf858bede90acc6…` | m2 |
  | `tools/check-report-receipts.py` | `7b79122ad0482099…` | `18584522eb6689a4…` | m6 |
  | `tools/score-census-handoff-r32.py` | `f9eb17f810e0768a…` | `db5eecb174ff592e…` | m3 |
  | `tools/mutants-btrfs-space-r30.py` | `3713bec5a32c0e0c…` | `6d4e5a0a2ece6b2…` | m4 |
  | `tools/run-receipt.py` | `c91962b1c053a97c…` | `85f9429deb6d881…` | m5 |

* Syntax: every mutated file compiles (`python3 -m py_compile` → rc=0) for all six.

## 4. Expected detector outcome (for the wave-2 falsifier)

Under the frozen `tools/probe-child-env-allowlist-r36.py --set livefive`, each mutant should read
`leaking_pairs > 0` on **its own target** and 0 on the other four, with `harness_errors` empty and
exit 0 — i.e. each mutant is *killed* by the frozen probe. m6 is the one to watch: it is killed by
the PATH value channel, not by the injected-name channel, so a wave-2 score that shows m6 surviving
would be a **coverage finding about the PATH value channel**, not a defect in m6.

## 5. Files

| file | content |
|---|---|
| `mutant-1.diff` … `mutant-6.diff` | the six unified diffs against the changed tree |
| `mutants.md` | this document |
| `restoration.json` | per-mutant before/after sha256 and the exact-restore verdicts |
| `detector-det2.py` | the bounded ordinary strace/execve leak detector (scratch copy) |
| `detector-results.json` | raw detector output for every pristine/mutant run |
| `samples.json` | the leaking children's argv and env samples per mutant |

## 6. Findings for the L1

* **F-1 (blocking for the L1's apply step).** `ExecC1Design/c1-five-tools.diff` is zero-context
  and plain `git apply` rejects it. Apply with `git apply --unidiff-zero` (verified rc=0) or
  regenerate with context. Two earlier intermediate states of the same file were outright corrupt
  (`corrupt patch at …:75`; `malformed patch at line 64`), so the L1 should re-verify the file's
  md5 at apply time rather than trusting a copy taken earlier in wave 1.
* **F-2.** m6 is the only mutant whose leak is a *value* leak, not a *name* leak. If wave 2 reads
  m6 as surviving, the frozen probe's PATH value channel is not doing its job — that is the
  round-34 `MutPathCopy` gap re-opened, and it is a claim-level finding for C1's kill rule.
* **F-3.** The `livefive` target set in the r36 probe draft runs
  `tools/run-receipt.py … -- tools/probe-child-env-allowlist-r34.py --version`; the r34 probe
  rejects `--version` (`error: the following arguments are required: --revision`), so that
  target's tool child exits 2 in every run. The leak measurement for run-receipt is unaffected
  (the git children it starts before that still leak), but the target's exit code is not a clean
  0 and may need an argument fix before the after-battery receipt is taken.
