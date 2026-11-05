# ExecAnchor — round 82, C1 depth (executor)

Scope: `corpus/knowledge/mount-unit-fstab-plane-r81.json` (lines only) and `.md`
(table anchors, new Coordinate convention section, Limits bullet). Nothing else
was written in the lane. Counter, snapshot, SOURCES.md, SCORECARD.md untouched.

## Located spans (counter's own `strip_view` + `locate`) and rewrites

Pinned snapshot: `.ufo/waves/round-81/before/src/systemd.mount.xml`
sha256 `afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394`, 707 raw lines, 707 strip lines.

| row | old lines | new lines |
|---|---|---|
| MT1 | [133, 137] | [135, 138] |
| MT2 | [498, 503] | [502, 503] |
| MT3 | [481, 487] | [486, 487] |
| MT4 | [489, 491] | [491, 492] |
| MT5 | [229, 241] | [234, 236] |
| MT6 | [335, 347] | [339, 341] |
| MT7 | [194, 212] | [198, 201] |
| MT8 | [254, 265] | [259, 260] |

Every old range was a container of the quote, not the quote span. All eight quotes
located, none refused. Each new span was checked by eye against the raw file
(e.g. MT1 raw 135-138 "automatically gain an After= ... among nofail"; MT7 raw
198-201 "Configures a Requires= ... unit"). Round-81 numbers were shifted two lines early,
as the declaration said.

Not changed: any `quote`, `statement`, `setting`, `source`, `snapshot`, or top-level field;
the `measured` sub-objects (S332 coordinates into `host/generator.txt`, not the snapshot).

## Counter output (frozen `tools/check-anchor-coordinates.py`)

Selftest (`--selftest`, run from the scratch dir), verbatim tail:
```
  ok   cited-range-malformed: rc=1 count=0/1 unmet
SELFTEST total=12 passed=12 failed=0
rc=0
```

Fixture run, `--fixture /fast/scratch/hyaku/tsukuroi-r82/ExecAnchor/lane`, verbatim:
```
{"claim": "C1", "revision": null, "count": 8, "target": 8, "finding": "met", "rows": [{"id": "MT1", "cited": [135, 138], "located": [135, 138], "exact": true, "why": "ok"}, {"id": "MT2", "cited": [502, 503], "located": [502, 503], "exact": true, "why": "ok"}, {"id": "MT3", "cited": [486, 487], "located": [486, 487], "exact": true, "why": "ok"}, {"id": "MT4", "cited": [491, 492], "located": [491, 492], "exact": true, "why": "ok"}, {"id": "MT5", "cited": [234, 236], "located": [234, 236], "exact": true, "why": "ok"}, {"id": "MT6", "cited": [339, 341], "located": [339, 341], "exact": true, "why": "ok"}, {"id": "MT7", "cited": [198, 201], "located": [198, 201], "exact": true, "why": "ok"}, {"id": "MT8", "cited": [259, 260], "located": [259, 260], "exact": true, "why": "ok"}]}
rc=0
```
Note: the counter emits JSON, not the literal line `count 8 / target 8 / met`; the
JSON carries the same count/target/finding. Exit 0.

Not run: `--revision <REV>` (the lane commit is the L1's to make; I did not commit).

## Markdown changes

- Decision table `source` column: MT1 :135-138, MT2 :502-503, MT3 :486-487, MT4 :491-492,
  MT5 :234-236, MT6 :339-341, MT7 :198-201, MT8 :259-260 (old ranges replaced).
- New `## Coordinate convention` section after the table: raw line numbers of the pinned
  `systemd.mount.xml` at v262, SHA256 `afbf3be6…2394`, line-preserving strip,
  round-81 numbers were tag-stripped and ran two lines early, round 82 re-anchors.
- Limits bullet "Line anchors": rewritten to state the raw-line convention and name
  round 82 as superseding round 81's coordinates. The old "a reader using sed adds 2"
  sentence is removed, since it is now false.

## Statements checked against raw source (no contradiction found)

- MT5 (raw 234-236 + nofail sentence 239-243): "configures a Before=/After= ... nofail ... re-acquires" consistent.
- MT7 (raw 198-201, 212-214): "always applies to the created mount unit regardless of automount" consistent.
- MT1, MT4, MT8 prose versus raw 135-138, 491-492, 259-260: consistent.
- I did not audit every prose claim in the md (the "What this host does" section cites S332
  generator.txt, not the snapshot). Not in C1's predicate; untouched.

## Refused / left alone

- Did not touch any `measured` block, the host section, or the recheck line (it names
  `tools/count-mount-rows-r81.py`, a round-81 instrument, which I did not re-verify).
- Did not commit, stage, or run any git mutation.

## Tools

No tools installed or upgraded. Only python3 (system) and coreutils were used.

## Scratch

`/fast/scratch/hyaku/tsukuroi-r82/ExecAnchor/` removed before yield (see final yield).
