# RevSourceS160 — wave-2 falsify review of SOURCES.md row S160 (REJECT)

Verdict: partly holds. The S160 rejection itself survives — the page is genuinely archived,
self-declared obsolete, unpinned, and every scoped teaching is already covered by the round's
tier-A rows — but one clause of the recorded reason is false on the v7.1 sources: `limit=` is
documented in btrfs-progs v7.1 `Documentation/ch-balance-filters.rst` and still parsed by
`cmds/balance.c`, so "the ENOSPC recipe does not survive v7.1 ... a `limit` filter that
btrfs-balance.rst v7.1 never documents (0 occurrences of `limit`)" misstates the situation.
All mechanical checks (hash, snapshot, quotes, cells, dates) pass. Recommendation: keep the
`rejected` status; the reason text and `corpus/knowledge/btrfs-space-r30.md:43` carry a
fixable false clause.

## Findings

1. [obs] Live bytes match the anchor and the committed snapshot. `curl -s` on
   https://archive.kernel.org/oldwiki/btrfs.wiki.kernel.org/index.php/FAQ.html today
   (2026-10-22) returned HTTP 200, 109101 bytes, sha256
   961d9b6b9913f1013bf33ea9ee27d75b141f77ec71d97a7ef8d17f5e14b925cc — identical to the
   anchor cell digest in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:166`,
   to the working-tree snapshot
   `.ufo/waves/round-30/w1/ScribeSrcReject/S160-oldwiki-faq.html`, and to the committed blob
   `0c2bcd3e14baf477c3cf17cdd99e80bdaf6ecbdc` at 29bf87fa3971df04cb96e4ad9a28805d8154ed2f
   (`git show <rev>:<path> | sha256sum` → 961d9b6b…). The row itself is byte-identical at the
   pinned revision and at lane HEAD 857126711c (`git show 29bf87fa:corpus/SOURCES.md |
   sed -n '166p'` and working-tree line 166 hash to the same sha256, and the 29bf87fa→HEAD
   diff of SOURCES.md touches S154/S155/S158 anchors only, not S160).

2. [obs] Gate quote verified verbatim on the cited line. In the live copy
   `.ufo/waves/round-30/w2/RevSourceS160/S160-faq-live-2026-10-22.html`,
   `sed -n '536p' | grep -cF 'Until at least 3.14, balance is sometimes needed to fix
   filesystem full issues'` prints 1; the quote is 13 whitespace-separated words (≤25).
   The other gate checks also print 1: line 43 ("This wiki has been archived and the
   content is no longer updated.", same line as "OBSOLETE CONTENT"), line 216
   (`btrfs balance start /mountpoint -dlimit=3`), line 892 ("This page was last modified
   on 1 June 2022, at 07:21."). Anchor line cites all confirmed on live bytes: ENOSPC
   headings at lines 187 and 188, block reserve "typically 512 MiB" at 213, `btrfs fi df`
   diagnostics at 211/214/227, kernel bug 74101 at 227, "mkfs.btrfs since v4.2" at 588.

3. [obs] Row shape conforms to CORPUS.md contract v1: 11 cells (awk -F'|' → NF=13), no `|`
   inside cells; `kind=docs`, `tier=C`; `status=rejected` (valid), `opened=2026-10-22`
   (valid ISO date, matches the fetch date), `recheck=on-release` (contract cadence token).
   `used-by` = `corpus/lessons/round-30.md, corpus/knowledge/btrfs-space-r30.md` — both
   files do cite S160 (lesson Gate row at round-30.md:19 and registry note at :24;
   knowledge note lines 1 and 43 name S160 as a rejected candidate), so the cell is honest.
   `teaches` reads `REJECTED for this round: <reason> … Flip: <condition>` — the contract
   template is `REJECTED: <reason>; flip: <condition>`; the "for this round" infix and
   capitalised "Flip:" are cosmetic deviations, not a contract violation of substance.

4. [obs] R4 clause in the reason is correctly stated. The C1 counter
   `tools/check-btrfs-space-r30.py` docstring line 25-27 and code lines 312-313 require the
   `source:`-named row's status cell to be exactly `mined`; a `rejected` row therefore
   cannot ground any Dnn row. Verified in the file.

5. [obs] Rejection reason — the parts that are true on the live page: the archive banner on
   line 43 reads "OBSOLETE CONTENT" / "This wiki has been archived and the content is no
   longer updated."; the footer (line 892) dates the content 1 June 2022 and the URL carries
   oldid=33687; the page is version-unpinned ("Until at least 3.14" line 536, kernel bug
   74101 line 227, "mkfs.btrfs since v4.2" line 588 — era references, no pin). The bare URL
   `index.php/FAQ` returns HTTP 404, 1882 bytes (live-fetched body sha256
   38bef8cb64da496d6b9f6fc74514c4f785015a7fbd235468f5dde039a77a2fbd), as the anchor states.
   `btrfs filesystem df` supersession claims are true: r31-filesystem.rst lines 22-23 call
   df a debugging helper "not suitable for quick overview" and lines 366-368 say `usage` "is
   supposed to replace" it; GlobalReserve "usually not larger than 512MiB" at lines 48-50 —
   all verified in the seat's snapshot (sha256 a0ce33f5… matches the anchor).

6. [obs] Rejection reason — the clause that is FALSE: "the partial balance it prescribes
   … uses a `limit` filter that btrfs-balance.rst v7.1 never documents (0 occurrences of
   `limit`)". `grep -c limit` on the seat's r31-balance.rst is indeed 0, but
   btrfs-balance.rst line 92 is `.. include:: ch-balance-filters.rst` — the filters live in
   the included chapter, which is itself a cited authority (S153 cites
   ch-balance-filters.rst:50-59). Fetched today from
   https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-balance-filters.rst
   (161 lines, sha256 d38bc2dc13e5a84a2d08c7c7b2c1bb42f0eb834fbf2af6d6f7cc0ecfd10a784c,
   saved at `.ufo/waves/round-30/w2/RevSourceS160/ch-balance-filters-v7.1.rst`): line 114
   documents `limit=<number>, limit=<range>` — "Process only given number of chunks, after
   all filters are applied." — i.e. exactly the FAQ's `-dlimit=3` semantics; lines 1 and 5
   describe balance limiting generally, and `balance.c` in the same seat directory
   (sha256 a21cf8a18cf8854630b37fe6986d4eb24526223454cb2a51088441768de9597c) still parses
   `limit` at lines 187-193 and echoes it at 270-273. So `-dlimit=3` remains valid,
   documented v7.1 syntax; the recipe has not been removed — the accurate defect is that it
   is the weaker tool (it limits chunk count without selecting by usage) while v7.1
   documents `-dusage=` (filters.rst:50-59 per S153) as the reclaim path. The false clause
   propagated to `corpus/knowledge/btrfs-space-r30.md:43` ("a balance `limit` filter that
   the v7.1 documentation does not describe").

7. [obs/inf] Would admitting S160 add anything tier-A rows lack? No. Every element of its
   scoped `scope` cell is already held: allocated-but-unused-chunk reclaim → S153
   (usage filter, ENOSPC advice); the 512 MiB "block reserve" threshold → S152
   (GlobalReserve ≤512MiB) plus S156 (block-rsv.c cap in v7.2 kernel code); free-work-space
   test → S153 (btrfs-balance.rst:104-114); df diagnosis → S152 (usage replaces df). The only
   unique content is historical (pre-3.14 behaviour, bug 74101) — commentary-grade, which is
   what tier C is for ("lead only — never sole support"). Admitting it as mined would add a
   self-declared-obsolete, unpinned source under claims that already carry primary
   documentation and kernel code. The rejection costs the corpus nothing.

8. [inf] Flip condition is sound: requiring an explicitly historical claim grounded in a
   version-pinned btrfs-progs/kernel file of that era, with this page as commentary only,
   is the correct admission bar under contract v1 (tier C can never be sole support) and is
   a bar the page can never clear alone — appropriate for an archived wiki. Minor weakness:
   the flip's commentator role arguably applies to S160 already (it is being cited as
   rejected-candidate commentary in btrfs-space-r30.md), so the condition is satisfiable in
   principle but unlikely ever to justify re-opening.

9. [obs] Minor anchor inaccuracy, not load-bearing: "the live host btrfs.wiki.kernel.org now
   answers 301 to that archived URL" — true for `/index.php/FAQ` (301 →
   archive.kernel.org/oldwiki/btrfs.wiki.kernel.org/index.php/FAQ.html), but
   `/index.php/FAQ.html` 301-redirects to `…/index.php/FAQ.html.html`, a mangled target; the
   sentence is accurate only under the bare-URL reading.

10. [unk] The seat's `balance.c` is not version-labelled in the gate notes (presumed
    btrfs-progs v7.1 `cmds/balance.c`); finding 6 does not depend on it — the
    ch-balance-filters.rst v7.1 bytes alone establish that `limit=` is documented.

Verdict on the attack questions: the reject decision holds (agree — status should stay
`rejected`); the stated reason is mostly true on the live page but contains one false clause
(disagree with that clause — `limit` is documented in v7.1, in the included filters chapter
the row's own sibling source S153 cites); the flip condition is sound; admission would have
added nothing the tier-A rows lack.

Scope: read=corpus/SOURCES.md S160 row and neighbours, CORPUS.md contract v1 section,
w1/ScribeSrcReject seat files (S160-gate.md, S160-row.md, S160-oldwiki-faq.html,
r31-balance.rst, r31-filesystem.rst, balance.c), tools/check-btrfs-space-r30.py R4 lines,
SCORECARD.md round-30 declaration lines, corpus/knowledge/btrfs-space-r30.md and
corpus/lessons/round-30.md S160 citations, live FAQ page and redirect probes; wrote=
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS160.md,
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS160/S160-faq-live-2026-10-22.html
(sha256 961d9b6b9913f1013bf33ea9ee27d75b141f77ec71d97a7ef8d17f5e14b925cc),
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS160/S160-faq-bare-2026-10-22.bin
(sha256 38bef8cb64da496d6b9f6fc74514c4f785015a7fbd235468f5dde039a77a2fbd),
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS160/ch-balance-filters-v7.1.rst
(sha256 d38bc2dc13e5a84a2d08c7c7b2c1bb42f0eb834fbf2af6d6f7cc0ecfd10a784c);
executed=curl (4 GET/HEAD probes), sha256sum, git read-only (rev-parse, log, status,
ls-tree, show, diff), grep/sed/awk line checks — all read-only against the lane repo
Model: devin/swe-2
Installs: none
