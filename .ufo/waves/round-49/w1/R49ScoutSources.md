VERDICT: supports

Axes: census exit and W/E codes; id budget (count, gaps, next free id); used-by fit of the three rows added in round 48 against the frozen round-49 claims. Census expectations hold. Do not mint a new id for either named candidate.

## Census

Command (cwd `/fast/scratch/hyaku/tsukuroi-r49/R49ScoutSources`, `TMPDIR` that dir):

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`

Observed twice (1.87 s, then 1.90 s). Both exited 0. Receipt: `.ufo/waves/round-49/w1/R49ScoutSources/census-validate.txt` (script lines 1–41; line 42 `EXIT:0` is this seat’s trailer, not script output).

Last script lines:

```
tsukuroi	W04	S230 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

W/E codes present: **W04 only, 40 lines**. No E01–E12. No W01, W02, or W03. Code list is `scripts/sources-census.sh:24-33`. W04 does not fail the lane (`scripts/sources-census.sh:33`, `:364-365`).

The validator read the **working tree**, not the freeze blob. The only `corpus/SOURCES.md` delta versus freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c` is S255’s `used-by` cell (below). That cell still names an on-disk path, so E11 did not fire. HEAD `d7cfc27308e8af51b76b5cfe0c656acc1788cefb` has no commit after the freeze that touches `corpus/SOURCES.md`; the delta is unstaged (`git status --porcelain`: ` M corpus/SOURCES.md`, `?? corpus/lessons/round-49.md`).

### Every W04 (receipt lines 1–40)

| id | duplicate url |
|---|---|
| S038 | man.archlinux.org/man/access.2 |
| S041 | man.archlinux.org/man/systemd.exec.5 |
| S042 | github.com/omacom/omarchy/issues/8047 |
| S043 | github.com/omacom/omarchy/issues/6629 |
| S044 | man.archlinux.org/man/systemd.exec.5 |
| S046 | man.archlinux.org/man/systemd.exec.5 |
| S049 | man.archlinux.org/man/pacman.8 |
| S058 | gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init |
| S082 | git-scm.com/docs/git-rev-parse/2.56.0 |
| S087 | archlinux.org/news |
| S089 | man.archlinux.org/man/pacman.8 |
| S090 | man.archlinux.org/man/pacman.8 |
| S092 | wiki.archlinux.org/title/System_maintenance?oldid=885170 |
| S095 | gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/merge_requests/482 |
| S098 | gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs |
| S105 | archlinux.org/news/update-to-ca-certificates-mozilla-31311-1-to-prevent-man-in-the-middle-attacks |
| S106 | man.archlinux.org/man/pacman.8 |
| S107 | man.archlinux.org/man/pacman.8 |
| S108 | wiki.archlinux.org/title/Downgrading_packages?oldid=887421 |
| S109 | gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/functions |
| S111 | gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/26.134.222-3/plymouth.initcpio_hook |
| S126 | raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml |
| S136 | raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml |
| S137 | raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml |
| S138 | raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst |
| S149 | raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c |
| S155 | raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst |
| S158 | raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c |
| S182 | raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c |
| S184 | raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml |
| S185 | raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst |
| S203 | man7.org/linux/man-pages/man3/errno.3.html |
| S204 | man7.org/linux/man-pages/man3/errno.3.html |
| S217 | gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c |
| S221 | gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/util.c |
| S222 | gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c |
| S223 | gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/hook.c |
| S224 | gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc |
| S226 | gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc |
| S230 | gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c |

None of S251, S253, S254, or S255 appear in that list.

## Id budget

`grep -cE '^\| S[0-9]{3}' corpus/SOURCES.md` → **255** (working tree). Same count on freeze `55c07cd3` and on round-48 commit `a7e2b391`. Parser of the 255 `| Snnn |` lines: ids S001–S255, no gaps, no duplicate ids. **Next free id: S256.**

Round-47 commit `c5397574` has 252 ids. Round-48 commit `a7e2b391` adds exactly **S253, S254, S255** (`corpus/lessons/round-48.md:21`: “IDs S001–S252 existed at start; S253 admitted, S254 rejected and S255 admitted this round.”).

### Candidates — do not allocate S256

- **proc_pid_fd** is already **S251** (`corpus/SOURCES.md:260`). Source `https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html`. Scope: “What a /proc/<pid>/fd/<n> entry is for a file and for a pipe”. Teaches: “each fd entry is a symbolic link to the actual file; a pipe's entry reads type:[inode]”. Status mined, opened 2026-10-27, recheck 180d. used-by: `corpus/knowledge/census-identity-r46.md, corpus/lessons/round-48.md`. Round 48 re-opened it (`corpus/lessons/round-48.md:16`, `:37`); the anchor records “re-opened 2026-10-28 by SScoutProcFd, digest unchanged”. A second row on the same URL and scope would be E04 (`scripts/sources-census.sh:26`, `:646-649`); a different scope on that URL would be another W04.
- **bash redirections** is already **S255** (`corpus/SOURCES.md:264`). Source `https://www.gnu.org/software/bash/manual/bash.html`. Scope: “Explicit fd numbers in redirections, `{varname}` descriptor allocation, and the fd>9 caveat behind the census selftest's 240-249 fd-alias band”. Teaches: “Redirections using file descriptors greater than 9 should be used with care, as they may conflict with file descriptors the shell uses internally”. Status mined, opened 2026-10-28, recheck on-release. Frozen C3 is explicitly “sourced: S255 bash fd>9, re-opened this round” (`.ufo/waves/round-49/frozen/FROZEN.md:17`).

### Last 30 registry rows (working tree)

Lines `corpus/SOURCES.md:235-264`. All tier A except S254 (tier C, rejected).

| line | id | opened | recheck | used-by |
|---|---|---|---|---|
| 235 | S226 | 2026-10-26 | on-release | corpus/knowledge/pacman-exec-environment-r40.md |
| 236 | S227 | 2026-10-26 | on-release | corpus/knowledge/alpm-package-anatomy-r41.md |
| 237 | S228 | 2026-10-26 | on-release | corpus/knowledge/alpm-package-anatomy-r41.md |
| 238 | S229 | 2026-10-26 | on-release | corpus/knowledge/alpm-package-anatomy-r41.md |
| 239 | S230 | 2026-10-26 | on-release | corpus/knowledge/alpm-package-anatomy-r41.md |
| 240 | S231 | 2026-10-26 | on-release | corpus/knowledge/alpm-package-anatomy-r41.md |
| 241 | S232 | 2026-10-26 | on-release | corpus/knowledge/alpm-package-anatomy-r41.md |
| 242 | S233 | 2026-10-26 | on-release | corpus/knowledge/alpm-package-anatomy-r41.md |
| 243 | S234 | 2026-10-26 | on-release | corpus/knowledge/alpm-package-anatomy-r41.md |
| 244 | S235 | 2026-10-26 | on-release | corpus/knowledge/alpm-package-anatomy-r41.md |
| 245 | S236 | 2026-10-26 | 30d | corpus/knowledge/alpm-package-anatomy-r41.md |
| 246 | S237 | 2026-10-26 | on-release | corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md |
| 247 | S238 | 2026-10-26 | on-release | corpus/knowledge/btrfs-scrub-record-r42.md |
| 248 | S239 | 2026-10-26 | 30d | corpus/knowledge/btrfs-scrub-record-r42.md |
| 249 | S240 | 2026-10-26 | on-release | corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/lessons/round-48.md |
| 250 | S241 | 2026-10-26 | 30d | corpus/knowledge/btrfs-scrub-record-r43.md |
| 251 | S242 | 2026-10-26 | on-release | corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md |
| 252 | S243 | 2026-10-26 | on-release | corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md |
| 253 | S244 | 2026-10-26 | on-release | corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md |
| 254 | S245 | 2026-10-26 | 30d | corpus/knowledge/btrfs-scrub-record-r44.md |
| 255 | S246 | 2026-10-27 | on-release | corpus/knowledge/btrfs-scrub-grounding-r45.md |
| 256 | S247 | 2026-10-27 | on-release | corpus/knowledge/btrfs-scrub-grounding-r45.md |
| 257 | S248 | 2026-10-27 | on-release | corpus/knowledge/btrfs-scrub-grounding-r45.md |
| 258 | S249 | 2026-10-27 | 30d | corpus/knowledge/btrfs-scrub-grounding-r45.md |
| 259 | S250 | 2026-10-27 | on-release | corpus/knowledge/census-identity-r46.md |
| 260 | S251 | 2026-10-27 | 180d | corpus/knowledge/census-identity-r46.md, corpus/lessons/round-48.md |
| 261 | S252 | 2026-10-27 | 180d | corpus/lessons/round-47.md |
| 262 | S253 | 2026-10-28 | on-release | corpus/lessons/round-48.md |
| 263 | S254 | 2026-10-28 | on-release | — |
| 264 | S255 | 2026-10-28 | on-release | corpus/lessons/round-48.md, corpus/lessons/round-49.md |

Titles: S226 alpm-hooks(5); S227 alpm-package(7); S228 be_package.c; S229 makepkg.sh.in; S230 add.c (database members); S231 check.c; S232 PKGBUILD(5); S233 version.c; S234 be_local.c; S235 query.c; S236 round-41 host package-anatomy capture; S237 btrfs-progs v7.1 cmds/scrub.c; S238 btrfs-progs v7.1 CHANGES; S239 round-42 host scrub-record capture; S240 Linux v7.2.11 fs/btrfs/ioctl.c; S241 round-43 host scrub-ioctl capture; S242 scrub.c; S243 sysfs.c; S244 Arch btrfs-progs packaging 7.1-1; S245 round-44 host scrub-surface capture; S246 cmdline.c/vsprintf.c/kstrtox.c; S247 dev-replace.c; S248 systemd.kill.xml; S249 round-45 host scrub-service stop capture; S250 GNU bash 5.3 shell.c/general.c/general.h; S251 proc_pid_fd(5); S252 mktemp(1); S253 POSIX.1-2024 ch.2 word expansion; S254 Unix & Linux Q131766 (rejected); S255 GNU Bash Reference Manual 5.3, Redirections.

## Round-48 rows vs round-49 claims

Added rows and freeze `used-by` (same as `a7e2b391`, recorded at `corpus/lessons/round-48.md:38-40`):

- **S253** mined, used-by `corpus/lessons/round-48.md`. POSIX field-splitting / double quotes (`corpus/SOURCES.md:262`). C1 is the scrub grounding note, C2 is `PROVINCE.md` ADJ anchors, C3 is the census fd-band diagnostic sourced from S255 (`.ufo/waves/round-49/frozen/FROZEN.md:15-17`). None of those surfaces cite S253. **No used-by change.**
- **S254** rejected, used-by `—` (`corpus/SOURCES.md:263`; `corpus/lessons/round-48.md:39`). Not cited by C1–C3. **No used-by change.** A mined flip would be a new decision, not a used-by edit.
- **S255** needs a used-by append for C3. Freeze cell is only `corpus/lessons/round-48.md` (`git diff 55c07cd3 -- corpus/SOURCES.md` removes that single-path cell). C3 names S255 as its source (`.ufo/waves/round-49/frozen/FROZEN.md:17`). Untracked `corpus/lessons/round-49.md:15` already logs the change: `used-by` `corpus/lessons/round-48.md` → `corpus/lessons/round-48.md, corpus/lessons/round-49.md`, and the working-tree row at `corpus/SOURCES.md:264` already has that new cell. `corpus/lessons/round-49.md` is absent from the freeze (`git cat-file -e 55c07cd3:corpus/lessons/round-49.md` fails; the file exists on disk, 29 lines). **Do not append the path a second time.** S253 and S254 are unchanged in that diff.

Not in scope of “rows added in round 48”, but relevant to the same claims: C1’s grounding file is already on the used-by of S237 and S242–S249 (`corpus/SOURCES.md:246`, `:251-258`). C2 does not add a registry consumer for S253–S255. S251’s round-48 used-by extension is already landed (`corpus/lessons/round-48.md:37`); round-49 claims do not require a further S251 used-by edit.

## Not done

No `sources-census.sh` mode other than `validate` for lane `tsukuroi`. No selftest. No edit of lane content. Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ScoutSources` removed after the receipt was copied.
