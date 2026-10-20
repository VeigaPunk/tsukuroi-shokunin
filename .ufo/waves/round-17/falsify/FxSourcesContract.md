# FxSourcesContract — SOURCES contract, rows S051–S057 + round-17 Search log

**Verdict: SURVIVES** — two minor findings, no contract failure.

## Evidence [obs unless marked]
- Census (canonical CORPUS.md § SOURCES.md checks, lane root): rows S051–S057 NF=13 → 0 malformed; kind/tier/status enums → 0 violations; no community-A; all mined, every used-by path exists (`test -e`). Duplicate ids: none; S051–S057 follow S050 sequentially.
- `opened` 2026-10-20 ISO, `recheck: on-release` cadence, all 7 rows. Anchors non-bare: S053 names CHANGES sections + release dates; S057 names MR description + merge commit `00392d94`. own-work rows cite repo capture paths.
- Gate (Rule 1): lessons/round-17.md Gate table has path/URL + accessed date + ≤25-word quote per row; quotes verified verbatim: boot-chain-capture.txt:174-175 "VERSION 42.2" / "init /sysroot refs 7 ; /new_root refs 0"; fresh-capture.txt:16; overlay-emulation.txt:8,46; supplement-capture.txt:113. ✓
- Rule 2 append-only: `git diff dd15c183..HEAD -- corpus/SOURCES.md` → only `+S058` row; S051–S057 byte-identical since wave 1; absent at baseline 6923fe0b (grep count 0). No mutable-field change to S051–S057, so nothing unlogged. S054 correction correctly done as new row S058 opening `supersedes S054 —`.
- used-by citation truth: corpus/knowledge/boot-chain-r17.md cites S051–S057; initramfs-v42-sysroot-recovery.md cites S055.
- Search log (SOURCES.md:104): question, where, date, identified/screened/included/excluded 5/5/5/0, stop rationale, mutable changes — all present.

## Findings (minor)
1. used-by over-claim: S051/S055/S056 list `corpus/knowledge/boot-chain-r17.json`, but that JSON contains zero `S05x` citations — it references captures by path only (`.captures.*`). mined stays valid via the .md; the cell overstates. [inf: fixing requires logged old→new]
2. Search log counts S057 in "included 5" but the paragraph's "Opened…" list never states the MR was opened/where; it appears only in the findings sentence (Gate table covers it separately).

## Not verified
- External URL contents (S053/S057 remote text) not re-fetched this round; relied on gate quotes and prior seats.
[inf] = inference.

Scope: executed=git-rev-parse, git-log, git-diff, git-show, sed, awk, grep, python3-json-inspect, test-e
