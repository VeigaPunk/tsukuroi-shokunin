source: S219, S220, S221, S222, S223, S224, S225 in `corpus/SOURCES.md` — libalpm `lib/libalpm/{util.c,trans.c,hook.c}`, `doc/alpm-hooks.5.asciidoc` and `meson_options.txt` at pacman commit `54d9411`, the Arch packaging `PKGBUILD` at tag `7.1.0.r9.g54d9411-3` (the installed package; snapshots `.ufo/waves/round-40/frozen/src/`, digests in `SHA256SUMS`), and the own-work host capture `.ufo/waves/round-40/frozen/hostcap/` (MANIFEST sha256 `57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5`)
verified-at: 2026-10-26 (sources fetched 2026-10-26T06:52:42Z; capture 2026-10-26T06:54:46Z)
recheck: `python3 tools/check-exec-environment-r40.py --revision <REV>` re-verifies every EX row against the pinned snapshots and the two host values against the frozen capture; on-release of pacman for S219–S224; 30d for S225

# The environment libalpm gives hook commands and install scriptlets (round 40)

Ground: the update-safety plane (`PROVINCE.md` Core). `corpus/knowledge/pacman-hook-order-r38.md` holds which hooks
run and in what order within a phase (HO1–HO7); `corpus/knowledge/pacman-transaction-order-r39.md` holds where the
phases and scriptlets sit in a transaction and how their output is logged (TO1–TO8). This entry holds what a hook
command or an install scriptlet **finds when it starts**: working directory, standard streams, environment, umask,
interpreter, where the scriptlet file lives, what a `NeedsTargets` hook reads on stdin, what an unsatisfied
`Depends` does, and which paths a `Path` trigger matches. Every rule is read from the source of the installed
build; the host column comes from a frozen read-only capture. Nothing here authorizes a package, hook or
transaction action. It also carries the residual staged propositions round 39 deferred (`NeedsTargets` on stdin,
scriptlet working directory, interpreter, `.pacnew` trigger target; `corpus/lessons/round-39.md` Gate).

## Rules (source-level, pacman 54d9411, Arch build 7.1.0.r9.g54d9411-3)

| id | rule | value | source (file:line and quote) | host |
|---|---|---|---|---|
| EX1 | libalpm changes into the installation root in the parent, chroots the child when that root differs from `/`, and the child then sets its working directory to `/` before execv | `/` | S221 util.c:677-687 “if(strcmp(handle->root, "/") != 0 && chroot(handle->root) != 0) {” (parent `chdir(handle->root)` :628; child `chdir("/")` :683) | A hook or scriptlet that uses relative paths resolves them from `/` on this host (root `/`, so no chroot call happens) |
| EX2 | the child duplicates fd 1 and fd 2 from the same child-to-parent socket so stdout and stderr arrive merged, and fd 0 from a second socket the parent closes at once, so stdin reads end-of-file | `stdout+stderr: one socket; stdin: second socket` | S221 util.c:659-668 “while(dup2(child2parent_pipefd[HEAD], 2) == -1 && errno == EINTR);” (stdin end closed in the parent at :722-726) | The `[ALPM-SCRIPTLET]` lines of TO8 carry both streams of a command interleaved; the log gives a reader one merged stream |
| EX3 | before execv the child sets SHLVL to 1 only when it is unset, unsets BASH_ENV, sets umask 0022 and passes the rest of the environment through | `SHLVL=1 BASH_ENV=unset umask=0022` | S221 util.c:688-698 “/* bash sources $BASH_ENV when run non-interactively */” (`setenv("SHLVL", "1", 0)` :692, `unsetenv("BASH_ENV")` :694, `umask(0022)` :695, `execv` :698) | Files a hook or scriptlet creates get mode bits under umask 0022 whatever the operator's shell umask; variables exported in the shell that ran pacman (and kept by sudo) reach the command |
| EX4 | this Arch build passes -Dscriptlet-shell=/usr/bin/bash so scriptlets run under /usr/bin/bash -c while the upstream meson_options default is /bin/sh | `/usr/bin/bash` | S220 PKGBUILD:113-115 “-Ddoc=enabled \ -Ddoxygen=enabled \ -Dscriptlet-shell=/usr/bin/bash \” (S222 trans.c:357-358 `strcpy(arg0, SCRIPTLET_SHELL)`, `"-c"`; command line :400-406; run :410) | `/usr/lib/libalpm.so.16.0.1` (owned by pacman 7.1.0.r9.g54d9411-3) carries the string `/usr/bin/bash` (strings index 1277) and lacks `/bin/sh` (S225 `libalpm-shell-strings.txt`) |
| EX5 | libalpm requests tmp with mode 01777, makes a unique tmp/alpm_XXXXXX directory under the root, places the scriptlet there as .INSTALL, sources it, then unlinks the file and rmdirs the directory | `tmp/alpm_XXXXXX/.INSTALL` | S222 trans.c:360-377 “/* create a directory in $root/tmp/ for copying/extracting the scriptlet */” (`mkdtemp` :368, error `could not create temp directory` :369, cleanup :412-420) | A root whose `/tmp` cannot hold a new directory fails every scriptlet with `could not create temp directory` (trans.c:369); on this host `/tmp` is a tmpfs |
| EX6 | a NeedsTargets hook reads its stdin sorted by strcmp and de-duplicated by _alpm_strlist_dedup, one newline-terminated target per line with duplicate matches removed | `sorted, deduplicated, one per line` | S223 hook.c:519-526 “/* hooks with multiple triggers could have duplicate matches */” (feed loop `_alpm_hook_feed_targets` :469-490, newline :476); documented in S224 alpm-hooks.5.asciidoc:91-93 | 14 of 69 effective hook files carry `NeedsTargets` (S225 `hooks-needstargets.tsv`; a file in `/etc/pacman.d/hooks` replaces the same-named file in `/usr/share/libalpm/hooks`) |
| EX7 | the running log line is written before _alpm_hook_run_hook checks Depends, a missing satisfier logs could not satisfy dependencies and returns failure, and only a hook with AbortOnFail aborts the PreTransaction phase | `could not satisfy dependencies` | S223 hook.c:507-517 “_("unable to run hook %s: %s\n"), hook->name, _("could not satisfy dependencies"));” (`running` logged :653 before `_alpm_hook_run_hook` :660; abort :660-668); `Depends` documented in S224 alpm-hooks.5.asciidoc:83-85 | A `running` line in `pacman.log` proves the hook was selected, and its command may still have been skipped; the live log holds 0 such errors (`grep -c 'could not satisfy dependencies' /var/log/pacman.log`, 2026-10-26) |
| EX8 | a Path trigger matches the file list names relative to the installation root, alpm_option_match_noextract skips NoExtract paths on the install side, and hook.c ignores NoUpgrade so a .pacnew outcome still matches | `NoExtract` | S223 hook.c:258-279 “/* check if file will be installed */” (`alpm_option_match_noextract` :271; upgrade and removal sides :281-306); target semantics in S224 alpm-hooks.5.asciidoc:61-67 | A hook targeting `etc/<file>` of a NoUpgrade file fires on an upgrade that leaves `<file>.pacnew`, so its command must expect the old file in place |

## What a hook or scriptlet author can rely on (derived from EX1–EX8)

1. Start directory `/`, umask 0022, `BASH_ENV` gone, `SHLVL` 1 unless inherited (EX1, EX3).
2. One merged output stream, logged line by line under `[ALPM-SCRIPTLET]` (EX2, TO8).
3. Stdin: the sorted, de-duplicated target list for a `NeedsTargets` hook; end-of-file for everything else (EX2, EX6).
4. Scriptlets: bash on Arch, sourced from a private directory under `<root>/tmp` that is removed afterwards (EX4, EX5).
5. A `running` line is selection, not execution (EX7); a `.pacnew` outcome still triggers the original path (EX8).

## Boundaries

- Source-level for pacman 54d9411 as patched by the Arch package; the two packaging patches that touch libalpm
  (`0001-libalpm-invalidate-curl-data-in-child.patch`, `0002-libalpm-use-curl-s-effective-url-…`, PKGBUILD:54-55)
  are named for review and their file scope is a wave item, not assumed here.
- EX1–EX3 and EX5 have no host instance in the capture: observing them needs a running transaction, and pacman
  transactions are paused on this host.
- The environment that reaches pacman itself (sudo's `env_reset`, a systemd unit) is outside this entry.
