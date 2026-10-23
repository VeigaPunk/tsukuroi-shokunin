source: S191 pacman `lib/libalpm/add.c` at 54d94116164b; S192 pacman `lib/libalpm/remove.c` at 54d94116164b; S193 pacman-contrib `src/pacdiff.sh.in` at v1.13.1; S194 pacman `doc/pacman.8.asciidoc` at 54d94116164b; S195 pacman `doc/pacman.conf.5.asciidoc` at 54d94116164b; S196 pacman NEWS at 54d94116164b (5.0.0 entry); S010/S011 ArchWiki (operator guidance and log limits)
verified-at: 2026-10-23
recheck: on-release; procedure: after a pacman or pacman-contrib upgrade, re-open the same paths at the installed commit or tag (the directory names `/var/lib/pacman/local/pacman-<version>` and `/var/lib/pacman/local/pacman-contrib-<version>` name it) and re-read the hash branches and `alpm_logaction` calls of add.c, the save and `shift_pacsave` code of remove.c, pacdiff's find expression, and the NoUpgrade text; any host comparison reads file names and `/var/log/pacman.log` only; no package-manager transaction

# Pacman 7.1 backup files — when pacman makes `.pacnew` and `.pacsave`, and which events it logs (round 35)

Round 35, C2 (depth, exploratory). Integrated by the L1 from wave-1 ScribeC2Draft (`.ufo/waves/round-35/w1/ScribeC2Draft/`) with the wave-2 corrections of W2QuoteHash, W2QuoteRemove, W2QuotePacdiff, W2CritC2Depth and W2RevC2Quality. Source snapshots and sha256: `.ufo/waves/round-35/w1/Src*/` and `ScribeC2Draft/`. Version scope: pacman 7.1.0 at commit 54d94116164b0b2202c6061c4a59c6f3e70820d8 (`/var/lib/pacman/local/pacman-7.1.0.r9.g54d9411-3`), pacman-contrib 1.13.1.

## Prior state

`pacnew-plane.md` (fleet round 1) pairs the readable `/etc` sweep with the log and bounds permission failures; `package-state-plane.md:146-155,217-226` explains backup-file differences in `pacman -Qkk`; S011 already says the log does not track current files. No entry said, from pacman's own code, which situation makes which file, which of those events pacman logs, or why a current `.pac*` file can have no log line. That mechanism is what this note adds: deeper ground on an owned surface, not a new surface. Sweep (QUALITY 68, 2026-10-23): `grep -rlniE 'pacsave|pacnew|NoUpgrade' corpus/knowledge SKILL.md PROVINCE.md corpus/README.md` lists `arch-news-gate-2026.md`, `degraded-triage-r4.md`, `host-health-report-r3.md`, `pacnew-plane.md`, `update-safety-note.md`, `update-safety-v2.md`, `update-safety-v3.md`, two JSON registries, `corpus/README.md`, `PROVINCE.md` and `SKILL.md`; none reads pacman's source for these branches.

## [obs] Upgrade: the three hashes (S191, S194)

When an archive member would overwrite an existing regular file that the old package lists as a backup file, pacman compares MD5 digests: the original recorded in the old package's backup entry, the current file on disk, and the incoming file (S194 `Handling Config Files`, lines 527-561; S191 lines 352-404). The new package's backup record is assigned the incoming file's MD5 before the decision (S191 lines 333-336), so keeping a locally modified file does not make its digest the recorded one.

| original / current / incoming | Outcome | Log line |
|---|---|---|
| X / X / X | new file installed over the current one | none |
| X / X / Y | current file unmodified: new file installed | none |
| X / Y / X | package unchanged, file modified: current file kept | none |
| X / Y / Y | current already equals the new file: installed | none |
| X / Y / Z | current kept, incoming written as `<F>.pacnew` | `warning: <F> installed as <F>.pacnew` (S191 lines 403-404) |
| none / Y / Z | no recorded original (first install, or a file the new package newly marks as backup: "allow adding backup files retroactively", S191 line 310): current kept, incoming as `.pacnew` | same warning |

S194 line 552-554: "All three files are different, so install the new file with a '.pacnew' extension and warn the user." With no original hash and current equal to incoming (none / Y / Y), the first branch (current equals incoming) installs the file and writes no `.pacnew` (S191 lines 365-372): an absent original hash is not by itself a `.pacnew` case.

[inf] An existing `<F>.pacnew` from an earlier upgrade can be overwritten silently. pacman extracts the incoming bytes to the `.pacnew` path first and removes that path afterwards only when it did not exist before; in the X / Y / X branch no warning is written, so an old `.pacnew` can change content with no new log line (W2CritC2Depth finding 2, a reading of S191 lines 315-380, not reproduced on a host).

## [obs] NoUpgrade and NoExtract (S191, S195)

S195 lines 136-138: "All files listed with a `NoUpgrade` directive will never be touched during a package install/upgrade, and the new files will be installed with a '.pacnew' extension." In the code this holds only when the target already exists as a regular file: NoExtract is checked first and skips the member entirely, a missing target is extracted normally, and directory/type cases return before the NoUpgrade check (S191 lines 223-250, 286-304). For an existing listed file the hash comparison is skipped and the incoming file always becomes `.pacnew`, with the same warning line (S191 lines 338-350). NoUpgrade and NoExtract are file-extraction rules, not package version pins: the older grouping of them with `IgnorePkg` as pins (`SKILL.md:397-399`, `update-safety-note.md:420-424`, `update-safety-v2.md:52,193-198`) is superseded as a classification by this note; the values those entries recorded (both empty on this host, re-measured 2026-10-23 by wave-1 ExecHostPacnew) stand.

## [obs] Removal and numbered saves (S192, S194)

On removal, a backup-listed file is saved only when NOSAVE is unset and its current MD5 differs from the recorded one: "int cmp = filehash ? strcmp(filehash, backup->hash) : 0;" (S192 line 536). If the MD5 cannot be computed (`filehash` NULL), `cmp` is 0, no save is made and the code goes on to unlink the file (S192 lines 536-575): an absent `.pacsave` is not proof that the file was unmodified. `--nosave` skips the save (S192 line 533; S194 lines 54-55: "Most configuration files will be saved with a '.pacsave' extension unless the '\--nosave' option is used.").

Before writing a new `<F>.pacsave`, `shift_pacsave` renames existing numbered saves up by one and the existing `<F>.pacsave` to `<F>.pacsave.1` (S192 lines 347-417). Those renames have no `alpm_logaction`; only the new save is logged afterwards, as `warning: <F> saved as <F>.pacsave` (S192 lines 559-560).

## [obs] `.pacorig` and pacdiff's names (S193, S196)

The NEWS 5.0.0 entry at the pinned commit says: "Remove support for ".pacorig" files.  Instead, packages files are extracted as a ".pacnew" and the original stays in place" (S196, NEWS lines 527-528). add.c, remove.c, pacman.8 and pacman.conf.5 at 54d9411 contain no `pacorig` (grep, 2026-10-23), and `/usr/lib/libalpm.so.16` on this host carries no `.pacorig` string (ExecHostPacnew). [inf] pacman 7.1's own config-file handling no longer produces `.pacorig`; a package that ships a file literally named `*.pacorig` would still install it like any file. pacdiff 1.13.1 still searches `\*.pacnew \*.pacorig \*.pacsave '*.pacsave.[0-9]*'` with no type filter (S193 lines 228-235); its pacman-database mode derives candidates from `%BACKUP%` records (S193 lines 243-245); and it files `.pacsave.N` among old saves without prompting (S193 line 327: "add matches for pacsave.N to oldsaves array, do not prompt"). Discovery names are not production evidence. The `.pacorig` grep: `grep -c pacorig` over the four snapshots under `.ufo/waves/round-35/w1/Src*/` (0 each) and `grep -rn pacorig` over the extracted pinned tree (`ScribeC2Draft/pacman-54d9411.tar.gz`, sha256 `830ab30f0b10…c9a5a`, not committed: over 1 MiB), whose only hits are NEWS:527 and README:537, 574, 582-585 (history notes).

## [inf] Reading the log against the filesystem

- A current `<F>.pacsave.N` never has a log line naming it: the rename that made it is unlogged; the log names only the `<F>.pacsave` it was at save time.
- A current `<F>.pacnew` may have been rewritten after its logged event (above), so its log line dates its first appearance, not its content.
- A logged target that is gone now is the normal result of an operator merge (S011: "Always compare and merge the changes manually."); S011 also says the log "does not keep track of the files currently in the filesystem nor the ones that have already been removed."
- A current `.pacorig` is not from pacman 7.1's backup handling; it predates 5.0.0 or comes from elsewhere.

## [unk]

No host event was reproduced: the silent-rewrite and NULL-hash branches are source readings. Whether this host ever hit them is unknown.

## Falsifier

At the pinned sources: an `alpm_logaction` on any `shift_pacsave` rename path, a `.pacnew` decision branch other than the six rows and NoUpgrade, or a `.pacorig` producer in add.c or remove.c falsifies the matching statement. A later pacman release that changes these is version drift, recorded by the recheck, not a falsification of this pinned note.

## QUALITY check

1. Falsifiable: each branch statement names its source lines; the Falsifier names the contrary evidence. 2, 7. Sources are S191-S196 (tier A, opened this round) and S010/S011 (registered); no tier C. 3. [obs]/[inf]/[unk] are marked; the silent rewrite and the `.pacorig` conclusion are [inf]. 4. New note; corrections will be appended. 6, 26. No package-manager action is advised or run; the recheck reads names and the log only. 8. Header trio with cadence. 9. The `.pacorig` negative names its grep scope (four files at 54d9411 and the host library) and date. 12. pacman's code and manuals were opened. 19, 66. Each quote is ≤25 words; branches are kept (the NULL-hash cases, NoUpgrade's prerequisites). 63. No opened source contradicted a declared mechanism statement. 67. The superseded NoUpgrade grouping is named with its loci; those files are not edited. 68. Sweep named under Prior state.
