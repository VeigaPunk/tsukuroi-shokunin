Source opened; S192 is drafted as `candidate`, not admitted.

1. [obs] I fetched the pinned pacman source from `https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/remove.c` with `curl -sL --fail` on 2026-10-23 and saved the response bytes unchanged at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/SrcRemoveC/remove.c`. `sha256sum` returned `a052d455f088f34bf1d713a434957de7e1b9322862a07b69160c65ee15dca314`; `wc -l -c` returned `798 23468`.

2. [obs] In `remove.c:529-562`, a backup entry is required; if NOSAVE is set, pacman logs the debug text `transaction is set to NOSAVE, not backing up '%s'` and skips the hash/save branch. Otherwise it computes the current MD5, compares it with `backup->hash` (`:535-538`), and only when the comparison is nonzero builds `<file>.pacsave`, renames the file and calls `alpm_logaction` with the exact payload `warning: %s saved as %s\n` (`:538-560`). If `alpm_compute_md5sum` returns null, the source sets `cmp` to zero, so this branch does not create a `.pacsave` (`:535-538`).

3. [obs] `shift_pacsave` scans names matching `<basename>.pacsave.<digits>`, shifts numbered names using `rename(oldfile, newfile)`, then renames an existing `.pacsave` to `.pacsave.1` (`remove.c:371-417`). Those successful renames have no success log call in the function; its `_alpm_log` calls concern directory-open failure or path-length overflow (`:376-380,397-417`). This distinguishes pacman.log's new-save warning from silent successful suffix rotation. The C1 oracle's docstring lists `remove.c` log formats and expects `warning: <F> saved as <F>.pacsave` (`tools/score-pacnew-arm-r35.py:14-24`).

4. [obs] The saved-source quotes and proposed 11-cell row are in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/SrcRemoveC/S192-draft.md`. Each quote is at most 25 whitespace-separated words. The row uses kind `code`, scoped tier `A`, the pinned raw-file URL, anchor lines, SHA-256 and snapshot path; it lists `tools/score-pacnew-arm-r35.py` as used-by.

5. [obs] The new note path `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/pacman-backup-files-r35.md` was absent when checked, so I left the draft status `candidate` rather than claiming note use. A search of the current registry for `remove.c`, the exact raw URL and the full SHA-256 returned no matches. [unk] I did not compare this body byte-for-byte against every differently named artifact; no duplicate is known from the registry's URL/digest records.

Gates: source fetch and digest/size measurement succeeded. No C1 scoring, census run, tests, builds, installation or host action was performed. The counter's docstring/PREDICATE were read for citation scope; its result was not re-executed.

Touched surfaces: only the source capture and S192 draft under the SrcRemoveC seat directory, plus this requested report. `corpus/SOURCES.md`, the C1 counter, the census and the C2 knowledge note were not edited. Out of scope: landing the registry row, making the note cite it, C1 counter scoring, and conclusions about live host pacsave state.

Artifacts:
- Source bytes: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/SrcRemoveC/remove.c`
- Row and quotes: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/SrcRemoveC/S192-draft.md`
- Report: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/SrcRemoveC.md`

Scope: read=CORPUS.md §64–148, SOURCES.md header/S099/S185–S190 and duplicate search, remove.c lines 347–426 and 529–562, counter docstring/PREDICATE, existing pacnew-plane.md; wrote=.ufo/waves/round-35/w1/SrcRemoveC/remove.c, .ufo/waves/round-35/w1/SrcRemoveC/S192-draft.md, .ufo/waves/round-35/w1/SrcRemoveC.md; executed=timeout 20 mkdir -p /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/SrcRemoveC; timeout 60 curl -sL --fail https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/remove.c -o /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/SrcRemoveC/remove.c; timeout 10 sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/SrcRemoveC/remove.c; timeout 10 wc -l -c /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/SrcRemoveC/remove.c
Model: not exposed
Installs: none
