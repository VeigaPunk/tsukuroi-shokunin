VERDICT: supports

# W-B4 — frozen range-gap review

Axes: depth, C1, gaps. Revision reviewed: `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`. No actionable finding within this item. This is a review recommendation, not admission.

## (a) Mechanical equality — supports

Executed from `/fast/scratch/hyaku/tsukuroi-r52/R52RevGapBlock`, with `TMPDIR` explicitly set to that directory:

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/lint-grounding-r51.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`

Observed exit 0: `verdict: PASS`, `gap_ok: 1`, `gap_missing: []`, `gap_extra: []`, `gap_dups: []`, `gaps_computed: 98`, `lint_ok: 3`, `rows_clean: 3`, `cite_bad: 0`, `quote_bad: 0`. Thus gap_missing and gap_extra each have cardinality zero (the instrument returns lists, not numeric zeros).

The same command with `--emit-gaps` exited 0 and printed exactly the six entries at frozen `corpus/knowledge/btrfs-scrub-grounding-r45.md:367-374`.

## (b) No inside-range bloat — supports

Independently re-derived source/file/line sets without importing or calling the linter's parsing functions. Read both files with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:<path>`. Declared ranges were transcribed from frozen `corpus/SOURCES.md:246` (S237), `:249` (S240), `:251-253` (S242–S244), `:255-257` (S246–S248). Scanned only GR1–GR3 (`corpus/knowledge/btrfs-scrub-grounding-r45.md:14-324`), including Statement, Quote, and Host reading, expanding inclusive ranges and resolving abbreviated `:line` citations against their preceding filename. Source identity distinguishes kernel S242 scrub.c from userspace S237 scrub.c; host-capture references are not upstream range declarations.

For each source/file key, computed cited lines intersect declared lines, and intersected that with the block's expanded entries. Observed `inside-range bloat = {}`. In particular the two scrub.c sources were never conflated merely because their basenames match.

## (c) No outside-range holes — supports

For each row, independently subtracting declared ranges from cited lines produced:

| Row | Source/file | Outside-range lines |
|---|---|---|
| GR1 | S246 kstrtox.c | 70, 75, 77 |
| GR1 | S242 scrub.c | 1400-1401 |
| GR2 | S247 dev-replace.c | 309, 970, 1197, 1236-1242 |
| GR2 | S242 scrub.c | 3081, 3094-3139, 3250-3253 |
| GR2 | S240 ioctl.c | 3076-3078, 3080-3082, 3084-3085, 3087-3090, 3093-3095, 3109-3110, 3115, 3190 |
| GR2 | S243 sysfs.c | 78, 1288, 1302, 2015, 2019 |
| GR3 | S237 scrub.c | 421, 439, 442, 1247, 1292-1293, 1546, 1710 |

The union contains 98 distinct source/file/line keys. Independent comparison with the literal frozen block observed `missing = {}`, `extra = {}`. This reproduces the emitted block, including S242's 3094-3139 interval: GR2 explicitly cites the broad scrub.c:3094-3153 range at entry lines 111-112, not merely the isolated quoted lines. Row-local scrub.c line-number overlap does not imply source overlap.

## (d) Heading and position unchanged — supports

Executed:

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 6abef5d0 ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 -- corpus/knowledge/btrfs-scrub-grounding-r45.md`

Observed exit 0 and empty output. Consequently the complete entry, including heading `### Range gaps (R51)` at line 367 and its placement between Limits and Gate status — round 45, is unchanged from the r51 amendment. Frozen headings: Limits line 338; Range gaps line 367; following Gate status line 376.

## Residual risk and verification gaps

- `read xd://lsp` returned `No such tool`; no LSP server/device was available. This Markdown/source-range review therefore uses frozen Git bytes and explicit text-set arithmetic, not semantic references/definition/diagnostics proof.
- Named lint commands execute the lane tool pathname and request frozen input via `--revision`, exactly as assigned. I did not independently hash the mutable script against the frozen script. The independent citation-set derivation does not rely on that script.
- No source truth/behavior re-review, C1 admission counter, counted-seat binding, C2/C3 battery, resume path, runtime/rerouting, or saturation assessment was performed; those are outside W-B4. No admission marks or tracked lane files were written. No tooling installed.

Self-check: accuracy 4/5 (script-byte provenance not independently hashed); completeness 5/5 (a–d answered with observed evidence); clarity 4/5 (source-range arithmetic requires technical reading); actionability 5/5 (no correction indicated); conciseness 4/5 (full per-row table retained for auditability). Overall 4.4/5. Future improvement: retain an independently hashed command receipt when tool identity itself is in scope. These limitations do not alter the frozen block equality result.
