VERDICT: defect-found

# R51ExecCensusSources — item F-3 (sources census and registry sanity)

## Commands run (only the item's)
1. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` (output to my scratch file, 41 lines)
   - **exit code: 0**
   - W04 lines: **40** (`grep -c W04`); the other line is `tsukuroi	ok	.../corpus/SOURCES.md`. No E-codes, no W01/W02/W03.
   - None of the W04 lines name S237 S240 S242 S243 S244 S246 S247 S248 S249 S256 (grep of S237-S259 ids in the output: no hits). Example W04s are S038/S041-S044 ... S230 (older URL-across-scopes dupes).
2. `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **256** rows (same 256 at rev 2732ee6c via `git show`; `git diff --stat 2732ee6c -- corpus/SOURCES.md` is empty, so the working tree file equals the frozen rev; HEAD seen = 6d051ef0).

Caveat: validate reads the working tree, and E11 checks used-by paths on disk. It is clean now ONLY because `corpus/lessons/round-51.md` is not yet referenced.

## Row sanity (parsed from `git show 2732ee6c:corpus/SOURCES.md`, split on `|`; used-by paths checked against `git ls-tree -r 2732ee6c`)
| id | cells | opened (ISO) | recheck | used-by all resolve at rev |
|---|---|---|---|---|
| S237 | 11 | 2026-10-26 ok | on-release ok | yes (4 paths) |
| S240 | 11 | 2026-10-26 ok | on-release ok | yes (4) |
| S242 | 11 | 2026-10-26 ok | on-release ok | yes (2) |
| S243 | 11 | 2026-10-26 ok | on-release ok | yes (2) |
| S244 | 11 | 2026-10-26 ok | on-release ok | yes (2) |
| S246 | 11 | 2026-10-27 ok | on-release ok | yes (1) |
| S247 | 11 | 2026-10-27 ok | on-release ok | yes (1) |
| S248 | 11 | 2026-10-27 ok | on-release ok | yes (1) |
| S249 | 11 | 2026-10-27 ok | 30d ok | yes (1) |
| S256 | 11 | 2026-10-28 ok | on-release ok | yes (1: corpus/lessons/round-50.md) |
All ten rows pass; no defect in any existing row.

## Defect / hazard found
`corpus/lessons/round-51.md` does NOT exist at 2732ee6c (`git cat-file -e` fails; `corpus/lessons/` ends at round-50.md). If the used-by edits below land in SOURCES.md before/without that file in the same commit, `sources-census.sh validate` raises **E11** (missing used-by) for 8 rows and exits 1. The SOURCES.md amendment and the creation of corpus/lessons/round-51.md MUST be the same commit (or lesson file first).

## Exact used-by edits (old -> new); append `, corpus/lessons/round-51.md` as the last list item (existing cell separator is ", ")
- S237: `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md`
  -> `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md, corpus/lessons/round-51.md`
- S240: `corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/lessons/round-48.md, corpus/knowledge/btrfs-scrub-grounding-r45.md`
  -> `corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/lessons/round-48.md, corpus/knowledge/btrfs-scrub-grounding-r45.md, corpus/lessons/round-51.md`
- S242: `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md`
  -> `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md, corpus/lessons/round-51.md`
- S243: `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md`
  -> `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md, corpus/lessons/round-51.md`
- S246: `corpus/knowledge/btrfs-scrub-grounding-r45.md` -> `corpus/knowledge/btrfs-scrub-grounding-r45.md, corpus/lessons/round-51.md`
- S247: `corpus/knowledge/btrfs-scrub-grounding-r45.md` -> `corpus/knowledge/btrfs-scrub-grounding-r45.md, corpus/lessons/round-51.md`
- S248: `corpus/knowledge/btrfs-scrub-grounding-r45.md` -> `corpus/knowledge/btrfs-scrub-grounding-r45.md, corpus/lessons/round-51.md`
- S256: `corpus/lessons/round-50.md` -> `corpus/lessons/round-50.md, corpus/lessons/round-51.md`
Not edited (not in the round's claim list): S244, S249. Rows must remain 11 cells (the edit only extends the final cell; the trailing ` |` is untouched). SOURCES.md was not modified by me.

## Not done
No re-run of validate after a hypothetical edit (SOURCES.md is read-only for me); the E11 claim rests on the script header (sources-census.sh:29, "E11 used-by path missing on disk") and the absence of the file at the rev, not on an observed E11 run.
Scratch /fast/scratch/hyaku/tsukuroi-r51/R51ExecCensusSources removed on exit.
