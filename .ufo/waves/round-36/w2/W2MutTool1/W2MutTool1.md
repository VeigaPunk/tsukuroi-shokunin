# W2MutTool1 — after-mutant m1 kill-check for C1 (round 36, wave 2, FALSIFY)

Seat: `W2MutTool1` (mutation-tester, leaf). Lane: `tsukuroi-shokunin`.
Scope: one assigned probe — the declared after-mutant **m1** of wave 1
(`.ufo/waves/round-36/w1/MutToolMutants/mutant-1.diff`), scored once with the frozen
probe `tools/probe-child-env-allowlist-r36.py` VERSION 7 `--set livefive
--only tools/check-revision-binding.py`, plus the ordinary-run ambient-marker check.

## 0. TL;DR verdict

**KILLED.** The mutant restores an ambient-environment copy in
`tools/check-revision-binding.py`'s `clean_env()`; the frozen probe reads
`leaking > 0` on the mutant and `leaking == 0` on the pristine change commit. The
ordinary (untraced) run confirms the ambient marker `R36LEAKMARK=…` reaches git
children in the mutant (6/6) and none in the pristine tree (0/3).

**But the kill required a landed revision.** Scored as a detached commit not reachable
from `refs/heads/master`, the frozen probe returns `harness_errors:
["tools/check-revision-binding.py"]` with `leaking: 0` — i.e. a naive mutant run
reads **inconclusive**, not killed. A second trap: the probe archives the
*revision*, never the working tree, so an uncommitted sandbox patch is scored as
pristine. Both traps had to be defeated to get a verdict (findings P-1, P-2).

## 1. Setup and byte identity

Sandbox: `mktemp` clone of the lane, `/tmp/w2mt1.BLXSGY/lane`, checked out at the
change commit `c052bb7d41ced49aa888817069afd804eccfecf1`. No fleet or lane file was
written; the only VCS mutation was inside this `mktemp` sandbox (a local mutant
commit and a local `refs/heads/master` move) — no push, no fleet repo touched.

| artifact | sha256 |
|---|---|
| frozen probe `tools/probe-child-env-allowlist-r36.py` at c052bb7 | `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` (VERSION 7, as frozen) |
| `tools/check-revision-binding.py` pristine (c052bb7) | `41a6f76bb8aaacdc112fd59ec857f45793d9102c37a751a91eb4f10f4824f3b9` |
| same file after `mutant-1.diff` | `e9fe110ef1b046d5770639c50f2dd0a08e48591b930f2f657a82319f78f6ce82` |
| same file after `patch -p1 -R mutant-1.diff` | `41a6f76bb8aaacdc112fd59ec857f45793d9102c37a751a91eb4f10f4824f3b9` (exact restore) |

`git apply --check mutant-1.diff` → rc 0 on the change commit (no fuzz, no
`--unidiff-zero` needed: the wave-1 m1 diff carries real context). The mutant touches
exactly one file.

The diff restores the wave-1 declared mutant at the smallest behaviour-bearing
point — the body of `clean_env()`:

```python
def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C",
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
    return env
```

i.e. it replaces the fixed allowlist dict with the ambient environment minus `GIT_*`
and hands that to the `git --no-pager -c core.hooksPath=… -C <repo> …` child.

## 2. Detector: frozen probe, scored three ways

Command shape (run from the sandbox clone, probe read from the sandbox tree):

```
/usr/bin/python3 tools/probe-child-env-allowlist-r36.py \
  --lane /tmp/w2mt1.BLXSGY/lane --revision <REV> \
  --set livefive --only tools/check-revision-binding.py \
  --scratch /tmp/w2mt1.BLXSGY/scratch-<tag>
```

`livefive` target args are fixed by the probe: `--tools-revision {rev}
--object-target-types`; the target itself is run from a clone/checkout of `{rev}`.

| run | lane state | --revision | exit | leaking | leaking_pairs | harness_errors |
|---|---|---|---|---|---|---|
| pristine baseline | HEAD detached `38c6d5ec`*, master `c052bb7` | `c052bb7` | **0** | **0** | `[]` | `[]` |
| mutant attempt A (killed mid-run) | HEAD detached `38c6d5ec`, master `c052bb7` | `38c6d5ec` | – | – | – | – |
| mutant attempt B | HEAD detached `38c6d5ec`, master `c052bb7` | `38c6d5ec` | **2** | 0 | `[]` | `["tools/check-revision-binding.py"]` |
| mutant attempt C | HEAD detached `c052bb7`, master `38c6d5ec` | `38c6d5ec` | crash | – | – | `RuntimeError` (probe exit 1) |
| mutant attempt D — **scored** | HEAD detached `c052bb7`, master `38c6d5ec` | `38c6d5ec` | **1** | **4** | all four channels | `[]` |

Attempt A was killed by the job runner at 98 s (its `probe-mut.jsonl` holds a
truncated first line, no verdict); B and C are the two distinct traps documented in
P-2, each reproduced; D is the verdict. The `--only` filter and argv are identical in
all four.

\* the pristine baseline run was taken while the sandbox working tree already carried
the mutant bytes; the probe ignored them and read the `c052bb7` commit — direct
evidence for finding P-1.

Baseline channel detail (all four pairs, pristine):

| channel | leak | channel_rc | notes |
|---|---|---|---|
| names | false | 0 | control 2542 child execs, 2397 git execs |
| quiet | false | 0 | same counts |
| source | false | – | `scanned: ["tools/check-revision-binding.py"]`, `findings: []` |
| untraced | false | 0 | same counts |

Summary line: `{"targets": 1, "pairs": 4, "leaking": 0, "leaking_pairs": [],
"harness_errors": [], "probe_sha256": "a2a5acac…", "probe_version": 7,
"target_set": "livefive", "base": "6d76fb20…", "predicate_label": "leaking"}`.

### 2.1 Landed-mutant score

Lane state for the scored run: sandbox HEAD detached at `c052bb7` (pristine), mutant
commit `38c6d5ecc02e08b4201722f86c2f8ba0f3ffd739` reachable as `refs/heads/master`
(parent `c052bb7`, one file changed). Timing: the probe printed all five lines and the
summary; the wrapper shell was killed by the job runner ~104 s in, before it could echo
`$?`, so the exit code is derived from the probe's own contract and not directly
captured — `main()` ends `return 2 if errors else (1 if leaking else 0)` (probe line
1275), and `errors` is empty while `leaking` is 4, so **exit 1** [inf from probe
source + observed summary].

Summary line (`probe-mut4.jsonl`, last line):

```json
{"revision": "38c6d5ecc02e08b4201722f86c2f8ba0f3ffd739", "targets": 1, "pairs": 4,
 "leaking": 4,
 "leaking_pairs": ["tools/check-revision-binding.py:names",
                   "tools/check-revision-binding.py:quiet",
                   "tools/check-revision-binding.py:source",
                   "tools/check-revision-binding.py:untraced"],
 "harness_errors": [], "probe_sha256": "a2a5acac…", "probe_version": 7,
 "target_set": "livefive", "base": "6d76fb20…", "predicate_label": "leaking"}
```

Control viability on the mutant tree: `control_rc 0`, `control_child_execs 2550`,
`git_execs 2405`, `git_missing_kept 0`, `execveat 0`, `unparsed_exec_records 0`;
`parity_diffs: []` and `base_parity_diffs: []` were also empty (recorded, not evidence
under the `livefive` named limit). So the kill is a clean predicate kill, not a
harness artefact: the control run is viable and the difference from the pristine
baseline (which fired **no** channel) is the mutation itself.

## 3. Ordinary-run check (ambient marker reaches a child)

Detector: wave-1 `detector-det2.py` (strace `-f -e trace=execve -v`, same execve-env
mechanism as the frozen probe), ambient environment carrying the run-unique name
`R36LEAKMARK=leak-<pid>`; argv `--tools-revision <rev> --object-target-types`; cwd =
materialised tree.

| tree | rc | children | marker leaks | non-fixed PATH | leaking child argv |
|---|---|---|---|---|---|
| pristine (`c052bb7`) | 2 | 3 | **0** | 0 | — |
| mutant (`38c6d5ec`) | 2 | 6 | **6** | 6 | `git --no-pager -c …` (x2 exe records per git start: injected-PATH shim + `/usr/bin/git`) |

The marker reaches every git child in the mutant and none in pristine. The rc 2 is
identical on both trees and is the target's own `E-REVISION-INVALID` gate for the
`--tools-revision` value used by the detector (see §5/T-3) — it is not
mutant-induced and does not affect the marker measurement. Sample from
`ordinary-mut.json`:

```
{"exe": "/usr/bin/git", "argv": ["git", "--no-pager", "-c"],
 "marker": ["R36LEAKMARK=leak-1262424"],
 "path": ["PATH=/tmp/r36d-bxrah_73/bin:/usr/bin:/bin"]}
```

## 4. Which channels fired

**All four.** The mutant is killed redundantly, not by a single fragile channel:

| channel | leak | evidence (verbatim from `probe-mut4.jsonl`) |
|---|---|---|
| names | true | `12 of 12 injected names reached a child`; `10 of 10 value-channel NAME=VALUE strings reached a child: HOME,LANG,LOGNAME,PATH,SHELL,TERM,TMPDIR,TZ,USER,XDG_CONFIG_HOME`; `76 child environment strings carry a run-unique ambient value under some name`; sample name `BASH_ENV` in `/bin/sh`, `/usr/bin/git`, `/usr/bin/python3`, `/usr/lib/git-core/git-upload-pack` |
| quiet | true | `8 of 8 injected names reached a child`; same 10/10 value-channel strings; `64 child environment strings carry a run-unique ambient value` |
| source | true | `1 source findings` — `tools/check-revision-binding.py:104 ambient-read .environ` |
| untraced | true | `12 of 12 injected names reached a child`; `10 of 10 value-channel NAME=VALUE strings`; `19 child environment strings carry a run-unique ambient value`; sample `BASH_ENV` in `git` |

The kill is therefore not attributable to an injected-PATH artefact: the `names`
channel works by NAME and the `quiet` channel is the control-shaped run, and both see
the ambient HOME/TMPDIR/PATH/LANG/TZ/TERM/USER/LOGNAME/SHELL `NAME=VALUE` strings in
git children. `untraced` independently confirms the same with wrappers. No `execveat`
calls and no unparseable execve records on either tree, so those clauses did not
contribute.

## 5. Findings

### P-1 (methodology trap, high): the frozen probe scores the *revision*, never the working tree
`export_tree()` runs `git -C lane archive rev` (probe line 422) and `main()` resolves
`rev^{commit}` (lines 1113–1116); `one_run` then clones `rev` into a fresh worktree
(lines 486–508). A patch applied to a sandbox working tree but not committed is
therefore **invisible**: it scores as pristine. Empirical proof in this seat: the
baseline run took place with the mutant bytes already in the sandbox working tree
(HEAD detached at the mutant commit) and still read `leaking: 0` for `--revision
c052bb7`. Any wave-2/after-battery operator that applies a `.diff` and does not
commit it will record a false SURVIVED. Mutants must be committed inside the
disposable sandbox.

### P-2 (harness trap, high): the `livefive` revision-binding target has a landing gate
`tools/check-revision-binding.py` refuses a `--tools-revision` that is not reachable
from `refs/heads/master` in the worktree clone, printing
`{"findings": [{"detail": "38c6d5ec… not reachable from refs/heads/master", "id":
"E-REVISION-NOT-LANDED", …}], "status": "CANNOT_EVALUATE"}` and exiting 2. The probe's
control run then fails rc 2 and the target is recorded as a **harness error**, with
summary `leaking: 0` — a naive reading of the summary would score the mutant as not
killed. Two independent preconditions must hold for a mutant of this target to be
scorable:
1. the mutant commit must be reachable from `refs/heads/master`
   (`git branch -f master <mutant>` in the sandbox), and
2. the sandbox HEAD must *not* be detached exactly at the master tip: when it is,
   `git clone --bare` writes `HEAD: ref: refs/heads/master`, the probe's internal
   `--no-checkout` clone then already has a local `master`, and `one_run` dies with
   `RuntimeError: cannot create local master branch` (measured: probe traceback,
   exit 1, zero output lines). Keeping HEAD detached at any *other* commit restores
   the detached bare-HEAD path the probe expects.

Both conditions are undocumented in the probe and in the wave-1 mutant record; they
are reproduced in `probe-mut.jsonl` (harness error) and `probe-mut3.err` (traceback)
in this directory.

### P-3 (documentation defect, low): the wave-1 mutants.md hash table is wrong for m1
`mutants.md` §3 lists the m1 mutant hash as `1dfd5b48364f2cf7…`; the actual bytes
produced by `mutant-1.diff` on the change commit are `e9fe110ef1b046d5…`, which is
what `restoration.json` entry `"1"."mutated_sha"` also records and what this seat
reproduced twice (patch and `patch -R` round trip). The table's m4 row
(`6d4e5a0a2ece6b2…`) likewise disagrees with `restoration.json`
(`5f56fc8f94ef8b06…`); m2/m3/m5/m6 rows agree. [inf] for m4: not reproduced here,
only cross-read.

### P-4 (positive coverage note): the source channel is also armed against this leak shape
Contrary to the wave-1 record's framing (which expected the PATH/marker channels to
carry the kill), the `source` channel fired too: `tools/check-revision-binding.py:104
ambient-read .environ`. The source scan's builder rule (`env_ok`) explicitly accepts
dict comprehensions, so the kill does **not** come from there; it comes from the
ambient-read clause, which flags *any* attribute named `environ`/`environb`/`getenv`/
`getenvb` on any object (probe lines 980–982, constant at 782). Consequence for the
claim: restoring an ambient copy in this file is caught statically as well as
behaviourally, so the C1 fixed-dict form is the only form that satisfies both — but a
mutant that obtained the ambient environment through a name the scan does not know
(e.g. via `dict(os.__dict__['environ'])` or a value threaded in from elsewhere) would
still need the runtime channels, which is why the three runtime channels matter.

## 6. Machine files in this directory

| file | content |
|---|---|
| `mutant-1.diff` | the exact patch applied (copy of the wave-1 artifact) |
| `pristine.sha`, `mutant.sha`, `restored.sha` | sha256 before, after, after reverse-apply |
| `mutant.commit.txt` | sandbox mutant commit id |
| `probe-base.jsonl` | frozen-probe baseline run (pristine): leaking 0 |
| `probe-mut.jsonl` | attempt A, killed mid-write (truncated JSON, no verdict) |
| `probe-mut2.jsonl` | attempt B: harness error `control run failed rc 2` (P-2, landing gate) |
| `probe-mut3.err` | attempt C: `RuntimeError: cannot create local master branch` (P-2, HEAD-at-tip trap) |
| `probe-mut4.jsonl` | attempt D: the scored landed-mutant run (leaking 4) |
| `ordinary-base.json`, `ordinary-mut.json` | ordinary-run ambient-marker detector output |
| `restore.log` | reverse-apply transcript and exact-restore verdict |

Tooling: none installed or upgraded (no pacman; no uv/cargo/npm). Host `strace`
7.2, `git` 2.56.0, `/usr/bin/python3` only.
