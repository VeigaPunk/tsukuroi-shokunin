2026-11-03T22:31:27Z

# C1Connector — sibling-overlap scan (round 68, w1)

Register: `.ufo/waves/round-68/drafts/c1/connector-overlap.md` (9 rows; the full command/rc ledger is there).

Chronicle:
1. Read the lane's ownership anchors (`PROVINCE.md:46-52` ADJ-01..07, `:121-130` OUT-001..010, `:137-146` digests).
2. Hashed mori's `PROVINCE.md` and reconciled the mismatch against the pinned blob at `91940fa339e3`.
3. Mapped the memory-controller surfaces of C1 (cgroup `memory.events`, `memory.events.local`, `oom_kill`,
   S149/S182 code) onto OUT-001, OUT-005 and ADJ-04; found the upstream-source surface unassigned.
4. Scanned sibling `tools/` for the C2 cross-check; found it in two souji tools, not in any `KNOWLEDGE-REF` file.
5. Scanned sibling registries/knowledge for the five C1 URLs and the v7.3 digests; found mori already
   registers the v7.3 bytes via cgit and has measured the raw route as unstable.

Results: `OVERLAP_ROWS=9 CONFLICTS=2 MORI_PROVINCE_SHA=2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838 MORI_MATCH=no SIBLING_KNOWLEDGE_HITS=0`

Two contradictions the L1 must see before landing:
- **OV-04/OV-05 (CONFLICTS).** mori's `round-53-verifier-spotcheck.md:136` votes `reject` on the
  `raw.githubusercontent…/v7.3/` route as a row locator ("it cannot be the stable locator of a row",
  HTTP 429 on 1 of 3 paths). C1 opens S286 and S287 as rows on exactly that route. The rows are payable —
  the L1's own fetch of 2026-11-03 pinned all eight files (`before/src/SHA256SUMS`) — but a throttled
  recheck would read as drift. Either name the pinned local bytes as the recheck, or carry the cgit
  locator alongside; the bytes are already in mori (`SOURCES.md:313` S533, `:319` S539).
- **OV-07 (AGREES, not novel).** The C2 check already exists fleet-wide: `souji-gate-check.py:14/128`
  (check5) and `souji-registry-agreement.py:9-10` (K1, revision-aware over committed blobs). The
  surviving delta is the header gate's fence/binding semantics, so C2 is lane-scoped novelty only.

`MORI_MATCH=no` is a locator-freshness finding, not an anchor failure: the blob at `91940fa339e3` hashes
to the OUT-001 digest `73abda79…`, mori's HEAD moved to `84c6cbc3` (423 insertions, 7 deletions on that
path), and both quoted clauses are still byte-identical at HEAD lines 8 and 9.

The memory-controller boundary for C1: byte and line identity may pass through in RW1/RW4; counter
semantics, dated-event classification and memcg-vs-global kill attribution are mori's under OUT-001 and
OUT-005. The `mm/oom_kill.c` code-reading surface has no anchor at all (OV-03, `NONE`) — unassigned, not free.
