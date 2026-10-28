
## Gate status — round 48 (the depth gate FAILED; GR2 stays pending)

Round 48 bound the rows through the seat-written channel of its one counted wave (`w2`): `tools/check-scrub-admission-r48.py`
(frozen at `ae99f021b76f8eb1c8805d32d80644464afb1ff6`) credited no seat on GR2's current bytes (section sha256
`e0b391e198f67ff57ce7971e2dd589faaa9390ebf2d2fd49dc6d103c163a52ce`). GR1 and GR3 stay pending too: the predicate needs all
three rows. No row is admitted this round; the marks are not written and the entry's GR2 narrowing is unread by any counted seat.
