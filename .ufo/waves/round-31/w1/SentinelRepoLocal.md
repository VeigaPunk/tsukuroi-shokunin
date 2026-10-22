# SentinelRepoLocal — repository-local include / core.fsmonitor channel (round-31 owed item 5)

**Verdict: partly holds.** All eleven C2 tools read the `.git/config` of a repository they did
not create, and the round-30 child-environment contract does **not** suppress the
repository-local scope — but **no canary fires** in any of the twenty-two measured runs, because
every git subcommand the eleven tools run against a foreign repository is read-only plumbing
(`show`, `ls-tree`, `rev-parse`, `merge-base`, `cat-file`, `archive`, `for-each-ref`) and the
mutating subcommands (`add`, `commit`, `checkout`, `clean`) all run inside repositories the tool
itself created. The channel is **live but not reachable today**; it is a latent one-line change
away, and the frozen r31 probe has **no channel that would detect it**.

---

## 1. Which of the eleven tools run git against a repository whose `.git/config` they did not create?

All eleven. The distinction that matters is *which* repository, and *whether the git operation
against it is read-only*.

| # | Tool (TARGETS order) | Foreign repo it runs git against | Did the tool create that repo? | Foreign-repo subcommands used | Mutating op in the foreign repo? |
|---|---|---|---|---|---|
| 1 | `check-adjacency-overlap.py` | `--repo` (default = lane checkout) | **no** | `show`, `rev-parse`, `cat-file` | no |
| 2 | `check-freshness-r17.py` | `ROOT` (the lane checkout, by `__file__` parent) | **no** | `show`, `rev-parse`, `merge-base`, `check-ref-format` | no |
| 3 | `check-kernel-taint.py` | `--repo` (default = `ROOT`) | **no** | `show`, `ls-tree`, `rev-parse`, `merge-base`, `cat-file` | no |
| 4 | `check-memory-pressure.py` | `ROOT` | **no** | `show`, `rev-parse` | no |
| 5 | `check-registry-coverage.py` | `ROOT` | **no** | `ls-tree`, `show`, `rev-parse`, `merge-base`, `cat-file` | no |
| 6 | `check-storage-health.py` | `--repo` (default = `ROOT`) | **no** | `show`, `ls-tree`, `rev-parse` | no |
| 7 | `mutants-adjacency-overlap.py` | `--lane` (probe's `{clone}`) — `rev-parse`, `archive`, `show` | **no** (the lane/clone) | `rev-parse`, `archive`, `show` | no (its `add`/`commit`/`checkout` run in `SBX`, its own `git init` sandbox) |
| 8 | `mutants-kernel-taint.py` | `--lane` — `rev-parse`, `archive`, `show` | **no** | `rev-parse`, `archive`, `show` | no (its `add`/`commit`/`checkout` run in `REPO`, its own sandbox) |
| 9 | `check-self-assessment.py` | `--repo` (default = lane checkout) | **no** | `show`, `ls-tree`, `archive`, `rev-parse` | no |
| 10 | `mutants-owed-statements-r29.py` | `--lane` — `rev-parse`, `show`; and **`git clone --no-local ARGS.lane REPO`** | **no** (the lane); the clone `REPO` it makes is its own | `rev-parse`, `show` | no (its `checkout`/`commit` run in `REPO`, the clone) |
| 11 | `mutants-owed-statements-r29-landed.py` | `--lane` — `rev-parse`, `show`; and **`git clone --no-local ARGS.lane REPO`** | **no** | `rev-parse`, `show` | no (its `checkout`/`clean`/`add`/`commit` run in `REPO`, the clone) |

Evidence for the table (read-only git on the lane, `tools/_revision.py:64-77`, and each tool's
own git helper):

- `tools/_revision.py:72` — `subprocess.run(["git", "--no-pager", "-C", str(repo), *args], … env=clean_env())`,
  where `clean_env()` (`tools/_revision.py:64-68`) sets only `GIT_OPTIONAL_LOCKS`, `GIT_PAGER=cat`,
  `LC_ALL=C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=os.devnull`. It sets **no**
  `GIT_CONFIG_SYSTEM`, and it sets nothing that suppresses the **repository-local** scope.
- `tools/check-kernel-taint.py:289`, `check-memory-pressure.py:142`, `check-registry-coverage.py:80`,
  `check-storage-health.py:276`, `check-freshness-r17.py:360` — the same shape.
- `tools/check-adjacency-overlap.py:472` — `git(sib_repo, 'cat-file', …)` against the **live**
  sibling repo `/home/vgpnk/Projects/shokunin/mori-shokunin`, whose `--siblings-root` default is
  `tools/check-adjacency-overlap.py:925`. This is a second foreign repo the tool does not create.
- `tools/mutants-owed-statements-r29.py:49` and `tools/mutants-owed-statements-r29-landed.py:48` —
  `subprocess.run(['git', 'clone', '-q', '--no-local', ARGS.lane, REPO], …)`.

Measured per-tool foreign-repo git exec counts (from the strace traces committed under
`traces/`), e.g. `check-registry-coverage.py.B.trace`: 34 `ls-tree` + 33 `show` + 4 `rev-parse`
+ 2 `merge-base` + 1 `cat-file`, all with `-C <poisoned clone>`.

---

## 2. Experiment: poisoned `.git/config` in a sandbox clone at 8cff9e7

Setup (read-only on the lane; all writes under the seat scratch and the seat path):

```
S=/fast/scratch/hyaku/tsukuroi-r31/SentinelRepoLocal
git clone -q --no-local /home/vgpnk/Projects/shokunin/tsukuroi-shokunin $S/poisoned
git -C $S/poisoned checkout -q 8cff9e7cfb034b49c645d548801ac3185a827cb4
printf '[core]\n\tfsmonitor = <canary script>\n[include]\n\tpath = <file setting core.hooksPath to canary hooks>\n' \
  >> $S/poisoned/.git/config
```

The canary script appends `FIRED fsmonitor <ns> args=…` to `canary.log`; nine canary hooks
(`post-commit`, `pre-commit`, `post-checkout`, `post-merge`, `post-index-change`, `pre-rebase`,
`post-rewrite`, `prepare-commit-msg`, `reference-transaction`, `post-update`) append
`FIRED hook:<name> <ns>`. Every run is under
`strace -f -qq -s 65536 -e trace=execve,openat`, so we observe both execution and file reads.

Harness: `files/harness.py`. Results: `files/results.json`. Traces: `traces/*.trace.gz`.

### Positive control (the poison is live)

```
$ git -C $S/poisoned status --porcelain
FIRED fsmonitor 1792710841006029230 args=2 1792710841004347970
FIRED hook:post-index-change 1792710841013437067
```

`results.json` → `control.lines_added = 2`. The poison fires on demand.

### Results, all twenty-two runs

| Tool | Mode | rc | canary fired | foreign `include.cfg` opened | git execs |
|---|---|---|---|---|---|
| check-adjacency-overlap | probe-argv (`--selftest`) | 0 | **no** | no | 1167 |
| check-adjacency-overlap | revision-mode (`--repo` poisoned) | 0 | **no** | **yes (17)** | 15 |
| check-freshness-r17 | probe-argv | 0 | **no** | no | 113 |
| check-freshness-r17 | revision-mode | 0 | **no** | **yes (23)** | 25 |
| check-kernel-taint | probe-argv | 0 | **no** | no | 877 |
| check-kernel-taint | revision-mode | 0 | **no** | **yes (20)** | 21 |
| check-memory-pressure | probe-argv | 0 | **no** | no | 349 |
| check-memory-pressure | revision-mode | 0 | **no** | **yes (12)** | 13 |
| check-registry-coverage | probe-argv | 0 | **no** | no | 303 |
| check-registry-coverage | revision-mode | 1 | **no** | **yes (74)** | 75 |
| check-storage-health | probe-argv | 0 | **no** | no | 673 |
| check-storage-health | revision-mode | 0 | **no** | **yes (26)** | 27 |
| mutants-adjacency-overlap | probe-argv (`--lane` poisoned) | 0 | **no** | **yes (5)** | 957 |
| mutants-adjacency-overlap | revision-mode | 0 | **no** | **yes (5)** | 957 |
| mutants-kernel-taint | probe-argv | 0 | **no** | **yes (5)** | 609 |
| mutants-kernel-taint | revision-mode | 0 | **no** | **yes (5)** | 609 |
| check-self-assessment | probe-argv | 0 | **no** | no | 312 |
| check-self-assessment | revision-mode | 1 | **no** | **yes (41)** | 21 |
| mutants-owed-statements-r29 | probe-argv | 0 | **no** | **yes (5)** | 858 |
| mutants-owed-statements-r29 | revision-mode | 0 | **no** | **yes (5)** | 858 |
| mutants-owed-statements-r29-landed | probe-argv | 0 | **no** | **yes (5)** | 1012 |
| mutants-owed-statements-r29-landed | revision-mode | 1 | **no** | **yes (5)** | 15 |

**Zero canary fires in twenty-two runs.** Yet the foreign repository's `[include]` file **is**
opened — 5 to 74 times per run — by the git children themselves:

```
$ grep -c include.cfg traces/check-registry-coverage.py.B.trace
74
```

and every one of those opens happens while a `/usr/bin/git` child is the running process
(`files/` — the attribution script counted 20 git-context opens and 0 non-git-context opens in
`check-kernel-taint.py.B.trace`).

---

## 3. Why no canary fires — the mechanism, measured

`files/RECAP.txt` records the measured git 2.56.0 behaviour:

- `core.fsmonitor` fires on **index-refreshing** operations: `status`, `diff`, `add`, `commit`,
  `checkout`. It does **not** fire on `show`, `ls-tree`, `archive`, `rev-parse`, `cat-file`,
  `log`, `for-each-ref`, `config --list`.
- `core.hooksPath` hooks fire only on operations that run hooks: `commit`
  (`pre-commit`, `prepare-commit-msg`, `commit-msg`, `reference-transaction`, `post-commit`) and
  `checkout` (`post-checkout`, `post-index-change`). No read-only plumbing operation runs a hook.
- `git clone` does **not** inherit `core.fsmonitor`, `core.hooksPath` or `include.path` from the
  source repo's local config (verified for both a normal and a `--bare` clone).
- `git init` in a subdirectory of a poisoned repo does **not** inherit them either.

Every foreign-repo git call the eleven tools make is read-only plumbing, and every mutating
call (`add`, `commit`, `checkout`, `clean`) runs in a repository the tool created (`git init`
sandbox, or `git clone --no-local` output). Hence: **no fire**.

The channel is nevertheless **open at the environment level**. The round-30 child contract does
not reach the repository-local scope:

```
$ env GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null \
    git -C $S/poisoned config --get core.hooksPath
/fast/scratch/hyaku/tsukuroi-r31/SentinelRepoLocal/canary/hooks
$ env GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null \
    git -C $S/poisoned config --get core.fsmonitor
/fast/scratch/hyaku/tsukuroi-r31/SentinelRepoLocal/canary/fsmonitor.sh
```

`GIT_CONFIG_NOSYSTEM` / `GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM` cover the **system** and
**global** scopes only. The **local** (repository) scope is read unconditionally by every git
command that touches that repository, and the local scope is where `[include] path` lives. This
is the mechanism the round-30 spot-check flagged as a probe gap
(`corpus/lessons/round-30.md:45`, `corpus/lessons/round-30-verifier-spotcheck.md:186`).

---

## 4. The behaviour change is not observable

Same-clone A/B control (`files/ab-control.txt`): the poison present vs. the two poison lines
removed from the *same* `.git/config`, same clone, same revision — every tool's exit code and
stdout are unchanged:

```
check-registry-coverage: with_poison_rc=1 without_poison_rc=1 stdout=IDENTICAL
check-self-assessment:   with_poison_rc=1 without_poison_rc=1 stdout=IDENTICAL
check-kernel-taint:      with_poison_rc=0 without_poison_rc=0 stdout=IDENTICAL
check-storage-health:    with_poison_rc=0 without_poison_rc=0 stdout=IDENTICAL
check-memory-pressure:   with_poison_rc=0 without_poison_rc=0 stdout=IDENTICAL
check-adjacency-overlap: with_poison_rc=0 without_poison_rc=0 stdout=IDENTICAL
check-freshness-r17:     with_poison_rc=0 without_poison_rc=0 stdout=IDENTICAL
```

(The `rc=1` for `check-registry-coverage` and `check-self-assessment` is the tool's ordinary
verdict at revision 8cff9e7 in this clone, not a poison effect: it is identical with and without
the poison. An earlier cross-clone comparison showed `rc=2` vs `rc=1`; that was an artefact of
the lane's `master` tip moving from 8cff9e7 to 13ca52d mid-session, which changes
`_revision.bind`'s branch check (`tools/_revision.py:176-194`), not the poison.)

---

## 5. The frozen r31 probe cannot detect this channel

`tools/probe-git-child-env-r31.py` has three frozen channels — `loader-env`, `child-contract`,
`dotgit-pointer` — and **no** channel that poisons a repository's local config:

```
$ grep -niE "fsmonitor|include|hooksPath|repo-local|local config" tools/probe-git-child-env-r31.py
(no output)
```

Its `child-contract` channel checks only that git children carry `GIT_CONFIG_NOSYSTEM=1`,
`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null` and a non-empty
`GIT_CEILING_DIRECTORIES` (`tools/probe-git-child-env-r31.py:84-89`). Those four names are
satisfied by the current tools **while the local scope is still fully honoured**, so the probe
would score this channel 0 leaking even with the poison in place. This is precisely the
"repository-local `include`/`core.fsmonitor`" bullet of routed defect 5
(`corpus/lessons/round-30-verifier-spotcheck.md:186`), and it remains uncovered.

---

## 6. Exploit path (the risk that justifies closing it)

**Path.** A repository whose `.git/config` the tool did not create carries

```
[core]
        fsmonitor = /path/to/attacker/script
[include]
        path = /path/to/attacker/extra.config      # extra.config: [core] hooksPath = /path/hooks
```

Any git child of any of the eleven tools that runs an **index-refreshing** or **hook-triggering**
subcommand against that repository executes attacker-chosen code with the tool's own
privileges. The eleven tools do not currently do that against a foreign repo — but the distance
is one subcommand:

- `tools/check-adjacency-overlap.py:373-375` and `tools/check-kernel-taint.py:328` already
  contain the token `status` in their result payloads; a future `git status` or `git diff`
  against `--repo`/`ROOT` would fire the fsmonitor hook immediately.
- `tools/mutants-owed-statements-r29.py:49` already runs `git clone --no-local ARGS.lane REPO`.
  A clone is safe today only because git does not copy the source's local config; but the
  *source* repository's config is read by upload-pack during the clone, and the repo is under
  the tool's `--lane` argument, i.e. outside the tool's control.
- The live sibling repo `mori-shokunin` (read at `tools/check-adjacency-overlap.py:472`, default
  `--siblings-root /home/vgpnk/Projects/shokunin`) is a **third** foreign repository whose local
  config is read by the tool's git child (verified: `git -C …/mori-shokunin cat-file -p …`
  opens `.git/config` relative to the repo).

**Impact.** Arbitrary code execution in the lane's tool context. The trigger is a config value
in a repository the tool merely reads. Because the local scope is not covered by the round-30
contract, no existing mitigation stops it, and the frozen probe cannot see it.

**Smallest remediation** (for the lane, not for this seat — this seat has no remediation scope):

1. Make the *probe* able to see the channel, so the claim can fail on it: add a fourth channel
   that poisons the target repository's `.git/config` with `core.fsmonitor` and an
   `[include] path` that sets `core.hooksPath`, and treat any canary line as a leak. The probe
   must also detect the *read* of the include file, not only execution, so a near-miss (a tool
   that only reads) is visible.
2. Make the *tools* immune: every git child that runs against a repository the tool did not
   create should add `-c core.fsmonitor=` and `-c core.hooksPath=/dev/null` (or the equivalent
   `GIT_CONFIG_COUNT` / `GIT_CONFIG_KEY_*` / `GIT_CONFIG_VALUE_*` environment form, which was
   measured to work: `canary lines: 0`). Verified mitigations:

   ```
   R1  GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=core.fsmonitor GIT_CONFIG_VALUE_0= \
       GIT_CONFIG_KEY_1=core.hooksPath GIT_CONFIG_VALUE_1=/dev/null   -> 0 canary lines
   R3  -c core.fsmonitor= -c core.hooksPath=/dev/null                  -> 0 canary lines
   R2  -c core.fsmonitor=false                                         -> 10 canary lines (does NOT work)
   R4  no mitigation                                                    -> 13 canary lines
   ```

   `-c core.fsmonitor=false` does **not** neutralise the hook (the empty value does), and
   `-c core.hooksPath=/dev/null` beats an `[include]`-supplied `hooksPath`
   (`git config --get core.hooksPath` under `-c core.hooksPath=/dev/null` returns `/dev/null`).
   Note that `GIT_CONFIG_KEY_*` / `GIT_CONFIG_VALUE_*` / `GIT_CONFIG_COUNT` are themselves `GIT_*`
   names, so they must be set **after** the round-30 `GIT_*` scrub, not before.
3. Independently, `tools/_revision.py:64-68` should also set `GIT_CONFIG_SYSTEM=os.devnull`
   (the round-30 contract names it; `_revision.clean_env` currently sets only `GIT_CONFIG_NOSYSTEM`
   and `GIT_CONFIG_GLOBAL`). That is a system-scope gap, not this local-scope gap, but it is in
   the same function and the same family.

**Caveat, stated plainly.** Findings 1–5 are measured. The exploit path in §6 is a
demonstrated mechanism (the canary fires on `status`/`diff`/`add`/`commit`/`checkout` in a
poisoned repo, and the mitigations are measured) applied to a subcommand the eleven tools do not
currently issue against a foreign repo; that application is **[inf]**, not observed.

---

## 7. Scope notes and limits

- Host actions were read-only except for the sandbox clone and the seat scratch
  (`/fast/scratch/hyaku/tsukuroi-r31/SentinelRepoLocal/`). No `git`/`jj` **write** command was
  run inside `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` or
  `/home/vgpnk/Projects/shokunin`; the only writes in the lane tree are the new files under
  `.ufo/waves/round-31/w1/SentinelRepoLocal/`. All sandbox git commands were prefixed with
  `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`.
- The lane's `master` tip moved from 8cff9e7 to 13ca52d during this seat's run (a wave-1
  integration landed upstream). All measurements are anchored to the pinned revision
  8cff9e7cfb034b49c645d548801ac3185a827cb4 as the assignment requires; the cross-clone
  `rc=2`/`rc=1` difference in §4 is a consequence of that tip move and is explicitly **not** a
  poison effect (the same-clone A/B is identical).
- `uploadpack.packObjectsHook` is present as a config key in the installed git 2.56.0
  (`strings /usr/lib/git-core/git-upload-pack` → `uploadpack.packObjectsHook`) but did not fire
  in any of our tests (`clone --no-local`, `file://` clone, `fetch`, direct
  `git upload-pack --stateless-rpc`). Treated as **[unk]** for this git build, not as a closed
  vector.
- `core.alternateRefsCommand` did not fire on `for-each-ref`, `ls-remote`, `fetch` or
  `rev-list --alternate-refs`; `core.pager` did not fire because the tools capture pipes, never
  a tty. Both measured, both closed in this configuration.
- The probe's `dotgit-pointer` channel is a neighbouring concern (a dropped `.git` pointer file)
  and was not re-tested here; this report covers only the repository-local `include` /
  `core.fsmonitor` bullet of routed defect 5.

---

## Artefacts

- `files/harness.py` — the experiment harness (poisoned clone build, canaries, strace capture,
  per-run JSON).
- `files/results.json` — the twenty-two runs, the positive control, the per-run
  include-opened / canary-fired flags.
- `files/RECAP.txt` — the measured git 2.56.0 firing matrix for each config key.
- `files/ab-control.txt` — the same-clone A/B control (poison vs no poison).
- `traces/*.trace.gz` — the raw strace traces for all twenty-two runs plus the live-sibling run.

Scope: read=probe-git-child-env-r31.py, tools/_revision.py, the eleven target tools, git 2.56.0 config semantics, corpus/lessons/round-30.md, corpus/lessons/round-30-verifier-spotcheck.md; wrote=.ufo/waves/round-31/w1/SentinelRepoLocal.md, .ufo/waves/round-31/w1/SentinelRepoLocal/files/{harness.py,results.json,RECAP.txt,ab-control.txt}, .ufo/waves/round-31/w1/SentinelRepoLocal/traces/*.trace.gz; executed=git clone/checkout/strace/python3 harness runs under /fast/scratch/hyaku/tsukuroi-r31/SentinelRepoLocal (read-only on the lane; no git/jj write in the lane or fleet repo).
Model: MiniMax-M3.1-Flash (minimax-code/MiniMax-M3.1-Flash)
Installs: none
