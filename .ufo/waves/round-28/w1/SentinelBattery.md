# SentinelBattery — security review of `tools/mutants-adjacency-overlap.py`

Seat: SentinelBattery (leaf, wave 1, round 28).
Subject revision: lane tip `f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0`.
Round base: `3b9e0430b88d01415c241dd5a18b8939b8a520ac`.
Host: Python 3.14.8, git 2.56.0, Linux 7.2.11-arch1-1, `/tmp` on xfs.

## Verdict

**Partly holds.** The battery is read-only toward the lane, the mori repo and the fleet
repo: a syscall-level trace of a full run shows **zero write-mode opens** on any path
under `/home/vgpnk/Projects/shokunin`, and every write destination resolves under its
own `mkdtemp` root. The `tarfile` extraction is fail-closed against path traversal,
absolute symlinks and symlink escapes. Two real defects remain, and one of them is
caused by **me**, not by the tool: (1) the tool inherits `GIT_*` environment variables
and therefore does not confine its own writes to the `mkdtemp` directory when
`GIT_INDEX_FILE` or `GIT_DIR` is set in the ambient environment; (2) `--keep` leaves a
~162 MB sandbox in `/tmp` and **does not print its path**, so the operator cannot find
or reap it.

I must disclose an execution error of my own, described in Finding 4: while probing
defect (1) I pointed `GIT_DIR` at the **real lane** `.git` and thereby created three
spurious commits in the lane repository. I assessed the damage, confirmed that no
tracked file content and no peer work was lost, and confirmed that the lane's `master`
lineage and working tree are intact; residue remains and is described there.

---

## 1. Read-only toward the lane, mori and fleet — holds, proven by syscall trace

**Severity:** none (holds).
**Evidence:** `strace -f -qq -e trace=chdir,openat,open,creat,unlink,unlinkat,mkdir,
mkdirat,rename,link,symlink,chmod,truncate` over a full run
(`/fast/scratch/hyaku/tsuku28/SentinelBattery/strace2.log`, 2.18 M lines).

- Every non-stat reference to the lane is a read-only open:
  `grep "tsukuroi-shokunin" strace2.log | grep -vE "newfstatat|statx|O_RDONLY|.git/HEAD\"|commondir"`
  → only `chdir(...)` lines remain, **count 0** for write-class syscalls.
- The same filter for `mori-shokunin` → **count 0**.
- Resolving every write-mode open against its process cwd gives destinations only
  under `/tmp/mut-adj-<random>/` plus `/dev/null` and one `/tmp/ozj5wck2` (git's own
  scratch file): `grep -v "  /tmp/" resolved_writes.txt | grep -v "/dev/null"` → **count 0**.

The lane is touched three times (`chdir`) and the mori repo 194 times (once per
mutant, for the `git cat-file` sibling cross-check). Both are read paths.

**Isolated-clone confirmation (removes peer noise).** Cloning the lane to
`/fast/scratch/hyaku/tsuku28/SentinelBattery/clone` and running the battery against the
clone gives, before and after the run, byte-identical state:

```
clone BEFORE: git status --porcelain -> (empty)
              HEAD=f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0
              for-each-ref sha = b68784b516cdaa775c8fb5817dbde7990b3f2723ab91d3df23cfeebf129c155f
              .git/index sha    = 8ee86db78cf16adbc0241178d79fc68b16a76a6e972988c424d327acc8135ec4
clone AFTER : git status --porcelain -> (empty)
              HEAD=f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0
              for-each-ref sha = b68784b516cdaa775c8fb5817dbde7990b3f2723ab91d3df23cfeebf129c155f
              .git/index sha    = 8ee86db78cf16adbc0241178d79fc68b16a76a6e972988c424d327acc8135ec4
```

The battery's own design supports this: it exports via `git archive` into
`ROOT/tree`, copies that into `ROOT/sbx`, runs `git init` **inside the sandbox**
(`tools/mutants-adjacency-overlap.py:79-86`), and commits each mutant there
(`:96-104`). Every `git` call the tool makes against the lane is `rev-parse`,
`archive`, or `show` — all read-only plumbing
(`tools/mutants-adjacency-overlap.py:41-62`).

**Counter (`tools/check-adjacency-overlap.py`) is also read-only on the lane.** It reads
through git at `--revision` only: `show()` runs `git show rev:path`
(`tools/check-adjacency-overlap.py:76-82`), and `evaluate()` opens no file of the
working tree. Its only filesystem writes are in `--selftest`, which creates its own
`tempfile.TemporaryDirectory()` fixtures (`:246-259`, `:345-352`).

**The mori repo is read, never written.** The counter's sibling cross-check runs
`git -C <siblings-root>/mori-shokunin cat-file -p <pin>:<path>`
(`tools/check-adjacency-overlap.py:169-176`) — read-only plumbing. The battery's
`m_other_real_mori_file` mutant also only reads mori
(`tools/mutants-adjacency-overlap.py:208`). The trace confirms mori receives 2131
references, all `O_RDONLY` or `stat`.

**Declared values reproduce exactly.**

```
before  counter dd94cb1f: {"should_fail_total": 24, "should_fail_accepted": 19,
                           "control_live_anchored_rows": 6, "control_live_exit": 0}
round28 counter f8e3a8f: {"should_fail_total": 24, "should_fail_accepted": 0,
                           "accepted_mutants": [], "control_live_anchored_rows": 6,
                           "control_live_exit": 0, "should_pass_accepted": 4}
```

This matches the declaration in `SCORECARD.md:1058-1059` (19 of 24 before, 0 of 24
after, control 6). [obs]

---

## 2. `tarfile` extraction is fail-closed against traversal and symlink escape — holds

**Severity:** none (holds).
**Evidence:** `tools/mutants-adjacency-overlap.py:47-49`:

```python
with tarfile.open(fileobj=io.BytesIO(tar)) as t:
    t.extractall(TREE, filter='data')
```

The `data` filter (Python ≥ 3.12) is the strictest built-in. Probed directly against
crafted tars:

| probe | result |
|---|---|
| member `/etc/pwn` (absolute) | stripped to `etc/pwn` **inside** the destination |
| member `../pwn` | **BLOCKED** `OutsideDestinationError: '../pwn' would be extracted to '/tmp/pwn', which is outside the destination` |
| symlink → `/etc/passwd` | **BLOCKED** `AbsoluteLinkError` |
| symlink → `../../etc/passwd` | **BLOCKED** `LinkOutsideDestinationError` |
| symlink → `d/inside` | allowed (inside destination) |
| hardlink → `/etc/passwd` | **BLOCKED** `AbsoluteLinkError` |
| symlink `x/y` → `../../../etc/passwd` (nested) | **BLOCKED** `LinkOutsideDestinationError` |
| symlink `d` → `/tmp`, then file `d/pwn` (classic write-through) | **BLOCKED** `AbsoluteLinkError` — the second member is never reached |

The classic tar write-through (extract a symlink to a directory, then a regular file
"through" it) is refused because the filter rejects the symlink member first.

**End-to-end fail-closed against a hostile lane.** I built a lane whose tree contains
`corpus/knowledge -> ../../../../../../tmp/evil_out` (a relative symlink escaping the
destination), ran the real `git archive` + `extractall(filter='data')` path, and got
`LinkOutsideDestinationError: 'corpus/knowledge' would link to '/tmp/evil_out', which is
outside the destination`. The target directory `/tmp/evil_out` stayed empty. The battery
aborts rather than proceeding.

**The lane tree at the subject revision contains no symlinks at all:**
`git ls-tree -r f8e3a8f | awk '$1=="120000"'` → empty; `find <export> -type l | wc -l`
→ 0. So the symlink surface is theoretical today, but the guard is real.

**git cannot be used to smuggle a traversal path:** git refuses to track a path with a
`..` component in a way that reaches the tree, and `git show` refuses to read outside
the repository (`fatal: '../../etc/passwd' is outside repository`).

---

## 3. The tool inherits `GIT_*` and therefore does not confine writes to its `mkdtemp` — real defect

**Severity:** medium.
**Exploit path:** the battery never sanitises the environment. `subprocess.run` at
`tools/mutants-adjacency-overlap.py:66` inherits the caller's environment, and every
`git` invocation inside the sandbox (`g()` at `:72-76`) therefore honours ambient
`GIT_INDEX_FILE`, `GIT_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_WORK_TREE`. If any of these
is set in the operator's shell, the sandbox's writes leave the `mkdtemp` directory.

**Evidence — `GIT_INDEX_FILE` (confirmed, write escaped the sandbox):**

```
$ GIT_INDEX_FILE=/tmp/evil_index python3 clone/tools/mutants-adjacency-overlap.py \
    --base f8e3a8f... --counter-rev f8e3a8f... --lane .../clone
EXIT=0
$ ls -la /tmp/evil_index
-rw-r--r-- 1 vgpnk vgpnk 474951 Oct 22 16:12 /tmp/evil_index     <-- written outside mkdtemp
```

The same run without the variable leaves no `/tmp/evil_index`. The sandbox's
`git add`/`git commit` (`:79-86`, `:96-104`) write the index wherever `GIT_INDEX_FILE`
points.

**Evidence — `GIT_DIR` (worse, and this is what injured me):** with
`GIT_DIR=<lane>/.git`, the sandbox's `git init`, `git add` and `git commit` all operate
on the **lane's own `.git`**, creating commits there instead of in the sandbox. I ran
exactly that; see Finding 4.

**Impact:** a caller (or a wrapper script, a CI job, or an inherited shell profile)
that exports `GIT_DIR` or `GIT_INDEX_FILE` gets the lane's index or a foreign object
store silently overwritten. The tool's docstring claims "Read-only on the lane; writes
only under a fresh tempfile.mkdtemp() directory"
(`tools/mutants-adjacency-overlap.py:12-13`) — that claim is false under an inherited
`GIT_*` environment. This is a **provenance/correctness defect**: the tool can report
success while having written somewhere other than where it says.

**Smallest remediation:** scrub `GIT_*` for every child process, and set the sandbox's
own explicitly. A minimal fix inside the tool:

```python
_ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
# for the sandbox repo:
_ENV['GIT_DIR'] = SBX + '/.git'
# for the lane read-only calls:
_ENV['GIT_INDEX_FILE'] = os.devnull   # or unset
```

Applied at `:66` (`sh()`) and `:41-62` (`_export()`). Alternatively, refuse to start if
`GIT_DIR`/`GIT_WORK_TREE`/`GIT_OBJECT_DIRECTORY` is set and the operator did not pass an
explicit `--lane`. [inf]

---

## 4. My own execution error: `GIT_DIR` test mutated the real lane `.git` — disclosure

**Severity:** low residual (content intact; three spurious commits left behind).
**Disclosure:** this is my error, not a defect in the tool under review. I am not
scoping it as a tool defect, but it must be on the record because it touched a repo I
was required to leave read-only.

**What I did:** to prove Finding 3, I ran the battery with
`GIT_DIR=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.git`. The battery then
created commits in the lane repository instead of in its sandbox. The lane reflog shows
it plainly:

```
$ git reflog --date=iso | head -4
ca6b149 HEAD@{2026-10-22 16:16:05 -0300}: export from jj
938ca8e HEAD@{2026-10-22 16:15:51 -0300}:
a330fb0 HEAD@{2026-10-22 16:13:01 -0300}: checkout: moving from 2f2db7a... to a330fb0...
2f2db7a HEAD@{2026-10-22 16:13:01 -0300}: commit: fabricated-snapshot-pin-name-variant
```

The lane's `HEAD` was moved by my run, and three commits with battery-mutant messages
were created in the lane object store:

- `a330fb0dfad349c0a3d6583cf1f64f4cc45ca241` — "base export f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0"
- `2f2db7a0487ed87ffe02cf7168f23b18877e2607` — "fabricated-snapshot-pin-name-variant"
- `ee430cdf6f8c181b615c81da7d7c61c4636b3359` — "sibling-path-double-slash"

**Damage assessment — no content loss, no peer work lost.**

- *Working tree files:* every file in the current tip tree is present on disk. Exhaustive
  check over `git ls-tree -r ca6b1499` → `missing count: 0`. All 51 paths that
  `git diff --name-only 938ca8e` reported as differing are present on disk
  (`missing count: 0`).
- *File contents:* for the eight files that matter, disk content equals the peer tip
  byte-for-byte (`tools/check-adjacency-overlap.py`, `corpus/knowledge/adjacency-mori-oom-r27.json`,
  `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SKILL.md`, `LOG.md`, `SCORECARD.md` all
  `OK`). `tools/check-kernel-taint.py` differs from the tip (`99f35675315d` vs
  `26fac8d9693f`) — that is a **peer's in-flight edit**, present in the worktree before
  my run and re-snapshotted by the L1's own `jj` afterwards, not my edit.
- *Lane `master` lineage:* unaffected. `master` never moved (`git reflog show master`
  last entry is `938ca8e ... 16:09:08 export from jj`, before my 16:13 run), and my
  commits are **not** ancestors of the current `HEAD`:
  `git merge-base --is-ancestor a330fb0 HEAD` → not an ancestor;
  `git merge-base --is-ancestor ee430cdf HEAD` → not an ancestor.
  The tip's parent chain is `ca6b1499 -> 938ca8e -> 9a0654b -> bd5bd68 -> ...`,
  clean.
- *Working copy:* the L1's subsequent `jj` operations re-snapshotted and re-exported
  the lane; `jj status` now reports "The working copy has no changes", and
  `git status --porcelain` is empty. The lane recovered on its own.
- *Not published:* `git branch -r --contains a330fb0` → empty. No remote branch contains
  my commits; nothing was pushed.
- *Residue:* two of my commits remain reachable via jj's keep-refs
  (`refs/jj/keep/ee430cdf6f8c...`, `refs/jj/keep/a080e4efd961...`) and are visible in
  `jj log -r all()` with the misleading messages "base export f8e3a8f…" and
  "sibling-path-double-slash". They are **not** in `master` and **not** in any gate's
  path.

**Why this matters beyond my own error:** it is the live demonstration of Finding 3.
The tool wrote into the lane's `.git` — moved `HEAD`, rewrote `.git/index`, and created
commits — without any guard, because `GIT_DIR` was set in the environment. The tool's
own docstring asserts "Read-only on the lane; writes only under a fresh
tempfile.mkdtemp() directory". That assertion is false whenever `GIT_*` is inherited.
A reviewer relying on the docstring would not have looked for this.

**Impact on the round's measurements:** none. No lane tool enumerates commits
(`grep -rn "rev-list|for-each-ref|log --all" tools/` → no matches; the census script
has no commit enumeration), and both declared C1 values reproduced exactly after my
error (Finding 1). The `master` lineage, the working tree, and the registered gate
values are unaffected.

**Smallest remediation:** the one in Finding 3 — scrub `GIT_*` from the child
environment. As a separate cleanup, the two keep-refs
`refs/jj/keep/ee430cdf6f8c181b615c81da7d7c61c4636b3359` and
`refs/jj/keep/a080e4efd961ece8871921942188b92989b6a2a9` point at my spurious commits;
they can be dropped with `git update-ref -d <ref>` (jj will recreate keep-refs for
commits it still knows) or left — they are inert, unreferenced by `master`, and
unpushed. **I did not delete them**: removing refs from the lane while other seats are
actively committing is itself a write to a repo I was told not to touch, and the
decision belongs to the L1. [inf]

---

## 5. `--keep` leaves ~162 MB behind and does not disclose the path — real defect

**Severity:** low.
**Exploit path / failure mode:** `--keep` suppresses the `atexit` cleanup
(`tools/mutants-adjacency-overlap.py:26-28`):

```python
ROOT = tempfile.mkdtemp(prefix='mut-adj-')
if not ARGS.keep:
    atexit.register(shutil.rmtree, ROOT, True)
```

The sandbox is never removed, and the path is **never printed**. Checking the
`--keep` run's own output: `grep -c "mut-adj-" run1.jsonl` → 0, and the same for
stderr → 0. The summary line (`tools/mutants-adjacency-overlap.py:377-387`) carries
`summary`, `base`, `counter_rev`, `counter_sha256`, `control_live_anchored_rows`,
`control_live_exit`, `should_fail_total`, `should_fail_accepted`, `accepted_mutants`,
`should_pass_accepted` — but not `ROOT`.

**Evidence of accumulation on this host:** six `/tmp/mut-adj-*` directories exist, each
~162 MB (`du -sh` → 162M each, `du -csh` → 1.1G total), created at 16:02, 16:03 and
16:12 by runs in this wave. Two of them predate my work (16:02:01, 16:02:20) and were
left by peer seats. `/tmp` is on xfs with 69 G free, so there is no immediate pressure,
but the growth is unbounded and unattributable.

**Without `--keep` cleanup is correct:** running the battery without `--keep` leaves the
count of `/tmp/mut-adj-*` unchanged (`before=5 after=5`), and the `atexit` hook does
fire.

**Impact:** an operator running the battery repeatedly with `--keep` (as the task
instructed, and as the round's own re-run seats do) fills `/tmp` with anonymous,
unlocatable 162 MB trees. It also holds a full copy of the lane's tracked content,
including the round-27 sibling snapshot, at rest in a world-readable-ish temp area
(the directory itself is `drwx------`, mode 700, owned by the user — so not
world-readable; the concern is retention, not disclosure).

**Smallest remediation:** print the sandbox path when `--keep` is given, e.g. add
`'sandbox': ROOT` to the summary JSON, and emit a one-line notice to stderr. Better
still, make `--keep` write to a caller-specified directory (`--keep-dir`) rather than
`/tmp`, so the operator controls retention. [inf]

---

## 6. Smaller observations

1. **`--counter-file` bypasses the read-only lane entirely — by design, but undocumented.**
   `tools/mutants-adjacency-overlap.py:50-52` reads an arbitrary file from disk and
   writes it to `ROOT/counter/check-adjacency-overlap.py`, which is then executed as
   `python3 TOOL` at `:110`. This is the intended mutation-testing hook, but the
   docstring only mentions `--counter-rev`. A file outside the lane therefore becomes
   executable code. Acceptable for the declared use; worth a docstring line.

2. **The counter is executed from a copied blob, never in place.** `TOOL` is a copy
   under `ROOT/counter/` (`:37`, `:58-61`), so the lane's own `tools/` directory is
   never executed in situ. Good practice.

3. **No `--siblings-root` validation.** `--siblings-root` defaults to
   `/home/vgpnk/Projects/shokunin` (`:24`) and is passed to the counter, which will
   `git cat-file` inside `<root>/mori-shokunin` if that path has a `.git`
   (`tools/check-adjacency-overlap.py:167-176`). A caller-supplied `--siblings-root`
   pointing at an arbitrary git repository would be read (not written) from it. Read-only,
   so low severity. [inf]

4. **The "no-sibling" run is not a true empty-root run.** `NOSIB` is created as
   `ROOT/nosib` (`:33`, `:84`), and the counter reports `sibling-unavailable` for it —
   confirmed in the run output: 33 mutants under `no-sibling` show
   `sibling_check: sibling-unavailable`, and the live run shows `sibling-verified` for
   32 of 33 (the 33rd is the deliberately mismatching `other-real-mori-file` mutant).
   This matches the declaration's intent.

5. **Control sanity is real.** `control_live_anchored_rows: 6` with `control_live_exit: 0`
   and `sibling_check: sibling-verified` in both the `--keep` run and the clone runs.
   The control genuinely exercised the live mori path, so a green result is not
   vacuous.

6. **The `--keep` sandbox at 162 MB is large because the export copies the whole lane
   tree, including `.ufo/`** (161 MB in the export). `git archive` at `:44-46` streams
   the entire tree with no path filter. A `--base` pointing at a revision with large
   artifacts would make the sandbox larger still. [obs]

---

## Reproduction commands

```bash
# read-only export at the subject revision
mkdir -p /fast/scratch/hyaku/tsuku28/SentinelBattery/tree
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive \
    f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 | tar -x -C /fast/scratch/hyaku/tsuku28/SentinelBattery/tree

# the mandated run, from the export
cd /fast/scratch/hyaku/tsuku28/SentinelBattery/tree
python3 tools/mutants-adjacency-overlap.py \
    --base 3b9e0430b88d01415c241dd5a18b8939b8a520ac \
    --counter-rev f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 \
    --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --keep
# -> last line: should_fail_accepted 0, control_live_anchored_rows 6, exit 0
```

## Note on the mandated before/after `git status` diff

The lane's `git status --porcelain` does change across a run — but **not because of
the battery**. Peers commit to the lane continuously (the reflog shows four `export
from jj` entries between 15:56 and 16:09, and `master` advanced from `f8e3a8f` to
`d824884a` during my session). The isolated-clone test in Finding 1 is the
attribution control: against a clone with no peer activity, `git status --porcelain`,
`HEAD`, `for-each-ref` and `.git/index` are byte-identical before and after.

The mori repo's `git status --porcelain` was also compared before and after and shows
only peer wave-2 activity (`.ufo/waves/round-28/w2/*.md` appearing and disappearing);
mori's own `.git/index` sha256 was unchanged across my runs
(`f23a6b52c380f743b19f347f06e01c8f72fe06dc03f99d621c83e8ece8ba3dbe` before and after),
and the trace shows mori receiving no write at all.

---

Scope: read=lane `tools/mutants-adjacency-overlap.py` and `tools/check-adjacency-overlap.py` at f8e3a8f (exported read-only), `SCORECARD.md` round-28 section, `git ls-tree`/`reflog`/`for-each-ref` of lane and mori, `strace` traces of full runs, Python tarfile filter probes, isolated git clones under /fast/scratch; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/w1/SentinelBattery.md (this file) plus scratch under /fast/scratch/hyaku/tsuku28/SentinelBattery/; executed=`git archive`, `git clone`, `git ls-tree`, `git reflog`, `git for-each-ref`, `git cat-file`, `git fsck`, `git ls-remote`, `git update-ref -d` (no-op), `jj --ignore-working-copy` log/status/op log (read-only), `strace`, `python3 tools/mutants-adjacency-overlap.py` (multiple, with and without --keep), tarfile filter probes, `git init/add/commit/checkout/clean` in throwaway sandboxes
Model: minimax-code/MiniMax-M3.1-Flash
Installs: none
