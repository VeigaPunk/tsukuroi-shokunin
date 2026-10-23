source: S191 pacman 54d9411 lib/libalpm/add.c; S192 pacman 54d9411 lib/libalpm/remove.c; S193 pacman-contrib v1.13.1 src/pacdiff.sh.in; S194 pacman 54d9411 doc/pacman.8.asciidoc; S195 pacman 54d9411 doc/pacman.conf.5.asciidoc; S010/S011 ArchWiki guidance and log limits; supplemental unregistered same-commit pacman NEWS (5.0.0 entry, URL below).
verified-at: 2026-10-23
recheck: on-release; procedure: reopen the pinned upstream paths at each release and recheck the hash branches, action-log calls, removal shifts, NoUpgrade text, and pacdiff search names; any host comparison reads existing files and logs only, with no package-manager invocation or mutation.

# Pacman backup files — source-grounded behavior (round 35 draft)

Draft only; intended landing path: `corpus/knowledge/pacman-backup-files-r35.md`. Axis: depth (exploratory). These are version-scoped source observations, not a live-host measurement.

## [obs] Upgrade hash decision

Tuple is `(original recorded MD5, current filesystem MD5, incoming package MD5)`. Pacman 7.1's manual names all three (S194, `Handling Config Files`, lines 529–534); `add.c` compares current/new first, then original/new, then original/current (S191 lines 357–404).

| Hashes | Outcome | pacman.log artifact line | Located source quote and support |
|---|---|---|---|
| X/X/X | Install new file over current; no `.pacnew`. | none | S194:536–538, “All three files are the same, so overwrites are not an issue.” Code branch S191:365–370. |
| X/X/Y | Install new version over unmodified current; no `.pacnew`. | none | S194:540–543, “Since the user did not ever modify the file, and the new one may contain improvements or bug fixes, install the new file.” Code S191:381–388. |
| X/Y/X | Keep modified current; discard staged new copy when newly staged. | none | S194:545–547, “Both package versions contain the exact same file, but the one on the file system has been modified. Leave the current file in place.” Code S191:373–380. |
| X/Y/Y | Install new file over current; no `.pacnew`. | none | S194:549–550, “The new file is identical to the current file. Install the new file.” Code S191:365–372. |
| X/Y/Z | Keep current and install incoming version as `.pacnew`. | `warning: <path> installed as <path>.pacnew` (S191:403–404). | S194:552–555, “All three files are different, so install the new file with a '.pacnew' extension and warn the user.” |
| NULL/Y/Z | Existing file lacks a prior recorded backup hash (first install or retroactively designated backup): keep current and install `.pacnew`. | `warning: <path> installed as <path>.pacnew` (S191:403–404). | S194:557–560, “package was not previously installed”; “Install the new file with a '.pacnew' extension and warn the user.” S191:310–313: “allow adding backup files retroactively.” |

The log column means a `.pacnew`/`.pacsave` artifact warning, not the separate package transaction record. The first four cases take debug-log branches; the warning `alpm_logaction` for hash-based `.pacnew` creation is the final branch (S191:365–404).

[obs] `NoUpgrade` bypasses the hash decision: matching archive paths are not touched, the package version becomes `.pacnew`, and `add.c` emits the `.pacnew` warning (S191:301–314, 338–350). S195:135–138 says “files listed with a `NoUpgrade` directive will never be touched during a package install/upgrade” and “new files will be installed with a '.pacnew' extension.”

## [obs] Removal and numbered saves

A recorded backup file is saved only when `NOSAVE` is false and its current MD5 differs from the package database's recorded hash: `alpm_compute_md5sum(file)` is compared with `backup->hash`, and only `cmp != 0` enters the save branch (S192:529–548). Source quote S192:529–530: “if the file needs backup and has been modified, back it up to .pacsave”; S192:535–538 gives the MD5 comparison. `NOSAVE` skips the backup (S192:532–534; quote at 533: “transaction is set to NOSAVE, not backing up '%s'”). After a successful rename, the logged warning is `warning: <path> saved as <path>.pacsave` (S192:549–560). The man page also states `--nosave` bypasses the usual backup designation (S194:398–401).

Before making a new `.pacsave`, `shift_pacsave` moves numbered saves upward and renames an existing `.pacsave` to `.pacsave.1` (S192:347–417). Those success-path renames have no separate `alpm_logaction`; the new base `.pacsave` warning is logged afterward (S192:559–560). pacdiff recognizes numbered saves and puts them in its old-saves list without prompting (S193:327–330, quote: “add matches for pacsave.N to oldsaves array, do not prompt”).

## [obs] `.pacorig`

[obs] Targeted source grep on 2026-10-23, pattern `pacorig|\.pacorig`, across S191 `add.c`, S192 `remove.c`, S194 `pacman.8.asciidoc`, and S195 `pacman.conf.5.asciidoc` returned no matches.
[obs] The same pattern over the fetched full pacman 54d9411 source tree reported `NEWS:527`, `README:537`, `README:574`, and `README:582–585`. NEWS is the 5.0.0 entry and says “Remove support for ".pacorig" files. Instead, packages files are extracted as a ".pacnew" and the original stays in place.” README hits are historical API names/removal notes, not a creator.
[inf] Pacman 7.1 no longer makes `.pacorig`: the pinned tree's 5.0.0 NEWS says support was removed, and the reviewed add/remove implementation has no hits. pacdiff still searches `.pacorig` (S193:228–235) and constructs that pathname from package backup data (S193:243–245, `print_existing "/$bkup.pacorig"`); discovery is not creation.

## [inf] Reading the log against the filesystem

The log is event history, not a current inventory: S011, `Locating .pac* files`, says “the log does not keep track of the files currently in the filesystem nor the ones that have already been removed.” A present `.pacsave.1` may have no log line naming that current path because the shift renames `.pacsave` without a distinct action-log entry; the creation warning names the unsuffixed `.pacsave` (S192:397–417, 559–560). Conversely, a logged warning does not establish that the artifact remains present now.

S010, `Deal promptly with new configuration files`, says “users must deal with these files promptly”; S011, `Managing .pac* files`, says “Always compare and merge the changes manually.” These are source guidance, not an action performed here.

## [unk]

No live filesystem or pacman.log state was measured. The `.pacorig` conclusion is source-scoped to the full fetched pacman 54d9411 tree; it does not rule out external creators. No particular current file's origin or history is established.

## Falsifier

A re-opened S191/S192 revision showing pacman create `.pacorig`, or an action-log call for the successful `.pacsave.N` renames, falsifies the corresponding source-scoped claims. A filesystem/log capture showing a present numbered save with a distinct matching shift event would falsify the stated log interpretation for that capture.

## QUALITY check

1. Pass: each hash outcome is falsifiable against the pinned branch and the Falsifier names contrary source evidence.
2. Partial: S191–S195 and S010/S011 have pinned objects and anchors; supplemental NEWS has a URL, section, and quote but no registered row, so register it before admission if retained.
3. Pass: source observations, inferences, and unknown host state are separated.
4. Pass: this is a new draft; any later correction should be an appended dated erratum.
5. Pass: no source is rejected or silently removed; any later rejection must retain its reason and flip condition.
6. Pass: no package-manager operation is advised; handling guidance is attributed to S010/S011 and no mutation was performed.
7. Partial: primary sources support the mechanism; the supplemental NEWS object is not yet an S### row and must be registered before its claim is admitted.
8. Pass: header has source, verification date, release cadence and read-only recheck; unknowns are bounded.
9. Pass: the `.pacorig` token, date, targeted four-file no-match search, and full pinned-tree match locations are stated; no host-wide absence is claimed.
10. N/A: no correction commit is proposed; no README/SKILL/knowledge sweep is claimed.
11. N/A: this draft has no landing commit; a landing must carry its matching LOG entry.
12. Pass: pacman code and manuals, plus pacdiff source, were opened; absence of a local tool is not treated as a mechanism explanation.
19. Pass for this draft: each hash row names S194's located quote and code branch; other operative claims name the source object, anchor, and a quote of at most 25 words. This is not an independent admission verdict.

## Source pins

S191: https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/add.c (add.c lines above).
S192: https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/remove.c (remove.c lines above).
S193: https://gitlab.archlinux.org/pacman/pacman-contrib/-/raw/v1.13.1/src/pacdiff.sh.in (pacdiff lines above).
S194: https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/pacman.8.asciidoc (Handling Config Files; Remove Options).
S195: https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/pacman.conf.5.asciidoc (NoUpgrade).
Supplemental, not registered: https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/NEWS, 5.0.0 section lines 510–528; captured bytes SHA-256 `30c0da27238efffb96b4fe27fcf512b2f7194f40cef4c6350681821af8d94bed`.
S010: https://wiki.archlinux.org/title/System_maintenance?oldid=885170 (Deal promptly with new configuration files).
S011: https://wiki.archlinux.org/title/Pacman/Pacnew_and_Pacsave?oldid=869214 (Locating and Managing .pac* files).
