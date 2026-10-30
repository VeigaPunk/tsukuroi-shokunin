VERDICT: draft

## Before → after measurements

Axes: C1 depth, C2 operability, C3 adjacency; this scribe is judged on calibration and report.
Provenance: `.ufo/waves/round-52/frozen/FROZEN.md:3-8,28-35`; before measurement revision `cc88b81d78bcbe06bce3f6bf722a108432ad276f`; freeze `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`.
Commands below are counting-command templates, not executions by this scribe. `<REV>` must name the final integrated revision; C2 `<DIR>` must be undisturbed scratch.

### C1 — depth
Counting command: `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r52.py --revision <REV>`.
BEFORE: `structural_ok=1; lint_ok=3; quotes_ok=3; verdicts_ok=0; seats_ok=0; marks_ok=0; verdict=FAIL` (`.ufo/waves/round-52/before/c1-at-base.json:1`; recorded exit status `.ufo/waves/round-52/before/c1-at-base.rc:1` is `1`).
AFTER: PENDING w1 — final re-run decides all six legs and verdict; counted 18-seat cohort decides bound row verdicts, and L1 alone adds admission marks after three clean counted rows (`.ufo/waves/round-52/frozen/FROZEN.md:28,37-45`).
Target: `structural_ok=1; lint_ok=3; quotes_ok=3; verdicts_ok=3; seats_ok=18; marks_ok=3`.

### C2 — operability (instrument-measurement completion)
Counting command: `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-counter-cheats-r51.py --revision <REV> --scratch <DIR>`.
BEFORE: no valid measurement receipt; frozen declaration says the round-51 attempt has ERROR rows and was graded `unprovable`. Numeric before legs `real_pass`, `cheats`, `cheats_rejected`, `r50_cheats_rejected` are not supplied by `before/*.json`; do not replace missing evidence with zero (`.ufo/waves/round-52/frozen/FROZEN.md:11-12,29`).
AFTER: PENDING w1 — final scorer receipt must report `real_pass=1; cheats=5; cheats_rejected=5; r50_cheats_rejected=0`, without ERROR rows or disturbed scratch.
Its measured bytes are the counters and controls, not a change to the census, PROVINCE.md or the registry (`.ufo/waves/round-52/frozen/FROZEN.md:32-35`).

### C3 — adjacency (instrument-measurement completion)
Counting command: `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-table-r51.py --revision <REV>`.
BEFORE: `verdict=PASS; mode=measurement; checker_rev_bytes=1` at `cc88b81d78bcbe06bce3f6bf722a108432ad276f` (`.ufo/waves/round-52/before/c3-at-base-r52.json:1`; recorded exit status `.ufo/waves/round-52/before/c3-at-base-r52.rc:1` is `0`).
Exact predicate legs from that receipt:
- `adj_rows=7; linked_rows=7; bare_ranges=0; anchors_ok=7; registry_ok=7; anchors_checker_rc=0`.
- `quote_at_pin_ok=9; live_quote_ok=9; stub_fails=1; display_bound_ok=10; quote_specific_ok=10`.
- `display_forge_fails=1; override_blocked=1; digests_bound_ok=10; r50_blind=1; anchor_rows_exact=1`.
- `adj_exact=1; bare_all=0; ancestry_ok=10; recipient_ok=7`.
AFTER: PENDING w1 — remeasure the complete leg set at ONE named integrated revision, retaining the frozen predicate (including `live_quote_ok >= 8`) and requiring a green battery (`.ufo/waves/round-52/frozen/FROZEN.md:30,52-68`).
Its measured bytes are the counters and controls, not a change to the census, PROVINCE.md or the registry (`.ufo/waves/round-52/frozen/FROZEN.md:32-35`).

### Gates, limits and touched surfaces
Pre-data K-pass fixtures establish counter capability, not claim measurements; no cohort outcome or final rerun is credited here (`.ufo/waves/round-52/frozen/FROZEN.md:69-70`).
Only this report is the deliverable; no product files, admission marks, fixtures, judges or commits were modified. No product runtime, counting command, selftest or battery was run by this scribe; Python was used only to extract existing receipt fields.
Other before receipts are not substitutes for C1–C3: registry coverage records PASS with 88/88 tools registered and zero findings (`.ufo/waves/round-52/before/registry-coverage-at-base.json:1`); self-assessment records FAIL, 27 checked and 3 mismatches (`.ufo/waves/round-52/before/self-assessment-at-base.json:2-6`).
Observed provenance check: `git show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:tools/<tool> | sha256sum` matched FROZEN-hashes.txt for `check-scrub-admission-r52.py` (`bd5563af…`), `score-counter-cheats-r51.py` (`96ad3ad5…`) and `check-adjacency-table-r51.py` (`cfe3ee23…`). This is not a claim rerun.
Findings: C1 before fails admission; C2 has no valid before measurement; C3 already passes before, so its claimed completion is a named-revision measurement plus green controls, not an asserted numerical improvement.
Artifact: `.ufo/waves/round-52/w1/R52ScribeBefore.md`.
