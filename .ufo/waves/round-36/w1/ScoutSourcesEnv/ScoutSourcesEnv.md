# ScoutSourcesEnv

Heading time: 02:48:58Z (`date -u +%H:%M:%SZ`).
Evidence: `method-sources.md` in this directory. No production edit. No package installed (pacman paused; nothing needed).

## Finding

**No.** `corpus/SOURCES.md` has no row that legitimates PATH-interposition wrappers as a child-environment observation channel.

Last registry id is **S197**. S198 is reserved by the round-36 declaration for journalctl(1) and is not in the table. There is no `exec(3)` / `execvp(3)` / `execve(2)` row.

Child-env cluster and the verdict on each:

- **S173** (strace 7.2, tier A, mined) — the traced channel (`-f`, `-v` unabbreviated environment calls). Not the untraced view.
- **S176** (environ(7) 6.19, tier A, mined) — closest text. Saved snapshot lines 132–144, inside the registered anchor, describe `PATH` search for a slash-free filename "from beginning to end" until an executable is found. The row's question and establishes-clause refuse using it as proof of a tool's or probe's child environment. Not a wrapper-channel source.
- **S181** (`proc_pid_environ(5)`, tier A, mined) — read half only: the file is the initial `execve(2)` environment and does not reflect later `putenv`. Question says "not host or probe behavior."
- **S171** (ld.so(8), tier A, mined) — linker `LD_PRELOAD` / `LD_LIBRARY_PATH` / `LD_AUDIT`. Wrong interposition. Do not cite it for a `PATH` wrapper.
- **S180** (CPython 3.14.8 `subprocess` `env=`, lines 648–650 only) — construction, not search, not observation.
- **S172, S174, S175** — `PYTHON*`, glibc SUID removal list, Bash `BASH_ENV`. Not this channel.
- **S179** — rejected tier C. Copy-`os.environ` advice, not an observation method.

The r34 probe predicate (`leaking` in `tools/probe-child-env-allowlist-r34.py`; declaration label `leaking_pairs`) is the **measure**. It assumes a channel. It does not say why a wrapper's `/proc/self/environ` log line is the child's environment. It does not substitute for a method source.

## Recommendation

Open one new tier-A row: **man-pages 6.19 `exec(3)`**, the `p` functions. Local `man -s 3 exec` (footer `Linux man-pages 6.19 2025-05-17`, not yet a snapshot) states that a filename with no slash is sought in `PATH`, and a filename with a slash ignores `PATH`. That second sentence is the absolute-path hole; strace (S173) still sees those execs.

Do not open ld.so(8) again. Do not open execve(2) as the PATH source: local man-pages 6.19 `execve(2)` (footer 2026-02-08) defers PATH search to `exec(3)`. The envp handoff is already S176. Keep S181 for the `/proc/self/environ` read; quote its saved lines 12–16 and 26–36 rather than stretching the establishes-clause.

Optional, only if the lesson claims Python is the searcher: a **new** row on CPython 3.14.8 `subprocess` executable search. Installed 3.14.8 `subprocess.py` lines 1911–1917 call `os.get_exec_path(env)` when the executable has no directory component. That text is not inside S180. Do not rewrite S180. `[unk]` whether the v3.14.8 doc rst states the same rule; this seat did not re-fetch it.

Id: not S198.

## Dependencies

`.ufo/waves/round-36/w1/ExecProbeR36/` was absent at listing time. Not required: the landed method is strace (`probe-child-env-allowlist-r34.py` lines 33–34).

## Confidence

High on the negative registry result and on the S176/S181 quotes (saved snapshots). Medium on the exec(3) wording until the L1 pins man-pages-6.19 bytes. LSP unused: markdown registry, table split, not a call graph.
