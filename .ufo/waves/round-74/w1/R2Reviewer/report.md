# R2Reviewer — round-74 w1 (tsukuroi, hyaku run 15) — C2 routed-repair + instrument-digest attacks

Seat: R2Reviewer (reviewer, L2). Scope: attack the C2 repair drafts against the frozen instrument
`tools/check-r73-routed-r74.py` and verify the instrument-digest claim. Declaration `e51fb49d`,
base `d749a625`. No repo bytes mutated; all fixtures live under `fixtures/` in this seat dir; the
20-case mutant battery runs through `evaluate(fixture_texts=...)` (in-process, no git) and the two
decisive shapes were re-run through the real CLI with `--repo <fixture-dir>`.

Baseline (honest open state): at tip `810daf13` and at the declaration commit `e51fb49d` the
checker reads `ROUTED_STALE=2 ROUTED_OK=0/2`, rc 1 — item 1 "section absent in lesson", item 2
"missing token '14' in LOG.md correction block body". At base `d749a625` both files are absent
(stale 2). This matches the L1's pre-data control `.ufo/waves/round-74/before/absence-controls.txt`.
The repairs have not landed yet; everything below is about whether the planned landing can land.

## Findings (by severity)

### HIGH-1 — The spot-check's prescribed repair shape (append a headed correction at EOF) can never close item 2
`check_r73_log_count` (tools/check-r73-routed-r74.py:62-70) selects the **first** block matching
`"R73-LOG-COUNT-STALE" in b or ("Round 73" in b and "correction" in b.lower() and "selftest" in b)`.
LOG.md's **last** block — `## Round 73 (2026-11-03) — the systemd unit-load merge plane, and three
r72 routed repairs` — already matches the fallback clause ("Round 73" in the heading; body carries
"appended correction" and "twelfth selftest") and lacks the token `14`. A correction block appended
at EOF sits **after** it in iteration order and is never evaluated.

- Spot-check §6.2 (`corpus/lessons/round-73-verifier-spotcheck.md:164-168`) prescribes exactly this
  shape: "the append-only LOG has no correction entry. **Append one** naming the superseded counts."
- Receipt (CLI, real bytes): `fixtures/cli-g1-append-eof/` (LOG sha256 prefix `a583f42e14540e61`,
  tip bytes + perfect headed correction block at EOF, lesson repaired) → `ROUTED_STALE=1
  ROUTED_OK=1/2`, rc 1, "missing token '14'". Battery case G1 agrees (stale=1).
- The only passing shapes are non-append: (G2) headed block **inserted immediately before** the
  Round 73 entry heading — CLI `fixtures/cli-g2-insert-before/` (LOG sha256 prefix
  `b88105778fda2731`) → `ROUTED_STALE=0 ROUTED_OK=2/2` rc 0;
  or (G3) the correction appended as an **unheaded paragraph inside** the Round 73 entry block
  (battery G3: 0/2 ok).
- Consequence: an executor who follows the routed-defect text lands bytes that still read
  `ROUTED_STALE=1`, and the frozen C2 target (`ROUTED_STALE=0 ROUTED_OK=2/2`, rc 0) is unreachable
  by the prescribed shape. Lane options: use the G3 or G2 shape, or amend the instrument (last-match
  or id-priority selection) — an instrument change, which under the round-73 rule (R73-INSTRUMENT-
  MIDWAVE) needs its erratum written **before** the repair commit.

### MEDIUM-2 — Item 2 passes without naming R73-LOG-COUNT-STALE
C2's frozen wording requires the LOG correction "naming R73-LOG-COUNT-STALE". The fallback clause
("Round 73" + "correction" + "selftest") accepts a block that never carries the id: battery G4
(id-less heading `## Round 73 — correction (selftest counts)`, inserted before the R73 entry) →
0/2 PASS. Instrument is weaker than the claim text.

### MEDIUM-3 — Bare-substring token matching (both items)
`req not in body` is plain substring membership. L5 passes with **wrong numbers**:
`install.c:23831`, superseding `12387`, anchors `:368-3700`, `:237-2380`, `:238-2390`. G5 passes
with the final counts written as the single token `1314` (satisfies both `13` and `14`). The r73
checker's own repaired bar (R73-CHECKER-LEXICAL: whole-token matching) did not carry into the r74
instrument.

### MEDIUM-4 — No direction, supersession-verb, or instrument-attribution check
- L6 denial-inversion passes: a block saying the correction is REJECTED and the original anchors
  stand, containing all five required tokens as the *rejected* claims, reads `ok`.
- G6 direction inversion passes: "the final committed counts are 12 and 11; the mid-wave figures 13
  and 14 were wrong and stand superseded" → 0/2 PASS.
- G10 misattribution passes: the block attributes the final 13/14 cases to the **round-74**
  instruments (`tools/count-uf-rows-r74.py`, `tools/check-r73-routed-r74.py`) → PASS. The counts
  are never bound to tool names or to the digests `1f22c26b…`/`ad853877…`; the instrument-digest
  claim is only held by prose elsewhere (SCORECARD.md:6039-6040, corpus/README.md:685-686, lesson
  `## Correction 2`), not by this checker.

### MEDIUM-5 — First-match shadowing can falsify item 1 the same way
L8: a block that merely *mentions* the id earlier in the lesson (e.g. a tracking line in `## Gate`)
makes a later, valid, EOF-appended correction FAIL (stale=1, "missing token 'install.c:2383'").
Today no lesson block mentions the id, so EOF append works (L0 control: 0/2) — but any seat that
references the defect id above the correction poisons it. Same first-match fragility as HIGH-1.

### LOW-6 — Placement/appendedness and sentence-ness unenforced (item 1)
L7: id + all five tokens inside the unrelated `## Gate` section pass with **no correction block at
all** (0/2). L10: a bare comma-separated token list with no sentence passes — the exact vacuity
class (r73 F1/F6) the round-73 wave named and fixed for the r73 checker.

### Negative results (attacks that correctly fail — the omission semantics hold)
- L1 lesson draft omitting `install.c:2383` → FAIL (missing token).
- L2 draft omitting the superseded `2387` → FAIL (the claim's "superseding 2387" is enforced as a
  token, if only lexically).
- L3/L4 drafts omitting the S304 anchors (`:238-239`, or all three) → FAIL.
- G7 LOG draft omitting superseded 12/11 (words accepted: "twelfth"/"eleven") → FAIL.
- G8 LOG draft omitting finals 13/14 → FAIL (this is the live tip failure mode).
- Absent files/blocks → stale (selftest CONTROL/MISSING cases pass; 6-case selftest rc 0).

## Instrument-digest claim — VERIFIED (holds)
- `tools/count-ul-rows-r73.py` = `1f22c26b95c52be745a8cdd97ec52ebf06a362f697daf2a8e1e0d77e28f3e643`
  (tip = declaration `e51fb49d`), `--selftest` **PASS (13 cases)** rc 0 under a fresh `mktemp -d`
  TMPDIR. Under `TMPDIR=/tmp` it correctly refuses (SELFTEST-HERMETIC, rc 2) — by design, receipt
  `selftest-counter.txt`.
- `tools/check-r72-routed-r73.py` = `ad853877bd4d5117d0ee356f346f3bf515c0b064fd1e9ed8bc670ac97295a281`
  (tip = declaration), `--selftest` **PASS (14 cases)** rc 0 — receipt `selftest-checker.txt`.
- Claimed digests match committed bytes at SCORECARD.md:6039-6040 and corpus/README.md:685-686.
- Both round-74 instruments are byte-frozen mid-wave: `check-r73-routed-r74.py` `2da4ff1f…` and
  `count-uf-rows-r74.py` `94d46a5e…`, identical at tip and declaration.

## Named limit (recorded, not new)
The instrument is lexical: it cannot entail that `install.c:2383`/the corrected anchors match the
pinned v262 snapshots, and L6/G6 show it accepts text that contradicts the repairs. That layer
stays with the reviewer, consistent with the r73 "denial leg" record. What IS new: the r74
instrument sits strictly **below** the r73 checker's own lexical bar (no whole-token, no verb, no
direction), and its item-2 selection makes the prescribed append shape unpassable.

## Receipts
- `battery.py`, `battery-out.txt` — 20 mutants, 0 mismatches vs the checker's actual behavior.
- `fixtures/cli-g1-append-eof/` — ROUTED_STALE=1 rc 1 (prescribed shape fails).
- `fixtures/cli-g2-insert-before/` — ROUTED_STALE=0 ROUTED_OK=2/2 rc 0 (only non-append shape passes).
- `selftest-counter.txt` (TMPDIR=/tmp refusal, rc 2), `selftest-checker.txt` (14 cases PASS rc 0);
  counter 13-case PASS run printed in-session under `mktemp -d` TMPDIR.
- Fixture LOG digests (truncated to 16 hex): g1 `a583f42e14540e61`, g2 `b88105778fda2731`.

## Recommendation to the lane
1. Land the LOG correction as an **unheaded paragraph appended inside the Round 73 entry block**
   (G3; pure append, no reordering, passes) or as a headed block **inserted immediately before**
   the `## Round 73 (2026-11-03)` heading (G2). Never a headed block at EOF.
2. Append the lesson correction anywhere at EOF (works today); do not mention
   `R73-GATE-QUOTE-LINE-DRIFT` in any earlier section, or the correction must precede that mention.
3. If the lane wants headed-at-EOF append (closest to the routed text), amend the checker first and
   write the instrument erratum before the repair commit (R73-INSTRUMENT-MIDWAVE rule).
4. Consider the regressed lexical bar (whole-token, verb, direction, count↔instrument binding) for
   a same-instrument hardening before closure, with the erratum discipline above.

## Verification gaps
- C1 counter mutants are out of seat scope (other seats hold that axis).
- No live re-open of the v262 snapshots here; the spot-check's measurements stand unchallenged.
- Whether lane protocol tolerates the G2 insertion (out of chronological order) vs G3 (unheaded)
  is the L1's call; both are proven to pass the frozen bytes.
