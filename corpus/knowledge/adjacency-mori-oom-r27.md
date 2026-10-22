# Overlap register with mori's userspace OOM killer entry — round 27

source: mori-shokunin `corpus/knowledge/userspace-oom-killers-r26.md` at commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` (sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`, snapshot `.ufo/waves/round-27/siblings/mori/corpus/knowledge/userspace-oom-killers-r26.md`)
recheck: when mori lands a new revision of that entry (mori HEAD was `0becc421` while this was drafted, with reworded F8 and decision-table rows)
verified-at: 2026-10-22 (mori pin ef9dbee1 and lane revision 75784ea4; mori HEAD df886be1 observed in the wave-2 corrections below)
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

## Wave-2 corrections (round 27, attempt 2, appended 2026-10-22)

One in-place edit, disclosed here: a `verified-at:` header line was inserted (QUALITY 8; wave-2 CritTrendVerdicts). Otherwise append-only; the same items are in the JSON companion under `corrections_r27_a2`.

- OV6: the sibling quote starts on pinned snapshot line 198, not 196 (196 is the low-memory row). The row still counts because the counter accepts the quote anywhere in `quote_line` to `quote_line + 2` (wave-2 ConnMoriHeadDrift).
- What the register is: only OV1 and OV2 replay a mori pointer into this lane; OV3 to OV6 classify topical overlaps. `anchored_rows` counts anchors that resolve against the pinned snapshot and the lane; it does not test the class, the owner, or that the lane side is the file mori names. Wave-2 CritC2Tool and MutC2Counter built register mutants that the pinned counter still scores 6 (an extra OV7 row, a lane quote taken from this register or from `.ufo/`, six `LANE-GAP` rows, one-character quotes). The live rows use none of these shapes (CritC2Tool, "Live rows"); class and owner rest on the row reviews RevRowOV1 to RevRowOV6.
- Sibling availability: the declaration says a sibling checkout without the pinned commit reports `sibling-unavailable` and still counts. The pinned counter scores 0 with exit 1 when a mori repository lacks `ef9dbee1`, and 6 when no mori repository exists. The count needs a mori checkout that holds `ef9dbee1`, as this host's does (wave-2 CritClaimSizingFinal).
- Mori HEAD, observed 2026-10-22: `df886be1`; the entry blob there is `94efb7cf…`, unchanged since mori `79ecf58`, so the `0becc421` named in the header and under "Also observed" is the same bytes.
- Inbound work found at mori HEAD, outside the six rows and not absorbed: mori `SKILL.md:345` points at this lane's `PROVINCE.md:19`, which is now line 28; mori's round-27 work says this lane's "+200 band scanned first" reading (`oom-event-plane.md:116,349`, `kill-event-deep-r8.md:147,260`) is false and answers the lane's open question Q12. These are recorded for a later round of this lane; the items for mori are listed in the round-27 report.
