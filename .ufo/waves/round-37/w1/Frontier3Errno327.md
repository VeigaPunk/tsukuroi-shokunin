# Frontier3Errno327 — errno theme: one precise locator defect (S204 / `errno(3)` `EXAMPLES`)

- **Seat:** Frontier3Errno327 (scout, L2, tsukuroi lane round 37 attempt 1, wave w1).
- **Date:** 2026-10-25.
- **Axes:** adjacency, frontier:errno.
- **Milestone:** Source and overlap scan.
- **Bounds:** read-only. No lane/fleet/sibling/source-repo write; no git/jj write; no pacman or
  host change; no campaign tool; no subagent dispatch. Only surface written: this file.
- **Tools:** none installed or updated (no tool change was needed; nothing to record under
  `/home/vgpnk/.omp/agent/RULES.md`, which was read first — lines 1–14, channel order and the
  update-safety gate). All pacman transactions are paused host-wide; pacman was not used.

---

## 1. Axes and scope

- **frontier:errno:** the theme must discriminate errno *classes* on the lane's own snapshot/journal
  ground, and every claim must name a **locatable** upstream anchor. A row whose anchor names a
  section that does not exist cannot be re-opened, re-checked or falsified by a later round.
- **adjacency:** keep this inside Tsukuroi's host/rollback-net surface. Reading a public man page
  and a public kernel header is OS triage documentation, not shipped-artifact RE
  (`PROVINCE.md` "Refuses", ADJ-06 / OUT-008 / OUT-009). No sibling lane claims errno semantics —
  a bounded sweep of all 18 sibling `PROVINCE.md` files in `/home/vgpnk/Projects/shokunin/` found
  **0** case-insensitive `errno` mentions in every one. Boundary is clean; the finding below is
  internal to this lane's registry.

## 2. Bounded sweep performed

Read this round (lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`):

- `PROVINCE.md` (full), `corpus/README.md` (coverage map), `corpus/SOURCES.md` (207 rows at HEAD
  `8936643`), `corpus/knowledge/snapper-eacces-mechanism.md`,
  `corpus/knowledge/source-locator-clarification-r15.md`, `corpus/knowledge/root-dac-decision-r12.md`,
  `corpus/knowledge/root-dac-correction-r13.md`, `corpus/lessons/round-37.md`,
  `SCORECARD.md:1857-1953` (round-37 declaration), `SKILL.md` (supersession/registry discipline).
- Wave artifacts: `.ufo/waves/round-37/w1-spec.json`, `w1-plan.json`, `w1-dispatch.json`,
  `w1/swarm-registry.json`, `assimilation/{reg-ids,staged-ids,collisions,quarantine-decisions.md,
  validate/output.txt}`, and sibling seat reports `Frontier1Errno125.md`, `Frontier2Errno226.md`,
  `Frontier4Errno428.md`, `Frontier5Errno529.md`, `Frontier8Errno832.md`.
- Campaign package (read-only): `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`
  (147 rows, S200–S346), `MERGE-REPORT.md`, and the 70 staged knowledge files under
  `merge/tsukuroi/knowledge/corpus/knowledge/` (13 of them errno-named).

Id-space arithmetic (package vs. landed registry, computed from the committed bytes):

| measure | value |
|---|---|
| landed registry rows at HEAD `8936643` | 207, ids S001–S207 |
| staged package rows | 147, ids S200–S346 |
| `assimilation/reg-ids` (frozen base) | 199 ids, max S199 |
| `assimilation/collisions` | **0 bytes** |
| id numbers claimed by **both** spaces, with different content | **8** (S200–S207) |

## 3. Precise issue found — one locator defect (admit-with-correction, not a rejection)

**Staged row S281 and landed row S204 both locate the `errno(3)` worked example under a section
heading that does not exist in `errno(3)`.**

- **Staged package** `SOURCES.append.md`, row `S281`, locator cell:
  *"the `EXAMPLES` section of `errno(3)`, the `errno -s permission` worked example — the man-pages
  6.19 footer"*; the row's `teaches` cell carries the quote `EACCES 13 Permission denied`.
- **Landed row** `corpus/SOURCES.md` at HEAD `8936643`, row `S204` (11 cells, `docs`, tier A,
  `mined`, opened 2026-10-25): locator cell *"EXAMPLES, `errno -s permission`; Linux man-pages
  6.19"*, teaches cell *"EACCES 13 Permission denied"*.
- **Landed note** `corpus/knowledge/errno-contract-variance-r37.md` line 4 (source line):
  *"source: S204 — https://man7.org/linux/man-pages/man3/errno.3.html — `EXAMPLES`,
  `errno -s permission`, man-pages 6.19 (opened 2026-10-25)"*.
- **Landed lesson** `corpus/lessons/round-37.md` line 15 (Gate table): the S204 row's locator cell
  reads *"`EXAMPLES`, `errno -s permission`, man-pages 6.19"*.

**The quote is real; the section name is not.** `errno(3)` has **no `EXAMPLES` section**. Verified
this round, opened 2026-10-25:

1. `https://man7.org/linux/man-pages/man3/errno.3.html` (man-pages 6.19, footer
   `Linux man-pages 6.19 2026-05-28`) — section headings present: NAME, LIBRARY, SYNOPSIS,
   DESCRIPTION, NOTES, SEE ALSO, COLOPHON. Occurrences of the string `EXAMPLES`: **0**. The
   `errno -s permission` example sits inside DESCRIPTION under the subsection
   *Error numbers and names*. Located quote (20 words): *"The error numbers that correspond to each
   symbolic name vary across UNIX systems, and even across different architectures on Linux."*
2. `https://man.archlinux.org/man/errno.3` — fetched this round (HTTP 200, 30 819 bytes, sha256
   `a8c4b16faa2a08d322b8c01ed462595ace76be9b7aa2cff6e9aaef5043571e31`); headings NAME, LIBRARY,
   SYNOPSIS, DESCRIPTION, *errno*, *Error numbers and names*, *List of error names*, NOTES,
   SEE ALSO; footer `Linux man-pages 6.19` / `2026-05-28`; `EXAMPLES` occurrences: **0**.
3. `https://manpages.debian.org/trixie/manpages-dev/errno.3.en.html` and
   `https://manpages.ubuntu.com/manpages/noble/man3/errno.3.html` — same structure, no EXAMPLES.
4. Upstream roff source `https://raw.githubusercontent.com/mkerrisk/man-pages/master/man3/errno.3`
   (opened 2026-10-25): `.SH NAME`, `.SH SYNOPSIS`, `.SH DESCRIPTION` (with `.SS errno`,
   `.SS Error numbers and names`, `.SS List of error names`), `.SH NOTES`, `.SH SEE ALSO`.
   Occurrences of `EXAMPLES`: **0**. The `errno -s permission` example is inside the
   `.SS Error numbers and names` block, immediately before `.SS List of error names`.

**Why this is the right class of finding, and why it is a scope issue rather than a rejection.**

- The *teaching* is sound: the page does print `EACCES 13 Permission denied` (located quote, 4
  words) as the output of `errno -s permission`, and the row's own point — that this pairing is one
  system's observed lookup, not a portable table — is exactly right. The row must **not** be
  rejected for a false proposition.
- The *locator* is unsound, and this lane already has a named precedent for that class:
  `corpus/knowledge/source-locator-clarification-r15.md` § R15-LOCATOR withdraws a reader-dependent
  locator and requires a **stable heading path** instead, with QUALITY 21 ("Portable locators").
  `EXAMPLES` is neither a heading on the page nor in the upstream source; it names nothing.
- **Internal corroboration from the same package:** staged row `S319` locates the *same* page and
  the *same* example correctly — *"the `DESCRIPTION` section's `errno(1)` worked examples and the
  `List of error names` section"* — and staged row `S205` locates `errno(3)` as *"DESCRIPTION
  (errno); List of error names; NOTES"*. So the package itself demonstrates the correct anchor; only
  S281 is wrong. The correct locator for S204 is
  **`DESCRIPTION` → `Error numbers and names`**, the `errno -s permission` example.
- Because the anchor is in the `source:` frontmatter and the Gate table, the defect propagates
  into both the note and the lesson, and the lane's `recheck:` procedure for S204
  ("re-read errno(3), compare its footer…") cannot be executed as written by a later reader who
  looks for an EXAMPLES section and finds none.

**Verdict:** **admit with a corrected locator** — amend the locator cell of `S204` and the S204
source line of `corpus/knowledge/errno-contract-variance-r37.md` and the S204 Gate row of
`corpus/lessons/round-37.md` to name `DESCRIPTION` → `Error numbers and names` (the
`errno -s permission` example). Do **not** change the quote, the tier, the status, the recheck
cadence, or the used-by target; the proposition stands and the anchor is repairable without
touching the teaching. This is a three-cell text correction in already-landed bytes, which is
outside a read-only seat's authority — it is routed, not performed here.

## 4. Secondary observation (not the finding of record; bounded, no action taken)

The round-37 declaration (`SCORECARD.md:1936-1941`) still names the appended rows as
*"rows S204/S205/S214/S220/S279–S282/S286/S287 appended (transformed to fleet schema in scratch,
census-validated, collision-guard proven)"*. The landed registry at HEAD `8936643` instead holds
**S200–S207** for this theme, and S214/S220/S279–S282/S286/S287 do not exist in the registry at
all (max id is S207). The empty `assimilation/collisions` file is truthful against its frozen
199-row base (`reg-ids` max S199) but no longer describes the two id-spaces in play: **S200–S207**
are now claimed by both the landed registry and the staged package with **different content**
(package S200 = `mkinitcpio(8)`, landed S200 = `mount(2)`; package S204 = `btrfs-subvolume.rst`,
landed S204 = `errno(3)`; package S205 = `errno(3)` at man.archlinux.org, landed S205 =
`asm-generic/errno-base.h`). The claim "collision-guard proven" is therefore true of the frozen
base and stale against the current registry. This is a traceability/calibration defect about the
*record of what landed*, not a defect in the errno content, and it is reported for the L1 to
reconcile — the 8 renumbered rows are a legitimate transform (the package ids are simply not the
landed ids), so no row content is wrong on this account.

Sibling reports `Frontier1Errno125`, `Frontier2Errno226` and `Frontier5Errno529` independently
reached the same substantive verdict on the staged `mount-errno-contract-r26.md` (`CAP_SYS_ADMIN`
→ `EPERM` for subvolume creation conflicts with the lane's held `root-dac-correction-r13.md`
position, and the 6-class vs 12-class tables compete without supersession metadata). The lane
resolved that by **rejecting** the generic `errno-name-discrimination-r25.md` entry and admitting
rewritten `mount-errno-contract-r37.md` / `errno-contract-variance-r37.md` with a narrowed
`mount(2)` scope and no `EPERM`-for-creation claim (`corpus/lessons/round-37.md` Gate). That
resolution is consistent with the held corpus and with `PROVINCE.md`'s boundary, and I did not
re-litigate it. `Frontier8Errno832` reported "no id collision" — true against the frozen base, see
§4 above.

## 5. Adjacency and boundary conclusion

- The theme sits inside Tsukuroi's Core (host/journal/rollback-net diagnosis). No sibling lane
  declares errno semantics (0 mentions across 18 sibling `PROVINCE.md` files). No handoff is
  implied and none is requested; ADJ-01..ADJ-07 and OUT-001..OUT-010 are untouched.
- The landed notes' own boundary paragraphs are correct and are not disturbed by this finding: an
  errno class is not a cause, and an empty retained journal window is not evidence of repair
  (`corpus/knowledge/errno-contract-variance-r37.md` § Boundaries). The correction proposed in §3
  changes an anchor, not a boundary.
- No new coverage surface is claimed by this theme; both landed notes state that they deepen
  existing errno ground (`corpus/README.md:38-42, 151-153`).

## 6. Sources opened this round (2026-10-25)

| source | located quote (≤25 words) |
|---|---|
| `https://man7.org/linux/man-pages/man3/errno.3.html` (man-pages 6.19, footer 2026-05-28) | *"The error numbers that correspond to each symbolic name vary across UNIX systems, and even across different architectures on Linux."* (20 words) |
| same page, worked example | *"EACCES 13 Permission denied"* (4 words) |
| `https://raw.githubusercontent.com/mkerrisk/man-pages/master/man3/errno.3` (upstream roff) | headings `.SH NAME` / `.SH SYNOPSIS` / `.SH DESCRIPTION` / `.SS Error numbers and names` / `.SS List of error names` / `.SH NOTES` / `.SH SEE ALSO`; no `EXAMPLES` |
| `https://man.archlinux.org/man/errno.3` (HTTP 200, 30 819 B, sha256 `a8c4b16f…`) | same section set; footer `Linux man-pages 6.19` / `2026-05-28` |
| `https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno-base.h` (kernel tag v7.2) | *`#define EACCES 13 /* Permission denied */`* (5 tokens) |

Carriers that failed this round and are therefore **not** cited as opened: `https://man.archlinux.org/man/errno.3`
via the `read` tool (ECONNRESET — the same URL was successfully fetched via `curl` and is cited
above with its byte count and digest); `https://raw.githubusercontent.com/mkerrisk/man-pages/v6.19/man3/errno.3.xml`
and `.../master/man3/errno.3.xml` / `.pod` (HTTP 404 — the upstream tree now stores `man3/errno.3`
as roff, which is what I read instead); `https://gitlab.archlinux.org/archlinux/man-pages/-/raw/master/man3/errno.3.pod`
(GitLab sign-in wall).

## 7. Confidence and remaining unknowns

- **High confidence** that `errno(3)` has no `EXAMPLES` section (four independent carriers plus the
  upstream roff source, all opened this round) and that the S204 locator cell, the note's source
  line and the lesson Gate row all carry that non-existent anchor (read from committed bytes at
  `8936643`).
- **High confidence** that the quote `EACCES 13 Permission denied` is present on the page and that
  the row's proposition is sound — so the correct disposition is a locator correction, not a
  rejection.
- **Medium confidence** on the §4 traceability observation: the arithmetic is exact and read from
  committed bytes, but whether the declaration is meant to describe the *package* ids or the
  *landed* ids is a reading of L1 intent that I cannot settle from the repo.
- **Unknown / not assessed here:** whether the other 139 staged package rows will be appended in a
  later round and under which id-space (I did not audit them beyond the errno family); and whether
  any external verifier has already recorded the `EXAMPLES` defect.

## 8. Verification surfaces for the L1

1. Re-open `https://man7.org/linux/man-pages/man3/errno.3.html` and confirm the section list contains
   no `EXAMPLES`; confirm `EACCES 13 Permission denied` is present under DESCRIPTION →
   *Error numbers and names*.
2. Grep the landed corpus for the literal `EXAMPLES` and confirm exactly three sites, all being the
   S204 anchor in `corpus/SOURCES.md`, `corpus/knowledge/errno-contract-variance-r37.md` line 4, and
   `corpus/lessons/round-37.md` line 15.
3. After the three-cell correction, re-run
   `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` and confirm the
   exit status and the row count (207) are unchanged — the correction must not alter the schema, the
   id set, the tier/status cells, or the used-by targets.
4. Reconcile `SCORECARD.md:1936-1941` with the landed row ids (S200–S207) or annotate that the
   declaration names the *package* ids.

---

Report: `.ufo/waves/round-37/w1/Frontier3Errno327.md`
