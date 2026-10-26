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
| EX1 | Every command libalpm runs through `_alpm_run_chroot` (hook `Exec` commands, install scriptlets and `ldconfig`) starts in working directory `/`: the parent first changes into the installation root, the child calls chroot only when that root differs from `/`, and the child then changes its directory to `/` | `/` | S221 util.c:677-687 “if(strcmp(handle->root, "/") != 0 && chroot(handle->root) != 0) {” (parent `chdir(handle->root)` :628; child `chdir("/")` :683) | A hook or scriptlet that uses relative paths resolves them from `/` on this host (root `/`, so no chroot call happens) |
| EX2 | The child's stdout and stderr are both duplicated onto one socket that the parent reads, so the two streams arrive merged; its stdin is a second socket, which the parent closes at once when the caller passes a null input callback, so such a child reads end-of-file on stdin | `stdout+stderr: one socket; stdin: second socket` | S221 util.c:659-668 “while(dup2(child2parent_pipefd[HEAD], 2) == -1 && errno == EINTR);” (stdin end closed in the parent at :722-726) | The `[ALPM-SCRIPTLET]` lines of TO8 carry both streams of a command interleaved; the log gives a reader one merged stream |
| EX3 | Before `execv` the child sets `SHLVL` to 1 when the variable is unset (an inherited value is kept), removes `BASH_ENV` from its environment, sets umask 0022 and resets signal handlers; every other variable of the calling pacman process passes through to the command unchanged | `SHLVL=1 BASH_ENV=unset umask=0022` | S221 util.c:688-698 “/* bash sources $BASH_ENV when run non-interactively */” (`setenv("SHLVL", "1", 0)` :692, `unsetenv("BASH_ENV")` :694, `umask(0022)` :695, `execv` :698) | Files a hook or scriptlet creates get mode bits under umask 0022 whatever the operator's shell umask; variables exported in the shell that ran pacman (and kept by sudo) reach the command |
| EX4 | Arch builds pacman with `-Dscriptlet-shell=/usr/bin/bash`, so every install scriptlet runs as `/usr/bin/bash -c '. <scriptlet>; <function> <new version> [<old version>]'` through `_alpm_run_chroot`; the upstream build default is `/bin/sh` (S219 meson_options.txt:17), so bash-only syntax in a scriptlet depends on this packaging choice | `/usr/bin/bash` | S220 PKGBUILD:113-115 “-Ddoc=enabled \ -Ddoxygen=enabled \ -Dscriptlet-shell=/usr/bin/bash \” (S222 trans.c:357-358 `strcpy(arg0, SCRIPTLET_SHELL)`, `"-c"`; command line :400-406; run :410) | `/usr/lib/libalpm.so.16.0.1` (owned by pacman 7.1.0.r9.g54d9411-3) carries the string `/usr/bin/bash` (strings index 1277) and lacks `/bin/sh` (S225 `libalpm-shell-strings.txt`) |
| EX5 | Before a scriptlet runs, libalpm requests `<root>/tmp` with mode 01777 when that directory is missing, makes a private directory `tmp/alpm_XXXXXX` under the root, copies (from the local database) or extracts (from a package file) the scriptlet into it as `.INSTALL`, sources it from there, and afterwards removes the file and the directory, logging a warning when either removal fails | `tmp/alpm_XXXXXX/.INSTALL` | S222 trans.c:360-377 “/* create a directory in $root/tmp/ for copying/extracting the scriptlet */” (`mkdtemp` :368, error `could not create temp directory` :369, cleanup :412-420) | A root whose `/tmp` cannot hold a new directory fails every scriptlet with `could not create temp directory` (trans.c:369); on this host `/tmp` is a tmpfs |
| EX6 | A hook marked `NeedsTargets` receives its matched trigger targets on stdin, sorted with `strcmp`, with duplicate matches from several triggers removed, one target per line; a hook lacking `NeedsTargets` gets the closed stdin of EX2 | `sorted, deduplicated, one per line` | S223 hook.c:519-526 “/* hooks with multiple triggers could have duplicate matches */” (feed loop `_alpm_hook_feed_targets` :469-490, newline :476); documented in S224 alpm-hooks.5.asciidoc:91-93 | 14 of 69 effective hook files carry `NeedsTargets` (S225 `hooks-needstargets.tsv`; a file in `/etc/pacman.d/hooks` replaces the same-named file in `/usr/share/libalpm/hooks`) |
| EX7 | The `running '<name>'...` log line is written before the hook's `Depends` are checked; when an installed package satisfying a listed `Depends` is missing, libalpm logs `unable to run hook <name>: … satisfy dependencies` and skips the command, and that failure stops the PreTransaction phase, and with it the transaction, only for a hook carrying `AbortOnFail` | `could not satisfy dependencies` | S223 hook.c:507-517 “_("unable to run hook %s: %s\n"), hook->name, _("could not satisfy dependencies"));” (`running` logged :653 before `_alpm_hook_run_hook` :660; abort :660-668); `Depends` documented in S224 alpm-hooks.5.asciidoc:83-85 | A `running` line in `pacman.log` proves the hook was selected, and its command may still have been skipped; the live log holds 0 such errors (`grep -c 'could not satisfy dependencies' /var/log/pacman.log`, 2026-10-26) |
| EX8 | A `Path` trigger matches file paths as the package's file list names them, relative to the installation root; on the install side a path that NoExtract excludes is skipped, and matching ignores NoUpgrade, so a protected file that pacman writes as `.pacnew` still matches under its listed name | `NoExtract` | S223 hook.c:258-279 “/* check if file will be installed */” (`alpm_option_match_noextract` :271; upgrade and removal sides :281-306); target semantics in S224 alpm-hooks.5.asciidoc:61-67 | A hook targeting `etc/<file>` of a NoUpgrade file fires on an upgrade that leaves `<file>.pacnew`, so its command must expect the old file in place |

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

## Wave-1 corrections (appended 2026-10-26; the rule, value and source cells above stay as written)

Integrated by the L1 from the round-40 wave (`.ufo/waves/round-40/w1/`); every line re-read against the pinned
snapshots `.ufo/waves/round-40/frozen/src/`. Extra sources cited only here: S208 (hook.c validation), S209
(alpm-hooks.5 `AbortOnFail`), S217 (trans.c Post phase) and S226 (alpm-hooks.5 CAVEATS), rows in `corpus/SOURCES.md`.

- **EX4 — arguments and scope** (seat C2CritEX4). `<new version> [<old version>]` is the install/upgrade form only:
  the call passes libalpm's `ver` then `oldver` (trans.c:400-406), so `pre_install`/`post_install` get the new
  version, `pre_upgrade`/`post_upgrade` new then old (TO4), and `pre_remove`/`post_remove` the removed package's
  version (TO7). The interpreter applies to every scriptlet that runs; `pacman --noscriptlet` skips the run, and a
  scriptlet file lacking the phase function returns before staging or after extraction (trans.c:351, :392). The
  interpreter path is resolved inside the installation root after the optional chroot (util.c:677-687), so a
  `--root` target lacking `/usr/bin/bash` fails the scriptlet with `call to execv failed` (util.c:698-700). The
  `.INSTALL` file is sourced with `.`, so a shebang inside it is inert. Scope of the consequence sentence: on this
  host `/bin/sh` is a symlink to bash (seat measurement, `C2ScribeSkill.md`), so bash syntax would also run under
  the upstream default here; "bash-only syntax depends on this packaging choice" holds for a root whose `/bin/sh`
  is another shell [inference].
- **EX5 — host cell sentence 2 withdrawn as false** (seat C2RevEX5). "on this host `/tmp` is a tmpfs" is wrong:
  `/tmp` is an xfs filesystem on `/dev/nvme1n1p1` (`findmnt /tmp`, `stat -f -c %T /tmp` → `xfs`, observed
  2026-10-26T07:18:06Z, receipt `.ufo/waves/round-40/w1/C2RevEX5/host-tmp-fstype.txt`), and the frozen capture S225
  never recorded a `/tmp` fstype, so the sentence had no anchor (QUALITY 2). Sentence 1 stands. Two rule-cell glosses
  are qualified (QUALITY 66): "private" is `mkdtemp(3)` semantics (mode 0700), which trans.c does not state; "copies
  (from the local database)" is the non-archive branch (trans.c:382-386) — which file the caller passes is TO3/TO7's
  call-site fact, not trans.c's.
- **EX7 — the lookup time and the PostTransaction case** (seat C2CritEX7). `Depends` is looked up in the local
  package cache when the phase runs (hook.c:509); for a PreTransaction hook that is before `transaction started`
  (TO1, trans.c:201-208), so a Pre hook whose `Depends` names a package the same transaction installs skips its
  command during that transaction. A PostTransaction hook carrying `AbortOnFail` loads with the warning
  `AbortOnFail set for PostTransaction hook` (S208 hook.c:141-144), runs, and its failure return is dropped: the Post
  call `_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION)` ignores the result and `alpm_trans_commit` returns 0
  (S217 trans.c:237-244). The manual says the same: “Only applies to PreTransaction hooks” (S209
  alpm-hooks.5.asciidoc:87-89).
- **EX8 — which operation matches** (seat C2CritEX8). After collecting matches, `_alpm_hook_trigger_match_file`
  moves every path present in both the old and the new package's file list from `install` to `upgrade`
  (hook.c:310-337, `upgrade = alpm_list_add(upgrade, path)` :321, `install = alpm_list_remove_item(install, i)` :324;
  operation test :339-341). So an upgraded protected file that leaves `.pacnew` is an `Upgrade` match, and an
  `Operation = Install` trigger fires for it only when the old package lacks that path. The `.pacnew` rule is
  documented upstream: “When installing or upgrading a file that is extracted with a '.pacnew' extension, the
  original file name is used in triggering the hook.” (S226 alpm-hooks.5.asciidoc:125-127). On this host
  `pacman-conf NoUpgrade` prints nothing (seat C2ScribeSkill, 2026-10-26), so the NoUpgrade case is source-level
  here.
- **Observation and inference** (QUALITY 3; seat CritTrend). Host cells that are observations: EX4 (strings of the
  installed libalpm), EX6 (14 of 69 from S225), EX7's "0 such errors" (live `pacman.log` count). Host cells that are
  source-derived inference with no host instance: EX1, EX2, EX3, EX5 sentence 1, EX7's first sentence, EX8.

## QUALITY check (appended 2026-10-26; QUALITY 14)

| Criterion | Result | Pointer |
|---|---|---|
| 1 falsifiable | each rule names its file and lines; the counter re-checks the quote and the derived value | `tools/check-exec-environment-r40.py`, `.ufo/waves/round-40/after/c2-after-bf23805.jsonl` |
| 2 measured anchor | failed once, repaired: the EX5 `/tmp` sentence had no anchor and is withdrawn above | `C2RevEX5.md` |
| 3 observation vs inference | labelled in the corrections above | this section |
| 4 errata append-only | the corrections section; the rows are unchanged | `git diff` of this file shows additions only |
| 7 exact S-row, tier, anchor | S219–S226 tier A; scopes distinct from S208, S209, S216, S217 | `corpus/SOURCES.md`; `C2RevSourcesRows.md` |
| 8 provenance trio | `source:`, `verified-at:`, `recheck:` at the top | lines 1-3 |
| 9 negative claims carry a sweep | "matching ignores NoUpgrade": `grep -ci noupgrade` over the pinned hook.c → 0 | counter `derive_values`; `C2CritEX8.md` Q3 |
| 66 every branch kept | three omitted branches found by the wave (EX4 removal arguments, EX7 Post `AbortOnFail`, EX8 operation split) appended above | seats C2CritEX4, C2CritEX7, C2CritEX8 |
| 68 novelty swept | 0 base hits for the eight novelty tokens; EX2's merged streams and EX7's `AbortOnFail` half were already held at base (TO8, HO rows), so they are deeper restatement, not new ground | receipt `before/c2-before.jsonl`; `C2ScoutNovelty.md` |
| 86 upstream row per rule | every EX row cites a code or docs row; S225 carries host values only | counter `upstream` conjunct |
| 87 content read | the counter reads value, tokens and polarity, but a token-list writer and affirmatively false rules still pass it (`C2CritControl.md`, `C2CritXFalse.md`), so content rests on the per-row verdicts: EX1, EX2, EX3, EX6 hold; EX4, EX5, EX7, EX8 partly, corrected above | `C2RevEX1.md`–`C2RevEX8.md` |

## Wave-1 corrections — packaging patch (appended 2026-10-26)

- **Line numbers are upstream 54d9411, not the installed build** (seat C2RevenPatches). Of the four patches the Arch
  package applies (PKGBUILD:51-55), `0001-libalpm-invalidate-curl-data-in-child.patch` inserts 5 lines into
  `_alpm_run_chroot` after util.c:675, so in the installed source every cited util.c line after :675 (EX1 :677-687,
  EX2 :722-726, EX3 :688-698) sits 5 lines later; the inserted lines change no EX value, and no patch touches trans.c,
  hook.c or meson_options.txt (`.ufo/waves/round-40/w1/C2RevenPatches.md` §1-§3). The Boundaries bullet "their file
  scope is a wave item, not assumed here" is answered by that report.
