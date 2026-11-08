# ScoutSources — round-96 w1 — the S390/S391 SOURCES row, the S389 re-open, the Sphinx caveat

Seat: SCOUT (leaf member; no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
@ `a814f24dc31270bca4e8999ac3cd907ecd72f100` (HEAD detached; `refs/heads/master` at the same commit).
Axis: **freshness**. Date: 2026-11-08. Scratch: `/fast/scratch/hyaku/tsukuroi-r96/ScoutSources/`
(created before the first command, removed on exit).
Files written by this seat: **only** `.ufo/waves/round-96/w1/ScoutSources/` (report + `receipts/`
+ `pins/`) and this wave-level file. No lane file was edited; no git/jj mutation was run in the
lane (`git rev-parse`, `git log`, `git ls-tree`, `git cat-file`, `git diff`, `git status`,
`git archive` only). No tool was installed, upgraded or removed — every command used a
preinstalled `curl`, `python3`, `sha256sum`, `wc`, `cmp`, `git`, `tar`. **No installs, no
updates, no channel; no pacman transaction.**

**State note.** The registry at HEAD **already carries an S390 row** (landed by the L1 in commit
`59cbfe2f`, alongside `corpus/knowledge/limine-bound-per-component-r96.md` and
`corpus/lessons/round-96.md`). This seat was dispatched to *draft* the S390 row; by the time it
ran the row existed. So the report verifies the landed row against the source byte by byte,
drafts the corrected row the contract requires under it (CORPUS.md rule 2 — a correction is a
new row whose `teaches` opens `supersedes S0NN —`), and gates both shapes.

Full report with every command and its raw output: `.ufo/waves/round-96/w1/ScoutSources/report.md`.
Receipts: `.ufo/waves/round-96/w1/ScoutSources/receipts/` (`pin-table.tsv`,
`receipt-01-sys-int-info.txt`, `receipt-02-stdtypes-reopen.txt`, `receipt-03-s390-row-draft.txt`,
`receipt-04-findings.txt`, `receipt-05-lesson-gate-draft.txt`, `gate-*.out`) and
`pins/python-3-sys.html`, `pins/python-3-stdtypes.html`.

## Measured

| item | measured |
|---|---|
| `https://docs.python.org/3/library/sys.html#sys.int_info.default_max_str_digits` | HTTP **200**, **280632** bytes, sha256 `a7e005875e4152bcccaf44b9a834c123cc69bf7b66b3b8398aef91cffe77dd0e`; the `/3.15/` copy is byte-identical |
| the requested quote (12 words, ≤25) | verbatim; **not** byte-contiguous in the raw HTML (a reference link and a newline split it) — raw text runs at **157851** and **158097**, rendered-contiguous at **42794**; the anchor element `id="sys.int_info.default_max_str_digits"` at **157495**, the `id` value at **157529**, the visible name at **157698** |
| tier-A grounding | the attribute's own upstream definition in the CPython reference docs; the page states **no 4300** (0 occurrences), **no 640** (0), **no Limine** (0), no "as provided by" (0) — the 4300 figure is S389's page |
| S389 re-open (`…/stdtypes.html#integer-string-conversion-length-limitation`) | HTTP **200**, **815447** bytes, sha256 `6bf2ce2b…`, **byte-identical to the r95 pin**; the 4300-digit sentence at **785297** and all four of the row's offsets (780197 / 780256 / 785297 / 782228) re-resolve |
| Sphinx caveat (r95 Gate: `corpus/lessons/round-95.md:38`, `corpus/lessons/round-95-verifier-spotcheck.md` §3) | the pin's sha256 is Sphinx-stamp dependent ("Last updated on Nov 08, 2026 (07:53 UTC)" is a moving line); re-verify by title/version and the sentence offsets, never the digest alone — both pins reproduce the r95 digests today because the build has not been re-stamped since, which is a property of this build, not a guarantee |
| drafted row | 11 columns (NF 13), **no `|` in any cell**, teaches 12 words, opened 2026-11-08, recheck 180d, used-by `corpus/knowledge/limine-bound-per-component-r96.md` |
| census gate | `scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` → **exit 0, 0 E findings**, 58 W (the lane's pre-existing 57 W04 + 1 W01 baseline); negative controls fire **E03** (duplicate id) and **E04** (duplicate url within the same scope), so the gate discriminates |

## Findings against the landed S390 row

- **F1 — the anchor byte does not resolve to the quote.** The row cites "byte 157653"; on that
  exact pin (sha256 `a7e00587…`) byte 157653 is a **space inside `<span class="sig-name descname">`**
  (tag starts 157648) — not the attribute id, not the visible name, not any part of the sentence.
  The same wrong byte is repeated in `corpus/lessons/round-96.md`'s Gate table.
- **F2 — the source URL is the rolling `/3/` alias, not version-pinned.** The lane's own precedent
  is `S385` (supersedes `S377`) and the sibling `S389` uses the pinned form; measured today the two
  forms are byte-identical, so this is a drift exposure, not a current factual error.
- **F3 — the scope cell states a design consequence the source does not state** ("the cap a parser
  that hands a component to int() must bound itself"); the page says only what the default value is.
- **F4 — scope limit, not a defect:** the page states no 4300, no 640 and no Limine behaviour; the
  landed `teaches` cell correctly stops at the quoted sentence.

What is **correct** in the landed row (verified): the quote is verbatim and 12 words; the sha256
prefix reproduces this seat's independent fetch exactly; the `used-by` path exists at HEAD
(`git ls-tree` → blob `061ddb94…`), so `mined` is not dangling; the row is census-clean at HEAD
(exit 0, 0 E).

## Asked of the L1

1. Land **Draft B** (id **S391**, `teaches` opened `supersedes S390 —`) after S390 — the
   correction CORPUS.md rule 2 requires; gated clean at exit 0. Draft A (id S390, `queued`) is
   also clean but cannot take that id at the landed tree (E03).
2. Correct the byte in `corpus/lessons/round-96.md`'s Gate table for S390, or record the S391
   supersession there with the offsets 157851 / 158097 (draft lines in
   `receipts/receipt-05-lesson-gate-draft.txt`).
3. Version-pin S390's URL (F2), or let the superseding row carry the pinned form (Draft B does).

{"seat":"ScoutSources","verdict":"findings","notes":"sys.html pinned (200, 280632 B, sha256 a7e00587...); the 12-word quote is verbatim but split by the reference link, so it resolves at raw text runs 157851 and 158097 (rendered-contiguous 42794), while the landed S390 row's cited byte 157653 is markup whitespace (F1). Page states no 4300/640/Limine (F4). S389 re-opened: 200, 815447 B, sha256 6bf2ce2b..., byte-identical to the r95 pin, 4300 sentence at 785297; Sphinx 'Last updated' caveat recorded. Row drafted (NF 13, no '|' in any cell) as S390 and, per CORPUS.md rule 2, as S391 'supersedes S390'. Census gate on the appended mirror: exit 0, 0 E findings, 58 W baseline; negative controls fire E03 (duplicate id) and E04 (duplicate url within the same scope). Also filed: F2 rolling /3/ URL not version-pinned, F3 scope states a parser-cap consequence the source does not state."}
