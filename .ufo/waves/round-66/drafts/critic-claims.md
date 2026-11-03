2026-11-03T21:05:35Z

# CLAIMS-FALSIFY — K1Critic (round 66, wave w1)

Critic seat. Report only; no frozen predicate amended, no tracked file edited.
Inputs read: SCORECARD.md "Round 66 — declaration" (:4902-4917), fleet AXES.md
(`/home/vgpnk/Projects/shokunin/AXES.md`, 83 lines — see R1: the lane has no AXES.md),
SCORECARD.md "Axes — current self-assessment (round 65 final measured surface)" (:4851-4864).

## R0. Standing receipt — the lane has no AXES.md; the axis definitions live at the fleet root

```
$ grep -n 'Working the axes' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/AXES.md
grep: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/AXES.md: No such file or directory (os error 2)
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -e HEAD:AXES.md; echo rc=$?
fatal: path 'AXES.md' does not exist in 'HEAD'
rc=128
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --oneline --all -- AXES.md
(no output)
$ wc -l /home/vgpnk/Projects/shokunin/AXES.md
83 /home/vgpnk/Projects/shokunin/AXES.md
```
The item's step 1 ("AXES.md ... at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin") is
BLOCKED as written; the file is at the fleet root and was read there. The lane's own
round-28 record quotes the same file's operative sentence (`.ufo/waves/round-28/w1/RevC1Declaration.md:24`):
"At least one claim works the lane's lowest-scoring non-retired axis"; claims must be causally
separable, name distinct axes, 1–3 per round." Fleet HEAD AXES.md carries that text at
"## Working the axes" and the axis table at "## The six axes":
- depth — "Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources"; signal: "A reader can act on SKILL.md alone; no filler".
- adjacency — "Cross-domain awareness — evidence belonging to another domain reported, not absorbed"; signal: "Lane reports name contested scope; integrator arbitrates".
- freshness — "Drift detection — skill claims re-verified against live surfaces; stale items flagged or fixed".

## C1 — depth claim (`corpus/knowledge/systemd262-credentials-boot-policy-r66.md`, S283)

### Attack 1 — is the counter a depth counter or a row-count counter?
The counted predicates are `grep -c '^| CB' <note>` ≥ 5, SOURCES ≥ 283 (S283 directly after
S282, NF 13, Gate quote ≤ 25 words), census validate, knowledge-header PASS. `grep -c '^| CB'`
grades row presence, not depth: AXES.md depth = decision tables with real thresholds, named
error signatures, cited sources. Five shallow rows meet the count. This is exactly the
round-30 rejection class:
```
$ grep -n 'sourceless fixture' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md | head -3
1185:... its depth counter could not fail on depth: a sourceless fixture reached its target
(corpus/lessons/round-30-verifier-spotcheck.md, section 2, C1). ...
1250:... a content-free or post-data shortcut met a counter (depth twice, adjacency once) ...
```
### Attack 2 — does the named fixture meet the frozen counter, and does the header check catch it?
Named sourceless fixture: a note whose body is exactly 5 lines starting `| CB` and nothing else
— no `source:`, no `verified-at:`, no `recheck:`.
- `grep -c '^| CB'` → 5: meets the count (shape only).
- SOURCES ≥ 283: independent of the note (S283 lives in `corpus/SOURCES.md`); meets it.
- census validate: reads SOURCES.md, not the note; meets it.
- knowledge-header: **fails it.** `tools/check-knowledge-header.py` requires all three header
  lines outside fences (docstring :5-13; `KEYS = ("source", "verified-at", "recheck")` :56;
  `RULES = {"source": None, "verified-at": date_problem, "recheck": cadence_problem}` :202):
```
$ grep -n 'missing-source' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-knowledge-header.py
408:        case("missing-source-verified-at", ... FAIL, {MISSING}, {MISSING: "source:"}, {"finding_count": 2, "complete_count": 0})
412:        case("missing-source", ... FAIL, {MISSING}, {MISSING: "source:"}, {"finding_count": 1})
```
So the fully sourceless fixture (the r30 class) is caught by the frozen counting set — the
claim is not r30-blind. **Named limit:** the header gate checks shape, not truth: its `source:`
rule is `None` (no value validation) and its selftest passes a note citing `source: S999.`
(:414-417 builds `source: S999.` fixtures; no logic in the tool references `corpus/SOURCES.md` —
grep over the file shows none). No named gate binds the note's `source:` id to S283 or binds
note text to the pinned bytes: `check-section-citations.py` is the narrow round-16/S050 errata
gate (docstring :1-13); `check-registry-coverage.py` binds the SKILL.md gate registry to tools,
not notes to sources. A fixture with `source: S999.` + five well-formed CB rows therefore
passes every frozen counting command; "sourced" is carried by the sha256-pinned-bytes receipt
and per-host-value receipts, not by the counter.
### Attack 3 — kill-rule reachability (honest path)
Kill rule: "the option absent from the pinned bytes, or a measured input contradicting the
documented semantics → the note states what was measured and the claim stops honestly (no
verdict is softened)". Reachable: the pinned bytes are grep-able once the sha256
(`008e1265…`) is re-verified; every host input is no-sudo readable on this host —
`systemd-creds has-tpm2` is on the seat allow-list, `/proc/cmdline` is world-readable,
`bootctl status` (partial ok) names SecureBoot state. The failure shape is honest-fail, not
pad. Reachable.

### Verdict C1 — STANDS-WITH-NAMED-LIMIT
The claim is a genuine depth move in content (sourced decision table + host-measured inputs +
named falsifier) and its counter set does catch the sourceless fixture via the header gate.
Limit, recorded not fatal: the counter cannot distinguish a truthfully-sourced note from a
header-decorated one (`source:` value unvalidated, note↔S283 binding unenforced by any named
gate); the sourcing burden rests entirely on receipts.

## C2 — adjacency claim (`adjacency-recheck-r66.md` 10-row live locator table + overlap table + erratum)

### Attack 1 — false provenance in the cited ceiling (defect in the frozen framing text)
The declaration reads: "ceiling read from `AXES.md`: "no formal overlap table"".
No AXES.md revision contains that text:
```
$ grep -n 'overlap\|ceiling' /home/vgpnk/Projects/shokunin/AXES.md
33:claim. At least one claim works the lane's **lowest-scoring non-retired axis**,
70:recorded in `SCORECARD.md`), the lowest-axis obligation is waived: the round
$ for r in 609ecb6e 84bade03 e867f786; do git -C /home/vgpnk/Projects/shokunin grep -c 'overlap' $r -- AXES.md; done
(no output for any revision — no match in fleet HEAD or any historical blob)
```
"No formal overlap table" is the lane's own **round-11** ceiling (`SCORECARD.md:52`), superseded
since round 25 — every later axes row states the opposite:
```
$ sed -n '836p' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md   (same text at 951, 983, 1034, 1097, 1140, 1181, 1246, 1295, 1484, ...)
| adjacency | 8 | ... `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to
ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership
anchors OUT-001 to OUT-010) ... Ceiling: recipient acknowledgement and independently replayed
handoffs are not verified. | ...
```
The recorded, operative adjacency ceiling is **recipient acknowledgement / independent replay**,
which the lane itself has repeatedly ruled not lane-producible (`SCORECARD.md:2282-2283`: "a
sibling acknowledgement cannot be produced by this lane; adjacency stays unclaimed and is not
harmed"; likewise :2642-2643, :2740). The frozen predicate cells are unaffected (they count
rows and an erratum, never ceiling text), so the claim is not void — but the round must not be
recorded as closing a "no formal overlap table" ceiling that closed at fleet round 1 / round 19.
### Attack 2 — adjacency move or freshness/operability count?
- **For adjacency:** AXES.md adjacency = "evidence belonging to another domain reported, not
  absorbed." The credential-plane overlap table (ADJ-02/ADJ-06/ADJ-04 boundaries,
  connector-scanned) classifies which sibling owns which part of a new plane — exactly
  reported-not-absorbed, and the lane's own idiom: recent rounds record boundary restatements
  in new notes as the adjacency evidence of the round ("round-63 ADJ-04 restatement in the new
  note, ordinal unchanged", `SCORECARD.md:4686`; same shape :4585, :4770, :4864). The 10-row
  live-locator table also strengthens awareness: reading ten siblings' live HEADs is more
  current cross-domain knowledge than the round-19 pins alone.
- **Against (freshness/operability count):** the frozen counter counts only the 10 AR-row
  re-locations and `## Erratum (round 66)` count 1. Re-locating already-reported r19 anchor
  quotes at live HEADs is re-verification — freshness's own definition ("skill claims
  re-verified against live surfaces; stale items flagged or fixed") applied to sibling pins —
  and the lane has already measured exactly this class without an ordinal move:
```
$ sed -n '3234p' .../SCORECARD.md   (round 50)
... C3 measured 9/9 pinned quotes/digests and 9/9 live-tip quotes ... | adjacency ordinal remains 8; no new surface claimed |
$ sed -n '3377p' .../SCORECARD.md   (round 51)
... quote_at_pin_ok 9, live_quote_ok 9, stub_fails 1, ... recipient_ok 7 ... | adjacency unchanged (8); the routed round-51 defect ... is closed |
```
  The erratum is a stale-pin repair (freshness idiom: "stale items flagged or fixed"). The
  genuinely adjacency-shaped content — the overlap table — has **no counting command** in the
  frozen predicate; under AXES.md an uncountable-but-real improvement must be declared
  exploratory (named non-author reviewer, at most one per round) to carry admission weight. As
  declared (a measured claim), the claim's verification weight sits on the recheck count, which
  is a freshness/operability-graded re-verification. And the true recorded ceiling (recipient
  acknowledgement) is untouched by every cell of the claim.
### Attack 3 — kill-rule reachability (honest path)
Kill rule: "a sibling HEAD unreadable or a quote unlocated → that row is not `located` and the
count is below 10 → the claim stays unverified (never padded, never re-pinned to a convenient
quote)". Reachable and honest-fail: siblings sit at the fleet root (`mori-shokunin` et al.),
`git -C <sibling> rev-parse HEAD` is a read; a drift yields a non-located row and the claim
fails rather than pads. Precedent says 10/10 is empirically plausible (round-19 anchors held
8/8 in-range with 3 pin drifts; r50/r51 live_quote_ok 9/9).
**Named limits:** (a) the counter validates row shape only — `| located |` is a literal in the
frozen grep; nothing machine-checks the cell's truth, and `check-adjacency-anchors.py` does not
read the r66 table (`DEFAULT_REGISTRY`/`DEFAULT_KNOWLEDGE` are the r19 paths, `tools/check-adjacency-anchors.py:24-26`;
grep for `recheck-r66` in the tool: no hits), so `located` is self-attested unless each row
carries a receipt; (b) the erratum's append-only property has no named prefix gate in the claim
— the anchors gate re-reads `adjacency-anchors-r19.md` (278 lines, `wc -l`), so the erratum
must land as an EOF append that duplicates no anchor-bearing heading, or a no-harm regression
lands with it (the r44-45 IN-109 class). Both limits are disclosure obligations, not blockers.

### Verdict C2 — STANDS-WITH-NAMED-LIMIT
Admissible as declared on its own cells; it is a hybrid whose counted half is a
freshness/operability-graded re-verification and whose adjacency-shaped half (overlap table)
is uncounted. It does not touch the operative ceiling (recipient acknowledgement), so it
carries no ordinal weight. The ceiling misattribution to AXES.md is a false-provenance defect
to be recorded by the L1; the frozen predicate itself stands.

## Ordinals (item step 5)

```
$ sed -n '4851,4864p' .../SCORECARD.md   ("Axes — current self-assessment (round 65 final measured surface)")
| depth | 8 | 82 notes ...; the sourced systemd v262 applicability plane SY1-SY5 landed round 65 ... | round 4; round-65 entry added, ordinal unchanged |
| adjacency | 8 | the C1 note restates the ADJ-06 ... and ADJ-04 ... boundaries ...; contested kaidoku/revenger ownership remains unruled. | fleet round 1; round-65 boundary restatement, ordinal unchanged |
```
Confirmed: depth 8, adjacency 8, tied lowest; both r66 claims sit on the tied-lowest axes, so
the lowest-axis duty ("at least one claim works the lane's lowest-scoring non-retired axis")
is satisfied. The honest ordinal change from either claim is **8 → 8 (0)**, and neither claim
preclaims a transition. Precedent binds:
- depth: `SCORECARD.md:962` — "C1 adds one sourced entry with six rows on new ground, which the
  round-25 depth row's ceiling (ordinal last moved at round 4) does not by itself lift; an
  uplift would need a separate measured claim."
- adjacency: `SCORECARD.md:1045` — "Adjacency stays 8: C2 records overlap sites ... not
  acknowledged"; r50/r51 live-tip legs left it 8 (:3234, :3377).
No claim, as frozen, justifies any ordinal move; recording 8→9 on either axis would be an
opinion, not a measurement.

## Summary of verdicts

| Claim | Verdict | Decisive evidence |
|---|---|---|
| C1 depth | STANDS-WITH-NAMED-LIMIT | knowledge-header FAILs the fully sourceless fixture (check-knowledge-header.py :408-417); limit: `source:` value unvalidated, note↔S283 binding enforced by no named gate |
| C2 adjacency | STANDS-WITH-NAMED-LIMIT | ceiling "no formal overlap table" exists in no AXES.md revision and is the superseded r11 ceiling (SCORECARD:52 vs :836 et seq.); counted half is live re-verification (r50/r51 precedent, ordinal 8); overlap table uncounted |
| Ordinals | both 8 → 8 (0) | SCORECARD:4851-4864 (r65 surface); :962, :1045, :3234, :3377 precedents; no claim preclaims a transition |
