# Round 34 w1 — ReadRunChannels: code reading of the probe's run channels (defect 4, item 3)

Verdict (code-reading item, no control scored): the run channels (`carriers`, `value_carriers`,
`is_git`+kept-settings, `parity`, `one_run`/`parse_trace`) do NOT flag 9 construct classes that
pass ambient environment values to child processes; 2 classes are inside the declared named limit
(S181, the read side). NO-EXEC item: nothing was run or built; every claim is from reading the
frozen probe at `6de666c` (sha256 `35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8`,
914 lines; I saved the exact bytes to `/fast/scratch/hyaku/tsukuroi-r34/ReadRunChannels/probe.py`).
All line numbers are from that file at that commit.

Frozen rule facts read from the file: `carriers` = probe.py:445-460 (name-presence via
`item.startswith(name + '=')` at :456, over `execs[1:]` at :452); `value_carriers` = :463-473
(exact `NAME=VALUE` match against `wanted` at :466/:470-471); `is_git` = :293-294; kept-settings =
`KEPT_GIT_SETTINGS` at :197 and check at :344-345; `parity` = :350-355 over `rc`/`stdout_sha256`/`git_execs`
(:352), with stdout normalisation at :333-335; `one_run` = :309-347 (`strace -f -qq -v -s 65536 -e trace=execve`
at :327-328, `env` = hermetic + extra at :323-325, `execs` = `parse_trace(trace)` at :341);
`parse_trace` = :261-290 (only successful execve records, :282-283); `parse_strings` = :234-258.

## Findings, by severity

1. [outside named limit] **Passing an ambient value through a channel the tracer does not inspect:
argv, stdin/stdout pipe, a file, a socket, or an fd.** A lane tool can copy an ambient name/value
into the child's argv (e.g. `subprocess.Popen([..., os.environ['BASH_ENV']], env=clean_env)`) or
write it to a file the child reads after starting clean; the run channels look only at the `envp`
array of each traced execve (`carriers` :452-457, `value_carriers` :468-472), never argv, fds,
pipes or files. Source scan does not see it either (the `os.environ` attribute read at :687 is the
only trigger; a copy read via a loop is a clean `Attribute`). Example (text only):
`subprocess.Popen(['/bin/sh', '-c', 'printf %s "$1" >&2', 'sh', os.environ['XDG_CONFIG_HOME']], env=clean)`
→ misses at `carriers` :452-457 and `value_carriers` :468-472.

2. [outside named limit] **Renaming the key: an injected or value-channel name carried under a
different name.** `env={'MY_HOME': os.environ['HOME']}` puts the run-unique HOME value in the
child under `MY_HOME`; the name check (`carriers` :456) matches only names in the run's injected
list, and the value check (`value_carriers` :466/:470) matches only the exact 10 `NAME=VALUE`
strings — a renamed value matches neither. (Rename also defeats the prefix rule: `BASH_ENVX=` is
caught, but a leading-space or renamed key is not.) Source sees only the `os.environ` read (:687),
not the rename.

3. [outside named limit] **Mutating the value of a value-channel name.** `value_carriers`
(:466, :470-471) requires the exact ambient `NAME=VALUE` string; any mutation (append, prefix,
substring, encoding/case change) passes silently, e.g. `env={'PATH': os.environ['PATH'] + ':/extra'}`.
The name-presence rule never applies to the ten value names (they are not in the injected `names`
lists, :868, :200, :364-388), so a child carrying `PATH=/usr/bin:/bin:<inject>/<random>:/extra`
is not flagged. Source sees only the `os.environ` attribute read (:687).

4. [outside named limit] **Unwatched ambient names: any ambient name that is neither an injected
name nor one of the ten value names.** The run checks only the per-run injected `names` (fixed four
plus eight random, `build_injection` :425, :432-437; `names` list at :868) and the ten
`VALUE_NAMES` (:194-195). Every other ambient name that `hermetic_env` keeps (:216-217) — e.g.
`LC_*` (except `LC_ALL=C` forced at :218), `HOSTNAME`, `XDG_*` other than `XDG_CONFIG_HOME`,
`TERM`'s siblings, `GIT_CONFIG_SYSTEM` (set at :226), any user name — flows to children unflagged if
it is not one of the injected names. Concrete: a tool passing `os.environ['HOSTNAME']` through to a
git child leaks the ambient value with no evidence (the keep-settings check `git_missing_kept`
:344-345 only demands the two `GIT_CONFIG_*` strings, not a clean *rest*). Source sees the
`os.environ` read (:687) but the run channels do not.

5. [outside named limit] **Starting a child that never execs (`os.fork()`), so no execve record
exists.** `one_run` traces only `execve` (:327-328); a forked child that inherits the ambient
`env` (with all injected names) and calls `os._exit()` or communicates back via a pipe produces no
record. `carriers`/`value_carriers`/`parity` see nothing (work on `execs`, :452, :468, :343).
The source channel also misses `os.fork()`: `OS_INHERIT` (:478-479) contains `spawn*` but not
`fork`; `SPAWN_ANY` (:482-485) lists `fork` only for the alias/getattr rules — there is no `head
== 'os'` branch for `fork` before the `elif` at :728, so no finding is emitted.

6. [outside named limit] **A child started by a spawner the tracer does not follow (re-parenting
outside the traced tree): `systemd-run`, `at`, `cron`, a detached daemonizing service.** The
probe's `strace -f` watches only descendants of the target (:327-328); a target that hands an
ambient value to `systemd-run --setenv` or a `cron` job hands it to a process outside the traced
tree, whose own `execve` is never recorded. (The target's own launch execve of the spawner is
recorded, but its envp carries only what the tool passes at *that* exec — which the tool can keep
clean while passing the value in argv.) Misses at `one_run` :327-328 and `parse_trace` :261-290.

7. [outside named limit] **`execveat(2)` (and `fexecve`): a distinct syscall the trace regex does
not match.** `parse_trace` matches only `execve\("` (:264); CPython's `os.execve` uses
`execveat` when `dir_fd` is given or `follow_symlinks=False`, and `os.execveat`/`fexecve` use it
directly, so such an exec is invisible to `carriers`, `value_carriers`, `git_execs` and parity.
`execveat` is a real, separate syscall (x86-64 `__NR_execveat 322`; `/usr/include/asm/unistd_64.h:326`
and `/usr/include/unistd.h:300` declare it) [inf: that Python maps `os.execve(dir_fd=...)` to it is
from CPython's documented behaviour, not verified on this host].

8. [outside named limit] **Erasing the exec record via a >64 KiB environment string.** The strace
line for a child is captured with `-s 65536` (:327); a value longer than that is truncated with no
closing quote, `parse_strings` runs to end-of-line (:243-253), and the record is then dropped
because `rest` no longer shows `= 0` (:278-283). The child's env is then invisible to all run
checks (and, if it is a git exec, to `git_execs`, which also breaks parity unless the control run
pads identically).

9. [outside named limit] **A git child run through a non-standard path.** `is_git` (:293-294)
matches only `SYSTEM_GIT` (`/usr/bin/git`, :177) and `/usr/lib/git-core/*`; a git invoked via a
symlink, a copy, or `git` found through a different PATH is not counted by `git_execs` (:343) and
escapes the kept-settings clause (`git_missing_kept` :344-345). Its env is still seen by
`carriers`/`value_carriers`, but the `GIT_CONFIG_*` requirement never applies; if control and
channel runs make different use of such a path, parity (rc/stdout/git count) is unchanged, so the
missing settings go unflagged.

10. [inside named limit] **Trace-gating: behave differently when traced, so the injected run only
ever sees the clean branch.** A target that learns it is observed (e.g. reads `/proc/self/status`
`TracerPid`) and, only when observed, scrubs the child env, never leaks under the probe (every run
is traced), so all run evidence is empty while an untraced production run leaks. This is exactly
the read side S181 leaves open, so the class is inside the named limit; the run channels contain no
rule that sees it (they only see execve envp under the tracer).

11. [inside named limit] **Procfs re-read of the initial environment: reading `/proc/self/environ`
(or a parent's `/proc/<pid>/environ`) after a clean exec, and merging those bytes into the child
env or a side channel.** The run channels inspect only the envp at each execve; an environment
assembled by the children from procfs is never compared against the injected names. This is the
same S181 read-side hole, whether the read runs in the target (before its first exec) or in the
child itself; both are inside the named limit. (Passing the pre-exec `os.environ` copy via
argv/files is class 1, outside.)

## Named limit assessment

The declared named limit is the read side: a target that learns through procfs that it is traced
and reads its initial environment there (S181). Classes 10 and 11 are inside it. All others
(1-9) rely only on ordinary `os.environ` reads (or no read) and normal spawn plumbing; none requires
procfs or trace awareness, so they are **outside** the named limit. Count of classes OUTSIDE the
named limit: **9**.

## What kinds of children the runs see

- Non-git children: seen if and only if they perform a successful, parseable, `-e trace=execve`
  matching execve (name `execve` — not `execveat`) that is a traced descendant while the run is
  alive; their envp is checked for injected names and value strings (`carriers` :452-457,
  `value_carriers` :468-472). A child of a non-git kind carrying *nothing* new is not a leak only
  because there is nothing to carry; a child carrying a renamed/mutated/unwatched value is missed
  (classes 2-4).
- A child that re-execs: re-entry is visible if the later execve succeeds and parses; its env is
  checked at *each* execve, so an intermediate re-exec with a dirty env is caught even if a later
  one is clean. If an intermediate re-exec is itself performed via `execveat` (class 7) or with an
  oversized envp (class 8), it is invisible.
- A long-lived daemon: visible for as long as it is a traced descendant and is still executing its
  own execves; a daemon that detaches from the traced tree (double-fork into a service, or a
  spawner like `systemd-run`) is no longer observed (class 6). A daemon that lingers past the
  run's `strace` window is not observed at all.
- A child started after the target exits: not a *descendant* at exec time is not seen; a descendant
  that execs after the main process exits is still traced (strace keeps the process tree), so it is
  seen if its execve is parseable. Children of spawners the target started and left behind (class
  6) are invisible.
- The first record is the target's own exec and is always skipped (`execs[1:]`, :452, :468); the
  hooks' own execves are outside the same window, and children of the harness (git calls for
  export/clone) happen before/outside the per-run trace and are not counted.

## Verification notes

- NO-EXEC: no command other than read-only `git show`, `grep` for registry/syscall facts, and
  `sha256sum` of the saved bytes was used; nothing was built or run. The probe was not executed.
- Evidence for line numbers: file saved from `git show 6de666c:tools/probe-child-env-allowlist-r34.py`
  (sha256 `35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8`, matching the declared
  hash); all "probe.py:NNN" pointers are to that file. Registry: `corpus/SOURCES.md:187` (S181,
  proc_pid_status/proc_pid_environ). Syscall facts: `/usr/include/asm/unistd_64.h:326`
  (`__NR_execveat 322`), `/usr/include/unistd.h:300` (execveat declaration).
- `execveat`/`fexecve` usage by CPython's `os.execve` with `dir_fd`/`follow_symlinks=False` is
  [inf] from documented CPython behaviour, not verified on this host.
- No server was available for any file (`lsp` is not present in this environment); all semantics
  are from direct reading of the cited bytes.

Scope: read=<frozen probe at 6de666c; SCORECARD.md round-34 declaration; corpus/SOURCES.md S181;
/usr/include syscall tables>; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ReadRunChannels.md, /fast/scratch/hyaku/tsukuroi-r34/ReadRunChannels/probe.py (exact frozen bytes, sha256 35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8); executed=read-only git show, grep, sha256sum (no probe runs, no builds)
Model: not exposed
Installs: none
