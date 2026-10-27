VERDICT: draft

# C2-S8 — post-admission stale text review

## Axes

Depth and QUALITY 10 are the judged axes. This report scopes the stale-text risk if GR1–GR3 are admitted; it does not assert admission or a measured outcome.

## Counterexample and evidence

The strongest counterexample to treating this as a blanket rewrite is that admission is conditional and the 2026-10-27 task's frozen counter, not the proposed prose, decides whether the rows are admitted. Thus existing round-45 wording remains historically accurate; only current-use summaries/status need an append-only supersession notice, and only if the measured predicate admits all three rows.

- `corpus/knowledge/btrfs-scrub-grounding-r45.md:180-198` has `## Limits`, including that no seat has read the last narrowing, and `## Gate status — round 45 (the depth gate FAILED; rows pending)`. These accurately describe the old observation but become stale as current status if GR1–GR3 are admitted. Preserve them verbatim and append a round-46 status.
- `corpus/knowledge/btrfs-scrub-grounding-r45.md:200-207` records `verdicts_ok 0` and pending rows for the round-45 gate. This is historical and must not be rewritten; the proposed appended round-46 block must identify the measured revision and receipt.
- `SKILL.md:4424` registry row names `scrub-grounding-r45` and its a2w1/a2r1 bound-verdict measurement. The registry is a dated tool record, not itself the admission status; no replacement of that row is warranted. A new round-46 admission section should clarify the new counter result and leave the old row historical.
- `corpus/README.md:466` ends with the round-45 pending/not-admitted statement; if GR1–GR3 are admitted, that current-sounding statement is stale. The README also has no located round-45 coverage-map row for the grounding note (the top table lists entries through the early map; later round additions are append-only narrative). Grep: `grep -n 'btrfs-scrub-grounding-r45.md\|round 45\|FAILED\|pending, not admitted' corpus/README.md SKILL.md corpus/knowledge/btrfs-scrub-grounding-r45.md corpus/knowledge/btrfs-scrub-record-r44.md SCORECARD.md`.
- `corpus/knowledge/btrfs-scrub-record-r44.md:153-161` says round-44 failed and rows pending; this is historical and remains correct as round-44 history. The later `:163-173` stop-outcome qualification is independent and remains applicable; do not replace it.
- `SCORECARD.md:256` is a historical round-12 depth claim and is not the round-46 depth evidence cell. The inspected file’s round-46 declaration/axis evidence was not located in the bounded read; therefore do not infer its exact cell or propose editing the old round-12 row. Locate the applicable depth cell and append/qualify it only if it explicitly presents the round-45 pending state as current.

## Smallest safe append-only drafts (conditional on measured admission)

Place these only after the measured run establishes the admitted predicate. Replace both placeholders with actual values; do not publish a placeholder as evidence. `MEASURED_REVISION` is the exact revision scored. `COUNTER_RECEIPT` is the committed/retained receipt path that contains the observed counter output.

### Entry: `corpus/knowledge/btrfs-scrub-grounding-r45.md`

Append exactly:

```markdown
## Gate status — round 46 (GR1-GR3 admitted)

Append-only; the round-45 Limits and gate-status text above remains the historical account of that gate. On measured revision `MEASURED_REVISION`, `tools/check-scrub-admission-r46.py --revision MEASURED_REVISION` returned `r45_legs_ok=1 verdicts_ok=3 marks_ok=3` (receipt: `COUNTER_RECEIPT`). GR1–GR3 are admitted for this round by the frozen round-46 predicate; this does not certify claims beyond those rows or revise the round-45 measurement.
```

### SKILL.md

Append exactly:

```markdown
## Scrub grounding — round 46 admission

Append-only; `scrub-grounding-r45` remains the historical round-45 gate record. On measured revision `MEASURED_REVISION`, `python3 tools/check-scrub-admission-r46.py --revision MEASURED_REVISION` returned `r45_legs_ok=1 verdicts_ok=3 marks_ok=3` (receipt: `COUNTER_RECEIPT`). The counted GR1–GR3 verdicts are admitted for round 46; this records the scoped depth evidence and does not supersede the source limits or the independent round-44 history.
```

### `corpus/README.md`

Append exactly one line containing both required phrases:

```markdown
| `knowledge/btrfs-scrub-grounding-r45.md` | Round-45 GR1–GR3 rows admitted in round 46 by the counted verdict gate; measured revision `MEASURED_REVISION`, counter receipt `COUNTER_RECEIPT` | S246–S249; `tools/check-scrub-admission-r46.py` |
```

The line is a deliberately narrow map pointer; append it at the appropriate round-46 coverage-map location without rewriting earlier rows. If the counter output differs from the exact predicate/output above, do not use these drafts or claim admission; report the actual result instead.
