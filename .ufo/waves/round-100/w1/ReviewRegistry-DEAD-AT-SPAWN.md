# ReviewRegistry — dead at spawn (L1 record, NOT a seat report)

This file is the lane's record of a seat that produced nothing. It is not a seat artifact and is not
credited as a read.

- Seat: `ReviewRegistry`, role `reviewer`, round 100 wave `w1` (attack seat).
- Dispatch: `.ufo/waves/round-100/w1.ready.dispatched` lists it with handle `ReviewRegistry-4` at
  2026-11-08T12:11:12.
- Result: `.ufo/waves/round-100/w1-results.json` carries its row with a **0-byte output**; no
  `w1/ReviewRegistry/` directory and no `w1/ReviewRegistry.md` exists.
- Orchestrator ruling (message to the L1, 2026-11-08): "ReviewRegistry is dead at spawn and has no
  report — record it as an unfiled seat in the round record; do not synthesise anything for it, and
  do not credit it."
- Consequence for the round: the C2 forgery battery was carried by the other attack seats
  (`CriticClaims` C2.1-C2.8, `MutInstruments` M1-M8, `SentinelHarm`, `ConnectorOverlap`), and the
  ledger row `C2  w1-results.json  neutral` records the absence. The seat was **not replaced** (a
  dead seat stays dead in the evidence).
