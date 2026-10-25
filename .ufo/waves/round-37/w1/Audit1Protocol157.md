# Audit1Protocol157 — round-37 w1 read-only audit: scorecard claim rules

- seat: Audit1Protocol157 (scribe, L2, tsukuroi lane round 37 attempt 1, wave w1)
- assignment (w1-spec.json item Audit1Protocol157): "Read-only audit item 1/4. Inspect one distinct contract surface: scorecard claim rules, SOURCES contract, assimilation package, quarantine slice, lessons/spot-check requirements. Record actionable evidence-based gaps and report in seat directory. No lane/fleet/source writes."
- surface inspected: **scorecard claim rules** (the other four surfaces are left to the sibling audit seats)
- milestone: Protocol/source audit · date: 2026-10-25 · HEAD inspected: `0e5f70fadba12bc9bbb9db564c2262c2c0194535` (only untracked `.ufo/waves/round-37/*` differ)
- bounds honored: read-only; no lane/fleet/source writes; no git/jj mutation; no pacman/host changes; no campaign tools run; no installs (tools used: read/grep/glob + read-only count shell).

## 1. Contract authority opened this round (local, path:line)

- `/home/vgpnk/Projects/shokunin/PROTOCOL.md:343-451` — Evidence standard, Gate standard, File contract (SCORECARD row, line 436: "Every score is a claim: it carries the counting command that produced it and the commit it was measured against"); "Claimed ≠ re-executed" (361-362); commits cited by hash (368).
- `/home/vgpnk/Projects/shokunin/AXES.md:25-83` — claim rules: 1–3 claims, one axis-move each, falsifiable before→after, causal separability, distinct axes, lowest-axis obligation, capability rows enter only with a demonstrated run, SCORECARD contract fields.
- `SCORECARD.md:1835-2041` — round-36 final; round-37 declaration (C1/C2/C3), pre-freeze C3 correction; three round-37 axes/capabilities table generations.
- `tools/check-self-assessment.py` (full read) — K01–K27 implementations, `evaluate()` lines 434-810.
- `.ufo/waves/round-37/before/c3-before.json`, `c3-before-exit.txt`; `after-c3-5124bf.json`, `after-c3-d06ced.json`, `after-c3-ee36f9.json`, `after-c3-0e5f70.json`.
- Independent count re-derivations at HEAD (read-only): notes=56, SKILL.md=3110 `wc -l`, pipe lines=839, lessons=49, corpus/README.md=269, SOURCES rows=199 (S001–S199).

## 2. Observed conformance (positive evidence)

- C3 before-state claim matches capture: at base `564db0b614` the checker reported `checked 27, mismatches 5, FAIL, exit 1` (c3-before.json; c3-before-exit.txt `exit=1`), mismatches exactly K07–K11 (stated 55/3009/784/46/256 vs observed 56/3110/839/49/269).
- C3 after-state claim holds at the measured tip: at HEAD `0e5f70f` the same command reports `checked 27, mismatches 0, PASS, exit 0` (after-c3-0e5f70.json). The frozen predicate (mismatches==0 && checked==27 && exit==0) is satisfied now.
- The five count cells I re-derived independently at HEAD all equal the operative round-37 table (56/3110/839/49/269); K13's census 105/105 selftest value is exercised inside the checker and reads 105 at every capture.
- C1/C2/C3 declarations each carry the AXES-mandated prose elements: falsifiable before→after, counting command, do-nothing control (C1 V7-at-base; C2 checker-on-uncorrected-note; C3 5-mismatch base), C1 kill rule + sensitivity conjuncts + freeze rule, and cross-claim separability (SCORECARD.md:1895-1934). No fabrication found in the claimed scope.
- Intermediate captures are honestly present (5124bf/d06ced/ee36f9), i.e. the correction sequence is recorded, not hidden.

## 3. Findings (actionable, evidence-based)

**F1 (medium, process/tooling) — duplicate "current" tables with identical headings; the checker's correctness rests on last-match order, not markers.** The round-37 section carries two `## Axes — current self-assessment (round 37)` tables (SCORECARD.md:1976, :2000) and three `## Capabilities` blocks (:1989, :2013, :2032) plus the partial K17 correction row (:2024). Supersession is stated only in body prose (e.g. :2002 "The preceding table is superseded"), never in the headings themselves; `check-self-assessment.py` selects by "last matching section/table" (find_section/pick_table, lines 452-489), so any reader or tool that takes the first `## Axes — current` match sees the older table with no machine-visible marker. Action: mark predecessor headings explicitly (e.g. append "(superseded by the table below)" or a `## Axes — superseded (round 37)` heading) so first-match readers cannot misread; keep one operative heading exact.

**F2 (low-medium, maintainability) — table prose is shaped to parser literalism, not the reverse.** The operative second axes table exists because the first table's phrasing ("3110 newline characters (`wc -l`)", "839 pipe-prefixed lines") does not match the checker's K08/K09 patterns (lines 592-608: requires `` `SKILL.md` N `wc -l` `` and "N table lines"), and the correction note itself admits "the self-assessment parser requires the literal count phrases shown here" (:2002). A harmless prose rephrase silently flips K08/K09 to mismatch with no semantic change. Action: either document the literal-phrase requirement in SKILL/README near the counting command, or widen the checker's patterns to the row's own counting styles (the checker already has multiple "counting styles" branches for case counts; K08/K09 could get the same tolerance).

**F3 (medium, consistency) — stale order-of-operations text contradicts the corrected C3.** The Order list still names "the change commit (probe V8, C2 corrections + checker, C3 ledger + checker, SOURCES rows, …)" (SCORECARD.md:1946). The pre-freeze correction withdrew the C3 ledger/checker ("the new ledger concept is deferred, not claimed or scored", :1970-1972). A future integrator reading the Order step could expect a ledger/checker that the claim no longer declares. Action: append a correction line to the Order paragraph (or mark the ledger phrase superseded) before the change commit is executed.

**F4 (low, robustness) — the 27-check population is fragile across intermediate states; only the final tip satisfies the predicate.** `after-c3-5124bf.json` is `CANNOT_EVALUATE` ("missing capability row sources-registry", checked 0); `after-c3-d06ced.json` had 2 mismatches; `after-c3-ee36f9.json` had 1 (K17: host-census-gate row states no case count). All three are legitimate intermediates, and only after-c3-0e5f70.json corresponds to the declared after-state — but the captures make plain that "checked 27" did not hold through the sequence, and K17's requirement (capability row must state the census case count) is what forced the third capability-table generation. Action: state in the C3 claim's evidence that the measured tip is the only predicate-evaluable revision (already implied by "measured round-37 branch-tip revision"); consider making the intermediate could-not-evaluate states explicit in the round lesson so they are not misread as tip measurements.

**F5 (scope note) — claim-*declaration* rules are prose-only; the checker covers tables/SHONEN, not declaration shape.** K01–K27 validate the axes/capabilities tables, census counters, and SHONEN boxes only. Nothing machine-checks that a declared claim carries a before→after, a counting command, a do-nothing control, a kill rule, separability, or the source-quote rules (AXES.md:25-38). For round 37 these elements are present in prose; the gap is that no regressor would catch a future declaration that omits one. Action: have the wave-2 falsify seats explicitly check declaration-shape (they already review claims), or add a minimal declaration-shape validator later; not required for this round.

## 4. Limits

- I did not execute `check-self-assessment.py`; evidence is the committed captures plus code reading plus my own read-only count re-derivations at HEAD. No external sources opened (none were needed). No subagent dispatch. No writes outside this seat file.
