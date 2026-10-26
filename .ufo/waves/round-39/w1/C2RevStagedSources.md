VERDICT: supports

# C2-19 (assimilation) — staged `pacman-hook-timing-r25.md` sentences vs re-opened sources

Item: re-open the staged entry's cited sources today (2026-10-26) and check six staged sentences against
them and against libalpm at 54d9411. Staged file (read-only, not modified):
`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/pacman-hook-timing-r25.md`
(sentences under "What is now sourced", sections "Failure semantics" and "The scriptlet contract").

## Sources re-opened (all fetched 2026-10-26 by this seat, curl -fsS)

| source | receipt (sha256, prefix) | today's rendering |
|---|---|---|
| https://man.archlinux.org/man/alpm-hooks.5 | `74830815…` `.ufo/waves/round-39/w1/C2RevStagedSources/alpm-hooks.5.html` | Pacman 7.1.0, man date 2026-10-15 |
| https://devblog.archlinux.page/2026/on-scripts-and-hooks/ | `ea3085d7…` `…/on-scripts-and-hooks.html` | `datetime="2026-08-09T11:00:00+00:00"` |
| https://man.archlinux.org/man/alpm-install-scriptlet.5 | `a18a5c60…` `…/alpm-install-scriptlet.5.html` | extra/alpm-docs 0.13.0-1 |

`.txt` siblings are text extractions of the same HTML; quoted line numbers below refer to the `.txt` files.

Drift check vs staged metadata: entry says "Pacman 7.1.0, man date 2026-10-15" for S201 and devblog
2026-08-09 for S202 — both unchanged today. Bonus: today's man page footer shows package
`7.1.0.r9.g54d9411-3` (alpm-hooks.5.txt, Package information block), i.e. the same pacman revision the
frozen snapshot pins (`frozen/src/FETCH.txt:3` "installed: pacman 7.1.0.r9.g54d9411-3", base URL
`…/54d9411/lib/libalpm/<file>` at line 2). Man page and frozen source are the same code revision; no
version skew to worry about. Frozen sources verified against `frozen/src/SHA256SUMS` — all six match
(`sha256sum -c` result: add.c `fd313629…`, hook.c `99f1044b…`, remove.c `a052d455…`, sync.c `6b297364…`,
trans.c `637c1165…`, util.c `381618b6…`, as listed in the file).

## S1 — "On upgrade, the old package version's pre-transaction hooks run first, then the new version's install-scriptlet functions, then the new version's post-transaction hooks." → HOLDS

- libalpm order: `trans.c:201-204` runs `_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION)` before the
  `"transaction started"` logaction at `trans.c:208` and before any commit; `sync.c:1340-1356`
  (`_alpm_sync_commit`) removes replaced/conflicting packages first, then `_alpm_upgrade_packages`,
  where `add.c:467-473` runs the pre scriptlet and `add.c:638-645` the post scriptlet of each package;
  Post hooks run only on the success path, `trans.c:230-239` (after `"transaction completed"`,
  `trans.c:235`). So Pre hooks → scriptlets (interleaved with file ops per package) → Post hooks.
- "Old"/"new" attribution: hook dirs are re-read per phase (`hook.c:532-565`, `readdir` at 565; invoked
  once per phase at `trans.c:201-204` and `trans.c:237-238`), so at Pre time only the old package set's
  `.hook` files exist, and by Post time the new package's files (including its hooks) are installed.
  The pre_upgrade function comes from the new package archive (`add.c:472`, `pkgfile`),
  post_upgrade from the new package's stored script (`add.c:641`, `_alpm_local_db_pkgpath(db, newpkg,
  "install")`).
- Devblog (accessed 2026-10-26), "Transaction example", observed upgrade log of test 0.1.0-1 → 0.1.0-2:
  `on-scripts-and-hooks.txt:392` "(1/1) Running the pre-transaction hook for test package 0.1.0-1...",
  `:395-398` "upgrading test... / Running the pre_upgrade function for test package 0.1.0-2 ...",
  `:400` "(2/2) Running the post-transaction hook for test package 0.1.0-2...", and the summary
  `:403`: "First, the pre-transaction tasks of the alpm-hooks(5) in the test package version 0.1.0-1,
  then the pre- and post-upgrade functions of the alpm-install-scriptlet(5) in the test package
  version 0.1.0-2 and finally the post-transaction tasks of the alpm-hooks(5) in test package version
  0.1.0-2 are run." — same order, same old/new attribution as the staged sentence.
- Nuance (does not weaken the claim): hooks are not version-bound objects; "the old version's
  pre-transaction hooks" is attribution shorthand for "the hook files present at Pre time, which are
  those shipped by the currently (old) installed set". The staged entry uses it exactly for that
  attribution purpose.

## S2 — "A hook exists only while its providing package is installed." → HOLDS

- Devblog (accessed 2026-10-26), "🪝 Hooks": `on-scripts-and-hooks.txt:79` "As hooks are read from the
  target system's filesystem, pre-transaction tasks are only available and run once the package is
  installed, that provides them." and `:81` "A post-transaction task is only available and run as long
  as the package is installed, that provides it." The staged sentence is a faithful compression of
  these two sentences.
- Code agrees: hooks are read from disk at run time, per phase (`hook.c:532-565`), from
  `/usr/share/libalpm/hooks` and configured hook dirs (alpm-hooks.5.txt:29-33); the system dir's files
  are package-owned, so uninstalling the package removes the hook. Devblog removal log
  (`:431-441`): after `removing test...`, the post-transaction hook list contains only "Arming
  ConditionNeedsUpdate" — the removed package's own post hook is gone.
- Boundary (stated in the staged entry's own sources, not contradicting it): administrator hooks in
  `/etc/pacman.d/hooks/` and overrides ("Hooks may be disabled by overriding them with a symlink to
  /dev/null", alpm-hooks.5.txt:106-109) are not package-tied; the staged sentence is scoped to hooks
  that have "a providing package", which is exactly the devblog's scope.

## S3 — "NeedsTargets passes the matched trigger targets to the hook on stdin." → HOLDS

- alpm-hooks.5.txt:101-102 (ACTIONS, accessed 2026-10-26): "the list of matched trigger targets to be
  passed to the running hook on stdin."
- Code: `hook.c:519-526` — if `hook->needs_targets`, `_alpm_run_chroot(handle, hook->cmd[0], hook->cmd,
  (_alpm_cb_io) _alpm_hook_feed_targets, &ctx)`; `_alpm_hook_feed_targets` (`hook.c:469-477`) writes
  the sorted, deduped matches; `util.c:667` `dup2(parent2child_pipefd[TAIL], 0)` makes that pipe the
  child's fd 0, i.e. stdin. `needs_targets` parsed at `hook.c:232-233`.

## S4 — "A file extracted with the .pacnew extension triggers the hook on the original file name." → HOLDS

- alpm-hooks.5.txt:128-130 (CAVEATS, accessed 2026-10-26): "a .pacnew extension, the original file name
  is used in triggering the hook."
- Code, `add.c` (extract_single_file path): notouch branch — event initialized `.file = filename`
  (`add.c:344`), then `add.c:346-347` `"remove" the .pacnew suffix` /
  `filename[filename_len] = '\0';` BEFORE `EVENT(handle, &event)` at `add.c:348`. The initializer
  copies the pointer, not the string, so the dispatched event carries the original (suffix-stripped)
  name; the logaction at `add.c:349-350` prints `"%s installed as %s.pacnew"` with the truncated name.
  needbackup branch dispatches `.file = origfile` (`add.c:397`), built suffix-free at `add.c:355`
  (`strncat(origfile, filename, filename_len)`). Both branches therefore trigger on the original name.

## S5 — ".INSTALL functions execute in the system root (/), so every path inside them must be absolute." → HOLDS

- alpm-install-scriptlet.5.txt:17-19 (DESCRIPTION, accessed 2026-10-26): "The shell functions are
  executed in the root (/) of the system, so all paths inside of it must be absolute."
- Code: `trans.c:397-398` — "chop off the root so we can find the tmpdir in the chroot",
  `scriptpath = scriptfn + strlen(handle->root) - 1` → absolute script path in the target root;
  command line `. scriptfn; fn ver [oldver]` at `trans.c:401-405`; child process does
  `chroot(handle->root)` unless root is already `/` (`util.c:677-682`, "don't chroot() to '/'") and
  then `chdir("/")` (`util.c:683-686`). Scriptlets therefore run at `/` of the target root.

## S6 — "the shell interpreter is chosen globally by the distribution and cannot be selected per package." → HOLDS

- alpm-install-scriptlet.5.txt:36-41 (accessed 2026-10-26): "the shell interpreter used by package
  management software to run the script is defined globally (e.g. per distribution)… the shell
  interpreter cannot be changed on a per-package basis." Also `:37` "No shebang is used in the script".
- Devblog `on-scripts-and-hooks.txt:46`: "the shell in use is tied to the build-time configuration of
  the package manager (Bash for Arch Linux)."
- Code: the interpreter is the compile-time constant `SCRIPTLET_SHELL` — `trans.c:357`
  (`strcpy(arg0, SCRIPTLET_SHELL)`) and `trans.c:410`
  (`_alpm_run_chroot(handle, SCRIPTLET_SHELL, argv, NULL, NULL)`), invoked as `SCRIPTLET_SHELL -c`
  (`trans.c:357-358`, matching the man page's "-c command line option" wording). No per-package input
  reaches the choice. Gap, noted honestly: the `#define` itself lives in a header not captured in
  `frozen/src/` (grep over all six frozen files shows only the two usages), so its literal value
  (`/bin/sh`) is not verifiable from the snapshot — but the judged sentence does not claim a value.

## Adjacent confirmations (same staged paragraphs, checked in passing)

- "Ordering is alphabetical … ignores the suffix": alpm-hooks.5.txt:36-38; maintainers' "missing a
  documented ordering system" quote in the staged entry matches `on-scripts-and-hooks.txt:446-448`.
- "AbortOnFail … PreTransaction only": alpm-hooks.5.txt:96-97 "Only applies to PreTransaction hooks."
- "PostTransaction hooks do not run if the transaction fails": alpm-hooks.5.txt:134-135; code
  `trans.c:230-239` (post hooks skipped on the `STATE_INTERRUPTED` / failure path).
- "pre_upgrade and post_upgrade take the new version first": `add.c:472-473` and `add.c:644-645` both
  pass `newpkg->version, oldpkg->version`; man page Functions list (alpm-install-scriptlet.5.txt:66,
  :79 "New package version" first); devblog example log `:396-398` prints "(new (0.1.0-2) and old
  (0.1.0-1) package version)".

## Per-sentence verdict lines

- S1 (old Pre → scriptlets → new Post): holds — on-scripts-and-hooks.txt:403; trans.c:201-208,230-239; sync.c:1340-1356
- S2 (hook exists only while providing package installed): holds — on-scripts-and-hooks.txt:79-81; hook.c:532-565
- S3 (NeedsTargets on stdin): holds — alpm-hooks.5.txt:101-102; hook.c:519-526; util.c:667
- S4 (.pacnew triggers on original name): holds — alpm-hooks.5.txt:128-130; add.c:344-348,397
- S5 (scriptlets run in /, absolute paths): holds — alpm-install-scriptlet.5.txt:17-19; util.c:677-686; trans.c:397-398
- S6 (interpreter chosen globally): holds — alpm-install-scriptlet.5.txt:36-41; trans.c:357,410; on-scripts-and-hooks.txt:46

Kill-rule note: this report judges staged sentences of the r25 merge entry, not any TO1-TO8 row of
`corpus/knowledge/pacman-transaction-order-r39.md`; no TO row was judged FALSE, the C2 kill rule is not
triggered by this seat.

## Residual risk / what I did not do

- Did not execute pacman or libalpm; verdicts rest on the frozen source text, today's man pages, and
  the devblog's own observed transaction logs (which are themselves execution evidence, but by the
  blog authors, not by me).
- `SCRIPTLET_SHELL`'s value unverifiable from `frozen/src/` (header not captured) — see S6 gap.
- S212 (archlinuxcn wiki) was outside my assigned three sources and was not re-opened.
- Entry's Chinese-rendering section (five-step order, tier B) not assessed — out of item scope.

Tooling: nothing installed or upgraded for this item (curl/text-extraction only); scratch dir
`/fast/scratch/hyaku/tsukuroi-r39/C2RevStagedSources` was created per rules, stayed empty, and is
removed at finish. No lane file other than this report and the receipts dir was written.
