VERDICT: supports

## Review

Reviewed S250/S251 in `corpus/SOURCES.md` at implementation revision `a44770491eb5ca15ce9f8b3207309d1af683ffaf` (the inspected lane snapshot rows are at `corpus/SOURCES.md:259-260`). Both rows have the contract's 11 cells (`/home/vgpnk/Projects/shokunin/CORPUS.md:86-108`). `code`/`docs`, tier A, and scope are appropriate for the cited Bash implementation details and proc fd documentation (`CORPUS.md:91-100`). The sources are opened/frozen locally; `FETCH.txt:2-8` identifies tag/commit and URL provenance; `SHA256SUMS:1-4` matches all four row digests.

- S250 teaches that Bash opens the named script (`shell.c:1586`), moves the descriptor to a high available fd (`shell.c:1697-1703`; `general.c:696-704`; `general.h:251-252`), while stdin is read from fd 0 (`shell.c:780-785`). These directly ground the row's `teaches` at `SOURCES.md:259`. Tag `bash-5.3`, peeled commit, file/line anchors and per-file digests are specified; `FETCH.txt:6` correctly qualifies host patches as not part of that upstream tag. Mined status is supported by the used-by knowledge entry, and `on-release` is appropriate for a versioned software source whose relevant contents follow releases.
- S251 teaches the documented proc fd behavior: entries are symlinks to the open file, while pipes/sockets expose type and inode (`proc_pid_fd.5.html:72-84`). This grounds the `teaches` at `SOURCES.md:260`. The row gives fetch timestamp, raw HTML line range and matching digest. Mined status is supported by used-by; `180d` is an appropriate periodic recheck for this man-pages documentation. The knowledge entry's `source` and `verified-at` identify both rows and the pinned revision (`corpus/knowledge/census-identity-r46.md:1-3`), and its cited derivation repeats the sourced details (`:26-32`).

No corrective replacement cells proposed.

## Census

Ran `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` from seat scratch. Observed exit `0`, `40` warnings, and `tsukuroi\tok\t/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`. All 40 warnings are W04 duplicate-URL-across-scopes warnings; none name S250 or S251. Baseline `before/sources-census-start.txt` records 2026-10-27T04:49:57Z and the same validation output; its warning lines are also 40. Thus warning count is unchanged (40 → 40), exit remains 0.