status: complete
verdict: four C1 index/doc drafts delivered (SKILL decision table T1-T6, SKILL registry rows for `count-ul-rows-r73` and `check-r72-routed-r73`, PROVINCE Frontier->Core note, corpus/README round-73 index); the wave-1 note draft scores `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0 met=1` against the frozen counter in a private fixture tree and against the lane working tree with the hardened counter; four findings reported, the blocking one being that both instruments moved inside wave 1 (`count-ul-rows-r73` `542f9c…` -> `84501ab8…`, `check-r72-routed-r73` `93f034e3…` -> `316dd51a…` -> `328a6bf6…`, uncommitted, one checker state failing its own CONTROL), so registry digests must be re-read from the committed blobs.

# SC3Index — index/doc deltas for C1 (round 73, w1)

Seat: L2 index/doc (scribe role, leaf). Item: draft the SKILL decision table, the SKILL registry
continuation rows, the PROVINCE Frontier -> Core paragraph and the corpus/README round-73 index section.

No lane write beyond this wave directory and the report. The only host interaction was read-only
`systemctl show` / `is-enabled` / `list-unit-files` / `systemd-analyze unit-paths` / `readlink` / `stat`
probes; no unit was started, stopped, masked, unmasked, enabled, disabled or edited, and no instrument was
modified in the lane.

Drafts live beside this report: `deltas.md` (all four in labelled fenced blocks, plus the landing
checklist and the findings) and one file per target so the L1 can paste without touching the fences.
