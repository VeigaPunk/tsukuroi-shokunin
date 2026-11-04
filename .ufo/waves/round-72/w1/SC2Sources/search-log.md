# Round 72 — SOURCES.md `## Search log` paragraph (draft)

Insert as the last paragraph of `corpus/SOURCES.md` § Search log — in the current working tree that is
immediately before the `## Leads (unopened)` heading on line 390, not at EOF. The working tree already
appends a `- Round-72 search log (2026-11-03): …` bullet at EOF, inside the Leads section; that bullet
carries the counts but no exclusion reasons and no stop rationale, and a bullet is not the paragraph
form this section uses. Keep one of the two — this paragraph — and drop the bullet.

Round-72 C1 registry search (2026-11-03, Sources seat): question — what does kmod v34 specify about the
modprobe configuration plane: directory precedence and same-name suppression, lexicographic ordering
across directories with partial replacement, duplicate-filename handling in libkmod, the kernel command
line's place in the parse, dry-run, and blacklist application? Searched the three kmod v34 plain blobs
committed under `.ufo/waves/round-72/before/src/` (`man/modprobe.d.5.scd`, `libkmod/libkmod-config.c`,
`tools/modprobe.c`; digests and URLs in `src/SOURCES.json`) and, read-only and for the open lead only,
`libkmod/libkmod.c` at the same tag (HTTP 200, 19158 bytes, sha256
a3899a59ee468c1f5b1b5e59de163f589ad0384968ca08e95cc3d6ddc9923b17), whose `default_config_paths`
array at lines 44-50 is where the compiled directory list lives. Identified 3, screened 3, included 3 as
S301-S303 (docs, code, code; all tier A, status mined), excluded 0 rows. Exclusion reasons: none this
pass — the earlier r71 exclusion (a `man/modprobe.d.xml` path returning HTTP 404 at v34) is not carried
forward, because the v34 tree ships the page as `man/modprobe.d.5.scd`, which is the path now read. The
`libkmod.c` read produced no row and grounds no rule statement: it only located the array for the open
lead, and the precedence claim rests on S301's SYNOPSIS text. Stop rationale: each of the six frozen
propositions has a located line range in one of the three included snapshots, so one more source would
add vocabulary rather than resolve an open question. Registry 300 → 303 rows.
