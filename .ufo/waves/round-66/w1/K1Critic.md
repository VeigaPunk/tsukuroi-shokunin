2026-11-03T21:05:35Z

# K1Critic — CLAIMS-FALSIFY report (round 66 w1)

Scope: falsify claims C1 and C2 of the frozen "Round 66 — declaration" (SCORECARD.md:4902-4917).
Full per-claim attacks with receipts: `.ufo/waves/round-66/drafts/critic-claims.md`.
Report only; no frozen predicate amended; no tracked file edited; no scratch residue.

## Verdicts

- **C1 (depth): STANDS-WITH-NAMED-LIMIT.** The r30-class sourceless fixture (5 `| CB` rows, no
  header) is caught: `tools/check-knowledge-header.py` requires `source:`/`verified-at:`/`recheck:`
  and its selftest fails `missing-source` with finding_count 1 (:408-417). Named limit: the gate
  validates header shape, not citation truth (`RULES` source rule is `None`; a `source: S999.`
  fixture passes), and no named gate binds the note to S283 — census validates SOURCES.md rows,
  check-section-citations is the narrow r16/S050 gate, check-registry-coverage binds SKILL.md to
  tools. Sourcing is carried by receipts, not by the counter. Kill rule reachable by the honest
  path (pinned bytes re-verifiable by sha256; all host inputs no-sudo: `systemd-creds has-tpm2`
  allow-listed, `/proc/cmdline`, `bootctl status`); failure shape is honest-stop.
- **C2 (adjacency): STANDS-WITH-NAMED-LIMIT, with a false-provenance defect in its framing.**
  The cited ceiling "no formal overlap table" appears in **no** AXES.md revision (fleet HEAD and
  blobs 609ecb6e/84bade03/e867f786: zero `overlap` matches) — it is the lane's superseded
  round-11 ceiling (SCORECARD.md:52). Since round 25 the operative row reads "formal overlap
  table present … Ceiling: recipient acknowledgement and independently replayed handoffs are not
  verified" (:836 et seq.), a ceiling the lane itself rules not lane-producible (:2282-2283).
  Axis placement: the counted half (10 live-located r19 anchor quotes + erratum 1) is
  re-verification — freshness/operability-graded; r50/r51 already measured live-tip quote
  location (`live_quote_ok 9/9`) with adjacency unchanged at 8 (:3234, :3377). The
  adjacency-shaped half (credential-plane overlap table, ADJ-02/06/04) has no counting command;
  as a measured claim it can only be evidence, not the counted deliverable. Kill rule reachable:
  an unreadable sibling HEAD or unlocated quote must leave the row non-`located`, count < 10,
  claim unverified — the rule forbids padding. Named limits: `located` is a self-attested cell
  (the anchors gate does not read `adjacency-recheck-r66.md`; its defaults are the r19 paths,
  check-adjacency-anchors.py:24-26), and the erratum's append-only property has no named prefix
  gate — it must land as an EOF append of the 278-line `adjacency-anchors-r19.md` duplicating no
  anchor-bearing heading, or the anchors gate regresses (r44-45 IN-109 class).
- **Ordinals:** r65 surface confirms depth 8, adjacency 8, tied lowest (SCORECARD.md:4851-4864);
  both claims sit on the tied-lowest axes, satisfying the lowest-axis duty. Honest change from
  either claim: **8 → 8 (0)**; no claim preclaims a transition. Precedent binds: a sourced entry
  does not lift depth 8 without a separate measured claim (:962); overlap/live-tip adjacency
  work left 8 (:1045, :3234, :3377). Recording any 8→9 would be an opinion, not a measurement.

## Smallest safe corrections for the L1 (not applied by this seat)

1. Record in the round lesson that C2's ceiling quote is misattributed to `AXES.md` (the text
   exists only at SCORECARD.md:52, superseded since r25); rest C2's admission on its frozen
   cells (10/10 located, erratum 1, anchors gate PASS) with adjacency 8→8.
2. Require per-row receipts for each `located` cell (the counter is shape-only) and an
   EOF-append check for the erratum (no duplicate heading in the anchors knowledge file).

## Key receipts (commands + outputs in drafts/critic-claims.md)

- Lane AXES.md absent: `cat-file -e HEAD:AXES.md` rc 128; fleet `/home/vgpnk/Projects/shokunin/AXES.md`
  = 83 lines, axis table + "Working the axes" read there.
- `grep -c 'overlap'` on every historical fleet AXES.md blob: no match.
- Both claim files absent at HEAD: `cat-file -e` rc 128 each (honest before-state).
- `sed -n '204p' corpus/knowledge/adjacency-anchors-r19.md | grep -c 2277` → 1;
  register `found_line.*2822` → 1; `PROVINCE.md` `^| OUT` rows → 10; file is 278 lines.
