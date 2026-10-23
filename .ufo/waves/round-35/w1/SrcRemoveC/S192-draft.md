# S192 draft — pacman removal source

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S192 | pacman libalpm remove.c at 54d9411 — https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/remove.c | code | A | Pacman 7.1.0 package-removal handling for backup-tracked files, MD5 comparison, NOSAVE, `.pacsave` creation/rotation, and removal action-log payloads; not upgrade-time `.pacnew` handling or host state | Commit 54d9411; `lib/libalpm/remove.c` lines 347–426 and 529–562; raw bytes SHA-256 `a052d455f088f34bf1d713a434957de7e1b9322862a07b69160c65ee15dca314`; snapshot `.ufo/waves/round-35/w1/SrcRemoveC/remove.c` (798 lines), fetched 2026-10-23 | A backup-tracked file is saved as `.pacsave` only when its computed MD5 differs from the recorded hash and NOSAVE is unset; earlier saves rotate to numbered suffixes without a success action-log call, while the new save uses `warning: %s saved as %s` | candidate | 2026-10-23 | on-release | tools/score-pacnew-arm-r35.py |

## Located quotes

All quotations below are exact substrings of the saved source; each is under 25 whitespace-separated words.

- `remove.c:536`: `int cmp = filehash ? strcmp(filehash, backup->hash) : 0;`
- `remove.c:533`: `"transaction is set to NOSAVE, not backing up '%s'\n"`
- `remove.c:548`: `"%s.pacsave"`
- `remove.c:400`: `"%s.pacsave.%lu"`
- `remove.c:560`: `"warning: %s saved as %s\n"`

## Status and duplicate check

`candidate` is deliberate: `corpus/knowledge/pacman-backup-files-r35.md` did not exist when checked, so no knowledge note was observed citing this row. The existing C1 oracle names `remove.c` among its source inputs (`tools/score-pacnew-arm-r35.py:14-24`), so that tool is the only used-by entry in this draft. Change to `mined` only once a note cites S192. A search of the current `corpus/SOURCES.md` for the exact raw URL, `remove.c`, and this SHA-256 found no match; no duplicate row is known by URL or recorded digest. Different-URL saved artifacts were not exhaustively byte-compared.
