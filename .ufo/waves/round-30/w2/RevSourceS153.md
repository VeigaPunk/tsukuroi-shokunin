# S153 re-open review — wave 2 (falsify)

Verdict: partly disagree — the row's digest, quote, shape and admit cells all hold, but
`used-by` names `corpus/lessons/round-30.md`, a file that does not exist at the
evaluated revision 29bf87fa3971df04cb96e4ad9a28805d8154ed2f.

## Findings

1. **Dangling `used-by` path at the revision under review (defect).** The S153
   `used-by` cell lists `corpus/knowledge/btrfs-space-r30.json`,
   `corpus/knowledge/btrfs-space-r30.md`, `SKILL.md` and
   `corpus/lessons/round-30.md`. At tip `29bf87f`, `git cat-file -e` on
   `corpus/lessons/round-30.md` fails and `git ls-tree corpus/lessons/` contains no
   round-30 lesson; the file first enters history at `7165f11`, after the tip.
   The row was committed at `a3f19372` already naming this not-yet-committed
   lesson — a forward reference. The cell definition
   (`/home/vgpnk/Projects/shokunin/CORPUS.md:107-108`) makes used-by the paths that
   cite the row, and the contract's own census
   (`/home/vgpnk/Projects/shokunin/CORPUS.md:147`) treats missing used-by paths of
   `mined` rows as defects. Severity is low: `mined` still holds via the three
   real citing paths, the lesson exists at HEAD (`8571267`) and does carry the
   S153 gate row (`corpus/lessons/round-30.md:12`), and the row itself was never
   edited in place (identical at `a3f19372` and `29bf87f`).

2. **Live bytes re-fetch: both digests match [obs].** Fetched today (2026-10-22)
   with plain `curl -sL` to raw.githubusercontent.com; no 429, no fallback needed.
   Saved unchanged under
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS153/`.
   `live-ch-balance-filters.rst` sha256
   `d38bc2dc13e5a84a2d08c7c7b2c1bb42f0eb834fbf2af6d6f7cc0ecfd10a784c` (161 lines,
   7009 bytes) and `live-btrfs-balance.rst` sha256
   `ca245fbf145166ec24c8a84864ffd44fbef98ca66551fdf50cfb8be552d22cea` (274 lines,
   10439 bytes) — exactly the digests and sizes claimed in the anchor cell, and
   identical to the committed snapshots (re-hash of `git show
   29bf87f:.ufo/waves/round-30/w1/ScribeSrcBalance/S153-*.rst` matches).

3. **Gate quote verified verbatim [obs].** Quote `"Balances only block groups
   with usage under the given percentage. The"` (11 words, ≤ 25):
   `sed -n '51p' S153-balance-filters.rst | grep -cF '<quote>'` → 1, in
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcBalance/S153-gate.md:3`.
   Note [obs]: the gate cites the included chapter URL
   (`ch-balance-filters.rst`) while the row's `source` URL is the page URL
   (`btrfs-balance.rst`); coherent, since the row title discloses the included
   chapter and the anchor records both files' digests.

4. **Row shape and lifecycle cells valid [obs].** Row at SOURCES.md line 159 at
   tip: awk `-F'|'` gives NF=13 → exactly 11 cells. `status` = `mined` (valid;
   ≥1 citing path exists — three do). `opened` = `2026-10-22` (ISO date,
   consistent with commit timestamps). `recheck` = `on-release` (contract
   cadence). No `|` inside cells.

5. **Anchor and admit cells accurate [obs].** `kind=docs`, `tier=A` correct:
   upstream btrfs-progs documentation, and the scope is pinned to "the installed
   btrfs-progs 7.1" — `btrfs --version` on this host prints `btrfs-progs v7.1`.
   `git ls-remote --tags https://github.com/kdave/btrfs-progs` gives
   `v7.1^{} = 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`, exactly the peeled
   commit claimed. Every cited line range verified against the snapshot:
   filters.rst 29-31 (unallocated space before profile changes), 50-59
   (`usage=<percent>` definition, `usage=0` and ENOSPC advice), balance.rst 92
   (`.. include:: ch-balance-filters.rst`), 97-102 (work space vs ENOSPC),
   104-116 (`size - used = free work space`), 118-120 (`usage=0` needs no
   workspace), 124-126 (interrupted balance leaves partially filled groups).
   `teaches` is grounded in those lines; the json/mD/SKILL.md cites carry the
   same claims (D03 row of `btrfs-space-r30.json` quotes line 51;
   `btrfs-space-r30.md:27` and `SKILL.md:2608` cite it).

6. **Residual risk [inf].** The one-cell defect is a bookkeeping forward
   reference, not a fabricated citation: all claims trace to real bytes. Nothing
   else in the row failed. The round-30 lesson now on disk is modified in the
   working tree (` M` in git status) — expected wave-2 churn, not part of this
   check.

Scope: read=SOURCES.md row S153 at 29bf87f, CORPUS.md contract v1, w1/ScribeSrcBalance gate+snapshots, tip blobs of the four used-by paths; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS153/{live-btrfs-balance.rst,live-ch-balance-filters.rst,RevSourceS153.md}, /fast/scratch/hyaku/tsukuroi-r30/RevSourceS153/SOURCES-tip.md; executed=curl (2 fetches), sha256sum, sed/grep/awk verification, read-only git (show, ls-tree, cat-file -e, ls-remote, log, status)
Model: not exposed
Installs: none
