# W2MutTool4 — after-mutant kill-check m4

**Verdict: KILLED** — the frozen probe read `leaking=3` on the mutated tool,
`harness_errors=[]`, while the same probe on the same target at the landed change
commit `c052bb7` read `leaking=0` with exit 0.
Written 2026-10-24T04:37:07Z (UTC).

## 1. Mutant

| item | value |
|---|---|
| source diff | `.ufo/waves/round-36/w1/MutToolMutants/mutant-4.diff` (sha256 `7c4f6414abef368b…`) |
| file | `tools/mutants-btrfs-space-r30.py`, `run_case()` line 363 |
| change | fixed dict `{PATH:/usr/bin:/bin, LC_ALL:C, GIT_CONFIG_NOSYSTEM:1, GIT_CONFIG_GLOBAL:os.devnull}` → `{k: v for k, v in os.environ.items() if not k.startswith('GIT_')}` |
| child that receives it | `/usr/bin/python3 <tool>/check-btrfs-space-r30.py --tree <fixture> --base-sources <file>` (the counter child), 84 execs per battery run |
| pristine sha256 | `35e1bbaa4eacabce97ab52eefbe1ec5991718ac8e9cf415575cec5f61cd793a6` |
| mutated sha256 | `38f76b4af84575f35a4f4df32feb4e1cd31af4ee1c990a858e8638d4e718a163` |

Sandbox: `git clone --no-local file:///home/vgpnk/Projects/shokunin/tsukuroi-shokunin` into
`mktemp -d /tmp/r36m4.XXXXXXXX`; the clone's default HEAD was `8d5fa7f` (wave-2 spec commit),
so I checked out the assigned `c052bb7d41ced49aa888817069afd804eccfecf1` explicitly. The diff
applied with plain `git apply` (`--check` rc 0) and touched exactly one file.

**Mechanism disclosure (one deviation).** The frozen probe resolves `--revision^{commit}` and
materialises the target tree with `git archive rev`, so a mutant can only be scored as a
commit. I materialised it as **one commit inside the throwaway mktemp clone only**
(`7b945d5bef23c33b74dfb2acb1e61d8a6736f69e`, 1 file changed; the other four tools' blob
hashes are identical to `c052bb7`). This is the round-34 `MutPathCopy` precedent ("exactly one
variant commit was made in the isolated clone"). No lane ref, index or worktree byte was
touched — the lane file was and remains
`35e1bbaa4eacabce97ab52eefbe1ec5991718ac8e9cf415575cec5f61cd793a6`, lane HEAD remains
`8d5fa7f`. The clone is deleted (see §5).

## 2. Expected detector

Frozen `tools/probe-child-env-allowlist-r36.py`, VERSION 7, sha256 `a2a5acac…`, run once as
`--set livefive --only tools/mutants-btrfs-space-r30.py`. The mutant copies the ambient
environment into the counter child, so the `names` and `quiet` channels (injected names and
value-channel `NAME=VALUE` strings after the target's first exec) and the `source` channel
(`.environ` read) should fire; `leaking > 0` on a target whose control run is clean.

## 3. Actual output

**Base control** (`--revision c052bb7…`, same probe, same `--only`), 30.7 s:

```json
{"revision": "c052bb7d41ced49aa888817069afd804eccfecf1", "targets": 1, "channels": ["names","quiet","source","untraced"], "pairs": 4, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a", "probe_version": 7, "target_set": "livefive", "base": "6d76fb20f6ecbc940e5c8fff36c74060c885e161", "predicate_label": "leaking"}
```
exit 0.

**Mutant** (`--revision 7b945d5…`), 30.4 s:

```json
{"revision": "7b945d5bef23c33b74dfb2acb1e61d8a6736f69e", "targets": 1, "channels": ["names","quiet","source","untraced"], "pairs": 4, "leaking": 3, "leaking_pairs": ["tools/mutants-btrfs-space-r30.py:names", "tools/mutants-btrfs-space-r30.py:quiet", "tools/mutants-btrfs-space-r30.py:source"], "harness_errors": [], "probe_sha256": "a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a", "probe_version": 7, "target_set": "livefive", "base": "6d76fb20f6ecbc940e5c8fff36c74060c885e161", "predicate_label": "leaking"}
```
exit 1, which is the probe's documented leak rule `2 if harness_errors else (1 if leaking else 0)`.

**Channels that fired** (all against the one target):

| channel | leak | measurement |
|---|---|---|
| `names` | **yes** | 12/12 injected names reached a child; 10/10 value-channel `NAME=VALUE` strings reached a child (HOME,LANG,LOGNAME,PATH,SHELL,TERM,TMPDIR,TZ,USER,XDG_CONFIG_HOME); 19 child env strings carry a run-unique ambient value under another name; control_rc 0, channel_rc 0, control_child_execs 84, parity_diffs [], execveat 0, unparsed 0 |
| `quiet` | **yes** | 8/8 injected names; 10/10 value-channel strings; 16 ambient values under other names; control_rc 0, channel_rc 0, control_child_execs 84, parity_diffs [], execveat 0, unparsed 0 |
| `source` | **yes** | `tools/mutants-btrfs-space-r30.py:363 ambient-read .environ` |
| `untraced` | no (UNINFORMATIVE) | 0 records; the mutant's only child exec is absolute `/usr/bin/python3`, so the injected wrapper dir is unreachable — the declaration's named limit (zero records is never a leak, never a harness error). The kill does not depend on this channel. |

No `harness_errors`, no `execveat` calls, no unparsed exec records, no parity diffs.

## 4. Ordinary-run check (ambient marker reaches a child)

Bound mechanism, no strace: a `sitecustomize.py` on an ambient `PYTHONPATH` writes
`{pid, argv, R36M4MARK, PATH, ppid}` at interpreter start; the tool is run through its normal
CLI (`python3 tools/mutants-btrfs-space-r30.py`, default battery mode).

| tree | rc | records | child records | children carrying `R36M4MARK=leak-2943-…` | battery stdout |
|---|---|---|---|---|---|
| pristine `c052bb7` | 0 | 1 | **0** | 0 | identical sha256 `315cb6fc…` |
| mutant | 0 | 85 | **84** | **84** | identical sha256 `315cb6fc…` |

Every mutant child is `…/tools/check-btrfs-space-r30.py --tree <tmp>/<shape>` (e.g. `CONTROL`,
`F01-json-missing`, `P11-angle-brackets`) and carries the ambient marker and the ambient
`PATH`, not `/usr/bin:/bin`. The pristine run's only record is the parent interpreter: the
fixed dict strips `PYTHONPATH` and the marker, so no child can be observed. The battery's own
stdout is byte-identical between the two runs, i.e. the leak changes the child environment and
nothing the tool reports — which is exactly why the child-env predicate, not output diffing,
is the detector. The 84 child execs match the probe's `control_child_execs=84`.

## 5. Restoration evidence

* Worktree file restored in the clone with `git checkout c052bb7… -- tools/mutants-btrfs-space-r30.py`:
  `35e1bbaa…` = the pristine `c052bb7` blob = the lane's current file.
* Mutant commit changed exactly one file (`git diff --name-only c052bb7 7b945d5` →
  `tools/mutants-btrfs-space-r30.py`); the other four tools keep their `c052bb7` blob hashes
  (`41a6f76b…`, `e7a79113…`, `f9eb17f8…`, `c91962b1…`).
* The probe removed its own scratch roots (`/fast/scratch/hyaku/s6f517e3…`, `s9ea3bc5…`: both
  absent afterwards). The mktemp clone is deleted; the mutant is reproducible from
  `mutant-4.diff` (sha256 `7c4f6414…`) by the exact command in `mutant.json`.
* The lane tree and index were never written: `git -C <lane> rev-parse HEAD` = `8d5fa7f` and
  `tools/mutants-btrfs-space-r30.py` = `35e1bbaa…` before and after.

## 6. Findings for the L1

* **F1 — stale mutant hash in the wave-1 declaration.** `MutToolMutants/mutants.md` records the
  m4 mutant file as `6d4e5a0a2ece6b2…`; that hash is the **pre-C1** blob at `189d8a0`. Against
  the landed C1 commit `c052bb7` the same revert is `38f76b4a…`, because C1 also hoisted
  `import re` and edited the module docstring. The reverted `env` line is byte-identical to the
  pre-C1 builder, the diff applies cleanly, and the kill is unaffected — only the recorded hash
  is obsolete. A future after-battery should key mutants by diff hash (`7c4f6414…`), not by
  file hash, or record the mutant hash against the landed commit.
* **F2 — clone default HEAD drift.** A plain `--no-local` clone of the lane lands on `8d5fa7f`,
  not on the change commit; the "sandbox clone at `c052bb7`" step needs an explicit checkout.
  The five tool files are identical at both revisions, so the mutant terrain did not change.
* **F3 — untraced channel is blind to this target's leak (already named).** Zero records on
  both pristine and mutant: the counter child is exec'd by absolute path and the injected
  wrappers are never reached. Consistent with the declaration's named limit; the kill rests on
  `names`, `quiet`, `source`.

## 7. Files and scope

Read: godspeed `skill://`, the assignment, `w1/MutToolMutants/{mutant-4.diff,mutants.md}`,
the frozen probe, `tools/mutants-btrfs-space-r30.py` at `c052bb7` and `189d8a0`.
Wrote: only `.ufo/waves/round-36/w2/W2MutTool4/` and `/tmp/r36m4.P3oIJ8uz/` (deleted).
Executed: one `git clone --no-local` into mktemp, one `git checkout --detach`, one
`git apply`, one commit in that throwaway clone, two probe runs (base control + mutant score),
two ordinary battery runs, hash/`git show`/`git diff` reads. No pacman, no installs, no
delegation, no lane write.

| file | content |
|---|---|
| `mutant.json` | machine summary: sandbox, mutant, detector, both scores, channel detail, verdict, findings |
| `restoration.json` | before/mutated/restored hashes, untouched-tool hashes, lane state |
| `probe-m4.jsonl` / `probe-m4.err` | raw mutant score (4 pair lines + summary), stderr |
| `probe-base.jsonl` / `probe-base.err` | raw base control at `c052bb7`, stderr |
| `ordinary-pristine.jsonl` / `ordinary-mutant.jsonl` | sitecustomize records (argv/env marker), 1 vs 85 records |
| `pristine.{out,err,rc}` / `mutant.{out,err,rc}` | battery stdout/stderr/exit for the ordinary runs (stdout sha256 identical) |
