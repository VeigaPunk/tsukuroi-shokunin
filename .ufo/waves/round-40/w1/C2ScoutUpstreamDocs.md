VERDICT: no-finding

Item C2-18 (scout, upstream docs vs EX1-EX8). No official document I could open contradicts EX1-EX8. None says Arch scriptlets run under `/bin/sh`, none gives a cwd other than `/`, and none gives another NeedsTargets format. Three precision defects in the entry's own citation text and one pin-drift note are listed in section 4. Every page below was fetched and read 2026-10-26 (first fetch 07:15:10Z). Scratch (clones, html copies) was under `/fast/scratch/hyaku/tsukuroi-r40/C2ScoutUpstreamDocs/` and is removed on exit. No lane file was touched. No tool was installed.

## 1. What I opened (access 2026-10-26)

| page | how | result |
|---|---|---|
| https://man.archlinux.org/man/PKGBUILD.5 | curl, HTML to text | read section INSTALL/UPGRADE/REMOVE SCRIPTING in full |
| https://man.archlinux.org/man/alpm-hooks.5 | curl | read in full; footer "Pacman 7.1.0" |
| https://man.archlinux.org/man/pacman.8 | curl | grep + read of `--noscriptlet`, `--root`, `--sysroot`, stdin |
| https://man.archlinux.org/man/pacman.conf.5 | curl | read NoUpgrade, NoExtract, RootDir |
| https://man.archlinux.org/man/libalpm.3, makepkg.8 | curl | grep: no scriptlet/cwd/shell statement |
| https://wiki.archlinux.org/title/Pacman | curl | read Hooks, transaction-workflow, NoUpgrade sections |
| https://wiki.archlinux.org/title/PKGBUILD | curl | read `install` section |
| https://wiki.archlinux.org/title/Creating_packages, /Pacman/Pacnew_and_Pacsave, /Pacman/Tips_and_tricks | curl | grep: no cwd/shell/stdin claim about scriptlets |
| https://bbs.archlinux.org/viewtopic.php?pid=913891 | `read` tool | developer reply on chroot+chdir (the thread the wiki cites) |
| pacman `master` (a6f7467d, 2026-01-25) | `git clone https://gitlab.archlinux.org/pacman/pacman.git`; read `NEWS`, `HACKING`, `proto/proto.install`, `doc/*.asciidoc`, `lib/libalpm/*` | see section 3 |
| Arch packaging `main` (8027406, 2026-10-24) | `git clone https://gitlab.archlinux.org/archlinux/packaging/packages/pacman.git` | see section 3 |
| https://gitlab.archlinux.org/pacman/pacman/-/raw/master/{doc/alpm-hooks.5.asciidoc,NEWS} | `read` tool | matches the clone |

Not opened: https://www.reddit.com/r/archlinux/comments/1lrdeap/ (blocked: "You've been blocked by network security"). It is a forum thread, not an official document. A `web_search` answer claiming scriptlets start at `/` was a synthesized summary, so I give it no weight. I could not curl raw gitlab URLs (Anubis challenge page), so I read the cloned repos instead.

Page hashes (sha256 of the fetched HTML, for repeatability): PKGBUILD.5 af56d68912cf8e83dffc72ec5c5ccf164e2af91606242ebaacc68ff6dd7c8529; alpm-hooks.5 748308154e750f64f951b25f108f157f47581d13e7a5583c1a4c395b0394aea5; pacman.8 531ebf4868faf7674a24ba0d9e4bb8af9ab99511ba86a5df87645ce0403fd495; wiki Pacman 38676c7f7dea5b068a0898db0f424a7f302c73b2ecb6bb71c5dbcca2c5e48eb1; wiki PKGBUILD 11a56701421ce6e55b33fc7924f26ac23237ba45b583fe2556da8f220bc7e274. The pages change, so a re-fetch may differ.

## 2. Statements by row, with located quotes (each from a page opened above)

**EX1, cwd `/`. Supported by a pacman developer, not contradicted.**
- Developer toofishes, https://bbs.archlinux.org/viewtopic.php?pid=913891 (2011-04-06): "We chroot() and then chdir() to the root directory in every install script executed- so it is no assumption at all." This is the only document that states the cwd. It was written for the code of 2011 (unconditional chroot).
- ArchWiki PKGBUILD, `install` section: "Each function is run chrooted inside the pacman install directory." This says "chrooted", not cwd. It is looser than EX1 (the current code skips `chroot()` when root is `/`, util.c:677), but the cwd is the same. Not a contradiction.
- libalpm `alpm.h:1661` at master: "Hooks and scriptlets will also be run in a chroot to ensure they behave correctly in alternative roots."
- No page in section 1 states a cwd other than `/`. PKGBUILD.5, alpm-hooks.5 and pacman.8 say nothing about cwd.

**EX2, merged output, closed stdin. Supported by NEWS and the wiki.**
- pacman NEWS 5.0.0: "prevent install scriptlets using stdin for user interaction".
- NEWS 5.0.1: "fix handling of stdin scripts called by pacman" (the line is ambiguous: it could mean scripts fed on stdin or scripts reading stdin).
- ArchWiki Pacman, Hooks: "pacman hooks are not interactive."
- No doc says stdout and stderr stay separate. No doc describes the socket.

**EX3, SHLVL / BASH_ENV / umask 0022. Supported by NEWS, no doc contradicts.**
- NEWS 2.8: "FS#1003: set umask before scriptlet calls" (umask).
- NEWS 5.1.2: "Reset known signal handlers before running install scripts or hooks (FS#56756)" (the entry's "resets signal handlers").
- No doc mentions SHLVL or BASH_ENV.

**EX4, scriptlet shell. No doc says Arch scriptlets run under `/bin/sh`.**
- PKGBUILD(5) INSTALL/UPGRADE/REMOVE SCRIPTING names no interpreter. It gives only function names and arguments ("Scripts are passed either one or two "full version strings"").
- The wiki `install` section and `proto/proto.install` at master name no interpreter. proto.install has no shebang; its text is "# This is a default template for a post-install scriptlet."
- The only `/bin/sh` default is the build option `meson_options.txt:17` (S219): `option('scriptlet-shell', type : 'string', value : '/bin/sh', ...)`. The entry already cites it.
- Arch packaging `main` (8027406, pkgrel 4) still has `PKGBUILD:115: -Dscriptlet-shell=/usr/bin/bash \`.
- NEWS 4.1.0: "configure shell for running install scriptlets (FS#20557)", the origin of the option.
- NEWS 7.0.0: "Prevent buffer overflow with long scriptlet shell path". It touches the `strcpy(arg0, SCRIPTLET_SHELL)` the entry cites (trans.c:357), so the pin carries that fix.
- Tips and tricks has `Exec = /bin/sh -c '/usr/bin/pacman -Qqe > /etc/pkglist.txt'` (line 413) and `/usr/bin/bash -c "..."` (line 298). Those are hook `Exec` lines that name a shell explicitly. They say nothing about scriptlets, and they agree with hooks being `execv`'d with no shell (hook.c:507-526).

**EX5, `.INSTALL` in `<root>/tmp/alpm_XXXXXX`.** Only the name `.INSTALL` is in docs: wiki Creating_packages: ".INSTALL — an optional file used to execute commands after the install/upgrade/remove stage (this file is present only if specified in the PKGBUILD)." NEWS 2.7.x: "Renamed the install scriptlet from ._install to .INSTALL". No doc on the staging directory, so nothing contradicts it.

**EX6, NeedsTargets stdin format. No doc gives another format.**
- alpm-hooks.5 at 7.1.0 and at master: "Causes the list of matched trigger targets to be passed to the running hook on 'stdin'." This is the whole documentation. It gives no ordering, de-duplication or separator.
- Upstream commit 5312e683 (2015-11-28, "hooks: pass matched targets to hooks") has no message body. The code is the only source for "sorted, deduplicated, one per line" (hook.c:519-526).
- NEWS 5.1.0 "parse stdin as newline-separated instead of whitespace-separated (FS#52992)" is about `pacman -` targets on the command line, not the hook feed. Do not conflate them.

**EX7, `Depends`, `running` line, `AbortOnFail`. No contradiction.**
- alpm-hooks.5: "Packages that must be installed for the hook to run." and "Causes the transaction to be aborted if the hook exits non-zero. Only applies to PreTransaction hooks."
- The docs say nothing about the order of the `running` log line and the Depends check. The claim "an unmet Depends aborts a PreTransaction AbortOnFail hook" is code-derived (hook.c:507-517 returns -1, hook.c:660 sets ret). The doc wording "exits non-zero" does not cover it. This is a refinement, not a contradiction.

**EX8, Path triggers, NoExtract, `.pacnew`. Supported directly by the docs.**
- alpm-hooks.5 CAVEATS: "When installing or upgrading a file that is extracted with a '.pacnew' extension, the original file name is used in triggering the hook."
- alpm-hooks.5 Target: "Paths refer to the files in the package archive; the installation root should *not* be included in the path."
- pacman.conf(5) NoExtract: "All files listed with a NoExtract directive will never be extracted from a package into the filesystem."
- pacman.conf(5) NoUpgrade: "the new files will be installed with a .pacnew extension."
- ArchWiki Pacman (NoUpgrade section): "All files listed with a NoUpgrade directive will never be touched during a package install/upgrade, and the new files will be installed with a .pacnew extension."

## 3. Pin drift: pacman 54d9411 vs current master

`git diff 54d9411 HEAD` (HEAD a6f7467d, 2026-01-25) over `lib/libalpm/{hook,util,trans}.c doc/alpm-hooks.5.asciidoc meson_options.txt doc/PKGBUILD.5.asciidoc doc/pacman.8.asciidoc doc/pacman.conf.5.asciidoc HACKING`:
- `util.c` sha256 `381618b6…bdd2` at 54d9411 and at master (identical). `trans.c` and `meson_options.txt` show no diff.
- `hook.c` differs by 4 lines, from commit b5b79efe "Remove deprecated File target for hook types". It removes the `File` branch in `_alpm_hook_parse_cb`. It does not touch EX6-EX8.
- `alpm-hooks.5.asciidoc` loses the sentence "'File' is a deprecated alias for 'Path' and will be removed in a future release." (the snapshot S224 line 58 still has it).
- `PKGBUILD.5.asciidoc` gains an `sccache` option (unrelated).
- Arch packaging: tag `7.1.0.r9.g54d9411-3` to `main` (-4, "Rebuild for OpenSSL 4.1", 2026-10-24) changes only `pkgrel` (3 to 4) and `.SRCINFO`. The entry's "installed package" is therefore one rebuild behind packaging `main`, with the same source and flags.
- The HACKING file has no scriptlet or hook statement (grep returned none).

So EX1-EX5 and EX7-EX8 describe code that is unchanged between the pin and master. The one drift (`File` type removed) is outside the eight rows.

## 4. Citation-precision defects in the entry (not contradictions)

1. EX6's source cell says "documented in S224 alpm-hooks.5.asciidoc:91-93". Those lines (S224 snapshot lines 91-93) document only that targets are passed on stdin. Sorted order, de-duplication and one-per-line come from hook.c:519-526 and :469-490 alone. Suggest wording: "stdin delivery documented in S224:91-93; the order and format are code-only."
2. EX8's source cell does not cite the doc line that states the `.pacnew` rule directly: S224 alpm-hooks.5.asciidoc:126-127, "When installing or upgrading a file that is extracted with a '.pacnew' extension, the original file name is used in triggering the hook." Suggest adding it.
3. EX1 could add the two documents that attest the cwd: the BBS reply above (developer statement, 2011) and the wiki "chrooted" line. The BBS reply predates the conditional chroot at util.c:677, so cite it as history only.

## 5. What I did not do

- I did not open the BBS thread's linked git permalink (projects.archlinux.org, long dead).
- I did not read the Arch wiki talk pages or the pacman-dev mailing list archive.
- I did not run the counter `tools/check-exec-environment-r40.py` and did not test any quote against it. I did not run pacman, hooks or scriptlets.
- I did not verify the code claims in util.c/trans.c/hook.c beyond the spot checks in section 2 (hook.c:507-526, 640-668; util.c chdir/chroot/dup2/setenv lines; trans.c:357, 410). Those spot checks agree with the entry.

Receipts: none beyond the commands and quotes above (HTML fetched to scratch only; hashes in section 1).
