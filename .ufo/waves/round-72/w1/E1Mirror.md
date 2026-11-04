# E1Mirror — independent mirror harness for the frozen C1 counter (round 72, wave w1)

Axes: (1) counter fidelity — the frozen counter must accept an independently authored six-row
fixture; (2) reader independence — a second implementation re-derives the row contract without
importing the counter; (3) disagreement map — every clause only the frozen counter enforces is
named with a witness mutant.

## Inputs (read-only)

- Declaration commit `6b4267623b3d6cf88b32c2df8daaad1a5bc9f19e`; predicates used as frozen.
- Counter `tools/count-md-rows-r72.py` sha256
  `d615c653f32a29af3a4355d882041b8543ff56882b3225f7e3eedf173d8706a6`, identical before and
  after all runs (never modified).
- Snapshots copied byte-for-byte from `.ufo/waves/round-72/before/src`: `modprobe.d.5.scd`
  `aa1a869e…98ee46e`, `libkmod-config.c` `ae520a07…7ceb11`, `modprobe.c` `1e8e3526…71bf3f`
  (match `SHA256SUMS` and `src/SOURCES.json`).
- Scratch: `S=/fast/scratch/hyaku/tsukuroi-r72/E1Mirror`, fixture at `$S/mirror`; removed before yield.

## Fixture (authored here, not copied from `before/control/battery.py`)

- `build-mirror.py` writes `$S/mirror/.ufo/waves/round-72/before/src/{three snapshots,SOURCES.json}`,
  `corpus/SOURCES.md` (S301 docs / S302 code / S303 code, map URL in source cell, basename in
  anchor cell) and `corpus/knowledge/modprobe-config-plane-r72.md` (six rows, two per source).
- Quotes are verbatim snapshot text (15, 23, 5, 1, 7, 5 words). Two first drafts failed
  grounding (MD5 `4/7`, MD6 `2/9`); reworded from snapshot-native tokens to `8/8` and `12/15`
  before the control run.

## Counter run (exact output in `counter-run.txt`)

```
$ python3 …/tools/count-md-rows-r72.py --fixture $S/mirror
MD_ROW ok MD1 source=S301 snapshot=modprobe.d.5.scd
MD_ROW ok MD2 source=S301 snapshot=modprobe.d.5.scd
MD_ROW ok MD3 source=S302 snapshot=libkmod-config.c
MD_ROW ok MD4 source=S302 snapshot=libkmod-config.c
MD_ROW ok MD5 source=S303 snapshot=modprobe.c
MD_ROW ok MD6 source=S303 snapshot=modprobe.c
MD_ROWS=6 MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0
MD_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1
rc=0
```

## Independent reader (`reader.py`, sha256 `c1fa45b4…d1a75f`)

Own quote-aware cell splitter; imports only hashlib/json/re/sys/pathlib. Checks: row count == 6,
id contiguity from 1, quote located verbatim (whitespace-normalized) in the named snapshot,
digest == sha256 of the snapshot file, source id present in `corpus/SOURCES.md`, that row's
source cell contains the `SOURCES.json` map URL, and its anchor cell contains the basename.

- Control: `READER rows=6 ok=6 red=0 contiguous=1`, rc 0.
- Foreign-quote fixture (MD1 quote replaced by `Ignoring duplicate config file: %s/%s` from
  `libkmod-config.c` while MD1 cites `modprobe.d.5.scd`): `READER rows=6 ok=5 red=1`,
  `MD1 quote-absent`, rc 1. Counter on the same tree: `MD_ROW fail MD1 quote-absent`, met=0.

## Verdict matrix (15 fixtures; exact stdout in `reader-runs.txt`)

| case | counter | reader | class |
|---|---|---|---|
| control | met=1 rc0 | 6/6 rc0 | agree green |
| quote-foreign | MD1 quote-absent, met=0 | MD1 red, 5/6 | agree red |
| short-statement | MD1 statement-words=7 statement-grounding=5/5 | 6/6 | **disagree** |
| ungrounded-long | MD2 statement-grounding=5/10 | 6/6 | **disagree** |
| ownwork-kind | MD1+MD2 source-kind=own-work | 6/6 | **disagree** |
| map-digest | MD5+MD6 map-digest | 6/6 | **disagree** |
| reuse-three | global snapshot-reuse modprobe.d.5.scd=3, met=0 | 6/6 | **disagree (global)** |
| malformed-row | global malformed-row `MD7`, met=0 | 6/6 (info malformed-lines=1) | **disagree (global)** |
| long-quote | MD1 quote-words=30 | 6/6 | **disagree** |
| spacing (double space in a cell) | MD1 malformed-row, rows=5, ids-not-contiguous | 6/6 | **disagree** |
| anchor-missing | MD3+MD4 anchor-not-bound | MD3+MD4 red | agree red |
| source-url-missing | MD5+MD6 source-not-bound | MD5+MD6 source-url-not-bound | agree red |
| digest-swap | MD5 digest-mismatch map-digest | MD5 digest-mismatch | agree red |
| quote-pipe | MD3 malformed-row, rows=5, ids-not-contiguous | MD3 quote-absent, 5/6 | agree red, different mechanism |
| duplicate-id | one MD1 duplicate-id, ids-not-contiguous | per-row 6/6, global ids-not-contiguous rc1 | agree red, different granularity |

No fixture produced reader-red / counter-green: the reader never reds a row the counter accepts.

## Row-by-row disagreements (8 fixtures, counter red, reader green)

- `short-statement` MD1 (statement floor/grounding), `ungrounded-long` MD2 (grounding only),
  `ownwork-kind` MD1+MD2 (kind), `map-digest` MD5+MD6 (map digest), `long-quote` MD1 (quote
  word cap), `spacing` MD1 (exact cell grammar: counter drops the row as malformed, reader
  parses it because it strips cells).
- Global-only: `reuse-three` (all rows ok, reuse cap trips), `malformed-row` (all rows ok,
  appended MD-shaped stub is malformed).

## Counter clauses the reader cannot check (witness)

1. statement >= 12 words — `short-statement` (`MD1 statement-words=7`).
2. statement grounding: >= 6 distinct shared non-stop tokens (len >= 4) and shared/total >= 0.5
   — `short-statement` (`5/5`), `ungrounded-long` (`5/10`).
3. registry kind in the source-kind set and never `own-work` — `ownwork-kind`.
4. note digest == `SOURCES.json` map digest for that snapshot — `map-digest`.
5. quote <= 25 words — `long-quote` (`quote-words=30`).
6. every MD-shaped line that fails the exact grammar or `|`-cell count is a malformed-row
   finding — `malformed-row`, `spacing`, `quote-pipe`.
7. snapshot reuse cap 2 — `reuse-three` (`snapshot-reuse modprobe.d.5.scd=3`).
8. distinct sources >= 3 and distinct snapshots >= 3 are global target clauses; not separately
   witnessed here (`reuse-three` still holds 3 sources and 3 snapshots, so only clause 7 fires).
   The reader checks row count and id contiguity but not these two floors.

## Limits

- The reader is a locator/binder, not a semantic judge; reader-green is not a substitute for
  `met=1` and must never be reported as one.
- Only `--fixture` mode was exercised; the lane tree, git/jj state, `.ufo/state`, `.scratch`
  and package/service state were untouched. No tool installs; stdlib only; no `/tmp` writes.
- The fixture's statements are authored to satisfy the frozen grounding rule; they make no
  claim about the final corpus note's wording.

## Artifacts

`.ufo/waves/round-72/w1/E1Mirror/{counter-run.txt, reader.py, reader-runs.txt, build-mirror.py,
run-matrix.py, report.md}`; this file is the seat report.
