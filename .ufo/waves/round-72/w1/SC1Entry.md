# SC1Entry — C1 knowledge note draft (round 72 w1)

**Behavior.** Drafted `corpus/knowledge/modprobe-config-plane-r72.md` for the C1
claim: the modprobe configuration plane (directory precedence, cross-directory
lexicographic ordering, duplicate-filename rejection, kernel-command-line parse
into the same config object, dry-run, blacklist reach). The draft carries the
provenance trio (`source:`, `verified-at:`, `recheck:`), exactly six rule rows
MD1–MD6 in the frozen grammar (7 pipe cells each, one physical line, no pipe or
double quote inside a cell), a short "Why these six" reading, a `## Decision
table` of six observed host shapes with verdict, operator action and evidence
column, and a `## Limits` section.

**Gates (exercised, not inferred).**

| gate | result |
|---|---|
| `count-md-rows-r72.py --fixture <mirror>` on the draft + the three committed snapshots + planned registry rows S301–S303 | `MD_ROWS=6 MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0`, `met=1`, rc 0 |
| same draft and snapshots with the **real** `corpus/SOURCES.md` bytes (S301–S303 present, uncommitted; kinds `docs`/`code`) | identical `met=1`, rc 0 — the planned-row synthetic registry was not doing any work |
| quotes located verbatim per row (counter's own check) | 6/6 (`quote_located=True` each) |
| statement word floor (>= 12) | 31, 48, 34, 25, 30, 25 |
| lexical share (>= 6 tokens, >= 0.5) | 15/15, 17/17, 13/19, 11/15, 10/13, 9/13 |
| snapshot reuse (<= 2) | 2, 2, 2 |
| `--revision HEAD` on the lane (note uncommitted by design; L1 commits) | `MD_NOTE absent`, rc 128 |

The mirror is byte-identical to the lane snapshots (copied from
`.ufo/waves/round-72/before/src/`), so the only synthetic part is the registry
file, whose S301–S303 rows use the planned ids, kinds (`docs`/`code`), the exact
`SOURCES.json` URLs and anchors naming each snapshot basename.

**Touched surfaces.** Only `w1/SC1Entry/modprobe-config-plane-r72.md` and
`w1/SC1Entry/counter-run.txt`. The lane tree, registry, counter, SCORECARD and
scratch fixtures were not modified.

**Out of scope / handoff.** The registry rows S301–S303 are the L1's write and
now exist uncommitted in `corpus/SOURCES.md` with kinds `docs`/`code`, the exact
`SOURCES.json` URLs and anchors naming each snapshot basename; the frozen
counter binds against those real bytes (see gate table). The remaining gate is
the commit of `corpus/knowledge/modprobe-config-plane-r72.md`: at HEAD that path
is still absent, and the counter there reads `MD_NOTE absent` rc 128.

**Findings.**

1. MD3's message path is DBG-level (`DBG(ctx, "Ignoring duplicate config file:
   %s/%s\n", ...)` with `return -EEXIST`), so duplicate suppression is silent at
   default verbosity — recorded in `## Limits` as an operator visibility limit.
2. The man page's first and fourth SYNOPSIS entries are `@SYSCONFDIR@` and
   `@DISTCONFDIR@` placeholders; mapping them to `/etc/modprobe.d` and
   `/usr/lib/modprobe.d` rests on the host capture's path list, not on the
   snapshot text — stated explicitly in `## Limits`.
3. `/lib/modprobe.d` and `/usr/lib/modprobe.d` are one directory on this host
   (`/lib` resolves to `/usr/lib`), so two SYNOPSIS entries cover one physical
   directory; the decision table's D1 records that shape as a single walk.
4. Snapshots are kmod v34 bytes while the host runs kmod 34.2; the rows state
   v34 source behaviour and the tag-to-installed gap is not measured.
5. The decision table's D4–D6 rows are rule applications, not host
   observations: the capture is paths/modes/names only and no `install`,
   `blacklist` or `options` line was read.

**Artifacts.**

- `.ufo/waves/round-72/w1/SC1Entry/modprobe-config-plane-r72.md` (draft, sha256 `d2570b68531af50706b4fe30ca6984911c85c9e1600b1e17ee0c25a35bf2edf7`)
- `.ufo/waves/round-72/w1/SC1Entry/counter-run.txt`
- this report: `.ufo/waves/round-72/w1/SC1Entry.md`

Scratch `/fast/scratch/hyaku/tsukuroi-r72/SC1Entry` removed before yield.
