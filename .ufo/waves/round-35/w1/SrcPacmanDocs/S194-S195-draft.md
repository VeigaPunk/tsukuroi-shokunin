# S194/S195 source-row drafts

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S194 | pacman 7.1 pacman(8) — https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/pacman.8.asciidoc | docs | A | Pacman's documented configuration-file upgrade hash cases and package-removal saves; not evidence of any particular host's current files | commit 54d9411; `-R, --remove` lines 50-56 and `Handling Config Files` lines 527-561; raw bytes SHA-256 `bf1569d62f74c1f380565ab55c4f8edb07d6d59ae3e5de3b79847ac6f520ee3b`; snapshot `.ufo/waves/round-35/w1/SrcPacmanDocs/pacman.8.asciidoc`; fetched 2026-10-23 | During upgrade, pacman compares original, new, and current-file MD5 hashes; the documented differing-hash and pre-existing-file cases install `.pacnew`; package removal saves most configuration files as `.pacsave` unless `--nosave` is used | queued | 2026-10-23 | on-release | — |
| S195 | pacman 7.1 pacman.conf(5) — https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/pacman.conf.5.asciidoc | docs | A | `NoUpgrade` and `NoExtract` handling of package archive paths; not evidence of host state | commit 54d9411; `NoUpgrade` lines 135-144 and `NoExtract` lines 146-157; raw bytes SHA-256 `c8e659b15d77133699ac541cfdc162d66ae5580bad5996ee30149f76671fff8f`; snapshot `.ufo/waves/round-35/w1/SrcPacmanDocs/pacman.conf.5.asciidoc`; fetched 2026-10-23 | `NoUpgrade` leaves matching paths untouched and installs incoming files as `.pacnew`; `NoExtract` prevents matching package paths from being extracted to the filesystem; both directives accept glob patterns and inverted matches | queued | 2026-10-23 | on-release | — |

## Located source quotes

- S194, `pacman.8.asciidoc:54-55`: “Most configuration files will be saved with a '.pacsave' extension unless the '\--nosave' option is used.”
- S194, `pacman.8.asciidoc:552-554`: “All three files are different, so install the new file with a '.pacnew' extension and warn the user.”
- S194, `pacman.8.asciidoc:558-559`: “The package was not previously installed, and the file already exists on the file system. Install the new file with a '.pacnew' extension”
- S195, `pacman.conf.5.asciidoc:137-138`: “a package install/upgrade, and the new files will be installed with a '.pacnew' extension.”
- S195, `pacman.conf.5.asciidoc:147-148`: “All files listed with a `NoExtract` directive will never be extracted from a package into the filesystem.”

The draft assumes the planned C2 note will cite both rows. The note path was not present in the lane when checked; confirm the citation before landing mined status. The C1 oracle's current docstring names pacman libalpm sources and pacman-contrib `pacdiff`, not these two manual pages. These rows are not registered in `corpus/SOURCES.md` by this draft.
