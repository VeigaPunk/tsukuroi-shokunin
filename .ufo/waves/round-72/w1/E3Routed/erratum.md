## Round 71 — receipt erratum (append-only; closes R71-C1-UNRECEIPTED-RUN)

The round-71 C1 outcome header was written without a receipt of the counting run, so
the note's six verified MP rows rested on a number nobody could re-derive from the
record. This block is that receipt; it is appended, not spliced into the measured
outcome, and it names one revision for both the row count and the receipt.

- receipt: `.ufo/waves/round-71/after/count-mp-rows-final.txt`
- record revision: `2b358d2d` (`2b358d2d229f79411a3f6a5c883b31f92e1de789`)
- re-derivation: `python3 tools/count-mp-rows-r71.py --revision 2b358d2d`, rc 0, prints
  `MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0` and
  `MP_TARGET rows=6 verified=6 sources>=4 snapshots>=4 max_reuse=2 met=1` — the two
  summary lines in the receipt byte for byte, with the six `MP_ROW ok` lines above them.
- checker: `python3 tools/check-r71-routed-r72.py` reads the receipt, this block and the
  note correction below as one freshness claim; the C1 outcome header keeps its own
  revisions (`2959254a` note, `2b358d2d` tally) and is not rewritten.
