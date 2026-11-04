# SC2Sources — round 72 w1 (C1 registry rows, search log, leads)

## Behavior

Drafted the three C1 registry rows (S301 `man/modprobe.d.5.scd`, S302 `libkmod/libkmod-config.c`,
S303 `tools/modprobe.c`; docs/code/code, tier A, mined, opened 2026-11-03, recheck on-release,
used-by `corpus/knowledge/modprobe-config-plane-r72.md`), a `## Search log` paragraph, a
`## Leads (unopened)` closing line, and 15 line-located verbatim quotes for the MD row author.

## Conflict found (reported, not resolved)

`corpus/SOURCES.md` in the lane working tree already carried S301–S303 and two r72 prose bullets when
this draft was finished: `git diff --stat` reads `1 file changed, 6 insertions(+)`, three added `| S30x`
rows and two added `- Round-72 …` bullets at EOF. My write scope excludes the lane tree and I wrote
nothing there; the draft is a delta, not a landed artifact. Both row sets bind to the frozen counter:
`.ufo/waves/round-72/probes/SC2Sources/registry-row-check.txt` runs the counter's own
`registry_rows()` over the working tree alone and over the tree with the draft overriding by id — all
`kind`, `source-url-bound`, `anchor-basename-bound` checks PASS in both runs (`fails=0`).

Delta items recorded in `rows.md`: D1 the landed S302 anchor starts `conf_files_insert_sorted` at 915
(the function is 920–971); D2 the landed S302 anchor starts `kmod_config_new` at 1020 (it is 1014);
D3 the landed S303 `260-300` for `command_do` is correct as scoped (function 260–313, dry-run return
298–299); D4 both landed prose bullets sit at EOF inside `## Leads (unopened)` (heading line 390), and
the search-log bullet carries counts but no exclusion reasons and no stop rationale.

## Gates run

- `check.py` over the draft: 3 snapshots re-hashed against `src/SOURCES.json` (all equal), 3 rows × 11
  cells with 13 pipe-splits and no stray pipe, kind/tier/status/opened/recheck/used-by asserted, one
  snapshot named per anchor, exact map URL present in each source cell, and every quote re-located by
  token alignment in the committed bytes with its declared line range, word count, `pipe=` and `dq=`
  flags. Result `RESULT fails=0`, rc 0.
- `counter_blocks.py`: the frozen counter's `registry_rows()` over the working tree and over the draft.
  Result `COUNTER-PARSER fails=0`, rc 0.

## Touched surfaces

Wrote only `.ufo/waves/round-72/w1/SC2Sources/{rows.md,search-log.md,leads.md}`,
`.ufo/waves/round-72/w1/SC2Sources.md` and `.ufo/waves/round-72/probes/SC2Sources/registry-row-check.txt`.
No lane file, no git/jj command, no `~/.local/bin`, no fleet-root tracked file, no install.

## Out of scope (not done)

The C1 knowledge note and its MD rows (SC1Entry); the counter, batteries and declaration (frozen);
committing, applying the delta or editing `corpus/SOURCES.md` (L1 only). `libkmod/libkmod.c` was
fetched read-only to locate `default_config_paths` for the lead line; it is not a registry row and no
rule statement is drawn from it.

## Findings

- Correction (after SC1Entry's counter run): the frozen counter locates a quote with `norm(quote) in
  norm(snapshot)` — plain substring containment, not token alignment. Under that rule the
  `-n`/`--dry-run` and `-b`/`--use-blacklist` usage substrings DO locate, even though they stop
  mid-token immediately before the literal `\n"` in the C string literal (verified: the two spans are
  followed by `\n"` then the next `"\t-…`). So they are usable MD-row quotes today; what the grammar
  still forbids is a `"` in the quote cell, which is why such a quote must be trimmed at `out` rather
  than run through the escape. The token-aligned quotes in `rows.md` end on a whole token and would
  survive a later tightening; both classes pass the frozen counter.
- `modprobe.c` L626 (`flags |= KMOD_PROBE_APPLY_BLACKLIST_ALIAS_ONLY;`) contains `|=`, so an MD row
  quoting it breaks the no-pipe cell rule; the alias-only claim must be quoted from L807–809 or stated
  from the anchor range.
- All three committed snapshot digests reproduce `src/SOURCES.json` exactly (8306, 28910, 23892 bytes).

## Artifact paths

`.ufo/waves/round-72/w1/SC2Sources/rows.md`;
`.ufo/waves/round-72/w1/SC2Sources/search-log.md`;
`.ufo/waves/round-72/w1/SC2Sources/leads.md`;
`.ufo/waves/round-72/probes/SC2Sources/registry-row-check.txt`;
`.ufo/waves/round-72/w1/SC2Sources.md` (this report).
