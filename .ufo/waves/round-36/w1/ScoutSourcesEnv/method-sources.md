# Method sources — untraced child-env view

Heading time: 02:48:58Z (`date -u +%H:%M:%SZ` immediately before this write).
Seat: ScoutSourcesEnv. Read-only recon. No production edit. No tool installed.

Registry read: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md` (live worktree; last table id **S197**; **S198 is not a row yet**). Declaration commit `6d76fb20f6ecbc940e5c8fff36c74060c885e161` reserves S198 for journalctl(1). A method row, if the L1 opens one, is the next free id after that (S199), not S198.

## Answer

**No.** The lane does not hold a source that legitimates PATH-interposition wrappers as a child-environment observation channel.

No registry row's question or establishes-clause names PATH-interposition, a wrapper placed on `PATH`, or an untraced log of `/proc/self/environ`. The traced channel the current probe uses is sourced (S173). The two facts the untraced view needs are only partly present, and neither row authorizes the channel:

- search half — a slash-free name is sought in `PATH` from the front until an executable is found (text sits inside S176's anchor, but the row's own scope refuses tool/probe use);
- read half — `/proc/pid/environ` is the initial `execve(2)` environment and does not show later scrubs (S181), scoped "not host or probe behavior".

**A new tier-A row is needed for the search half. The probe predicate does not suffice as method.**

Do not open the prompt's two candidates as that row:

- **ld.so(8) is already S171** and is the wrong mechanism (dynamic-linker `LD_PRELOAD` / `LD_LIBRARY_PATH` / `LD_AUDIT`, not command search).
- **execve(2) is the wrong page for PATH search.** Local man-pages 6.19 `execve(2)` (footer `Linux man-pages 6.19 2026-02-08`) says the libc variants "including ones that search the PATH environment variable" are on `exec(3)`. The envp handoff is already S176. Opening `execve(2)` would duplicate S176 and still miss the wrapper.

Open, if the untraced view is described as a method: **man-pages 6.19 `exec(3)`** (same pin family as S171 / S176 / S181), the `p` functions (`execlp`, `execvp`, `execvpe`). Pair the read with the existing **S181** snapshot; do not reopen `proc_pid_environ(5)` unless the lesson needs a sentence the establishes-clause compressed.

## What "the channel" is

From the wave-1 probe seat text (not this seat's design; `.ufo/waves/round-36/l1/gen-w1-spec.py` seat `ExecProbeR36`): wrappers named `git` / `python3` / `bash` / `sh` in a directory prepended to `PATH`; each wrapper appends `/proc/self/environ` to a log, then execs the real binary from `/usr/bin`. Children that inherit the ambient `PATH` hit a wrapper; fixed-`PATH` children do not. That log is the untraced view, independent of strace.

Dependency: `.ufo/waves/round-36/w1/ExecProbeR36/` was absent when this seat listed `w1/` (other seats had started). This finding does not wait on that draft. The landed counter is `tools/probe-child-env-allowlist-r34.py`, whose method is strace, not wrappers (docstring lines 33–34: `strace -f -e trace=execve -v`).

## Hits (child-env / exec / environ cluster)

Keyword pass over every `| S…` row, then column-split. Ids that actually bear on execve, strace, `/proc/pid/environ`, `PATH`, or interposition:

| id | tier | status | bears on | legitimates PATH-wrapper channel? |
|---|---|---|---|---|
| S171 | A docs | mined | ld.so(8) 6.19: `LD_LIBRARY_PATH`, `LD_PRELOAD`, `LD_AUDIT`, secure-execution | **No.** Linker interposition. `LD_PRELOAD` overrides functions in a loaded ELF object. It does not make a bare `git` resolve to a script earlier on `PATH`. |
| S172 | A docs | mined | CPython 3.14.8 `-E`/`-I`/`PYTHON*` | No. Not children, not `PATH` search. |
| S173 | A docs | mined | strace 7.2 `-f -qq -v -s`; environment calls unabbreviated | **No.** This is the **traced** channel the r31–r34 probes use. The untraced view is defined as independent of it. |
| S174 | A code | mined | glibc 2.44 `unsecvars.h` SUID removal list (34 names) | No. Allow-list construction for SUID policy, not an observation channel. |
| S175 | A docs | mined | Bash 5.3 `BASH_ENV` / `ENV` startup files | No. Anchors are invocation files, not `PATH` search. |
| S176 | A docs | mined | environ(7) 6.19: execve-supplied environment, fork copy, `PATH` convention | **Partial text, no.** See quotes. Row question: "not proof of how a particular tool constructs or filters its child environment." Establishes-clause does not mention search-order interception. |
| S179 | C community | **rejected** | Stack Overflow `os.environ.copy()` + change `PATH` | No. Rejected. The accepted answer copies the ambient environment. Not an observation method. |
| S180 | A docs | mined | CPython 3.14.8 `subprocess` `env=` (doc lines 648–650 only) | **No.** Construction: an explicit mapping replaces inheritance. Anchor does not include executable search. |
| S181 | A docs | mined | `proc_pid_environ(5)` + `TracerPid` | **Read half only, and the row forbids probe use.** "/proc/pid/environ describes the initial execve(2) environment"; question says "not host or probe behavior." |

No row for `exec(3)`, `execvp(3)`, `execve(2)`, or `posix_spawnp`. `execve(2)` appears only inside S027's capabilities bounding note, S176, and S181. S197 is the last id. Leads section has no exec/PATH-wrapper lead.

False friends from a bare `PATH` grep (not this question): S016, S021, S022, S028, S035, S039, S041, S045, S047, S048, S051, S055, S059, S079, S085, S086, S102, S110, S117, S119, S131, S134, S140, S141, S148, S158, S162, S163, S168, S178, S182, S195. Those are filesystem paths, `ProtectSystem`, or unrelated "path" wording.

## Quotes that bound the closest rows

S176 saved snapshot `.ufo/waves/round-32/w1/ScribeSrcEnviron7/environ.7` lines 132–144 (inside the registered anchor 132–155):

> PATH
> The sequence of directory prefixes that sh(1) and many other programs employ when searching for an executable file that is specified as a simple filename (i.a., a pathname that contains no slashes). The prefixes are separated by colons (:). The list of prefixes is searched from beginning to end, by checking the pathname formed by catenating a prefix, a slash, and the filename, until a file with execute permission is found.

Lines 18–20: the environment array "is made available to the process by the execve(2) call when a new program is started."

S176 establishes-clause (registry, not the man page): "execve makes an environment available to a newly started program, and a fork-created child inherits a copy; the manual lists the common variable conventions above, but does not establish any lane tool's filtering behavior."

That search paragraph is why a prepended directory *can* intercept a slash-free name, for `sh(1)` "and many other programs." It does not name libc `execvp`, CPython `subprocess`, or a wrapper used as an observer. Citing S176 for the untraced view would exceed the row.

S181 saved `.ufo/waves/round-33/a3w1/SrcProcPidStatus/proc_pid_environ.5` lines 12–16 and 26–36:

> This file contains the initial environment that was set when the currently executing program was started via execve(2).

> If, after an execve(2), the process modifies its environment (e.g., by calling functions such as putenv(3) or modifying the environ(7) variable directly), this file will not reflect those changes.

Lines 43–47: access is a `PTRACE_MODE_READ_FSCREDS` check. The wrapper reads **its own** `/proc/self/environ` at its start, which is the file the page describes, not another process's. The registered establishes-clause compresses this and marks the "target can inspect" sentence `[inf]`. Enough to quote for the read; not a license to call the wrapper an observation channel.

## Why the predicate is not a method

`tools/probe-child-env-allowlist-r34.py` `PREDICATE` (lines 195–213) defines when a `(target, channel)` pair is **leaking**: a traced `execve` after the target's first exec carries an injected name or a run-unique value, or `execveat` / unparseable record / missing git settings / parity break / source-scan hit. Label on that file is `leaking` (line 215). The round-36 declaration renames the frozen label to `leaking_pairs` and adds an untraced view; it does not say the predicate is the reason a wrapper log line is the child's environment.

The predicate assumes an observation channel. Today that channel is strace, which S173 covers. Replacing the channel without a source leaves the new view unsourced. Counting `leaking_pairs` does not establish that the log was produced by PATH search or that the bytes are the execve environment.

## Recommendation (what to open)

1. **Needed: one new tier-A docs row, man-pages 6.19 `exec(3)`.** Local render this seat (`man -s 3 exec`), footer `Linux man-pages 6.19 2025-05-17`. Not a saved snapshot and not a registry row. Quoted from that render, `p - execlp(), execvp(), execvpe()`:

   > These functions duplicate the actions of the shell in searching for an executable file if the specified filename does not contain a slash (/) character. The file is sought in the colon-separated list of directory pathnames specified in the PATH environment variable.

   > If the specified filename includes a slash character, then PATH is ignored, and the file at the specified pathname is executed.

   Same page: the `p` functions continue searching after `EACCES`, and on `ENOEXEC` they run `/bin/sh` with the file as its first argument. The slash sentence is also the bound: an absolute-path exec (`/usr/bin/git`) never hits the wrapper. That hole stays with the strace channel (S173). `execvpe` searches `PATH` from the **caller** environment, not from the `envp` it passes — relevant if a tool puts the wrapper dir only in the child's `PATH`.

   Local `execve(2)` lines 39–42 (same man-pages 6.19, footer 2026-02-08), the cross-reference that disqualifies execve(2) as the PATH source:

   > This manual page describes the Linux system call in detail; for an overview of the nomenclature and the many, often preferable, standardised variants of this function provided by libc, including ones that search the PATH environment variable, see exec(3).

2. **Not needed as a new row: the read half.** Quote S181 lines 12–16 and 26–36. The wrapper is the program image `execve` started, so its first read of `/proc/self/environ` is the initial environment; a later `putenv` in the real binary is invisible to that file, and cannot precede the wrapper's read because the wrapper is the image that was entered. `[inf]` on one residual: the same page says `PR_SET_MM_ENV_START` can retarget the memory the file refers to. A normal `git`/`python3` child does not do that before the wrapper runs; a target that did would be the wrapper itself, which the probe controls.

3. **Do not stretch S171.** Its establishes-clause is linker search and `LD_PRELOAD` function override under secure-execution rules. A PATH wrapper is not an audit object and not a preloaded ELF.

4. **Optional second pin, only if the lesson claims Python `subprocess` is the searcher.** Installed CPython **3.14.8** (`python3 -c` → `3.14.8 (main, Oct  2 2026, …)`), `/usr/lib/python3.14/subprocess.py` lines 1911–1917: if `os.path.dirname(executable)` is empty, the child tries `os.path.join(dir, executable)` for `dir` in `os.get_exec_path(env)`; otherwise it uses the path as given. `os.py` `get_exec_path` (lines 649–690) reads `env['PATH']` when `env` is passed, else `os.environ`, and splits on `os.pathsep`. That is the caller-side of the wrapper, and it is **not** inside S180 (S180 is doc lines 648–650, the `env=` mapping, sha256 pinned, no snapshot path in the row). Do not rewrite S180. If this pin is wanted, it is a new row on the 3.14.8 tag of `Lib/subprocess.py` (or the doc paragraph that states the same rule), not the installed-tree lines alone. `[unk]` whether `Doc/library/subprocess.rst` at tag v3.14.8 states the slash rule in prose; this seat did not re-fetch that file.

5. **Id hygiene.** S198 is declared for journalctl(1) and is not in the table. Do not use S198 for exec(3).

## Confidence and gaps

- High: no existing row legitimates the wrapper channel; S171/S173/S176/S180/S181 scopes are the registry text quoted above; S176 and S181 snapshots contain the quoted lines; local exec(3)/execve(2) footers are man-pages 6.19.
- Medium: exec(3) quotes are a local `man` render, not a hashed upstream snapshot. The L1 still has to pin tag `man-pages-6.19` bytes before the row is mined.
- Not done: no fetch of exec(3) from kernel.org cgit; no hash compare of installed `subprocess.py` to the v3.14.8 tag; probe draft not present.
- LSP: not used. The question is a markdown registry, not a code symbol. Rows were taken by splitting the table, not by grep-as-proof of a call graph.
