# Overlap register with mori's userspace OOM killer entry — round 27

source: mori-shokunin `corpus/knowledge/userspace-oom-killers-r26.md` at commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` (sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`, snapshot `.ufo/waves/round-27/siblings/mori/corpus/knowledge/userspace-oom-killers-r26.md`)
recheck: when mori lands a new revision of that entry (mori HEAD was `0becc421` while this was drafted, with reworded F8 and decision-table rows)
companion: `corpus/knowledge/adjacency-mori-oom-r27.json` holds the anchors; a correction is appended to both files.

## What this register does

It replays mori's pointers into this lane and classifies each place where the two lanes' entries meet, with an owner and an action. It reports; it never copies mori's facts into this lane. Counted by `python3 tools/check-adjacency-overlap.py --revision <REV>` (field `anchored_rows`); the counter checks that anchors resolve and the vocabulary is used, not that a class is the right judgement. The classes rest on wave-1 connector ConnMoriInbound (per-pointer replay, `.ufo/waves/round-27/w1/ConnMoriInbound.md`) and critic CritAdjacencyMove.

| id | mori anchor (snapshot line, heading) | lane side | class | owner | action |
|---|---|---|---|---|---|
| OV1 | 143, Facts (F8 unit list) | `memory-pressure-r25.md` 204-206 | INBOUND-RESOLVES | tsukuroi | record only |
| OV2 | 153, Facts (pointer to the lane PROVINCE row) | `PROVINCE.md` 32 | INBOUND-DRIFTED | mori | report: mori re-pins `PROVINCE.md:66` |
| OV3 | 146, Facts (meaning of `auto`) | `memory-pressure-r25.md` 201-202 | AGREES | tsukuroi | record; mori HEAD adds the ancestor clause |
| OV4 | 145, Facts (nothing monitored even if started) | `memory-pressure-r25.md` 390 | CONFLICTS | tsukuroi | report to mori; the lane's SKILL MP4 row and JSON MP4 still carry the unqualified headline (lane debt) |
| OV5 | 128, Facts (no delegation in earlyoom 1.9.0) | `memory-pressure-r25.md` 382 | CONFLICTS | mori | lane notice appended pointing at mori's F7; report mori's r12 entry contradiction |
| OV6 | 196, Decision table (oomd accounting attributes) | none | LANE-GAP | mori | do not absorb; cite mori when needed |

## Also observed, not counted

- Mori HEAD's new source row S133 teaches that systemd-oomd monitors only cgroups of units set to `kill`; the lane's `memory-pressure-r25.md` line 387 says units with `OOMRules=` are also monitored. Observed at mori HEAD `0becc421` (mori round 27 in flight); not in the pinned snapshot, so not a row. Reported to mori (wave-1 ConnSiblingOverlap).
- Mori's S125 and this lane's S125 are different source rows; any citation must say which lane's id it means.
