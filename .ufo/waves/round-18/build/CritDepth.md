# CritDepth — C1 correction count: genuine depth move or superficial annotation?

Axes checked: falsifiability of the counting command, defect coverage, capture grounding, axis attribution.

## Surviving basis (what holds)

- Axis attribution is defensible: correction records in `corpus/knowledge/boot-chain-r17.md` are depth work under the lane's own admitted precedent — r13/r14/r15/r16 all claimed depth improved at 8→8(0) for statement/citation corrections (`SCORECARD.md:324,388,446,492`), and the r17 verifier admitted C1 depth despite defect 3 (`corpus/lessons/round-17-verifier-spotcheck.md:121`).
- The drafted set is semantically correct and covers defect 3: `drafts/NoticeBootCorrections.records.json` has 4 records (the ":40-42/:43-46" bullet split into CORR-02/03). Verified locally: capture line 59 names 12 packages vs note ":19" "13 named packages"; B:124 mtime 09:26:22 vs B:115 history copy 09:29:18; B:198-200 linux-lts digests equal B:182-184. Every `capture_quote` is a literal substring of its cited S051 line.
- Capture grounding is structurally enforced: `capture_quote` must be an exact substring at `capture_ref` and `baseline_quote` an exact baseline substring (gate contract in spec.json; mirrors `check-freshness-r17.py:64-65,186-259`).

## Counterexample (the defect)

**The gate cannot bind records to the routed defect; count green ≠ defect 3 resolved.** The `check-appended-notices.py` contract validates record *form* only (registry schema, baseline quote, heading novelty, capture substring, append-only). Nothing in it pins which baseline statements must be corrected. Consequence, concrete: had the scribe written CORR-01 with `now`: "plus 13 named packages (B:59, B:82)" — the same wrong count — the gate would still count it resolved, because `capture_quote` substring-ness cannot arbitrate 12 vs 13. That is the failure class QUALITY19 already names: "a passing structural count does not establish source agreement" (`corpus/QUALITY.md:26`). The claim "resolved correction records 0→3+ for closure defect3" (`SCORECARD.md:537`) is therefore falsifiable at record level but *not* at defect level: a registry omitting the 13→12 record entirely could still yield resolved_records≥3 if a fourth statement were noticed.

Impacted axes: depth (claim validity), calibration (count could certify an unrepaired defect).

## Smallest safe correction

1. Keep the generic gate as the form check; add a per-claim defect manifest (3 named defect-3 statements) and require every named item covered — i.e. resolved_records ≥ 3 *and* coverage 3/3 — not count alone.
2. Require the baseline run to emit item-named red findings (pattern already used: `check-source-scope-correction.py` red baseline names the old false universal, `SCORECARD.md:333-335`), not just NOTICE-MISSING.
3. Report verdict "improved" only after pairing each record's `now` text against the capture arithmetic — the current draft passes that audit by hand; make the pairing an explicit integrator checklist, not an implicit gate claim.

Note: append-only location of corrections is precedent-accepted (QUALITY23, `QUALITY.md:32`); not a defect. Residual reader-experience weakness (wrong ":19" stands until tail) is a known tradeoff, not rejectable.

## Follow-up (integrator response)

L1 accepted the defect-level concern and assigned MigBoot an optional `check-boot-chain.py --statement-corrections` mode: fixed four required R18-CORR ids, exact current propositions, capture arithmetic/hash and live-vs-history mtime checks, named unresolved findings and restored wrong-now fixtures. That design implements corrections 1–3 above; residual attack surface shifts to the landed implementation (does the red mode actually fail on each defect-3 statement and on a wrong `now`, not merely notice-missing). Wave-2 falsify should demand the restored-defect selftest cases exist and run red.

Scope: executed=none (read-only file/git reads only)
