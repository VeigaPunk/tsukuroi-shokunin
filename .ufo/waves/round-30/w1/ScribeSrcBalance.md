# ScribeSrcBalance — S153 source seat (round 30, wave 1)

Verdict: done — S153 opened, saved and verified; one registry row, one Gate row and one D03 candidate row drafted; no conflicts with the canonical Rust judge encountered.

1. The named file exists at tag v7.1, but it does not hold the `usage` filter text. `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-balance.rst` returned HTTP 200, 10439 bytes, but at its line 92 it contains `.. include:: ch-balance-filters.rst`; the `usage=<percent>, usage=<range>` entry is in that included chapter. I saved both files unchanged, as the assignment asks for the file that holds the filter text. [obs] Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcBalance/S153-balance.rst:92` and `S153-balance-filters.rst:50`.

2. Snapshots and hashes. [obs]
   - `.ufo/waves/round-30/w1/ScribeSrcBalance/S153-balance.rst` — 274 lines, 10439 bytes, `sha256 ca245fbf145166ec24c8a84864ffd44fbef98ca66551fdf50cfb8be552d22cea`.
   - `.ufo/waves/round-30/w1/ScribeSrcBalance/S153-balance-filters.rst` — 161 lines, 7009 bytes, `sha256 d38bc2dc13e5a84a2d08c7c7b2c1bb42f0eb834fbf2af6d6f7cc0ecfd10a784c`.
   - Second fetch of the filters chapter returned the identical hash, so the snapshot is reproducible now.
   - Tag peel verified read-only: `git ls-remote https://github.com/kdave/btrfs-progs 'refs/tags/v7.1*'` printed `0a919c7d6e389c07920675b7fad3f793b92aa78b refs/tags/v7.1` and `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b refs/tags/v7.1^{}` (exit 0). No alternate endpoint (cgit, jsDelivr) was needed; raw.githubusercontent.com returned 200 on both fetches.

3. Quotes verified with the exact required form, each printing 1. [obs] Commands run from the seat directory, outputs pasted:
   - `sed -n '51p' S153-balance-filters.rst | grep -cF 'Balances only block groups with usage under the given percentage. The'` → `1`
   - `sed -n '54p' S153-balance-filters.rst | grep -cF 'in case balance is returning ENOSPC and your filesystem is not too full.'` → `1`
   - `sed -n '29p' S153-balance-filters.rst | grep -cF 'Before changing profiles, make sure there is enough unallocated space on'` → `1`
   - `sed -n '99p' S153-balance.rst | grep -cF 'For that it needs the work space, otherwise it fails for ENOSPC reasons.'` → `1`
   - `sed -n '118p' S153-balance.rst | grep -cF 'An example of a filter that does not require workspace is *usage=0*. This will'` → `1`

4. Draft (a) `S153-row.md`: one registry row, mechanically checked to parse as 11 columns with leading and trailing pipes, status `mined`, opened `2026-10-22`, recheck `on-release`, used-by exactly the four required paths, and the anchor cell contains the literal `sha256 d38bc2dc13e5a84a2d08c7c7b2c1bb42f0eb834fbf2af6d6f7cc0ecfd10a784c`. [obs] Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcBalance/S153-row.md:1`; column check printed `registry columns: 11 leading/trailing ok: True` and `has required sha literal: True`. No cell contains an unescaped pipe, so no `\|` escape was needed. Tier A, kind `docs`, matching rows S129 and S139.

5. Draft (b) `S153-gate.md`: header plus one Gate row in the round-29 lesson shape (`corpus/lessons/round-29.md:9`), six columns, quote 11 words on a single line, location `.ufo/waves/round-30/w1/ScribeSrcBalance/S153-balance-filters.rst` line 51 with sha256, decision `admit, mined, tier A`. [obs] Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcBalance/S153-gate.md:3`; mechanical check printed `gate cols: 6`, `gate quote words: 11`, `grep= 1`.

6. Draft (c) `S153-rows.json`: a one-element JSON list with `id` `D03`, statement 34 words, source `S153`, snapshot the filters file, line 51, quote 69 characters containing the frozen token `usage` (case-insensitive). Re-parsed with Python and re-quoted against the saved file: `grep= 1`. [obs] Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcBalance/S153-rows.json:3`. I kept one canonical row because the corpus list must hold one row per id; the three verified alternates are recorded in `S153-notes.md` and marked not for direct insertion. [inf]

7. What the documentation says about balance needing free space. [obs] All line numbers in `S153-balance.rst`:
   - 97-99: balance usually creates a new block group and moves the old data there before the old block group can be removed, and "For that it needs the work space, otherwise it fails for ENOSPC reasons."
   - 100-102: this is not the same ENOSPC as exhausted free space; it is space at the block-group level, so a filesystem with free bytes can still fail a balance.
   - 104-116: free work space is `size - used` per device from `btrfs filesystem show`; worked example 53.90GiB - 51.90GiB = 2.00GiB.
   - 118-120: `usage=0` needs no workspace; it scans unused block groups and reclaims the space, after which other filters may become possible.
   - 124-126: striping conversions need work space on each device, and an interrupted balance may leave partially filled block groups that consume it.

8. What it says about a nearly full filesystem. [obs] `S153-balance-filters.rst:52-54`: the value 0 cleans up completely unused block groups, "should not require any new work space allocated", and "You may want to use *usage=0* in case balance is returning ENOSPC and your filesystem is not too full." The advice is scoped to a filesystem that is not too full; neither file gives a filter or procedure for one that already is too full. Neither file uses the word `unallocated` for the reclaimed space — it says "reclaim the space" (line 119) and the old block group "can be removed" (line 98) — so the D03 statement is worded inside that language and does not claim a literal return to `unallocated`. [inf] This is the one place where a judge reading D03 strictly could push back: the frozen token `usage` is present and the quote is exact, but "return to unallocated space" is the operator's framing, not the document's phrase.

9. Out of scope and not done: no product code, judge, battery, counter or `SKILL.md` line touched; no `[R30-D03]` decision-table line drafted (that belongs to the SKILL.md seat); no corpus knowledge row written; no gate tool run against these drafts. Nothing was committed, and no git or jj write command ran in the lane or fleet repo; the only git invocation was the read-only `ls-remote` above, run from `/tmp` with `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` unset. [obs]

Artifact paths (all under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`): `.ufo/waves/round-30/w1/ScribeSrcBalance/S153-balance.rst`, `S153-balance-filters.rst`, `S153-row.md`, `S153-gate.md`, `S153-rows.json`, `S153-notes.md`.

Scope: read=SCORECARD.md round-30 section via context, corpus/SOURCES.md rows S129/S139/S148-S151 and header, corpus/lessons/round-29.md Gate table, fetched btrfs-balance.rst and ch-balance-filters.rst at v7.1; wrote=.ufo/waves/round-30/w1/ScribeSrcBalance/S153-balance.rst, .ufo/waves/round-30/w1/ScribeSrcBalance/S153-balance-filters.rst, .ufo/waves/round-30/w1/ScribeSrcBalance/S153-row.md, .ufo/waves/round-30/w1/ScribeSrcBalance/S153-gate.md, .ufo/waves/round-30/w1/ScribeSrcBalance/S153-rows.json, .ufo/waves/round-30/w1/ScribeSrcBalance/S153-notes.md, .ufo/waves/round-30/w1/ScribeSrcBalance.md; executed=curl -sL (two fetches, HTTP 200), sha256sum, wc -l, grep -n, awk, sed -n | grep -cF (five quote checks, all 1), git ls-remote (read-only, tag peel), python3 JSON/column validation
Model: not exposed
Installs: none
