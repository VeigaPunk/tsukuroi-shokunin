# RevSourcesContract — SOURCES contract (R17)

Frozen v1: `/home/vgpnk/Projects/shokunin/CORPUS.md:66-68` (lane-relative `../CORPUS.md`); `corpus/SOURCES.md:1-6` has only title + `## Registry` (no rules/tier block).

## Columns (11; pipe NF=13) — `../CORPUS.md:85`
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`

- id `S`+3 digits, next unused, never reused; no `|` in any cell (89). kind `spec|docs|paper|code|tool|dataset|talk|book|community|own-work` (91-92).
- tier `A|B|C`, scoped to `scope`, never global; community never A; C never sole support (93-97). anchor: exact heading/line + revision, never a homepage (99-100).
- teaches: one grounded benefit; rejected = `REJECTED: <reason>; flip: <what changes the verdict>` (101-102).
- status `queued|mined|rejected`; mined = ≥1 used-by path; `watch` invalid (103-104). opened ISO date; recheck ISO date or cadence (`90d`, `180d`, `on-release`) (105-106). used-by repo-relative paths or `—` (107-108).
- recheck divergence [obs]: `corpus/QUALITY.md:12` allows `<N>d`|`on-release`; census E09 allows any `NNd` or symbolic cadence.

## Rejection rules
1. No row without opening it that round; exact anchor (112-114). 2. Rejected rows kept: status rejected, REJECTED/flip, used-by `—` (W02). 3. C never sole support; community never A (E10). 4. Correction = new row whose teaches opens `supersedes S0NN —`, never an edit. 5. Append-only: only status/recheck/used-by change in place, each old→new in the round lesson. 6. Search log: query, date, identified/screened/included/excluded counts, exclusion reasons, stop rationale; negative claims carry sweeps (126-128). 7. No credentials, session URLs, `op://` (129). Machine: E01–E12, W01–W04 (`../scripts/sources-census.sh:19-33`).

## Gate must record
- New row: URL (repo path/command if own-work), access date, ≤25-word quote + its location grounding teaches (112-115). No quote column exists, so only the Gate satisfies this.
- Changed row: field old→new (116-117); re-opening does not rewrite `opened`.

## Findings
- **HIGH** `corpus/lessons/round-17.md` absent at review; `.ufo/waves/round-17/build/drafts/lesson-r17.md:27` has one S051–S054 row with `<L1 fills>`, no per-row URL/date/quote — rule 1 unmet for S051–S054; `corpus/knowledge/boot-chain-r17.md:156-157` already cites that Gate.
- **HIGH** S015/S016/S021/S022 old→new only at `SOURCES.md:100`, not the round lesson.
- **MED** `SOURCES.md:100` counts 4 included while 6 rows were added (4 external + S051/S052).
- **MED** `corpus/QUALITY.md:11` points to SOURCES.md for tier definitions; none exist there.
- **PASS** [obs] 54 rows S001–S054 contiguous; S051–S054 11 columns; four changed rows differ from 6923fe0 only in used-by.

Deviation: no EXEC-AUTHORIZED; commands were read-only repo text/git reads, no host probes, scripts or writes.

Scope: executed=git status, git diff, git show, grep, ls, sed -n
