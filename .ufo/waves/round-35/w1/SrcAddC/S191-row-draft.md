# S191 source-row draft

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S191 | pacman 7.1.0 libalpm add.c — https://gitlab.archlinux.org/pacman/pacman/-/raw/54d94116164b0b2202c6061c4a59c6f3e70820d8/lib/libalpm/add.c | code | A | Pacman 7.1 package-extraction behavior for NoUpgrade and backup-file `.pacnew` handling, MD5 decisions, and ALPM warning formats; not `.pacsave` or `.pacorig` creation or installed-host state | Commit 54d94116164b0b2202c6061c4a59c6f3e70820d8; `lib/libalpm/add.c` lines 303-404; raw bytes SHA-256 fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1; snapshot `.ufo/waves/round-35/w1/SrcAddC/add.c` (695 lines), fetched 2026-10-23 | NoUpgrade entries are extracted to `.pacnew`; backup entries compare local, new-package, and original MD5 values to choose replacement, preservation, or retaining the incoming file as `.pacnew` | mined | 2026-10-23 | on-release | tools/score-pacnew-arm-r35.py |

## Located quotes

1. “if(_alpm_fnmatch_patterns(handle->noupgrade, entryname) == 0) {” and “notouch = 1;” (`add.c:303-304`); “warning: %s installed as %s.pacnew\n” (`add.c:350`).
2. “if(hash_local && hash_pkg && strcmp(hash_local, hash_pkg) == 0) {” (`add.c:365`); “action: installing new file: %s\n” (`add.c:368`).
3. “else if(hash_orig && hash_pkg && strcmp(hash_orig, hash_pkg) == 0) {” (`add.c:373`); “action: leaving existing file in place\n” (`add.c:376-377`).
4. “else if(hash_orig && hash_local && strcmp(hash_orig, hash_local) == 0) {” (`add.c:381`); “action: installing new file: %s\n” (`add.c:384-385`).
5. “action: keeping current file and installing new one with .pacnew ending\n” (`add.c:399-401`); “warning: %s installed as %s\n” (`add.c:403-404`).

## Provenance and duplication

GitLab's commit API resolves `54d9411` to `54d94116164b0b2202c6061c4a59c6f3e70820d8`. The fetched file was identified as C source, ASCII text, and its SHA-256 is recorded in the anchor. The S001-S190 registry search found no matching `lib/libalpm/add.c` URL or commit, and no row contains this SHA-256. Byte identity against registry sources that have no recorded digest remains unknown.
