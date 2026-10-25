# Frontier7Errno731 — round-37 errno-discrimination theme: source and overlap scan

Seat: Frontier7Errno731 (scout). Wave: `tsukuroi-r37-w1`. Lane tip read: `8936643` ("round-37: assimilate sourced errno entries and quarantine gate"), working tree also carries uncommitted round-37 C2 work (`LOG.md`, `SKILL.md`, `corpus/README.md`, `corpus/knowledge/journalctl-v262-field-filter-r36.md`, `tools/check-journalctl-v262-corrections.py`).
Lane bounds: leaf member — no subagent dispatch, no background jobs, no wave spawns, no git/jj writes, no pacman, no host change. Only write performed: this report.

## Axes

- **frontier:errno** — is the errno-discrimination theme's admitted material *sourced* (does every cited locator actually resolve to the quoted bytes), and is the theme admitted on the right scope rather than as new coverage?
- **adjacency** — do the theme's rows and entries stay inside the lane's own registry/coverage-map namespace, or do they collide with the staged package and with the sibling lane's file space?

Godspeed moves kept: one bounded source sweep (cheap, parallel) over the three staged entries' own cited sources; one bounded overlap sweep over `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, the staged package, the landed round-37 artifacts, and the sibling `shokuknow` merge tree. Moves dropped: no host probe (nothing in the question needed live host state); no campaign tool; no package tool.

## Scope of this scan

Sources and artifacts opened **this round** (2026-10-25), read-only:

| Artifact | Path / URL | Note |
|---|---|---|
| staged package (read-only sibling) | `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/` | `MERGE-REPORT.md`, `MERGE-REPORT.json`, `SOURCES.append.md`, `knowledge/corpus/knowledge/*.md` |
| three staged entries | `errno-name-discrimination-r25.md`, `mount-errno-contract-r26.md`, `errno-contract-variance-r37.md` | read in full |
| sibling own-work captures | `shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt`, `lane-errno13-probe.txt` | read in full |
| lane registry | `corpus/SOURCES.md` (207 rows at tip) | full sweep |
| lane coverage map | `corpus/README.md` (278 lines worktree / 282 at tip) | round-37 rows read |
| lane lesson | `corpus/lessons/round-37.md` | § Gate read in full |
| lane declaration | `SCORECARD.md:1936-1941` (§10 Assimilation) | read |
| lane province | `PROVINCE.md` § Core / § Frontier / § Adjacent | read |
| lane held errno notes | `corpus/knowledge/snapper-eacces-mechanism.md`, `root-dac-decision-r12.md` | swept for overlap |
| staged/landed tooling | `.ufo/waves/round-37/assimilation/{staged-ids,reg-ids,collisions,SOURCES.append.md,quarantine-decisions.md}` | read |
| upstream sources | errno(3), mount(2), errno-base.h, btrfs ioctl.c, btrfs-subvolume.rst, overlayfs.rst | see citations below |

Fetch errors observed (reported, not worked around silently): `https://man.archlinux.org/man/errno.3` → **ECONNRESET** (transport failure) on 2026-10-25; `https://man.archlinux.org/man/mount.2` → **ECONNRESET** on 2026-10-25; `https://git.kernel.org/.../man-pages-6.19` master branch → empty body (only the `man-pages-6.19` tag resolved); `raw.githubusercontent.com/man-pages/man-pages/master/man/man3/errno.3` → HTTP 404 (repository layout differs from the mirror used). Consequence: the errno(3) section structure below is established from the **man-pages 6.19 tag source at git.kernel.org** and from the **man7.org 6.19 render**, both of which resolved; no claim about man.archlinux.org's own rendering is made.

## Finding F1 (primary, precise) — row S204 cites a section that does not exist in errno(3)

**Statement.** The landed row S204 and both landing artifacts that restate it locate the quote "EACCES 13 Permission denied" in an `EXAMPLES` section of errno(3). errno(3) has no such section; the example is inside `DESCRIPTION`, in the `Error numbers and names` subsection.

Landing sites of the wrong locator:
- `corpus/SOURCES.md:213` — row S204 anchor cell: "EXAMPLES, `errno -s permission`; Linux man-pages 6.19".
- `corpus/knowledge/errno-contract-variance-r37.md:4` — `source:` header line for S204: "`EXAMPLES`, `errno -s permission`".
- `corpus/lessons/round-37.md:15` — § Gate row S204, Location column: "`EXAMPLES`, `errno -s permission`".

Evidence (opened this round):
- `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man3/errno.3?h=man-pages-6.19` (accessed 2026-10-25). Section list is exactly: `.SH NAME`, `.SH LIBRARY`, `.SH SYNOPSIS`, `.SH DESCRIPTION`, `.SH NOTES`, `.SH SEE ALSO` — there is **no** `.SH EXAMPLES`. Located quote (4 words): `".SS Error numbers and names"` — the subsection that begins the number-and-name material (roff line 65).
- The example itself is at roff line 125, inside that subsection, in an `.EX/.EE` block. Located quote (6 words): `'.RB $ " errno \-s permission" ;'`. The quoted output line follows at line 126.
- `https://man7.org/linux/man-pages/man3/errno.3.html` (accessed 2026-10-25) — the rendered 6.19 page exposes anchors `NAME`, `LIBRARY`, `SYNOPSIS`, `DESCRIPTION`, `NOTES`, `SEE_ALSO`, `COLOPHON`; a search for an `EXAMPLES` anchor returns **0** hits. Located quote (21 words): "The error numbers that correspond to each symbolic name vary across UNIX systems, and even across different architectures on Linux."

Adjacent rows on the same page are correct, which localizes the fault to S204 rather than to the source: S202 anchors "DESCRIPTION, errno significance paragraph" and S203 anchors "DESCRIPTION, Error numbers and names" — both are real headings of the same document. S204 is the only row of the three naming a section that is absent.

**Provenance.** The defect is inherited, not freshly introduced: staged row S281 in `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` already anchors it as "the `EXAMPLES` section of `errno(3)`", and the staged entry `errno-contract-variance-r37.md` repeats the framing. The round-37 transform re-grounded the quotes but carried the section name through unchanged.

**Why it matters.** The lane's own bar makes this a hard defect, not a stylistic nit: QUALITY 23 (R16-SECTION) — "resolve the exact heading and uniquely identified table row in the cited revision… A correct quote does not excuse a wrong section number" — and QUALITY 21 (R15-LOCATOR) — "use a stable source heading/fragment". QUALITY 61 (R26-GATE-RECORD-MISSING) requires the Gate record to carry a located quote; the S204 Gate row carries a correct quote under a location that does not exist, so the Gate's own locator is unresolvable.

**Smallest correction.** Change the S204 anchor in `corpus/SOURCES.md:213` from `EXAMPLES, `errno -s permission`` to `DESCRIPTION, Error numbers and names (the errno(1) example); Linux man-pages 6.19`, and apply the same string in `corpus/knowledge/errno-contract-variance-r37.md:4` and `corpus/lessons/round-37.md:15`. No row status, teaches cell, or quote changes; the taught proposition ("the page's example of resolving EACCES to its number on a specific Linux system") is unaffected — "EACCES 13 Permission denied" is verbatim in the source.

## Finding F2 (scope, precise) — the declaration's ids and filenames do not match what landed, and collide with the staged package's own id meanings

**Statement.** `SCORECARD.md:1936-1941` (§10 Assimilation) states: "THREE package entries admitted from `merge/tsukuroi/`: `errno-name-discrimination-r25.md`, `mount-errno-contract-r26.md`, `errno-contract-variance-r37.md`; rows S204/S205/S214/S220/S279–S282/S286/S287 appended". At tip `8936643`, none of that matches the landed state:

- **Ids that do not exist.** `corpus/SOURCES.md` at tip holds S001–S207 (207 rows). S214, S220, S279, S280, S281, S282, S286, S287 each return **0** matches. The landed rows are S200–S207 only.
- **Filenames that do not exist.** The landed entries are `corpus/knowledge/mount-errno-contract-r37.md` and `corpus/knowledge/errno-contract-variance-r37.md`. There is no `mount-errno-contract-r26.md`; `errno-name-discrimination-r25.md` was **rejected** (`corpus/lessons/round-37.md:22`), not admitted. The declaration also describes "collision-guard proven", while `.ufo/waves/round-37/assimilation/collisions` is **0 bytes**.
- **Id-meaning collision between two committed artifacts.** The merge package's own `SOURCES.append.md` (committed in the same tip commit) maps its S204 to btrfs-subvolume(8), S205 to errno(3) at man.archlinux.org, S200 to mkinitcpio(8), S201 to alpm-hooks(5), S203 to overlayfs.rst. The lane registry's S200–S207 map to entirely different sources (mount(2), btrfs ioctl.c, errno(3)×3, errno-base.h, two own-work captures). S204 and S205 therefore name **different documents** in the two files that both live inside the lane repo at the same tip.

**Why it matters.** Two readers can both be "right" and still be citing different documents under one id: the wave's staged id space (`.ufo/waves/round-37/assimilation/staged-ids`, S200–S346, 147 ids) overlaps the landed id space S200–S207 that was reused for re-grounded rows. The empty `collisions` file does not cover this, because the guard compares staged ids against the *pre-round* registry (S001–S199), not against the staged package's own id→source mapping. The lane's convention for correcting a superseded claim is an appended notice (QUALITY 60, R26-UNDISCLOSED-INPLACE); the round-37 truth is currently recorded only in `corpus/lessons/round-37.md` § Gate and `corpus/README.md:271-278`, while the tracked declaration still carries the pre-landing wording.

**Smallest correction.** Append to `SCORECARD.md` (do not rewrite §10) a round-37 assimilation notice naming: two entries admitted (`mount-errno-contract-r37.md` = S200–S201, `errno-contract-variance-r37.md` = S202–S207); one candidate rejected (`errno-name-discrimination-r25.md`, reason at `corpus/lessons/round-37.md:22`); the staged package's S200–S346 id space was **not** adopted, so its id→source meanings must not be cited against the lane registry; and the eight declared-but-absent ids (S214, S220, S279–S282, S286, S287) never entered the lane registry.

## Finding F3 (scope, precise) — S206/S207 locators are unresolvable from the lane repo root

**Statement.** Rows S206 and S207 locate their own-work captures as `shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt` and `…/lane-errno13-probe.txt` (`corpus/SOURCES.md:215-216`; same strings in `.ufo/waves/round-37/assimilation/SOURCES.append.md` and `corpus/lessons/round-37.md:16-17`). From the lane repository root those paths do not resolve: `ls shokuknow` → "No such file or directory"; the lane repo has no `lanes/` directory either. The path is neither absolute nor lane-relative — it is relative to `/home/vgpnk/Projects`.

**Why it matters.** The lane's own-work rows elsewhere use lane-relative (`tools/tsukuroi-census.sh`, `corpus/knowledge/…`) or absolute host paths (`/var/log/pacman.log`). A reader at the lane repo root cannot re-open the cited bytes from the row as written; QUALITY 21 (R15-LOCATOR) requires a locator that resolves. The same pattern affects 28 rows of the staged package, so it is a package-wide convention rather than a one-row slip.

**Smallest correction.** In `corpus/SOURCES.md:215-216`, write the absolute path `/home/vgpnk/Projects/shokuknow/lanes/tsukuroi/round9/…` (as the lane's existing S030 does for an out-of-lane artifact), or copy the two capture files under `corpus/knowledge/` and cite them lane-relative; apply the same change in `corpus/lessons/round-37.md:16-17` and in the note headers.

## Finding F4 (secondary, informs the reject row) — the rejected candidate's overlayfs rows are unsupported by its own declared sources

**Statement.** `errno-name-discrimination-r25.md` (the rejected candidate) lists a six-class errno table whose `EXDEV`, `ESTALE` and `EBUSY` rows attribute overlayfs-specific semantics ("an overlayfs lower/merged-directory rename with `redirect_dir` disabled"; "overlayfs failed to verify the lower root origin at mount time"; "the upperdir/workdir is already in use by another overlay mount"). The candidate's own declared sources are errno(3) (S205) and btrfs-subvolume(8) (S204). Neither mentions overlayfs: `grep -ci overlay` returns **0** for both, opened this round. The actual support is staged row S203 (overlayfs.rst) — a source the candidate does not declare and that was not adopted.

Evidence for the true support: `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/overlayfs.rst` (accessed 2026-10-25). Located quotes — "return EXDEV error: this error is returned by rename(2) when trying to move a file or directory across filesystem boundaries" (19 words); "On failure to verify the lower root origin, mount will fail with ESTALE." (14 words); "Using an upper layer path and/or a workdir path that are already used by another overlay mount is not allowed and may fail with EBUSY." (24 words). The btrfs side of the same candidate is sound: `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-subvolume.rst` (accessed 2026-10-25), located quote (12 words): "returns error (EPERM) and this is logged to the system log".

**Why it matters.** The recorded reject reason (`corpus/lessons/round-37.md:22`) is "duplicates… and the candidate has no explicit `## QUALITY check` required by QUALITY 14". The reject decision is correct, but the *strongest* available ground is missing: three of six table rows are attributed to sources that do not carry them, which is QUALITY 19 (R14-SOURCE-SCOPE) and QUALITY 66 (R26-TEACHES-OVERSTATED), independent of duplication and of the missing QUALITY check. The recorded flip condition ("a revised entry demonstrates a distinct uncovered proposition… passes every applicable QUALITY criterion with source/evidence pointers resolved") would cover it only if a reviser notices it; naming it explicitly prevents a future revival from re-attaching overlayfs semantics to errno(3) or btrfs-subvolume(8).

**Smallest correction.** Append to the reject row in `corpus/lessons/round-37.md:22` one clause: the candidate additionally mis-attributes its overlayfs EXDEV/ESTALE/EBUSY semantics to S205/S204, which do not mention overlayfs; the overlayfs statements are supported only by staged S203 (overlayfs.rst), which was not admitted. No row change; the reject stands either way.

## Overlap and coverage assessment (bounded sweep)

- **The theme is held ground, and the landing says so.** `PROVINCE.md:23` places the Snapper/rollback net in Core with the boundary "Diagnose filesystem mode and unit capability restrictions; report mechanism/falsifier"; `corpus/README.md:40-41` carries the standing "errno:13 mechanism stays [inf]" frontier bullet. The two landed notes are additions to that surface, and `corpus/README.md:278` states it plainly: "These entries deepen the existing errno/snapshot frontier (`corpus/README.md:38-42,151-153`); they add no new coverage surface or host repair." No coverage-map overclaim found.
- **No duplicate of the landed errno(3) rows already in the lane registry.** Before this round the registry held no errno(3) row; S035 (mkdir(2), man.archlinux.org) is the only errno-semantics row and covers a different proposition (directory-creation errno classes, not the significance/portability contract). The landed S202/S203 are therefore new *rows*, not re-registrations. The three-row split of one page into S202/S203/S204 is disclosed as two W04 duplicate-URL advisories (`corpus/lessons/round-37.md:28`), consistent with the lane's existing scope-separated reuse practice.
- **Same-document reuse across hosts is a latent hazard.** The staged package's S205 (errno(3) at man.archlinux.org) and its S279–S281 (errno(3) at man7.org) are the same man-pages 6.19 document under two URLs; the landed registry represents that document only via man7.org (S202–S204). Any future revival of staged errno(3) rows must not add a fourth/fifth row for the same page.
- **Adjacency to the sibling lane is respected on content, not on locators.** The two own-work rows import bytes from the sibling `shokuknow` tree (F3), but the sibling tree was read only; no sibling file was modified. The lane's own `corpus/knowledge/snapper-eacces-mechanism.md` (8 `errno:13` matches, 2026-10-19) and `root-dac-decision-r12.md:61` (9 matches at the 2026-10-20 query) remain in place, and the new note's own-work evidence says the recheck now returns 0 — the lane has not been asked to rewrite its held evidence, and it was not.
- **The rejected candidate's namespace overlap was correctly judged.** The candidate's six-class vocabulary table overlaps the admitted operation-specific table in `mount-errno-contract-r37.md` and the retention-aware entry in `errno-contract-variance-r37.md`; the reject is consistent with QUALITY 68 (R27-DECLARED-FRONTIER-OVERCLAIM) applied to the package rather than to the lane's coverage map.

## Sources cited (opened this round; URL, access date, located quote)

| # | URL | Accessed | Located quote (≤25 words) | Location |
|---|---|---|---|---|
| 1 | https://man7.org/linux/man-pages/man3/errno.3.html | 2026-10-25 | "The error numbers that correspond to each symbolic name vary across UNIX systems, and even across different architectures on Linux." | `DESCRIPTION` → `Error numbers and names`; footer "Linux man-pages 6.19 2026-05-28" |
| 2 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man3/errno.3?h=man-pages-6.19 | 2026-10-25 | ".SS Error numbers and names" | roff line 65, inside `.SH DESCRIPTION` (line 18) |
| 3 | https://man7.org/linux/man-pages/man2/mount.2.html | 2026-10-25 | "Some filesystems instead return the error EROFS on an attempt to mount a read-only filesystem." | `ERRORS`; footer "Linux man-pages 6.19 2026-02-11" |
| 4 | https://man7.org/linux/man-pages/man2/mount.2.html | 2026-10-25 | "ENODEV filesystemtype not configured in the kernel." | `ERRORS` |
| 5 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno-base.h | 2026-10-25 | "#define EACCES 13 /* Permission denied */" | tag v7.2 |
| 6 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c | 2026-10-25 | "Subvolume creation is not restricted, but snapshots are limited to own subvolumes only" | `create_snapshot`, lines 1178-1186 |
| 7 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-subvolume.rst | 2026-10-25 | "returns error (EPERM) and this is logged to the system log" | `delete` subsection |
| 8 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/overlayfs.rst | 2026-10-25 | "On failure to verify the lower root origin, mount will fail with ESTALE." | tag v7.2 |
| 9 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/overlayfs.rst | 2026-10-25 | "Using an upper layer path and/or a workdir path that are already used by another overlay mount is not allowed and may fail with EBUSY." | tag v7.2 |
| 10 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/overlayfs.rst | 2026-10-25 | "return EXDEV error: this error is returned by rename(2) when trying to move a file or directory across filesystem boundaries" | "renaming directories" |

Local artifacts read this round (all under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` unless noted): `corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`, `corpus/lessons/round-37.md`, `corpus/knowledge/errno-contract-variance-r37.md`, `corpus/knowledge/mount-errno-contract-r37.md`, `corpus/knowledge/snapper-eacces-mechanism.md`, `corpus/knowledge/root-dac-decision-r12.md`, `PROVINCE.md`, `SCORECARD.md`, `.ufo/waves/round-37/assimilation/*`; sibling read-only `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/{MERGE-REPORT.md,MERGE-REPORT.json,SOURCES.append.md,knowledge/corpus/knowledge/*}`, `/home/vgpnk/Projects/shokuknow/lanes/tsukuroi/round9/{host-errno-capture.txt,lane-errno13-probe.txt}`.

## Confidence and unknowns

- **High** — F1 (S204 `EXAMPLES`): the 6.19 tag source and the 6.19 render both lack that section, and the two adjacent rows on the same page use real headings; the string appears verbatim in three landing sites.
- **High** — F2 (declaration vs landed): verified by id existence counts against the tip registry and by reading the tip's §10 wording; the tip commit also carries the staged package's competing id→source mapping.
- **High** — F3 (own-work locator): path non-resolution reproduced from the lane repo root.
- **Medium-high** — F4 (candidate mis-attribution): the two declared sources provably never mention overlayfs, and overlayfs.rst carries the statements; the judgment that this is a *stronger* reject ground than the recorded one is mine and is labeled as such.
- **Unknown / not claimed** — the final round-37 tip (the wave is mid-flight; uncommitted C2 work is present); whether the L1 will amend `SCORECARD.md` before measurement (F2's correction is proposed, not observed as landed); the man.archlinux.org rendering of errno(3)/mount(2), which could not be fetched (transport failure, not absence); the non-author closure sample, which `corpus/lessons/round-37.md:24` records as pending and which is not lane-dispatched verification.

## Tooling

Read `/home/vgpnk/.omp/agent/RULES.md` first, as instructed. **No tool was installed or updated** — no package-manager transaction was attempted (all pacman transactions are paused host-wide, and the wave context forbids pacman), and no new binary was needed for a read-only source/overlap sweep. Source bytes were fetched over HTTPS with the session's read tool and with `curl` for byte-level section extraction only; no source body was executed or treated as instructions.

---

Report: .ufo/waves/round-37/w1/Frontier7Errno731.md
