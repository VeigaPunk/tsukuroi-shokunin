source: own-work row S0NN — pointer census `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json` (schema tsukuroi-adjacency-pointers-r19-v1; lane_tip 452a054677f6b18284917d7c08c45361f91c25ac; counts inbound 114, outbound 10); own-work rows S0NN (×8) — sibling `PROVINCE.md` snapshots `.ufo/waves/round-19/l1-capture/siblings/<lane>/<commit12>/PROVINCE.md` for kama/e75cf680b534, kagi/c2cab35bc92e, mado/a4046a821608, mori/91940fa339e3, kumitate/1770305fae20, kaidoku/d1d981d2cc04, revenger/cf02419276e5, tameshi/01d586ddbc5f; lane `PROVINCE.md` ADJ-01..07 table (lines 35-52) and handoff checklist (lines 54-68).
verified-at: 2026-10-20 lane 452a054
recheck: 30d; procedure: `python3 tools/check-adjacency-anchors.py --revision <REV>`, where `<REV>` is a landed lane commit resolved under corpus/QUALITY.md criterion 27; re-read each sibling declaration before any later handoff.

# Adjacency anchors — round 19

## 1. Scope and counted claims

Two directions, one gate. Outbound: the ten sibling ownership pointers in
`PROVINCE.md` (line-range only) gain portable anchors: exact heading, exact
quote of at most 25 words, pinned sibling commit and blob sha256. Inbound: the
114 sibling-file pointers into tsukuroi files in the census are classified
RESOLVES, DRIFTED or UNRESOLVABLE against the current lane tip.

Counted sets, named so each count can be re-derived (corpus/QUALITY.md
criterion 30):

- outbound_portable 0 → 10 counts exactly census `outbound[]` records OUT-001..OUT-010.
- inbound_classified 0 → 114 counts exactly census `inbound[]` records IN-001..IN-114.

A count is a count of records that pass the gate. It is not a semantic proof
that each sibling sentence is correct.

## 2. Method

Outbound (per OUT record):

1. Open the snapshot path named by the census record.
2. Find the Markdown heading whose section holds the cited ownership text.
3. Choose an exact single-line quote of at most 25 words inside that section.
4. Record the 1-based snapshot line of the quote.
5. Confirm that the census `sibling_commit` and `sibling_blob_sha256` match the snapshot bytes.
6. Record whether the quote lies inside the cited range.

The heading plus quote is the locator. Line numbers are supplementary and are
valid only against the named snapshot.

Inbound (per IN record):

1. Read the current lane file at the record's `target_path`.
2. Locate the content the sibling sentence relies on by an exact quote.
3. Classify RESOLVES if `found_line` falls inside the record's target ranges.
4. Classify DRIFTED if the content exists at another line.
5. Classify UNRESOLVABLE if the content is absent. State the bounded search, for example `grep -nF '<quote>' <target_path>`, and its result.
6. Set `scope` to `operative` when `sibling_path` does not start with `.ufo/`, otherwise `historical`.

## 3. Scope limits

- Classification is relative to the current lane tip 452a054, not to the revision the sibling cited. A RESOLVES result says nothing about the sibling's pinned view of tsukuroi.
- Historical pointers (`sibling_path` under `.ufo/`) are dated records. They are classified and retained. They never become owner handoffs.
- Only operative DRIFTED or UNRESOLVABLE rows become owner handoffs (§4).
- Tsukuroi never edits sibling files. Siblings are read-only. A handoff is a report to the owner.
- A pointer is not proof of ownership. The cited text supplies ownership; a digest match is drift evidence only (as in `adjacency-handoffs-fleet-r1.md`).
- This entry is repository evidence only. It runs no host probe and no package, boot, service or configuration action.

## 4. Owner-handoff packet format

Each operative drift becomes one packet with:

- the ADJ row (ADJ-01..ADJ-07) selected by the question being asked, not by the binary or service name (`PROVINCE.md` lines 44-52);
- the IN id, sibling, `sibling_path`, pinned commit, `target_path`, cited range and `found_line`;
- the minimum evidence fields of that ADJ row (`PROVINCE.md` lines 46-52, last column);
- one question for the owner, with no instruction to change a sibling file.

Closure states follow the handoff checklist (`PROVINCE.md` lines 65-68):
`prepared`, `reported`, `acknowledged`, `accepted`, `resolved`.

- A new packet starts at `prepared`.
- It becomes `reported` only when the fleet report names the recipient.
- `acknowledged`, `accepted` and `resolved` need recipient-side durable evidence. None is claimed by this entry.
- Acknowledgement is not acceptance. Resolution requires owner-side closure evidence.

Packets for this round are listed below the inbound table by the L1 integrator.

## 5. Records

### Outbound anchors

<<OUTBOUND-TABLE>>

### Inbound classification

<<INBOUND-TABLE>>

## 6. Recheck and bounded sweeps

- Gate: `python3 tools/check-adjacency-anchors.py --revision <REV>`. This seat has not run it.
- Pointer census (negative claim: exactly ten sibling-file pointers in the lane `PROVINCE.md`): `grep -nE '\.\./[a-z0-9-]+-shokunin/[^ )|]*\.md' PROVINCE.md`. Observed 2026-10-20 at the lane working tree: matches on lines 33, 46, 47, 48, 49, 50 (two), 51 (two) and 52, which is ten. Scope: `PROVINCE.md` only.
- No portable section yet (negative claim): `grep -n '^## Adjacent — portable' PROVINCE.md`. Observed 2026-10-20: no match. Scope: `PROVINCE.md` only.

## QUALITY check

Performed on this frame's bytes at authoring, 2026-10-20. Author-side only.
Not independent verification. It admits nothing. Instance-level checks wait
for the L1-filled tables and the gate run.

1. Falsifiable: an outbound row fails when its quote is absent at `quote_line` or when the commit or blob hash differs. An inbound row fails when `found_line` lies outside the cited range or the quote is absent. Gate run pending.
2. Source: every claim cites census record ids, snapshot paths, or lane `PROVINCE.md` lines named above.
3. Separation: census fields and the two grep results are observations. The RESOLVES, DRIFTED and UNRESOLVABLE labels are inferences against the tip. Whether a pinned sibling commit still contains its text is `[unk]` until the snapshot is checked.
4. Errata append-only: the line-range table in `PROVINCE.md` is retained. Corrections go in appended blocks.
5. Rejection kept: DRIFTED and UNRESOLVABLE rows stay in the inbound table. None is silently dropped.
7. External claims: none in this frame, and no `corpus/SOURCES.md` S### row is cited. Not applicable.
9. Negative claims: the two claims in §6 each carry the bounded search command, its scope and date. The rule that siblings are not edited is a scope rule, not a measured negative, and no sibling-state negative is asserted.
21. Portable locators: met by design. Each anchor is a heading, an exact quote of at most 25 words, a pinned commit and a blob sha256. Line numbers are supplementary. Per-row verification waits for the gate.
30. Whole-proposition counts: met by design. The 10 and 114 counts name their finite sets (OUT-001..OUT-010; IN-001..IN-114). Plural statements cite each record. Counts stay `[unk]` until gate output is recorded.
